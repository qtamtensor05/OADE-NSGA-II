"""Build reproducible, source-traceable per-problem research folders.

Run from any directory: python scripts/organize_by_problem.py
Only standard-library modules are required. Source evidence is never moved.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
from collections import defaultdict
from problem_reports import generate_reports
from csv_archives import archive_lookup, verify
from research_readmes import generate_readmes

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/by_problem"
ARCHIVED = archive_lookup()
SOURCES = {
    "benchmark_classic": "results/algorithm_benchmark",
    "benchmark_adaptive": "results/algorithm_benchmark_v2",
    "restart_confirmation": "results/restart_confirmation",
    "ablation_classic": "results/ablation",
    "sensitivity_classic": "results/sensitivity",
    "sensitivity_adaptive": "results/experiments/zdt_sensitivity_ofat_v1/derived",
    "benchmark_dtlz": "results/dtlz_benchmark",
    "benchmark_wfg_m2": "results/wfg_m2_7algo_benchmark",
    "benchmark_wfg_scaling": "results/wfg_compact_benchmark",
    "sensitivity_dtlz": "results/experiments/dtlz_sensitivity_ofat_v1/derived",
}
REPORTS = {
    "zdt": ["docs/reports/benchmark_v2_results_report.md",
            "docs/reports/restart_confirmation_report.md",
            "docs/reports/ablation_results_report.md",
            "docs/reports/zdt_parameter_sensitivity_report.md",
            "docs/reports/sensitivity_analysis.md",
            "docs/protocols/zdt_sensitivity.md",
            "docs/protocols/experiment_registry.md",
            "results/provenance/zdt_composition.json",
            "results/provenance/zdt_validation.json",
            "results/experiments/zdt_sensitivity_ofat_v1/study_manifest.json"],
    "dtlz": ["docs/reports/dtlz_results_report.md", "docs/protocols/dtlz_sensitivity.md"],
    "wfg": ["docs/reports/wfg_compact_report.md"],
}


def link(base, path):
    path = ARCHIVED.get(path, path)
    return os.path.relpath(ROOT / path, base).replace("\\", "/")


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if any(not (ROOT / path).exists() for path in ARCHIVED):
        verify(restore=True)
    evidence = defaultdict(list)
    coverage = []
    for category, source_dir in SOURCES.items():
        for source in sorted((ROOT / source_dir).glob("*.csv")):
            with source.open(newline="", encoding="utf-8-sig") as stream:
                reader = csv.DictReader(stream)
                fields = reader.fieldnames or []
                if "problem" not in fields:
                    continue
                groups = defaultdict(list)
                for row in reader:
                    problem = row["problem"].lower()
                    if re.fullmatch(r"(?:zdt|dtlz|wfg)\d+(?:_m\d+)?", problem):
                        groups[problem].append(row)
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            for problem, rows in sorted(groups.items()):
                family = "zdt" if problem.startswith("zdt") else "dtlz" if problem.startswith("dtlz") else "wfg"
                destination = OUT / family / problem / category / source.name
                write_csv(destination, fields, rows)
                record = {"category": category, "source": source.relative_to(ROOT).as_posix(),
                          "source_sha256": source_hash,
                          "output": destination.relative_to(ROOT).as_posix(),
                          "output_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                          "rows": len(rows), "filter": {"problem": problem}}
                evidence[(family, problem)].append(record)
                if source.name.endswith("raw_runs.csv"):
                    coverage.append({"family": family, "problem": problem, "study": category,
                                     "rows": len(rows),
                                     "algorithms": ";".join(sorted({r.get("algorithm", "OADE_NSGAII") for r in rows})),
                                     "seeds": len({r.get("seed", "") for r in rows}),
                                     "source": record["source"]})

    for (family, problem), records in sorted(evidence.items()):
        base = OUT / family / problem
        generate_reports(base, family, problem, records, REPORTS[family], link)
        (base / "manifest.json").write_text(json.dumps({
            "problem": problem, "artifacts": records,
            "note": "Filtered views, not new independent executions. Original statistical correction families are preserved."
        }, indent=2) + "\n", encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "coverage.csv", ["family", "problem", "study", "rows", "algorithms", "seeds", "source"], coverage)
    generate_readmes()
    print(f"Organized {len(evidence)} problems, {sum(len(v) for v in evidence.values())} CSV views in {OUT}")


if __name__ == "__main__":
    main()
