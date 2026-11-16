import unittest
import numpy as np
from pymoo.problems import get_problem
from oade_nsga2 import OADE_NSGAII, ProblemWrapper
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from research.studies.mechanism_impact import ObservedOADE, run_one, VARIANTS


class MechanismImpactTests(unittest.TestCase):
    def test_observation_preserves_fixed_solver(self):
        for name in ('zdt4', 'zdt6'):
            results = []
            for cls in (OADE_NSGAII, ObservedOADE):
                counter = BudgetedProblem(get_problem(name, n_var=10), 500)
                solver = cls(ProblemWrapper(counter), pop_size=10, n_gen=500, seed=42)
                try:
                    solver.run()
                except EvaluationBudgetExceeded:
                    pass
                results.append((counter.n_eval, np.array([i.F for i in solver.population])))
            self.assertEqual(results[0][0], results[1][0])
            np.testing.assert_array_equal(results[0][1], results[1][1])

    def test_interventions_and_budget(self):
        for variant in VARIANTS:
            r = run_one('zdt6', 42, variant, 10, 300)
            self.assertLessEqual(r['n_eval'], 300)
            if variant == 'no_obl':
                self.assertFalse(any(e['mechanism']=='obl' for e in r['events']))
            if variant == 'fixed_f_cr':
                self.assertTrue(all(t['mean_F']==.65 and t['mean_CR']==.5 for t in r['trace']))
            if variant == 'fixed_pde':
                self.assertTrue(all(t['pde']==.5 for t in r['trace']))
            if variant in ('de_only', 'sbx_only'):
                absent = 'sbx' if variant == 'de_only' else 'de'
                self.assertTrue(all(t[absent+'_trials']==0 for t in r['trace']))
