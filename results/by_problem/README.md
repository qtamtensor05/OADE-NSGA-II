# Hồ sơ nghiên cứu theo bài toán

Ưu tiên nghiên cứu hiện tại: **ZDT1, ZDT2, ZDT3, ZDT4, ZDT6**. Không có dữ liệu ZDT5 trong các đợt được tuyển chọn.

| Bộ bài toán | Vai trò | Hồ sơ |
|---|---|---|
| ZDT | Trọng tâm: benchmark 7 thuật toán classic/adaptive, xác nhận restart, ablation, độ nhạy | [ZDT](zdt/README.md) |
| DTLZ | Bằng chứng mở rộng hiện có, tiếp tục chạy và bổ sung | [DTLZ](dtlz/README.md) |
| WFG | Bằng chứng mở rộng hiện có, tách benchmark M=2 và scaling | [WFG](wfg/README.md) |

Mỗi hồ sơ có thư mục `reports/` chứa báo cáo Markdown riêng cho từng nhóm thí nghiệm, với bảng số liệu chỉ của bài toán tương ứng. ZDT có thêm `reports/classic_vs_adaptive.md`. Báo cáo được tái tạo cùng dữ liệu khi chạy script.

Mỗi bài toán có thư mục thí nghiệm riêng, README, CSV đã lọc và manifest SHA-256. [coverage.csv (ZIP)](csv_results.zip) thống kê số dòng raw theo bài toán/đợt, không phải tổng lượt thực thi độc lập.

Nguồn gốc và đường dẫn thực thi giữ nguyên; đây là lớp tổ chức để đọc và phân tích. Không lấy smoke, correction trung gian hoặc benchmark legacy làm bằng chứng chính. Các báo cáo/hình nhiều bài toán được liên kết thay vì sao chép và đổi nhãn thành hình riêng.

ZDT: benchmark classic/adaptive mỗi bộ 1.050 dòng (5 × 7 × 30), dùng chung 6 block đối chứng; restart confirmation 450 dòng; adaptive OFAT 2.850 dòng duy nhất. Sensitivity classic là bằng chứng lịch sử riêng.

Tái tạo sau khi bổ sung dữ liệu: `python scripts/organize_by_problem.py`. Thêm nguồn nghiên cứu mới vào `SOURCES` của script; mọi bài toán xuất hiện trong cột `problem` sẽ được tách vào đúng bộ. Nguồn chưa có CSV derived sẽ chưa được đánh dấu có kết quả. Không dùng thư mục này làm nơi ghi checkpoint của các lượt đang chạy.

[Tải CSV dạng ZIP và hướng dẫn khôi phục](../CSV_DOWNLOADS.md).
