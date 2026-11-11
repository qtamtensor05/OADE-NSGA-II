"""Inventory existing evidence without asserting historical execution provenance."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inventory() -> dict:
    studies = {}
    for directory in sorted((ROOT / "results").iterdir()):
        if not directory.is_dir() or directory.name.startswith("smoke"):
            continue
        raw_path = directory / "algorithm_benchmark_raw_runs.csv"
        if not raw_path.exists():
            continue
        with raw_path.open(encoding="utf-8", newline="") as handle:
            raw = list(csv.DictReader(handle))
        stats_path = directory / "algorithm_benchmark_paired_statistics.csv"
        with stats_path.open(encoding="utf-8", newline="") as handle:
            stats = list(csv.DictReader(handle))
        invalid = [r for r in raw if r["valid"].lower() != "true"]
        keys = {(r["problem"], r["algorithm"], r["run_idx"]) for r in raw}
        studies[directory.name] = {
            "historical_execution_environment": "unknown; not inferred from current environment",
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
    return {"kind": "historical_inventory", "schema": 1,
            "observed_utc": datetime.now(timezone.utc).isoformat(),
            "boundary": "Observed file hashes are not execution-time provenance or independent replications",
            "studies": studies}


if __name__ == "__main__":
    target = ROOT / "results/research_inventory.json"
    target.write_text(json.dumps(inventory(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)}; historical primary evidence unchanged")
