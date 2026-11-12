# Phân tích độ nhạy tham số

## Phạm vi và phiên bản cấu hình

Nghiên cứu này đánh giá riêng OADE-NSGA-II trên năm bài toán ZDT, với 30 run cho mỗi cấu hình, seed `42–71` và mức trần 20.000 lần đánh giá hàm mục tiêu. Các sweep thay đổi `pop_size`, `stagnation_patience` và giá trị khởi tạo F/CR. Đây là mức trần: số đánh giá thực tế có thể thấp hơn khi một thế hệ vượt ngân sách.

> Các sweep được tạo trước khi mặc định trong mã nguồn đổi sang adaptive; baseline dùng restart cổ điển với `restart_elite_ratio: 0.30`, `stagnation_patience: 20` và F/CR khởi tạo cố định. `config/studies/sensitivity.yaml` hiện đặt `restart_mode: classic` tường minh để lần chạy mới giữ cùng giao thức. Đây không phải phép thử trực tiếp cho OADE-NSGA-II v2 với adaptive restart.

Các mức tham số được kiểm tra:

| Study | Baseline | Mức so sánh |
|---|---|---|
| `pop_size` | 100 | 50, 200 |
| `stagnation_patience` | 20 | 5, 10, 15, 25, 30, 40 |
| `f_cr_init` | `fixed_baseline` (`mean_F=0.65`, `mean_CR=0.5`) | `low_init`, `high_init`, `random_uniform` |

## Kết quả chính

Các con số dưới đây được đọc từ `results/sensitivity/sensitivity_summary.csv` và `sensitivity_statistics.csv`; không tái chạy thuật toán.

### Kích thước quần thể

- Kiểm định Friedman phát hiện khác biệt giữa các mức `pop_size` ở cả 10 tổ hợp bài toán–metric (5 bài toán × IGD/HV).
- So với baseline 100, `pop_size=50` kém hơn ở cả 10 so sánh hậu nghiệm; `pop_size=200` tốt hơn ở cả 10. Các p-value hậu nghiệm đã được Holm hiệu chỉnh trong từng tổ hợp bài toán–metric.
- Mean IGD thấp nhất và mean HV cao nhất trong từng bài toán đều thuộc mức 200. Đây là kết quả của sweep theo ngân sách đánh giá bằng nhau; số thế hệ thay đổi theo kích thước quần thể.

### Ngưỡng trì trệ

- Friedman phát hiện khác biệt giữa các mức `stagnation_patience` ở cả 10 tổ hợp bài toán–metric.
- Trong 60 so sánh hậu nghiệm với baseline 20, có 14 kết quả nghiêng về baseline, 1 kết quả nghiêng về một mức khác, và 45 kết quả không phát hiện khác biệt sau hiệu chỉnh Holm trong từng tổ hợp bài toán–metric.
- Không có một mức patience thay thế nào thắng nhất quán trên toàn bộ năm bài toán và hai metric.

### Giá trị khởi tạo F/CR

- Friedman phát hiện khác biệt ở 2/10 tổ hợp bài toán–metric.
- Trong 30 so sánh hậu nghiệm với baseline, 2 kết quả nghiêng về baseline và 28 không phát hiện khác biệt sau hiệu chỉnh Holm trong từng tổ hợp bài toán–metric. Không có mức thay thế nào được xác nhận tốt hơn baseline trong các so sánh hậu nghiệm đã lưu.

## Cách kiểm định và giới hạn diễn giải

- Một run theo seed là đơn vị phân tích; các mức tham số được ghép theo `run_idx`.
- Friedman là kiểm định omnibus trên các mức tham số. P-value Friedman trong CSV **chưa được hiệu chỉnh giữa các tổ hợp study–problem–metric**; do đó các tỷ lệ 10/10 và 2/10 ở trên là kết quả thăm dò trên nhiều kiểm định.
- Wilcoxon signed-rank hậu nghiệm so sánh từng mức với baseline. Holm được áp dụng riêng cho các mức thay thế trong từng study–problem–metric, không phải cho toàn bộ nghiên cứu sensitivity.
- Tệp kết quả không có khoảng tin cậy cho paired effect hoặc mức cải thiện. Chưa nên dùng các kết quả này để khẳng định một cấu hình tối ưu chung.
- Nghiên cứu chỉ gồm năm bài toán ZDT và cấu hình restart cổ điển. Cần đánh giá lại cấu hình được chọn trên seed mới, các suite DTLZ/WFG và adaptive restart trước khi áp dụng cho OADE v2.

## Tái lập và đầu ra

Chạy sensitivity study:

```powershell
.\.venv\Scripts\python.exe main.py sensitivity
```

Tạo biểu đồ:

```powershell
.\.venv\Scripts\python.exe main.py plot-sensitivity
```

Các đầu ra nằm trong `results/sensitivity/`:

- `sensitivity_raw_runs.csv`: dữ liệu từng run, gồm IGD, HV, runtime, số lần restart, mức sử dụng ngân sách và F/CR.
- `sensitivity_summary.csv`: mean, độ lệch chuẩn và giá trị tốt nhất theo cấu hình.
- `sensitivity_statistics.csv`: Friedman và Wilcoxon signed-rank hậu nghiệm cùng p-value đã hiệu chỉnh Holm.
- `sensitivity_fcr_trace.csv`: diễn tiến mean F, mean CR và xác suất chọn DE.
- `plots/`: biểu đồ sensitivity và trace thích nghi.
