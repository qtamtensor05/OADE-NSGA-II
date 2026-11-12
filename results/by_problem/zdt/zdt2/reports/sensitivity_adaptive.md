# ZDT2 — Độ nhạy tham số adaptive OFAT

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt2` trong đợt `sensitivity_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **570 dòng raw**, **30 seed** (6000–6029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số: median và IQR

| parameter | level | baseline_level | runs | valid_runs | IGD_median | IGD_q25 | IGD_q75 | HV_median | HV_q25 | HV_q75 | restart_completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | 30 | 30 | 0.009402584 | 0.009155438 | 0.009644648 | 0.5319512 | 0.5315852 | 0.5323594 | 2 |
| pop_size | 100 | 100 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| pop_size | 200 | 100 | 30 | 30 | 0.002366914 | 0.002254487 | 0.002511581 | 0.540519 | 0.5404402 | 0.5405669 | 0 |
| stagnation_patience | 10 | 20 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.5376534 | 0.5375772 | 0.5378549 | 1 |
| stagnation_patience | 20 | 20 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| stagnation_patience | 40 | 20 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375772 | 0.5378549 | 0 |
| stagnation_tolerance | 1e-05 | 0.0001 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375772 | 0.5378549 | 0 |
| stagnation_tolerance | 0.0001 | 0.0001 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| stagnation_tolerance | 0.001 | 0.0001 | 30 | 30 | 0.004633391 | 0.004448731 | 0.004846822 | 0.5377069 | 0.5374803 | 0.5378817 | 4 |
| diversity_threshold | 0.01 | 0.02 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| diversity_threshold | 0.02 | 0.02 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| diversity_threshold | 0.05 | 0.02 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| restart_elite_ratio | 0.8 | 0.8 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| restart_elite_ratio | 0.9 | 0.8 | 30 | 30 | 0.004633391 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| restart_elite_ratio | 0.95 | 0.8 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.5376543 | 0.5375772 | 0.5378549 | 1 |
| prob_de | 0.2 | 0.5 | 30 | 30 | 0.004715966 | 0.004530828 | 0.004861617 | 0.5377588 | 0.5375227 | 0.5378248 | 0 |
| prob_de | 0.5 | 0.5 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| prob_de | 0.8 | 0.5 | 30 | 30 | 0.004611824 | 0.00439873 | 0.004752189 | 0.5377023 | 0.537529 | 0.5378281 | 5 |
| n_neighbors | 3 | 5 | 30 | 30 | 0.004639425 | 0.004466613 | 0.004878343 | 0.5376092 | 0.5375144 | 0.5377578 | 0 |
| n_neighbors | 5 | 5 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| n_neighbors | 10 | 5 | 30 | 30 | 0.004706783 | 0.004403133 | 0.005001039 | 0.5376728 | 0.5374858 | 0.5379104 | 0 |
| mean_F | 0.4 | 0.65 | 30 | 30 | 0.004726661 | 0.004576569 | 0.004991341 | 0.5377023 | 0.5375025 | 0.5378881 | 0 |
| mean_F | 0.65 | 0.65 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| mean_F | 0.9 | 0.65 | 30 | 30 | 0.004673203 | 0.004451099 | 0.004813775 | 0.5376875 | 0.5375836 | 0.5378162 | 0 |
| mean_CR | 0.1 | 0.5 | 30 | 30 | 0.004668907 | 0.004501589 | 0.004869662 | 0.5377635 | 0.5375965 | 0.537883 | 0 |
| mean_CR | 0.5 | 0.5 | 30 | 30 | 0.004664604 | 0.004448731 | 0.004846822 | 0.537652 | 0.5375612 | 0.5378549 | 1 |
| mean_CR | 0.9 | 0.5 | 30 | 30 | 0.004784851 | 0.004598727 | 0.005021825 | 0.5375702 | 0.5373134 | 0.5377936 | 1 |

## Thay đổi so với baseline

| parameter | level | baseline_level | metric | n_pairs | baseline_median | level_median | percent_change | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | IGD | 30 | 0.004664604 | 0.009402584 | 101.573 | higher |
| pop_size | 50 | 100 | HV | 30 | 0.537652 | 0.5319512 | -1.060314 | lower |
| pop_size | 50 | 100 | runtime_seconds | 30 | 18.70793 | 14.70112 | -21.4177 | lower |
| pop_size | 100 | 100 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| pop_size | 100 | 100 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| pop_size | 100 | 100 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| pop_size | 200 | 100 | IGD | 30 | 0.004664604 | 0.002366914 | -49.25799 | lower |
| pop_size | 200 | 100 | HV | 30 | 0.537652 | 0.540519 | 0.5332492 | higher |
| pop_size | 200 | 100 | runtime_seconds | 30 | 18.70793 | 16.91797 | -9.567953 | lower |
| stagnation_patience | 10 | 20 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| stagnation_patience | 10 | 20 | HV | 30 | 0.537652 | 0.5376534 | 0.0002584496 | higher |
| stagnation_patience | 10 | 20 | runtime_seconds | 30 | 18.70793 | 15.07793 | -19.40353 | lower |
| stagnation_patience | 20 | 20 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| stagnation_patience | 20 | 20 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| stagnation_patience | 20 | 20 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| stagnation_patience | 40 | 20 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| stagnation_patience | 40 | 20 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| stagnation_patience | 40 | 20 | runtime_seconds | 30 | 18.70793 | 4.903454 | -73.78944 | lower |
| stagnation_tolerance | 1e-05 | 0.0001 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | runtime_seconds | 30 | 18.70793 | 4.63722 | -75.21255 | lower |
| stagnation_tolerance | 0.0001 | 0.0001 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | IGD | 30 | 0.004664604 | 0.004633391 | -0.6691415 | lower |
| stagnation_tolerance | 0.001 | 0.0001 | HV | 30 | 0.537652 | 0.5377069 | 0.01020528 | higher |
| stagnation_tolerance | 0.001 | 0.0001 | runtime_seconds | 30 | 18.70793 | 4.502355 | -75.93344 | lower |
| diversity_threshold | 0.01 | 0.02 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | runtime_seconds | 30 | 18.70793 | 4.037952 | -78.41583 | lower |
| diversity_threshold | 0.02 | 0.02 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | runtime_seconds | 30 | 18.70793 | 3.975278 | -78.75084 | lower |
| restart_elite_ratio | 0.8 | 0.8 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | IGD | 30 | 0.004664604 | 0.004633391 | -0.6691415 | lower |
| restart_elite_ratio | 0.9 | 0.8 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | runtime_seconds | 30 | 18.70793 | 3.902448 | -79.14014 | lower |
| restart_elite_ratio | 0.95 | 0.8 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | HV | 30 | 0.537652 | 0.5376543 | 0.0004322297 | higher |
| restart_elite_ratio | 0.95 | 0.8 | runtime_seconds | 30 | 18.70793 | 3.824371 | -79.55749 | lower |
| prob_de | 0.2 | 0.5 | IGD | 30 | 0.004664604 | 0.004715966 | 1.101092 | higher |
| prob_de | 0.2 | 0.5 | HV | 30 | 0.537652 | 0.5377588 | 0.01986075 | higher |
| prob_de | 0.2 | 0.5 | runtime_seconds | 30 | 18.70793 | 3.660631 | -80.43273 | lower |
| prob_de | 0.5 | 0.5 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| prob_de | 0.8 | 0.5 | IGD | 30 | 0.004664604 | 0.004611824 | -1.131493 | lower |
| prob_de | 0.8 | 0.5 | HV | 30 | 0.537652 | 0.5377023 | 0.009352186 | higher |
| prob_de | 0.8 | 0.5 | runtime_seconds | 30 | 18.70793 | 3.799665 | -79.68955 | lower |
| n_neighbors | 3 | 5 | IGD | 30 | 0.004664604 | 0.004639425 | -0.5397864 | lower |
| n_neighbors | 3 | 5 | HV | 30 | 0.537652 | 0.5376092 | -0.007959627 | lower |
| n_neighbors | 3 | 5 | runtime_seconds | 30 | 18.70793 | 3.683363 | -80.31122 | lower |
| n_neighbors | 5 | 5 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| n_neighbors | 5 | 5 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| n_neighbors | 5 | 5 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| n_neighbors | 10 | 5 | IGD | 30 | 0.004664604 | 0.004706783 | 0.9042249 | higher |
| n_neighbors | 10 | 5 | HV | 30 | 0.537652 | 0.5376728 | 0.003857235 | higher |
| n_neighbors | 10 | 5 | runtime_seconds | 30 | 18.70793 | 3.786519 | -79.75982 | lower |
| mean_F | 0.4 | 0.65 | IGD | 30 | 0.004664604 | 0.004726661 | 1.33037 | higher |
| mean_F | 0.4 | 0.65 | HV | 30 | 0.537652 | 0.5377023 | 0.009348249 | higher |
| mean_F | 0.4 | 0.65 | runtime_seconds | 30 | 18.70793 | 3.730196 | -80.06088 | lower |
| mean_F | 0.65 | 0.65 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| mean_F | 0.9 | 0.65 | IGD | 30 | 0.004664604 | 0.004673203 | 0.1843423 | higher |
| mean_F | 0.9 | 0.65 | HV | 30 | 0.537652 | 0.5376875 | 0.006607315 | higher |
| mean_F | 0.9 | 0.65 | runtime_seconds | 30 | 18.70793 | 3.757103 | -79.91706 | lower |
| mean_CR | 0.1 | 0.5 | IGD | 30 | 0.004664604 | 0.004668907 | 0.09224747 | higher |
| mean_CR | 0.1 | 0.5 | HV | 30 | 0.537652 | 0.5377635 | 0.02073003 | higher |
| mean_CR | 0.1 | 0.5 | runtime_seconds | 30 | 18.70793 | 3.738838 | -80.01469 | lower |
| mean_CR | 0.5 | 0.5 | IGD | 30 | 0.004664604 | 0.004664604 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | HV | 30 | 0.537652 | 0.537652 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | runtime_seconds | 30 | 18.70793 | 18.70793 | 0 | unchanged |
| mean_CR | 0.9 | 0.5 | IGD | 30 | 0.004664604 | 0.004784851 | 2.577856 | higher |
| mean_CR | 0.9 | 0.5 | HV | 30 | 0.537652 | 0.5375702 | -0.01521577 | lower |
| mean_CR | 0.9 | 0.5 | runtime_seconds | 30 | 18.70793 | 14.20233 | -24.0839 | lower |

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
