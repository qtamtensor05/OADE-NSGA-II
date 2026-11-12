# DTLZ4_M5 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz4_m5` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **3 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('14', '5', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.3726514 | 0.02812465 | 0.6475771 | 0.1049922 | 3.040268 | 19959.43 |
| NSGA2 | 30 | 30 | 0.8023551 | 0.108677 | 0.0381603 | 0.05528108 | 1.596479 | 20000 |
| RNSGA2 | 30 | 30 | 0.7387604 | 0.1056883 | 0.3370042 | 0.2151673 | 5.418358 | 20000 |
| DNSGA2 | 30 | 30 | 0.7876573 | 0.1202807 | 0.05715825 | 0.06305908 | 1.507636 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.3886597 | 0.01764011 | 0.6545986 | 0.05882757 | 72.25243 | 20000 |
| NSGAII_SDR_OLS | 30 | 27 | 1.116311 | 0.02510422 | 0.1503031 | 0.01905013 | 2.683338 | 20000 |
| CE_MOEA | 30 | 30 | 0.3835737 | 0.0162317 | 0.6287712 | 0.0786031 | 72.24253 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **CGDE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.8031788 | 0.3333333 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 0.2726466 | 0.4666667 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 27 | 4.61936e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 1 | 0.1139785 | no_significant_difference |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1 | -0.07096774 | no_significant_difference |
| HV | OADE_NSGAII | DNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 27 | 6.556511e-07 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 3.893673e-05 | 0.9053763 | reference_better |

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
