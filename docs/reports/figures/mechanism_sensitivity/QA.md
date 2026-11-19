# Figure contract and QA — parameter-level sensitivity

Question: how do numeric levels alter paired final quality and its seed-to-seed spread? Core conclusion: effects depend on parameter, problem and metric; a clear dose trend is not evidence of a universal optimum. Archetype: quantitative grid. Overview figures carry paired inference; ten detail figures expose every observation, spread and failure tail. No optimizer was rerun. Drawing, final exports and previews use R only, with the project's established viewport-measurement helper.

## Data and export contract

- Input: audited comparisons (124), audited summary groups (70), run rows (2,100) and audit JSON. Each overview retains 62 endpoints; each detail panel contains every one of its 30 seeds per level. No exclusions or subsampling. A reference group reappears in several detail files for context; this does not create extra replication.
- Reference: full production for static parameters; matched single-parameter held reference for F/CR/pDE. Held reference values are 0.65/0.5/0.5. Ordered category axes retain actual level labels, including the reference in numeric order; spacing is categorical, not numeric distance.
- Paired benefit: 100 times median(reference−level) / observed reference median for IGD; sign reversed for HV. Positive favors the tested level. CI bounds are the existing marginal paired-bootstrap bounds, transformed by the same fixed denominator/sign; no ratio uncertainty is inferred. IGD overview uses signed pseudo-log (sigma=1 percentage point), HV overview linear. Panels have their own ranges. All CI bounds remain visible.
- Overview colors: teal ZDT4, brown ZDT6; point fill additionally encodes the fixed Holm decision. Open is NS, not equivalence. Black diamond is the deterministic reference at zero. A two-line caption explains all encodings; no duplicated or clipped legend remains. CI is unadjusted 95%, while point fill uses Holm across 124 endpoints.
- Detail: all points, sample median, Q1–Q3 box and 1.5 IQR whiskers. IGD coordinate transform is applied after statistics, preserving original-scale median/quartiles. HV linear axes may zoom to data; no bars or zero-based magnitude claim. Jitter is horizontal only (seed 42), not measurement perturbation. Shapes and box fills are descriptive, not significance marks.
- Dimensions: 183 mm wide; overview 265 mm high, detail 170 mm high. Generic report assets, not certification for a named journal. Editable PDF/SVG plus white-background 300 dpi PNG preview; no TIFF submission raster requested. Input hashes and R session information are preserved alongside source CSVs.

## Automated gates and tool exception

All 12 final PDFs pass glyph-floor audit (minimum required 5 pt), collision audit (zero FAIL and zero WARN), and render-time viewport alignment within 1.5 pt. Alignment reports, glyph JSON and collision JSON/text are stored per figure. Overview contained-fill overlays are intentional marker/text geometry classified by the tool; visual inspection found no obscured labels. These automated gates do not test statistical validity.

Source preflight has a known false positive: it demands a `cairo_pdf()` call for editable text. Base `pdf()` actually preserves Helvetica text operators, read successfully by the glyph audit; SVG independently preserves text. Cairo previously coalesced separated labels into large trace boxes on this runtime, making geometry inspection unreliable. The base-PDF device is retained as a documented exception; the static tool is not claimed to pass. Other warnings (300 dpi preview rather than 600 dpi/TIFF, basic static syntax checker) are resolved by vector delivery, the stated preview purpose and successful execution by R. Source-preflight output is preserved.

## Panel-by-panel visual review

All panels below were inspected individually in the final R-generated PNGs and as complete figures. Names a–j follow the parameter order used by the script. All labels, intervals, point directions, tails, level ordering, reference markers and repeated axis conventions were reviewed. No clipping or ambiguous text overlap remains.

| Figure | Panels inspected | Distinct evidence | Center / uncertainty | Unit | Labels, alignment, collision |
|---|---|---|---|---|---|
| Paired IGD overview | a, b, c, d, e, f, g, h, i, j | Paired direction and scale across levels; long ZDT4 tails retained | Paired median / marginal bootstrap 95% CI | 30 paired seeds/endpoint | PASS for every panel |
| Paired HV overview | a, b, c, d, e, f, g, h, i, j | Small HV changes and endpoint-specific Holm decisions | Same paired definition / same CI rule | 30 paired seeds/endpoint | PASS for every panel |
| OBL interval | a, b, c, d | Frequency dependence and quality tails | All points, median, IQR, 1.5 IQR whiskers | 30 seeds/level/problem | PASS for every panel |
| OBL jump rate | a, b, c, d | Low-rate failure boundary on ZDT4 | Same distribution definition | Same | PASS for every panel |
| Stagnation patience | a, b, c, d | Quality despite changing restart exposure | Same distribution definition | Same | PASS for every panel |
| Stagnation tolerance | a, b, c, d | Flat paired medians versus marginal quality variation | Same distribution definition | Same | PASS for every panel |
| Diversity threshold | a, b, c, d | Quality boundary of activation-threshold changes | Same distribution definition | Same | PASS for every panel |
| Restart elite ratio | a, b, c, d | Preserved-elite level effects within the tested regime | Same distribution definition | Same | PASS for every panel |
| DE neighbors | a, b, c, d | Local-neighborhood size and outlier tails | Same distribution definition | Same | PASS for every panel |
| Mean F held | a, b, c, d | Opposing problem-specific response to held F | Same distribution definition | Same | PASS for every panel |
| Mean CR held | a, b, c, d | Small HV changes and high-CR boundary | Same distribution definition | Same | PASS for every panel |
| pDE held | a, b, c, d | DE-share response and distinct IGD/HV behavior | Same distribution definition | Same | PASS for every panel |

Single-parameter grids intentionally use problem/metric-specific y ranges. Do not interpret marginal box overlap as a paired test, colors as overall ranks, or isolated significance as a tested interaction. Full interpretations and formulas are in the linked figure gallery and audited report.
