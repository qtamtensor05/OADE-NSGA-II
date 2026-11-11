# Integrated ZDT and DTLZ1–4 results

The current tables cover 17 problem configurations and 3,570 stored records. Algorithms are paired by seed, with 30 scheduled runs per configuration. Valid-output quality is conditional on the reported validation rules; failures remain in raw evidence.

| Dataset | Records | Invalid | Comparisons | OADE W / ND / L |
|---|---:|---:|---:|---|
| algorithm_benchmark_v2 | 1050 | 0 | 60 | 58 / 1 / 1 |
| dtlz_benchmark | 2520 | 18 | 144 | 91 / 40 / 13 |

Combined descriptive W / ND / L: **149 / 41 / 14** over 204 comparisons. Holm families are separate: m=30 per ZDT metric and m=72 per DTLZ metric. This combined count is not one 204-test family and does not establish universal superiority.

## Detailed evidence

- [ZDT v2 tables and tests](benchmark_v2_results_report.md).
- [DTLZ tables, failures, valid sample sizes and tests](dtlz_results_report.md).
- [Method and attribution boundaries](manuscript.md).

## Figures

![Integrated landscape](../results/figures/integrated_7algo_landscape.png)

Panel a: IGD rank-biserial effects, positive favoring OADE. Panel b: descriptive comparison counts. Panel c: mean quality rank across 34 endpoints (IGD medians, HV means) against DTLZ4 runtime only; this runtime proxy is not a full-suite speed frontier. Source CSVs are in results/figures/.

![DTLZ scaling](../results/figures/dtlz1_4_scaling_diagnosis.png)

Markers show valid-run medians; bars show the 25th–75th percentiles, not effect confidence intervals. The DTLZ2 panel normalizes to the NSGA-II median. The DTLZ4 panel reports observed HV, not a new structural-collapse classification. See [QA](../results/figures/figure_qa.md).
