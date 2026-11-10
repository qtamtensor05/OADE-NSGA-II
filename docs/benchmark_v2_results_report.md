# OADE-NSGA-II: Fixed-Budget Benchmark v2 Results Report

## 1. Executive Summary

This report evaluates the **Benchmark v2** results stored in `results/algorithm_benchmark_v2`. In this iteration, **OADE-NSGA-II v2** uses the **Adaptive Diversity-Aware Restart** configuration (`restart_mode: "adaptive"`, `restart_elite_ratio: 0.80`, `diversity_threshold: 0.02`), alongside Opposition-Based Learning (OBL) and adaptive operators. This benchmark compares complete configurations; it does not isolate the restart policy's contribution.

The benchmark schedules 1,050 runs across five bi-objective ZDT problems and pairs OADE-NSGA-II with six baseline implementations: NSGA-II, CGDE-NSGA-II, NSGA-II-SDR-OLS, CE-MOEA, D-NSGA-II, and R-NSGA-II. Each configuration uses the same 30 seeds ($42 \dots 71$) and a cap of 20,000 objective evaluations; actual evaluation counts can be lower.

### Main findings
1. **More favorable pairwise outcomes in the v2 benchmark**:
   * In the v1 result set (classic restart), OADE-NSGA-II had 39 significant wins, 20 comparisons with no detected difference, and 1 significant loss among 60 comparisons.
   * In v2 (adaptive restart), it had 58 significant wins, 1 comparison with no detected difference, and 1 significant loss. These are counts from two separately analysed benchmark versions; they are not a direct statistical test of v2 against v1.
2. **ZDT2 comparison with NSGA-II**:
   * In v2, OADE-NSGA-II had lower IGD and higher HV than NSGA-II, with Holm-adjusted $p = 7.82 \times 10^{-8}$ and $p = 5.58 \times 10^{-8}$, respectively, within the configured per-metric family.
3. **Descriptive rank across endpoints**:
   * OADE-NSGA-II v2 had the best mean on 8 of 10 problem-metric endpoints. On ZDT6, CGDE-NSGA-II had the best mean for both metrics; the IGD comparison was not significant after correction, while the HV comparison favored CGDE-NSGA-II.

---

## 2. Experimental Design and Statistical Discipline

| Design Element | Specification |
|---|---|
| **Problems** | ZDT1 ($D=30$), ZDT2 ($D=30$), ZDT3 ($D=30$), ZDT4 ($D=10$), and ZDT6 ($D=10$) |
| **Compared Algorithms (7)** | 1. OADE-NSGA-II v2 (Adaptive Restart)<br>2. NSGA-II (Deb et al., 2002)<br>3. D-NSGA-II (Direction-based NSGA-II)<br>4. R-NSGA-II (Reference point NSGA-II)<br>5. CGDE-NSGA-II (Competitive & Guided DE)<br>6. NSGA-II-SDR-OLS (Strengthened Dominance Relation + Orthogonal Local Search)<br>7. CE-MOEA (Cross-Entropy MOEA) |
| **Replication Unit** | One stochastic run ($n = 30$ paired runs per comparison, $N = 1,050$ total observations) |
| **Seed Range** | Seeds 42–71 (exact paired seed correspondence across all 7 algorithms) |
| **Evaluation Budget** | Capped at 20,000 objective evaluations per run; actual use can be slightly lower when a generation would cross the cap |
| **Validation Diagnostics** | 1,050 valid runs (`ok`); 0 collapsed fronts; 0 out-of-bounds violations |
| **Hypothesis Testing** | Two-sided paired Wilcoxon signed-rank test |
| **Multiplicity Control** | Holm-Bonferroni step-down adjustment separately across the 30 comparisons per metric |
| **Effect Size** | Matched-pairs rank-biserial effect $r \in [-1, 1]$; positive values denote superiority of OADE-NSGA-II v2 |

---

## 3. Visual Evidence

### 3.1 Pairwise Outcome Counts Across 60 Comparisons
![Benchmark v2 Outcome Counts](../results/figures/benchmark_v2_outcome_counts.png)

*Figure 1: Pairwise Wilcoxon outcomes after the configured Holm correction for OADE-NSGA-II v2 against six comparators across 10 problem-metric endpoints. OADE-NSGA-II v2 had 58 significant wins, 1 comparison with no detected difference, and 1 significant loss. The adjustment is applied separately within each metric family; “no detected difference” does not establish equivalence.*

### 3.2 Generational Leap: OADE v1 vs OADE v2
![OADE v1 vs v2 Delta](../results/figures/benchmark_v2_v1_vs_v2_delta.png)

*Figure 2: Descriptive mean IGD comparison between OADE v1 (classic restart) and OADE v2 (adaptive restart). Mean IGD was 24.5%–40.0% lower on ZDT1–ZDT3 in v2. The figure does not report a direct paired inferential comparison between v1 and v2, so these deltas should be read descriptively.*

---

## 4. Descriptive Results

Values are reported as Mean ± Sample Standard Deviation across 30 independent runs. Bold indicates the best-performing algorithm on that metric.

| Problem | Algorithm | IGD ↓ | HV ↑ | Mean Runtime (s) |
|---|---|---:|---:|---:|
| **ZDT1** | **OADE-NSGA-II v2** | **0.004475 ± 0.000251** | **0.870866 ± 0.000232** | 14.50 |
| | NSGA-II | 0.005175 ± 0.000298 | 0.868053 ± 0.000417 | 0.93 |
| | D-NSGA-II | 0.005633 ± 0.000423 | 0.867066 ± 0.000685 | 0.85 |
| | R-NSGA-II | 0.632213 ± 0.081377 | 0.350416 ± 0.086453 | 1.23 |
| | CGDE-NSGA-II | 0.007433 ± 0.000527 | 0.863362 ± 0.000969 | 39.56 |
| | NSGA-II-SDR-OLS | 0.015633 ± 0.019704 | 0.858421 ± 0.014846 | 1.05 |
| | CE-MOEA | 0.006908 ± 0.000874 | 0.864472 ± 0.001779 | 38.82 |
| **ZDT2** | **OADE-NSGA-II v2** | **0.004756 ± 0.000292** | **0.537674 ± 0.000222** | 14.78 |
| | NSGA-II | 0.005405 ± 0.000306 | 0.534072 ± 0.000611 | 1.97 |
| | D-NSGA-II | 0.005881 ± 0.000392 | 0.532697 ± 0.000974 | 1.84 |
| | R-NSGA-II | 0.520240 ± 0.030498 | 0.121961 ± 0.008550 | 2.69 |
| | CGDE-NSGA-II | 0.006815 ± 0.000510 | 0.530572 ± 0.001170 | 136.06 |
| | NSGA-II-SDR-OLS | 0.050319 ± 0.152326 | 0.499634 ± 0.106117 | 3.48 |
| | CE-MOEA | 0.007477 ± 0.000980 | 0.529670 ± 0.001905 | 144.51 |
| **ZDT3** | **OADE-NSGA-II v2** | **0.004986 ± 0.000336** | **1.051221 ± 0.000152** | 10.79 |
| | NSGA-II | 0.007191 ± 0.010231 | 1.047182 ± 0.006699 | 1.69 |
| | D-NSGA-II | 0.005568 ± 0.000291 | 1.046953 ± 0.000680 | 1.63 |
| | R-NSGA-II | 0.729365 ± 0.061686 | 0.409883 ± 0.051660 | 2.41 |
| | CGDE-NSGA-II | 0.008262 ± 0.000984 | 1.035047 ± 0.003604 | 108.59 |
| | NSGA-II-SDR-OLS | 0.018648 ± 0.002970 | 1.035815 ± 0.004358 | 2.53 |
| | CE-MOEA | 0.008561 ± 0.001533 | 1.034400 ± 0.005116 | 100.30 |
| **ZDT4** | **OADE-NSGA-II v2** | **0.006831 ± 0.003329** | **0.865051 ± 0.005679** | 11.98 |
| | NSGA-II | 0.009953 ± 0.005080 | 0.859362 ± 0.007910 | 2.21 |
| | D-NSGA-II | 0.019973 ± 0.027370 | 0.846750 ± 0.036867 | 2.10 |
| | R-NSGA-II | 0.637785 ± 0.167283 | 0.335380 ± 0.160439 | 3.06 |
| | CGDE-NSGA-II | 12.171576 ± 2.800419 | 0.000000 ± 0.000000 | 138.42 |
| | NSGA-II-SDR-OLS | 10.891407 ± 6.777696 | 0.000000 ± 0.000000 | 2.37 |
| | CE-MOEA | 0.357214 ± 0.234331 | 0.409725 ± 0.227870 | 129.20 |
| **ZDT6** | OADE-NSGA-II v2 | 0.003844 ± 0.000193 | 0.438177 ± 0.000253 | 13.34 |
| | NSGA-II | 0.016368 ± 0.002011 | 0.417891 ± 0.002872 | 2.06 |
| | D-NSGA-II | 0.022588 ± 0.002794 | 0.408917 ± 0.003997 | 2.02 |
| | R-NSGA-II | 0.189393 ± 0.092652 | 0.264148 ± 0.068359 | 2.79 |
| | **CGDE-NSGA-II** | **0.003823 ± 0.000223** | **0.439057 ± 0.000199** | 103.07 |
| | NSGA-II-SDR-OLS | 0.139446 ± 0.082748 | 0.282923 ± 0.058962 | 2.12 |
| | CE-MOEA | 0.004957 ± 0.000336 | 0.437794 ± 0.000360 | 101.56 |

---

## 5. Inferential Statistics (Paired Wilcoxon Signed-Rank Tests)

All comparisons evaluate OADE-NSGA-II v2 as the reference ($n = 30$ paired runs). Multiplicity is controlled via Holm step-down adjustment separately across the 30 comparisons per metric family ($\alpha = 0.05$).

### Summary of Corrected Outcomes:
* **Against NSGA-II**: OADE-NSGA-II v2 wins **10 out of 10 endpoints** (all $p_{\text{adj}} < 0.005$, rank-biserial $r$ up to $1.000$).
* **Against D-NSGA-II**: OADE-NSGA-II v2 wins **10 out of 10 endpoints** (all $p_{\text{adj}} < 0.0005$).
* **Against R-NSGA-II**: OADE-NSGA-II v2 wins **10 out of 10 endpoints** (all $p_{\text{adj}} < 10^{-7}$).
* **Against CE-MOEA**: OADE-NSGA-II v2 wins **10 out of 10 endpoints** (all $p_{\text{adj}} < 10^{-7}$).
* **Against SDR-OLS**: OADE-NSGA-II v2 wins **10 out of 10 endpoints** (all $p_{\text{adj}} < 10^{-7}$).
* **Against CGDE-NSGA-II**:
  * ZDT1: OADE wins both IGD and HV ($p_{\text{adj}} < 10^{-7}$).
  * ZDT2: OADE wins both IGD and HV ($p_{\text{adj}} < 10^{-7}$).
  * ZDT3: OADE wins both IGD and HV ($p_{\text{adj}} < 10^{-7}$).
  * ZDT4: OADE wins both IGD and HV ($p_{\text{adj}} < 10^{-7}$, CGDE failed with HV = 0).
  * ZDT6: no difference detected on IGD ($p_{\text{adj}} = 0.776$); CGDE is significantly better on HV ($p_{\text{adj}} = 5.58 \times 10^{-8}$).
  * Total against CGDE: **8 significant wins, 1 comparison with no detected difference, 1 significant loss**.

---

## 6. Computational Cost and Efficiency Analysis

* **OADE-NSGA-II v2 Runtime**: Averaged **10.8 to 14.8 seconds** per run across the five problems.
* **Heavy Competitors**: Local Python implementations of CGDE-NSGA-II and CE-MOEA required **39.6 to 144.5 seconds** per run (up to 10× slower than OADE).
* **Lightweight Competitors**: C-optimized pymoo implementations (NSGA-II, D-NSGA-II) required 0.8 to 2.2 seconds.
* **Observed quality-runtime trade-off**: OADE-NSGA-II v2 had better corrected outcomes than NSGA-II on all 10 endpoints in this benchmark, but its measured runtime was longer than the pymoo-based NSGA-II implementation. Runtime comparisons describe these implementations and this execution environment, not algorithm-independent complexity.

---

## 7. Research Conclusion

In this benchmark, OADE-NSGA-II v2 with Adaptive Diversity-Aware Restart had better corrected pairwise outcomes than the v1 configuration on several tested endpoints and led the descriptive means on eight of ten endpoints. The results support further evaluation of this configuration on these five ZDT problems; they do not establish general or universal dominance.

The outcome count is 58 wins, one non-significant comparison and one loss among the 60 configured paired tests. This is evidence for the tested implementations, seeds and protocol. Mechanistic attribution to eliminated false triggers requires trigger-level diagnostics; generalization requires additional benchmark suites and independent implementations.

---

## 8. Data Provenance

All raw runs, statistical tests, summaries, and figures are archived reproducibly:
- Raw runs: `results/algorithm_benchmark_v2/algorithm_benchmark_raw_runs.csv`
- Statistical tests: `results/algorithm_benchmark_v2/algorithm_benchmark_paired_statistics.csv`
- Summary table: `results/algorithm_benchmark_v2/algorithm_benchmark_igd_hv_summary.csv`
- Validation logs: `results/algorithm_benchmark_v2/algorithm_benchmark_validation.csv`
- Cost summary: `results/algorithm_benchmark_v2/algorithm_benchmark_cost_summary.csv`
- Figures: `results/figures/benchmark_v2_outcome_counts.*`, `results/figures/benchmark_v2_v1_vs_v2_delta.*`

---

## 9. Multi- and Many-Objective Extension (DTLZ1–DTLZ4, $M \in \{2, 3, 5\}$)

To test whether the Benchmark v2 gains generalize beyond continuous bi-objective ZDT problems, the identical 7-algorithm suite was subsequently evaluated across **DTLZ1–DTLZ4** ($M \in \{2, 3, 5\}$, 12 configurations, 2,520 runs; see [`docs/dtlz1_4_integrated_report.md`](dtlz1_4_integrated_report.md)):

* **Integrated 17-problem outcome count (ZDT + DTLZ1–DTLZ4, 204 comparisons)**: **149 significant wins (73.0%), 41 comparisons with no detected difference (20.1%), and 14 significant losses (6.9%)** across 3,570 stochastic runs (`510/510` valid OADE fronts). The ZDT and DTLZ p-values were Holm-adjusted within separate suite-by-metric families; this combined count is descriptive, not a single 204-test correction.
* **Results from later DTLZ validation**: Favorable corrected outcomes were observed on selected DTLZ1/3 comparisons, with some maximal effect sizes at $M=3$. No OADE collapsed front was recorded in 90 DTLZ4 runs, compared with 11/30 and 30/30 collapsed fronts for NSGA-II at $M=2$ and $M=5$. Across the 48 $M=5$ comparisons, OADE had no significant losses against NSGA-II or D-NSGA-II. These findings are bounded to the tested configurations and seeds; they do not establish immunity or general superiority.
* **Specific Weaknesses Revealed**: On smooth or biased 3-objective spherical fronts (`dtlz2_m3`, `dtlz4_m3`), SBX-based NSGA-II/D-NSGA-II and CGDE-NSGA-II outperform OADE-NSGA-II v2 (~6%–14% IGD, ~2.3%–4.1% HV); at $M=5$ under extreme multimodality (`dtlz1_m5`, `dtlz3_m5`), crowding-distance saturation still limits Hypervolume penetration into the reference box ($\text{HV}_{\text{med}} = 0.0$).

