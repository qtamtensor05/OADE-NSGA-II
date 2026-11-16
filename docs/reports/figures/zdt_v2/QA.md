# Figure contract and QA

## Log-scale IGD overview

`igd_log_comparison` replaces the full-range IGD bars in the report and README.
All 35 groups use median points and Q1–Q3 segments, computed from all 1,049 valid
observations; CGDE ZDT4 has 29 runs, all other groups 30. A common positive log10
range is used across the five panels. No pseudocount, clipping or new exclusion
is applied. Median/IQR replace mean/SD explicitly because mean-minus-SD is
negative for some skewed groups and cannot be displayed on a logarithmic axis.
The full distributions and mean tables retain the large-error tails.

The R-generated PNG was reviewed panel by panel. Rendered panel alignment,
PDF text floor (minimum 7 pt) and collision checks passed with no failures or
warnings. PDF/SVG/PNG and source CSV are provided. To regenerate only this view,
append `docs/reports/figures/zdt_v2 --log-only` to the Rscript command below.

## Bar-chart addition

Three R figures (`hv_bars`, `igd_bars_focus` and `hv_bars_focus`)
show audited arithmetic means with one SD. All panels use linear axes starting
at zero. Negative mean-minus-SD whiskers are displayed at zero; source SDs remain
unchanged. The full HV view contains all 35 algorithm/problem groups. Focus views
contain the 15 OADE/NSGA2/DNSGA2 groups, selected explicitly by comparator identity,
with mean labels to five decimal places. No valid seeds are excluded from a group.
These views use 183 × 240 mm pages. All three passed rendered alignment, PDF text
floor and collision audits (zero failures/warnings). All panels were visually
reviewed. The obsolete full IGD bars and associated source/QA artifacts were
removed after replacement by the log-scale overview; the script no longer
generates them. Focus views provide readable comparisons without truncating bar
axes. The bars do not encode significance or replace paired tests.

To regenerate just the bars, append
`docs/reports/figures/zdt_v2 --bars-only` to the Rscript command below.

These report figures describe the audited five-problem ZDT v2 benchmark. They
do not establish performance beyond this dataset or isolate OADE mechanisms.
R is the exclusive plotting backend. Vector exports are 183 mm wide; distribution
figures are 220 mm high and the paired-effect overview is 92 mm high. PNG previews
are 300 dpi; TIFF submission files are outside this report export contract.

Evidence roles:

- `paired_effects`: matched-seed rank-biserial effects, qualified by the prespecified
  Holm family of 60 tests. Four NS endpoints remain visible.
- `igd_distribution`: convergence quality and large-error tails on a log axis.
- `hv_distribution`: full-front coverage, including legitimate zero HV values.
- `runtime_distribution`: measured implementation cost, not complexity or FE-based
  convergence speed.

Quality uses 1,049/1,050 runs. The only exclusion is the prespecified CGDE ZDT4
seed 63 collapsed front. Runtime uses all 1,050 completed runs. No observations
are sampled, clipped or removed as statistical outliers. Horizontal jitter is
zero; vertical jitter has a fixed seed. Boxplots show quartiles, median and 1.5-IQR
whiskers, not confidence intervals. Each problem has its own metric range.

All three five-panel layouts passed the rendered viewport alignment gate at
1.5 pt tolerance, without exemptions. The project helper measures resolved
viewports on a Cairo device because direct conversion of unresolved gtable null
units in the bundled helper returns zero width/height on this stack. Authoritative
PDFs use R's Helvetica PDF device, avoiding Cairo's combined text traces that
cause spurious text-overlap reports in the geometry auditor. SVG and PNG remain
direct R exports.

PDF text audits passed the 5 pt floor (minimum 7 pt). Collision audits for all
three distribution figures passed with zero failures or warnings. The paired
effect overview has zero failures and two warnings at the end labels of its
colour bar. Visual review confirms that both labels sit below the colour bar
with readable clearance; the warnings are harmless bounding-box interactions
with the legend region. NS text inside tiles and points inside boxes are
intentional overlays. Automated outputs are stored next to the figures.

Every full PNG and every problem panel was visually reviewed: labels readable,
no clipping, consistent algorithm order, OADE highlighted, ZDT4 tails retained.
The full-range HV figure intentionally resolves broad coverage rather than the
very small differences between leading methods; the audited tables and paired
effect overview supply that complementary information.

Reproduce from the repository root:

```powershell
& 'C:/Program Files/R/R-4.6.2/bin/Rscript.exe' --vanilla analysis/plot_zdt_comparison.R
```

`R-session.txt`, `input-checksums.csv` and `*.source.csv` record package versions,
input identity and plotted observations. No optimisation or new inferential test
is run. Static preflight reports one device-rule failure because it recognises
only `cairo_pdf`, while the authoritative export uses `grDevices::pdf` with
Helvetica and editable text. PDF text extraction and the text/collision audits
verify the actual output; this static finding is a documented false positive,
not a claim that the source preflight passed. Warnings about TIFF/600 dpi are
outside the chosen vector-plus-preview export contract; the log axis is explicitly guarded
by finite and positive-value assertions before drawing.
