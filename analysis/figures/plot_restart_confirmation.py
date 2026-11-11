#!/usr/bin/env python3
"""
Generate Nature-standard publication figures for the restart confirmation experiment.
Follows nature-figure and nature-statistics protocols.
Zero pandas dependency: uses only Python stdlib (csv) + numpy + matplotlib.
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
        "axes.labelsize": 8.0,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5,
        "figure.titlesize": 10.0,
        "axes.linewidth": 0.6,
        "grid.linewidth": 0.4,
        "lines.linewidth": 1.0,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def load_raw_data(csv_path: Path) -> dict[tuple[str, int], dict[str, dict[str, float]]]:
    """
    Read raw CSV without pandas.
    Returns: mapping (problem, run_idx) -> {algorithm: {"IGD": val, "HV": val}}
    """
    data: dict[tuple[str, int], dict[str, dict[str, float]]] = {}
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prob = row["problem"].strip().lower()
            run_idx = int(row["run_idx"])
            algo = row["algorithm"].strip()
            igd = float(row["IGD"])
            hv = float(row["HV"])
            
            key = (prob, run_idx)
            if key not in data:
                data[key] = {}
            data[key][algo] = {"IGD": igd, "HV": hv}
    return data


def generate_figures(
    input_dir: Path = Path("results/restart_confirmation"),
    output_dir: Path = Path("results/figures"),
) -> None:
    set_nature_style()
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_file = input_dir / "algorithm_benchmark_raw_runs.csv"
    if not raw_file.exists():
        print(f"Warning: {raw_file} does not exist yet. Run the benchmark first.")
        return

    raw_data = load_raw_data(raw_file)
    problems = ["zdt1", "zdt2", "zdt3", "zdt4", "zdt6"]
    comparisons = ["Adaptive Restart", "No Restart"]
    algo_map = {
        "No Restart": "OADE_NO_RESTART",
        "Adaptive Restart": "OADE_ADAPTIVE_RESTART",
    }
    
    # Compute relative paired improvement (%) over OADE_FULL
    # IGD: lower is better -> (Full - Comp) / Full * 100
    # HV: higher is better -> (Comp - Full) / Full * 100
    records = []
    diff_data: dict[tuple[str, str], dict[str, list[float]]] = {}

    for prob in problems:
        for comp in comparisons:
            diff_data[(prob, comp)] = {"IGD": [], "HV": []}

    for (prob, run_idx), algos in raw_data.items():
        if "OADE_FULL" not in algos:
            continue
        full_igd = algos["OADE_FULL"]["IGD"]
        full_hv = algos["OADE_FULL"]["HV"]

        for comp, algo_key in algo_map.items():
            if algo_key in algos:
                comp_igd = algos[algo_key]["IGD"]
                comp_hv = algos[algo_key]["HV"]
                
                rel_igd = 100.0 * (full_igd - comp_igd) / abs(full_igd)
                rel_hv = 100.0 * (comp_hv - full_hv) / abs(full_hv)

                if (prob, comp) in diff_data:
                    diff_data[(prob, comp)]["IGD"].append(rel_igd)
                    diff_data[(prob, comp)]["HV"].append(rel_hv)

                records.append({
                    "problem": prob.upper(),
                    "comparison": comp,
                    "run_idx": run_idx,
                    "IGD_improvement_pct": rel_igd,
                    "HV_improvement_pct": rel_hv,
                })

    # Export source data CSV for Nature audit
    source_csv = output_dir / "restart_confirmation_paired_source.csv"
    with open(source_csv, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["problem", "comparison", "run_idx", "IGD_improvement_pct", "HV_improvement_pct"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # -------------------------------------------------------------
    # Figure: Paired Run-Level Performance Comparison (Nature 2-panel)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8), dpi=300)
    colors = {"No Restart": "#3182BD", "Adaptive Restart": "#31A354"}
    
    # Panel a: IGD improvement %
    ax_a = axes[0]
    ax_a.axvline(0, color="#666666", linestyle="--", linewidth=0.8, zorder=1)
    
    y_labels = []
    y_ticks = []
    pos = 0.0

    np.random.seed(42)  # reproducible jitter
    for prob in problems:
        for comp in ["Adaptive Restart", "No Restart"]:
            vals = diff_data.get((prob, comp), {}).get("IGD", [])
            if not vals:
                continue
            ax_a.boxplot(
                vals, positions=[pos], orientation="horizontal", widths=0.55,
                patch_artist=True, showfliers=False,
                boxprops=dict(facecolor=colors[comp], alpha=0.35, edgecolor=colors[comp], linewidth=0.8),
                medianprops=dict(color="#111111", linewidth=1.2),
                whiskerprops=dict(color=colors[comp], linewidth=0.8),
                capprops=dict(color=colors[comp], linewidth=0.8),
            )
            jitter = np.random.uniform(-0.15, 0.15, size=len(vals))
            ax_a.scatter(vals, pos + jitter, color=colors[comp], alpha=0.6, s=10, zorder=3)
            y_labels.append(f"{prob.upper()} ({comp[:4]})")
            y_ticks.append(pos)
            pos += 1.0
        pos += 0.5  # gap between problems

    ax_a.set_yticks(y_ticks)
    ax_a.set_yticklabels(y_labels, fontsize=7)
    ax_a.set_xlabel("IGD Improvement over Full OADE (%)", fontsize=8)
    ax_a.set_title("a  IGD Paired Differences (n = 30 new seeds)", loc="left", fontweight="bold", fontsize=8.5)
    ax_a.grid(axis="x", linestyle=":", alpha=0.5)

    # Panel b: HV improvement %
    ax_b = axes[1]
    ax_b.axvline(0, color="#666666", linestyle="--", linewidth=0.8, zorder=1)
    
    pos = 0.0
    for prob in problems:
        for comp in ["Adaptive Restart", "No Restart"]:
            vals = diff_data.get((prob, comp), {}).get("HV", [])
            if not vals:
                continue
            ax_b.boxplot(
                vals, positions=[pos], orientation="horizontal", widths=0.55,
                patch_artist=True, showfliers=False,
                boxprops=dict(facecolor=colors[comp], alpha=0.35, edgecolor=colors[comp], linewidth=0.8),
                medianprops=dict(color="#111111", linewidth=1.2),
                whiskerprops=dict(color=colors[comp], linewidth=0.8),
                capprops=dict(color=colors[comp], linewidth=0.8),
            )
            jitter = np.random.uniform(-0.15, 0.15, size=len(vals))
            ax_b.scatter(vals, pos + jitter, color=colors[comp], alpha=0.6, s=10, zorder=3)
            pos += 1.0
        pos += 0.5

    ax_b.set_yticks(y_ticks)
    ax_b.set_yticklabels([])
    ax_b.set_xlabel("HV Improvement over Full OADE (%)", fontsize=8)
    ax_b.set_title("b  HV Paired Differences (n = 30 new seeds)", loc="left", fontweight="bold", fontsize=8.5)
    ax_b.grid(axis="x", linestyle=":", alpha=0.5)

    # Legend
    custom_lines = [
        mpl.lines.Line2D([0], [0], color=colors["No Restart"], lw=3, alpha=0.7),
        mpl.lines.Line2D([0], [0], color=colors["Adaptive Restart"], lw=3, alpha=0.7),
    ]
    fig.legend(custom_lines, ["No Restart", "Adaptive Restart (New)"], loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.02))

    plt.tight_layout()
    
    # Save in Nature formats: PDF, SVG, TIFF (300 dpi), PNG
    base_name = output_dir / "restart_confirmation_paired"
    fig.savefig(f"{base_name}.pdf", bbox_inches="tight")
    fig.savefig(f"{base_name}.svg", bbox_inches="tight")
    fig.savefig(f"{base_name}.tiff", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved publication figures and source data to {output_dir}")


if __name__ == "__main__":
    generate_figures()
