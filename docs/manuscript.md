# OADE-NSGA-II: performance and failure boundaries of an adaptive DE/OBL search configuration

Working research manuscript, updated 12 November 2026. This document integrates the available evidence; it does not claim publication readiness, established algorithmic novelty or a verified adaptive-restart mechanism. Detailed numeric tables remain in the linked experiment reports.

## Abstract

Combining differential evolution, opposition-based search and restart with NSGA-II introduces interacting design choices whose benefits can depend on the test landscape and objective count. We evaluated the repository's OADE-NSGA-II configuration under a cap of 20,000 objective evaluations and 30 scheduled stochastic runs per configuration. The fixed-budget protocol used common uniform initial populations; the solver's standalone Sobol/initial-opposition branch was bypassed. In the archived ZDT v2 comparison, OADE had 58 favorable, one inconclusive and one unfavorable Holm-adjusted pairwise metric comparisons against six configured implementations. DTLZ1–4 produced 91 favorable, 40 inconclusive and 13 unfavorable comparisons, conditional on valid matched output. Bi-objective WFG produced 42 favorable and six unfavorable comparisons, whereas a five-algorithm WFG scaling study showed a declining favorable fraction from M=2 to M=5. Held-out restart comparisons did not distinguish the adaptive mechanism from disabling restart: their final IGD/HV outputs matched in 148 of 150 problem–seed pairs. These findings support a bounded empirical performance profile, with unresolved mechanism attribution, baseline fidelity and uncertainty intervals.

## 1. Research question and scope

The study asks when a particular DE/OBL-enhanced NSGA-II implementation improves final approximation quality under a common evaluation cap, and which failure boundaries remain. A secondary question is whether component-removal experiments support attributing observed gains to the added mechanisms.

The contribution supported here is an implementation and empirical characterization across selected unconstrained continuous test suites. It is not a general superiority theorem or evidence for every added component. Establishing a novel algorithmic contribution requires a literature comparison that distinguishes the design from prior combinations of DE, OBL, parameter adaptation and restart.

## 2. Relationship to existing methods

NSGA-II supplies nondominated sorting and crowding-based environmental selection [Deb et al., 2002; references.bib]. pymoo supplies standard problem definitions, indicators and three comparator implementations [Blank and Deb, 2020]. The benchmark also includes locally implemented Cross-Generation DE–NSGA-II, NSGA-II/SDR-OLS with capped local search, and a continuous-search adaptation of Continuous Encoding MOEA.

These comparators answer different questions. Dynamic NSGA-II is exercised on static functions, and R-NSGA-II emphasizes aspiration regions rather than uniform coverage of the full front. The CE adaptation does not exercise the graph encoding in its source paper. The [baseline registry](baselines.md) therefore constrains interpretation to the exact implementations tested. A verified comparison to contemporary, task-aligned state-of-the-art algorithms remains future work; the local CGDE comparator currently has no established matching publication citation.

## 3. Implemented method

### Problem and output

The tested problem is unconstrained minimization of a vector F(x) over continuous box bounds. The solver maintains a population and returns decision/objective arrays; the benchmark extracts the nondominated output before indicator evaluation. Constrained and discrete problems were not evaluated.

### Search cycle

The OADE benchmark configuration uses population size 100, initial DE probability 0.5, five objective-space neighbors, μF=0.65 and μCR=0.5. Neighborhoods are computed from normalized objective coordinates. Variation combines DE and SBX with polynomial mutation and bound handling. Enabled opposition injection occurs at generation indices 0, 10, 20, … . Duplicate handling, filling and environmental selection act before the parameter updates. Exact operators and defaults are defined by src/oade_nsga2/algorithm.py, operators.py and selection.py; the new execution manifest records hashes rather than treating an unversioned formula summary as sufficient provenance.

The standalone solver supports Sobol/OBL initialization. The benchmark instead supplies a common uniform warm start and bypasses that branch. Consequently, the no-OBL comparison concerns the injected opposition candidates used on that path; it provides no evidence for Sobol initialization.

### Adaptation

For DE offspring assigned rank 1 during selection, the scale-factor location uses a smoothed Lehmer mean and the crossover-rate location uses a smoothed arithmetic mean:

\[
\mu_F \leftarrow 0.9\mu_F+0.1\frac{\operatorname{mean}(F^2)}{\operatorname{mean}(F)},\qquad
\mu_{CR}\leftarrow0.9\mu_{CR}+0.1\operatorname{mean}(CR).
\]

The operator probability update uses the generated share:

\[
p_{DE}\leftarrow\operatorname{clip}\left(0.9p_{DE}+0.1\frac{n_{DE}}{n_{DE}+n_{SBX}},0.2,0.8\right).
\]

This is not a success-based comparison between DE and SBX. Changing it to such a rule would define a new algorithm version requiring separate evidence.

### Restart

Classic restart checks consecutive small changes in the ideal point and replaces 70% of the population with random points, resetting adaptation history. The v2 adaptive configuration requires stagnation and a diversity-collapse condition; it retains at least 80% and generates local opposition/Gaussian replacements with soft parameter decay. The [restart report](restart_confirmation_report.md) specifies the thresholds and formulas. Neither the historical CSVs nor the final metrics record the trigger events, so mechanism operation in those runs cannot be reconstructed.

### Operational pseudocode

```text
generate a common uniform initial population from the paired seed
evaluate and select the supplied initial population
while another requested evaluation batch fits within the cap:
    check stagnation; apply the configured restart condition if eligible
    generate DE/SBX offspring and enabled periodic opposition candidates
    evaluate candidates; handle duplicates and fill the population if needed
    select the next population using ranks and crowding
    update F/CR locations and the generated-share DE probability
return the last complete solver population; benchmark extracts nondominated output
```

The budget proxy rejects a batch before its evaluation if it would exceed the cap. The archived RNSGA2 path omitted a population-sized aspiration-point setup evaluation from its counter and timer; new runs charge that work, so historical budget fairness has this stated exception. Actual recorded search evaluation use may be lower; this pseudocode does not imply every run consumes exactly 20,000 evaluations or that each partial internal operation is a completed generation.

## 4. Experimental protocol

The core suites contain five ZDT configurations, twelve DTLZ1–4 configurations at M=2/3/5 and four bi-objective WFG configurations with seven algorithms. A compact WFG study includes twelve configurations and five algorithms. Thirty runs were scheduled per configuration, using seeds 42–71; restart confirmation used seeds 1000–1029. Shared seeds and initialization define paired blocks. Reuse of baseline rows across versions and overlap between WFG studies do not create independent replications.

IGD uses the problem-specific Pareto reference sample. DTLZ/WFG references use Das-Dennis directions with H=200, 20 or 6 for M=2, 3 or 5 unless configured. HV uses max(reference front)+0.1. Indicators across different objective scales are not pooled as absolute performance quantities.

The analysis uses two-sided paired Wilcoxon signed-rank tests and Holm adjustment separately within each suite and metric: 30 comparisons for ZDT, 72 for DTLZ, 24 for bi-objective seven-algorithm WFG and 48 for compact WFG. Effect sizes are matched-pairs rank-biserial correlations oriented toward the reference. Thirty runs are scheduled, but some DTLZ tests contain only 26–29 valid matched pairs after 18 invalid collapsed-front records. The complete-case quality estimand is conditional on valid output; failure rates remain a separate part of the evidence. Exact values, descriptive mean/SD and median/IQR are in the detailed tables. No confidence intervals for the paired effects are currently available.

## 5. Results

### Quality improvements are landscape-dependent

The [ZDT v2 report](benchmark_v2_results_report.md) records 58 favorable, one inconclusive and one unfavorable comparisons. OADE had the best descriptive means on eight of ten endpoints. CGDE had better HV on ZDT6; the IGD comparison on that problem did not establish a corrected difference.

The [DTLZ report](dtlz1_4_integrated_report.md) records 91 favorable, 40 inconclusive and 13 unfavorable comparisons. Results were favorable on selected multimodal cases, but NSGA-II and other comparators remained competitive or better on smooth three-objective DTLZ2/4. OADE's HV was zero in 17/30 DTLZ1-M5 runs and all DTLZ3-M5 runs despite favorable IGD comparisons. This limits a claim of reliable convergence under the tested cap. Crowding saturation is one hypothesis, not an experimentally isolated explanation.

### WFG scaling exposes a boundary

The [WFG report](wfg_compact_report.md) records 42 favorable and six unfavorable comparisons at M=2 with seven implementations. In the compact five-algorithm study, outcomes were 56 favorable, 11 inconclusive and 29 unfavorable. The favorable fraction declined from 87.5% at M=2 to 53.1% at M=3 and 34.4% at M=5. These are observations for four WFG functions, one decision dimension and the selected comparator pool, not a general scaling law.

### Component evidence does not establish adaptive-restart causality

The [classic ablation](ablation_results_report.md) supports a periodic-OBL contribution on the tested ZDT4 configuration. It does not establish an isolated corrected benefit for every adaptive component. In [held-out restart confirmation](restart_confirmation_report.md), both Adaptive and No Restart improved on classic Full OADE on several endpoints, but matched each other's final IGD/HV in 148/150 problem–seed pairs. The evidence therefore supports avoiding the harmful classic configuration in these cases more directly than it supports a new adaptive-trigger mechanism.

### Computational cost is implementation-dependent

Recorded wall-clock measurements compare specific Python implementations, package environments, worker contention and thread settings. The integrated quality-rank figure uses DTLZ4 runtime as a proxy while aggregating quality ranks across 34 endpoints; it is not a full-suite cost frontier. Hardware-independent complexity or general speed superiority is not inferred from these measurements.

## 6. Discussion and limitations

The central result is heterogeneity: the implemented search configuration performs favorably in several selected settings while losing quality on other fronts and at some higher objective counts. This is a useful empirical boundary even without attributing gains to every mechanism.

Three limitations directly constrain the interpretation. First, incomplete baseline fidelity and task alignment limit published-method and state-of-the-art comparisons. Second, missing trigger telemetry prevents a causal account of adaptive restart. Third, conditional exclusion of structural failures and absent effect intervals leave uncertainty and failure-aware performance incompletely characterized. The original DTLZ corner-collapse diagnostic also differs from the validator's collapsed_front rule and lacks a complete historical run-level definition; it should not be treated as a newly validated endpoint.

The next evidence should resolve these uncertainties rather than simply expand the number of benchmarks. Verify intended baseline sources, quantify paired-effect uncertainty and, if restart is the central proposed contribution, compare Adaptive with No Restart using event telemetry on fresh settings/seeds. Standalone initialization benefits require their own budgeted experiment. See [follow-up decisions](followup_experiments.md).

## 7. Reproducibility and availability

Code, configurations, tests, figure sources, detailed reports and run-level CSVs are organized in this repository. [Reproducibility instructions](reproducibility.md) distinguish present-day environment snapshots and historical artifact inventories from prospective execution manifests. Historical source/package versions cannot be certified retroactively. New runs record code/config/environment identity and primary artifact checksums, and refuse unsafe resume or overwrite.

## Evidence allocation

| Evidence function | Main text | Detailed record |
|---|---|---|
| Core observation | Landscape-dependent quality and WFG scaling boundary | ZDT/DTLZ/WFG tables and source CSVs |
| Necessary support | Common cap/start, matched run design, conditional n | Configs, provenance, statistical tables |
| Qualification | ZDT6 loss, smooth M=3 deficits, zero-HV cases, local baseline adaptations | Failure diagnostics and baseline registry |
| Attribution | OBL ablation and nearly identical Adaptive/No Restart outcomes | Ablation and held-out restart reports |
| Robustness/provenance | Limitations and next checks | Sensitivity report, inventory, environment and QA records |

AUTHOR_INPUT_NEEDED before submission: intended primary contribution and journal, matching published source for local CGDE if one exists, historical environment/source evidence if recoverable, complete corner-collapse definition and author-selected licensing. These gaps remain explicit rather than being filled with invented metadata.
