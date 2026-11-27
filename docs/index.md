# Research documentation

## Current results

The active comparison is the new six-solver ZDT suite (OADE, NSGA2, DNSGA2, CGDE, GDE3, NSDE); 900 runs are complete, 899 valid. Global Holm (50 endpoints): 44 favor OADE and 6 are nonsignificant. Previous seven-solver ZDT v2 results are historical, not results of the new suite. The OADE component studies remain separate. DTLZ/WFG have not been reevaluated with the active set.

- [Audited six-solver results and conclusions](reports/zdt_six_fixed_oade_report.md)
- [Optimum-location bias check: 3,720 runs on original and shifted ZDT](reports/bias_location_check_report.md) — OADE's ZDT1/2/3 advantage over NSGA-II reverses when the optimum is moved off the bound; the ZDT4 OBL benefit comes mainly from the optimum at the domain centre; ZDT6 holds
- [Current comparison tables](../README.md)
- [Active six-solver protocol, configuration and run commands](protocols/zdt_six_fixed_oade.md)
- [Audited ZDT v2 report](reports/zdt_seven_fixed_oade_v2_report.md)
- [OADE final solutions on true ZDT fronts: best-IGD seeds](reports/oade_zdt_pareto_fronts.md)
- [Audited mechanism study: 480 runs on ZDT4/ZDT6](reports/mechanism_zdt46_report.md)
- [Audited parameter-level conclusions: 2,100 runs, 124 endpoints](reports/mechanism_sensitivity_report.md)
- [Parameter-level figures: paired changes and all-seed distributions](reports/mechanism_sensitivity_figures.md)
- [Complete parameter-level comparison and summary tables](reports/mechanism_sensitivity_tables.md)
- [Execution protocol](protocols/zdt_seven_fixed_oade.md)
- [Baseline identities and source papers](protocols/baselines.md)
- [Reconstruction assumptions](protocols/baseline_paper_corrections.md)
- [Experiment registry](protocols/experiment_registry.md)
- [Reproduction](protocols/reproducibility.md)

## Component-study protocols

- [Parameter-level sensitivity of current OADE mechanisms](protocols/mechanism_sensitivity.md)

Earlier component-study results have been removed. New 480-run mechanism and 2,100-run parameter-level studies on ZDT4/ZDT6 are analysed in the reports above. The other links below describe pipelines and do not establish retained result evidence.

- [Restart](protocols/restart_comparison.md)
- [Periodic diversity injection](protocols/diversity_injection.md)
- [Probability adaptation](protocols/probability_ablation.md)
- [ZDT sensitivity](protocols/zdt_sensitivity.md)
- [DTLZ sensitivity](protocols/dtlz_sensitivity.md)
