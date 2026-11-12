from __future__ import annotations

import unittest
import numpy as np

from oade_nsga2.algorithm import OADE_NSGAII, _make_evaluated_individual
from oade_nsga2.core import ProblemWrapper


class DummyProblem:
    n_var = 5
    n_obj = 2
    xl = np.zeros(5)
    xu = np.ones(5)

    def evaluate(self, x):
        x = np.atleast_2d(np.asarray(x, dtype=float))
        f1 = np.sum(x, axis=1)
        f2 = np.sum((1.0 - x) ** 2, axis=1)
        return np.column_stack([f1, f2])


class RestartMechanismTests(unittest.TestCase):
    def setUp(self):
        self.problem = ProblemWrapper(DummyProblem())

    def test_default_is_adaptive_mode(self):
        solver = OADE_NSGAII(self.problem, pop_size=20, n_gen=40)
        self.assertEqual(solver.restart_mode, "adaptive")
        self.assertTrue(solver.enable_restart)

    def test_classic_restart_triggers_on_stagnation_alone(self):
        solver = OADE_NSGAII(self.problem, pop_size=20, n_gen=40)
        solver.restart_mode = "classic"
        solver.stagnation_patience = 5
        # Build population
        solver.population = [
            _make_evaluated_individual(np.full(5, float(i) / 20.0), np.array([float(i) / 20.0, 1.0 - float(i) / 20.0]))
            for i in range(20)
        ]
        last_ideal = np.array([0.0, 0.0])
        counter = 4
        # At counter = 5, classic should trigger partial restart and reset counter to 0
        new_counter, new_ideal = solver._check_and_handle_stagnation(counter, last_ideal)
        self.assertEqual(new_counter, 0)

    def test_adaptive_restart_does_not_trigger_when_diversity_is_healthy(self):
        solver = OADE_NSGAII(self.problem, pop_size=20, n_gen=40)
        solver.restart_mode = "adaptive"
        solver.stagnation_patience = 5
        solver.diversity_threshold = 0.02
        # Population is diverse across [0, 1]
        solver.population = [
            _make_evaluated_individual(np.full(5, float(i) / 20.0), np.array([float(i) / 20.0, 1.0 - float(i) / 20.0]))
            for i in range(20)
        ]
        self.assertFalse(solver._is_diversity_collapsed())
        last_ideal = np.array([0.0, 0.05])
        counter = 4
        # Even though stagnation patience is reached, diversity is healthy -> should NOT trigger full restart
        new_counter, _ = solver._check_and_handle_stagnation(counter, last_ideal)
        self.assertEqual(new_counter, solver.stagnation_patience // 2)

    def test_adaptive_restart_triggers_when_diversity_collapses(self):
        solver = OADE_NSGAII(self.problem, pop_size=20, n_gen=40)
        solver.restart_mode = "adaptive"
        solver.stagnation_patience = 5
        solver.diversity_threshold = 0.02
        # Collapsed population: all individuals virtually identical
        solver.population = [
            _make_evaluated_individual(np.full(5, 0.5) + np.random.normal(0, 1e-4, 5), np.array([0.5, 0.5]))
            for _ in range(20)
        ]
        self.assertTrue(solver._is_diversity_collapsed())
        last_ideal = np.array([0.5, 0.5])
        counter = 4
        # When diversity collapsed AND stagnation reached -> triggers adaptive restart
        new_counter, _ = solver._check_and_handle_stagnation(counter, last_ideal)
        self.assertEqual(new_counter, 0)
        self.assertEqual(len(solver.population), 20)


if __name__ == "__main__":
    unittest.main()
