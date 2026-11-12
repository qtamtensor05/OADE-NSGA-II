# ZDT4 — Classic và adaptive

## Benchmark seed 42–71

Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.

| algorithm | IGD_classic | IGD_adaptive | HV_classic | HV_adaptive |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 0.006977176 | 0.00683066 | 0.8648781 | 0.8650507 |
| NSGA2 | 0.009952722 | 0.009952722 | 0.8593619 | 0.8593619 |
| RNSGA2 | 0.6205746 | 0.6205746 | 0.3510772 | 0.3510772 |
| DNSGA2 | 0.01997309 | 0.01997309 | 0.8467496 | 0.8467496 |
| CGDE_NSGAII | 12.17158 | 12.17158 | 0 | 0 |
| NSGAII_SDR_OLS | 10.89141 | 10.89141 | 0 | 0 |
| CE_MOEA | 0.3572136 | 0.3572136 | 0.409725 | 0.409725 |

## Xác nhận seed 1000–1029

Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.

## Báo cáo nguồn

- [Benchmark classic](benchmark_classic.md)
- [Benchmark adaptive](benchmark_adaptive.md)

[Danh mục báo cáo](README.md)
