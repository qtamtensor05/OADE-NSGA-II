# Ablation xác suất DE theo thành công

Mặc định `probability_update_mode: success_rate`; `fixed` giữ xác suất ban đầu. Chỉ hỗ trợ hai mode này; các phương án đối chứng cũ được mô tả trong [báo cáo kết quả lịch sử](../reports/probability_generated_vs_success_zdt_report.md). `enable_probability_adaptation: false` tắt mọi cập nhật xác suất, ưu tiên hơn mode.

Thành công là không bị trội trong pool cha–con đã đánh giá trước loại trùng, không phải sống sót sau crowding hay cải thiện so với cha. Từng trial DE/SBX được đếm một lần, kể cả trùng; các cá thể OBL không nằm trong mẫu số toán tử nhưng vẫn có thể trội trial. Đây là một định nghĩa thiết kế cần kiểm chứng thực nghiệm, chưa bảo đảm cải thiện.

Với s là số thành công, n là số trial từng toán tử:

$$
r_{\mathrm{DE},t}=\frac{s_{\mathrm{DE},t}}{n_{\mathrm{DE},t}},
\qquad
r_{\mathrm{SBX},t}=\frac{s_{\mathrm{SBX},t}}{n_{\mathrm{SBX},t}}.
$$

$$
q_t=\frac{r_{\mathrm{DE},t}}{r_{\mathrm{DE},t}+r_{\mathrm{SBX},t}},
\qquad
p_{t+1}=\min\!\left\{0.8,\max\!\left\{0.2,0.9p_t+0.1q_t\right\}\right\}.
$$

Trong đó $p_t$ là xác suất chọn DE; $n$ là số trial và $s$ là số trial thành công của mỗi toán tử trong thế hệ $t$.

Giữ pDE nếu một toán tử chưa được dùng hoặc cả hai rate bằng 0. Chuẩn hóa theo n tránh ưu tiên toán tử chỉ vì được chọn nhiều. F/CR không đổi công thức; success-rate vẫn hoạt động khi tắt adaptation F/CR.

```powershell
# Xem thiết kế, không chạy solver
.\.venv\Scripts\python.exe -m research ablation-probability --stage plan
# Chạy 300 run: 2 mode x 5 ZDT x 30 seed, cap 20.000/run
.\.venv\Scripts\python.exe -m research ablation-probability --stage run
# Tiếp tục, cùng source/config/environment
.\.venv\Scripts\python.exe -m research ablation-probability --stage run --resume
# Chỉ tạo lại báo cáo
.\.venv\Scripts\python.exe -m research ablation-probability --stage report --resume
# Smoke nhỏ: kiểm tra kỹ thuật, không phải bằng chứng cải thiện
.\.venv\Scripts\python.exe -m research ablation-probability --config config/smoke/smoke_probability_ablation.yaml --stage run
```

Output `results/experiments/probability_fixed_vs_success_zdt_v1/`: primary JSON, manifest/reference snapshot, `derived/report.md`, `raw_runs.csv`, `comparisons.csv`, `probability_trace.csv`, `convergence.csv`, `restart_events.csv`. Trace từng thế hệ có nDE/nSBX, sDE/sSBX, target và p trước/sau; fixed để trống success counts. Các phương án dùng cùng cấu hình adaptive restart, cùng quần thể uniform ban đầu và seed; chỉ mode khác nhau. Đây là ablation kiểm soát từ uniform chung, không đánh giá lợi ích Sobol–OBL khởi tạo hay toàn bộ OADE native. Không tự thay giao thức khởi tạo trong thí nghiệm này.

Chất lượng: IGD giảm/HV tăng tốt. Một cặp fixed–success_rate trên mỗi bài và metric, Wilcoxon ghép seed hai phía, zero_method=wilcox, xấp xỉ chuẩn; toàn delta zero đặt p=1. Holm theo cặp/bài/metric; chỉ một cặp nên p Holm bằng p thô, alpha=0,05. Báo median delta từng cặp và số cặp hợp lệ/bị loại; không phát hiện khác biệt không đồng nghĩa tương đương. Đọc cặp success_rate–fixed; không kết luận cải thiện từ pDE thay đổi hoặc smoke. Tất cả objective calls tính vào cap; batch nguyên tử có thể để dư, xem n_eval.

Mã nguồn/môi trường/tham số được hash; checkpoint không tương thích bị từ chối. Dùng thư mục mới khi đổi source. Kết quả lịch sử không được gán lại nhãn success-rate.

Việc chọn mặc định success-rate theo định hướng thiết kế của tác giả không đồng nghĩa đã chứng minh cải thiện: thí nghiệm đối chứng lịch sử trước đây chưa phát hiện khác biệt chất lượng. Không resume các run cũ sau thay đổi này.
