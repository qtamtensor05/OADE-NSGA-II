# WFG1_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_m2

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 1.02608 và mean HV 1.77197. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 1.02608 ± 0.0107426 | 1.77197 ± 0.0304387 | 12.5302 |
| NSGA2 | 30/30 | 1.20215 ± 0.0747406 | 0.903008 ± 0.190228 | 6.9754 |
| RNSGA2 | 30/30 | 1.69532 ± 0.0703903 | 0 ± 0 | 6.39909 |
| DNSGA2 | 30/30 | 1.56666 ± 0.0426862 | 0.00981927 ± 0.0296991 | 5.78754 |
| CGDE_NSGAII | 30/30 | 1.13856 ± 0.00725811 | 1.45262 ± 0.0179108 | 214.86 |
| NSGAII_SDR_OLS | 30/30 | 1.14603 ± 0.0181704 | 1.42008 ± 0.0422428 | 8.26199 |
| CE_MOEA | 30/30 | 1.1299 ± 0.00854937 | 1.48311 ± 0.0233624 | 253.891 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_m2.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 1.02608 và mean HV 1.77197. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 1.02608 ± 0.0107426 | 1.77197 ± 0.0304387 | 12.5302 |
| NSGA2 | 30/30 | 1.20215 ± 0.0747406 | 0.903008 ± 0.190228 | 6.9754 |
| RNSGA2 | 30/30 | 1.69532 ± 0.0703903 | 0 ± 0 | 6.39909 |
| DNSGA2 | 30/30 | 1.56666 ± 0.0426862 | 0.00981927 ± 0.0296991 | 5.78754 |
| NSGAII_SDR_OLS | 30/30 | 1.14603 ± 0.0181704 | 1.42008 ± 0.0422428 | 8.26199 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
