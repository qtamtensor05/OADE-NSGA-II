# DTLZ4_M5: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.372651 và mean HV 0.647577. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=14, n_obj=5. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.372651 ± 0.0281246 | 0.647577 ± 0.104992 | 3.04027 |
| NSGA2 | 30/30 | 0.802355 ± 0.108677 | 0.0381603 ± 0.0552811 | 1.59648 |
| RNSGA2 | 30/30 | 0.73876 ± 0.105688 | 0.337004 ± 0.215167 | 5.41836 |
| DNSGA2 | 30/30 | 0.787657 ± 0.120281 | 0.0571582 ± 0.0630591 | 1.50764 |
| CGDE_NSGAII | 30/30 | 0.38866 ± 0.0176401 | 0.654599 ± 0.0588276 | 72.2524 |
| NSGAII_SDR_OLS | 27/30 | 1.11631 ± 0.0251042 | 0.150303 ± 0.0190501 | 2.68334 |
| CE_MOEA | 30/30 | 0.383574 ± 0.0162317 | 0.628771 ± 0.0786031 | 72.2425 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
