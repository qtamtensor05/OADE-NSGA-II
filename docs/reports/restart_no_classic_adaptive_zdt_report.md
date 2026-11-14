# Đối chứng no restart, classic và adaptive trên OADE

**Ngày phân tích:** 14/11/2026.

**Tên báo cáo:** `restart_no_classic_adaptive_zdt_report.md`, phản ánh đúng ba nhánh được so sánh. Tên cũ có `success_rate` vì đây là phiên bản OADE dùng chung cơ chế cập nhật xác suất DE theo thành công; không có phương pháp restart mang tên “success”.

**Bộ kết quả thực tế:** `results/experiments/restart_success_rate_zdt_v1/`. Giữ nguyên thư mục đã đo và manifest để không làm lệch provenance/resume. Tất cả liên kết dữ liệu trong báo cáo trỏ trực tiếp tới bộ 450 run này, không trỏ sang đối chứng xác suất DE hoặc đối chứng OBL.

**Kết luận chính:** Classic có tác động bất lợi so với adaptive/no-restart trên một số bài ZDT. Adaptive chủ yếu tránh các lần restart không cần thiết; chưa có bằng chứng rằng việc adaptive restart thực sự kích hoạt cải thiện chất lượng so với không restart. Adaptive và no-restart có X/F cuối giống hệt ở 147/150 cặp seed.

## 1. Thiết kế và kiểm tra dữ liệu

| Thành phần | Thiết lập |
|:---|:---|
| Dữ liệu | 3 nhánh × 5 bài ZDT × 30 seed = 450 run; tất cả hợp lệ |
| Seed | 1000–1029, ghép theo bài/seed; 150 bộ ba quần thể đầu giống nhau |
| Cơ chế chung | Uniform, OBL định kỳ, success-rate, adaptation F/CR, neighborhood |
| Population | 100 |
| Ngân sách | Cap 20.000 evaluation/run, gồm khởi tạo, OBL và restart |

Đã kiểm tra hashes của toàn bộ primary/reference, đủ task và seed, source hashes và môi trường khớp. Tái tạo quần thể đầu; tính lại F từ X và IGD/HV cuối; kiểm tra telemetry restart/OBL, 87.074 bước cập nhật xác suất, Wilcoxon và Holm. n_eval thực dùng 19.901–20.000, không vượt cap.
150/150 run adaptive tái lập chính xác X/F cuối của nhánh bật OBL trong thí nghiệm trước. Đây là kiểm tra tái lập; không cộng các run cũ như replicate độc lập mới.

## 2. Công thức và tham số của ba chính sách restart

### 2.1. Ký hiệu và cấu hình đã thực sự chạy

Các giá trị dưới đây được đối chiếu với **manifest của bộ 450 run**, không lấy từ giả định hay cấu hình của một đợt nghiên cứu khác.

| Ký hiệu | Ý nghĩa | Giá trị đã đo |
|:---|:---|:---|
| $P_t$, $N$ | Quần thể tại đầu vòng lặp; kích thước quần thể | $N=100$ |
| $\mathbf{l},\mathbf{h}$ | Bounds dưới/trên của từng biến quyết định | Theo từng bài ZDT |
| $\mathbf{z}^{*}_t$ | Ideal point tính trên $P_t$ | Min của từng mục tiêu |
| $s_t$, $T$ | Counter stagnation trước xử lý restart; patience | $T=20$ |
| $\tau$ | Ngưỡng thay đổi ideal point | $10^{-4}$ |
| $\varepsilon_f$ | Ngưỡng range mục tiêu để nhận diện collapse | $10^{-3}$ |
| $\delta_x$ | Ngưỡng độ lệch chuẩn biến quyết định chuẩn hóa | $0.02$ |
| $\rho_c$, $\rho_a$ | Tỷ lệ elite giữ lại khi classic/adaptive restart | $0.30$; $0.80$ |
| $\mu_F$, $\mu_{CR}$ | Tâm phân phối tham số DE | Ban đầu $0.65$; $0.50$ |
| $p_{\mathrm{DE},0}$ | Xác suất chọn DE ban đầu | $0.50$ |

| Thiết lập chung | Giá trị ở cả ba nhánh |
|:---|:---|
| Ngân sách objective | 20.000 evaluation/run, gồm mọi cơ chế |
| Replication | 30 seed 1000–1029/bài/nhánh |
| Bài toán | ZDT1/2/3: 30 biến; ZDT4/6: 10 biến; đều 2 mục tiêu |
| Khởi tạo | Uniform cùng quần thể đầu cho từng bài/seed; 100 evaluation |
| Láng giềng DE | 5 |
| Cập nhật xác suất DE | Success-rate, hệ số EMA $0.1$, giới hạn $[0.2,0.8]$ |
| Thích nghi F/CR | Bật ở cả ba nhánh |
| OBL định kỳ | Bật; chỉ số thế hệ $0,10,20,\ldots$; jump rate $0.2$ |

**Success-rate là cơ chế cập nhật xác suất chọn DE/SBX được giữ chung**, không phải một loại restart và không phải tên khác của adaptive restart.

### 2.2. Điều kiện stagnation dùng chung

Ideal point tại thời điểm xét restart:

$$
z^{*}_{t,j}=\min_{\mathbf{x}\in P_t}f_j(\mathbf{x}),
\qquad j\in\{1,2\}.
$$

Độ lớn thay đổi so với ideal point đã lưu ở vòng trước:

$$
d_t=\left\|\mathbf{z}^{*}_t-\mathbf{z}^{*}_{t-1}\right\|_2.
$$

Gọi $s^{\mathrm{out}}_{t-1}$ là counter sau xử lý restart ở vòng trước. Counter trước xử lý tại vòng hiện tại là:

$$
s_t=
\begin{cases}
0, & t=0,\\
0, & t>0\;\text{và}\;d_t\ge\tau,\\
s^{\mathrm{out}}_{t-1}+1, & t>0\;\text{và}\;d_t<\tau.
\end{cases}
$$

Đủ điều kiện stagnation khi $s_t\ge T$. **Lưu ý đúng theo mã:** $d_t$ đo độ lớn thay đổi, không phân biệt ideal point tốt lên hay xấu đi. Ideal point được lưu là giá trị **trước restart**, không tính lại ngay sau thay quần thể.

### 2.3. Không restart

Không có điều kiện nào dẫn tới can thiệp restart:

$$
P_t^{+}=P_t,
\qquad
s_t^{\mathrm{out}}=s_t.
$$

Tại riêng bước restart, $\mu_F$, $\mu_{CR}$ và $p_{\mathrm{DE}}$ được giữ nguyên. Các cơ chế thích nghi thông thường vẫn tiếp tục sau bước sinh con/chọn lọc trong thế hệ. Chi phí restart bằng **0 evaluation**.

Nhánh này vẫn theo dõi counter stagnation để đối chứng, nhưng không xét collapse, không sinh cá thể restart và không rút RNG phục vụ restart.

### 2.4. Classic — chính sách restart cũ

**Kích hoạt:** $s_t\ge T$; không yêu cầu collapse.

Số elite và số cá thể mới:

$$
n_{\mathrm{keep}}=\lfloor\rho_cN\rfloor=30,
\qquad
n_{\mathrm{new}}=N-n_{\mathrm{keep}}=70.
$$

Gọi $E_{30}(P_t)$ là 30 cá thể đầu theo thứ tự rank tăng, crowding giảm của quần thể. Với mỗi cá thể mới:

$$
\mathbf{u}_i\sim\mathcal{U}([0,1]^{n_{\mathrm{var}}}),
\qquad
\mathbf{x}^{\mathrm{new}}_i
=\mathbf{l}+\mathbf{u}_i\odot(\mathbf{h}-\mathbf{l}).
$$

Sau đánh giá, tạo quần thể restart:

$$
P_t^{+}
=\mathcal{S}_N\!\left(E_{30}(P_t)\uplus Q_{70}\right),
$$

trong đó $Q_{70}$ chứa 70 cá thể mới đã đánh giá; $\mathcal{S}_N$ là chọn lọc Pareto/crowding và $\uplus$ biểu thị ghép danh sách ứng viên, không tự loại trùng.

Reset trạng thái:

$$
\mu_F^{+}=\mu_{CR}^{+}=0.5,
\qquad
s_t^{\mathrm{out}}=0.
$$

Không reset $p_{\mathrm{DE}}$. Mỗi restart hoàn tất tốn **70 evaluation**. Nếu không đủ ngân sách để đánh giá nguyên batch, bị chặn trước đánh giá, không reset F/CR và không tính hoàn tất. Nếu chưa đủ patience, $P_t^{+}=P_t$ và $s_t^{\mathrm{out}}=s_t$.

### 2.5. Adaptive — chính sách restart mới

**Bước 1 — xác định collapse.** Với từng mục tiêu:

$$
R_f=\max_j\left[
\max_{\mathbf{x}\in P_t}f_j(\mathbf{x})-
\min_{\mathbf{x}\in P_t}f_j(\mathbf{x})
\right].
$$

Chuẩn hóa biến quyết định theo bounds:

$$
y_{i,k}=\frac{x_{i,k}-l_k}{w_k},
\qquad
w_k=
\begin{cases}
h_k-l_k, & h_k-l_k>10^{-12},\\
1, & \text{ngược lại}.
\end{cases}
$$

Tính độ lệch chuẩn với mẫu số $N$, đúng với `np.std(..., ddof=0)`:

$$
\bar y_k=\frac{1}{N}\sum_{i=1}^{N}y_{i,k},
\qquad
D_x=\max_k\sqrt{\frac{1}{N}\sum_{i=1}^{N}(y_{i,k}-\bar y_k)^2}.
$$

Điều kiện collapse:

$$
C_t=(R_f<10^{-3})\;\lor\;(D_x<0.02).
$$

Mã còn coi quần thể có ít hơn 2 cá thể là collapsed; trường hợp đó không xảy ra trong bộ đo $N=100$ này.

**Bước 2 — điều kiện kích hoạt:** $s_t\ge20$ **và** $C_t$ đúng. Nếu đủ stagnation nhưng không collapse, không thay quần thể và đặt:

$$
s_t^{\mathrm{out}}=\left\lfloor\frac{T}{2}\right\rfloor=10.
$$

**Bước 3 — tạo ứng viên khi kích hoạt.** Số elite được giữ:

$$
n_{\mathrm{keep}}
=\max\!\left(\lfloor\rho_aN\rfloor,\lfloor0.8N\rfloor\right)=80,
\qquad n_{\mathrm{new}}=20.
$$

Với mỗi ứng viên, chọn ngẫu nhiên đều một base $\mathbf{b}_i$ trong $E_{80}(P_t)$ và lấy $\boldsymbol{\epsilon}_i\sim\mathcal{N}(\mathbf{0},\mathbf{I})$:

$$
\mathbf{v}_i=
\begin{cases}
\mathbf{l}+\mathbf{h}-\mathbf{b}_i
+0.05\,\boldsymbol{\epsilon}_i\odot(\mathbf{h}-\mathbf{l}),
& \text{xác suất }0.5,\\
\mathbf{b}_i+0.10\,\boldsymbol{\epsilon}_i\odot(\mathbf{h}-\mathbf{l}),
& \text{xác suất }0.5.
\end{cases}
$$

Clip từng biến vào bounds rồi đánh giá:

$$
\mathbf{x}^{\mathrm{new}}_i
=\operatorname{clip}(\mathbf{v}_i,\mathbf{l},\mathbf{h}),
\qquad
P_t^{+}=\mathcal{S}_N\!\left(E_{80}(P_t)\uplus Q_{20}\right).
$$

Điều chỉnh trạng thái nhẹ thay vì reset toàn bộ:

$$
\mu_F^{+}=0.8\mu_F+0.2(0.5),
\qquad
\mu_{CR}^{+}=0.8\mu_{CR}+0.2(0.5),
\qquad
s_t^{\mathrm{out}}=0.
$$

Không reset $p_{\mathrm{DE}}$. Mỗi lần hoàn tất tốn **20 evaluation**; batch bị chặn nếu không đủ ngân sách. Nếu chưa đủ stagnation thì không xét collapse, không restart và giữ counter đã cập nhật.

### 2.6. Phạm vi đối chứng

Mỗi run chỉ dùng **một** chính sách. Các cặp “Classic – Adaptive”, “Classic – Không restart” và “Adaptive – Không restart” là phép so sánh hai run độc lập cùng bài/seed, không phải một thuật toán kết hợp các restart.

Đây là đối chứng **toàn bộ chính sách**: điều kiện kích hoạt, tỷ lệ elite, kernel sinh ứng viên và cách điều chỉnh F/CR. Không coi đây là phép thử chỉ thay riêng diversity gate.

## 3. Chất lượng cuối — median 30 run

### IGD ↓

| Bài | Không restart | Classic | Adaptive |
|:---|---:|---:|---:|
| ZDT1 | 0.0044769 | 0.0051874 | 0.0044769 |
| ZDT2 | 0.0047255 | 0.0054509 | 0.0047255 |
| ZDT3 | 0.0050642 | 0.0055369 | 0.0050642 |
| ZDT4 | 0.0055402 | 0.0055402 | 0.0055402 |
| ZDT6 | 0.0038108 | 0.0040517 | 0.0038108 |

### HV ↑

| Bài | Không restart | Classic | Adaptive |
|:---|---:|---:|---:|
| ZDT1 | 0.8709181 | 0.8701650 | 0.8709181 |
| ZDT2 | 0.5377362 | 0.5363211 | 0.5377362 |
| ZDT3 | 1.0512775 | 1.0511320 | 1.0512775 |
| ZDT4 | 0.8675027 | 0.8675027 | 0.8675027 |
| ZDT6 | 0.4380637 | 0.4377869 | 0.4380637 |

Median adaptive và no-restart giống nhau trên mọi bài; không được suy ra cả hai trùng ở tất cả seed chỉ từ median. So sánh X/F từng seed được trình bày riêng bên dưới.

## 4. Kiểm định đủ ba cặp

Đơn vị phân tích là cặp run cùng seed/bài, $n=30$. Wilcoxon signed-rank hai phía, `zero_method="wilcox"`, xấp xỉ chuẩn; toàn delta zero đặt $p=1$. Họ kiểm định chính đã định trước gồm **30 endpoint**: 5 bài × 2 metric × 3 cặp, Holm với $\alpha=0.05$. Bảng dưới dùng p đã hiệu chỉnh trên toàn bộ họ này.

| Bài | Cặp | $p$ Holm IGD | $p$ Holm HV | Khác biệt được phát hiện |
|:---|:---|---:|---:|:---|
| ZDT1 | Classic – Adaptive | 0.000448 | 0.000885 | Classic kém: IGD, HV |
| ZDT1 | Classic – Không restart | 0.000448 | 0.000885 | Classic kém: IGD, HV |
| ZDT1 | Adaptive – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT2 | Classic – Adaptive | 0.012689 | 0.000727 | Classic kém: IGD, HV |
| ZDT2 | Classic – Không restart | 0.012689 | 0.000727 | Classic kém: IGD, HV |
| ZDT2 | Adaptive – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT3 | Classic – Adaptive | 0.059149 | 0.079013 | Chưa phát hiện |
| ZDT3 | Classic – Không restart | 0.059149 | 0.079013 | Chưa phát hiện |
| ZDT3 | Adaptive – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT4 | Classic – Adaptive | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT4 | Classic – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT4 | Adaptive – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |
| ZDT6 | Classic – Adaptive | 0.115964 | 0.021749 | Classic kém: HV |
| ZDT6 | Classic – Không restart | 0.085115 | 0.021178 | Classic kém: HV |
| ZDT6 | Adaptive – Không restart | 1.000000 | 1.000000 | Chưa phát hiện |

**Diễn giải:** classic kém adaptive và no-restart về IGD/HV trên ZDT1–2, và về HV trên ZDT6. Trên ZDT3, kiểm định riêng họ ba cặp/bài/metric đạt ngưỡng nhưng không còn đạt sau Holm toàn bộ 30 endpoint (IGD 0,0591; HV 0,0790). Không nâng kết luận ZDT3 thành khác biệt vững trên toàn bộ nghiên cứu.
Các cặp classic–adaptive và classic–no-restart chia sẻ run, nhiều kết quả còn trùng; không đếm chúng như bằng chứng độc lập mới. Không phát hiện khác biệt không đồng nghĩa đã chứng minh tương đương.

## 5. Restart có thực sự kích hoạt?

| Bài | Classic: bắt đầu / hoàn tất / bị chặn | Adaptive: bắt đầu / hoàn tất | Adaptive: xét collapse / từ chối do khỏe | X/F adaptive trùng no-restart |
|:---|---:|---:|---:|---:|
| ZDT1 | 208 / 208 / 0 | 0 / 0 | 413 / 413 | 30/30 |
| ZDT2 | 166 / 164 / 2 | 0 / 0 | 325 / 325 | 30/30 |
| ZDT3 | 180 / 177 / 3 | 0 / 0 | 356 / 356 | 30/30 |
| ZDT4 | 3 / 3 / 0 | 0 / 0 | 4 / 4 | 30/30 |
| ZDT6 | 92 / 92 / 0 | 3 / 3 | 155 / 152 | 27/30 |

Tổng classic: **649 attempt, 644 hoàn tất, 5 bị chặn trước đánh giá**, tiêu tốn **45.080 objective evaluations**. Adaptive: **3 attempt, đều hoàn tất**, tiêu tốn **60 evaluations**. No-restart: 0.
Adaptive xét collapse **1.253 lần**, từ chối restart **1.250 lần** vì diversity vẫn khỏe. Đây là số lần kiểm tra, không phải 1.253 episode stagnation độc lập. Counter được reset/giảm khác nhau giữa các nhánh nên không so trực tiếp số đủ patience như số đợt trì trệ.
**ZDT1–4:** adaptive không restart và trùng no-restart ở toàn bộ 120 cặp. Vì vậy, lợi thế so với classic trên ZDT1–2 phù hợp với việc tránh can thiệp restart bất lợi, không phải bằng chứng adaptive đã cải thiện nghiệm bằng một lần restart thành công.

## 6. Ba lần adaptive restart trên ZDT6

| Seed | Thế hệ | Evaluation trước restart | IGD adaptive / không restart | HV adaptive / không restart |
|---:|---:|---:|---:|---:|
| 1006 | 108 | 11028 | 0.00371676 / 0.00354618 | 0.43844133 / 0.43824510 |
| 1014 | 171 | 17461 | 0.00390802 / 0.00390449 | 0.43793228 / 0.43798437 |
| 1018 | 191 | 19489 | 0.00394126 / 0.00385373 | 0.43758994 / 0.43777955 |

Trên cả ba seed này, IGD cuối của adaptive **kém hơn** no-restart; HV tốt hơn ở 1 seed và kém hơn ở 2 seed. Ngay sau cả ba event, IGD tăng và HV giảm so với trước event. Điều này mô tả đánh đổi chất lượng tức thời khi thay cá thể, không chứng minh adaptive restart luôn có hại.
Trên toàn bộ 30 seed ZDT6, adaptive và no-restart còn 27 cặp trùng hẳn. IGD có p thô 0,1088, p Holm 30 endpoint bằng 1; HV p bằng 1. Chỉ ba cặp thay đổi nên chưa đủ bằng chứng lợi ích hoặc kết luận tổng quát về tác hại của restart adaptive. Sự trùng median không thay thế việc kiểm tra ba cặp này.

## 7. Độ lớn hiệu ứng và chi phí

Phần trăm dưới đây so sánh median adaptive với median classic; IGD giảm và HV tăng là tốt. Đây là thống kê mô tả, không phải kết luận kiểm định riêng.

| Bài | IGD giảm khi dùng adaptive (%) | HV tăng (%) | Ngân sách restart classic (%) | Ngân sách restart adaptive (%) |
|:---|---:|---:|---:|---:|
| ZDT1 | +13.697 | +0.0865 | 2.4302 | 0.0000 |
| ZDT2 | +13.307 | +0.2639 | 1.9177 | 0.0000 |
| ZDT3 | +8.537 | +0.0138 | 2.0705 | 0.0000 |
| ZDT4 | +0.000 | -0.0000 | 0.0351 | 0.0000 |
| ZDT6 | +5.945 | +0.0632 | 1.0763 | 0.0100 |

Mọi chi phí nằm trong cap, không cấp thêm evaluation cho restart. Classic có thể mất chất lượng vì loại cá thể, reset F/CR, đổi quỹ đạo và dành ngân sách cho restart; thiết kế này chưa phân rã từng nguyên nhân. Chất lượng thấp hơn dù cùng cap là hiệu ứng ròng của chính sách.
Cột p_holm trong CSV giữ họ ba cặp/bài/metric để truy vết, nhưng kết luận chung dùng p_holm_all_endpoints. Mean/SD/median/Q25/Q75, số seed tốt/kém và CI nằm trong các CSV audit.
CI 95% trong audit_effects.csv là bootstrap percentile của **mean** $\Delta=M_b-M_a$, 20.000 resample cặp seed; seed base 20261114. CI là phân tích bổ sung, chưa hiệu chỉnh đa kiểm định; không thay thế kết luận Wilcoxon–Holm. Mean delta và median delta có thể khác hướng hoặc độ lớn.
Runtime giữa các nhóm task có chênh lệch lớn (ví dụ ZDT1 classic khoảng 3,9 s/run trong khi adaptive khoảng 17,1 s/run), dù code/môi trường xác minh khớp. Thứ tự task và tải máy không được hoán đổi ngẫu nhiên, nên không suy ra overhead hay tốc độ riêng của chính sách từ runtime này.

## 8. Kết luận áp dụng

- **Không ưu tiên classic** làm mặc định trong cấu hình ZDT này: có bằng chứng chất lượng kém hơn no-restart/adaptive trên một số bài, đặc biệt ZDT1–2.
- Adaptive hoạt động như một cơ chế bảo vệ thận trọng trước restart không cần thiết. Có thể giữ như thiết kế hiện tại, nhưng **chưa được tuyên bố adaptive restart cải thiện so với không restart**.
- No-restart là đối chứng thiết yếu. Kết quả hiện tại cho thấy lợi thế adaptive so với classic phần lớn đi kèm không kích hoạt restart; 147/150 cặp adaptive/no-restart trùng chính xác.
- Nếu muốn chứng minh giá trị của adaptive khi thực sự collapse, cần bài toán/điều kiện phù hợp và xác nhận độc lập. Không ép threshold trên chính bộ seed này cho đến khi có kết quả tốt rồi coi đó là kiểm chứng độc lập.
- Phạm vi kết luận: uniform, OBL định kỳ bật, success-rate, population 100, cap 20.000, 5 bài ZDT và 30 seed đã thử. Không thay mặc định hoặc chạy thêm benchmark trong đợt phân tích này.

## Dữ liệu và truy vết

### Đối chiếu nhận dạng bộ dữ liệu

| Nhánh trong báo cáo | ID trong JSON | Số run | Cơ chế thực sự dùng |
|:---|:---|---:|:---|
| Không restart | `no_restart` | 150 | Tắt can thiệp restart |
| Classic | `classic` | 150 | Restart cũ |
| Adaptive | `adaptive` | 150 | Restart mới, có kiểm tra collapse |

Manifest ghi đúng population 100, cap 20.000, seed 1000–1029, 5 bài ZDT và ba cấu hình đã nêu. Nhánh `no_restart` có thể vẫn lưu `restart_mode: classic` và elite ratio 0,30 trong JSON, nhưng cờ `enable_restart: false` vô hiệu hóa toàn bộ bước restart; đây không phải nhánh vừa classic vừa không restart.

| Tệp | Nội dung |
|:---|:---|
| [Primary JSON](../../results/experiments/restart_success_rate_zdt_v1/primary/) | 450 run, X/F đầu và cuối, telemetry, event, probability trace |
| [Manifest](../../results/experiments/restart_success_rate_zdt_v1/study_manifest.json) | Cấu hình, mã nguồn, môi trường và checksum |
| [Kiểm tra độc lập](../../results/experiments/restart_success_rate_zdt_v1/derived/audit_validation.json) | Toàn vẹn, tái lập, tính lại chỉ số và kiểm định |
| [Thống kê ba nhánh](../../results/experiments/restart_success_rate_zdt_v1/derived/audit_summary.csv) | Chất lượng, độ phân tán, trigger và chi phí |
| [Hiệu ứng ba cặp](../../results/experiments/restart_success_rate_zdt_v1/derived/audit_effects.csv) | Số seed tốt/kém/trùng, delta, CI, p và Holm 30 endpoint |
| [Ba seed adaptive kích hoạt](../../results/experiments/restart_success_rate_zdt_v1/derived/audit_adaptive_triggered_seeds.json) | Before/after event và đối chiếu no-restart từng seed |
| [Nhật ký restart](../../results/experiments/restart_success_rate_zdt_v1/derived/restart_events.csv) | Toàn bộ attempt, thời điểm, trạng thái và chi phí |

Chỉ làm tròn khi trình bày; primary, manifest và CSV gốc giữ nguyên. Không chạy lại optimizer trong đợt audit này.
