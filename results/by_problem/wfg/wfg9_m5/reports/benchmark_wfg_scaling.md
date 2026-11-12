# WFG9_M5 — Benchmark WFG mở rộng số mục tiêu

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg9_m5` trong đợt `benchmark_wfg_scaling`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **150 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '5', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 1.96313 | 0.09934742 | 983.5274 | 133.1168 | 17.52769 | 19955.87 |
| NSGA2 | 30 | 30 | 1.732541 | 0.06846882 | 1304.332 | 96.15085 | 10.31562 | 20000 |
| RNSGA2 | 30 | 30 | 3.92028 | 0.1102886 | 410.3209 | 11.67902 | 9.990555 | 20000 |
| DNSGA2 | 30 | 30 | 1.71491 | 0.07142945 | 1318.301 | 107.5795 | 10.35558 | 19910 |
| NSGAII_SDR_OLS | 30 | 30 | 1.971272 | 0.1091136 | 1031.392 | 130.3662 | 10.44133 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **DNSGA2**; HV cao nhất: **DNSGA2**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 6.984919e-07 | -0.9655914 | comparison_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 1 | 0.07096774 | no_significant_difference |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | -1 | comparison_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 1.955777e-06 | -0.9483871 | comparison_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 0.4805079 | -0.3505376 | no_significant_difference |
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
