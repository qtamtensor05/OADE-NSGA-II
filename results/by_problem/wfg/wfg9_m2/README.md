# WFG9_M2 — hồ sơ nghiên cứu

[Báo cáo riêng của bài toán](reports/README.md)

Dữ liệu đã lọc riêng theo bài toán; giữ nguyên cột, giá trị và thứ tự dòng từ nguồn.

| Nhóm thí nghiệm | Số dòng raw | Số seed |
|---|---:|---:|
| [benchmark_wfg_m2](reports/benchmark_wfg_m2.md) | 210 | 30 |
| [benchmark_wfg_scaling](reports/benchmark_wfg_scaling.md) | 150 | 30 |

## Bảng và dữ liệu

- [benchmark_wfg_m2/algorithm_benchmark_convergence.csv](csv_results.zip) (2041 dòng)
- [benchmark_wfg_m2/algorithm_benchmark_cost_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_wfg_m2/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_wfg_m2/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (12 dòng)
- [benchmark_wfg_m2/algorithm_benchmark_raw_runs.csv](csv_results.zip) (210 dòng)
- [benchmark_wfg_m2/algorithm_benchmark_validation.csv](csv_results.zip) (210 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_convergence.csv](csv_results.zip) (1441 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_cost_summary.csv](csv_results.zip) (5 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (5 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (8 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_raw_runs.csv](csv_results.zip) (150 dòng)
- [benchmark_wfg_scaling/algorithm_benchmark_validation.csv](csv_results.zip) (150 dòng)

## Báo cáo, hình và nguồn dùng chung

- [wfg_compact_report.md](../../../../docs/reports/wfg_compact_report.md)

## Truy vết và bổ sung

`manifest.json` ghi nguồn, SHA-256 và số dòng của từng tệp. P-value/Holm được giữ theo họ kiểm định gốc, không hiệu chỉnh lại theo thư mục.
Các bảng khác số mục tiêu/kích thước vẫn giữ cột n_obj/n_var; không gộp thành một điều kiện.
Bổ sung kết quả vào nguồn theo đúng giao thức, rồi chạy `python scripts/organize_by_problem.py`. Không chỉnh trực tiếp bản tách được sinh tự động.
