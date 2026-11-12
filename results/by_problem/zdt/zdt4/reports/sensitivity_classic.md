# ZDT4 — Độ nhạy tham số classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt4` trong đợt `sensitivity_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **420 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('10', '', '')`. Trường trống là thông tin không được lưu ở nguồn.

Giữ riêng thiết kế và seed của đợt này; không ghép classic với adaptive. OFAT không đo tương tác giữa tham số. Baseline dùng lại giữa các bảng không phải các lượt thực thi mới.

## Đáp ứng tham số classic

| study | parameter_label | runs | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | restart_count_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | 50 | 30 | 0.1303189 | 0.1760525 | 0.6893946 | 0.2201856 | 0.758297 | 0.2333333 |
| pop_size | 100 | 30 | 0.006088708 | 0.001719517 | 0.8664509 | 0.003087756 | 1.761637 | 0.3 |
| pop_size | 200 | 30 | 0.002484718 | 0.0003474172 | 0.8727016 | 0.0004549528 | 4.177491 | 0.3333333 |
| stagnation_patience | 5 | 30 | 0.01168646 | 0.004845173 | 0.8589845 | 0.00731475 | 1.829453 | 12.2 |
| stagnation_patience | 10 | 30 | 0.008932419 | 0.005444538 | 0.8627961 | 0.007949434 | 1.743853 | 1.766667 |
| stagnation_patience | 15 | 30 | 0.006681987 | 0.002707396 | 0.8656383 | 0.004233917 | 1.740981 | 0.5333333 |
| stagnation_patience | 20 | 30 | 0.006088708 | 0.001719517 | 0.8664509 | 0.003087756 | 1.701066 | 0.3 |
| stagnation_patience | 25 | 30 | 0.006316451 | 0.001884643 | 0.8661917 | 0.003223054 | 1.766162 | 0.2333333 |
| stagnation_patience | 30 | 30 | 0.00634831 | 0.001871584 | 0.8661382 | 0.003174487 | 1.76483 | 0.1333333 |
| stagnation_patience | 40 | 30 | 0.006053984 | 0.001652998 | 0.8665399 | 0.003128263 | 1.748155 | 0.03333333 |
| f_cr_init | fixed_baseline | 30 | 0.006088708 | 0.001719517 | 0.8664509 | 0.003087756 | 1.709481 | 0.3 |
| f_cr_init | low_init | 30 | 0.0190501 | 0.03768096 | 0.8467458 | 0.05857919 | 1.719023 | 0.3666667 |
| f_cr_init | high_init | 30 | 0.07115034 | 0.1861342 | 0.7824875 | 0.1971674 | 1.782074 | 0.03333333 |
| f_cr_init | random_uniform | 30 | 0.02116295 | 0.05837365 | 0.8433725 | 0.08933131 | 1.670345 | 0.1 |

## Kiểm định độ nhạy đã lưu

| study | metric | test | baseline_label | comparison_label | p_value | p_adjusted_holm | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pop_size | IGD | friedman | 100 | all | 9.357623e-14 |  | parameter_effect_detected |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 1.862645e-09 | 3.72529e-09 | baseline_better |
| pop_size | IGD | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 1.862645e-09 | 3.72529e-09 | comparison_better |
| pop_size | HV | friedman | 100 | all | 9.357623e-14 |  | parameter_effect_detected |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 50 | 1.862645e-09 | 3.72529e-09 | baseline_better |
| pop_size | HV | wilcoxon_signed_rank_vs_baseline | 100 | 200 | 1.862645e-09 | 3.72529e-09 | comparison_better |
| stagnation_patience | IGD | friedman | 20 | all | 5.759877e-09 |  | parameter_effect_detected |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 6.910414e-07 | 4.146248e-06 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.002234578 | 0.01117289 | baseline_better |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.213223 | 0.6918197 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.2488639 | 0.6918197 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.1729549 | 0.6918197 | no_significant_difference |
| stagnation_patience | IGD | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.3454475 | 0.6918197 | no_significant_difference |
| stagnation_patience | HV | friedman | 20 | all | 6.007345e-08 |  | parameter_effect_detected |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 5 | 4.42192e-06 | 2.653152e-05 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 10 | 0.005110261 | 0.0255513 | baseline_better |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 15 | 0.2477462 | 0.9909848 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 25 | 0.6001795 | 1 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 30 | 0.2488639 | 0.9909848 | no_significant_difference |
| stagnation_patience | HV | wilcoxon_signed_rank_vs_baseline | 20 | 40 | 0.7531524 | 1 | no_significant_difference |
| f_cr_init | IGD | friedman | fixed_baseline | all | 5.142924e-06 |  | parameter_effect_detected |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.8393927 | 0.8393927 | no_significant_difference |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 1.192093e-06 | 3.576279e-06 | baseline_better |
| f_cr_init | IGD | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.3930502 | 0.7861004 | no_significant_difference |
| f_cr_init | HV | friedman | fixed_baseline | all | 1.091551e-05 |  | parameter_effect_detected |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | low_init | 0.7000329 | 0.954213 | no_significant_difference |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | high_init | 4.712492e-07 | 1.413748e-06 | baseline_better |
| f_cr_init | HV | wilcoxon_signed_rank_vs_baseline | fixed_baseline | random_uniform | 0.4771065 | 0.954213 | no_significant_difference |

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
