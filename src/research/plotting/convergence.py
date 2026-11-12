"""Plot median convergence curves with interquartile uncertainty bands."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def plot_metric(rows: list[dict], problem: str, metric: str, output: Path) -> None:
    grouped: dict[tuple[str, float], list[float]] = defaultdict(list)
    for row in rows:
        if row["problem"] == problem:
            grouped[(row["algorithm"], float(row["checkpoint_fraction"]))].append(float(row[metric]))

    fig, axis = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    algorithms = sorted({key[0] for key in grouped})
    for algorithm in algorithms:
        fractions = sorted({key[1] for key in grouped if key[0] == algorithm})
        values = [np.asarray(grouped[(algorithm, fraction)], dtype=float) for fraction in fractions]
        median = [float(np.median(item)) for item in values]
        lower = [float(np.quantile(item, 0.25)) for item in values]
        upper = [float(np.quantile(item, 0.75)) for item in values]
        axis.plot(fractions, median, marker="o", linewidth=1.6, label=algorithm)
        axis.fill_between(fractions, lower, upper, alpha=0.15)

    axis.set_xlabel("Fraction of evaluation budget")
    axis.set_ylabel(metric)
    axis.set_title(f"{problem}: {metric} convergence")
    axis.grid(alpha=0.25)
    axis.legend(fontsize=7, ncol=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="results/algorithm_benchmark/algorithm_benchmark_convergence.csv",
    )
    parser.add_argument("--out-dir", default="results/algorithm_benchmark/convergence_plots")
    args = parser.parse_args(argv)
    rows = load_rows(Path(args.input))
    out_dir = Path(args.out_dir)
    for problem in sorted({row["problem"] for row in rows}):
        for metric in ("IGD", "HV"):
            plot_metric(rows, problem, metric, out_dir / f"{problem}_{metric.lower()}_convergence.png")


if __name__ == "__main__":
    main()
