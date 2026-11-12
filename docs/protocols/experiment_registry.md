# Experiment registry

This registry describes the current result sets. Stored rows are not necessarily independently executed new runs: baseline blocks are shared across tables and some WFG configurations overlap.

| Results directory | Reproduction configuration | Role and provenance |
|---|---|---|
| algorithm_benchmark | config/suites/algorithm_benchmark_classic.yaml | ZDT, classic OADE, 1,050 records; 150 RNSGA2 records have execution-time provenance; 900 retain archived provenance. |
| algorithm_benchmark_v2 | config/suites/algorithm_benchmark_v2.yaml | ZDT, adaptive OADE, 1,050 records; shares the same RNSGA2 block and the other five comparator blocks with the classic table. |
| ablation | config/studies/ablation.yaml | Classic Full OADE and six removals/basic variants; 1,050 records, seeds 42–71; periodic OBL ablation under uniform warm start. |
| restart_confirmation | config/studies/restart_confirmation.yaml | Classic Full, No Restart, Adaptive; 450 records, seeds 1000–1029; trigger telemetry was not saved. |
| dtlz_benchmark | config/suites/dtlz1_4_benchmark.yaml | 2520 records; 18 invalid; 26–30 valid matched pairs. RNSGA2: 360 records with captured execution provenance; other blocks archived. |
| wfg_m2_7algo_benchmark | config/suites/wfg_m2_7algo_benchmark.yaml | 840 records; 0 invalid; 30–30 valid matched pairs. RNSGA2: 120 records with captured execution provenance; other blocks archived. |
| wfg_compact_benchmark | config/suites/wfg_compact_benchmark.yaml | 1800 records; 0 invalid; 30–30 valid matched pairs. RNSGA2: 360 records with captured execution provenance; other blocks archived. |
| sensitivity | config/studies/sensitivity.yaml | Classic restart, seeds 42–71; exploratory parameter sweeps, not direct v2 sensitivity evidence. |

Each core configuration schedules 30 runs. Cross-suite win counts summarize separately adjusted Holm families. The default OADE YAML specifies adaptive restart; use the explicit classic reproduction configuration for classic OADE.

## Budget definition

RNSGA2 aspiration-point setup is included within the 20,000-evaluation cap and runtime for ZDT, DTLZ, WFG. Other solvers can finish below the cap when another batch would exceed it. Reference-front/indicator calculations are measurement overhead rather than solver objective-search evaluations.

## Source data and traceability

- [Artifact inventory](../../results/research_inventory.json): observed CSV checksums, completeness, failures and outcome counts.
- [ZDT composition](../../results/provenance/zdt_composition.json): current checksums and algorithm-block provenance.
- [RNSGA2 ZDT execution manifest](../../results/provenance/rnsga2_zdt_execution.json): protocol, source hashes, environment and primary block hashes captured during execution. Filtering RNSGA2 from either ZDT table reconstructs these primary block hashes.
- [ZDT validation](../../results/provenance/zdt_validation.json): paired-seed checks, independent Wilcoxon/Holm recalculation, summary/cost consistency and PDF QA.
- [Dataset lineage](../../results/provenance/zdt_dataset_lineage.json): machine-readable traceability separate from the main research narrative.

Source/package versions for archived blocks without execution manifests remain unknown. Do not assign the current environment to them. Older results/benchmark and results/three_algorithms use legacy protocols and are excluded from the main fixed-budget claim.

Multiobjective algorithm-block provenance and dataset checksums: [multiobjective composition](../../results/provenance/multiobjective_composition.json). The same 120-run RNSGA2 M=2 block is shared by both WFG tables.

Multiobjective execution manifests: [DTLZ](../../results/provenance/rnsga2_dtlz_execution.json) and [WFG](../../results/provenance/rnsga2_wfg_execution.json). See [current validation](../../results/provenance/multiobjective_validation.json) for the independent p-value/Holm/effect-size checks and PDF checksums.
