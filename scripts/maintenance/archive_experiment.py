"""Package manifest-indexed primary evidence without deleting local checkpoints."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def archive(directory):
    directory = directory.resolve(strict=True)
    manifest_path = directory / 'study_manifest.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    artifacts = manifest['artifacts']
    actual = {p.relative_to(directory).as_posix() for p in (directory / 'primary').rglob('*') if p.is_file()}
    if actual != set(artifacts):
        raise ValueError('Primary files differ from the manifest; archive refused')
    paths = sorted([*artifacts, 'study_manifest.json',
                    *(p.relative_to(directory).as_posix() for p in (directory / 'config').rglob('*') if p.is_file())])
    target = directory / 'evidence.zip'
    temporary = directory / 'evidence.zip.tmp'
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name in paths:
                relative = PurePosixPath(name)
                source = (directory / name).resolve(strict=True)
                if relative.is_absolute() or '..' in relative.parts or not source.is_relative_to(directory):
                    raise ValueError('Unsafe archive path')
                data = source.read_bytes()
                if name in artifacts and sha256(data) != artifacts[name]:
                    raise ValueError(f'Checkpoint checksum mismatch: {name}')
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, data, compresslevel=9)
        with zipfile.ZipFile(temporary) as bundle:
            if bundle.testzip() is not None or set(bundle.namelist()) != set(paths):
                raise ValueError('Archive verification failed')
            for name, checksum in artifacts.items():
                if sha256(bundle.read(name)) != checksum:
                    raise ValueError(f'Archived checksum mismatch: {name}')
            if bundle.read('study_manifest.json') != manifest_bytes:
                raise ValueError('Archived manifest changed')
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    metadata = {'archive': target.name, 'sha256': sha256(target.read_bytes()),
                'bytes': target.stat().st_size, 'entries': len(paths), 'primary_records': len(artifacts),
                'manifest_sha256': sha256(manifest_bytes), 'verification': 'CRC and all primary SHA-256 passed',
                'checkpoints_deleted': False}
    (directory / 'evidence_archive.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    print(json.dumps(archive(parser.parse_args().directory), indent=2))
