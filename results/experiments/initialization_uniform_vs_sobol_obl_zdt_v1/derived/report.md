# Đối chứng khởi tạo Uniform và Sobol–OBL

Thí nghiệm ghép seed trên ZDT.
Tổng số run: **300**; hợp lệ: **300**.

## Hai phương pháp khởi tạo

| Phương pháp | Cách tạo quần thể | Chi phí ban đầu |
|:---|:---|---:|
| Uniform | Uniform theo seed, cùng cách khởi tạo benchmark đối chứng trước đây | $N$ evaluation |
| Sobol–OBL | Scrambled Sobol + GOBL của OADE hiện có; chọn $N$ cá thể từ $2N$ ứng viên | $2N$ evaluation |

Sobol và GOBL dùng seed tường minh, RNG khởi tạo riêng; không rút số từ RNG tiến hóa. Sau khởi tạo, cả hai nhánh reset cùng seed tìm kiếm; quỹ đạo có thể phân kỳ do quần thể khác nhau. Ghép seed không có nghĩa cùng quần thể đầu.
Cả hai giữ adaptive restart, success-rate, F/CR adaptation, neighborhood và OBL định kỳ. Chỉ thay cách khởi tạo. Gói Sobol–OBL được đo như một thành phần kết hợp, chưa tách đóng góp Sobol và OBL.
## Kết quả cuối — median

| Bài | Phương pháp | Valid/run | IGD ↓ | HV ↑ | Runtime (s) |
|:---|:---|---:|---:|---:|---:|
| ZDT1 | uniform | 30/30 | 0.0044769 | 0.8709181 | 3.744 |
| ZDT1 | sobol_obl | 30/30 | 0.0044690 | 0.8709242 | 4.145 |
| ZDT2 | uniform | 30/30 | 0.0047255 | 0.5377362 | 3.954 |
| ZDT2 | sobol_obl | 30/30 | 0.0046543 | 0.5377180 | 4.134 |
| ZDT3 | uniform | 30/30 | 0.0050642 | 1.0512775 | 3.906 |
| ZDT3 | sobol_obl | 30/30 | 0.0050153 | 1.0512537 | 4.084 |
| ZDT4 | uniform | 30/30 | 0.0055402 | 0.8675027 | 4.705 |
| ZDT4 | sobol_obl | 30/30 | 0.0056375 | 0.8673616 | 4.679 |
| ZDT6 | uniform | 30/30 | 0.0038108 | 0.4380637 | 4.133 |
| ZDT6 | sobol_obl | 30/30 | 0.0038224 | 0.4381861 | 3.946 |

## Cách đọc đối chứng

Một cặp uniform–sobol_obl trên mỗi bài và chỉ số. Wilcoxon signed-rank hai phía, zero_method=wilcox, xấp xỉ chuẩn; toàn delta bằng 0 đặt p=1. Holm theo cặp/bài/metric; với một cặp, p hiệu chỉnh bằng p thô. Alpha=0,05. Không phát hiện khác biệt không chứng minh tương đương. Nếu tổng hợp kết luận chung qua nhiều bài/metric, cần xem xét thêm đa kiểm định.
Trong comparisons.csv, delta = uniform − sobol_obl: IGD dương ủng hộ Sobol–OBL; HV âm ủng hộ Sobol–OBL. Các cặp chất lượng chỉ gồm run hợp lệ, có ghi số cặp bị loại.
So sánh ở cùng cap tổng, không cùng số thế hệ: Sobol–OBL trả chi phí khởi tạo cao hơn và còn ít ngân sách tiến hóa hơn. Tất cả objective calls (khởi tạo, OBL định kỳ và restart) tính vào cap; batch nguyên tử có thể để dư, phải đọc n_eval thực.
summary.csv chứa chất lượng sau khởi tạo và chất lượng cuối, mean/SD/median/Q25/Q75, thời gian và số restart. Chất lượng đầu tốt hơn chưa bảo đảm kết quả cuối tốt hơn. Runtime chứa cả khởi tạo, tìm kiếm và instrumentation trên máy/worker đang dùng.
Primary JSON lưu X/F đầu được chọn, chi phí khởi tạo, X/F cuối, convergence, probability trace và restart events. Manifest lưu hash mã/môi trường/reference và checkpoint; không trộn dữ liệu lịch sử hay resume sau đổi mã.
