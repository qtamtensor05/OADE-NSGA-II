# DTLZ4_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.00513331 và mean HV 0.418761. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=11, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00513331 ± 0.000212008 | 0.418761 ± 0.000356253 | 2.73619 |
| NSGA2 | 30/30 | 0.275331 ± 0.36109 | 0.305909 ± 0.151613 | 1.64391 |
| RNSGA2 | 30/30 | 0.490558 ± 0.214511 | 0.175908 ± 0.0707743 | 7.67105 |
| DNSGA2 | 30/30 | 0.103326 ± 0.254759 | 0.378151 ± 0.106976 | 1.4376 |
| CGDE_NSGAII | 27/30 | 0.00528141 ± 0.000194838 | 0.41814 ± 0.000370651 | 73.0864 |
| NSGAII_SDR_OLS | 27/30 | 0.741922 ± 6.13884e-06 | 0.109994 ± 1.79527e-05 | 2.70141 |
| CE_MOEA | 30/30 | 0.00520312 ± 0.000186965 | 0.418381 ± 0.00026741 | 72.4274 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
