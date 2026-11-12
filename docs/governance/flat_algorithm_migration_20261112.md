# Điều chỉnh: mỗi thuật toán một thư mục trong src

Ngày: 2026-11-12. Điều chỉnh theo yêu cầu tác giả sau đợt chuyển đổi đầu.
Cấu trúc hiện hành ở [project_structure.md](project_structure.md).

## Ranh giới đã triển khai

```text
src/
├── oade_nsga2/
├── nsga2/
├── rnsga2/
├── dnsga2/
├── cgde_nsga2/
├── nsga2_sdr_ols/
├── ce_moea/
├── shared/
└── research/
```

Mỗi thư mục thuật toán chỉ chứa mã nguồn thuật toán và luồng gọi riêng:
kernel, operators, selection, runner, và legacy invocation nếu có. Không chứa
benchmark, tính IGD/HV, tổng hợp thống kê, plotting, CLI hoặc công cụ dọn tmp.
README của ba baseline chuyển sang docs/protocols/algorithms.

`nsga2/runner.py`, `dnsga2/runner.py`, `rnsga2/runner.py` chọn lớp pymoo cụ thể
và xử lý setup riêng. RNSGA2 sở hữu aspiration points và warning policy.
`shared/pymoo_execution.py` chỉ tái sử dụng budget, sampling, callback và cách
gọi minimize; không chọn thuật toán cụ thể và không tính metric. Các hàm gọi
generation-based lịch sử cũng được chuyển vào thư mục thuật toán tương ứng.

`shared/` sở hữu contracts, budget/validation, quần thể, Pareto helpers, đường
dẫn, artifact routing và YAML/CSV. Không import research. `research/` sở hữu
orchestration, convergence metric, statistics, provenance, persistence, studies,
plotting, QA, maintenance và CLI. Benchmark adapter module chỉ còn registry/router.

Structure checker kiểm tra thêm ranh giới import trên toàn bộ src: thuật toán
và shared không phụ thuộc research; thuật toán không import kernel thuật toán
khác; lớp solver cụ thể của pymoo phải được chọn trong package thuật toán.

## Kiểm chứng

- Cài lại editable thành công; `oade` trỏ đến `research.cli:main`. `main.py` và
  tên lệnh cũ giữ nguyên; module CLI mới là `python -m research`.
- **35/35 unittest đạt**, không skip, gồm kiểm tra ranh giới source, junction,
  budget, provenance, resume/reuse, layout mới/cũ và CLI ngoài checkout.
- Smoke qua `main.py`, đường dẫn config alias cũ và 2 worker: 28 lượt ZDT1
  đủ 7 thuật toán × 4 seed, không invalid theo validator.
- Đối chiếu adapter trước/sau trên ZDT1, DTLZ2 M=3 và WFG4 M=3: **21/21**
  trường hợp bằng nhau về X, F, số evaluation và toàn bộ convergence metrics.
  Mỗi thuật toán dùng pop=20, budget=400, seed=42; hai phía dùng cùng reference
  front. Runtime không thuộc tiêu chí bằng nhau. Đây là kiểm tra ở quy mô smoke,
  không chứng minh mọi cấu hình hoặc tái lập benchmark đầy đủ.
- **651 file** lịch sử trong results/scratch giữ nguyên đường dẫn và SHA-256.
  Chi tiết trong [validation JSON](flat_algorithm_validation.json).

Không sửa manifest lịch sử hoặc nới kiểm tra source hash. Source đã di chuyển
giữa các package nên resume execution cũ vẫn cần checkout/môi trường tương ứng.
Không chạy benchmark lớn, không tạo lại hình nghiên cứu, không commit/push.

Script chuyển đổi và log kiểm tra nằm trong session one_off có metadata, được
đánh dấu disposable sau khi đóng; báo cáo và validation JSON được giữ trong Git.
