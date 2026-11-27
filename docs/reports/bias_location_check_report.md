# Ưu thế của OADE trên ZDT phụ thuộc vị trí nghiệm tối ưu

Ngày phân tích: 27/11/2026. Hai vòng chạy mới, tổng **3.720 lượt, không có lượt lỗi**. [Giao thức](../protocols/bias_location_check.md) · [Manifest vòng xác nhận](../../results/experiments/bias_location_confirm_v1/manifest.json) · [Bảng kết quả tự sinh](../../results/experiments/bias_location_confirm_v1/report.md).

## Kết luận chính

Khi dời nghiệm tối ưu của ZDT vào bên trong miền mà giữ nguyên Pareto front:

1. **Ưu thế của OADE so với NSGA-II trên ZDT1/2/3 đảo chiều.** Ở bài gốc OADE tốt hơn có ý nghĩa; ở cả ba vectơ dịch chuyển, NSGA-II tốt hơn có ý nghĩa ở cả IGD và HV.
2. **Lợi ích của OBL trên ZDT4 chủ yếu đến từ việc nghiệm tối ưu nằm ở tâm miền.** Lợi ích giảm từ khoảng 80 lần xuống mức không có ý nghĩa. Trên các bài còn lại, OBL không tạo khác biệt.
3. **Sửa biên bằng clip chỉ tạo lợi thế nhỏ, riêng trên ZDT6 gốc**; nó không giải thích được ưu thế của OADE trên ZDT1/2/3.
4. **ZDT6 là ngoại lệ:** ưu thế của OADE vẫn giữ, và còn lớn hơn, sau khi dịch chuyển.

Vòng xác nhận dùng seed mới, đủ năm bài và ba vectơ dịch chuyển; chiều kết quả khớp với vòng thăm dò. Kết luận chính trong [báo cáo sáu thuật toán](zdt_six_fixed_oade_report.md) (44/50 endpoint có lợi cho OADE) vì vậy phần lớn gắn với cấu trúc của bộ ZDT, chưa thể khái quát cho bài có nghiệm tối ưu nằm trong miền.

## 1. OADE so với NSGA-II

Ô là median theo seed của IGD(NSGA-II)/IGD(OADE); lớn hơn 1 nghĩa là OADE tốt hơn. Ký hiệu IGD/HV sau Holm chung 160 endpoint: `+` OADE tốt hơn, `−` NSGA-II tốt hơn, `≈` NS. Trong ngoặc là số seed OADE có IGD tốt hơn.

| Bài | Bài gốc | Dịch chuyển A | Dịch chuyển B | Dịch chuyển C |
|---|---|---|---|---|
| ZDT1 | 1,17 (+/+, 29/30) | 0,66 (−/−, 0/30) | 0,63 (−/−, 0/30) | 0,65 (−/−, 0/30) |
| ZDT2 | 1,12 (+/+, 28/30) | 0,79 (−/−, 1/30) | 0,79 (−/−, 3/30) | 0,80 (−/−, 0/30) |
| ZDT3 | 1,06 (+/+, 25/30) | 0,59 (−/−, 0/30) | 0,60 (−/−, 0/30) | 0,61 (−/−, 0/30) |
| ZDT4 | 2,13 (≈/≈, 23/30) | 0,048 (−/−, 2/30) | 0,042 (−/−, 1/30) | 0,035 (−/−, 1/30) |
| ZDT6 | 4,01 (+/+, 30/30) | 6,98 (+/+, 30/30) | 7,30 (+/+, 30/30) | 7,29 (+/+, 30/30) |

Cả 15 kiểm định tương tác (bài gốc so với từng vectơ) đều có ý nghĩa sau Holm chung 60 kiểm định, p Holm ≤ 4,4×10⁻⁷. Trên ZDT1/2/3, OADE chuyển từ tốt hơn 6–17% sang kém hơn 20–40%. Trên ZDT4 dịch chuyển, NSGA-II có median IGD khoảng 0,01, còn OADE khoảng 0,26–0,29.

## 2. OBL định kỳ

| Bài | Bài gốc: IGD(noOBL)/IGD(OADE) | Dịch chuyển A / B / C |
|---|---|---|
| ZDT4 | **80,7** (+/+, 29/30; p Holm 5×10⁻⁷) | 1,90 / 1,54 / 1,35 (≈/≈ cả ba) |
| ZDT1/2/3/6 | 0,99–1,01 (≈/≈) | 0,91–1,00 (≈/≈ cả mười hai) |

Tương tác trên ZDT4 có ý nghĩa ở cả ba vectơ (p Holm ≤ 6,1×10⁻⁷). Kết quả này giải thích vì sao [nghiên cứu cơ chế 480 lượt](mechanism_zdt46_report.md) thấy tắt OBL gây bất lợi lớn trên ZDT4 nhưng không có tác dụng trên ZDT6: trên ZDT4, phép phản chiếu tĩnh x' = −x giữ nguyên các điểm gần nghiệm tối ưu ở tâm miền.

Hệ quả: khi nghiệm tối ưu không ở tâm, OADE kẹt ở front cục bộ trong gần như mọi lượt.

| ZDT4, số lượt IGD > 10⁻² / 30 | OADE | OADE_random | OADE_bounce | OADE_noOBL | NSGA2 |
|---|---:|---:|---:|---:|---:|
| Bài gốc | 6 | 22 | 25 | 30 | 17 |
| Dịch chuyển A | 29 | 30 | 30 | 29 | 16 |
| Dịch chuyển B | 29 | 29 | 30 | 30 | 13 |
| Dịch chuyển C | 29 | 30 | 30 | 30 | 11 |

## 3. Sửa biên của DE

So với `OADE_random` (gene vượt biên được lấy lại ngẫu nhiên trên toàn miền, không kéo về biên):

| Bài | Bài gốc: IGD(random)/IGD(OADE) | Dịch chuyển A / B / C | Tương tác |
|---|---|---|---|
| ZDT1 | 1,01 (≈/≈) | 1,04 / 1,01 / 1,06 | NS cả ba |
| ZDT2 | 1,00 (≈/+) | 1,14 / 1,06 / 1,11 | Có ý nghĩa ở A, C |
| ZDT3 | 0,96 (≈/≈) | 1,06 / 1,01 / 1,06 | NS cả ba |
| ZDT4 | 4,52 (+/+, 27/30) | 1,63 / 1,69 / 1,31 (≈/≈) | Có ý nghĩa ở C |
| ZDT6 | 1,20 (+/+, 28/30) | 0,97 / 0,93 / 0,99 (≈/≈) | Có ý nghĩa cả ba |

- **ZDT6:** clip tạo lợi thế khoảng 20% chỉ khi nghiệm tối ưu nằm trên biên. Đây là lợi thế nhân tạo nhưng nhỏ so với ưu thế 4–7 lần của OADE trước NSGA-II trên bài này.
- **ZDT1/2/3:** clip không tạo khác biệt ở bài gốc, nên không phải nguyên nhân của ưu thế. Trên ZDT2 dịch chuyển, clip còn tốt hơn `OADE_random` khoảng 10%, ngược chiều với giả thuyết.
- **ZDT4:** clip tốt hơn rõ ở bài gốc, nhưng tương tác chỉ có ý nghĩa ở một trong ba vectơ, nên chưa kết luận.
- Nhánh `OADE_bounce` cho kết quả cùng chiều; trên ZDT4 nó kém OADE ở cả bài gốc và bài dịch chuyển. [Bảng đầy đủ](../../results/experiments/bias_location_confirm_v1/report.md).

Thí nghiệm chưa xác định được thành phần nào làm ưu thế của OADE trên ZDT1/2/3 phụ thuộc vị trí nghiệm tối ưu: không phải clip, cũng không phải OBL.

## 4. Đối chiếu với vòng thăm dò

Vòng thăm dò (720 lượt, seed 9000–9029, ZDT1/4/6, một vectơ dịch chuyển) cho cùng chiều ở mọi kết luận chính:

| Kết quả | Thăm dò | Xác nhận |
|---|---|---|
| OADE/NSGA-II trên ZDT1: gốc → dịch chuyển | 1,16 → 0,62 | 1,17 → 0,63–0,66 |
| OBL trên ZDT4: gốc → dịch chuyển | 49,6 → 2,0 (NS) | 80,7 → 1,35–1,90 (NS) |
| OADE/NSGA-II trên ZDT6: gốc → dịch chuyển | 4,28 → 7,42 | 4,01 → 6,98–7,30 |
| Clip so với bounce trên ZDT1 gốc | NS | NS |

[Bảng vòng thăm dò](../../results/experiments/bias_location_exploratory_v1/report.md).

## 5. Giới hạn

- Với ZDT1/2/3/6, phép dịch chuyển |x − o| tạo một điểm gãy tại nghiệm tối ưu. Chưa tách hoàn toàn được ảnh hưởng của vị trí nghiệm tối ưu với ảnh hưởng của điểm gãy. Riêng ZDT4 là phép dịch thuần túy.
- Chỉ có một mức ngân sách (20.000 FE), quần thể 100 và 30 seed mỗi nhóm.
- NSGA-II mặc định của pymoo là đối chứng ngoài duy nhất; chưa chạy lại GDE3, NSDE hay CGDE.
- Các giả thuyết được hình thành sau khi đọc mã. Vòng xác nhận cố định giả thuyết và họ kiểm định trong docstring của script trước khi chạy, nhưng không đăng ký trước ở nơi bên ngoài.
- Kiểm định tương tác so sánh hai nhóm khác bài, nên dùng Mann–Whitney không ghép cặp; seed trùng nhau giữa bài gốc và bài dịch chuyển không được coi là cặp.
- Chưa có audit bằng đường tính riêng như các nghiên cứu khác; script tự kiểm tra ngân sách, tính hợp lệ của front và đánh giá lại F từ X (sai số lớn nhất bằng 0).

## 6. Hệ quả cho dự án

1. Cần bổ sung benchmark có nghiệm tối ưu nằm bên trong miền (ZDT/DTLZ dịch chuyển, WFG, UF của CEC 2009) trước khi công bố ưu thế của OADE.
2. Không nên trình bày OBL định kỳ như một đóng góp nếu chưa có bằng chứng ngoài ZDT4 gốc.
3. Nên giữ ZDT6 làm bằng chứng mạnh nhất cho OADE.
4. Báo cáo sáu thuật toán và README cần nêu giới hạn này khi diễn giải 44/50 endpoint.
