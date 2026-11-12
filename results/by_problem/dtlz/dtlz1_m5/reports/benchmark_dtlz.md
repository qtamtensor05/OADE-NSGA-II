# DTLZ1_M5 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz1_m5` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('9', '5', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 2.552925 | 4.97343 | 0.00919743 | 0.02191764 | 6.91154 | 19948.43 |
| NSGA2 | 30 | 30 | 39.75192 | 14.78137 | 0 | 0 | 3.31465 | 20000 |
| RNSGA2 | 30 | 30 | 16.19388 | 10.60053 | 0 | 0 | 7.044792 | 20000 |
| DNSGA2 | 30 | 30 | 37.30309 | 15.45558 | 0 | 0 | 3.304365 | 19910 |
| CGDE_NSGAII | 30 | 30 | 12.26756 | 4.971148 | 0 | 0 | 170.7382 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 32.65934 | 11.93069 | 0 | 0 | 4.163416 | 20000 |
| CE_MOEA | 30 | 30 | 6.899712 | 2.477686 | 0 | 0 | 189.2001 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.001006667 | 0.7849462 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 2.164766e-05 | 0.9096774 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1.41561e-07 | 0.9956989 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 0.0001314171 | 0.8580645 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.04863477 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 0.04863477 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.04863477 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.04863477 | 1 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.04863477 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 0.04863477 | 1 | reference_better |

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
