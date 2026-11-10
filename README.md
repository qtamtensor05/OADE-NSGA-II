# OADE-NSGA-II: Adaptive Opposition-Based Differential Evolution NSGA-II

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/Benchmark-Fixed--Budget%2020k-orange.svg)](#experimental-protocol)
[![Nature Standards](https://img.shields.io/badge/Standards-Nature%20Portfolio-red.svg)](#statistical-discipline)

An improved multi-objective evolutionary algorithm integrating **Opposition-Based Learning (OBL)**, **Neighborhood-Directed Adaptive Differential Evolution (DE)**, **SaDE-style parameter adaptation**, and an **Adaptive Diversity-Aware Restart** mechanism into the NSGA-II framework.

---

## 📌 Table of Contents
- [1. Overview & Key Innovations](#1-overview--key-innovations)
- [2. Experimental Protocol & Statistical Discipline](#2-experimental-protocol--statistical-discipline)
- [3. Key Results & Achievements](#3-key-results--achievements)
- [4. Strengths & Advantages](#4-strengths--advantages)
- [5. Weaknesses, Limitations & Claim Boundaries](#5-weaknesses-limitations--claim-boundaries)
- [6. Visual Evidence & Figures](#6-visual-evidence--figures)
- [7. Project Structure & Reproducibility](#7-project-structure--reproducibility)
- [8. Quick Start Guide](#8-quick-start-guide)

---

## 1. Overview & Key Innovations

Standard NSGA-II (Deb et al., 2002) frequently suffers from premature convergence on multimodal landscapes and slow lateral exploration on complex Pareto fronts. **OADE-NSGA-II** addresses these fundamental limitations via four complementary mechanisms:

1. **OBL + Sobol Quasi-Random Initialization**: Explores both candidates and their opposite spatial points at generation zero, guaranteeing high initial spatial dispersion.
2. **Periodic Opposition Injection**: Injects opposite candidates every 10 generations to continuously escape local basins of attraction.
3. **Neighborhood-Directed DE Mutation (DE/current-to-pbest/1)**: Guides mutation along high-density neighborhood vectors rather than purely random pairings, balancing exploration and exploitation.
4. **Adaptive Diversity-Aware Restart (v2 Upgrade)**: Replaces classic naive stagnation triggers with a dual-condition safeguard:
   * **Stagnation detection**: Tracks ideal point progress ($\|\Delta \mathbf{z}^*\| < 10^{-4}$).
   * **Diversity collapse verification**: Checks whether decision-space variance $\max_j \sigma_j < 0.02$ or objective spread $< 10^{-3}$.
   * **Conservative renewal**: Preserves 80% of elite solutions, perturbing the remaining 20% via local OBL and Gaussian mutations, while softly decaying adaptation history ($\mu_F, \mu_{CR}$).

---

## 2. Experimental Protocol & Statistical Discipline

All experiments strictly follow the reporting and replication guidelines of **Nature Machine Intelligence**:

* **Independent Experimental Unit**: One complete stochastic run ($n = 30$ paired runs per problem-metric endpoint).
* **Strict Evaluation Budget**: Fixed at exactly 20,000 function evaluations per run (verified budget utilization $> 99.7\%$).
* **Paired Design**: All competing algorithms start from the exact same initial population and pseudo-random seed on each run.
* **Test Suites (21 Balanced Benchmark Configurations, 6,210 Main Benchmark Runs)**:
  * **Bi-objective ZDT (`1,050` runs, 7 algorithms)**: ZDT1 ($D=30$), ZDT2 ($D=30$), ZDT3 ($D=30$), ZDT4 ($D=10$, $21^9$ local fronts), and ZDT6 ($D=10$, non-uniform density).
  * **Multi-/Many-objective DTLZ1–DTLZ4 (`2,520` runs, 7 algorithms)**: DTLZ1 ($M \in \{2,3,5\}, D \in \{6,7,9\}$) and DTLZ2–DTLZ4 ($M \in \{2,3,5\}, D \in \{11,12,14\}$).
  * **Bi-objective WFG (`840` runs, 7 algorithms)**: `WFG1, WFG4, WFG6, WFG9` ($M=2, D=24, k=4$) testing bias/flatness, separable concave multimodality, non-separability, and deceptive traps.
  * **Compact WFG Scaling (`1,800` runs, 5 fast algorithms)**: `WFG1, WFG4, WFG6, WFG9` ($M \in \{2,3,5\}, D=24, k \in \{4,8\}$) across `OADE_NSGAII`, `NSGA2`, `DNSGA2`, `RNSGA2`, and `NSGAII_SDR_OLS`.
* **Competing Baselines (6 Algorithms)**:
  * NSGA-II (Deb et al., 2002)
  * D-NSGA-II (Direction-based NSGA-II)
  * R-NSGA-II (Reference point-based NSGA-II)
  * CGDE-NSGA-II (Competitive & Guided Differential Evolution)
  * NSGA-II-SDR-OLS (Strengthened Dominance Relation + Orthogonal Local Search)
  * CE-MOEA (Cross-Entropy Multi-Objective Evolutionary Algorithm)
* **Statistical Inference**: Two-sided paired Wilcoxon signed-rank tests with family-wise error rate controlled via **Holm-Bonferroni step-down correction** separately per metric family ($m = 30$ for ZDT; $m = 72$ for DTLZ1–4; $m = 24$ for WFG $M=2$ 7-algo; $m = 48$ for Compact WFG 5-algo; $\alpha = 0.05$).
* **Effect Sizes**: Matched-pairs rank-biserial correlation $r \in [-1, 1]$.

---

## 3. Key Results & Achievements

### Combined 7-Algorithm Scorecard (ZDT + DTLZ1–DTLZ4 = 204 Pairwise Tests, 3,570 Runs)

* **Combined Outcome (204 Holm-Adjusted Comparisons)**: **149 Wins (73.0%) / 41 Ties (20.1%) / 14 Losses (6.9%)** across 3,570 runs (`OADE-NSGA-II v2`: **510/510 valid runs**, 0 collapsed fronts).
  * **ZDT Benchmark v2 (60 comparisons)**: **58 Wins (96.7%) / 1 Tie / 1 Loss** (Rank #1 on 8/10 endpoints).
  * **DTLZ1–DTLZ4 Benchmark (144 comparisons)**: **91 Wins (63.2%) / 40 Ties (27.8%) / 13 Losses (9.0%)** (Rank #1 on 8/12 IGD medians and 7/12 HV means; zero losses at $M=5$).
* **Zero-Loss Records Across All 17 Problems**: OADE-NSGA-II v2 never lost a single Holm-corrected comparison against **`CE-MOEA`** (23–11–0), **`NSGA-II-SDR-OLS`** (30–4–0), or **`R-NSGA-II`** (31–3–0), while leading **`NSGA-II`** (22–7–5), **`D-NSGA-II`** (22–7–5), and **`CGDE-NSGA-II`** (21–9–4).

### Bi-Objective ZDT Benchmark v2 (`results/algorithm_benchmark_v2/`, 1,050 Runs)

| Problem | Metric | OADE-NSGA-II v2 | Best Competitor | Competitor Name | $p_{\text{adj}}$ (Holm) | Effect Size ($r$) | Inferential Result |
|---|---|---:|---:|---|---:|---:|---|
| **ZDT1** | IGD ↓<br>HV ↑ | **0.004475 ± 0.000251**<br>**0.870866 ± 0.000232** | 0.005175 ± 0.000298<br>0.868053 ± 0.000417 | NSGA-II<br>NSGA-II | $5.59 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+1.000$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT2** | IGD ↓<br>HV ↑ | **0.004756 ± 0.000292**<br>**0.537674 ± 0.000222** | 0.005405 ± 0.000306<br>0.534072 ± 0.000611 | NSGA-II<br>NSGA-II | $7.82 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+0.983$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT3** | IGD ↓<br>HV ↑ | **0.004986 ± 0.000336**<br>**1.051221 ± 0.000152** | 0.005568 ± 0.000291<br>1.047182 ± 0.006699 | D-NSGA-II<br>NSGA-II | $1.17 \times 10^{-5}$<br>$5.59 \times 10^{-8}$ | $+0.884$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT4** | IGD ↓<br>HV ↑ | **0.006831 ± 0.003329**<br>**0.865051 ± 0.005679** | 0.009953 ± 0.005080<br>0.859362 ± 0.007910 | NSGA-II<br>NSGA-II | $4.04 \times 10^{-3}$<br>$8.72 \times 10^{-4}$ | $+0.626$<br>$+0.669$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT6** | IGD ↓<br>HV ↑ | 0.003844 ± 0.000193<br>0.438177 ± 0.000253 | **0.003823 ± 0.000223**<br>**0.439057 ± 0.000199** | CGDE-NSGA-II<br>CGDE-NSGA-II | $0.776$ (Tie)<br>$5.58 \times 10^{-8}$ | $-0.062$<br>$-1.000$ | Indistinguishable (#2)<br>CGDE Wins (#2) |

### Multi-/Many-Objective DTLZ1–DTLZ4 Highlights (`results/dtlz_benchmark/`, 2,520 Runs)

| Problem Family | $M=2$ Outcome | $M=3$ Outcome | $M=5$ Outcome |
|---|---|---|---|
| **DTLZ1** (Multimodal linear) | **6/6 IGD & HV Wins** (`0.0022` med IGD) | **6/6 Wins ($r = +1.000, W=0$)**; `0.0292` vs NSGA-II `0.0967` | **6/6 IGD Wins** (`0.8972` vs `40.17` NSGA-II); **13/30 HV>0** vs **0/30** all baselines |
| **DTLZ2** (Unimodal sphere) | **IGD Tie** vs NSGA-II (`0.0050`); NSGA-II +0.11% HV | **Trails SBX & CGDE** (`0.0762` vs `0.0685`–`0.0720` IGD) | **Rank #1** (`0.4214` IGD, `0.4517` HV); beats D-NSGA-II, CGDE, CE-MOEA, R-NSGA-II, SDR-OLS |
| **DTLZ3** (Hard multimodal sphere) | **6/6 IGD Wins** (`1.0708` med, **11/30 HV>0**) | **6/6 IGD Wins ($r = +1.000$)**; `2.5460` vs `14.1763`–`108.7107` | **5/6 IGD Wins** (`72.7081` vs `108.3939`–`258.9448`; ties SDR-OLS); **0/30 HV>0** all algorithms |
| **DTLZ4** ($\alpha=100$ biased sphere) | **0/30 collapses** (`0.0051` med); NSGA-II collapses **11/30** (`0.2753` mean) | **Trails SBX & CGDE** (`0.0780` vs `0.0686`–`0.0704` IGD) | **Rank #1 IGD (`0.3746`, 0/30 collapses)**; ties CE-MOEA/CGDE at **23.8× faster speed**; NSGA-II/D-NSGA-II collapse **30/30** (`HV = 0.0205`/`0.0422`) |

Full tables (Median [IQR], Mean ± SD, effect sizes) are archived in [`docs/dtlz1_4_integrated_report.md`](docs/dtlz1_4_integrated_report.md).

### WFG Suite Highlights (`results/wfg_m2_7algo_benchmark/` & `results/wfg_compact_benchmark/`, 2,640 Runs)

* **Full 7-Algorithm `WFG M=2` Scorecard (48 Holm tests, 840 runs, 0 invalid)**: **`42 Wins (87.5%) / 0 Ties / 6 Losses (12.5%)`**, Ranked **#1 overall (`1.75` mean rank vs `NSGA2` `3.12`, `CGDE` `3.25`, `CE_MOEA` `3.50`)** — zero losses vs `CE-MOEA` (`8–0–0`), `NSGA-II-SDR-OLS` (`8–0–0`), and `R-NSGA-II` (`8–0–0`).
  * **Bi-objective ZDT + WFG 7-Algo Combined (108 tests, 9 problems)**: **`100 Wins (92.6%) / 1 Tie / 7 Losses`**!
* **5-Fast-Algorithm `WFG M = 2 -> 3 -> 5` Scaling (96 Holm tests, 1,800 runs, 0 invalid)**: **`56 Wins (58.3%) / 11 Ties (11.5%) / 29 Losses (30.2%)`** — exposing a sharp dimensional phase shift from **`87.5%` wins at $M=2$** (`28/0/4`) $\to$ **`53.1%` at $M=3$** (`17/4/11`) $\to$ **`34.4%` at $M=5$** (`11/7/14`).

| Problem (Property) | $M=2$ (Full 7-Algo Verdict) | $M=3$ (5-Algo Verdict) | $M=5$ (5-Algo Verdict) |
|---|---|---|---|
| **WFG1** *(biased, flat)* | **#1 (`12/12` Wins)**; `1.0264` IGD / `1.7730` HV (`12.5s`) | Beats `NSGA2` `+20.9%` HV; #2 behind `SDR-OLS` | Ties `NSGA2` IGD, beats `NSGA2` `+26.6%` HV (`1303.33`); #2 behind `SDR-OLS` |
| **WFG4** *(sep., concave)* | **8/12 Wins** (`+beats CE/CGDE`, trails `NSGA2/DNSGA2`) | Trails `NSGA2` & `DNSGA2` (`16.31` vs `19.13` HV) | Trails `NSGA2` & `DNSGA2` (`664.43` vs `883.28` HV); ties `SDR-OLS` |
| **WFG6** *(non-separable)* | **10/12 Wins**; #2 behind `CGDE` (`0.0526` vs `0.0302`, **101× faster**) | Trails `NSGA2` & `DNSGA2` (`15.51` vs `18.12` HV) | Trails `NSGA2` & `DNSGA2` (`1364.36` vs `1500.76` HV); ties `SDR-OLS` |
| **WFG9** *(non-sep., deceptive)* | **#1 (`12/12` Wins)**; sole solver escaping `~0.13` trap (`0.0347` IGD in `5.2s`, `~84–88×` faster than `CE/CGDE`) | **Statistical Tie** vs `NSGA2` & `DNSGA2` (`0.3372` IGD) | **Early 2k-eval lead overtaken at ~5k** (`947.63` vs `1313.48–1337.20` HV) |

Full WFG statistical tables and mechanistic analysis are archived in [`docs/wfg_compact_report.md`](docs/wfg_compact_report.md).

---

## 4. Strengths & Advantages

1. **Multimodal & Deceptive Escape Across 2–5 Objectives**:
   OBL initialization and periodic opposition injection break local-optimum traps on ZDT4 ($21^9$ fronts), DTLZ1 (18/18 IGD wins), DTLZ3 (17/18 IGD wins), and non-separable deceptive **WFG9 ($M=2$)**—where all six comparators (`NSGA-II`, `D-NSGA-II`, `CGDE-NSGA-II`, `CE-MOEA`, `SDR-OLS`, `R-NSGA-II`) stall around IGD `0.128–0.640` while OADE reaches `0.0347` in `5.2s/run`.
2. **Immunity to Severe Coordinate Bias (DTLZ4 Collapse Resistance)**:
   While standard SBX algorithms suffer severe corner collapse on DTLZ4 (36.7% failure for `NSGA-II` at $M=2$; **100% failure** for both `NSGA-II` and `D-NSGA-II` at $M=5$), OADE-NSGA-II v2 logged **0 collapses across all 90 DTLZ4 runs** and **100% valid fronts** across ZDT (`150/150`), DTLZ1–4 (`360/360`), and WFG (`360/360`) (vs 15 `collapsed_front` failures in `SDR-OLS` and 3 in `CGDE` on DTLZ1–4, plus severe `M=2` WFG front shrinkage down to 20.7 points in `SDR-OLS`).
3. **Stabilized Variance via Adaptive Restart**:
   The adaptive diversity check prevents premature destruction of converged populations. Standard deviations on ZDT1–ZDT3 dropped by **11× to 27×** compared to classic restart, eliminating late-run archive contamination and boosting ZDT win rate from 39/60 (v1) to **58/60 (v2)**.
4. **Computational Efficiency**:
   Averages **10.8–14.8s/run** on ZDT, **2.74–3.04s/run** on DTLZ4, and **4.42–12.53s/run** on `WFG M=2` (`OMP_NUM_THREADS=1`), running **7.7× to 101× faster** than local implementations of `CGDE-NSGA-II` and `CE-MOEA`.
5. **Online Parameter Self-Adaptation**:
   $F$ and $CR$ parameters adapt online via Lehmer-mean updates from successful offspring, avoiding problem-specific manual tuning.

---

## 5. Weaknesses, Limitations & Claim Boundaries

In adherence to Nature reporting rigor, empirically observed weaknesses and boundaries must be stated explicitly:

1. **Confirmed Deficit on Smooth/Concave Multi-Objective Fronts (`dtlz2_m3`, `dtlz4_m3`, `WFG4`, and Scaled `WFG6/9` at $M \ge 3$)**:
   When local traps are absent or SBX resolves coupling at higher objective dimension, OADE-NSGA-II v2 trails SBX-based `NSGA-II` / `D-NSGA-II` on `dtlz2_m3`, `dtlz4_m3`, separable concave `WFG4` ($M=2,3,5$), `WFG6` ($M=3,5$), and `WFG9` ($M=5$), while `CGDE-NSGA-II` wins bi-objective non-separable `wfg6_m2` (`0.0302` vs `0.0526` IGD) at **101× runtime cost** (`448.1s` vs `4.4s`). Source inspection attributes late-budget 5D stagnation (`wfg9_m5` peaking around 16k evals) to three addressable mechanisms: `n_neighbors: 5` YAML override, `prob_de` updating from generation rate rather than Rank-1 survival rate, and unbounded crowding boundaries on `[0, 2M]` scaled fronts.
2. **Crowding-Distance Saturation at $M=5$ Under Extreme Multimodality (`dtlz1_m5`, `dtlz3_m5`)**:
   Retaining NSGA-II crowding-distance selection limits convergence pressure at 5 objectives under a 20,000-evaluation cap: 17/30 runs on `dtlz1_m5` ($\text{IGD}_{\text{med}} = 0.8972$, right-skewed max `24.71`) and 30/30 runs on `dtlz3_m5` fail to reach positive Hypervolume (`HV = 0.0`).
3. **Remaining Test Suite Boundaries**:
   Current empirical evidence covers **ZDT1–4, ZDT6** ($M=2$), **DTLZ1–4** ($M \in \{2, 3, 5\}$), **WFG1, WFG4, WFG6, WFG9** ($M=2$ with all 7 solvers; $M \in \{2,3,5\}$ with the 5 fast solvers). Performance on **degenerate/disconnected DTLZ5–7**, remaining WFG suites (`WFG2, WFG3, WFG5, WFG7, WFG8`), `CE_MOEA`/`CGDE_NSGAII` at $M=3,5$ WFG, constrained MOPs, and discrete problems remains untested.
4. **Hardware-Dependent Runtime**:
   Reported wall-clock runtimes reflect Python execution overhead and BLAS thread settings (`OMP_NUM_THREADS=1` cut DTLZ4 runtimes ~3× vs unpinned DTLZ1–3 batches), and must **not** be interpreted as hardware-independent asymptotic complexities $\mathcal{O}(\cdot)$.
5. **Isolated Component Attribution & Inconclusive Tests**:
   Ablation confirms OBL drives ZDT4 and Adaptive Restart cures ZDT1–ZDT3, whereas F/CR and operator probability adaptation act primarily as **tail-risk safeguards**. Non-significant comparisons (e.g., `ZDT6` IGD vs CGDE, `dtlz4_m5` vs CE-MOEA/CGDE) denote absence of statistically detectable difference at $n=30$, **not** mathematical equivalence.

---

## 6. Visual Evidence & Figures

All figures are archived reproducibly in vector PDF, SVG, and PNG preview under [`results/figures/`](results/figures/) (oversized `.tiff` print files, QA audit overlays, and standalone figure-helper scripts are excluded via `.gitignore`):

| Figure File | Description |
|---|---|
| [`integrated_7algo_landscape.png`](results/figures/integrated_7algo_landscape.png) | **Multi-panel overview**: 17-problem rank-biserial effect-size matrix (`a`), 204-test outcome ledger (`b`), and 34-endpoint mean-rank vs runtime Pareto trade-off (`c`). |
| [`dtlz1_4_scaling_diagnosis.png`](results/figures/dtlz1_4_scaling_diagnosis.png) | **2×2 DTLZ scaling grid ($M=2,3,5$)**: Multimodal escape on DTLZ1/3 (`a, b`), 3-objective spherical deficit on DTLZ2 (`c`), and DTLZ4 corner-collapse immunity (`d`). |
| [`wfg_m2_7algo_profile.png`](results/figures/wfg_m2_7algo_profile.png) | **7-Algorithm WFG $M=2$ validation**: 48-test IGD/HV effect heatmap (`a`), raw-seed `WFG9` deceptive trap escape (`b`), and 8-endpoint rank vs runtime Pareto front (`c`). |
| [`wfg_scaling_diagnosis.png`](results/figures/wfg_scaling_diagnosis.png) | **2×2 WFG scaling grid ($M=2 \to 3 \to 5$)**: 5-algo Holm outcome transition (`a`), paired `OADE/NSGA2` IGD ratios (`b`), and `wfg1_m5` / `wfg9_m5` HV convergence (`c, d`). |
| [`benchmark_v2_outcome_counts.png`](results/figures/benchmark_v2_outcome_counts.png) | Horizontal stacked bar chart displaying the 58 wins, 1 tie, and 1 loss on ZDT v2 against 6 baselines. |
| [`benchmark_v2_v1_vs_v2_delta.png`](results/figures/benchmark_v2_v1_vs_v2_delta.png) | Direct IGD reduction from OADE v1 to OADE v2 across all 5 ZDT problems (-24.5% to -40.0%). |
| [`restart_direct_comparison.png`](results/figures/restart_direct_comparison.png) | Grouped boxplots comparing Old Restart, No Restart, and New Restart side-by-side with overlaid raw seeds. |
| [`restart_convergence.png`](results/figures/restart_convergence.png) | Within-budget convergence trajectories (Median IGD + IQR shaded bands) over 20,000 evaluations. |
| [`restart_confirmation_paired.png`](results/figures/restart_confirmation_paired.png) | Paired percentage improvement distribution on 30 held-out seeds ($1000 \dots 1029$). |

Full quality assurance audits and font-size checks are logged in [`results/figures/figure_qa.md`](results/figures/figure_qa.md).

---

## 7. Project Structure & Reproducibility

```text
OADE-NSGA-II/
├── algorithms/                 # Baseline competitor implementations
│   ├── ce_moea/                # Cross-Entropy MOEA
│   ├── cgde_nsga2/             # Competitive & Guided DE NSGA-II
│   └── nsga2_sdr_ols/          # SDR + Orthogonal Local Search
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

*(Note: local unit tests `tests/`, smoke configurations `config/smoke_*.yaml`, standalone plotting scripts `analysis/`, 600-DPI `.tiff` rasters, and figure QA intermediates are kept locally via `.gitignore`.)*

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
.venv\Scripts\python.exe scripts\run_benchmark_v2.py
```

### Reproduce DTLZ1–DTLZ4 Benchmark (M = 2, 3, 5; 2,520 Runs)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-dtlz --config config/dtlz1_4_benchmark.yaml --jobs 8
```

### Reproduce Compact WFG Benchmarks (M = 2, 3, 5 & Full 7-Algo M = 2)
```powershell
$env:OMP_NUM_THREADS=1; $env:OPENBLAS_NUM_THREADS=1; $env:MKL_NUM_THREADS=1
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_compact_benchmark.yaml --jobs 8
.venv\Scripts\python.exe main.py benchmark-wfg --config config/wfg_m2_7algo_benchmark.yaml --jobs 10
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
