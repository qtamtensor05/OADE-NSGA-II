# Research Figure QA Record

## Shared contract

- Backend: R 4.6.2 with project-local `renv` dependencies.
- Independent unit: one stochastic run.
- Replication: 30 runs per algorithm-problem or variant-problem group.
- Export size: figure-specific within 165-180 mm width and 105-125 mm height.
- Formats: editable PDF/SVG, 600-dpi TIFF, and 300-dpi PNG preview.
- Multi-panel alignment: not applicable; each deliverable contains one plot area.

## Benchmark rank heatmap

| Check | Result |
|---|---|
| Unique claim | Shows OADE-NSGA-II's descriptive rank against six baselines across five problems and two metrics |
| Center/summary | Rank of mean IGD or mean HV |
| Spread/interval | Not encoded; the caption directs inferential interpretation to paired statistics |
| Replicate unit | 30 stochastic runs per cell |
| Labels/legend | Short display labels; full canonical names remain in the report and source-data CSV |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS at final physical size; title, cells, labels, legend, and caption are legible |

## Ablation effect heatmap

| Check | Result |
|---|---|
| Unique claim | Shows whether each component removal favours the removal or Full OADE |
| Center/summary | Matched-pairs rank-biserial effect |
| Spread/interval | No confidence interval is available; significant cells mark Holm-adjusted paired tests |
| Replicate unit | 30 paired stochastic runs per cell |
| Labels/legend | Component abbreviations are defined by the report and source-data CSV |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS at final physical size; diverging direction, effect labels, significance markers, legend, and caption are legible |

## Benchmark top-three counts

| Check | Result |
|---|---|
| Unique claim | Summarizes how often each algorithm reaches descriptive ranks 1-3 across ten endpoints |
| Center/summary | Count of endpoint ranks based on 30-run means |
| Spread/interval | Not encoded; the figure explicitly labels ranks as descriptive |
| Replicate unit | 30 stochastic runs underlying each endpoint mean |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS; stacks, counts, legend, labels, and scope caption are legible |

## Benchmark runtime

| Check | Result |
|---|---|
| Unique claim | Compares observed implementation runtime without presenting it as algorithm-independent complexity |
| Center/summary | Mean seconds per run across five problems |
| Spread/interval | Whiskers show the minimum-to-maximum problem-level mean |
| Scale guard | PASS; all plotted runtime values are positive before applying the log scale |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS; log scale, bars, whiskers, labels, and qualification caption are legible |

## ZDT4 and ZDT6 convergence

| Check | Result |
|---|---|
| Unique claim | Shows within-budget median IGD trajectories for selected competitive algorithms |
| Center/summary | Median IGD at each recorded checkpoint fraction |
| Spread/interval | Interquartile band across 30 stochastic runs |
| Selection disclosure | Four algorithms are shown per problem for readability; complete convergence data remain in the benchmark CSV |
| Collision audit | PASS for both PDFs; 0 failures and 0 warnings |
| PDF glyph floor | PASS for both PDFs; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS; trajectories, uncertainty bands, log scale, legend, and captions are legible |

## Corrected ablation outcome counts

| Check | Result |
|---|---|
| Unique claim | Counts corrected Full-better, Removal-better, and unresolved endpoints for each removal |
| Center/summary | Count across five problems and two metrics |
| Inference | Two-sided paired Wilcoxon tests with Holm adjustment; non-significance is not called equivalence |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS; segment direction, counts, legend, and inferential caption are legible |

## Restart paired-run distribution

| Check | Result |
|---|---|
| Unique claim | Shows the run-level distribution of final-quality change after removing restart |
| Center/summary | Boxplot median and interquartile range |
| Replicate unit | Each point is one of 30 paired seeds per endpoint |
| Direction | Positive means No Restart improved IGD by reduction or HV by increase |
| Collision audit | PASS; 0 failures and 0 warnings |
| PDF glyph floor | PASS; minimum 6 pt against a 5 pt requirement |
| Visual inspection | PASS; all endpoints, zero reference, points, boxes, scale, and caption are legible; extreme values are retained |

## Reviewed warnings

- The source validator reports that R syntax should be checked by R itself. `Rscript --vanilla` parsed the complete source successfully.
- The static source validator could not infer the runtime positivity assertion near `scale_x_log10`; the script stops before plotting if any runtime minimum is non-positive.
- The PDF text scanner reports unsupported filters in two streams but still identifies the documents as auditable, finds the minimum 6 pt glyph size, and reports no below-threshold text.
- R prints Windows locale warnings for `C.UTF-8`; exported labels were visually inspected and contain no damaged characters.
