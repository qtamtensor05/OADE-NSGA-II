# Reproducing the current evaluation

## Environment

Install the project in an isolated Python environment. The exact completed-run environment is captured in the [ZDT v2 manifest](../../results/experiments/zdt_seven_fixed_oade_v2/study_manifest.json); the earlier audit snapshot is not its execution environment.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

## Current benchmark

Use the [ZDT seven-algorithm protocol](zdt_seven_fixed_oade.md). Fixed OADE and corrected baselines are required. Earlier result reports and benchmark datasets are not the reproduction target.

```powershell
$env:OMP_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage plan
.\.venv\Scripts\python.exe -m research benchmark-zdt-seven --stage run --jobs 4 --out-dir results/experiments/zdt_seven_fixed_oade_v2_replication
```

Add `--resume` only for the same interrupted execution. Never edit a manifest to authorize changed code, configuration or environment. The main OADE solver is `oade_nsga2`; the research entry point only orchestrates the study.

## Audit completed results

```powershell
.\.venv\Scripts\python.exe analysis/audit_zdt_seven_v2.py
```

This verifies primary/source checksums, X/F, indicators and statistics, and writes derived audit tables and the report. It does not rerun solvers. See the [current report](../reports/zdt_seven_fixed_oade_v2_report.md) for exclusions, test definitions and interpretation boundaries.

## Component studies and checks

Restart, initialization, diversity and sensitivity studies have their own protocols in the [experiment registry](experiment_registry.md). Keep their evidence separate from the comparator benchmark. Use `tmp` for disposable smoke runs. The structure checker verifies maintained documentation links and source boundaries.

```powershell
.\.venv\Scripts\python.exe -m research check-structure
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
