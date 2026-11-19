"""Deb et al. (2002) metrics in raw objective coordinates (minimization)."""
import numpy as np
from scipy.spatial import cKDTree
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting


def nondominated(values):
    f = np.asarray(values, dtype=float)
    if f.size == 0:
        return np.empty((0, 2))
    if f.ndim != 2 or not np.isfinite(f).all():
        raise ValueError('Expected a finite objective matrix')
    return f[NonDominatedSorting().do(f, only_non_dominated_front=True)]


def convergence_metric(front, reference):
    """Mean nearest-reference distance; reference must contain exactly 500 points."""
    ref = np.asarray(reference, dtype=float)
    if ref.ndim != 2 or len(ref) != 500 or not np.isfinite(ref).all():
        raise ValueError('Require 500 finite true-front reference points')
    f = nondominated(front)
    if not len(f):
        return None
    if f.shape[1] != ref.shape[1]:
        raise ValueError('Objective dimensions differ')
    return float(cKDTree(ref).query(f)[0].mean())


def diversity_metric(front, extremes):
    """Original two-objective Delta; undefined for fewer than two distinct points."""
    f = nondominated(front)
    e = np.asarray(extremes, dtype=float)
    if e.shape != (2, 2) or not np.isfinite(e).all():
        raise ValueError('Require two known true-front extremes')
    if len(f) and f.shape[1] != 2:
        raise ValueError('Original Delta requires two objectives')
    if len(f) < 2:
        return None
    f = f[np.lexsort((f[:, 1], f[:, 0]))]
    e = e[np.argsort(e[:, 0])]
    gaps = np.linalg.norm(np.diff(f, axis=0), axis=1)
    if not gaps.sum():
        return None
    boundary = np.linalg.norm(f[0]-e[0]) + np.linalg.norm(f[-1]-e[-1])
    return float((boundary + np.abs(gaps-gaps.mean()).sum()) / (boundary+gaps.sum()))


def zdt_reference(name):
    """500 equal arc-length samples, never interpolating across ZDT3 gaps.

    Dense analytical curves approximate arc length; endpoints are retained.
    """
    bounds = [(0., 1.)]
    if name == 'zdt3':
        bounds = [(0., .0830015349), (.1822287280, .2577623634),
                  (.4093136748, .4538821041), (.6183967944, .6525117038),
                  (.8233317983, .8518328654)]
    elif name == 'zdt6':
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(lambda x: 1-np.exp(-4*x)*np.sin(6*np.pi*x)**6,
                                 bounds=(0., 1/6), method='bounded', options={'xatol': 1e-15})
        bounds = [(float(result.fun), 1.)]
    elif name not in {'zdt1', 'zdt2', 'zdt4'}:
        raise ValueError('No audited true-front provider for '+name)
    curves = []
    for lo, hi in bounds:
        x = np.linspace(lo, hi, 100001)
        y = 1-x*x if name in {'zdt2', 'zdt6'} else 1-np.sqrt(x)
        if name == 'zdt3':
            y -= x*np.sin(10*np.pi*x)
        f = np.column_stack((x, y))
        s = np.r_[0., np.cumsum(np.linalg.norm(np.diff(f, axis=0), axis=1))]
        curves.append((f, s))
    lengths = np.array([s[-1] for _, s in curves])
    allocation = np.full(len(curves), 2) + np.floor((500-2*len(curves))*lengths/lengths.sum()).astype(int)
    for i in range(500-int(allocation.sum())):
        allocation[i % len(curves)] += 1
    ref = np.concatenate([np.column_stack([np.interp(np.linspace(0, s[-1], n), s, f[:, j])
                                          for j in range(2)]) for (f, s), n in zip(curves, allocation)])
    return ref, ref[[0, -1]]
