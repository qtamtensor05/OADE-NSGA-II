# ZDT3 — Classic và adaptive

## Benchmark seed 42–71

Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.

| algorithm | IGD_classic | IGD_adaptive | HV_classic | HV_adaptive |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 0.008319198 | 0.004985851 | 1.049238 | 1.051221 |
| NSGA2 | 0.007191168 | 0.007191168 | 1.047182 | 1.047182 |
| RNSGA2 | 0.7405515 | 0.7405515 | 0.4010049 | 0.4010049 |
| DNSGA2 | 0.005568199 | 0.005568199 | 1.046953 | 1.046953 |
| CGDE_NSGAII | 0.008261615 | 0.008261615 | 1.035047 | 1.035047 |
| NSGAII_SDR_OLS | 0.01864812 | 0.01864812 | 1.035815 | 1.035815 |
| CE_MOEA | 0.008560882 | 0.008560882 | 1.0344 | 1.0344 |

## Xác nhận seed 1000–1029

Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.

## Báo cáo nguồn

- [Benchmark classic](benchmark_classic.md)
- [Benchmark adaptive](benchmark_adaptive.md)

[Danh mục báo cáo](README.md)
