# DTLZ3_M2: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 1.34808 và mean HV 0.0997882. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=11, n_obj=2. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 1.34808 ± 1.27211 | 0.0997882 ± 0.158176 | 8.59561 |
| NSGA2 | 30/30 | 2.64577 ± 1.99319 | 0.0115128 ± 0.0550477 | 3.69395 |
| RNSGA2 | 30/30 | 4.65993 ± 3.10363 | 0 ± 0 | 2.09326 |
| DNSGA2 | 30/30 | 3.94583 ± 2.37758 | 0 ± 0 | 3.80679 |
| CGDE_NSGAII | 30/30 | 106.434 ± 41.4792 | 0 ± 0 | 235.126 |
| NSGAII_SDR_OLS | 30/30 | 33.4945 ± 25.6911 | 0 ± 0 | 6.41065 |
| CE_MOEA | 30/30 | 23.3953 ± 12.7191 | 0 ± 0 | 192.977 |

Giới hạn chất lượng của riêng cấu hình này: OADE có **19/30 lượt HV = 0** theo điểm tham chiếu đã dùng. HV = 0 không tự đồng nghĩa với output không hợp lệ theo kiểm tra cấu trúc; cần giữ hai tiêu chí tách biệt.

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
