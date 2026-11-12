# DTLZ3_M2 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz3_m2` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('11', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 1.348082 | 1.272106 | 0.09978823 | 0.1581764 | 8.59561 | 19959.57 |
| NSGA2 | 30 | 30 | 2.64577 | 1.993191 | 0.01151276 | 0.05504769 | 3.693947 | 20000 |
| RNSGA2 | 30 | 30 | 4.659926 | 3.103635 | 0 | 0 | 2.093255 | 20000 |
| DNSGA2 | 30 | 30 | 3.945826 | 2.377576 | 0 | 0 | 3.806793 | 19910 |
| CGDE_NSGAII | 30 | 30 | 106.4339 | 41.47925 | 0 | 0 | 235.126 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 33.49452 | 25.69105 | 0 | 0 | 6.410651 | 20000 |
| CE_MOEA | 30 | 30 | 23.39526 | 12.71907 | 0 | 0 | 192.9774 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 5.637109e-05 | 0.883871 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.02982411 | 0.6301075 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 3.548339e-05 | 0.8967742 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.08364045 | 1 | no_significant_difference |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 0.08364045 | 1 | no_significant_difference |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.08364045 | 1 | no_significant_difference |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.07739256 | 0.9340659 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.08364045 | 1 | no_significant_difference |
| HV | OADE_NSGAII | RNSGA2 | 30 | 0.08364045 | 1 | no_significant_difference |

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
