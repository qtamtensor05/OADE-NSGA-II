# ZDT benchmark: v1 classic OADE

This report summarizes the current fixed-budget ZDT result tables, with all algorithm–problem summaries and paired comparisons.

## Scope and provenance

Five ZDT problems, seven implementations, 30 paired seeds (42–71), population 100. ZDT1–3 use D=30; ZDT4/6 use D=10. All 1,050 rows are present and valid. The 150 RNSGA2 rows have a captured execution manifest; the other 900 rows retain their archived provenance. RNSGA2 aspiration-point setup is included in the 20,000-evaluation cap and runtime. These tables combine algorithm blocks, rather than a simultaneous execution of all seven algorithms.

See [baseline identities](baselines.md), [ablation](ablation_results_report.md), [held-out restart evidence](restart_confirmation_report.md) and [reproducibility](reproducibility.md). Common uniform initial populations bypass standalone Sobol/initial OBL.

## Analysis

One stochastic run is the experimental unit. Every paired test uses 30 matched seeds. Tests are two-sided paired Wilcoxon signed-rank, with Holm correction over 30 comparisons separately for IGD and HV. The table contains all 60 configured tests, calculated from the current paired run records. Positive matched-pairs rank-biserial effect favors OADE. No detected difference is not equivalence. Mean ± sample SD below describes run dispersion, not a confidence interval for the paired effect.

## Outcome counts

OADE wins: **39**; no detected difference: **20**; OADE losses: **1**.

## All algorithm–problem summaries

| Problem | Implementation ID | IGD mean ± SD ↓ | HV mean ± SD ↑ | Mean seconds | Mean n_eval |
|---|---|---:|---:|---:|---:|
| zdt1 | OADE_NSGAII | 0.005925 ± 0.002536 | 0.868961 ± 0.003342 | 1.360 | 19975.5 |
| zdt1 | NSGA2 | 0.005175 ± 0.000298 | 0.868053 ± 0.000417 | 0.929 | 20000.0 |
| zdt1 | RNSGA2 | 0.632973 ± 0.087624 | 0.348062 ± 0.093888 | 2.758 | 20000.0 |
| zdt1 | DNSGA2 | 0.005633 ± 0.000423 | 0.867066 ± 0.000685 | 0.853 | 19910.0 |
| zdt1 | CGDE_NSGAII | 0.007433 ± 0.000527 | 0.863362 ± 0.000969 | 39.562 | 20000.0 |
| zdt1 | NSGAII_SDR_OLS | 0.015633 ± 0.019704 | 0.858421 ± 0.014846 | 1.050 | 20000.0 |
| zdt1 | CE_MOEA | 0.006908 ± 0.000874 | 0.864472 ± 0.001779 | 38.817 | 20000.0 |
| zdt2 | OADE_NSGAII | 0.007734 ± 0.005316 | 0.533739 ± 0.006240 | 3.844 | 19945.1 |
| zdt2 | NSGA2 | 0.005405 ± 0.000306 | 0.534072 ± 0.000611 | 1.973 | 20000.0 |
| zdt2 | RNSGA2 | 0.523507 ± 0.025314 | 0.120884 ± 0.007089 | 6.414 | 20000.0 |
| zdt2 | DNSGA2 | 0.005881 ± 0.000392 | 0.532697 ± 0.000974 | 1.841 | 19910.0 |
| zdt2 | CGDE_NSGAII | 0.006815 ± 0.000510 | 0.530572 ± 0.001170 | 136.061 | 20000.0 |
| zdt2 | NSGAII_SDR_OLS | 0.050319 ± 0.152326 | 0.499634 ± 0.106117 | 3.476 | 20000.0 |
| zdt2 | CE_MOEA | 0.007477 ± 0.000980 | 0.529670 ± 0.001905 | 144.511 | 20000.0 |
| zdt3 | OADE_NSGAII | 0.008319 ± 0.005096 | 1.049238 ± 0.003634 | 3.100 | 19943.1 |
| zdt3 | NSGA2 | 0.007191 ± 0.010231 | 1.047182 ± 0.006699 | 1.687 | 20000.0 |
| zdt3 | RNSGA2 | 0.740552 ± 0.057316 | 0.401005 ± 0.049497 | 2.383 | 20000.0 |
| zdt3 | DNSGA2 | 0.005568 ± 0.000291 | 1.046953 ± 0.000680 | 1.629 | 19910.0 |
| zdt3 | CGDE_NSGAII | 0.008262 ± 0.000984 | 1.035047 ± 0.003604 | 108.590 | 20000.0 |
| zdt3 | NSGAII_SDR_OLS | 0.018648 ± 0.002970 | 1.035815 ± 0.004358 | 2.531 | 20000.0 |
| zdt3 | CE_MOEA | 0.008561 ± 0.001533 | 1.034400 ± 0.005116 | 100.297 | 20000.0 |
| zdt4 | OADE_NSGAII | 0.006977 ± 0.003323 | 0.864878 ± 0.005621 | 4.675 | 19960.6 |
| zdt4 | NSGA2 | 0.009953 ± 0.005080 | 0.859362 ± 0.007910 | 2.208 | 20000.0 |
| zdt4 | RNSGA2 | 0.620575 ± 0.165318 | 0.351077 ± 0.155278 | 2.097 | 20000.0 |
| zdt4 | DNSGA2 | 0.019973 ± 0.027370 | 0.846750 ± 0.036867 | 2.105 | 19910.0 |
| zdt4 | CGDE_NSGAII | 12.171576 ± 2.800419 | 0.000000 ± 0.000000 | 138.416 | 20000.0 |
| zdt4 | NSGAII_SDR_OLS | 10.891407 ± 6.777696 | 0.000000 ± 0.000000 | 2.369 | 20000.0 |
| zdt4 | CE_MOEA | 0.357214 ± 0.234331 | 0.409725 ± 0.227870 | 129.200 | 20000.0 |
| zdt6 | OADE_NSGAII | 0.005286 ± 0.003371 | 0.436557 ± 0.003740 | 3.584 | 19940.4 |
| zdt6 | NSGA2 | 0.016368 ± 0.002011 | 0.417891 ± 0.002872 | 2.055 | 20000.0 |
| zdt6 | RNSGA2 | 0.185764 ± 0.092787 | 0.267636 ± 0.068590 | 2.207 | 20000.0 |
| zdt6 | DNSGA2 | 0.022588 ± 0.002794 | 0.408917 ± 0.003997 | 2.020 | 19910.0 |
| zdt6 | CGDE_NSGAII | 0.003823 ± 0.000223 | 0.439057 ± 0.000199 | 103.072 | 20000.0 |
| zdt6 | NSGAII_SDR_OLS | 0.139446 ± 0.082748 | 0.282923 ± 0.058962 | 2.121 | 20000.0 |
| zdt6 | CE_MOEA | 0.004957 ± 0.000336 | 0.437794 ± 0.000360 | 101.561 | 20000.0 |

## All paired comparisons

| Problem | Metric | Comparator ID | n | Holm p | Rank-biserial r | Result for OADE |
|---|---|---|---:|---:|---:|---|
| zdt1 | IGD | CE_MOEA | 30 | 0.15661909 | +0.518280 | no_significant_difference |
| zdt1 | IGD | CGDE_NSGAII | 30 | 0.018481566 | +0.651613 | reference_better |
| zdt1 | IGD | DNSGA2 | 30 | 1 | +0.208602 | no_significant_difference |
| zdt1 | IGD | NSGA2 | 30 | 1 | -0.006452 | no_significant_difference |
| zdt1 | IGD | NSGAII_SDR_OLS | 30 | 2.1457672e-05 | +0.901075 | reference_better |
| zdt1 | IGD | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt2 | IGD | CE_MOEA | 30 | 1 | +0.238710 | no_significant_difference |
| zdt2 | IGD | CGDE_NSGAII | 30 | 1 | +0.195699 | no_significant_difference |
| zdt2 | IGD | DNSGA2 | 30 | 1 | +0.002151 | no_significant_difference |
| zdt2 | IGD | NSGA2 | 30 | 1 | -0.096774 | no_significant_difference |
| zdt2 | IGD | NSGAII_SDR_OLS | 30 | 0.0080878139 | +0.694624 | reference_better |
| zdt2 | IGD | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt3 | IGD | CE_MOEA | 30 | 1 | +0.225806 | no_significant_difference |
| zdt3 | IGD | CGDE_NSGAII | 30 | 1 | +0.247312 | no_significant_difference |
| zdt3 | IGD | DNSGA2 | 30 | 1 | -0.298925 | no_significant_difference |
| zdt3 | IGD | NSGA2 | 30 | 0.4226026 | -0.432258 | no_significant_difference |
| zdt3 | IGD | NSGAII_SDR_OLS | 30 | 8.8475645e-07 | +0.965591 | reference_better |
| zdt3 | IGD | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | IGD | CE_MOEA | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | IGD | CGDE_NSGAII | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | IGD | DNSGA2 | 30 | 0.002335703 | +0.750538 | reference_better |
| zdt4 | IGD | NSGA2 | 30 | 0.092953511 | +0.556989 | no_significant_difference |
| zdt4 | IGD | NSGAII_SDR_OLS | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | IGD | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | IGD | CE_MOEA | 30 | 0.91949627 | +0.354839 | no_significant_difference |
| zdt6 | IGD | CGDE_NSGAII | 30 | 0.1639589 | -0.509677 | no_significant_difference |
| zdt6 | IGD | DNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | IGD | NSGA2 | 30 | 7.4505806e-08 | +0.995699 | reference_better |
| zdt6 | IGD | NSGAII_SDR_OLS | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | IGD | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt1 | HV | CE_MOEA | 30 | 7.7655539e-05 | +0.858065 | reference_better |
| zdt1 | HV | CGDE_NSGAII | 30 | 1.9557774e-06 | +0.948387 | reference_better |
| zdt1 | HV | DNSGA2 | 30 | 0.028222559 | +0.587097 | reference_better |
| zdt1 | HV | NSGA2 | 30 | 0.14662929 | +0.449462 | no_significant_difference |
| zdt1 | HV | NSGAII_SDR_OLS | 30 | 5.3979456e-06 | +0.926882 | reference_better |
| zdt1 | HV | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt2 | HV | CE_MOEA | 30 | 0.025783911 | +0.600000 | reference_better |
| zdt2 | HV | CGDE_NSGAII | 30 | 0.14662929 | +0.453763 | no_significant_difference |
| zdt2 | HV | DNSGA2 | 30 | 0.51179519 | +0.290323 | no_significant_difference |
| zdt2 | HV | NSGA2 | 30 | 0.71975585 | +0.195699 | no_significant_difference |
| zdt2 | HV | NSGAII_SDR_OLS | 30 | 0.00014620274 | +0.836559 | reference_better |
| zdt2 | HV | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt3 | HV | CE_MOEA | 30 | 6.3329935e-08 | +0.995699 | reference_better |
| zdt3 | HV | CGDE_NSGAII | 30 | 6.3329935e-08 | +0.995699 | reference_better |
| zdt3 | HV | DNSGA2 | 30 | 0.0041839667 | +0.703226 | reference_better |
| zdt3 | HV | NSGA2 | 30 | 0.063589565 | +0.526882 | no_significant_difference |
| zdt3 | HV | NSGAII_SDR_OLS | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt3 | HV | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | HV | CE_MOEA | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | HV | CGDE_NSGAII | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | HV | DNSGA2 | 30 | 0.00097421557 | +0.767742 | reference_better |
| zdt4 | HV | NSGA2 | 30 | 0.019689979 | +0.621505 | reference_better |
| zdt4 | HV | NSGAII_SDR_OLS | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt4 | HV | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | HV | CE_MOEA | 30 | 0.71975585 | +0.079570 | no_significant_difference |
| zdt6 | HV | CGDE_NSGAII | 30 | 5.5879354e-08 | -1.000000 | comparison_better |
| zdt6 | HV | DNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | HV | NSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | HV | NSGAII_SDR_OLS | 30 | 5.5879354e-08 | +1.000000 | reference_better |
| zdt6 | HV | RNSGA2 | 30 | 5.5879354e-08 | +1.000000 | reference_better |

## Interpretation boundary

These comparisons concern the configured implementations and seeds. Retained algorithms' historical package/source versions remain unverified. Runtime is implementation-, environment- and contention-dependent. These comparisons neither establish Sobol benefit nor isolate adaptive-restart causality. Paired-effect confidence intervals and failure-aware robustness analyses remain unavailable. DTLZ/WFG have a separate accounting convention documented in the experiment registry.

## Source files

- `results/algorithm_benchmark/algorithm_benchmark_raw_runs.csv`
- `results/algorithm_benchmark/algorithm_benchmark_validation.csv`
- `results/algorithm_benchmark/algorithm_benchmark_convergence.csv`
- `results/algorithm_benchmark/algorithm_benchmark_igd_hv_summary.csv`
- `results/algorithm_benchmark/algorithm_benchmark_paired_statistics.csv`
- `results/algorithm_benchmark/algorithm_benchmark_cost_summary.csv`

Execution-time provenance for the RNSGA2 block: `results/provenance/rnsga2_zdt_execution.json`. Dataset composition and checksums: `results/provenance/zdt_composition.json`. Validation record: `results/provenance/zdt_validation.json`.
