"""Invoke this solver under the common execution contract."""
from __future__ import annotations
import random
import time
import numpy as np
from shared.contracts import RunOutcome
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from shared.fronts import non_dominated_xy
from . import NSGAIISDROLS, ProblemAdapter as SDROLSProblemAdapter

def run(spec, problem, pop_size, budget, initial_x, seed, recorder) -> RunOutcome:
    budgeted = BudgetedProblem(problem, budget)
    params = dict(spec.params)
    factor = params.pop("local_search_max_neighbors_factor", None)
    max_neighbors = None if factor is None else int(factor) * pop_size
    solver = NSGAIISDROLS(
        SDROLSProblemAdapter(budgeted), pop_size=pop_size, n_gen=budget, seed=seed,
        local_search_max_neighbors=max_neighbors, **params,
    )
    start = time.perf_counter()
    try:
        solver.run(
            initial_x=initial_x,
            progress_callback=lambda _generation, _total: recorder.record(
                budgeted.n_eval, solver.result_F()
            ),
        )
    except EvaluationBudgetExceeded:
        pass
    runtime = time.perf_counter() - start
    x, f = non_dominated_xy(solver.result_X(), solver.result_F())
    recorder.record(budgeted.n_eval, f)
    return RunOutcome(x, f, budgeted.n_eval, runtime, tuple(recorder.rows))
