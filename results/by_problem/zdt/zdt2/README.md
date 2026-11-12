# ZDT2: kết quả OADE-NSGA-II

Trên ZDT2, OADE adaptive đạt IGD trung bình 0.00475622 và HV trung bình 0.537674; NSGA2 lần lượt đạt 0.00540493 và 0.534072 trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.

## Thiết kế và phạm vi

Bài toán có 30 biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.

## Benchmark adaptive: 7 thuật toán

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00475622 ± 0.000292104 | 0.537674 ± 0.000221914 | 14.7846 |
| NSGA2 | 30/30 | 0.00540493 ± 0.000306249 | 0.534072 ± 0.000611177 | 1.97288 |
| RNSGA2 | 30/30 | 0.523507 ± 0.0253141 | 0.120884 ± 0.00708899 | 6.41374 |
| DNSGA2 | 30/30 | 0.00588101 ± 0.00039197 | 0.532697 ± 0.000974228 | 1.84104 |
| CGDE_NSGAII | 30/30 | 0.00681507 ± 0.00051003 | 0.530572 ± 0.00116976 | 136.061 |
| NSGAII_SDR_OLS | 30/30 | 0.0503186 ± 0.152326 | 0.499634 ± 0.106117 | 3.47569 |
| CE_MOEA | 30/30 | 0.00747684 ± 0.000980341 | 0.52967 ± 0.00190535 | 144.511 |

So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.

| Chỉ số | n cặp | p Holm | Rank-biserial | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| IGD | 30 | 7.82311e-08 | 0.982796 | reference_better |
| HV | 30 | 5.58794e-08 | 1 | reference_better |

Các đối chứng còn lại và kết quả từng kiểm định được giữ trong [báo cáo benchmark adaptive](reports/benchmark_adaptive.md); không suy rộng kết quả của bài toán này sang bài toán khác.

## Classic và adaptive

Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.

| Cấu hình | IGD mean | HV mean |
| --- | --- | --- |
| Classic, seed 42–71 | 0.00773397 | 0.533739 |
| Adaptive, seed 42–71 | 0.00475622 | 0.537674 |

Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_FULL | 30/30 | 0.00678176 ± 0.00319012 | 0.53447 ± 0.00418593 | 3.9203 |
| OADE_NO_RESTART | 30/30 | 0.00459058 ± 0.000293594 | 0.537682 ± 0.000166956 | 3.84475 |
| OADE_ADAPTIVE_RESTART | 30/30 | 0.00459058 ± 0.000293594 | 0.537682 ± 0.000166956 | 3.83875 |

Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.

## Độ nhạy tham số adaptive

Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ 0.0046646 thành 0.00236691; median HV đổi từ 0.537652 thành 0.540519.

Thay đổi population đồng thời thay đổi số thế hệ khả dụng và độ phân giải tập nghiệm ở ngân sách cố định. Vì vậy chênh lệch IGD không tự đo riêng tốc độ hội tụ.

| Tham số | Mức | Lượt hợp lệ | IGD median | IGD Q25–Q75 | HV median | Restart hoàn tất |
| --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.00940258 | 0.00915544–0.00964465 | 0.531951 | 2 |
| pop_size | 100 | 30 | 0.0046646 | 0.00444873–0.00484682 | 0.537652 | 1 |
| pop_size | 200 | 30 | 0.00236691 | 0.00225449–0.00251158 | 0.540519 | 0 |
| prob_de | 0.2 | 30 | 0.00471597 | 0.00453083–0.00486162 | 0.537759 | 0 |
| prob_de | 0.5 | 30 | 0.0046646 | 0.00444873–0.00484682 | 0.537652 | 1 |
| prob_de | 0.8 | 30 | 0.00461182 | 0.00439873–0.00475219 | 0.537702 | 5 |

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
