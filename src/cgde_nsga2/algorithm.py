"""CGDE-NSGA-II reconstructed from Qiu, Xu and Tan, CEC 2014."""
from __future__ import annotations
import numpy as np
from .core import ProblemAdapter, resize_initial_population
from .nsga2 import environmental_selection
from .operators import cgde_offspring, neighborhood_pools


class CGDE_NSGAII:
    """Local reconstruction; see algorithm protocol for unresolved paper details."""

    def __init__(self, problem: ProblemAdapter, pop_size=100, n_gen=200,
                 n_neighbors=5, f_bounds=(0.2, 0.9), f_perturbation=0.2,
                 cr_bounds=(0.0, 1.0), seed=None):
        self.problem = problem
        self.pop_size = int(pop_size)
        self.n_gen = int(n_gen)
        self.n_neighbors = int(n_neighbors)
        self.f_bounds = tuple(map(float, f_bounds))
        self.f_perturbation = float(f_perturbation)
        self.cr_bounds = tuple(map(float, cr_bounds))
        if self.pop_size < 2 or self.n_neighbors < 1:
            raise ValueError("CGDE requires population >= 2 and neighbors >= 1")
        if not (0 <= self.f_bounds[0] < self.f_bounds[1] <= 1):
            raise ValueError("Require 0 <= F lower < upper <= 1")
        if not (0 <= self.cr_bounds[0] < self.cr_bounds[1] <= 1) or self.f_perturbation < 0:
            raise ValueError("Invalid crossover range or F perturbation")
        self.rng = np.random.default_rng(seed)
        self.population = self.objectives = None
        self.previous_population = self.previous_objectives = None
        self.scaling_factors = None
        self.history = []

    def run(self, initial_x=None, progress_callback=None):
        p = (self.rng.uniform(self.problem.xl, self.problem.xu,
                              size=(self.pop_size, self.problem.n_var))
             if initial_x is None else resize_initial_population(
                 initial_x, self.pop_size, self.problem.xl, self.problem.xu, self.rng))
        objectives = self.problem.evaluate(p)
        scaling = self.rng.uniform(*self.f_bounds, size=self.pop_size)
        # Bootstrap: no previous generation exists at initialization.
        previous, previous_f = p.copy(), objectives.copy()
        self.history.clear()
        self._save(p, objectives, previous, previous_f, scaling)
        for generation in range(1, self.n_gen):
            current_neighbors, previous_neighbors = neighborhood_pools(
                objectives, previous_f, self.n_neighbors)
            crossover = self.rng.uniform(*self.cr_bounds, size=self.pop_size)
            offspring = np.asarray([
                cgde_offspring(i, p, previous, current_neighbors, previous_neighbors,
                               scaling[i], crossover[i], self.problem.xl,
                               self.problem.xu, self.rng)
                for i in range(self.pop_size)])
            offspring_f = self.problem.evaluate(offspring)
            merged_scaling = np.concatenate([scaling, scaling])
            selected_p, selected_f, _, _, indices = environmental_selection(
                np.vstack([p, offspring]), np.vstack([objectives, offspring_f]),
                self.pop_size, return_indices=True)
            scaling = np.clip(merged_scaling[indices] + self.rng.uniform(
                -self.f_perturbation, self.f_perturbation, self.pop_size), *self.f_bounds)
            previous, previous_f = p.copy(), objectives.copy()
            p, objectives = selected_p, selected_f
            self.history.append(objectives.copy())
            self._save(p, objectives, previous, previous_f, scaling)
            if progress_callback is not None:
                progress_callback(generation + 1, self.n_gen)
        return self.result_X(), self.result_F()

    def _save(self, p, f, previous, previous_f, scaling):
        self.population, self.objectives = p.copy(), f.copy()
        self.previous_population = previous.copy()
        self.previous_objectives = previous_f.copy()
        self.scaling_factors = scaling.copy()

    def result_X(self):
        if self.population is None:
            raise RuntimeError("run() must be called first")
        return self.population.copy()

    def result_F(self):
        if self.objectives is None:
            raise RuntimeError("run() must be called first")
        return self.objectives.copy()
