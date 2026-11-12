# OADE-NSGA-II: performance and failure boundaries of an adaptive DE/OBL search configuration

Working research manuscript, updated 12 November 2026. This document integrates the available evidence; it does not claim publication readiness, established algorithmic novelty or a verified adaptive-restart mechanism. Detailed numeric tables remain in the linked experiment reports.

## Abstract

Combining DE, opposition-based search and restart with NSGA-II introduces interacting design choices whose benefits depend on landscape and objective count. We evaluated the recorded configurations with 30 scheduled paired seeds and configured 20,000-evaluation budgets. The suite-specific accounting and algorithm-block provenance are documented in the experiment registry. The common uniform warm start bypasses standalone Sobol/initial OBL.

ZDT v2 produced 58 favorable, 1 inconclusive and 1 unfavorable pairwise metric comparisons after the stated suite-by-metric Holm adjustment.

DTLZ1–4 produced 91 favorable, 40 inconclusive and 13 unfavorable pairwise metric comparisons after the stated suite-by-metric Holm adjustment.

Bi-objective WFG produced 42 favorable, 0 inconclusive and 6 unfavorable pairwise metric comparisons after the stated suite-by-metric Holm adjustment.

Compact WFG produced 56 favorable, 11 inconclusive and 29 unfavorable pairwise metric comparisons after the stated suite-by-metric Holm adjustment.

These counts describe the selected implementations, conditional on valid matched output, and do not establish universal superiority. Held-out Adaptive and No Restart final metrics matched in 148/150 pairs, leaving adaptive-trigger attribution unresolved. Baseline fidelity and paired-effect uncertainty remain limitations.

## 1. Research question and scope

The study asks when a particular DE/OBL-enhanced NSGA-II implementation improves final approximation quality under a common evaluation cap, and which failure boundaries remain. A secondary question is whether component-removal experiments support attributing observed gains to the added mechanisms.

The contribution supported here is an implementation and empirical characterization across selected unconstrained continuous test suites. It is not a general superiority theorem or evidence for every added component. Establishing a novel algorithmic contribution requires a literature comparison that distinguishes the design from prior combinations of DE, OBL, parameter adaptation and restart.

## 2. Relationship to existing methods

NSGA-II supplies nondominated sorting and crowding-based environmental selection [Deb et al., 2002; references.bib]. pymoo supplies standard problem definitions, indicators and three comparator implementations [Blank and Deb, 2020]. The benchmark also includes locally implemented Cross-Generation DE–NSGA-II, NSGA-II/SDR-OLS with capped local search, and a continuous-search adaptation of Continuous Encoding MOEA.

These comparators answer different questions. Dynamic NSGA-II is exercised on static functions, and R-NSGA-II emphasizes aspiration regions rather than uniform coverage of the full front. The CE adaptation does not exercise the graph encoding in its source paper. The [baseline registry](../protocols/baselines.md) therefore constrains interpretation to the exact implementations tested. A verified comparison to contemporary, task-aligned state-of-the-art algorithms remains future work; the local CGDE comparator currently has no established matching publication citation.

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

Classic restart checks consecutive small changes in the ideal point and replaces 70% of the population with random points, resetting adaptation history. The v2 adaptive configuration requires stagnation and a diversity-collapse condition; it retains at least 80% and generates local opposition/Gaussian replacements with soft parameter decay. The [restart report](../reports/restart_confirmation_report.md) specifies the thresholds and formulas. Neither the historical CSVs nor the final metrics record the trigger events, so mechanism operation in those runs cannot be reconstructed.

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

The budget proxy rejects a batch before its evaluation if it would exceed the cap. The current RNSGA2 blocks on ZDT, DTLZ and WFG include aspiration-point setup in their evaluation counters and runtimes. Suite-specific RNSGA2 accounting is specified in the [experiment registry](../protocols/experiment_registry.md#budget-definition). Actual recorded search evaluation use may be lower; this pseudocode does not imply every run consumes exactly 20,000 evaluations or that each partial internal operation is a completed generation.

## 4. Experimental protocol

The core suites contain five ZDT configurations, twelve DTLZ1–4 configurations at M=2/3/5 and four bi-objective WFG configurations with seven algorithms. A compact WFG study includes twelve configurations and five algorithms. Thirty runs were scheduled per configuration, using seeds 42–71; restart confirmation used seeds 1000–1029. Shared seeds and initialization define paired blocks. Reuse of baseline rows across versions and overlap between WFG studies do not create independent replications.

IGD uses the problem-specific Pareto reference sample. DTLZ/WFG references use Das-Dennis directions with H=200, 20 or 6 for M=2, 3 or 5 unless configured. HV uses max(reference front)+0.1. Indicators across different objective scales are not pooled as absolute performance quantities.

The analysis uses two-sided paired Wilcoxon signed-rank tests and Holm adjustment separately within each suite and metric: 30 comparisons for ZDT, 72 for DTLZ, 24 for bi-objective seven-algorithm WFG and 48 for compact WFG. Effect sizes are matched-pairs rank-biserial correlations oriented toward the reference. Thirty runs are scheduled; the current DTLZ tests use 26–30 valid matched pairs after 18 invalid output records. The complete-case quality estimand is conditional on valid output; failure rates remain a separate part of the evidence. Exact values, descriptive mean/SD and median/IQR are in the detailed tables. No confidence intervals for the paired effects are currently available.

## 5. Results

| Dataset | Records | Invalid | Comparisons | OADE W / ND / L |
|---|---:|---:|---:|---|
| algorithm_benchmark_v2 | 1050 | 0 | 60 | 58 / 1 / 1 |
| dtlz_benchmark | 2520 | 18 | 144 | 91 / 40 / 13 |
| wfg_m2_7algo_benchmark | 840 | 0 | 48 | 42 / 0 / 6 |
| wfg_compact_benchmark | 1800 | 0 | 96 | 56 / 11 / 29 |

These are separately corrected suite results; counts across suites are descriptive. The detailed [DTLZ](../reports/dtlz_results_report.md) and [WFG](../reports/wfg_compact_report.md) reports include all implementation–problem summaries and exact paired tests, including failures and conditional sample sizes. [Integrated ZDT/DTLZ evidence](../reports/dtlz1_4_integrated_report.md) provides the 17-configuration synthesis.

The component evidence remains bounded: the classic ablation supports periodic OBL on the tested ZDT4 configuration, while Adaptive and No Restart matched final metrics in 148/150 held-out pairs. Full-algorithm suite comparisons do not isolate adaptive-restart causality or standalone Sobol initialization.

Runtime comparisons concern the recorded implementations and environment. The integrated rank figure uses DTLZ4 runtime as a proxy for aggregate quality rank, rather than a full-suite speed frontier.

## 6. Discussion and limitations

The central result is heterogeneity: the implemented search configuration performs favorably in several selected settings while losing quality on other fronts and at some higher objective counts. This is a useful empirical boundary even without attributing gains to every mechanism.

Three limitations directly constrain the interpretation. First, incomplete baseline fidelity and task alignment limit published-method and state-of-the-art comparisons. Second, missing trigger telemetry prevents a causal account of adaptive restart. Third, conditional exclusion of structural failures and absent effect intervals leave uncertainty and failure-aware performance incompletely characterized. The original DTLZ corner-collapse diagnostic also differs from the validator's collapsed_front rule and lacks a complete historical run-level definition; it should not be treated as a newly validated endpoint.

The next evidence should resolve these uncertainties rather than simply expand the number of benchmarks. Verify intended baseline sources, quantify paired-effect uncertainty and, if restart is the central proposed contribution, compare Adaptive with No Restart using event telemetry on fresh settings/seeds. Standalone initialization benefits require their own budgeted experiment. See [follow-up decisions](../protocols/followup_experiments.md).

## 7. Reproducibility and availability

Code, configurations, tests, figure sources, detailed reports and run-level CSVs are organized in this repository. [Reproducibility instructions](../protocols/reproducibility.md) distinguish present-day environment snapshots and historical artifact inventories from prospective execution manifests. The RNSGA2 ZDT execution manifest and composition of the ZDT tables are recorded in results/provenance/. Other archived source/package versions cannot be certified retroactively. New runs record code/config/environment identity and primary artifact checksums, and refuse unsafe resume or overwrite.

## Evidence allocation

| Evidence function | Main text | Detailed record |
|---|---|---|
| Core observation | Landscape-dependent quality and WFG scaling boundary | ZDT/DTLZ/WFG tables and source CSVs |
| Necessary support | Common cap/start, matched run design, conditional n | Configs, provenance, statistical tables |
| Qualification | ZDT6 loss, smooth M=3 deficits, zero-HV cases, local baseline adaptations | Failure diagnostics and baseline registry |
| Attribution | OBL ablation and nearly identical Adaptive/No Restart outcomes | Ablation and held-out restart reports |
| Robustness/provenance | Limitations and next checks | Sensitivity report, inventory, environment and QA records |

AUTHOR_INPUT_NEEDED before submission: intended primary contribution and journal, matching published source for local CGDE if one exists, historical environment/source evidence if recoverable, complete corner-collapse definition and author-selected licensing. These gaps remain explicit rather than being filled with invented metadata.
