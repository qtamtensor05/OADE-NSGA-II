# Đối chứng không restart, classic và adaptive

Tổng run: **450**; invalid: **0**.
Đối chứng ghép seed trên ZDT.

Cả ba nhánh dùng cùng uniform initial population, success-rate, OBL định kỳ, adaptation F/CR và neighborhood. Chỉ thay toàn bộ chính sách restart.

| Bài | Nhánh | Valid/run | IGD median ↓ | HV median ↑ | Restart bắt đầu / hoàn tất | Evaluation restart |
|:---|:---|---:|---:|---:|---:|---:|
| zdt1 | classic | 30 / 30 | 0.00518739 | 0.870165 | 208 / 208 | 14560 |
| zdt1 | adaptive | 30 / 30 | 0.00447689 | 0.870918 | 0 / 0 | 0 |
| zdt1 | no_restart | 30 / 30 | 0.00447689 | 0.870918 | 0 / 0 | 0 |
| zdt2 | classic | 30 / 30 | 0.00545091 | 0.536321 | 166 / 164 | 11480 |
| zdt2 | adaptive | 30 / 30 | 0.00472555 | 0.537736 | 0 / 0 | 0 |
| zdt2 | no_restart | 30 / 30 | 0.00472555 | 0.537736 | 0 / 0 | 0 |
| zdt3 | classic | 30 / 30 | 0.00553693 | 1.05113 | 180 / 177 | 12390 |
| zdt3 | adaptive | 30 / 30 | 0.00506424 | 1.05128 | 0 / 0 | 0 |
| zdt3 | no_restart | 30 / 30 | 0.00506424 | 1.05128 | 0 / 0 | 0 |
| zdt4 | classic | 30 / 30 | 0.00554021 | 0.867503 | 3 / 3 | 210 |
| zdt4 | adaptive | 30 / 30 | 0.00554021 | 0.867503 | 0 / 0 | 0 |
| zdt4 | no_restart | 30 / 30 | 0.00554021 | 0.867503 | 0 / 0 | 0 |
| zdt6 | classic | 30 / 30 | 0.00405168 | 0.437787 | 92 / 92 | 6440 |
| zdt6 | adaptive | 30 / 30 | 0.00381081 | 0.438064 | 3 / 3 | 60 |
| zdt6 | no_restart | 30 / 30 | 0.00381081 | 0.438064 | 0 / 0 | 0 |

## Các chính sách được đo

| Nhánh | Điều kiện kích hoạt | Cách làm mới |
|:---|:---|:---|
| Không restart | Không kích hoạt | Chỉ theo dõi stagnation, không tốn RNG/evaluation restart |
| Classic | Đủ patience stagnation | Giữ 30% elite, sinh uniform phần còn lại, reset F/CR về 0,5 |
| Adaptive | Đủ patience và diversity collapse | Giữ ít nhất 80% elite, sinh OBL/Gauss, kéo F/CR về 0,5 |

Theo mã hiện có, stagnation đo độ lớn thay đổi ideal point giữa hai thế hệ (chuẩn Euclid), không phải điều kiện cải thiện đơn điệu từng mục tiêu. Nếu thay đổi dưới tolerance thì tăng counter; đủ patience mới xét restart. Adaptive coi collapse khi objective range lớn nhất < 0,001 hoặc max std của biến quyết định chuẩn hóa < diversity_threshold. Nếu diversity khỏe, counter giảm về patience//2, không restart.
## Đọc đối chứng

comparisons.csv chứa đủ classic–adaptive, classic–no_restart và adaptive–no_restart; delta = a − b. IGD thấp hơn tốt, HV cao hơn tốt. Wilcoxon signed-rank hai phía, zero_method=wilcox, xấp xỉ chuẩn; toàn delta zero đặt p=1. Cột p_holm giữ họ ba cặp/bài/metric; p_holm_all_endpoints hiệu chỉnh đồng thời mọi bài × 2 metric × 3 cặp (30 endpoint khi chạy đủ ZDT), alpha=0,05. Invalid được giữ và đếm, loại riêng khỏi cặp chất lượng. Không phát hiện khác biệt không chứng minh tương đương.
summary.csv ghi số lần đủ stagnation, số xét collapse/dương tính/từ chối do diversity khỏe, số run có restart, tần suất, chi phí và chất lượng mean/SD/median/Q25/Q75. restart_events.csv ghi generation, evaluations trước/sau, trạng thái và IGD/HV tức thời trước/sau restart.
Nếu adaptive không trigger và trùng no-restart, không có bằng chứng về lợi ích của restart đã kích hoạt. Classic kém no-restart không tự chứng minh adaptive chủ động cải thiện. Đây là đối chứng toàn bộ chính sách restart, không tách riêng gate, elite ratio, kernel và F/CR reset.
Cùng cap tổng, gồm khởi tạo, OBL định kỳ và restart; batch nguyên tử có thể để dư nên phải xem n_eval. Convergence dùng mốc observation thực, không nội suy. Tác động trước/sau event chỉ là mô tả tức thời, chưa chứng minh lợi ích cuối.
Primary JSON lưu X/F đầu và cuối, hash quần thể đầu, các event và probability trace. Manifest chụp source/environment/reference và kiểm tra resume; writer có bounded retry cho lỗi Windows tạm thời. Giữ dữ liệu nếu lỗi checkpoint kéo dài, không xóa primary để ép resume.
