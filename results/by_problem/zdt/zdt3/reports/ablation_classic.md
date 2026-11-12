# ZDT3 — Ablation OADE classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt3` trong đợt `ablation_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.008319198 | 0.005096248 | 1.049238 | 0.00363392 | 3.600154 | 19943.1 |
| OADE_NO_FCR_ADAPTATION | 30 | 30 | 0.01072344 | 0.006935822 | 1.047546 | 0.005524846 | 3.401892 | 19948.63 |
| OADE_NO_PROBABILITY_ADAPTATION | 30 | 30 | 0.009551823 | 0.006540346 | 1.048329 | 0.004744549 | 3.506504 | 19950.17 |
| OADE_NO_NEIGHBORHOOD | 30 | 30 | 0.00834873 | 0.005025007 | 1.049171 | 0.004113366 | 4.01111 | 19948.17 |
| OADE_NO_RESTART | 30 | 30 | 0.004985851 | 0.0003361072 | 1.051221 | 0.0001520047 | 3.445738 | 19949.9 |
| OADE_NO_OBL | 30 | 30 | 0.008642299 | 0.003805811 | 1.049038 | 0.002942437 | 3.457714 | 19952.33 |
| OADE_BASIC | 30 | 30 | 0.005049974 | 0.0003601774 | 1.051283 | 0.0001106889 | 4.1748 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NO_RESTART**; HV cao nhất: **OADE_BASIC**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_BASIC | 30 | 0.003330097 | -0.7548387 | comparison_better |
| IGD | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.2817204 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | 0.07956989 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.1612903 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.1655914 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 0.003330097 | -0.7548387 | comparison_better |
| HV | OADE_FULL | OADE_BASIC | 30 | 0.0001553111 | -0.8580645 | comparison_better |
| HV | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.2258065 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.02365591 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.1870968 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.1526882 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 0.01751044 | -0.6774194 | comparison_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1926 dòng)
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
