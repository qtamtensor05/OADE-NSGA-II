# OADE-NSGA-II: NSGA-II kết hợp tiến hóa vi phân thích nghi và học đối lập

**Language / Ngôn ngữ:** [English](README.md) | **Tiếng Việt**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Giao thức](https://img.shields.io/badge/Benchmark-Fixed--Budget%2020k-orange.svg)](#giao-thuc)

Dự án nghiên cứu kết hợp **học đối lập (OBL)**, **tiến hóa vi phân (DE) định hướng theo lân cận**, **cập nhật F/CR trực tuyến** và **khởi động lại có xét độ đa dạng** vào khung NSGA-II. Các kết quả dưới đây áp dụng cho những bộ bài toán và bản triển khai đã thử nghiệm; chưa chứng minh cải thiện phổ quát so với NSGA-II.

Đọc [mục lục nghiên cứu](docs/index.md), [bản thảo tổng hợp](docs/manuscript.md), [bảng định danh thuật toán đối chứng](docs/baselines.md) và [hướng dẫn tái lập](docs/reproducibility.md). Tài liệu chuyên sâu và chữ trong hình hiện chủ yếu bằng tiếng Anh; mã lệnh và định danh kết quả giữ nguyên giữa hai bản README.

## Mục lục

- [1. Tổng quan và các thành phần](#tong-quan)
- [2. Giao thức thí nghiệm và thống kê](#giao-thuc)
- [3. Kết quả đã ghi nhận](#ket-qua)
- [4. Điểm mạnh trong phạm vi đã thử nghiệm](#diem-manh)
- [5. Hạn chế và giới hạn kết luận](#han-che)
- [6. Hình minh họa và dữ liệu nguồn](#hinh-minh-hoa)
- [7. Cấu trúc dự án và khả năng tái lập](#cau-truc)
- [8. Hướng dẫn chạy](#huong-dan)
- [Tài liệu nghiên cứu và trích dẫn](#tai-lieu)

<a id="tong-quan"></a>

## 1. Tổng quan và các thành phần

Việc một cơ chế xuất hiện trong mã nguồn không tự chứng minh rằng cơ chế đó cải thiện hiệu năng. Các thành phần chính gồm:

1. **Khởi tạo Sobol + OBL ở chế độ độc lập:** solver có thể lấy mẫu ứng viên và điểm đối lập trước khi chọn quần thể ban đầu. Benchmark ngân sách cố định truyền quần thể uniform dùng chung, nên bỏ qua nhánh khởi tạo này. Ablation OBL hiện đánh giá việc bổ sung ứng viên đối lập định kỳ, kể cả thế hệ 0, chứ không đánh giá Sobol.
2. **Bổ sung ứng viên đối lập định kỳ:** thực hiện mỗi 10 thế hệ. Kết quả hiện tại chưa cô lập đóng góp nhân quả của cơ chế này trên tất cả các bộ bài toán.
3. **Đột biến DE theo lân cận (DE/current-to-pbest/1):** dùng thông tin lân cận khi tạo ứng viên DE. Đóng góp riêng chưa được xác nhận trên toàn bộ phạm vi thử nghiệm.
4. **Khởi động lại thích nghi theo độ đa dạng, cấu hình v2:** yêu cầu trì trệ ideal point ($\|\Delta\mathbf{z}^*\|<10^{-4}$) cùng điều kiện sụp đổ đa dạng. Mã kiểm tra độ lệch chuẩn trong không gian quyết định đã chuẩn hóa ($\max_j\sigma_j<0.02$) hoặc độ trải rộng mục tiêu dưới $10^{-3}$. Khi kích hoạt, cấu hình giữ 80% cá thể và tạo phần thay thế bằng OBL cục bộ/nhiễu Gaussian, đồng thời cập nhật mềm lịch sử F/CR. Dữ liệu lịch sử không lưu số lần kích hoạt, nên chưa chứng minh trigger này gây ra cải thiện quan sát được.

<a id="giao-thuc"></a>

## 2. Giao thức thí nghiệm và thống kê

Báo cáo ghi rõ thiết kế benchmark, dữ liệu từng lần chạy, kiểm định và giới hạn. Đây chưa phải chứng nhận đáp ứng quy định của một tạp chí cụ thể.

| Thành phần | Thiết lập và cách diễn giải |
|---|---|
| Đơn vị phân tích | Một lần chạy ngẫu nhiên hoàn chỉnh; lên lịch 30 lần/cấu hình. DTLZ có 26–30 cặp hợp lệ mỗi so sánh; các bộ benchmark chính còn lại có 30 cặp. |
| Ngân sách | ZDT có trần 20.000 đánh giá/lần, bao gồm bước tạo aspiration points và runtime của RNSGA2. DTLZ/WFG lưu theo quy ước ngân sách tìm kiếm riêng; xem [định nghĩa ngân sách](docs/experiment_registry.md#budget-definition). |
| Sử dụng ngân sách | Có thể dừng dưới trần nếu lô đánh giá tiếp theo vượt ngân sách; OADE thường dùng khoảng 99,7–99,9%. |
| Ghép cặp | Các thuật toán được cấp cùng quần thể ban đầu và cùng seed cho mỗi lần chạy. |
| Chỉ số chất lượng | IGD càng thấp càng tốt; HV càng cao càng tốt. |
| Kiểm định | Wilcoxon signed-rank ghép cặp, hai phía; Holm riêng theo từng bộ bài toán và chỉ số, $\alpha=0.05$. |
| Họ so sánh Holm | ZDT: $m=30$; DTLZ1–4: $m=72$; WFG hai mục tiêu, 7 thuật toán: $m=24$; compact WFG: $m=48$. |
| Cỡ hiệu ứng | Tương quan rank-biserial ghép cặp, $r\in[-1,1]$. |

**Không phát hiện khác biệt có ý nghĩa thống kê không đồng nghĩa với tương đương.** Tổng số thắng/thua qua nhiều bộ bài toán chỉ là mô tả các họ kiểm định riêng, không phải một họ Holm chung.

Phạm vi gồm 21 cấu hình chính và 12 cấu hình compact WFG, tổng cộng **6.210 bản ghi**. Một số baseline và thiết lập được tái sử dụng giữa các đợt; đây không phải 6.210 lần chạy mới độc lập.

| Bộ bài toán | Số bản ghi | Cấu hình |
|---|---:|---|
| ZDT hai mục tiêu, 7 thuật toán | 1.050 | ZDT1–3: $D=30$; ZDT4 và ZDT6: $D=10$. |
| DTLZ1–4, 7 thuật toán | 2.520 | $M\in\{2,3,5\}$; DTLZ1: $D\in\{6,7,9\}$; DTLZ2–4: $D\in\{11,12,14\}$. |
| WFG hai mục tiêu, 7 thuật toán | 840 | WFG1, WFG4, WFG6, WFG9; $M=2,D=24,k=4$. |
| Compact WFG, 5 thuật toán | 1.800 | Cùng bốn hàm WFG; $M\in\{2,3,5\},D=24,k\in\{4,8\}$; OADE, NSGA2, DNSGA2, RNSGA2 và SDR-OLS. |

Sáu thuật toán đối chứng thực tế:

- **NSGA-II:** bản triển khai pymoo, dựa trên Deb và cộng sự (2002).
- **D-NSGA-II:** Dynamic NSGA-II, không phải thuật toán dựa trên hướng; được thử trên các hàm tĩnh trong nghiên cứu này.
- **R-NSGA-II:** NSGA-II dựa trên điểm tham chiếu/aspiration points.
- **CGDE-NSGA-II:** Cross-Generation DE, bản triển khai cục bộ; chưa xác lập citation bài gốc khớp hoàn toàn.
- **NSGA-II/SDR-OLS:** quan hệ trội tăng cường, học đối lập và tìm kiếm cục bộ; bản cục bộ có giới hạn số láng giềng tìm kiếm.
- **CE-MOEA:** bản điều chỉnh thành phần tìm kiếm liên tục của Continuous Encoding MOEA; không phải Cross-Entropy MOEA và không đánh giá đầy đủ graph encoding của bài gốc.

Xem [bảng baseline](docs/baselines.md) để biết nguồn mã, cấu hình và khác biệt so với phương pháp gốc.

<a id="ket-qua"></a>

## 3. Kết quả đã ghi nhận

### Tổng hợp ZDT v2 và DTLZ1–4

Trong **204 so sánh** từ 3.570 bản ghi, OADE có **149 thắng (73,0%), 41 không phát hiện khác biệt (20,1%) và 14 thua (6,9%)**. OADE có 510/510 lần chạy hợp lệ. Tổng này gộp các họ Holm riêng và chỉ mang ý nghĩa mô tả.

| Bộ kết quả | Thắng | Không phát hiện khác biệt | Thua | Xếp hạng mô tả |
|---|---:|---:|---:|---|
| ZDT v2 | 58 | 1 | 1 | Hạng 1 theo trung bình trên 8/10 tổ hợp bài toán–chỉ số. |
| DTLZ1–4 | 91 | 40 | 13 | Hạng 1 trên 8/12 trung vị IGD và 7/12 trung bình HV; không có so sánh thua có ý nghĩa thống kê tại $M=5$ trong bộ này. |

Trên 17 cấu hình, số thắng/không phát hiện khác biệt/thua lần lượt là: CE-MOEA **23/11/0**, SDR-OLS **30/4/0**, R-NSGA-II **31/3/0**, NSGA-II **22/7/5**, D-NSGA-II **22/7/5** và CGDE **21/9/4**.

### ZDT v2

Giá trị OADE dưới đây là **trung bình ± độ lệch chuẩn** trên 30 lần chạy. Xếp hạng mô tả không thay thế kiểm định ghép cặp.

| Bài toán | IGD ↓ của OADE | HV ↑ của OADE | Diễn giải |
|---|---:|---:|---|
| ZDT1 | 0.004475 ± 0.000251 | 0.870866 ± 0.000232 | Tốt nhất theo trung bình ở cả hai chỉ số; thắng NSGA-II sau Holm. |
| ZDT2 | 0.004756 ± 0.000292 | 0.537674 ± 0.000222 | Tốt nhất theo trung bình ở cả hai chỉ số; thắng NSGA-II sau Holm. |
| ZDT3 | 0.004986 ± 0.000336 | 1.051221 ± 0.000152 | Tốt nhất theo trung bình ở cả hai chỉ số. |
| ZDT4 | 0.006831 ± 0.003329 | 0.865051 ± 0.005679 | Tốt nhất theo trung bình ở cả hai chỉ số; thắng NSGA-II sau Holm. |
| ZDT6 | 0.003844 ± 0.000193 | 0.438177 ± 0.000253 | CGDE có trung bình tốt hơn; IGD không phát hiện khác biệt ($p_{adj}=0.776$), HV nghiêng về CGDE ($p_{adj}\approx5.58\times10^{-8}$). |

Bảng đối chứng đầy đủ, p-value và cỡ hiệu ứng nằm trong [báo cáo ZDT v2](docs/benchmark_v2_results_report.md).

### Điểm nổi bật trên DTLZ1–4

- **DTLZ1:** kết quả thuận lợi trên các cấu hình đa cực trị. Tại $M=5$, trung vị IGD của OADE là `0.8972`, so với NSGA-II `40.17`; chỉ 13/30 lần OADE có HV dương, các baseline đều 0/30 trong cấu hình này.
- **DTLZ2:** tại $M=3$, OADE có IGD kém hơn NSGA-II/D-NSGA-II và CGDE; tại $M=5$, OADE có trung vị IGD `0.4214` và HV `0.4517`.
- **DTLZ3:** OADE có kết quả IGD thuận lợi ở nhiều so sánh, nhưng tại $M=5$ cả bảy thuật toán đều có HV bằng 0 trong toàn bộ 30 lần chạy.
- **DTLZ4:** tại $M=3$, OADE vẫn có thiếu hụt IGD trước một số đối chứng; tại $M=5$, OADE có trung vị IGD `0.3746`. OADE không có đầu ra bị validator đánh dấu không hợp lệ trong 90 lần DTLZ4. Các chẩn đoán corner-collapse lịch sử là tiêu chuẩn khác, chưa có rule ghi lại đầy đủ; không diễn giải chúng như tỷ lệ lỗi cấu trúc.

Toàn bộ DTLZ có **18 đầu ra không hợp lệ** từ các đối chứng; các kiểm định chất lượng dùng cặp hợp lệ và vì vậy có điều kiện theo valid output. Xem [báo cáo tích hợp](docs/dtlz1_4_integrated_report.md).

### WFG hai mục tiêu và mở rộng số mục tiêu

| Thí nghiệm | Thắng / không phát hiện khác biệt / thua | Phạm vi |
|---|---|---|
| WFG $M=2$, 7 thuật toán | **42 / 0 / 6** trên 48 so sánh | 840 bản ghi, 0 không hợp lệ; OADE có hạng trung bình mô tả 1.75. |
| Compact WFG, 5 thuật toán | **56 / 11 / 29** trên 96 so sánh | 1.800 bản ghi, 0 không hợp lệ. |
| Compact WFG tại $M=2$ | 28 / 0 / 4 | Tỷ lệ thắng 87,5%. |
| Compact WFG tại $M=3$ | 17 / 4 / 11 | Tỷ lệ thắng 53,1%. |
| Compact WFG tại $M=5$ | 11 / 7 / 14 | Tỷ lệ thắng 34,4%. |

OADE thuận lợi trên WFG1 và WFG9 hai mục tiêu. Với `wfg9_m2`, trung vị IGD là `0.0347`, trong khi sáu đối chứng có trung vị khoảng `0.128–0.640`. Với `wfg6_m2`, CGDE có IGD tốt hơn (`0.0302` so với `0.0526`) nhưng runtime đo được lớn hơn khoảng 101 lần trong môi trường và bản triển khai này. WFG4 và một số WFG6/9 ở số mục tiêu cao bộc lộ hạn chế của OADE.

Tổng hợp ZDT + WFG hai mục tiêu cho 100/1/7 trên 108 so sánh, nhưng vẫn là mô tả các họ kiểm định riêng. Xem [báo cáo WFG](docs/wfg_compact_report.md); không suy diễn xu hướng trên bốn hàm thành quy luật mở rộng tổng quát.

<a id="diem-manh"></a>

## 4. Điểm mạnh trong phạm vi đã thử nghiệm

1. **Kết quả thuận lợi trên một số bài toán đa cực trị:** ZDT4, DTLZ1/3 và WFG9 hai mục tiêu. Chưa cô lập được cơ chế gây ra toàn bộ cải thiện.
2. **Không có đầu ra OADE DTLZ4 không hợp lệ theo validator cấu trúc:** 0/90 trong các lần đã thử; không bảo đảm cho cấu hình hoặc seed khác.
3. **No Restart và Adaptive có độ biến thiên thấp hơn classic restart trên một số ZDT held-out:** tuy nhiên, final IGD/HV của hai biến thể này trùng nhau ở 148/150 cặp bài toán–seed, nên chưa xác nhận đóng góp riêng của adaptive trigger.
4. **Runtime cạnh tranh ở các bản triển khai đã đo:** khoảng 10,8–14,8 giây/lần trên ZDT, 2,74–3,04 giây trên DTLZ4 và 4,42–12,53 giây trên WFG hai mục tiêu. Tỷ lệ nhanh/chậm phụ thuộc mã, phần cứng, thread và tải chạy song song, không phải độ phức tạp độc lập môi trường.
5. **Cập nhật F/CR trực tuyến:** F dùng Lehmer mean làm trơn; CR dùng trung bình cộng làm trơn của con DE được gán rank 1. Xác suất chọn DE theo tỷ phần con DE được sinh, không theo lợi thế thành công DE/SBX; chưa chứng minh không cần tinh chỉnh cấu hình.

<a id="han-che"></a>

## 5. Hạn chế và giới hạn kết luận

- **Thiếu hụt chất lượng ở một số mặt Pareto:** gồm DTLZ2/4 ba mục tiêu, WFG4 và các cấu hình WFG6/9 có số mục tiêu cao. Các giải thích từ mã nguồn vẫn là giả thuyết cần ablation.
- **HV bằng 0 trong nhiều trường hợp khó:** 17/30 lần `dtlz1_m5` và toàn bộ 30 lần `dtlz3_m5` của OADE. Áp lực chọn lọc/crowding saturation là một giải thích đề xuất, chưa phải cơ chế đã xác nhận.
- **Phạm vi bài toán còn giới hạn:** chưa có bằng chứng cho DTLZ5–7, các WFG còn lại, bài toán có ràng buộc hoặc rời rạc; CE/CGDE chưa được thử trên WFG $M=3,5$ trong các bộ này.
- **Baseline cần diễn giải đúng:** một số đối chứng là bản cục bộ hoặc adaptation; chưa đủ căn cứ cho kết luận vượt state of the art.
- **Chưa cô lập đầy đủ đóng góp thành phần:** ablation hỗ trợ periodic OBL trên ZDT4, chưa xác nhận lợi ích riêng của mọi cập nhật thích nghi hay adaptive restart.
- **Bất định và thất bại:** chưa có khoảng tin cậy cho paired effects; cần bổ sung phân tích có xét thất bại, đồng thời giữ rõ định nghĩa structural invalid và quality collapse.
- **Provenance lịch sử chưa đầy đủ:** không thể dùng snapshot môi trường audit để chứng nhận phiên bản tạo dữ liệu cũ. Khối RNSGA2 trên ZDT có manifest thực thi; các khối khác giữ nguồn gốc theo từng đợt, và DTLZ/WFG dùng quy ước ngân sách tìm kiếm riêng.

Xem [kế hoạch thí nghiệm tiếp theo](docs/followup_experiments.md).

<a id="hinh-minh-hoa"></a>

## 6. Hình minh họa và dữ liệu nguồn

Các bản PDF, SVG, PNG và CSV nguồn nằm trong [results/figures/](results/figures/). TIFF dung lượng lớn và PDF overlay chẩn đoán được giữ cục bộ; mã tạo hình và JSON QA có trong nguồn dự án.

| Hình | Nội dung và giới hạn |
|---|---|
| [Tổng quan ZDT + DTLZ](results/figures/integrated_7algo_landscape.png) | Ma trận cỡ hiệu ứng, số kết quả kiểm định và hạng chất lượng. Runtime ở panel c chỉ là proxy từ DTLZ4, không phải tốc độ tổng hợp toàn bộ suite. |
| [Mở rộng số mục tiêu DTLZ](results/figures/dtlz1_4_scaling_diagnosis.png) | IGD của DTLZ1/3, tỷ số IGD DTLZ2 và HV quan sát của DTLZ4; chú thích HV trung vị không phải tỷ lệ lỗi cấu trúc. |
| [WFG hai mục tiêu, 7 thuật toán](results/figures/wfg_m2_7algo_profile.png) | Cỡ hiệu ứng IGD/HV, phân bố IGD WFG9 và runtime đo được của các implementation. |
| [Mở rộng số mục tiêu WFG](results/figures/wfg_scaling_diagnosis.png) | Số kết quả Holm, tỷ số IGD ghép cặp và diễn tiến HV của WFG1/9. |
| [Kết quả kiểm định ZDT v2](results/figures/benchmark_v2_outcome_counts.png) | 58 thắng, 1 không phát hiện khác biệt, 1 thua. |
| [So sánh v1 và v2](results/figures/benchmark_v2_v1_vs_v2_delta.png) | Mức thay đổi IGD giữa hai bộ kết quả; không tự cô lập cơ chế restart. |
| [So sánh ba chế độ restart](results/figures/restart_direct_comparison.png) | Boxplot và dữ liệu từng seed của Classic, No Restart và Adaptive. |
| [Diễn tiến restart](results/figures/restart_convergence.png) | Trung vị IGD và dải IQR theo ngân sách. |
| [Chênh lệch restart ghép cặp](results/figures/restart_confirmation_paired.png) | Phần trăm cải thiện trên 30 seed held-out, 1000–1029. |

[Hồ sơ QA hình](results/figures/figure_qa.md) phân biệt các nhóm hình và phạm vi kiểm tra. Kết quả kiểm tra tự động không thay thế xem hình ở kích thước in hoặc kiểm chứng khoa học.

<a id="cau-truc"></a>

## 7. Cấu trúc dự án và khả năng tái lập

```text
OADE-NSGA-II/
├── algorithms/          # Các bản triển khai đối chứng cục bộ
├── analysis/figures/    # Mã tạo hình R và Python
├── config/              # Giao thức benchmark, tham số và ablation
├── docs/                # Bản thảo, báo cáo, nguồn tham khảo và hướng dẫn
├── results/             # Dữ liệu từng lần chạy, bảng thống kê và hình
├── scripts/             # Runner, inventory và công cụ QA hình
├── src/
│   ├── oade_nsga2/      # Solver OADE và toán tử
│   ├── benchmarking/    # Ngân sách, validation, thống kê và provenance
│   ├── plotting/        # Các lệnh vẽ tích hợp
│   ├── sensitivity/     # Nghiên cứu độ nhạy
│   └── utils/           # Đọc cấu hình và CSV
├── tests/               # Kiểm thử thuật toán/giao thức/provenance
└── renv.lock            # Snapshot thư viện R hiện có
```

Run mới ghi manifest gồm cấu hình đã giải quyết, hash mã nguồn, môi trường và checksum CSV. Resume/reuse kiểm tra dữ liệu trước khi tiếp tục; fresh run từ chối ghi đè kết quả đã có. Dữ liệu lịch sử chỉ được lập inventory, không được chứng nhận ngược bằng môi trường hiện tại.

Test, YAML smoke, mã hình, lockfile và JSON QA được đưa vào hồ sơ nguồn. Cache, đầu ra smoke, TIFF và overlay PDF là artifact cục bộ. Xem [hướng dẫn tái lập](docs/reproducibility.md) và [danh mục thí nghiệm](docs/experiment_registry.md).

<a id="huong-dan"></a>

## 8. Hướng dẫn chạy

### Cài môi trường và kiểm thử

Cần Python 3.10 trở lên. Chạy từ thư mục gốc dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

### Chạy mới ZDT v2, đủ 7 thuật toán

Lệnh này lên lịch 1.050 lần chạy. Dùng thư mục đầu ra mới để giữ nguyên bằng chứng lịch sử:

```powershell
.venv\Scripts\python.exe main.py benchmark --config config/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2
```

### Chạy DTLZ1–4 với 2, 3 và 5 mục tiêu

```powershell
$env:OMP_NUM_THREADS=1
$env:OPENBLAS_NUM_THREADS=1
$env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-dtlz --config config/dtlz1_4_benchmark.yaml --out-dir results/reproduction_dtlz --jobs 8
```

### Chạy compact WFG và WFG hai mục tiêu đủ 7 thuật toán

```powershell
$env:OMP_NUM_THREADS=1
$env:OPENBLAS_NUM_THREADS=1
$env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_compact_benchmark.yaml --out-dir results/reproduction_wfg_compact --jobs 8
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_m2_7algo_benchmark.yaml --out-dir results/reproduction_wfg_m2 --jobs 10
```

### Tiếp tục một lần chạy có manifest phù hợp

```powershell
.venv\Scripts\python.exe main.py benchmark --config config/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2 --resume
```

Resume theo đơn vị bài toán đã hoàn tất và từ chối dữ liệu không khớp cấu hình/môi trường/checksum. Không tự gán manifest mới cho CSV lịch sử để vượt kiểm tra.

### Tạo biểu đồ tổng hợp tích hợp

```powershell
.venv\Scripts\python.exe main.py plot-algorithm-benchmark
.venv\Scripts\python.exe main.py plot-convergence
```

Các lệnh vẽ tích hợp dùng cấu hình/đường dẫn đầu vào của chúng; không tự chuyển sang thư mục reproduction chỉ vì vừa chạy benchmark ở đó. Mã tạo bộ hình báo cáo nằm trong `analysis/figures/`; xem hướng dẫn tái lập trước khi cập nhật hình đã lưu.

<a id="tai-lieu"></a>

## Tài liệu nghiên cứu và trích dẫn

- [Bản thảo tổng hợp](docs/manuscript.md) và [mục lục tài liệu](docs/index.md).
- [Nguồn tham khảo BibTeX](docs/references.bib) và [định danh baseline](docs/baselines.md).
- [Báo cáo ZDT v2](docs/benchmark_v2_results_report.md).
- [Báo cáo tích hợp ZDT + DTLZ1–4](docs/dtlz1_4_integrated_report.md).
- [Báo cáo compact WFG và WFG hai mục tiêu](docs/wfg_compact_report.md).
- [Ablation thành phần](docs/ablation_results_report.md).
- [Xác nhận restart trên seed held-out](docs/restart_confirmation_report.md).
- [Độ nhạy tham số của cấu hình classic](docs/sensitivity_analysis.md).

Khi trích dẫn hoặc sử dụng kết quả, nêu đúng phiên bản cấu hình, implementation đối chứng và giới hạn giao thức. Giấy phép phát hành của dự án chưa được xác định trong hồ sơ hiện tại.
