# Experiment registry

These are archived batches, not prospective execution manifests. Machine/package versions and exact historical source hashes were not captured. The [file inventory](../results/research_inventory.json) records present-day hashes and completeness without filling that gap.

| Results directory | Protocol/config route | Role and known version boundary |
|---|---|---|
| algorithm_benchmark | config/algorithm_benchmark.yaml | Historical v1 classic restart, 1,050 records. The referenced OADE algorithm YAML now specifies adaptive restart; the current config does not reconstruct v1. For a new classic run, use the explicit classic reproduction config below. |
| algorithm_benchmark_v2 | config/algorithm_benchmark_v2.yaml | 150 new OADE runs + 900 copied v1 comparator records; 1,050 total, seeds 42–71 |
| ablation | config/ablation.yaml | Classic Full OADE and six removals/basic variants; 1,050 records, seeds 42–71; periodic OBL ablation under uniform warm start |
| restart_confirmation | config/restart_confirmation.yaml | Classic Full, No Restart, Adaptive; 450 records, held-out seeds 1000–1029; trigger telemetry not historically saved |
| dtlz_benchmark | config/dtlz1_4_benchmark.yaml | DTLZ1–4, M=2/3/5; 2,520 records, 18 invalid, 26–30 matched valid pairs |
| wfg_m2_7algo_benchmark | config/wfg_m2_7algo_benchmark.yaml | Four WFG functions, seven implementations, M=2; 840 records |
| wfg_compact_benchmark | config/wfg_compact_benchmark.yaml | Four WFG functions, five implementations, M=2/3/5; 1,800 records; overlaps settings/seeds with the M=2 study and is not independent replication of that setting |
| sensitivity | config/sensitivity.yaml | Classic restart, seeds 42–71; parameter sweeps, not direct v2 sensitivity evidence |

All core batches use a 20,000-evaluation cap and 30 scheduled runs per configuration. Cross-suite win counts combine separate Holm families and are descriptive. Totals of stored rows do not equal counts of independently executed new runs.

For prospective classic-v1 reproduction, use config/algorithm_benchmark_classic.yaml, which points to an explicit named classic algorithm config. This preserves the historical OADE_NSGAII ID while making the restart mode unambiguous. It reconstructs documented settings, not unknown historical package/source versions.

Older results/benchmark and results/three_algorithms belong to legacy routes. They are not part of the primary fixed-budget claim. Do not pool their p-values with the current paired/Holm protocol.

## Prospective budget-accounting correction

The archived runner derived RNSGA2 aspiration points by evaluating the initial population outside the budget proxy and before its runtime timer. Its recorded search counter therefore omitted one population-sized setup evaluation. New runs include that work in the cap and runtime; they can differ from archived RNSGA2 results even with identical seeds. Manifests mark this as budget-accounting v2. No archived metric or recorded evaluation count has been rewritten. Other reference PF/indicator computations are benchmark measurement overhead, not solver objective-search evaluations.
