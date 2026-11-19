# Experiment registry

## Current algorithm-comparison baseline

As of 15 November 2026, the starting point is `results/experiments/zdt_seven_fixed_oade_v2/`: corrected baselines and fixed OADE, 1,050 newly executed runs, 1,049 valid and one collapsed CGDE ZDT4 front. No previous baseline blocks are reused.

- [Configuration](../../config/suites/zdt_seven_fixed_oade.yaml)
- [Audit report](../reports/zdt_seven_fixed_oade_v2_report.md)
- [Manifest](../../results/experiments/zdt_seven_fixed_oade_v2/study_manifest.json)
- [Execution protocol](zdt_seven_fixed_oade.md)

Previous benchmark result directories and reports have been removed. DTLZ/WFG have not been reevaluated with the corrected implementations; no current-version result is claimed for them.

## Separate OADE component studies

Earlier component-study results have been removed. A subsequent 480-run mechanism study on ZDT4/ZDT6 is retained in `results/experiments/oade_mechanism_zdt46/`. Its [audited report](../reports/mechanism_zdt46_report.md) documents 28 Holm-corrected comparisons and provenance limitations. Other component pipelines below require new evidence before effect claims.

| Study | Protocol |
|---|---|
| Current-solver mechanism parameter levels | [OFAT with initial/held levels](mechanism_sensitivity.md) — 2,100 valid runs; [audited report](../reports/mechanism_sensitivity_report.md), 124 Holm-corrected endpoints |
| Restart | [Classic, adaptive and no restart](restart_comparison.md) |
| Periodic diversity | [Injection on/off](diversity_injection.md) |
| Initialization | [Uniform and Sobol–OBL](initialization_comparison.md) |
| Operator probability | [Probability adaptation](probability_ablation.md) |
| ZDT sensitivity | [OFAT](zdt_sensitivity.md) |
| DTLZ sensitivity | [OFAT](dtlz_sensitivity.md) |

## Budget definition

All solver objective evaluations, including RNSGA2 aspiration-point setup, OBL, local search and restart, count against the 20,000-evaluation cap. Reference-front/indicator calculations are measurement overhead. Atomic batches may leave unused budget; use each run's actual n_eval. Primary X/F and original execution settings are retained for the current evaluation.
