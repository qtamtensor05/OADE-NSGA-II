# ZDT3 — hồ sơ nghiên cứu

[Báo cáo riêng của bài toán](reports/README.md)

Dữ liệu đã lọc riêng theo bài toán; giữ nguyên cột, giá trị và thứ tự dòng từ nguồn.

| Nhóm thí nghiệm | Số dòng raw | Số seed |
|---|---:|---:|
| [benchmark_classic](reports/benchmark_classic.md) | 210 | 30 |
| [benchmark_adaptive](reports/benchmark_adaptive.md) | 210 | 30 |
| [restart_confirmation](reports/restart_confirmation.md) | 90 | 30 |
| [ablation_classic](reports/ablation_classic.md) | 210 | 30 |
| [sensitivity_classic](reports/sensitivity_classic.md) | 420 | 30 |
| [sensitivity_adaptive](reports/sensitivity_adaptive.md) | 570 | 30 |

## Bảng và dữ liệu

- [benchmark_classic/algorithm_benchmark_convergence.csv](csv_results.zip) (2040 dòng)
- [benchmark_classic/algorithm_benchmark_cost_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_classic/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_classic/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (12 dòng)
- [benchmark_classic/algorithm_benchmark_raw_runs.csv](csv_results.zip) (210 dòng)
- [benchmark_classic/algorithm_benchmark_validation.csv](csv_results.zip) (210 dòng)
- [benchmark_adaptive/algorithm_benchmark_convergence.csv](csv_results.zip) (2041 dòng)
- [benchmark_adaptive/algorithm_benchmark_cost_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (7 dòng)
- [benchmark_adaptive/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (12 dòng)
- [benchmark_adaptive/algorithm_benchmark_raw_runs.csv](csv_results.zip) (210 dòng)
- [benchmark_adaptive/algorithm_benchmark_validation.csv](csv_results.zip) (210 dòng)
- [restart_confirmation/algorithm_benchmark_convergence.csv](csv_results.zip) (812 dòng)
- [restart_confirmation/algorithm_benchmark_cost_summary.csv](csv_results.zip) (3 dòng)
- [restart_confirmation/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (3 dòng)
- [restart_confirmation/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (4 dòng)
- [restart_confirmation/algorithm_benchmark_raw_runs.csv](csv_results.zip) (90 dòng)
- [restart_confirmation/algorithm_benchmark_validation.csv](csv_results.zip) (90 dòng)
- [ablation_classic/algorithm_benchmark_convergence.csv](csv_results.zip) (1926 dòng)
- [ablation_classic/algorithm_benchmark_cost_summary.csv](csv_results.zip) (7 dòng)
- [ablation_classic/algorithm_benchmark_igd_hv_summary.csv](csv_results.zip) (7 dòng)
- [ablation_classic/algorithm_benchmark_paired_statistics.csv](csv_results.zip) (12 dòng)
- [ablation_classic/algorithm_benchmark_raw_runs.csv](csv_results.zip) (210 dòng)
- [ablation_classic/algorithm_benchmark_validation.csv](csv_results.zip) (210 dòng)
- [sensitivity_classic/sensitivity_fcr_trace.csv](csv_results.zip) (84000 dòng)
- [sensitivity_classic/sensitivity_raw_runs.csv](csv_results.zip) (420 dòng)
- [sensitivity_classic/sensitivity_statistics.csv](csv_results.zip) (28 dòng)
- [sensitivity_classic/sensitivity_summary.csv](csv_results.zip) (14 dòng)
- [sensitivity_adaptive/comparisons.csv](csv_results.zip) (81 dòng)
- [sensitivity_adaptive/paired_seed_changes.csv](csv_results.zip) (1620 dòng)
- [sensitivity_adaptive/prob_de_paired_plot_data.csv](csv_results.zip) (4 dòng)
- [sensitivity_adaptive/raw_runs.csv](csv_results.zip) (570 dòng)
- [sensitivity_adaptive/response_diagnostics.csv](csv_results.zip) (18 dòng)
- [sensitivity_adaptive/summary.csv](csv_results.zip) (27 dòng)

## Classic và adaptive trên benchmark 7 thuật toán

Hai bảng dùng chung các block đối chứng; không cộng thành các lượt chạy độc lập mới.

| Thuật toán | IGD classic | IGD adaptive | HV classic | HV adaptive |
|---|---:|---:|---:|---:|
| OADE_NSGAII | 0.0083192 | 0.00498585 | 1.04924 | 1.05122 |
| NSGA2 | 0.00719117 | 0.00719117 | 1.04718 | 1.04718 |
| RNSGA2 | 0.740552 | 0.740552 | 0.401005 | 0.401005 |
| DNSGA2 | 0.0055682 | 0.0055682 | 1.04695 | 1.04695 |
| CGDE_NSGAII | 0.00826161 | 0.00826161 | 1.03505 | 1.03505 |
| NSGAII_SDR_OLS | 0.0186481 | 0.0186481 | 1.03581 | 1.03581 |
| CE_MOEA | 0.00856088 | 0.00856088 | 1.0344 | 1.0344 |

Đây là trung bình mô tả từ benchmark seed 42–71. Để đánh giá trực tiếp classic/adaptive/no-restart trên seed 1000–1029, xem `restart_confirmation/`. Không diễn giải chênh lệch mô tả như kiểm định mới.

## Báo cáo, hình và nguồn dùng chung

- [benchmark_v2_results_report.md](../../../../docs/reports/benchmark_v2_results_report.md)
- [restart_confirmation_report.md](../../../../docs/reports/restart_confirmation_report.md)
- [ablation_results_report.md](../../../../docs/reports/ablation_results_report.md)
- [zdt_parameter_sensitivity_report.md](../../../../docs/reports/zdt_parameter_sensitivity_report.md)
- [sensitivity_analysis.md](../../../../docs/reports/sensitivity_analysis.md)
- [zdt_sensitivity.md](../../../../docs/protocols/zdt_sensitivity.md)
- [experiment_registry.md](../../../../docs/protocols/experiment_registry.md)
- [zdt_composition.json](../../../provenance/zdt_composition.json)
- [zdt_validation.json](../../../provenance/zdt_validation.json)
- [study_manifest.json](../../../experiments/zdt_sensitivity_ofat_v1/study_manifest.json)
- [Hình tổng hợp các bài toán](../../../figures/)
- [Hình độ nhạy adaptive OFAT](../../../experiments/zdt_sensitivity_ofat_v1/figures/)

Độ nhạy classic và adaptive có seed, thiết kế khác nhau; giữ riêng hai thư mục. Các hình trên là hình nhiều bài toán, không phải hình đã lọc riêng.

## Truy vết và bổ sung

`manifest.json` ghi nguồn, SHA-256 và số dòng của từng tệp. P-value/Holm được giữ theo họ kiểm định gốc, không hiệu chỉnh lại theo thư mục.
Các bảng khác số mục tiêu/kích thước vẫn giữ cột n_obj/n_var; không gộp thành một điều kiện.
Bổ sung kết quả vào nguồn theo đúng giao thức, rồi chạy `python scripts/organize_by_problem.py`. Không chỉnh trực tiếp bản tách được sinh tự động.
