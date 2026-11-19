# Figure QA — current six-solver evidence

Input study: `zdt_six_fixed_oade_v1`. R-only export; PNG 300 dpi, editable SVG and base-R PDF. See `export_audit.json` for checksums and text/collision results. Multipanel alignment JSON files use final-device viewport measurements (1.5 pt tolerance); single panels do not require this gate.

All PNGs were visually reviewed: readable axes and captions, no clipped labels; all five problems retained. IGD distributions and runtime use log view transformations with box statistics on the raw scale; the IGD overview shows raw-scale medians/IQR on a common log axis. HV retains zero values. Quality uses 899 valid runs; runtime uses all 900. Pareto figures use all 500 stored nondominated solutions from best-IGD seeds, with the five ZDT3 components kept disconnected.

Base PDF is intentional: its editable text is checked directly. The static validator's preferred cairo device rule is not a full pass; no journal submission specification is claimed. This is a documentation figure set.
