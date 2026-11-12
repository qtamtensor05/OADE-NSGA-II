# ZDT1 — Benchmark 7 thuật toán — classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt1` trong đợt `benchmark_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.005925213 | 0.002536145 | 0.8689611 | 0.003342054 | 1.359582 | 19975.5 |
| NSGA2 | 30 | 30 | 0.005174662 | 0.0002979038 | 0.8680528 | 0.0004172684 | 0.9287496 | 20000 |
| RNSGA2 | 30 | 30 | 0.6329726 | 0.08762427 | 0.3480615 | 0.0938884 | 2.757568 | 20000 |
| DNSGA2 | 30 | 30 | 0.005632946 | 0.000423465 | 0.867066 | 0.0006850103 | 0.8533771 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.007433421 | 0.0005274822 | 0.8633624 | 0.0009685192 | 39.56211 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.01563308 | 0.01970436 | 0.8584207 | 0.01484556 | 1.049613 | 20000 |
| CE_MOEA | 30 | 30 | 0.006908169 | 0.0008738724 | 0.8644716 | 0.001778518 | 38.81715 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGA2**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 0.1566191 | 0.5182796 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 0.01848157 | 0.6516129 | reference_better |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1 | 0.2086022 | no_significant_difference |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1 | -0.006451613 | no_significant_difference |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 2.145767e-05 | 0.9010753 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 7.765554e-05 | 0.8580645 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 1.955777e-06 | 0.9483871 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.02822256 | 0.5870968 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.1466293 | 0.4494624 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 5.397946e-06 | 0.9268817 | reference_better |
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
