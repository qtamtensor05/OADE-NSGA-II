#!/usr/bin/env python3
"""
Generate intuitive, easy-to-understand publication figures for the restart confirmation experiment.
Follows nature-figure guidelines with zero pandas dependency (uses stdlib csv + numpy + matplotlib).

Produces two intuitive deliverables:
1. results/figures/restart_direct_comparison.{pdf,svg,png,tiff}:
   Side-by-side grouped boxplots of raw IGD (lower=better) and HV (higher=better) across all 5 ZDT problems.
2. results/figures/restart_convergence.{pdf,svg,png,tiff}:
   Evaluation-budget convergence trajectories (Median IGD + IQR shaded band).
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
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 8.0,
        "figure.titlesize": 10.5,
        "axes.linewidth": 0.7,
        "grid.linewidth": 0.4,
        "lines.linewidth": 1.2,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def plot_direct_comparison(
    raw_csv: Path,
    output_dir: Path,
) -> None:
    """
    Figure 1: Direct comparison of IGD and HV values side-by-side.
    Each problem has 3 adjacent boxes: Full OADE (red), No Restart (blue), Adaptive Restart (green).
    """
    # Read raw runs
    data: dict[str, dict[str, dict[str, list[float]]]] = {}
    problems = ["zdt1", "zdt2", "zdt3", "zdt4", "zdt6"]
    algos = ["OADE_FULL", "OADE_NO_RESTART", "OADE_ADAPTIVE_RESTART"]
    algo_labels = {
        "OADE_FULL": "Old Restart (Full OADE)",
        "OADE_NO_RESTART": "No Restart",
        "OADE_ADAPTIVE_RESTART": "New Restart (Adaptive)",
    }
    palette = {
        "OADE_FULL": "#D95F0E",            # Warm orange-red (warns of instability)
        "OADE_NO_RESTART": "#3182BD",       # Nature blue
        "OADE_ADAPTIVE_RESTART": "#31A354",  # Nature green
    }

    for p in problems:
        data[p] = {a: {"IGD": [], "HV": []} for a in algos}

    with open(raw_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["problem"].strip().lower()
            a = row["algorithm"].strip()
            if p in data and a in data[p]:
                data[p][a]["IGD"].append(float(row["IGD"]))
                data[p][a]["HV"].append(float(row["HV"]))

    fig, axes = plt.subplots(2, 5, figsize=(9.5, 5.0), dpi=300)
    fig.subplots_adjust(hspace=0.35, wspace=0.30)

    np.random.seed(42)

    # Row 0: IGD (Lower is better)
    for col_idx, p in enumerate(problems):
        ax = axes[0, col_idx]
        positions = [1, 2, 3]
        for a_idx, a in enumerate(algos):
            vals = data[p][a]["IGD"]
            pos = positions[a_idx]
            color = palette[a]
            ax.boxplot(
                vals, positions=[pos], widths=0.6, patch_artist=True,
                showfliers=False,
                boxprops=dict(facecolor=color, alpha=0.35, edgecolor=color, linewidth=0.9),
                medianprops=dict(color="#111111", linewidth=1.3),
                whiskerprops=dict(color=color, linewidth=0.9),
                capprops=dict(color=color, linewidth=0.9),
            )
            # Add jittered raw seeds
            jitter = np.random.uniform(-0.12, 0.12, size=len(vals))
            ax.scatter([pos + j for j in jitter], vals, color=color, alpha=0.65, s=12, zorder=3)

        ax.set_title(p.upper(), fontweight="bold", fontsize=9)
        ax.set_xticks(positions)
        ax.set_xticklabels(["Old Restart", "No Restart", "New Restart"], fontsize=6.8, rotation=15)
        ax.grid(axis="y", linestyle=":", alpha=0.6)
        if col_idx == 0:
            ax.set_ylabel("IGD (Lower is better ↓)", fontsize=8.5, fontweight="bold")

    # Row 1: HV (Higher is better)
    for col_idx, p in enumerate(problems):
        ax = axes[1, col_idx]
        positions = [1, 2, 3]
        for a_idx, a in enumerate(algos):
            vals = data[p][a]["HV"]
            pos = positions[a_idx]
            color = palette[a]
            ax.boxplot(
                vals, positions=[pos], widths=0.6, patch_artist=True,
                showfliers=False,
                boxprops=dict(facecolor=color, alpha=0.35, edgecolor=color, linewidth=0.9),
                medianprops=dict(color="#111111", linewidth=1.3),
                whiskerprops=dict(color=color, linewidth=0.9),
                capprops=dict(color=color, linewidth=0.9),
            )
            jitter = np.random.uniform(-0.12, 0.12, size=len(vals))
            ax.scatter([pos + j for j in jitter], vals, color=color, alpha=0.65, s=12, zorder=3)

        ax.set_title(f"{p.upper()} (HV)", fontweight="bold", fontsize=9)
        ax.set_xticks(positions)
        ax.set_xticklabels(["Old Restart", "No Restart", "New Restart"], fontsize=6.8, rotation=15)
        ax.grid(axis="y", linestyle=":", alpha=0.6)
        if col_idx == 0:
            ax.set_ylabel("HV (Higher is better ↑)", fontsize=8.5, fontweight="bold")

    # Legend at top
    custom_patches = [
        mpl.patches.Patch(facecolor=palette[a], edgecolor=palette[a], alpha=0.5, label=algo_labels[a])
        for a in algos
    ]
    fig.legend(
        handles=custom_patches,
        loc="upper center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.99),
        fontsize=8.5,
    )

    fig.suptitle("Direct Metric Comparison Across 30 Independent Seeds (n = 30)", y=1.03, fontweight="bold", fontsize=11)
    
    base_name = output_dir / "restart_direct_comparison"
    fig.savefig(f"{base_name}.pdf", bbox_inches="tight")
    fig.savefig(f"{base_name}.svg", bbox_inches="tight")
    fig.savefig(f"{base_name}.tiff", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved direct comparison figures to {base_name}.*")


def plot_convergence(
    conv_csv: Path,
    output_dir: Path,
) -> None:
    """
    Figure 2: Convergence trajectories of IGD over evaluation budget.
    Shows how classic restart causes erratic spikes, while adaptive restart is smooth and stable.
    """
    problems = ["zdt1", "zdt2", "zdt3", "zdt4", "zdt6"]
    algos = ["OADE_FULL", "OADE_NO_RESTART", "OADE_ADAPTIVE_RESTART"]
    algo_labels = {
        "OADE_FULL": "Old Restart (Full OADE)",
        "OADE_NO_RESTART": "No Restart",
        "OADE_ADAPTIVE_RESTART": "New Restart (Adaptive)",
    }
    palette = {
        "OADE_FULL": "#D95F0E",
        "OADE_NO_RESTART": "#3182BD",
        "OADE_ADAPTIVE_RESTART": "#31A354",
    }
    linestyles = {
        "OADE_FULL": ":",
        "OADE_NO_RESTART": "--",
        "OADE_ADAPTIVE_RESTART": "-",
    }

    # Read convergence records: (problem, algo, checkpoint) -> list of IGDs
    records: dict[tuple[str, str, float], list[float]] = {}
    with open(conv_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["problem"].strip().lower()
            a = row["algorithm"].strip()
            cp = float(row["checkpoint_fraction"])
            igd = float(row["IGD"])
            key = (p, a, cp)
            if key not in records:
                records[key] = []
            records[key].append(igd)

    fig, axes = plt.subplots(1, 5, figsize=(10.5, 2.7), dpi=300)
    fig.subplots_adjust(wspace=0.32)

    for idx, p in enumerate(problems):
        ax = axes[idx]
        checkpoints = sorted({cp for (prob, _, cp) in records if prob == p})
        
        for a in algos:
            medians = []
            q25s = []
            q75s = []
            valid_cps = []
            for cp in checkpoints:
                vals = records.get((p, a, cp), [])
                if vals:
                    valid_cps.append(cp * 20000)  # Convert fraction to evaluations
                    medians.append(float(np.median(vals)))
                    q25s.append(float(np.percentile(vals, 25)))
                    q75s.append(float(np.percentile(vals, 75)))

            if valid_cps:
                ax.plot(
                    valid_cps, medians, label=algo_labels[a],
                    color=palette[a], linestyle=linestyles[a], linewidth=1.4
                )
                ax.fill_between(valid_cps, q25s, q75s, color=palette[a], alpha=0.15)

        ax.set_title(p.upper(), fontweight="bold", fontsize=9)
        ax.set_xlabel("Evaluations", fontsize=8)
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.tick_params(axis="both", which="major", labelsize=7)
        if idx == 0:
            ax.set_ylabel("IGD (Median ± IQR)", fontsize=8.5, fontweight="bold")

    # Legend at top
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", ncol=3, frameon=False,
        bbox_to_anchor=(0.5, 1.12), fontsize=8.5
    )

    base_name = output_dir / "restart_convergence"
    fig.savefig(f"{base_name}.pdf", bbox_inches="tight")
    fig.savefig(f"{base_name}.svg", bbox_inches="tight")
    fig.savefig(f"{base_name}.tiff", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved convergence figures to {base_name}.*")


def main() -> None:
    set_nature_style()
    data_dir = Path("results/restart_confirmation")
    figures_dir = Path("results/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    raw_file = data_dir / "algorithm_benchmark_raw_runs.csv"
    conv_file = data_dir / "algorithm_benchmark_convergence.csv"

    if raw_file.exists():
        plot_direct_comparison(raw_file, figures_dir)
    else:
        print(f"File not found: {raw_file}")

    if conv_file.exists():
        plot_convergence(conv_file, figures_dir)
    else:
        print(f"File not found: {conv_file}")


if __name__ == "__main__":
    main()
