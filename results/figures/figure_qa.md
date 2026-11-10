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

## Restart confirmation paired-run distribution (Held-out seeds)

| Check | Result |
|---|---|
| Unique claim | Confirms run-level IGD and HV improvements of No Restart and Adaptive Restart over Full OADE across 30 held-out seeds |
| Center/summary | Boxplot median and interquartile range (IQR) |
| Replicate unit | 30 independent paired seeds (1000–1029) per endpoint |
| Direction | Positive means comparison algorithm (No Restart or Adaptive Restart) improved over Full OADE |
| Layout / Panels | 2 panels (a: IGD improvement %, b: HV improvement %) with jittered raw points |
| Color / Contrast | Restrained publication palette: `#3182BD` (No Restart) and `#31A354` (Adaptive Restart) |
| Multi-format export | Vector PDF, vector SVG, 300-DPI uncompressed TIFF, and PNG preview |
| Source data CSV | PASS; complete paired run differences exported to `restart_confirmation_paired_source.csv` |
| Visual inspection | PASS; clear labels, zero threshold line, distinct problem separations, legible legend |

## Direct metric comparison across 5 problems (Grouped Boxplots)

| Check | Result |
|---|---|
| Unique claim | Directly displays absolute IGD and HV metric values side-by-side without abstraction |
| Center/summary | Median and IQR with overlaid raw seed jitter points ($n = 30$) |
| Metric clarity | Row 1: IGD with "Lower is better ↓"; Row 2: HV with "Higher is better ↑" |
| Color encoding | `#D95F0E` (Full OADE, warning), `#3182BD` (No Restart), `#31A354` (Adaptive Restart) |
| Multi-format export | `restart_direct_comparison.{pdf,svg,tiff,png}` |
| Visual inspection | PASS; clear problem columns, distinct colors, readable tick marks |

## Evaluation convergence trajectories (Median IGD + IQR band)

| Check | Result |
|---|---|
| Unique claim | Reveals within-budget convergence dynamics and shows perturbation spikes of classic restart |
| Trajectory encoding | Solid/dashed/dotted lines with shaded 25th–75th percentile ribbons |
| X-axis | Exact function evaluations ($0 \dots 20,000$) |
| Multi-format export | `restart_convergence.{pdf,svg,tiff,png}` |
| Visual inspection | PASS; trajectories distinguish stability clearly |

## Benchmark v2 pairwise outcome counts

| Check | Result |
|---|---|
| Unique claim | Visualizes the number of Holm-corrected statistical wins, ties, and losses of OADE v2 against 6 baselines |
| Metric total | 60 comparisons (5 problems × 2 metrics × 6 comparators) |
| Outcome summary | 58 wins (#31A354), 1 tie (#BDBDBD), 1 loss (#E6550D) |
| Multi-format export | `benchmark_v2_outcome_counts.{pdf,svg,png}` |
| Visual inspection | PASS; clear horizontal bar layout, numeric counts inside segments, unambiguous legend |

## Benchmark v2 performance leap (OADE v1 vs v2)

| Check | Result |
|---|---|
| Unique claim | Displays the exact percentage reduction in mean IGD from OADE v1 to OADE v2 across all 5 ZDT problems |
| Direct values | ZDT1: -24.5%, ZDT2: -38.5%, ZDT3: -40.0%, ZDT4: 0.0%, ZDT6: -27.3% |
| Multi-format export | `benchmark_v2_v1_vs_v2_delta.{pdf,svg,png}` |
| Visual inspection | PASS; side-by-side bar comparison with green callout annotations |

## Reviewed warnings

- The source validator reports that R syntax should be checked by R itself. `Rscript --vanilla` parsed the complete source successfully.
- The static source validator could not infer the runtime positivity assertion near `scale_x_log10`; the script stops before plotting if any runtime minimum is non-positive.
- The PDF text scanner reports unsupported filters in two streams but still identifies the documents as auditable, finds the minimum 6 pt glyph size, and reports no below-threshold text.
- R prints Windows locale warnings for `C.UTF-8`; exported labels were visually inspected and contain no damaged characters.

---

## Integrated 7-Algorithm Landscape (`integrated_7algo_landscape`)

| Check | Result |
|---|---|
| Backend | Python 3.14 / Matplotlib 3.11.2 (`analysis/figures/plot_integrated_7algo_dtlz.py`) |
| Unique claim | Synthesizes OADE-NSGA-II v2's Holm-adjusted effect sizes (`a`), 204-test outcome ledger (`b`), and symmetric 34-endpoint rank-runtime trade-off (`c`) across ZDT and DTLZ1–4 |
| Palette & Salience | Colorblind-safe blue-white-coral diverging heatmap (`#0F4D92`, `#F7F7F7`, `#B64342`); hero markers emphasized |
| Source preflight | PASS (`21 pass, 0 warn, 0 fail` via `validate_figure.py`) |
| Multi-panel alignment | PASS (`strict=True` via `require_matplotlib_panel_alignment`; external colorbar excluded from grid alignment) |
| PDF glyph floor | PASS (minimum found `5.25 pt` >= `5.0 pt`; 0 below minimum via `audit_pdf_text.py`) |
| Collision audit | PASS (`0 fail, 0 warn`, 97 text boxes, 101 strokes via `audit_figure_collisions.py`) |
| Export bundle | `integrated_7algo_landscape.{pdf,svg,tiff,png}`, `.alignment.json/.svg`, `integrated_7algo_source_data.csv`, `integrated_7algo_cost_rank_source.csv` |
| Visual inspection | PASS at final double-column width (`182.9 mm`); markers and labels verified free of overlap |

## DTLZ1–4 Multi-Objective Scaling Diagnosis (`dtlz1_4_scaling_diagnosis`)

| Check | Result |
|---|---|
| Backend | Python 3.14 / Matplotlib 3.11.2 (`analysis/figures/plot_integrated_7algo_dtlz.py`) |
| Unique claim | Reveals objective-scaling separation (`a`, `b`: multimodal escape on DTLZ1/3), 3-objective spherical interpolation deficit (`c`: DTLZ2 ratio vs NSGA-II), and 5-objective corner-collapse resistance (`d`: DTLZ4 HV) across $M \in \{2, 3, 5\}$ |
| Center / Spread | Median and interquartile range (25th–75th percentiles) over $n=26$–$30$ valid paired runs per configuration |
| Scale & Exclusion disclosure | Panels `a, b` guard strict positivity for log scale; Panel `c` zooms to `0.78–1.65` ratio vs NSGA-II (omitting off-scale R-NSGA-II & SDR-OLS > 1.5, documented in caption & source CSV) |
| Source preflight | PASS (`21 pass, 0 warn, 0 fail` via `validate_figure.py`) |
| Multi-panel alignment | PASS (`strict=True` via `require_matplotlib_panel_alignment` on 2×2 grid) |
| PDF glyph floor | PASS (minimum found `5.25 pt` >= `5.0 pt`; 0 below minimum via `audit_pdf_text.py`) |
| Collision audit | PASS (`0 fail, 0 warn`, 51 text boxes, 480 strokes via `audit_figure_collisions.py`) |
| Export bundle | `dtlz1_4_scaling_diagnosis.{pdf,svg,tiff,png}`, `.alignment.json/.svg`, `dtlz1_4_scaling_source_data.csv` |
| Visual inspection | PASS; DTLZ4 collapse callout and DTLZ2 `M=3` annotation sit in clear whitespace without touching lines |

