# README rewrite: evidence and editorial audit

This rewrite applies the local nature-writing and nature-statistics guidance to repository reports. It reorganizes supplied findings without adding runs, fitting new models, recalculating p-values or asserting journal compliance. English and Vietnamese project READMEs share the same problem-specific evidence.

## Terminology ledger

| Canonical term | Definition / source identity | Reporting decision |
| --- | --- | --- |
| OADE-NSGA-II | Tên phương pháp; ID benchmark là OADE_NSGAII. | Classic và adaptive được xác định bằng cấu hình/đợt chạy, không bằng ID benchmark. |
| Classic | Cấu hình restart cổ điển; ID xác nhận là OADE_FULL. | Không dùng từ classic để gọi adaptive. |
| Adaptive | Cấu hình restart thích nghi; ID xác nhận là OADE_ADAPTIVE_RESTART. | Không suy từ cải thiện chất lượng sang xác nhận cơ chế trigger. |
| IGD | Inverted generational distance; thấp hơn tốt hơn. | Mean ± SD cho benchmark; median và IQR cho OFAT. |
| HV | Hypervolume; cao hơn tốt hơn theo reference point của từng bài. | Không so trực tiếp trị số HV giữa các bài toán. |
| OFAT | One factor at a time: thay một tham số mỗi lần. | Không suy ra tương tác hoặc cấu hình tối ưu từ OFAT. |
| n | Một lượt chạy ngẫu nhiên tại một bài toán, thuật toán và seed. | Block đối chứng/baseline dùng lại không tạo lượt độc lập mới. |

## Result allocation

| Evidence | Role | Location |
| --- | --- | --- |
| Adaptive benchmark versus NSGA2, per ZDT | Core observation | Root README: one subsection/problem with all seven comparator means/SDs, classic/adaptive differences, held-out means and OFAT responses; detailed tests in problem reports |
| ZDT4 population-200 deterioration | Conclusion-changing boundary | Root and ZDT4 README; complete OFAT tables in sensitivity_adaptive report |
| ZDT6 CGDE_NSGAII comparison | Adverse comparator boundary | Root and ZDT6 README; retain IGD non-detection and HV disadvantage |
| Classic/adaptive benchmark and held-out restart | Necessary support and mechanism boundary | Each ZDT README; separate seed blocks and report links |
| Full ablation and nine-parameter sensitivity records | Supporting evidence | Per-problem experiment reports; classic and adaptive kept separate |
| DTLZ/WFG objective-count conditions | Scope extension | One README per problem/configuration; WFG seven-/five-algorithm studies remain separate |
| CSV hashes and block provenance | Traceability | Per-problem manifest, ZIP catalog and protocol links |
| Pooled cross-suite wins/ranks and runtime claims | Removed from entry-point narrative | Historical reports retained as reference; no newly pooled replacement |

## Claim–evidence map

| Claim | Evidence member (inside problem ZIP) | Status |
| --- | --- | --- |
| ZDT1 adaptive mean IGD versus NSGA2 | results/by_problem/zdt/zdt1/benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv | Supported descriptive report; existing paired tests linked separately |
| ZDT2 adaptive mean IGD versus NSGA2 | results/by_problem/zdt/zdt2/benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv | Supported descriptive report; existing paired tests linked separately |
| ZDT3 adaptive mean IGD versus NSGA2 | results/by_problem/zdt/zdt3/benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv | Supported descriptive report; existing paired tests linked separately |
| ZDT4 adaptive mean IGD versus NSGA2 | results/by_problem/zdt/zdt4/benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv | Supported descriptive report; existing paired tests linked separately |
| ZDT6 adaptive mean IGD versus NSGA2 | results/by_problem/zdt/zdt6/benchmark_adaptive/algorithm_benchmark_igd_hv_summary.csv | Supported descriptive report; existing paired tests linked separately |

## Statistics and repetition decisions

One stochastic run is the experimental unit. Benchmark mean ± sample SD describes run dispersion, not a confidence interval for a paired effect. Existing Wilcoxon/Holm families are preserved; no inferential family is redefined per folder. OFAT baseline reuse is not counted as new replication. OFAT summaries remain separate from benchmark means. No new confidence intervals, interaction tests or causal mechanism claims were introduced.

The project README is a self-contained summary report. Each ZDT subsection includes a seven-algorithm mean/SD table, descriptive classic/adaptive comparison, held-out variant means, OFAT responses and a selected classic-ablation result. Seven existing figures are embedded with captions explaining their scope and uncertainty. DTLZ/WFG have numeric summary rows for every configuration. Links lead to full tests and diagnostics rather than replacing the main summary. No figure was regenerated or edited; original aggregate figure panels are identified as context, not used to assert pooled superiority.

## Before/after word counts

Counts are whitespace-delimited tokens, useful for a mechanical length audit rather than comparing English with Vietnamese. Former pooled Results sections were replaced; there is no one-to-one mapping from the old cross-suite subsections to the new problem subsections.

| File | Before | After |
| --- | --- | --- |
| README.md | 1987 | 3601 |
| README.vi.md | 2577 | 4336 |
| docs/index.md | 363 | 352 |
| results/by_problem/README.md | 328 | 487 |
| results/by_problem/dtlz/dtlz1_m2/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz1_m3/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz1_m5/README.md | 165 | 472 |
| results/by_problem/dtlz/dtlz2_m2/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz2_m3/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz2_m5/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz3_m2/README.md | 165 | 472 |
| results/by_problem/dtlz/dtlz3_m3/README.md | 165 | 472 |
| results/by_problem/dtlz/dtlz3_m5/README.md | 165 | 472 |
| results/by_problem/dtlz/dtlz4_m2/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz4_m3/README.md | 165 | 426 |
| results/by_problem/dtlz/dtlz4_m5/README.md | 165 | 426 |
| results/by_problem/wfg/wfg1_m2/README.md | 194 | 645 |
| results/by_problem/wfg/wfg1_m3/README.md | 163 | 396 |
| results/by_problem/wfg/wfg1_m5/README.md | 163 | 396 |
| results/by_problem/wfg/wfg4_m2/README.md | 194 | 645 |
| results/by_problem/wfg/wfg4_m3/README.md | 163 | 396 |
| results/by_problem/wfg/wfg4_m5/README.md | 163 | 396 |
| results/by_problem/wfg/wfg6_m2/README.md | 194 | 645 |
| results/by_problem/wfg/wfg6_m3/README.md | 163 | 396 |
| results/by_problem/wfg/wfg6_m5/README.md | 163 | 396 |
| results/by_problem/wfg/wfg9_m2/README.md | 194 | 645 |
| results/by_problem/wfg/wfg9_m3/README.md | 163 | 396 |
| results/by_problem/wfg/wfg9_m5/README.md | 163 | 396 |
| results/by_problem/zdt/zdt1/README.md | 523 | 1056 |
| results/by_problem/zdt/zdt2/README.md | 523 | 1056 |
| results/by_problem/zdt/zdt3/README.md | 523 | 1056 |
| results/by_problem/zdt/zdt4/README.md | 523 | 1059 |
| results/by_problem/zdt/zdt6/README.md | 523 | 1157 |

## ZDT strengths, limitations and extension direction

The root READMEs now explicitly distinguish observed ZDT benefits, algorithm/evidence limitations and future research stages. Quality, dispersion and runtime statements were checked against the per-problem benchmark summaries. DTLZ/WFG results remain supplementary evidence; proposed telemetry, uncertainty, parameter-confirmation and other-problem studies are not represented as completed. The seven embedded figures remain intact.

## Remaining evidence limits

Archived blocks without execution manifests retain unknown execution environments. Confidence intervals for paired effects are not present in the current report tables. Held-out restart telemetry was not saved. These limits are stated in the problem reports; they are not filled with invented details.
