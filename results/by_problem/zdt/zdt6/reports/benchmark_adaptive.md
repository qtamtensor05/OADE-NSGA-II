# ZDT6 — Benchmark 7 thuật toán — adaptive

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt6` trong đợt `benchmark_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.003843999 | 0.0001929227 | 0.4381765 | 0.0002527955 | 13.34138 | 19948 |
| NSGA2 | 30 | 30 | 0.01636813 | 0.002011487 | 0.4178915 | 0.002872109 | 2.055383 | 20000 |
| RNSGA2 | 30 | 30 | 0.1857638 | 0.09278693 | 0.2676365 | 0.06858999 | 2.207116 | 20000 |
| DNSGA2 | 30 | 30 | 0.0225884 | 0.002794084 | 0.4089167 | 0.003997333 | 2.019729 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.003823051 | 0.0002226666 | 0.4390565 | 0.0001994666 | 103.0721 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.1394459 | 0.08274753 | 0.2829226 | 0.05896156 | 2.120926 | 20000 |
| CE_MOEA | 30 | 30 | 0.004956833 | 0.0003359531 | 0.4377938 | 0.0003599741 | 101.5612 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **CGDE_NSGAII**; HV cao nhất: **CGDE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 0.7765688 | -0.06236559 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 5.587935e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.0003772005 | 0.7376344 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 5.587935e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |

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
