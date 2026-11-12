# ZDT6 — Độ nhạy tham số adaptive OFAT

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt6` trong đợt `sensitivity_adaptive`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **570 dòng raw**, **30 seed** (6000–6029), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số: median và IQR

| parameter | level | baseline_level | runs | valid_runs | IGD_median | IGD_q25 | IGD_q75 | HV_median | HV_q25 | HV_q75 | restart_completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | 30 | 30 | 0.007340236 | 0.00716027 | 0.007554611 | 0.4346082 | 0.4341984 | 0.4349417 | 1 |
| pop_size | 100 | 100 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| pop_size | 200 | 100 | 30 | 30 | 0.0024559 | 0.002334737 | 0.002554453 | 0.4394865 | 0.439365 | 0.4397991 | 1 |
| stagnation_patience | 10 | 20 | 30 | 30 | 0.003868254 | 0.003685289 | 0.003998235 | 0.4382281 | 0.4381075 | 0.4383224 | 25 |
| stagnation_patience | 20 | 20 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| stagnation_patience | 40 | 20 | 30 | 30 | 0.003830559 | 0.003673112 | 0.004029485 | 0.4382656 | 0.4381214 | 0.4383724 | 1 |
| stagnation_tolerance | 1e-05 | 0.0001 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383724 | 7 |
| stagnation_tolerance | 0.0001 | 0.0001 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| stagnation_tolerance | 0.001 | 0.0001 | 30 | 30 | 0.003824873 | 0.003692415 | 0.003947091 | 0.4382656 | 0.4380735 | 0.4383927 | 16 |
| diversity_threshold | 0.01 | 0.02 | 30 | 30 | 0.003830559 | 0.00368396 | 0.004029485 | 0.4382568 | 0.4381075 | 0.438363 | 0 |
| diversity_threshold | 0.02 | 0.02 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| diversity_threshold | 0.05 | 0.02 | 30 | 30 | 0.003795594 | 0.003649798 | 0.003908588 | 0.4381979 | 0.4380353 | 0.4383308 | 78 |
| restart_elite_ratio | 0.8 | 0.8 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| restart_elite_ratio | 0.9 | 0.8 | 30 | 30 | 0.003845519 | 0.003673112 | 0.004008624 | 0.4382656 | 0.4381214 | 0.4383881 | 7 |
| restart_elite_ratio | 0.95 | 0.8 | 30 | 30 | 0.003830559 | 0.003670631 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| prob_de | 0.2 | 0.5 | 30 | 30 | 0.003951477 | 0.003794714 | 0.004216221 | 0.4376468 | 0.4375509 | 0.4379017 | 22 |
| prob_de | 0.5 | 0.5 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| prob_de | 0.8 | 0.5 | 30 | 30 | 0.003628518 | 0.003496851 | 0.003761904 | 0.4387729 | 0.4384931 | 0.4390173 | 2 |
| n_neighbors | 3 | 5 | 30 | 30 | 0.003809653 | 0.003597068 | 0.003906037 | 0.4382845 | 0.4381589 | 0.4385174 | 3 |
| n_neighbors | 5 | 5 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| n_neighbors | 10 | 5 | 30 | 30 | 0.003838441 | 0.00370888 | 0.004003751 | 0.4380905 | 0.4379444 | 0.4382733 | 7 |
| mean_F | 0.4 | 0.65 | 30 | 30 | 0.003809554 | 0.003720046 | 0.003898796 | 0.4381478 | 0.4379798 | 0.4382672 | 4 |
| mean_F | 0.65 | 0.65 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| mean_F | 0.9 | 0.65 | 30 | 30 | 0.003889477 | 0.003749415 | 0.003956469 | 0.4382496 | 0.4380466 | 0.438368 | 4 |
| mean_CR | 0.1 | 0.5 | 30 | 30 | 0.003696408 | 0.003566561 | 0.003794171 | 0.4385607 | 0.4384051 | 0.438671 | 8 |
| mean_CR | 0.5 | 0.5 | 30 | 30 | 0.003827524 | 0.003675803 | 0.003967707 | 0.4382656 | 0.4381214 | 0.4383881 | 6 |
| mean_CR | 0.9 | 0.5 | 30 | 30 | 0.003927335 | 0.003827292 | 0.004112927 | 0.4379385 | 0.4376864 | 0.438194 | 9 |

## Thay đổi so với baseline

| parameter | level | baseline_level | metric | n_pairs | baseline_median | level_median | percent_change | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 100 | IGD | 30 | 0.003827524 | 0.007340236 | 91.77506 | higher |
| pop_size | 50 | 100 | HV | 30 | 0.4382656 | 0.4346082 | -0.8345163 | lower |
| pop_size | 50 | 100 | runtime_seconds | 30 | 14.65193 | 12.07283 | -17.60242 | lower |
| pop_size | 100 | 100 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| pop_size | 100 | 100 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| pop_size | 100 | 100 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| pop_size | 200 | 100 | IGD | 30 | 0.003827524 | 0.0024559 | -35.8358 | lower |
| pop_size | 200 | 100 | HV | 30 | 0.4382656 | 0.4394865 | 0.2785907 | higher |
| pop_size | 200 | 100 | runtime_seconds | 30 | 14.65193 | 16.88718 | 15.25572 | higher |
| stagnation_patience | 10 | 20 | IGD | 30 | 0.003827524 | 0.003868254 | 1.064143 | higher |
| stagnation_patience | 10 | 20 | HV | 30 | 0.4382656 | 0.4382281 | -0.008554277 | lower |
| stagnation_patience | 10 | 20 | runtime_seconds | 30 | 14.65193 | 13.7423 | -6.208234 | lower |
| stagnation_patience | 20 | 20 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| stagnation_patience | 20 | 20 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| stagnation_patience | 20 | 20 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| stagnation_patience | 40 | 20 | IGD | 30 | 0.003827524 | 0.003830559 | 0.07930315 | higher |
| stagnation_patience | 40 | 20 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| stagnation_patience | 40 | 20 | runtime_seconds | 30 | 14.65193 | 4.468298 | -69.50368 | lower |
| stagnation_tolerance | 1e-05 | 0.0001 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| stagnation_tolerance | 1e-05 | 0.0001 | runtime_seconds | 30 | 14.65193 | 3.879169 | -73.52451 | lower |
| stagnation_tolerance | 0.0001 | 0.0001 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| stagnation_tolerance | 0.0001 | 0.0001 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | IGD | 30 | 0.003827524 | 0.003824873 | -0.06926389 | lower |
| stagnation_tolerance | 0.001 | 0.0001 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| stagnation_tolerance | 0.001 | 0.0001 | runtime_seconds | 30 | 14.65193 | 3.962967 | -72.95259 | lower |
| diversity_threshold | 0.01 | 0.02 | IGD | 30 | 0.003827524 | 0.003830559 | 0.07930315 | higher |
| diversity_threshold | 0.01 | 0.02 | HV | 30 | 0.4382656 | 0.4382568 | -0.00200892 | lower |
| diversity_threshold | 0.01 | 0.02 | runtime_seconds | 30 | 14.65193 | 4.775121 | -67.4096 | lower |
| diversity_threshold | 0.02 | 0.02 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| diversity_threshold | 0.02 | 0.02 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| diversity_threshold | 0.05 | 0.02 | IGD | 30 | 0.003827524 | 0.003795594 | -0.8342299 | lower |
| diversity_threshold | 0.05 | 0.02 | HV | 30 | 0.4382656 | 0.4381979 | -0.01543386 | lower |
| diversity_threshold | 0.05 | 0.02 | runtime_seconds | 30 | 14.65193 | 3.750412 | -74.40328 | lower |
| restart_elite_ratio | 0.8 | 0.8 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| restart_elite_ratio | 0.8 | 0.8 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | IGD | 30 | 0.003827524 | 0.003845519 | 0.4701471 | higher |
| restart_elite_ratio | 0.9 | 0.8 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| restart_elite_ratio | 0.9 | 0.8 | runtime_seconds | 30 | 14.65193 | 3.799661 | -74.06716 | lower |
| restart_elite_ratio | 0.95 | 0.8 | IGD | 30 | 0.003827524 | 0.003830559 | 0.07930315 | higher |
| restart_elite_ratio | 0.95 | 0.8 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| restart_elite_ratio | 0.95 | 0.8 | runtime_seconds | 30 | 14.65193 | 3.593575 | -75.4737 | lower |
| prob_de | 0.2 | 0.5 | IGD | 30 | 0.003827524 | 0.003951477 | 3.238474 | higher |
| prob_de | 0.2 | 0.5 | HV | 30 | 0.4382656 | 0.4376468 | -0.1411843 | lower |
| prob_de | 0.2 | 0.5 | runtime_seconds | 30 | 14.65193 | 3.358436 | -77.07853 | lower |
| prob_de | 0.5 | 0.5 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| prob_de | 0.5 | 0.5 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| prob_de | 0.8 | 0.5 | IGD | 30 | 0.003827524 | 0.003628518 | -5.19933 | lower |
| prob_de | 0.8 | 0.5 | HV | 30 | 0.4382656 | 0.4387729 | 0.1157521 | higher |
| prob_de | 0.8 | 0.5 | runtime_seconds | 30 | 14.65193 | 3.718421 | -74.62162 | lower |
| n_neighbors | 3 | 5 | IGD | 30 | 0.003827524 | 0.003809653 | -0.4669179 | lower |
| n_neighbors | 3 | 5 | HV | 30 | 0.4382656 | 0.4382845 | 0.004321752 | higher |
| n_neighbors | 3 | 5 | runtime_seconds | 30 | 14.65193 | 3.621872 | -75.28057 | lower |
| n_neighbors | 5 | 5 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| n_neighbors | 5 | 5 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| n_neighbors | 5 | 5 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| n_neighbors | 10 | 5 | IGD | 30 | 0.003827524 | 0.003838441 | 0.2852198 | higher |
| n_neighbors | 10 | 5 | HV | 30 | 0.4382656 | 0.4380905 | -0.03993394 | lower |
| n_neighbors | 10 | 5 | runtime_seconds | 30 | 14.65193 | 3.641967 | -75.14342 | lower |
| mean_F | 0.4 | 0.65 | IGD | 30 | 0.003827524 | 0.003809554 | -0.4694884 | lower |
| mean_F | 0.4 | 0.65 | HV | 30 | 0.4382656 | 0.4381478 | -0.02686629 | lower |
| mean_F | 0.4 | 0.65 | runtime_seconds | 30 | 14.65193 | 3.536941 | -75.86023 | lower |
| mean_F | 0.65 | 0.65 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| mean_F | 0.65 | 0.65 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| mean_F | 0.9 | 0.65 | IGD | 30 | 0.003827524 | 0.003889477 | 1.618622 | higher |
| mean_F | 0.9 | 0.65 | HV | 30 | 0.4382656 | 0.4382496 | -0.003631087 | lower |
| mean_F | 0.9 | 0.65 | runtime_seconds | 30 | 14.65193 | 3.49011 | -76.17985 | lower |
| mean_CR | 0.1 | 0.5 | IGD | 30 | 0.003827524 | 0.003696408 | -3.425615 | lower |
| mean_CR | 0.1 | 0.5 | HV | 30 | 0.4382656 | 0.4385607 | 0.06733852 | higher |
| mean_CR | 0.1 | 0.5 | runtime_seconds | 30 | 14.65193 | 5.401082 | -63.1374 | lower |
| mean_CR | 0.5 | 0.5 | IGD | 30 | 0.003827524 | 0.003827524 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | HV | 30 | 0.4382656 | 0.4382656 | 0 | unchanged |
| mean_CR | 0.5 | 0.5 | runtime_seconds | 30 | 14.65193 | 14.65193 | 0 | unchanged |
| mean_CR | 0.9 | 0.5 | IGD | 30 | 0.003827524 | 0.003927335 | 2.607713 | higher |
| mean_CR | 0.9 | 0.5 | HV | 30 | 0.4382656 | 0.4379385 | -0.07463621 | lower |
| mean_CR | 0.9 | 0.5 | runtime_seconds | 30 | 14.65193 | 13.10347 | -10.56827 | lower |

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
