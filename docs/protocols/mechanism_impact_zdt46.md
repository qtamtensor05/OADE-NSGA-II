# OADE mechanism impact on ZDT4 and ZDT6

Run the fixed production solver with observation-only overrides, then paired
leave-one-mechanism-out interventions in a research subclass. Production OADE
configuration and search code are unchanged. D=10, population=100, budget=20,000,
seeds=42..71 by default: 480 runs. Initialization is the same seeded uniform
population within each problem/seed. Each run counts all objective calls,
including OBL, restart and duplicate filling. Atomic batches can leave unused budget.

```powershell
.\.venv\Scripts\python.exe -m research mechanism-impact --stage plan
.\.venv\Scripts\python.exe -m research mechanism-impact --stage run
# Continue an interrupted run with identical arguments and source:
.\.venv\Scripts\python.exe -m research mechanism-impact --stage run --resume
```

Smoke verification (32 runs; not performance evidence):

```powershell
.\.venv\Scripts\python.exe -m research mechanism-impact --stage run --runs 2 --population 10 --budget 300 --out-dir results/experiments/oade_mechanism_zdt46_smoke
```

| Variant | Intervention |
|---|---|
| full | Fixed OADE with passive measurement |
| no_obl | Disable periodic OBL |
| no_restart | Suppress adaptive restart |
| fixed_f_cr | Hold mean F=.65, mean CR=.5, including at restart; sampling remains stochastic |
| fixed_pde | Hold pDE=.5 |
| global_neighborhood | Use all other individuals as DE neighbors; retain donor rule |
| sbx_only | Always choose SBX |
| de_only | Always choose DE |

Outputs under the chosen directory:

- `manifest.json`: dimensions and implementation hashes; resume rejects changed configuration/source.
- `primary/*.json`: atomic per-run records, final X/F, reference front, telemetry.
- `derived/runs.csv`: IGD, HV, validity, actual evaluations, runtime.
- `derived/events.csv`: OBL/restart attempts, completion, budget blocking and evaluation cost; includes events in an interrupted final generation.
- `derived/trace.csv`: completed generations only; DE/SBX/OBL trial counts and retained counts, learned F/CR/pDE and parameter changes.
- `derived/activation.csv`: per-run activations divided by observed generations (including an unfinished generation when it has an OBL/restart event). DE/SBX activation means a completed generation with at least one trial; parameter activation means an actual change, not merely executing the update function. Event evaluation totals exclude initialization and DE/SBX; read runs.csv for total cost. Zero observed restarts is not evidence that restart cannot help.
- `derived/impact.csv`: full versus each intervention using paired valid seeds, median paired difference (full minus intervention), rank-biserial effects, excluded pair counts and two-sided Wilcoxon. Holm correction covers all 28 endpoints (2 problems x 7 comparisons x 2 metrics). IGD lower / HV higher is better; positive rank-biserial favors full. Smoke p-values are only pipeline checks.

These interventions estimate conditional contribution within the full algorithm,
not independent additive contributions. They do not identify interactions. Shared
seeds match initialization but diverging search paths consume different random
draws. Survival is descriptive, not causal benefit. OBL/restart event completion
does not imply that its containing generation completed. Runtime includes telemetry
and must not be compared directly to earlier uninstrumented benchmark timings.
