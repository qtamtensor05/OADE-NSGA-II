# WFG4_M2 — Benchmark WFG mở rộng số mục tiêu

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg4_m2` trong đợt `benchmark_wfg_scaling`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **150 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.03322243 | 0.003508986 | 2.145999 | 0.01682578 | 10.24079 | 19958.3 |
| NSGA2 | 30 | 30 | 0.02635144 | 0.00398152 | 2.200659 | 0.01336407 | 5.468285 | 20000 |
| RNSGA2 | 30 | 30 | 0.7761592 | 0.08765851 | 1.318446 | 0.03634877 | 5.63939 | 20000 |
| DNSGA2 | 30 | 30 | 0.027004 | 0.00451905 | 2.193684 | 0.01603379 | 5.360852 | 19910 |
| NSGAII_SDR_OLS | 30 | 30 | 0.2535845 | 0.04897362 | 1.254482 | 0.1510167 | 6.295853 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGA2**; HV cao nhất: **NSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 9.158626e-06 | -0.9096774 | comparison_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 3.979728e-05 | -0.8666667 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.005828e-07 | -0.9913978 | comparison_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1440 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (8 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (150 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (150 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
