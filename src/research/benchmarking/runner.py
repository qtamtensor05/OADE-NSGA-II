"""Seed/problem orchestration and command line parsing."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from pymoo.indicators.hv import HV
from pymoo.indicators.igd import IGD
from pymoo.problems import get_problem
from pymoo.util.ref_dirs import get_reference_directions
from .models import *
from .adapters import ConvergenceRecorder, run_algorithm
from .evaluation import validate_result
from shared.population import make_initial_population
from .persistence import persist_outputs, read_rows, row_is_valid
from .provenance import make_manifest, prepare_manifest, checkpoint_manifest, validate_records
from shared.io.config import load_yaml_config

DEFAULT_CONFIG_PATH = Path("config/suites/algorithm_benchmark.yaml")

__all__ = ["DEFAULT_CONFIG_PATH", "load_algorithm_specs", "reference_front",
           "configured_problem_label", "run_single_seed", "run_one_problem", "main"]

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



def reference_front(problem, problem_cfg: dict) -> np.ndarray:
    """Create a deterministic reference front for ZDT/DTLZ-style problems."""

    name = str(problem_cfg["name"]).lower()
    if name.startswith(("dtlz", "wfg")):
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



def configured_problem_label(problem_cfg: dict) -> str:
    name = str(problem_cfg["name"])
    if "label" in problem_cfg:
        return str(problem_cfg["label"])
    if name.lower().startswith(("dtlz", "wfg")):
        return f"{name}_m{int(problem_cfg['n_obj'])}"
    return name



def run_single_seed(
    problem_cfg: dict,
    global_cfg: dict,
    specs: list[AlgorithmSpec],
    run_idx: int,
    *,
    run_solver=run_algorithm,
) -> tuple[list[dict], list[dict], list[dict]]:
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
    pop_size = int(global_cfg["pop_size"])
    budget, seed_base = int(global_cfg["evaluation_budget"]), int(global_cfg["seed_base"])
    raw_rows, validation_rows, convergence_rows = [], [], []
    seed = seed_base + run_idx
    initial_x = make_initial_population(problem, pop_size, seed)
    for spec in specs:
        recorder = ConvergenceRecorder(budget, igd_indicator, hv_indicator)
        outcome = run_solver(spec, problem, pop_size, budget, initial_x, seed, recorder)
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
        for point in outcome.convergence:
            convergence_rows.append({
                "problem": problem_label,
                "n_obj": int(problem.n_obj),
                "run_idx": run_idx,
                "seed": seed,
                "algorithm": spec.name,
                **point,
            })
    return raw_rows, validation_rows, convergence_rows



def run_one_problem(
    problem_cfg: dict,
    cfg: dict,
    specs: list[AlgorithmSpec],
    jobs: int = 1,
) -> tuple[list[dict], list[dict], list[dict]]:
    runs = int(cfg["global"]["runs"])
    problem_label = configured_problem_label(problem_cfg)
    results = []
    if jobs <= 1:
        for run_idx in range(runs):
            results.append(run_single_seed(problem_cfg, cfg["global"], specs, run_idx))
            print(f"[{problem_label}] run {run_idx + 1}/{runs} done.", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(run_single_seed, problem_cfg, cfg["global"], specs, run_idx): run_idx
                for run_idx in range(runs)
            }
            completed = 0
            for future in as_completed(futures):
                results.append(future.result())
                completed += 1
                print(
                    f"[{problem_label}] {completed}/{runs} runs done "
                    f"(latest run_idx={futures[future]}).",
                    flush=True,
                )

    raw_rows = [row for result in results for row in result[0]]
    validation_rows = [row for result in results for row in result[1]]
    convergence_rows = [row for result in results for row in result[2]]
    raw_rows.sort(key=lambda row: (int(row["run_idx"]), str(row["algorithm"])))
    validation_rows.sort(key=lambda row: (int(row["run_idx"]), str(row["algorithm"])))
    convergence_rows.sort(
        key=lambda row: (
            int(row["run_idx"]), str(row["algorithm"]), float(row["checkpoint_fraction"])
        )
    )
    return raw_rows, validation_rows, convergence_rows



def _main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--out-dir", help="new output directory; existing evidence is never overwritten")
    parser.add_argument("--experiment", help="create a versioned execution under results/experiments/<id>")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="resume after the last fully completed problem using current-schema CSV files",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=None,
        help="number of independent seed workers (default: config value or 1)",
    )
    args = parser.parse_args(argv)
    cfg = load_yaml_config(Path(args.config))
    jobs = int(args.jobs or cfg["global"].get("jobs", 1))
    if jobs < 1:
        raise ValueError("--jobs must be at least 1")
    specs = load_algorithm_specs([str(path) for path in cfg["algorithm_configs"]])
    from .layout import configure_output, snapshot_environment
    out_dir = configure_output(cfg, out_dir=args.out_dir, experiment=args.experiment, resume=args.resume)
    manifest = prepare_manifest(out_dir, make_manifest(cfg, specs), resume=args.resume)
    snapshot_environment(out_dir, manifest)
    from .layout import execution_log
    with execution_log(out_dir):
        _execute(cfg, specs, out_dir, manifest, args, jobs)


def _execute(cfg, specs, out_dir, manifest, args, jobs):
    if args.resume:
        raw_rows = read_rows(out_dir / RAW_CSV, RAW_FIELDNAMES)
        validation_rows = read_rows(out_dir / VALIDATION_CSV, VALIDATION_FIELDNAMES)
        convergence_rows = read_rows(out_dir / CONVERGENCE_CSV, CONVERGENCE_FIELDNAMES)
        validate_records(raw_rows, validation_rows, cfg, specs, convergence=convergence_rows)
        # Fail fast on schema/type/aggregation regressions before spending time
        # on another problem. This also repairs derived files after a previous
        # process stopped after primary evidence was checkpointed.
        persist_outputs(
            out_dir,
            raw_rows,
            validation_rows,
            convergence_rows,
            specs,
            cfg.get("statistics", {}),
        )
        checkpoint_manifest(out_dir, manifest)
        print(
            f"Resume preflight passed for {len(raw_rows)} existing run rows.",
            flush=True,
        )
    else:
        raw_rows, validation_rows, convergence_rows = [], [], []
    expected_per_problem = int(cfg["global"]["runs"]) * len(specs)
    print(f"Using {jobs} seed worker(s).", flush=True)
    for problem_cfg in cfg["problems"]:
        label = configured_problem_label(problem_cfg)
        completed = sum(str(row["problem"]) == label for row in raw_rows)
        if args.resume and completed == expected_per_problem:
            print(f"[{label}] resume: already complete ({completed} runs).")
            continue
        if args.resume and completed:
            raise ValueError(
                f"cannot safely resume partially completed problem {label}: "
                f"found {completed}/{expected_per_problem} rows"
            )
        problem_rows, problem_validation, problem_convergence = run_one_problem(
            problem_cfg, cfg, specs, jobs=jobs
        )
        raw_rows.extend(problem_rows)
        validation_rows.extend(problem_validation)
        convergence_rows.extend(problem_convergence)
        validate_records(raw_rows, validation_rows, cfg, specs, convergence=convergence_rows)
        persist_outputs(
            out_dir,
            raw_rows,
            validation_rows,
            convergence_rows,
            specs,
            cfg.get("statistics", {}),
        )
        checkpoint_manifest(out_dir, manifest)
        print(f"[{label}] checkpoint saved to {out_dir.as_posix()}.")
    validate_records(raw_rows, validation_rows, cfg, specs, require_complete=True,
                     convergence=convergence_rows)
    invalid = sum(not row_is_valid(row) for row in raw_rows)
    print(f"Saved benchmark outputs to {out_dir.as_posix()} ({invalid} invalid runs).")


def main(argv: list[str] | None = None) -> None:
    from research.maintenance.tmp_sessions import run_configured
    return run_configured(_main, argv)



