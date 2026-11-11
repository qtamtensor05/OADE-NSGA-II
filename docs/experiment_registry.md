# Experiment registry

This registry describes the current result sets. Stored rows are not necessarily independently executed new runs: baseline blocks are shared across tables and some WFG configurations overlap.

| Results directory | Reproduction configuration | Role and provenance |
|---|---|---|
| algorithm_benchmark | config/algorithm_benchmark_classic.yaml | ZDT, classic OADE, 1,050 records; 150 RNSGA2 records have execution-time provenance; 900 retain archived provenance. |
| algorithm_benchmark_v2 | config/algorithm_benchmark_v2.yaml | ZDT, adaptive OADE, 1,050 records; shares the same RNSGA2 block and the other five comparator blocks with the classic table. |
| ablation | config/ablation.yaml | Classic Full OADE and six removals/basic variants; 1,050 records, seeds 42–71; periodic OBL ablation under uniform warm start. |
| restart_confirmation | config/restart_confirmation.yaml | Classic Full, No Restart, Adaptive; 450 records, seeds 1000–1029; trigger telemetry was not saved. |
| dtlz_benchmark | config/dtlz1_4_benchmark.yaml | DTLZ1–4, M=2/3/5; 2,520 records, 18 invalid, 26–30 valid matched pairs. |
| wfg_m2_7algo_benchmark | config/wfg_m2_7algo_benchmark.yaml | Four WFG functions, seven implementations, M=2; 840 records. |
| wfg_compact_benchmark | config/wfg_compact_benchmark.yaml | Four WFG functions, five implementations, M=2/3/5; 1,800 records; overlapping M=2 settings/seeds are not independent replication. |
| sensitivity | config/sensitivity.yaml | Classic restart, seeds 42–71; exploratory parameter sweeps, not direct v2 sensitivity evidence. |

Each core configuration schedules 30 runs. Cross-suite win counts summarize separately adjusted Holm families. The default OADE YAML specifies adaptive restart; use the explicit classic reproduction configuration for classic OADE.

## Budget definition

Current ZDT RNSGA2 records include aspiration-point setup within the 20,000-evaluation cap and runtime. Their recorded count is 20,000 for all 150 runs. Other solvers may finish below the cap when another requested batch would exceed it.

Archived DTLZ/WFG RNSGA2 counters cover search evaluations and exclude population-sized aspiration-point setup. Those suites have not been rerun under total-cost accounting and should not be presented as verified total-evaluation-budget comparisons for RNSGA2. Indicator/reference-Pareto-front calculations are measurement overhead rather than solver search evaluations.

## Source data and traceability

- [Artifact inventory](../results/research_inventory.json): observed CSV checksums, completeness, failures and outcome counts.
- [ZDT composition](../results/provenance/zdt_composition.json): current checksums and algorithm-block provenance.
- [RNSGA2 ZDT execution manifest](../results/provenance/rnsga2_zdt_execution.json): protocol, source hashes, environment and primary block hashes captured during execution. Filtering RNSGA2 from either ZDT table reconstructs these primary block hashes.
- [ZDT validation](../results/provenance/zdt_validation.json): paired-seed checks, independent Wilcoxon/Holm recalculation, summary/cost consistency and PDF QA.
- [Dataset lineage](../results/provenance/zdt_dataset_lineage.json): machine-readable traceability separate from the main research narrative.

Source/package versions for archived blocks without execution manifests remain unknown. Do not assign the current environment to them. Older results/benchmark and results/three_algorithms use legacy protocols and are excluded from the main fixed-budget claim.
