# ZDT4 — Độ nhạy tham số adaptive OFAT

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt4` trong đợt `sensitivity_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **570 dòng raw**, **30 seed** (6000–6029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số: median và IQR

| parameter | level | baseline_level | runs | valid_runs | IGD_median | IGD_q25 | IGD_q75 | HV_median | HV_q25 | HV_q75 | restart_completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | 30 | 30 | 0.00889516 | 0.00873444 | 0.009318254 | 0.8638225 | 0.8632123 | 0.8646262 | 0 |
| pop_size | 100 | 100 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| pop_size | 200 | 100 | 30 | 30 | 0.5984772 | 0.3592549 | 0.9324992 | 0.09285597 | 0.002236884 | 0.3093798 | 0 |
| stagnation_patience | 10 | 20 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| stagnation_patience | 20 | 20 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| stagnation_patience | 40 | 20 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| stagnation_tolerance | 1e-05 | 0.0001 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| stagnation_tolerance | 0.0001 | 0.0001 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| stagnation_tolerance | 0.001 | 0.0001 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| diversity_threshold | 0.01 | 0.02 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| diversity_threshold | 0.02 | 0.02 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| diversity_threshold | 0.05 | 0.02 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| restart_elite_ratio | 0.8 | 0.8 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| restart_elite_ratio | 0.9 | 0.8 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| restart_elite_ratio | 0.95 | 0.8 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| prob_de | 0.2 | 0.5 | 30 | 30 | 0.01140357 | 0.007945389 | 0.02168105 | 0.8568599 | 0.8380654 | 0.8626692 | 0 |
| prob_de | 0.5 | 0.5 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| prob_de | 0.8 | 0.5 | 30 | 30 | 0.004660071 | 0.004499782 | 0.004997017 | 0.8693266 | 0.8687377 | 0.8696609 | 0 |
| n_neighbors | 3 | 5 | 30 | 30 | 0.005840398 | 0.004977974 | 0.008118307 | 0.866702 | 0.8627602 | 0.8685097 | 0 |
| n_neighbors | 5 | 5 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| n_neighbors | 10 | 5 | 30 | 30 | 0.005288554 | 0.004795761 | 0.007068405 | 0.8677737 | 0.8643892 | 0.8690949 | 0 |
| mean_F | 0.4 | 0.65 | 30 | 30 | 0.005076778 | 0.00467334 | 0.007692336 | 0.868173 | 0.8629945 | 0.8691902 | 0 |
| mean_F | 0.65 | 0.65 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| mean_F | 0.9 | 0.65 | 30 | 30 | 0.00609374 | 0.005000754 | 0.007863512 | 0.8665989 | 0.8626457 | 0.8684246 | 0 |
| mean_CR | 0.1 | 0.5 | 30 | 30 | 0.005416496 | 0.004867904 | 0.006738787 | 0.8676508 | 0.8650069 | 0.8692665 | 0 |
| mean_CR | 0.5 | 0.5 | 30 | 30 | 0.005582561 | 0.004973281 | 0.006697578 | 0.8672159 | 0.8646886 | 0.868644 | 0 |
| mean_CR | 0.9 | 0.5 | 30 | 30 | 0.005549007 | 0.005047991 | 0.006797795 | 0.8673124 | 0.8649933 | 0.8682642 | 0 |

## Thay đổi so với baseline

| parameter | level | baseline_level | metric | n_pairs | baseline_median | level_median | percent_change | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | IGD | 30 | 0.005582561 | 0.00889516 | 59.33835 | higher |
| pop_size | 50 | 100 | HV | 30 | 0.8672159 | 0.8638225 | -0.3912954 | lower |
| pop_size | 50 | 100 | runtime_seconds | 30 | 14.37475 | 14.25634 | -0.8237346 | lower |
| pop_size | 100 | 100 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| pop_size | 100 | 100 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| pop_size | 100 | 100 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| pop_size | 200 | 100 | IGD | 30 | 0.005582561 | 0.5984772 | 10620.48 | higher |
| pop_size | 200 | 100 | HV | 30 | 0.8672159 | 0.09285597 | -89.29263 | lower |
| pop_size | 200 | 100 | runtime_seconds | 30 | 14.37475 | 20.02 | 39.27197 | higher |
| stagnation_patience | 10 | 20 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_patience | 10 | 20 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_patience | 10 | 20 | runtime_seconds | 30 | 14.37475 | 15.76387 | 9.663615 | higher |
| stagnation_patience | 20 | 20 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_patience | 20 | 20 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_patience | 20 | 20 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| stagnation_patience | 40 | 20 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_patience | 40 | 20 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_patience | 40 | 20 | runtime_seconds | 30 | 14.37475 | 4.442081 | -69.09803 | lower |
| stagnation_tolerance | 1e-05 | 0.0001 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | runtime_seconds | 30 | 14.37475 | 4.456531 | -68.99751 | lower |
| stagnation_tolerance | 0.0001 | 0.0001 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | runtime_seconds | 30 | 14.37475 | 4.907664 | -65.85914 | lower |
| diversity_threshold | 0.01 | 0.02 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | runtime_seconds | 30 | 14.37475 | 5.413338 | -62.34135 | lower |
| diversity_threshold | 0.02 | 0.02 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | runtime_seconds | 30 | 14.37475 | 4.419644 | -69.25412 | lower |
| restart_elite_ratio | 0.8 | 0.8 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | runtime_seconds | 30 | 14.37475 | 4.37237 | -69.58299 | lower |
| restart_elite_ratio | 0.95 | 0.8 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | runtime_seconds | 30 | 14.37475 | 4.32038 | -69.94466 | lower |
| prob_de | 0.2 | 0.5 | IGD | 30 | 0.005582561 | 0.01140357 | 104.2713 | higher |
| prob_de | 0.2 | 0.5 | HV | 30 | 0.8672159 | 0.8568599 | -1.194163 | lower |
| prob_de | 0.2 | 0.5 | runtime_seconds | 30 | 14.37475 | 4.032356 | -71.94834 | lower |
| prob_de | 0.5 | 0.5 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| prob_de | 0.8 | 0.5 | IGD | 30 | 0.005582561 | 0.004660071 | -16.52449 | lower |
| prob_de | 0.8 | 0.5 | HV | 30 | 0.8672159 | 0.8693266 | 0.2433891 | higher |
| prob_de | 0.8 | 0.5 | runtime_seconds | 30 | 14.37475 | 4.186099 | -70.87881 | lower |
| n_neighbors | 3 | 5 | IGD | 30 | 0.005582561 | 0.005840398 | 4.618628 | higher |
| n_neighbors | 3 | 5 | HV | 30 | 0.8672159 | 0.866702 | -0.05925732 | lower |
| n_neighbors | 3 | 5 | runtime_seconds | 30 | 14.37475 | 4.24792 | -70.44874 | lower |
| n_neighbors | 5 | 5 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| n_neighbors | 5 | 5 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| n_neighbors | 5 | 5 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| n_neighbors | 10 | 5 | IGD | 30 | 0.005582561 | 0.005288554 | -5.26652 | lower |
| n_neighbors | 10 | 5 | HV | 30 | 0.8672159 | 0.8677737 | 0.06432318 | higher |
| n_neighbors | 10 | 5 | runtime_seconds | 30 | 14.37475 | 4.295803 | -70.11563 | lower |
| mean_F | 0.4 | 0.65 | IGD | 30 | 0.005582561 | 0.005076778 | -9.060052 | lower |
| mean_F | 0.4 | 0.65 | HV | 30 | 0.8672159 | 0.868173 | 0.1103676 | higher |
| mean_F | 0.4 | 0.65 | runtime_seconds | 30 | 14.37475 | 4.314227 | -69.98747 | lower |
| mean_F | 0.65 | 0.65 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| mean_F | 0.9 | 0.65 | IGD | 30 | 0.005582561 | 0.00609374 | 9.156714 | higher |
| mean_F | 0.9 | 0.65 | HV | 30 | 0.8672159 | 0.8665989 | -0.07114122 | lower |
| mean_F | 0.9 | 0.65 | runtime_seconds | 30 | 14.37475 | 4.178118 | -70.93432 | lower |
| mean_CR | 0.1 | 0.5 | IGD | 30 | 0.005582561 | 0.005416496 | -2.974707 | lower |
| mean_CR | 0.1 | 0.5 | HV | 30 | 0.8672159 | 0.8676508 | 0.05015432 | higher |
| mean_CR | 0.1 | 0.5 | runtime_seconds | 30 | 14.37475 | 4.140388 | -71.1968 | lower |
| mean_CR | 0.5 | 0.5 | IGD | 30 | 0.005582561 | 0.005582561 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | HV | 30 | 0.8672159 | 0.8672159 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | runtime_seconds | 30 | 14.37475 | 14.37475 | 0 | unchanged |
| mean_CR | 0.9 | 0.5 | IGD | 30 | 0.005582561 | 0.005549007 | -0.6010394 | lower |
| mean_CR | 0.9 | 0.5 | HV | 30 | 0.8672159 | 0.8673124 | 0.01112663 | higher |
| mean_CR | 0.9 | 0.5 | runtime_seconds | 30 | 14.37475 | 15.52093 | 7.97356 | higher |

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
