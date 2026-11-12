# ZDT1 — Ablation OADE classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt1` trong đợt `ablation_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.005925213 | 0.002536145 | 0.8689611 | 0.003342054 | 3.25072 | 19975.5 |
| OADE_NO_FCR_ADAPTATION | 30 | 30 | 0.007522371 | 0.004233344 | 0.8668325 | 0.006583184 | 3.103683 | 19979.77 |
| OADE_NO_PROBABILITY_ADAPTATION | 30 | 30 | 0.005762944 | 0.002953738 | 0.8690545 | 0.003917073 | 3.098378 | 19977.03 |
| OADE_NO_NEIGHBORHOOD | 30 | 30 | 0.005285846 | 0.002853754 | 0.8697741 | 0.004069881 | 3.732408 | 19978.27 |
| OADE_NO_RESTART | 30 | 30 | 0.004475332 | 0.0002512405 | 0.8708662 | 0.0002322392 | 3.465398 | 19950.83 |
| OADE_NO_OBL | 30 | 30 | 0.006320623 | 0.004042228 | 0.8685199 | 0.005350379 | 3.438151 | 19989 |
| OADE_BASIC | 30 | 30 | 0.004412584 | 0.0002887561 | 0.870983 | 0.0002359664 | 3.874576 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_BASIC**; HV cao nhất: **OADE_BASIC**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_BASIC | 30 | 0.0002581626 | -0.8451613 | comparison_better |
| IGD | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 0.4419771 | 0.4752688 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.2344086 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.01075269 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | -0.2430108 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 0.1710026 | -0.544086 | no_significant_difference |
| HV | OADE_FULL | OADE_BASIC | 30 | 0.0001193918 | -0.8666667 | comparison_better |
| HV | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 0.8097944 | 0.427957 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.3204301 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.006451613 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | -0.1870968 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 0.0238779 | -0.6602151 | comparison_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1924 dòng)
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
