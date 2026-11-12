# ZDT4 — Ablation OADE classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt4` trong đợt `ablation_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.006977176 | 0.003323347 | 0.8648781 | 0.005620671 | 3.859753 | 19960.63 |
| OADE_NO_FCR_ADAPTATION | 30 | 30 | 0.006442176 | 0.004255377 | 0.866429 | 0.006972493 | 3.741226 | 19967.07 |
| OADE_NO_PROBABILITY_ADAPTATION | 30 | 30 | 0.02612011 | 0.0556555 | 0.8356099 | 0.08446716 | 4.040014 | 19957.4 |
| OADE_NO_NEIGHBORHOOD | 30 | 30 | 0.01142284 | 0.02260406 | 0.8582386 | 0.0344122 | 4.86146 | 19952 |
| OADE_NO_RESTART | 30 | 30 | 0.00683066 | 0.003328584 | 0.8650507 | 0.005678768 | 4.34094 | 19956.33 |
| OADE_NO_OBL | 30 | 30 | 0.3483546 | 0.1794228 | 0.4070337 | 0.1908653 | 4.203249 | 20000 |
| OADE_BASIC | 30 | 30 | 0.3795846 | 0.3121818 | 0.426806 | 0.2788453 | 4.48853 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NO_FCR_ADAPTATION**; HV cao nhất: **OADE_NO_FCR_ADAPTATION**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_BASIC | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 0.5571913 | -0.4537634 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.04516129 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_OBL | 30 | 1.080334e-07 | 0.9956989 | reference_better |
| IGD | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.3333333 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 1 | -0.4285714 | no_significant_difference |
| HV | OADE_FULL | OADE_BASIC | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 0.4128771 | -0.483871 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.06666667 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_OBL | 30 | 1.080334e-07 | 0.9956989 | reference_better |
| HV | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.311828 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 1 | -0.2380952 | no_significant_difference |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1954 dòng)
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
