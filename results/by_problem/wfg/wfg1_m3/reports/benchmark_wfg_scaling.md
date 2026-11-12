# WFG1_M3 — Benchmark WFG mở rộng số mục tiêu

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg1_m3` trong đợt `benchmark_wfg_scaling`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **150 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '3', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 1.417953 | 0.0103613 | 16.40281 | 0.1706685 | 13.86958 | 19951.13 |
| NSGA2 | 30 | 30 | 1.392464 | 0.03098437 | 13.69409 | 1.24201 | 8.264426 | 20000 |
| RNSGA2 | 30 | 30 | 2.116165 | 0.05430919 | 0.1053519 | 0.2704382 | 5.416359 | 20000 |
| DNSGA2 | 30 | 30 | 1.706894 | 0.04535446 | 6.160764 | 0.9944947 | 6.223565 | 19966.33 |
| NSGAII_SDR_OLS | 30 | 30 | 1.388143 | 0.02075836 | 16.59645 | 0.2841247 | 8.772732 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **NSGAII_SDR_OLS**; HV cao nhất: **NSGAII_SDR_OLS**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 0.002660653 | -0.7075269 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1.564622e-06 | -0.9483871 | comparison_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.005828e-07 | 0.9913978 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.01212109 | -0.6258065 | comparison_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1445 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (8 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (150 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (150 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
