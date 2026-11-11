#!/usr/bin/env python3
"""
Generate Nature-standard publication figures for Benchmark v2.
Compares OADE-NSGA-II v2 against 6 baseline algorithms (NSGA-II, CGDE, SDR-OLS, CE-MOEA, DNSGA-II, RNSGA-II)
and visualizes the massive leap from v1 to v2.
"""

from __future__ import annotations

import csv
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def set_nature_style() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.0,
        "axes.titlesize": 9.0,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 8.0,
        "figure.titlesize": 10.5,
        "axes.linewidth": 0.7,
        "grid.linewidth": 0.4,
        "lines.linewidth": 1.1,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def plot_v2_figures(
    v2_dir: Path = Path("results/algorithm_benchmark_v2"),
    output_dir: Path = Path("results/figures"),
) -> None:
    set_nature_style()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_file = v2_dir / "algorithm_benchmark_igd_hv_summary.csv"
    stat_file = v2_dir / "algorithm_benchmark_paired_statistics.csv"

    # 1. Figure: Corrected Outcome Counts (58 wins, 1 tie, 1 loss)
    # Read statistics
    stat_rows = []
    with open(stat_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            stat_rows.append(r)

    comparators = ["NSGA2", "DNSGA2", "RNSGA2", "CGDE_NSGAII", "NSGAII_SDR_OLS", "CE_MOEA"]
    comp_labels = {
        "NSGA2": "NSGA-II",
        "DNSGA2": "D-NSGA-II",
        "RNSGA2": "R-NSGA-II",
        "CGDE_NSGAII": "CGDE",
        "NSGAII_SDR_OLS": "SDR-OLS",
        "CE_MOEA": "CE-MOEA",
    }
    
    outcomes: dict[str, dict[str, int]] = {
        c: {"OADE better": 0, "No diff": 0, "Comparator better": 0}
        for c in comparators
    }

    for r in stat_rows:
        comp = r["comparison_algorithm"]
        if comp not in outcomes:
            continue
        sig = r["significant"].lower() == "true"
        res = r["result"]
        if sig and res == "reference_better":
            outcomes[comp]["OADE better"] += 1
        elif sig and res == "comparison_better":
            outcomes[comp]["Comparator better"] += 1
        else:
            outcomes[comp]["No diff"] += 1

    fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=300)
    y_pos = np.arange(len(comparators))
    bar_height = 0.55

    oade_better_counts = [outcomes[c]["OADE better"] for c in comparators]
    no_diff_counts = [outcomes[c]["No diff"] for c in comparators]
    comp_better_counts = [outcomes[c]["Comparator better"] for c in comparators]

    p1 = ax.barh(y_pos, oade_better_counts, height=bar_height, color="#31A354", alpha=0.85, label="OADE-NSGA-II v2 Wins")
    p2 = ax.barh(y_pos, no_diff_counts, left=oade_better_counts, height=bar_height, color="#BDBDBD", alpha=0.85, label="No Significant Diff")
    lefts = [o + n for o, n in zip(oade_better_counts, no_diff_counts)]
    p3 = ax.barh(y_pos, comp_better_counts, left=lefts, height=bar_height, color="#E6550D", alpha=0.85, label="Comparator Wins")

    # Add numeric labels on bars
    for i, (o, n, c) in enumerate(zip(oade_better_counts, no_diff_counts, comp_better_counts)):
        if o > 0:
            ax.text(o / 2, i, str(o), ha="center", va="center", color="white", fontweight="bold", fontsize=7.5)
        if n > 0:
            ax.text(o + n / 2, i, str(n), ha="center", va="center", color="#333333", fontweight="bold", fontsize=7.5)
        if c > 0:
            ax.text(o + n + c / 2, i, str(c), ha="center", va="center", color="white", fontweight="bold", fontsize=7.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([comp_labels[c] for c in comparators], fontweight="bold", fontsize=8)
    ax.set_xlabel("Number of Metric Endpoints (Total = 10 per algorithm)", fontsize=8.5)
    ax.set_title("Benchmark v2: Pairwise Holm-Adjusted Wilcoxon Outcomes (Total: 58 Wins / 60)", fontweight="bold", fontsize=9.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False, fontsize=8)
    ax.set_xlim(0, 10.5)
    ax.grid(axis="x", linestyle=":", alpha=0.5)

    plt.tight_layout()
    fig.savefig(output_dir / "benchmark_v2_outcome_counts.png", dpi=300)
    fig.savefig(output_dir / "benchmark_v2_outcome_counts.pdf")
    fig.savefig(output_dir / "benchmark_v2_outcome_counts.svg")
    plt.close(fig)

    # 2. Figure: Direct comparison of OADE v1 vs OADE v2 on IGD
    v1_summary = Path("results/algorithm_benchmark/algorithm_benchmark_igd_hv_summary.csv")
    v1_oade = {}
    with open(v1_summary, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["algorithm"] == "OADE_NSGAII":
                v1_oade[r["problem"]] = {"IGD": float(r["IGD_mean"]), "HV": float(r["HV_mean"])}

    v2_oade = {}
    with open(summary_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["algorithm"] == "OADE_NSGAII":
                v2_oade[r["problem"]] = {"IGD": float(r["IGD_mean"]), "HV": float(r["HV_mean"])}

    problems = ["zdt1", "zdt2", "zdt3", "zdt4", "zdt6"]
    v1_igds = [v1_oade[p]["IGD"] for p in problems]
    v2_igds = [v2_oade[p]["IGD"] for p in problems]

    fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=300)
    x = np.arange(len(problems))
    width = 0.35

    rects1 = ax.bar(x - width/2, v1_igds, width, label="OADE v1 (Old Restart)", color="#E6550D", alpha=0.85)
    rects2 = ax.bar(x + width/2, v2_igds, width, label="OADE v2 (Adaptive Restart)", color="#31A354", alpha=0.85)

    ax.set_ylabel("Mean IGD (Lower is better ↓)", fontsize=8.5, fontweight="bold")
    ax.set_title("OADE-NSGA-II Performance Leap: v1 vs v2", fontweight="bold", fontsize=9.5)
    ax.set_xticks(x)
    ax.set_xticklabels([p.upper() for p in problems], fontweight="bold", fontsize=8.5)
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y", linestyle=":", alpha=0.5)

    # Annotate percentage reductions
    for i, (v1, v2) in enumerate(zip(v1_igds, v2_igds)):
        pct = (v1 - v2) / v1 * 100.0
        if pct > 0.5:
            ax.annotate(
                f"-{pct:.1f}%",
                xy=(i + width/2, v2),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=7.5, fontweight="bold", color="#1B7837"
            )

    plt.tight_layout()
    fig.savefig(output_dir / "benchmark_v2_v1_vs_v2_delta.png", dpi=300)
    fig.savefig(output_dir / "benchmark_v2_v1_vs_v2_delta.pdf")
    fig.savefig(output_dir / "benchmark_v2_v1_vs_v2_delta.svg")
    plt.close(fig)

    print("Saved Benchmark v2 figures to results/figures/.")


if __name__ == "__main__":
    plot_v2_figures()
