# ZDT2 — Classic và adaptive

## Benchmark seed 42–71

Trung bình hai phiên bản trên cùng bộ đối chứng; sáu block đối chứng được dùng chung. Đây là so sánh mô tả, không phải kiểm định mới.

| algorithm | IGD_classic | IGD_adaptive | HV_classic | HV_adaptive |
| --- | --- | --- | --- | --- |
| OADE_NSGAII | 0.007733971 | 0.004756218 | 0.5337388 | 0.5376738 |
| NSGA2 | 0.005404928 | 0.005404928 | 0.5340721 | 0.5340721 |
| RNSGA2 | 0.5235072 | 0.5235072 | 0.1208837 | 0.1208837 |
| DNSGA2 | 0.005881009 | 0.005881009 | 0.532697 | 0.532697 |
| CGDE_NSGAII | 0.006815073 | 0.006815073 | 0.5305716 | 0.5305716 |
| NSGAII_SDR_OLS | 0.05031861 | 0.05031861 | 0.4996336 | 0.4996336 |
| CE_MOEA | 0.007476844 | 0.007476844 | 0.5296702 | 0.5296702 |

## Xác nhận seed 1000–1029

Xem [báo cáo restart riêng](restart_confirmation.md) để đọc chất lượng, chi phí và kiểm định đã lưu giữa classic, adaptive và no-restart. Không trộn seed của đợt này với benchmark.

## Báo cáo nguồn

- [Benchmark classic](benchmark_classic.md)
- [Benchmark adaptive](benchmark_adaptive.md)

[Danh mục báo cáo](README.md)
