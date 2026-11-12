# DTLZ2_M2 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz2_m2` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **1 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('11', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.005041059 | 0.0002414587 | 0.4189526 | 0.0003155717 | 9.929606 | 19961.83 |
| NSGA2 | 30 | 30 | 0.005050402 | 0.0001801723 | 0.4194037 | 0.0002362815 | 5.074933 | 20000 |
| RNSGA2 | 30 | 30 | 0.1943121 | 0.02002737 | 0.2256933 | 0.01121392 | 6.53742 | 20000 |
| DNSGA2 | 30 | 30 | 0.00498284 | 0.0002211184 | 0.4193512 | 0.0002466506 | 4.609749 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.005184638 | 0.0001622803 | 0.4180133 | 0.0002867845 | 274.2291 | 20000 |
| NSGAII_SDR_OLS | 30 | 29 | 0.6055763 | 0.2370358 | 0.1485967 | 0.07036038 | 6.828994 | 20000 |
| CE_MOEA | 30 | 30 | 0.005114282 | 0.0001949782 | 0.4184345 | 0.0003954447 | 275.5844 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **DNSGA2**; HV cao nhất: **NSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.9546476 | 0.2774194 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 0.05639703 | 0.5827957 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1 | -0.2301075 | no_significant_difference |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1 | 0.02795699 | no_significant_difference |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 29 | 1.41561e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.0001954958 | 0.8623656 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 2.793968e-07 | 0.9913978 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.001208605 | -0.8021505 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.54227e-05 | -0.9268817 | comparison_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 29 | 2.04891e-07 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |

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

- [dtlz_results_report.md](../../../../../docs/reports/dtlz_results_report.md)
- [dtlz_sensitivity.md](../../../../../docs/protocols/dtlz_sensitivity.md)

[Danh mục báo cáo của bài toán](README.md)
