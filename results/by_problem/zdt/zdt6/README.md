# ZDT6: kết quả OADE-NSGA-II

Trên ZDT6, OADE adaptive đạt IGD trung bình 0.003844 và HV trung bình 0.438177; NSGA2 lần lượt đạt 0.0163681 và 0.417891 trong benchmark seed 42–71. Bảng bên dưới giữ đầy đủ các đối chứng của bài toán này.

## Thiết kế và phạm vi

Bài toán có 10 biến và 2 mục tiêu. Benchmark dùng population 100, trần 20.000 lần đánh giá và 30 seed ghép cặp (42–71). Đơn vị phân tích là một lượt chạy ngẫu nhiên. Một lượt có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn tương ứng với chất lượng tốt hơn theo front/điểm tham chiếu của bài toán. Benchmark báo cáo mean ± độ lệch chuẩn mẫu (SD); SD mô tả phân tán giữa lượt chạy, không phải khoảng tin cậy của hiệu ứng.

## Benchmark adaptive: 7 thuật toán

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.003844 ± 0.000192923 | 0.438177 ± 0.000252795 | 13.3414 |
| NSGA2 | 30/30 | 0.0163681 ± 0.00201149 | 0.417891 ± 0.00287211 | 2.05538 |
| RNSGA2 | 30/30 | 0.185764 ± 0.0927869 | 0.267636 ± 0.06859 | 2.20712 |
| DNSGA2 | 30/30 | 0.0225884 ± 0.00279408 | 0.408917 ± 0.00399733 | 2.01973 |
| CGDE_NSGAII | 30/30 | 0.00382305 ± 0.000222667 | 0.439057 ± 0.000199467 | 103.072 |
| NSGAII_SDR_OLS | 30/30 | 0.139446 ± 0.0827475 | 0.282923 ± 0.0589616 | 2.12093 |
| CE_MOEA | 30/30 | 0.00495683 ± 0.000335953 | 0.437794 ± 0.000359974 | 101.561 |

So sánh với NSGA2 dưới đây dùng Wilcoxon signed-rank ghép cặp hai phía. Holm được giữ theo họ gốc gồm 30 so sánh trên 5 bài ZDT, riêng cho mỗi chỉ số; không hiệu chỉnh lại sau khi tách báo cáo.

| Chỉ số | n cặp | p Holm | Rank-biserial | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| IGD | 30 | 5.58794e-08 | 1 | reference_better |
| HV | 30 | 5.58794e-08 | 1 | reference_better |

Giới hạn đối chứng cần giữ khi đọc kết quả: CGDE_NSGAII có mean IGD 0.00382305 và mean HV 0.439057. Bởi vậy lợi thế so với NSGA2 không được diễn giải thành ưu thế trước mọi thuật toán trên ZDT6.

| Đối chứng | Chỉ số | n cặp | p Holm | Kết quả theo OADE |
| --- | --- | --- | --- | --- |
| CGDE_NSGAII | IGD | 30 | 0.776569 | no_significant_difference |
| CGDE_NSGAII | HV | 30 | 5.58794e-08 | comparison_better |

Kiểm định IGD không phát hiện khác biệt với CGDE_NSGAII, trong khi kiểm định HV ưu thế cho CGDE_NSGAII theo bảng đã lưu. Đây là hai kết quả khác nhau, không phải bằng chứng tương đương trên IGD. [Toàn bộ kiểm định](reports/benchmark_adaptive.md).

## Classic và adaptive

Hai benchmark dùng chung sáu block đối chứng. Bảng này chỉ đối chiếu cấu hình OADE; chênh lệch trung bình giữa hai bảng không phải một kiểm định mới.

| Cấu hình | IGD mean | HV mean |
| --- | --- | --- |
| Classic, seed 42–71 | 0.00528589 | 0.436557 |
| Adaptive, seed 42–71 | 0.003844 | 0.438177 |

Thí nghiệm xác nhận dùng riêng seed 1000–1029, 30 lượt cho mỗi biến thể. Không ghép những lượt này vào benchmark seed 42–71.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_FULL | 30/30 | 0.00656552 ± 0.00502073 | 0.435092 ± 0.00559134 | 7.3016 |
| OADE_NO_RESTART | 30/30 | 0.00386259 ± 0.000187961 | 0.438147 ± 0.000249285 | 8.01504 |
| OADE_ADAPTIVE_RESTART | 30/30 | 0.00387635 ± 0.000182962 | 0.438148 ± 0.000247478 | 7.47499 |

Kiểm định xác nhận và chiều effect size được giữ trong [báo cáo restart](reports/restart_confirmation.md). Do telemetry trigger không được lưu trong đợt này, chất lượng cuối không tự chứng minh restart adaptive đã kích hoạt hoặc gây ra cải thiện. So sánh trực tiếp với no-restart cần được giữ khi đánh giá cơ chế.

## Độ nhạy tham số adaptive

Ở OFAT seed 6000–6029, tăng population từ 100 lên 200 làm median IGD đổi từ 0.00382752 thành 0.0024559; median HV đổi từ 0.438266 thành 0.439487.

Thay đổi population đồng thời thay đổi số thế hệ khả dụng và độ phân giải tập nghiệm ở ngân sách cố định. Vì vậy chênh lệch IGD không tự đo riêng tốc độ hội tụ.

| Tham số | Mức | Lượt hợp lệ | IGD median | IGD Q25–Q75 | HV median | Restart hoàn tất |
| --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.00734024 | 0.00716027–0.00755461 | 0.434608 | 1 |
| pop_size | 100 | 30 | 0.00382752 | 0.0036758–0.00396771 | 0.438266 | 6 |
| pop_size | 200 | 30 | 0.0024559 | 0.00233474–0.00255445 | 0.439487 | 1 |
| prob_de | 0.2 | 30 | 0.00395148 | 0.00379471–0.00421622 | 0.437647 | 22 |
| prob_de | 0.5 | 30 | 0.00382752 | 0.0036758–0.00396771 | 0.438266 | 6 |
| prob_de | 0.8 | 30 | 0.00362852 | 0.00349685–0.0037619 | 0.438773 | 2 |

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
