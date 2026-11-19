# Reproducing the current evaluation

## Environment

Install the project in an isolated Python environment. The completed six-solver execution environment is captured in its [manifest](../../results/experiments/zdt_six_fixed_oade_v1/study_manifest.json): Python 3.14.7, numpy 2.5.4, scipy 1.18.1 and pymoo 0.6.2. The historical ZDT v2 environment is separate.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

## Current benchmark

Use the [six-algorithm protocol](zdt_six_fixed_oade.md): fixed OADE, NSGA-II, D-NSGA-II, CGDE, GDE3 and NSDE. All 900 runs completed (899 valid); the historical seven-algorithm study is a separate reproduction target. Use a new directory for replication.

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage plan
.\.venv\Scripts\python.exe -m research benchmark-zdt-six --stage run --jobs 8 --out-dir results/experiments/zdt_six_replication
```

Add `--resume` only for the same interrupted execution. Never edit a manifest to authorize changed code, configuration or environment. The main OADE solver is `oade_nsga2`; the research entry point only orchestrates the study.

The completed study recorded eight workers but no OMP/BLAS thread-variable limits. Setting the limits above is a recommendation for a new replication, not a description of the original run; do not change environment variables when resuming a strict-identity study.

After source maintenance, use a fresh output directory for new execution. The [execution source snapshot](../../results/experiments/zdt_six_fixed_oade_v1/config/execution_sources.zip) preserves the 113 files hashed by the completed study. Its audit verifies snapshot bytes against original manifest hashes when the current file has changed or been removed; it does not rewrite historical provenance or bypass strict resume identity.

## Audit completed results

```powershell
.\.venv\Scripts\python.exe analysis/audit_zdt_six.py
& "C:/Program Files/R/R-4.6.2/bin/Rscript.exe" --vanilla analysis/plot_zdt_six_comparison.R
.\.venv\Scripts\python.exe analysis/report_zdt_six.py
```

This verifies primary/source checksums, X/F, indicators and statistics, then regenerates the figure and report without rerunning solvers. The R script uses the project R library. See the [current audited report](../reports/zdt_six_fixed_oade_report.md) for exclusions, all 50 global-Holm endpoints and interpretation boundaries. The independent calculation path shares the analyst and objective/indicator libraries with the original pipeline; it is not external replication.

## Component studies and checks

Restart, initialization, diversity and sensitivity studies have their own protocols in the [experiment registry](experiment_registry.md). Keep their evidence separate from the comparator benchmark. Use `tmp` for disposable smoke runs. The structure checker verifies maintained documentation links and source boundaries.

```powershell
.\.venv\Scripts\python.exe -m research check-structure
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
