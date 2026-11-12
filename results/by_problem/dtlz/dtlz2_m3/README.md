# DTLZ2_M3: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.0766053 và mean HV 0.684464. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=12, n_obj=3. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.0766053 ± 0.00275687 | 0.684464 ± 0.00720538 | 5.63193 |
| NSGA2 | 30/30 | 0.0719165 ± 0.00249944 | 0.7014 ± 0.00658344 | 2.75778 |
| RNSGA2 | 30/30 | 0.450833 ± 0.00654874 | 0.250539 ± 0.0061373 | 3.82749 |
| DNSGA2 | 30/30 | 0.0715652 ± 0.00328283 | 0.700857 ± 0.0061776 | 2.75296 |
| CGDE_NSGAII | 30/30 | 0.0684255 ± 0.00207281 | 0.697546 ± 0.00412858 | 126.939 |
| NSGAII_SDR_OLS | 29/30 | 0.842408 ± 0.170264 | 0.145896 ± 0.0757661 | 3.07363 |
| CE_MOEA | 30/30 | 0.0782169 ± 0.00295766 | 0.67936 ± 0.00603614 | 136.811 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
