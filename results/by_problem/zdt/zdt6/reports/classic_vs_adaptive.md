# ZDT6 — Classic và adaptive

## Benchmark seed 42–71

Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.

| algorithm | IGD_classic | IGD_adaptive | HV_classic | HV_adaptive |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 0.005285892 | 0.003843999 | 0.4365567 | 0.4381765 |
| NSGA2 | 0.01636813 | 0.01636813 | 0.4178915 | 0.4178915 |
| RNSGA2 | 0.1857638 | 0.1857638 | 0.2676365 | 0.2676365 |
| DNSGA2 | 0.0225884 | 0.0225884 | 0.4089167 | 0.4089167 |
| CGDE_NSGAII | 0.003823051 | 0.003823051 | 0.4390565 | 0.4390565 |
| NSGAII_SDR_OLS | 0.1394459 | 0.1394459 | 0.2829226 | 0.2829226 |
| CE_MOEA | 0.004956833 | 0.004956833 | 0.4377938 | 0.4377938 |

## Xác nhận seed 1000–1029

Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.

## Báo cáo nguồn

- [Benchmark classic](benchmark_classic.md)
- [Benchmark adaptive](benchmark_adaptive.md)

[Danh mục báo cáo](README.md)
