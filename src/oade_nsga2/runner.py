"""Invoke this solver under the common execution contract."""
from __future__ import annotations
import random
import time
import numpy as np
from shared.contracts import RunOutcome
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from shared.fronts import non_dominated_xy
from . import OADE_NSGAII, ProblemWrapper

def run(spec, problem, pop_size, budget, initial_x, seed, recorder, *, solver_factory=OADE_NSGAII, observer=None) -> RunOutcome:
    np.random.seed(seed)
    random.seed(seed)
    budgeted = BudgetedProblem(problem, budget)
    solver = solver_factory(ProblemWrapper(budgeted), pop_size=pop_size, n_gen=budget)
    for key, value in spec.params.items():
        if hasattr(solver, key):
            setattr(solver, key, value)
    start = time.perf_counter()
    def progress(generation, _total):
        recorder.record(budgeted.n_eval, np.asarray([item.F for item in solver.population]))
        if observer is not None:
            observer(solver, generation, budgeted.n_eval)

    try:
        solver.run(
            initial_x=initial_x,
            progress_callback=progress,
        )
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x = np.asarray([item.X for item in solver.population], dtype=float)
    f = np.asarray([item.F for item in solver.population], dtype=float)
    x, f = non_dominated_xy(x, f)
    recorder.record(budgeted.n_eval, f)
    return RunOutcome(x, f, budgeted.n_eval, runtime, tuple(recorder.rows))


def run_instrumented(spec, problem, pop_size, budget, initial_x, seed, recorder):
    """Return normal outcome plus restart/adaptation observations for sensitivity."""
    from .telemetry import InstrumentedOADE
    holder, trace = [], []

    def factory(*args, **kwargs):
        solver = InstrumentedOADE(*args, **kwargs)
        holder.append(solver)
        return solver

    def observe(solver, generation, n_eval):
        if not trace or n_eval - trace[-1]["n_eval"] >= max(1, budget // 10):
            trace.append({"generation": generation, "n_eval": n_eval,
                          "mean_F": float(solver.mean_F), "mean_CR": float(solver.mean_CR),
                          "prob_de": float(solver.prob_de)})

    outcome = run(spec, problem, pop_size, budget, initial_x, seed, recorder,
                  solver_factory=factory, observer=observe)
    solver = holder[0]
    return outcome, {"telemetry": solver.telemetry, "adaptation_trace": trace,
                     "final_mean_F": float(solver.mean_F), "final_mean_CR": float(solver.mean_CR),
                     "final_prob_de": float(solver.prob_de)}
