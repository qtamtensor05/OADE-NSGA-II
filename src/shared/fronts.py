"""Shared Pareto-front extraction."""
import numpy as np
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

def non_dominated_xy(x: np.ndarray, f: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)
    indices = NonDominatedSorting().do(f, only_non_dominated_front=True)
    return x[indices], f[indices]

def non_dominated(F: np.ndarray) -> np.ndarray:
    nds = NonDominatedSorting()
    front = nds.do(F, only_non_dominated_front=True)
    return F[front]
