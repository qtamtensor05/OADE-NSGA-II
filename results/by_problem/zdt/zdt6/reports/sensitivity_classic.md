# ZDT6 — Độ nhạy tham số classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt6` trong đợt `sensitivity_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **420 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '', '')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số classic

| study | parameter_label | runs | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | restart_count_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.0113225 | 0.007347544 | 0.4296837 | 0.008038868 | 0.6284284 | 3.033333 |
| pop_size | 100 | 30 | 0.005688635 | 0.004016719 | 0.4361534 | 0.004349807 | 1.579276 | 3.666667 |
| pop_size | 200 | 30 | 0.00351342 | 0.001916788 | 0.4388189 | 0.002139836 | 3.475657 | 4.033333 |
| stagnation_patience | 5 | 30 | 0.009441083 | 0.004169659 | 0.4315991 | 0.004946028 | 1.697683 | 23.1 |
| stagnation_patience | 10 | 30 | 0.006262911 | 0.003586499 | 0.4355373 | 0.003678642 | 1.532428 | 9.7 |
| stagnation_patience | 15 | 30 | 0.005729633 | 0.003353105 | 0.436052 | 0.00377792 | 1.539182 | 5.733333 |
| stagnation_patience | 20 | 30 | 0.005688635 | 0.004016719 | 0.4361534 | 0.004349807 | 1.541312 | 3.666667 |
| stagnation_patience | 25 | 30 | 0.005334632 | 0.003315207 | 0.4365367 | 0.003816111 | 1.554774 | 2.6 |
| stagnation_patience | 30 | 30 | 0.004580446 | 0.001590475 | 0.4374287 | 0.001682804 | 1.513959 | 2.066667 |
| stagnation_patience | 40 | 30 | 0.004667189 | 0.003292029 | 0.437277 | 0.00345323 | 1.470059 | 1.2 |
| f_cr_init | fixed_baseline | 30 | 0.005688635 | 0.004016719 | 0.4361534 | 0.004349807 | 1.556745 | 3.666667 |
| f_cr_init | low_init | 30 | 0.005714692 | 0.003821862 | 0.4360555 | 0.004075874 | 1.551732 | 2.133333 |
| f_cr_init | high_init | 30 | 0.00537745 | 0.002708697 | 0.4366818 | 0.002878625 | 1.574002 | 7.266667 |
| f_cr_init | random_uniform | 30 | 0.005331776 | 0.003938444 | 0.4365586 | 0.004463758 | 1.464747 | 4.5 |

## Kiểm định độ nhạy đã lưu

| study | metric | test | baseline_label | comparison_label | p_value | p_adjusted_holm | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | IGD | friedman | 100 | all | 1.473068e-08 |  | parameter_effect_detected |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 0.0003127549 | 0.0006255098 | baseline_better |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 0.007111456 | 0.007111456 | comparison_better |
| pop_size | HV | friedman | 100 | all | 1.473068e-08 |  | parameter_effect_detected |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 0.0002316367 | 0.0004632734 | baseline_better |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 0.002187775 | 0.002187775 | comparison_better |
| stagnation_patience | IGD | friedman | 20 | all | 2.856653e-11 |  | parameter_effect_detected |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.001457477 | 0.008744862 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.07672122 | 0.3836061 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.3707406 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.9192965 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.5698576 | 1 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.1980758 | 0.7923032 | no_significant_difference |
| stagnation_patience | HV | friedman | 20 | all | 6.157787e-12 |  | parameter_effect_detected |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.0004601069 | 0.002760641 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.08406548 | 0.4203274 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.2534361 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 1 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.5158484 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.3598779 | 1 | no_significant_difference |
| f_cr_init | IGD | friedman | fixed_baseline | all | 0.4862321 |  | no_parameter_effect_detected |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.7000329 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.4399668 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.5978078 | 1 | no_significant_difference |
| f_cr_init | HV | friedman | fixed_baseline | all | 0.9775893 |  | no_parameter_effect_detected |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.8235769 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 1 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.9032265 | 1 | no_significant_difference |

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
