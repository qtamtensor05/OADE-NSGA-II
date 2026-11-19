# Hai bản triển khai OADE

## Bản chính — một cấu hình thống nhất

Mã nguồn: [`src/oade_nsga2/`](../../src/oade_nsga2/). Cấu hình benchmark: [`config/algorithms/oade_nsga2.yaml`](../../config/algorithms/oade_nsga2.yaml), runner `local_oade`.

Đây là một bản triển khai độc lập, không kế thừa hoặc import thuật toán từ bản research. Không có các công tắc ablation, nhánh classic/no-restart, fixed probability, các tùy chọn khởi tạo khác.

| Thành phần | Cơ chế cố định |
|:---|:---|
| Khởi tạo | Uniform theo seed, như benchmark 7 thuật toán cũ |
| DE/SBX | Kết hợp hai toán tử, xác suất DE ban đầu 0,5 |
| Cập nhật xác suất | **Success-rate** chuẩn hóa theo số trial từng toán tử |
| F/CR | Thích nghi; giá trị đầu 0,65 / 0,5 |
| Thành công của offspring | Không bị trội trong pool cha–con **trước loại trùng**; không dựa vào rank thiếu/stale |
| Neighborhood | 5 láng giềng |
| OBL định kỳ | Mỗi 10 thế hệ, gồm index 0; jump rate 0,2 |
| Restart | Chỉ adaptive; patience 20, tolerance $10^{-4}$, diversity threshold 0,02 |
| Adaptive restart kernel | Giữ ít nhất 80% elite, sinh OBL/Gauss, cập nhật F/CR nhẹ |
| Chọn lọc | Pareto/crowding và loại trùng mục tiêu như bản đã sửa |
| Ngân sách | Mọi objective calls tính vào cap; không bù ngân sách cho OBL/restart |

Các giá trị cơ chế được ghi ở [`configuration.py`](../../src/oade_nsga2/configuration.py). YAML không nhận override; runner từ chối `params` khác rỗng để tránh âm thầm biến bản chính thành một cấu hình nghiên cứu khác. Nếu benchmark truyền quần thể đầu, nó phải khớp uniform theo seed.

Seed, số thế hệ/ngân sách, kích thước quần thể và bài toán là điều khiển **lượt chạy**, không phải các option chọn cơ chế. Benchmark ZDT chuẩn vẫn là population 100, cap 20.000, 30 seed 42–71 trên 5 bài. Các lượt nhỏ chỉ dùng để kiểm tra kỹ thuật.

```python
from oade_nsga2 import OADE_NSGAII, ProblemWrapper

solver = OADE_NSGAII(ProblemWrapper(problem), pop_size=100, n_gen=200, seed=42)
front = solver.run()
```

Ví dụ này chạy theo số thế hệ; để so sánh ở cap objective cố định, dùng pipeline benchmark và runner `local_oade`.

## Bản nghiên cứu — giữ các tùy chọn và instrumentation

Mã nguồn cũ đã chuyển vào [`src/research/oade_nsga2/`](../../src/research/oade_nsga2/), import bằng `research.oade_nsga2`. Runner: `local_oade_research`.

| Nội dung | Vị trí |
|:---|:---|
| Baseline có thể điều chỉnh | [`config/research/oade_nsga2.yaml`](../../config/research/oade_nsga2.yaml) |
| Classic research | [`config/research/oade_classic.yaml`](../../config/research/oade_classic.yaml) |
| Các ablation | [`config/ablations/`](../../config/ablations/) |
| Restart, OBL định kỳ, probability, sensitivity | Các lệnh research hiện tại, đã đổi import/runner sang bản research |

Bản nghiên cứu giữ classic/adaptive/no-restart, khởi tạo uniform, bật/tắt OBL và các adaptation; cùng telemetry restart, diversity, initialization và probability. **Không khôi phục generated-share hoặc lỗi cũ.**

## Các bản sửa lỗi được giữ lại

- Cập nhật F/CR theo quan hệ Pareto trên pool đã đánh giá trước loại trùng; không bỏ DE trial tốt chỉ vì `rank=None`, không dùng rank stale để tính thành công.
- Tỷ lệ thành công DE/SBX được chuẩn hóa theo số trial; giữ xác suất khi thiếu toán tử hoặc cả hai tỷ lệ bằng 0; giới hạn xác suất 0,2–0,8.
- Objective accounting và xử lý batch vượt cap vẫn giữ nguyên.
- Khởi tạo uniform có seed tường minh; RNG riêng có thể được dùng khi gọi initializer trực tiếp.
- Retry ghi checkpoint khi Windows chặn thay file vẫn nằm trong pipeline research.

Kiểm thử đối chiếu bản chính với research cùng cấu hình yêu cầu X/F, n_eval và convergence khớp hoàn toàn trên các run nhỏ; có hồi quy riêng cho lỗi duplicate/stale rank và chuẩn hóa success-rate.

## Phạm vi của các kết quả đã lưu

Việc tách package **không chạy lại benchmark** và không đổi nhãn kết quả lịch sử. Bộ benchmark cũ với 6 đối chứng vẫn thuộc phiên bản đã đo; các ablation mới cũng giữ nguyên JSON, manifest và đường dẫn bộ kết quả. Source hashes trong manifest cũ mô tả layout/mã tại thời điểm chạy, không được sửa để giả vờ bộ dữ liệu được sinh từ package mới.

Do đường dẫn source/runner đã thay đổi, không resume các execution cũ bằng mã mới. Các lượt chạy mới phải dùng thư mục mới. Không tự tái sử dụng block đối chứng lịch sử thiếu chứng nhận source/environment chỉ vì cùng seed.
