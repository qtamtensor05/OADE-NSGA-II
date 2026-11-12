"""Run contracts and stable artifact schemas."""
from __future__ import annotations
from shared.artifacts import RAW_CSV, SUMMARY_CSV, STATISTICS_CSV, VALIDATION_CSV, CONVERGENCE_CSV, COST_CSV


RAW_FIELDNAMES = [
    "problem", "n_var", "n_obj", "run_idx", "seed", "algorithm", "runner",
    "evaluation_budget", "n_eval", "budget_utilization", "runtime_seconds",
    "front_size", "duplicate_fraction", "valid", "validation_status", "IGD", "HV",
]
SUMMARY_FIELDNAMES = [
    "problem", "n_var", "n_obj", "algorithm", "runner", "runs_total", "runs_valid",
    "IGD_mean", "IGD_std", "IGD_median", "IGD_best", "HV_mean", "HV_std",
    "HV_median", "HV_best", "runtime_mean", "n_eval_mean", "budget_utilization_mean",
]
VALIDATION_FIELDNAMES = [
    "problem", "run_idx", "seed", "algorithm", "valid", "validation_status",
    "validation_message", "front_size", "duplicate_fraction", "n_eval", "evaluation_budget",
]
CONVERGENCE_FIELDNAMES = [
    "problem", "n_obj", "run_idx", "seed", "algorithm", "checkpoint_fraction",
    "target_evaluations", "n_eval", "IGD", "HV",
]
COST_FIELDNAMES = [
    "problem", "algorithm", "runs_valid", "runtime_mean", "runtime_std",
    "runtime_median", "n_eval_mean", "budget_utilization_mean", "front_size_mean",
]


from shared.contracts import AlgorithmSpec, RunOutcome

__all__ = [name for name in globals() if name.isupper()] + ["AlgorithmSpec", "RunOutcome"]
