# OADE-NSGA-II

**Ngôn ngữ:** [English](README.md) | **Tiếng Việt**

OADE-NSGA-II kết hợp sinh offspring bằng DE/SBX, cập nhật F/CR, bơm đa dạng OBL định kỳ và chọn lọc NSGA-II. Bản chính dùng một cấu hình thống nhất; các biến thể nghiên cứu được tách riêng.

## Mốc kết quả hiện tại

**Từ ngày 15/11/2026, ZDT v2 là mốc bắt đầu cho đối chứng thuật toán.** Các bảng, hình và nhận định từ những lần chạy trước khi sửa baseline đã được gỡ khỏi README này; chúng không được dùng để chứng minh hiệu quả của mã hiện tại. Toàn bộ dữ liệu, báo cáo và bản đóng gói kết quả cũ đã được xóa. Chỉ giữ bộ ZDT v2 đã đối chiếu. DTLZ/WFG chưa được chấm lại với bộ baseline mới nên chưa có kết luận hiện tại cho các tập đó.

[Báo cáo đã đối chiếu](docs/reports/zdt_seven_fixed_oade_v2_report.md) · [Giao thức](docs/protocols/zdt_seven_fixed_oade.md) · [Baseline và bài báo nguồn](docs/protocols/baselines.md)

## Thiết kế và cấu hình

Xem [bộ biểu đồ R và chú thích trong báo cáo](docs/reports/zdt_seven_fixed_oade_v2_report.md#biểu-đồ-so-sánh-bằng-r): phân bố IGD/HV, hiệu ứng theo cặp seed và runtime của đủ bảy thuật toán.

![Hiệu ứng theo cặp seed; NS là chưa phát hiện khác biệt sau Holm](docs/reports/figures/zdt_v2/paired_effects.png)

Màu dương thiên về OADE; màu thể hiện rank-biserial effect, không phải phần trăm cải thiện. Bốn ô NS thuộc ZDT4 so với NSGA2/DNSGA2. [IGD](docs/reports/figures/zdt_v2/igd_distribution.png) · [HV](docs/reports/figures/zdt_v2/hv_distribution.png) · [Runtime](docs/reports/figures/zdt_v2/runtime_distribution.png).

### Cấu hình thí nghiệm

Biểu đồ [IGD đủ 7 thuật toán với trục log₁₀](docs/reports/figures/zdt_v2/igd_log_comparison.png) dùng điểm median và đoạn Q1–Q3 để nhìn rõ các nhóm chênh lệch nhiều bậc độ lớn. [HV](docs/reports/figures/zdt_v2/hv_bars.png) giữ cột mean ± SD từ 0. Bản cột tập trung OADE/NSGA2/DNSGA2 có nhãn số: [IGD](docs/reports/figures/zdt_v2/igd_bars_focus.png) · [HV](docs/reports/figures/zdt_v2/hv_bars_focus.png). Xem định nghĩa và giới hạn trong báo cáo.

| Thành phần | Thiết lập |
|---|---|
| Bài toán | ZDT1/2/3: D=30; ZDT4/6: D=10; M=2 |
| Thuật toán | OADE_NSGAII, NSGA2, RNSGA2, DNSGA2, CGDE_NSGAII, NSGAII_SDR_OLS, CE_MOEA |
| Quần thể / ngân sách | 100 / 20.000 lần đánh giá mục tiêu mỗi run |
| Seed | 42–71; 30 run mỗi thuật toán/bài; tổng 1.050 |
| Phiên bản triển khai | `paper_corrections_2026_11_14`; `zdt_seven_fixed_oade_v2` |
| OADE | `oade_nsga2`, `local_oade`, uniform, adaptive restart, periodic OBL, `success_rate` |

OADE khởi đầu với F=0,65, CR=0,5, pDE=0,5; 5 láng giềng; patience 20; tolerance 10⁻⁴; diversity threshold 0,02; elite ratio 0,8; OBL interval 10 và jump rate 0,2. Cấu hình được chụp trong manifest; không chạy bản `research.oade_nsga2`.

Mỗi bài/seed có cùng uniform input giữa các solver. SDR-OLS vẫn thực hiện OBL khởi tạo riêng; mọi đánh giá OBL, local search và thiết lập aspiration points của RNSGA2 đều nằm trong ngân sách. Batch có thể để dư FE; dùng n_eval thực khi đối chiếu chi phí.

## Kết quả đối chứng

**1.050 run đã hoàn tất; 1.049 hợp lệ.** CGDE trên ZDT4, seed 63, có collapsed front. OADE tốt hơn ở **56/60 endpoint** sau Holm chung 60 kiểm định; bốn endpoint chưa phát hiện khác biệt là IGD/HV trên ZDT4 so với NSGA2 và DNSGA2. Không có endpoint nào kết luận baseline tốt hơn OADE theo kiểm định đã định.

Trong bảng dưới, “+/+” nghĩa là OADE tốt hơn ở cả IGD/HV; “NS/NS” nghĩa là chưa phát hiện khác biệt ở cả hai. Các cặp CGDE ZDT4 dùng n=29, còn lại n=30. Đây là số endpoint, không phải các thí nghiệm độc lập.

| Bài | NSGA2 | RNSGA2 | DNSGA2 | CGDE_NSGAII | NSGAII_SDR_OLS | CE_MOEA |
|---|---|---|---|---|---|---|
| ZDT1 | +/+ | +/+ | +/+ | +/+ | +/+ | +/+ |
| ZDT2 | +/+ | +/+ | +/+ | +/+ | +/+ | +/+ |
| ZDT3 | +/+ | +/+ | +/+ | +/+ | +/+ | +/+ |
| ZDT4 | NS/NS | +/+ | NS/NS | +/+ | +/+ | +/+ |
| ZDT6 | +/+ | +/+ | +/+ | +/+ | +/+ | +/+ |

IGD giảm tốt, HV tăng tốt. Các bảng dùng **mean ± SD** trên run hợp lệ; runtime là median giây/run. Giữ bảy thuật toán trên từng bài, không gộp chỉ số giữa các bài có thang đo khác nhau.

### ZDT1

| Thuật toán | Hợp lệ | IGD ↓ (trung bình ± SD) | HV ↑ (trung bình ± SD) | Runtime median (s) |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 30/30 | 0.004469996 ± 0.0002461367 | 0.8708345 ± 0.0002705209 | 7.398 |
| NSGA2 | 30/30 | 0.005174662 ± 0.0002979038 | 0.8680528 ± 0.0004172684 | 3.484 |
| RNSGA2 | 30/30 | 0.6329726 ± 0.08762427 | 0.3480615 ± 0.0938884 | 3.610 |
| DNSGA2 | 30/30 | 0.005632946 ± 0.000423465 | 0.867066 ± 0.0006850103 | 3.257 |
| CGDE_NSGAII | 30/30 | 0.005202101 ± 0.0003939673 | 0.8699383 ± 0.0004466639 | 118.025 |
| NSGAII_SDR_OLS | 30/30 | 1.844996 ± 0.158428 | 0 ± 0 | 38.268 |
| CE_MOEA | 30/30 | 0.006800385 ± 0.0007568819 | 0.8646314 ± 0.001397095 | 178.953 |

### ZDT2

| Thuật toán | Hợp lệ | IGD ↓ (trung bình ± SD) | HV ↑ (trung bình ± SD) | Runtime median (s) |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 30/30 | 0.004709676 ± 0.0003506824 | 0.5376825 ± 0.0002095407 | 7.897 |
| NSGA2 | 30/30 | 0.005404928 ± 0.0003062495 | 0.5340721 ± 0.000611177 | 2.778 |
| RNSGA2 | 30/30 | 0.5235072 ± 0.02531412 | 0.1208837 ± 0.00708899 | 3.858 |
| DNSGA2 | 30/30 | 0.005881009 ± 0.0003919705 | 0.532697 ± 0.000974228 | 3.399 |
| CGDE_NSGAII | 30/30 | 0.005539142 ± 0.0004257992 | 0.5364841 ± 0.0004320833 | 156.693 |
| NSGAII_SDR_OLS | 30/30 | 3.042347 ± 0.2797306 | 0 ± 0 | 41.547 |
| CE_MOEA | 30/30 | 0.007799739 ± 0.001289595 | 0.5292563 ± 0.002599526 | 180.302 |

### ZDT3

| Thuật toán | Hợp lệ | IGD ↓ (trung bình ± SD) | HV ↑ (trung bình ± SD) | Runtime median (s) |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 30/30 | 0.004998217 ± 0.0003862774 | 1.051217 ± 0.0001910845 | 7.426 |
| NSGA2 | 30/30 | 0.007191168 ± 0.01023075 | 1.047182 ± 0.006699209 | 3.804 |
| RNSGA2 | 30/30 | 0.7405515 ± 0.05731643 | 0.4010049 ± 0.04949664 | 5.867 |
| DNSGA2 | 30/30 | 0.005568199 ± 0.0002905857 | 1.046953 ± 0.000679974 | 2.980 |
| CGDE_NSGAII | 30/30 | 0.00612553 ± 0.0004490891 | 1.050619 ± 0.0002276871 | 178.629 |
| NSGAII_SDR_OLS | 30/30 | 1.575167 ± 0.2255406 | 0.0008118896 ± 0.003089748 | 40.696 |
| CE_MOEA | 30/30 | 0.00881295 ± 0.002077688 | 1.034105 ± 0.006937207 | 117.514 |

### ZDT4

| Thuật toán | Hợp lệ | IGD ↓ (trung bình ± SD) | HV ↑ (trung bình ± SD) | Runtime median (s) |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 30/30 | 0.03978991 ± 0.07313553 | 0.8139427 ± 0.1120385 | 9.062 |
| NSGA2 | 30/30 | 0.009952722 ± 0.005080291 | 0.8593619 ± 0.007910405 | 3.273 |
| RNSGA2 | 30/30 | 0.6205746 ± 0.1653183 | 0.3510772 ± 0.1552783 | 5.031 |
| DNSGA2 | 30/30 | 0.01997309 ± 0.02736954 | 0.8467496 ± 0.03686742 | 3.765 |
| CGDE_NSGAII | 29/30 | 2.320433 ± 1.62697 | 0.01647341 ± 0.05151324 | 118.540 |
| NSGAII_SDR_OLS | 30/30 | 23.83874 ± 7.582792 | 0 ± 0 | 15.735 |
| CE_MOEA | 30/30 | 0.2883965 ± 0.132077 | 0.4653022 ± 0.1654559 | 206.108 |

### ZDT6

| Thuật toán | Hợp lệ | IGD ↓ (trung bình ± SD) | HV ↑ (trung bình ± SD) | Runtime median (s) |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 30/30 | 0.003881201 ± 0.0002201265 | 0.4380939 ± 0.0002440285 | 7.923 |
| NSGA2 | 30/30 | 0.01636813 ± 0.002011487 | 0.4178915 ± 0.002872109 | 3.054 |
| RNSGA2 | 30/30 | 0.1857638 ± 0.09278693 | 0.2676365 ± 0.06858999 | 5.488 |
| DNSGA2 | 30/30 | 0.0225884 ± 0.002794084 | 0.4089167 ± 0.003997333 | 2.542 |
| CGDE_NSGAII | 30/30 | 0.004827706 ± 0.0003294287 | 0.4379368 ± 0.0002590232 | 114.378 |
| NSGAII_SDR_OLS | 30/30 | 5.257007 ± 0.3926272 | 0 ± 0 | 15.004 |
| CE_MOEA | 30/30 | 0.004887331 ± 0.0003339747 | 0.4378238 ± 0.0003542558 | 138.853 |

## Mức cải thiện và giới hạn

So với NSGA2, IGD median OADE giảm 12,59% trên ZDT1; 11,64% trên ZDT2; 7,69% trên ZDT3; 22,63% trên ZDT4; 75,92% trên ZDT6. Riêng ZDT4 chưa đạt ý nghĩa thống kê. Phần trăm tính từ hai median nhóm, không phải median phần trăm theo cặp.

- **ZDT4 thiếu ổn định:** OADE có IGD median 0,00625933 nhưng mean 0,0397899, kém NSGA2 (mean 0,00995272) và DNSGA2 (mean 0,0199731). Một số seed sai số lớn làm thay đổi kết luận; không loại chúng khỏi phân tích.
- **HV ZDT6 so với CGDE:** chỉ tăng khoảng 0,0256%, p Holm=0,0465056; cải thiện nhỏ và sát ngưỡng.
- **Chi phí:** runtime median OADE cao hơn NSGA2 khoảng 1,95–2,84 lần theo từng bài trong môi trường bốn worker đã đo; khác biệt triển khai không cho phép suy ra độ phức tạp thuần túy.
- **Phạm vi baseline:** RNSGA2 nhắm vùng ưu tiên, DNSGA2 nhắm bài động; CE trên ZDT chỉ là adaptation lõi tìm kiếm. SDR-OLS có 148/150 run HV=0 và local search tiêu tốn nhiều FE. Các bản tự dựng dùng bài báo công khai và quy ước được ghi rõ.
- **Giới hạn cơ chế:** benchmark này không tách đóng góp của restart, OBL hay success_rate và không chứng minh ưu thế ngoài năm bài ZDT đã đo.

## Thống kê và kiểm chứng

Wilcoxon signed-rank hai phía theo cặp seed, zero_method=wilcox, SciPy method=auto; all-zero p=1. Kết luận chung dùng Holm trên 60 endpoint, alpha=0,05. Chỉ loại cặp invalid theo quy tắc đã định; báo số cặp bị loại. Không phát hiện khác biệt không chứng minh tương đương. Bảng dữ liệu bổ sung có rank-biserial và CI bootstrap 95% của median chênh lệch, chưa hiệu chỉnh đa kiểm định.

Audit xác minh 1.050 checksum primary, 106 hash source/dependency, reference snapshot, uniform input và toàn bộ final X/F. IGD/HV tính lại khớp chính xác; 35 dòng summary và 60 kiểm định được đối chiếu độc lập. Tổng FE thực là 20.979.322. Các checkpoint sau batch phải đọc theo n_eval thực, không coi target danh nghĩa là thời điểm đã đo.

- [Manifest thực thi](results/experiments/zdt_seven_fixed_oade_v2/study_manifest.json)
- [Biên bản kiểm chứng](results/experiments/zdt_seven_fixed_oade_v2/derived/audit.json)
- [Bảng tổng hợp đã đối chiếu](results/experiments/zdt_seven_fixed_oade_v2/derived/audited_summary.csv)
- [Đối chứng theo cặp, effect size và khoảng tin cậy](results/experiments/zdt_seven_fixed_oade_v2/derived/audited_comparisons.csv)
- [Mã kiểm chứng độc lập](analysis/audit_zdt_seven_v2.py)

## Chạy lại từ mốc hiện tại

Không chạy ghi đè lên bộ đã chấm. Dùng thư mục mới cho lần chạy độc lập:

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"

.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage plan
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage run --jobs 4 --out-dir results/experiments/zdt_seven_fixed_oade_v2_replication
```

Thêm `--resume` để tiếp tục đúng lần chạy bị gián đoạn. Lệnh `-m research` điều phối thí nghiệm; solver OADE vẫn là bản chính `oade_nsga2`. Manifest từ chối thay đổi mã, cấu hình, môi trường hoặc primary bị sửa. Không dùng lệnh benchmark cũ để tái tạo các bảng hiện tại.

## Nghiên cứu thành phần và tài liệu

Mã nguồn và giao thức nghiên cứu thành phần vẫn còn. Toàn bộ kết quả thành phần cũ đã được xóa; cần chạy mới trước khi báo cáo hiệu quả của chúng. Chỉ bộ đối chứng ZDT v2 phía trên được giữ.

- [OADE bản thống nhất và bản nghiên cứu](docs/protocols/oade_implementations.md)
- [Ablation restart](docs/protocols/restart_comparison.md)
- [Bơm đa dạng định kỳ](docs/protocols/diversity_injection.md)
- [Nghiên cứu khởi tạo](docs/protocols/initialization_comparison.md)
- [Thích nghi xác suất toán tử](docs/protocols/probability_ablation.md)
- [Sửa baseline và giả định tái dựng](docs/protocols/baseline_paper_corrections.md)
- [Danh mục thí nghiệm](docs/protocols/experiment_registry.md)
- [Mục lục tài liệu](docs/index.md)
