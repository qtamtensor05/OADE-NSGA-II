# Follow-up experiments: decisions after the audit

## Claim retained now

The current claim concerns the performance and failure boundaries of the implemented OADE configurations on selected continuous unconstrained benchmarks. It does not assert a new adaptive-restart mechanism, Sobol initialization benefit or superiority to the state of the art. Correcting names, formulas and documentation does not require rerunning archived benchmarks.

## Prioritized evidence plan

| Priority | Question and decision | Required evidence and prespecified boundary |
|---|---|---|
| 1 | Are the intended published baselines actually represented? | Keep local CGDE and adapted CE explicitly labeled. Before a published-method superiority claim, select the intended paper, map equations/config and verify a faithful implementation on diagnostic examples. Rerun only affected comparisons under the same cap and with new provenance. No unsupported CGDE citation is supplied. |
| 2 | Does adaptive restart add value over simply disabling classic restart? | Run Adaptive vs No Restart with telemetry on fresh seeds and selected failure-prone problems. Record trigger checks, activations, diversity measures and restart evaluations. The held-out ZDT evidence alone does not establish this mechanism. Keep paired final IGD/HV and failure frequency; define multiplicity family before running. |
| 3 | How uncertain are the paired gains? | Add paired effect CIs from existing run-level data with an explicit resampling unit, interval method, bootstrap seed and coverage policy. Use matched seeds, preserve zero HV differences, and retain all failed-run diagnostics. This is a new analysis, not a change to stored p-values. |
| 4 | Do exclusions change the conclusion? | Separate structural failures from quality collapse. Define the failure-aware estimand before recomputing; show valid-output quality and failure rates alongside a sensitivity analysis. Do not choose penalties after seeing which improves OADE's score. |
| 5 | Does a success-based DE probability improve the algorithm? | Treat it as a separately named new version. Compare the current generated-share EMA, fixed probability and a specified success-based rule. Do not relabel existing v2 outputs after changing the rule. |
| 6 | Does Sobol/initial OBL help? | Separate initialization from periodic injection in a factorial or focused ablation; charge every objective evaluation. A common warm start and a method-specific initialization answer different questions and must be reported as separate protocols. |

## Execution decision

No full benchmark rerun is required for this documentation/provenance correction. The code paths receive small smoke checks; historical observations remain intact. Do not launch all six proposals as a single expensive batch. Baseline identity and the intended contribution determine which new scientific experiment is necessary. The safe fresh-run and manifest infrastructure is available for that next stage.

Suggested next scientific focus is adaptive vs no restart with telemetry, if the author intends adaptive restart as the primary contribution. Otherwise prioritize verified task-aligned baselines and uncertainty for the bounded empirical claim. Neither choice implies journal acceptance or novelty has already been established.
