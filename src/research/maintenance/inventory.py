"""Inventory result artifacts and link any recorded algorithm-block provenance."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from shared.paths import ROOT
from research.benchmarking.layout import artifact_path


def inventory() -> dict:
    studies = {}
    composition_path = ROOT / "results/provenance/zdt_composition.json"
    composition = (json.loads(composition_path.read_text(encoding="utf-8"))
                   if composition_path.exists() else {"datasets": {}})
    provenance_links = {name: "results/provenance/zdt_composition.json"
                        for name in composition["datasets"]}
    multi_path = ROOT / "results/provenance/multiobjective_composition.json"
    if multi_path.exists():
        provenance_links.update({name: "results/provenance/multiobjective_composition.json"
                                 for name in json.loads(multi_path.read_text(encoding="utf-8"))["datasets"]})
    directories = list((ROOT / "results").iterdir())
    directories.extend((ROOT / "results/experiments").glob("*/*/primary"))
    for directory in sorted(directories):
        if not directory.is_dir() or directory.name.startswith("smoke"):
            continue
        raw_path = directory / "algorithm_benchmark_raw_runs.csv"
        if not raw_path.exists():
            continue
        with raw_path.open(encoding="utf-8", newline="") as handle:
            raw = list(csv.DictReader(handle))
        stats_path = artifact_path(directory, "algorithm_benchmark_paired_statistics.csv")
        with stats_path.open(encoding="utf-8", newline="") as handle:
            stats = list(csv.DictReader(handle))
        invalid = [r for r in raw if r["valid"].lower() != "true"]
        keys = {(r["problem"], r["algorithm"], r["run_idx"]) for r in raw}
        key = directory.parent.relative_to(ROOT / "results").as_posix() if directory.name == "primary" else directory.name
        studies[key] = {
            "execution_environment_provenance": (
                provenance_links[directory.name] + ": RNSGA2 execution captured; other blocks archived"
                if directory.name in provenance_links
                else str((directory / "experiment_manifest.json").relative_to(ROOT))
                if (directory / "experiment_manifest.json").exists()
                else "unknown; not inferred from current environment"
            ),
            "observed_artifact_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in sorted(directory.glob("*.csv"))},
            "records": len(raw), "duplicate_keys": len(raw) - len(keys),
            "seed_values": sorted({int(r["seed"]) for r in raw}),
            "invalid_records": len(invalid),
            "invalid_groups": dict(Counter(f"{r['problem']}/{r['algorithm']}/{r['validation_status']}"
                                           for r in invalid)),
            "budget_overruns": sum(int(r["n_eval"]) > int(r["evaluation_budget"]) for r in raw),
            "pair_count_range": [min(int(r["n_pairs"]) for r in stats),
                                 max(int(r["n_pairs"]) for r in stats)] if stats else None,
            "outcomes": dict(Counter(r["result"] for r in stats)),
        }
    return {"kind": "artifact_inventory", "schema": 1,
            "observed_utc": datetime.now(timezone.utc).isoformat(),
            "boundary": "Observed file hashes are not execution-time provenance or independent replications",
            "studies": studies}


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "results/research_inventory.json")
    args = parser.parse_args(argv)
    target = args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(inventory(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target}; primary evidence unchanged")
