# Đối chứng bật/tắt OBL bơm đa dạng định kỳ

**Chỉ thay một công tắc:** OBL bổ sung định kỳ trong tiến hóa. Cả hai nhánh giữ cùng quần thể uniform và seed, adaptive restart, success-rate, adaptation F/CR và neighborhood. Không sử dụng Sobol–OBL khởi tạo trong đối chứng này.

| Thành phần | Bật | Tắt |
|:---|:---|:---|
| OBL định kỳ | Chỉ số thế hệ 0, 10, 20, … | Không gọi |
| Khởi tạo | Uniform, 100 evaluation | Cùng uniform và seed |
| Adaptive restart | Bật | Bật |
| Cập nhật xác suất DE | Success-rate | Success-rate |
| Cap tổng | 20.000 evaluation | 20.000 evaluation |

**Tắt OBL định kỳ không có nghĩa tắt mọi cơ chế làm mới đa dạng.** Adaptive restart vẫn có phần OBL/Gauss riêng. Phải giữ nguyên cơ chế đó để tách riêng hiệu quả của bơm định kỳ.

## Kernel đang đo

Mỗi lần gọi, từng cá thể được chọn với xác suất $p_{\mathrm{jump}}=0.2$. Với cá thể được chọn, kernel chọn ngẫu nhiên một trong hai cách phản chiếu với xác suất bằng nhau:

$$
\mathbf{x}'=
\begin{cases}
\mathbf{x}_{\min}^{\mathrm{pop}}+\mathbf{x}_{\max}^{\mathrm{pop}}-\mathbf{x}, & \text{dynamic OBL},\\
\mathbf{x}_{\min}+\mathbf{x}_{\max}-\mathbf{x}, & \text{static OBL}.
\end{cases}
$$

Điểm mới được clip vào bounds, đánh giá objective rồi đưa vào pool cha–con. Số ứng viên thực tế là ngẫu nhiên; không mặc định mỗi lần bơm sinh cả quần thể. Nhánh tắt không gọi kernel và không tiêu thụ RNG/evaluation của kernel; các quỹ đạo về sau có thể phân kỳ.

## Cách chạy

5 bài ZDT1/2/3/4/6 × 30 seed 1000–1029 × 2 nhánh = **300 run**. Population 100; mọi evaluation khởi tạo, OBL và restart đều tính vào cap. Nhánh bật không được bù ngân sách hoặc ép cùng số thế hệ.

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"

# Xem kế hoạch, không chạy optimizer
.\.venv\Scripts\python.exe -m research ablation-diversity --stage plan

# Benchmark chính thức: bạn chủ động chạy
.\.venv\Scripts\python.exe -m research ablation-diversity --stage run --jobs 4

# Tiếp tục checkpoint còn thiếu
.\.venv\Scripts\python.exe -m research ablation-diversity --stage run --jobs 4 --resume

# Tạo lại báo cáo từ dữ liệu đã hoàn tất
.\.venv\Scripts\python.exe -m research ablation-diversity --stage report --resume
```

Cấu hình: `config/studies/diversity_injection.yaml`. Output: `results/experiments/diversity_injection_zdt_v1/`. Có thể dùng `--out-dir <thư mục mới>`. Giữ nguyên source/config/environment trong lúc chạy; không resume checkpoint cũ sau sửa mã.

## Dữ liệu và cách kết luận

- `primary/*.json`: X/F đầu và cuối, n_eval thực, trace xác suất, convergence, restart events và diversity events; manifest lưu source/environment/reference hashes và checkpoint.
- `derived/raw_runs.csv`: chỉ số từng run và chi phí OBL trên tổng ngân sách.
- `derived/summary.csv`: mean/SD/median/Q25/Q75 của IGD/HV, runtime, n_eval; tổng lần gọi, số ứng viên/evaluation OBL và số giữ lại.
- `derived/diversity_events.csv`: từng lần gọi, trạng thái completed/empty/budget_blocked, chi phí, số ứng viên, thế hệ có hoàn tất và số ứng viên còn lại sau chọn lọc. Nếu OBL đã đánh giá nhưng bước DE tiếp theo hết ngân sách, chi phí vẫn tính và `generation_completed=false`; `retained` để trống.
- `derived/comparisons.csv`: delta bật − tắt, IGD âm hoặc HV dương ủng hộ bật; số cặp hợp lệ, p thô và p hiệu chỉnh.
- `derived/report.md`, `convergence.csv`, `probability_trace.csv`, `restart_events.csv`: báo cáo và dấu vết chi tiết.

Đơn vị phân tích: cặp run cùng seed/bài, $n=30$. Wilcoxon signed-rank hai phía, bỏ zero, xấp xỉ chuẩn; toàn delta zero đặt $p=1$. Định trước **Holm trên cả 10 endpoint** (5 bài × IGD/HV), $\alpha=0.05$, cột `p_holm_all_endpoints`. Cột `p_holm` giữ phép hiệu chỉnh riêng từng bài/metric để truy vết, không thay kết luận chung. Invalid được giữ và đếm, loại riêng khỏi cặp chất lượng. Không phát hiện khác biệt không chứng minh tương đương.

Số ứng viên được giữ lại chỉ là bằng chứng cơ chế đã tham gia chọn lọc, chưa chứng minh cải thiện lâu dài. Lợi ích ròng phải đọc IGD/HV cuối tại cùng cap và độ dao động. Số restart có thể khác nhau như hệ quả của thay đổi quỹ đạo; thiết kế này đo hiệu ứng tổng của OBL định kỳ, chưa tách riêng vai trò trung gian của restart. Runtime mô tả máy/worker đang dùng; không suy ra độ phức tạp từ thời gian.
