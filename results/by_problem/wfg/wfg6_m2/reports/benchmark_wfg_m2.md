# WFG6_M2 — Benchmark WFG M=2

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg6_m2` trong đợt `benchmark_wfg_m2`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.05479008 | 0.01645683 | 2.042368 | 0.08336763 | 4.423403 | 19966 |
| NSGA2 | 30 | 30 | 0.07169428 | 0.01073373 | 1.958037 | 0.0496875 | 2.734838 | 20000 |
| RNSGA2 | 30 | 30 | 0.7724877 | 0.09182576 | 1.158809 | 0.08803847 | 3.58073 | 20000 |
| DNSGA2 | 30 | 30 | 0.07377146 | 0.01517018 | 1.958104 | 0.05018826 | 2.964342 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.03383516 | 0.01047516 | 2.181996 | 0.02615905 | 448.085 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.2912865 | 0.05381885 | 1.239371 | 0.1470939 | 2.849619 | 20000 |
| CE_MOEA | 30 | 30 | 0.1161347 | 0.01622029 | 1.730847 | 0.08803833 | 283.4629 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **CGDE_NSGAII**; HV cao nhất: **CGDE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 4.470348e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.564622e-07 | -0.9741935 | comparison_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 7.046387e-06 | 0.883871 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 4.96842e-05 | 0.7892473 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 4.470348e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 4.470348e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 3.195554e-05 | 0.827957 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 4.96842e-05 | 0.7892473 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 4.470348e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (2042 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (12 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (210 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (210 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
