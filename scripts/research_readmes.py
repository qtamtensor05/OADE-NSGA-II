"""Evidence-bound research READMEs, organized by problem rather than pooled claims.

Uses existing summaries and statistical tables; does not fit or rerun tests.
Can read published ZIPs directly when extracted CSVs are absent.
"""
import csv
import io
from pathlib import Path
import zipfile

from csv_archives import ROOT, archive_lookup

OUT = ROOT / 'results/by_problem'
ZDT = ('zdt1', 'zdt2', 'zdt3', 'zdt4', 'zdt6')
TERMS = [
    ('OADE-NSGA-II', 'Tên phương pháp; ID benchmark là OADE_NSGAII.', 'Classic và adaptive được xác định bằng cấu hình/đợt chạy, không bằng ID benchmark.'),
    ('Classic', 'Cấu hình restart cổ điển; ID xác nhận là OADE_FULL.', 'Không dùng từ classic để gọi adaptive.'),
    ('Adaptive', 'Cấu hình restart thích nghi; ID xác nhận là OADE_ADAPTIVE_RESTART.', 'Không suy từ cải thiện chất lượng sang xác nhận cơ chế trigger.'),
    ('IGD', 'Inverted generational distance; thấp hơn tốt hơn.', 'Mean ± SD cho benchmark; median và IQR cho OFAT.'),
    ('HV', 'Hypervolume; cao hơn tốt hơn theo reference point của từng bài.', 'Không so trực tiếp trị số HV giữa các bài toán.'),
    ('OFAT', 'One factor at a time: thay một tham số mỗi lần.', 'Không suy ra tương tác hoặc cấu hình tối ưu từ OFAT.'),
    ('n', 'Một lượt chạy ngẫu nhiên tại một bài toán, thuật toán và seed.', 'Block đối chứng/baseline dùng lại không tạo lượt độc lập mới.'),
]


def rows(path):
    if path.exists():
        return list(csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'), newline='')))
    relative = path.relative_to(ROOT).as_posix()
    archive_name = archive_lookup().get(relative)
    if not archive_name:
        return []
    archive = ROOT / archive_name
    member = path.relative_to(archive.parent).as_posix()
    with zipfile.ZipFile(archive) as bundle:
        return list(csv.DictReader(io.StringIO(bundle.read(member).decode('utf-8-sig'), newline='')))


def summary(base, category):
    return rows(base / category / 'algorithm_benchmark_igd_hv_summary.csv')


def number(value):
    return f'{float(value):.6g}'


def md_table(header, body):
    return ['| ' + ' | '.join(header) + ' |', '| ' + ' | '.join('---' for _ in header) + ' |',
            *['| ' + ' | '.join(str(v) for v in row) + ' |' for row in body], '']


def save(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')


def benchmark_table(data):
    return md_table(['ID thuật toán', 'Hợp lệ/tổng', 'IGD mean ± SD', 'HV mean ± SD', 'Giây/lượt'], [
        [r['algorithm'], f"{r['runs_valid']}/{r['runs_total']}",
         f"{number(r['IGD_mean'])} ± {number(r['IGD_std'])}",
         f"{number(r['HV_mean'])} ± {number(r['HV_std'])}", number(r['runtime_mean'])] for r in data])


def zdt_evidence(problem):
    base = OUT / 'zdt' / problem
    adaptive = {r['algorithm']: r for r in summary(base, 'benchmark_adaptive')}
    classic = {r['algorithm']: r for r in summary(base, 'benchmark_classic')}
    sensitivity = rows(base / 'sensitivity_adaptive/summary.csv')
    return base, adaptive, classic, sensitivity


def sensitivity_sentence(data, lang):
    small = next(r for r in data if r['parameter'] == 'pop_size' and float(r['level']) == 100)
    large = next(r for r in data if r['parameter'] == 'pop_size' and float(r['level']) == 200)
    if lang == 'vi':
        return (f"Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ "
                f"{number(small['IGD_median'])} thành {number(large['IGD_median'])}; median HV đổi từ "
                f"{number(small['HV_median'])} thành {number(large['HV_median'])}.")
    return (f"In OFAT seeds 6000–6029, increasing population from 100 to 200 changed median IGD "
            f"from {number(small['IGD_median'])} to {number(large['IGD_median'])} and median HV "
            f"from {number(small['HV_median'])} to {number(large['HV_median'])}.")


def write_zdt(problem):
    base, adaptive, classic, sensitivity = zdt_evidence(problem)
    oade, nsga = adaptive['OADE_NSGAII'], adaptive['NSGA2']
    nvar = 30 if problem in ('zdt1', 'zdt2', 'zdt3') else 10
    lines = [f'# {problem.upper()}: kết quả OADE-NSGA-II', '',
             f'Trên {problem.upper()}, OADE adaptive đạt IGD trung bình {number(oade["IGD_mean"])} và HV trung bình {number(oade["HV_mean"])}; NSGA2 lần lượt đạt {number(nsga["IGD_mean"])} và {number(nsga["HV_mean"])} trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.', '',
             '## Thiết kế và phạm vi', '',
             f'Bài toán có {nvar} biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.', '',
             'IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.', '',
             '## Benchmark adaptive: 7 thuật toán', ''] + benchmark_table(list(adaptive.values()))
    stats = rows(base / 'benchmark_adaptive/algorithm_benchmark_paired_statistics.csv')
    lines += ['So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.', '']
    lines += md_table(['Chỉ số', 'n cặp', 'p Holm', 'Rank-biserial', 'Kết quả theo OADE'], [
        [r['metric'], r['n_pairs'], number(r['p_adjusted_holm']), number(r['rank_biserial_effect']), r['result']]
        for r in stats if r['comparison_algorithm'] == 'NSGA2'])
    if problem == 'zdt6':
        competitor = adaptive['CGDE_NSGAII']
        lines += [f'Giới hạn đối chứng cần giữ khi đọc kết quả: CGDE_NSGAII có mean IGD {number(competitor["IGD_mean"])} và mean HV {number(competitor["HV_mean"])}. Bởi vậy lợi thế so với NSGA2 không được diễn giải thành ưu thế trước mọi thuật toán trên ZDT6.', '']
        lines += md_table(['Đối chứng', 'Chỉ số', 'n cặp', 'p Holm', 'Kết quả theo OADE'], [
            [r['comparison_algorithm'], r['metric'], r['n_pairs'], number(r['p_adjusted_holm']), r['result']]
            for r in stats if r['comparison_algorithm'] == 'CGDE_NSGAII'])
        lines += ['Kiểm định IGD không phát hiện khác biệt với CGDE_NSGAII, trong khi kiểm định HV ưu thế cho CGDE_NSGAII theo bảng đã lưu. Đây là hai kết quả khác nhau, không phải bằng chứng tương đương trên IGD. [Toàn bộ kiểm định](reports/benchmark_adaptive.md).', '']
    else:
        lines += ['Các đối chứng còn lại và kết quả từng kiểm định được giữ trong [báo cáo benchmark adaptive](reports/benchmark_adaptive.md); không suy rộng kết quả của bài toán này sang bài toán khác.', '']
    lines += ['## Classic và adaptive', '',
              'Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.', '']
    lines += md_table(['Cấu hình', 'IGD mean', 'HV mean'], [
        ['Classic, seed 42–71', number(classic['OADE_NSGAII']['IGD_mean']), number(classic['OADE_NSGAII']['HV_mean'])],
        ['Adaptive, seed 42–71', number(oade['IGD_mean']), number(oade['HV_mean'])]])
    heldout = summary(base, 'restart_confirmation')
    lines += ['Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.', ''] + benchmark_table(heldout)
    lines += ['Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.', '',
              '## Độ nhạy tham số adaptive', '', sensitivity_sentence(sensitivity, 'vi'), '']
    if problem == 'zdt4':
        lines += ['Suy giảm tại population 200 là giới hạn quan trọng của cấu hình ở trần ngân sách này. Chưa có thí nghiệm cô lập nguyên nhân; không suy ra population lớn luôn tốt hơn hoặc restart là nguyên nhân.', '']
    else:
        lines += ['Thay đổi population đồng thời thay đổi số thế hệ khả dụng và độ phân giải tập nghiệm ở ngân sách cố định. Vì vậy chênh lệch IGD không tự đo riêng tốc độ hội tụ.', '']
    selected = [r for r in sensitivity if r['parameter'] in ('pop_size', 'prob_de')]
    lines += md_table(['Tham số', 'Mức', 'Lượt hợp lệ', 'IGD median', 'IGD Q25–Q75', 'HV median', 'Restart hoàn tất'], [
        [r['parameter'], r['level'], r['valid_runs'], number(r['IGD_median']),
         f"{number(r['IGD_q25'])}–{number(r['IGD_q75'])}", number(r['HV_median']), r['restart_completed']] for r in selected])
    lines += ['Mỗi mức có 30 seed ghép cặp. Baseline được dùng lại giữa các bảng tham số, không tính thành lượt thực thi độc lập mới. OFAT chỉ thay một tham số mỗi lần; không đo tương tác và không xác lập một cấu hình tối ưu. F, CR và xác suất DE là giá trị khởi tạo có thể cập nhật trong lượt chạy.', '',
              '## Ablation và bằng chứng bổ sung', '',
              'Ablation thuộc cấu hình classic và khởi tạo uniform chung. Đọc [báo cáo ablation của bài toán](reports/ablation_classic.md) để phân biệt loại bỏ thành phần với đánh giá cấu hình adaptive. [Độ nhạy classic](reports/sensitivity_classic.md) là đợt lịch sử riêng, không gộp với [OFAT adaptive](reports/sensitivity_adaptive.md).', '',
              '## Dữ liệu và tái lập', '',
              '- [CSV của riêng bài toán, tải ZIP](csv_results.zip)',
              '- [Danh mục báo cáo chi tiết](reports/README.md)',
              '- [Manifest CSV và SHA-256](manifest.json)',
              '- [Danh mục tải dữ liệu và lệnh khôi phục](../../../CSV_DOWNLOADS.md)',
              '- [Cấu hình benchmark adaptive](../../../../config/suites/algorithm_benchmark_v2.yaml)',
              '- [Cấu hình benchmark classic](../../../../config/suites/algorithm_benchmark_classic.yaml)',
              '- [Giao thức OFAT](../../../../docs/protocols/zdt_sensitivity.md)', '',
              'Giải nén ZIP cạnh tệp ZIP để khôi phục các thư mục thí nghiệm. Các block đối chứng có provenance khác nhau: block RNSGA2 có manifest thực thi, các block lịch sử khác không được gán ngược môi trường hiện tại. Xem [provenance ZDT](../../../provenance/zdt_composition.json). Chưa có khoảng tin cậy cho hiệu ứng ghép cặp trong các bảng hiện tại.', '',
              '[Trở về ZDT](../README.md)', '']
    save(base / 'README.md', lines)


def write_extension(family, problem):
    base = OUT / family / problem
    available = [(category, summary(base, category)) for category in ('benchmark_dtlz', 'benchmark_wfg_m2', 'benchmark_wfg_scaling')]
    available = [(c, data) for c, data in available if data]
    lines = [f'# {problem.upper()}: báo cáo riêng', '',
             'Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.', '',
             'IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.', '']
    for category, data in available:
        oade = next(r for r in data if r['algorithm'] == 'OADE_NSGAII')
        lines += [f'## {category}', '',
                  f"Đợt này có {len(data)} thuật toán. OADE_NSGAII có {oade['runs_valid']}/{oade['runs_total']} lượt hợp lệ, mean IGD {number(oade['IGD_mean'])} và mean HV {number(oade['HV_mean'])}. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.", '',
                  f"Cấu hình lưu trong bảng: n_var={oade['n_var']}, n_obj={oade['n_obj']}. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.", '']
        lines += benchmark_table(data)
        raw = rows(base / category / 'algorithm_benchmark_raw_runs.csv')
        oade_raw = [r for r in raw if r['algorithm'] == 'OADE_NSGAII']
        zero_hv = sum(float(r['HV']) == 0 for r in oade_raw)
        if zero_hv:
            lines += [f'Giới hạn chất lượng của riêng cấu hình này: OADE có **{zero_hv}/{len(oade_raw)} lượt HV = 0** theo điểm tham chiếu đã dùng. HV = 0 không tự đồng nghĩa với output không hợp lệ theo kiểm tra cấu trúc; cần giữ hai tiêu chí tách biệt.', '']
        lines += [f'[Báo cáo và toàn bộ kiểm định của đợt này](reports/{category}.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.', '']
    lines += ['## Giới hạn và bổ sung', '',
              'Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.', '',
              'Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.', '',
              '## Nguồn của bài toán', '', '- [Tải CSV dạng ZIP](csv_results.zip)', '- [Manifest và SHA-256](manifest.json)',
              '- [Danh mục báo cáo](reports/README.md)', f'- [Trở về {family.upper()}](../README.md)', '']
    save(base / 'README.md', lines)


def family_index(family, problems):
    lines = [f'# {family.upper()}: đọc theo từng bài toán', '',
             'Chọn đúng bài toán và số mục tiêu. Mỗi README trình bày kết quả, điều kiện thử và giới hạn riêng; không có bảng thắng/thua gộp giữa các bài.', '']
    lines += md_table(['Bài toán', 'Báo cáo chính', 'Báo cáo thí nghiệm', 'CSV'], [
        [p.upper(), f'[README]({p}/README.md)', f'[Danh mục]({p}/reports/README.md)', f'[ZIP]({p}/csv_results.zip)'] for p in problems])
    lines += ['[Trở về mục lục nghiên cứu](../README.md)', '']
    save(OUT / family / 'README.md', lines)


def root_protocol(vi):
    lines = [('## Thiết kế nghiên cứu và cách đọc' if vi else '## Study design and reading guide'), '',
             ('OADE-NSGA-II kết hợp tạo ứng viên DE theo lân cận, cập nhật F/CR trực tuyến, bổ sung nghiệm đối lập định kỳ và lựa chọn môi trường NSGA-II. Classic dùng restart cổ điển; adaptive bổ sung điều kiện đa dạng và thay thế cục bộ. Thiết kế thuật toán và bằng chứng về đóng góp từng thành phần được đọc tách biệt.' if vi else
              'OADE-NSGA-II combines neighborhood-based DE offspring, online F/CR updates, periodic opposition-based candidates and NSGA-II environmental selection. Classic uses the original restart; adaptive adds diversity conditions and local replacement. Algorithm design and evidence for individual component contributions are interpreted separately.'), '']
    lines += md_table(['Thành phần' if vi else 'Item', 'Thiết lập' if vi else 'Specification'], [
        ['Benchmark ZDT', '7 algorithms; 30 paired seeds 42–71; population 100; evaluation cap 20,000'],
        ['ZDT1 / ZDT2 / ZDT3', '30 variables; 2 objectives'],
        ['ZDT4 / ZDT6', '10 variables; 2 objectives'],
        ['Restart confirmation', 'Classic / no restart / adaptive; 30 paired seeds 1000–1029'],
        ['Adaptive OFAT', '9 parameters; 19 unique configurations; 30 seeds 6000–6029 per problem/configuration'],
        ['Metrics', 'IGD ↓; HV ↑; mean ± sample SD for benchmarks; median and Q25–Q75 for OFAT']])
    lines += [('Các bảng dưới đây báo cáo từng bài toán. Holm giữ nguyên họ kiểm định gốc; các block đối chứng dùng chung không được đếm lại thành lượt chạy mới. Khởi tạo uniform chung trong benchmark bỏ qua Sobol/OBL khởi tạo độc lập. Runtime là thời gian của bản triển khai đã đo, không phải độ phức tạp độc lập phần cứng.' if vi else
               'Tables below report individual problems. Holm corrections retain their original families; reused comparator blocks are not new independent runs. Common uniform benchmark initialization bypasses standalone initial Sobol/OBL. Runtime describes the measured implementation, rather than hardware-independent complexity.'), '',
              '![Classic versus adaptive mean IGD by ZDT problem](results/figures/benchmark_v2_v1_vs_v2_delta.png)', '',
              ('**Hình 1. Classic và adaptive trên từng bài ZDT.** Mỗi cặp cột là mean IGD của 30 seed benchmark. Phần trăm trên hình là chênh lệch mô tả giữa hai cấu hình, không cô lập nguyên nhân do restart.' if vi else
               '**Figure 1. Classic and adaptive on each ZDT problem.** Each pair shows mean IGD over 30 benchmark seeds. Percentages describe configuration differences and do not isolate a restart mechanism.'), '']
    return lines


def root_problem_details(problem, vi):
    base, adaptive, classic, sensitivity = zdt_evidence(problem)
    lines = [('**Đối chứng: mean ± SD, 30 lượt/thuật toán.**' if vi else '**Comparators: mean ± SD, 30 runs per algorithm.**'), '']
    lines += md_table(['Algorithm', 'IGD ↓', 'HV ↑', 's/run'], [
        [r['algorithm'], f"{number(r['IGD_mean'])} ± {number(r['IGD_std'])}",
         f"{number(r['HV_mean'])} ± {number(r['HV_std'])}", number(r['runtime_mean'])] for r in adaptive.values()])
    a, c = adaptive['OADE_NSGAII'], classic['OADE_NSGAII']
    tests = rows(base / 'benchmark_adaptive/algorithm_benchmark_paired_statistics.csv')
    pvals = {r['metric']: number(r['p_adjusted_holm']) for r in tests if r['comparison_algorithm'] == 'NSGA2'}
    if vi:
        lines += [f"**Classic → adaptive, seed 42–71:** mean IGD {number(c['IGD_mean'])} → {number(a['IGD_mean'])}; mean HV {number(c['HV_mean'])} → {number(a['HV_mean'])}. So với NSGA2, kiểm định ghép cặp của adaptive có p Holm IGD = {pvals['IGD']}, HV = {pvals['HV']}. Chênh lệch classic–adaptive ở đây là mô tả.", '']
    else:
        lines += [f"**Classic → adaptive, seeds 42–71:** mean IGD {number(c['IGD_mean'])} → {number(a['IGD_mean'])}; mean HV {number(c['HV_mean'])} → {number(a['HV_mean'])}. Adaptive versus NSGA2 paired tests gave Holm p = {pvals['IGD']} for IGD and {pvals['HV']} for HV. The classic–adaptive difference here is descriptive.", '']
    heldout = summary(base, 'restart_confirmation')
    lines += [('**Xác nhận restart, seed 1000–1029:** mean của 30 lượt/biến thể.' if vi else '**Restart confirmation, seeds 1000–1029:** means of 30 runs per variant.'), '']
    names = {'OADE_FULL': 'Classic', 'OADE_NO_RESTART': 'No restart', 'OADE_ADAPTIVE_RESTART': 'Adaptive'}
    lines += md_table(['Variant', 'IGD mean ↓', 'HV mean ↑'], [
        [names[r['algorithm']], number(r['IGD_mean']), number(r['HV_mean'])] for r in heldout])
    lines += [('**Độ nhạy adaptive.** ' if vi else '**Adaptive sensitivity.** ') + sensitivity_sentence(sensitivity, 'vi' if vi else 'en'), '']
    low = next(r for r in sensitivity if r['parameter'] == 'prob_de' and float(r['level']) == 0.5)
    high = next(r for r in sensitivity if r['parameter'] == 'prob_de' and float(r['level']) == 0.8)
    if vi:
        lines += [f"Tăng xác suất DE khởi tạo từ 0,5 lên 0,8 làm median IGD đổi từ {number(low['IGD_median'])} thành {number(high['IGD_median'])}, median HV từ {number(low['HV_median'])} thành {number(high['HV_median'])}. Đây là đáp ứng OFAT của bài toán này, chưa phải cấu hình tối ưu hoặc bằng chứng tương tác.", '']
    else:
        lines += [f"Increasing initial DE probability from 0.5 to 0.8 changed median IGD from {number(low['IGD_median'])} to {number(high['IGD_median'])} and median HV from {number(low['HV_median'])} to {number(high['HV_median'])}. These are problem-specific OFAT responses, not an optimal configuration or an interaction analysis.", '']
    variant = 'OADE_NO_OBL' if problem == 'zdt4' else 'OADE_NO_RESTART'
    ablation = rows(base / 'ablation_classic/algorithm_benchmark_paired_statistics.csv')
    selected = [r for r in ablation if r['comparison_algorithm'] == variant]
    def meaning(result):
        return {'comparison_better': 'ưu thế cho biến thể loại bỏ' if vi else 'favors removal',
                'reference_better': 'ưu thế cho Full OADE' if vi else 'favors Full OADE',
                'no_significant_difference': 'chưa phát hiện khác biệt' if vi else 'no difference detected'}.get(result, result)
    details = '; '.join(f"{r['metric']}: {meaning(r['result'])}, p Holm = {number(r['p_adjusted_holm'])}" for r in selected)
    lines += [(f'**Ablation classic ({variant} so với Full OADE).** {details}. Không chuyển kết luận này thành ablation của cấu hình adaptive.' if vi else
               f'**Classic ablation ({variant} versus Full OADE).** {details}. This is not an ablation of the adaptive configuration.'), '']
    return lines


def root_zdt_figures(vi):
    lines = [('## Minh họa: restart, hội tụ, ablation và độ nhạy ZDT' if vi else '## Visual evidence: ZDT restart, convergence, ablation and sensitivity'), '',
             ('Các hình dùng lại trực tiếp kết quả đã lưu. Mỗi ô hoặc cặp hàng giữ định danh bài toán riêng; không dùng tổng thắng/thua để thay cho kết luận từng bài.' if vi else
              'These figures reuse existing research outputs. Each panel or row pair retains its problem identity; pooled win counts do not replace problem-specific conclusions.'), '']
    for path, en, vn in [
        ('results/figures/restart_direct_comparison.png',
         '**Figure 2. Held-out restart distributions.** IGD and HV are shown separately for each problem and variant (30 seeds, 1000–1029). No-restart and adaptive overlap closely; final metrics alone do not establish trigger operation.',
         '**Hình 2. Phân bố xác nhận restart.** IGD và HV được tách theo bài toán và biến thể, mỗi nhóm 30 seed 1000–1029. No-restart và adaptive gần trùng nhau; chỉ số cuối không tự chứng minh trigger đã hoạt động.'),
        ('results/figures/restart_convergence.png',
         '**Figure 3. Within-budget convergence.** Curves show median IGD and shaded IQR for each problem. Panels have different vertical scales. The trajectories compare outcomes, not observed trigger counts.',
         '**Hình 3. Hội tụ trong ngân sách.** Đường biểu diễn median IGD, vùng tô là IQR theo từng bài. Các ô có thang tung khác nhau. Đường hội tụ so sánh kết quả, không phải số lần kích hoạt trigger.'),
        ('results/figures/ablation_effect_heatmap.png',
         '**Figure 4. Classic component ablation.** Blue favors removing the named component; orange favors Full OADE. Asterisks mark Holm-adjusted p < 0.05. The ZDT4 OBL result contrasts with restart removals on ZDT1–3; there is no uniform component benefit.',
         '**Hình 4. Ablation thành phần classic.** Xanh ưu thế cho loại bỏ thành phần; cam ưu thế cho Full OADE. Dấu sao là p Holm < 0,05. Vai trò OBL trên ZDT4 khác với loại bỏ restart trên ZDT1–3; không có lợi ích đồng đều của mọi thành phần.'),
        ('results/experiments/zdt_sensitivity_ofat_v1/figures/prob_de_paired.png',
         '**Figure 5. Initial DE probability sensitivity.** Bars show median improvement over 0.5 using 30 matched seeds; whiskers show Q25–Q75, not confidence intervals. Positive values mean improvement for both IGD and HV. Each problem has its own scale; median paired improvements differ from ratios of marginal medians quoted above.',
         '**Hình 5. Độ nhạy xác suất DE khởi tạo.** Cột là median cải thiện so với mức 0,5 qua 30 cặp seed; thanh mảnh là Q25–Q75, không phải khoảng tin cậy. Giá trị dương là cải thiện cho cả IGD/HV. Mỗi bài có thang riêng; median thay đổi từng cặp khác với tỷ lệ giữa các median biên nêu ở trên.')]:
        lines += [f'![{Path(path).stem}]({path})', '', vn if vi else en, '']
    lines += [('Baseline OFAT được dùng lại giữa các bảng tham số. Khi thay population ở trần đánh giá cố định, cả số thế hệ khả dụng và độ phân giải tập nghiệm đều thay đổi. Các đáp ứng trên cần thí nghiệm xác nhận trước khi chọn lại cấu hình mặc định.' if vi else
               'OFAT baseline runs are reused between parameter tables. Under a fixed evaluation cap, population changes alter both available generations and solution-set resolution. These responses require confirmation before changing default settings.'), '']
    return lines


def root_extension(family, problems, vi):
    lines = []
    body = []
    for problem in problems:
        base = OUT / family / problem
        category = 'benchmark_dtlz' if family == 'dtlz' else ('benchmark_wfg_m2' if summary(base, 'benchmark_wfg_m2') else 'benchmark_wfg_scaling')
        data = summary(base, category)
        by_id = {r['algorithm']: r for r in data}
        a, n = by_id['OADE_NSGAII'], by_id['NSGA2']
        body.append([problem.upper(), len(data), number(a['IGD_mean']), number(n['IGD_mean']), number(a['HV_mean']),
                     f'[Report](results/by_problem/{family}/{problem}/README.md)'])
    lines += md_table(['Problem', 'Algorithms', 'IGD OADE ↓', 'IGD NSGA2 ↓', 'HV OADE ↑', 'Detail'], body)
    if family == 'dtlz':
        lines += [('**Giới hạn cần thấy ngay:** ở DTLZ1_M5, OADE có 17/30 lượt HV = 0; ở DTLZ3_M5 là 30/30 lượt. Đây là giới hạn chất lượng theo điểm tham chiếu, không đồng nghĩa lỗi cấu trúc output. Số cặp hợp lệ của từng đối chứng được ghi trong báo cáo riêng.' if vi else
                   '**Visible failure boundary:** OADE had HV = 0 in 17/30 DTLZ1_M5 runs and all 30 DTLZ3_M5 runs. These are reference-point quality outcomes, not necessarily structural output failures. Valid matched-pair counts are reported per comparison.'), '',
                  '![DTLZ objective-count scaling](results/figures/dtlz1_4_scaling_diagnosis.png)', '',
                  ('**Hình 6. DTLZ theo số mục tiêu.** Các ô tách DTLZ1, DTLZ3, so sánh DTLZ2 và HV DTLZ4. Thang IGD log cho thấy khó khăn khi tăng số mục tiêu; không lấy kết quả ZDT để thay cho bằng chứng trên DTLZ.' if vi else
                   '**Figure 6. DTLZ objective-count scaling.** Panels separately show DTLZ1, DTLZ3, DTLZ2 comparisons and DTLZ4 HV. Log-scale IGD exposes the difficulty of increasing the objective count; ZDT results are not substituted for DTLZ evidence.'), '']
    else:
        lines += [('Các hàng M=2 dùng benchmark đủ 7 thuật toán; M=3/5 dùng tập compact 5 thuật toán. Không cộng các block M=2 dùng chung thành lượt độc lập mới. Mean trong bảng không phải median được vẽ ở hình bên dưới.' if vi else
                   'M=2 rows use the seven-algorithm benchmark; M=3/5 use the five-algorithm compact study. Shared M=2 blocks are not new independent runs. Means in the table are not the medians plotted below.'), '',
                  '![WFG bi-objective comparator profiles](results/figures/wfg_m2_7algo_profile.png)', '',
                  ('**Hình 7. Đối chứng WFG hai mục tiêu.** Ô a giữ hiệu ứng IGD/HV riêng cho WFG1/4/6/9; ô b trình bày phân bố WFG9. Ô c là bối cảnh chi phí tổng hợp trong hình gốc, không thay cho kết quả từng hàng ở bảng trên và không áp dụng cho M=3/5.' if vi else
                   '**Figure 7. Bi-objective WFG comparator profiles.** Panel a retains separate IGD/HV effects for WFG1/4/6/9; panel b shows WFG9 run distributions. Panel c is the original figure’s aggregate cost context, not a substitute for the problem rows above or evidence for M=3/5.'), '']
    return lines


def root_strengths_and_limits(vi):
    if vi:
        lines = ['## Ưu điểm ghi nhận trên ZDT', '',
                 'Các ưu điểm sau là kết quả của bản triển khai và điều kiện đã thử trên ZDT1/2/3/4/6. Đọc chúng cùng các bảng và hình phía trên; không chuyển thành khẳng định ưu thế trên mọi lớp bài toán.', '']
        lines += md_table(['Ưu điểm', 'Bằng chứng hiện có', 'Phạm vi diễn giải'], [
            ['Chất lượng nghiệm so với NSGA2', 'Adaptive có mean IGD thấp hơn và mean HV cao hơn NSGA2 trong từng bài ZDT đã báo cáo; các kiểm định ghép cặp được giữ theo bài.', '30 seed 42–71, population 100, trần 20.000 đánh giá; không suy ra vượt mọi đối chứng.'],
            ['Giảm phân tán so với classic trên ZDT1–3', 'SD của IGD trong benchmark adaptive thấp hơn classic trên riêng ZDT1, ZDT2 và ZDT3; hình xác nhận cho thấy các đuôi chất lượng kém của classic.', 'Lợi ích ở mức cấu hình; no-restart gần trùng adaptive nên chưa quy nguyên nhân cho trigger.'],
            ['Có bằng chứng thành phần cụ thể trên ZDT4', 'Ablation classic cho thấy giữ OBL tốt hơn loại OBL trên cả IGD và HV sau hiệu chỉnh Holm.', 'Đánh giá bổ sung OBL định kỳ với khởi tạo uniform chung, không phải lợi ích của Sobol/OBL khởi tạo.'],
            ['Có dữ liệu để kiểm tra độ nhạy và tái lập', 'Benchmark ghép seed, thí nghiệm xác nhận riêng, OFAT adaptive, manifest và ZIP có SHA-256 đều đã có.', 'Đây là ưu điểm của hồ sơ thực nghiệm; không tự tạo bảo đảm về hội tụ hoặc tối ưu.']])
        lines += ['## Hạn chế và giới hạn kết luận', '']
        lines += md_table(['Hạn chế', 'Biểu hiện trên ZDT', 'Hệ quả khi diễn giải'], [
            ['Không vượt mọi thuật toán', 'ZDT6: IGD chưa phát hiện khác biệt với CGDE_NSGAII, trong khi HV ưu thế cho CGDE_NSGAII.', 'Báo cáo riêng từng chỉ số và đối chứng; không kết luận thắng tuyệt đối.'],
            ['Chi phí chạy cao hơn đối chứng đơn giản', 'OADE adaptive chậm hơn NSGA2/DNSGA2 trong các hàng runtime ZDT đã đo.', 'Lợi ích chất lượng cần được cân nhắc cùng thời gian và bản triển khai; không suy ra độ phức tạp lý thuyết từ runtime.'],
            ['Nhạy với cấu hình và ngân sách', 'ZDT4 suy giảm mạnh tại population 200 ở trần 20.000 đánh giá; tăng population không có lợi đồng đều.', 'Không chọn một mức population lớn làm mặc định cho mọi bài.'],
            ['Chưa cô lập giá trị của restart adaptive', 'Kết quả adaptive và no-restart gần trùng trong xác nhận; đợt này không lưu telemetry trigger.', 'Cần seed mới và số lần kiểm tra/kích hoạt restart trước khi khẳng định cơ chế.'],
            ['OFAT chưa đo tương tác hoặc xác nhận tối ưu', 'Mỗi lần chỉ thay một tham số quanh baseline; F/CR và xác suất DE có thể cập nhật trong lượt chạy.', 'Các mức có lợi là ứng viên xác nhận, không phải cấu hình tối ưu tổng quát.'],
            ['Chưa kiểm tra riêng lợi ích khởi tạo', 'Benchmark truyền quần thể uniform chung, bỏ qua khởi tạo Sobol/OBL độc lập.', 'Không dùng ablation OBL định kỳ để khẳng định lợi ích khởi tạo.'],
            ['Bất định và provenance còn thiếu', 'Chưa có CI của hiệu ứng ghép cặp trong các bảng hiện tại; một số block lịch sử thiếu manifest thực thi.', 'SD/IQR không thay cho CI; không gán môi trường hiện tại cho những lượt chạy lịch sử.'],
            ['Phạm vi nghiên cứu chính còn hẹp', 'Trọng tâm hiện tại là ZDT liên tục hai mục tiêu đã có dữ liệu; ZDT5 không nằm trong bộ đang báo cáo.', 'Chưa xác lập khả năng tổng quát sang nhiều mục tiêu, ràng buộc, biến rời rạc hoặc bài toán thực tế.']])
        lines += ['## Định hướng: hoàn thiện ZDT trước, mở rộng sau', '',
                  '**Ưu tiên hiện tại là củng cố kết luận trên ZDT.** DTLZ/WFG đã có một số kết quả mở rộng và vẫn được giữ ở các mục bên dưới, nhưng chưa thay thế trọng tâm nghiên cứu ZDT hoặc xác lập ưu thế tổng quát.', '']
        lines += md_table(['Giai đoạn', 'Việc cần làm', 'Bằng chứng cần bổ sung'], [
            ['1. Hoàn thiện ZDT', 'Xác nhận adaptive so với no-restart; kiểm tra ứng viên tham số và giới hạn population trên ZDT4.', 'Seed mới, telemetry restart, chi phí đánh giá restart, CI ghép cặp và phân tích chất lượng/chi phí.'],
            ['2. Mở rộng DTLZ/WFG', 'Bổ sung so sánh và ablation theo từng bài, từng số mục tiêu; giữ các đợt đã có làm bằng chứng bổ sung.', 'Đối chứng được kiểm chứng, giao thức ngân sách rõ ràng, xử lý output không hợp lệ và kiểm tra khả năng mở rộng.'],
            ['3. Các lớp bài toán khác', 'Lần lượt xét bài toán có ràng buộc, biến rời rạc hoặc bài toán ứng dụng khi xác định được mục tiêu đánh giá.', 'Giao thức và đối chứng phù hợp từng lớp; không chuyển trực tiếp cấu hình hoặc kết luận ZDT.']])
        lines += ['Đây là định hướng nghiên cứu, không phải các thí nghiệm đã hoàn tất. Kết quả mới sẽ được bổ sung vào đúng thư mục bài toán, kèm cấu hình, seed, ngân sách, manifest và báo cáo riêng. [Kế hoạch bằng chứng chi tiết](docs/protocols/followup_experiments.md).', '']
        return lines
    lines = ['## Strengths observed on ZDT', '',
             'These strengths concern the implemented configurations on ZDT1/2/3/4/6 under the reported conditions. They accompany the problem-specific tables and figures, rather than establish superiority across problem classes.', '']
    lines += md_table(['Strength', 'Current evidence', 'Interpretation boundary'], [
        ['Solution quality versus NSGA2', 'Adaptive has lower mean IGD and higher mean HV than NSGA2 in each reported ZDT problem; paired tests remain problem-specific.', '30 seeds 42–71, population 100, 20,000-evaluation cap; not superiority over every comparator.'],
        ['Lower dispersion than classic on ZDT1–3', 'Adaptive benchmark IGD SD is lower than classic separately on ZDT1, ZDT2 and ZDT3; held-out distributions expose poor-quality classic tails.', 'A configuration-level benefit; near-overlap with no-restart prevents attribution to the adaptive trigger.'],
        ['Specific component evidence on ZDT4', 'Classic ablation favors retaining OBL over removing it for both IGD and HV after Holm correction.', 'Periodic OBL under common uniform initialization, not standalone initial Sobol/OBL.'],
        ['Evidence for sensitivity checks and reproduction', 'Matched-seed benchmarks, separate confirmation seeds, adaptive OFAT, manifests and SHA-256 ZIP records are available.', 'A strength of the experimental record, not a convergence or optimality guarantee.']])
    lines += ['## Limitations and claim boundaries', '']
    lines += md_table(['Limitation', 'ZDT evidence or design boundary', 'Consequence'], [
        ['Not better than every algorithm', 'ZDT6: no IGD difference detected from CGDE_NSGAII, while HV favors CGDE_NSGAII.', 'Retain metric- and comparator-specific conclusions.'],
        ['Runtime overhead', 'Adaptive OADE is slower than NSGA2/DNSGA2 in the measured ZDT runtime rows.', 'Assess quality alongside implementation-specific cost; runtime does not establish theoretical complexity.'],
        ['Configuration and budget sensitivity', 'ZDT4 deteriorates strongly at population 200 under the 20,000-evaluation cap.', 'Larger populations are not a universally beneficial default.'],
        ['Adaptive restart value remains unisolated', 'Adaptive and no-restart nearly overlap in confirmation; trigger telemetry was not saved.', 'Fresh seeds and restart checks/activations are needed for a mechanism claim.'],
        ['OFAT does not establish interactions or optimality', 'One parameter changes around baseline; F/CR and DE probability can update within a run.', 'Favorable levels are confirmation candidates, not a general optimum.'],
        ['Initialization benefit remains untested', 'Benchmark populations use common uniform initialization, bypassing standalone Sobol/OBL.', 'Periodic-OBL ablation does not establish an initialization benefit.'],
        ['Uncertainty and provenance gaps', 'Current tables lack paired-effect CIs; some historical blocks lack execution manifests.', 'SD/IQR are not CIs; current environments cannot be assigned retrospectively.'],
        ['Limited primary scope', 'The current focus is the reported continuous bi-objective ZDT problems; ZDT5 is not included.', 'Generalization to more objectives, constraints, discrete variables or applications is not established.']])
    lines += ['## Research direction: consolidate ZDT, then extend', '',
              '**The current priority is to strengthen the ZDT conclusions.** Existing DTLZ/WFG extension results remain below as supplementary evidence. They do not replace the ZDT focus or establish general superiority.', '']
    lines += md_table(['Stage', 'Work to prioritize', 'Evidence to add'], [
        ['1. Consolidate ZDT', 'Confirm adaptive versus no-restart, candidate parameter settings and the ZDT4 population boundary.', 'Fresh seeds, restart telemetry/evaluation cost, paired-effect CIs and quality–cost analysis.'],
        ['2. Extend DTLZ/WFG', 'Add comparisons and ablations per problem and objective count; retain existing batches as supplementary evidence.', 'Verified comparators, explicit budgets, invalid-output handling and scaling checks.'],
        ['3. Other problem classes', 'Consider constrained, discrete or application problems once their evaluation objective is defined.', 'Task-appropriate protocols and comparators, without directly transferring ZDT settings or claims.']])
    lines += ['This is a research direction, not a list of completed experiments. New evidence will be added to its own problem folder with configuration, seeds, budget, manifest and a separate report. See the [detailed evidence plan](docs/protocols/followup_experiments.md).', '']
    return lines


def root_readme(lang, families):
    vi = lang == 'vi'
    lines = ['# OADE-NSGA-II', '',
             '**Ngôn ngữ:** [English](README.md) | **Tiếng Việt**' if vi else '**Language:** **English** | [Tiếng Việt](README.vi.md)', '',
             'Dự án đánh giá việc kết hợp differential evolution thích nghi và học đối lập trong khung NSGA-II. Nghiên cứu hiện ưu tiên ZDT. Kết quả được trình bày theo từng bài toán, với đối chứng, cấu hình classic/adaptive và giới hạn suy luận riêng.' if vi else
             'This project evaluates adaptive differential evolution and opposition-based learning within NSGA-II. ZDT is the current research priority. Results are reported separately for each problem, including comparator performance, classic/adaptive configurations and inference boundaries.', '',
             '## ZDT: trọng tâm nghiên cứu' if vi else '## ZDT: primary research focus', '',
             'Mỗi bài dưới đây có báo cáo benchmark 7 thuật toán, so sánh classic/adaptive, xác nhận restart, ablation và độ nhạy tham số. Chọn bài toán để đọc đầy đủ bảng số liệu và kiểm định.' if vi else
             'Each problem has reports for the seven-algorithm benchmark, classic/adaptive comparison, restart confirmation, ablation and parameter sensitivity. Open the problem README for its full tables and tests.', '']
    # The root README is a readable research summary, not only a link directory.
    insert = lines.index('## ZDT: trọng tâm nghiên cứu' if vi else '## ZDT: primary research focus')
    lines[insert:insert] = root_protocol(vi)
    for problem in ZDT:
        base, adaptive, classic, sensitivity = zdt_evidence(problem)
        oade, nsga = adaptive['OADE_NSGAII'], adaptive['NSGA2']
        prefix = f'results/by_problem/zdt/{problem}'
        lines += [f'### {problem.upper()}', '']
        if vi:
            lines += [f"Ở benchmark seed 42–71, mean IGD của OADE adaptive là **{number(oade['IGD_mean'])}**, so với **{number(nsga['IGD_mean'])}** của NSGA2. Đây là kết quả của riêng {problem.upper()}, với 30 lượt/thuật toán và trần 20.000 đánh giá.", '']
        else:
            lines += [f"In benchmark seeds 42–71, adaptive OADE had a mean IGD of **{number(oade['IGD_mean'])}**, compared with **{number(nsga['IGD_mean'])}** for NSGA2. These results apply to {problem.upper()}, with 30 runs per algorithm and a 20,000-evaluation cap.", '']
        if problem == 'zdt4':
            lines += [('OFAT ghi nhận suy giảm chất lượng ở population 200; giới hạn này được giữ trong báo cáo chính của ZDT4.' if vi else 'OFAT recorded a loss of solution quality at population 200; this boundary remains visible in the ZDT4 report.'), '']
        if problem == 'zdt6':
            lines += [('Kiểm định IGD không phát hiện khác biệt với CGDE_NSGAII, còn HV ưu thế cho CGDE_NSGAII. Lợi thế so với NSGA2 không đồng nghĩa vượt mọi thuật toán.' if vi else 'The IGD test detected no difference from CGDE_NSGAII, whereas HV favored CGDE_NSGAII. The comparison with NSGA2 does not establish superiority over every algorithm.'), '']
        lines += root_problem_details(problem, vi)
        labels = ['Báo cáo chính', 'Classic/adaptive', 'Độ nhạy', 'CSV ZIP'] if vi else ['Problem report', 'Classic/adaptive', 'Sensitivity', 'CSV ZIP']
        paths = ['README.md', 'reports/classic_vs_adaptive.md', 'reports/sensitivity_adaptive.md', 'csv_results.zip']
        lines += [' · '.join(f'[{label}]({prefix}/{path})' for label, path in zip(labels, paths)), '']
    lines += root_zdt_figures(vi)
    lines += root_strengths_and_limits(vi)
    for family in ('dtlz', 'wfg'):
        lines += [f'## {family.upper()}: ' + ('bổ sung theo từng bài toán' if vi else 'incremental extension by problem'), '',
                  ('Mỗi cấu hình số mục tiêu có hồ sơ riêng. Các kết quả hiện có được giữ tách biệt để tiếp tục chạy và bổ sung.' if vi else 'Each objective-count configuration has its own record. Existing results remain separate for incremental extension.'), '']
        lines += root_extension(family, families[family], vi)
    lines += [('## Cách đọc bằng chứng' if vi else '## Reading the evidence'), '',
              ('Benchmark dùng mean ± SD; độ nhạy adaptive dùng median và IQR (Q25–Q75). IGD thấp hơn và HV cao hơn là tốt hơn theo bài toán. Các phép Wilcoxon ghép cặp và hiệu chỉnh Holm giữ nguyên họ kiểm định gốc, dù báo cáo đã tách theo bài.' if vi else
               'Benchmarks report mean ± SD; adaptive sensitivity reports median and IQR (Q25–Q75). Lower IGD and higher HV indicate better quality within a problem. Paired Wilcoxon tests retain their original Holm correction families after reports are split.'), '',
              ('Classic và adaptive là hai cấu hình OADE; sáu block đối chứng được dùng chung giữa hai benchmark ZDT. Thí nghiệm restart seed 1000–1029 và OFAT seed 6000–6029 được đọc riêng. Chất lượng cuối không tự chứng minh cơ chế restart; OFAT không đánh giá tương tác tham số.' if vi else
               'Classic and adaptive are two OADE configurations; the six comparator blocks are reused between the ZDT benchmarks. Restart seeds 1000–1029 and OFAT seeds 6000–6029 are interpreted separately. Final quality does not itself establish the restart mechanism, and OFAT does not evaluate parameter interactions.'), '',
              ('## Tải dữ liệu và chạy lại' if vi else '## Data access and reproduction'), '',
              ('CSV được phân phối trong ZIP. Báo cáo Markdown và hình có thể xem trực tiếp. [Danh mục tải và SHA-256](results/CSV_DOWNLOADS.md).' if vi else
               'CSVs are distributed as ZIP bundles. Markdown reports and figures can be read directly. See the [download index and SHA-256 records](results/CSV_DOWNLOADS.md).'), '',
              '```powershell', 'python -m venv .venv', r'.venv\Scripts\python.exe -m pip install -e .',
              r'.venv\Scripts\python.exe scripts/csv_archives.py restore', '```', '',
              ('Tái lập benchmark adaptive ZDT vào thư mục mới:' if vi else 'Reproduce the adaptive ZDT benchmark in a new directory:'), '',
              '```powershell', r'.venv\Scripts\python.exe main.py benchmark --config config/suites/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2', '```', '',
              ('Sau khi bổ sung dữ liệu nguồn, tái tạo hồ sơ và đóng gói:' if vi else 'After updating source evidence, regenerate problem reports and bundles:'), '',
              '```powershell', r'.venv\Scripts\python.exe scripts/organize_by_problem.py', r'.venv\Scripts\python.exe scripts/csv_archives.py pack', '```', '',
              ('## Tài liệu phương pháp' if vi else '## Methods documentation'), '',
              '- [Baseline identities and citations](docs/protocols/baselines.md)',
              '- [Experiment registry](docs/protocols/experiment_registry.md)',
              '- [Reproducibility](docs/protocols/reproducibility.md)',
              '- [Documentation index](docs/index.md)', '']
    save(ROOT / ('README.vi.md' if vi else 'README.md'), lines)


def generate_readmes():
    families = {family: sorted(p.parent.name for p in (OUT / family).glob('*/manifest.json')) for family in ('zdt', 'dtlz', 'wfg')}
    for problem in families['zdt']:
        write_zdt(problem)
    for family in ('dtlz', 'wfg'):
        for problem in families[family]:
            write_extension(family, problem)
    for family, problems in families.items():
        family_index(family, problems)
    root_readme('en', families)
    root_readme('vi', families)
    lines = ['# Hồ sơ nghiên cứu theo bài toán', '',
             'ZDT là trọng tâm hiện tại. Mỗi bài toán có một báo cáo chính và các báo cáo thí nghiệm riêng. DTLZ/WFG là phần mở rộng được bổ sung theo từng cấu hình. Không cộng lượt chạy hoặc kết quả kiểm định giữa các bảng để tạo một kết luận chung.', '']
    for family, problems in families.items():
        lines += [f'## {family.upper()}', '']
        lines += md_table(['Bài toán', 'Báo cáo chính', 'Thí nghiệm', 'CSV'], [
            [p.upper(), f'[README]({family}/{p}/README.md)', f'[Báo cáo]({family}/{p}/reports/README.md)', f'[ZIP]({family}/{p}/csv_results.zip)'] for p in problems])
    lines += ['## Tái lập và bổ sung', '', '[Hướng dẫn tải, khôi phục và kiểm tra CSV](../CSV_DOWNLOADS.md).', '',
              '`python scripts/organize_by_problem.py` tái tạo các báo cáo từ nguồn đã lưu. `python scripts/csv_archives.py pack` cập nhật các ZIP sau khi bổ sung kết quả. Manifest trong từng thư mục ghi SHA-256 và nguồn của CSV. Không chỉnh sửa trực tiếp các README được sinh tự động; sửa nội dung trong `scripts/research_readmes.py`.', '']
    save(OUT / 'README.md', lines)
    lines = ['# Research documentation', '',
             'Read results by problem. ZDT is the current research focus; each objective-count configuration in DTLZ and WFG has a separate report. No pooled cross-problem result is used as the main entry point.', '']
    for family, problems in families.items():
        lines += [f'## {family.upper()}', '']
        lines += md_table(['Problem', 'Report', 'Experiment reports'], [
            [p.upper(), f'[README](../results/by_problem/{family}/{p}/README.md)', f'[Index](../results/by_problem/{family}/{p}/reports/README.md)'] for p in problems])
    lines += ['## Shared protocols and data access', '',
              '- [Baseline identities and references](protocols/baselines.md)', '- [Reproducibility](protocols/reproducibility.md)',
              '- [Experiment registry and provenance](protocols/experiment_registry.md)', '- [ZDT OFAT protocol](protocols/zdt_sensitivity.md)',
              '- [DTLZ sensitivity protocol](protocols/dtlz_sensitivity.md)', '- [CSV ZIP downloads and restore instructions](../results/CSV_DOWNLOADS.md)',
              '- [README rewrite evidence and terminology audit](reports/readme_rewrite_audit.md)', '',
              'Historical reports and the integrated manuscript remain in the repository as reference records. Current result reading starts with the separate problem reports above.', '']
    save(ROOT / 'docs/index.md', lines)
    print(f'Wrote two project READMEs and {sum(map(len, families.values()))} problem READMEs, with separate family/documentation indexes.')


if __name__ == '__main__':
    generate_readmes()
