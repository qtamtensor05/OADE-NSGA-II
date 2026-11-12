# WFG1_M2 — Benchmark WFG mở rộng số mục tiêu

## Phạm vi

Chỉ gồm dữ liệu `problem=wfg1_m2` trong đợt `benchmark_wfg_scaling`. Các số hiển thị được làm tròn; CSV giữ nguyên độ chính xác.

CSV nguồn được đóng gói trong ZIP ở các liên kết cuối báo cáo. Giải nén cạnh ZIP hoặc chạy `python scripts/csv_archives.py restore` từ gốc dự án để mở CSV theo đường dẫn cũ.

Có **150 dòng raw**, **30 seed** (42–71), **0 dòng không hợp lệ** theo cột valid đã lưu.

Điều kiện `(n_var, n_obj, evaluation_budget)` trong raw: `('24', '2', '20000')`. Trường trống là thông tin không được lưu ở nguồn.

## Chất lượng và chi phí

| algorithm | runs_total | runs_valid | IGD_mean | IGD_std | HV_mean | HV_std | runtime_mean | n_eval_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OADE_NSGAII | 30 | 30 | 1.02608 | 0.0107426 | 1.77197 | 0.03043873 | 12.53017 | 19943.73 |
| NSGA2 | 30 | 30 | 1.202149 | 0.07474058 | 0.9030075 | 0.1902277 | 6.9754 | 20000 |
| RNSGA2 | 30 | 30 | 1.695321 | 0.07039025 | 0 | 0 | 6.399092 | 20000 |
| DNSGA2 | 30 | 30 | 1.566661 | 0.04268617 | 0.009819265 | 0.02969914 | 5.78754 | 19967.67 |
| NSGAII_SDR_OLS | 30 | 30 | 1.146026 | 0.01817038 | 1.420078 | 0.04224277 | 8.26199 | 20000 |

Theo trung bình mô tả, IGD thấp nhất: **OADE_NSGAII**; HV cao nhất: **OADE_NSGAII**. Xếp theo trung bình không thay thế kiểm định.

## Kiểm định ghép cặp đã lưu

| metric | reference_algorithm | comparison_algorithm | n_pairs | p_adjusted_holm | rank_biserial_effect | result |
| --- | --- | --- | --- | --- | --- | --- |
| IGD | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| IGD | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | DNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | NSGA2 | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | NSGAII_SDR_OLS | 30 | 8.940697e-08 | 1 | reference_better |
| HV | OADE_NSGAII | RNSGA2 | 30 | 8.940697e-08 | 1 | reference_better |

## Giới hạn diễn giải

P-value/Holm và chiều effect size giữ theo đợt gốc, không tính lại họ hiệu chỉnh riêng cho bài toán. Đọc result theo reference_algorithm/comparison_algorithm. Không phát hiện khác biệt không đồng nghĩa tương đương. Bảng thay đổi phần trăm là mô tả, không phải kiểm định mới.

## Dữ liệu và truy vết

- [algorithm_benchmark_convergence.csv](../csv_results.zip) (1449 dòng)
- [algorithm_benchmark_cost_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_igd_hv_summary.csv](../csv_results.zip) (5 dòng)
- [algorithm_benchmark_paired_statistics.csv](../csv_results.zip) (8 dòng)
- [algorithm_benchmark_raw_runs.csv](../csv_results.zip) (150 dòng)
- [algorithm_benchmark_validation.csv](../csv_results.zip) (150 dòng)

SHA-256 và đường dẫn nguồn: [manifest](../manifest.json).

Giao thức và báo cáo toàn đợt:

- [wfg_compact_report.md](../../../../../docs/reports/wfg_compact_report.md)

[Danh mục báo cáo của bài toán](README.md)
