# DTLZ4_M3: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0786625 và mean HV 0.680528. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=12, n_obj=3. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0786625 ± 0.00289827 | 0.680528 ± 0.00718355 | 2.79677 |
| NSGA2 | 30/30 | 0.0698968 ± 0.00297973 | 0.707544 ± 0.00607245 | 1.51696 |
| RNSGA2 | 30/30 | 0.632848 ± 0.146837 | 0.233086 ± 0.0990346 | 5.45695 |
| DNSGA2 | 30/30 | 0.0691032 ± 0.00207763 | 0.708986 ± 0.00445435 | 1.42092 |
| CGDE_NSGAII | 30/30 | 0.116432 ± 0.142161 | 0.673255 ± 0.0729688 | 72.6821 |
| NSGAII_SDR_OLS | 29/30 | 0.948479 ± 1.25786e-06 | 0.120996 ± 3.18031e-06 | 2.75142 |
| CE_MOEA | 30/30 | 0.0798476 ± 0.00302256 | 0.675123 ± 0.00775663 | 72.4059 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
