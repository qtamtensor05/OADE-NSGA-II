# Đối chứng bơm đa dạng OBL định kỳ trên OADE

**Ngày phân tích:** 14/11/2026.

**Kết luận:** OBL định kỳ đem lại lợi ích rõ ràng trên ZDT4 trong cấu hình và ngân sách đã thử: cả 30 seed đều tốt hơn khi bật, cho cả IGD và HV, kể cả sau hiệu chỉnh Holm trên 10 endpoint. Trên ZDT1/2/3/6 chưa phát hiện khác biệt chất lượng sau hiệu chỉnh. Nên giữ OBL định kỳ trong cấu hình OADE đang nghiên cứu; không khái quát rằng nó cải thiện trên mọi bài.

## 1. Thiết kế và xác minh

| Thành phần | Thiết lập |
|:---|:---|
| Can thiệp duy nhất | Bật hoặc tắt OBL bổ sung định kỳ |
| Khởi tạo | Cùng uniform, cùng quần thể đầu theo mỗi seed; 100 evaluation |
| Cơ chế chung | Adaptive restart, success-rate, adaptation F/CR, neighborhood |
| Bài toán và seed | ZDT1/2/3/4/6; 30 seed 1000–1029/bài/nhánh |
| Quần thể và ngân sách | 100 cá thể; cap 20.000 evaluation/run, gồm mọi objective calls |
| Tổng dữ liệu | 300 run hợp lệ, 150 cặp seed; không loại run nào |

Đã kiểm tra toàn bộ primary/reference hashes, task set, seed, source hashes và môi trường. Tái tạo quần thể uniform; xác minh 150 cặp có X/F đầu giống nhau; tính lại F từ X và IGD/HV đầu/cuối; đối chiếu 59.017 bước cập nhật xác suất, telemetry OBL/restart, Wilcoxon và Holm. n_eval thực dùng từ 19.901 đến 20.000; không vượt cap.
38 checkpoint từng được khôi phục sau WinError 5 giữ nguyên checksum trong manifest cuối. Có hồ sơ bảo trì riêng cho thay đổi cơ chế ghi checkpoint; thuật toán tìm kiếm không đổi. 150/150 run nhánh bật có X/F cuối khớp nhánh uniform của thí nghiệm khởi tạo trước; đây là bằng chứng tái lập, không được cộng các run đó thành replicate độc lập mới.

## 2. Cơ chế bơm đang đánh giá

OBL được gọi tại chỉ số thế hệ $g=0,10,20,\ldots$. Mỗi cá thể được chọn với xác suất $p_{\mathrm{jump}}=0.2$; điểm phản chiếu dùng bounds quần thể hoặc bounds bài toán với xác suất bằng nhau:

$$
\mathbf{x}^{\prime}=\begin{cases}
\mathbf{x}_{\min}^{\mathrm{pop}}+\mathbf{x}_{\max}^{\mathrm{pop}}-\mathbf{x},&\text{dynamic OBL},\\
\mathbf{x}_{\min}+\mathbf{x}_{\max}-\mathbf{x},&\text{static OBL}.
\end{cases}
$$

Điểm mới được clip vào bounds, đánh giá rồi đưa vào pool chọn lọc. Tắt OBL định kỳ không tắt OBL/Gauss trong adaptive restart. Không dùng Sobol–OBL khởi tạo ở cả hai nhánh.

## 3. Chất lượng cuối theo median

Gọi $\widetilde{M}_{\mathrm{on}}$ và $\widetilde{M}_{\mathrm{off}}$ là median của hai nhánh. Phần trăm cải thiện khi bật OBL:

$$
I_{\mathrm{IGD}}=100\,\frac{\widetilde{\mathrm{IGD}}_{\mathrm{off}}-\widetilde{\mathrm{IGD}}_{\mathrm{on}}}{\widetilde{\mathrm{IGD}}_{\mathrm{off}}},
\qquad
I_{\mathrm{HV}}=100\,\frac{\widetilde{\mathrm{HV}}_{\mathrm{on}}-\widetilde{\mathrm{HV}}_{\mathrm{off}}}{\widetilde{\mathrm{HV}}_{\mathrm{off}}}.
$$

**Dương là tốt hơn khi bật; âm là kém hơn.** Đây là tỷ lệ giữa median hai nhóm, không phải median tỷ lệ từng cặp seed. Đọc cùng kết quả ghép seed và độ dao động.

### IGD ↓

| Bài | Tắt OBL | Bật OBL | Cải thiện (%) | Seed tốt / kém | $p$ Holm (10 endpoint) |
|:---|---:|---:|---:|---:|---:|
| ZDT1 | 0.0043939 | 0.0044769 | -1.888 | 13 / 17 | 0.6872 |
| ZDT2 | 0.0046648 | 0.0047255 | -1.302 | 15 / 15 | 1.0000 |
| ZDT3 | 0.0050115 | 0.0050642 | -1.052 | 14 / 16 | 1.0000 |
| ZDT4 | 0.4001848 | 0.0055402 | +98.616 | 30 / 0 | 0.00001734 |
| ZDT6 | 0.0038767 | 0.0038108 | +1.699 | 18 / 12 | 1.0000 |

### HV ↑

| Bài | Tắt OBL | Bật OBL | Cải thiện (%) | Seed tốt / kém | $p$ Holm (10 endpoint) |
|:---|---:|---:|---:|---:|---:|
| ZDT1 | 0.8709198 | 0.8709181 | -0.000 | 13 / 17 | 1.0000 |
| ZDT2 | 0.5377146 | 0.5377362 | +0.004 | 17 / 13 | 1.0000 |
| ZDT3 | 1.0512146 | 1.0512775 | +0.006 | 18 / 12 | 1.0000 |
| ZDT4 | 0.3400835 | 0.8675027 | +155.085 | 30 / 0 | 0.00001734 |
| ZDT6 | 0.4380203 | 0.4380637 | +0.010 | 18 / 12 | 1.0000 |

Không có cặp bằng nhau trong cả 10 phép so sánh.

## 4. ZDT4: đóng góp rõ ràng của OBL định kỳ

- **IGD median:** 0,4001848 khi tắt → 0,0055402 khi bật; giảm **98,62%**, tương đương thấp hơn khoảng 72 lần.
- **HV median:** 0,3400835 khi tắt → 0,8675027 khi bật; tăng **155,09%** so với nhánh tắt.
- Cả IGD và HV đều tốt hơn ở **30/30 seed**; $p_{\mathrm{raw}}=1.7344\times10^{-6}$ và $p_{\mathrm{Holm}}=1.7344\times10^{-5}$.
- **Mean IGD ± SD:** tắt 0,5444060 ± 0,4674164; bật 0,0192867 ± 0,0412440. Nhánh bật vẫn còn đuôi run chất lượng kém, nhưng thấp hơn rõ về cả mức trung tâm và độ phân tán trong mẫu này.
- Adaptive restart không kích hoạt lần nào trên ZDT4 ở cả hai nhánh. Lợi ích ghi nhận không cần một thay đổi số lần restart để giải thích; đối chứng trực tiếp ủng hộ việc giữ OBL định kỳ trong cấu hình này.
- Chưa đo trực tiếp chỉ số đa dạng quần thể, nên không khẳng định riêng cơ chế tăng diversity là nguyên nhân trung gian duy nhất; bằng chứng hiện có xác định đóng góp tổng của bật OBL định kỳ đối với chất lượng.

## 5. Hiệu ứng ghép seed và bất định

Đơn vị phân tích là cặp run cùng seed/bài, $n=30$. Delta được định nghĩa $\Delta_i=M_{\mathrm{on},i}-M_{\mathrm{off},i}$: IGD âm tốt hơn; HV dương tốt hơn. Wilcoxon signed-rank hai phía, `zero_method="wilcox"`, xấp xỉ chuẩn; Holm được định trước trên cả 10 endpoint (5 bài × 2 chỉ số), $\alpha=0.05$.

CI 95% dưới đây là bootstrap percentile của **mean delta**, 20.000 resample cặp seed, seed base 20261114. CI không hiệu chỉnh đa kiểm định và là phân tích bổ sung; không dùng CI để thay kết luận kiểm định Holm.

| Bài | Chỉ số | Mean $\Delta$ | CI 95% của mean $\Delta$ |
|:---|:---|---:|---:|
| ZDT1 | IGD | +0.00013548 | [+0.00000739; +0.00026800] |
| ZDT1 | HV | -0.00011098 | [-0.00023983; +0.00000641] |
| ZDT2 | IGD | -0.00006717 | [-0.00021863; +0.00007587] |
| ZDT2 | HV | +0.00006510 | [-0.00005872; +0.00019651] |
| ZDT3 | IGD | -0.00002763 | [-0.00018120; +0.00012060] |
| ZDT3 | HV | +0.00001828 | [-0.00006805; +0.00009824] |
| ZDT4 | IGD | -0.52511926 | [-0.70145510; -0.37253907] |
| ZDT4 | HV | +0.51407912 | [+0.42903977; +0.59770745] |
| ZDT6 | IGD | -0.00004320 | [-0.00011639; +0.00003377] |
| ZDT6 | HV | +0.00008851 | [-0.00003199; +0.00021405] |

ZDT1 có mean delta IGD dương với CI bổ sung không chứa 0, nhưng đó là thống kê mean chưa hiệu chỉnh, khác endpoint Wilcoxon. Wilcoxon IGD có p thô 0,0859 và p Holm 0,6872, nên chưa gọi là suy giảm có ý nghĩa theo giao thức chính. Tương tự, không gọi ZDT2 là thắng/thua chỉ từ marginal median vì hướng mean hoặc paired delta có thể khác.
Không phát hiện khác biệt trên ZDT1/2/3/6 không chứng minh tương đương hoặc chứng minh OBL vô ích trên các bài đó. Không cộng số endpoint thắng thành kết luận ưu thế trên mọi bài toán.

## 6. Số lần bơm, chi phí và chọn lọc

| Bài | Lần bơm | Ứng viên / evaluation OBL | Ngân sách dùng cho OBL (%) | Được giữ | Tỷ lệ giữ (%) |
|:---|---:|---:|---:|---:|---:|
| ZDT1 | 600 | 11931 | 1.993 | 1461 | 12.25 |
| ZDT2 | 600 | 12111 | 2.025 | 1873 | 15.47 |
| ZDT3 | 600 | 11936 | 1.994 | 1171 | 9.81 |
| ZDT4 | 600 | 12017 | 2.008 | 4799 | 39.94 |
| ZDT6 | 600 | 12063 | 2.016 | 1034 | 8.57 |

Mỗi run bật có 20 lần gọi OBL; nhánh tắt không có lần gọi, ứng viên hay evaluation OBL định kỳ. Số evaluation bằng số ứng viên được sinh. Chi phí OBL khoảng **2% tổng objective calls**, không phải 20%: kernel chỉ chọn khoảng 20% cá thể sau mỗi 10 thế hệ.
Tỷ lệ giữ ứng viên OBL trên ZDT4 gần **40%**, cao hơn các bài còn lại (khoảng 8,6–15,5%). Đây là bằng chứng ứng viên OBL có tham gia chọn lọc mạnh trên ZDT4; chưa tự chứng minh đóng góp lâu dài của từng cá thể.

## 7. Restart, số thế hệ và runtime

| Bài | Restart: bật / tắt | Số thế hệ hoàn tất trung bình: bật / tắt | Runtime median (s): bật / tắt |
|:---|---:|---:|---:|
| ZDT1 | 0 / 0 | 194.53 / 199.00 | 15.679 / 17.762 |
| ZDT2 | 0 / 0 | 194.37 / 199.00 | 4.242 / 17.278 |
| ZDT3 | 0 / 0 | 194.53 / 199.00 | 4.167 / 17.770 |
| ZDT4 | 0 / 0 | 194.50 / 199.00 | 19.388 / 20.402 |
| ZDT6 | 3 / 4 | 194.43 / 198.87 | 16.576 / 18.239 |

Nhánh bật trả chi phí OBL trong cùng cap nên hoàn tất ít thế hệ hơn, khoảng 194–195 so với 199 khi tắt. Không cấp thêm evaluation để bù; đây là so sánh lợi ích ròng theo ngân sách.
ZDT1–4 không có restart. ZDT6 có 3 attempt khi bật và 4 khi tắt, 23/30 cặp đều không restart. Sai khác này là hệ quả có thể có của quỹ đạo khác nhau; không tách riêng vai trò trung gian restart trong thiết kế hiện tại.
**Không suy ra bật OBL chạy nhanh hơn từ bảng runtime.** Đợt đo đã gián đoạn và tiếp tục sau sửa checkpoint; tốc độ giữa các nhóm task chênh lệch lớn, ví dụ ZDT2/3. Runtime phụ thuộc tải máy, phiên chạy và thứ tự task, chưa phải phép đo overhead được kiểm soát. Source tìm kiếm và môi trường package/thread vẫn được xác minh.

## 8. Quyết định phù hợp với bằng chứng

- **Giữ bật OBL định kỳ** trong cấu hình OADE đang nghiên cứu: có đóng góp lớn và nhất quán trên ZDT4 với chi phí khoảng 2% ngân sách.
- Giới hạn tuyên bố ở ZDT4 và cấu hình đã đo: uniform, adaptive restart, success-rate, population 100, cap 20.000. Chưa có bằng chứng cải thiện chung trên mọi ZDT hoặc các cấu hình khác.
- Không gán kết quả này cho khởi tạo Sobol–OBL: cơ chế đó không tham gia trong cả hai nhánh. Không thay thế bảng benchmark lịch sử hoặc tự suy ra thắng thêm các thuật toán đối chứng khác.
- Dữ liệu hiện tại đủ cho kết luận ablation cục bộ đã nêu; không cần chạy ngay lưới factorial 72 cấu hình chỉ để xác nhận OBL định kỳ có đóng góp trên ZDT4.

## Dữ liệu và truy vết

| Tệp | Nội dung |
|:---|:---|
| [Primary JSON](../../results/experiments/diversity_injection_zdt_v1/primary/) | 300 run, X/F đầu và cuối, trace xác suất, sự kiện OBL/restart |
| [Manifest](../../results/experiments/diversity_injection_zdt_v1/study_manifest.json) | Tham số, source/environment hashes và lịch sử bảo trì checkpoint |
| [Xác minh độc lập](../../results/experiments/diversity_injection_zdt_v1/derived/audit_validation.json) | Toàn vẹn, tái lập và tính lại chỉ số |
| [Thống kê đầy đủ](../../results/experiments/diversity_injection_zdt_v1/derived/audit_summary.csv) | Mean, SD, median, Q25/Q75, chi phí và số thế hệ |
| [Hiệu ứng ghép seed](../../results/experiments/diversity_injection_zdt_v1/derived/audit_effects.csv) | Delta, CI, số seed tốt/kém, p và Holm |
| [Sự kiện OBL](../../results/experiments/diversity_injection_zdt_v1/derived/diversity_events.csv) | Ứng viên, evaluation và số được giữ sau chọn lọc |
| [Hội tụ](../../results/experiments/diversity_injection_zdt_v1/derived/audit_convergence.csv) | Median theo checkpoint và n_eval quan sát thực |

Chỉ làm tròn khi trình bày; primary, manifest và CSV gốc được giữ nguyên. Không chạy lại optimizer trong đợt kiểm tra này.
