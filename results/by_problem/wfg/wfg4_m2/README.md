# WFG4_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_m2

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0332224 và mean HV 2.146. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0332224 ± 0.00350899 | 2.146 ± 0.0168258 | 10.2408 |
| NSGA2 | 30/30 | 0.0263514 ± 0.00398152 | 2.20066 ± 0.0133641 | 5.46829 |
| RNSGA2 | 30/30 | 0.776159 ± 0.0876585 | 1.31845 ± 0.0363488 | 5.63939 |
| DNSGA2 | 30/30 | 0.027004 ± 0.00451905 | 2.19368 ± 0.0160338 | 5.36085 |
| CGDE_NSGAII | 30/30 | 0.0792816 ± 0.0026062 | 1.91727 ± 0.011875 | 238.423 |
| NSGAII_SDR_OLS | 30/30 | 0.253584 ± 0.0489736 | 1.25448 ± 0.151017 | 6.29585 |
| CE_MOEA | 30/30 | 0.0715537 ± 0.00532457 | 1.95327 ± 0.0275459 | 360.878 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_m2.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0332224 và mean HV 2.146. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0332224 ± 0.00350899 | 2.146 ± 0.0168258 | 10.2408 |
| NSGA2 | 30/30 | 0.0263514 ± 0.00398152 | 2.20066 ± 0.0133641 | 5.46829 |
| RNSGA2 | 30/30 | 0.776159 ± 0.0876585 | 1.31845 ± 0.0363488 | 5.63939 |
| DNSGA2 | 30/30 | 0.027004 ± 0.00451905 | 2.19368 ± 0.0160338 | 5.36085 |
| NSGAII_SDR_OLS | 30/30 | 0.253584 ± 0.0489736 | 1.25448 ± 0.151017 | 6.29585 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
