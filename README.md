# OADE-NSGA-II: Adaptive Opposition-Based Differential Evolution NSGA-II

**Language / Ngôn ngữ:** **English** | [Tiếng Việt](README.vi.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Protocol](https://img.shields.io/badge/Benchmark-Fixed--Budget%2020k-orange.svg)](#2-experimental-protocol--statistical-discipline)
[![Reproducible Benchmarks](https://img.shields.io/badge/Benchmarks-Reproducible-blue.svg)](#2-experimental-protocol--statistical-discipline)

A research implementation that combines **Opposition-Based Learning (OBL)**, **neighborhood-directed Differential Evolution (DE)**, **online F/CR updates**, and a configurable **diversity-aware restart** policy with the NSGA-II framework. The benchmark reports below evaluate these variants on selected test suites; they do not establish universal improvement over NSGA-II.

---

Research entry point: [current manuscript and report index](docs/index.md). Implementation identities: [baseline registry](docs/baselines.md). Execution and historical provenance: [reproducibility](docs/reproducibility.md).

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

* **Independent Experimental Unit**: One complete stochastic run (30 scheduled runs per configuration; 26–30 valid matched pairs per comparison in DTLZ, 30 in the other core suites).
* **Evaluation Budget**: ZDT uses a 20,000-evaluation cap including RNSGA2 aspiration-point setup and runtime. Archived DTLZ/WFG counters use the search-budget convention described in the [experiment registry](docs/experiment_registry.md#budget-definition). Actual use may be lower when the next batch would exceed the cap; OADE typically uses about 99.7–99.9%.
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

### Combined 7-Algorithm Scorecard (ZDT + DTLZ1–DTLZ4; 204 Pairwise Comparisons, 3,570 Runs)

* **Combined outcome count**: **149 significant wins (73.0%) / 41 comparisons with no detected difference (20.1%) / 14 significant losses (6.9%)** across 3,570 runs (`OADE-NSGA-II v2`: **510/510 valid runs**, 0 validation failures). Each adjusted p-value belongs to its suite-by-metric Holm family; the combined count is descriptive and is not a single 204-test family-wise analysis.
  * **ZDT Benchmark v2 (60 comparisons)**: **58 wins / 1 comparison with no detected difference / 1 loss** (descriptive Rank #1 on 8/10 endpoints).
  * **DTLZ1–DTLZ4 Benchmark (144 comparisons)**: **91 wins / 40 with no detected difference / 13 losses** (Rank #1 on 8/12 IGD medians and 7/12 HV means; no losses at $M=5$ in this suite).
* **Pairwise outcome counts across the 17 tested configurations**: OADE-NSGA-II v2 had no significant losses against **`CE-MOEA`** (23–11–0), **`NSGA-II-SDR-OLS`** (30–4–0), or **`R-NSGA-II`** (31–3–0), while results against **`NSGA-II`** (22–7–5), **`D-NSGA-II`** (22–7–5), and **`CGDE-NSGA-II`** (21–9–4) were mixed. Counts are descriptive; each comparison uses the correction family stated above.

### Bi-Objective ZDT Benchmark v2 (`results/algorithm_benchmark_v2/`, 1,050 Runs)

| Problem | Metric | OADE-NSGA-II v2 | Best Competitor | Competitor Name | $p_{\text{adj}}$ (Holm) | Effect Size ($r$) | Inferential Result |
|---|---|---:|---:|---|---:|---:|---|
| **ZDT1** | IGD ↓<br>HV ↑ | **0.004475 ± 0.000251**<br>**0.870866 ± 0.000232** | 0.005175 ± 0.000298<br>0.868053 ± 0.000417 | NSGA-II<br>NSGA-II | $5.59 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+1.000$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT2** | IGD ↓<br>HV ↑ | **0.004756 ± 0.000292**<br>**0.537674 ± 0.000222** | 0.005405 ± 0.000306<br>0.534072 ± 0.000611 | NSGA-II<br>NSGA-II | $7.82 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+0.983$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT3** | IGD ↓<br>HV ↑ | **0.004986 ± 0.000336**<br>**1.051221 ± 0.000152** | 0.005568 ± 0.000291<br>1.047182 ± 0.006699 | D-NSGA-II<br>NSGA-II | $1.17 \times 10^{-5}$<br>$5.59 \times 10^{-8}$ | $+0.884$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT4** | IGD ↓<br>HV ↑ | **0.006831 ± 0.003329**<br>**0.865051 ± 0.005679** | 0.009953 ± 0.005080<br>0.859362 ± 0.007910 | NSGA-II<br>NSGA-II | $4.04 \times 10^{-3}$<br>$8.72 \times 10^{-4}$ | $+0.626$<br>$+0.669$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT6** | IGD ↓<br>HV ↑ | 0.003844 ± 0.000193<br>0.438177 ± 0.000253 | **0.003823 ± 0.000223**<br>**0.439057 ± 0.000199** | CGDE-NSGA-II<br>CGDE-NSGA-II | $0.776$ (no detected difference)<br>$5.58 \times 10^{-8}$ | $-0.062$<br>$-1.000$ | No detected difference (#2)<br>CGDE better (#2) |

### Multi-/Many-Objective DTLZ1–DTLZ4 Highlights (`results/dtlz_benchmark/`, 2,520 Runs)

| Problem Family | $M=2$ Outcome | $M=3$ Outcome | $M=5$ Outcome |
|---|---|---|---|
| **DTLZ1** (Multimodal linear) | **6/6 IGD & HV Wins** (`0.0022` med IGD) | **6/6 Wins ($r = +1.000, W=0$)**; `0.0292` vs NSGA-II `0.0967` | **6/6 IGD Wins** (`0.8972` vs `40.17` NSGA-II); **13/30 HV>0** vs **0/30** all baselines |
| **DTLZ2** (Unimodal sphere) | **No detected IGD difference** vs NSGA-II (`0.0050`); NSGA-II +0.11% HV | **Trails SBX & CGDE** (`0.0762` vs `0.0685`–`0.0720` IGD) | **Rank #1** (`0.4214` IGD, `0.4517` HV); beats D-NSGA-II, CGDE, CE-MOEA, R-NSGA-II, SDR-OLS |
| **DTLZ3** (Hard multimodal sphere) | **6/6 IGD Wins** (`1.0708` med, **11/30 HV>0**) | **6/6 IGD Wins ($r = +1.000$)**; `2.5460` vs `14.1763`–`108.7107` | **5/6 IGD Wins** (`72.7081` vs `108.3939`–`258.9448`; no detected difference vs SDR-OLS); **0/30 HV>0** all algorithms |
| **DTLZ4** ($\alpha=100$ biased sphere) | **0/30 collapsed fronts** (`0.0051` median); NSGA-II collapses **11/30** (`0.2753` mean) | **Trails SBX & CGDE** (`0.0780` vs `0.0686`–`0.0704` IGD) | **Rank #1 IGD (`0.3746`, 0/30 collapsed fronts)**; no detected difference vs CE-MOEA/CGDE, with lower measured runtime in this implementation; NSGA-II/D-NSGA-II collapse **30/30** (`HV = 0.0205`/`0.0422`) |

Full tables (Median [IQR], Mean ± SD, effect sizes) are archived in [`docs/dtlz1_4_integrated_report.md`](docs/dtlz1_4_integrated_report.md).

### WFG Suite Highlights (`results/wfg_m2_7algo_benchmark/` & `results/wfg_compact_benchmark/`, 2,640 Runs)

* **Full 7-Algorithm `WFG M=2` Outcome Count (48 comparisons, 840 runs, 0 invalid)**: **`42 wins (87.5%) / 0 with no detected difference / 6 losses (12.5%)`**, Ranked **#1 overall (`1.75` mean rank vs `NSGA2` `3.12`, `CGDE` `3.25`, `CE_MOEA` `3.50`)** — no detected losses vs `CE-MOEA` (`8–0–0`), `NSGA-II-SDR-OLS` (`8–0–0`), and `R-NSGA-II` (`8–0–0`).
  * **Bi-objective ZDT + WFG 7-algorithm descriptive count (108 comparisons, 9 problems)**: **`100 wins / 1 with no detected difference / 7 losses`**. These outcomes combine separately corrected suite results; they do not form one Holm family.
* **5-Fast-Algorithm `WFG M=2 -> 3 -> 5` Outcome Count (96 comparisons, 1,800 runs, 0 invalid)**: **`56 wins (58.3%) / 11 with no detected difference (11.5%) / 29 losses (30.2%)`**. In these four WFG problems, the win fraction declined from **87.5% at $M=2$** (`28/0/4`) to **53.1% at $M=3$** (`17/4/11`) and **34.4% at $M=5$** (`11/7/14`). This pattern is limited to the selected functions and algorithm pool.

| Problem (Property) | $M=2$ (Full 7-Algo Verdict) | $M=3$ (5-Algo Verdict) | $M=5$ (5-Algo Verdict) |
|---|---|---|---|
| **WFG1** *(biased, flat)* | **#1 (`12/12` Wins)**; `1.0264` IGD / `1.7730` HV (`12.5s`) | Beats `NSGA2` `+20.9%` HV; #2 behind `SDR-OLS` | No detected IGD difference vs `NSGA2`; beats it by `+26.6%` HV (`1303.33`); #2 behind `SDR-OLS` |
| **WFG4** *(sep., concave)* | **8/12 Wins** (`+beats CE/CGDE`, trails `NSGA2/DNSGA2`) | Trails `NSGA2` & `DNSGA2` (`16.31` vs `19.13` HV) | Trails `NSGA2` & `DNSGA2` (`664.43` vs `883.28` HV); no detected difference vs `SDR-OLS` |
| **WFG6** *(non-separable)* | **10/12 Wins**; #2 behind `CGDE` (`0.0526` vs `0.0302`, **101× slower for CGDE**) | Trails `NSGA2` & `DNSGA2` (`15.51` vs `18.12` HV) | Trails `NSGA2` & `DNSGA2` (`1364.36` vs `1500.76` HV); no detected difference vs `SDR-OLS` |
| **WFG9** *(non-sep., deceptive)* | **#1 (`12/12` Wins)**; OADE had median IGD `0.0347` (`5.2s/run`), versus comparator medians around `0.13–0.64` | No detected IGD difference vs `NSGA2` and `DNSGA2` | **Early 2k-eval lead overtaken at ~5k** (`947.63` vs `1313.48–1337.20` HV) |

Full WFG statistical tables and mechanistic analysis are archived in [`docs/wfg_compact_report.md`](docs/wfg_compact_report.md).

---

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

All figures are archived reproducibly in vector PDF, SVG, and PNG preview under [`results/figures/`](results/figures/) (oversized `.tiff` print files and diagnostic overlay PDFs are local; figure sources and JSON QA records are included):

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

```text
OADE-NSGA-II/
├── algorithms/                 # Baseline competitor implementations
│   ├── ce_moea/                # Continuous Encoding MOEA (continuous-search adaptation)
│   ├── cgde_nsga2/             # Cross-Generation DE (local implementation) NSGA-II
│   └── nsga2_sdr_ols/          # SDR + Opposition and Local Search
├── config/                     # YAML configuration files
│   ├── algorithm_benchmark_v2.yaml  # 7-algorithm ZDT benchmark suite v2
│   ├── dtlz1_4_benchmark.yaml       # DTLZ1-4 suite (M = 2, 3, 5)
│   ├── wfg_compact_benchmark.yaml   # Compact WFG scaling suite (5 fast algos, M=2,3,5)
│   ├── wfg_m2_7algo_benchmark.yaml  # Full 7-algorithm WFG M=2 config
│   ├── restart_confirmation.yaml    # Held-out seed confirmation config
│   └── ablations/              # Component ablation specifications
├── docs/                       # Formal scientific research reports
│   ├── wfg_compact_report.md        # Compact WFG 7-algo M=2 & M=2..5 scaling analysis
│   ├── dtlz1_4_integrated_report.md # Integrated ZDT + DTLZ1-4 analysis
│   ├── benchmark_v2_results_report.md
│   ├── restart_confirmation_report.md
│   ├── ablation_results_report.md
│   └── research_results_report.md
├── results/                    # Transparent benchmark outputs (CSV, Logs)
│   ├── algorithm_benchmark_v2/ # 1,050 ZDT runs, summaries, paired stats
│   ├── dtlz_benchmark/         # 2,520 DTLZ1-4 runs, summaries, paired stats
│   ├── wfg_compact_benchmark/  # 1,800 WFG1/4/6/9 runs (M=2,3,5, 5 fast algos)
│   ├── wfg_m2_7algo_benchmark/ # 840 WFG1/4/6/9 M=2 runs (all 7 algos)
│   ├── restart_confirmation/   # 450 held-out runs
│   └── figures/                # Publication figures (PDF, SVG, PNG, Source CSVs)
├── scripts/                    # High-level runner utilities
│   └── run_benchmark_v2.py
└── src/                        # Core algorithmic & evaluation framework
    ├── oade_nsga2/             # OADE-NSGA-II implementation
    │   ├── algorithm.py        # Main solver class & adaptive restart
    │   ├── operators.py        # DE mutation, SBX, polynomial mutation, OBL
    │   └── selection.py        # Environmental selection, crowding distance
    ├── benchmarking/           # Benchmark protocol, budgeting, statistics
    ├── plotting/               # Built-in benchmark plotters (via main.py)
    ├── sensitivity/            # Parameter sensitivity pipeline
    └── utils/                  # YAML config & CSV utilities
```

Tests, smoke configurations, figure sources, environment lockfiles and JSON QA records are included in the research source. Generated smoke outputs, caches, TIFF rasters and diagnostic overlay PDFs remain local. See [reproducibility guide](docs/reproducibility.md).

---

## 8. Quick Start Guide

### Prerequisites
* Python 3.10+
* Virtual environment with dependencies from `requirements.txt`:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Reproduce Benchmark v2 (ZDT, 7 Algorithms, 1,050 Runs)
```powershell
.venv\Scripts\python.exe main.py benchmark --config config/algorithm_benchmark_v2.yaml --out-dir results/reproduction_zdt_v2
```

### Reproduce DTLZ1–DTLZ4 Benchmark (M = 2, 3, 5; 2,520 Runs)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-dtlz --config config/dtlz1_4_benchmark.yaml --out-dir results/reproduction_dtlz --jobs 8
```

### Reproduce Compact WFG Benchmarks (M = 2, 3, 5 & Full 7-Algo M = 2)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_compact_benchmark.yaml --out-dir results/reproduction_wfg_compact --jobs 8
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_m2_7algo_benchmark.yaml --out-dir results/reproduction_wfg_m2 --jobs 10
```

### Generate Built-in Summary Plots
```powershell
.venv\Scripts\python.exe main.py plot-algorithm-benchmark
.venv\Scripts\python.exe main.py plot-convergence
```

---

## 📜 Citation & Research Reports

If you use OADE-NSGA-II in your research, please refer to the detailed evaluation reports in `docs/`:
* **WFG Compact & M=2 7-Algorithm Report**: [`docs/wfg_compact_report.md`](docs/wfg_compact_report.md)
* **Integrated ZDT + DTLZ1–4 Report**: [`docs/dtlz1_4_integrated_report.md`](docs/dtlz1_4_integrated_report.md)
* **Benchmark v2 Report (ZDT)**: [`docs/benchmark_v2_results_report.md`](docs/benchmark_v2_results_report.md)
* **Restart Confirmation Report**: [`docs/restart_confirmation_report.md`](docs/restart_confirmation_report.md)
* **Component Ablation Report**: [`docs/ablation_results_report.md`](docs/ablation_results_report.md)
