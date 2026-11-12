"""Paired statistical analysis for stochastic algorithm benchmarks."""

from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np
from scipy.stats import wilcoxon


STATISTICS_FIELDNAMES = [
    "problem",
    "metric",
    "reference_algorithm",
    "comparison_algorithm",
    "n_pairs",
    "reference_mean",
    "comparison_mean",
    "median_paired_difference",
    "statistic",
    "p_value",
    "p_adjusted_holm",
    "rank_biserial_effect",
    "alpha",
    "significant",
    "result",
]


def holm_adjust(p_values: Iterable[float]) -> list[float]:
    values = [
        1.0 if math.isnan(float(value)) else min(1.0, max(0.0, float(value)))
        for value in p_values
    ]
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    adjusted = [1.0] * len(values)
    previous = 0.0
    total = len(values)
    for rank, (original_index, p_value) in enumerate(indexed):
        candidate = min(1.0, (total - rank) * p_value)
        candidate = max(previous, candidate)
        adjusted[original_index] = candidate
        previous = candidate
    return adjusted


def paired_rank_biserial(reference: np.ndarray, comparison: np.ndarray, metric: str) -> float:
    """Return signed matched-pairs rank-biserial effect; positive favours reference."""

    raw = np.asarray(comparison, dtype=float) - np.asarray(reference, dtype=float)
    differences = raw if metric == "IGD" else -raw
    differences = differences[differences != 0]
    if len(differences) == 0:
        return 0.0
    ranks = _average_ranks(np.abs(differences))
    positive = float(np.sum(ranks[differences > 0]))
    negative = float(np.sum(ranks[differences < 0]))
    denominator = positive + negative
    return 0.0 if denominator == 0 else (positive - negative) / denominator


def _average_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        average = (start + 1 + end) / 2.0
        ranks[order[start:end]] = average
        start = end
    return ranks


def paired_wilcoxon_rows(
    raw_rows: list[dict],
    reference_algorithm: str,
    alpha: float = 0.05,
) -> list[dict]:
    """Compare a reference algorithm to all others using matched run indices.

    Holm adjustment is applied separately for IGD and HV across every included
    problem and comparison algorithm. This makes the correction family explicit.
    """

    # Resume preflight intentionally persists an empty checkpoint before the
    # first problem starts.  There is no comparison family at that point, so
    # emit an empty statistics table instead of treating the configured
    # reference algorithm as missing.
    if not raw_rows:
        return []

    problems = sorted({str(row["problem"]) for row in raw_rows})
    algorithms = sorted({str(row["algorithm"]) for row in raw_rows})
    if reference_algorithm not in algorithms:
        raise ValueError(f"reference algorithm is absent: {reference_algorithm}")

    rows: list[dict] = []
    for metric in ("IGD", "HV"):
        metric_rows: list[dict] = []
        for problem in problems:
            problem_rows = [row for row in raw_rows if str(row["problem"]) == problem]
            reference = {
                int(row["run_idx"]): float(row[metric])
                for row in problem_rows
                if str(row["algorithm"]) == reference_algorithm and _is_valid(row)
            }
            for comparison_algorithm in algorithms:
                if comparison_algorithm == reference_algorithm:
                    continue
                comparison = {
                    int(row["run_idx"]): float(row[metric])
                    for row in problem_rows
                    if str(row["algorithm"]) == comparison_algorithm and _is_valid(row)
                }
                paired_indices = sorted(set(reference) & set(comparison))
                if not paired_indices:
                    continue
                reference_values = np.asarray([reference[index] for index in paired_indices])
                comparison_values = np.asarray([comparison[index] for index in paired_indices])
                differences = reference_values - comparison_values
                if np.all(differences == 0.0):
                    statistic = 0.0
                    p_value = 1.0
                else:
                    try:
                        result = wilcoxon(reference_values, comparison_values, zero_method="wilcox")
                        statistic = float(result.statistic)
                        p_value = float(result.pvalue)
                    except ValueError:
                        statistic = 0.0
                        p_value = 1.0
                    if math.isnan(p_value):
                        statistic = 0.0
                        p_value = 1.0
                metric_rows.append(
                    {
                        "problem": problem,
                        "metric": metric,
                        "reference_algorithm": reference_algorithm,
                        "comparison_algorithm": comparison_algorithm,
                        "n_pairs": len(paired_indices),
                        "reference_mean": float(np.mean(reference_values)),
                        "comparison_mean": float(np.mean(comparison_values)),
                        "median_paired_difference": float(np.median(differences)),
                        "statistic": statistic,
                        "p_value": p_value,
                        "rank_biserial_effect": paired_rank_biserial(
                            reference_values, comparison_values, metric
                        ),
                        "alpha": float(alpha),
                    }
                )

        adjusted = holm_adjust(row["p_value"] for row in metric_rows)
        for row, adjusted_p in zip(metric_rows, adjusted):
            significant = adjusted_p < alpha
            effect = float(row["rank_biserial_effect"])
            row["p_adjusted_holm"] = adjusted_p
            row["significant"] = significant
            row["result"] = (
                "no_significant_difference"
                if not significant
                else "reference_better" if effect > 0
                else "comparison_better"
            )
        rows.extend(metric_rows)
    return rows


def _is_valid(row: dict) -> bool:
    value = row.get("valid", True)
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)

