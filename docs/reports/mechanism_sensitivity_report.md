# Độ nhạy tham số cơ chế OADE: kết quả và kết luận mới trên ZDT4/ZDT6

**Ngày phân tích: 19/11/2026.** Bộ dữ liệu `mechanism_sensitivity_v1`, 2.100 lượt chạy đã hoàn tất. Báo cáo phân tích dữ liệu hiện có, không chạy lại tối ưu và không sửa cấu hình production. [Giao thức](../protocols/mechanism_sensitivity.md) · [Audit độc lập](../../results/experiments/mechanism_sensitivity_v1/derived/audit.json) · [Phụ lục toàn bộ bảng](mechanism_sensitivity_tables.md).

## Kết luận chính

Độ nhạy quan sát được tập trung ở tỷ lệ OBL và các mức giữ cố định của mean F, mean CR, pDE; không có bằng chứng rằng một mức thay thế cải thiện đồng đều hai bài toán. Trong **124 endpoint sau Holm**, mức tham chiếu tốt hơn ở **15**, mức thử tốt hơn ở **5**, và **104 chưa phát hiện khác biệt**. Endpoint là bài × mức thử so với tham chiếu × chỉ số; các endpoint dùng chung tham chiếu không phải các thí nghiệm độc lập.

Ba kết luận mới có thể bảo vệ là:

1. Trên ZDT4, giảm `obl_jump_rate` từ 0,2 xuống 0,05 làm giảm chất lượng ở cả IGD/HV; trong các so sánh F giữ cố định, mean F=0,5 tốt hơn mốc 0,65 ở cả hai chỉ số.
2. Trên ZDT6, mean F thấp 0,4–0,5 có những bất lợi so với mốc 0,65; mean CR=0,3 và pDE=0,8 cải thiện riêng HV so với các mốc held tương ứng. Không kết luận cải thiện cả IGD/HV khi chỉ HV đạt ngưỡng.
3. Các ngưỡng restart có thể làm thay đổi mạnh số lần kích hoạt trên ZDT6, nhưng chưa tạo ra khác biệt IGD/HV đạt ngưỡng Holm. Trên ZDT4, nhóm full và các mức tham số restart đã thử không có restart hoàn tất; do đó chưa đánh giá được lợi ích khi cơ chế thực sự hoạt động ở bài này.

## 1. Thiết kế và đơn vị phân tích

Đo 10 tham số theo OFAT: mỗi cấu hình chỉ thay một tham số. Có 35 cấu hình duy nhất, gồm full production, 3 mốc held và 31 mức khác mốc; mỗi cấu hình chạy trên ZDT4/ZDT6 (D=10, M=2), 30 seed **7000–7029**, quần thể 100 và cap 20.000 FE. Tổng thực dùng **41.898.954 FE**; không vượt cap từng lượt. Khởi tạo uniform và hash quần thể ban đầu khớp giữa các cấu hình trong từng block bài/seed.

Đơn vị thực nghiệm là lượt chạy theo seed. Mỗi phép so sánh có **n=30 cặp hợp lệ**, không loại seed, không thay thế lượt lỗi và không lọc outlier. Cá thể, thế hệ và sự kiện restart không được coi là replicate để tăng n. Không có dữ liệu sinh học hay train/test split. Việc chọn bài và các mức là thiết kế thăm dò có chủ đích; không phải lấy mẫu ngẫu nhiên toàn không gian bài toán/tham số hay đăng ký trước trên một registry bên ngoài.

### Phải phân biệt hai loại mốc

| Nhóm | Cách thay giá trị | Mốc kiểm định |
|---|---|---|
| OBL, ngưỡng restart, số láng giềng | Gán mức tham số tĩnh; các cơ chế khác như production | `full` production |
| mean F | Giữ riêng mean F ở mức thử; CR/pDE vẫn thích nghi | Mean F=0,65 held |
| mean CR | Giữ riêng mean CR ở mức thử; F/pDE vẫn thích nghi | Mean CR=0,5 held |
| pDE | Giữ riêng xác suất chọn DE ở mức thử; F/CR vẫn thích nghi | pDE=0,5 held |

Mean F/CR là trung bình phân phối lấy mẫu của DE, không phải F/CR của mọi offspring đều bằng giá trị đó. Held áp dụng cả sau bước cập nhật và restart. Các mốc held không đồng nhất với full adaptive. Bộ 124 kiểm định **không trực tiếp kiểm định full adaptive với từng mốc held**, và không so mọi cặp mức với nhau. Vì vậy không gọi F=0,5 là “tốt hơn cơ chế thích nghi” hoặc là mức tối ưu toàn cục từ nghiên cứu này.

[Cấu hình thực thi](../../config/studies/mechanism_sensitivity.yaml) quy định các mức: OBL interval 5/10/20/40; jump rate 0,05/0,1/0,2/0,4; patience 5/10/20/40; tolerance 10⁻⁵/10⁻⁴/10⁻³; diversity threshold 0,01/0,02/0,05/0,1; elite ratio 0,8/0,9/0,95; neighbors 3/5/10/20; mean F 0,4/0,5/0,65/0,8/0,9; mean CR 0,1/0,3/0,5/0,7/0,9; pDE 0,2/0,35/0,5/0,65/0,8. Tham số tĩnh vẫn giữ mức đã gán suốt lượt, dù trường cấu hình ghi `initial`.

## 2. Phương pháp thống kê và kiểm chứng

IGD thấp tốt hơn, HV cao tốt hơn. Wilcoxon signed-rank **hai phía** theo cặp seed, `zero_method=wilcox`, `method=auto`; toàn bộ chênh lệch bằng 0 cho statistic=0, p=1. Holm áp dụng **chung 124 endpoint**, alpha=0,05. Không đổi họ kiểm định sau khi thấy kết quả. Median chênh lệch lưu theo **tham chiếu − mức thử**: IGD dương hoặc HV âm thiên về mức thử. Rank-biserial dương thiên về tham chiếu; đây là hiệu ứng thứ hạng, không phải phần trăm cải thiện.

Audit bổ sung bootstrap 20.000 lần lấy lại mẫu **cặp seed trong từng bài và contrast**, seed bootstrap 20261119, percentile CI 95% cho median chênh lệch. Các CI này được thêm ở bước phân tích, **chưa hiệu chỉnh đa kiểm định** và không thay thế quyết định Holm. Wilcoxon không tự động kiểm định median khi phân bố chênh lệch bất đối xứng; CI median và p-value có thể khác thông điệp vì nhắm đại lượng khác nhau. Mean ± SD mẫu, median và Q1–Q3 ở phụ lục là mô tả phân bố, không phải CI của mean.

[Script audit](../../analysis/audit_mechanism_sensitivity.py) đọc primary trực tiếp, không gọi solver hoặc helper thống kê pipeline. Đã xác nhận:

- Đủ 2.100 task duy nhất và checksum primary; 21 hash source khớp checkout.
- Final X/F hữu hạn, trong bounds, có nhiều hơn một điểm mục tiêu phân biệt và không bị trội. Tính lại F từ X và IGD/HV từ F có sai số lớn nhất **0**; reference snapshot khớp reference giải tích hiện tại.
- 2.100 dòng runs, 70 dòng summary, 124 Wilcoxon/effect/Holm và 4.200 dòng activation khớp khi tính lại; không mất cặp.
- Hash khởi tạo khớp trong 60 block bài/seed; giá trị held trong các trace lưu tuân thủ mức đã gán. Hash ban đầu chưa được tái dựng độc lập từ quá trình khởi tạo.
- Đổi source giữa lúc chạy chỉ ở `atomic_json` để retry lỗi khóa file Windows; audit AST xác nhận toàn bộ mã ngoài hàm này giống bản snapshot trước sửa. Manifest giữ hash cũ, hash mới và lịch sử recovery; không coi đây là hai phiên bản thuật toán tìm kiếm.

Đường phân tích độc lập vẫn do cùng tác nhân thực hiện và dùng pymoo cho bài toán/chỉ số, không phải tái lập bởi nhóm khác hay triển khai toán học thứ hai. Audit không kiểm lại mọi dòng của CSV trace/events hoặc từng bước chuyển trạng thái solver. Checksum xác nhận tính nhất quán với manifest đang lưu, không thay thế kho lưu trữ bất biến bên ngoài.

## 3. Kết quả theo từng tham số

Xem [bộ 12 biểu đồ: chênh lệch theo cặp và phân bố theo mức tham số](mechanism_sensitivity_figures.md). Các hình giữ đủ 30 seed mỗi nhóm và toàn bộ 124 endpoint, có mốc full/held riêng tương ứng.

| Tham số | Mốc tốt hơn | Mức thử tốt hơn | Chưa phát hiện khác biệt | Tổng endpoint |
|---|---:|---:|---:|---:|
| OBL interval | 0 | 0 | 12 | 12 |
| OBL jump rate | 2 | 0 | 10 | 12 |
| Stagnation patience | 0 | 0 | 12 | 12 |
| Stagnation tolerance | 0 | 0 | 8 | 8 |
| Diversity threshold | 0 | 0 | 12 | 12 |
| Restart elite ratio | 0 | 0 | 8 | 8 |
| Số láng giềng | 0 | 0 | 12 | 12 |
| Mean F held | 7 | 3 | 6 | 16 |
| Mean CR held | 3 | 1 | 12 | 16 |
| pDE held | 3 | 1 | 12 | 16 |
| **Tổng** | **15** | **5** | **104** | **124** |

### 3.1. Giảm tỷ lệ OBL quá thấp gây bất lợi trên ZDT4

Full có IGD median 0,00541441 và HV median 0,867651 trên ZDT4. Với jump rate=0,05, các median tương ứng là 0,0721610 và 0,762704. Median chênh lệch theo cặp là −0,0373494 cho IGD, +0,0603558 cho HV, thiên về full; p Holm lần lượt **0,00506871** và **0,00691528**. Đây là chênh lệch median theo cặp, không phải hiệu của hai median nhóm vừa nêu.

Các mức jump rate còn lại và interval 5/20/40 chưa tạo ra endpoint đạt ngưỡng sau Holm. Kết quả hỗ trợ việc tránh giảm mạnh jump rate xuống 0,05 trong cấu hình ZDT4 đang đo, nhưng không chứng minh 0,2 là mức tối ưu, cũng không chứng minh mọi interval đã thử tương đương nhau.

### 3.2. Mean F thể hiện đánh đổi giữa hai bài

Trên ZDT4, F=0,5 held tốt hơn F=0,65 held ở cả IGD/HV; F=0,4 chỉ có HV đạt ngưỡng. Ngược lại, F=0,8 và 0,9 kém mốc 0,65 ở cả hai chỉ số. F median sampling thấp hơn vì thế là hướng kiểm tra tiếp có căn cứ cho ZDT4, nhưng các mức 0,4 và 0,5 chưa được kiểm định trực tiếp với nhau trong họ này.

Trên ZDT6, F=0,5 kém mốc 0,65 ở IGD và HV (p Holm **0,00620778** và **0,00506871**); F=0,4 kém ở HV (p Holm **0,00506871**). Các so sánh còn lại của nhóm F trên bài này chưa đạt ngưỡng. Sự đảo chiều của các so sánh F=0,5 cho thấy một quy tắc “giảm F chung cho cả hai bài” không được kết quả hiện tại hỗ trợ. Đây là mô tả theo bài; nghiên cứu chưa thực hiện kiểm định tương tác bài × mức F.

### 3.3. Mean CR và pDE: cải thiện HV không đồng nghĩa cải thiện toàn bộ chất lượng

Trên ZDT6, CR=0,3 held cải thiện HV so với CR=0,5 held, p Holm **0,0483112**. Kết quả sát ngưỡng và IGD chưa phát hiện khác biệt; không mô tả là cải thiện mạnh hoặc chắc chắn bền vững. CR=0,7 kém mốc ở HV; CR=0,9 kém ở IGD/HV. Trên ZDT4, không so sánh CR nào đạt ngưỡng Holm.

pDE=0,8 held cải thiện HV trên ZDT6 so với pDE=0,5 held, nhưng IGD chưa đạt ngưỡng. pDE=0,2 kém mốc trên cả IGD/HV của ZDT4 và trên HV của ZDT6. Điều này giới hạn ý tưởng giảm mạnh tỷ trọng DE; không chứng minh pDE=0,8 là tốt nhất, không thay thế bằng chứng riêng cho quy tắc thích nghi pDE và không loại trừ tương tác với F/CR.

### 3.4. Quy mô và độ bất định của năm endpoint cải thiện

Tất cả n=30 cặp. Δ là median(tham chiếu − mức thử); CI 95% percentile chưa hiệu chỉnh. “Thắng” là số seed mức thử có giá trị tốt hơn, không phải số kiểm định độc lập.

| Bài | Mức held so với mốc held | Chỉ số | Δ [CI 95%] | p Holm | Mức thử thắng |
|---|---|---|---:|---:|---:|
| ZDT4 | F=0,4 so với 0,65 | HV | −0,000751206 [−0,00134134; −0,000321143] | 0,0133204 | 23/30 |
| ZDT4 | F=0,5 so với 0,65 | IGD | +0,000351941 [+0,000183816; +0,000538227] | 0,00556463 | 25/30 |
| ZDT4 | F=0,5 so với 0,65 | HV | −0,000808642 [−0,00143827; −0,000645271] | 9,69134×10⁻⁶ | 27/30 |
| ZDT6 | CR=0,3 so với 0,5 | HV | −0,000322267 [−0,000515928; −0,000156290] | 0,0483112 | 23/30 |
| ZDT6 | pDE=0,8 so với 0,5 | HV | −0,000490150 [−0,000773863; −0,000320682] | 3,03667×10⁻⁵ | 28/30 |

Chênh lệch HV ở nhóm tốt có thể nhỏ về trị tuyệt đối dù hiệu ứng thứ hạng lớn. Không quy đổi thành phần trăm chất lượng tổng thể và không cộng các cải thiện của F/CR/pDE để dự đoán một cấu hình kết hợp.

## 4. Telemetry: ngưỡng thay đổi hoạt động restart nhưng chưa chứng minh lợi ích chất lượng

Trên **ZDT4**, full và toàn bộ cấu hình thay một trong bốn tham số restart có **0/30 seed** với restart hoàn tất. Chưa phát hiện khác biệt chất lượng trong các so sánh đó không phải bằng chứng restart vô ích hoặc ngưỡng đã tối ưu; đường tác động thông qua restart hoàn tất chưa được tạo ra trong các lượt này.

Trên **ZDT6**, có sự thay đổi hành vi rõ ràng:

| Thiết lập | Seed có restart hoàn tất / 30 | Tổng restart hoàn tất |
|---|---:|---:|
| Full: patience=20, diversity threshold=0,02 | 6 | 8 |
| Patience=5 | 19 | 102 |
| Patience=10 | 10 | 23 |
| Patience=40 | 0 | 0 |
| Diversity threshold=0,01 | 0 | 0 |
| Diversity threshold=0,05 | 28 | 91 |
| Diversity threshold=0,1 | 30 | 105 |

Mỗi dòng chỉ đổi tham số nêu trong dòng. Toàn bộ so sánh IGD/HV của bốn nhóm tham số restart đều chưa đạt ngưỡng Holm. Số sự kiện là mô tả telemetry trong 30 lượt, không được dùng làm n=102 hay n=105. Việc tăng activation không bảo đảm chất lượng cuối lượt tốt hơn dưới cap FE, vì FE dành cho restart thay thế một phần ngân sách tìm kiếm khác. Đây là cách giải thích phù hợp với thiết kế, chưa phải một phân tích trung gian nhân quả hoặc phép thử tương đương chất lượng.

Đủ 140 dòng tổng hợp activation, bao gồm OBL/restart cho 70 nhóm, nằm trong [bảng telemetry đã audit](../../results/experiments/mechanism_sensitivity_v1/derived/audited_activation_summary.csv).

## 5. Quan hệ với các kết quả trước

[Ablation 480 lượt](mechanism_zdt46_report.md) hỏi việc tắt/thay một cơ chế trong hệ đầy đủ ảnh hưởng thế nào. Bộ mới hỏi việc đổi **mức số** của một tham số, dùng seed mới và mốc held theo từng tham số thích nghi. Hai thiết kế bổ sung nhau nhưng không phải lặp lại cùng giả thuyết.

Kết quả OBL trên ZDT4 nhất quán về hướng: bộ trước cho thấy tắt OBL gây bất lợi, bộ mới cho thấy giảm jump rate quá thấp cũng gây bất lợi. Tuy nhiên, không dùng hai bộ để suy ra quan hệ liều–đáp ứng đơn điệu hoặc ngưỡng tối ưu. Bộ mới mở rộng mô tả restart trên ZDT6: không chỉ ít activation ở cấu hình full, mà các ngưỡng khác có thể tạo nhiều activation hơn mà vẫn chưa phát hiện lợi ích chất lượng theo họ kiểm định hiện tại.

Việc F=0,5 held tốt hơn F=0,65 held trên ZDT4 không trực tiếp xác nhận lại kết luận “tắt thích nghi F/CR tốt hơn full” của ablation trước, vì các đối chứng và can thiệp khác nhau. Tương tự, pDE=0,8 held cải thiện HV không đồng nhất với phép so DE-only ở bộ trước. Không gộp 28 và 124 endpoint hoặc gộp seed của hai nghiên cứu để tạo một p-value chung.

[Đối chứng bảy thuật toán ZDT v2](zdt_seven_fixed_oade_v2_report.md) vẫn là bằng chứng riêng cho chất lượng so với baseline. Nghiên cứu tham số này không chạy lại NSGA2 hoặc các đối thủ, nên không cập nhật con số 56/60 của benchmark và không chứng minh ưu thế của một cấu hình mới so với chúng.

## 6. Chi phí, giới hạn và quyết định kỹ thuật

Tất cả lượt dùng 8 worker theo primary và lịch sử execution sessions. Manifest lưu OMP/OPENBLAS/MKL chưa đặt, không được mô tả là đã cố định 1 luồng thư viện. Run runtime bao gồm telemetry và thuộc môi trường chạy song song, có lần gián đoạn/khôi phục; chỉ dùng mô tả chi phí quan sát, không suy ra độ phức tạp hoặc so trực tiếp với benchmark trước. Full có runtime median khoảng 5,33 s trên ZDT4 và 3,78 s trên ZDT6. Bảng source giữ runtime/FE cho từng nhóm, không dùng runtime để chọn mức thắng.

Nghiên cứu chỉ xét hai bài ZDT, 30 seed/mức và các mức rời rạc đã chọn. OFAT không xác định tương tác, cấu hình kết hợp hoặc tối ưu liên tục; việc thay mức cũng thay đường tìm kiếm và phân bổ FE. 104 endpoint NS không chứng minh độ bền tham số trên toàn không gian, và không thể suy ra hai bài khác nhau có tương tác chỉ vì một bài có p<0,05 còn bài kia không. Chưa có dữ liệu DTLZ/WFG hiện hành hoặc xác nhận trên tập seed độc lập thứ hai cho các mức được chú ý sau phân tích.

**Quyết định hiện tại:** giữ production làm mốc có phiên bản; không tự đổi F, CR, pDE từ bảng này. Nếu triển khai bước xác nhận, khóa trước giả thuyết cho F thấp trên ZDT4 và pDE cao trên ZDT6, giữ đối chứng full adaptive, dùng seed mới và họ kiểm định riêng đã định trước. Nếu mục tiêu là đề xuất một cấu hình chung, cần kiểm tra trực tiếp các tổ hợp có căn cứ và đánh đổi giữa bài; không ghép tùy ý các mức thắng từ OFAT.

## 7. Đoạn kết luận dùng cho bản thảo

Trong nghiên cứu OFAT gồm 2.100 lượt chạy trên ZDT4 và ZDT6, tác động của các mức tham số OADE phụ thuộc vào bài toán, chỉ số và chế độ giữ tham số. Sau hiệu chỉnh Holm cho 124 endpoint, mức thử cải thiện năm endpoint, mức tham chiếu tốt hơn ở 15 endpoint và 104 endpoint chưa phát hiện khác biệt. Mean F=0,5 được giữ cố định cải thiện IGD và HV so với mean F=0,65 giữ cố định trên ZDT4, nhưng gây bất lợi trên ZDT6; các cải thiện còn lại chỉ xuất hiện ở HV của những so sánh cụ thể. Thay đổi ngưỡng restart làm tăng mạnh số lần kích hoạt trên ZDT6 mà chưa tạo ra lợi ích chất lượng đạt ngưỡng thống kê. Các kết quả này xác định những hướng xác nhận có mục tiêu và giới hạn của cấu hình hiện tại, thay vì thiết lập một bộ tham số tối ưu chung hoặc chứng minh lợi ích độc lập của mọi cơ chế thích nghi.

## Tệp nguồn và tái tạo

- [Audit JSON](../../results/experiments/mechanism_sensitivity_v1/derived/audit.json): số kiểm tra, sai số, hash manifest và môi trường phân tích.
- [70 nhóm mean/SD/median/IQR/min/max](../../results/experiments/mechanism_sensitivity_v1/derived/audited_summary.csv).
- [124 endpoint có statistic/p/effect/CI và thắng–thua](../../results/experiments/mechanism_sensitivity_v1/derived/audited_comparisons.csv), gồm cả 104 endpoint NS.
- [Telemetry tổng hợp](../../results/experiments/mechanism_sensitivity_v1/derived/audited_activation_summary.csv).
- [Phụ lục bảng đọc trực tiếp](mechanism_sensitivity_tables.md).

```powershell
.\.venv\Scripts\python.exe analysis/audit_mechanism_sensitivity.py
.\.venv\Scripts\python.exe analysis/report_mechanism_sensitivity_tables.py
```

Lệnh chỉ tạo lại các dẫn xuất audit/phụ lục. Primary, manifest, kết quả kiểm định gốc và source thuật toán không bị sửa. Môi trường phân tích: Python 3.14.7, NumPy 2.5.4, SciPy 1.18.1; phiên bản thực thi và các source hash đầy đủ nằm trong manifest.
