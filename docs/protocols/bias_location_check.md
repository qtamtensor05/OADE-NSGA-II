# Kiểm tra thiên lệch theo vị trí nghiệm tối ưu

Ngày thiết lập: 27/11/2026. Nghiên cứu này kiểm tra liệu ưu thế của OADE trên ZDT có phụ thuộc vào vị trí đặc biệt của nghiệm tối ưu (nằm trên biên hoặc ở tâm miền) hay không. Không sửa solver production. [Báo cáo kết quả](../reports/bias_location_check_report.md).

## Giả thuyết

Các giả thuyết được đặt ra sau khi đọc mã nguồn OADE:

| Mã | Giả thuyết | Cơ sở trong mã |
|---|---|---|
| H-OBL | OBL có lợi trên ZDT4 chủ yếu vì nghiệm tối ưu nằm ở tâm miền | Trên ZDT4, x₂..x₁₀ ∈ [−5, 5] và nghiệm tối ưu bằng 0. Phản chiếu tĩnh x' = xl + xu − x = −x biến điểm gần tối ưu thành điểm gần tối ưu ([operators.py](../../src/oade_nsga2/operators.py), `generate_obl_offspring`) |
| H-CLIP | Sửa biên bằng clip có lợi nhân tạo khi nghiệm tối ưu nằm trên biên | DE trial được `np.clip` về miền; ZDT1/2/3/6 có nghiệm tối ưu x₂..xₙ = 0, đúng biên dưới (`de_mutation`) |
| H-LOC | Ưu thế của OADE so với NSGA-II thay đổi khi dời nghiệm tối ưu vào trong miền | Hệ quả chung của hai giả thuyết trên |

## Bài toán dịch chuyển

Biến x₁ giữ nguyên; các biến còn lại được biến đổi trước khi đưa vào hàm ZDT gốc. Cận biến, hàm mục tiêu và Pareto front không đổi, nên IGD/HV dùng chung tham chiếu với bài gốc.

| Bài | Biến đổi (i ≥ 2) | Vectơ dịch chuyển |
|---|---|---|
| ZDT4 | z_i = x_i − o_i | o_i ~ U(−2,5; 2,5) |
| ZDT1/2/3/6 | z_i = \|x_i − o_i\| | o_i ~ U(0,2; 0,8) |

Nghiệm tối ưu mới là x_i = o_i, nằm bên trong miền. Script kiểm tra rằng nghiệm tối ưu mới tái tạo đúng Pareto front chuẩn trước khi chạy. Với ZDT1/2/3/6, phép trị tuyệt đối tạo một điểm gãy tại nghiệm tối ưu; ZDT4 là phép dịch thuần túy.

## Các nhánh thuật toán

| Nhánh | Khác với OADE production |
|---|---|
| `OADE` | Không khác; solver `src/oade_nsga2` nguyên bản |
| `OADE_random` | Gene vượt biên của DE trial được lấy lại ngẫu nhiên đều trên toàn miền (không kéo về biên) |
| `OADE_bounce` | Gene vượt biên được đặt ngẫu nhiên giữa biên bị vượt và gene của cá thể đích (vẫn kéo về biên khi quần thể đã gần biên) |
| `OADE_noOBL` | Tắt OBL định kỳ |
| `NSGA2` | pymoo NSGA-II mặc định, dùng chung quần thể khởi tạo uniform theo seed |

Các nhánh repair giữ nguyên thứ tự tiêu thụ số ngẫu nhiên của production, chỉ thêm lượt rút khi có gene vượt biên. Mọi nhánh dùng quần thể 100, ngân sách 20.000 FE/lượt qua `BudgetedProblem`, 10 worker, OMP/OPENBLAS/MKL = 1 luồng.

## Hai vòng chạy

| Vòng | Vai trò | Seed | Bài | Dịch chuyển | Nhánh | Lượt |
|---|---|---|---|---|---|---:|
| [Thăm dò](../../results/experiments/bias_location_exploratory_v1/manifest.json) | Phát hiện | 9000–9029 | ZDT1/4/6 | 1 vectơ (RNG 12345) | OADE, bounce, noOBL, NSGA2 | 720 |
| [Xác nhận](../../results/experiments/bias_location_confirm_v1/manifest.json) | Xác nhận, giả thuyết và họ kiểm định cố định trước khi chạy | 9100–9129 (mới) | ZDT1/2/3/4/6 | 3 vectơ (RNG 12345, 2024, 777) | Thêm `OADE_random` | 3.000 |

Vòng xác nhận không dùng lại dữ liệu nào của vòng thăm dò.

## Thống kê

- **Ghép cặp:** Wilcoxon signed-rank hai phía theo seed, `zero_method=wilcox`, alpha = 0,05. Vòng xác nhận: 4 nhánh × 5 bài × 4 phiên bản × IGD/HV = **160 endpoint**, một họ Holm.
- **Tương tác:** Mann–Whitney hai phía trên log tỷ lệ IGD(nhánh)/IGD(OADE) theo seed, so bài gốc với từng vectơ dịch chuyển. Vòng xác nhận: 4 nhánh × 5 bài × 3 vectơ = **60 kiểm định**, một họ Holm.
- **Mô tả:** số lượt ZDT4 có IGD > 10⁻² (kẹt ở front cục bộ).

## Chạy lại

```powershell
.\.venv\Scripts\python.exe analysis/bias_location_confirm.py --stage smoke --jobs 10
.\.venv\Scripts\python.exe analysis/bias_location_confirm.py --stage run --jobs 10
.\.venv\Scripts\python.exe analysis/bias_location_confirm.py --stage report
```

`--stage run` bỏ qua các lượt đã có trong `runs.jsonl`. Muốn lặp lại độc lập, đổi `SEEDS` và `OUT` sang thư mục mới. Smoke ghi vào `tmp/smoke/`. Vòng thăm dò dùng `analysis/bias_location_exploratory.py` với cùng các stage.

Manifest ghi hash mã OADE và `shared/` tại thời điểm chạy (commit `b320ea4`, `src/` không có thay đổi chưa commit), phiên bản môi trường và hash dữ liệu. Bản script trong `analysis/` chỉ khác bản đã chạy ở đường dẫn ROOT/OUT, dòng hướng dẫn, đường dẫn smoke và phần sửa mã hóa stdout; mã solver, bài toán và thống kê giữ nguyên.
