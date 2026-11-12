# DTLZ1_M2 — Benchmark DTLZ

## Phạm vi

Chỉ gồm dữ liệu `problem=dtlz1_m2` trong đợt `benchmark_dtlz`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **4 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('6', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.002284317 | 0.0002349323 | 0.2332177 | 0.0002646554 | 5.066044 | 19961.83 |
| NSGA2 | 30 | 30 | 0.002946055 | 0.0008342738 | 0.2323494 | 0.0008518194 | 2.525676 | 20000 |
| RNSGA2 | 30 | 30 | 0.1345761 | 0.1074221 | 0.145778 | 0.04724947 | 5.023168 | 20000 |
| DNSGA2 | 30 | 30 | 0.003759927 | 0.002299337 | 0.2315823 | 0.002050192 | 2.385852 | 19910 |
| CGDE_NSGAII | 30 | 30 | 1.369691 | 0.3721457 | 0 | 0 | 178.9244 | 20000 |
| NSGAII_SDR_OLS | 30 | 26 | 5.531123 | 3.600808 | 0.00380253 | 0.01345965 | 4.056065 | 20000 |
| CE_MOEA | 30 | 30 | 0.9224931 | 0.9631486 | 0.02270802 | 0.0527111 | 155.433 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 8.814037e-06 | 0.9311828 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 5.637109e-05 | 0.883871 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 26 | 8.642673e-07 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1.341105e-07 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 4.200265e-06 | 0.9526882 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 5.997717e-07 | 0.9827957 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 26 | 1.251698e-06 | 1 | reference_better |
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
