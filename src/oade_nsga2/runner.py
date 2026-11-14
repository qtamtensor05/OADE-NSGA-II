"""Run the fixed OADE policy under the common objective-budget contract."""
import time
import numpy as np
from shared.contracts import RunOutcome
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from shared.fronts import non_dominated_xy
from shared.population import make_initial_population
from . import OADE_NSGAII, ProblemWrapper


def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    if spec.params:
        raise ValueError("Fixed OADE accepts no parameter overrides; use local_oade_research for experiments")
    expected = make_initial_population(problem,pop_size,seed)
    if initial_x is not None and not np.array_equal(initial_x,expected):
        raise ValueError("Fixed OADE requires the seeded common uniform initial population")
    if pop_size < 6 or budget < pop_size:
        raise ValueError("Require population >=6 and enough budget for initialization")
    budgeted=BudgetedProblem(problem,budget)
    solver=OADE_NSGAII(ProblemWrapper(budgeted),pop_size=pop_size,n_gen=budget,seed=seed)
    def progress(_generation,_total):
        recorder.record(budgeted.n_eval,np.asarray([i.F for i in solver.population]))
    start=time.perf_counter()
    try:
        solver.run(progress_callback=progress)
    except EvaluationBudgetExceeded:
        pass
    runtime=time.perf_counter()-start
    x=np.asarray([i.X for i in solver.population],dtype=float)
    f=np.asarray([i.F for i in solver.population],dtype=float)
    x,f=non_dominated_xy(x,f)
    recorder.record(budgeted.n_eval,f)
    return RunOutcome(x,f,budgeted.n_eval,runtime,tuple(recorder.rows))
