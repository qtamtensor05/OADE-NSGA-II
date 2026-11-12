# ZDT1 — Xác nhận restart classic/adaptive/no-restart

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt1` trong đợt `restart_confirmation`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **90 dòng raw**, **30 seed** (1000–1029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

OADE_FULL là classic; OADE_ADAPTIVE_RESTART là adaptive; OADE_NO_RESTART tắt restart. Seed xác nhận là 1000–1029. Telemetry trigger không được lưu: chất lượng cuối không tự xác nhận cơ chế kích hoạt restart.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_FULL | 30 | 30 | 0.007921126 | 0.004754444 | 0.8663648 | 0.006561879 | 10.45029 | 19975.5 |
| OADE_NO_RESTART | 30 | 30 | 0.004530767 | 0.0003287793 | 0.8708189 | 0.0002370447 | 6.145147 | 19953.97 |
| OADE_ADAPTIVE_RESTART | 30 | 30 | 0.004530767 | 0.0003287793 | 0.8708189 | 0.0002370447 | 7.419269 | 19953.97 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NO_RESTART**; HV cao nhất: **OADE_NO_RESTART**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_FULL | OADE_ADAPTIVE_RESTART | 30 | 1.991168e-05 | -0.888172 | comparison_better |
| IGD | OADE_FULL | OADE_NO_RESTART | 30 | 1.991168e-05 | -0.888172 | comparison_better |
| HV | OADE_FULL | OADE_ADAPTIVE_RESTART | 30 | 6.365776e-05 | -0.8408602 | comparison_better |
| HV | OADE_FULL | OADE_NO_RESTART | 30 | 6.365776e-05 | -0.8408602 | comparison_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (810 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (3 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (3 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (4 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (90 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (90 dòng)

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
