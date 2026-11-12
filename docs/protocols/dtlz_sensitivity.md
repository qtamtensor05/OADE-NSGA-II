# Đo độ nhạy tham số v2 trên DTLZ1–4

Pipeline `sensitivity-dtlz` khảo sát từng tham số độc lập quanh cấu hình OADE-NSGA-II v2 hiện tại. Thiết kế và danh sách mức tương ứng đợt ZDT; không chấm điểm tổng hợp hoặc tự chọn cấu hình.

## Phạm vi và ngân sách

| Bài | M = 2: số biến | M = 3: số biến | M = 5: số biến |
|---|---:|---:|---:|
| DTLZ1 | 6 | 7 | 9 |
| DTLZ2 | 11 | 12 | 14 |
| DTLZ3 | 11 | 12 | 14 |
| DTLZ4 | 11 | 12 | 14 |

Phạm vi mặc định khớp bộ DTLZ1–4 trong báo cáo đa mục tiêu hiện tại. Có 12 trường hợp riêng, được định danh như `dtlz2_m3`; dữ liệu giữa các số mục tiêu không được gộp. Mỗi trường hợp dùng 30 seed từ 7000 đến 7029, tối đa 20.000 lần đánh giá hàm mục tiêu mỗi lượt, gồm khởi tạo và restart.

| Tham số | Các mức | Mức tham chiếu |
|---|---|---:|
| `pop_size` | 50, 100, 200 | 100 |
| `stagnation_patience` | 10, 20, 40 | 20 |
| `stagnation_tolerance` | 0,00001; 0,0001; 0,001 | 0,0001 |
| `diversity_threshold` | 0,01; 0,02; 0,05 | 0,02 |
| `restart_elite_ratio` | 0,8; 0,9; 0,95 | 0,8 |
| `prob_de` | 0,2; 0,5; 0,8 | 0,5 |
| `n_neighbors` | 3, 5, 10 | 5 |
| `mean_F` | 0,4; 0,65; 0,9 | 0,65 |
| `mean_CR` | 0,1; 0,5; 0,9 | 0,5 |

Baseline được chạy một lần cho mỗi bài/số mục tiêu/seed và dùng chung cho các danh sách. Có 19 cấu hình duy nhất, tổng cộng **6.840 lượt**, cap tổng **136.800.000 evaluation**. Có thể bỏ các tham số hoặc trường hợp bài toán khỏi [cấu hình](../../config/studies/dtlz_sensitivity.yaml) trước khi bắt đầu để thu hẹp thí nghiệm; mỗi danh sách phải chứa mức tham chiếu.

Front tham chiếu dùng chung hàm tạo với benchmark DTLZ: Das–Dennis H = 200/20/6 cho M = 2/3/5; điểm tham chiếu HV bằng cực đại từng mục tiêu trên front cộng 0,1. Front được chụp vào `config/reference_fronts.json` và kiểm tra checksum khi resume. HV tuyệt đối không được so sánh giữa các số mục tiêu khác nhau.

## Lệnh chạy

Chạy từ thư mục gốc dự án. `plan` chỉ đếm thiết kế, không chạy solver:

```powershell
.\.venv\Scripts\python.exe -m research sensitivity-dtlz --stage plan
```

Chạy phép đo, xuất bảng/báo cáo và biểu đồ:

```powershell
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -m research sensitivity-dtlz --config config/studies/dtlz_sensitivity.yaml --stage all --jobs 6
```

Tiếp tục sau khi bị ngắt:

```powershell
.\.venv\Scripts\python.exe -m research sensitivity-dtlz --config config/studies/dtlz_sensitivity.yaml --stage all --jobs 6 --resume
```

`--stage run` chỉ đo và xuất bảng/báo cáo, không cần R. `--stage report --resume` tổng hợp lại bảng; `--stage plot --resume` tổng hợp và vẽ lại từ primary, không chạy lại solver. Bước `all/plot` kiểm tra R và các package trước khi thực hiện. Cấu hình mặc định dùng 6 worker; có thể thay bằng số phù hợp với máy, runtime khi chạy song song chỉ là số đo quan sát.

## Đầu ra và phạm vi Git

Kết quả chính lưu tại `results/experiments/dtlz_sensitivity_ofat_v1/`:

- `primary/`: checkpoint từng lượt, giữ cục bộ và đã bị loại khỏi Git.
- `study_manifest.json`, `config/`: danh tính source, môi trường, cấu hình, front và checksum.
- `derived/raw_runs.csv`: từng lượt, có số mục tiêu, evaluation thực tế, trạng thái hợp lệ và telemetry restart.
- `derived/summary.csv`: từng tham số/mức/trường hợp; mean, SD, median, Q25/Q75, valid/invalid và restart.
- `derived/comparisons.csv`: chênh lệch median so với baseline trên cặp seed đều hợp lệ; IGD giảm và HV tăng là chiều thuận lợi.
- `derived/report.md`: đủ bảng và ảnh nhúng cho từng tham số, tách nhóm M = 2/3/5.
- `figures/<parameter>_m<M>.{png,pdf,svg}`: 27 bộ hình với cấu hình đầy đủ; điểm là median, vùng tô Q25–Q75, không phải khoảng tin cậy.

Output invalid được giữ trong primary/raw và số đếm, không được thay bằng số chất lượng giả. Baseline bằng 0 thì chênh lệch phần trăm không xác định; không có cặp hợp lệ thì ghi `no_valid_pairs`. Không gộp các trường hợp thành một điểm hoặc diễn giải median bằng nhau thành tương đương thống kê. Các tham số F/CR/probability là giá trị khởi tạo có adaptation.

Hoàn tất phép đo, đóng gói bằng chứng gốc để lưu Git bằng một file thay vì hàng nghìn checkpoint:

```powershell
.\.venv\Scripts\python.exe scripts/maintenance/archive_experiment.py results/experiments/dtlz_sensitivity_ofat_v1
```

Giữ nguyên source, môi trường, cấu hình và front khi resume. Thư mục kết quả mới không được chứa dữ liệu cũ; mỗi thay đổi thiết kế dùng thư mục mới. Worker lỗi dừng study và giữ checkpoint đã ghi. Báo cáo hoàn chỉnh chỉ được xuất khi có đủ task duy nhất. Cấu hình và nội dung smoke nằm trong `tmp/`, không đưa vào commit.
