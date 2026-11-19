# OADE-NSGA-II

**Ngôn ngữ:** [English](README.md) | **Tiếng Việt**

OADE-NSGA-II kết hợp sinh nghiệm DE/SBX, thích nghi F/CR, bơm đa dạng OBL định kỳ, adaptive restart và chọn lọc NSGA-II. Giữ nguyên solver OADE production và CGDE đã triển khai.

## Baseline so sánh hiện tại — sáu thuật toán

Từ 19/11/2026, nhóm so sánh chính gồm **OADE_NSGAII, NSGA2, DNSGA2, CGDE_NSGAII, GDE3, NSDE**. Bỏ CE-MOEA, R-NSGA-II và SDR-OLS khỏi bộ chạy chính; mã nguồn/cấu hình cũ được giữ để truy xuất lịch sử.

| Thuật toán | Triển khai | Vai trò đối chứng |
|---|---|---|
| OADE-NSGA-II | Solver production cục bộ, cấu hình cố định | Thuật toán đề xuất |
| NSGA-II | pymoo | Mốc nền NSGA-II |
| D-NSGA-II | pymoo | Phản ứng đa dạng; ở đây đo trên bài tĩnh |
| CGDE-NSGA-II | Bản tái dựng đã có, giữ nguyên | DE xuyên thế hệ và lân cận |
| GDE3 | pymoo 0.6.2+ | Cạnh tranh cha–con bằng DE |
| NSDE | pymoo 0.6.2+ | DE với sorting/survival NSGA-II |

GDE3/NSDE dùng trực tiếp thuật toán trong thư viện: `DE/rand/1/bin`, F=0,5, CR=0,5, gamma=10⁻⁴, bounce-back repair và RankAndCrowding mặc định. Cả sáu nhận cùng khởi tạo uniform theo bài/seed, không dùng LHS mặc định của NSDE. Không dựng lại toán tử tìm kiếm của hai thuật toán mới.

[Giao thức thực thi](docs/protocols/zdt_six_fixed_oade.md) · [Cấu hình bộ chạy](config/suites/zdt_six_fixed_oade.yaml) · [Danh mục baseline](docs/protocols/baselines.md).

## Cấu hình thí nghiệm và trạng thái kết quả

| Thành phần | Thiết lập |
|---|---|
| Bài toán | ZDT1/2/3: D=30; ZDT4/6: D=10; mọi bài M=2 |
| Quần thể / ngân sách | 100 / tối đa 20.000 đánh giá mục tiêu mỗi lượt |
| Seed | 42–71, 30 lượt mỗi thuật toán/bài |
| Tổng | **900 lượt chạy mới**, tối đa 18 triệu FE solver |
| Thống kê | OADE so với năm baseline: **50 endpoint**, Holm chung, alpha=0,05 |
| Chạy song song | Mặc định 8 process; đổi bằng `--jobs` |
| Output mới | `results/experiments/zdt_six_fixed_oade_v1/` |

<!-- six-solver-audited-results:start -->

**Đã hoàn tất 900 lượt, 899 hợp lệ.** Sau Holm chung 50 endpoint: **OADE tốt hơn 44, 6 NS, không có endpoint baseline tốt hơn có ý nghĩa**. Một lượt CGDE–ZDT4 seed 63 có front suy biến; nhóm này dùng 29 lượt hợp lệ, các nhóm khác 30. OADE có mean tốt nhất ở ZDT1/2/3/6; NSGA-II có mean tốt nhất trên ZDT4. [Audited report](docs/reports/zdt_six_fixed_oade_report.md).

Ô là mean (best run): min IGD/max HV; in đậm hai đại lượng riêng theo số chưa làm tròn. Best hai chỉ số có thể thuộc seed khác nhau; NS không chứng minh tương đương.

### IGD ↓ — mean (best)

| Problem | NSGA2 | DNSGA2 | CGDE_NSGAII | GDE3 | NSDE | OADE_NSGAII |
|---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 5.175e-3 (4.417e-3) | 5.633e-3 (4.97e-3) | 5.202e-3 (4.584e-3) | 4.961e-3 (4.469e-3) | 4.872e-3 (4.373e-3) | **4.47e-3** (**3.952e-3**) |
| ZDT2 | 5.405e-3 (4.938e-3) | 5.881e-3 (5.189e-3) | 5.539e-3 (4.774e-3) | 8.597e-2 (4.764e-3) | 1.665e-1 (4.535e-3) | **4.71e-3** (**4.149e-3**) |
| ZDT3 | 7.191e-3 (4.695e-3) | 5.568e-3 (5.049e-3) | 6.126e-3 (5.246e-3) | 5.349e-3 (4.917e-3) | 5.186e-3 (4.565e-3) | **4.998e-3** (**4.453e-3**) |
| ZDT4 | **9.953e-3** (4.767e-3) | 1.997e-2 (**4.574e-3**) | 2.32e0 (4.666e-1) | 8.542e0 (5.599e0) | 6.938e0 (3.668e0) | 3.979e-2 (4.636e-3) |
| ZDT6 | 1.637e-2 (1.299e-2) | 2.259e-2 (1.699e-2) | 4.828e-3 (4.24e-3) | 1.154e-2 (8.408e-3) | 2.588e-2 (7.242e-3) | **3.881e-3** (**3.461e-3**) |

### HV ↑ — mean (best)

| Problem | NSGA2 | DNSGA2 | CGDE_NSGAII | GDE3 | NSDE | OADE_NSGAII |
|---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 8.681e-1 (8.686e-1) | 8.671e-1 (8.683e-1) | 8.699e-1 (8.706e-1) | 8.686e-1 (8.693e-1) | 8.689e-1 (8.695e-1) | **8.708e-1** (**8.713e-1**) |
| ZDT2 | 5.341e-1 (5.349e-1) | 5.327e-1 (5.345e-1) | 5.365e-1 (5.373e-1) | 4.78e-1 (5.356e-1) | 4.218e-1 (5.359e-1) | **5.377e-1** (**5.38e-1**) |
| ZDT3 | 1.047e0 (1.049e0) | 1.047e0 (1.048e0) | 1.051e0 (1.051e0) | 1.048e0 (1.049e0) | 1.048e0 (1.049e0) | **1.051e0** (**1.052e0**) |
| ZDT4 | **8.594e-1** (8.686e-1) | 8.467e-1 (8.688e-1) | 1.647e-2 (2.453e-1) | 0 (0) | 0 (0) | 8.139e-1 (**8.693e-1**) |
| ZDT6 | 4.179e-1 (4.226e-1) | 4.089e-1 (4.17e-1) | 4.379e-1 (4.385e-1) | 4.249e-1 (4.297e-1) | 4.175e-1 (4.315e-1) | **4.381e-1** (**4.385e-1**) |

Kết quả sau Holm, theo thứ tự **IGD / HV**; +: OADE tốt hơn có ý nghĩa, NS: chưa phát hiện khác biệt.

| Baseline | ZDT1 | ZDT2 | ZDT3 | ZDT4 | ZDT6 | OADE better / 10 |
|---|---|---|---|---|---|---:|
| NSGA2 | + / + | + / + | + / + | NS / NS | + / + | 8 |
| DNSGA2 | + / + | + / + | + / + | NS / NS | + / + | 8 |
| CGDE_NSGAII | + / + | + / + | + / + | + / + | + / NS | 9 |
| GDE3 | + / + | + / + | + / + | + / + | + / + | 10 |
| NSDE | + / + | + / + | NS / + | + / + | + / + | 9 |

![Paired effects after global Holm](docs/reports/figures/zdt_six/paired_effects.png)

Màu là rank-biserial (dương có lợi cho OADE), không phải phần trăm cải thiện. GDE3/NSDE nhanh hơn trong runtime đo được nhưng kém rõ trên ZDT4 (HV=0); NSDE–ZDT3 IGD và CGDE–ZDT6 HV vẫn NS. Audit khớp 900 primary, 30 summary và 50 kiểm định; sai lệch objective/IGD/HV bằng 0. [Dữ liệu kiểm định và giới hạn diễn giải](docs/reports/zdt_six_fixed_oade_report.md).

![IGD median and IQR, current six-solver study](docs/reports/figures/zdt_six/igd_log_comparison.png)

Điểm là median, đoạn là Q1–Q3, trục log10 chung; không phải CI. [Phân bố IGD đầy đủ](docs/reports/figures/zdt_six/igd_distribution.png) · [Phân bố HV](docs/reports/figures/zdt_six/hv_distribution.png) · [Runtime](docs/reports/figures/zdt_six/runtime_distribution.png) · [Pareto OADE từ dữ liệu mới](docs/reports/oade_zdt_pareto_fronts.md).

<!-- six-solver-audited-results:end -->

Không đổi tên hoặc ghép dữ liệu cũ thành kết quả bộ mới. [Báo cáo ZDT v2 trước đây](docs/reports/zdt_seven_fixed_oade_v2_report.md), dữ liệu gốc được giữ như **bằng chứng lịch sử**, cùng họ 60 endpoint và các giới hạn triển khai ban đầu. Các nghiên cứu chỉ đo OADE ở phần dưới vẫn là bằng chứng riêng, không bị xóa hoặc dùng để điền baseline mới.

## Chạy bộ so sánh mới

```powershell
# Chỉ xem kế hoạch; không chạy solver.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage plan --jobs 8

$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"

# Lặp lại độc lập: dùng thư mục output MỚI.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage run --jobs 8 --out-dir results/experiments/zdt_six_replication

# Tiếp tục cùng source/configuration/môi trường và output.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage run --jobs 8 --resume
```

Dùng `--stage report --resume` để tái tạo bảng của bộ đã hoàn tất. Lần lặp độc lập dùng `--out-dir` mới; không chạy `benchmark-zdt-seven` để tái tạo thiết kế sáu thuật toán. Mọi đánh giá nội bộ tính vào cap; đọc FE thực khi xem convergence. Runtime đã được đo; giới hạn so sánh máy/worker/thread được nêu trong báo cáo.

## Ảnh hưởng của mức tham số trên ZDT4 và ZDT6

Nghiên cứu OFAT đã hoàn tất **2.100/2.100 lượt hợp lệ**: 35 cấu hình × 2 bài × 30 seed mới (7000–7029), quần thể 100, cap 20.000 FE/lượt. Sau Holm chung **124 endpoint**, mốc tốt hơn ở **15**, mức thử tốt hơn ở **5**, **104 chưa phát hiện khác biệt**. Endpoint là bài × mức so với mốc × chỉ số, không phải các thí nghiệm độc lập. [Báo cáo đã audit](docs/reports/mechanism_sensitivity_report.md) · [Bảng đầy đủ](docs/reports/mechanism_sensitivity_tables.md) · [Giao thức và các mức](docs/protocols/mechanism_sensitivity.md).

**Mốc so sánh:** tham số tĩnh so với full production; mean F/CR/pDE so với cùng tham số được **giữ cố định (held)** tại 0,65/0,5/0,5. Khi giữ một tham số, các tham số thích nghi khác vẫn hoạt động. Kết quả held không phải phép so trực tiếp với full adaptive. IGD thấp tốt hơn; HV cao tốt hơn.

### Tham số nào làm thay đổi kết quả?

Trong bảng, “tốt/kém hơn” là mức thử so với mốc, đã đạt p Holm <0,05; **NS** là chưa phát hiện khác biệt, không chứng minh tương đương. Mỗi endpoint dùng đủ 30 cặp seed.

| Tham số và mốc | ZDT4: IGD | ZDT4: HV | ZDT6: IGD | ZDT6: HV |
|---|---|---|---|---|
| OBL interval, mốc 10 | NS ở 5/20/40 | NS ở 5/20/40 | NS ở 5/20/40 | NS ở 5/20/40 |
| OBL jump rate, mốc 0,2 | **0,05 kém hơn**; 0,1/0,4 NS | **0,05 kém hơn**; 0,1/0,4 NS | NS ở mọi mức thử | NS ở mọi mức thử |
| Patience, tolerance, diversity threshold, elite ratio | NS ở mọi mức thử | NS ở mọi mức thử | NS ở mọi mức thử | NS ở mọi mức thử |
| Số láng giềng, mốc 5 | NS ở 3/10/20 | NS ở 3/10/20 | NS ở 3/10/20 | NS ở 3/10/20 |
| Mean F held, mốc 0,65 | **0,5 tốt hơn; 0,8/0,9 kém hơn**; 0,4 NS | **0,4/0,5 tốt hơn; 0,8/0,9 kém hơn** | **0,5 kém hơn**; 0,4/0,8/0,9 NS | **0,4/0,5 kém hơn**; 0,8/0,9 NS |
| Mean CR held, mốc 0,5 | NS ở mọi mức thử | NS ở mọi mức thử | **0,9 kém hơn**; 0,1/0,3/0,7 NS | **0,3 tốt hơn; 0,7/0,9 kém hơn**; 0,1 NS |
| pDE held, mốc 0,5 | **0,2 kém hơn**; 0,35/0,65/0,8 NS | **0,2 kém hơn**; 0,35/0,65/0,8 NS | NS ở mọi mức thử | **0,8 tốt hơn; 0,2 kém hơn**; 0,35/0,65 NS |

![Chênh lệch HV theo mức tham số trên ZDT4 và ZDT6](docs/reports/figures/mechanism_sensitivity/paired_hv_overview.png)

**Cách đọc:** dương là mức thử tốt hơn, âm là kém hơn; xanh ZDT4, nâu ZDT6. Chấm đặc theo Holm, chấm rỗng là NS; đoạn dọc là CI bootstrap 95% **chưa hiệu chỉnh**. Đại lượng hiển thị là median chênh lệch HV theo cặp chia cho median mốc, không phải phần trăm cải thiện của từng seed. Các panel có phạm vi riêng. [Tổng quan IGD](docs/reports/figures/mechanism_sensitivity/paired_igd_overview.png) dùng signed pseudo-log để giữ cả CI dài; [hướng dẫn đầy đủ cho 12 hình](docs/reports/mechanism_sensitivity_figures.md).

### Chất lượng đạt được ở các trường hợp tiêu biểu

Số dưới đây là **median nhóm (best run): mốc → mức thử**, không phải median chênh lệch theo cặp. Trong ngoặc là giá trị tốt nhất trong 30 lượt cho chỉ số đó. Kết luận vẫn dựa trên kiểm định theo cặp, không suy ra từ hai median hoặc best-run khác nhau.

| Bài | Thay đổi một tham số | IGD median (best) ↓ | HV median (best) ↑ | Kết luận sau Holm |
|---|---|---:|---:|---|
| ZDT4 | OBL jump rate 0,2 → 0,05 | **5.414e-3** (**4.68e-3**) → 7.216e-2 (4.858e-3) | **8.677e-1** (**8.696e-1**) → 7.627e-1 (8.693e-1) | Kém ở cả hai; p=0,005069 / 0,006915 |
| ZDT4 | Mean F held 0,65 → 0,5 | 4.805e-3 (**3.89e-3**) → **4.516e-3** (3.995e-3) | 8.692e-1 (8.704e-1) → **8.702e-1** (**8.71e-1**) | Tốt ở cả hai; p=0,005565 / 9,691×10⁻⁶ |
| ZDT6 | Mean F held 0,65 → 0,5 | **3.829e-3** (**3.442e-3**) → 4.028e-3 (3.613e-3) | **4.381e-1** (**4.385e-1**) → 4.377e-1 (4.382e-1) | Kém ở cả hai; p=0,006208 / 0,005069 |
| ZDT6 | Mean CR held 0,5 → 0,3 | 3.739e-3 (3.44e-3) → **3.669e-3** (**3.28e-3**) | 4.382e-1 (4.387e-1) → **4.385e-1** (**4.391e-1**) | IGD NS; HV tốt hơn, p=0,048311 |
| ZDT6 | pDE held 0,5 → 0,8 | 3.812e-3 (3.31e-3) → **3.663e-3** (**3.034e-3**) | 4.382e-1 (4.387e-1) → **4.388e-1** (**4.395e-1**) | IGD NS; HV tốt hơn, p=3,037×10⁻⁵ |

![Phân bố chất lượng theo mean F giữ cố định](docs/reports/figures/mechanism_sensitivity/levels_mean_F.png)

F thấp có lợi trên ZDT4 trong những so sánh cụ thể nhưng F=0,5 gây bất lợi trên ZDT6. Mỗi chấm là một seed, hộp là Q1–Q3, hình thoi là median; IGD dùng trục log10, HV tuyến tính. Đường dọc chấm là mốc held. Giữ đủ các đuôi sai số, không so độ cao giữa các panel có phạm vi khác nhau.

![Phân bố chất lượng theo xác suất OBL](docs/reports/figures/mechanism_sensitivity/levels_obl_jump_rate.png)

Giảm jump rate xuống 0,05 làm ZDT4 kém hơn; các mức còn lại chưa đủ bằng chứng xác định 0,2 là tối ưu. Cách đọc hộp/điểm như hình F; mốc ở đây là full production với jump rate=0,2.

**Kết luận thực nghiệm:** không có mức thay thế nào được chứng minh cải thiện đồng đều cả hai bài và hai chỉ số. CR=0,3 và pDE=0,8 chỉ có bằng chứng cải thiện HV trên ZDT6; riêng CR=0,3 có p sát ngưỡng. Ngưỡng restart có thể làm thay đổi hành vi mà chưa cải thiện chất lượng đạt ngưỡng: trên ZDT6, patience=5 tạo 102 restart trong 19/30 seed so với 8 restart trong 6/30 seed của full, nhưng IGD/HV vẫn NS. Trên ZDT4, full và các mức tham số restart đã thử không có restart hoàn tất.

Đây là OFAT trên hai bài, không kiểm định tương tác hay tối ưu tổ hợp tham số. Không cộng các mức thắng thành cấu hình mới, không suy rộng sang DTLZ/WFG và không tự đổi production. Bộ này không chạy lại các đối thủ nên không thay kết luận benchmark ZDT v2 ở trên. [Audit dữ liệu và 124 kiểm định](results/experiments/mechanism_sensitivity_v1/derived/audit.json).

## Nghiên cứu thành phần khác và tài liệu

Mã nguồn và giao thức nghiên cứu thành phần vẫn còn. Kết quả thành phần cũ đã được xóa. Bộ chạy mới 480 lượt trên ZDT4/ZDT6 đã có [báo cáo, biểu đồ và kiểm chứng độc lập](docs/reports/mechanism_zdt46_report.md): 6 endpoint thiên về bản đầy đủ, 4 thiên về biến thể và 18 chưa phát hiện khác biệt sau Holm chung 28 endpoint. Báo cáo nêu rõ giới hạn provenance và số lần restart kích hoạt thấp.

- [OADE bản thống nhất và bản nghiên cứu](docs/protocols/oade_implementations.md)
- [Ablation restart](docs/protocols/restart_comparison.md)
- [Bơm đa dạng định kỳ](docs/protocols/diversity_injection.md)
- [Nghiên cứu khởi tạo](docs/protocols/initialization_comparison.md)
- [Thích nghi xác suất toán tử](docs/protocols/probability_ablation.md)
- [Sửa baseline và giả định tái dựng](docs/protocols/baseline_paper_corrections.md)
- [Danh mục thí nghiệm](docs/protocols/experiment_registry.md)
- [Mục lục tài liệu](docs/index.md)
