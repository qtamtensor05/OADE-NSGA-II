"""Render complete audited tables as Markdown; no new inference or solver run."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'results/experiments/mechanism_sensitivity_v1/derived'


def rows(name):
    with (D/name).open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def num(value):
    return f'{float(value):.7g}'


def main():
    comparisons=rows('audited_comparisons.csv');summary=rows('audited_summary.csv')
    assert len(comparisons)==124 and len(summary)==70
    lines=['# Phụ lục: độ nhạy tham số cơ chế OADE','',
        '[Báo cáo kết luận](mechanism_sensitivity_report.md). Tạo từ các bảng đã audit; giữ đủ 124 endpoint và 70 nhóm, không chỉ chọn kết quả có ý nghĩa.',
        '', '## Toàn bộ so sánh','',
        'n=30 cặp seed mỗi dòng, không loại cặp. Δ=median(tham chiếu−mức thử); IGD dương/HV âm thiên về mức thử. Rank-biserial dương thiên về tham chiếu. CI 95% percentile (20.000 bootstrap cặp seed) chưa hiệu chỉnh đa kiểm định; p Holm hiệu chỉnh chung 124 endpoint. Thắng/thua/hòa theo hướng có lợi cho mức thử. Mốc initial là full; mốc held là cùng tham số held tại mức production (F=0,65; CR=0,5; pDE=0,5). NS là chưa phát hiện khác biệt, không phải tương đương.',
        '', '| Bài | Tham số | Mode | Mức | Metric | Δ [CI 95%] | W | p thô | p Holm | Rank-biserial | Mức thử thắng/thua/hòa | Kết luận |',
        '|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
    for r in comparisons:
        result={'not_significant':'NS','reference_better':'Mốc tốt hơn','level_better':'Mức thử tốt hơn'}[r['result']]
        lines.append(f'| {r["problem"]} | {r["parameter"]} | {r["mode"]} | {r["level"]} | {r["metric"]} | {num(r["median_paired_difference"])} [{num(r["ci_low"])}; {num(r["ci_high"])}] | {num(r["statistic"])} | {num(r["p_value"])} | {num(r["p_adjusted_holm"])} | {num(r["rank_biserial_effect"])} | {r["level_wins"]}/{r["reference_wins"]}/{r["ties"]} | {result} |')
    lines+=['','## Đủ 70 nhóm','',
        'Mỗi nhóm 30/30 lượt hợp lệ. Mean ± SD mẫu và median [Q1; Q3] là mô tả phân bố, không phải CI. Full chỉ chạy một lần mỗi bài/seed dù dùng chung trong nhiều contrast. Runtime là median giây/lượt trong môi trường tám worker có telemetry.',
        '', '| Bài | Algorithm ID | Tham số | Mức | Mode | IGD mean ± SD | IGD median [Q1; Q3] | HV mean ± SD | HV median [Q1; Q3] | Runtime (s) | FE min–max |',
        '|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f'| {r["problem"]} | {r["algorithm"]} | {r["parameter"]} | {r["level"] or "—"} | {r["mode"]} | {num(r["IGD_mean"])} ± {num(r["IGD_sd"])} | {num(r["IGD_median"])} [{num(r["IGD_q1"])}; {num(r["IGD_q3"])}] | {num(r["HV_mean"])} ± {num(r["HV_sd"])} | {num(r["HV_median"])} [{num(r["HV_q1"])}; {num(r["HV_q3"])}] | {num(r["runtime_median"])} | {r["n_eval_min"]}–{r["n_eval_max"]} |')
    (ROOT/'docs/reports/mechanism_sensitivity_tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':main()
