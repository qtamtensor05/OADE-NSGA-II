# Xử lý sau rà soát — 12/11/2026

## Kết quả theo thứ tự ưu tiên

1. **Định danh và mô tả phương pháp:** sửa tên baseline trong README/báo cáo, thêm bảng nguồn–implementation–adaptation và BibTeX; chốt claim hiện tại ở mức thực nghiệm của cấu hình đã triển khai. Mô tả rõ uniform warm start, periodic OBL, F dùng Lehmer mean, CR dùng arithmetic mean và pDE theo generated share. Không sửa công thức tìm kiếm hoặc gán kết quả cũ cho một rule adaptation mới.
2. **Tái lập và bảo vệ kết quả:** bỏ ignore cho test, smoke YAML, mã figure, R bootstrap/lockfile và JSON QA; thêm snapshot môi trường audit, inventory checksum dữ liệu lịch sử và manifest thực thi cho run mới. Resume/reuse kiểm tra protocol, source, environment, checksum, tập khóa, seed, dimension, budget, validation và trajectory trước khi tiếp tục. Fresh run từ chối ghi đè evidence. V2 reuse tính số invalid thực tế thay vì in cố định 0.
3. **Báo cáo và hình:** thêm index và manuscript tổng hợp, registry thí nghiệm, hướng dẫn tái lập/thống kê; phân biệt scheduled n=30 với 26–30 valid pairs trong DTLZ, structural invalid với quality corner-collapse. Đổi chú thích hình không đủ căn cứ sang median/quality được quan sát; ghi rõ DTLZ4 runtime proxy. Giữ báo cáo audit ban đầu như bản ghi lịch sử.
4. **Quyết định thí nghiệm bổ sung:** ghi kế hoạch ưu tiên trong followup_experiments.md. Các sửa văn bản và provenance không cần rerun toàn bộ benchmark. Published-baseline claim cần xác minh implementation; adaptive-restart claim cần telemetry + No Restart trên thiết kế mới; CI và failure-aware sensitivity là phân tích mới cần phương pháp định trước.

## Phát hiện thêm khi triển khai

RNSGA2 aspiration-point setup từng gọi objective trên problem chưa bọc và nằm ngoài timer. Đã chuyển setup qua BudgetedProblem và tính vào runtime cho run mới. Đây là **budget-accounting v2**, có thể làm thay đổi kết quả RNSGA2 mới do ít budget còn lại cho search. Toàn bộ CSV lịch sử được giữ nguyên; tài liệu công khai rằng recorded search counter cũ bỏ sót một lần đánh giá population-sized setup. Không dùng manifest mới để chứng nhận ngược dữ liệu cũ.

README từng hiển thị MIT badge trong khi không có LICENSE. Đã bỏ badge, chưa tự chọn giấy phép cho tác giả hoặc baseline.

## Kiểm chứng

- Unit test: 21/21 qua, gồm kiểm tra actual objective-call count của RNSGA2, drift cấu hình/source/environment, duplicate/missing/wrong-seed records, integrity mismatch và bảo vệ ghi đè.
- Benchmark nhỏ: một ZDT1, 2 seeds, population 20, cap 500, đủ 7 thuật toán; 14/14 record, 0 invalid. Đây là smoke kiểm tra pipeline, không phải kết quả nghiên cứu bổ sung.
- Resume bộ smoke hoàn chỉnh: preflight qua, bỏ qua problem đã đủ record, không chạy lại thuật toán.
- V2 reuse: preflight chấp nhận 12 comparator record đã có manifest; chạy 2 OADE run và ghép thành 14 record, 0 invalid.
- Negative checks: từ chối baseline lịch sử thiếu execution manifest, từ chối fresh overwrite và từ chối resume khi seed thay đổi.
- Bốn bundle hình DTLZ/WFG được render lại, alignment và text-floor qua; final collision JSON và QA record đi kèm. Không mở rộng PASS này thành chứng nhận chuẩn nộp bài.
- Không thay đổi raw-run CSV lịch sử hoặc kiểm định đã lưu. Các nguồn dữ liệu figure vẫn xuất từ các quan sát lịch sử.

## Các giới hạn vẫn còn

Chưa xác nhận tính mới từ tổng quan tài liệu đầy đủ; chưa có citation bài gốc khớp local CGDE; CE là adaptation; chưa kiểm chứng baseline theo từng phương trình; không khôi phục được package/source versions lịch sử. Chưa có CI cho paired effects, phân tích failure-aware hoặc telemetry của run cũ. Rule corner-collapse lịch sử chưa đầy đủ. Giấy phép phát hành và tạp chí đích chưa được tác giả xác định.

Các điểm trên đã được giới hạn trong claim và kế hoạch, không được đánh dấu là đã giải quyết bằng cách chỉ đổi tên hoặc chạy unit test. Chưa commit/push thay đổi.
