# Baseline identity and implementation registry

This registry identifies the implementations actually evaluated. Result IDs are unchanged to preserve joins with archived CSVs. It does not certify equation-by-equation reproduction of every cited method.

| CSV ID | Defensible name | Owning implementation and configuration | Source and interpretation boundary |
|---|---|---|---|
| NSGA2 | NSGA-II | pymoo.algorithms.moo.nsga2.NSGA2; config/algorithms/nsga2.yaml | Deb et al. (2002), doi:10.1109/4235.996017; pymoo implementation, common uniform warm start |
| DNSGA2 | Dynamic NSGA-II (D-NSGA-II) | pymoo.algorithms.moo.dnsga2.DNSGA2; config/algorithms/dnsga2.yaml | [pymoo documentation](https://pymoo.org/algorithms/moo/dnsga2.html). Tested here on static functions; change-detection evaluations count against the budget. This is not a direction-based algorithm or evidence about dynamic optimization performance. |
| RNSGA2 | Reference point NSGA-II | pymoo.algorithms.moo.rnsga2.RNSGA2; config/algorithms/rnsga2.yaml | [pymoo documentation](https://pymoo.org/algorithms/moo/rnsga2.html). Aspiration points are derived from initial objective values, not the true PF. Whole-front IGD/HV also measure a different goal from preference-region coverage. |
| CGDE_NSGAII | Cross-Generation DE–NSGA-II, local implementation | algorithms/cgde_nsga2; config/algorithms/cgde_nsga2.yaml | Local operator: v = x_i + F(x_pbest − x_i) + F(x_r1,current − x_r2,archive). Citation to a matching original publication has not been established. Treat this as the local comparator, not an independently verified published Competitive & Guided DE method. |
| NSGAII_SDR_OLS | NSGA-II/SDR-OLS, local implementation with capped local search | algorithms/nsga2_sdr_ols; config/algorithms/nsga2_sdr_ols.yaml | Zhang, Wang and Wang (2023), [doi:10.3390/math11081911](https://doi.org/10.3390/math11081911). Opposition and local search, not orthogonal local search. SDR, OBL and Gaussian omega+/omega− local search are implemented locally. The benchmark limits neighbors to 2 × population size; this differs from unrestricted variable-wise local search. |
| CE_MOEA | Continuous Encoding MOEA, continuous-search adaptation | algorithms/ce_moea.CEMOEA; config/algorithms/ce_moea.yaml | Sun et al., [arXiv:2006.03996v2](https://arxiv.org/abs/2006.03996v2). Benchmark uses the NSGA-II/DE search component on continuous test functions; graph encoding and community-detection objectives are not used. It is not Cross-Entropy MOEA. |

Python package versions at historical execution are unknown unless recorded separately. The environment snapshot captured during the audit describes the current machine only. New execution manifests pin the resolved class paths, parameters and source hashes.

The main empirical claim is restricted to these implementations and parameterizations. Counts against RNSGA2, DNSGA2 or locally adapted solvers should not be presented as proof of superiority to all modern general-purpose multiobjective optimizers. A state-of-the-art claim requires a literature review, task-aligned comparators and verified implementations.

## Method mapping for OADE

- Fixed-budget benchmark: `make_initial_population` draws uniform samples using `default_rng(seed)` and passes `initial_x` to every solver. OADE's standalone Sobol/initial OBL branch is bypassed.
- Periodic OBL: enabled injection occurs when generation index modulo 10 equals zero, including generation zero. The no-OBL ablation disables these injections under the common warm start.
- F update: μF ← 0.9 μF + 0.1 mean(F²)/mean(F) for DE offspring assigned rank 1 during selection.
- CR update: μCR ← 0.9 μCR + 0.1 mean(CR) over the same offspring.
- Operator probability: pDE ← clip(0.9 pDE + 0.1 nDE/(nDE+nSBX), 0.2, 0.8). This tracks generated share, not comparative survival success.
- Restart configuration is part of the tested algorithm version. Descriptive differences between classic and adaptive result sets do not isolate the adaptive trigger's causal contribution.

## Citation status

See [references.bib](references.bib). Known sources are supplied; no matching CGDE paper is invented. The project previously displayed an MIT badge without a tracked LICENSE. The badge has been removed pending an author-selected license and review of imported baseline rights; this change does not assign a new license.
