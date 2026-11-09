"""Evaluation accounting and result validation for fair benchmarks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


class EvaluationBudgetExceeded(RuntimeError):
    """Raised before an objective evaluation would exceed the fixed budget."""


class BudgetedProblem:
    """Problem proxy that counts and strictly limits objective evaluations."""

    def __init__(self, problem: Any, max_evaluations: int) -> None:
        if max_evaluations <= 0:
            raise ValueError("max_evaluations must be positive")
        self._problem = problem
        self.max_evaluations = int(max_evaluations)
        self.n_eval = 0
        self.n_var = int(problem.n_var)
        self.n_obj = int(problem.n_obj)
        self.xl = np.asarray(problem.xl, dtype=float)
        self.xu = np.asarray(problem.xu, dtype=float)

    @property
    def remaining_evaluations(self) -> int:
        return self.max_evaluations - self.n_eval

    def evaluate(self, x: np.ndarray, *args, **kwargs):
        values = np.asarray(x)
        count = 1 if values.ndim == 1 else len(values)
        if count > self.remaining_evaluations:
            raise EvaluationBudgetExceeded(
                f"evaluation request of {count} exceeds remaining budget "
                f"{self.remaining_evaluations}"
            )
        result = self._problem.evaluate(x, *args, **kwargs)
        self.n_eval += count
        return result

    def pareto_front(self, *args, **kwargs):
        return self._problem.pareto_front(*args, **kwargs)

    def __getattr__(self, name: str):
        return getattr(self._problem, name)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    status: str
    message: str
    front_size: int
    duplicate_fraction: float


def validate_result(
    x: np.ndarray,
    f: np.ndarray,
    problem: Any,
    *,
    expected_objectives: int | None = None,
) -> ValidationResult:
    """Validate bounds, shapes, finiteness, and basic front diversity."""

    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)
    n_obj = int(expected_objectives or problem.n_obj)

    if x.ndim != 2 or f.ndim != 2:
        return ValidationResult(False, "invalid_shape", "X and F must be 2D", 0, 1.0)
    if len(x) == 0 or len(f) == 0:
        return ValidationResult(False, "empty_front", "result front is empty", 0, 1.0)
    if len(x) != len(f):
        return ValidationResult(False, "length_mismatch", "X and F row counts differ", len(f), 1.0)
    if x.shape[1] != int(problem.n_var) or f.shape[1] != n_obj:
        return ValidationResult(False, "invalid_shape", "decision/objective dimensions are incorrect", len(f), 1.0)
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(f)):
        return ValidationResult(False, "non_finite", "result contains NaN or infinity", len(f), 1.0)

    xl = np.asarray(problem.xl, dtype=float)
    xu = np.asarray(problem.xu, dtype=float)
    tolerance = 1e-10
    if np.any(x < xl - tolerance) or np.any(x > xu + tolerance):
        return ValidationResult(False, "out_of_bounds", "decision vectors violate bounds", len(f), 1.0)

    rounded = np.round(f, decimals=12)
    unique_count = len(np.unique(rounded, axis=0))
    duplicate_fraction = 1.0 - unique_count / len(f)
    if len(f) > 1 and unique_count == 1:
        return ValidationResult(
            False,
            "collapsed_front",
            "all objective vectors are identical",
            len(f),
            duplicate_fraction,
        )

    return ValidationResult(True, "ok", "validated", len(f), duplicate_fraction)

