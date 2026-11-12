# WFG9_M2 — Benchmark WFG M=2

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg9_m2` trong đợt `benchmark_wfg_m2`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.03636132 | 0.007809284 | 2.152992 | 0.01711845 | 5.156569 | 19956.9 |
| NSGA2 | 30 | 30 | 0.1101229 | 0.03767332 | 1.792418 | 0.1884144 | 3.444099 | 20000 |
| RNSGA2 | 30 | 30 | 0.6219575 | 0.07090626 | 1.203633 | 0.1748462 | 4.079628 | 20000 |
| DNSGA2 | 30 | 30 | 0.1121911 | 0.03417156 | 1.7865 | 0.177633 | 4.119274 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.1180576 | 0.02680549 | 1.76547 | 0.1400671 | 453.1078 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.2996603 | 0.0596967 | 1.146553 | 0.1526176 | 3.461024 | 20000 |
| CE_MOEA | 30 | 30 | 0.1294737 | 0.001357267 | 1.701562 | 0.002775765 | 434.252 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 4.470348e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 4.470348e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 6.519258e-08 | 0.9870968 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 4.004687e-07 | 0.9569892 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 4.470348e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 1.862645e-07 | 0.9655914 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 9.443611e-07 | 0.9311828 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 4.470348e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 4.470348e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (2041 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (12 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (210 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (210 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
