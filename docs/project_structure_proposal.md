# Đánh giá và đề xuất cấu trúc dự án nghiên cứu

Ngày khảo sát: 2026-11-12. Trạng thái: đề xuất, chưa di chuyển mã hoặc dữ liệu.

## 1. Kết luận

Dự án có nền tảng phù hợp cho nghiên cứu thực nghiệm: thuật toán, cấu hình,
benchmark, thống kê, kiểm tra provenance và báo cáo đã có nơi lưu riêng. Nên
chuẩn hóa theo hướng **một package Python, thí nghiệm có định danh, bằng chứng
được bảo toàn và dữ liệu tạm có vòng đời rõ ràng**. Không cần đưa các lớp service,
repository hay framework dependency injection vào mọi phần của mã nghiên cứu.

Ưu tiên trước là quy định nơi đặt file và tách dữ liệu tạm; sau đó mới đóng gói
Python và tách trách nhiệm runner. Đổi tên toàn bộ ngay sẽ làm tăng chi phí kiểm
chứng mà chưa cải thiện chất lượng bằng chứng nghiên cứu.

## 2. Đánh giá cấu trúc hiện tại

| Khu vực | Quan sát trực tiếp | Đánh giá / hướng xử lý |
|---|---|---|
| `src/oade_nsga2/` | Tách algorithm, core, operators, selection | Giữ ranh giới thuật toán, bổ sung giao diện chạy thống nhất khi cần |
| `algorithms/` | Ba baseline nội bộ nằm ngoài `src/` | Hợp nhất vào cùng package trong giai đoạn đóng gói |
| `src/benchmarking/` | Có evaluation, statistics, provenance riêng | Nền tảng tốt; tiếp tục bảo vệ budget, pairing và provenance |
| `src/benchmarking/algorithm_benchmark.py` | Chứa schema, adapter thuật toán, tổng hợp, I/O, orchestration và CLI | Nhiều lý do thay đổi trong một module; nên tách theo trách nhiệm |
| `main.py` | Registry lệnh chung, import trực tiếp các module xử lý | Giữ tương thích khi thêm CLI trong package |
| `scripts/run_benchmark_v2.py` | Có xử lý reuse và orchestration, sửa `sys.path` | Chuyển logic tái sử dụng vào package; script chỉ nhận tham số và gọi |
| `config/` | Suite, smoke và cấu hình khác nằm chung; algorithm/ablation có thư mục riêng | Phân nhóm suite, study, smoke; giữ định danh lịch sử trong registry |
| `src/plotting/` và `analysis/figures/` | Hai khu vực biểu đồ | Phân biệt tiện ích vẽ tái sử dụng với công thức tạo hình cho từng nghiên cứu |
| `docs/` | Có index, manuscript, registry và nhiều báo cáo ngang cấp | Tách governance, protocol, reports, manuscript khi số tài liệu tăng |
| `results/` | Chứa CSV chính, dẫn xuất, hình, provenance và smoke cục bộ | Bảo toàn dữ liệu chính; output thử chuyển sang `tmp/` |
| `scratch/` | Có probe/merge script, YAML smoke, validation JSON và thư mục archive | Không thể coi toàn bộ là rác; phải phân loại trước khi dọn |
| `tests/test_provenance.py` | Tạo thư mục UUID trong `scratch/`, dọn ở `finally` | Đã có cô lập; đổi sang `tmp/tests/` khi triển khai chính sách mới |
| Root | Có log, requirements snapshot theo ngày, môi trường Python/R | Log mới về tmp/run; snapshot môi trường về hồ sơ thực nghiệm |
| Packaging | Chưa có `pyproject.toml`; import `src.*`, script chèn root vào `sys.path` | Cần package cài được, tránh phụ thuộc thư mục chạy |

`.gitignore` hiện bỏ qua `scratch/`, `results/smoke*/`, log, cache và một số
artifact QA nặng. Đây là quy tắc Git, không phải chính sách lưu trữ hay bằng chứng
rằng các file bị ignore có thể xóa. Working tree sạch tại thời điểm bắt đầu khảo sát.

## 3. Cấu trúc đích

Đây là cấu trúc đề xuất cho mã và thí nghiệm mới; các đường dẫn dữ liệu công bố
hiện có được giữ trong thời gian chuyển đổi.

```text
OADE-NSGA-II/
├── pyproject.toml
├── README.md
├── README.vi.md
├── main.py                         # shim tương thích trong giai đoạn chuyển đổi
├── src/
│   └── oade_nsga2/                  # một namespace Python cài được
│       ├── __init__.py
│       ├── cli.py
│       ├── algorithms/
│       │   ├── oade/                # algorithm, core, operators, selection
│       │   └── baselines/           # ce_moea, cgde_nsga2, nsga2_sdr_ols
│       ├── benchmarking/
│       │   ├── models.py            # AlgorithmSpec, RunOutcome, schema
│       │   ├── adapters/            # tích hợp từng họ solver
│       │   ├── runner.py            # điều phối seed/problem/checkpoint
│       │   ├── evaluation.py        # budget, chỉ số, validation
│       │   ├── statistics.py        # pairing, test, effect size
│       │   └── provenance.py
│       ├── studies/                # ablation và sensitivity
│       ├── io/                     # YAML, CSV, lưu checkpoint
│       └── plotting/               # primitive/style vẽ dùng chung
├── config/
│   ├── algorithms/
│   ├── suites/                     # zdt, dtlz, wfg
│   ├── studies/                    # ablation, restart, sensitivity
│   ├── smoke/                      # cấu hình kiểm tra nhỏ, có version control
│   └── plotting/
├── analysis/
│   ├── figures/                    # recipe tạo hình theo nghiên cứu
│   └── tables/                     # recipe tạo bảng khi có nhu cầu
├── scripts/
│   ├── maintenance/                # inventory, kiểm tra cấu trúc, dọn tmp
│   └── figure_qa/                  # công cụ QA tái sử dụng
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/                   # mẫu nhỏ cần tái lập
├── docs/
│   ├── index.md
│   ├── governance/                # cấu trúc, đặt tên, vòng đời artifact
│   ├── protocols/                 # budget, thống kê, reproducibility
│   ├── reports/
│   └── manuscript/                # manuscript, references
├── results/
│   ├── <historical_dataset>/       # giữ đường dẫn cũ đã được viện dẫn
│   ├── provenance/                # lineage/composition hiện có
│   ├── figures/                   # bundle hình hiện có
│   └── experiments/                # thí nghiệm mới
│       └── <experiment_id>/
│           └── <execution_id>/
│               ├── primary/       # CSV gốc, validation, convergence, manifest
│               ├── derived/       # summary, paired statistics, cost
│               ├── figures/       # PDF, SVG, PNG và source data
│               ├── qa/
│               ├── config/        # snapshot cấu hình đã resolve
│               ├── environment/   # dependency snapshot và thông tin hệ thống
│               └── logs/
├── tmp/                            # chỉ dữ liệu được phép loại bỏ
│   ├── smoke/<session_id>/
│   ├── one_off/<session_id>/
│   ├── tests/<session_id>/
│   └── figure_qa/<session_id>/
├── requirements.txt               # giữ tương thích khi chuyển packaging
├── renv.lock
└── renv/                           # giữ cơ chế bootstrap R hiện có
```

Chưa tạo thư mục rỗng để cho đủ cây. Chỉ tạo khi có nội dung hoặc khi công cụ cần.
Phân chia `primary/derived` là thay đổi hợp đồng output tương lai: runner và
provenance hiện đọc các CSV trong cùng một thư mục; phải cập nhật cùng nhau trước
khi dùng cấu trúc này. Không chỉ di chuyển file bằng tay.

## 4. Quy định đặt tên

| Đối tượng | Quy tắc | Ví dụ |
|---|---|---|
| Module, script, YAML, thư mục mới | `lower_snake_case`, không dấu, không khoảng trắng | `run_benchmark.py`, `restart_confirmation.yaml` |
| Hàm, biến | `snake_case`; đại lượng có đơn vị khi cần | `runtime_seconds`, `evaluation_budget` |
| Class / constant | `PascalCase` / `UPPER_SNAKE_CASE` | `RunOutcome`, `PRIMARY_FILES` |
| Script tái sử dụng | Động từ + đối tượng | `inventory_research.py`, `validate_provenance.py` |
| Script dùng một lần | `probe_`, `check_`, `merge_`, `repair_` theo mục đích, đặt trong session | `tmp/one_off/.../probe_wfg_runtime.py` |
| Test | `test_<behavior_or_module>.py` | `test_budget_accounting.py` |
| Tài liệu mới | Tên chủ đề ổn định | `artifact_lifecycle.md`, `project_structure.md` |
| Experiment ID | Câu hỏi / suite + protocol revision | `zdt_7algo_budget20k_v3` |
| Execution / session ID | `YYYYMMDDTHHMMSSZ_<purpose>_<shortid>`; UTC | `20261112T030000Z_restart_probe_a1b2c3` |
| Artifact trong execution | Tên vai trò ổn định, không nhắc lại mọi tham số | `raw_runs.csv`, `validation.csv`, `summary.csv` |
| Figure | Tên ngữ nghĩa thống nhất cho cả bundle | `wfg_scaling.pdf`, `wfg_scaling.svg`, `wfg_scaling_source.csv` |

Không dùng `final`, `final2`, `new`, `latest`, `backup` để phân biệt phiên bản.
Đổi protocol thì tăng revision; chạy lại cùng protocol thì tạo execution mới.
Git quản lý phiên bản mã; manifest quản lý danh tính lần chạy. Tham số chi tiết,
seed list, commit, source hash và package version thuộc manifest, không nhồi vào tên.

Tên thuật toán đã dùng trong CSV (`OADE_NSGAII`, `NSGA2`, ...) là định danh dữ liệu:
giữ nguyên và đối chiếu `docs/baselines.md`. Không áp dụng snake_case để đổi nhãn
lịch sử. Các tên CLI hiện dùng dấu gạch ngang và file hệ thống như `README.md`,
`renv.lock` là ngoại lệ có chủ ý. Không đổi schema/tên CSV lịch sử chỉ để đẹp tên.

## 5. Chính sách tmp và dọn dẹp

### Phân loại bắt buộc

| Nội dung | Nơi lưu | Điều kiện dọn |
|---|---|---|
| Smoke config tái sử dụng, fixture, script QA chung | `config/smoke/`, `tests/fixtures/`, `scripts/` | Quản lý bằng Git, không đi vào cleanup tmp |
| Smoke output, probe, script dùng một lần | `tmp/<category>/<session_id>/` | Session đã hoàn thành, được đánh dấu disposable |
| Dữ liệu nghiên cứu, correction, lineage, bằng chứng trước sửa | `results/` với registry liên kết | Không nằm trong cleanup tự động |
| Cache môi trường | `.venv/`, `renv/library/`, `.r-bootstrap/` | Chính sách riêng; không gom chung với cleanup nghiên cứu |

Mỗi session tạm có `session.json` và có thể có `README.md` ngắn. Schema tối thiểu
đề xuất cho công cụ tương lai:

```json
{
  "schema": 1,
  "purpose": "Smoke provenance after packaging change",
  "created_utc": "2026-11-12T03:00:00Z",
  "status": "completed",
  "disposable": true,
  "retention_days": 7,
  "promoted_to": [],
  "command": "exact command used"
}
```

Vòng đời: `active` → `completed` hoặc `failed` → lưu phần cần giữ → xác nhận
`disposable=true` → dọn. `failed` không tự đồng nghĩa với disposable; lỗi có thể
là bằng chứng cần điều tra. Session đang chạy không được dọn chỉ vì đã quá hạn.
Khởi tạo mặc định `status=active`, `disposable=false`; chuyển trạng thái khi kết thúc.

Quy tắc đề xuất cho `scripts/maintenance/clean_tmp.py` khi triển khai:

1. Mặc định chỉ in danh sách và tổng dung lượng (`dry-run`); dùng `--apply` mới xóa.
2. Chỉ nhận session bên dưới `tmp/` đã resolve trong repo, không nhận repo root,
   không theo symlink/junction/reparse point ra ngoài. Không xóa chính `tmp/`.
3. Chỉ chọn session có metadata hợp lệ, đã kết thúc, `disposable=true` và hết
   retention; thiếu metadata thì báo để phân loại thủ công.
4. Kiểm tra không có file Git tracked và không có tác vụ đang sử dụng. Công cụ
   tạo session cần lock dùng chung; khi xóa phải kiểm tra và giữ lock độc quyền.
5. Ghi danh sách đã xóa vào log ngoài session đang xóa. Cho phép chọn một session.
6. Tuyệt đối không mở rộng phạm vi sang `scratch/`, `results/` hoặc môi trường.

Retention khởi điểm: smoke/test/QA tạm 7 ngày, one-off 14 ngày; đây là mặc định
đề xuất, không phải lý do tự xóa file hiện có.

Nếu một probe trở thành bằng chứng trong báo cáo, đưa script có ích vào
`analysis/` hoặc package; đưa output và nguồn gốc vào `results/`; ghi liên kết và
checksum. Chỉ sau khi kiểm tra bản lưu mới đánh dấu session disposable. Script
merge/repair dữ liệu nghiên cứu cần giữ recipe và lineage, dù chỉ chạy một lần.

Trong giai đoạn đầu, bổ sung `/tmp/` vào `.gitignore`; chính sách tmp được lưu
ở tài liệu tracked. Tiếp tục giữ ignore `scratch/` và `results/smoke*/` để tương
thích, nhưng ngừng tạo session mới ở đó sau khi các caller đã được đổi.

## 6. Áp dụng SOLID theo nhu cầu thực tế

SOLID hướng dẫn ranh giới trách nhiệm và phụ thuộc; cây thư mục riêng lẻ không
chứng minh mã tuân thủ SOLID.

| Nguyên tắc | Áp dụng đề xuất | Kiểm chứng hữu ích |
|---|---|---|
| Single responsibility | Tách CLI, runner, adapters, schema, persistence; giữ evaluation/statistics riêng | Đổi format lưu không phải sửa thuật toán |
| Open/closed | Adapter registry và cấu hình solver; dựa trên `AlgorithmSpec` hiện có | Thêm solver không phải thêm nhiều nhánh vào orchestration |
| Liskov substitution | Adapter trả cùng hợp đồng `RunOutcome`, budget và seed/warm start | Contract test cho từng adapter về shape, budget, diagnostics |
| Interface segregation | Giao diện nhỏ cho chạy solver, ghi kết quả và ghi trajectory khi cần | Solver không bị buộc phụ thuộc plotting hoặc CLI |
| Dependency inversion | Runner nhận adapter/writer qua tham số; kernel thuật toán không import runner/CLI | Unit test có thể dùng solver giả và writer tạm |

Luồng phụ thuộc: CLI → runner/study → adapters → thuật toán; runner dùng
evaluation, statistics và persistence. Analysis đọc artifact qua hợp đồng dữ liệu,
không import CLI. Chỉ tạo interface khi có nhu cầu thay thế hoặc kiểm thử; ưu tiên
function, dataclass và `typing.Protocol` nhỏ thay vì hệ thống class lớn.

## 7. Lộ trình triển khai và tiêu chí hoàn thành

### Giai đoạn 1 — Chính sách và dữ liệu tạm

- Thông qua quy ước; thêm ignore tmp và helper tạo/đóng session.
- Chuyển output mặc định của smoke sang tmp session; giữ smoke config tracked.
- Chuyển thư mục tạm trong test provenance sang `tmp/tests/`.
- Phân loại từng mục trong `scratch/`: disposable, cần promotion, hoặc chưa rõ.
  Đặc biệt các archive và validation JSON không tự động bị coi là rác.
- Triển khai cleanup dry-run trước, kiểm thử đường dẫn thoát root, junction,
  session active, metadata lỗi, file tracked và retention.

Hoàn thành khi một smoke mới gom script/config thử/output/log vào cùng session,
cleanup chỉ chọn đúng session đã kết thúc, và không thay đổi checksum kết quả cũ.

### Giai đoạn 2 — Package và ranh giới mã

- Thêm `pyproject.toml`, namespace package và CLI; cài editable trong môi trường.
- Chuyển baseline vào package, cập nhật import và `class_path` cấu hình.
- Giữ `main.py` shim và alias lệnh cũ; bỏ chèn `sys.path` sau khi caller đã chuyển.
- Tách benchmark module từng bước, không đổi thuật toán hay protocol cùng đợt.
- Cập nhật cách xác định root và danh sách source hash trong provenance.

Hoàn thành khi CLI/package import được ngoài repo root, bộ unit/integration hiện
có đạt, smoke kiểm tra được mọi adapter và budget, và lệnh cũ còn hoạt động theo
cam kết tương thích. Smoke không thay thế bằng chứng benchmark đầy đủ.

### Giai đoạn 3 — Experiment và tài liệu

- Cập nhật writer/reader/provenance đồng bộ trước khi dùng primary/derived.
- Thí nghiệm mới dùng experiment/execution ID, snapshot config và môi trường.
- Tách docs theo vai trò, sửa index và toàn bộ liên kết tương ứng.
- Phân biệt plotting primitive dùng chung với recipe figure gắn với nghiên cứu.
- Thêm kiểm tra cấu trúc nhẹ cho file mới: không log ở root, không script
  disposable ở scripts, không output thử trong dataset công bố.

Hoàn thành khi mỗi báo cáo truy được đến execution/dataset, config, nguồn dữ liệu,
recipe phân tích, hình và QA; không có liên kết cũ bị đứt.

### Ràng buộc bảo toàn nghiên cứu

`src/benchmarking/provenance.py` hiện hash mã theo đường dẫn và so sánh chính xác
`protocol`, `source_hashes`, `environment` trước resume/reuse. Di chuyển module
làm thay đổi source identity dù thuật toán không đổi. Vì vậy:

- Không sửa manifest cũ để ép tương thích, không chứng nhận lại dữ liệu lịch sử
  bằng code hiện tại, không nới kiểm tra hash chỉ để vượt qua refactor.
- Hoàn tất hoặc bảo quản execution đang dở trước thay đổi; sau refactor dùng
  output directory mới. Nếu cần tiếp tục execution cũ, dùng đúng checkout và
  môi trường cũ được ghi nhận.
- Giữ CSV, checksum, lineage và đường dẫn lịch sử. Di chuyển dữ liệu chỉ khi có
  inventory trước/sau, ánh xạ đường dẫn, cập nhật tất cả consumer và kiểm chứng.
- Không chạy lại benchmark lớn chỉ để xác nhận việc tổ chức file; dùng test
  hành vi và smoke trước. So sánh số liệu bổ sung chỉ khi thay đổi có thể tác
  động kết quả hoặc kiểm tra phát hiện sai khác.

## 8. Phạm vi thay đổi của lần đánh giá này

Chỉ bổ sung tài liệu đề xuất và liên kết trong docs index. Chưa thực hiện cleanup,
đổi tên, di chuyển, thêm package, sửa output hay chạy benchmark. Các ví dụ cấu
trúc và schema ở trên mô tả trạng thái đích, không phải tính năng đã triển khai.
