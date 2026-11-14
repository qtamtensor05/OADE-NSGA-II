# Probability adaptation ablation

Paired seed-controlled measurements.
Runs: 300; invalid: 0.

Only probability_update_mode differs: generated_share, success_rate.
Success: nondominated in the complete evaluated parent/offspring pool before deduplication. Each trial counts once. OBL/initial/restart individuals are not DE/SBX trials but can dominate trials.
rDE=sDE/nDE; rSBX=sSBX/nSBX; q=rDE/(rDE+rSBX); p <- clip(0.9*p+0.1*q,0.2,0.8). Hold p if either operator has zero trials or both rates are zero. Fixed holds initial p. F/CR adaptation is unchanged.
Initialization is common uniform, bypassing native Sobol/OBL. This controlled ablation does not evaluate complete native-initialized OADE. Restart and all other settings are shared across variants.
comparisons.csv: all 1 pairs per problem/metric, paired valid seeds, median paired delta a-b and two-sided Wilcoxon (wilcox zeros, normal approximation; all zero p=1), Holm across pairs per problem/metric, alpha=0.05. Excluded pairs are counted. IGD lower / HV higher is better. No detected difference is not equivalence.
raw_runs.csv contains per-run quality, runtime, validity and final pDE; probability_trace.csv contains every completed generation, trial/success counts, target and before/after pDE. Legacy/fixed success counts are blank, not measured as zero.
Primary JSON contains final X/F and reference snapshot hashes for recomputation. All objective calls count against the cap; atomic batches may leave unused evaluations. Read n_eval. Convergence has actual observation budgets; no interpolation.

| Problem | Mode | Valid/runs | Median IGD | Median HV | Median final pDE |
|---|---|---:|---:|---:|---:|
| zdt1 | generated_share | 30/30 | 0.0045106 | 0.870891 | 0.496188 |
| zdt1 | success_rate | 30/30 | 0.00447689 | 0.870918 | 0.460963 |
| zdt2 | generated_share | 30/30 | 0.00466417 | 0.537607 | 0.49893 |
| zdt2 | success_rate | 30/30 | 0.00472555 | 0.537736 | 0.463851 |
| zdt3 | generated_share | 30/30 | 0.00509946 | 1.05126 | 0.510026 |
| zdt3 | success_rate | 30/30 | 0.00506424 | 1.05128 | 0.42191 |
| zdt4 | generated_share | 30/30 | 0.00628789 | 0.865553 | 0.497329 |
| zdt4 | success_rate | 30/30 | 0.00554021 | 0.867503 | 0.527628 |
| zdt6 | generated_share | 30/30 | 0.00378964 | 0.4382 | 0.492073 |
| zdt6 | success_rate | 30/30 | 0.00381081 | 0.438064 | 0.45074 |
