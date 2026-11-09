"""Unified, budget-controlled benchmark for all configured algorithms."""

from __future__ import annotations

import argparse
import importlib
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from pymoo.indicators.hv import HV
from pymoo.indicators.igd import IGD
from pymoo.optimize import minimize
from pymoo.problems import get_problem
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from pymoo.util.ref_dirs import get_reference_directions

from algorithms.ce_moea import CEMOEA
from algorithms.cgde_nsga2 import CGDE_NSGAII
from algorithms.cgde_nsga2 import ProblemAdapter as CGDEProblemAdapter
from algorithms.nsga2_sdr_ols import NSGAIISDROLS
from algorithms.nsga2_sdr_ols import ProblemAdapter as SDROLSProblemAdapter
from src.benchmarking.evaluation import BudgetedProblem, EvaluationBudgetExceeded, validate_result
from src.benchmarking.pymoo_compare import make_initial_population, make_rnsga2_ref_points
from src.benchmarking.statistics import STATISTICS_FIELDNAMES, paired_wilcoxon_rows
from src.oade_nsga2 import OADE_NSGAII, ProblemWrapper
from src.utils.config import load_yaml_config
from src.utils.csv_io import write_csv


DEFAULT_CONFIG_PATH = Path("config") / "algorithm_benchmark.yaml"
RAW_CSV = "algorithm_benchmark_raw_runs.csv"
SUMMARY_CSV = "algorithm_benchmark_igd_hv_summary.csv"
STATISTICS_CSV = "algorithm_benchmark_paired_statistics.csv"
VALIDATION_CSV = "algorithm_benchmark_validation.csv"

RAW_FIELDNAMES = [
    "problem", "n_var", "n_obj", "run_idx", "seed", "algorithm", "runner",
    "evaluation_budget", "n_eval", "budget_utilization", "runtime_seconds",
    "front_size", "duplicate_fraction", "valid", "validation_status", "IGD", "HV",
]
SUMMARY_FIELDNAMES = [
    "problem", "n_var", "n_obj", "algorithm", "runner", "runs_total", "runs_valid",
    "IGD_mean", "IGD_std", "IGD_median", "IGD_best", "HV_mean", "HV_std",
    "HV_median", "HV_best", "runtime_mean", "n_eval_mean", "budget_utilization_mean",
]
VALIDATION_FIELDNAMES = [
    "problem", "run_idx", "seed", "algorithm", "valid", "validation_status",
    "validation_message", "front_size", "duplicate_fraction", "n_eval", "evaluation_budget",
]


@dataclass(frozen=True)
class AlgorithmSpec:
    name: str
    runner: str
    params: dict[str, Any]
    class_path: str | None = None
    sampling: str | None = None
    auto_ref_points: bool = False


@dataclass(frozen=True)
class RunOutcome:
    x: np.ndarray
    f: np.ndarray
    n_eval: int
    runtime_seconds: float


def load_algorithm_specs(paths: list[str]) -> list[AlgorithmSpec]:
    specs = []
    for path_text in paths:
        cfg = load_yaml_config(Path(path_text))
        specs.append(AlgorithmSpec(
            name=str(cfg["name"]), runner=str(cfg["runner"]),
            params=dict(cfg.get("params") or {}), class_path=cfg.get("class_path"),
            sampling=cfg.get("sampling"), auto_ref_points=bool(cfg.get("auto_ref_points", False)),
        ))
    names = [spec.name for spec in specs]
    if len(names) != len(set(names)):
        raise ValueError("algorithm names must be unique")
    return specs


def import_class(class_path: str):
    module_name, class_name = class_path.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def non_dominated_xy(x: np.ndarray, f: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)
    indices = NonDominatedSorting().do(f, only_non_dominated_front=True)
    return x[indices], f[indices]


def reference_front(problem, problem_cfg: dict) -> np.ndarray:
    """Create a deterministic reference front for ZDT/DTLZ-style problems."""

    name = str(problem_cfg["name"]).lower()
    if name.startswith("dtlz"):
        n_obj = int(problem.n_obj)
        partitions_by_objectives = {2: 200, 3: 20, 5: 6}
        partitions = int(
            problem_cfg.get("reference_partitions", partitions_by_objectives.get(n_obj, 6))
        )
        directions = get_reference_directions(
            "das-dennis", n_obj, n_partitions=partitions
        )
        front = problem.pareto_front(directions)
    else:
        front = problem.pareto_front()
    front = np.asarray(front, dtype=float)
    if front.ndim != 2 or front.shape[1] != int(problem.n_obj):
        raise ValueError(f"invalid Pareto front for {name}")
    return front


def _run_pymoo(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    if not spec.class_path:
        raise ValueError(f"{spec.name} uses runner=pymoo but has no class_path")
    budgeted = BudgetedProblem(problem, budget)
    params = dict(spec.params)
    params.setdefault("pop_size", pop_size)
    if spec.sampling == "initial_population":
        params.setdefault("sampling", initial_x)
    if spec.auto_ref_points:
        params.setdefault("ref_points", make_rnsga2_ref_points(problem, initial_x))
    algorithm = import_class(spec.class_path)(**params)
    start = time.perf_counter()
    result = None
    try:
        result = minimize(
            budgeted,
            algorithm,
            termination=("n_eval", budget),
            seed=seed,
            verbose=False,
            copy_algorithm=False,
        )
    except EvaluationBudgetExceeded:
        # Some pymoo algorithms perform extra internal evaluations (for
        # example DNSGA-II change detection). Preserve the last complete
        # population instead of allowing those evaluations to exceed the cap.
        pass
    runtime = time.perf_counter() - start
    if result is None or result.X is None or result.F is None:
        if algorithm.pop is None:
            raise RuntimeError(f"{spec.name} produced no checkpoint before budget exhaustion")
        x, f = algorithm.pop.get("X"), algorithm.pop.get("F")
    else:
        x, f = np.atleast_2d(result.X), np.atleast_2d(result.F)
    x, f = non_dominated_xy(x, f)
    return RunOutcome(x, f, budgeted.n_eval, runtime)


def _run_oade(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    np.random.seed(seed)
    random.seed(seed)
    budgeted = BudgetedProblem(problem, budget)
    solver = OADE_NSGAII(ProblemWrapper(budgeted), pop_size=pop_size, n_gen=budget)
    for key, value in spec.params.items():
        if hasattr(solver, key):
            setattr(solver, key, value)
    start = time.perf_counter()
    try:
        solver.run(initial_x=initial_x)
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x = np.asarray([item.X for item in solver.population], dtype=float)
    f = np.asarray([item.F for item in solver.population], dtype=float)
    x, f = non_dominated_xy(x, f)
    return RunOutcome(x, f, budgeted.n_eval, runtime)


def _run_cgde(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    budgeted = BudgetedProblem(problem, budget)
    solver = CGDE_NSGAII(CGDEProblemAdapter(budgeted), pop_size=pop_size, n_gen=budget, seed=seed, **spec.params)
    start = time.perf_counter()
    try:
        solver.run(initial_x=initial_x)
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x, f = non_dominated_xy(solver.result_X(), solver.result_F())
    return RunOutcome(x, f, budgeted.n_eval, runtime)


def _run_sdr(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    budgeted = BudgetedProblem(problem, budget)
    params = dict(spec.params)
    factor = params.pop("local_search_max_neighbors_factor", None)
    max_neighbors = None if factor is None else int(factor) * pop_size
    solver = NSGAIISDROLS(
        SDROLSProblemAdapter(budgeted), pop_size=pop_size, n_gen=budget, seed=seed,
        local_search_max_neighbors=max_neighbors, **params,
    )
    start = time.perf_counter()
    try:
        solver.run(initial_x=initial_x)
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x, f = non_dominated_xy(solver.result_X(), solver.result_F())
    return RunOutcome(x, f, budgeted.n_eval, runtime)


def _run_ce(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    budgeted = BudgetedProblem(problem, budget)
    solver = CEMOEA(budgeted, pop_size=pop_size, n_gen=budget, seed=seed, **spec.params)
    start = time.perf_counter()
    try:
        solver.run(initial_x=initial_x)
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x, f = non_dominated_xy(solver.population, solver.objectives)
    return RunOutcome(x, f, budgeted.n_eval, runtime)


def run_algorithm(spec, problem, pop_size, budget, initial_x, seed) -> RunOutcome:
    runners = {
        "pymoo": _run_pymoo, "local_oade": _run_oade, "local_cgde_nsga2": _run_cgde,
        "local_nsga2_sdr_ols": _run_sdr, "local_ce_moea": _run_ce,
    }
    if spec.runner not in runners:
        raise ValueError(f"unsupported runner: {spec.runner}")
    return runners[spec.runner](spec, problem, pop_size, budget, initial_x, seed)


def summarize(raw_rows: list[dict], specs: list[AlgorithmSpec]) -> list[dict]:
    rows = []
    keys = sorted({(row["problem"], row["n_var"], row["n_obj"]) for row in raw_rows})
    for problem, n_var, n_obj in keys:
        for spec in specs:
            selected = [row for row in raw_rows if row["problem"] == problem and row["algorithm"] == spec.name]
            valid = [row for row in selected if row["valid"]]
            if not valid:
                continue
            igd = np.asarray([row["IGD"] for row in valid])
            hv = np.asarray([row["HV"] for row in valid])
            runtime = np.asarray([row["runtime_seconds"] for row in valid])
            n_eval = np.asarray([row["n_eval"] for row in valid])
            utilization = np.asarray([row["budget_utilization"] for row in valid])
            rows.append({
                "problem": problem, "n_var": n_var, "n_obj": n_obj,
                "algorithm": spec.name, "runner": spec.runner,
                "runs_total": len(selected), "runs_valid": len(valid),
                "IGD_mean": float(np.mean(igd)), "IGD_std": float(np.std(igd, ddof=1)) if len(igd) > 1 else 0.0,
                "IGD_median": float(np.median(igd)), "IGD_best": float(np.min(igd)),
                "HV_mean": float(np.mean(hv)), "HV_std": float(np.std(hv, ddof=1)) if len(hv) > 1 else 0.0,
                "HV_median": float(np.median(hv)), "HV_best": float(np.max(hv)),
                "runtime_mean": float(np.mean(runtime)), "n_eval_mean": float(np.mean(n_eval)),
                "budget_utilization_mean": float(np.mean(utilization)),
            })
    return rows


def run_one_problem(problem_cfg: dict, cfg: dict, specs: list[AlgorithmSpec]) -> tuple[list[dict], list[dict]]:
    name = str(problem_cfg["name"])
    metadata_keys = {"reference_partitions", "label"}
    kwargs = {
        key: value for key, value in problem_cfg.items()
        if key != "name" and key not in metadata_keys
    }
    problem = get_problem(name, **kwargs)
    problem_label = str(
        problem_cfg.get(
            "label",
            f"{name}_m{int(problem.n_obj)}" if name.lower().startswith(("dtlz", "wfg")) else name,
        )
    )
    pareto_front = reference_front(problem, problem_cfg)
    igd_indicator = IGD(pareto_front)
    hv_indicator = HV(ref_point=np.max(pareto_front, axis=0) + 0.1)
    global_cfg = cfg["global"]
    runs, pop_size = int(global_cfg["runs"]), int(global_cfg["pop_size"])
    budget, seed_base = int(global_cfg["evaluation_budget"]), int(global_cfg["seed_base"])
    raw_rows, validation_rows = [], []
    for run_idx in range(runs):
        seed = seed_base + run_idx
        initial_x = make_initial_population(problem, pop_size, seed)
        for spec in specs:
            outcome = run_algorithm(spec, problem, pop_size, budget, initial_x, seed)
            validation = validate_result(outcome.x, outcome.f, problem)
            budget_valid = outcome.n_eval <= budget
            valid = validation.valid and budget_valid
            status = validation.status if budget_valid else "budget_exceeded"
            utilization = outcome.n_eval / budget
            row = {
                "problem": problem_label, "n_var": int(problem.n_var), "n_obj": int(problem.n_obj),
                "run_idx": run_idx, "seed": seed, "algorithm": spec.name, "runner": spec.runner,
                "evaluation_budget": budget, "n_eval": outcome.n_eval, "budget_utilization": utilization,
                "runtime_seconds": outcome.runtime_seconds, "front_size": validation.front_size,
                "duplicate_fraction": validation.duplicate_fraction, "valid": valid,
                "validation_status": status,
                "IGD": float(igd_indicator(outcome.f)) if valid else float("nan"),
                "HV": float(hv_indicator(outcome.f)) if valid else float("nan"),
            }
            raw_rows.append(row)
            validation_rows.append({
                "problem": problem_label, "run_idx": run_idx, "seed": seed, "algorithm": spec.name,
                "valid": valid, "validation_status": status, "validation_message": validation.message,
                "front_size": validation.front_size, "duplicate_fraction": validation.duplicate_fraction,
                "n_eval": outcome.n_eval, "evaluation_budget": budget,
            })
        print(f"[{problem_label}] run {run_idx + 1}/{runs} done (seed={seed}).")
    return raw_rows, validation_rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    args = parser.parse_args(argv)
    cfg = load_yaml_config(Path(args.config))
    specs = load_algorithm_specs([str(path) for path in cfg["algorithm_configs"]])
    out_dir = Path(cfg["global"]["out_dir"])
    raw_rows, validation_rows = [], []
    for problem_cfg in cfg["problems"]:
        problem_rows, problem_validation = run_one_problem(problem_cfg, cfg, specs)
        raw_rows.extend(problem_rows)
        validation_rows.extend(problem_validation)
    summary_rows = summarize(raw_rows, specs)
    stat_cfg = cfg.get("statistics", {})
    statistics_rows = paired_wilcoxon_rows(
        raw_rows, str(stat_cfg.get("reference_algorithm", "OADE_NSGAII")),
        float(stat_cfg.get("alpha", 0.05)),
    )
    write_csv(out_dir / RAW_CSV, raw_rows, RAW_FIELDNAMES)
    write_csv(out_dir / SUMMARY_CSV, summary_rows, SUMMARY_FIELDNAMES)
    write_csv(out_dir / STATISTICS_CSV, statistics_rows, STATISTICS_FIELDNAMES)
    write_csv(out_dir / VALIDATION_CSV, validation_rows, VALIDATION_FIELDNAMES)
    invalid = sum(not row["valid"] for row in raw_rows)
    print(f"Saved benchmark outputs to {out_dir.as_posix()} ({invalid} invalid runs).")


if __name__ == "__main__":
    main()
