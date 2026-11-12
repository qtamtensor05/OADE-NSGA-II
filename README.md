# OADE-NSGA-II: Adaptive Opposition-Based Differential Evolution NSGA-II

**Language / Ngôn ngữ:** **English** | [Tiếng Việt](README.vi.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Protocol](https://img.shields.io/badge/Benchmark-Fixed--Budget%2020k-orange.svg)](#2-experimental-protocol--statistical-discipline)
[![Reproducible Benchmarks](https://img.shields.io/badge/Benchmarks-Reproducible-blue.svg)](#2-experimental-protocol--statistical-discipline)

A research implementation that combines **Opposition-Based Learning (OBL)**, **neighborhood-directed Differential Evolution (DE)**, **online F/CR updates**, and a configurable **diversity-aware restart** policy with the NSGA-II framework. The benchmark reports below evaluate these variants on selected test suites; they do not establish universal improvement over NSGA-II.

---

Research entry point: [current manuscript and report index](docs/index.md). Implementation identities: [baseline registry](docs/protocols/baselines.md). Execution and historical provenance: [reproducibility](docs/protocols/reproducibility.md).

## 📌 Table of Contents
- [1. Overview & Algorithm Components](#1-overview--algorithm-components)
- [2. Experimental Protocol & Statistical Discipline](#2-experimental-protocol--statistical-discipline)
- [3. Reported Results](#3-reported-results)
- [4. Observed Strengths in Tested Suites](#4-observed-strengths-in-tested-suites)
- [5. Weaknesses, Limitations & Claim Boundaries](#5-weaknesses-limitations--claim-boundaries)
- [6. Visual Evidence & Figures](#6-visual-evidence--figures)
- [7. Project Structure & Reproducibility](#7-project-structure--reproducibility)
- [8. Quick Start Guide](#8-quick-start-guide)

---

## 1. Overview & Algorithm Components

This project studies four mechanisms added to an NSGA-II-based search procedure. Their presence in the implementation does not, by itself, establish that each mechanism improves performance:

1. **OBL + Sobol Quasi-Random Initialization**: The standalone solver can sample candidates and opposite points before selecting its initial population. This standalone initialization is bypassed in the fixed-budget benchmarks, which use a common uniform initial population. The reported OBL ablation concerns periodic injection, including generation zero, rather than Sobol initialization.
2. **Periodic Opposition Injection**: Injects opposite candidates every 10 generations. The current results do not isolate its causal contribution from the other OADE components.
3. **Neighborhood-Directed DE Mutation (DE/current-to-pbest/1)**: Uses neighborhood information when constructing differential-evolution mutation candidates. Its isolated contribution has not been established across all tested suites.
4. **Adaptive Diversity-Aware Restart (v2 configuration)**: Implements a dual-condition trigger:
   * **Stagnation detection**: Tracks ideal point progress ($\|\Delta \mathbf{z}^*\| < 10^{-4}$).
   * **Diversity collapse verification**: Checks whether normalized decision-space standard deviation $\max_j \sigma_j < 0.02$ or objective spread $< 10^{-3}$.
   * **Renewal rule**: Retains 80% of selected individuals and generates replacements using local OBL and Gaussian perturbations, with soft decay of adaptation history ($\mu_F, \mu_{CR}$). Held-out results do not yet verify that this trigger caused the measured outcomes; trigger counts were not recorded.

---

## 2. Experimental Protocol & Statistical Discipline

The reports document the benchmark design, run-level data, statistical tests, and known limitations. This project summary is not a formal compliance claim for a journal; requirements should be checked against the selected venue before submission.

* **Independent Experimental Unit**: One stochastic run; 30 scheduled per configuration. Current valid matched-pair counts: algorithm_benchmark_v2: 30–30; dtlz_benchmark: 26–30; wfg_m2_7algo_benchmark: 30–30; wfg_compact_benchmark: 30–30.
* **Evaluation Budget**: The RNSGA2 blocks for ZDT, DTLZ, WFG include aspiration-point setup within the 20,000-evaluation cap and runtime. See the [suite-specific accounting](docs/protocols/experiment_registry.md#budget-definition). Other algorithms may finish below the cap when another batch would exceed it.
* **Paired Design**: All competing algorithms start from the exact same initial population and pseudo-random seed on each run.
* **Test Suites (21 core configurations plus 12 compact-WFG scaling configurations; 6,210 stored records; some baselines and settings are reused across batches)**:
  * **Bi-objective ZDT (`1,050` runs, 7 algorithms)**: ZDT1 ($D=30$), ZDT2 ($D=30$), ZDT3 ($D=30$), ZDT4 ($D=10$, $21^9$ local fronts), and ZDT6 ($D=10$, non-uniform density).
  * **Multi-/Many-objective DTLZ1–DTLZ4 (`2,520` runs, 7 algorithms)**: DTLZ1 ($M \in \{2,3,5\}, D \in \{6,7,9\}$) and DTLZ2–DTLZ4 ($M \in \{2,3,5\}, D \in \{11,12,14\}$).
  * **Bi-objective WFG (`840` runs, 7 algorithms)**: `WFG1, WFG4, WFG6, WFG9` ($M=2, D=24, k=4$) testing bias/flatness, separable concave multimodality, non-separability, and deceptive traps.
  * **Compact WFG Scaling (`1,800` runs, 5 fast algorithms)**: `WFG1, WFG4, WFG6, WFG9` ($M \in \{2,3,5\}, D=24, k \in \{4,8\}$) across `OADE_NSGAII`, `NSGA2`, `DNSGA2`, `RNSGA2`, and `NSGAII_SDR_OLS`.
* **Competing Baselines (6 Algorithms)**:
  * NSGA-II (Deb et al., 2002)
  * D-NSGA-II (Dynamic NSGA-II)
  * R-NSGA-II (Reference point-based NSGA-II)
  * CGDE-NSGA-II (Cross-Generation Differential Evolution (local implementation))
  * NSGA-II-SDR-OLS (Strengthened Dominance Relation + Opposition and Local Search)
  * CE-MOEA (Continuous Encoding MOEA (continuous-search adaptation))
* **Statistical Inference**: Two-sided paired Wilcoxon signed-rank tests with Holm correction within each suite and metric family ($m = 30$ for ZDT; $m = 72$ for DTLZ1–4; $m = 24$ for WFG $M=2$ 7-algorithm; $m = 48$ for compact WFG; $\alpha = 0.05$). Cross-suite win counts are descriptive summaries of these separately corrected results, not one 204-test Holm family. “No significant difference” does not establish equivalence.
* **Effect Sizes**: Matched-pairs rank-biserial correlation $r \in [-1, 1]$.

---

## 3. Reported Results

| Dataset | Records | Invalid | Comparisons | OADE W / ND / L |
|---|---:|---:|---:|---|
| algorithm_benchmark_v2 | 1050 | 0 | 60 | 58 / 1 / 1 |
| dtlz_benchmark | 2520 | 18 | 144 | 91 / 40 / 13 |
| wfg_m2_7algo_benchmark | 840 | 0 | 48 | 42 / 0 / 6 |
| wfg_compact_benchmark | 1800 | 0 | 96 | 56 / 11 / 29 |

Detailed tables: [ZDT](docs/reports/benchmark_v2_results_report.md), [DTLZ](docs/reports/dtlz_results_report.md), [integrated ZDT/DTLZ](docs/reports/dtlz1_4_integrated_report.md), [WFG](docs/reports/wfg_compact_report.md). W/ND/L means OADE win/no detected difference/loss. Each metric/suite has its own Holm family; cross-suite counts are descriptive. The same 120 RNSGA2 WFG M=2 records are shared by both WFG tables.

## 4. Observed Strengths in Tested Suites

1. **Strong Results on Selected Multimodal Problems**:
   OADE-NSGA-II v2 had favorable comparisons on the tested ZDT4, DTLZ1/3, and bi-objective WFG9 cases. On `wfg9_m2`, its median IGD was `0.0347` versus `0.128–0.640` for the six tested comparators. These results do not isolate which OBL or DE component caused the gains.
2. **No Invalid OADE DTLZ4 Outputs Under the Structural Validator**:
   OADE-NSGA-II v2 had **0 invalid outputs in 90 DTLZ4 runs** under the recorded structural validator. Historical corner-collapse counts for other solvers use a different quality diagnosis with an incompletely recorded rule; they should not be compared as structural failure rates. No guarantee is made for other settings.
3. **Lower Variability with Restart Candidates on Held-Out ZDT Runs**:
   On held-out seeds, both No Restart and Adaptive Restart had lower variability than classic restart on several ZDT problems. Their final IGD and HV values were identical in 148/150 paired problem-seed rows, so the data do not establish that the adaptive trigger itself caused the improvement.
4. **Computational Efficiency**:
   Measured runtimes averaged **10.8–14.8s/run** on ZDT, **2.74–3.04s/run** on DTLZ4, and **4.42–12.53s/run** on `WFG M=2` (`OMP_NUM_THREADS=1`). Some local `CGDE-NSGA-II` and `CE-MOEA` implementations took 7.7× to 101× longer in these runs. These ratios compare the measured implementations and environment, not algorithm-independent complexity.
5. **Online Parameter Self-Adaptation**:
   $F$ uses a smoothed Lehmer mean and $CR$ a smoothed arithmetic mean of DE offspring assigned rank 1. The DE selection probability tracks the generated DE share, rather than relative DE/SBX success. These updates do not establish freedom from configuration sensitivity.

---

## 5. Weaknesses, Limitations & Claim Boundaries

The reports state the following observed weaknesses and boundaries:

1. **Confirmed Deficit on Smooth/Concave Multi-Objective Fronts (`dtlz2_m3`, `dtlz4_m3`, `WFG4`, and Scaled `WFG6/9` at $M \ge 3$)**:
   On the tested configurations, OADE-NSGA-II v2 trails `NSGA-II` / `D-NSGA-II` on `dtlz2_m3`, `dtlz4_m3`, separable concave `WFG4` ($M=2,3,5$), `WFG6` ($M=3,5$), and `WFG9` ($M=5$). `CGDE-NSGA-II` has lower median IGD on `wfg6_m2` (`0.0302` vs `0.0526`) but took about 101× longer in this implementation and environment. The WFG report proposes three source-level explanations for late-budget stagnation; these remain hypotheses pending targeted ablations.
2. **Crowding-Distance Saturation at $M=5$ Under Extreme Multimodality (`dtlz1_m5`, `dtlz3_m5`)**:
   Under the tested 20,000-evaluation cap, 17/30 runs on `dtlz1_m5` ($\text{IGD}_{\text{med}} = 0.8972$, maximum `24.71`) and 30/30 runs on `dtlz3_m5` had `HV = 0`. This is consistent with limited convergence pressure in these cases; the proposed explanation has not been isolated experimentally.
3. **Remaining Test Suite Boundaries**:
   Current empirical evidence covers **ZDT1–4, ZDT6** ($M=2$), **DTLZ1–4** ($M \in \{2, 3, 5\}$), **WFG1, WFG4, WFG6, WFG9** ($M=2$ with all 7 solvers; $M \in \{2,3,5\}$ with the 5 fast solvers). Performance on **degenerate/disconnected DTLZ5–7**, remaining WFG suites (`WFG2, WFG3, WFG5, WFG7, WFG8`), `CE_MOEA`/`CGDE_NSGAII` at $M=3,5$ WFG, constrained MOPs, and discrete problems remains untested.
4. **Hardware-Dependent Runtime**:
   Reported wall-clock runtimes reflect Python execution overhead and BLAS thread settings (`OMP_NUM_THREADS=1` cut DTLZ4 runtimes ~3× vs unpinned DTLZ1–3 batches), and must **not** be interpreted as hardware-independent asymptotic complexities $\mathcal{O}(\cdot)$.
5. **Isolated Component Attribution & Inconclusive Tests**:
   The ablation supports an OBL contribution to ZDT4 performance, but evaluates periodic injection under the common uniform warm start; it does not evaluate initial Sobol/OBL. Held-out results show No Restart and Adaptive Restart outperforming Full OADE on ZDT1–ZDT3 and ZDT6; because their outputs are nearly identical and trigger counts are absent, the adaptive mechanism itself is not confirmed. The data suggest, but do not establish, a tail-risk role for some adaptive components. Non-significant comparisons denote no detected difference at $n=30$, not equivalence. Confidence intervals for paired effects are also not yet reported.

---

## 6. Visual Evidence & Figures

All figures are archived reproducibly in vector PDF, SVG, and PNG preview under [`results/figures/`](results/figures) (oversized `.tiff` print files and diagnostic overlay PDFs are local; figure sources and JSON QA records are included):

| Figure File | Description |
|---|---|
| [`integrated_7algo_landscape.png`](results/figures/integrated_7algo_landscape.png) | **Multi-panel overview**: 17-problem rank-biserial effect-size matrix (`a`), 204-test outcome ledger (`b`), and 34-endpoint mean rank vs DTLZ4 runtime proxy (`c`). |
| [`dtlz1_4_scaling_diagnosis.png`](results/figures/dtlz1_4_scaling_diagnosis.png) | **2×2 DTLZ scaling grid ($M=2,3,5$)**: IGD summaries on DTLZ1/3 (`a, b`), 3-objective DTLZ2 comparison (`c`), and observed DTLZ4 median HV (`d`). |
| [`wfg_m2_7algo_profile.png`](results/figures/wfg_m2_7algo_profile.png) | **7-Algorithm WFG $M=2$ validation**: 48-test IGD/HV effect heatmap (`a`), run-level `WFG9` IGD distributions (`b`), and 8-endpoint quality rank vs measured runtime (`c`). |
| [`wfg_scaling_diagnosis.png`](results/figures/wfg_scaling_diagnosis.png) | **2×2 WFG scaling grid ($M=2 \to 3 \to 5$)**: 5-algo Holm outcome transition (`a`), paired `OADE/NSGA2` IGD ratios (`b`), and `wfg1_m5` / `wfg9_m5` HV convergence (`c, d`). |
| [`benchmark_v2_outcome_counts.png`](results/figures/benchmark_v2_outcome_counts.png) | Horizontal stacked bar chart displaying 58 significant wins, 1 comparison with no detected difference, and 1 significant loss on ZDT v2 against 6 baselines. |
| [`benchmark_v2_v1_vs_v2_delta.png`](results/figures/benchmark_v2_v1_vs_v2_delta.png) | Descriptive mean IGD reductions from OADE v1 to v2 across five ZDT problems (2.1%–40.1%); this does not isolate the restart mechanism. |
| [`restart_direct_comparison.png`](results/figures/restart_direct_comparison.png) | Grouped boxplots comparing Old Restart, No Restart, and New Restart side-by-side with overlaid raw seeds. |
| [`restart_convergence.png`](results/figures/restart_convergence.png) | Within-budget convergence trajectories (Median IGD + IQR shaded bands) over 20,000 evaluations. |
| [`restart_confirmation_paired.png`](results/figures/restart_confirmation_paired.png) | Paired percentage improvement distribution on 30 held-out seeds ($1000 \dots 1029$). |

Full quality assurance audits and font-size checks are logged in [`results/figures/figure_qa.md`](results/figures/figure_qa.md).

---

## 7. Project Structure & Reproducibility

Each algorithm has its own directory under `src/`. Shared utilities are in `src/shared/`; experiment orchestration, statistics and plotting are in `src/research/`.


Tests, smoke configurations, figure sources, environment lockfiles and JSON QA records are included in the research source. Generated smoke outputs, caches, TIFF rasters and diagnostic overlay PDFs remain local. See [reproducibility guide](docs/protocols/reproducibility.md).

---

## 8. Quick Start Guide

### Prerequisites
* Python 3.10+
* Virtual environment with dependencies from `requirements.txt`:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### Reproduce Benchmark v2 (ZDT, 7 Algorithms, 1,050 Runs)
```powershell
.venv\Scripts\python.exe main.py benchmark --config config/suites/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2
```

### Reproduce DTLZ1–DTLZ4 Benchmark (M = 2, 3, 5; 2,520 Runs)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-dtlz --config config/suites/dtlz1_4_benchmark.yaml --out-dir results/reproduction_dtlz --jobs 8
```

### Reproduce Compact WFG Benchmarks (M = 2, 3, 5 & Full 7-Algo M = 2)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-wfg --config config/suites/wfg_compact_benchmark.yaml --out-dir results/reproduction_wfg_compact --jobs 8
.venv\Scripts\python.exe main.py benchmark-wfg --config config/suites/wfg_m2_7algo_benchmark.yaml --out-dir results/reproduction_wfg_m2 --jobs 10
```

### Generate Built-in Summary Plots
```powershell
.venv\Scripts\python.exe main.py plot-algorithm-benchmark
.venv\Scripts\python.exe main.py plot-convergence
```

---

## 📜 Citation & Research Reports

If you use OADE-NSGA-II in your research, please refer to the detailed evaluation reports in `docs/`:
* **WFG Compact & M=2 7-Algorithm Report**: [`docs/reports/wfg_compact_report.md`](docs/reports/wfg_compact_report.md)
* **Integrated ZDT + DTLZ1–4 Report**: [`docs/reports/dtlz1_4_integrated_report.md`](docs/reports/dtlz1_4_integrated_report.md)
* **Benchmark v2 Report (ZDT)**: [`docs/reports/benchmark_v2_results_report.md`](docs/reports/benchmark_v2_results_report.md)
* **Restart Confirmation Report**: [`docs/reports/restart_confirmation_report.md`](docs/reports/restart_confirmation_report.md)
* **Component Ablation Report**: [`docs/reports/ablation_results_report.md`](docs/reports/ablation_results_report.md)

## Results organized by problem

Download CSV evidence from the [ZIP index](results/CSV_DOWNLOADS.md). After cloning, run `python scripts/csv_archives.py restore` before data-dependent analyses. Reports and figures remain readable without extraction.

The current research focus is **ZDT**. See [the per-problem research folders](results/by_problem/README.md) for seven-algorithm results, classic/adaptive comparisons, restart confirmation, ablation and sensitivity. Existing DTLZ/WFG evidence is organized alongside ZDT for gradual extension. Rebuild these views with `python scripts/organize_by_problem.py` after adding source results.
