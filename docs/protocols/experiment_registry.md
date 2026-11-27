# Experiment registry

## Current algorithm-comparison baseline

**19 November 2026:** the active comparison is now the [six-solver ZDT protocol](zdt_six_fixed_oade.md): OADE, NSGA2, DNSGA2, CGDE, GDE3 and NSDE. New run directory `results/experiments/zdt_six_fixed_oade_v1/`; 900 completed runs (899 valid) and 50 Holm endpoints: 44 favor OADE, 6 nonsignificant. See the [audited report](../reports/zdt_six_fixed_oade_report.md). CE/RNSGA2/SDR-OLS are legacy only. Component-study datasets remain separate and retained.

## Optimum-location bias check

**27 November 2026:** [protocol](bias_location_check.md) and [report](../reports/bias_location_check_report.md). OADE variants (production, random/bounce DE repair, no OBL) and NSGA-II on original and shifted ZDT, where the shift moves the optimum inside the domain with an unchanged Pareto front.

| Study | Role | Seeds | Runs | Directory |
|---|---|---|---:|---|
| Exploratory | Discovery, ZDT1/4/6, one shift | 9000–9029 | 720 | `results/experiments/bias_location_exploratory_v1/` |
| Confirmation | Pre-specified, ZDT1/2/3/4/6, three shifts | 9100–9129 | 3,000 | `results/experiments/bias_location_confirm_v1/` |

These runs do not change the stored six-solver results; they limit how those results may be generalised.

## Historical algorithm-comparison baseline

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
| Operator probability | [Probability adaptation](probability_ablation.md) |
| ZDT sensitivity | [OFAT](zdt_sensitivity.md) |
| DTLZ sensitivity | [OFAT](dtlz_sensitivity.md) |

## Budget definition

All solver objective evaluations, including RNSGA2 aspiration-point setup, OBL, local search and restart, count against the 20,000-evaluation cap. Reference-front/indicator calculations are measurement overhead. Atomic batches may leave unused budget; use each run's actual n_eval. Primary X/F and original execution settings are retained for the current evaluation.
