"""Render complete audited tables as Markdown; no new inference or solver run."""
import csv
from pathlib import Path
from result_display import sci

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'results/experiments/mechanism_sensitivity_v1/derived'


def rows(name):
    with (D/name).open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))


def num(value):
    return sci(value)


def main():
    comparisons=rows('audited_comparisons.csv');summary=rows('audited_summary.csv')
    assert len(comparisons)==124 and len(summary)==70
    columns=('IGD_mean','IGD_median','HV_mean','HV_median','runtime_median','IGD_min','HV_max')
    best={(p,k):(max if k.startswith('HV') else min)(float(r[k]) for r in summary if r['problem']==p)
          for p in {r['problem'] for r in summary} for k in columns}
    def value(r,key):
        text=num(r[key])
        return f'**{text}**' if float(r[key])==best[r['problem'],key] else text
    lines=['# Phụ lục: độ nhạy tham số cơ chế OADE','',
        '[Báo cáo kết luận](mechanism_sensitivity_report.md). Tạo từ các bảng đã audit; giữ đủ 124 endpoint và 70 nhóm, không chỉ chọn kết quả có ý nghĩa.',
        '', '## Toàn bộ so sánh','',
        'n=30 cặp seed mỗi dòng, không loại cặp. Δ=median(tham chiếu−mức thử); IGD dương/HV âm thiên về mức thử. Rank-biserial dương thiên về tham chiếu. CI 95% percentile (20.000 bootstrap cặp seed) chưa hiệu chỉnh đa kiểm định; p Holm hiệu chỉnh chung 124 endpoint. Thắng/thua/hòa theo hướng có lợi cho mức thử. Mốc initial là full; mốc held là cùng tham số held tại mức production (F=0,65; CR=0,5; pDE=0,5). NS là chưa phát hiện khác biệt, không phải tương đương.',
        '', '| Bài | Tham số | Mode | Mức | Metric | Δ [CI 95%] | W | p thô | p Holm | Rank-biserial | Mức thử thắng/thua/hòa | Kết luận |',
        '|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
    for r in comparisons:
        result={'not_significant':'NS','reference_better':'Mốc tốt hơn','level_better':'Mức thử tốt hơn'}[r['result']]
        lines.append(f'| {r["problem"]} | {r["parameter"]} | {r["mode"]} | {r["level"]} | {r["metric"]} | {num(r["median_paired_difference"])} [{num(r["ci_low"])}; {num(r["ci_high"])}] | {num(r["statistic"])} | {num(r["p_value"])} | {num(r["p_adjusted_holm"])} | {num(r["rank_biserial_effect"])} | {r["level_wins"]}/{r["reference_wins"]}/{r["ties"]} | {result} |')
    lines+=['','## Hai bảng chất lượng cho đủ 70 nhóm','',
        'Mỗi nhóm có 30 run hợp lệ. Ô mean (best) ghi trung bình và giá trị tốt nhất: IGD min, HV max; hai best có thể thuộc hai seed khác nhau. Bỏ Valid, Runtime, FE và SD khỏi bảng trình bày; số liệu đầy đủ vẫn giữ trong CSV nguồn. Full chỉ chạy một lần mỗi bài/seed dù dùng chung trong nhiều contrast. In đậm mean và best-run tốt nhất riêng trong 35 cấu hình của cùng bài, xét số chưa làm tròn và giữ đồng hạng. Hiển thị tối đa 4 chữ số có nghĩa; số nhìn bằng nhau chưa chắc đồng hạng. In đậm không phải kết luận kiểm định hay tham số tối ưu. Mode held chỉ giữ tham số nêu trong dòng; mốc tương ứng ghi trong báo cáo.',
    ]
    lookup={(r['algorithm'],r['problem']):r for r in summary}
    for metric in ('IGD','HV'):
        lines+=['',f'### {metric} — mean (best), {"thấp hơn tốt hơn" if metric=="IGD" else "cao hơn tốt hơn"}','',
                '| Tham số | Mức | Mode | ZDT4 | ZDT6 |','|---|---:|---|---:|---:|']
        for original in [r for r in summary if r['problem']=='zdt4']:
            scores=[]
            for problem in ('zdt4','zdt6'):
                r=lookup[original['algorithm'],problem]
                scores.append(f'{value(r,metric+"_mean")} ({value(r,metric+("_min" if metric=="IGD" else "_max"))})')
            lines.append(f'| {original["parameter"]} | {original["level"] or "—"} | {original["mode"]} | '+ ' | '.join(scores)+' |')
    (ROOT/'docs/reports/mechanism_sensitivity_tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':main()
