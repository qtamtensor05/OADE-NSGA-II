# DTLZ2_M5: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_dtlz

Đợt này có 7 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 0.42009 và mean HV 0.460191. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=14, n_obj=5. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 0.42009 ± 0.0345094 | 0.460191 ± 0.0846499 | 8.32174 |
| NSGA2 | 30/30 | 0.457093 ± 0.0593325 | 0.430292 ± 0.110118 | 4.39282 |
| RNSGA2 | 30/30 | 0.66922 ± 0.0334772 | 0.255631 ± 0.0403322 | 3.3619 |
| DNSGA2 | 30/30 | 0.468075 ± 0.0474111 | 0.391872 ± 0.0957259 | 3.68244 |
| CGDE_NSGAII | 30/30 | 0.636379 ± 0.0941996 | 0.156506 ± 0.0919104 | 218.084 |
| NSGAII_SDR_OLS | 30/30 | 1.04636 ± 0.121364 | 0.12351 ± 0.0804767 | 5.90488 |
| CE_MOEA | 30/30 | 0.466914 ± 0.0218494 | 0.356086 ± 0.0732435 | 207.812 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_dtlz.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về DTLZ](../README.md)
