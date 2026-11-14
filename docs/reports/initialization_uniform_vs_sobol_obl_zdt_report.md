# Đối chứng khởi tạo Uniform và Sobol–OBL trên OADE

**Ngày phân tích:** 14/11/2026.

**Kết luận:** Sobol–OBL cho IGD ngay sau khởi tạo thấp hơn trên cả 5 bài ZDT, nhưng chưa chứng minh cải thiện chất lượng cuối một cách nhất quán ở cap 20.000 evaluation. ZDT6 có tín hiệu HV tốt hơn trong kiểm định riêng; tín hiệu này không còn đạt ngưỡng 0,05 khi hiệu chỉnh đồng thời 10 endpoint.

## 1. Thiết kế và xác minh

| Thành phần | Thiết lập |
|:---|:---|
| Phương pháp | Uniform và Sobol–OBL (scrambled Sobol + GOBL đang triển khai) |
| Bài toán | ZDT1, ZDT2, ZDT3, ZDT4, ZDT6 |
| Replication | 30 seed ghép cặp 1000–1029/bài; 300 run; không có run invalid |
| Quần thể | 100 cá thể |
| Ngân sách | 20.000 evaluation/run, gồm khởi tạo, OBL định kỳ và restart |
| Cơ chế chung | Adaptive restart, success-rate, adaptation F/CR, neighborhood và OBL định kỳ |
| Chi phí khởi tạo | Uniform: 100; Sobol–OBL: 200 evaluation |

Đã xác minh hash toàn bộ primary JSON/reference snapshot; đủ task và seed; mã nguồn và môi trường khớp manifest. Tái tạo cả 300 quần thể khởi đầu, kiểm tra X/F, tính lại IGD/HV đầu và cuối, kiểm tra 58.194 bước cập nhật xác suất cùng telemetry restart. Ngân sách thực dùng 19.901–20.000, không vượt cap.
150/150 run uniform tái lập đúng X/F cuối của nhánh success-rate trong đợt đối chứng xác suất trước. Đây là kiểm tra tái lập; không cộng các run cũ như replicate độc lập mới.
Hai nhánh ghép theo seed nhưng không có cùng quần thể đầu. RNG khởi tạo tách khỏi RNG tiến hóa. Sobol–OBL được đánh giá như một gói, không tách đóng góp riêng Sobol và GOBL.

## 2. Chất lượng ngay sau khởi tạo

Bảng dùng **median 30 run**. IGD càng thấp càng tốt. Mức giảm là chênh lệch giữa hai median, không phải mức giảm median của từng cặp seed.

| Bài | IGD Uniform ↓ | IGD Sobol–OBL ↓ | Giảm IGD (%) | HV Uniform → Sobol–OBL ↑ |
|:---|---:|---:|---:|---:|
| ZDT1 | 2.321163 | 0.527107 | +77.29 | 0.000000 → 0.197178 |
| ZDT2 | 3.656108 | 0.888747 | +75.69 | 0.000000 → 0.000000 |
| ZDT3 | 2.110507 | 0.531557 | +74.81 | 0.000000 → 0.316373 |
| ZDT4 | 85.811075 | 82.096396 | +4.33 | 0.000000 → 0.000000 |
| ZDT6 | 6.825316 | 3.297490 | +51.69 | 0.000000 → 0.000000 |

IGD đầu thấp hơn trên cả 5 bài theo median; đây là quan sát mô tả, không phải kiểm định mới về chất lượng khởi tạo. Sobol–OBL đã dùng gấp đôi evaluation ở thời điểm này; không diễn giải bảng đầu như so sánh cùng chi phí. HV bằng 0 có thể vì nghiệm đầu nằm ngoài hộp tham chiếu, không đồng nghĩa run lỗi hoặc quần thể sụp đổ.

## 3. Chất lượng cuối tại cùng ngân sách

Gọi $\widetilde{M}_{U}$ và $\widetilde{M}_{S}$ là median của Uniform và Sobol–OBL. Phần trăm cải thiện được trình bày theo chiều tốt hơn:

$$
I_{\mathrm{IGD}}=100\,\frac{\widetilde{\mathrm{IGD}}_U-\widetilde{\mathrm{IGD}}_S}{\widetilde{\mathrm{IGD}}_U},
\qquad
I_{\mathrm{HV}}=100\,\frac{\widetilde{\mathrm{HV}}_S-\widetilde{\mathrm{HV}}_U}{\widetilde{\mathrm{HV}}_U}.
$$

**Dương là cải thiện; âm là suy giảm.** Phần trăm giữa các median có thể khác hướng với thống kê ghép seed hoặc mean; luôn đọc kèm kiểm định và độ dao động.

### IGD ↓

| Bài | Uniform | Sobol–OBL | Cải thiện (%) | Seed tốt / kém | $p$ riêng | $p$ Holm × 10 |
|:---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 0.0044769 | 0.0044690 | +0.177 | 16 / 14 | 0.5857 | 1.0000 |
| ZDT2 | 0.0047255 | 0.0046543 | +1.508 | 15 / 15 | 0.8130 | 1.0000 |
| ZDT3 | 0.0050642 | 0.0050153 | +0.967 | 17 / 13 | 0.5304 | 1.0000 |
| ZDT4 | 0.0055402 | 0.0056375 | -1.756 | 15 / 15 | 0.7655 | 1.0000 |
| ZDT6 | 0.0038108 | 0.0038224 | -0.305 | 15 / 15 | 0.8451 | 1.0000 |

### HV ↑

| Bài | Uniform | Sobol–OBL | Cải thiện (%) | Seed tốt / kém | $p$ riêng | $p$ Holm × 10 |
|:---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 0.8709181 | 0.8709242 | +0.001 | 15 / 15 | 0.5577 | 1.0000 |
| ZDT2 | 0.5377362 | 0.5377180 | -0.003 | 13 / 17 | 0.7499 | 1.0000 |
| ZDT3 | 1.0512775 | 1.0512537 | -0.002 | 16 / 14 | 0.7971 | 1.0000 |
| ZDT4 | 0.8675027 | 0.8673616 | -0.016 | 17 / 13 | 0.8936 | 1.0000 |
| ZDT6 | 0.4380637 | 0.4381861 | +0.028 | 21 / 9 | 0.0300 | 0.3001 |

Không có cặp seed bằng nhau ở cả 10 phép so sánh.

## 4. Kiểm định, hiệu ứng và bất định

Đơn vị phân tích là cặp run cùng seed/bài, $n=30$. Wilcoxon signed-rank hai phía, `zero_method="wilcox"`, xấp xỉ chuẩn. Giao thức gốc hiệu chỉnh Holm giữa các cặp phương án trong từng bài/chỉ số; chỉ có một cặp nên $p_{\mathrm{Holm}}=p_{\mathrm{thô}}$. Bảng bổ sung Holm cho cả 10 endpoint (5 bài × 2 chỉ số) để kiểm tra độ vững của kết luận toàn bộ ZDT; đây là phân tích nhạy bổ sung, không thay đổi hồi tố họ kiểm định gốc.

Đặt $\Delta_i=M_{S,i}-M_{U,i}$: IGD âm tốt hơn, HV dương tốt hơn. CI 95% dưới đây là bootstrap percentile của **mean delta**, 20.000 resample cặp seed, seed base 20261114. CI không hiệu chỉnh đa kiểm định và là phân tích bổ sung sau khi xem kết quả.

| Bài | Chỉ số | Mean $\Delta$ | CI 95% của mean $\Delta$ |
|:---|:---|---:|---:|
| ZDT1 | IGD | -0.00004974 | [-0.00019382; +0.00009108] |
| ZDT1 | HV | +0.00008424 | [-0.00004233; +0.00022209] |
| ZDT2 | IGD | +0.00001881 | [-0.00010328; +0.00014183] |
| ZDT2 | HV | -0.00000521 | [-0.00011723; +0.00011024] |
| ZDT3 | IGD | -0.00005218 | [-0.00019468; +0.00008853] |
| ZDT3 | HV | +0.00001367 | [-0.00006261; +0.00009627] |
| ZDT4 | IGD | +0.01552322 | [-0.01577129; +0.04946470] |
| ZDT4 | HV | -0.02313826 | [-0.07543953; +0.02469225] |
| ZDT6 | IGD | -0.00000427 | [-0.00007795; +0.00006778] |
| ZDT6 | HV | +0.00012463 | [+0.00001524; +0.00023175] |

**ZDT6–HV:** Sobol–OBL tốt hơn ở 21/30 seed, kiểm định riêng có p=0,0300 và CI mean delta không chứa 0. Tuy nhiên, median HV tăng khoảng 0,028% và Holm trên 10 endpoint cho p=0,3001. Có tín hiệu cục bộ; chưa đủ để khẳng định lợi ích chung hoặc mạnh trên ZDT.
**ZDT4:** median IGD mới kém khoảng 1,76%; mean IGD Uniform là 0,0192867 ± SD 0,0412440, Sobol–OBL là 0,0348100 ± SD 0,0777704. Đuôi kết quả kém và độ phân tán lớn hơn cần lưu ý, nhưng p=0,7655 không cho phép gọi đây là suy giảm có ý nghĩa thống kê. Không bỏ các run đuôi để làm đẹp kết quả.
Không phát hiện khác biệt không chứng minh tương đương. Cả IGD/HV đều là chỉ số phụ thuộc bài và reference snapshot; không gộp trị số thô giữa các bài để tạo điểm tổng.

## 5. Hội tụ, restart và thời gian

| Bài | IGD median tại mốc 10% cap: Uniform → Sobol–OBL | Restart tổng: Uniform / Sobol–OBL | Median runtime (s): Uniform → Sobol–OBL |
|:---|---:|---:|---:|
| ZDT1 | 0.042602 → 0.009169 | 0 / 0 | 3.744 → 4.145 |
| ZDT2 | 0.614316 → 0.008822 | 0 / 0 | 3.954 → 4.134 |
| ZDT3 | 0.036357 → 0.045805 | 0 / 0 | 3.906 → 4.084 |
| ZDT4 | 23.845647 → 20.926644 | 0 / 0 | 4.705 → 4.679 |
| ZDT6 | 0.962326 → 0.110934 | 3 / 13 | 4.133 → 3.946 |

Mốc 10% là snapshot tại n_eval thực đầu tiên vượt ngưỡng, không phải mọi run được quan sát chính xác ở 2.000 evaluation; xem audit_convergence.csv. Không nội suy. Lợi thế đầu có thể giảm hoặc đảo chiều cuối run.
ZDT1–4 không có restart ở cả hai nhánh. ZDT6 có 3 attempt ở Uniform và 13 ở Sobol–OBL. Cùng chính sách restart không có nghĩa cùng số lần kích hoạt: đây là tác động hạ nguồn của quần thể/quỹ đạo khác nhau. Không thể tách lợi ích khởi tạo khỏi vai trò trung gian của restart chỉ bằng so sánh hai nhánh này.
Runtime gồm khởi tạo, tìm kiếm và instrumentation, đo với 4 worker trên máy đang dùng. Thứ tự task/tải máy có thể gây nhiễu; không dùng chênh lệch runtime để suy ra độ phức tạp lý thuyết hoặc tốc độ phần cứng độc lập.

## 6. Kết luận áp dụng

- Sobol–OBL có lợi thế chất lượng đầu về IGD trong thiết kế này, nhưng đã trả thêm 100 objective evaluations. Chưa có bằng chứng lợi ích cuối ổn định trên toàn bộ bộ ZDT ở cap 20.000.
- Không nên tuyên bố Sobol–OBL là nguyên nhân tạo ra các kết quả benchmark lịch sử: các benchmark đó khởi tạo uniform. Thí nghiệm này cũng không rerun các thuật toán đối chứng khác.
- Có thể giữ Sobol–OBL như một phương pháp khởi tạo của OADE, nhưng cần trình bày trung thực rằng lợi ích cuối chưa được xác lập. Chọn nó vì định hướng thiết kế khác với tuyên bố đã chứng minh cải thiện.
- Nếu cần xác nhận tín hiệu HV trên ZDT6, dùng seed mới và endpoint xác định trước; không tự tăng thêm seed của chính tập hiện tại cho đến khi p đạt ngưỡng. Không cần mở ngay lưới factorial 72 cấu hình.

## Dữ liệu và truy vết

| Tệp | Nội dung |
|:---|:---|
| [Primary JSON](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/primary/) | 300 run; X/F đầu và cuối, chi phí khởi tạo, trace xác suất, restart |
| [Manifest](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/study_manifest.json) | Cấu hình, nguồn, môi trường và hash dữ liệu |
| [Xác minh độc lập](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/derived/audit_validation.json) | Kết quả kiểm tra toàn vẹn và tính lại chỉ số |
| [Thống kê đầy đủ](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/derived/audit_summary.csv) | Mean, SD, median, Q25/Q75, runtime và restart |
| [Hiệu ứng ghép seed](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/derived/audit_effects.csv) | Delta, CI, p, số seed tốt/kém và Holm 10 endpoint |
| [Hội tụ](../../results/experiments/initialization_uniform_vs_sobol_obl_zdt_v1/derived/audit_convergence.csv) | Chất lượng và ngân sách quan sát thực tại từng checkpoint |

Chỉ làm tròn số khi trình bày. Primary JSON, manifest và CSV gốc được giữ nguyên; không chạy lại optimizer trong đợt phân tích này.
