"""Publish audited six-solver evidence; preserve the separate OADE study sections."""
from pathlib import Path
import csv
import json
from result_display import sci

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'results/experiments/zdt_six_fixed_oade_v1/derived'
rows = list(csv.DictReader((D/'audited_summary.csv').open(encoding='utf-8')))
pairs = list(csv.DictReader((D/'audited_comparisons.csv').open(encoding='utf-8')))
audit = json.loads((D/'audit.json').read_text(encoding='utf-8'))
assert audit['records'] == 900 and audit['valid_runs'] == 899
names = ['NSGA2','DNSGA2','CGDE_NSGAII','GDE3','NSDE','OADE_NSGAII']
problems = ['zdt1','zdt2','zdt3','zdt4','zdt6']
lookup = {(r['problem'],r['algorithm']):r for r in rows}

def table(metric):
    lines = ['| Problem | '+' | '.join(names)+' |', '|---|'+'---:|'*6]
    extreme = min if metric == 'IGD' else max
    bestkey = metric+('_min' if metric == 'IGD' else '_max')
    for problem in problems:
        winners = {key:extreme(float(lookup[problem,n][key]) for n in names)
                   for key in [metric+'_mean',bestkey]}
        cells=[]
        for name in names:
            parts=[]
            for key in winners:
                value=float(lookup[problem,name][key]); label=sci(value)
                parts.append('**'+label+'**' if value==winners[key] else label)
            cells.append(parts[0]+' ('+parts[1]+')')
        lines.append('| '+problem.upper()+' | '+' | '.join(cells)+' |')
    return '\n'.join(lines)

tables = '### IGD ↓ — mean (best)\n\n'+table('IGD')+'\n\n### HV ↑ — mean (best)\n\n'+table('HV')
outcomes=['| Baseline | ZDT1 | ZDT2 | ZDT3 | ZDT4 | ZDT6 | OADE better / 10 |',
          '|---|---|---|---|---|---|---:|']
for name in names[:-1]:
    cells=[]; count=0
    for problem in problems:
        values=[]
        for metric in ['IGD','HV']:
            r=next(r for r in pairs if r['problem']==problem and r['comparison_algorithm']==name and r['metric']==metric)
            win=r['result']=='reference_better'; count+=win
            values.append('+' if win else 'NS')
        cells.append(' / '.join(values))
    outcomes.append('| '+name+' | '+' | '.join(cells)+f' | {count} |')
outcomes='\n'.join(outcomes)
ns=[r for r in pairs if r['result']=='no_significant_difference']
ns_table='| Problem | Metric | Baseline | Paired n | Holm p |\n|---|---|---|---:|---:|\n'+'\n'.join(
    f"| {r['problem'].upper()} | {r['metric']} | {r['comparison_algorithm']} | {r['n_pairs']} | {sci(r['p_adjusted_holm'])} |" for r in ns)

report=f'''# Kết quả đối chứng sáu thuật toán trên ZDT

Ngày phân tích: 19/11/2026. Bộ `zdt_six_fixed_oade_v1` đã hoàn tất **900 lượt**, trong đó **899 hợp lệ**. Sau hiệu chỉnh Holm chung 50 endpoint, OADE tốt hơn có ý nghĩa ở **44**, **6 chưa phát hiện khác biệt**, không có endpoint baseline tốt hơn có ý nghĩa. OADE có mean IGD thấp nhất và mean HV cao nhất trên ZDT1/2/3/6; NSGA-II có mean tốt nhất trên ZDT4. Đây là kết quả của các triển khai và cấu hình được đo, không phải kết luận ưu thế phổ quát.

## Thiết kế và mẫu phân tích

Sáu thuật toán: OADE_NSGAII, NSGA2, DNSGA2, CGDE_NSGAII, GDE3, NSDE. ZDT1/2/3 có D=30, ZDT4/6 có D=10; tất cả M=2. Mỗi nhóm dùng 30 seed 42–71, quần thể 100, cap 20.000 FE/lượt, cùng khởi tạo uniform theo bài/seed. Tổng thực tế **{audit['total_evaluations']:,} FE**, không giả định mọi lượt dùng hết cap. [Giao thức](../protocols/zdt_six_fixed_oade.md) · [Manifest](../../results/experiments/zdt_six_fixed_oade_v1/study_manifest.json).

GDE3/NSDE dùng pymoo 0.6.2, DE/rand/1/bin, F=0,5, CR=0,5, gamma=10⁻⁴, bounce-back và RankAndCrowding mặc định. OADE và CGDE giữ nguyên cấu hình. D-NSGA-II được thử trên bài tĩnh; CGDE là bản tái dựng có các giả định đã ghi trong [registry](../protocols/baselines.md).

Một lượt CGDE trên ZDT4, seed 63, có front suy biến (`invalid_collapsed_front`); không gán IGD/HV giả để thay thế. Nhóm CGDE–ZDT4 và hai phép so tương ứng dùng 29 lượt/cặp; các nhóm còn lại dùng 30. Tất cả 300 lượt GDE3/NSDE hợp lệ. HV bằng 0 là kết quả hợp lệ khi front không đóng góp thể tích đối với reference point đã cố định, không đồng nghĩa lỗi chương trình.

## Hai bảng chất lượng

Ô là **mean (best run)** trên các lượt hợp lệ; IGD thấp tốt, HV cao tốt. Best là min IGD hoặc max HV, có thể thuộc seed khác nhau. In đậm mean và best riêng theo số chưa làm tròn; các số cùng cách hiển thị có thể không bằng nhau. SD và runtime được giữ trong CSV, không đặt cạnh mean trong bảng này. Best run chỉ mô tả một lượt, không phải bằng chứng thống kê.

{tables}

## So sánh theo cặp sau Holm

Đơn vị ghép cặp là seed trong từng bài. Wilcoxon hai phía (`zero_method=wilcox`, `method=auto`; toàn chênh lệch 0 đặt p=1), alpha=0,05; Holm trên **5 bài × 5 baseline × 2 chỉ số = 50 endpoint**. Bảng dưới ghi **IGD / HV**: `+` là OADE tốt hơn có ý nghĩa; NS là chưa phát hiện khác biệt, không chứng minh tương đương. Các endpoint dùng chung reference nên không phải 50 thí nghiệm độc lập.

{outcomes}

![Hiệu ứng theo cặp và ý nghĩa sau Holm](figures/zdt_six/paired_effects.png)

Màu là rank-biserial, định hướng dương có lợi cho OADE, âm có lợi cho baseline; đây không phải phần trăm cải thiện. Ký hiệu +/NS lấy từ kiểm định sau Holm; độ lớn hiệu ứng không thay thế p. Mỗi ô dùng 30 cặp, riêng CGDE–ZDT4 dùng 29. [PDF](figures/zdt_six/paired_effects.pdf) · [SVG](figures/zdt_six/paired_effects.svg).

Sáu endpoint chưa đạt ngưỡng:

{ns_table}

[CSV kiểm định đã audit](../../results/experiments/zdt_six_fixed_oade_v1/derived/audited_comparisons.csv) giữ median chênh lệch **OADE − baseline** theo cặp, rank-biserial (dương có lợi cho OADE), số thắng/thua/hòa và CI bootstrap percentile 95% với 20.000 lần lấy mẫu lại cặp seed, RNG 20261119. CI là khoảng biên chưa hiệu chỉnh đa kiểm định; kết luận ý nghĩa dùng p Holm, không suy từ CI đó. Chiều median chênh lệch thuận lợi là âm cho IGD, dương cho HV.

## Diễn giải và kết luận

- **Đối chứng mới:** OADE tốt hơn GDE3 ở cả 10 endpoint và NSDE ở 9/10. Trên ZDT3, mean IGD của OADE thấp hơn NSDE nhưng p Holm=0,2024 nên chưa đủ bằng chứng khác biệt; HV vẫn tốt hơn có ý nghĩa. Các kết quả này hỗ trợ lợi ích chất lượng của cấu hình OADE so với hai cấu hình DE thư viện đã đo, chưa quy được lợi ích cho riêng một cơ chế.
- **ZDT2:** GDE3/NSDE có best IGD gần các thuật toán khác nhưng mean tăng lên 8,597e-2 / 1,665e-1. Khoảng cách giữa best và mean cho thấy chỉ nhìn seed tốt nhất sẽ che các lượt có sai số lớn. OADE có mean IGD 4,710e-3, mean HV 5,377e-1.
- **ZDT4 là hạn chế chính:** NSGA-II có mean IGD 9,953e-3 và mean HV 8,594e-1, tốt hơn mô tả so với OADE 3,979e-2 / 8,139e-1; kiểm định OADE với NSGA-II và D-NSGA-II đều NS ở cả hai chỉ số. Không được diễn giải thành OADE thắng trên ZDT4. GDE3/NSDE có mean IGD 8,542 / 6,938 và HV bằng 0 trong cả 30 lượt mỗi thuật toán; cấu hình DE cố định này chưa phù hợp với ZDT4 ở ngân sách đang xét.
- **ZDT6:** OADE có mean IGD tốt nhất 3,881e-3 và tốt hơn cả năm baseline có ý nghĩa về IGD. HV so với CGDE có p Holm=0,05581, nên chưa đạt ngưỡng dù mean OADE nhỉnh hơn. Không chuyển kết luận từ họ 60 endpoint lịch sử sang họ 50 endpoint mới.
- **Chi phí chạy:** median runtime theo bài của GDE3 khoảng 1,21–1,33 giây, NSDE 1,10–1,18 giây, NSGA-II 2,09–2,23 giây, D-NSGA-II 2,04–2,22 giây, OADE 4,04–4,62 giây và CGDE 93,98–286,35 giây. Hai baseline mới giảm thời gian đo được nhưng có đánh đổi chất lượng, rõ nhất ở ZDT2/4. Runtime là mô tả trên máy và triển khai này, không phải kiểm định tăng tốc hay độ phức tạp thuật toán.

Manifest ghi hai phiên 8 worker (900 lượt chờ ban đầu, 319 khi resume); OMP/OPENBLAS/MKL thread variables không được đặt trong snapshot. Vì vậy không khẳng định mỗi worker chỉ dùng một thread và không so runtime với đợt lịch sử như phép thử tăng tốc có kiểm soát.

Các seed và cấu hình của bốn thuật toán giữ lại trùng thiết kế trước; đợt này chạy mới nhưng không phải xác nhận trên seed holdout. Chưa đo DTLZ/WFG, M>2 hay tối ưu động. Các nghiên cứu cơ chế/OFAT OADE là bằng chứng riêng; không suy nguyên nhân từ bảng so thuật toán. Không có cơ sở đổi cấu hình production chỉ từ best seed hoặc kết quả benchmark này.

## Biểu đồ phân bố và Pareto mới nhất

![IGD median và IQR trên trục log](figures/zdt_six/igd_log_comparison.png)

Điểm là median, đoạn ngang là Q1–Q3 trên cùng phạm vi log10 giữa các panel; không phải CI. Giữ 899 lượt hợp lệ của sáu thuật toán, riêng CGDE–ZDT4 có 29. [Phân bố IGD đủ seed](figures/zdt_six/igd_distribution.png) giữ các đuôi lớn; boxplot tính trên thang gốc rồi đổi trục log khi hiển thị.

![Phân bố HV của sáu thuật toán](figures/zdt_six/hv_distribution.png)

HV cao tốt; trục tuyến tính từ 0, giữ mọi giá trị 0. Mỗi chấm là một seed; hộp Q1–Q3, vạch giữa median, râu 1,5 IQR. Phạm vi mỗi bài riêng, không xếp hạng bằng HV giữa các bài. [Runtime](figures/zdt_six/runtime_distribution.png) dùng đủ 900 lượt hoàn tất, kể cả lượt CGDE có front suy biến; trục log và các giới hạn worker/thread như đã nêu.

[Nghiệm OADE trên Pareto front chuẩn](oade_zdt_pareto_fronts.md) đã được trích và vẽ lại từ đợt sáu thuật toán hiện tại, chọn seed có IGD tốt nhất mỗi bài. Đây là hình best-case, không phải mô tả lượt điển hình. Bộ hình bảy thuật toán và các sidecar cũ đã được thay thế; không dùng chúng minh họa kết quả mới.

## Kiểm chứng và tái tạo phân tích

[Script kiểm chứng](../../analysis/audit_zdt_six.py) dùng đường tính riêng với pipeline báo cáo: xác minh **900 checksum primary**, **113 hash source**, **150 khối khởi tạo ghép cặp**, bounds, không trội, tính lại objective từ X và IGD/HV từ F; đối chiếu 900 dòng raw, 30 dòng summary và toàn bộ 50 kiểm định/Holm. Sai số lớn nhất objective, IGD/HV đều **0**. Manifest được kiểm tra không đổi. [Biên bản audit](../../results/experiments/zdt_six_fixed_oade_v1/derived/audit.json) · [Summary](../../results/experiments/zdt_six_fixed_oade_v1/derived/audited_summary.csv).

Đây là kiểm chứng bằng đường tính độc lập do cùng người phân tích thực hiện, vẫn dùng cùng thư viện pymoo cho objective/indicator; không phải xác nhận từ nhóm nghiên cứu bên ngoài, không chạy lại optimizer và không kiểm chứng toàn bộ transition trace.

Kiểm tra bảo trì: `git diff --check` đạt; đối chiếu bảng và liên kết tài liệu đạt. Lệnh `research check-structure` hiện báo hai lỗi vì allowlist cũ chưa chứa package `gde3`/`nsde`, dù import solver nằm đúng package. Khi bổ sung hai tên vào allowlist trong bộ nhớ rồi chạy lại, toàn bộ kiểm tra cấu trúc/liên kết đạt. Chưa sửa file source đã được hash trong manifest; đây là hạn chế của công cụ kiểm tra cấu trúc, tách biệt với audit số liệu ở trên.

```powershell
.\\.venv\\Scripts\\python.exe analysis/audit_zdt_six.py
& "C:/Program Files/R/R-4.6.2/bin/Rscript.exe" --vanilla analysis/plot_zdt_six_comparison.R
& "C:/Program Files/R/R-4.6.2/bin/Rscript.exe" --vanilla analysis/plot_zdt_distributions.R
.\\.venv\\Scripts\\python.exe analysis/report_zdt_six.py
```

Hình dùng dữ liệu đã audit; [mã vẽ hiệu ứng](../../analysis/plot_zdt_six_comparison.R), [mã vẽ phân bố](../../analysis/plot_zdt_distributions.R). Báo cáo và dữ liệu bảy thuật toán vẫn là bằng chứng lịch sử riêng; các hình cũ đã được gỡ sau khi có hình thay thế.
'''
(ROOT/'docs/reports/zdt_six_fixed_oade_report.md').write_text(report,encoding='utf-8')

for filename,vi in [('README.md',False),('README.vi.md',True)]:
    path=ROOT/filename; text=path.read_text(encoding='utf-8')
    begin='<!-- six-solver-audited-results:start -->'
    finish='<!-- six-solver-audited-results:end -->'
    if begin in text:
        start=text.index(begin); end=text.index(finish,start)+len(finish)
    else:
        needle='**Chưa có kết quả đối chứng chính thức' if vi else '**Official six-algorithm results are pending.'
        if needle in text:
            start=text.index(needle); end=text.index('\n\n',start)
        else:
            start=text.index('**Đã hoàn tất 900 lượt' if vi else '**Completed: 900 runs')
            end=text.index('\n\nKhông đổi tên' if vi else '\n\nNo results from the old',start)
    description=('**Đã hoàn tất 900 lượt, 899 hợp lệ.** Sau Holm chung 50 endpoint: **OADE tốt hơn 44, 6 NS, không có endpoint baseline tốt hơn có ý nghĩa**. Một lượt CGDE–ZDT4 seed 63 có front suy biến; nhóm này dùng 29 lượt hợp lệ, các nhóm khác 30. OADE có mean tốt nhất ở ZDT1/2/3/6; NSGA-II có mean tốt nhất trên ZDT4. '
                 if vi else '**Completed: 900 runs, 899 valid.** Global Holm across 50 endpoints: **OADE better in 44, 6 nonsignificant, none significantly favoring a baseline**. CGDE–ZDT4 seed 63 collapsed; that group has 29 valid runs, all others 30. OADE has the best means on ZDT1/2/3/6; NSGA-II has the best means on ZDT4. ')
    description+='[Audited report](docs/reports/zdt_six_fixed_oade_report.md).\n\n'
    description+=('Ô là mean (best run): min IGD/max HV; in đậm hai đại lượng riêng theo số chưa làm tròn. Best hai chỉ số có thể thuộc seed khác nhau; NS không chứng minh tương đương.\n\n' if vi else 'Cells show mean (best run): min IGD/max HV; means and best runs are bolded separately using unrounded values. Metric best runs may use different seeds; NS does not establish equivalence.\n\n')
    description+=tables+'\n\n'+('Kết quả sau Holm, theo thứ tự **IGD / HV**; +: OADE tốt hơn có ý nghĩa, NS: chưa phát hiện khác biệt.\n\n' if vi else 'Holm outcomes in **IGD / HV** order; +: OADE significantly better, NS: no detected difference.\n\n')+outcomes
    description+='\n\n![Paired effects after global Holm](docs/reports/figures/zdt_six/paired_effects.png)\n\n'
    description+=('Màu là rank-biserial (dương có lợi cho OADE), không phải phần trăm cải thiện. GDE3/NSDE nhanh hơn trong runtime đo được nhưng kém rõ trên ZDT4 (HV=0); NSDE–ZDT3 IGD và CGDE–ZDT6 HV vẫn NS. Audit khớp 900 primary, 30 summary và 50 kiểm định; sai lệch objective/IGD/HV bằng 0. [Dữ liệu kiểm định và giới hạn diễn giải](docs/reports/zdt_six_fixed_oade_report.md).'
                  if vi else 'Color shows rank-biserial effects (positive favors OADE), not percentage improvement. GDE3/NSDE had lower measured runtime but poor ZDT4 quality (HV=0); NSDE–ZDT3 IGD and CGDE–ZDT6 HV remain nonsignificant. Independent recalculation matched 900 primary records, 30 summaries and 50 tests, with zero objective/IGD/HV discrepancy. [Statistical data and interpretation limits](docs/reports/zdt_six_fixed_oade_report.md).')
    description+='\n\n![IGD median and IQR, current six-solver study](docs/reports/figures/zdt_six/igd_log_comparison.png)\n\n'
    description+=('Điểm là median, đoạn là Q1–Q3, trục log10 chung; không phải CI. [Phân bố IGD đầy đủ](docs/reports/figures/zdt_six/igd_distribution.png) · [Phân bố HV](docs/reports/figures/zdt_six/hv_distribution.png) · [Runtime](docs/reports/figures/zdt_six/runtime_distribution.png) · [Pareto OADE từ dữ liệu mới](docs/reports/oade_zdt_pareto_fronts.md).'
                  if vi else 'Points show medians and segments show Q1–Q3 on a shared log10 axis, not confidence intervals. [All-seed IGD](docs/reports/figures/zdt_six/igd_distribution.png) · [HV](docs/reports/figures/zdt_six/hv_distribution.png) · [Runtime](docs/reports/figures/zdt_six/runtime_distribution.png) · [OADE Pareto fronts from current data](docs/reports/oade_zdt_pareto_fronts.md).')
    text=text[:start]+begin+'\n\n'+description+'\n\n'+finish+text[end:]
    if vi:
        text=text.replace('[hình Pareto đã vẽ](docs/reports/oade_zdt_pareto_fronts.md) và dữ liệu gốc được giữ như **bằng chứng lịch sử**','dữ liệu gốc được giữ như **bằng chứng lịch sử**')
    else:
        text=text.replace('[figures](docs/reports/oade_zdt_pareto_fronts.md) and original datasets remain **historical evidence**','original datasets remain **historical evidence**')
    text=text.replace('# Fresh official study.','# Fresh replication: use a NEW output directory.').replace('# Chạy chính thức trong thư mục mới.','# Lặp lại độc lập: dùng thư mục output MỚI.')
    text=text.replace('benchmark-zdt-six --stage run --jobs 8\n','benchmark-zdt-six --stage run --jobs 8 --out-dir results/experiments/zdt_six_replication\n')
    text=text.replace('Chưa kết luận tăng tốc runtime trước khi đo trong môi trường đã ghi.','Runtime đã được đo; giới hạn so sánh máy/worker/thread được nêu trong báo cáo.').replace('Runtime includes implementation and machine effects and must be measured before claiming a speedup.','Recorded runtime includes implementation, worker and machine effects; see the report for its limits.')
    path.write_text(text,encoding='utf-8')

p=ROOT/'docs/index.md'; t=p.read_text(encoding='utf-8').replace('official results are pending.','900 runs are complete, 899 valid. Global Holm (50 endpoints): 44 favor OADE and 6 are nonsignificant.')
t=t.replace('- [Audited six-solver results and conclusions](reports/zdt_six_fixed_oade_report.md)\n','')
t=t.replace('- [Current comparison tables]','- [Audited six-solver results and conclusions](reports/zdt_six_fixed_oade_report.md)\n- [Current comparison tables]');p.write_text(t,encoding='utf-8')
for filename in ['docs/protocols/baselines.md','docs/protocols/experiment_registry.md']:
    p=ROOT/filename;t=p.read_text(encoding='utf-8').replace('official results are pending.','900 runs are complete, 899 valid; global Holm: 44/50 favor OADE, 6 nonsignificant. See the [audited report](../reports/zdt_six_fixed_oade_report.md).').replace('900 planned runs and 50 Holm endpoints. Official execution/results are pending.','900 completed runs (899 valid) and 50 Holm endpoints: 44 favor OADE, 6 nonsignificant. See the [audited report](../reports/zdt_six_fixed_oade_report.md).');p.write_text(t,encoding='utf-8')
p=ROOT/'docs/protocols/zdt_six_fixed_oade.md'; t=p.read_text(encoding='utf-8').replace('Chưa có kết luận đối chứng chính thức cho bộ sáu thuật toán trước khi chạy và kiểm chứng dữ liệu mới.','Kết luận chính thức sau khi hoàn tất và kiểm chứng dữ liệu được liên kết ở phần dưới.'); marker='## Kết quả hoàn tất — 19/11/2026';t=t.split('\n'+marker)[0];p.write_text(t+'\n'+marker+'\n\n900/900 lượt đã hoàn tất; 899 hợp lệ. Sau Holm chung 50 endpoint: 44 có lợi cho OADE, 6 chưa phát hiện khác biệt. Một lượt CGDE–ZDT4 seed 63 suy biến. [Báo cáo, bảng IGD/HV, hình và kiểm chứng](../reports/zdt_six_fixed_oade_report.md). Thiết kế và nguồn primary giữ nguyên.\n',encoding='utf-8')
(ROOT/'docs/manuscript/manuscript.md').write_text('''# OADE-NSGA-II: current evidence

Updated 19 November 2026. The active comparison includes OADE, NSGA-II, D-NSGA-II, CGDE-NSGA-II, GDE3 and NSDE on ZDT1/2/3/4/6 (two objectives; D=30 for ZDT1/2/3, D=10 for ZDT4/6). With population 100, a 20,000-evaluation cap and 30 paired seeds, all 900 runs completed; 899 were valid. CGDE–ZDT4 seed 63 produced a collapsed front, leaving 29 valid pairs for its two endpoints.

Global Holm correction across 50 paired Wilcoxon endpoints identified 44 in favor of OADE and six nonsignificant; none significantly favored a baseline. OADE had the best mean IGD and HV on ZDT1/2/3/6. NSGA-II had the best means on ZDT4; comparisons of OADE with NSGA-II and D-NSGA-II were nonsignificant for both metrics there. OADE outperformed GDE3 on all ten endpoints and NSDE on nine, with ZDT3 IGD nonsignificant. ZDT6 HV versus CGDE was also nonsignificant (Holm p=0.05581).

These findings concern the tested implementations and fixed settings. GDE3/NSDE had lower measured runtime but poor ZDT4 quality. Runtime was measured with eight workers and no recorded OMP/BLAS thread limit; it is not a controlled complexity or cross-study speedup claim. D-NSGA-II was tested on static functions; CGDE remains a documented reconstruction. The retained solvers use the same seeds as the historical study, so this is not held-out-seed confirmation. DTLZ/WFG and more than two objectives have not been evaluated with the active comparison set.

The [audited six-solver report](../reports/zdt_six_fixed_oade_report.md) provides both quality tables, all six nonsignificant endpoints, effect sizes, bootstrap uncertainty, the figure and provenance. Independent recalculation verified 900 primary checksums, 113 source hashes, all summaries and all 50 tests, with zero objective/IGD/HV discrepancy. This used a separate calculation path by the same analyst and the same objective/indicator libraries, not external replication or a complete transition audit.

The [480-run mechanism study](../reports/mechanism_zdt46_report.md) and [2,100-run parameter study](../reports/mechanism_sensitivity_report.md) remain separate evidence for component effects. The [seven-solver report](../reports/zdt_seven_fixed_oade_v2_report.md) and its 60-endpoint correction remain historical, with superseded charts removed. [Best-seed Pareto figures](../reports/oade_zdt_pareto_fronts.md) now use the current six-solver dataset. Historical data are not pooled into the active comparison. A full submission-ready manuscript has not yet been drafted.

See the [protocol](../protocols/zdt_six_fixed_oade.md), [baseline registry](../protocols/baselines.md), [reconstruction assumptions](../protocols/baseline_paper_corrections.md) and [references](references.bib).
''',encoding='utf-8')
print('Published audited tables and updated six main documentation files plus protocol/report.')
