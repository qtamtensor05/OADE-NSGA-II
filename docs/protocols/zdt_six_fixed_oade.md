# Bộ đối chứng ZDT mới: OADE và năm baseline

Ngày thiết lập: 19/11/2026. Thay nhóm so sánh chính bằng **OADE_NSGAII, NSGA2, DNSGA2, CGDE_NSGAII, GDE3, NSDE**. CE-MOEA, R-NSGA-II và SDR-OLS không còn trong bộ mới. Giữ mã/config legacy và dữ liệu lịch sử để truy xuất; không dùng các run cũ làm kết quả của bộ mới. Không sửa solver OADE hoặc CGDE đã xây dựng.

## Thiết kế khóa trước khi chạy

| Thành phần | Cấu hình |
|---|---|
| Bài toán | ZDT1/2/3: D=30; ZDT4/6: D=10; mọi bài M=2 |
| Quần thể | 100 |
| Ngân sách | Tối đa 20.000 đánh giá mục tiêu/lượt, tính mọi đánh giá nội bộ |
| Seed | 42–71, 30 lượt/thuật toán/bài |
| Tổng | 6 × 5 × 30 = **900 lượt**, tối đa 18 triệu FE |
| Đối chứng thống kê | OADE so với 5 baseline × 5 bài × IGD/HV = **50 endpoint** |
| Worker mặc định | 8 process; có `--jobs` |
| Output mới | `results/experiments/zdt_six_fixed_oade_v1/` |

Mỗi thuật toán nhận cùng quần thể uniform theo bài/seed, kiểm hash input; GDE3/NSDE không dùng LHS mặc định. Tất cả đánh giá đi qua hard-cap wrapper. Batch nguyên tử có thể để dư FE; đọc `n_eval` thực. Giữ final X/F, reference snapshot, checksum primary, source/environment và convergence theo n_eval thực. Không suy luận AUC từ checkpoint target chưa được đo đúng thời điểm.

## Hai baseline từ pymoo

Yêu cầu pymoo >=0.6.2,<0.7; máy triển khai đang dùng 0.6.2. Dùng trực tiếp implementation thư viện, chỉ thêm wrapper tích hợp budget/sampling/checkpoint:

| Baseline | Class | Cấu hình cố định |
|---|---|---|
| GDE3 | `pymoo.algorithms.moo.gde3.GDE3` | DE/rand/1/bin, F=0,5, CR=0,5, gamma=10⁻⁴, bounce-back repair |
| NSDE | `pymoo.algorithms.moo.nsde.NSDE` | Cùng thông số DE và repair |

Cả hai giữ survival RankAndCrowding mặc định của phiên bản thư viện; không tự chuyển sang pruning crowding, MNN/2NN hoặc điều chỉnh tham số sau khi xem kết quả. Đây là các cấu hình benchmark cụ thể, không tuyên bố là cấu hình tối ưu của từng phương pháp. NSDE kết hợp DE với sorting/survival NSGA-II. GDE3 có cạnh tranh cha–con trước khi cắt pool, nên không phải hai tên cho cùng thuật toán. [GDE3](https://pymoo.org/algorithms/moo/gde3.html) · [NSDE](https://pymoo.org/algorithms/moo/nsde.html).

NSGA-II và D-NSGA-II dùng class pymoo đang có; CGDE giữ implementation đã sửa theo paper và các giả định tái dựng đã ghi. D-NSGA-II vẫn được đo trên bài tĩnh; không diễn giải kết quả thành hiệu quả phản ứng môi trường động. Mã CE/R-NSGA-II/SDR-OLS còn để phục vụ kết quả legacy, không có tên nào được chọn bởi thiết kế mới.

## Lệnh chạy

Từ gốc repository:

```powershell
# Chỉ xem kế hoạch; không chạy solver, không tạo kết quả.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage plan --jobs 8

# Môi trường luồng được ghi vào manifest và phải giữ khi resume.
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"

# Chạy chính thức: fresh output, không tái dùng primary bộ cũ.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage run --jobs 8

# Tiếp tục cùng cấu hình/source/environment và output.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage run --jobs 8 --resume

# Tạo lại bảng từ bộ hoàn tất, không chạy task còn thiếu.
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage report --resume
```

`--config` và `--out-dir` hỗ trợ một lần chạy mới ở thư mục riêng. Không dùng `benchmark-zdt-seven` để chạy thiết kế mới. Không chạy đồng thời hai lệnh ghi vào cùng thư mục. Checkpoint dùng file tạm và retry khi Windows tạm khóa replace; checksum/source/environment khác hoặc primary orphan sẽ bị từ chối để kiểm tra, không tự bỏ qua bảo vệ dữ liệu.

Smoke 60 lượt nhỏ để kiểm tra đủ sáu solver trên đủ năm bài; không dùng làm bằng chứng hiệu năng:

```powershell
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --config config/smoke/smoke_zdt_six.yaml --stage run --jobs 2
```

## Kết quả và quy tắc diễn giải

`derived/report.md` tự tạo hai bảng **IGD** và **HV**, hàng là bài, cột là thuật toán, mỗi ô `mean (best run)` dạng e, không kèm SD/Valid/Runtime. Best-run là IGD min hoặc HV max trên run hợp lệ, có thể thuộc seed khác nhau; in đậm mean và best riêng theo số chưa làm tròn. CSV vẫn giữ mean/SD/median/min/max, runtime, FE và số run hợp lệ/invalid.

Wilcoxon signed-rank hai phía theo cặp seed, zero_method=wilcox, method=auto; all-zero p=1. **Holm chung 50 endpoint**, alpha=0,05. Loại cặp invalid và báo n; endpoint không còn cặp vẫn giữ p=1 trong họ và nhãn `no_valid_pairs`. Không phát hiện khác biệt không chứng minh tương đương. Không ghép 60 endpoint của bộ cũ với 50 endpoint mới hoặc cập nhật kết luận 56/60 bằng cách chỉ bỏ cột.

Các bộ 480 lượt ablation và 2.100 lượt đo tham số OADE vẫn là bằng chứng riêng: không bị xóa và không dùng để điền kết quả baseline mới. Kết luận chính thức sau khi hoàn tất và kiểm chứng dữ liệu được liên kết ở phần dưới. Việc giảm chi phí tái dựng không bảo đảm tăng tốc runtime; cần đo trong điều kiện thực thi đã ghi.

## Kết quả hoàn tất — 19/11/2026

900/900 lượt đã hoàn tất; 899 hợp lệ. Sau Holm chung 50 endpoint: 44 có lợi cho OADE, 6 chưa phát hiện khác biệt. Một lượt CGDE–ZDT4 seed 63 suy biến. [Báo cáo, bảng IGD/HV, hình và kiểm chứng](../reports/zdt_six_fixed_oade_report.md). Thiết kế và nguồn primary giữ nguyên.
