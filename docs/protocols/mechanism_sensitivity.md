# Pipeline đo ảnh hưởng của nhiều mức tham số cơ chế

Ngày triển khai: 19/11/2026. Pipeline nghiên cứu riêng bám solver production `oade_nsga2`, có telemetry như bộ mechanism-impact. Không thay cấu hình production, không tái dùng kết quả 480 lượt cũ, không tự chọn cấu hình tốt nhất. Phạm vi hiện tại: ZDT4/ZDT6, D=10, M=2.

**Trạng thái 19/11/2026:** đã hoàn tất 2.100 lượt, tất cả hợp lệ; có [báo cáo kết luận và kiểm chứng độc lập](../reports/mechanism_sensitivity_report.md). Phần dưới mô tả giao thức thực thi. Không chạy ghi đè bộ đã hoàn tất; dùng `--out-dir` mới cho lần lặp độc lập.

## Câu hỏi và thiết kế

Mỗi lần thay đúng một tham số sang một mức trong danh sách (OFAT), giữ các thành phần còn lại như production. Dùng cùng seed/quần thể uniform và cùng cap FE cho các cấu hình. Kiểm tra hash quần thể ban đầu trong từng block bài/seed; không coi các đường tìm kiếm sau đó là dùng cùng chuỗi random draws. Đo IGD/HV cuối lượt, số FE thực, runtime, các trạng thái F/CR/pDE qua thế hệ, số trial/retained DE/SBX/OBL, sự kiện OBL/restart và chi phí FE.

Hai chế độ cho tham số thích nghi:

- `initial`: gán mức lúc khởi tạo rồi để thuật toán thích nghi; mốc so sánh là `full` production. Đây là độ nhạy với giá trị khởi đầu, không phải mức được giữ suốt lượt.
- `held`: giữ riêng tham số đang xét ở mức đã gán, kể cả sau cập nhật thích nghi và restart; các tham số khác vẫn thích nghi. Mốc so sánh là cùng chế độ held tại giá trị production. Ví dụ F=0,4 held so với F=0,65 held, CR/pDE vẫn thích nghi. Không trộn ảnh hưởng giá trị với việc bật/tắt thích nghi. `held` chỉ áp dụng cho `mean_F`, `mean_CR`, `prob_de`.

`mean_F`/`mean_CR` là trung bình phân phối lấy mẫu DE, không phải F/CR của mọi offspring đều bằng số đó. “Mốc” trong pipeline này là mức tham số giữa các lượt chạy, không phải lịch đổi tham số theo thời gian trong một lượt.

## Các mức mặc định

[Cấu hình chính](../../config/studies/mechanism_sensitivity.yaml) là nguồn thực thi; sửa trước khi chạy.

| Tham số | Các mức | Mốc production | Chế độ |
|---|---|---:|---|
| `obl_interval` | 5, 10, 20, 40 thế hệ | 10 | initial |
| `obl_jump_rate` | 0,05; 0,1; 0,2; 0,4 | 0,2 | initial |
| `stagnation_patience` | 5, 10, 20, 40 | 20 | initial |
| `stagnation_tolerance` | 10⁻⁵, 10⁻⁴, 10⁻³ | 10⁻⁴ | initial |
| `diversity_threshold` | 0,01; 0,02; 0,05; 0,1 | 0,02 | initial |
| `restart_elite_ratio` | 0,8; 0,9; 0,95 | 0,8 | initial |
| `n_neighbors` | 3, 5, 10, 20 | 5 | initial |
| `mean_F` | 0,4; 0,5; 0,65; 0,8; 0,9 | 0,65 | held |
| `mean_CR` | 0,1; 0,3; 0,5; 0,7; 0,9 | 0,5 | held |
| `prob_de` | 0,2; 0,35; 0,5; 0,65; 0,8 | 0,5 | held |

Tham số tĩnh không tự thích nghi; `initial` ở đó vẫn có hiệu lực suốt lượt. OBL dùng chỉ số thế hệ từ 0 như production: interval=10 có lịch gen=0,10,20,..., tức nhãn telemetry 1,11,21,... . Jump rate là xác suất theo cá thể, không đảm bảo đúng tỷ lệ đó trong mỗi thế hệ.

35 cấu hình duy nhất = full + 3 mốc held + 31 mức khác mốc. Mỗi cấu hình chạy trên 2 bài × 30 seed 7000–7029, quần thể 100 và cap 20.000 FE: **2.100 lượt**, tối đa **42 triệu FE**. Full/mốc held chỉ chạy một lần mỗi bài/seed, không nhân n khi dùng chung cho nhiều so sánh. Đây là các mức thăm dò được chọn trước khi thực thi, chưa có kết luận chúng tối ưu hoặc đã được xác nhận trên dữ liệu độc lập.

Các mức phải hữu hạn, không trùng và chứa mốc đúng một lần. Từ chối ratio restart dưới 0,8 vì production có clamp; số láng giềng phải từ 2 đến population−1. Có thể thu hẹp các danh sách, đổi `initial`/`held` hoặc bỏ tham số trước khi chạy. Thay đổi sau khi chạy yêu cầu thư mục mới.

## Chạy và tiếp tục

```powershell
# Chỉ xem kế hoạch; không chạy solver, không tạo thư mục kết quả.
.\.venv\Scripts\python.exe -m research sensitivity-mechanisms --stage plan --jobs 4

# Chạy nghiên cứu chính thức khi người dùng quyết định thực thi.
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -m research sensitivity-mechanisms --stage run --jobs 4

# Tiếp tục cùng source/config/reference/môi trường và thư mục.
.\.venv\Scripts\python.exe -m research sensitivity-mechanisms --stage run --jobs 4 --resume

# Tái tạo bảng/báo cáo; yêu cầu đủ primary, không chạy các task thiếu.
.\.venv\Scripts\python.exe -m research sensitivity-mechanisms --stage report --resume
```

Có `--config` và `--out-dir` để dùng cấu hình/thư mục riêng. `--jobs N` chạy tối đa N tiến trình solver độc lập, mặc định 1; N phải >=1. Dùng process spawn, không dùng thread chung RNG. Chỉ tiến trình cha ghi primary/manifest sau từng task hoàn tất; giữ tối đa 2N task đang chờ và xuất bảng theo thứ tự kế hoạch. Biến OMP/OPENBLAS/MKL ở trên giới hạn mỗi thư viện về 1 luồng mỗi worker; pipeline ghi nhận và kế thừa các biến này, không tự ép chúng. `--jobs 4` vì vậy là tối đa 4 solver đồng thời, không phải bảo đảm toàn bộ hệ thống chỉ có 4 thread.

Manifest ghi `execution_sessions` và mỗi primary ghi `execution_jobs`. Có thể đổi jobs khi resume với cùng source/config/reference/môi trường; runtime thuộc các mức tải khác nhau cần đọc riêng. Thay đổi mã từ phiên bản pipeline tuần tự cũ vẫn bị kiểm tra source từ chối, không tự nới kiểm tra hash để tiếp tục dữ liệu cũ. In kế hoạch ngay khi bắt đầu và tiến độ sau mỗi task; xuất bảng khi toàn bộ task hoàn tất. Khi gián đoạn giữa các task, `--resume` dùng lại dữ liệu đã có checksum. Nếu mất điện đúng giữa ghi primary và cập nhật manifest, pipeline từ chối orphan file để người vận hành kiểm tra, không tự tin tưởng dữ liệu không có checksum. Không chạy đồng thời hai lệnh ghi vào cùng thư mục kết quả.

Smoke nhỏ kiểm tra đường chạy, không phải bằng chứng chất lượng:

```powershell
.\.venv\Scripts\python.exe -m research sensitivity-mechanisms --config config/smoke/smoke_mechanism_sensitivity.yaml --stage run --jobs 2 --out-dir tmp/smoke/mechanism_sensitivity_jobs_smoke
```

Smoke: 8 cấu hình × 2 bài × 2 seed = 32 lượt, cap 300, quần thể 10. Không so p-value smoke với nghiên cứu chính thức.

## Dữ liệu và thống kê

Thư mục mặc định `results/experiments/mechanism_sensitivity_v1/`:

- `manifest.json`: thiết kế, danh sách cấu hình/đối chứng, source hashes, phiên bản Python/gói, biến thread, reference fronts và checksum primary cập nhật sau từng lượt.
- `primary/*.json`: task identity, mức/mode/settings, initial population hash, reference hash, final X/F, chỉ số, FE, runtime, trace và events.
- `derived/runs.csv`, `summary.csv`: mọi lượt và mean/SD mẫu/median IGD/HV của run hợp lệ; vẫn báo tổng run và số hợp lệ. SD không phải CI.
- `derived/comparisons.csv`: paired Wilcoxon hai phía, zero_method=wilcox, all-zero p=1; median(reference−level), rank-biserial dương thiên về mốc, p thô/p Holm và số cặp bị loại.
- `derived/trace.csv`, `events.csv`, `activation.csv`: diễn biến tham số, hoạt động toán tử, số sự kiện hoàn tất/bị chặn bởi cap và FE OBL/restart. FE event không bao gồm toàn bộ khởi tạo/DE/SBX; đọc `runs.csv` cho chi phí tổng.
- `derived/report.md`: bảng kết quả tự sinh, không tự suy diễn cơ chế hoặc đề xuất sửa production.

Đơn vị là lượt chạy theo seed; ghép cùng seed trong từng bài. Holm chung toàn họ đã cấu hình: mặc định **124 endpoint = 31 mức khác mốc × 2 bài × 2 chỉ số**, alpha=0,05. Không coi các endpoint chia sẻ mốc là thí nghiệm độc lập. Loại riêng cặp có output invalid và báo n; endpoint không còn cặp giữ p=1 trong họ và nhãn `no_valid_pairs`, không diễn giải là tương đương. IGD thấp/HV cao tốt. Không có điểm tổng, xếp hạng giữa bài hoặc tự chọn mức sau khi xem p-value.

Cần đọc chất lượng cùng activation: một mức ngưỡng không làm restart kích hoạt thì chưa kiểm tra được tác dụng khi restart hoạt động. OFAT không xác định tương tác hoặc đóng góp cộng tính; thay giá trị còn thay đường tìm kiếm và phân bổ FE. Runtime có telemetry. Chưa có CI bootstrap, kiểm chứng độc lập thứ hai hay biểu đồ tự sinh trong pipeline mới; các CSV đầy đủ cho phân tích/vẽ tiếp sau khi có dữ liệu chính thức. Không dùng pipeline nghiên cứu cũ `sensitivity-zdt` để tái tạo thiết kế này.
