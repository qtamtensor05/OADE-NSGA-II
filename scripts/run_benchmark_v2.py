#!/usr/bin/env python3
"""
Reproducible Benchmark v2 Runner for OADE-NSGA-II.
Evaluates OADE-NSGA-II v2 (with Adaptive Restart) across 30 seeds (42..71) on all 5 ZDT problems,
merging with the exact identical 30-seed baseline runs of the 6 comparator algorithms
(NSGA-II, CGDE, SDR-OLS, CE-MOEA, DNSGA-II, RNSGA-II).
Outputs full paired inferential statistics and summaries to results/algorithm_benchmark_v2/.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import numpy as np

from src.utils.config import load_yaml_config
from src.benchmarking.algorithm_benchmark import (
    RAW_CSV,
    RAW_FIELDNAMES,
    VALIDATION_CSV,
    VALIDATION_FIELDNAMES,
    CONVERGENCE_CSV,
    CONVERGENCE_FIELDNAMES,
    AlgorithmSpec,
    load_algorithm_specs,
    persist_outputs,
    read_rows,
    run_single_seed,
    configured_problem_label,
)


def run_benchmark_v2() -> None:
    config_path = Path("config/algorithm_benchmark_v2.yaml")
    cfg = load_yaml_config(config_path)
    all_specs = load_algorithm_specs([str(p) for p in cfg["algorithm_configs"]])
    oade_spec = [s for s in all_specs if s.name == "OADE_NSGAII"]
    if not oade_spec:
        raise ValueError("OADE_NSGAII spec not found in config")

    out_dir = Path(cfg["global"]["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    v1_dir = Path("results/algorithm_benchmark")

    # 1. Read existing baseline rows from v1
    v1_raw = read_rows(v1_dir / RAW_CSV, RAW_FIELDNAMES)
    v1_val = read_rows(v1_dir / VALIDATION_CSV, VALIDATION_FIELDNAMES)
    v1_conv = read_rows(v1_dir / CONVERGENCE_CSV, CONVERGENCE_FIELDNAMES)

    # Filter to only the 6 baseline algorithms (excluding old OADE_NSGAII)
    baseline_raw = [r for r in v1_raw if r["algorithm"] != "OADE_NSGAII"]
    baseline_val = [r for r in v1_val if r["algorithm"] != "OADE_NSGAII"]
    baseline_conv = [r for r in v1_conv if r["algorithm"] != "OADE_NSGAII"]

    print(f"Loaded {len(baseline_raw)} baseline run rows from v1 (6 comparator algorithms).")

    # 2. Run OADE-NSGA-II v2 (Adaptive Restart) on all 5 problems across 30 seeds
    runs = int(cfg["global"]["runs"])
    jobs = int(cfg["global"].get("jobs", 6))
    print(f"Running OADE-NSGA-II v2 across {len(cfg['problems'])} problems, {runs} seeds with {jobs} workers...")

    oade_raw, oade_val, oade_conv = [], [], []
    start_time = time.perf_counter()

    for problem_cfg in cfg["problems"]:
        problem_label = configured_problem_label(problem_cfg)
        p_start = time.perf_counter()
        results = []
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(run_single_seed, problem_cfg, cfg["global"], oade_spec, run_idx): run_idx
                for run_idx in range(runs)
            }
            for future in as_completed(futures):
                results.append(future.result())

        for res in results:
            oade_raw.extend(res[0])
            oade_val.extend(res[1])
            oade_conv.extend(res[2])

        print(f"[{problem_label}] 30/30 runs completed in {time.perf_counter() - p_start:.2f}s.")

    print(f"All OADE-NSGA-II v2 runs completed in {time.perf_counter() - start_time:.2f}s.")

    # 3. Merge baseline and OADE v2 rows
    combined_raw = baseline_raw + oade_raw
    combined_val = baseline_val + oade_val
    combined_conv = baseline_conv + oade_conv

    # Ensure correct sort ordering
    combined_raw.sort(key=lambda r: (str(r["problem"]), int(r["run_idx"]), str(r["algorithm"])))
    combined_val.sort(key=lambda r: (str(r["problem"]), int(r["run_idx"]), str(r["algorithm"])))
    combined_conv.sort(
        key=lambda r: (
            str(r["problem"]), int(r["run_idx"]), str(r["algorithm"]), float(r["checkpoint_fraction"])
        )
    )

    # 4. Compute summaries and paired Wilcoxon statistics with Holm correction
    stat_cfg = cfg.get("statistics", {"reference_algorithm": "OADE_NSGAII", "alpha": 0.05})
    persist_outputs(out_dir, combined_raw, combined_val, combined_conv, all_specs, stat_cfg)
    print(f"Persisted Benchmark v2 outputs to {out_dir}: {len(combined_raw)} total runs, 0 invalid.")


if __name__ == "__main__":
    run_benchmark_v2()
