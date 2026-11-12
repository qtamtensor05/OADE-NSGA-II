"""Stable artifact filenames and layout routing shared by readers/writers."""
import json
from pathlib import Path

RAW_CSV = "algorithm_benchmark_raw_runs.csv"
SUMMARY_CSV = "algorithm_benchmark_igd_hv_summary.csv"
STATISTICS_CSV = "algorithm_benchmark_paired_statistics.csv"
VALIDATION_CSV = "algorithm_benchmark_validation.csv"
CONVERGENCE_CSV = "algorithm_benchmark_convergence.csv"
COST_CSV = "algorithm_benchmark_cost_summary.csv"

PRIMARY = {RAW_CSV, VALIDATION_CSV, CONVERGENCE_CSV, "experiment_manifest.json"}


def execution_root(directory: Path) -> Path | None:
    directory = Path(directory)
    if (directory / "execution.json").is_file():
        metadata = json.loads((directory / "execution.json").read_text(encoding="utf-8"))
        if metadata.get("schema") != 1:
            raise ValueError("Unsupported execution envelope")
        return directory
    if directory.name in {"primary", "derived"} and (directory.parent / "execution.json").is_file():
        return execution_root(directory.parent)
    return None


def primary_directory(directory: Path) -> Path:
    root = execution_root(directory)
    return root / "primary" if root else Path(directory)


def artifact_path(directory: Path, filename: str) -> Path:
    root = execution_root(directory)
    if root:
        return root / ("primary" if filename in PRIMARY else "derived") / filename
    return Path(directory) / filename


