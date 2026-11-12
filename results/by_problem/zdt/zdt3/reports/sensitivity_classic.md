# ZDT3 — Độ nhạy tham số classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt3` trong đợt `sensitivity_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **420 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số classic

| study | parameter_label | runs | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | restart_count_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.01632879 | 0.01013093 | 1.043308 | 0.009395393 | 0.667522 | 5.733333 |
| pop_size | 100 | 30 | 0.008418885 | 0.004601899 | 1.049099 | 0.00322619 | 1.561818 | 6.7 |
| pop_size | 200 | 30 | 0.003322444 | 0.001957673 | 1.052259 | 0.001399345 | 3.402228 | 7.033333 |
| stagnation_patience | 5 | 30 | 0.01273004 | 0.004926694 | 1.045568 | 0.003996761 | 1.688306 | 30.1 |
| stagnation_patience | 10 | 30 | 0.01030994 | 0.005145336 | 1.047727 | 0.003802009 | 1.63771 | 14.3 |
| stagnation_patience | 15 | 30 | 0.007414473 | 0.003271361 | 1.049879 | 0.002079436 | 1.606195 | 9.066667 |
| stagnation_patience | 20 | 30 | 0.008418885 | 0.004601899 | 1.049099 | 0.00322619 | 1.58804 | 6.7 |
| stagnation_patience | 25 | 30 | 0.007684734 | 0.004553532 | 1.04967 | 0.002803022 | 1.544733 | 5.166667 |
| stagnation_patience | 30 | 30 | 0.00654063 | 0.003469089 | 1.050275 | 0.002474155 | 1.507118 | 4.133333 |
| stagnation_patience | 40 | 30 | 0.006474569 | 0.003860326 | 1.050226 | 0.003183442 | 1.504953 | 2.966667 |
| f_cr_init | fixed_baseline | 30 | 0.008418885 | 0.004601899 | 1.049099 | 0.00322619 | 1.541853 | 6.7 |
| f_cr_init | low_init | 30 | 0.008782618 | 0.005166609 | 1.048853 | 0.00390703 | 1.571923 | 5.133333 |
| f_cr_init | high_init | 30 | 0.008019422 | 0.004977701 | 1.049392 | 0.003677857 | 1.606919 | 7 |
| f_cr_init | random_uniform | 30 | 0.006861653 | 0.002672492 | 1.050199 | 0.001901728 | 1.499349 | 6.433333 |

## Kiểm định độ nhạy đã lưu

| study | metric | test | baseline_label | comparison_label | p_value | p_adjusted_holm | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | IGD | friedman | 100 | all | 9.00417e-12 |  | parameter_effect_detected |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 5.592592e-05 | 5.592592e-05 | baseline_better |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 9.313226e-09 | 1.862645e-08 | comparison_better |
| pop_size | HV | friedman | 100 | all | 2.066489e-10 |  | parameter_effect_detected |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 0.000152871 | 0.000152871 | baseline_better |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 3.72529e-09 | 7.450581e-09 | comparison_better |
| stagnation_patience | IGD | friedman | 20 | all | 3.650419e-08 |  | parameter_effect_detected |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.0002091266 | 0.00125476 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.1003974 | 0.3011921 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.2449464 | 0.4898929 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.4399668 | 0.4898929 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.02774144 | 0.1109658 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.01546 | 0.07730002 | no_significant_difference |
| stagnation_patience | HV | friedman | 20 | all | 3.707291e-09 |  | parameter_effect_detected |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 0.000152871 | 0.0009172261 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.04490721 | 0.182175 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.1839691 | 0.3679382 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.4898461 | 0.4898461 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.06666471 | 0.1999941 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.036435 | 0.182175 | no_significant_difference |
| f_cr_init | IGD | friedman | fixed_baseline | all | 0.4716875 |  | no_parameter_effect_detected |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.6701806 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.7456547 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.1190766 | 0.3572297 | no_significant_difference |
| f_cr_init | HV | friedman | fixed_baseline | all | 0.4436368 |  | no_parameter_effect_detected |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.7921591 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.5291052 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.140283 | 0.4208491 | no_significant_difference |

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
