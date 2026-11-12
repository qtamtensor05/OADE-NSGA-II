"""Own the NSGA2 library invocation and algorithm-specific setup."""
from pymoo.algorithms.moo.nsga2 import NSGA2
from shared.pymoo_execution import run_pymoo

def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    return run_pymoo(NSGA2, spec, problem, pop_size, budget, initial_x, seed, recorder)
