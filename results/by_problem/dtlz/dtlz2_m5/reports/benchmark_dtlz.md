# DTLZ2_M5 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz2_m5` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('14', '5', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.4200898 | 0.03450937 | 0.4601915 | 0.08464994 | 8.321735 | 19953.13 |
| NSGA2 | 30 | 30 | 0.4570932 | 0.05933251 | 0.4302923 | 0.1101179 | 4.392825 | 20000 |
| RNSGA2 | 30 | 30 | 0.6692201 | 0.03347719 | 0.2556312 | 0.04033218 | 3.361897 | 20000 |
| DNSGA2 | 30 | 30 | 0.4680755 | 0.04741115 | 0.3918717 | 0.0957259 | 3.682443 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.636379 | 0.09419957 | 0.156506 | 0.09191036 | 218.0838 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 1.046363 | 0.1213644 | 0.1235104 | 0.08047671 | 5.904883 | 20000 |
| CE_MOEA | 30 | 30 | 0.4669139 | 0.02184938 | 0.3560863 | 0.07324345 | 207.8122 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.0001383573 | 0.8537634 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.41561e-07 | 0.9956989 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 0.000510823 | 0.8107527 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.0743399 | 0.5612903 | no_significant_difference |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.0002210196 | 0.8580645 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.1860224 | 0.5354839 | no_significant_difference |
| HV | OADE_NSGAII | NSGA2 | 30 | 1 | 0.2086022 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 2.793968e-07 | 0.9913978 | reference_better |

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
