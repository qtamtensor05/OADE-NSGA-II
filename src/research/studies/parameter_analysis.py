"""Run parameter sensitivity experiments for OADE-NSGA-II."""

from __future__ import annotations

import argparse
import csv
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from pymoo.indicators.hv import HV
from pymoo.indicators.igd import IGD
from pymoo.problems import get_problem
from scipy.stats import friedmanchisquare, wilcoxon

from research.benchmarking.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from shared.population import make_initial_population
from shared.fronts import non_dominated
from oade_nsga2 import OADE_NSGAII, ProblemWrapper
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv


DEFAULT_CONFIG_PATH = Path("config/studies/sensitivity.yaml")
RAW_FIELDNAMES = [
    "study",
    "parameter",
    "parameter_label",
    "problem",
    "n_var",
    "run_idx",
    "seed",
    "pop_size",
    "evaluation_budget",
    "n_eval",
    "budget_utilization",
    "stagnation_patience",
    "initial_mean_F",
    "initial_mean_CR",
    "final_mean_F",
    "final_mean_CR",
    "mean_F_gen30",
    "mean_CR_gen30",
    "mean_F_gen50",
    "mean_CR_gen50",
    "IGD",
    "HV",
    "runtime_seconds",
    "restart_count",
]

SUMMARY_FIELDNAMES = [
    "study",
    "parameter",
    "parameter_label",
    "problem",
    "n_var",
    "runs",
    "IGD_mean",
    "IGD_std",
    "IGD_best",
    "HV_mean",
    "HV_std",
    "HV_best",
    "runtime_mean",
    "n_eval_mean",
    "budget_utilization_mean",
    "restart_count_mean",
    "final_mean_F_mean",
    "final_mean_CR_mean",
]

STATS_FIELDNAMES = [
    "study",
    "problem",
    "metric",
    "test",
    "baseline_label",
    "comparison_label",
    "statistic",
    "p_value",
    "p_adjusted_holm",
    "alpha",
    "significant",
    "result",
]

TRACE_FIELDNAMES = [
    "study",
    "parameter_label",
    "problem",
    "run_idx",
    "seed",
    "generation",
    "mean_F",
    "mean_CR",
    "prob_de",
]


@dataclass(frozen=True)
class Experiment:
    study: str
    parameter: str
    label: str
    spec: Any


class TrackingOADE_NSGAII(OADE_NSGAII):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.restart_count = 0

    def _partial_restart(self) -> None:
        self.restart_count += 1
        super()._partial_restart()


def std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return float(np.std(np.asarray(values, dtype=float), ddof=1))


def metric_direction(metric: str) -> str:
    if metric == "IGD":
        return "lower"
    if metric == "HV":
        return "higher"
    raise ValueError(f"Unsupported metric: {metric}")


def compare_result(baseline_values: list[float], comparison_values: list[float], metric: str, significant: bool) -> str:
    if not significant:
        return "no_significant_difference"
    baseline_mean = float(np.mean(baseline_values))
    comparison_mean = float(np.mean(comparison_values))
    if metric_direction(metric) == "lower":
        return "baseline_better" if baseline_mean < comparison_mean else "comparison_better"
    return "baseline_better" if baseline_mean > comparison_mean else "comparison_better"


def holm_adjust(p_values: list[float]) -> list[float]:
    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    adjusted = [1.0 for _ in p_values]
    previous = 0.0
    total = len(p_values)
    for rank, (original_idx, p_value) in enumerate(indexed):
        adjusted_value = min(1.0, (total - rank) * p_value)
        adjusted_value = max(previous, adjusted_value)
        previous = adjusted_value
        adjusted[original_idx] = adjusted_value
    return adjusted


def build_experiments(cfg: dict) -> tuple[list[Experiment], dict[str, str], dict[str, list[str]]]:
    experiments = []
    baselines = {}
    study_labels = {}

    for study_cfg in cfg["studies"]:
        study = str(study_cfg["name"])
        parameter = str(study_cfg["parameter"])
        baselines[study] = str(study_cfg["baseline"])
        study_labels[study] = []

        for value in study_cfg["values"]:
            label = str(value.get("label")) if isinstance(value, dict) else str(value)
            experiments.append(Experiment(study=study, parameter=parameter, label=label, spec=value))
            study_labels[study].append(label)

    return experiments, baselines, study_labels


def resolve_settings(cfg: dict, experiment: Experiment, seed: int) -> tuple[int, dict, float, float]:
    baseline = dict(cfg["baseline"])
    oade_cfg = {
        "stagnation_patience": int(baseline["stagnation_patience"]),
        "stagnation_tolerance": float(baseline["stagnation_tolerance"]),
        "restart_elite_ratio": float(baseline["restart_elite_ratio"]),
        "prob_de": float(baseline["prob_de"]),
        "n_neighbors": int(baseline["n_neighbors"]),
        "mean_F": float(baseline["mean_F"]),
        "mean_CR": float(baseline["mean_CR"]),
    }
    pop_size = int(baseline["pop_size"])

    if experiment.parameter == "pop_size":
        pop_size = int(experiment.spec)
    elif experiment.parameter == "stagnation_patience":
        oade_cfg["stagnation_patience"] = int(experiment.spec)
    elif experiment.parameter == "f_cr_init":
        spec = dict(experiment.spec)
        rng = np.random.default_rng(seed + 100_000)
        if "mean_F_range" in spec:
            low, high = [float(v) for v in spec["mean_F_range"]]
            oade_cfg["mean_F"] = float(rng.uniform(low, high))
        else:
            oade_cfg["mean_F"] = float(spec["mean_F"])

        if "mean_CR_range" in spec:
            low, high = [float(v) for v in spec["mean_CR_range"]]
            oade_cfg["mean_CR"] = float(rng.uniform(low, high))
        else:
            oade_cfg["mean_CR"] = float(spec["mean_CR"])
    else:
        raise ValueError(f"Unsupported sensitivity parameter: {experiment.parameter}")

    return pop_size, oade_cfg, oade_cfg["mean_F"], oade_cfg["mean_CR"]


def apply_oade_config(solver: TrackingOADE_NSGAII, oade_cfg: dict) -> None:
    solver.stagnation_patience = int(oade_cfg["stagnation_patience"])
    solver.stagnation_tolerance = float(oade_cfg["stagnation_tolerance"])
    solver.restart_elite_ratio = float(oade_cfg["restart_elite_ratio"])
    solver.prob_de = float(oade_cfg["prob_de"])
    solver.n_neighbors = int(oade_cfg["n_neighbors"])
    solver.mean_F = float(oade_cfg["mean_F"])
    solver.mean_CR = float(oade_cfg["mean_CR"])


def trace_value(trace: list[dict], key: str, generation: int) -> float | str:
    if len(trace) < generation:
        return ""
    return float(trace[generation - 1][key])


def run_experiment(
    cfg: dict,
    experiment: Experiment,
    problem_name: str,
    n_var: int | None,
    run_idx: int,
    seed: int,
) -> tuple[dict, list[dict]]:
    problem_kwargs = {}
    if n_var is not None:
        problem_kwargs["n_var"] = n_var
    problem = get_problem(problem_name, **problem_kwargs)

    pf = np.asarray(problem.pareto_front())
    igd_indicator = IGD(pf)
    hv_indicator = HV(ref_point=np.max(pf, axis=0) + 0.1)

    pop_size, oade_cfg, initial_mean_f, initial_mean_cr = resolve_settings(cfg, experiment, seed)
    evaluation_budget = int(cfg["global"]["evaluation_budget"])
    initial_x = make_initial_population(problem, pop_size, seed)

    np.random.seed(seed)
    random.seed(seed)
    budgeted_problem = BudgetedProblem(problem, evaluation_budget)
    solver = TrackingOADE_NSGAII(
        ProblemWrapper(budgeted_problem), pop_size=pop_size, n_gen=evaluation_budget
    )
    apply_oade_config(solver, oade_cfg)

    trace = []

    def record_trace(generation: int, _n_gen: int) -> None:
        trace.append(
            {
                "generation": generation,
                "mean_F": float(solver.mean_F),
                "mean_CR": float(solver.mean_CR),
                "prob_de": float(solver.prob_de),
            }
        )

    start = time.perf_counter()
    try:
        front = non_dominated(solver.run(initial_x=initial_x, progress_callback=record_trace))
    except EvaluationBudgetExceeded:
        front = non_dominated(np.asarray([individual.F for individual in solver.population]))
    runtime = time.perf_counter() - start

    raw_row = {
        "study": experiment.study,
        "parameter": experiment.parameter,
        "parameter_label": experiment.label,
        "problem": problem_name,
        "n_var": n_var,
        "run_idx": run_idx,
        "seed": seed,
        "pop_size": pop_size,
        "evaluation_budget": evaluation_budget,
        "n_eval": budgeted_problem.n_eval,
        "budget_utilization": budgeted_problem.n_eval / evaluation_budget,
        "stagnation_patience": int(oade_cfg["stagnation_patience"]),
        "initial_mean_F": initial_mean_f,
        "initial_mean_CR": initial_mean_cr,
        "final_mean_F": float(solver.mean_F),
        "final_mean_CR": float(solver.mean_CR),
        "mean_F_gen30": trace_value(trace, "mean_F", 30),
        "mean_CR_gen30": trace_value(trace, "mean_CR", 30),
        "mean_F_gen50": trace_value(trace, "mean_F", 50),
        "mean_CR_gen50": trace_value(trace, "mean_CR", 50),
        "IGD": float(igd_indicator(front)),
        "HV": float(hv_indicator(front)),
        "runtime_seconds": float(runtime),
        "restart_count": int(solver.restart_count),
    }

    trace_rows = [
        {
            "study": experiment.study,
            "parameter_label": experiment.label,
            "problem": problem_name,
            "run_idx": run_idx,
            "seed": seed,
            **item,
        }
        for item in trace
    ]

    return raw_row, trace_rows


def summarize(raw_rows: list[dict]) -> list[dict]:
    grouped = {}
    for row in raw_rows:
        key = (row["study"], row["parameter"], row["parameter_label"], row["problem"], row["n_var"])
        grouped.setdefault(key, []).append(row)

    summary_rows = []
    for (study, parameter, label, problem, n_var), rows in grouped.items():
        igd = [float(row["IGD"]) for row in rows]
        hv = [float(row["HV"]) for row in rows]
        runtime = [float(row["runtime_seconds"]) for row in rows]
        n_eval = [float(row["n_eval"]) for row in rows]
        budget_utilization = [float(row["budget_utilization"]) for row in rows]
        restart_count = [float(row["restart_count"]) for row in rows]
        final_mean_f = [float(row["final_mean_F"]) for row in rows]
        final_mean_cr = [float(row["final_mean_CR"]) for row in rows]
        summary_rows.append(
            {
                "study": study,
                "parameter": parameter,
                "parameter_label": label,
                "problem": problem,
                "n_var": n_var,
                "runs": len(rows),
                "IGD_mean": float(np.mean(igd)),
                "IGD_std": std(igd),
                "IGD_best": float(np.min(igd)),
                "HV_mean": float(np.mean(hv)),
                "HV_std": std(hv),
                "HV_best": float(np.max(hv)),
                "runtime_mean": float(np.mean(runtime)),
                "n_eval_mean": float(np.mean(n_eval)),
                "budget_utilization_mean": float(np.mean(budget_utilization)),
                "restart_count_mean": float(np.mean(restart_count)),
                "final_mean_F_mean": float(np.mean(final_mean_f)),
                "final_mean_CR_mean": float(np.mean(final_mean_cr)),
            }
        )
    return summary_rows


def values_by_run(rows: list[dict], study: str, problem: str, label: str, metric: str) -> dict[int, float]:
    return {
        int(row["run_idx"]): float(row[metric])
        for row in rows
        if row["study"] == study and row["problem"] == problem and row["parameter_label"] == label
    }


def statistical_tests(
    raw_rows: list[dict],
    baselines: dict[str, str],
    study_labels: dict[str, list[str]],
    alpha: float,
) -> list[dict]:
    stats_rows = []
    problems = sorted({str(row["problem"]) for row in raw_rows})

    for study, labels in study_labels.items():
        baseline_label = baselines[study]
        for problem in problems:
            for metric in ("IGD", "HV"):
                label_values = []
                common_runs = None
                for label in labels:
                    value_map = values_by_run(raw_rows, study, problem, label, metric)
                    common_runs = set(value_map) if common_runs is None else common_runs & set(value_map)
                    label_values.append(value_map)

                common_run_list = sorted(common_runs or [])
                arrays = [[value_map[i] for i in common_run_list] for value_map in label_values]
                if len(arrays) >= 3 and common_run_list:
                    try:
                        test_result = friedmanchisquare(*arrays)
                        statistic = float(test_result.statistic)
                        p_value = float(test_result.pvalue)
                    except ValueError:
                        statistic = 0.0
                        p_value = 1.0
                    stats_rows.append(
                        {
                            "study": study,
                            "problem": problem,
                            "metric": metric,
                            "test": "friedman",
                            "baseline_label": baseline_label,
                            "comparison_label": "all",
                            "statistic": statistic,
                            "p_value": p_value,
                            "p_adjusted_holm": "",
                            "alpha": alpha,
                            "significant": p_value < alpha,
                            "result": "parameter_effect_detected" if p_value < alpha else "no_parameter_effect_detected",
                        }
                    )

                baseline_map = values_by_run(raw_rows, study, problem, baseline_label, metric)
                pair_rows = []
                p_values = []
                for label in labels:
                    if label == baseline_label:
                        continue
                    comparison_map = values_by_run(raw_rows, study, problem, label, metric)
                    paired_runs = sorted(set(baseline_map) & set(comparison_map))
                    baseline_values = [baseline_map[i] for i in paired_runs]
                    comparison_values = [comparison_map[i] for i in paired_runs]
                    if not paired_runs:
                        continue
                    try:
                        test_result = wilcoxon(baseline_values, comparison_values, zero_method="wilcox")
                        statistic = float(test_result.statistic)
                        p_value = float(test_result.pvalue)
                    except ValueError:
                        statistic = 0.0
                        p_value = 1.0
                    pair_rows.append((label, statistic, p_value, baseline_values, comparison_values))
                    p_values.append(p_value)

                adjusted_values = holm_adjust(p_values)
                for (label, statistic, p_value, baseline_values, comparison_values), adjusted in zip(
                    pair_rows, adjusted_values
                ):
                    significant = adjusted < alpha
                    stats_rows.append(
                        {
                            "study": study,
                            "problem": problem,
                            "metric": metric,
                            "test": "wilcoxon_signed_rank_vs_baseline",
                            "baseline_label": baseline_label,
                            "comparison_label": label,
                            "statistic": statistic,
                            "p_value": p_value,
                            "p_adjusted_holm": adjusted,
                            "alpha": alpha,
                            "significant": significant,
                            "result": compare_result(baseline_values, comparison_values, metric, significant),
                        }
                    )

    return stats_rows


def read_existing_rows(path: Path, expected_fields: list[str]) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise ValueError(
                f"cannot resume from {path}: schema differs from the current sensitivity pipeline"
            )
        return list(reader)


def persist_sensitivity(
    out_dir: Path,
    raw_rows: list[dict],
    trace_rows: list[dict],
    baselines: dict[str, str],
    study_labels: dict[str, list[str]],
    alpha: float,
) -> None:
    write_csv(out_dir / "sensitivity_raw_runs.csv", raw_rows, RAW_FIELDNAMES)
    write_csv(out_dir / "sensitivity_summary.csv", summarize(raw_rows), SUMMARY_FIELDNAMES)
    write_csv(
        out_dir / "sensitivity_statistics.csv",
        statistical_tests(raw_rows, baselines, study_labels, alpha),
        STATS_FIELDNAMES,
    )
    write_csv(out_dir / "sensitivity_fcr_trace.csv", trace_rows, TRACE_FIELDNAMES)


def _main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="resume after the last fully completed parameter level",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=None,
        help="number of independent problem/seed workers (default: config value or 1)",
    )
    args = parser.parse_args(argv)

    cfg = load_yaml_config(Path(args.config))
    from shared.paths import repository_path
    out_dir = args.out_dir or repository_path(cfg["global"]["out_dir"])
    runs = int(cfg["global"]["runs"])
    seed_base = int(cfg["global"]["seed_base"])
    alpha = float(cfg["global"]["alpha"])
    experiments, baselines, study_labels = build_experiments(cfg)
    jobs = int(args.jobs or cfg["global"].get("jobs", 1))
    if jobs < 1:
        raise ValueError("--jobs must be at least 1")
    print(f"Using {jobs} sensitivity worker(s).", flush=True)

    if args.resume:
        raw_rows = read_existing_rows(out_dir / "sensitivity_raw_runs.csv", RAW_FIELDNAMES)
        trace_rows = read_existing_rows(out_dir / "sensitivity_fcr_trace.csv", TRACE_FIELDNAMES)
    else:
        raw_rows = []
        trace_rows = []

    for experiment in experiments:
        expected = len(cfg["problems"]) * runs
        completed = sum(
            str(row["study"]) == experiment.study
            and str(row["parameter_label"]) == experiment.label
            for row in raw_rows
        )
        if args.resume and completed == expected:
            print(
                f"[{experiment.study}={experiment.label}] resume: "
                f"already complete ({completed} runs)."
            )
            continue
        if args.resume and completed:
            raise ValueError(
                f"cannot safely resume partially completed level "
                f"{experiment.study}={experiment.label}: found {completed}/{expected} rows"
            )
        tasks = [
            (
                str(problem_item["name"]),
                problem_item.get("n_var"),
                run_idx,
                seed_base + run_idx,
            )
            for problem_item in cfg["problems"]
            for run_idx in range(runs)
        ]
        level_results = []
        if jobs <= 1:
            for problem_name, n_var, run_idx, seed in tasks:
                level_results.append(
                    run_experiment(cfg, experiment, problem_name, n_var, run_idx, seed)
                )
                print(
                    f"[{experiment.study}={experiment.label}] "
                    f"{problem_name} run {run_idx + 1}/{runs} done (seed={seed}).",
                    flush=True,
                )
        else:
            with ProcessPoolExecutor(max_workers=jobs) as executor:
                futures = {
                    executor.submit(
                        run_experiment, cfg, experiment, problem_name, n_var, run_idx, seed
                    ): (problem_name, run_idx, seed)
                    for problem_name, n_var, run_idx, seed in tasks
                }
                completed_count = 0
                for future in as_completed(futures):
                    level_results.append(future.result())
                    completed_count += 1
                    problem_name, run_idx, seed = futures[future]
                    print(
                        f"[{experiment.study}={experiment.label}] "
                        f"{completed_count}/{len(tasks)} tasks done "
                        f"(latest {problem_name}, run_idx={run_idx}, seed={seed}).",
                        flush=True,
                    )

        new_raw_rows = [result[0] for result in level_results]
        new_raw_rows.sort(key=lambda row: (str(row["problem"]), int(row["run_idx"])))
        new_trace_rows = [row for result in level_results for row in result[1]]
        new_trace_rows.sort(
            key=lambda row: (
                str(row["problem"]), int(row["run_idx"]), int(row["generation"])
            )
        )
        raw_rows.extend(new_raw_rows)
        trace_rows.extend(new_trace_rows)

        persist_sensitivity(
            out_dir, raw_rows, trace_rows, baselines, study_labels, alpha
        )
        print(
            f"[{experiment.study}={experiment.label}] checkpoint saved to "
            f"{out_dir.as_posix()}."
        )

    persist_sensitivity(out_dir, raw_rows, trace_rows, baselines, study_labels, alpha)

    print(f"Saved: {(out_dir / 'sensitivity_raw_runs.csv').as_posix()}")
    print(f"Saved: {(out_dir / 'sensitivity_summary.csv').as_posix()}")
    print(f"Saved: {(out_dir / 'sensitivity_statistics.csv').as_posix()}")
    print(f"Saved: {(out_dir / 'sensitivity_fcr_trace.csv').as_posix()}")
    print("Plot with: python main.py plot-sensitivity")


def main(argv: list[str] | None = None) -> None:
    from research.maintenance.tmp_sessions import run_configured
    return run_configured(_main, argv)


if __name__ == "__main__":
    main()
