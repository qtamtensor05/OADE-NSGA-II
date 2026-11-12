"""Reusable budget, sampling and checkpoint plumbing for pymoo adapters."""
from __future__ import annotations
import time
import warnings
import numpy as np
from pymoo.core.callback import Callback
from pymoo.core.sampling import Sampling
from pymoo.optimize import minimize
from shared.contracts import RunOutcome
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from shared.fronts import non_dominated_xy

class PymooConvergenceCallback(Callback):
    def __init__(self, budgeted: BudgetedProblem, recorder) -> None:
        super().__init__()
        self.budgeted = budgeted
        self.recorder = recorder

    def notify(self, algorithm) -> None:
        if algorithm.pop is not None:
            self.recorder.record(self.budgeted.n_eval, algorithm.pop.get("F"))

class FixedInitialSampling(Sampling):
    """Return the common initial population once and remain callable thereafter."""

    def __init__(self, initial_x: np.ndarray, seed: int) -> None:
        super().__init__()
        self.initial_x = np.asarray(initial_x, dtype=float).copy()
        self.rng = np.random.default_rng(seed + 900_000)
        self.used_initial = False

    def _do(self, problem, n_samples, **kwargs):
        if not self.used_initial and n_samples == len(self.initial_x):
            self.used_initial = True
            return self.initial_x.copy()
        return self.rng.uniform(problem.xl, problem.xu, size=(n_samples, problem.n_var))

def run_pymoo(algorithm_factory, spec, problem, pop_size, budget, initial_x, seed, recorder, *, configure=None, warning_module=None) -> RunOutcome:
    budgeted = BudgetedProblem(problem, budget)
    params = dict(spec.params)
    params.setdefault("pop_size", pop_size)
    if spec.sampling == "initial_population":
        params.setdefault("sampling", FixedInitialSampling(initial_x, seed))
    start = time.perf_counter()
    if configure is not None:
        configure(budgeted, params, initial_x)
    algorithm = algorithm_factory(**params)
    result = None
    try:
        with warnings.catch_warnings():
            if warning_module:
                warnings.filterwarnings("ignore", category=RuntimeWarning, module=warning_module)
            result = minimize(
                budgeted,
                algorithm,
                termination=("n_eval", budget),
                seed=seed,
                verbose=False,
                copy_algorithm=False,
                callback=PymooConvergenceCallback(budgeted, recorder),
            )
    except EvaluationBudgetExceeded:
        # Some pymoo algorithms perform extra internal evaluations (for
        # example DNSGA-II change detection). Preserve the last complete
        # population instead of allowing those evaluations to exceed the cap.
        pass
    runtime = time.perf_counter() - start
    if result is None or result.X is None or result.F is None:
        if algorithm.pop is None:
            raise RuntimeError(f"{spec.name} produced no checkpoint before budget exhaustion")
        x, f = algorithm.pop.get("X"), algorithm.pop.get("F")
    else:
        x, f = np.atleast_2d(result.X), np.atleast_2d(result.F)
    x, f = non_dominated_xy(x, f)
    recorder.record(budgeted.n_eval, f)
    return RunOutcome(x, f, budgeted.n_eval, runtime, tuple(recorder.rows))
