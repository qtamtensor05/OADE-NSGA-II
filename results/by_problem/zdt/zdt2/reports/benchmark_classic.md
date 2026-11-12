# ZDT2 — Benchmark 7 thuật toán — classic

## Phạm vi

Chỉ gồm dữ liệu `problem=zdt2` trong đợt `benchmark_classic`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **210 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('30', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

Hai benchmark classic/adaptive dùng chung sáu block đối chứng; không cộng các block dùng lại thành các lượt chạy độc lập mới.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.007733971 | 0.005315963 | 0.5337388 | 0.006239717 | 3.8437 | 19945.1 |
| NSGA2 | 30 | 30 | 0.005404928 | 0.0003062495 | 0.5340721 | 0.000611177 | 1.972879 | 20000 |
| RNSGA2 | 30 | 30 | 0.5235072 | 0.02531412 | 0.1208837 | 0.00708899 | 6.413736 | 20000 |
| DNSGA2 | 30 | 30 | 0.005881009 | 0.0003919705 | 0.532697 | 0.000974228 | 1.841043 | 19910 |
| CGDE_NSGAII | 30 | 30 | 0.006815073 | 0.0005100299 | 0.5305716 | 0.001169756 | 136.0613 | 20000 |
| NSGAII_SDR_OLS | 30 | 30 | 0.05031861 | 0.1523264 | 0.4996336 | 0.106117 | 3.475694 | 20000 |
| CE_MOEA | 30 | 30 | 0.007476844 | 0.0009803407 | 0.5296702 | 0.001905347 | 144.5108 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGA2**; HV cao nhất: **NSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | CE_MOEA | 30 | 1 | 0.2387097 | no_significant_difference |
| IGD | OADE_NSGAII | CGDE_NSGAII | 30 | 1 | 0.1956989 | no_significant_difference |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 1 | 0.002150538 | no_significant_difference |
| IGD | OADE_NSGAII | NSGA2 | 30 | 1 | -0.09677419 | no_significant_difference |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.008087814 | 0.6946237 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |
| HV | OADE_NSGAII | CE_MOEA | 30 | 0.02578391 | 0.6 | reference_better |
| HV | OADE_NSGAII | CGDE_NSGAII | 30 | 0.1466293 | 0.4537634 | no_significant_difference |
| HV | OADE_NSGAII | DNSGA2 | 30 | 0.5117952 | 0.2903226 | no_significant_difference |
| HV | OADE_NSGAII | NSGA2 | 30 | 0.7197559 | 0.1956989 | no_significant_difference |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.0001462027 | 0.8365591 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 5.587935e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (2041 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (7 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (12 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (210 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (210 dòng)

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
