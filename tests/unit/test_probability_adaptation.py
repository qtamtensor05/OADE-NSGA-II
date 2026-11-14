import unittest
import numpy as np
from pymoo.problems import get_problem
from research.oade_nsga2.algorithm import OADE_NSGAII, _make_evaluated_individual
from research.oade_nsga2.core import ProblemWrapper, CreationMode


class ProbabilityTests(unittest.TestCase):
    def solver(self,mode='success_rate'):
        s=OADE_NSGAII(ProblemWrapper(get_problem('zdt1',n_var=10)))
        s.probability_update_mode=mode
        s.enable_fcr_adaptation=False
        return s

    def trials(self,mode,n,successful):
        result=[]
        for i in range(n):
            ind=_make_evaluated_individual(np.zeros(10),np.array([0.,1.] if i<successful else [2.,2.]))
            ind.creation_mode=mode
            result.append(ind)
        return result

    def update(self,s,de=(8,4),sbx=(2,1)):
        trials=self.trials(CreationMode.DE,*de)+self.trials(CreationMode.SBX,*sbx)
        s._update_adaptive_parameters(trials,reference_population=trials)

    def test_normalizes_by_operator_usage(self):
        s=self.solver()
        self.update(s)
        self.assertEqual(s.last_probability_update['target'],.5)
        self.assertEqual(s.prob_de,.5)

    def test_rewards_better_success_rate_and_measures_without_fcr(self):
        s=self.solver()
        self.update(s,de=(8,8),sbx=(2,0))
        self.assertAlmostEqual(s.prob_de,.55)
        self.assertEqual(s.last_probability_update['success_de'],8)
        s=self.solver()
        self.update(s,de=(8,0),sbx=(2,2))
        self.assertAlmostEqual(s.prob_de,.45)

    def test_no_success_or_missing_operator_holds_probability(self):
        for de,sbx in [((8,0),(2,0)),((8,8),(0,0)),((0,0),(2,2))]:
            s=self.solver()
            trials=self.trials(CreationMode.DE,*de)+self.trials(CreationMode.SBX,*sbx)
            anchor=_make_evaluated_individual(np.zeros(10),np.array([0.,0.]))
            pool=trials+[anchor] if de[1]+sbx[1]==0 else trials
            s._update_adaptive_parameters(trials,reference_population=pool)
            self.assertEqual(s.prob_de,.5)
            self.assertIsNone(s.last_probability_update['target'])

    def test_fixed_disabled_and_bounds(self):
        s=self.solver('fixed'); self.update(s); self.assertEqual(s.prob_de,.5)
        s=self.solver(); s.enable_probability_adaptation=False
        self.update(s,de=(8,8),sbx=(2,0)); self.assertEqual(s.prob_de,.5)
        s=self.solver(); s.prob_de=.79
        self.update(s,de=(8,8),sbx=(2,0)); self.assertEqual(s.prob_de,.8)
        s=self.solver(); s.prob_de=.21
        self.update(s,de=(8,0),sbx=(2,2)); self.assertEqual(s.prob_de,.2)

    def test_default_is_success_rate(self):
        s=OADE_NSGAII(ProblemWrapper(get_problem('zdt1',n_var=10)))
        self.assertEqual(s.probability_update_mode,'success_rate')

    def test_unknown_mode_rejected_even_when_adaptation_disabled(self):
        for enabled in (True,False):
            s=self.solver('invalid_mode')
            s.enable_probability_adaptation=enabled
            with self.assertRaisesRegex(ValueError,'success_rate or fixed'):
                self.update(s)
            from unittest.mock import patch
            with patch.object(s,'_build_initial_population') as initialize:
                with self.assertRaisesRegex(ValueError,'success_rate or fixed'):
                    s.run()
                initialize.assert_not_called()


if __name__=='__main__': unittest.main()
