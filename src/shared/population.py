"""Common seeded initialization."""
import numpy as np

def make_initial_population(problem, pop_size: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    xl = np.asarray(problem.xl)
    xu = np.asarray(problem.xu)
    return rng.uniform(xl, xu, size=(pop_size, problem.n_var))
