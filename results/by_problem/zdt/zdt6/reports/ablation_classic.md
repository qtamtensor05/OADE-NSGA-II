# ZDT6 — Ablation OADE classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt6` trong đợt `ablation_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Ablation thuộc cấu hình classic với khởi tạo uniform chung; không suy rộng thành ablation adaptive hoặc khởi tạo Sobol.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.005285892 | 0.00337052 | 0.4365567 | 0.003739811 | 2.87116 | 19940.43 |
| OADE_NO_FCR_ADAPTATION | 30 | 30 | 0.00581307 | 0.004541655 | 0.435739 | 0.005094101 | 2.793528 | 19946.53 |
| OADE_NO_PROBABILITY_ADAPTATION | 30 | 30 | 0.006148314 | 0.004952884 | 0.4355107 | 0.005600701 | 2.918002 | 19957 |
| OADE_NO_NEIGHBORHOOD | 30 | 30 | 0.005288662 | 0.003951643 | 0.436622 | 0.004195262 | 3.240592 | 19953.27 |
| OADE_NO_RESTART | 30 | 30 | 0.0038364 | 0.0001943726 | 0.438171 | 0.0002625684 | 2.63734 | 19948.2 |
| OADE_NO_OBL | 30 | 30 | 0.006036284 | 0.004232809 | 0.4356141 | 0.004868684 | 2.715887 | 19954.67 |
| OADE_BASIC | 30 | 30 | 0.003803681 | 0.0002319744 | 0.4381168 | 0.0002003413 | 2.998131 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_BASIC**; HV cao nhất: **OADE_NO_RESTART**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_BASIC | 30 | 0.1460698 | -0.5569892 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.144086 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.2258065 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.2817204 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.1870968 | no_significant_difference |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 0.1328593 | -0.5655914 | no_significant_difference |
| HV | OADE_FULL | OADE_BASIC | 30 | 1 | -0.372043 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_FCR_ADAPTATION | 30 | 1 | 0.3892473 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_NEIGHBORHOOD | 30 | 1 | -0.2645161 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_OBL | 30 | 1 | 0.372043 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_PROBABILITY_ADAPTATION | 30 | 1 | 0.2344086 | no_significant_difference |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 0.3614867 | -0.4967742 | no_significant_difference |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1920 dòng)
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
