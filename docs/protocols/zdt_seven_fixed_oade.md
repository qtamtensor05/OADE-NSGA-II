# Chạy mới 7 thuật toán trên ZDT — OADE bản thống nhất

Pipeline này **chạy mới toàn bộ 7 thuật toán**, không dùng `reuse-baselines`, không ghép kết quả lịch sử. OADE bắt buộc là [`src/oade_nsga2/`](../../src/oade_nsga2/) bản chính, runner `local_oade`, không có override. Bản `research.oade_nsga2` không được phép tham gia như solver đối chứng.

## Thiết kế

| Thành phần | Thiết lập |
|:---|:---|
| Thuật toán | OADE_NSGAII, NSGA2, RNSGA2, DNSGA2, CGDE_NSGAII, NSGAII_SDR_OLS, CE_MOEA |
| Bài toán | ZDT1/2/3: 30 biến; ZDT4/6: 10 biến; đều 2 mục tiêu |
| Population | 100 |
| Ngân sách | 20.000 objective evaluations/run |
| Seed | 42–71, 30 run/thuật toán/bài |
| Tổng | **1.050 run**, tối đa 21 triệu objective evaluations |
| Khởi tạo | Uniform chung theo bài/seed |
| Thứ tự chạy | Xáo thứ tự task bằng seed 20261114; resume xáo các task còn thiếu |

OADE cố định uniform + adaptive restart + OBL định kỳ + success-rate; F/CR ban đầu 0,65/0,5, xác suất DE đầu 0,5, 5 láng giềng, patience 20, tolerance $10^{-4}$, elite ratio 0,8 và diversity threshold 0,02. Giữ các bản sửa lỗi F/CR trên offspring bị loại trùng, stale rank và objective accounting. Tham số đóng băng được chụp vào `protocol.oade_fixed_parameters` trong manifest.

Sáu đối chứng dùng các YAML hiện có trong `config/algorithms/`, được chụp nguyên runner/class/params vào manifest. Đây là các bản triển khai trong repository; xem [registry baseline](baselines.md) về các khác biệt cục bộ. RNSGA2 tính cả objective calls dựng aspiration points; mọi OBL/local search/restart được tính trong cùng cap. Batch nguyên tử có thể để dư; xem `n_eval` thực.

Phiên bản chấm hiện tại là `zdt_seven_fixed_oade_v2`, baseline revision `paper_corrections_2026_11_14`. Pipeline kiểm tra cấu hình CGDE/SDR-OLS/CE-MOEA đã sửa ngay khi lập kế hoạch; từ chối tham số CGDE cũ hoặc cap local search cũ. OADE tiếp tục dùng bản thống nhất. Không ghép dữ liệu v1 vào v2.

## Cách chạy

Từ thư mục repository trong PowerShell:

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"

# Xem kế hoạch; mặc định không chạy optimizer
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage plan

# Chạy chính thức: bạn chủ động chạy
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage run --jobs 4

# Tiếp tục đúng các run còn thiếu
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage run --jobs 4 --resume

# Chỉ tạo lại bảng/báo cáo sau khi đủ dữ liệu
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage report --resume
```

Cấu hình: [`config/suites/zdt_seven_fixed_oade.yaml`](../../config/suites/zdt_seven_fixed_oade.yaml). Output sau sửa baseline: `results/experiments/zdt_seven_fixed_oade_v2/`. Các báo cáo và thư mục benchmark trước sửa đã được gỡ bỏ. Xem [các sửa đổi theo bài báo và giới hạn còn lại](baseline_paper_corrections.md). Không resume kết quả trước sửa bằng mã mới. Có thể đổi số worker; dùng `--out-dir <thư mục mới>` nếu đã có dữ liệu không tương thích. Không sửa source hoặc YAML trong lúc chạy.

Lệnh `-m research` là điểm vào **điều phối thí nghiệm**, không có nghĩa chọn solver nghiên cứu: pipeline kiểm tra và chỉ chấp nhận OADE `local_oade`, không chấp nhận `local_oade_research`, class khác hoặc params ghi đè.

## Checkpoint và dữ liệu

- **Checkpoint từng run**, không đợi hoàn tất cả bài ZDT: một file `primary/*.json` chứa algorithm/bài/seed, resolved settings, X/F cuối, IGD/HV, runtime, validity, n_eval, convergence và hash quần thể đầu/reference.
- Manifest có source/environment hashes, toàn bộ cấu hình đã resolve, reference snapshot và checksum từng JSON. Resume từ chối sai nguồn/cấu hình/môi trường hoặc dữ liệu hỏng.
- Không ghi đè output cũ, không nhập lại CSV hoặc block đối chứng lịch sử. Nếu gián đoạn giữa ghi primary và manifest, giữ nguyên file tạm để kiểm tra/phục hồi; không xóa primary để ép resume.
- Writer có retry hữu hạn cho lỗi Windows tạm chặn thay file manifest.
- `derived/raw_runs.csv`: từng run, kể cả invalid.
- `derived/summary.csv`: mean, SD, median, Q25/Q75 của IGD/HV, runtime và n_eval; số valid/invalid.
- `derived/comparisons.csv`: OADE ghép seed với từng đối chứng, effect size, p và hiệu chỉnh đa kiểm định.
- `derived/convergence.csv`: checkpoint theo ngân sách, có n_eval thực; không nội suy.
- `derived/report.md`: bảng tổng hợp cuối. Số liệu CSV/JSON giữ độ chính xác gốc, chỉ làm tròn khi trình bày.

Không đo telemetry cơ chế chi tiết của bản research trong benchmark này. Trường telemetry của JSON chỉ chứa tổng objective evaluations thực dùng; không bịa số lần restart/OBL cho bản chính.

## Kiểm định và phạm vi kết luận

Đơn vị phân tích là cặp run cùng seed/bài. Chỉ dùng cặp hợp lệ, báo `n_pairs` và số cặp bị loại. IGD giảm tốt; HV tăng tốt. Wilcoxon signed-rank hai phía, `zero_method="wilcox"`, SciPy `method="auto"`; all-zero differences đặt $p=1$. Phiên bản SciPy được chụp trong môi trường.

- `p_adjusted_holm`, `result`: họ **30 so sánh cho từng metric** (5 bài × 6 đối chứng), để đối chiếu cách báo cáo benchmark cũ.
- `p_holm_all_endpoints`, `result_all_endpoints`: họ chung **60 endpoint**, dùng cho kết luận chung toàn bộ nghiên cứu.
- $\alpha=0.05$. Nếu có endpoint không đủ cặp, giữ chúng trong kích thước họ đã định bằng p bảo thủ bằng 1; không dùng invalid để thu nhỏ họ kiểm định.

Không phát hiện khác biệt không chứng minh tương đương. Không suy ra ưu thế trên mọi lớp bài toán hay mọi phiên bản thuật toán cùng tên. Runtime còn phụ thuộc máy/worker/tải máy dù task đã xáo thứ tự. Bộ mới không đổi nhãn kết quả lịch sử và không tự thay các bảng đã công bố trong README trước khi có dữ liệu mới và audit.
