# WFG1_M3: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 1.41795 và mean HV 16.4028. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=3. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 1.41795 ± 0.0103613 | 16.4028 ± 0.170669 | 13.8696 |
| NSGA2 | 30/30 | 1.39246 ± 0.0309844 | 13.6941 ± 1.24201 | 8.26443 |
| RNSGA2 | 30/30 | 2.11616 ± 0.0543092 | 0.105352 ± 0.270438 | 5.41636 |
| DNSGA2 | 30/30 | 1.70689 ± 0.0453545 | 6.16076 ± 0.994495 | 6.22357 |
| NSGAII_SDR_OLS | 30/30 | 1.38814 ± 0.0207584 | 16.5964 ± 0.284125 | 8.77273 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
