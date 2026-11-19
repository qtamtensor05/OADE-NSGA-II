"""Use pymoo's GDE3 implementation without rebuilding its search operators."""
from pymoo.algorithms.moo.gde3 import GDE3
from shared.pymoo_execution import run_pymoo


def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    return run_pymoo(GDE3, spec, problem, pop_size, budget, initial_x, seed, recorder)
