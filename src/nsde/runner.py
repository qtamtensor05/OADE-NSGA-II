"""Use pymoo's NSDE implementation, with the common benchmark initialization."""
from pymoo.algorithms.moo.nsde import NSDE
from shared.pymoo_execution import run_pymoo


def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    return run_pymoo(NSDE, spec, problem, pop_size, budget, initial_x, seed, recorder)
