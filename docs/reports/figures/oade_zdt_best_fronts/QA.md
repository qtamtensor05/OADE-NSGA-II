# Best-IGD OADE front figures — contract and QA

Core question: where do exported final OADE solutions lie relative to the true PF in the user-requested best runs? Archetype: quantitative grid. R backend exclusively draws the 183 × 145 mm five-panel overview and five 100 × 90 mm individual plots. No optimizer is run. This is a generic report figure, not journal-specific submission certification.

Selection: minimum final IGD from all 30 OADE runs per ZDT1/2/3/4/6 in ZDT v2; tie broken by smallest seed. Selected seeds: 48/69/65/44/65. One selected run per panel, 100 exported final nondominated points each, 500 total. No uncertainty interval is applicable to this single-run geometry; the caption explicitly identifies best-case selection. Selection is by IGD, not HV; HV labels refer to the same selected records. No point exclusions, subsampling, jitter, interpolation of OADE solutions or combination across seeds.

Pink open circles and connecting paths are the stored reference snapshot, checksum-verified; blue crosses are final F. The reference path follows f1 order; ZDT3's five disconnected segments are independently grouped and never bridged. Paths between sampled reference points are visual guides, not a new analytic evaluation. All axes are linear and use their own ranges; no cross-problem comparison of distances or areas is implied. The visible reference can be partly occluded because final points lie close to it. Color and shape distinguish layers.

The extraction script verifies selected primary checksums, identity and validity, objective reevaluation and stored IGD/HV. Audit source CSVs preserve coordinates, seeds, metrics, reference segments and selection metadata. CSV run summaries determine the selection; full primary audit is documented in the existing benchmark report, not rerun here.

All six final PDFs pass rendered glyph audit (5 pt floor) and collision audit with zero FAIL/WARN. The overview passes actual R-viewport alignment within 1.5 pt; single-panel alignment is N/A. A three-column layout has equal rendered plot widths and row heights. An empty bottom-right grid slot is intentional for the five-problem set, not a missing result. Per-file alignment/glyph/collision reports are retained.

| Panels reviewed | Evidence | Center / spread | Unit | Visual review |
|---|---|---|---|---|
| a / standalone ZDT1 | Coverage of convex PF | No aggregate / no CI | One best-IGD run, 100 points | Labels, endpoints, layer distinction and geometry inspected |
| b / standalone ZDT2 | Coverage of concave PF | Same | Same | Same checks passed |
| c / standalone ZDT3 | Coverage of disconnected PF | Same | Same | Five components visible; no cross-gap path |
| d / standalone ZDT4 | Best-case quality on multimodal problem | Same | Same | All points retained; explicitly best-case, not stability evidence |
| e / standalone ZDT6 | Coverage of restricted f1 range | Same | Same | Appropriate objective limits; all points retained |

Device exception: source preflight requires `cairo_pdf()` for editable vectors, but base `pdf()` preserves Helvetica text and gives separately auditable text traces on this runtime. Actual final PDF glyph inspection and SVG text verify editable text. The static editable-device flag is documented as a false positive, not called a pass. PNG 300 dpi is preview only; vector PDF/SVG are authoritative. Source syntax is verified by execution in R. Static warnings about no TIFF/600 dpi are accepted for this report export contract. Every final overview panel and standalone plot was visually inspected for readable labels, reference visibility, endpoints, clipping and scientific meaning.
