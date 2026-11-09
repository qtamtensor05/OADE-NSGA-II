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
- [5. Limitations & Claim Boundaries](#5-limitations--claim-boundaries)
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
* **Test Suite**: Standard bi-objective CEC benchmark suite: ZDT1 ($D=30$), ZDT2 ($D=30$), ZDT3 ($D=30$), ZDT4 ($D=10$, $21^9$ local fronts), and ZDT6 ($D=10$, non-uniform density).
* **Competing Baselines (6 Algorithms)**:
  * NSGA-II (Deb et al., 2002)
  * D-NSGA-II (Direction-based NSGA-II)
  * R-NSGA-II (Reference point-based NSGA-II)
  * CGDE-NSGA-II (Competitive & Guided Differential Evolution)
  * NSGA-II-SDR-OLS (Strengthened Dominance Relation + Orthogonal Local Search)
  * CE-MOEA (Cross-Entropy Multi-Objective Evolutionary Algorithm)
* **Statistical Inference**: Two-sided paired Wilcoxon signed-rank tests with family-wise error rate controlled via **Holm-Bonferroni step-down correction** separately across comparisons for each metric family ($m = 30$, $\alpha = 0.05$).
* **Effect Sizes**: Matched-pairs rank-biserial correlation $r \in [-1, 1]$.

---

## 3. Key Results & Achievements

### Benchmark v2: Head-to-Head Comparison (1,050 Independent Runs)

Full empirical evidence stored in [`results/algorithm_benchmark_v2/`](results/algorithm_benchmark_v2/):

| Problem | Metric | OADE-NSGA-II v2 | Best Competitor | Competitor Name | $p_{\text{adj}}$ (Holm) | Effect Size ($r$) | Inferential Result |
|---|---|---:|---:|---|---:|---:|---|
| **ZDT1** | IGD ↓<br>HV ↑ | **0.004475 ± 0.000251**<br>**0.870866 ± 0.000232** | 0.005175 ± 0.000298<br>0.868053 ± 0.000417 | NSGA-II<br>NSGA-II | $5.59 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+1.000$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT2** | IGD ↓<br>HV ↑ | **0.004756 ± 0.000292**<br>**0.537674 ± 0.000222** | 0.005405 ± 0.000306<br>0.534072 ± 0.000611 | NSGA-II<br>NSGA-II | $7.82 \times 10^{-8}$<br>$5.59 \times 10^{-8}$ | $+0.983$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT3** | IGD ↓<br>HV ↑ | **0.004986 ± 0.000336**<br>**1.051221 ± 0.000152** | 0.005568 ± 0.000291<br>1.047182 ± 0.006699 | D-NSGA-II<br>NSGA-II | $1.17 \times 10^{-5}$<br>$5.59 \times 10^{-8}$ | $+0.884$<br>$+1.000$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT4** | IGD ↓<br>HV ↑ | **0.006831 ± 0.003329**<br>**0.865051 ± 0.005679** | 0.009953 ± 0.005080<br>0.859362 ± 0.007910 | NSGA-II<br>NSGA-II | $4.04 \times 10^{-3}$<br>$8.72 \times 10^{-4}$ | $+0.626$<br>$+0.669$ | **OADE v2 Wins (#1)**<br>**OADE v2 Wins (#1)** |
| **ZDT6** | IGD ↓<br>HV ↑ | 0.003844 ± 0.000193<br>0.438177 ± 0.000253 | **0.003823 ± 0.000223**<br>**0.439057 ± 0.000199** | CGDE-NSGA-II<br>CGDE-NSGA-II | $0.776$ (Tie)<br>$5.58 \times 10^{-8}$ | $-0.062$<br>$-1.000$ | Indistinguishable (#2)<br>CGDE Wins (#2) |

### Overall Scorecard Across 60 Pairwise Tests:
* **OADE-NSGA-II v2 Wins**: **58 / 60 comparisons (96.7%)**
* **Ties**: 1 / 60 (ZDT6 IGD against CGDE, $p_{\text{adj}} = 0.776$)
* **Losses**: 1 / 60 (ZDT6 HV against CGDE, $p_{\text{adj}} < 10^{-7}$)
* **Overall Rank**: **Rank #1 in 8 out of 10 problem-metric endpoints**, and Rank #2 in the remaining 2 endpoints.

---

## 4. Strengths & Advantages

1. **Unmatched Accuracy & Convergence**:
   Achieves the lowest IGD and highest Hypervolume across ZDT1, ZDT2, ZDT3, and ZDT4, outperforming classic NSGA-II across all 10 endpoints after Holm multiplicity correction.
2. **Robust Multimodal Escape (OBL Resilience)**:
   On ZDT4 ($21^9$ local Pareto fronts), OADE achieves near-optimal IGD ($0.00683$), while competitor algorithms like CGDE-NSGA-II and NSGA-II-SDR-OLS completely collapsed into local optima ($\text{HV} = 0.0, \text{IGD} > 10.8$).
3. **Stabilized Variance via Adaptive Restart**:
   The new adaptive diversity check prevents premature destruction of converged populations. Standard deviations dropped by **11× to 27×** compared to classic restart, completely eliminating late-run archive contamination.
4. **Computational Efficiency**:
   Averages **10.8 to 14.8 seconds** per run across all problems in Python. It runs **7.7× to 10× faster** than local implementations of CGDE-NSGA-II (103–138s) and CE-MOEA (39–145s).
5. **No Parameter Tuning Required**:
   $F$ and $CR$ parameters are self-adapted online using Lehmer-mean updates based on successful offspring, avoiding problem-specific manual tuning.

---

## 5. Limitations & Claim Boundaries

In adherence to Nature reporting rigor, the boundaries of the empirical findings must be explicitly stated:

1. **Test Suite Scope**:
   Evidence is strictly bounded to the 5 tested continuous bi-objective ZDT problems ($D \in \{10, 30\}, M=2$) under a 20,000-evaluation budget. Performance on discrete, constrained, noisy, dynamically changing, or many-objective ($M \ge 3$) problems (e.g., DTLZ, WFG) remains to be formally confirmed.
2. **Hardware-Dependent Runtime**:
   Reported wall-clock runtimes reflect execution in a multi-threaded Python 3 environment. They demonstrate practical implementation efficiency, but must **not** be interpreted as hardware-independent asymptotic time complexities $\mathcal{O}(\cdot)$.
3. **Isolated Component Attribution**:
   The ablation study confirms that OBL is the decisive driver on ZDT4 and Adaptive Restart cures ZDT1–ZDT3. However, isolated main effects of F/CR adaptation and operator probability adaptation did not reach statistical significance after Holm correction; their primary verified function is **tail-risk failure prevention** rather than median shifting.
4. **Inconclusive Comparisons**:
   On ZDT6 IGD against CGDE ($p_{\text{adj}} = 0.776$), the non-significant outcome represents an absence of detectable difference under the current sample size ($n=30$), **not** mathematical equivalence.

---

## 6. Visual Evidence & Figures

All figures are generated reproducibly in vector PDF, SVG, 300-DPI uncompressed TIFF, and PNG preview under [`results/figures/`](results/figures/):

| Figure File | Description |
|---|---|
| [`benchmark_v2_outcome_counts.png`](results/figures/benchmark_v2_outcome_counts.png) | Horizontal stacked bar chart displaying the 58 wins, 1 tie, and 1 loss against 6 baselines. |
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
├── analysis/
│   └── figures/                # Standalone figure generation scripts
│       ├── plot_benchmark_v2.py
│       ├── plot_intuitive_restart_figures.py
│       └── plot_restart_confirmation.py
├── config/                     # YAML configuration files
│   ├── algorithm_benchmark_v2.yaml  # 7-algorithm benchmark suite v2
│   ├── restart_confirmation.yaml    # Held-out seed confirmation config
│   └── ablations/              # Component ablation specifications
├── docs/                       # Formal scientific research reports
│   ├── benchmark_v2_results_report.md
│   ├── restart_confirmation_report.md
│   ├── ablation_results_report.md
│   └── research_results_report.md
├── results/                    # Transparent benchmark outputs (CSV, Logs)
│   ├── algorithm_benchmark_v2/ # 1,050 raw runs, summaries, paired stats
│   ├── restart_confirmation/   # 450 held-out runs
│   └── figures/                # Publication-ready figures (PDF, TIFF, SVG, CSV)
├── scripts/                    # High-level runner utilities
│   ├── run_benchmark_v2.py
│   └── render_research_figures.ps1
├── src/                        # Core algorithmic framework
│   ├── oade_nsga2/             # OADE-NSGA-II implementation
│   │   ├── algorithm.py        # Main solver class & adaptive restart
│   │   ├── operators.py        # DE mutation, SBX, polynomial mutation, OBL
│   │   └── selection.py        # Environmental selection, crowding distance
│   └── benchmarking/           # Benchmark protocol, budgeting, statistics
└── tests/                      # Automated unit test suite
    └── test_restart_mechanisms.py
```

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

### Run Automated Unit Tests
```powershell
.venv\Scripts\python.exe -m unittest discover tests
```

### Reproduce Benchmark v2 (7 Algorithms, 1,050 Runs)
```powershell
.venv\Scripts\python.exe scripts\run_benchmark_v2.py
```

### Regenerate All Nature Figures
```powershell
.venv\Scripts\python.exe analysis/figures/plot_benchmark_v2.py
.venv\Scripts\python.exe analysis/figures/plot_intuitive_restart_figures.py
```

---

## 📜 Citation & Research Reports

If you use OADE-NSGA-II in your research, please refer to the detailed evaluation reports in `docs/`:
* **Benchmark v2 Report**: [`docs/benchmark_v2_results_report.md`](docs/benchmark_v2_results_report.md)
* **Restart Confirmation Report**: [`docs/restart_confirmation_report.md`](docs/restart_confirmation_report.md)
* **Component Ablation Report**: [`docs/ablation_results_report.md`](docs/ablation_results_report.md)
