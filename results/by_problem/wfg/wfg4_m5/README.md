# WFG4_M5: báo cáo riêng

Bài toán này thuộc phần mở rộng nghiên cứu. Các bảng dưới đây giữ riêng từng đợt chạy; kết quả không được cộng với ZDT hoặc các cấu hình số mục tiêu khác.

IGD (inverted generational distance) thấp hơn và HV (hypervolume) cao hơn là tốt hơn theo reference front/point đã lưu. Dữ liệu được mô tả bằng mean ± độ lệch chuẩn mẫu (SD); runtime là giây/lượt trong môi trường đã đo.

## benchmark_wfg_scaling

Đợt này có 5 thuật toán. OADE_NSGAII có 30/30 lượt hợp lệ, mean IGD 1.38378 và mean HV 663.471. Mỗi thuật toán được lên lịch 30 seed (42–71), trần 20.000 đánh giá, population 100.

Cấu hình lưu trong bảng: n_var=24, n_obj=5. Số cặp hợp lệ và phép loại lượt không hợp lệ phải đọc theo từng so sánh, không mặc định mọi kiểm định đều có 30 cặp.

| ID thuật toán | Hợp lệ/tổng | IGD mean ± SD | HV mean ± SD | Giây/lượt |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 30/30 | 1.38378 ± 0.0581451 | 663.471 ± 80.3449 | 9.68408 |
| NSGA2 | 30/30 | 1.23067 ± 0.0527609 | 915.694 ± 89.9789 | 5.30658 |
| RNSGA2 | 30/30 | 3.68988 ± 0.285738 | 280.65 ± 31.1723 | 6.38293 |
| DNSGA2 | 30/30 | 1.23434 ± 0.0563479 | 894.704 ± 107.37 | 4.99949 |
| NSGAII_SDR_OLS | 30/30 | 1.42312 ± 0.0629387 | 693.096 ± 118.865 | 4.83443 |

[Báo cáo và toàn bộ kiểm định của đợt này](reports/benchmark_wfg_scaling.md). P-value/Holm giữ nguyên họ hiệu chỉnh gốc; không hiệu chỉnh lại riêng theo thư mục. Runtime phản ánh bản triển khai và môi trường, không phải độ phức tạp độc lập phần cứng.

## Giới hạn và bổ sung

Không gộp các bảng có tập thuật toán khác nhau thành số lượt độc lập. Không phát hiện khác biệt không đồng nghĩa tương đương; các kết quả dưới đây không xác lập lợi thế tổng quát của OADE.

Chỉ có báo cáo classic/adaptive, ablation hoặc độ nhạy riêng khi dữ liệu của chính bài toán đó đã được bổ sung và kiểm tra. Không thay bằng kết quả ZDT.

## Nguồn của bài toán

- [Tải CSV dạng ZIP](csv_results.zip)
- [Manifest và SHA-256](manifest.json)
- [Danh mục báo cáo](reports/README.md)
- [Trở về WFG](../README.md)
