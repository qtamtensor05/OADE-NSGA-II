# WFG6_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_m2

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0547901 và mean HV 2.04237. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0547901 ± 0.0164568 | 2.04237 ± 0.0833676 | 4.4234 |
| NSGA2 | 30/30 | 0.0716943 ± 0.0107337 | 1.95804 ± 0.0496875 | 2.73484 |
| RNSGA2 | 30/30 | 0.772488 ± 0.0918258 | 1.15881 ± 0.0880385 | 3.58073 |
| DNSGA2 | 30/30 | 0.0737715 ± 0.0151702 | 1.9581 ± 0.0501883 | 2.96434 |
| CGDE_NSGAII | 30/30 | 0.0338352 ± 0.0104752 | 2.182 ± 0.0261591 | 448.085 |
| NSGAII_SDR_OLS | 30/30 | 0.291287 ± 0.0538188 | 1.23937 ± 0.147094 | 2.84962 |
| CE_MOEA | 30/30 | 0.116135 ± 0.0162203 | 1.73085 ± 0.0880383 | 283.463 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_m2.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0547901 và mean HV 2.04237. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0547901 ± 0.0164568 | 2.04237 ± 0.0833676 | 4.4234 |
| NSGA2 | 30/30 | 0.0716943 ± 0.0107337 | 1.95804 ± 0.0496875 | 2.73484 |
| RNSGA2 | 30/30 | 0.772488 ± 0.0918258 | 1.15881 ± 0.0880385 | 3.58073 |
| DNSGA2 | 30/30 | 0.0737715 ± 0.0151702 | 1.9581 ± 0.0501883 | 2.96434 |
| NSGAII_SDR_OLS | 30/30 | 0.291287 ± 0.0538188 | 1.23937 ± 0.147094 | 2.84962 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
