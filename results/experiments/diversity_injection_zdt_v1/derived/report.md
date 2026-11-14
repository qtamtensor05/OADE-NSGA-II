# Đối chứng bơm đa dạng OBL định kỳ

Đối chứng ghép seed trên ZDT.
Đã đo **300 run**, hợp lệ **300**.

## Thiết kế

| Nhánh | OBL định kỳ | Các cơ chế chung |
|:---|:---|:---|
| Bật | Chỉ số thế hệ 0, 10, 20, … | Uniform cùng quần thể đầu/seed, adaptive restart, success-rate, F/CR, neighborhood |
| Tắt | Không gọi OBL định kỳ | Giữ nguyên các cơ chế còn lại |

Kernel OBL hiện có chọn từng cá thể với xác suất jump_rate=0,2 rồi phản chiếu theo bounds quần thể hoặc bounds bài toán (50/50). Chỉ các ứng viên được sinh mới tốn evaluation; không mặc định mỗi lần bơm có đủ 100 ứng viên.
Tắt bơm định kỳ không tắt adaptive restart hoặc phần OBL/Gauss bên trong restart. Vì vậy nhánh tắt vẫn có thể được restart làm mới quần thể. Khởi tạo Sobol–OBL không tham gia cả hai nhánh.
## Chất lượng cuối — median

| Bài | Nhánh | Valid/run | IGD ↓ | HV ↑ | Runtime (s) |
|:---|:---|---:|---:|---:|---:|
| ZDT1 | Bật | 30/30 | 0.0044769 | 0.8709181 | 15.679 |
| ZDT1 | Tắt | 30/30 | 0.0043939 | 0.8709198 | 17.762 |
| ZDT2 | Bật | 30/30 | 0.0047255 | 0.5377362 | 4.242 |
| ZDT2 | Tắt | 30/30 | 0.0046648 | 0.5377146 | 17.278 |
| ZDT3 | Bật | 30/30 | 0.0050642 | 1.0512775 | 4.167 |
| ZDT3 | Tắt | 30/30 | 0.0050115 | 1.0512146 | 17.770 |
| ZDT4 | Bật | 30/30 | 0.0055402 | 0.8675027 | 19.388 |
| ZDT4 | Tắt | 30/30 | 0.4001848 | 0.3400835 | 20.402 |
| ZDT6 | Bật | 30/30 | 0.0038108 | 0.4380637 | 16.576 |
| ZDT6 | Tắt | 30/30 | 0.0038767 | 0.4380203 | 18.239 |

## Bằng chứng kích hoạt và chi phí

| Bài | Nhánh | Lần gọi / hoàn tất | Ứng viên OBL | Evaluation OBL | Được giữ sau chọn lọc | Restart |
|:---|:---|---:|---:|---:|---:|---:|
| ZDT1 | Bật | 600 / 600 | 11931 | 11931 | 1461 | 0 |
| ZDT1 | Tắt | 0 / 0 | 0 | 0 | 0 | 0 |
| ZDT2 | Bật | 600 / 600 | 12111 | 12111 | 1873 | 0 |
| ZDT2 | Tắt | 0 / 0 | 0 | 0 | 0 | 0 |
| ZDT3 | Bật | 600 / 600 | 11936 | 11936 | 1171 | 0 |
| ZDT3 | Tắt | 0 / 0 | 0 | 0 | 0 | 0 |
| ZDT4 | Bật | 600 / 600 | 12017 | 12017 | 4799 | 0 |
| ZDT4 | Tắt | 0 / 0 | 0 | 0 | 0 | 0 |
| ZDT6 | Bật | 600 / 600 | 12063 | 12063 | 1034 | 3 |
| ZDT6 | Tắt | 0 / 0 | 0 | 0 | 0 | 4 |

## Đọc kết quả

comparisons.csv dùng delta = bật − tắt: IGD âm hoặc HV dương ủng hộ bật. Wilcoxon signed-rank hai phía trên cặp seed hợp lệ, zero_method=wilcox, xấp xỉ chuẩn; toàn delta zero đặt p=1. Alpha=0,05. p_holm_all_endpoints hiệu chỉnh đồng thời mọi bài × 2 chỉ số (10 endpoint khi chạy đủ ZDT); p_holm giữ họ từng bài/metric cho truy vết. Không phát hiện khác biệt không chứng minh tương đương.
Cả hai có cùng cap tổng, bao gồm khởi tạo, OBL định kỳ và restart. Nhánh bật trả evaluation cho OBL nên có thể hoàn tất ít thế hệ hơn; không bù thêm ngân sách. Batch nguyên tử có thể để dư, xem n_eval.
diversity_events.csv ghi từng lần gọi, số ứng viên và evaluation, bị chặn ngân sách, thế hệ có hoàn tất chọn lọc hay không, số ứng viên còn lại trong quần thể sau chọn lọc. completed chỉ nghĩa đã sinh/xử lý OBL, không bảo đảm thế hệ đã hoàn tất; retained để trống khi chưa chọn lọc. Ứng viên được giữ không tự chứng minh đóng góp lâu dài.
summary.csv lưu mean, SD, median, Q25/Q75; chất lượng đầu và cuối, chi phí, runtime và xác suất DE. Primary JSON chứa X/F đầu/cuối, probability trace, convergence và cả hai loại sự kiện. Tần suất và số giữ lại là mô tả; lợi ích ròng cần đọc chất lượng cuối ở cùng cap.
Nếu khác biệt downstream làm restart kích hoạt khác nhau, đây là một phần tác động tổng của bật/tắt OBL định kỳ; thiết kế này chưa tách riêng cơ chế trung gian. Runtime mô tả máy/worker đang dùng, không suy ra độ phức tạp từ thời gian.
