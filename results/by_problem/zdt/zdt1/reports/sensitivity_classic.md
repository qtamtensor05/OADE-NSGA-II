# ZDT1 — Độ nhạy tham số classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt1` trong đợt `sensitivity_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **420 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số classic

| study | parameter_label | runs | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | restart_count_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.01403413 | 0.007768118 | 0.8578672 | 0.01151934 | 0.7508758 | 6.833333 |
| pop_size | 100 | 30 | 0.00726116 | 0.004420169 | 0.8674642 | 0.005503612 | 1.603477 | 7.4 |
| pop_size | 200 | 30 | 0.003346264 | 0.001522152 | 0.8725131 | 0.001905417 | 3.383917 | 7.666667 |
| stagnation_patience | 5 | 30 | 0.01029658 | 0.004444231 | 0.8624002 | 0.00708938 | 1.60942 | 31.93333 |
| stagnation_patience | 10 | 30 | 0.008308896 | 0.004033886 | 0.8658702 | 0.005310799 | 1.565602 | 15.43333 |
| stagnation_patience | 15 | 30 | 0.006539527 | 0.003725964 | 0.8682742 | 0.004650423 | 1.662775 | 10 |
| stagnation_patience | 20 | 30 | 0.00726116 | 0.004420169 | 0.8674642 | 0.005503612 | 1.5757 | 7.4 |
| stagnation_patience | 25 | 30 | 0.006516709 | 0.003187883 | 0.8684364 | 0.003973861 | 1.559077 | 5.966667 |
| stagnation_patience | 30 | 30 | 0.006296727 | 0.00348421 | 0.8685517 | 0.004283182 | 1.601554 | 4.966667 |
| stagnation_patience | 40 | 30 | 0.006415549 | 0.00398827 | 0.8682247 | 0.005267774 | 1.606363 | 3.4 |
| f_cr_init | fixed_baseline | 30 | 0.00726116 | 0.004420169 | 0.8674642 | 0.005503612 | 1.501901 | 7.4 |
| f_cr_init | low_init | 30 | 0.007586489 | 0.004472907 | 0.8669084 | 0.005920087 | 1.554777 | 6 |
| f_cr_init | high_init | 30 | 0.006773043 | 0.003543614 | 0.8679191 | 0.004823894 | 1.55594 | 7.666667 |
| f_cr_init | random_uniform | 30 | 0.006370176 | 0.003530776 | 0.8684987 | 0.004865078 | 1.533126 | 7.3 |

## Kiểm định độ nhạy đã lưu

| study | metric | test | baseline_label | comparison_label | p_value | p_adjusted_holm | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | IGD | friedman | 100 | all | 1.096932e-10 |  | parameter_effect_detected |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 0.001038169 | 0.001038169 | baseline_better |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 1.991168e-06 | 3.982335e-06 | comparison_better |
| pop_size | HV | friedman | 100 | all | 1.480704e-10 |  | parameter_effect_detected |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 0.0009517744 | 0.0009517744 | baseline_better |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 2.762303e-06 | 5.524606e-06 | comparison_better |
| stagnation_patience | IGD | friedman | 20 | all | 1.190005e-05 |  | parameter_effect_detected |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.00814298 | 0.04885788 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.1579477 | 0.6317907 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.7456547 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.7921591 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.5561133 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.01852948 | 0.0926474 | no_significant_difference |
| stagnation_patience | HV | friedman | 20 | all | 5.974778e-07 |  | parameter_effect_detected |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.0008718204 | 0.005230922 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.05492163 | 0.2196865 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.8552717 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.6850471 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.6408254 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.02622899 | 0.131145 | no_significant_difference |
| f_cr_init | IGD | friedman | fixed_baseline | all | 0.914476 |  | no_parameter_effect_detected |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.7921591 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.6263463 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.6554384 | 1 | no_significant_difference |
| f_cr_init | HV | friedman | fixed_baseline | all | 0.849467 |  | no_parameter_effect_detected |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.8078304 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.5425279 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.730342 | 1 | no_significant_difference |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [sensitivity_fcr_trace.csv](../csv_results.zip) (84000 dòng)
- [sensitivity_raw_runs.csv](../csv_results.zip) (420 dòng)
- [sensitivity_statistics.csv](../csv_results.zip) (28 dòng)
- [sensitivity_summary.csv](../csv_results.zip) (14 dòng)

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
