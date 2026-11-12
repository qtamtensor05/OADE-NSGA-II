"""Pack, verify or restore maintained CSV evidence using only Python's stdlib."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'results/csv_archives.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def catalog(root=ROOT):
    path = root / 'results/csv_archives.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'archives': []}


def safe_path(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
        raise ValueError(f'Unsafe archive path: {name}')
    target = (root / name).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes destination: {name}')
    return target


def archive_lookup(root=ROOT):
    return {f['path']: a['archive'] for a in catalog(root)['archives'] for f in a['files']}


def verify(root=ROOT, restore=False):
    count = 0
    for record in catalog(root)['archives']:
        archive = safe_path(root, record['archive'])
        if digest(archive.read_bytes()) != record['sha256']:
            raise ValueError(f'ZIP checksum mismatch: {archive}')
        with zipfile.ZipFile(archive) as bundle:
            expected = {f['member'] for f in record['files']}
            if len(bundle.namelist()) != len(expected) or set(bundle.namelist()) != expected or bundle.testzip():
                raise ValueError(f'ZIP entries/CRC mismatch: {archive}')
            for item in record['files']:
                target = safe_path(root, item['path'])
                member_target = safe_path(archive.parent, item['member'])
                if member_target != target or target.suffix != '.csv':
                    raise ValueError(f'Invalid CSV destination: {item}')
                data = bundle.read(item['member'])
                if len(data) != item['bytes'] or digest(data) != item['sha256']:
                    raise ValueError(f'CSV checksum mismatch: {item["path"]}')
                if restore:
                    if target.exists() and target.read_bytes() != data:
                        raise ValueError(f'Local CSV differs; will not overwrite: {target}')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        target.write_bytes(data)
                count += 1
    return count


def pack():
    tracked = subprocess.check_output(['git', 'ls-files', '-z', 'results'], cwd=ROOT).decode('utf-8').split('\0')
    paths = {p for p in tracked if p.endswith('.csv')}
    paths.update(archive_lookup())
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'results/by_problem').rglob('*.csv'))
    groups = {}
    for name in sorted(paths):
        source = safe_path(ROOT, name)
        if not source.is_file():
            raise FileNotFoundError(f'Restore CSVs before packing: {name}')
        parts = source.relative_to(ROOT).parts
        folder = source.parent
        # by_problem/<family>/<problem>/csv_results.zip includes every study.
        if len(parts) >= 6 and parts[1] == 'by_problem':
            folder = ROOT.joinpath(*parts[:4])
        groups.setdefault(folder / 'csv_results.zip', []).append(source)
    entries = []
    for archive, sources in sorted(groups.items()):
        temporary = archive.with_suffix('.zip.tmp')
        files = []
        try:
            with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
                for source in sources:
                    data = source.read_bytes()
                    member = source.relative_to(archive.parent).as_posix()
                    info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    bundle.writestr(info, data, compresslevel=9)
                    files.append({'path': source.relative_to(ROOT).as_posix(), 'member': member,
                                  'bytes': len(data), 'sha256': digest(data)})
            with zipfile.ZipFile(temporary) as bundle:
                assert bundle.testzip() is None
                for item in files:
                    assert digest(bundle.read(item['member'])) == item['sha256']
            temporary.replace(archive)
        finally:
            temporary.unlink(missing_ok=True)
        entries.append({'archive': archive.relative_to(ROOT).as_posix(), 'sha256': digest(archive.read_bytes()),
                        'bytes': archive.stat().st_size, 'files': files})
    CATALOG.write_text(json.dumps({'schema': 1, 'archives': entries}, indent=2) + '\n', encoding='utf-8')
    write_index(entries)
    rewrite_csv_links()
    return verify()


def rewrite_csv_links():
    lookup = archive_lookup()
    documents = [ROOT / 'README.md', ROOT / 'README.vi.md',
                 *(ROOT / 'docs').rglob('*.md'), *(ROOT / 'results').rglob('*.md')]
    for document in documents:
        text = document.read_text(encoding='utf-8')
        def replace(match):
            label, target = match.groups()
            if target.startswith(('http:', 'https:', 'mailto:', '#')):
                return match.group(0)
            resolved = (document.parent / target.split('#', 1)[0]).resolve()
            if not resolved.is_relative_to(ROOT):
                return match.group(0)
            archive = lookup.get(resolved.relative_to(ROOT).as_posix())
            if not archive:
                return match.group(0)
            relative = os.path.relpath(ROOT / archive, document.parent).replace('\\', '/')
            return f'[{label} (ZIP)]({relative})'
        updated = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace, text)
        if updated != text:
            document.write_text(updated, encoding='utf-8')


def write_index(entries):
    raw_bytes = sum(f['bytes'] for a in entries for f in a['files'])
    packed_bytes = sum(a['bytes'] for a in entries)
    lines = ['# Tải dữ liệu CSV kết quả', '',
             'CSV được lưu trong ZIP; báo cáo Markdown và hình vẫn xem trực tiếp. Tải riêng ZIP bên dưới rồi giải nén ngay cạnh ZIP để có đúng cấu trúc thư mục cũ.', '',
             f'Tổng: **{sum(len(a["files"]) for a in entries)} CSV**, **{len(entries)} ZIP**, từ **{raw_bytes / 1048576:.2f} MiB** xuống **{packed_bytes / 1048576:.2f} MiB**.', '',
             '## Khôi phục sau khi clone', '', 'Chạy từ thư mục gốc dự án, chỉ cần Python chuẩn:', '',
             '```powershell', 'python scripts/csv_archives.py restore', '```', '',
             'Lệnh kiểm tra SHA-256 của ZIP và từng CSV, rồi khôi phục về đường dẫn cũ. Không ghi đè CSV cục bộ có nội dung khác. CSV đã giải nén được Git bỏ qua; ZIP là bản được commit.', '',
             'Chạy lệnh restore trước khi chạy phân tích, vẽ hình, inventory hoặc kiểm thử cần dữ liệu. Lệnh organize_by_problem tự khôi phục các CSV còn thiếu.', '',
             '## Kiểm tra và cập nhật', '', '```powershell', 'python scripts/csv_archives.py verify',
             'python scripts/organize_by_problem.py', 'python scripts/csv_archives.py pack', '```', '',
             'Pack gom các CSV đã có trong catalog, CSV đang được Git theo dõi và các bản tách trong by_problem. Để đưa nguồn CSV mới ở nơi khác vào gói, dùng `git add -f đường/dẫn.csv`, chạy pack rồi bỏ CSV đó khỏi index bằng `git rm --cached -- đường/dẫn.csv` trước khi commit ZIP. Không commit đồng thời ZIP và CSV rời.', '',
             'Catalog [csv_archives.json](csv_archives.json) lưu tên thành viên, đường dẫn phục hồi, kích thước và SHA-256. Manifest theo bài toán vẫn mô tả CSV sau giải nén. Việc nén không thay đổi dữ liệu hay provenance của các lượt chạy.', '',
             '| Bộ dữ liệu / bài toán | Tải ZIP | CSV | MiB |', '|---|---|---:|---:|']
    for a in entries:
        relative = Path(a['archive']).relative_to('results').as_posix()
        lines.append(f'| {Path(relative).parent.as_posix()} | [csv_results.zip]({relative}) | {len(a["files"])} | {a["bytes"] / 1048576:.2f} |')
    (ROOT / 'results/CSV_DOWNLOADS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['pack', 'verify', 'restore'])
    args = parser.parse_args()
    count = pack() if args.action == 'pack' else verify(restore=args.action == 'restore')
    print(f'{args.action}: {count} CSV files verified.')
