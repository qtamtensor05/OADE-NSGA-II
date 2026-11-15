# Pipeline so sánh restart có telemetry

**Triển khai nghiên cứu:** pipeline này dùng `research.oade_nsga2` và runner `local_oade_research`; bản chính `oade_nsga2` chỉ có một cấu hình. Xem [phân tách hai bản](oade_implementations.md). Dữ liệu và báo cáo cũ đã được xóa khi đặt lại mốc nghiên cứu; cần chạy mới, không dùng resume từ bộ cũ.

Pipeline mới chạy ba cấu hình độc lập trên chung lõi OADE: `classic`, `adaptive`, `no_restart`. Mặc định: ZDT1/2/3/4/6, 30 seed ghép cặp 1000–1029, population 100, cap 20.000 objective evaluations/run, tổng 450 run. Cùng khởi tạo uniform, bật OBL định kỳ, adaptation F/CR và neighborhood; cập nhật xác suất DE bằng **success-rate** ở cả ba nhánh. Không nhập lại số liệu lịch sử thiếu telemetry hoặc dùng công thức xác suất cũ.

Lõi hiện tại xác định DE offspring thành công bằng quan hệ Pareto trên pool cha–con đã đánh giá **trước loại trùng**, không dựa vào `rank` còn thiếu trên offspring bị loại. Mỗi DE trial không bị trội đóng góp F/CR một lần, kể cả khi trùng mục tiêu; trial gần trùng nhưng bị trội không đóng góp. Chọn lọc quần thể vẫn loại trùng như trước. Bản sửa này có thể thay đổi kết quả so với mã cũ; kết quả cũ không được tự coi là đã sửa. Nếu đã có run trước thay đổi mã, dùng thư mục output mới; kiểm tra provenance sẽ từ chối resume khác source hash.

Từ thư mục repository, PowerShell:

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"

# Chỉ xem thiết kế, không chạy thuật toán (đây cũng là stage mặc định)
.\.venv\Scripts\python.exe -m research restart-comparison --stage plan

# Benchmark chính thức, bạn chủ động chạy
.\.venv\Scripts\python.exe -m research restart-comparison --stage run --jobs 4

# Tiếp tục checkpoint còn thiếu, yêu cầu mã/cấu hình/môi trường không đổi
.\.venv\Scripts\python.exe -m research restart-comparison --stage run --jobs 4 --resume

# Tạo lại bảng/báo cáo từ primary đã hoàn tất
.\.venv\Scripts\python.exe -m research restart-comparison --stage report --resume

# Smoke ép trigger để kiểm tra pipeline; KHÔNG dùng làm kết quả nghiên cứu
.\.venv\Scripts\python.exe -m research restart-comparison --config config/smoke/smoke_restart_comparison.yaml --stage run --jobs 4
```

Có thể dùng `--jobs 1` hoặc `--out-dir <thư mục mới>`. Output chính ở `results/experiments/restart_success_rate_zdt_v1/`. Mỗi run lưu JSON riêng, manifest lưu hash mã nguồn, môi trường, cấu hình, reference fronts và checkpoint. Resume từ chối thay đổi hoặc hỏng dữ liệu. Nếu bị ngắt giữa lúc ghi JSON và manifest, giữ thư mục để kiểm tra; không xóa primary để ép resume.

## Đọc dữ liệu

- `derived/raw_runs.csv`: IGD/HV cuối, validity, runtime, n_eval thực dùng; số lần kiểm tra stagnation, số lần đủ patience (`stagnation_eligible`, kể cả no-restart), số lần xét collapse/dương tính, restart attempts/completed/budget_blocked và evaluation dành cho restart. Tần suất `restart_per_100_checks` và tỷ lệ ngân sách `restart_evaluation_fraction`.
- `derived/restart_events.csv`: từng attempt, generation (bắt đầu từ 1), evaluations trước/sau, trạng thái, IGD/HV trước/sau thay quần thể. Budget-blocked không tính hoàn tất. `no_op` là hàm trả về nhưng không sinh evaluation.
- `derived/comparisons.csv`: classic–adaptive, classic–no_restart, adaptive–no_restart; ghép seed hợp lệ; median của delta từng cặp (a−b), số cặp bị loại, p thô và Holm. IGD giảm tốt, HV tăng tốt. Wilcoxon hai phía, bỏ zero, xấp xỉ chuẩn; tất cả delta bằng 0 đặt p=1. Cột `p_holm` giữ họ 3 cặp/bài/metric để truy vết; **`p_holm_all_endpoints` hiệu chỉnh đồng thời 30 endpoint** (5 bài × 2 chỉ số × 3 cặp), alpha=0,05, dùng cho kết luận chung. Không phát hiện khác biệt không chứng minh tương đương.
- `derived/convergence.csv`: chất lượng tại mốc ngân sách, kèm n_eval quan sát thực. Không nội suy hoặc coi những mốc vượt target là cùng thời điểm chính xác.
- `derived/summary.csv`: mean, SD, median, Q25/Q75; số run có restart, số đủ stagnation, số xét collapse/dương tính và từ chối do diversity khỏe; tần suất, chi phí, chất lượng và runtime.
- `derived/probability_trace.csv` và `derived/diversity_events.csv`: kiểm tra success-rate và OBL định kỳ cùng được bật trong ba nhánh; số lần bơm thực tế có thể khác vì chi phí restart làm số thế hệ thay đổi.
- `derived/report.md`: tổng quan median chất lượng và số restart; giữ invalid trong thống kê run và loại riêng khỏi cặp chất lượng.
- `primary/*.json`: toàn bộ telemetry, event, convergence, hash quần thể đầu và X/F cuối để tính lại indicator với reference snapshot.

## Giới hạn suy luận

Khởi tạo uniform giống nhau theo seed; RNG được reset cùng seed cho từng cấu hình. Telemetry không lấy số ngẫu nhiên và không đổi quyết định tìm kiếm. Sau khi restart xảy ra, chuỗi RNG có thể phân kỳ. Objective calls cho restart cũng nằm trong cap; batch nguyên tử có thể để dư ngân sách, phải xem `n_eval`, không giả định mọi run dùng đúng 20.000.

Classic giữ 30% elite, thay bằng mẫu uniform và reset F/CR; adaptive giữ tối thiểu 80%, dùng OBL/Gauss và kéo F/CR về 0,5. Đây là so sánh **toàn bộ chính sách restart**, chưa tách riêng tác động của diversity gate, tỷ lệ elite, kernel và reset F/CR. No-restart dùng các tham số chung giống hai nhánh kia và chỉ tắt restart.

Nếu adaptive không trigger và trùng no-restart, không có bằng chứng rằng restart adaptive mang lại lợi ích trong các run đó. Nếu classic kém no-restart, diễn giải là chính sách classic gây giảm chất lượng trong thiết kế này; không tự suy ra adaptive đã cải thiện nhờ kích hoạt restart. Cần đọc đủ ba cặp.

IGD/HV trước–sau event mô tả hiệu ứng tức thời; chất lượng cuối ghép seed với no-restart mới đánh giá lợi ích ròng trong cap chung. Trigger nhiều có thể vì bài khó hoặc stagnation nhiều; tương quan trigger–chất lượng không chứng minh nguyên nhân. Smoke cố tình ép stagnation/collapse, không đại diện cho tần suất thực của cấu hình nghiên cứu.

## Điều kiện trigger được giữ nguyên

Trong mã hiện tại, counter stagnation tăng khi chuẩn Euclid của **thay đổi ideal point giữa hai thế hệ** nhỏ hơn tolerance; đây không phải kiểm tra cải thiện đơn điệu từng mục tiêu. Đủ patience=20 mới xét restart. Adaptive yêu cầu thêm một trong hai dấu hiệu:

- Objective range lớn nhất nhỏ hơn 0,001.
- Độ lệch chuẩn lớn nhất của biến quyết định sau chuẩn hóa bounds nhỏ hơn diversity_threshold=0,02.

Nếu diversity khỏe, adaptive đưa counter về patience//2. No-restart vẫn theo dõi counter nhưng không xét collapse hoặc sinh cá thể restart. Không ép trigger trong benchmark chính thức; nếu không kích hoạt phải báo đúng là không có bằng chứng lợi ích từ restart đã xảy ra. Smoke dùng tolerance/threshold rất lớn chỉ để xác minh đường đi và không được diễn giải như kết quả nghiên cứu.

Writer đã có retry hữu hạn khi Windows tạm chặn thay file manifest; nếu lỗi kéo dài giữ nguyên cả primary và file tạm để phục hồi, không xóa dữ liệu.

## Trạng thái kết quả

Bộ kết quả và báo cáo trước đây đã được xóa. Đây là giao thức có thể chạy lại, chưa có kết quả nghiên cứu thành phần được giữ tại mốc mới.
