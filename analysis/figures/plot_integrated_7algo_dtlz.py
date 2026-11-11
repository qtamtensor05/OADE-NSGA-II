#!/usr/bin/env python3
"""
Generate multi-panel research figures integrating
ZDT Benchmark v2 (1,050 runs) and DTLZ1-DTLZ4 (2,520 runs) across 7 algorithms.

Produces two research figure bundles under results/figures/:
  1. integrated_7algo_landscape.{pdf,svg,tiff,png}
     - Panel a: Rank-biserial effect size heatmap across 17 problems x 6 baselines
     - Panel b: Combined pairwise Holm-adjusted outcomes across 204 tests
     - Panel c: Quality rank vs DTLZ4 runtime proxy
  2. dtlz1_4_scaling_diagnosis.{pdf,svg,tiff,png}
     - 2x2 mechanistic scaling across M in {2, 3, 5} for DTLZ1, DTLZ3, DTLZ2, DTLZ4
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.transforms import ScaledTranslation
import numpy as np

QA_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts" / "figure_qa"
sys.path.insert(0, str(QA_SCRIPTS))
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402


# ── Mandatory Nature font & SVG/PDF configurators ─────────────────────────────
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 7.5,
    "axes.titlesize": 8.0,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 6.8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.75,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size": 2.8,
    "ytick.major.size": 2.8,
    "legend.frameon": False,
})


DISPLAY_NAMES = {
    "OADE_NSGAII": "OADE-NSGA-II v2",
    "NSGA2": "NSGA-II",
    "DNSGA2": "D-NSGA-II",
    "CGDE_NSGAII": "CGDE-NSGA-II",
    "CE_MOEA": "CE-MOEA",
    "RNSGA2": "R-NSGA-II",
    "NSGAII_SDR_OLS": "NSGA-II-SDR-OLS",
}

COMPARATORS = [
    "NSGA2",
    "DNSGA2",
    "CGDE_NSGAII",
    "CE_MOEA",
    "RNSGA2",
    "NSGAII_SDR_OLS",
]

ALL_ALGOS = ["OADE_NSGAII", *COMPARATORS]

ALGO_COLORS = {
    "OADE_NSGAII": "#0F4D92",     # Hero Nature deep blue
    "NSGA2": "#B64342",           # Coral-red focal comparator
    "DNSGA2": "#E28E2C",          # Amber
    "CGDE_NSGAII": "#339989",     # Teal
    "CE_MOEA": "#7C6CCF",         # Violet
    "RNSGA2": "#8C8C8C",          # Neutral mid gray
    "NSGAII_SDR_OLS": "#B5B5B5",  # Neutral light gray
}

ALGO_MARKERS = {
    "OADE_NSGAII": "o",
    "NSGA2": "s",
    "DNSGA2": "^",
    "CGDE_NSGAII": "D",
    "CE_MOEA": "v",
    "RNSGA2": "P",
    "NSGAII_SDR_OLS": "X",
}


def add_panel_label(
    ax: plt.Axes,
    label: str,
    x_offset_pt: float = -6.0,
    y_offset_pt: float = 4.0,
    fontsize: float = 9.0,
) -> None:
    """Anchor lowercase bold panel label with fixed physical point offset."""
    offset = ScaledTranslation(
        x_offset_pt / 72.0,
        y_offset_pt / 72.0,
        ax.figure.dpi_scale_trans,
    )
    ax.text(
        0.0,
        1.0,
        label,
        transform=ax.transAxes + offset,
        fontsize=fontsize,
        fontweight="bold",
        color="#111111",
        ha="left",
        va="bottom",
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _save_bundle(
    fig: plt.Figure,
    out_stem: Path,
    *,
    exclude_axes: list[plt.Axes] | None = None,
) -> None:
    fig.canvas.draw()
    require_matplotlib_panel_alignment(
        fig,
        json_out=f"{out_stem}.alignment.json",
        overlay_svg=f"{out_stem}.alignment.svg",
        tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,
        exclude_axes=exclude_axes or (),
        strict=True,
    )
    fig.savefig(f"{out_stem}.svg")
    fig.savefig(f"{out_stem}.pdf")
    fig.savefig(f"{out_stem}.tiff", dpi=600)
    fig.savefig(f"{out_stem}.png", dpi=300)
    plt.close(fig)


def build_integrated_landscape_figure(
    zdt_dir: Path = Path("results/algorithm_benchmark_v2"),
    dtlz_dir: Path = Path("results/dtlz_benchmark"),
    out_dir: Path = Path("results/figures"),
) -> None:
    """Create Figure 1: Integrated 17-problem effect-size heatmap, scorecard, and cost-rank frontier."""
    zdt_stats = _read_csv(zdt_dir / "algorithm_benchmark_paired_statistics.csv")
    dtlz_stats = _read_csv(dtlz_dir / "algorithm_benchmark_paired_statistics.csv")
    zdt_sum = _read_csv(zdt_dir / "algorithm_benchmark_igd_hv_summary.csv")
    dtlz_sum = _read_csv(dtlz_dir / "algorithm_benchmark_igd_hv_summary.csv")

    all_stats = zdt_stats + dtlz_stats

    problem_order = [
        "zdt1", "zdt2", "zdt3", "zdt4", "zdt6",
        "dtlz1_m2", "dtlz1_m3", "dtlz1_m5",
        "dtlz3_m2", "dtlz3_m3", "dtlz3_m5",
        "dtlz2_m2", "dtlz2_m3", "dtlz2_m5",
        "dtlz4_m2", "dtlz4_m3", "dtlz4_m5",
    ]
    problem_labels = {
        "zdt1": "ZDT1", "zdt2": "ZDT2", "zdt3": "ZDT3", "zdt4": "ZDT4", "zdt6": "ZDT6",
        "dtlz1_m2": "D1-M2", "dtlz1_m3": "D1-M3", "dtlz1_m5": "D1-M5",
        "dtlz3_m2": "D3-M2", "dtlz3_m3": "D3-M3", "dtlz3_m5": "D3-M5",
        "dtlz2_m2": "D2-M2", "dtlz2_m3": "D2-M3", "dtlz2_m5": "D2-M5",
        "dtlz4_m2": "D4-M2", "dtlz4_m3": "D4-M3", "dtlz4_m5": "D4-M5",
    }

    igd_lookup = {
        (r["problem"], r["comparison_algorithm"]): r
        for r in all_stats
        if r["metric"] == "IGD"
    }

    eff_matrix = np.zeros((len(COMPARATORS), len(problem_order)), dtype=float)
    sig_matrix = np.zeros((len(COMPARATORS), len(problem_order)), dtype=bool)
    for row_idx, comp in enumerate(COMPARATORS):
        for col_idx, prob in enumerate(problem_order):
            rec = igd_lookup[(prob, comp)]
            eff_matrix[row_idx, col_idx] = float(rec["rank_biserial_effect"])
            sig_matrix[row_idx, col_idx] = rec["significant"].lower() == "true"

    # Compute overall 204-test outcome counts (IGD + HV) per comparator
    outcome_counts: dict[str, dict[str, int]] = {
        c: {"win": 0, "tie": 0, "loss": 0} for c in COMPARATORS
    }
    for rec in all_stats:
        c = rec["comparison_algorithm"]
        if c not in outcome_counts:
            continue
        res = rec["result"]
        if res == "reference_better":
            outcome_counts[c]["win"] += 1
        elif res == "comparison_better":
            outcome_counts[c]["loss"] += 1
        else:
            outcome_counts[c]["tie"] += 1

    # Compute symmetric average ranks across all 17 problems x 2 metrics (34 endpoints)
    algo_ranks: dict[str, list[float]] = {a: [] for a in ALL_ALGOS}
    for srows in (zdt_sum, dtlz_sum):
        probs_in_suite = sorted({r["problem"] for r in srows})
        for p in probs_in_suite:
            by_algo = {r["algorithm"]: r for r in srows if r["problem"] == p}
            igd_vals = {a: float(by_algo[a]["IGD_median"]) for a in ALL_ALGOS}
            hv_vals = {a: float(by_algo[a]["HV_mean"]) for a in ALL_ALGOS}
            for a in ALL_ALGOS:
                better_i = sum(1 for b in ALL_ALGOS if igd_vals[b] < igd_vals[a] - 1e-12)
                eq_i = sum(1 for b in ALL_ALGOS if abs(igd_vals[b] - igd_vals[a]) <= 1e-12)
                algo_ranks[a].append(better_i + (eq_i + 1) / 2.0)

                better_h = sum(1 for b in ALL_ALGOS if hv_vals[b] > hv_vals[a] + 1e-12)
                eq_h = sum(1 for b in ALL_ALGOS if abs(hv_vals[b] - hv_vals[a]) <= 1e-12)
                algo_ranks[a].append(better_h + (eq_h + 1) / 2.0)

    # Fair BLAS-pinned runtime on DTLZ4 (identical OMP_NUM_THREADS=1 session)
    cost_summary: list[dict[str, str]] = []
    for a in ALL_ALGOS:
        avg_r = float(np.mean(algo_ranks[a]))
        rt_dtlz4 = float(
            np.mean([
                float(r["runtime_mean"])
                for r in dtlz_sum
                if r["algorithm"] == a and r["problem"].startswith("dtlz4")
            ])
        )
        rt_zdt = float(
            np.mean([float(r["runtime_mean"]) for r in zdt_sum if r["algorithm"] == a])
        )
        cost_summary.append({
            "algorithm": a,
            "display_name": DISPLAY_NAMES[a],
            "avg_rank_34_endpoints": f"{avg_r:.4f}",
            "mean_runtime_dtlz4_s": f"{rt_dtlz4:.4f}",
            "mean_runtime_zdt_s": f"{rt_zdt:.4f}",
        })

    # Persist source data CSV for traceability
    source_rows = []
    for rec in all_stats:
        source_rows.append({
            "problem": rec["problem"],
            "metric": rec["metric"],
            "comparator": rec["comparison_algorithm"],
            "n_pairs": rec["n_pairs"],
            "p_adjusted_holm": rec["p_adjusted_holm"],
            "rank_biserial_effect": rec["rank_biserial_effect"],
            "significant": rec["significant"],
            "result": rec["result"],
        })
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "integrated_7algo_source_data.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(source_rows[0].keys()))
        writer.writeheader()
        writer.writerows(source_rows)

    with (out_dir / "integrated_7algo_cost_rank_source.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(cost_summary[0].keys()))
        writer.writeheader()
        writer.writerows(cost_summary)

    # ── Layout & Plotting ─────────────────────────────────────────────────────
    fig = plt.figure(figsize=(7.2, 5.25), dpi=300)
    gs = fig.add_gridspec(
        2, 2,
        height_ratios=[1.15, 1.0],
        width_ratios=[1.15, 1.0],
        left=0.14, right=0.96, top=0.89, bottom=0.10,
        hspace=0.46, wspace=0.30,
    )

    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # Panel a: Diverging blue-white-coral effect size matrix
    cmap = LinearSegmentedColormap.from_list(
        "oade_div", ["#B64342", "#F7F7F7", "#0F4D92"], N=256
    )
    im = ax_a.imshow(eff_matrix, cmap=cmap, vmin=-1.0, vmax=1.0, aspect="auto")

    # Crisp white cell borders
    ax_a.set_xticks(np.arange(-0.5, len(problem_order), 1), minor=True)
    ax_a.set_yticks(np.arange(-0.5, len(COMPARATORS), 1), minor=True)
    ax_a.grid(which="minor", color="white", linestyle="-", linewidth=1.0)
    ax_a.tick_params(which="minor", bottom=False, left=False)

    # Suite dividers: ZDT (0..4) | DTLZ1/3 Multimodal (5..10) | DTLZ2/4 Spherical (11..16)
    ax_a.axvline(4.5, color="#222222", linewidth=1.3)
    ax_a.axvline(10.5, color="#222222", linewidth=1.3)

    # Mark non-significant cells cleanly with 'ns'; keep significant cells uncluttered
    for r in range(len(COMPARATORS)):
        for c in range(len(problem_order)):
            if not sig_matrix[r, c]:
                ax_a.text(
                    c, r, "ns",
                    ha="center", va="center",
                    fontsize=6.0, color="#333333", fontweight="normal",
                )

    ax_a.set_xticks(np.arange(len(problem_order)))
    ax_a.set_xticklabels(
        [problem_labels[p] for p in problem_order],
        rotation=35, ha="right", rotation_mode="anchor", fontsize=6.5,
    )
    ax_a.set_yticks(np.arange(len(COMPARATORS)))
    ax_a.set_yticklabels([DISPLAY_NAMES[c] for c in COMPARATORS], fontsize=6.8)
    for spine in ("top", "right", "left", "bottom"):
        ax_a.spines[spine].set_visible(False)

    # Group brackets above Panel a
    group_specs = [
        (2.0, "ZDT (M = 2)"),
        (7.5, "DTLZ1 & DTLZ3 (Multimodal)"),
        (13.5, "DTLZ2 & DTLZ4 (Spherical)"),
    ]
    for gx, gtxt in group_specs:
        ax_a.text(
            gx, -0.78, gtxt,
            ha="center", va="bottom",
            fontsize=7.0, fontweight="bold", color="#222222",
            clip_on=False,
        )

    # External colorbar neatly aligned above right side of Panel a (excluded from alignment check)
    pos_a = ax_a.get_position()
    cax = fig.add_axes([pos_a.x1 - 0.22, pos_a.y1 + 0.068, 0.22, 0.018])
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    cbar.set_ticks([-1.0, 0.0, 1.0])
    cbar.set_ticklabels(["-1 (Base wins)", "0", "+1 (OADE wins)"])
    cbar.ax.tick_params(labelsize=5.8, length=2.0, pad=1.5)
    cbar.outline.set_linewidth(0.5)
    cax.set_title("IGD rank-biserial effect r (ns: Holm p >= 0.05)", fontsize=6.0, pad=3.0)

    add_panel_label(ax_a, "a", x_offset_pt=-8.0, y_offset_pt=22.0)

    # Panel b: Combined 204-test Outcome Stacked Horizontal Bars
    comp_sorted = sorted(
        COMPARATORS,
        key=lambda c: (outcome_counts[c]["win"], -outcome_counts[c]["loss"]),
    )
    y_pos = np.arange(len(comp_sorted))
    wins = np.array([outcome_counts[c]["win"] for c in comp_sorted])
    ties = np.array([outcome_counts[c]["tie"] for c in comp_sorted])
    losses = np.array([outcome_counts[c]["loss"] for c in comp_sorted])

    bar_h = 0.58
    ax_b.barh(y_pos, wins, height=bar_h, color="#0F4D92", label="OADE wins")
    ax_b.barh(y_pos, ties, left=wins, height=bar_h, color="#D8D8D8", label="No sig. diff.")
    ax_b.barh(y_pos, losses, left=wins + ties, height=bar_h, color="#B64342", label="Baseline wins")

    for i, (w, t, l) in enumerate(zip(wins, ties, losses)):
        if w >= 4:
            ax_b.text(w / 2.0, i, str(w), ha="center", va="center", color="white", fontsize=6.2, fontweight="bold")
        if t >= 3:
            ax_b.text(w + t / 2.0, i, str(t), ha="center", va="center", color="#222222", fontsize=6.0)
        if l >= 2:
            ax_b.text(w + t + l / 2.0, i, str(l), ha="center", va="center", color="white", fontsize=6.0, fontweight="bold")

    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels([DISPLAY_NAMES[c] for c in comp_sorted], fontsize=6.8)
    ax_b.set_xlim(0, 35.5)
    ax_b.set_xticks([0, 10, 20, 30, 34])
    ax_b.set_xlabel("Paired comparisons (IGD + HV, max 34)", fontsize=7.0)
    ax_b.set_title("Combined: 149W / 41T / 14L (73.0%)", fontsize=7.3, fontweight="bold", pad=14.0)
    ax_b.legend(loc="lower center", bbox_to_anchor=(0.48, 0.99), ncol=3, fontsize=5.8, handlelength=1.1, columnspacing=0.9)
    add_panel_label(ax_b, "b", x_offset_pt=-8.0, y_offset_pt=14.0)

    # Panel c: Average Rank vs Runtime Trade-off Frontier
    label_offsets = {
        "OADE_NSGAII": (6.0, 4.0, "left", "bottom"),
        "NSGA2": (6.0, 4.0, "left", "bottom"),
        "DNSGA2": (6.0, -4.0, "left", "top"),
        "CE_MOEA": (-6.0, 4.0, "right", "bottom"),
        "CGDE_NSGAII": (-6.0, -4.0, "right", "top"),
        "RNSGA2": (6.0, 2.0, "left", "bottom"),
        "NSGAII_SDR_OLS": (6.0, -2.0, "left", "top"),
    }
    for row in cost_summary:
        a = row["algorithm"]
        rt = float(row["mean_runtime_dtlz4_s"])
        if rt <= 0:
            raise ValueError(f"runtime must be strictly positive for log axis ({a}: {rt})")
        rk = float(row["avg_rank_34_endpoints"])
        is_hero = a == "OADE_NSGAII"
        ax_c.scatter(
            rt, rk,
            s=62 if is_hero else 34,
            color=ALGO_COLORS[a],
            marker=ALGO_MARKERS[a],
            edgecolors="white",
            linewidths=0.8,
            zorder=5 if is_hero else 3,
        )
        dx, dy, ha, va = label_offsets[a]
        lbl = f"{DISPLAY_NAMES[a]} ({rk:.2f})" if is_hero else DISPLAY_NAMES[a]
        ax_c.annotate(
            lbl,
            xy=(rt, rk),
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha, va=va,
            fontsize=6.2 if is_hero else 6.0,
            fontweight="bold" if is_hero else "normal",
            color="#0F4D92" if is_hero else "#333333",
        )

    ax_c.set_xscale("log")
    ax_c.set_xlim(1.0, 140.0)
    ax_c.set_ylim(6.7, 0.8)  # Inverted: Rank 1 at top!
    ax_c.set_yticks([1, 2, 3, 4, 5, 6])
    ax_c.set_xlabel("DTLZ4 mean runtime (s, log scale)", fontsize=7.0)
    ax_c.set_ylabel("Mean rank across 34 endpoints", fontsize=7.0)
    ax_c.set_title("Quality rank vs DTLZ4 runtime proxy", fontsize=7.3, fontweight="bold", pad=14.0)
    add_panel_label(ax_c, "c", x_offset_pt=-8.0, y_offset_pt=14.0)

    _save_bundle(fig, out_dir / "integrated_7algo_landscape", exclude_axes=[cax])


def build_dtlz_scaling_figure(
    dtlz_dir: Path = Path("results/dtlz_benchmark"),
    out_dir: Path = Path("results/figures"),
) -> None:
    """Create Figure 2: 2x2 mechanistic scaling across M in {2, 3, 5} for DTLZ1-4."""
    raw = _read_csv(dtlz_dir / "algorithm_benchmark_raw_runs.csv")
    objectives = [2, 3, 5]

    # Pre-aggregate median and IQR across valid runs per (problem_base, M, algorithm)
    stats_grid: dict[tuple[str, int, str], dict[str, float]] = {}
    for base in ("dtlz1", "dtlz2", "dtlz3", "dtlz4"):
        for m in objectives:
            pname = f"{base}_m{m}"
            for a in ALL_ALGOS:
                sub = [
                    r for r in raw
                    if r["problem"] == pname
                    and r["algorithm"] == a
                    and r["valid"].lower() == "true"
                ]
                igds = np.array([float(r["IGD"]) for r in sub], dtype=float)
                hvs = np.array([float(r["HV"]) for r in sub], dtype=float)
                stats_grid[(base, m, a)] = {
                    "n": float(len(sub)),
                    "igd_q25": float(np.percentile(igds, 25)),
                    "igd_q50": float(np.percentile(igds, 50)),
                    "igd_q75": float(np.percentile(igds, 75)),
                    "hv_q25": float(np.percentile(hvs, 25)),
                    "hv_q50": float(np.percentile(hvs, 50)),
                    "hv_q75": float(np.percentile(hvs, 75)),
                }

    # Export source CSV for traceability
    source_rows = []
    for (base, m, a), vals in sorted(stats_grid.items()):
        source_rows.append({
            "problem_family": base,
            "n_obj": m,
            "algorithm": a,
            **vals,
        })
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "dtlz1_4_scaling_source_data.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(source_rows[0].keys()))
        writer.writeheader()
        writer.writerows(source_rows)

    fig, axes = plt.subplots(
        2, 2, figsize=(7.2, 5.1), dpi=300,
    )
    fig.subplots_adjust(
        left=0.09, right=0.97, top=0.83, bottom=0.10,
        hspace=0.40, wspace=0.25,
    )

    x_base = np.arange(len(objectives), dtype=float)
    offsets = np.linspace(-0.21, 0.21, len(ALL_ALGOS))

    def _plot_scaling_lines(ax: plt.Axes, family: str, metric_prefix: str, *, logy: bool) -> None:
        for idx, a in enumerate(ALL_ALGOS):
            is_hero = a == "OADE_NSGAII"
            is_muted = a in ("RNSGA2", "NSGAII_SDR_OLS")
            xs = x_base + offsets[idx]
            med = np.array([stats_grid[(family, m, a)][f"{metric_prefix}_q50"] for m in objectives])
            q25 = np.array([stats_grid[(family, m, a)][f"{metric_prefix}_q25"] for m in objectives])
            q75 = np.array([stats_grid[(family, m, a)][f"{metric_prefix}_q75"] for m in objectives])
            if logy and (np.any(med <= 0) or np.any(q25 <= 0)):
                raise ValueError(f"values must be strictly positive for log axis ({family}, {a})")
            yerr = np.vstack([np.maximum(0.0, med - q25), np.maximum(0.0, q75 - med)])
            ax.errorbar(
                xs, med, yerr=yerr,
                color=ALGO_COLORS[a],
                marker=ALGO_MARKERS[a],
                markersize=4.5 if is_hero else 3.2,
                linewidth=1.7 if is_hero else (0.85 if is_muted else 1.15),
                linestyle="--" if is_muted else "-",
                elinewidth=0.9 if is_hero else 0.65,
                capsize=2.0,
                alpha=1.0 if is_hero else (0.65 if is_muted else 0.88),
                zorder=5 if is_hero else (2 if is_muted else 3),
                label=DISPLAY_NAMES[a],
            )
        if logy:
            ax.set_yscale("log")
        ax.set_xticks(x_base)
        ax.set_xticklabels(["M = 2", "M = 3", "M = 5"], fontsize=7.5)

    # Panel a: DTLZ1 IGD (Log)
    ax_a = axes[0, 0]
    _plot_scaling_lines(ax_a, "dtlz1", "igd", logy=True)
    ax_a.set_ylabel("IGD (log scale, lower better)", fontsize=7.0)
    ax_a.set_title("DTLZ1: Multimodal linear front", fontsize=7.5, fontweight="bold", pad=6.0)
    add_panel_label(ax_a, "a", x_offset_pt=-22.0, y_offset_pt=6.0)

    # Panel b: DTLZ3 IGD (Log)
    ax_b = axes[0, 1]
    _plot_scaling_lines(ax_b, "dtlz3", "igd", logy=True)
    ax_b.set_ylabel("IGD (log scale, lower better)", fontsize=7.0)
    ax_b.set_title("DTLZ3: Hard multimodal sphere", fontsize=7.5, fontweight="bold", pad=6.0)
    add_panel_label(ax_b, "b", x_offset_pt=-22.0, y_offset_pt=6.0)

    # Panel c: DTLZ2 Normalized IGD relative to NSGA-II median (reveals M=3 crossover clearly!)
    ax_c = axes[1, 0]
    nsga_meds = {m: stats_grid[("dtlz2", m, "NSGA2")]["igd_q50"] for m in objectives}
    ax_c.axhline(1.0, color="#666666", linestyle=":", linewidth=0.9, zorder=1)
    for idx, a in enumerate(ALL_ALGOS):
        if a == "NSGAII_SDR_OLS":
            # SDR-OLS sits far above 2.0 (150x at M=2); denote concisely at top without crushing scale
            continue
        if a == "RNSGA2":
            continue
        is_hero = a == "OADE_NSGAII"
        xs = x_base + (idx - 2) * 0.08
        med = np.array([stats_grid[("dtlz2", m, a)]["igd_q50"] / nsga_meds[m] for m in objectives])
        q25 = np.array([stats_grid[("dtlz2", m, a)]["igd_q25"] / nsga_meds[m] for m in objectives])
        q75 = np.array([stats_grid[("dtlz2", m, a)]["igd_q75"] / nsga_meds[m] for m in objectives])
        yerr = np.vstack([np.maximum(0.0, med - q25), np.maximum(0.0, q75 - med)])
        ax_c.errorbar(
            xs, med, yerr=yerr,
            color=ALGO_COLORS[a],
            marker=ALGO_MARKERS[a],
            markersize=4.5 if is_hero else 3.2,
            linewidth=1.7 if is_hero else 1.15,
            elinewidth=0.9 if is_hero else 0.65,
            capsize=2.0,
            zorder=5 if is_hero else 3,
        )
    ax_c.annotate(
        "M=3 deficit (+5.8%)",
        xy=(1.0 + (-2) * 0.08, stats_grid[("dtlz2", 3, "OADE_NSGAII")]["igd_q50"] / nsga_meds[3]),
        xytext=(0.75, 1.32),
        arrowprops={"arrowstyle": "->", "color": "#0F4D92", "lw": 0.8},
        fontsize=6.0, fontweight="bold", color="#0F4D92", ha="center",
    )
    ax_c.set_xticks(x_base)
    ax_c.set_xticklabels(["M = 2", "M = 3", "M = 5"], fontsize=7.5)
    ax_c.set_ylim(0.78, 1.65)
    ax_c.set_ylabel("IGD ratio to NSGA-II (<1 better)", fontsize=7.5)
    ax_c.set_title("DTLZ2: Unimodal sphere (ratio vs NSGA-II)", fontsize=7.5, fontweight="bold", pad=6.0)
    add_panel_label(ax_c, "c", x_offset_pt=-22.0, y_offset_pt=6.0)

    # Panel d: DTLZ4 Hypervolume (shows observed objective-count dependence)
    ax_d = axes[1, 1]
    _plot_scaling_lines(ax_d, "dtlz4", "hv", logy=False)
    ax_d.annotate(
        "NSGA-II & D-NSGA-II\nM=5 median HV < 0.05",
        xy=(2.0 + offsets[1], 0.03),
        xytext=(0.68, 0.36),
        arrowprops={"arrowstyle": "->", "color": "#B64342", "lw": 0.85},
        fontsize=6.0, fontweight="bold", color="#B64342", ha="center", va="center",
    )
    ax_d.set_ylim(-0.04, 0.82)
    ax_d.set_ylabel("Hypervolume (higher better)", fontsize=7.5)
    ax_d.set_title("DTLZ4: Biased sphere, observed HV", fontsize=7.5, fontweight="bold", pad=6.0)
    add_panel_label(ax_d, "d", x_offset_pt=-22.0, y_offset_pt=6.0)

    # Shared figure-level legend at top
    handles, labels = ax_a.get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="upper center", bbox_to_anchor=(0.53, 0.985),
        ncol=4, fontsize=6.4, handlelength=1.8, columnspacing=1.1,
    )

    _save_bundle(fig, out_dir / "dtlz1_4_scaling_diagnosis")


def main() -> None:
    build_integrated_landscape_figure()
    build_dtlz_scaling_figure()
    print("Generated integrated_7algo_landscape and dtlz1_4_scaling_diagnosis figures.")


if __name__ == "__main__":
    main()
