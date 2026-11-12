# Research documentation

Start with [the integrated research manuscript](manuscript/manuscript.md) for the central question, implemented method, findings and limitations. It is a bounded research draft, not a submission-ready claim of novelty or journal compliance.

| Document | Role |
|---|---|
| [Current project structure (Vietnamese)](governance/project_structure.md) | Implemented namespace, naming rules, tmp cleanup and experiment execution workflow |
| [Flat algorithm ownership migration](governance/flat_algorithm_migration_20261112.md) | One directory per algorithm, shared functions and research tooling boundaries |
| [Project structure proposal (Vietnamese)](project_structure_proposal.md) | Repository audit, naming rules, tmp lifecycle and staged restructuring plan |
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
| [Historical v1 report](reports/research_results_report.md) | Archived classic-restart findings, not the current overview |

Current numeric source data are in results/. ZDT/DTLZ/WFG algorithm-block provenance, checksums and validation are in [results/provenance](../results/provenance). Figure QA is documented in [figure_qa.md](../results/figures/figure_qa.md).
