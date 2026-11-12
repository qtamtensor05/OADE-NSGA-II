# ZDT1: kết quả OADE-NSGA-II

Trên ZDT1, OADE adaptive đạt IGD trung bình 0.00447533 và HV trung bình 0.870866; NSGA2 lần lượt đạt 0.00517466 và 0.868053 trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.

## Thiết kế và phạm vi

Bài toán có 30 biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.

## Benchmark adaptive: 7 thuật toán

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00447533 ± 0.00025124 | 0.870866 ± 0.000232239 | 14.4968 |
| NSGA2 | 30/30 | 0.00517466 ± 0.000297904 | 0.868053 ± 0.000417268 | 0.92875 |
| RNSGA2 | 30/30 | 0.632973 ± 0.0876243 | 0.348062 ± 0.0938884 | 2.75757 |
| DNSGA2 | 30/30 | 0.00563295 ± 0.000423465 | 0.867066 ± 0.00068501 | 0.853377 |
| CGDE_NSGAII | 30/30 | 0.00743342 ± 0.000527482 | 0.863362 ± 0.000968519 | 39.5621 |
| NSGAII_SDR_OLS | 30/30 | 0.0156331 ± 0.0197044 | 0.858421 ± 0.0148456 | 1.04961 |
| CE_MOEA | 30/30 | 0.00690817 ± 0.000873872 | 0.864472 ± 0.00177852 | 38.8171 |

So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.

| Chỉ số | n cặp | p Holm | Rank-biserial | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| IGD | 30 | 5.58794e-08 | 1 | reference_better |
| HV | 30 | 5.58794e-08 | 1 | reference_better |

Các đối chứng còn lại và kết quả từng kiểm định được giữ trong [báo cáo benchmark adaptive](reports/benchmark_adaptive.md); không suy rộng kết quả của bài toán này sang bài toán khác.

## Classic và adaptive

Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.

| Cấu hình | IGD mean | HV mean |
| --- | --- | --- |
| Classic, seed 42–71 | 0.00592521 | 0.868961 |
| Adaptive, seed 42–71 | 0.00447533 | 0.870866 |

Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_FULL | 30/30 | 0.00792113 ± 0.00475444 | 0.866365 ± 0.00656188 | 10.4503 |
| OADE_NO_RESTART | 30/30 | 0.00453077 ± 0.000328779 | 0.870819 ± 0.000237045 | 6.14515 |
| OADE_ADAPTIVE_RESTART | 30/30 | 0.00453077 ± 0.000328779 | 0.870819 ± 0.000237045 | 7.41927 |

Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.

## Độ nhạy tham số adaptive

Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ 0.00439707 thành 0.00222923; median HV đổi từ 0.870962 thành 0.87382.

Thay đổi population đồng thời thay đổi số thế hệ khả dụng và độ phân giải tập nghiệm ở ngân sách cố định. Vì vậy chênh lệch IGD không tự đo riêng tốc độ hội tụ.

| Tham số | Mức | Lượt hợp lệ | IGD median | IGD Q25–Q75 | HV median | Restart hoàn tất |
| --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.00910643 | 0.008765–0.0096179 | 0.864754 | 0 |
| pop_size | 100 | 30 | 0.00439707 | 0.00425475–0.00462165 | 0.870962 | 0 |
| pop_size | 200 | 30 | 0.00222923 | 0.00212277–0.0022936 | 0.87382 | 0 |
| prob_de | 0.2 | 30 | 0.00443502 | 0.00421447–0.00456232 | 0.87098 | 0 |
| prob_de | 0.5 | 30 | 0.00439707 | 0.00425475–0.00462165 | 0.870962 | 0 |
| prob_de | 0.8 | 30 | 0.00442112 | 0.00426895–0.00464298 | 0.870941 | 0 |

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
