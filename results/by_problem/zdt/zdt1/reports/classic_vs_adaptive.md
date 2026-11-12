# ZDT1 — Classic và adaptive

## Benchmark seed 42–71

Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.

| algorithm | IGD_classic | IGD_adaptive | HV_classic | HV_adaptive |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 0.005925213 | 0.004475332 | 0.8689611 | 0.8708662 |
| NSGA2 | 0.005174662 | 0.005174662 | 0.8680528 | 0.8680528 |
| RNSGA2 | 0.6329726 | 0.6329726 | 0.3480615 | 0.3480615 |
| DNSGA2 | 0.005632946 | 0.005632946 | 0.867066 | 0.867066 |
| CGDE_NSGAII | 0.007433421 | 0.007433421 | 0.8633624 | 0.8633624 |
| NSGAII_SDR_OLS | 0.01563308 | 0.01563308 | 0.8584207 | 0.8584207 |
| CE_MOEA | 0.006908169 | 0.006908169 | 0.8644716 | 0.8644716 |

## Xác nhận seed 1000–1029

Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.

## Báo cáo nguồn

- [Benchmark classic](benchmark_classic.md)
- [Benchmark adaptive](benchmark_adaptive.md)

[Danh mục báo cáo](README.md)
