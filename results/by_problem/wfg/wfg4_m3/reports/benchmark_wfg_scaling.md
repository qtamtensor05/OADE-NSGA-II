# WFG4_M3 — Benchmark WFG mở rộng số mục tiêu

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg4_m3` trong đợt `benchmark_wfg_scaling`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **150 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '3', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 0.3537828 | 0.01422368 | 16.25886 | 0.5361859 | 12.65581 | 19963.93 |
| NSGA2 | 30 | 30 | 0.2803927 | 0.01239513 | 19.0866 | 0.372234 | 6.917278 | 20000 |
| RNSGA2 | 30 | 30 | 1.704287 | 0.1169167 | 7.093832 | 0.3727968 | 7.483404 | 20000 |
| DNSGA2 | 30 | 30 | 0.2847024 | 0.01427073 | 18.95045 | 0.3856759 | 6.71488 | 19910 |
| NSGAII_SDR_OLS | 30 | 30 | 0.5981101 | 0.05885561 | 12.51005 | 1.365066 | 8.245382 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGA2**; HV cao nhất: **NSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1441 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (8 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (150 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (150 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
