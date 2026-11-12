"""Run/report ZDT OFAT sensitivity from parameter lists, without model selection."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import redirect_stderr, redirect_stdout
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from pymoo.problems import get_problem

from oade_nsga2.runner import run_instrumented
from shared.contracts import AlgorithmSpec
from shared.evaluation import validate_result
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv
from shared.paths import ROOT, repository_path
from shared.population import make_initial_population
from research.benchmarking.convergence import ConvergenceRecorder
from research.benchmarking.provenance import digest, file_hash, environment
from research.maintenance.tmp_sessions import Tee, create, finish, session_lock, save
from .zdt_sensitivity_design import design, plan, task_id
from .zdt_sensitivity_analysis import analyze, report

DEFAULT_CONFIG = "config/studies/zdt_sensitivity.yaml"


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def identity(cfg, candidates):
    sources = sorted([*ROOT.joinpath("src").rglob("*.py"), ROOT / "requirements.txt", ROOT / "pyproject.toml",
                      ROOT / "analysis/figures/plot_zdt_sensitivity.R", ROOT / "analysis/figures/helpers/panel_alignment.R"])
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    return {"schema": 1, "kind": "zdt_ofat_execution", "protocol": cfg, "candidates": candidates,
            "source_hashes": {p.relative_to(ROOT).as_posix(): file_hash(p) for p in sources},
            "environment": environment(), "git_commit": commit, "artifacts": {}, "reference_sha256": None}


def open_study(directory, current, resume):
    path = directory / "study_manifest.json"
    if path.exists():
        if not resume:
            raise ValueError("Study already exists; use --resume or a new --out-dir")
        saved = json.loads(path.read_text(encoding="utf-8"))
        for key in ("schema", "kind", "protocol", "candidates", "source_hashes", "environment"):
            if saved.get(key) != current.get(key):
                raise ValueError(f"OFAT identity changed: {key}; use a fresh directory")
        for name, checksum in saved["artifacts"].items():
            if not (directory / name).is_file() or file_hash(directory / name) != checksum:
                raise ValueError(f"Checkpoint integrity mismatch: {name}")
        if {p.relative_to(directory).as_posix() for p in (directory / "primary").glob("*.json")} != set(saved["artifacts"]):
            raise ValueError("Orphan/uncommitted primary evidence; preserve directory for inspection")
        return saved
    if resume:
        raise ValueError("Missing OFAT manifest; previous selection/historical datasets cannot be resumed here")
    if directory.exists() and any(directory.iterdir()):
        raise ValueError("Fresh study requires an empty output directory")
    atomic_json(path, current)
    atomic_json(directory / "config/resolved.json", {"protocol": current["protocol"], "candidates": current["candidates"]})
    return current


def reference_fronts(directory, manifest, cfg):
    path = directory / "config/reference_fronts.json"
    if manifest["reference_sha256"]:
        if not path.exists() or file_hash(path) != manifest["reference_sha256"]:
            raise ValueError("Reference snapshot integrity mismatch")
        return json.loads(path.read_text(encoding="utf-8"))
    if path.exists():
        raise ValueError("Uncommitted reference snapshot")
    fronts = {}
    for p in cfg["problems"]:
        front = np.asarray(get_problem(p["name"], n_var=p["n_var"]).pareto_front(), dtype=float)
        if front.ndim != 2 or front.shape[1] != 2 or not len(front) or not np.all(np.isfinite(front)):
            raise ValueError("Invalid ZDT reference front")
        fronts[p["name"]] = front.tolist()
    atomic_json(path, fronts)
    manifest["reference_sha256"] = file_hash(path)
    atomic_json(directory / "study_manifest.json", manifest)
    return fronts


def run_task(cfg, candidate, problem_cfg, seed):
    settings = candidate["settings"]
    problem = get_problem(problem_cfg["name"], n_var=problem_cfg["n_var"])
    front = np.asarray(cfg["reference_fronts"][problem_cfg["name"]])
    igd, hv = IGD(front), HV(ref_point=np.max(front, axis=0) + 0.1)
    budget = cfg["global"]["evaluation_budget"]
    recorder = ConvergenceRecorder(budget, igd, hv)
    spec = AlgorithmSpec(name="OADE_NSGAII", runner="local_oade", params={k: v for k, v in settings.items() if k != "pop_size"})
    outcome, observed = run_instrumented(spec, problem, settings["pop_size"], budget,
                                        make_initial_population(problem, settings["pop_size"], seed), seed, recorder)
    validation = validate_result(outcome.x, outcome.f, problem)
    valid = validation.valid and 0 < outcome.n_eval <= budget
    igd_value, hv_value = (float(igd(outcome.f)), float(hv(outcome.f))) if valid else (None, None)
    if valid and not (np.isfinite(igd_value) and np.isfinite(hv_value)):
        valid, igd_value, hv_value = False, None, None
    return {"candidate": candidate["id"], "parameter": candidate["parameter"], "level": candidate["level"],
            "problem": problem_cfg["name"], "n_var": problem_cfg["n_var"], "seed": seed,
            "settings": settings, "evaluation_budget": budget, "n_eval": outcome.n_eval,
            "valid": valid, "validation_status": validation.status if validation.valid == valid else "invalid_metric_or_budget",
            "front_size": validation.front_size, "IGD": igd_value, "HV": hv_value,
            "runtime_seconds": outcome.runtime_seconds, "reference_sha256": digest(front.tolist()),
            "convergence": list(outcome.convergence), **observed}


def tasks(cfg, candidates):
    return {task_id(c["id"], p["name"], seed): (c, p, seed)
            for c in candidates for p in cfg["problems"] for seed in cfg["global"]["seeds"]}


def load_records(directory, manifest):
    return [json.loads((directory / name).read_text(encoding="utf-8")) for name in sorted(manifest["artifacts"])]


def validate_records(cfg, candidates, rows, complete=False):
    expected = tasks(cfg, candidates)
    seen = set()
    for row in rows:
        key = task_id(row["candidate"], row["problem"], row["seed"])
        if key not in expected or key in seen:
            raise ValueError("Unexpected/duplicate OFAT task")
        seen.add(key)
        candidate, problem, seed = expected[key]
        if (row["settings"] != candidate["settings"] or row["parameter"] != candidate["parameter"]
                or row["level"] != candidate["level"] or row["n_var"] != problem["n_var"]
                or row["evaluation_budget"] != cfg["global"]["evaluation_budget"]
                or not 0 < row["n_eval"] <= row["evaluation_budget"]):
            raise ValueError("Settings, dimensions or evaluation accounting changed")
        if type(row["valid"]) is not bool or row["valid"] and any(row[m] is None or not np.isfinite(row[m]) for m in ("IGD", "HV")):
            raise ValueError("Invalid quality record")
        if row["reference_sha256"] != digest(cfg["reference_fronts"][row["problem"]]):
            raise ValueError("Runs do not share the captured reference front")
        if any(type(v) is not int or v < 0 for v in row["telemetry"].values()):
            raise ValueError("Invalid restart telemetry")
    if complete and seen != set(expected):
        raise ValueError(f"Incomplete OFAT study: {len(seen)}/{len(expected)} tasks")


def execute(directory, manifest, cfg, candidates, jobs):
    expected = tasks(cfg, candidates)
    validate_records(cfg, candidates, load_records(directory, manifest))
    pending = {key: value for key, value in expected.items() if f"primary/{key}.json" not in manifest["artifacts"]}

    def checkpoint(key, row):
        c, p, seed = expected[key]
        if (row["candidate"], row["problem"], row["seed"]) != (c["id"], p["name"], seed):
            raise ValueError("Worker returned the wrong task")
        validate_records(cfg, candidates, [row])
        filename = f"primary/{key}.json"
        atomic_json(directory / filename, row)
        manifest["artifacts"][filename] = file_hash(directory / filename)
        atomic_json(directory / "study_manifest.json", manifest)
        print(f"[OFAT] {len(manifest['artifacts'])}/{len(expected)}: {row['parameter']}={row['level']} {row['problem']} seed={seed}", flush=True)

    if jobs == 1:
        for key, (candidate, problem, seed) in pending.items():
            checkpoint(key, run_task(cfg, candidate, problem, seed))
    else:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures = {pool.submit(run_task, cfg, c, p, seed): key for key, (c, p, seed) in pending.items()}
            for future in as_completed(futures):
                checkpoint(futures[future], future.result())


def write_outputs(directory, manifest, cfg, candidates):
    rows = load_records(directory, manifest)
    validate_records(cfg, candidates, rows, complete=True)
    summaries, comparisons = analyze(cfg, candidates, rows)
    scalar = [{k: v for k, v in row.items() if k not in {"settings", "convergence", "adaptation_trace", "telemetry"}}
              | {"settings_json": json.dumps(row["settings"], sort_keys=True)} | row["telemetry"] for row in rows]
    for filename, data in (("raw_runs.csv", scalar), ("summary.csv", summaries), ("comparisons.csv", comparisons)):
        write_csv(directory / "derived" / filename, data, list(data[0]))
    (directory / "derived/report.md").write_text(report(cfg, candidates, rows, summaries, comparisons), encoding="utf-8")
    return rows


def r_runtime():
    executable = shutil.which("Rscript")
    if not executable and os.name == "nt":
        options = sorted(Path(os.environ.get("ProgramFiles", "C:/Program Files")).glob("R/*/bin/Rscript.exe"))
        executable = str(options[-1]) if options else None
    if not executable:
        raise RuntimeError("Rscript is required for --stage all/plot. Use --stage run to collect measurements only.")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", TMPDIR=str(ROOT / "tmp"))
    libraries = sorted((ROOT / "renv/library/windows").glob("*/*")) if os.name == "nt" else []
    if libraries:
        env["R_LIBS_USER"] = str(libraries[-1])
    return executable, env


def check_plot_runtime():
    executable, env = r_runtime()
    code = 'for(p in c("ggplot2","patchwork","jsonlite","ragg","svglite")) if(!requireNamespace(p,quietly=TRUE)) stop(paste("Missing R package:",p))'
    result = subprocess.run([executable, "--vanilla", "-e", code], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError(result.stderr)


def plot_outputs(directory):
    executable, env = r_runtime()
    env["ZDT_SENSITIVITY_DIR"] = str(directory.resolve())
    code = ('Sys.setlocale("LC_CTYPE","English_United States.utf8"); ' if os.name == "nt" else '')
    code += 'source("analysis/figures/plot_zdt_sensitivity.R",encoding="UTF-8")'
    result = subprocess.run([executable, "--vanilla", "-e", code], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(result.stdout)
    if result.returncode:
        raise RuntimeError("Figure stage failed; primary measurements are preserved. " + result.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--stage", choices=("plan", "run", "report", "plot", "all"), default="plan")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--jobs", type=int)
    args = parser.parse_args(argv)
    cfg, candidates = design(load_yaml_config(Path(args.config)))
    if args.stage == "plan":
        print(json.dumps(plan(cfg, candidates), indent=2))
        return
    jobs = cfg["global"].get("jobs", 1) if args.jobs is None else args.jobs
    if jobs < 1:
        raise ValueError("--jobs must be positive")
    if args.stage in {"all", "plot"}:
        check_plot_runtime()
    if args.stage in {"report", "plot"} and not args.resume:
        raise ValueError("Existing measurements require --resume for report/plot")
    session = None
    if cfg.get("smoke") and args.out_dir is None:
        if args.resume:
            raise ValueError("Resume smoke with its explicit --out-dir")
        session = create("smoke", "zdt_ofat")
        metadata = json.loads((session / "session.json").read_text(encoding="utf-8"))
        metadata["command"] = [sys.executable, "-m", "research", "sensitivity-zdt", *(argv or sys.argv[2:])]
        save(session, metadata)
    directory = (args.out_dir or (session / "output" if session else repository_path(cfg["global"]["out_dir"]))).resolve()
    lock = session or ROOT / "tmp/study_locks" / digest(str(directory))
    lock.mkdir(parents=True, exist_ok=True)
    try:
        with session_lock(lock):
            current = identity(cfg, candidates)
            current["invocation"] = [sys.executable, "-m", "research", "sensitivity-zdt", *(argv or sys.argv[2:])]
            current["workers"] = jobs
            manifest = open_study(directory, current, args.resume)
            cfg = {**cfg, "reference_fronts": reference_fronts(directory, manifest, cfg)}
            (directory / "logs").mkdir(exist_ok=True)
            with (directory / "logs/run.log").open("a", encoding="utf-8") as handle:
                with redirect_stdout(Tee(sys.stdout, handle)), redirect_stderr(Tee(sys.stderr, handle)):
                    if args.stage in {"run", "all"}:
                        execute(directory, manifest, cfg, candidates, jobs)
                    rows = write_outputs(directory, manifest, cfg, candidates)
                    if args.stage in {"all", "plot"}:
                        plot_outputs(directory)
                    print(f"OFAT complete: {len(rows)} measured runs. No scoring or automatic parameter selection.")
        print(f"Results: {directory}")
    except BaseException:
        if session:
            finish(session, status="failed", disposable=False)
        raise
    else:
        if session:
            finish(session, disposable=True)
