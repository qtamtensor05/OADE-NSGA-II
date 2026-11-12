# DTLZ4_M3 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz4_m3` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **1 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('12', '3', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.07866247 | 0.002898266 | 0.6805276 | 0.007183551 | 2.796769 | 19959.13 |
| NSGA2 | 30 | 30 | 0.06989685 | 0.002979726 | 0.7075444 | 0.006072449 | 1.516959 | 20000 |
| RNSGA2 | 30 | 30 | 0.6328481 | 0.1468369 | 0.2330857 | 0.09903458 | 5.45695 | 20000 |
| DNSGA2 | 30 | 30 | 0.0691032 | 0.002077626 | 0.7089859 | 0.004454351 | 1.420916 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.1164322 | 0.1421608 | 0.6732552 | 0.07296882 | 72.68213 | 20000 |
| NSGAII_SDR_OLS | 30 | 29 | 0.9484789 | 1.257862e-06 | 0.1209963 | 3.180312e-06 | 2.751422 | 20000 |
| CE_MOEA | 30 | 30 | 0.07984759 | 0.003022558 | 0.6751226 | 0.007756635 | 72.40591 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **DNSGA2**; HV cao nhất: **DNSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.8031788 | 0.3462366 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 0.03030273 | -0.6258065 | comparison_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | -1 | comparison_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | -1 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 29 | 1.41561e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.1860224 | 0.5354839 | no_significant_difference |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 0.06912244 | -0.6129032 | no_significant_difference |
| HV | OADE_NSGAII | DNSGA2 | 30 | 2.04891e-07 | -0.9956989 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 2.04891e-07 | -0.9956989 | comparison_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 29 | 2.04891e-07 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (2040 dòng)
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
