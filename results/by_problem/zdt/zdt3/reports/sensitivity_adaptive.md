# ZDT3 — Độ nhạy tham số adaptive OFAT

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt3` trong đợt `sensitivity_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **570 dòng raw**, **30 seed** (6000–6029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số: median và IQR

| parameter | level | baseline_level | runs | valid_runs | IGD_median | IGD_q25 | IGD_q75 | HV_median | HV_q25 | HV_q75 | restart_completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | 30 | 30 | 0.0105921 | 0.01013627 | 0.01092422 | 1.04766 | 1.047447 | 1.04801 | 0 |
| pop_size | 100 | 100 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| pop_size | 200 | 100 | 30 | 30 | 0.00249304 | 0.002395409 | 0.00264858 | 1.052801 | 1.052775 | 1.052836 | 0 |
| stagnation_patience | 10 | 20 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| stagnation_patience | 20 | 20 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| stagnation_patience | 40 | 20 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| stagnation_tolerance | 1e-05 | 0.0001 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| stagnation_tolerance | 0.0001 | 0.0001 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| stagnation_tolerance | 0.001 | 0.0001 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| diversity_threshold | 0.01 | 0.02 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| diversity_threshold | 0.02 | 0.02 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| diversity_threshold | 0.05 | 0.02 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| restart_elite_ratio | 0.8 | 0.8 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| restart_elite_ratio | 0.9 | 0.8 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| restart_elite_ratio | 0.95 | 0.8 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| prob_de | 0.2 | 0.5 | 30 | 30 | 0.00515625 | 0.004893741 | 0.005317293 | 1.051175 | 1.05112 | 1.051293 | 0 |
| prob_de | 0.5 | 0.5 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| prob_de | 0.8 | 0.5 | 30 | 30 | 0.00512136 | 0.004968685 | 0.0052907 | 1.051268 | 1.051172 | 1.051347 | 0 |
| n_neighbors | 3 | 5 | 30 | 30 | 0.005000728 | 0.004807709 | 0.005195224 | 1.051322 | 1.051158 | 1.051388 | 0 |
| n_neighbors | 5 | 5 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| n_neighbors | 10 | 5 | 30 | 30 | 0.005057805 | 0.004906824 | 0.005401231 | 1.051288 | 1.051203 | 1.051359 | 0 |
| mean_F | 0.4 | 0.65 | 30 | 30 | 0.004957912 | 0.004766443 | 0.00524401 | 1.051304 | 1.051181 | 1.051351 | 0 |
| mean_F | 0.65 | 0.65 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| mean_F | 0.9 | 0.65 | 30 | 30 | 0.004913864 | 0.004676809 | 0.005117414 | 1.051295 | 1.051184 | 1.051332 | 0 |
| mean_CR | 0.1 | 0.5 | 30 | 30 | 0.005186618 | 0.004830229 | 0.005326093 | 1.051244 | 1.051164 | 1.051369 | 0 |
| mean_CR | 0.5 | 0.5 | 30 | 30 | 0.005159663 | 0.004881098 | 0.005367483 | 1.051176 | 1.051109 | 1.051298 | 0 |
| mean_CR | 0.9 | 0.5 | 30 | 30 | 0.005122476 | 0.004935295 | 0.005290349 | 1.051236 | 1.05115 | 1.051271 | 0 |

## Thay đổi so với baseline

| parameter | level | baseline_level | metric | n_pairs | baseline_median | level_median | percent_change | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | IGD | 30 | 0.005159663 | 0.0105921 | 105.2866 | higher |
| pop_size | 50 | 100 | HV | 30 | 1.051176 | 1.04766 | -0.3345269 | lower |
| pop_size | 50 | 100 | runtime_seconds | 30 | 12.08442 | 14.9385 | 23.61793 | higher |
| pop_size | 100 | 100 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| pop_size | 100 | 100 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| pop_size | 100 | 100 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| pop_size | 200 | 100 | IGD | 30 | 0.005159663 | 0.00249304 | -51.68211 | lower |
| pop_size | 200 | 100 | HV | 30 | 1.051176 | 1.052801 | 0.15455 | higher |
| pop_size | 200 | 100 | runtime_seconds | 30 | 12.08442 | 16.26203 | 34.5703 | higher |
| stagnation_patience | 10 | 20 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_patience | 10 | 20 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_patience | 10 | 20 | runtime_seconds | 30 | 12.08442 | 15.19048 | 25.70309 | higher |
| stagnation_patience | 20 | 20 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_patience | 20 | 20 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_patience | 20 | 20 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| stagnation_patience | 40 | 20 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_patience | 40 | 20 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_patience | 40 | 20 | runtime_seconds | 30 | 12.08442 | 3.909189 | -67.65098 | lower |
| stagnation_tolerance | 1e-05 | 0.0001 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | runtime_seconds | 30 | 12.08442 | 3.922916 | -67.53739 | lower |
| stagnation_tolerance | 0.0001 | 0.0001 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | runtime_seconds | 30 | 12.08442 | 4.665938 | -61.3888 | lower |
| diversity_threshold | 0.01 | 0.02 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | runtime_seconds | 30 | 12.08442 | 4.571022 | -62.17424 | lower |
| diversity_threshold | 0.02 | 0.02 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | runtime_seconds | 30 | 12.08442 | 3.805017 | -68.51302 | lower |
| restart_elite_ratio | 0.8 | 0.8 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | runtime_seconds | 30 | 12.08442 | 3.853288 | -68.11358 | lower |
| restart_elite_ratio | 0.95 | 0.8 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | runtime_seconds | 30 | 12.08442 | 3.807267 | -68.49441 | lower |
| prob_de | 0.2 | 0.5 | IGD | 30 | 0.005159663 | 0.00515625 | -0.06615978 | lower |
| prob_de | 0.2 | 0.5 | HV | 30 | 1.051176 | 1.051175 | -0.0001108924 | lower |
| prob_de | 0.2 | 0.5 | runtime_seconds | 30 | 12.08442 | 3.564045 | -70.5071 | lower |
| prob_de | 0.5 | 0.5 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| prob_de | 0.8 | 0.5 | IGD | 30 | 0.005159663 | 0.00512136 | -0.7423587 | lower |
| prob_de | 0.8 | 0.5 | HV | 30 | 1.051176 | 1.051268 | 0.008720554 | higher |
| prob_de | 0.8 | 0.5 | runtime_seconds | 30 | 12.08442 | 3.715286 | -69.25556 | lower |
| n_neighbors | 3 | 5 | IGD | 30 | 0.005159663 | 0.005000728 | -3.080348 | lower |
| n_neighbors | 3 | 5 | HV | 30 | 1.051176 | 1.051322 | 0.01388188 | higher |
| n_neighbors | 3 | 5 | runtime_seconds | 30 | 12.08442 | 3.6507 | -69.79001 | lower |
| n_neighbors | 5 | 5 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| n_neighbors | 5 | 5 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| n_neighbors | 5 | 5 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| n_neighbors | 10 | 5 | IGD | 30 | 0.005159663 | 0.005057805 | -1.974126 | lower |
| n_neighbors | 10 | 5 | HV | 30 | 1.051176 | 1.051288 | 0.01063868 | higher |
| n_neighbors | 10 | 5 | runtime_seconds | 30 | 12.08442 | 3.642827 | -69.85517 | lower |
| mean_F | 0.4 | 0.65 | IGD | 30 | 0.005159663 | 0.004957912 | -3.910158 | lower |
| mean_F | 0.4 | 0.65 | HV | 30 | 1.051176 | 1.051304 | 0.01218354 | higher |
| mean_F | 0.4 | 0.65 | runtime_seconds | 30 | 12.08442 | 3.723412 | -69.18832 | lower |
| mean_F | 0.65 | 0.65 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| mean_F | 0.9 | 0.65 | IGD | 30 | 0.005159663 | 0.004913864 | -4.763854 | lower |
| mean_F | 0.9 | 0.65 | HV | 30 | 1.051176 | 1.051295 | 0.011273 | higher |
| mean_F | 0.9 | 0.65 | runtime_seconds | 30 | 12.08442 | 3.657189 | -69.73631 | lower |
| mean_CR | 0.1 | 0.5 | IGD | 30 | 0.005159663 | 0.005186618 | 0.5224149 | higher |
| mean_CR | 0.1 | 0.5 | HV | 30 | 1.051176 | 1.051244 | 0.006416419 | higher |
| mean_CR | 0.1 | 0.5 | runtime_seconds | 30 | 12.08442 | 3.842283 | -68.20464 | lower |
| mean_CR | 0.5 | 0.5 | IGD | 30 | 0.005159663 | 0.005159663 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | HV | 30 | 1.051176 | 1.051176 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | runtime_seconds | 30 | 12.08442 | 12.08442 | 0 | unchanged |
| mean_CR | 0.9 | 0.5 | IGD | 30 | 0.005159663 | 0.005122476 | -0.7207326 | lower |
| mean_CR | 0.9 | 0.5 | HV | 30 | 1.051176 | 1.051236 | 0.005738809 | higher |
| mean_CR | 0.9 | 0.5 | runtime_seconds | 30 | 12.08442 | 14.21826 | 17.65783 | higher |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [comparisons.csv](../csv_results.zip) (81 dòng)
- [paired_seed_changes.csv](../csv_results.zip) (1620 dòng)
- [prob_de_paired_plot_data.csv](../csv_results.zip) (4 dòng)
- [raw_runs.csv](../csv_results.zip) (570 dòng)
- [response_diagnostics.csv](../csv_results.zip) (18 dòng)
- [summary.csv](../csv_results.zip) (27 dòng)

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
