# ZDT2 — Ablation OADE classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt2` trong đợt `ablation_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.007733971 | 0.005315963 | 0.5337388 | 0.006239717 | 3.381612 | 19945.1 |
| OADE_NO_FCR_ADAPTATION | 30 | 30 | 0.008112241 | 0.005556817 | 0.5328754 | 0.007234806 | 3.002144 | 19950.4 |
| OADE_NO_PROBABILITY_ADAPTATION | 30 | 30 | 0.007803364 | 0.006694573 | 0.534245 | 0.006772609 | 3.123044 | 19952.03 |
| OADE_NO_NEIGHBORHOOD | 30 | 30 | 0.008284577 | 0.006568322 | 0.5328248 | 0.007687736 | 3.481688 | 19956.27 |
| OADE_NO_RESTART | 30 | 30 | 0.004740679 | 0.0003019684 | 0.5376665 | 0.0002103821 | 3.083813 | 19955.73 |
| OADE_NO_OBL | 30 | 30 | 0.009689222 | 0.006504458 | 0.5314998 | 0.007543952 | 3.192997 | 19960.33 |
| OADE_BASIC | 30 | 30 | 0.004660979 | 0.0002998598 | 0.5376786 | 0.0002193614 | 3.804669 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_BASIC**; HV cao nhất: **OADE_BASIC**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_BASIC | 30 | 0.007081591 | -0.7204301 | comparison_better |
| IGD | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.09247312 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.002150538 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.2172043 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | -0.07096774 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 0.02284259 | -0.6645161 | comparison_better |
| HV | OADE_FULL | OADE_BASIC | 30 | 2.795458e-05 | -0.9053763 | comparison_better |
| HV | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.1096774 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | 0.01505376 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.255914 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | -0.1483871 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 0.0002652407 | -0.8408602 | comparison_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1922 dòng)
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
