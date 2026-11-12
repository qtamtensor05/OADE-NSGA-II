# Đo độ nhạy tham số trên ZDT bằng cách tăng/giảm từng tham số

## Phương pháp

Dùng cấu hình adaptive v2 trong `config/algorithms/oade_nsga2.yaml` làm mốc.
Mỗi lần chỉ đổi **một** tham số sang các giá trị trong danh sách, giữ nguyên
mọi tham số còn lại. Chạy mỗi mức trên cùng các seed và cùng bài toán, cùng
cap evaluation. Báo cáo trực tiếp việc tăng/giảm làm IGD/HV, độ dao động và
thời gian thay đổi thế nào **trên từng bài ZDT**.

Không có điểm tổng, rank, trọng số bộ bài toán, tương tác nhiều tham số,
winner/selection hoặc bước xác nhận cấu hình tự chọn. Không tự sửa cấu hình v2.
Baseline được chạy một lần mỗi bài/seed và dùng làm mốc cho mọi danh sách,
không nhân số replicate khi xuất nhiều bảng.

## Các mức mặc định

Chỉnh danh sách trong `config/studies/zdt_sensitivity.yaml` **trước khi chạy**.
Có thể bỏ bớt tham số để thu hẹp thí nghiệm. Mỗi danh sách phải có mức baseline
đúng một lần; pipeline từ chối tên sai, số không hợp lệ hoặc mức không có hiệu lực.

| Tham số | Danh sách mức | Baseline |
|---|---|---:|
| pop_size | 50, 100, 200 | 100 |
| stagnation_patience | 10, 20, 40 | 20 |
| stagnation_tolerance | 0.00001, 0.0001, 0.001 | 0.0001 |
| diversity_threshold | 0.01, 0.02, 0.05 | 0.02 |
| restart_elite_ratio | 0.8, 0.9, 0.95 | 0.8 |
| prob_de | 0.2, 0.5, 0.8 | 0.5 |
| n_neighbors | 3, 5, 10 | 5 |
| mean_F | 0.4, 0.65, 0.9 | 0.65 |
| mean_CR | 0.1, 0.5, 0.9 | 0.5 |

ZDT1/2/3 có 30 biến; ZDT4/6 có 10 biến. Không dùng ZDT5 vì bài đó mã hóa nhị
phân. Mặc định 30 seed 6000–6029, cap 20.000 evaluation/run. Có **19 cấu hình
duy nhất × 5 bài × 30 seed = 2.850 run**, tối đa 57 triệu solver evaluations.
Không tái sử dụng dữ liệu study chấm điểm đã bỏ.

Population khác nhau dùng khởi tạo từ cùng seed với quan hệ prefix, không phải
cùng số cá thể ban đầu. Front tham chiếu được chụp một lần mỗi bài, checksum
và dùng chung mọi run. Restart và mọi objective evaluation của solver đều tính
vào cap. Evaluation tạo front tham chiếu nằm ngoài cap solver.

## Lệnh chạy trên PowerShell

Chạy từ root repo bằng môi trường Python đã cài editable package.

```powershell
# Xem tổng số run trước; không chạy solver hoặc ghi kết quả.
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage plan

# Nghiên cứu chính thức: đo + xuất bảng/báo cáo + vẽ từng tham số.
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage all --jobs 6 --out-dir results/experiments/zdt_sensitivity_ofat_v1
```

Nếu dừng giữa chừng, giữ nguyên source/config/môi trường và dùng:

```powershell
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage all --jobs 6 --out-dir results/experiments/zdt_sensitivity_ofat_v1 --resume
```

Muốn tách đo và vẽ:

```powershell
# Chỉ đo và xuất bảng/báo cáo; không cần R ở bước này.
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage run --jobs 6 --out-dir results/experiments/zdt_sensitivity_ofat_v1

# Tạo lại bảng/report từ primary đã hoàn tất.
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage report --out-dir results/experiments/zdt_sensitivity_ofat_v1 --resume

# Vẽ từ dữ liệu đã đo; không chạy lại solver.
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage plot --out-dir results/experiments/zdt_sensitivity_ofat_v1 --resume
```

Vẽ bằng R, dùng thư viện renv của dự án. `--stage all/plot` kiểm tra R/packages
trước khi bắt đầu, không tự cài hay đổi backend. Nếu chưa có môi trường R,
cài R và restore `renv.lock`; vẫn có thể thu kết quả bằng `--stage run`.

Smoke nhỏ, không dùng làm kết quả nghiên cứu:

```powershell
.\.venv\Scripts\python.exe -m research sensitivity-zdt --config config/smoke/smoke_zdt_sensitivity.yaml --stage all --jobs 2
```

Smoke tự tạo session trong `tmp/smoke/`, có log và metadata; 100 run nhỏ trên
đủ năm bài và chín tham số. Study chính thức không chạy tự động trong kiểm tra.

## Kết quả cần đọc

```text
results/experiments/zdt_sensitivity_ofat_v1/
  study_manifest.json
  config/resolved.json
  config/reference_fronts.json
  primary/<task_id>.json
  derived/raw_runs.csv
  derived/summary.csv
  derived/comparisons.csv
  derived/report.md
  figures/<parameter>.png/.pdf/.svg
  figures/<parameter>.alignment.json
  figures/<parameter>.collision-audit.json
  figures/<parameter>.font-audit.json
  logs/run.log
```

- `summary.csv`: từng tham số/mức/bài, mean, SD, median, Q25/Q75 của IGD/HV,
  thời gian; valid/invalid, evaluation và restart telemetry. Baseline xuất trong
  mỗi danh sách để đọc, nhưng nguồn run chỉ được đo một lần.
- `comparisons.csv`: median mức thử và baseline trên cùng các seed hợp lệ,
  chênh lệch tuyệt đối và phần trăm. IGD có Δ âm là tốt; HV có Δ dương là tốt.
  Baseline bằng 0 thì không chia phần trăm, ghi `baseline_zero`. Không có cặp
  hợp lệ thì ghi `no_valid_pairs`, không tạo một số chất lượng giả.
- `report.md`: bảng trực tiếp và ảnh theo từng tham số, không chọn thay người đọc.
- Mỗi ảnh có 5 hàng bài toán, 2 cột IGD/HV; trục ngang là các mức tham số. Chấm
  là median, dải là Q25–Q75 (độ dao động, không phải CI). Đường cam đánh dấu mức
  v2 hiện tại. Đường nối chỉ hướng dẫn đọc các mức rời rạc.

Mọi invalid vẫn nằm trong primary/raw và số đếm. Chất lượng chỉ mô tả output
hợp lệ; bảng so sánh dùng cặp seed đều hợp lệ. Không xem median tốt hơn là
thắng có ý nghĩa thống kê, không tuyên bố tương đương hoặc tối ưu từ các hình.
Giá trị F/CR/probability là mức khởi tạo và có thể được adaptation cập nhật.

Nếu không có restart, chưa đo được tác động thực tế của các tham số restart.
Adaptive kernel ép elite ratio tối thiểu 0.8 nên không cho thử mức dưới 0.8.
Ngưỡng objective spread và các hằng số perturbation không được đổi trong study này.

## Toàn vẹn và tiếp tục chạy

Fresh run từ chối thư mục có dữ liệu. Checkpoint từng task sau khi hoàn tất;
resume kiểm tra danh tính source, config, môi trường, checksum, seed/task,
settings, front chung và budget trước khi dùng lại. Đổi danh sách sau khi có
kết quả phải dùng output mới, không sửa manifest để ép resume. Worker exception
dừng study và giữ dữ liệu đã checkpoint, không bỏ run lỗi để làm đẹp bảng.

Nếu bị ngắt giữa lúc ghi task và ghi manifest, orphan file bị từ chối; giữ lại
để điều tra, không tự chứng nhận. Báo cáo hoàn chỉnh chỉ xuất khi task đủ và
duy nhất. Nếu lỗi ở bước vẽ, primary và bảng vẫn giữ; sửa môi trường vẽ rồi
chạy lại `--stage plot --resume` với source/config tương ứng.

## Tái tạo phân tích bổ sung sau thực nghiệm

Tái tạo bảng kiểm tra và biểu đồ chính từ thư mục gốc bằng PowerShell:

```powershell
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
.\.venv\Scripts\python.exe -m research sensitivity-zdt --stage plot --resume --jobs 8
.\.venv\Scripts\python.exe analysis/tables/analyze_zdt_sensitivity.py
```

Hình bổ sung theo seed được tạo sau khi đã có `paired_seed_changes.csv`:

```powershell
$env:R_LIBS_USER = (Get-ChildItem renv/library/windows/R-4.6 -Directory | Select-Object -First 1).FullName
$env:TMPDIR = Join-Path (Get-Location).Path 'tmp'
& 'C:/Program Files/R/R-4.6.2/bin/Rscript.exe' --vanilla -e 'Sys.setlocale("LC_CTYPE","English_United States.utf8"); source("analysis/figures/plot_zdt_sensitivity_paired.R",encoding="UTF-8")'
```
