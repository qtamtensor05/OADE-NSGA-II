# DTLZ3_M3: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 2.52939 và mean HV 0.0407079. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=12, n_obj=3. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 2.52939 ± 1.49312 | 0.0407079 ± 0.15509 | 9.70128 |
| NSGA2 | 30/30 | 15.3961 ± 5.7943 | 0 ± 0 | 4.58032 |
| RNSGA2 | 30/30 | 15.6956 ± 6.22559 | 0 ± 0 | 2.89526 |
| DNSGA2 | 30/30 | 20.0643 ± 7.58985 | 0 ± 0 | 4.29965 |
| CGDE_NSGAII | 30/30 | 89.0957 ± 50.8062 | 0 ± 0 | 224.745 |
| NSGAII_SDR_OLS | 30/30 | 51.3491 ± 28.1096 | 0 ± 0 | 5.94382 |
| CE_MOEA | 30/30 | 35.291 ± 15.0291 | 0 ± 0 | 205.296 |

Giới hạn chất lượng của riêng cấu hình này: OADE có **27/30 lượt HV = 0** theo điểm tham chiếu đã dùng. HV = 0 không tự đồng nghĩa với output không hợp lệ theo kiểm tra cấu trúc; cần giữ hai tiêu chí tách biệt.

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
