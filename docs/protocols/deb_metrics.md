# Bổ sung Υ và Δ vào so sánh thuật toán

## Kiến trúc đã khảo sát

Các solver được chọn qua `AlgorithmSpec`, `runner.load_algorithm_specs` và `adapters.run_algorithm`. Hai pipeline `zdt_six` và `zdt_seven` dùng chung `zdt_seven.run_task`; mỗi run lưu `final_x`, `final_f`, seed, runtime, n_eval và validation trong primary JSON. `zdt_sensitivity` quản lý manifest, checksum, resume và danh sách task; số run mặc định trong cấu hình suite là 30. Vì thế các chỉ số bổ sung được tính từ objective vectors đã lưu tại bước báo cáo, không cần sửa solver hoặc chạy lại thí nghiệm.

## Định nghĩa và quy ước

Nguồn: Deb et al. (2002), mục IV.B, DOI https://doi.org/10.1109/4235.996017.

- Υ là trung bình khoảng cách Euclidean từ từng nghiệm nondominated cuối đến điểm gần nhất trong tập tham chiếu H=500. Đây là hướng obtained → reference, khác IGD. Khoảng cách tính trên objective gốc, không chuẩn hóa.
- Δ dùng khoảng cách hai biên đến extreme thật, cộng tổng sai lệch tuyệt đối của khoảng cách liên tiếp so với trung bình, chia cho khoảng cách biên cộng tổng khoảng cách liên tiếp. Sắp tăng theo f1, phá hòa theo f2, chỉ áp dụng cho hai mục tiêu minimization.
- Lọc dominated; giữ duplicates trong multiset đầu ra để phản ánh khoảng cách bằng 0. Với tập rỗng: cả hai N/A. Một nghiệm: Υ vẫn tính, Δ N/A. Tất cả nghiệm trùng: Δ N/A do không có phân bố khoảng cách có ý nghĩa.
- Mỗi metric có số run hợp lệ riêng. Run invalid không được sử dụng. Phương sai dân số dùng `ddof=0`, mẫu số R, đúng yêu cầu. Không gộp nghiệm từ nhiều run để tính Mean/Variance.
- Generations để N/A khi primary không ghi; không suy ra generations từ budget, vì các solver có thể đánh giá số nghiệm khác nhau trong một vòng. Luôn xuất n_eval và budget thật.

## True fronts và giới hạn

Provider hiện được kiểm tra cho ZDT1/2/3/4/6 hai mục tiêu, các benchmark của hai suite hiện tại. Dùng công thức giải tích: f2=1-sqrt(f1) với ZDT1/4, 1-f1² với ZDT2/6, và 1-sqrt(f1)-f1 sin(10πf1) với ZDT3. Biên dưới ZDT6 được tối thiểu hóa trên thùy đầu của hàm f1 thật. ZDT3 dùng năm khoảng Pareto đã biết với endpoint chính xác khoảng 10 chữ số.

Tham chiếu có đúng 500 điểm, xấp xỉ đều theo độ dài cung trong không gian mục tiêu bằng lưới giải tích dày 100001 điểm mỗi đoạn và nội suy theo độ dài cung. Phân bổ điểm theo chiều dài từng đoạn, giữ các endpoint; không nối khoảng trống ZDT3. Đây là xấp xỉ số công khai, không phải bộ điểm gốc của bài báo. Δ vẫn bao gồm khoảng cách qua các đoạn rời trong tập thu được theo công thức gốc; cần thận trọng diễn giải trên ZDT3.

Không tự nhận hỗ trợ SCH/FON/POL/KUR, DTLZ/WFG hoặc front tùy ý: provider chưa kiểm chứng sẽ báo N/A cùng lý do. Không thêm hàng thuật toán binary hay benchmark chưa có vào suite. Các bảng phản ánh đúng solver và bài thực tế.

## Chạy và xuất báo cáo

Tính từ một study đầy đủ đã có (kiểm tra checksum primary và tính đầy đủ của task trước khi xuất):

```powershell
.venv/Scripts/python.exe -m research report-deb-metrics --study results/experiments/zdt_six_fixed_oade_v1
```

Lệnh riêng này dùng manifest gốc, không yêu cầu source hiện tại trùng hash source của run lịch sử. Các lệnh resume benchmark hiện có vẫn giữ kiểm tra source nghiêm ngặt; không sửa manifest cũ để vượt kiểm tra.

Run mới: dùng `benchmark-zdt-six --config config/suites/zdt_six_fixed_oade.yaml --stage run` với thư mục output mới; điều chỉnh `global.runs` và `seed_base` trong cấu hình. Hai pipeline six/seven tự sinh thêm thư mục `derived/deb_metrics` khi xuất kết quả.

Output gồm `convergence_metric_results.csv`, `diversity_metric_results.csv`, `detailed_run_results.csv`, `experimental_results.xlsx` (hai bảng và run chi tiết), hai file `.tex` kiểu `table*`, `deb_metrics.md`, và `deb_reference_fronts.json` lưu toàn bộ reference, extremes và hash. XLSX được xuất trực tiếp bằng OOXML trong CLI Python, không cần dependency Excel bổ sung.

Kiểm thử: `.venv/Scripts/python.exe -m unittest tests.unit.test_deb_metrics`. Bao gồm ví dụ tính tay, hướng khoảng cách, dominated, empty/singleton/duplicates, reference deterministic, Mean/Variance theo run và XML workbook. Khả năng tái lập solver dùng các kiểm thử seed hiện có; bước metric hoàn toàn deterministic, không tiêu thụ RNG.
