# Bias check results

Runs: 720; invalid: 0; max |F re-eval error|: 0.0e+00; max n_eval: 20000

## Median IGD (Q1-Q3) / median HV

| Problem | Variant | OADE | OADE_bounce | OADE_noOBL | NSGA2 |
|---|---|---:|---:|---:|---:|
| zdt1 | original | 4.434e-03 (4.16e-03-4.59e-03) / 0.8709 | 4.473e-03 (4.35e-03-4.61e-03) / 0.8709 | 4.442e-03 (4.30e-03-4.58e-03) / 0.8710 | 5.150e-03 (5.03e-03-5.33e-03) / 0.8682 |
| zdt1 | shifted | 1.205e-02 (1.18e-02-1.30e-02) / 0.8551 | 1.289e-02 (1.26e-02-1.32e-02) / 0.8535 | 1.203e-02 (1.17e-02-1.26e-02) / 0.8550 | 7.619e-03 (7.20e-03-8.10e-03) / 0.8629 |
| zdt6 | original | 3.920e-03 (3.74e-03-3.99e-03) / 0.4381 | 4.354e-03 (4.22e-03-4.49e-03) / 0.4367 | 3.855e-03 (3.72e-03-3.98e-03) / 0.4380 | 1.647e-02 (1.54e-02-1.73e-02) / 0.4178 |
| zdt6 | shifted | 1.002e-01 (9.34e-02-1.05e-01) / 0.3069 | 1.059e-01 (9.55e-02-1.14e-01) / 0.2996 | 9.591e-02 (8.61e-02-1.02e-01) / 0.3105 | 7.302e-01 (6.62e-01-7.78e-01) / 0.0000 |
| zdt4 | original | 5.924e-03 (5.03e-03-1.06e-02) / 0.8661 | 1.124e-01 (1.69e-02-2.42e-01) / 0.6954 | 4.278e-01 (2.22e-01-6.42e-01) / 0.2895 | 8.939e-03 (7.70e-03-1.68e-02) / 0.8606 |
| zdt4 | shifted | 2.600e-01 (1.27e-01-5.15e-01) / 0.4941 | 7.430e-01 (4.05e-01-1.64e+00) / 0.0646 | 4.016e-01 (2.65e-01-5.95e-01) / 0.3234 | 8.133e-03 (6.24e-03-9.32e-03) / 0.8618 |

## Paired Wilcoxon, global Holm over 36 endpoints (diff = OADE - other)

| Contrast | Problem | Variant | Metric | median diff | OADE wins/30 | p Holm | verdict |
|---|---|---|---|---:|---:|---:|---|
| OADE vs OADE_bounce | zdt1 | original | IGD | -1.028e-04 | 18 | 1 | NS |
| OADE vs OADE_bounce | zdt1 | original | HV | -1.303e-05 | 15 | 1 | NS |
| OADE vs OADE_bounce | zdt1 | shifted | IGD | -7.836e-04 | 21 | 0.0228 | OADE better |
| OADE vs OADE_bounce | zdt1 | shifted | HV | +1.248e-03 | 23 | 0.00126 | OADE better |
| OADE vs OADE_bounce | zdt6 | original | IGD | -4.598e-04 | 28 | 2.14e-07 | OADE better |
| OADE vs OADE_bounce | zdt6 | original | HV | +1.443e-03 | 30 | 6.71e-08 | OADE better |
| OADE vs OADE_bounce | zdt6 | shifted | IGD | -4.493e-03 | 19 | 1 | NS |
| OADE vs OADE_bounce | zdt6 | shifted | HV | +4.888e-03 | 18 | 1 | NS |
| OADE vs OADE_bounce | zdt4 | original | IGD | -9.497e-02 | 26 | 0.00126 | OADE better |
| OADE vs OADE_bounce | zdt4 | original | HV | +1.502e-01 | 27 | 0.000671 | OADE better |
| OADE vs OADE_bounce | zdt4 | shifted | IGD | -4.271e-01 | 26 | 0.00275 | OADE better |
| OADE vs OADE_bounce | zdt4 | shifted | HV | +2.555e-01 | 26 | 0.00117 | OADE better |
| OADE vs OADE_noOBL | zdt1 | original | IGD | -9.564e-05 | 17 | 1 | NS |
| OADE vs OADE_noOBL | zdt1 | original | HV | -6.773e-05 | 11 | 1 | NS |
| OADE vs OADE_noOBL | zdt1 | shifted | IGD | +1.406e-04 | 13 | 1 | NS |
| OADE vs OADE_noOBL | zdt1 | shifted | HV | -2.989e-04 | 12 | 1 | NS |
| OADE vs OADE_noOBL | zdt6 | original | IGD | +6.152e-05 | 14 | 1 | NS |
| OADE vs OADE_noOBL | zdt6 | original | HV | +8.931e-05 | 18 | 1 | NS |
| OADE vs OADE_noOBL | zdt6 | shifted | IGD | +5.504e-03 | 11 | 1 | NS |
| OADE vs OADE_noOBL | zdt6 | shifted | HV | -7.931e-03 | 11 | 1 | NS |
| OADE vs OADE_noOBL | zdt4 | original | IGD | -4.039e-01 | 30 | 6.71e-08 | OADE better |
| OADE vs OADE_noOBL | zdt4 | original | HV | +5.540e-01 | 30 | 6.71e-08 | OADE better |
| OADE vs OADE_noOBL | zdt4 | shifted | IGD | -2.538e-01 | 21 | 0.313 | NS |
| OADE vs OADE_noOBL | zdt4 | shifted | HV | +1.809e-01 | 21 | 0.247 | NS |
| OADE vs NSGA2 | zdt1 | original | IGD | -6.916e-04 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt1 | original | HV | +2.671e-03 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt1 | shifted | IGD | +4.697e-03 | 0 | 6.71e-08 | other better |
| OADE vs NSGA2 | zdt1 | shifted | HV | -8.097e-03 | 0 | 6.71e-08 | other better |
| OADE vs NSGA2 | zdt6 | original | IGD | -1.264e-02 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt6 | original | HV | +2.028e-02 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt6 | shifted | IGD | -6.338e-01 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt6 | shifted | HV | +3.037e-01 | 30 | 6.71e-08 | OADE better |
| OADE vs NSGA2 | zdt4 | original | IGD | -2.373e-03 | 20 | 1 | NS |
| OADE vs NSGA2 | zdt4 | original | HV | +4.477e-03 | 20 | 1 | NS |
| OADE vs NSGA2 | zdt4 | shifted | IGD | +2.521e-01 | 0 | 6.71e-08 | other better |
| OADE vs NSGA2 | zdt4 | shifted | HV | -3.680e-01 | 0 | 6.71e-08 | other better |

## Interaction: median IGD(other)/IGD(OADE), original vs shifted (Mann-Whitney on per-seed log ratios, Holm over 9)

| Contrast | Problem | ratio original | ratio shifted | p Holm | verdict |
|---|---|---:|---:|---:|---|
| OADE vs OADE_bounce | zdt1 | 1.024 | 1.065 | 0.603 | NS |
| OADE vs OADE_bounce | zdt6 | 1.118 | 1.049 | 0.309 | NS |
| OADE vs OADE_bounce | zdt4 | 11.013 | 3.004 | 0.21 | NS |
| OADE vs OADE_noOBL | zdt1 | 1.021 | 0.988 | 0.603 | NS |
| OADE vs OADE_noOBL | zdt6 | 0.985 | 0.945 | 0.603 | NS |
| OADE vs OADE_noOBL | zdt4 | 49.572 | 2.005 | 8.58e-08 | differs |
| OADE vs NSGA2 | zdt1 | 1.159 | 0.619 | 2.72e-10 | differs |
| OADE vs NSGA2 | zdt6 | 4.282 | 7.419 | 1.42e-09 | differs |
| OADE vs NSGA2 | zdt4 | 1.414 | 0.034 | 1.83e-09 | differs |

ratio > 1: OADE (clip, with OBL) has lower IGD than the other algorithm.

## ZDT4 runs with IGD > 1e-2 (trapped on local fronts), out of 30

| Variant | OADE | OADE_bounce | OADE_noOBL | NSGA2 |
|---|---:|---:|---:|---:|
| original | 9 | 25 | 30 | 12 |
| shifted | 30 | 30 | 30 | 6 |
