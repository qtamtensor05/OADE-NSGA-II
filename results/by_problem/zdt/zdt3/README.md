# ZDT3: kết quả OADE-NSGA-II

Trên ZDT3, OADE adaptive đạt IGD trung bình 0.00498585 và HV trung bình 1.05122; NSGA2 lần lượt đạt 0.00719117 và 1.04718 trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.

## Thiết kế và phạm vi

Bài toán có 30 biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.

## Benchmark adaptive: 7 thuật toán

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00498585 ± 0.000336107 | 1.05122 ± 0.000152005 | 10.7916 |
| NSGA2 | 30/30 | 0.00719117 ± 0.0102307 | 1.04718 ± 0.00669921 | 1.68703 |
| RNSGA2 | 30/30 | 0.740552 ± 0.0573164 | 0.401005 ± 0.0494966 | 2.38314 |
| DNSGA2 | 30/30 | 0.0055682 ± 0.000290586 | 1.04695 ± 0.000679974 | 1.62852 |
| CGDE_NSGAII | 30/30 | 0.00826161 ± 0.000984232 | 1.03505 ± 0.0036038 | 108.59 |
| NSGAII_SDR_OLS | 30/30 | 0.0186481 ± 0.00296968 | 1.03581 ± 0.00435762 | 2.53103 |
| CE_MOEA | 30/30 | 0.00856088 ± 0.00153316 | 1.0344 ± 0.0051157 | 100.297 |

So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.

| Chỉ số | n cặp | p Holm | Rank-biserial | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| IGD | 30 | 0.00114028 | 0.707527 | reference_better |
| HV | 30 | 5.58794e-08 | 1 | reference_better |

Các đối chứng còn lại và kết quả từng kiểm định được giữ trong [báo cáo benchmark adaptive](reports/benchmark_adaptive.md); không suy rộng kết quả của bài toán này sang bài toán khác.

## Classic và adaptive

Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.

| Cấu hình | IGD mean | HV mean |
| --- | --- | --- |
| Classic, seed 42–71 | 0.0083192 | 1.04924 |
| Adaptive, seed 42–71 | 0.00498585 | 1.05122 |

Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_FULL | 30/30 | 0.011652 ± 0.00830036 | 1.04618 ± 0.00692504 | 9.05217 |
| OADE_NO_RESTART | 30/30 | 0.0049638 ± 0.000324374 | 1.05126 ± 0.000115237 | 7.5875 |
| OADE_ADAPTIVE_RESTART | 30/30 | 0.0049638 ± 0.000324374 | 1.05126 ± 0.000115237 | 7.39762 |

Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.

## Độ nhạy tham số adaptive

Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ 0.00515966 thành 0.00249304; median HV đổi từ 1.05118 thành 1.0528.

Thay đổi population đồng thời thay đổi số thế hệ khả dụng và độ phân giải tập nghiệm ở ngân sách cố định. Vì vậy chênh lệch IGD không tự đo riêng tốc độ hội tụ.

| Tham số | Mức | Lượt hợp lệ | IGD median | IGD Q25–Q75 | HV median | Restart hoàn tất |
| --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.0105921 | 0.0101363–0.0109242 | 1.04766 | 0 |
| pop_size | 100 | 30 | 0.00515966 | 0.0048811–0.00536748 | 1.05118 | 0 |
| pop_size | 200 | 30 | 0.00249304 | 0.00239541–0.00264858 | 1.0528 | 0 |
| prob_de | 0.2 | 30 | 0.00515625 | 0.00489374–0.00531729 | 1.05117 | 0 |
| prob_de | 0.5 | 30 | 0.00515966 | 0.0048811–0.00536748 | 1.05118 | 0 |
| prob_de | 0.8 | 30 | 0.00512136 | 0.00496868–0.0052907 | 1.05127 | 0 |

Mỗi mức có 30 seed ghép cặp. Baseline được dùng lại giữa các bảng tham số, không tính thành lượt thực thi độc lập mới. OFAT chỉ thay một tham số mỗi lần; không đo tương tác và không xác lập một cấu hình tối ưu. F, CR và xác suất DE là giá trị khởi tạo có thể cập nhật trong lượt chạy.

## Ablation và bằng chứng bổ sung

Ablation thuộc cấu hình classic và khởi tạo uniform chung. Đọc [báo cáo ablation của bài toán](reports/ablation_classic.md) để phân biệt loại bỏ thành phần với đánh giá cấu hình adaptive. [Độ nhạy classic](reports/sensitivity_classic.md) là đợt lịch sử riêng, không gộp với [OFAT adaptive](reports/sensitivity_adaptive.md).

## Dữ liệu và tái lập

- [CSV của riêng bài toán, tải ZIP](csv_results.zip)
- [Danh mục báo cáo chi tiết](reports/README.md)
- [Manifest CSV và SHA-256](manifest.json)
- [Danh mục tải dữ liệu và lệnh khôi phục](../../../CSV_DOWNLOADS.md)
- [Cấu hình benchmark adaptive](../../../../config/suites/algorithm_benchmark_v2.yaml)
- [Cấu hình benchmark classic](../../../../config/suites/algorithm_benchmark_classic.yaml)
- [Giao thức OFAT](../../../../docs/protocols/zdt_sensitivity.md)

Giải nén ZIP cạnh tệp ZIP để khôi phục các thư mục thí nghiệm. Các block đối chứng có provenance khác nhau: block RNSGA2 có manifest thực thi, các block lịch sử khác không được gán ngược môi trường hiện tại. Xem [provenance ZDT](../../../provenance/zdt_composition.json). Chưa có khoảng tin cậy cho hiệu ứng ghép cặp trong các bảng hiện tại.

[Trở về ZDT](../README.md)
