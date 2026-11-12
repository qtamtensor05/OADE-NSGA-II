"""CSV reading and writing helpers."""

from __future__ import annotations

import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    from shared.artifacts import artifact_path
    from shared.paths import repository_path
    path = repository_path(path)
    path = artifact_path(path.parent, path.name)
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

