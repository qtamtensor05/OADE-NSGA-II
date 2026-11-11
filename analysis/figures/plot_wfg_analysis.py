#!/usr/bin/env python3
"""
Generate multi-panel research figures for the WFG benchmark studies:
  1. wfg_m2_7algo_profile.{pdf,svg,tiff,png}
     - Full 7-algorithm bi-objective validation (WFG1, WFG4, WFG6, WFG9 at M=2; 840 runs)
     - Panel a: Holm-adjusted rank-biserial effect sizes across IGD and HV (48 tests)
     - Panel b: Raw-seed IGD escape from deceptive WFG9 (M=2) across all 7 algorithms
     - Panel c: 8-endpoint combined rank vs BLAS-pinned runtime trade-off at M=2
  2. wfg_scaling_diagnosis.{pdf,svg,tiff,png}
     - 5-fast-algorithm objective scaling M in {2, 3, 5} & convergence dynamics (1,800 runs)
     - Panel a: Holm-adjusted outcome transition across M=2 -> 3 -> 5 (96 tests)
     - Panel b: Paired IGD ratio (OADE / NSGA-II) across WFG landscapes and M
     - Panel c: Within-budget HV trajectory on WFG1 (M=5)
     - Panel d: Within-budget HV trajectory on WFG9 (M=5)
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.transforms import ScaledTranslation
import numpy as np

QA_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts" / "figure_qa"
sys.path.insert(0, str(QA_SCRIPTS))
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402


mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 7.5,
    "axes.titlesize": 7.8,
    "axes.labelsize": 7.2,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 6.8,
    "legend.fontsize": 6.4,
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

COMPARATORS_7 = [
    "CGDE_NSGAII",
    "NSGA2",
    "DNSGA2",
    "CE_MOEA",
    "NSGAII_SDR_OLS",
    "RNSGA2",
]
ALL_7_ALGOS = ["OADE_NSGAII", *COMPARATORS_7]
FAST_5_ALGOS = ["OADE_NSGAII", "NSGA2", "DNSGA2", "NSGAII_SDR_OLS", "RNSGA2"]

ALGO_COLORS = {
    "OADE_NSGAII": "#0F4D92",
    "NSGA2": "#B64342",
    "DNSGA2": "#E28E2C",
    "CGDE_NSGAII": "#339989",
    "CE_MOEA": "#7C6CCF",
    "NSGAII_SDR_OLS": "#2A7B6F",
    "RNSGA2": "#8C8C8C",
}

ALGO_MARKERS = {
    "OADE_NSGAII": "o",
    "NSGA2": "s",
    "DNSGA2": "^",
    "CGDE_NSGAII": "D",
    "CE_MOEA": "v",
    "NSGAII_SDR_OLS": "X",
    "RNSGA2": "P",
}

PROBLEM_COLORS = {
    "wfg1": "#0F4D92",
    "wfg9": "#2A7B6F",
    "wfg6": "#E28E2C",
    "wfg4": "#B64342",
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


def build_wfg_m2_7algo_figure(
    data_dir: Path = Path("results/wfg_m2_7algo_benchmark"),
    out_dir: Path = Path("results/figures"),
) -> None:
    """Create Figure 1: Full 7-algorithm M=2 WFG inferential profile, WFG9 escape, and cost trade-off."""
    raw = _read_csv(data_dir / "algorithm_benchmark_raw_runs.csv")
    stats = _read_csv(data_dir / "algorithm_benchmark_paired_statistics.csv")
    summary = _read_csv(data_dir / "algorithm_benchmark_igd_hv_summary.csv")

    prob_order = ["wfg1_m2", "wfg4_m2", "wfg6_m2", "wfg9_m2"]
    prob_short = {"wfg1_m2": "WFG1", "wfg4_m2": "WFG4", "wfg6_m2": "WFG6", "wfg9_m2": "WFG9"}
    col_specs = [(p, "IGD") for p in prob_order] + [(p, "HV") for p in prob_order]

    stat_map = {
        (r["problem"], r["metric"], r["comparison_algorithm"]): r
        for r in stats
    }
    eff_mat = np.zeros((len(COMPARATORS_7), len(col_specs)), dtype=float)
    sig_mat = np.zeros((len(COMPARATORS_7), len(col_specs)), dtype=bool)
    for r_idx, comp in enumerate(COMPARATORS_7):
        for c_idx, (prob, metric) in enumerate(col_specs):
            rec = stat_map[(prob, metric, comp)]
            eff_mat[r_idx, c_idx] = float(rec["rank_biserial_effect"])
            sig_mat[r_idx, c_idx] = rec["significant"].lower() == "true"

    # Compute 8-endpoint combined descriptive rank (median IGD/HV) & mean runtime across 4 M=2 problems
    algo_ranks: dict[str, list[float]] = {a: [] for a in ALL_7_ALGOS}
    for prob in prob_order:
        by_a = {r["algorithm"]: r for r in summary if r["problem"] == prob}
        igd_vals = {a: float(by_a[a]["IGD_median"]) for a in ALL_7_ALGOS}
        hv_vals = {a: float(by_a[a]["HV_median"]) for a in ALL_7_ALGOS}
        for a in ALL_7_ALGOS:
            better_i = sum(1 for b in ALL_7_ALGOS if igd_vals[b] < igd_vals[a] - 1e-12)
            eq_i = sum(1 for b in ALL_7_ALGOS if abs(igd_vals[b] - igd_vals[a]) <= 1e-12)
            algo_ranks[a].append(better_i + (eq_i + 1) / 2.0)

            better_h = sum(1 for b in ALL_7_ALGOS if hv_vals[b] > hv_vals[a] + 1e-12)
            eq_h = sum(1 for b in ALL_7_ALGOS if abs(hv_vals[b] - hv_vals[a]) <= 1e-12)
            algo_ranks[a].append(better_h + (eq_h + 1) / 2.0)

    cost_rows = []
    for a in ALL_7_ALGOS:
        rts = [
            float(r["runtime_mean"])
            for r in summary
            if r["algorithm"] == a
        ]
        cost_rows.append({
            "algorithm": a,
            "display_name": DISPLAY_NAMES[a],
            "mean_rank_8_endpoints": f"{float(np.mean(algo_ranks[a])):.4f}",
            "runtime_mean_s": f"{float(np.mean(rts)):.4f}",
            "runtime_min_s": f"{float(np.min(rts)):.4f}",
            "runtime_max_s": f"{float(np.max(rts)):.4f}",
        })

    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "wfg_m2_7algo_source_data.csv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "problem", "metric", "comparator", "n_pairs",
            "p_adjusted_holm", "rank_biserial_effect", "significant", "result",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in stats:
            w.writerow({
                "problem": r["problem"],
                "metric": r["metric"],
                "comparator": r["comparison_algorithm"],
                "n_pairs": r["n_pairs"],
                "p_adjusted_holm": r["p_adjusted_holm"],
                "rank_biserial_effect": r["rank_biserial_effect"],
                "significant": r["significant"],
                "result": r["result"],
            })

    with (out_dir / "wfg_m2_7algo_cost_rank_source.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cost_rows[0].keys()))
        w.writeheader()
        w.writerows(cost_rows)

    # ── Figure Canvas & Layout ────────────────────────────────────────────────
    fig = plt.figure(figsize=(7.2, 5.25), dpi=300)
    gs = fig.add_gridspec(
        2, 2,
        height_ratios=[1.12, 1.0],
        width_ratios=[1.18, 1.0],
        left=0.145, right=0.95, top=0.885, bottom=0.10,
        hspace=0.47, wspace=0.29,
    )
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # Panel a: 6 comparators x 8 endpoints effect size matrix (IGD | HV)
    cmap = LinearSegmentedColormap.from_list("oade_div", ["#B64342", "#F7F7F7", "#0F4D92"], N=256)
    im = ax_a.imshow(eff_mat, cmap=cmap, vmin=-1.0, vmax=1.0, aspect="auto")

    ax_a.set_xticks(np.arange(-0.5, len(col_specs), 1), minor=True)
    ax_a.set_yticks(np.arange(-0.5, len(COMPARATORS_7), 1), minor=True)
    ax_a.grid(which="minor", color="white", linestyle="-", linewidth=1.1)
    ax_a.tick_params(which="minor", bottom=False, left=False)
    ax_a.axvline(3.5, color="#111111", linewidth=1.4)

    for r_idx in range(len(COMPARATORS_7)):
        for c_idx in range(len(col_specs)):
            val = eff_mat[r_idx, c_idx]
            txt_color = "white" if abs(val) >= 0.55 else "#222222"
            suffix = "" if sig_mat[r_idx, c_idx] else " (ns)"
            ax_a.text(
                c_idx, r_idx, f"{val:+.2f}{suffix}",
                ha="center", va="center", fontsize=6.0,
                fontweight="bold" if val < 0 else "normal",
                color=txt_color,
            )

    ax_a.set_xticks(np.arange(len(col_specs)))
    ax_a.set_xticklabels([prob_short[p] for p, _ in col_specs], fontsize=6.8)
    ax_a.set_yticks(np.arange(len(COMPARATORS_7)))
    ax_a.set_yticklabels([DISPLAY_NAMES[c] for c in COMPARATORS_7], fontsize=6.8)
    for spine in ("top", "right", "left", "bottom"):
        ax_a.spines[spine].set_visible(False)

    ax_a.text(1.5, -0.78, "IGD comparison (M = 2)", ha="center", va="bottom",
              fontsize=7.0, fontweight="bold", color="#222222", clip_on=False)
    ax_a.text(5.5, -0.78, "Hypervolume comparison (M = 2)", ha="center", va="bottom",
              fontsize=7.0, fontweight="bold", color="#222222", clip_on=False)

    pos_a = ax_a.get_position()
    cax = fig.add_axes([pos_a.x1 - 0.255, pos_a.y1 + 0.068, 0.22, 0.018])
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    cbar.set_ticks([-1.0, 0.0, 1.0])
    cbar.set_ticklabels(["-1 (Base wins)", "0", "+1 (OADE wins)"])
    cbar.ax.tick_params(labelsize=5.8, length=2.0, pad=1.5)
    cbar.outline.set_linewidth(0.5)
    cax.set_title("Holm rank-biserial effect r (42W / 0T / 6L)", fontsize=6.0, pad=3.0)
    add_panel_label(ax_a, "a", x_offset_pt=-8.0, y_offset_pt=20.0)

    # Panel b: Raw-seed IGD distributions on non-separable deceptive WFG9 (M=2, n=30)
    wfg9_order = [
        "RNSGA2",
        "NSGAII_SDR_OLS",
        "CE_MOEA",
        "CGDE_NSGAII",
        "DNSGA2",
        "NSGA2",
        "OADE_NSGAII",
    ]
    wfg9_data = []
    for a in wfg9_order:
        vals = np.array([
            float(r["IGD"])
            for r in raw
            if r["problem"] == "wfg9_m2" and r["algorithm"] == a and r["valid"].lower() == "true"
        ], dtype=float)
        if np.any(vals <= 0.0):
            raise ValueError(f"WFG9 IGD must be strictly positive for log axis ({a})")
        wfg9_data.append(vals)

    y_pos = np.arange(len(wfg9_order), dtype=float)
    bp = ax_b.boxplot(
        wfg9_data,
        positions=y_pos,
        orientation="horizontal",
        widths=0.52,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#111111", "linewidth": 1.2},
        whiskerprops={"color": "#555555", "linewidth": 0.75},
        capprops={"color": "#555555", "linewidth": 0.75},
        boxprops={"linewidth": 0.75},
    )
    for idx, (box, a) in enumerate(zip(bp["boxes"], wfg9_order)):
        box.set_facecolor(ALGO_COLORS[a])
        box.set_alpha(0.35 if a != "OADE_NSGAII" else 0.55)
        box.set_edgecolor(ALGO_COLORS[a])

    for idx, (vals, a) in enumerate(zip(wfg9_data, wfg9_order)):
        jitter = (np.mod(np.arange(len(vals), dtype=float) * 0.6180339, 1.0) - 0.5) * 0.28
        ax_b.scatter(
            vals,
            np.full_like(vals, y_pos[idx]) + jitter,
            s=8.5 if a == "OADE_NSGAII" else 6.0,
            color=ALGO_COLORS[a],
            alpha=0.85 if a == "OADE_NSGAII" else 0.65,
            edgecolors="none",
            zorder=4,
        )

    nsga_med = float(np.median(wfg9_data[wfg9_order.index("NSGA2")]))
    oade_med = float(np.median(wfg9_data[wfg9_order.index("OADE_NSGAII")]))
    ax_b.axvline(nsga_med, color="#B64342", linestyle=":", linewidth=0.95, zorder=2)
    ax_b.annotate(
        f"Several baselines\n(~{nsga_med:.2f} IGD)",
        xy=(nsga_med, 3.0),
        xytext=(0.24, 5.25),
        arrowprops={"arrowstyle": "->", "color": "#B64342", "lw": 0.8},
        fontsize=6.0, color="#B64342", fontweight="bold", ha="left", va="center",
    )
    ax_b.annotate(
        f"OADE median ({oade_med:.3f})",
        xy=(oade_med + 0.005, 6.18),
        xytext=(0.16, 6.70),
        arrowprops={"arrowstyle": "->", "color": "#0F4D92", "lw": 0.8},
        fontsize=6.0, color="#0F4D92", fontweight="bold", ha="left", va="center",
    )

    ax_b.set_xscale("log")
    ax_b.set_xlim(0.022, 1.05)
    ax_b.set_ylim(-0.6, 7.25)
    ax_b.set_xticks([0.03, 0.05, 0.1, 0.2, 0.5, 1.0])
    ax_b.set_xticklabels(["0.03", "0.05", "0.1", "0.2", "0.5", "1.0"], fontsize=6.4)
    ax_b.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels([DISPLAY_NAMES[a] for a in wfg9_order], fontsize=6.5)
    ax_b.set_xlabel("WFG9 (M = 2) IGD (log scale, n = 30)", fontsize=7.0)
    ax_b.set_title("WFG9 final IGD (M = 2)", fontsize=7.3, fontweight="bold", pad=10.0)
    add_panel_label(ax_b, "b", x_offset_pt=-8.0, y_offset_pt=10.0)

    # Panel c: Combined 8-endpoint rank vs BLAS-pinned mean runtime at M=2
    offsets_c = {
        "OADE_NSGAII": (6.0, 2.0, "left", "bottom"),
        "NSGA2": (6.0, 2.0, "left", "bottom"),
        "DNSGA2": (6.0, -3.0, "left", "top"),
        "CGDE_NSGAII": (-6.0, 3.0, "right", "bottom"),
        "CE_MOEA": (-6.0, -3.5, "right", "top"),
        "NSGAII_SDR_OLS": (6.0, 2.0, "left", "bottom"),
        "RNSGA2": (6.0, -2.0, "left", "top"),
    }
    for row in cost_rows:
        a = row["algorithm"]
        rt = float(row["runtime_mean_s"])
        rt_lo = float(row["runtime_min_s"])
        rt_hi = float(row["runtime_max_s"])
        rk = float(row["mean_rank_8_endpoints"])
        if rt <= 0 or rt_lo <= 0:
            raise ValueError(f"runtime must be strictly positive for log axis ({a}: {rt})")
        is_hero = a == "OADE_NSGAII"
        ax_c.hlines(rk, rt_lo, rt_hi, color=ALGO_COLORS[a], linewidth=0.9, alpha=0.55, zorder=2)
        ax_c.scatter(
            rt, rk,
            s=62 if is_hero else 34,
            color=ALGO_COLORS[a],
            marker=ALGO_MARKERS[a],
            edgecolors="white",
            linewidths=0.8,
            zorder=5 if is_hero else 3,
        )
        dx, dy, ha, va = offsets_c[a]
        lbl = f"{DISPLAY_NAMES[a]} ({rk:.2f})" if is_hero else DISPLAY_NAMES[a]
        ax_c.annotate(
            lbl,
            xy=(rt, rk),
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha, va=va,
            fontsize=6.1 if is_hero else 5.9,
            fontweight="bold" if is_hero else "normal",
            color="#0F4D92" if is_hero else "#333333",
        )

    ax_c.annotate(
        "DE/CE ~41x slower\nin these runs",
        xy=(14.0, 1.95),
        xytext=(55.0, 2.15),
        arrowprops={"arrowstyle": "->", "color": "#0F4D92", "lw": 0.75, "ls": "--"},
        fontsize=5.9, color="#0F4D92", fontweight="bold", ha="left", va="center",
    )

    ax_c.set_xscale("log")
    ax_c.set_xlim(2.0, 680.0)
    ax_c.set_xticks([3, 10, 30, 100, 300])
    ax_c.set_xticklabels(["3", "10", "30", "100", "300"], fontsize=6.4)
    ax_c.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax_c.set_ylim(7.35, 1.05)
    ax_c.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax_c.set_xlabel("Mean runtime on WFG M = 2 (s, log scale)", fontsize=7.0)
    ax_c.set_ylabel("Mean rank across 8 endpoints", fontsize=7.0)
    ax_c.set_title("M = 2 quality rank vs runtime", fontsize=7.3, fontweight="bold", pad=10.0)
    add_panel_label(ax_c, "c", x_offset_pt=-8.0, y_offset_pt=10.0)

    _save_bundle(fig, out_dir / "wfg_m2_7algo_profile", exclude_axes=[cax])


def build_wfg_scaling_figure(
    compact_dir: Path = Path("results/wfg_compact_benchmark"),
    out_dir: Path = Path("results/figures"),
) -> None:
    """Create Figure 2: 2x2 WFG scaling shift (M=2->3->5) and within-budget convergence dynamics."""
    raw = _read_csv(compact_dir / "algorithm_benchmark_raw_runs.csv")
    stats = _read_csv(compact_dir / "algorithm_benchmark_paired_statistics.csv")
    conv = _read_csv(compact_dir / "algorithm_benchmark_convergence.csv")
    cost = _read_csv(compact_dir / "algorithm_benchmark_cost_summary.csv")

    objectives = [2, 3, 5]
    prob_bases = ["wfg1", "wfg9", "wfg6", "wfg4"]
    prob_labels = {
        "wfg1": "WFG1 (biased/flat)",
        "wfg9": "WFG9 (non-sep. deceptive)",
        "wfg6": "WFG6 (non-separable)",
        "wfg4": "WFG4 (sep. concave)",
    }

    # Panel a counts by M
    wtl_by_m: dict[int, tuple[int, int, int]] = {}
    for m in objectives:
        c = Counter(
            r["result"] for r in stats
            if r["problem"].endswith(f"_m{m}")
        )
        wtl_by_m[m] = (
            c.get("reference_better", 0),
            c.get("no_significant_difference", 0),
            c.get("comparison_better", 0),
        )

    # Panel b paired IGD ratio: IGD_OADE / IGD_NSGA2 for each matched seed (strictly > 0)
    raw_idx = {
        (r["problem"], r["algorithm"], int(r["run_idx"])): r
        for r in raw
        if r["valid"].lower() == "true"
    }
    ratio_grid: dict[tuple[str, int], dict[str, float]] = {}
    for pbase in prob_bases:
        for m in objectives:
            pname = f"{pbase}_m{m}"
            ratios = []
            for run_idx in range(30):
                o_row = raw_idx[(pname, "OADE_NSGAII", run_idx)]
                n_row = raw_idx[(pname, "NSGA2", run_idx)]
                o_igd = float(o_row["IGD"])
                n_igd = float(n_row["IGD"])
                if o_igd <= 0.0 or n_igd <= 0.0:
                    raise ValueError(f"Non-positive IGD on {pname} run {run_idx}")
                ratios.append(o_igd / n_igd)
            arr = np.asarray(ratios, dtype=float)
            ratio_grid[(pbase, m)] = {
                "n": float(len(arr)),
                "q25": float(np.percentile(arr, 25)),
                "q50": float(np.percentile(arr, 50)),
                "q75": float(np.percentile(arr, 75)),
            }

    # Panels c & d convergence trajectories: checkpoints 0.1..0.9 (n=30 exact) + final raw (n=30 exact)
    conv_map: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for r in conv:
        conv_map[(r["problem"], r["algorithm"], r["checkpoint_fraction"])].append(float(r["HV"]))

    cost_eval_map = {
        (r["problem"], r["algorithm"]): float(r["n_eval_mean"])
        for r in cost
    }

    trajectories: dict[tuple[str, str], list[dict[str, float]]] = {}
    for pname in ("wfg1_m5", "wfg9_m5"):
        for a in FAST_5_ALGOS:
            pts: list[dict[str, float]] = []
            for k in range(1, 10):
                fr = str(k / 10.0)
                vals = np.asarray(conv_map[(pname, a, fr)], dtype=float)
                if len(vals) != 30:
                    raise ValueError(f"Expected 30 runs at {pname} {a} {fr}, found {len(vals)}")
                pts.append({
                    "evals_k": float(k * 2.0),
                    "q25": float(np.percentile(vals, 25)),
                    "q50": float(np.percentile(vals, 50)),
                    "q75": float(np.percentile(vals, 75)),
                    "n": float(len(vals)),
                })
            final_vals = np.asarray([
                float(raw_idx[(pname, a, run_idx)]["HV"])
                for run_idx in range(30)
            ], dtype=float)
            pts.append({
                "evals_k": cost_eval_map[(pname, a)] / 1000.0,
                "q25": float(np.percentile(final_vals, 25)),
                "q50": float(np.percentile(final_vals, 50)),
                "q75": float(np.percentile(final_vals, 75)),
                "n": float(len(final_vals)),
            })
            trajectories[(pname, a)] = pts

    # Save complete source data CSV for Figure 2
    out_dir.mkdir(parents=True, exist_ok=True)
    source_rows = []
    for (pbase, m), vals in sorted(ratio_grid.items()):
        source_rows.append({
            "panel": "b_paired_igd_ratio",
            "series": pbase,
            "x_coord": m,
            **vals,
        })
    for (pname, a), pts in trajectories.items():
        for pt in pts:
            source_rows.append({
                "panel": f"cd_hv_{pname}",
                "series": a,
                "x_coord": pt["evals_k"],
                "n": pt["n"],
                "q25": pt["q25"],
                "q50": pt["q50"],
                "q75": pt["q75"],
            })
    with (out_dir / "wfg_scaling_source_data.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["panel", "series", "x_coord", "n", "q25", "q50", "q75"])
        w.writeheader()
        w.writerows(source_rows)

    # ── 2x2 Strict Symmetric Grid ─────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.15), dpi=300)
    fig.subplots_adjust(
        left=0.095, right=0.97, top=0.84, bottom=0.10,
        hspace=0.45, wspace=0.25,
    )

    # Panel a: 100%-stacked Holm outcome counts across M=2, 3, 5
    ax_a = axes[0, 0]
    x_m = np.arange(len(objectives), dtype=float)
    wins = np.array([wtl_by_m[m][0] for m in objectives], dtype=float)
    ties = np.array([wtl_by_m[m][1] for m in objectives], dtype=float)
    losses = np.array([wtl_by_m[m][2] for m in objectives], dtype=float)

    bar_w = 0.52
    ax_a.bar(x_m, wins, width=bar_w, color="#0F4D92", label="OADE wins")
    ax_a.bar(x_m, ties, bottom=wins, width=bar_w, color="#D8D8D8", label="No sig. diff.")
    ax_a.bar(x_m, losses, bottom=wins + ties, width=bar_w, color="#B64342", label="Baseline wins")

    for i, (w_val, t_val, l_val) in enumerate(zip(wins, ties, losses)):
        if w_val >= 3:
            ax_a.text(i, w_val / 2.0, f"{int(w_val)}W", ha="center", va="center",
                      color="white", fontsize=6.4, fontweight="bold")
        if t_val >= 3:
            ax_a.text(i, w_val + t_val / 2.0, f"{int(t_val)}T", ha="center", va="center",
                      color="#222222", fontsize=6.0)
        if l_val >= 3:
            ax_a.text(i, w_val + t_val + l_val / 2.0, f"{int(l_val)}L", ha="center", va="center",
                      color="white", fontsize=6.4, fontweight="bold")

    ax_a.set_xticks(x_m)
    ax_a.set_xticklabels([f"M = {m}" for m in objectives], fontsize=7.2)
    ax_a.set_ylim(0, 36.5)
    ax_a.set_yticks([0, 8, 16, 24, 32])
    ax_a.set_ylabel("Holm tests per M (max 32)", fontsize=7.0)
    ax_a.set_title("5-algo scaling: 87.5% to 34.4% wins", fontsize=7.3, fontweight="bold", pad=12.0)
    ax_a.legend(loc="lower center", bbox_to_anchor=(0.50, 0.96), ncol=3,
                fontsize=5.8, handlelength=1.0, columnspacing=0.8)
    add_panel_label(ax_a, "a", x_offset_pt=-22.0, y_offset_pt=12.0)

    # Panel b: Paired IGD ratio (OADE / NSGA-II) across M=2, 3, 5
    ax_b = axes[0, 1]
    ax_b.axhline(1.0, color="#555555", linestyle=":", linewidth=0.95, zorder=1)
    offsets_b = np.linspace(-0.12, 0.12, len(prob_bases))
    markers_b = {"wfg1": "o", "wfg9": "s", "wfg6": "^", "wfg4": "D"}
    for idx, pbase in enumerate(prob_bases):
        xs = x_m + offsets_b[idx]
        med = np.array([ratio_grid[(pbase, m)]["q50"] for m in objectives])
        q25 = np.array([ratio_grid[(pbase, m)]["q25"] for m in objectives])
        q75 = np.array([ratio_grid[(pbase, m)]["q75"] for m in objectives])
        yerr = np.vstack([np.maximum(0.0, med - q25), np.maximum(0.0, q75 - med)])
        ax_b.errorbar(
            xs, med, yerr=yerr,
            color=PROBLEM_COLORS[pbase],
            marker=markers_b[pbase],
            markersize=3.8,
            linewidth=1.35,
            elinewidth=0.75,
            capsize=2.0,
            label=prob_labels[pbase],
            zorder=4 if pbase in ("wfg1", "wfg9") else 3,
        )

    ax_b.set_xticks(x_m)
    ax_b.set_xticklabels([f"M = {m}" for m in objectives], fontsize=7.2)
    ax_b.set_ylim(0.15, 1.55)
    ax_b.set_yticks([0.25, 0.50, 0.75, 1.00, 1.25, 1.50])
    ax_b.set_ylabel("Paired IGD ratio: OADE / NSGA-II", fontsize=7.0)
    ax_b.set_title("Paired IGD ratio (< 1.0: OADE better)", fontsize=7.3, fontweight="bold", pad=12.0)
    ax_b.legend(loc="lower right", fontsize=5.8, handlelength=1.4, ncol=1)
    add_panel_label(ax_b, "b", x_offset_pt=-22.0, y_offset_pt=12.0)

    # Shared trajectory helper for Panels c and d
    def _plot_hv_traj(ax: plt.Axes, pname: str, title_txt: str, label_char: str) -> None:
        for a in FAST_5_ALGOS:
            is_hero = a == "OADE_NSGAII"
            is_muted = a == "RNSGA2"
            pts = trajectories[(pname, a)]
            xs = np.array([pt["evals_k"] for pt in pts])
            q25 = np.array([pt["q25"] for pt in pts])
            q50 = np.array([pt["q50"] for pt in pts])
            q75 = np.array([pt["q75"] for pt in pts])
            assert np.all(np.diff(xs) > 0), f"Non-monotone evaluation coordinates on {pname} {a}"
            ax.fill_between(
                xs, q25, q75,
                color=ALGO_COLORS[a],
                alpha=0.14 if is_hero else 0.08,
                linewidth=0,
                zorder=2,
            )
            ax.plot(
                xs, q50,
                color=ALGO_COLORS[a],
                linewidth=1.65 if is_hero else (0.9 if is_muted else 1.15),
                linestyle="--" if is_muted else "-",
                alpha=1.0 if is_hero else (0.72 if is_muted else 0.90),
                marker="o" if is_hero else None,
                markersize=2.4 if is_hero else 0.0,
                zorder=5 if is_hero else (2 if is_muted else 3),
                label=DISPLAY_NAMES[a],
            )
        ax.set_xlim(1.5, 20.6)
        ax.set_xticks([2, 6, 10, 14, 18, 20])
        ax.set_xlabel("Function evaluations (thousands)", fontsize=7.0)
        ax.set_ylabel("Hypervolume median (IQR)", fontsize=7.0)
        ax.set_title(title_txt, fontsize=7.3, fontweight="bold", pad=6.0)
        add_panel_label(ax, label_char, x_offset_pt=-22.0, y_offset_pt=6.0)

    # Panel c: WFG1 (M=5) convergence
    ax_c = axes[1, 0]
    _plot_hv_traj(ax_c, "wfg1_m5", "WFG1 (M = 5): Early jump then plateau", "c")
    ax_c.set_ylim(-60, 1490)
    ax_c.annotate(
        "OADE 1284 at 2k",
        xy=(2.0, 1283.63),
        xytext=(5.2, 1130),
        arrowprops={"arrowstyle": "->", "color": "#0F4D92", "lw": 0.8},
        fontsize=6.0, fontweight="bold", color="#0F4D92", ha="left", va="center",
    )

    # Panel d: WFG9 (M=5) convergence crossover
    ax_d = axes[1, 1]
    _plot_hv_traj(ax_d, "wfg9_m5", "WFG9 (M = 5): Early lead overtaken by SBX", "d")
    ax_d.set_ylim(340, 1490)
    ax_d.annotate(
        "Crossover ~5k evals",
        xy=(5.0, 1045),
        xytext=(6.2, 670),
        arrowprops={"arrowstyle": "->", "color": "#B64342", "lw": 0.8},
        fontsize=6.0, fontweight="bold", color="#B64342", ha="left", va="center",
    )

    # Bottom/middle shared legend specifically for the 5 algorithms in Panels c and d
    handles_cd, labels_cd = ax_c.get_legend_handles_labels()
    fig.legend(
        handles_cd, labels_cd,
        loc="upper center", bbox_to_anchor=(0.53, 0.98),
        ncol=5, fontsize=6.0, handlelength=1.4, columnspacing=0.95,
    )
    fig.text(
        0.53, 0.992,
        "Panels c–d trajectories (5 fast algorithms, n = 30 paired runs each)",
        ha="center", va="top", fontsize=6.2, color="#444444",
    )

    _save_bundle(fig, out_dir / "wfg_scaling_diagnosis")


def main() -> None:
    build_wfg_m2_7algo_figure()
    build_wfg_scaling_figure()
    print("Generated wfg_m2_7algo_profile and wfg_scaling_diagnosis figures.")


if __name__ == "__main__":
    main()
