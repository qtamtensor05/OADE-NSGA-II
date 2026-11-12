# DTLZ3_M5 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz3_m5` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('14', '5', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 80.82241 | 29.05379 | 0 | 0 | 9.788314 | 19949.47 |
| NSGA2 | 30 | 30 | 251.8627 | 58.43048 | 0 | 0 | 4.74213 | 20000 |
| RNSGA2 | 30 | 30 | 225.8499 | 69.26201 | 0 | 0 | 7.722764 | 20000 |
| DNSGA2 | 30 | 30 | 244.8518 | 64.0692 | 0 | 0 | 4.702857 | 19910 |
| CGDE_NSGAII | 30 | 30 | 268.1352 | 76.98489 | 0 | 0 | 257.2924 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 75.55031 | 44.30152 | 0 | 0 | 6.818071 | 20000 |
| CE_MOEA | 30 | 30 | 106.1331 | 20.57645 | 0 | 0 | 257.1512 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGAII_SDR_OLS**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.03030273 | 0.6258065 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1 | -0.09247312 | no_significant_difference |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.41561e-07 | 0.9956989 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 1 | 0 | no_significant_difference |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1 | 0 | no_significant_difference |
| HV | OADE_NSGAII | DNSGA2 | 30 | 1 | 0 | no_significant_difference |
| HV | OADE_NSGAII | NSGA2 | 30 | 1 | 0 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1 | 0 | no_significant_difference |
| HV | OADE_NSGAII | RNSGA2 | 30 | 1 | 0 | no_significant_difference |

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

- [dtlz_results_report.md](../../../../../docs/reports/dtlz_results_report.md)
- [dtlz_sensitivity.md](../../../../../docs/protocols/dtlz_sensitivity.md)

[Danh mục báo cáo của bài toán](README.md)
