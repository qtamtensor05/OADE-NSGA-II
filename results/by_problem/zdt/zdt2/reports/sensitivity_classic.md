# ZDT2 — Độ nhạy tham số classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt2` trong đợt `sensitivity_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **420 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '', '')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số classic

| study | parameter_label | runs | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | restart_count_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.0133611 | 0.007916264 | 0.5271767 | 0.008310476 | 0.6581804 | 4.766667 |
| pop_size | 100 | 30 | 0.005925597 | 0.002222301 | 0.5359536 | 0.002752362 | 1.575045 | 5.866667 |
| pop_size | 200 | 30 | 0.004304678 | 0.00279022 | 0.5378601 | 0.003376248 | 3.434177 | 6.933333 |
| stagnation_patience | 5 | 30 | 0.01157531 | 0.003725201 | 0.5288406 | 0.004316841 | 1.729069 | 25.86667 |
| stagnation_patience | 10 | 30 | 0.008920596 | 0.005471487 | 0.5319901 | 0.006786918 | 1.584337 | 12.23333 |
| stagnation_patience | 15 | 30 | 0.007635667 | 0.004761906 | 0.5338619 | 0.006389783 | 1.593312 | 7.966667 |
| stagnation_patience | 20 | 30 | 0.005925597 | 0.002222301 | 0.5359536 | 0.002752362 | 1.602619 | 5.866667 |
| stagnation_patience | 25 | 30 | 0.005947732 | 0.003108027 | 0.5355639 | 0.004484373 | 1.578789 | 4.633333 |
| stagnation_patience | 30 | 30 | 0.006088951 | 0.003303101 | 0.5357076 | 0.004324575 | 1.580016 | 3.733333 |
| stagnation_patience | 40 | 30 | 0.005319489 | 0.002158187 | 0.5367712 | 0.002983773 | 1.486055 | 2.6 |
| f_cr_init | fixed_baseline | 30 | 0.005925597 | 0.002222301 | 0.5359536 | 0.002752362 | 1.55719 | 5.866667 |
| f_cr_init | low_init | 30 | 0.008412059 | 0.005661189 | 0.5327949 | 0.007302899 | 1.615982 | 4.133333 |
| f_cr_init | high_init | 30 | 0.007625369 | 0.006476636 | 0.5338691 | 0.008001461 | 1.613974 | 6.8 |
| f_cr_init | random_uniform | 30 | 0.006760897 | 0.004463109 | 0.5348516 | 0.005629243 | 1.531503 | 6.333333 |

## Kiểm định độ nhạy đã lưu

| study | metric | test | baseline_label | comparison_label | p_value | p_adjusted_holm | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | IGD | friedman | 100 | all | 1.473068e-08 |  | parameter_effect_detected |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 1.862645e-08 | 3.72529e-08 | baseline_better |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 0.00538278 | 0.00538278 | comparison_better |
| pop_size | HV | friedman | 100 | all | 2.698018e-10 |  | parameter_effect_detected |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 1.862645e-09 | 3.72529e-09 | baseline_better |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 0.006194992 | 0.006194992 | comparison_better |
| stagnation_patience | IGD | friedman | 20 | all | 7.505197e-09 |  | parameter_effect_detected |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 5.718321e-07 | 3.430992e-06 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.005012613 | 0.02506306 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.2449464 | 0.7348393 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.5291052 | 0.9290901 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.464545 | 0.9290901 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.00538278 | 0.02506306 | comparison_better |
| stagnation_patience | HV | friedman | 20 | all | 1.220858e-09 |  | parameter_effect_detected |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 2.551824e-07 | 1.531094e-06 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.003744433 | 0.01872216 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.2710056 | 0.8130169 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.8552717 | 0.8552717 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.4161299 | 0.8322598 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.02209885 | 0.08839542 | no_significant_difference |
| f_cr_init | IGD | friedman | fixed_baseline | all | 0.2933296 |  | no_parameter_effect_detected |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.08032736 | 0.2409821 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.7921591 | 1 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.5425279 | 1 | no_significant_difference |
| f_cr_init | HV | friedman | fixed_baseline | all | 0.4041248 |  | no_parameter_effect_detected |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.1141767 | 0.34253 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 0.9353987 | 1 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.6120056 | 1 | no_significant_difference |

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
