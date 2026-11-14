# Đối chứng generated-share và success-rate trên ZDT

Ngày phân tích: 14/11/2026.

**Ghi chú phiên bản:** Sau phân tích, tác giả quyết định loại generated_share và chọn success_rate làm mặc định. Khuyến nghị thống kê bên dưới phản ánh thời điểm phân tích; dữ liệu, phép đo và kết luận chưa phát hiện khác biệt không đổi. Đây là quyết định thiết kế, không phải bằng chứng mới về cải thiện.

**Kết luận:** chưa có bằng chứng thống kê rằng success-rate cải thiện IGD/HV so với generated-share trên thiết kế này. Có tín hiệu mô tả tốt hơn ở ZDT4, nhưng chưa đủ để thay mặc định.

## Công thức cập nhật xác suất DE

Hai phương pháp dưới đây là các phương pháp đã tạo ra **300 run đối chứng**. Mã hiện tại chỉ hỗ trợ **success-rate** (mặc định) và **fixed**. Công thức generated-share được lưu ở đây để giải thích kết quả lịch sử.

### Ký hiệu

| Ký hiệu | Ý nghĩa tại thế hệ $t$ |
|:---|:---|
| $p_t$ | Xác suất chọn DE; xác suất chọn SBX là $1-p_t$ |
| $n_{\mathrm{DE},t}$, $n_{\mathrm{SBX},t}$ | Số offspring được sinh bằng từng toán tử |
| $s_{\mathrm{DE},t}$, $s_{\mathrm{SBX},t}$ | Số offspring thành công của từng toán tử |
| $r_{\mathrm{DE},t}$, $r_{\mathrm{SBX},t}$ | Tỷ lệ thành công của từng toán tử |
| $q_t$ | Xác suất mục tiêu dùng để cập nhật $p_t$ |
| $\alpha=0.1$ | Hệ số cập nhật; giữ trọng số $0.9$ cho xác suất hiện tại |

**Thành công** ở đây nghĩa là offspring không bị trội trong toàn bộ pool cha–con đã đánh giá, **trước khi loại trùng**. Không đồng nghĩa với việc sống sót sau chọn lọc crowding hoặc tốt hơn cha của chính nó.

### 1. Generated-share — phương án lịch sử

Xác suất mục tiêu chỉ phụ thuộc vào tỷ lệ DE được sinh:

$$
q_t^{\mathrm{gen}}
=\frac{n_{\mathrm{DE},t}}
       {n_{\mathrm{DE},t}+n_{\mathrm{SBX},t}}.
$$

Công thức này **không sử dụng chất lượng offspring**.

### 2. Success-rate — phương án hiện tại

Chuẩn hóa số thành công theo số lần thử của từng toán tử:

$$
r_{\mathrm{DE},t}
=\frac{s_{\mathrm{DE},t}}{n_{\mathrm{DE},t}},
\qquad
r_{\mathrm{SBX},t}
=\frac{s_{\mathrm{SBX},t}}{n_{\mathrm{SBX},t}}.
$$

Xác suất mục tiêu được tính từ hai tỷ lệ thành công:

$$
q_t^{\mathrm{succ}}
=\frac{r_{\mathrm{DE},t}}
       {r_{\mathrm{DE},t}+r_{\mathrm{SBX},t}}.
$$

**Trường hợp thiếu bằng chứng:** nếu một toán tử chưa được thử, hoặc cả hai tỷ lệ thành công đều bằng $0$, giữ nguyên $p_{t+1}=p_t$.

### Quy tắc cập nhật chung

Khi xác suất mục tiêu được xác định, hai phương pháp đều dùng:

$$
p_{t+1}
=\min\!\left\{0.8,\;
  \max\!\left\{0.2,\;(1-\alpha)p_t+\alpha q_t\right\}
\right\},
\qquad \alpha=0.1.
$$

Trong đối chứng, cả hai phương pháp bắt đầu tại $p_0=0.5$. Phương án **fixed** giữ $p_{t+1}=p_t$, nhưng **không tham gia đợt đo 300 run này**.

## Chỉ số đánh giá và chiều cải thiện

Xét bài toán cực tiểu hóa hai mục tiêu. Gọi $A$ là tập vector mục tiêu không bị trội thu được ở cuối run; $R$ là tập điểm tham chiếu trên Pareto front; $\mathbf{h}$ là điểm tham chiếu hypervolume.

### IGD — khoảng cách tới Pareto front tham chiếu ↓

$$
\operatorname{IGD}(A,R)
=\frac{1}{|R|}\sum_{\mathbf{z}\in R}
  \min_{\mathbf{a}\in A}\left\|\mathbf{z}-\mathbf{a}\right\|_2.
$$

**IGD càng nhỏ càng tốt:** tập nghiệm thu được càng gần và bao phủ tốt các điểm tham chiếu. Khoảng cách sử dụng chuẩn Euclid trong không gian mục tiêu, không chuẩn hóa thêm.

### HV — thể tích vùng bị tập nghiệm trội ↑

$$
\operatorname{HV}(A;\mathbf{h})
=\lambda_2\!\left(
  \bigcup_{\substack{\mathbf{a}\in A\\\mathbf{a}\preceq\mathbf{h}}}
  [a_1,h_1]\times[a_2,h_2]
\right).
$$

Ở đây $\lambda_2$ là diện tích trong không gian hai mục tiêu. **HV càng lớn càng tốt.** Những điểm nằm ngoài hộp tham chiếu không đóng góp diện tích. Trong phép đo này:

$$
h_j=\max_{\mathbf{z}\in R}z_j+0.1,
\qquad j\in\{1,2\}.
$$

Mỗi bài ZDT dùng cùng tập $R$ và điểm $\mathbf{h}$ cho cả hai phương pháp; không so trực tiếp trị số HV giữa các bài khác nhau.

### Phần trăm cải thiện được báo cáo

Gọi $\widetilde{M}_{\mathrm{gen}}$ và $\widetilde{M}_{\mathrm{succ}}$ là median của chỉ số $M$ trên 30 run mỗi phương pháp:

$$
I_{\mathrm{IGD}}
=100\,\frac{\widetilde{\mathrm{IGD}}_{\mathrm{gen}}
            -\widetilde{\mathrm{IGD}}_{\mathrm{succ}}}
           {\widetilde{\mathrm{IGD}}_{\mathrm{gen}}},
$$

$$
I_{\mathrm{HV}}
=100\,\frac{\widetilde{\mathrm{HV}}_{\mathrm{succ}}
            -\widetilde{\mathrm{HV}}_{\mathrm{gen}}}
           {\widetilde{\mathrm{HV}}_{\mathrm{gen}}}.
$$

**Số dương là cải thiện; số âm là suy giảm.** Đây là phần trăm giữa hai median, không phải median phần trăm cải thiện của các cặp seed.

## Thiết kế và xác minh

- 2 phương án × 5 bài ZDT × 30 seed 1000–1029 = 300 run, tất cả hợp lệ. Population 100, cap 20.000; n_eval thực dùng 19.901–20.000 do batch nguyên tử.
- Chỉ đổi probability_update_mode. Cùng uniform initial population theo seed, adaptive restart, OBL định kỳ, F/CR và neighborhood. Sobol/OBL khởi tạo không tham gia.
- Kiểm tra hash toàn bộ primary và reference snapshot, task set, hash quần thể đầu tái tạo theo seed, bounds và F tính lại từ X; tính lại IGD/HV và Wilcoxon đều khớp. Không thay primary hay chạy lại optimizer.
- 58.338 bước cập nhật xác suất đã được đối chiếu độc lập theo trace. Source hash khớp bản tạo kết quả. Môi trường benchmark giới hạn OMP/OPENBLAS/MKL threads=1.

## Chất lượng theo median

**Generated-share** là đối chứng lịch sử; **success-rate** là phương pháp mới. Mỗi ô median tổng hợp 30 run. Phần trăm cải thiện chỉ mô tả độ lớn thay đổi, không tự xác lập khác biệt thống kê.

### IGD ↓

| Bài | Generated-share | Success-rate | Cải thiện (%) | $p$ Wilcoxon |
|:---|---:|---:|---:|---:|
| ZDT1 | 0.0045106 | 0.0044769 | +0.747 | 0.5999 |
| ZDT2 | 0.0046642 | 0.0047255 | -1.316 | 0.7655 |
| ZDT3 | 0.0050995 | 0.0050642 | +0.691 | 0.8290 |
| ZDT4 | 0.0062879 | 0.0055402 | +11.891 | 0.4653 |
| ZDT6 | 0.0037896 | 0.0038108 | -0.559 | 0.4165 |

### HV ↑

| Bài | Generated-share | Success-rate | Cải thiện (%) | $p$ Wilcoxon |
|:---|---:|---:|---:|---:|
| ZDT1 | 0.8708912 | 0.8709181 | +0.003 | 0.7813 |
| ZDT2 | 0.5376075 | 0.5377362 | +0.024 | 0.2623 |
| ZDT3 | 1.0512614 | 1.0512775 | +0.002 | 0.8774 |
| ZDT4 | 0.8655528 | 0.8675027 | +0.225 | 0.4405 |
| ZDT6 | 0.4381999 | 0.4380637 | -0.031 | 0.0571 |

## Hiệu ứng ghép seed và bất định

Đơn vị phân tích là cặp run cùng seed/bài, $n=30$. Đặt $\Delta_i=M_{\mathrm{succ},i}-M_{\mathrm{gen},i}$: với IGD, $\Delta_i<0$ là tốt hơn; với HV, $\Delta_i>0$ là tốt hơn. CI dưới đây là bootstrap percentile 95% của **mean delta**, 20.000 resample cặp seed, seed base 20261114; CI không hiệu chỉnh đa kiểm định. Đây là phân tích bổ sung sau khi xem kết quả, không phải endpoint mới đã đăng ký trước.

| Bài | Chỉ số | Mean $\Delta$ | CI 95% của mean $\Delta$ | Seed tốt / kém | $p$ |
|:---|:---|---:|---:|---:|---:|
| ZDT1 | IGD | +0.00004329 | [-0.00007660; +0.00016852] | 13 / 17 | 0.5999 |
| ZDT1 | HV | -0.00007935 | [-0.00021890; +0.00005211] | 16 / 14 | 0.7813 |
| ZDT2 | IGD | -0.00002565 | [-0.00020340; +0.00012860] | 13 / 17 | 0.7655 |
| ZDT2 | HV | +0.00006338 | [-0.00003797; +0.00016181] | 17 / 13 | 0.2623 |
| ZDT3 | IGD | -0.00002010 | [-0.00020193; +0.00016536] | 15 / 15 | 0.8290 |
| ZDT3 | HV | -0.00001347 | [-0.00010339; +0.00007757] | 14 / 16 | 0.8774 |
| ZDT4 | IGD | -0.00935667 | [-0.03313028; +0.01491586] | 16 / 14 | 0.4653 |
| ZDT4 | HV | +0.01442002 | [-0.02332287; +0.05228737] | 16 / 14 | 0.4405 |
| ZDT6 | IGD | +0.00001378 | [-0.00006811; +0.00009033] | 12 / 18 | 0.4165 |
| ZDT6 | HV | -0.00011819 | [-0.00024493; +0.00000600] | 11 / 19 | 0.0571 |

Không có cặp seed bằng nhau ở cả 10 phép so sánh. Tất cả CI đều chứa $0$.

Wilcoxon signed-rank hai phía, `zero_method="wilcox"`, xấp xỉ chuẩn. Giao thức gốc dùng Holm riêng giữa các cặp phương án trên từng bài/metric; vì chỉ có một cặp nên $p_{\mathrm{Holm}}=p_{\mathrm{thô}}$. Không kiểm định nào đạt 0,05 ngay cả trước hiệu chỉnh. Kiểm tra nhạy bổ sung Holm cho cả 10 endpoint cho p nhỏ nhất 0,571; kết luận không đổi. Không phát hiện khác biệt không chứng minh tương đương.

ZDT4: mean IGD cũ 0,0286434 ± SD 0,0486673; mới 0,0192867 ± SD 0,0412440. Mean khác median nhiều cho thấy đuôi kết quả kém; chỉ 16/30 seed tốt hơn ở cả IGD/HV. Chưa có cải thiện ổn định. ZDT1 có median IGD mới thấp hơn, nhưng chỉ 13/30 cặp tốt hơn và mean delta IGD dương: không được đọc riêng marginal median để khẳng định lợi ích.

ZDT6: median IGD/HV mới đều kém nhẹ; HV chỉ tốt hơn ở 11/30 seed, p=0,0571, chưa đủ gọi là suy giảm có ý nghĩa ở $\alpha=0.05$.

## Xác suất DE, restart và thời gian

| Bài | Median $p_{\mathrm{DE}}$ cuối: cũ → mới | Restart tổng: cũ / mới | Median runtime (s): cũ → mới |
|---|---:|---:|---:|
| ZDT1 | 0.4962 → 0.4610 | 0 / 0 | 5.660 → 13.096 |
| ZDT2 | 0.4989 → 0.4639 | 0 / 0 | 14.920 → 16.432 |
| ZDT3 | 0.5100 → 0.4219 | 0 / 0 | 14.492 → 16.099 |
| ZDT4 | 0.4973 → 0.5276 | 0 / 0 | 15.613 → 17.468 |
| ZDT6 | 0.4921 → 0.4507 | 4 / 3 | 14.569 → 13.718 |

Success-rate dịch $p_{\mathrm{DE}}$ xuống dưới 0,5 ở ZDT1/2/3/6, và lên khoảng 0,528 ở ZDT4. Điều này xác nhận cơ chế phản hồi đã hoạt động, không chứng minh chất lượng tốt hơn. Đây là xác suất cuối, không phải tỷ lệ DE trung bình toàn run.

Restart không xuất hiện ở ZDT1–4. ZDT6 có 4 attempt ở generated-share và 3 ở success-rate, không cùng seed hoàn toàn (23/30 cặp đều không restart). Khác biệt trigger có thể phát sinh theo quỹ đạo tìm kiếm; không quy toàn bộ chênh lệch ZDT6 trực tiếp cho cập nhật xác suất mà bỏ qua tác động hạ nguồn này.

Runtime mô tả máy đo với 4 worker và thứ tự task không hoán đổi ngẫu nhiên; chênh lệch tải máy có thể gây nhiễu. Không kết luận overhead riêng của công thức từ tỷ lệ runtime, đặc biệt ZDT1. Success-rate cần kiểm tra thêm SBX so với generated-share, nhưng chi phí này chưa được cô lập bằng profiling.

## Quyết định phù hợp với bằng chứng

- **Quyết định hiện tại:** dùng success-rate làm mặc định theo định hướng thiết kế; giữ fixed làm đối chứng. Quyết định này không đồng nghĩa đã có bằng chứng thống kê về cải thiện. Generated-share chỉ còn trong dữ liệu và mô tả lịch sử.
- Không cần mở factorial 72 cấu hình từ kết quả này. Nếu nghiên cứu sâu success-rate, dùng seed mới cho xác nhận riêng, nhất là ZDT4; không điều chỉnh công thức trên chính tập seed rồi coi đó là xác nhận độc lập.
- Không dùng kết quả này để đánh giá đóng góp khởi tạo Sobol–OBL hoặc thay thế các bảng benchmark lịch sử: đây là ablation trên mã đã sửa lỗi F/CR, không phải rerun các đối chứng khác.

## Dữ liệu và truy vết

| Tệp | Nội dung |
|:---|:---|
| [JSON từng run](../../results/experiments/probability_generated_vs_success_zdt_v2/primary/) | 300 run, X/F cuối, trace xác suất và sự kiện restart |
| [Manifest](../../results/experiments/probability_generated_vs_success_zdt_v2/study_manifest.json) | Cấu hình, môi trường, hash mã nguồn và dữ liệu |
| [Kiểm tra toàn vẹn](../../results/experiments/probability_generated_vs_success_zdt_v2/derived/audit_validation.json) | Kết quả xác minh độc lập |
| [Thống kê từng phương án](../../results/experiments/probability_generated_vs_success_zdt_v2/derived/audit_summary.csv) | Mean, SD, median, Q25/Q75, thời gian và số restart |
| [Hiệu ứng ghép seed](../../results/experiments/probability_generated_vs_success_zdt_v2/derived/audit_effects.csv) | Delta, CI, số seed tốt/kém và giá trị $p$ |

Các bảng ở trên chỉ làm tròn để trình bày. JSON và CSV giữ nguyên độ chính xác gốc; không thay đổi dữ liệu đo.
