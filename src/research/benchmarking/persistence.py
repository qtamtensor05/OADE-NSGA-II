"""Primary checkpoint I/O and derived tables."""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
from .models import *
from .statistics import STATISTICS_FIELDNAMES, paired_wilcoxon_rows
from shared.io.csv_io import write_csv

__all__ = ["summarize", "summarize_costs", "read_rows", "row_is_valid", "persist_outputs"]

def summarize(raw_rows: list[dict], specs: list[AlgorithmSpec]) -> list[dict]:
    rows = []
    keys = sorted(
        {
            (str(row["problem"]), int(row["n_var"]), int(row["n_obj"]))
            for row in raw_rows
        }
    )
    for problem, n_var, n_obj in keys:
        for spec in specs:
            selected = [row for row in raw_rows if row["problem"] == problem and row["algorithm"] == spec.name]
            valid = [row for row in selected if row_is_valid(row)]
            if not valid:
                continue
            igd = np.asarray([row["IGD"] for row in valid], dtype=float)
            hv = np.asarray([row["HV"] for row in valid], dtype=float)
            runtime = np.asarray([row["runtime_seconds"] for row in valid], dtype=float)
            n_eval = np.asarray([row["n_eval"] for row in valid], dtype=float)
            utilization = np.asarray([row["budget_utilization"] for row in valid], dtype=float)
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



def summarize_costs(raw_rows: list[dict]) -> list[dict]:
    rows = []
    keys = sorted({(row["problem"], row["algorithm"]) for row in raw_rows})
    for problem, algorithm in keys:
        selected = [
            row for row in raw_rows
            if row["problem"] == problem and row["algorithm"] == algorithm and row_is_valid(row)
        ]
        if not selected:
            continue
        runtime = np.asarray([row["runtime_seconds"] for row in selected], dtype=float)
        n_eval = np.asarray([row["n_eval"] for row in selected], dtype=float)
        utilization = np.asarray(
            [row["budget_utilization"] for row in selected], dtype=float
        )
        front_size = np.asarray([row["front_size"] for row in selected], dtype=float)
        rows.append({
            "problem": problem,
            "algorithm": algorithm,
            "runs_valid": len(selected),
            "runtime_mean": float(np.mean(runtime)),
            "runtime_std": float(np.std(runtime, ddof=1)) if len(runtime) > 1 else 0.0,
            "runtime_median": float(np.median(runtime)),
            "n_eval_mean": float(np.mean(n_eval)),
            "budget_utilization_mean": float(np.mean(utilization)),
            "front_size_mean": float(np.mean(front_size)),
        })
    return rows



def read_rows(path: Path, expected_fields: list[str]) -> list[dict]:
    from .layout import artifact_path
    path = artifact_path(path.parent, path.name)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise ValueError(
                f"cannot resume from {path}: schema differs from the current pipeline"
            )
        return list(reader)



def row_is_valid(row: dict) -> bool:
    value = row.get("valid", True)
    return value.lower() == "true" if isinstance(value, str) else bool(value)



def persist_outputs(
    out_dir: Path,
    raw_rows: list[dict],
    validation_rows: list[dict],
    convergence_rows: list[dict],
    specs: list[AlgorithmSpec],
    stat_cfg: dict,
) -> None:
    from .layout import artifact_path
    # Persist primary evidence first. Derived summaries/statistics must never
    # cause completed runs to be lost if their calculation raises an error.
    write_csv(out_dir / RAW_CSV, raw_rows, RAW_FIELDNAMES)
    write_csv(out_dir / VALIDATION_CSV, validation_rows, VALIDATION_FIELDNAMES)
    write_csv(out_dir / CONVERGENCE_CSV, convergence_rows, CONVERGENCE_FIELDNAMES)
    summary_rows = summarize(raw_rows, specs)
    cost_rows = summarize_costs(raw_rows)
    statistics_rows = paired_wilcoxon_rows(
        raw_rows,
        str(stat_cfg.get("reference_algorithm", "OADE_NSGAII")),
        float(stat_cfg.get("alpha", 0.05)),
    )
    write_csv(artifact_path(out_dir, SUMMARY_CSV), summary_rows, SUMMARY_FIELDNAMES)
    write_csv(artifact_path(out_dir, STATISTICS_CSV), statistics_rows, STATISTICS_FIELDNAMES)
    write_csv(artifact_path(out_dir, COST_CSV), cost_rows, COST_FIELDNAMES)



