# DTLZ4_M2 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz4_m2` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **6 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('11', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.005133309 | 0.000212008 | 0.4187608 | 0.0003562526 | 2.736188 | 19962.77 |
| NSGA2 | 30 | 30 | 0.2753313 | 0.3610902 | 0.3059092 | 0.1516131 | 1.643914 | 20000 |
| RNSGA2 | 30 | 30 | 0.4905584 | 0.2145107 | 0.1759084 | 0.07077433 | 7.67105 | 20000 |
| DNSGA2 | 30 | 30 | 0.103326 | 0.2547593 | 0.3781505 | 0.1069757 | 1.4376 | 19910 |
| CGDE_NSGAII | 30 | 27 | 0.00528141 | 0.000194838 | 0.4181401 | 0.0003706507 | 73.08641 | 20000 |
| NSGAII_SDR_OLS | 30 | 27 | 0.7419222 | 6.138844e-06 | 0.1099942 | 1.795266e-05 | 2.70141 | 20000 |
| CE_MOEA | 30 | 30 | 0.005203119 | 0.0001869649 | 0.4183807 | 0.0002674101 | 72.42736 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.8031788 | 0.3333333 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 27 | 0.3853412 | 0.4550265 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1 | 0.01075269 | no_significant_difference |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.0113314 | 0.6817204 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 27 | 4.61936e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.001689263 | 0.7892473 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 27 | 0.00108844 | 0.8412698 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.3979724 | -0.4709677 | no_significant_difference |
| HV | OADE_NSGAII | NSGA2 | 30 | 1 | 0.2516129 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 27 | 6.556511e-07 | 1 | reference_better |
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
