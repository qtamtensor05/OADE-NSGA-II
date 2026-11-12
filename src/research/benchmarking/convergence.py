"""Metric recording belongs to the experiment layer."""
from __future__ import annotations
import numpy as np
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

class ConvergenceRecorder:
    def __init__(self, budget: int, igd_indicator: IGD, hv_indicator: HV) -> None:
        self.targets = [(fraction / 10.0, budget * fraction // 10) for fraction in range(1, 11)]
        self.igd_indicator = igd_indicator
        self.hv_indicator = hv_indicator
        self.rows: list[dict] = []
        self._next = 0

    def record(self, n_eval: int, objectives: np.ndarray | None) -> None:
        if objectives is None or self._next >= len(self.targets):
            return
        objectives = np.asarray(objectives, dtype=float)
        if objectives.ndim != 2 or len(objectives) == 0 or not np.all(np.isfinite(objectives)):
            return
        front = objectives[NonDominatedSorting().do(objectives, only_non_dominated_front=True)]
        while self._next < len(self.targets) and n_eval >= self.targets[self._next][1]:
            fraction, target = self.targets[self._next]
            self.rows.append({
                "checkpoint_fraction": fraction,
                "target_evaluations": target,
                "n_eval": n_eval,
                "IGD": float(self.igd_indicator(front)),
                "HV": float(self.hv_indicator(front)),
            })
            self._next += 1
