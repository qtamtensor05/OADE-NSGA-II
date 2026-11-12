# WFG9_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_m2

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0363613 và mean HV 2.15299. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0363613 ± 0.00780928 | 2.15299 ± 0.0171184 | 5.15657 |
| NSGA2 | 30/30 | 0.110123 ± 0.0376733 | 1.79242 ± 0.188414 | 3.4441 |
| RNSGA2 | 30/30 | 0.621958 ± 0.0709063 | 1.20363 ± 0.174846 | 4.07963 |
| DNSGA2 | 30/30 | 0.112191 ± 0.0341716 | 1.7865 ± 0.177633 | 4.11927 |
| CGDE_NSGAII | 30/30 | 0.118058 ± 0.0268055 | 1.76547 ± 0.140067 | 453.108 |
| NSGAII_SDR_OLS | 30/30 | 0.29966 ± 0.0596967 | 1.14655 ± 0.152618 | 3.46102 |
| CE_MOEA | 30/30 | 0.129474 ± 0.00135727 | 1.70156 ± 0.00277576 | 434.252 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_m2.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0363613 và mean HV 2.15299. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0363613 ± 0.00780928 | 2.15299 ± 0.0171184 | 5.15657 |
| NSGA2 | 30/30 | 0.110123 ± 0.0376733 | 1.79242 ± 0.188414 | 3.4441 |
| RNSGA2 | 30/30 | 0.621958 ± 0.0709063 | 1.20363 ± 0.174846 | 4.07963 |
| DNSGA2 | 30/30 | 0.112191 ± 0.0341716 | 1.7865 ± 0.177633 | 4.11927 |
| NSGAII_SDR_OLS | 30/30 | 0.29966 ± 0.0596967 | 1.14655 ± 0.152618 | 3.46102 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
