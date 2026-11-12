"""Solver execution contracts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np

@dataclass(frozen=True)
class AlgorithmSpec:
    name: str
    runner: str
    params: dict[str, Any]
    class_path: str | None = None
    sampling: str | None = None
    auto_ref_points: bool = False


@dataclass(frozen=True)
class RunOutcome:
    x: np.ndarray
    f: np.ndarray
    n_eval: int
    runtime_seconds: float
    convergence: tuple[dict, ...] = ()



