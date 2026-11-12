# ZDT4 — Benchmark 7 thuật toán — adaptive

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt4` trong đợt `benchmark_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.00683066 | 0.003328584 | 0.8650507 | 0.005678768 | 11.98332 | 19956.33 |
| NSGA2 | 30 | 30 | 0.009952722 | 0.005080291 | 0.8593619 | 0.007910405 | 2.208074 | 20000 |
| RNSGA2 | 30 | 30 | 0.6205746 | 0.1653183 | 0.3510772 | 0.1552783 | 2.096754 | 20000 |
| DNSGA2 | 30 | 30 | 0.01997309 | 0.02736954 | 0.8467496 | 0.03686742 | 2.10489 | 19910 |
| CGDE_NSGAII | 30 | 30 | 12.17158 | 2.800419 | 0 | 0 | 138.4162 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 10.89141 | 6.777696 | 0 | 0 | 2.368711 | 20000 |
| CE_MOEA | 30 | 30 | 0.3572136 | 0.2343311 | 0.409725 | 0.2278695 | 129.2001 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 0.0004423261 | 0.7591398 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.004040364 | 0.6258065 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.0001885984 | 0.7806452 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.0008718204 | 0.6688172 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |

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

- [benchmark_v2_results_report.md](../../../../../docs/reports/benchmark_v2_results_report.md)
- [restart_confirmation_report.md](../../../../../docs/reports/restart_confirmation_report.md)
- [ablation_results_report.md](../../../../../docs/reports/ablation_results_report.md)
- [zdt_parameter_sensitivity_report.md](../../../../../docs/reports/zdt_parameter_sensitivity_report.md)
- [sensitivity_analysis.md](../../../../../docs/reports/sensitivity_analysis.md)
- [zdt_sensitivity.md](../../../../../docs/protocols/zdt_sensitivity.md)
- [experiment_registry.md](../../../../../docs/protocols/experiment_registry.md)
- [zdt_composition.json](../../../../provenance/zdt_composition.json)
- [zdt_validation.json](../../../../provenance/zdt_validation.json)
- [study_manifest.json](../../../../experiments/zdt_sensitivity_ofat_v1/study_manifest.json)

[Danh mục báo cáo của bài toán](README.md)
