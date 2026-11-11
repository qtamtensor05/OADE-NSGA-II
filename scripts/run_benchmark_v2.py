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
import argparse
import json
from copy import deepcopy
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from concurrent.futures import ProcessPoolExecutor, as_completed
import time

from src.utils.config import load_yaml_config
from src.benchmarking.algorithm_benchmark import (
    RAW_CSV,
    RAW_FIELDNAMES,
    VALIDATION_CSV,
    VALIDATION_FIELDNAMES,
    CONVERGENCE_CSV,
    CONVERGENCE_FIELDNAMES,
    load_algorithm_specs,
    persist_outputs,
    read_rows,
    run_single_seed,
    configured_problem_label,
    row_is_valid,
)
from src.benchmarking.provenance import (
    MANIFEST, make_manifest, prepare_manifest, assert_compatible,
    validate_records, checkpoint_manifest, file_hash, PRIMARY_FILES,
)


def run_benchmark_v2(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Reuse only execution-manifest-verified baselines")
    parser.add_argument("--config", default="config/algorithm_benchmark_v2.yaml")
    parser.add_argument("--baseline-dir", default="results/algorithm_benchmark")
    parser.add_argument("--out-dir")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args(argv)
    config_path = Path(args.config)
    cfg = load_yaml_config(config_path)
    if args.out_dir:
        cfg["global"]["out_dir"] = args.out_dir
    all_specs = load_algorithm_specs([str(p) for p in cfg["algorithm_configs"]])
    oade_spec = [s for s in all_specs if s.name == "OADE_NSGAII"]
    if not oade_spec:
        raise ValueError("OADE_NSGAII spec not found in config")

    out_dir = Path(cfg["global"]["out_dir"])
    v1_dir = Path(args.baseline_dir)
    baseline_specs = [s for s in all_specs if s.name != "OADE_NSGAII"]
    if not baseline_specs:
        raise ValueError("No comparator algorithms configured")
    manifest_path = v1_dir / MANIFEST
    if not manifest_path.exists():
        raise ValueError("Baseline lacks execution-time provenance. Preserve historical CSVs; "
                         "use main.py benchmark --config config/algorithm_benchmark_v2.yaml "
                         "--out-dir results/algorithm_benchmark_v2_reproduction to run all algorithms")
    saved = json.loads(manifest_path.read_text(encoding="utf-8"))
    current = make_manifest(cfg, all_specs)
    saved_baseline = deepcopy(saved)
    current_baseline = deepcopy(current)
    names = {s.name for s in baseline_specs}
    for manifest in (saved_baseline, current_baseline):
        manifest["protocol"]["algorithms"] = [s for s in manifest["protocol"]["algorithms"]
                                                if s["name"] in names]
    assert_compatible(saved_baseline, current_baseline)
    for name in PRIMARY_FILES:
        target = v1_dir / name
        if not target.exists() or saved.get("artifacts", {}).get(name) != file_hash(target):
            raise ValueError(f"Baseline integrity check failed: {name}")

    # 1. Read existing baseline rows from v1
    v1_raw = read_rows(v1_dir / RAW_CSV, RAW_FIELDNAMES)
    v1_val = read_rows(v1_dir / VALIDATION_CSV, VALIDATION_FIELDNAMES)
    v1_conv = read_rows(v1_dir / CONVERGENCE_CSV, CONVERGENCE_FIELDNAMES)

    # Filter to only the 6 baseline algorithms (excluding old OADE_NSGAII)
    baseline_raw = [r for r in v1_raw if r["algorithm"] != "OADE_NSGAII"]
    baseline_val = [r for r in v1_val if r["algorithm"] != "OADE_NSGAII"]
    baseline_conv = [r for r in v1_conv if r["algorithm"] != "OADE_NSGAII"]
    validate_records(baseline_raw, baseline_val, cfg, baseline_specs,
                     require_complete=True, convergence=baseline_conv)
    if args.preflight_only:
        print(f"Baseline preflight passed: {len(baseline_raw)} verified records; no runs started.")
        return
    current["reused_baseline"] = {"directory": str(v1_dir),
                                  "manifest_sha256": file_hash(manifest_path),
                                  "artifacts": saved["artifacts"]}
    manifest = prepare_manifest(out_dir, current)

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

        print(f"[{problem_label}] {runs}/{runs} runs completed in {time.perf_counter() - p_start:.2f}s.")

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
    validate_records(combined_raw, combined_val, cfg, all_specs,
                     require_complete=True, convergence=combined_conv)
    persist_outputs(out_dir, combined_raw, combined_val, combined_conv, all_specs, stat_cfg)
    checkpoint_manifest(out_dir, manifest)
    invalid = sum(not row_is_valid(row) for row in combined_raw)
    print(f"Persisted Benchmark v2 outputs to {out_dir}: {len(combined_raw)} total runs, {invalid} invalid.")


if __name__ == "__main__":
    run_benchmark_v2()
