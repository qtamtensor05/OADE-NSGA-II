# DTLZ2_M3 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz2_m3` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **1 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('12', '3', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.07660528 | 0.002756874 | 0.6844643 | 0.007205385 | 5.631926 | 19964.77 |
| NSGA2 | 30 | 30 | 0.07191649 | 0.002499435 | 0.7014003 | 0.006583435 | 2.757775 | 20000 |
| RNSGA2 | 30 | 30 | 0.4508333 | 0.006548745 | 0.2505389 | 0.006137301 | 3.82749 | 20000 |
| DNSGA2 | 30 | 30 | 0.07156522 | 0.003282827 | 0.7008568 | 0.006177599 | 2.752964 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.06842551 | 0.00207281 | 0.6975459 | 0.004128575 | 126.9388 | 20000 |
| NSGAII_SDR_OLS | 30 | 29 | 0.8424076 | 0.1702638 | 0.1458963 | 0.07576608 | 3.073634 | 20000 |
| CE_MOEA | 30 | 30 | 0.07821691 | 0.002957662 | 0.6793596 | 0.006036142 | 136.8109 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **CGDE_NSGAII**; HV cao nhất: **NSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.4253314 | 0.4150538 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | -1 | comparison_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 0.0001314171 | -0.8580645 | comparison_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 8.814037e-06 | -0.9311828 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 29 | 1.41561e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.2034551 | 0.5225806 | no_significant_difference |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 2.793968e-07 | -0.9913978 | comparison_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 5.997717e-07 | -0.9827957 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | -1 | comparison_better |
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
