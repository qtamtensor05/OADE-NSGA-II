# Kết quả triển khai cấu trúc — 2026-11-12

Báo cáo lịch sử của đợt chuyển đổi đầu. Cấu trúc package đã được điều chỉnh
tiếp theo yêu cầu mỗi thuật toán một thư mục trong src; xem
[báo cáo điều chỉnh](flat_algorithm_migration_20261112.md) và
[quy định hiện hành](project_structure.md).

## Phạm vi hoàn thành

- Giai đoạn 1: session tmp, metadata, khóa OS, retention, cleanup dry-run/apply;
  smoke output về session, test output về tmp/tests; phân loại scratch cũ.
- Giai đoạn 2: editable package `oade-nsga2-research`, namespace `oade_nsga2`,
  console command `oade`, wrapper `main.py` và script cũ. Baseline nằm trong
  package; benchmark tách models/adapters/persistence/runner, có adapter registry
  và điểm truyền solver vào runner. Không thay đổi kernel solver.
- Giai đoạn 3: config phân nhóm, alias đường dẫn cũ, docs phân theo vai trò và
  trang chuyển tiếp; QA dùng chung import từ package; execution mới có
  primary/derived/config/environment/logs và reader tương ứng; có structure checker.

Chi tiết sử dụng và quy định tên ở [project_structure.md](project_structure.md).

## Bằng chứng kiểm tra

- Cài editable bằng `pip install -e . --no-deps` thành công; không nâng cấp thư
  viện thuật toán. Build isolation tải setuptools; TEMP ngắn trong repo tránh
  giới hạn đường dẫn Windows.
- Bộ unittest: 33 test, 31 đạt trong sandbox và 2 test junction bị giới hạn quyền.
  Chạy riêng cả 8 test tmp với quyền tạo junction: 8/8 đạt, gồm hai test bị skip.
- Integration test chạy CLI package và `main.py` từ thư mục khác; kiểm tra layout
  mới, resume không đổi primary, chống ghi đè, checksum tamper và preflight reuse
  baseline từ execution envelope. Flat output và alias YAML cũ vẫn hoạt động.
- Smoke thật: ZDT1 28 lượt (7 thuật toán × 4 seed); DTLZ2 M=3 14 lượt;
  WFG4 M=3 14 lượt. Cả ba dùng 2 worker và không có invalid theo validator.
  Sensitivity smoke 12 lượt (3 population levels × 4 seed), cũng với 2 worker,
  hoàn tất trong session riêng. Đây là kiểm tra vận hành, không phải benchmark
  chất lượng hay tái lập toàn bộ số liệu nghiên cứu.
- Kiểm tra bảo toàn: **651 file** ban đầu trong results và scratch giữ nguyên
  đường dẫn và SHA-256. Digest inventory trước/sau giống nhau.
- **22 module solver** có AST hành vi không đổi (bỏ qua import/docstring);
  AST của năm hàm adapter `_run_*` so sánh nguyên vẹn và đều bằng bản trước đổi.
  Xem [validation JSON](structure_migration_validation.json).

## Tương thích và giới hạn có chủ ý

Không di chuyển hoặc xóa dataset, figures, corrections, provenance, archive và
smoke cũ trong results/scratch. [Inventory scratch](legacy_scratch_inventory.json)
chỉ phân loại; mọi mục cũ đều chưa được tự động cấp quyền cleanup. Log cũ ở root
cũng được giữ để không làm mất dấu lịch sử. Công cụ mới ngừng tạo output ở các nơi đó.

Schema/tên CSV giữ nguyên. `--experiment` là lựa chọn cho runner benchmark chung;
sensitivity và legacy runner giữ hợp đồng output riêng. Thư mục figures/qa
của execution dành cho artifact khi được tạo, không tự tạo lại toàn bộ hình.
Recipe hình lịch sử tiếp tục dùng dữ liệu lịch sử.

Source hash/path đã thay đổi; manifest cũ không được sửa hoặc nới kiểm tra.
Resume/reuse execution trước đợt này cần checkout và môi trường cũ phù hợp,
hoặc bắt đầu execution mới. Không chạy benchmark đầy đủ, không chạy lại R figure
generation và không đưa ra kết luận mới về chất lượng thuật toán trong đợt này.

Chưa tạo commit hoặc push. Các thay đổi để trong working tree để xem diff.
