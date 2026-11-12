"""Historical generation-based invocation; distinct from the fixed-budget protocol."""
import random
import numpy as np
from shared.fronts import non_dominated
from pymoo.algorithms.moo.dnsga2 import DNSGA2
from pymoo.optimize import minimize

def run_dnsga2(problem, pop_size: int, n_gen: int, initial_x: np.ndarray, seed: int) -> np.ndarray:
    algorithm = DNSGA2(pop_size=pop_size, sampling=initial_x)
    res = minimize(problem, algorithm, termination=("n_gen", n_gen), seed=seed, verbose=False)
    return non_dominated(res.F)
