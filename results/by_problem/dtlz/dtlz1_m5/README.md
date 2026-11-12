# DTLZ1_M5: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 2.55293 và mean HV 0.00919743. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=9, n_obj=5. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 2.55293 ± 4.97343 | 0.00919743 ± 0.0219176 | 6.91154 |
| NSGA2 | 30/30 | 39.7519 ± 14.7814 | 0 ± 0 | 3.31465 |
| RNSGA2 | 30/30 | 16.1939 ± 10.6005 | 0 ± 0 | 7.04479 |
| DNSGA2 | 30/30 | 37.3031 ± 15.4556 | 0 ± 0 | 3.30436 |
| CGDE_NSGAII | 30/30 | 12.2676 ± 4.97115 | 0 ± 0 | 170.738 |
| NSGAII_SDR_OLS | 30/30 | 32.6593 ± 11.9307 | 0 ± 0 | 4.16342 |
| CE_MOEA | 30/30 | 6.89971 ± 2.47769 | 0 ± 0 | 189.2 |

Giới hạn chất lượng của riêng cấu hình này: OADE có **17/30 lượt HV = 0** theo điểm tham chiếu đã dùng. HV = 0 không tự đồng nghĩa với output không hợp lệ theo kiểm tra cấu trúc; cần giữ hai tiêu chí tách biệt.

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
