# Tải dữ liệu CSV kết quả

CSV được lưu trong ZIP; báo cáo Markdown và hình vẫn xem trực tiếp. Tải riêng ZIP bên dưới rồi giải nén ngay cạnh ZIP để có đúng cấu trúc thư mục cũ.

Tổng: **425 CSV**, **42 ZIP**, từ **96.05 MiB** xuống **28.32 MiB**.

## Khôi phục sau khi clone

Chạy từ thư mục gốc dự án, chỉ cần Python chuẩn:

```powershell
python scripts/csv_archives.py restore
```

Lệnh kiểm tra SHA-256 của ZIP và từng CSV, rồi khôi phục về đường dẫn cũ. Không ghi đè CSV cục bộ có nội dung khác. CSV đã giải nén được Git bỏ qua; ZIP là bản được commit.

Chạy lệnh restore trước khi chạy phân tích, vẽ hình, inventory hoặc kiểm thử cần dữ liệu. Lệnh organize_by_problem tự khôi phục các CSV còn thiếu.

## Kiểm tra và cập nhật

```powershell
python scripts/csv_archives.py verify
python scripts/organize_by_problem.py
python scripts/csv_archives.py pack
```

Pack gom các CSV đã có trong catalog, CSV đang được Git theo dõi và các bản tách trong by_problem. Để đưa nguồn CSV mới ở nơi khác vào gói, dùng `git add -f đường/dẫn.csv`, chạy pack rồi bỏ CSV đó khỏi index bằng `git rm --cached -- đường/dẫn.csv` trước khi commit ZIP. Không commit đồng thời ZIP và CSV rời.

Catalog [csv_archives.json](csv_archives.json) lưu tên thành viên, đường dẫn phục hồi, kích thước và SHA-256. Manifest theo bài toán vẫn mô tả CSV sau giải nén. Việc nén không thay đổi dữ liệu hay provenance của các lượt chạy.

| Bộ dữ liệu / bài toán | Tải ZIP | CSV | MiB |
|---|---|---:|---:|
| ablation | [csv_results.zip](ablation/csv_results.zip) | 6 | 0.25 |
| algorithm_benchmark | [csv_results.zip](algorithm_benchmark/csv_results.zip) | 6 | 0.25 |
| algorithm_benchmark_v2 | [csv_results.zip](algorithm_benchmark_v2/csv_results.zip) | 6 | 0.25 |
| benchmark | [csv_results.zip](benchmark/csv_results.zip) | 18 | 0.01 |
| by_problem | [csv_results.zip](by_problem/csv_results.zip) | 1 | 0.00 |
| by_problem/dtlz/dtlz1_m2 | [csv_results.zip](by_problem/dtlz/dtlz1_m2/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz1_m3 | [csv_results.zip](by_problem/dtlz/dtlz1_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz1_m5 | [csv_results.zip](by_problem/dtlz/dtlz1_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz2_m2 | [csv_results.zip](by_problem/dtlz/dtlz2_m2/csv_results.zip) | 6 | 0.06 |
| by_problem/dtlz/dtlz2_m3 | [csv_results.zip](by_problem/dtlz/dtlz2_m3/csv_results.zip) | 6 | 0.06 |
| by_problem/dtlz/dtlz2_m5 | [csv_results.zip](by_problem/dtlz/dtlz2_m5/csv_results.zip) | 6 | 0.06 |
| by_problem/dtlz/dtlz3_m2 | [csv_results.zip](by_problem/dtlz/dtlz3_m2/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz3_m3 | [csv_results.zip](by_problem/dtlz/dtlz3_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz3_m5 | [csv_results.zip](by_problem/dtlz/dtlz3_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/dtlz/dtlz4_m2 | [csv_results.zip](by_problem/dtlz/dtlz4_m2/csv_results.zip) | 6 | 0.05 |
| by_problem/dtlz/dtlz4_m3 | [csv_results.zip](by_problem/dtlz/dtlz4_m3/csv_results.zip) | 6 | 0.06 |
| by_problem/dtlz/dtlz4_m5 | [csv_results.zip](by_problem/dtlz/dtlz4_m5/csv_results.zip) | 6 | 0.06 |
| by_problem/wfg/wfg1_m2 | [csv_results.zip](by_problem/wfg/wfg1_m2/csv_results.zip) | 12 | 0.09 |
| by_problem/wfg/wfg1_m3 | [csv_results.zip](by_problem/wfg/wfg1_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg1_m5 | [csv_results.zip](by_problem/wfg/wfg1_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg4_m2 | [csv_results.zip](by_problem/wfg/wfg4_m2/csv_results.zip) | 12 | 0.10 |
| by_problem/wfg/wfg4_m3 | [csv_results.zip](by_problem/wfg/wfg4_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg4_m5 | [csv_results.zip](by_problem/wfg/wfg4_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg6_m2 | [csv_results.zip](by_problem/wfg/wfg6_m2/csv_results.zip) | 12 | 0.10 |
| by_problem/wfg/wfg6_m3 | [csv_results.zip](by_problem/wfg/wfg6_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg6_m5 | [csv_results.zip](by_problem/wfg/wfg6_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg9_m2 | [csv_results.zip](by_problem/wfg/wfg9_m2/csv_results.zip) | 12 | 0.10 |
| by_problem/wfg/wfg9_m3 | [csv_results.zip](by_problem/wfg/wfg9_m3/csv_results.zip) | 6 | 0.04 |
| by_problem/wfg/wfg9_m5 | [csv_results.zip](by_problem/wfg/wfg9_m5/csv_results.zip) | 6 | 0.04 |
| by_problem/zdt/zdt1 | [csv_results.zip](by_problem/zdt/zdt1/csv_results.zip) | 34 | 2.63 |
| by_problem/zdt/zdt2 | [csv_results.zip](by_problem/zdt/zdt2/csv_results.zip) | 34 | 2.54 |
| by_problem/zdt/zdt3 | [csv_results.zip](by_problem/zdt/zdt3/csv_results.zip) | 34 | 2.64 |
| by_problem/zdt/zdt4 | [csv_results.zip](by_problem/zdt/zdt4/csv_results.zip) | 34 | 2.45 |
| by_problem/zdt/zdt6 | [csv_results.zip](by_problem/zdt/zdt6/csv_results.zip) | 34 | 2.62 |
| dtlz_benchmark | [csv_results.zip](dtlz_benchmark/csv_results.zip) | 6 | 0.54 |
| experiments/zdt_sensitivity_ofat_v1/derived | [csv_results.zip](experiments/zdt_sensitivity_ofat_v1/derived/csv_results.zip) | 6 | 0.49 |
| figures | [csv_results.zip](figures/csv_results.zip) | 14 | 0.03 |
| restart_confirmation | [csv_results.zip](restart_confirmation/csv_results.zip) | 6 | 0.08 |
| sensitivity | [csv_results.zip](sensitivity/csv_results.zip) | 4 | 11.61 |
| three_algorithms | [csv_results.zip](three_algorithms/csv_results.zip) | 2 | 0.01 |
| wfg_compact_benchmark | [csv_results.zip](wfg_compact_benchmark/csv_results.zip) | 6 | 0.45 |
| wfg_m2_7algo_benchmark | [csv_results.zip](wfg_m2_7algo_benchmark/csv_results.zip) | 6 | 0.21 |
