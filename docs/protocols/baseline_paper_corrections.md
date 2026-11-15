# Đối chứng sau đối chiếu bài báo — 14/11/2026

Trạng thái hiện tại thay thế các mô tả trước sửa lỗi trong hai báo cáo audit. Các kết quả trước sửa không được dùng làm bằng chứng cho mã đã sửa; ZDT v2 là mốc đối chứng hiện tại. Không chạy benchmark đầy đủ trong lần sửa này.

| Đối chứng | Thay đổi mã | Nguồn và giới hạn |
|---|---|---|
| CGDE_NSGAII | Thay current-to-pbest/archive bằng hai toán tử cross-generation; bổ sung subrank, thế hệ trước chính xác, F theo cá thể và CR ngẫu nhiên | [Qiu, Xu, Tan — CEC 2014](https://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2014/WCCI/CEC-2014/PROGRAM/E-14533.pdf), mục III–IV. Đã tìm thấy đúng tên CGDE-NSGA-II; nhận định trước về việc chưa tìm được nguồn đã được cập nhật. |
| NSGAII_SDR_OLS | Bỏ cap 2N trong baseline; GA nhận toàn bộ P+S; SBX lấy ngẫu nhiên một trong hai con, bỏ thiên lệch luôn lấy con phía dưới | [Zhang, Wang, Wang — Mathematics 2023](https://doi.org/10.3390/math11081911), Algorithms 1–4. Vòng lặp tổng thể vẫn cần diễn giải do giả mã không nhất quán. |
| CE_MOEA | PM dùng số mũ eta như Algorithm 4; mặc định mục tiêu đa thuộc tính dùng cosine như phương trình in trong bài | [Sun et al. — bản v2](https://arxiv.org/html/2006.03996v2), Algorithms 1–4, Eqs. 5–10. ZDT chỉ đo lõi tìm kiếm; không tái lập community detection. |

## Quyết định triển khai cần công khai

CGDE: bài không ghi khoảng số cụ thể cho CR. Cấu hình dùng U(0,1). Khởi đầu chưa có thế hệ trước nên dùng P0 làm bootstrap; dùng subrank trên hợp hai thế hệ, đồng hạng khi giá trị bằng nhau, thứ tự ổn định khi khoảng cách bằng nhau, clip khi vượt bounds. Đây là các quy ước tái dựng, chưa xác nhận bằng mã tác giả.

SDR-OLS: hình Algorithm 4 lặp GA ở dòng 7/9, dòng 8 xếp hạng P0 dù đã lập R, và không ghi rõ cập nhật P0/cắt R về N. Không sao chép nguyên văn các bước mâu thuẫn thành thuật toán. Mã dùng vòng lặp P → LS → R=P+S → xếp hạng/crowding → GA → chọn N trên R+offspring. Đây là cách diễn giải đã ghi rõ, chưa phải chứng nhận tương đương mã tác giả. Hình Algorithm 1 xác nhận bước chuẩn hóa mục tiêu; giữ bước này.

Khi ngân sách FE kết thúc giữa local search, lấy ngẫu nhiên không hoàn lại từ toàn bộ tập lân cận còn có thể đánh giá, chọn lọc trên các nghiệm đã đánh giá và dừng. Không lấy một prefix cá thể. Đây là quy tắc kết thúc do benchmark áp đặt; local search ở thế hệ đầy đủ không bị cap. Chi phí OBL khởi tạo cũng được tính. Mã GA chung không được bài mô tả đủ để xác nhận mọi tham số SBX/PM; các giá trị cấu hình là lựa chọn tái dựng.

CE-MOEA: dùng biểu thức cosine in trong bài mặc dù diễn giải “nhỏ hơn đồng nhất hơn” có vấn đề về chiều tương tự. Chế độ `distance` là sửa đổi tùy chọn, không phải mặc định theo bài. Zero norm được quy ước cosine=0. Graph modularity hiện dùng góc nhìn vô hướng; chưa chứng nhận tái lập mạng có hướng. Không đưa graph encoding vào ZDT vì sẽ đổi bài toán.

## Kết quả và lần chạy mới

Không sửa hay ghép dữ liệu lịch sử vào kết quả sau sửa. Manifest kiểm tra hash mã nguồn/cấu hình, do đó không resume một lần chạy từ trước sửa bằng mã hiện tại. Bộ ZDT7 sau sửa mặc định ghi vào thư mục v2 riêng. Một bảng có đủ bảy tên không đồng nghĩa có bảy thuật toán được tái lập trọn vẹn: cần giữ nhãn CE adaptation và giới hạn SDR/CGDE nêu trên khi viết kết luận.

Kiểm thử công thức, kế thừa F qua chọn lọc, lưu đúng thế hệ trước, lân cận đủ biến/cá thể, mutation hai nhánh, SBX hai phía và ngân sách nằm trong `tests/unit/test_baseline_paper_operators.py`. Kiểm thử không chứng minh lặp lại kết quả số trong bài báo.

Đã chạy: 105 kiểm thử, 103 đạt, 2 bỏ qua do môi trường không tạo được junction; trong đó có pipeline smoke 28 run cho đủ 7 solver, kiểm tra checkpoint/resume và phát hiện sửa artifact. Kiểm tra cấu trúc/đường dẫn tài liệu và `git diff --check` đạt. Chưa chạy lại 1.050 run nghiên cứu; chưa xác nhận kết quả số từ mã tác giả.
