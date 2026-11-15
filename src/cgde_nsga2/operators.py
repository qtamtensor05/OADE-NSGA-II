"""Qiu, Xu and Tan (CEC 2014), equations (5), (7), (8)."""
from __future__ import annotations
import numpy as np


def subranks(objectives):
    """One-based per-objective ranks; equal values share a rank."""
    values = np.asarray(objectives, dtype=float)
    return 1 + (values[:, None, :] > values[None, :, :]).sum(axis=1)


def neighborhood_pools(current_f, previous_f, size):
    """Use joint subranks, stable distance ties, and exclude current target.

    Joint versus separate ranks and ties are unspecified in the paper.
    """
    n = len(current_f)
    ranks = subranks(np.vstack([current_f, previous_f]))
    distances = ((ranks[:n, None, :] - ranks[None, :, :]) ** 2).sum(axis=2).astype(float)
    distances[np.arange(n), np.arange(n)] = np.inf
    current = np.argsort(distances[:, :n], axis=1, kind="stable")[:, :min(size, n - 1)]
    previous = np.argsort(distances[:, n:], axis=1, kind="stable")[:, :min(size, len(previous_f))]
    return current, previous


def cgde_offspring(target_idx, population, previous, current_neighbors,
                   previous_neighbors, F, CR, xl, xu, rng):
    """Neighborhood/population mutation with equal probability, then Eq. (5)."""
    target = population[target_idx]
    if rng.random() < 0.5:
        first = population[int(rng.choice(current_neighbors[target_idx]))]
        second = previous[int(rng.choice(previous_neighbors[target_idx]))]
        mutant = first + F * (first - second)
    else:
        first = population[int(rng.integers(len(population)))]
        second = previous[int(rng.integers(len(previous)))]
        mutant = target + F * (first - second)
    return np.clip(binomial_crossover(target, mutant, CR, rng), xl, xu)


def binomial_crossover(target, mutant, CR, rng):
    mask = rng.random(target.size) <= CR
    mask[int(rng.integers(target.size))] = True
    return np.where(mask, mutant, target)
