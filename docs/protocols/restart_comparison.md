# Pipeline so sánh restart có telemetry

Pipeline mới chạy ba cấu hình độc lập trên chung lõi OADE: `classic`, `adaptive`, `no_restart`. Mặc định: ZDT1/2/3/4/6, 30 seed ghép cặp 1000–1029, population 100, cap 20.000 objective evaluations/run, tổng 450 run. Không nhập lại số liệu lịch sử thiếu telemetry.

Lõi hiện tại xác định DE offspring thành công bằng quan hệ Pareto trên pool cha–con đã đánh giá **trước loại trùng**, không dựa vào `rank` còn thiếu trên offspring bị loại. Mỗi DE trial không bị trội đóng góp F/CR một lần, kể cả khi trùng mục tiêu; trial gần trùng nhưng bị trội không đóng góp. Chọn lọc quần thể vẫn loại trùng như trước. Bản sửa này có thể thay đổi kết quả so với mã cũ; kết quả cũ không được tự coi là đã sửa. Nếu đã có run trước thay đổi mã, dùng thư mục output mới; kiểm tra provenance sẽ từ chối resume khác source hash.

Từ thư mục repository, PowerShell:

```powershell
# Chỉ xem thiết kế, không chạy thuật toán (đây cũng là stage mặc định)
.\.venv\Scripts\python.exe -m research restart-comparison --stage plan

# Benchmark chính thức, bạn chủ động chạy
.\.venv\Scripts\python.exe -m research restart-comparison --stage run

# Tiếp tục checkpoint còn thiếu, yêu cầu mã/cấu hình/môi trường không đổi
.\.venv\Scripts\python.exe -m research restart-comparison --stage run --resume

# Tạo lại bảng/báo cáo từ primary đã hoàn tất
.\.venv\Scripts\python.exe -m research restart-comparison --stage report --resume

# Smoke ép trigger để kiểm tra pipeline; KHÔNG dùng làm kết quả nghiên cứu
.\.venv\Scripts\python.exe -m research restart-comparison --config config/smoke/smoke_restart_comparison.yaml --stage run
```

Có thể dùng `--jobs 1` hoặc `--out-dir <thư mục mới>`. Output chính ở `results/experiments/restart_comparison_v1/`. Mỗi run lưu JSON riêng, manifest lưu hash mã nguồn, môi trường, cấu hình, reference fronts và checkpoint. Resume từ chối thay đổi hoặc hỏng dữ liệu. Nếu bị ngắt giữa lúc ghi JSON và manifest, giữ thư mục để kiểm tra; không xóa primary để ép resume.

## Đọc dữ liệu

- `derived/raw_runs.csv`: IGD/HV cuối, validity, runtime, n_eval thực dùng; số lần kiểm tra stagnation, số lần đủ patience (`stagnation_eligible`, kể cả no-restart), số lần xét collapse/dương tính, restart attempts/completed/budget_blocked và evaluation dành cho restart. Tần suất `restart_per_100_checks` và tỷ lệ ngân sách `restart_evaluation_fraction`.
- `derived/restart_events.csv`: từng attempt, generation (bắt đầu từ 1), evaluations trước/sau, trạng thái, IGD/HV trước/sau thay quần thể. Budget-blocked không tính hoàn tất. `no_op` là hàm trả về nhưng không sinh evaluation.
- `derived/comparisons.csv`: classic–adaptive, classic–no_restart, adaptive–no_restart; ghép seed hợp lệ; median của delta từng cặp (a−b), số cặp bị loại, p thô và Holm. IGD giảm tốt, HV tăng tốt. Wilcoxon hai phía, bỏ zero, xấp xỉ chuẩn; tất cả delta bằng 0 đặt p=1. Holm riêng cho 3 cặp/bài/metric, alpha=0,05. Không gộp thành kết luận toàn bộ ZDT.
- `derived/convergence.csv`: chất lượng tại mốc ngân sách, kèm n_eval quan sát thực. Không nội suy hoặc coi những mốc vượt target là cùng thời điểm chính xác.
- `derived/report.md`: tổng quan median chất lượng và số restart; giữ invalid trong thống kê run và loại riêng khỏi cặp chất lượng.
- `primary/*.json`: toàn bộ telemetry, event, convergence, hash quần thể đầu và X/F cuối để tính lại indicator với reference snapshot.

## Giới hạn suy luận

Khởi tạo uniform giống nhau theo seed; RNG được reset cùng seed cho từng cấu hình. Telemetry không lấy số ngẫu nhiên và không đổi quyết định tìm kiếm. Sau khi restart xảy ra, chuỗi RNG có thể phân kỳ. Objective calls cho restart cũng nằm trong cap; batch nguyên tử có thể để dư ngân sách, phải xem `n_eval`, không giả định mọi run dùng đúng 20.000.

Classic giữ 30% elite, thay bằng mẫu uniform và reset F/CR; adaptive giữ tối thiểu 80%, dùng OBL/Gauss và kéo F/CR về 0,5. Đây là so sánh **toàn bộ chính sách restart**, chưa tách riêng tác động của diversity gate, tỷ lệ elite, kernel và reset F/CR. No-restart dùng các tham số chung giống hai nhánh kia và chỉ tắt restart.

Nếu adaptive không trigger và trùng no-restart, không có bằng chứng rằng restart adaptive mang lại lợi ích trong các run đó. Nếu classic kém no-restart, diễn giải là chính sách classic gây giảm chất lượng trong thiết kế này; không tự suy ra adaptive đã cải thiện nhờ kích hoạt restart. Cần đọc đủ ba cặp.

IGD/HV trước–sau event mô tả hiệu ứng tức thời; chất lượng cuối ghép seed với no-restart mới đánh giá lợi ích ròng trong cap chung. Trigger nhiều có thể vì bài khó hoặc stagnation nhiều; tương quan trigger–chất lượng không chứng minh nguyên nhân. Smoke cố tình ép stagnation/collapse, không đại diện cho tần suất thực của cấu hình nghiên cứu.
