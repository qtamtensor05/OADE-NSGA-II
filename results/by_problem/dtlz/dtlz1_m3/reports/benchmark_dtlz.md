# DTLZ1_M3 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz1_m3` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **2 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('7', '3', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.02922824 | 0.001686336 | 0.1846578 | 0.000785746 | 5.45102 | 19948.13 |
| NSGA2 | 30 | 30 | 0.1915457 | 0.1732885 | 0.1127026 | 0.06782608 | 2.78283 | 20000 |
| RNSGA2 | 30 | 30 | 0.6026266 | 0.4238593 | 0.03791357 | 0.05380267 | 5.543853 | 20000 |
| DNSGA2 | 30 | 30 | 0.5060002 | 0.3967524 | 0.05406174 | 0.06591916 | 2.516922 | 19910 |
| CGDE_NSGAII | 30 | 30 | 1.494088 | 0.4162139 | 0 | 0 | 132.1126 | 20000 |
| NSGAII_SDR_OLS | 30 | 28 | 8.384921 | 5.527481 | 0 | 0 | 2.959231 | 20000 |
| CE_MOEA | 30 | 30 | 2.094016 | 1.284472 | 0.004533964 | 0.01374796 | 141.3856 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 28 | 2.384186e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 28 | 3.501773e-07 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |

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
