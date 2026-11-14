# Đối chứng khởi tạo Uniform và Sobol–OBL trên OADE

**Chỉ so sánh hai cách khởi tạo**, giữ nguyên OADE với adaptive restart và success-rate. OBL định kỳ, adaptation F/CR, neighborhood, population và tổng ngân sách giống nhau. Không chạy lưới factorial hoặc các thuật toán đối chứng khác trong thí nghiệm này.

| Nhánh | Khởi tạo | Chi phí objective ban đầu |
|:---|:---|---:|
| Uniform | `default_rng(seed).uniform`, đúng cách lấy mẫu của benchmark trước đây | $N$ |
| Sobol–OBL | Scrambled Sobol + GOBL đang triển khai; chọn $N$ từ $2N$ ứng viên bằng Pareto/crowding | $2N$ |

GOBL hiện có sinh điểm đối ứng $\mathbf{x}'=\operatorname{clip}(\mathbf{k}\odot(\mathbf{x}_{\min}+\mathbf{x}_{\max})-\mathbf{x})$, với từng phần tử của $\mathbf{k}$ lấy uniform trên $[0,1]$. Đây là đúng kernel hiện tại, không đổi sang một biến thể OBL khác. Sobol sinh số điểm bằng lũy thừa của 2 rồi lấy $N$ điểm đầu; chỉ các ứng viên đưa vào đánh giá mới tính objective calls.

Cả hai nhánh dùng cùng seed, nhưng cố ý có quần thể khởi đầu khác nhau. Sobol/GOBL có seed tường minh và dùng RNG khởi tạo riêng; RNG tìm kiếm được reset cùng seed, không bị dịch vì Sobol–OBL rút thêm số ngẫu nhiên. Quỹ đạo về sau vẫn có thể phân kỳ. Không tách riêng lợi ích của Sobol và OBL trong đối chứng này.

## Quy mô và cách chạy

5 bài ZDT1/2/3/4/6 × 30 seed 1000–1029 × 2 nhánh = **300 run**. Population $N=100$; cap **20.000 objective evaluations/run**, gồm khởi tạo, OBL định kỳ và restart. Nhánh Sobol–OBL còn ít ngân sách tiến hóa hơn do chi phí khởi tạo; không bù thêm evaluation. Batch nguyên tử có thể để dư, kiểm tra `n_eval` thực tế.

Từ thư mục repository trong PowerShell:

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"

# Xem kế hoạch, không chạy optimizer
.\.venv\Scripts\python.exe -m research compare-initialization --stage plan

# Benchmark chính thức: bạn chủ động chạy
.\.venv\Scripts\python.exe -m research compare-initialization --stage run --jobs 4

# Tiếp tục cùng mã nguồn/cấu hình/môi trường
.\.venv\Scripts\python.exe -m research compare-initialization --stage run --jobs 4 --resume

# Tạo lại báo cáo từ checkpoint hoàn tất
.\.venv\Scripts\python.exe -m research compare-initialization --stage report --resume
```

Cấu hình: `config/studies/initialization_comparison.yaml`. Output: `results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/`. Dùng `--out-dir <thư mục mới>` nếu đã có dữ liệu không tương thích; không sửa mã trong lúc benchmark chạy.

## Kết quả và suy luận

- `primary/*.json`: X/F sau khởi tạo được chọn, seed/hash, chi phí khởi tạo, X/F cuối, trace xác suất, convergence và restart events.
- `derived/summary.csv`: IGD/HV sau khởi tạo và cuối run; mean, SD, median, Q25/Q75; runtime, n_eval, xác suất DE cuối, số restart.
- `derived/comparisons.csv`: cặp uniform–sobol_obl theo từng bài và metric. Delta = uniform − Sobol–OBL; IGD dương hoặc HV âm ủng hộ Sobol–OBL.
- `derived/report.md`: bảng median và cách diễn giải. `raw_runs.csv`, `convergence.csv`, `probability_trace.csv` cung cấp dữ liệu chi tiết.
- Manifest, source/environment hashes và reference snapshot được lưu trước thực thi; resume từ chối sai cấu hình, đổi mã, thiếu hoặc hỏng checkpoint.

Đơn vị phân tích: cặp run cùng seed/bài, $n=30$. Wilcoxon signed-rank hai phía, bỏ zero, xấp xỉ chuẩn; toàn delta zero đặt $p=1$. Holm theo cặp/bài/metric, chỉ một cặp nên $p$ hiệu chỉnh bằng $p$ thô, $\alpha=0.05$. Run invalid được giữ lại và đếm nhưng loại khỏi cặp chất lượng. Không phát hiện khác biệt không chứng minh tương đương; nếu khẳng định chung qua 10 endpoint, cần xem thêm hiệu chỉnh đa kiểm định.

Chỉ kết luận lợi ích từ chất lượng **cuối run ở cùng cap** cùng độ dao động và kiểm định. Chất lượng ban đầu tốt hơn chưa bảo đảm cải thiện cuối. Runtime bao gồm khởi tạo và instrumentation, phụ thuộc số worker/tải máy. Tác động hạ nguồn qua restart hoặc success-rate là một phần của hiệu quả thay đổi khởi tạo, không phải các cơ chế được thay đổi thêm trong thiết kế.
