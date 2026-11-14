"""Historical generation-based invocation; distinct from the fixed-budget protocol."""
import random
import numpy as np
from shared.fronts import non_dominated
from . import OADE_NSGAII, ProblemWrapper

def run_oade(problem, pop_size: int, n_gen: int, initial_x: np.ndarray, seed: int, oade_cfg: dict) -> np.ndarray:
    np.random.seed(seed)
    random.seed(seed)
    solver = OADE_NSGAII(ProblemWrapper(problem), pop_size=pop_size, n_gen=n_gen)

    solver.stagnation_patience = int(oade_cfg["stagnation_patience"])
    solver.stagnation_tolerance = float(oade_cfg["stagnation_tolerance"])
    solver.restart_elite_ratio = float(oade_cfg["restart_elite_ratio"])
    solver.prob_de = float(oade_cfg["prob_de"])
    solver.n_neighbors = int(oade_cfg["n_neighbors"])
    solver.mean_F = float(oade_cfg["mean_F"])
    solver.mean_CR = float(oade_cfg["mean_CR"])

    F = solver.run(initial_x=initial_x)
    return non_dominated(F)
