# DTLZ1_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.00228432 và mean HV 0.233218. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=6, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.00228432 ± 0.000234932 | 0.233218 ± 0.000264655 | 5.06604 |
| NSGA2 | 30/30 | 0.00294605 ± 0.000834274 | 0.232349 ± 0.000851819 | 2.52568 |
| RNSGA2 | 30/30 | 0.134576 ± 0.107422 | 0.145778 ± 0.0472495 | 5.02317 |
| DNSGA2 | 30/30 | 0.00375993 ± 0.00229934 | 0.231582 ± 0.00205019 | 2.38585 |
| CGDE_NSGAII | 30/30 | 1.36969 ± 0.372146 | 0 ± 0 | 178.924 |
| NSGAII_SDR_OLS | 26/30 | 5.53112 ± 3.60081 | 0.00380253 ± 0.0134597 | 4.05607 |
| CE_MOEA | 30/30 | 0.922493 ± 0.963149 | 0.022708 ± 0.0527111 | 155.433 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
