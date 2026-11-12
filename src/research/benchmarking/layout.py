"""Versioned experiment envelopes; historical flat datasets remain supported."""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import uuid
from contextlib import contextmanager, redirect_stderr, redirect_stdout

from shared.paths import ROOT, repository_path
from .models import RAW_CSV, VALIDATION_CSV, CONVERGENCE_CSV

from shared.artifacts import execution_root, primary_directory, artifact_path


def configure_output(cfg: dict, *, out_dir=None, experiment=None, resume=False) -> Path:
    if experiment:
        if out_dir or resume:
            raise ValueError("--experiment creates a fresh execution; resume using --out-dir <execution>")
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", experiment):
            raise ValueError("Experiment ID must use lower_snake_case")
        execution_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"
        directory = ROOT / "results/experiments" / experiment / execution_id
        directory.mkdir(parents=True, exist_ok=False)
        for name in ("primary", "derived", "figures", "qa", "config", "environment", "logs"):
            (directory / name).mkdir()
        metadata = {"schema": 1, "experiment_id": experiment, "execution_id": execution_id,
                    "created_utc": datetime.now(timezone.utc).isoformat(),
                    "command": [sys.executable, *sys.argv]}
        (directory / "execution.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        (directory / "config/resolved.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    else:
        directory = Path(out_dir) if out_dir else repository_path(cfg["global"]["out_dir"])
    return primary_directory(directory)


def snapshot_environment(directory: Path, manifest: dict):
    root = execution_root(directory)
    if root:
        target = root / "environment/runtime.json"
        if not target.exists():
            target.write_text(json.dumps(manifest["environment"], indent=2) + "\n", encoding="utf-8")
            import importlib.metadata
            packages = {item.metadata["Name"]: item.version for item in importlib.metadata.distributions()
                        if item.metadata["Name"]}
            (root / "environment/installed_packages.json").write_text(
                json.dumps(packages, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            (root / "config/algorithms.json").write_text(
                json.dumps(manifest["protocol"]["algorithms"], indent=2) + "\n", encoding="utf-8")


@contextmanager
def execution_log(directory: Path):
    root = execution_root(directory)
    if root is None:
        yield
        return
    from research.maintenance.tmp_sessions import Tee
    with (root / "logs/run.log").open("a", encoding="utf-8") as log:
        with redirect_stdout(Tee(sys.stdout, log)), redirect_stderr(Tee(sys.stderr, log)):
            try:
                yield
            except BaseException:
                (root / "logs/status.json").write_text(json.dumps({"status": "failed"}) + "\n")
                raise
            else:
                (root / "logs/status.json").write_text(json.dumps({"status": "completed"}) + "\n")
