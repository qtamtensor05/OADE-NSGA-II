# Reproducing the research

## Environment and tests

Use Python 3.10+ and install the editable package in an isolated environment. `config/environments/requirements_audit_20261112.txt` is the exact installed audit-environment snapshot, not a reconstruction of the historical benchmark environment. Package availability and platform wheels may differ; no historical bitwise reproduction is promised.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests, smoke YAML, analysis scripts, R bootstrap files, renv.lock and JSON figure QA are source artifacts. Caches, generated smoke runs, TIFFs and diagnostic overlays are ignored.


## Current repository layout

See [structure, naming and artifact lifecycle](../governance/project_structure.md)
for session-based smoke commands and `--experiment` executions. Historical flat
datasets remain at their recorded paths. Source identities changed during the
package migration: resume an older execution only with its original checkout
and environment; never edit its manifest to authorize the refactored code.

## New runs and safe resume

Always use a new output directory to preserve archived research evidence:

```powershell
$env:OMP_NUM_THREADS=1
$env:OPENBLAS_NUM_THREADS=1
$env:MKL_NUM_THREADS=1
.\.venv\Scripts\python.exe main.py benchmark --config config/suites/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2 --jobs 6
.\.venv\Scripts\python.exe main.py benchmark --config config/suites/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2 --jobs 6 --resume
```

The same entry point accepts the DTLZ, WFG, ablation and restart YAMLs. A manifest is captured before evaluation: resolved algorithm parameters, protocol, source SHA-256 hashes, Python/package versions, platform, thread variables, Git commit and dirty state. Primary CSV checksums are committed after each complete problem. Resume checks identity, full problem-level run sets, paired seeds, dimensions, budgets, diagnostics and checkpoint integrity before recomputing derived tables. Output location and worker count are execution choices rather than algorithm parameters; runtime comparisons still require controlled worker contention.

An interruption inside a problem does not create a resumable partial problem. If interruption occurs while writing multiple checkpoint files, checksum disagreement blocks resume; preserve that directory for inspection rather than manually certifying it. A manifest without checkpoint files can resume from an empty start. Existing primary evidence is never overwritten by a fresh run.

The baseline-reuse runner `scripts/run_benchmark_v2.py` accepts `--baseline-dir`, `--out-dir` and `--preflight-only`. It requires execution-time provenance, matching comparator protocol/source/environment and complete diagnostic/trajectory records before starting OADE. Historical v1 CSVs lack this proof and are rejected for new reuse. Use the full seven-algorithm command above for a new reproduction. The current ZDT tables share comparator blocks. The RNSGA2 block has an execution manifest; the other blocks retain archived provenance. See [dataset composition](../../results/provenance/zdt_composition.json).

## Artifact inventory

```powershell
.\.venv\Scripts\python.exe scripts/inventory_research.py
```

This writes results/research_inventory.json with observed CSV hashes, record counts, invalid diagnostics, valid-pair ranges and descriptive outcomes. For ZDT, the inventory links to algorithm-block provenance in results/provenance/. The RNSGA2 primary blocks can be reconstructed by filtering either main table and checked against the retained execution manifest. Archived versions without captured manifests remain unknown. See the [experiment registry](experiment_registry.md).

## Figures

R source: analysis/figures/generate_research_figures.R produces the original v1/ablation figures. R version and package snapshot are in renv.lock. Restore with `Rscript -e 'renv::restore()'` after installing renv if necessary; then use scripts/render_research_figures.ps1 on Windows or `Rscript analysis/figures/generate_research_figures.R` from the activated project.

Python sources in analysis/figures produce ZDT v2, restart, DTLZ and WFG figures. Run them from the repository root with the Python environment. The integrated and WFG scripts import the installed research.plotting.qa alignment helper, so they do not require an agent skill installation. PDF collision inspection additionally requires PyMuPDF (`pip install -r config/environments/requirements_figure_qa.txt`).

```powershell
.\.venv\Scripts\python.exe analysis/figures/plot_integrated_7algo_dtlz.py
.\.venv\Scripts\python.exe scripts/figure_qa/audit_pdf_text.py results/figures/integrated_7algo_landscape.pdf
.\.venv\Scripts\python.exe scripts/figure_qa/audit_figure_collisions.py results/figures/integrated_7algo_landscape.pdf --json-out results/figures/integrated_7algo_landscape.collision-audit.json
```

Running figure scripts updates their bundles/source-data exports; review the diff before replacing published figures. Alignment/collision checks do not prove scientific validity or replace final-size visual inspection. The R and Python figure families have separate provenance; one does not substitute for the other.

## Statistical and failure conventions

The shared pipeline uses two-sided SciPy Wilcoxon signed-rank tests, `zero_method="wilcox"`, with SciPy's default method selection (`auto` in the audited environment). Exact numerical behavior for ties/zeros can depend on SciPy version. All-zero differences return statistic 0 and p=1. Holm adjustment is applied separately over each metric's configured problem–comparator family. Rank-biserial effects omit zero differences and use average ranks for ties. Positive effect favors the reference for IGD and HV; stored median_paired_difference is reference minus comparison for both, so HV improvement has the opposite sign.

Thirty runs are scheduled per configuration. DTLZ currently has 26–30 valid matched pairs and 18 invalid outputs; consult current per-comparison n for each suite. Report both run failures and conditional quality. Sample SD/IQR are run dispersion, not confidence intervals for paired effects.

`invalid collapsed_front` means all returned objective rows are identical after rounding to 12 decimals, with more than one row. The current validator accepts a single-point front if other checks pass. This is a structural validity rule, not a general convergence or diversity guarantee. `Corner collapse` in the historical DTLZ narrative is a quality diagnosis applied to some structurally valid outputs. Its complete run-level historical classification rule is not recorded; counts must be described as historical diagnostics, not validator failure rates or a reproducible new endpoint. HV=0 alone is not proof of identical objective vectors.

## Evaluation accounting

RNSGA2 setup is charged within the cap and runtime for ZDT, DTLZ, WFG. See the [suite-specific definitions](experiment_registry.md#budget-definition). Execution manifests and dataset composition retain the provenance of each algorithm block.

## Current result evidence

The full suite YAMLs above remain the normal reproduction route. Current RNSGA2 blocks in ZDT/DTLZ/WFG include setup in their cap and runtime. Algorithm-block manifests, dataset composition and validation are in results/provenance/. The WFG M=2 block is shared between the two WFG tables and is not an independent replication. Filtering the RNSGA2 records reconstructs the primary block checksums in the retained execution manifests.
