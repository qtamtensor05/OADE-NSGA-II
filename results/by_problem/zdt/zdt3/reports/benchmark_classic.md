# ZDT3 — Benchmark 7 thuật toán — classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt3` trong đợt `benchmark_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.008319198 | 0.005096248 | 1.049238 | 0.00363392 | 3.100225 | 19943.1 |
| NSGA2 | 30 | 30 | 0.007191168 | 0.01023075 | 1.047182 | 0.006699209 | 1.687028 | 20000 |
| RNSGA2 | 30 | 30 | 0.7405515 | 0.05731643 | 0.4010049 | 0.04949664 | 2.383138 | 20000 |
| DNSGA2 | 30 | 30 | 0.005568199 | 0.0002905857 | 1.046953 | 0.000679974 | 1.62852 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.008261615 | 0.0009842318 | 1.035047 | 0.003603796 | 108.5895 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.01864812 | 0.002969683 | 1.035815 | 0.004357624 | 2.531032 | 20000 |
| CE_MOEA | 30 | 30 | 0.008560882 | 0.001533163 | 1.0344 | 0.005115699 | 100.2967 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **DNSGA2**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 1 | 0.2258065 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1 | 0.2473118 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1 | -0.2989247 | no_significant_difference |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.4226026 | -0.4322581 | no_significant_difference |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.847564e-07 | 0.9655914 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 6.332994e-08 | 0.9956989 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 6.332994e-08 | 0.9956989 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.004183967 | 0.7032258 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.06358957 | 0.5268817 | no_significant_difference |
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
