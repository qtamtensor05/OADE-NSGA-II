"""Generate standalone Vietnamese reports from each problem's filtered evidence."""
import csv
from pathlib import Path

TITLES = {
    'benchmark_classic': 'Benchmark 7 thuật toán — classic',
    'benchmark_adaptive': 'Benchmark 7 thuật toán — adaptive',
    'restart_confirmation': 'Xác nhận restart classic/adaptive/no-restart',
    'ablation_classic': 'Ablation OADE classic',
    'sensitivity_classic': 'Độ nhạy tham số classic',
    'sensitivity_adaptive': 'Độ nhạy tham số adaptive OFAT',
    'benchmark_dtlz': 'Benchmark DTLZ',
    'benchmark_wfg_m2': 'Benchmark WFG M=2',
    'benchmark_wfg_scaling': 'Benchmark WFG mở rộng số mục tiêu',
    'sensitivity_dtlz': 'Độ nhạy tham số DTLZ',
}
TABLES = {
    'algorithm_benchmark_igd_hv_summary.csv': ('Chất lượng và chi phí', ['algorithm', 'runs_total', 'runs_valid', 'IGD_mean', 'IGD_std', 'HV_mean', 'HV_std', 'runtime_mean', 'n_eval_mean']),
    'algorithm_benchmark_paired_statistics.csv': ('Kiểm định ghép cặp đã lưu', ['metric', 'reference_algorithm', 'comparison_algorithm', 'n_pairs', 'p_adjusted_holm', 'rank_biserial_effect', 'result']),
    'summary.csv': ('Đáp ứng tham số: median và IQR', ['parameter', 'level', 'baseline_level', 'runs', 'valid_runs', 'IGD_median', 'IGD_q25', 'IGD_q75', 'HV_median', 'HV_q25', 'HV_q75', 'restart_completed']),
    'comparisons.csv': ('Thay đổi so với baseline', ['parameter', 'level', 'baseline_level', 'metric', 'n_pairs', 'baseline_median', 'level_median', 'percent_change', 'direction']),
    'sensitivity_summary.csv': ('Đáp ứng tham số classic', ['study', 'parameter_label', 'runs', 'IGD_mean', 'IGD_std', 'HV_mean', 'HV_std', 'runtime_mean', 'restart_count_mean']),
    'sensitivity_statistics.csv': ('Kiểm định độ nhạy đã lưu', ['study', 'metric', 'test', 'baseline_label', 'comparison_label', 'p_value', 'p_adjusted_holm', 'result']),
}


def read(path):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def display(value):
    try:
        return f'{float(value):.7g}'
    except (ValueError, TypeError):
        return str(value).replace('|', '\\|').replace('\n', ' ')


def table(rows, columns):
    columns = [c for c in columns if c in rows[0]]
    return ['| ' + ' | '.join(columns) + ' |',
            '| ' + ' | '.join('---' for _ in columns) + ' |',
            *['| ' + ' | '.join(display(r[c]) for c in columns) + ' |' for r in rows], '']


def generate_reports(base, family, problem, records, reports, link):
    folder = base / 'reports'
    folder.mkdir(exist_ok=True)
    index = [f'# Báo cáo riêng {problem.upper()}', '',
             'Mỗi báo cáo chỉ chứa kết quả của bài toán này. IGD thấp hơn và HV cao hơn là tốt hơn. Runtime tính bằng giây.', '']
    for category in dict.fromkeys(r['category'] for r in records):
        data = base / category
        lines = [f'# {problem.upper()} — {TITLES[category]}', '',
                 '## Phạm vi', '',
                 f'Chỉ gồm dữ liệu `problem={problem}` trong đợt `{category}`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.', '']
        lines += ['CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.', '']
        raw = read(data / 'algorithm_benchmark_raw_runs.csv') or read(data / 'raw_runs.csv') or read(data / 'sensitivity_raw_runs.csv')
        if raw:
            seeds = sorted({int(r['seed']) for r in raw if r.get('seed', '')})
            invalid = sum(r.get('valid', 'true').lower() not in ('true', '1') for r in raw)
            lines += [f'Có **{len(raw)} dòng raw**, **{len(seeds)} seed** ({min(seeds)}–{max(seeds)}), **{invalid} dòng không hợp lệ** theo cột valid đã lưu.', '']
            conditions = sorted({(r.get('n_var', ''), r.get('n_obj', ''), r.get('evaluation_budget', '')) for r in raw})
            lines += ['Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: ' + '; '.join(f'`{c}`' for c in conditions) + '. Trường trống là thông tin không được lưu ở nguồn.', '']
        if category in ('benchmark_classic', 'benchmark_adaptive'):
            lines += ['Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.', '']
        if category == 'restart_confirmation':
            lines += ['OADE_FULL là classic; OADE_ADAPTIVE_RESTART là adaptive; OADE_NO_RESTART tắt restart. Seed xác nhận là 1000–1029. Telemetry trigger không được lưu: chất lượng cuối không tự xác nhận cơ chế kích hoạt restart.', '']
        if category == 'ablation_classic':
            lines += ['Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.', '']
        if category.startswith('sensitivity'):
            lines += ['Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.', '']
        for filename, (title, columns) in TABLES.items():
            rows = read(data / filename)
            if rows:
                lines += [f'## {title}', ''] + table(rows, columns)
                if filename == 'algorithm_benchmark_igd_hv_summary.csv':
                    valid = [r for r in rows if int(r['runs_valid']) > 0]
                    if valid:
                        igd = min(valid, key=lambda r: float(r['IGD_mean']))
                        hv = max(valid, key=lambda r: float(r['HV_mean']))
                        lines += [f'Theo trung bình mô tả, IGD thấp nhất: **{igd["algorithm"]}**; HV cao nhất: **{hv["algorithm"]}**. Xếp theo trung bình không thay thế kiểm định.', '']
        lines += ['## Giới hạn diễn giải', '',
                  'P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.', '',
                  '## Dữ liệu và truy vết', '']
        for record in records:
            if record['category'] == category:
                lines.append(f'- [{Path(record["output"]).name}]({link(folder, record["output"])}) ({record["rows"]} dòng)')
        lines += ['', 'SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).', '', 'Giao thức và báo cáo toàn đợt:', '']
        lines += [f'- [{Path(p).name}]({link(folder, p)})' for p in reports if (base.parents[3] / p).exists()]
        lines += ['', '[Danh mục báo cáo của bài toán](README.md)', '']
        (folder / f'{category}.md').write_text('\n'.join(lines), encoding='utf-8')
        index.append(f'- [{TITLES[category]}]({category}.md)')
    if family == 'zdt':
        classic = read(base / 'benchmark_classic/algorithm_benchmark_igd_hv_summary.csv')
        adaptive = {r['algorithm']: r for r in read(base / 'benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv')}
        rows = []
        for r in classic:
            a = adaptive[r['algorithm']]
            rows.append({'algorithm': r['algorithm'], 'IGD_classic': r['IGD_mean'], 'IGD_adaptive': a['IGD_mean'], 'HV_classic': r['HV_mean'], 'HV_adaptive': a['HV_mean']})
        lines = [f'# {problem.upper()} — Classic và adaptive', '',
                 '## Benchmark seed 42–71', '',
                 'Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.', '']
        lines += table(rows, ['algorithm', 'IGD_classic', 'IGD_adaptive', 'HV_classic', 'HV_adaptive'])
        lines += ['## Xác nhận seed 1000–1029', '',
                  'Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.', '',
                  '## Báo cáo nguồn', '', '- [Benchmark classic](benchmark_classic.md)', '- [Benchmark adaptive](benchmark_adaptive.md)', '', '[Danh mục báo cáo](README.md)', '']
        (folder / 'classic_vs_adaptive.md').write_text('\n'.join(lines), encoding='utf-8')
        index.append('- [So sánh classic và adaptive](classic_vs_adaptive.md)')
    index += ['', '[Trở về hồ sơ dữ liệu](../README.md)', '']
    (folder / 'README.md').write_text('\n'.join(index), encoding='utf-8')
