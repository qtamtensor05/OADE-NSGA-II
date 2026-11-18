# Figure QA — mechanism study

Device exception: the static validator flags `EDITABLE-TEXT` because it requires a `cairo_pdf()` call. This is a false positive for the selected base `pdf()` device: final PDFs contain Helvetica text runs (glyph audit reads them), and SVG retains text. Testing Cairo on this runtime combined distant labels into oversized text-trace boxes, producing false collision failures. Final exports therefore use base PDF; their collision audits report zero FAIL/WARN. This documented device exception resolves the static finding by inspection rather than claiming the static tool passed. No fonts were outlined and no scientific content was rasterized in PDF/SVG.

Contract: quantitative grid answering whether all components improve full OADE equally. R is the saved plotting backend. Generic research-report exports, not certification for a named journal. Width 183 mm; heatmap 105 mm high, paired figure 175 mm high. PDF/SVG are vector, PNG is a 300 dpi preview. No TIFF submission raster requested.

All 480 runs are retained in the audited input. Heatmap includes all 28 endpoints. Paired IGD shows 420 comparisons; the source CSV also preserves 420 HV comparisons. No seed exclusions; jitter changes category position only. Heatmap color is rank-biserial, not percent improvement; NS is explicit. Dark median markers supplement all paired observations without claiming confidence intervals. Pseudo-log sigma=0.001 permits negative/zero values; axis ranges differ by problem and must not be compared as equal distances.

| Panel | Evidence role | Summary / spread | Unit | QA |
|---|---|---|---|---|
| Heatmap | Conditional direction and Holm decisions | Rank-biserial / no CI | 30 paired seeds per cell | Labels legible; intentional contained text in cells; single panel, alignment N/A |
| Paired a, ZDT4 | Failure tails and divergent component effects | Median and all 30 points per contrast | Paired seed | Labels clear; all tails retained; alignment PASS |
| Paired b, ZDT6 | Boundary where DE-only improves | Same as a | Paired seed | Labels clear; denser values use explicit small-number ticks; alignment PASS |

Automated source preflight, PDF glyph audit (floor 5 pt), and final rendered collision audits accompany generation. Static warnings about missing TIFF/600 dpi are accepted for vector report delivery with 300 dpi preview. Width is assigned through a variable (183 mm). Seed summary warning is resolved by plotting every paired observation and explicitly stating that no CI is drawn. R source execution provides syntax verification. Both complete PNGs and each panel were visually inspected; no clipping or ambiguous label overlap was observed. Alignment compares actual R viewports within 1.5 pt. Collision JSON files are preserved; fully contained heatmap text is intentional. Re-run audits after edits.
