"""Own the DNSGA2 library invocation and algorithm-specific setup."""
from pymoo.algorithms.moo.dnsga2 import DNSGA2
from shared.pymoo_execution import run_pymoo

def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    return run_pymoo(DNSGA2, spec, problem, pop_size, budget, initial_x, seed, recorder)
