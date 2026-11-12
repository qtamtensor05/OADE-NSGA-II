# ZDT1 — Độ nhạy tham số adaptive OFAT

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt1` trong đợt `sensitivity_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **570 dòng raw**, **30 seed** (6000–6029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số: median và IQR

| parameter | level | baseline_level | runs | valid_runs | IGD_median | IGD_q25 | IGD_q75 | HV_median | HV_q25 | HV_q75 | restart_completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | 30 | 30 | 0.009106426 | 0.008765003 | 0.009617902 | 0.8647541 | 0.86377 | 0.8651147 | 0 |
| pop_size | 100 | 100 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| pop_size | 200 | 100 | 30 | 30 | 0.002229231 | 0.002122772 | 0.0022936 | 0.8738196 | 0.8737621 | 0.873846 | 0 |
| stagnation_patience | 10 | 20 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| stagnation_patience | 20 | 20 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| stagnation_patience | 40 | 20 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| stagnation_tolerance | 1e-05 | 0.0001 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| stagnation_tolerance | 0.0001 | 0.0001 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| stagnation_tolerance | 0.001 | 0.0001 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| diversity_threshold | 0.01 | 0.02 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| diversity_threshold | 0.02 | 0.02 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| diversity_threshold | 0.05 | 0.02 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| restart_elite_ratio | 0.8 | 0.8 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| restart_elite_ratio | 0.9 | 0.8 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| restart_elite_ratio | 0.95 | 0.8 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| prob_de | 0.2 | 0.5 | 30 | 30 | 0.00443502 | 0.004214471 | 0.004562316 | 0.8709796 | 0.8708543 | 0.8711354 | 0 |
| prob_de | 0.5 | 0.5 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| prob_de | 0.8 | 0.5 | 30 | 30 | 0.004421124 | 0.00426895 | 0.004642976 | 0.8709408 | 0.8707363 | 0.8710816 | 0 |
| n_neighbors | 3 | 5 | 30 | 30 | 0.004516503 | 0.004407531 | 0.004684764 | 0.8708716 | 0.8706613 | 0.8710778 | 0 |
| n_neighbors | 5 | 5 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| n_neighbors | 10 | 5 | 30 | 30 | 0.004423577 | 0.004348593 | 0.004549751 | 0.8708561 | 0.8706915 | 0.8710589 | 0 |
| mean_F | 0.4 | 0.65 | 30 | 30 | 0.004483116 | 0.004318224 | 0.004561717 | 0.870919 | 0.8707943 | 0.8710166 | 0 |
| mean_F | 0.65 | 0.65 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| mean_F | 0.9 | 0.65 | 30 | 30 | 0.004420456 | 0.004352576 | 0.004517801 | 0.8709589 | 0.8707498 | 0.8710652 | 0 |
| mean_CR | 0.1 | 0.5 | 30 | 30 | 0.004359676 | 0.004246316 | 0.004635673 | 0.8709593 | 0.870896 | 0.871112 | 0 |
| mean_CR | 0.5 | 0.5 | 30 | 30 | 0.004397074 | 0.004254753 | 0.004621646 | 0.8709617 | 0.8708204 | 0.8710262 | 0 |
| mean_CR | 0.9 | 0.5 | 30 | 30 | 0.004387746 | 0.004222984 | 0.004537309 | 0.8708849 | 0.8707322 | 0.8710649 | 0 |

## Thay đổi so với baseline

| parameter | level | baseline_level | metric | n_pairs | baseline_median | level_median | percent_change | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | IGD | 30 | 0.004397074 | 0.009106426 | 107.102 | higher |
| pop_size | 50 | 100 | HV | 30 | 0.8709617 | 0.8647541 | -0.7127253 | lower |
| pop_size | 50 | 100 | runtime_seconds | 30 | 5.942742 | 14.15178 | 138.1356 | higher |
| pop_size | 100 | 100 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| pop_size | 100 | 100 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| pop_size | 100 | 100 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| pop_size | 200 | 100 | IGD | 30 | 0.004397074 | 0.002229231 | -49.30193 | lower |
| pop_size | 200 | 100 | HV | 30 | 0.8709617 | 0.8738196 | 0.3281379 | higher |
| pop_size | 200 | 100 | runtime_seconds | 30 | 5.942742 | 16.16663 | 172.0399 | higher |
| stagnation_patience | 10 | 20 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_patience | 10 | 20 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_patience | 10 | 20 | runtime_seconds | 30 | 5.942742 | 14.11387 | 137.4975 | higher |
| stagnation_patience | 20 | 20 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_patience | 20 | 20 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_patience | 20 | 20 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| stagnation_patience | 40 | 20 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_patience | 40 | 20 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_patience | 40 | 20 | runtime_seconds | 30 | 5.942742 | 6.715179 | 12.998 | higher |
| stagnation_tolerance | 1e-05 | 0.0001 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | runtime_seconds | 30 | 5.942742 | 4.688152 | -21.1113 | lower |
| stagnation_tolerance | 0.0001 | 0.0001 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | runtime_seconds | 30 | 5.942742 | 3.913771 | -34.142 | lower |
| diversity_threshold | 0.01 | 0.02 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| diversity_threshold | 0.01 | 0.02 | runtime_seconds | 30 | 5.942742 | 3.890993 | -34.52528 | lower |
| diversity_threshold | 0.02 | 0.02 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | runtime_seconds | 30 | 5.942742 | 4.121195 | -30.65162 | lower |
| restart_elite_ratio | 0.8 | 0.8 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | runtime_seconds | 30 | 5.942742 | 3.790249 | -36.22053 | lower |
| restart_elite_ratio | 0.95 | 0.8 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | runtime_seconds | 30 | 5.942742 | 3.748237 | -36.92748 | lower |
| prob_de | 0.2 | 0.5 | IGD | 30 | 0.004397074 | 0.00443502 | 0.8629797 | higher |
| prob_de | 0.2 | 0.5 | HV | 30 | 0.8709617 | 0.8709796 | 0.00206148 | higher |
| prob_de | 0.2 | 0.5 | runtime_seconds | 30 | 5.942742 | 3.480068 | -41.44002 | lower |
| prob_de | 0.5 | 0.5 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| prob_de | 0.8 | 0.5 | IGD | 30 | 0.004397074 | 0.004421124 | 0.5469547 | higher |
| prob_de | 0.8 | 0.5 | HV | 30 | 0.8709617 | 0.8709408 | -0.002396259 | lower |
| prob_de | 0.8 | 0.5 | runtime_seconds | 30 | 5.942742 | 3.672309 | -38.20514 | lower |
| n_neighbors | 3 | 5 | IGD | 30 | 0.004397074 | 0.004516503 | 2.716099 | higher |
| n_neighbors | 3 | 5 | HV | 30 | 0.8709617 | 0.8708716 | -0.01034264 | lower |
| n_neighbors | 3 | 5 | runtime_seconds | 30 | 5.942742 | 3.630456 | -38.9094 | lower |
| n_neighbors | 5 | 5 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| n_neighbors | 5 | 5 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| n_neighbors | 5 | 5 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| n_neighbors | 10 | 5 | IGD | 30 | 0.004397074 | 0.004423577 | 0.6027498 | higher |
| n_neighbors | 10 | 5 | HV | 30 | 0.8709617 | 0.8708561 | -0.01212559 | lower |
| n_neighbors | 10 | 5 | runtime_seconds | 30 | 5.942742 | 3.732146 | -37.19825 | lower |
| mean_F | 0.4 | 0.65 | IGD | 30 | 0.004397074 | 0.004483116 | 1.956815 | higher |
| mean_F | 0.4 | 0.65 | HV | 30 | 0.8709617 | 0.870919 | -0.004902026 | lower |
| mean_F | 0.4 | 0.65 | runtime_seconds | 30 | 5.942742 | 3.674778 | -38.1636 | lower |
| mean_F | 0.65 | 0.65 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| mean_F | 0.9 | 0.65 | IGD | 30 | 0.004397074 | 0.004420456 | 0.5317667 | higher |
| mean_F | 0.9 | 0.65 | HV | 30 | 0.8709617 | 0.8709589 | -0.0003156493 | lower |
| mean_F | 0.9 | 0.65 | runtime_seconds | 30 | 5.942742 | 3.829144 | -35.56604 | lower |
| mean_CR | 0.1 | 0.5 | IGD | 30 | 0.004397074 | 0.004359676 | -0.8505191 | lower |
| mean_CR | 0.1 | 0.5 | HV | 30 | 0.8709617 | 0.8709593 | -0.0002746753 | lower |
| mean_CR | 0.1 | 0.5 | runtime_seconds | 30 | 5.942742 | 3.493832 | -41.20842 | lower |
| mean_CR | 0.5 | 0.5 | IGD | 30 | 0.004397074 | 0.004397074 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | HV | 30 | 0.8709617 | 0.8709617 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | runtime_seconds | 30 | 5.942742 | 5.942742 | 0 | unchanged |
| mean_CR | 0.9 | 0.5 | IGD | 30 | 0.004397074 | 0.004387746 | -0.2121337 | lower |
| mean_CR | 0.9 | 0.5 | HV | 30 | 0.8709617 | 0.8708849 | -0.008814427 | lower |
| mean_CR | 0.9 | 0.5 | runtime_seconds | 30 | 5.942742 | 14.01264 | 135.7942 | higher |

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
