"""DE success must not depend on duplicate filtering or stale selection ranks."""
import unittest
from unittest.mock import patch

import numpy as np
from pymoo.problems import get_problem
from research.oade_nsga2.algorithm import OADE_NSGAII, _make_evaluated_individual
from research.oade_nsga2.core import CreationMode, ProblemWrapper
from research.oade_nsga2.selection import environmental_selection, remove_duplicates


def individual(f, *, mode=CreationMode.INIT, scale=.5, cr=.5):
    ind = _make_evaluated_individual(np.full(10,.5), np.asarray(f,dtype=float))
    ind.creation_mode, ind.used_F, ind.used_CR = mode, scale, cr
    return ind


class AdaptationDuplicateTests(unittest.TestCase):
    def solver(self):
        return OADE_NSGAII(ProblemWrapper(get_problem('zdt1', n_var=10)),pop_size=2,n_gen=1)

    def test_full_generation_includes_unranked_duplicate_de_trials(self):
        solver = self.solver()
        solver.enable_restart = False
        parents = [individual([0,1]),individual([1,0])]
        offspring = [individual([0,1],mode=CreationMode.DE,scale=.2,cr=.1),
                     individual([1,0],mode=CreationMode.DE,scale=.8,cr=.9)]
        # Both trials are removed, leaving rank=None. Old implementation skips
        # both and leaves mean_F=0.5 instead of applying Lehmer mean 0.68.
        with patch.object(solver,'_build_initial_population',return_value=parents), \
             patch.object(solver,'_generate_offspring',return_value=offspring):
            solver.run()
        self.assertTrue(all(i.rank is None for i in offspring))
        self.assertAlmostEqual(solver.mean_F,.9*.5+.1*.68)
        self.assertAlmostEqual(solver.mean_CR,.5)

    def test_dominated_duplicate_and_stale_rank_do_not_contribute(self):
        solver = self.solver()
        best = individual([0,0])
        child = individual([1,1],mode=CreationMode.DE,scale=.9,cr=.9)
        child.rank = 1  # stale metadata must not make a dominated trial successful
        solver.population = [best]
        solver._update_adaptive_parameters([child],reference_population=[best,child])
        self.assertEqual(solver.mean_F,.5)
        self.assertEqual(solver.mean_CR,.5)

    def test_near_duplicate_uses_own_objectives_not_representative_rank(self):
        solver = self.solver()
        parent = individual([0,0])
        child = individual([1e-6,1e-6],mode=CreationMode.DE,scale=.9,cr=.9)
        pool = [parent,child]
        self.assertEqual(len(remove_duplicates(pool)),1)
        solver._update_adaptive_parameters([child],reference_population=pool)
        self.assertEqual(solver.mean_F,.5)

    def test_nondominated_child_truncated_by_crowding_still_contributes(self):
        solver = self.solver()
        child = individual([.5,.5],mode=CreationMode.DE,scale=.8,cr=.2)
        pool = [individual([0,1]),individual([1,0]),child]
        solver.population = environmental_selection(pool,2,2)
        self.assertFalse(any(i is child for i in solver.population))
        solver._update_adaptive_parameters([child],reference_population=pool)
        self.assertAlmostEqual(solver.mean_F,.53)
        self.assertAlmostEqual(solver.mean_CR,.47)

    def test_disabled_fcr_and_single_operator_leave_parameters_unchanged(self):
        solver = self.solver()
        solver.enable_fcr_adaptation = False
        child = individual([0,0],mode=CreationMode.DE,scale=.9,cr=.9)
        solver._update_adaptive_parameters([child],reference_population=[child])
        self.assertEqual(solver.mean_F,.5)
        self.assertEqual(solver.mean_CR,.5)
        self.assertAlmostEqual(solver.prob_de,.5)


if __name__ == '__main__':
    unittest.main()
