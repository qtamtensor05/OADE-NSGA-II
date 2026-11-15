"""Numerical checks against primary-source formulas, not benchmark outcomes."""
import unittest
from unittest.mock import patch
import numpy as np
from pymoo.problems import get_problem
from cgde_nsga2 import CGDE_NSGAII, ProblemAdapter as CGAdapter
from cgde_nsga2.operators import cgde_offspring, neighborhood_pools, subranks
from ce_moea.operators import polynomial_mutation, differential_evolution_operator
from ce_moea import AttributedNetwork, AttributedNetworkProblem
from nsga2_sdr_ols import NSGAIISDROLS, ProblemAdapter as SDRAdapter
from nsga2_sdr_ols.core import make_individual
from nsga2_sdr_ols.operators import local_search, sbx_crossover
from shared.evaluation import BudgetedProblem


class Draws:
    def __init__(self, *values):
        self.values = iter(values)

    def random(self, size=None):
        value = next(self.values)
        return value if size is None else np.full(size, value)

    def choice(self, values):
        return values[0]

    def integers(self, high):
        return 0


class PaperOperatorTests(unittest.TestCase):
    def test_cgde_equations_7_and_8_and_no_extra_mutation(self):
        current = np.array([[.2, .3], [.6, .7]])
        previous = np.array([[.1, .2], [.3, .4]])
        neighbors = np.array([[1], [0]])
        old_neighbors = np.array([[0], [1]])
        args = (0, current, previous, neighbors, old_neighbors, .5, 1., np.zeros(2), np.ones(2))
        np.testing.assert_allclose(cgde_offspring(*args, Draws(.1, .1)), [.85, .95])
        np.testing.assert_allclose(cgde_offspring(*args, Draws(.9, .1)), [.25, .35])

    def test_subranks_invariant_to_objective_scale_and_neighborhood_excludes_target(self):
        f = np.array([[1., 3.], [1., 2.], [3., 1.]])
        np.testing.assert_array_equal(subranks(f), [[1, 3], [1, 2], [3, 1]])
        pools = neighborhood_pools(f, f[::-1], 1)
        scaled = neighborhood_pools(f * [1000, .01], f[::-1] * [1000, .01], 1)
        for a, b in zip(pools, scaled):
            np.testing.assert_array_equal(a, b)
        self.assertTrue(all(i not in pool for i, pool in enumerate(pools[0])))

    def test_cgde_inherits_selected_parent_scaling_and_retains_exact_previous_generation(self):
        p = np.array([[.1, .9], [.3, .6], [.6, .3], [.9, .1]])
        solver = CGDE_NSGAII(CGAdapter(get_problem('zdt1', n_var=2)),
                            pop_size=4, n_gen=2, seed=4, f_perturbation=0)
        initial_scaling = np.random.default_rng(4).uniform(.2, .9, 4)
        def select(x, f, n, **kwargs):
            indices = np.array([5, 0, 7, 2])
            return x[indices], f[indices], np.zeros(n), np.zeros(n), indices
        with patch('cgde_nsga2.algorithm.environmental_selection', side_effect=select):
            solver.run(p)
        np.testing.assert_array_equal(solver.previous_population, p)
        np.testing.assert_allclose(solver.scaling_factors, initial_scaling[[1, 0, 3, 2]])

    def test_ce_mutation_both_literal_paper_branches_on_asymmetric_bounds(self):
        for r in (.25, .75):
            ratio = .7 if r < .5 else .3
            delta = ((2*r + (1-2*r)*ratio**20)**(1/20)-1 if r < .5
                     else 1-(2-2*r+(2*r-1)*ratio**20)**(1/20))
            actual = polynomial_mutation(np.array([5.]), np.array([2.]),
                                         np.array([12.]), 1., 20., Draws(0., r))
            np.testing.assert_allclose(actual, [5.+10*delta], atol=1e-14)

    def test_ce_does_not_force_a_crossover_coordinate(self):
        x = np.array([.2, .4])
        actual = differential_evolution_operator(x, np.ones(2), np.zeros(2),
                                                 .7, 0., 0., 20., np.zeros(2),
                                                 np.ones(2), Draws(.5, .5, .5))
        np.testing.assert_array_equal(actual, x)

    def test_ce_network_default_uses_printed_cosine_objective(self):
        graph = AttributedNetwork.from_edges(2, [(0, 1)], np.ones((2, 2)))
        problem = AttributedNetworkProblem(graph)
        np.testing.assert_allclose(problem.evaluate(np.zeros((1, graph.n_var))), [[0., .5]])

    def test_sdr_visits_every_parent_and_coordinate_and_ga_sees_merged_pool(self):
        problem = SDRAdapter(get_problem('zdt1', n_var=3))
        solver = NSGAIISDROLS(problem, pop_size=4, n_gen=1, seed=3)
        from nsga2_sdr_ols.operators import make_ga_offspring
        with patch('nsga2_sdr_ols.algorithm.make_ga_offspring', wraps=make_ga_offspring) as ga:
            solver.run()
        self.assertEqual(len(ga.call_args.args[1]), 4 + 2*4*3)
        neighbors = local_search(problem, solver.population, 0., .1, np.random.default_rng(3))
        self.assertEqual(len(neighbors), 24)
        self.assertEqual({(n.metadata['parent'], n.metadata['variable']) for n in neighbors},
                         {(i, j) for i in range(4) for j in range(3)})

    def test_sdr_final_partial_neighborhood_uses_all_remaining_fe(self):
        budgeted = BudgetedProblem(get_problem('zdt1', n_var=3), 37)
        solver = NSGAIISDROLS(SDRAdapter(budgeted), pop_size=4, n_gen=100, seed=3)
        solver.run()
        self.assertEqual(budgeted.n_eval, 37)
        self.assertEqual(solver.result_X().shape, (4, 3))
        self.assertTrue(np.isfinite(solver.result_F()).all())

    def test_sbx_can_return_both_symmetric_children(self):
        args = (np.array([.2]), np.array([.8]), np.zeros(1), np.ones(1), 20.)
        lower = sbx_crossover(*args, Draws(0., .25, .1))
        upper = sbx_crossover(*args, Draws(0., .25, .9))
        self.assertLess(lower[0], .5)
        self.assertGreater(upper[0], .5)
        np.testing.assert_allclose(lower + upper, [1.])


if __name__ == '__main__':
    unittest.main()
