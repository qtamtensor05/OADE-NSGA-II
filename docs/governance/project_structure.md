# Cấu trúc dự án và quy định lưu artifact

Áp dụng từ 2026-11-12. Đây là quy định đang triển khai trong mã; bản khảo sát
trước chuyển đổi ở [đề xuất gốc](../project_structure_proposal.md).

## Cấu trúc hiện hành

```text
src/
  oade_nsga2/                   chỉ kernel OADE và luồng gọi của OADE
  nsga2/                        adapter/luồng gọi NSGA-II từ pymoo
  rnsga2/                       adapter pymoo, thiết lập aspiration points
  dnsga2/                       adapter/luồng gọi D-NSGA-II từ pymoo
  cgde_nsga2/                   kernel và luồng gọi CGDE
  nsga2_sdr_ols/                kernel và luồng gọi SDR-OLS
  ce_moea/                      kernel và luồng gọi CE-MOEA
  shared/
    contracts.py               AlgorithmSpec, RunOutcome
    evaluation.py              budget, kiểm tra kết quả
    population.py              khởi tạo quần thể chung
    fronts.py                  trích Pareto front chung
    pymoo_execution.py         sampling, budget/callback dùng chung cho pymoo
    artifacts.py               tên artifact và định tuyến layout
    io/                        YAML, CSV
    paths.py                   resolve root và đường dẫn checkout
  research/
    benchmarking/              điều phối, metric, thống kê, provenance, lưu kết quả
      adapters.py              chỉ registry/router, không chứa thân solver
      convergence.py           tính và ghi IGD/HV theo checkpoint
    studies/                   ablation, sensitivity
    plotting/                  plotting và QA dùng chung
    maintenance/               tmp, inventory, kiểm tra cấu trúc
    cli.py                     registry lệnh nghiên cứu
config/
  algorithms/  ablations/      cấu hình solver và biến thể thành phần
  suites/  studies/            benchmark và nghiên cứu bổ sung
  smoke/  plotting/            smoke tái sử dụng và cấu hình vẽ
  environments/               dependency snapshot theo mục đích
  legacy_paths.json           ánh xạ tên cấu hình cũ
analysis/figures/              recipe hình gắn với báo cáo cụ thể
scripts/                      wrapper CLI tương thích và công cụ vận hành
tests/unit/                   kernel, budget, thống kê, provenance, cleanup
tests/integration/            layout execution và resume
docs/
  governance/  protocols/  reports/  manuscript/
results/                      bằng chứng nghiên cứu được giữ lâu dài
tmp/                          output thử và script dùng một lần, Git ignored
```

Không tạo thư mục rỗng cho đủ cây. `analysis/tables/`, `tests/fixtures/` chỉ thêm
khi có recipe hoặc fixture thực tế. Mỗi thuật toán có một thư mục trực tiếp dưới src. Không có lớp algorithms/baselines
bọc bên ngoài, không đặt research bên trong thư mục OADE. Mỗi thư mục thuật toán
chỉ chứa Python source; tài liệu thuật toán nằm ở docs/protocols/algorithms.
`runner.py` sở hữu luồng chạy riêng; `legacy.py` giữ luồng generation-based cũ
khi thuật toán đó có hỗ trợ. `research/benchmarking/adapters.py` chỉ điều phối.

Các tài liệu cũ ở `docs/*.md` còn trang chuyển tiếp để giữ đường dẫn file.
Liên kết vào anchor của tài liệu cũ nên cập nhật sang trang canonical vì trang
chuyển tiếp không bảo toàn anchor. README và docs index dùng đường dẫn mới.

## Đặt tên và ranh giới trách nhiệm

- File/module/thư mục mới: `lower_snake_case`, không dấu và không khoảng trắng.
  Class `PascalCase`, constant `UPPER_SNAKE_CASE`; tên đại lượng ghi đơn vị như
  `runtime_seconds`. Ngoại lệ: tên chuẩn công cụ, README và CLI dùng dấu gạch ngang.
- Script tái sử dụng: động từ + đối tượng, ví dụ `check_structure.py`.
  Script probe/merge/repair dùng một lần nằm trong session; nếu là recipe tái lập
  dữ liệu nghiên cứu thì lưu ở `analysis/` và ghi lineage, dù chỉ chạy một lần.
- Experiment ID: câu hỏi/suite và revision protocol, ví dụ `zdt_7algo_budget20k_v3`.
  Execution ID tự sinh UTC + ID ngẫu nhiên. Cùng protocol, lần chạy mới → execution
  mới; thay protocol → revision mới. Không dùng `final2`, `new`, `latest`.
- Tên thuật toán và schema CSV lịch sử giữ nguyên. Các execution mới vẫn dùng
  `algorithm_benchmark_*.csv` để tương thích consumer; không đổi schema chỉ vì
  đã chuyển thư mục.
- Kernel thuật toán không phụ thuộc CLI, plotting hoặc persistence. Runner gọi
  adapter theo hợp đồng RunOutcome; evaluation, statistics và lưu file có module
  riêng. Facade chỉ tái xuất API; logic mới phải vào module sở hữu trách nhiệm.
- Primitive vẽ và QA dùng chung ở package; recipe tạo hình cụ thể ở analysis.
  Module không chèn root repo vào `sys.path`.
- Thuật toán và shared không được import research. Thuật toán không import kernel
  của thuật toán khác. Lựa chọn lớp solver cụ thể từ `pymoo.algorithms` nằm trong
  thư mục thuật toán sở hữu nó; không nằm trong benchmark.
- Code dùng chung cho sampling, budget và callback pymoo nằm ở shared; runner
  của từng thuật toán chọn lớp thư viện và thiết lập tham số riêng. RNSGA2 sở hữu
  logic aspiration points và warning policy; NSGA2/DNSGA2 có runner riêng.
- IGD/HV, validation, thống kê, bảng và biểu đồ không đặt trong thư mục thuật toán.
  Các phép toán tạo thành chính thuật toán (mutation, selection, adaptation) vẫn
  ở kernel thuật toán tương ứng.
- Thêm thuật toán pymoo mới: tạo thư mục và runner của thuật toán, đăng ký class
  path trong registry và thêm YAML. Không tự gọi một class path chưa có adapter.

## Cài và chạy

Distribution `oade-nsga2-research` chứa các package thuật toán ngang hàng,
`shared` và `research`. `oade_nsga2` chỉ là package thuật toán OADE.
CLI module hiện là `python -m research`; console command `oade` và `main.py`
giữ nguyên. Không đặt CLI trở lại trong thư mục thuật toán để giữ lệnh module cũ.

Package hiện hướng tới **editable checkout nghiên cứu**: cấu hình và dữ liệu nằm
trong repo, không được bundle vào wheel. Không coi wheel cài độc lập là bản phân
phối toàn bộ nghiên cứu.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m research --help
.\.venv\Scripts\oade.exe --help
.\.venv\Scripts\python.exe main.py --help
```

Sau cài editable, import/package CLI chạy được từ ngoài repo. Input cấu hình
tương đối được resolve từ root checkout; `--config` tuyệt đối dành cho input bên
ngoài. Output mặc định trong YAML được neo về repo; `--out-dir` tương đối được
hiểu theo working directory của người gọi. Lệnh cũ và đường dẫn cấu hình cũ còn
hoạt động qua wrapper/alias, không giữ hai bản implementation song song.

## Session tạm

```powershell
# Tự sinh session, snapshot config, log và output; thành công được đánh dấu disposable.
.\.venv\Scripts\python.exe -m research benchmark --config config/smoke/smoke_benchmark.yaml --jobs 2
.\.venv\Scripts\python.exe -m research sensitivity --config config/smoke/smoke_sensitivity.yaml

# Script dùng một lần: tạo session rồi lưu script, input, output, log vào đó.
.\.venv\Scripts\python.exe -m research tmp create one_off "probe_wfg_runtime"
.\.venv\Scripts\python.exe -m research tmp close <session_path> --disposable

# Mặc định dry-run. Chỉ --apply mới xóa.
.\.venv\Scripts\python.exe -m research tmp clean
.\.venv\Scripts\python.exe -m research tmp clean --session <session_path> --apply
```

Layout: `tmp/{smoke,one_off,tests,figure_qa}/<UTC_purpose_shortid>/`.
Metadata `session.json` ghi schema, purpose, created/closed UTC, status,
disposable, retention_days, promoted_to và command. Session bắt đầu active,
disposable=false; lỗi mặc định được giữ. Retention tính từ lúc đóng: 7 ngày
cho smoke/tests/QA, 14 ngày cho one-off. Trạng thái failed không tự cho phép xóa.

Smoke config là source tracked. Output smoke mặc định được bọc trong session
có lock, config snapshot và log; `--out-dir` tường minh là chế độ người gọi tự
quản lý, không tự cấp metadata/dọn. Resume smoke phải truyền đúng `--out-dir`
cũ; không dùng resume để tự tạo session khác.

Cleanup chỉ nhận session trực tiếp dưới category hợp lệ trong repo, từ chối
symlink/junction/reparse point, file Git tracked, metadata lỗi, session active,
session chưa hết hạn hoặc không disposable. Runner và cleaner dùng cùng khóa OS;
công cụ bên ngoài phải tuân thủ khóa này nếu dùng session. Với script thủ công,
giữ session active cho đến khi tiến trình đã kết thúc rồi mới đóng. Cleanup ghi
nhật ký ngoài session tại `tmp/cleanup.jsonl`. Đây là dọn có chủ ý theo lệnh,
không có lịch tự xóa nền.

Kết quả được viện dẫn trong báo cáo phải được promotion sang results cùng recipe,
checksum và lineage trước khi cho phép dọn session. Không dùng tmp làm bản lưu duy
nhất cho bằng chứng nghiên cứu. Không nhập session.json cho dữ liệu cũ để tự động
biến dữ liệu đó thành disposable.

## Execution nghiên cứu mới

```powershell
$env:OMP_NUM_THREADS=1
$env:OPENBLAS_NUM_THREADS=1
$env:MKL_NUM_THREADS=1
.\.venv\Scripts\python.exe -m research benchmark --config config/suites/algorithm_benchmark_v2.yaml --experiment zdt_7algo_budget20k_v3 --jobs 6
# Sao chép execution root in trong output; không dùng primary/derived riêng lẻ làm bộ dữ liệu.
.\.venv\Scripts\python.exe -m research benchmark --config config/suites/algorithm_benchmark_v2.yaml --out-dir <execution_root> --resume
```

`--experiment` áp dụng cho runner benchmark chung, bao gồm ablation, DTLZ và WFG;
không kết hợp với `--out-dir` hoặc `--resume`. Sensitivity và runner legacy giữ
layout riêng hiện có; output thử sensitivity vẫn được quản lý bằng tmp session.

```text
results/experiments/<experiment_id>/<execution_id>/
  execution.json
  primary/        raw_runs, validation, convergence, execution manifest
  derived/        summary, paired statistics, cost
  config/         resolved suite và cấu hình solver đã resolve
  environment/    runtime và dependency snapshot
  logs/           run log và trạng thái
  figures/        bundle hình khi được tạo
  qa/             kết quả QA khi được tạo
```

Reader CSV chung và benchmark persistence nhận execution root hoặc thư mục
primary/derived; tự định tuyến theo execution.json. Dataset lịch sử dạng flat
tiếp tục đọc/ghi theo hợp đồng cũ. Plotting CLI benchmark có thể nhận `--out-dir`
execution root và ghi vào figures; recipe hình theo báo cáo lịch sử vẫn đọc
dataset lịch sử của chính nó. Chuyển recipe đó sang dataset khác là thay đổi
phân tích riêng, không tự thực hiện trong đợt tổ chức thư mục.

Provenance nằm trong primary và checksum theo tên CSV gốc; derived có thể tái
tạo sau khi primary được xác minh. Reader không thay thế việc kiểm chứng manifest.
Không chỉnh manifest lịch sử để ép resume sau refactor. Source path/hash đã đổi;
execution trước refactor cần đúng checkout/môi trường cũ, hoặc chạy execution mới.

## Dữ liệu cũ và kiểm tra

Các dataset, figures, corrections, provenance và archive cũ không bị di chuyển
hay xóa trong đợt này. [Inventory scratch](legacy_scratch_inventory.json) phân
loại từng mục nhưng không cấp quyền xóa. `scratch/` và `results/smoke*/` tiếp tục
được ignore để tương thích; session mới đi vào tmp. Log cũ ở root được giữ;
không tạo thêm log root.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m research check-structure
.\.venv\Scripts\python.exe -m research inventory --out tmp/one_off/<session_id>/research_inventory.json
git diff --check
```

Structure checker xét file mới/thay đổi, chặn source namespace cũ, tên Python
không đúng quy tắc, script disposable ở scripts, log root và smoke output trong
results; đồng thời kiểm tra liên kết file trong README/docs đang duy trì.
Không áp đặt việc đổi tên hàng loạt dữ liệu/tài liệu lịch sử. Kết quả kiểm chứng
đợt điều chỉnh mới nhất ở [flat algorithm migration](flat_algorithm_migration_20261112.md).
Báo cáo [đợt chuyển đổi đầu](structure_migration_20261112.md) được giữ làm lịch sử.
