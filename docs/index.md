# Research documentation

CSV downloads: [verified ZIP bundles and restore instructions](../results/CSV_DOWNLOADS.md). Reports and figures remain directly readable. Restore the CSVs before running data-dependent analyses on a fresh clone.

Current research priority: **ZDT**. Open the [per-problem research folders](../results/by_problem/README.md) for ZDT1/2/3/4/6: seven-algorithm classic/adaptive benchmarks, restart confirmation, ablation and parameter sensitivity. Each folder contains filtered CSVs, source checksums and report/figure links. DTLZ and WFG use the same layout for incremental extension.

Standalone reports are now split by problem inside each folder's `reports/` directory: [ZDT1](../results/by_problem/zdt/zdt1/reports/README.md), [ZDT2](../results/by_problem/zdt/zdt2/reports/README.md), [ZDT3](../results/by_problem/zdt/zdt3/reports/README.md), [ZDT4](../results/by_problem/zdt/zdt4/reports/README.md), [ZDT6](../results/by_problem/zdt/zdt6/reports/README.md). These contain the problem's numeric tables and interpretation limits, rather than only links to combined reports. DTLZ and WFG folders also contain their own reports.

Start with [the integrated research manuscript](manuscript/manuscript.md) for the central question, implemented method, findings and limitations. It is a bounded research draft, not a submission-ready claim of novelty or journal compliance.

| Document | Role |
|---|---|
| [Baseline registry](protocols/baselines.md) | Canonical names, code ownership, adaptations and citations |
| [Reproducibility](protocols/reproducibility.md) | Fresh execution, safe resume, environment and figure sources |
| [Experiment registry](protocols/experiment_registry.md) | Historical batches and provenance boundaries |
| [Follow-up experiment plan](protocols/followup_experiments.md) | Decisions on additional evidence needed for each claim |
| [ZDT v2 report](reports/benchmark_v2_results_report.md) | Detailed v2 ZDT statistics |
| [DTLZ detailed results](reports/dtlz_results_report.md) | Full current summaries and paired tests |
| [ZDT + DTLZ report](reports/dtlz1_4_integrated_report.md) | Detailed multiobjective results, valid-pair counts and exclusions |
| [WFG report](reports/wfg_compact_report.md) | Bi-objective comparison and compact scaling |
| [Ablation](reports/ablation_results_report.md) | Classic-configuration component removals |
| [Restart confirmation](reports/restart_confirmation_report.md) | Held-out ZDT seeds; adaptive mechanism remains unconfirmed |
| [Sensitivity](reports/sensitivity_analysis.md) | Classic-restart parameter sweeps; exploratory multiplicity |
| [ZDT parameter sensitivity protocol (Vietnamese)](protocols/zdt_sensitivity.md) | One-parameter-at-a-time level lists, direct IGD/HV responses, variability and curves on ZDT |
| [DTLZ parameter sensitivity protocol (Vietnamese)](protocols/dtlz_sensitivity.md) | DTLZ1–4 at 2/3/5 objectives, explicit parameter lists, safe resume and per-objective figures |
| [ZDT v2 parameter sensitivity results (Vietnamese)](reports/zdt_parameter_sensitivity_report.md) | Completed 2,850-run OFAT study: per-problem effects, restart diagnostics, figures and configuration rationale |
| [Historical v1 report](reports/research_results_report.md) | Archived classic-restart findings, not the current overview |

Current numeric source data are in results/. ZDT/DTLZ/WFG algorithm-block provenance, checksums and validation are in [results/provenance](../results/provenance). Figure QA is documented in [figure_qa.md](../results/figures/figure_qa.md).
