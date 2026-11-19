# Baseline identity and implementation registry

## Current comparison set — 19 November 2026

The active [six-solver protocol](zdt_six_fixed_oade.md) uses OADE_NSGAII, NSGA2, DNSGA2, CGDE_NSGAII, **GDE3** and **NSDE**. CE_MOEA, RNSGA2 and NSGAII_SDR_OLS are removed from this active suite; their implementations and the older seven-solver results remain legacy evidence only. The new suite is a fresh 900-run design with 50 global-Holm endpoints; 900 runs are complete, 899 valid; global Holm: 44/50 favor OADE, 6 nonsignificant. See the [audited report](../reports/zdt_six_fixed_oade_report.md).

| ID | Library implementation | Role and settings |
|---|---|---|
| GDE3 | `pymoo.algorithms.moo.gde3.GDE3` | Parent–trial DE competition and nondominated/crowding survival; common uniform input, DE/rand/1/bin, F=0.5, CR=0.5, gamma=1e-4, bounce-back. [Official documentation](https://pymoo.org/algorithms/moo/gde3.html) |
| NSDE | `pymoo.algorithms.moo.nsde.NSDE` | DE variation with NSGA-II sorting/survival; same explicit DE settings and input. [Official documentation](https://pymoo.org/algorithms/moo/nsde.html) |

## Legacy seven-solver registry

This registry describes current executable implementations after the 2026-11-14 corrections. Earlier comparator results are excluded; the current evaluation starts with ZDT v2. See [paper corrections and remaining uncertainties](baseline_paper_corrections.md).

> For the locally reconstructed baselines, we could not locate author-provided source code or detailed explanations resolving the implementation ambiguities. We therefore reconstructed these methods from the publicly available papers, documenting our implementation assumptions.

The completed evaluation of these corrected baselines and fixed OADE is documented in the [ZDT v2 audit report](../reports/zdt_seven_fixed_oade_v2_report.md), with its [execution manifest](../../results/experiments/zdt_seven_fixed_oade_v2/study_manifest.json). Obsolete comparator reports have been removed; their results are not attributed to the corrected implementations.

| CSV ID | Defensible name | Owning implementation and configuration | Source and interpretation boundary |
|---|---|---|---|
| NSGA2 | NSGA-II | pymoo.algorithms.moo.nsga2.NSGA2; config/algorithms/nsga2.yaml | Deb et al. (2002), doi:10.1109/4235.996017; pymoo implementation, common uniform warm start |
| DNSGA2 | Dynamic NSGA-II (D-NSGA-II) | pymoo.algorithms.moo.dnsga2.DNSGA2; config/algorithms/dnsga2.yaml | [pymoo documentation](https://pymoo.org/algorithms/moo/dnsga2.html). Tested here on static functions; change-detection evaluations count against the budget. This is not a direction-based algorithm or evidence about dynamic optimization performance. |
| RNSGA2 | Reference point NSGA-II | pymoo.algorithms.moo.rnsga2.RNSGA2; config/algorithms/rnsga2.yaml | [pymoo documentation](https://pymoo.org/algorithms/moo/rnsga2.html). Aspiration points are derived from initial objective values, not the true PF. Whole-front IGD/HV also measure a different goal from preference-region coverage. |
| CGDE_NSGAII | Cross-Generation DE–NSGA-II, paper-based reconstruction | src/cgde_nsga2; config/algorithms/cgde_nsga2.yaml | [Qiu, Xu and Tan, CEC 2014](https://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2014/WCCI/CEC-2014/PROGRAM/E-14533.pdf). NCG/PCG, subrank neighborhoods, inherited individual F, stochastic CR. Unspecified CR range/bootstrap/ties documented separately. Not Competitive & Guided DE. |
| NSGAII_SDR_OLS | NSGA-II/SDR-OLS, uncapped local reconstruction | src/nsga2_sdr_ols; config/algorithms/nsga2_sdr_ols.yaml | [Zhang, Wang and Wang (2023)](https://doi.org/10.3390/math11081911). Opposition and local search. Full local neighborhood and merged mating pool; final FE stopping and inconsistent Algorithm 4 require documented interpretation. Not certified author-code reproduction. |
| CE_MOEA | Continuous Encoding MOEA, continuous-search adaptation on ZDT | src/ce_moea.CEMOEA; config/algorithms/ce_moea.yaml | [Sun et al., v2](https://arxiv.org/html/2006.03996v2), Algorithms 3–4. PM exponent corrected to printed eta. Graph mode defaults to printed cosine; ZDT does not use graph encoding/objectives. Not Cross-Entropy MOEA. |

Python package versions at historical execution are unknown unless recorded separately. The environment snapshot captured during the audit describes the current machine only. New execution manifests pin the resolved class paths, parameters and source hashes.

The main empirical claim is restricted to these implementations and parameterizations. Counts against RNSGA2, DNSGA2 or locally adapted solvers should not be presented as proof of superiority to all modern general-purpose multiobjective optimizers. A state-of-the-art claim requires a literature review, task-aligned comparators and verified implementations.

## Method mapping for OADE

- Fixed OADE uses seeded uniform initialization. Research OADE may separately study Sobol/OBL. A common uniform input does not imply identical effective initial populations: SDR-OLS applies its own OBL selection and charges its evaluations.
- Periodic OBL: enabled injection occurs when generation index modulo 10 equals zero, including generation zero. The no-OBL ablation disables these injections under the common warm start.
- F update: μF ← 0.9 μF + 0.1 mean(F²)/mean(F) for DE trials nondominated in the evaluated parent+trial pool before duplicate removal; no stale/None-rank filtering.
- CR update: μCR ← 0.9 μCR + 0.1 mean(CR) over the same offspring.
- Current default `probability_update_mode=success_rate` normalizes nondominated-trial success by each operator's trial count; `fixed` holds pDE. These are separate ablation variants, not relabelings of historical results. See [probability ablation](probability_ablation.md).
- Restart configuration is part of the tested algorithm version. Descriptive differences between classic and adaptive result sets do not isolate the adaptive trigger's causal contribution.

## Citation status

See [references.bib](../manuscript/references.bib). The CEC 2014 paper explicitly names CGDE-NSGA-II; earlier source audits are historical, superseded by the correction note. The project previously displayed an MIT badge without a tracked LICENSE. Its removal does not assign a new license.
