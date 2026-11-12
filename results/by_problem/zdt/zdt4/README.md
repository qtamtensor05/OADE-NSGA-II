# ZDT4: kết quả OADE-NSGA-II

Trên ZDT4, OADE adaptive đạt IGD trung bình 0.00683066 và HV trung bình 0.865051; NSGA2 lần lượt đạt 0.00995272 và 0.859362 trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.

## Thiết kế và phạm vi

Bài toán có 10 biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.

## Benchmark adaptive: 7 thuật toán

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00683066 ± 0.00332858 | 0.865051 ± 0.00567877 | 11.9833 |
| NSGA2 | 30/30 | 0.00995272 ± 0.00508029 | 0.859362 ± 0.0079104 | 2.20807 |
| RNSGA2 | 30/30 | 0.620575 ± 0.165318 | 0.351077 ± 0.155278 | 2.09675 |
| DNSGA2 | 30/30 | 0.0199731 ± 0.0273695 | 0.84675 ± 0.0368674 | 2.10489 |
| CGDE_NSGAII | 30/30 | 12.1716 ± 2.80042 | 0 ± 0 | 138.416 |
| NSGAII_SDR_OLS | 30/30 | 10.8914 ± 6.7777 | 0 ± 0 | 2.36871 |
| CE_MOEA | 30/30 | 0.357214 ± 0.234331 | 0.409725 ± 0.22787 | 129.2 |

So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.

| Chỉ số | n cặp | p Holm | Rank-biserial | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| IGD | 30 | 0.00404036 | 0.625806 | reference_better |
| HV | 30 | 0.00087182 | 0.668817 | reference_better |

Các đối chứng còn lại và kết quả từng kiểm định được giữ trong [báo cáo benchmark adaptive](reports/benchmark_adaptive.md); không suy rộng kết quả của bài toán này sang bài toán khác.

## Classic và adaptive

Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.

| Cấu hình | IGD mean | HV mean |
| --- | --- | --- |
| Classic, seed 42–71 | 0.00697718 | 0.864878 |
| Adaptive, seed 42–71 | 0.00683066 | 0.865051 |

Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_FULL | 30/30 | 0.0240858 ± 0.0547106 | 0.839208 ± 0.0811262 | 3.9723 |
| OADE_NO_RESTART | 30/30 | 0.0240433 ± 0.0547254 | 0.839264 ± 0.0811475 | 2.0597 |
| OADE_ADAPTIVE_RESTART | 30/30 | 0.0240433 ± 0.0547254 | 0.839264 ± 0.0811475 | 3.17783 |

Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.

## Độ nhạy tham số adaptive

Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ 0.00558256 thành 0.598477; median HV đổi từ 0.867216 thành 0.092856.

Suy giảm tại population 200 là giới hạn quan trọng của cấu hình ở trần ngân sách này. Chưa có thí nghiệm cô lập nguyên nhân; không suy ra population lớn luôn tốt hơn hoặc restart là nguyên nhân.

| Tham số | Mức | Lượt hợp lệ | IGD median | IGD Q25–Q75 | HV median | Restart hoàn tất |
| --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.00889516 | 0.00873444–0.00931825 | 0.863823 | 0 |
| pop_size | 100 | 30 | 0.00558256 | 0.00497328–0.00669758 | 0.867216 | 0 |
| pop_size | 200 | 30 | 0.598477 | 0.359255–0.932499 | 0.092856 | 0 |
| prob_de | 0.2 | 30 | 0.0114036 | 0.00794539–0.021681 | 0.85686 | 0 |
| prob_de | 0.5 | 30 | 0.00558256 | 0.00497328–0.00669758 | 0.867216 | 0 |
| prob_de | 0.8 | 30 | 0.00466007 | 0.00449978–0.00499702 | 0.869327 | 0 |

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
