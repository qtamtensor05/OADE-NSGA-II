"""Read-only primary-evidence audit; writes additional derived analysis only."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter
import numpy as np
from scipy.stats import wilcoxon, rankdata
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'results/experiments/zdt_seven_fixed_oade_v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def holm(values):
    order = np.argsort(values, kind='stable')
    result = np.empty(len(values))
    running = 0.
    for i, index in enumerate(order):
        running = max(running, min(1., (len(values)-i)*values[index]))
        result[index] = running
    return result


def main():
    manifest = json.loads((DIRECTORY/'study_manifest.json').read_text(encoding='utf-8'))
    cfg = manifest['protocol']
    assert manifest['kind'] == 'zdt_seven_fixed_oade_v2'
    assert cfg['baseline_revision'] == 'paper_corrections_2026_11_14'
    sources_changed = [p for p, expected in manifest['source_hashes'].items()
                       if not (ROOT/p).is_file() or sha(ROOT/p) != expected]
    assert not sources_changed, sources_changed
    assert sha(DIRECTORY/'config/reference_fronts.json') == manifest['reference_sha256']
    refs = json.loads((DIRECTORY/'config/reference_fronts.json').read_text())
    assert set(manifest['artifacts']) == {p.relative_to(DIRECTORY).as_posix()
                                         for p in (DIRECTORY/'primary').glob('*.json')}
    records = []
    max_f_error = max_metric_error = 0.
    for name, expected in manifest['artifacts'].items():
        assert sha(DIRECTORY/name) == expected, name
        records.append(json.loads((DIRECTORY/name).read_text(encoding='utf-8')))
    names = [c['id'] for c in manifest['candidates']]
    seeds = cfg['global']['seeds']
    lookup = {(r['problem'], r['algorithm'], r['seed']): r for r in records}
    assert len(lookup) == len(records) == 1050
    for p in cfg['problems']:
        name = p['name']
        problem = get_problem(name, n_var=p['n_var'])
        ref = np.asarray(refs[name])
        igd, hv = IGD(ref), HV(ref_point=ref.max(axis=0)+.1)
        for seed in seeds:
            initial = np.random.default_rng(seed).uniform(problem.xl, problem.xu,
                                                         size=(100, p['n_var']))
            for algorithm in names:
                r = lookup[name, algorithm, seed]
                assert r['run_idx'] == seed - 42
                assert r['initial_x_sha256'] == digest(initial.tolist())
                assert r['reference_sha256'] == digest(ref.tolist())
                assert r['settings'] == next(c['settings'] for c in manifest['candidates']
                                              if c['id'] == algorithm)
                assert 0 < r['n_eval'] <= 20000
                if algorithm == 'OADE_NSGAII':
                    assert r['runner'] == 'local_oade' and r['settings']['params'] == {}
                x, f = np.asarray(r['final_x']), np.asarray(r['final_f'])
                assert x.shape == (len(f), p['n_var']) and f.shape == (len(x), 2)
                assert np.isfinite(x).all() and np.isfinite(f).all()
                assert ((x >= problem.xl-1e-10) & (x <= problem.xu+1e-10)).all()
                error = float(np.max(np.abs(problem.evaluate(x)-f)))
                max_f_error = max(max_f_error, error)
                assert error < 1e-10, (name, algorithm, seed, error)
                dominates = ((f[:, None] <= f[None, :]).all(axis=2)
                             & (f[:, None] < f[None, :]).any(axis=2))
                assert not dominates.any()
                if r['valid']:
                    for metric, value in [('IGD', float(igd(f))), ('HV', float(hv(f)))]:
                        error = abs(value-r[metric])
                        max_metric_error = max(max_metric_error, error)
                        assert error < 1e-10
    comparisons = []
    summaries = []
    rng = np.random.default_rng(20261115)
    for p in cfg['problems']:
        problem = p['name']
        for algorithm in names:
            group = [lookup[problem, algorithm, seed] for seed in seeds]
            s = dict(problem=problem, algorithm=algorithm, runs=len(group),
                     valid_runs=sum(r['valid'] for r in group),
                     zero_hv_runs=sum(r['HV'] == 0 for r in group),
                     n_eval_min=min(r['n_eval'] for r in group),
                     n_eval_max=max(r['n_eval'] for r in group),
                     convergence_rows_min=min(len(r['convergence']) for r in group),
                     convergence_rows_max=max(len(r['convergence']) for r in group))
            for metric in ['IGD', 'HV', 'runtime_seconds', 'n_eval', 'front_size']:
                values = [r[metric] for r in group if r['valid'] or metric not in ['IGD','HV']]
                s[metric+'_mean'] = float(np.mean(values)) if values else None
                s[metric+'_sd'] = float(np.std(values, ddof=1)) if len(values)>1 else None
                s[metric+'_median'] = float(np.median(values)) if values else None
            summaries.append(s)
        for metric in ['IGD', 'HV']:
            for algorithm in names:
                if algorithm == 'OADE_NSGAII':
                    continue
                pairs = [(lookup[problem, 'OADE_NSGAII', seed], lookup[problem, algorithm, seed])
                         for seed in seeds]
                pairs = [(a,b) for a,b in pairs if a['valid'] and b['valid']]
                a = np.asarray([a[metric] for a,b in pairs])
                b = np.asarray([b[metric] for a,b in pairs])
                d = a-b
                signed = d if metric == 'HV' else -d
                stat, pv = (0., 1.) if np.all(d == 0) else wilcoxon(d, zero_method='wilcox',
                                                                                alternative='two-sided', method='auto')
                nonzero = signed[signed != 0]
                ranks = rankdata(abs(nonzero))
                effect = float(np.sum(ranks*np.sign(nonzero))/np.sum(ranks)) if len(nonzero) else 0.
                bootstrap = np.median(d[rng.integers(0, len(d), size=(20000,len(d)))], axis=1)
                ci = np.quantile(bootstrap, [.025,.975])
                baseline_median = float(np.median(b))
                relative = ((np.median(a)-baseline_median)/baseline_median*100
                            * (1 if metric=='HV' else -1)) if baseline_median != 0 else None
                comparisons.append(dict(problem=problem, metric=metric, algorithm=algorithm,
                    n_pairs=len(pairs), wins=int(sum(signed>0)), ties=int(sum(signed==0)),
                    losses=int(sum(signed<0)), median_oade=float(np.median(a)),
                    median_baseline=baseline_median, relative_median_improvement_pct=relative,
                    median_paired_oade_minus_baseline=float(np.median(d)),
                    ci95_median_difference_low=float(ci[0]), ci95_median_difference_high=float(ci[1]),
                    statistic=float(stat), p_value=float(pv), rank_biserial_effect=effect))
    adjusted = holm([r['p_value'] for r in comparisons])
    for r, pv in zip(comparisons, adjusted):
        r['p_holm_60'] = float(pv)
        r['result'] = ('no_significant_difference' if pv >= .05 else
                       'oade_better' if r['rank_biserial_effect']>0 else 'baseline_better')
    existing = {(r['problem'],r['metric'],r['comparison_algorithm']): r
                for r in read_csv(DIRECTORY/'derived/comparisons.csv')}
    for r in comparisons:
        old = existing[r['problem'],r['metric'],r['algorithm']]
        for key, old_key in [('p_value','p_value'), ('p_holm_60','p_holm_all_endpoints'),
                              ('rank_biserial_effect','rank_biserial_effect')]:
            assert np.isclose(r[key],float(old[old_key]),rtol=1e-10,atol=1e-12), (r,key,old)
    existing_summary = {(r['problem'], r['algorithm']):r for r in read_csv(DIRECTORY/'derived/summary.csv')}
    for row in summaries:
        old = existing_summary[row['problem'],row['algorithm']]
        for metric in ['IGD','HV','runtime_seconds','n_eval']:
            for suffix in ['mean','sd','median']:
                key = metric+'_'+suffix
                assert np.isclose(row[key],float(old[key]),rtol=1e-10,atol=1e-12), (row,key)
    write_csv(DIRECTORY/'derived/audited_comparisons.csv', comparisons)
    write_csv(DIRECTORY/'derived/audited_summary.csv', summaries)
    audit = dict(manifest_sha256=sha(DIRECTORY/'study_manifest.json'),
                 records=len(records), valid_runs=sum(r['valid'] for r in records),
                 validity_counts=dict(Counter(r['validation_status'] for r in records)),
                 source_files_verified=len(manifest['source_hashes']),
                 artifact_checksums_verified=len(manifest['artifacts']),
                 max_objective_recalculation_error=max_f_error,
                 max_metric_recalculation_error=max_metric_error,
                 comparison_rows_verified=len(comparisons), summary_rows_verified=len(summaries),
                 bootstrap=dict(seed=20261115,resamples=20000,unit='paired seed within problem',
                                interval='percentile 95%; marginal, not multiplicity-adjusted'),
                 results=dict(Counter(r['result'] for r in comparisons)),
                 environment=manifest['environment'])
    sensitivity = []
    for metric in ['IGD','HV']:
        a, b = [], []
        ref = np.asarray(refs['zdt4'])
        indicator = IGD(ref) if metric == 'IGD' else HV(ref_point=ref.max(axis=0)+.1)
        for seed in seeds:
            a.append(lookup['zdt4','OADE_NSGAII',seed][metric])
            b.append(float(indicator(np.asarray(lookup['zdt4','CGDE_NSGAII',seed]['final_f']))))
        test = wilcoxon(np.asarray(a)-b, zero_method='wilcox', method='auto')
        sensitivity.append(dict(metric=metric,n_pairs=30,p_value=float(test.pvalue),
                                oade_wins=int(sum((np.asarray(a)<b) if metric=='IGD' else (np.asarray(a)>b)))))
    audit['collapsed_front_sensitivity'] = sensitivity
    (DIRECTORY/'derived/audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    write_report(records, summaries, comparisons, audit, manifest)
    print(json.dumps(audit, indent=2))
    for p in cfg['problems']:
        print(p['name'], dict(Counter(r['result'] for r in comparisons if r['problem']==p['name'])))
    for r in comparisons:
        if r['result']!='oade_better':
            print('EXCEPTION',r)


def write_report(records, summaries, comparisons, audit, manifest):
    summary = {(r['problem'],r['algorithm']):r for r in summaries}
    def fmt(value):
        return '—' if value is None else f'{value:.7g}'
    lines = ['# Đối chứng 7 thuật toán trên ZDT — baseline mới và OADE thống nhất', '',
        '**Ngày kiểm tra: 15/11/2026.** Bộ dữ liệu: '
        '[zdt_seven_fixed_oade_v2](../../results/experiments/zdt_seven_fixed_oade_v2/). '
        'Chỉ phân tích lại bằng chứng đã chạy; không chạy lại thuật toán tối ưu.', '',
        '## Kết quả chính', '',
        'Đủ **1.050/1.050 run**, gồm **1.049 hợp lệ** và **1 collapsed front**. '
        'OADE tốt hơn ở **56/60 endpoint** sau Holm chung 60 kiểm định; '
        '4 endpoint chưa phát hiện khác biệt là IGD/HV trên ZDT4 khi so với NSGA2 và DNSGA2. '
        'Không có endpoint nào kết luận baseline tốt hơn OADE theo kiểm định đã định. '
        'Đây là số endpoint, không phải 60 thí nghiệm độc lập hay bằng chứng vượt mọi thuật toán.', '',
        'OADE tốt hơn tất cả sáu đối chứng trên cả IGD/HV ở ZDT1, ZDT2, ZDT3 và ZDT6. '
        'Trên ZDT4, OADE tốt hơn RNSGA2, CGDE, SDR-OLS và CE theo chỉ số toàn front, '
        'nhưng chưa đủ bằng chứng hơn NSGA2/DNSGA2. Độ ổn định ZDT4 là giới hạn nổi bật.', '',
        '## Xác minh dữ liệu và cấu hình', '',
        f'- Đã đối chiếu {audit["artifact_checksums_verified"]} checksum primary JSON, '
        f'{audit["source_files_verified"]} hash source/dependency với checkout hiện tại; '
        'reference snapshot khớp manifest. Không sửa primary hoặc manifest.',
        '- Mỗi block bài/thuật toán đủ 30 seed 42–71; không trùng/mất task; '
        'uniform input được tái tạo và hash khớp cho từng seed giữa bảy thuật toán.',
        '- OADE runner `local_oade`, params rỗng, cấu hình uniform + adaptive restart + '
        'OBL định kỳ + success_rate. Baseline revision `paper_corrections_2026_11_14`; '
        'CGDE dùng NCG/PCG, SDR-OLS bỏ cap 2N, CE dùng PM theo biểu thức công bố.',
        '- Đánh giá lại mọi final X bằng hàm ZDT; sai số X→F lớn nhất bằng 0. '
        'Kiểm tra bounds, hữu hạn, kích thước và tính không bị trội; '
        'IGD/HV của 1.049 run hợp lệ tính lại khớp tuyệt đối giá trị lưu.',
        '- Tái tính độc lập 35 dòng summary và 60 Wilcoxon/effect/Holm; khớp bảng pipeline. '
        'Lần tạo lại báo cáo ban đầu bị từ chối vì thiếu biến thread; khi đặt lại cả '
        'OMP/OPENBLAS/MKL=1 đúng manifest, bước report/resume qua. Không bỏ qua kiểm tra môi trường.',
        f'- Tổng FE thực: **{sum(r["n_eval"] for r in records):,}**; mọi run trong cap 20.000. '
        'OADE dùng 19.901–20.000; DNSGA2 dùng 19.910; các solver còn lại dùng 20.000.',
        f'- Manifest SHA-256: `{audit["manifest_sha256"]}`.', '',
        'Python 3.14.7; NumPy 2.5.4; SciPy 1.18.1; pymoo 0.6.2; PyYAML 6.0.3. '
        'Bốn worker, ba thư viện thread đặt 1. Hash xác minh tính nhất quán của artifact '
        'và mã lưu; không thay thế đối chứng với mã tác giả.', '',
        '## OADE so với NSGA2', '',
        'Dùng median riêng từng nhóm để tính phần trăm; số này khác median của chênh lệch '
        'theo cặp. IGD giảm tốt, HV tăng tốt. p là Holm chung 60 endpoint.', '',
        '| Bài | IGD OADE / NSGA2 | IGD giảm (%) | p Holm IGD | HV tăng (%) | p Holm HV |',
        '|---|---:|---:|---:|---:|---:|']
    for problem in ['zdt1','zdt2','zdt3','zdt4','zdt6']:
        ig = next(r for r in comparisons if r['problem']==problem and r['algorithm']=='NSGA2' and r['metric']=='IGD')
        hv = next(r for r in comparisons if r['problem']==problem and r['algorithm']=='NSGA2' and r['metric']=='HV')
        lines.append(f'| {problem.upper()} | {fmt(ig["median_oade"])} / {fmt(ig["median_baseline"])} '
                     f'| {ig["relative_median_improvement_pct"]:.2f} | {fmt(ig["p_holm_60"])} '
                     f'| {hv["relative_median_improvement_pct"]:.3f} | {fmt(hv["p_holm_60"])} |')
    lines += ['', '## Phân bố kết quả đủ bảy thuật toán', '',
              'IGD/HV trình bày mean ± SD và median, chỉ dùng run hợp lệ. '
              'Runtime median là thời gian đo trong lần chạy bốn worker; '
              'không phải so sánh tốc độ thuật toán thuần túy vì triển khai/thư viện khác nhau.', '']
    for problem in ['zdt1','zdt2','zdt3','zdt4','zdt6']:
        lines += [f'### {problem.upper()}', '',
                  '| Thuật toán | Valid | IGD mean ± SD | IGD median | HV mean ± SD | HV median | Runtime median (s) |',
                  '|---|---:|---:|---:|---:|---:|---:|']
        for candidate in manifest['candidates']:
            r = summary[problem,candidate['id']]
            lines.append(f'| {r["algorithm"]} | {r["valid_runs"]}/30 | '
                f'{fmt(r["IGD_mean"])} ± {fmt(r["IGD_sd"])} | {fmt(r["IGD_median"])} | '
                f'{fmt(r["HV_mean"])} ± {fmt(r["HV_sd"])} | {fmt(r["HV_median"])} | '
                f'{r["runtime_seconds_median"]:.3f} |')
        lines.append('')
    lines += ['## ZDT4: median tốt nhưng rủi ro sai số lớn', '',
        'OADE có IGD mean **0,0397899**, cao hơn NSGA2 **0,00995272** và DNSGA2 '
        '**0,0199731**, dù median thấp hơn. OADE thắng NSGA2 ở 21/30 cặp và DNSGA2 ở '
        '22/30 cặp, nhưng những lần thua có độ lớn đáng kể. Wilcoxon xét cả độ lớn '
        'qua thứ hạng, không chỉ đếm số lần thắng. Không được bỏ các seed này để nâng kết luận.', '',
        '| Seed OADE | IGD | HV |', '|---|---:|---:|']
    worst = sorted([r for r in records if r['problem']=='zdt4' and r['algorithm']=='OADE_NSGAII'],
                   key=lambda r:r['IGD'], reverse=True)[:7]
    for r in worst:
        lines.append(f'| {r["seed"]} | {fmt(r["IGD"])} | {fmt(r["HV"])} |')
    lines += ['', 'Độ bất định bổ sung: bootstrap theo cặp seed, 20.000 mẫu, seed 20261115; '
        'CI percentile 95% cho **median(OADE − baseline)**, chưa hiệu chỉnh đa kiểm định.', '',
        '| Baseline | Metric | Median chênh lệch [CI 95%] | Thắng/thua | Rank-biserial | p Holm 60 |',
        '|---|---|---:|---:|---:|---:|']
    for r in comparisons:
        if r['problem']=='zdt4' and r['algorithm'] in ['NSGA2','DNSGA2']:
            lines.append(f'| {r["algorithm"]} | {r["metric"]} | '
                f'{fmt(r["median_paired_oade_minus_baseline"])} '
                f'[{fmt(r["ci95_median_difference_low"])}, {fmt(r["ci95_median_difference_high"])}] '
                f'| {r["wins"]}/{r["losses"]} | {r["rank_biserial_effect"]:.4f} | {fmt(r["p_holm_60"])} |')
    lines += ['', 'CI median có thể không chứa 0 trong khi Wilcoxon không đạt ngưỡng: '
        'hai phép phân tích nhắm đến đại lượng khác nhau, và CI này chưa hiệu chỉnh. '
        'Phân bố lệch/đuôi lớn cũng giới hạn cách diễn giải Wilcoxon như một kiểm định median. '
        'Giữ kết luận chính theo phép kiểm định đã định, không chọn phép thử sau khi thấy kết quả.', '',
        '## CGDE, SDR-OLS và CE: giới hạn diễn giải', '',
        '- **CGDE ZDT6:** OADE có IGD median thấp hơn 19,10%, nhưng HV median chỉ cao '
        'hơn 0,0256% (0,43804748 so với 0,43793530); p Holm HV = 0,0465056, '
        '19/30 cặp thắng, 11/30 thua. Chênh lệch HV có ý nghĩa ở ngưỡng đã chọn nhưng nhỏ '
        'và sát ngưỡng; không mô tả là cải thiện mạnh.',
        '- **CGDE ZDT4 seed 63:** hai nghiệm cùng F=(0; 6,114447425477259), '
        'bị validator đánh dấu collapsed front. Đây là một run đã chạy xong nhưng không hợp lệ, '
        'không phải run thiếu. Hai endpoint liên quan dùng n=29; những cặp còn lại n=30. '
        'Phân tích nhạy cảm riêng tính chỉ số trên front collapsed vẫn cho OADE thắng cả '
        '30 seed, p thô=1,862645149×10⁻⁹ cho mỗi metric. Dữ liệu chính vẫn giữ quy tắc loại '
        'invalid và không ghi lại IGD/HV vào primary.',
        '- **SDR-OLS:** 148/150 run có HV=0; đây là kết quả theo reference point, '
        'không tự động là lỗi hay collapsed front. Với full local search, D=30 cần '
        '2ND=6.000 FE mỗi lượt, còn D=10 cần 2.000. Từ cấu trúc mã và FE: cap 20.000 '
        'chỉ đủ 3 hoặc 9 vòng GA đầy đủ sau LS, rồi một lượt LS cuối bị giới hạn bởi '
        'ngân sách. Khác biệt hiệu quả có thể liên quan chi phí tìm kiếm này; chưa có '
        'ablation để xác định nguyên nhân. Không phục hồi cap cũ nhằm làm đẹp kết quả.',
        '- **RNSGA2/DNSGA2:** kết quả đo toàn front trên bài tĩnh. RNSGA2 nhắm vùng '
        'ưu tiên, DNSGA2 nhắm môi trường động; điểm kém ở đây không chứng minh thất bại '
        'trên nhiệm vụ gốc.',
        '- **CE-MOEA:** chỉ lõi tìm kiếm liên tục được đo trên ZDT. Các bản tự dựng '
        'dựa trên bài báo công khai và quy ước đã ghi, chưa phải xác nhận tương đương mã tác giả. '
        'Xem [baseline](../protocols/baselines.md) và [giới hạn tái dựng](../protocols/baseline_paper_corrections.md).', '',
        '## Chi phí và convergence', '',
        'OADE runtime median khoảng 7,40–9,06 s/run, NSGA2 2,78–3,80 s/run: '
        'OADE chậm hơn khoảng 1,95–2,84 lần theo từng bài trong môi trường này. '
        'Không suy ra độ phức tạp từ số đo giữa mã Python cục bộ và thư viện pymoo.', '',
        'Convergence lưu ở thời điểm callback sau batch: SDR-OLS ZDT1 có các target '
        '2.000/4.000/6.000 cùng n_eval thực=6.300 và cùng metric. Không được coi đó là '
        'ba phép đo đúng tại 2.000/4.000/6.000 FE. OADE/DNSGA2 thường có 9 checkpoint '
        'vì dừng dưới cap; kết quả cuối dùng final X/F, không lấy checkpoint 90% thay thế. '
        'Không tính AUC hoặc suy luận tốc độ hội tụ từ các target chưa được đo đúng thời điểm.', '',
        '## Phương pháp thống kê và phạm vi kết luận', '',
        'Đơn vị là run theo seed, ghép cùng seed trong từng bài; mỗi bài có 30 lần chạy '
        'mỗi thuật toán. Endpoint là từng bài × đối chứng × metric; các endpoint có chung '
        'OADE và tương quan, không gộp thành các mẫu độc lập. Wilcoxon signed-rank hai phía, '
        'zero_method=wilcox, SciPy method=auto, all-zero p=1. Giữ họ 60 endpoint cho kết luận '
        'chung, alpha=0,05. Holm riêng 30/metric vẫn lưu để đối chiếu, không chọn cách hiệu '
        'chỉnh thuận lợi hơn. Rank-biserial dương thiên về OADE; CI bootstrap là phân tích '
        'bổ sung chưa hiệu chỉnh. Không phát hiện khác biệt không chứng minh tương đương.', '',
        'Có thể kết luận: **trong năm bài ZDT và ngân sách đã đo, OADE bản thống nhất '
        'cải thiện nhiều chỉ số chất lượng so với các cấu hình đối chứng cụ thể, nhưng '
        'độ ổn định ZDT4 chưa tốt hơn NSGA2/DNSGA2 và runtime cao hơn NSGA2**. '
        'Không dùng benchmark này để quy lợi ích riêng cho restart, OBL hay success_rate; '
        'việc đó cần các ablation đã ghép điều kiện. Không suy ra kết quả khác trước sửa '
        'baseline là tác động riêng của một thay đổi: nhiều cơ chế/code đã đổi đồng thời.', '',
        '## Dữ liệu đối chiếu', '',
        '- [Manifest](../../results/experiments/zdt_seven_fixed_oade_v2/study_manifest.json)',
        '- [Audit JSON](../../results/experiments/zdt_seven_fixed_oade_v2/derived/audit.json)',
        '- [35 dòng summary đã đối chiếu](../../results/experiments/zdt_seven_fixed_oade_v2/derived/audited_summary.csv)',
        '- [60 so sánh, thắng/thua, effect và CI](../../results/experiments/zdt_seven_fixed_oade_v2/derived/audited_comparisons.csv)',
        '- [Bảng gốc pipeline](../../results/experiments/zdt_seven_fixed_oade_v2/derived/comparisons.csv)',
        '- [Mã audit có thể chạy lại](../../analysis/audit_zdt_seven_v2.py)', '']
    (ROOT/'docs/reports/zdt_seven_fixed_oade_v2_report.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__ == '__main__':
    main()
