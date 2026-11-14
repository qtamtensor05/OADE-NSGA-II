"""The fixed solver must match the corrected research policy, without switches."""
import unittest
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from oade_nsga2 import OADE_NSGAII, ProblemWrapper, FIXED_PARAMETERS, CreationMode
from oade_nsga2.algorithm import _make_evaluated_individual
from oade_nsga2.runner import run
from research.oade_nsga2.runner import run as research_run
from shared.contracts import AlgorithmSpec
from shared.population import make_initial_population
from research.benchmarking.convergence import ConvergenceRecorder


class FixedOADETests(unittest.TestCase):
    def test_fixed_solver_matches_corrected_research_policy(self):
        params={k:FIXED_PARAMETERS[k] for k in ('mean_F','mean_CR','prob_de','n_neighbors',
                'stagnation_patience','stagnation_tolerance','diversity_threshold','restart_elite_ratio')}
        params.update(restart_mode='adaptive',probability_update_mode='success_rate',enable_restart=True,
                      enable_obl=True,enable_fcr_adaptation=True,enable_probability_adaptation=True,enable_neighborhood=True)
        for name in ('zdt1','zdt4','zdt6'):
            for seed in (42,43):
                with self.subTest(problem=name,seed=seed):
                    problem=get_problem(name,n_var=10)
                    initial=make_initial_population(problem,20,seed)
                    def recorder():
                        front=problem.pareto_front()
                        return ConvergenceRecorder(520,IGD(front),HV(ref_point=np.max(front,axis=0)+.1))
                    fixed=run(AlgorithmSpec('OADE','local_oade',{}),problem,20,520,initial,seed,recorder())
                    experimental=research_run(AlgorithmSpec('OADE','local_oade_research',params),problem,20,520,initial,seed,recorder())
                    np.testing.assert_array_equal(fixed.x,experimental.x)
                    np.testing.assert_array_equal(fixed.f,experimental.f)
                    self.assertEqual(fixed.n_eval,experimental.n_eval)
                    self.assertEqual(fixed.convergence,experimental.convergence)

    def test_no_mechanism_switches_and_constant_configuration(self):
        s=OADE_NSGAII(ProblemWrapper(get_problem('zdt1',n_var=10)))
        for name in ('enable_restart','enable_obl','restart_mode','probability_update_mode','initialization_seed'):
            self.assertFalse(hasattr(s,name),name)
        with self.assertRaises(TypeError):FIXED_PARAMETERS['restart']='classic'
        self.assertEqual(s.n_neighbors,5)
        self.assertEqual(s.stagnation_patience,20)
        self.assertEqual(s.mean_F,.65)

    def test_overrides_or_nonuniform_input_are_rejected(self):
        problem=get_problem('zdt1',n_var=10)
        with self.assertRaisesRegex(ValueError,'no parameter overrides'):
            run(AlgorithmSpec('OADE','local_oade',{'enable_obl':False}),problem,20,100,None,42,None)
        with self.assertRaisesRegex(ValueError,'uniform'):
            run(AlgorithmSpec('OADE','local_oade',{}),problem,20,100,np.zeros((20,10)),42,None)

    def test_duplicate_and_stale_rank_bug_remains_fixed(self):
        s=OADE_NSGAII(ProblemWrapper(get_problem('zdt1',n_var=10)))
        parent=_make_evaluated_individual(np.zeros(10),np.array([0.,1.]))
        child=_make_evaluated_individual(np.zeros(10),np.array([0.,1.]))
        child.creation_mode=CreationMode.DE;child.used_F=.8;child.used_CR=.2
        self.assertIsNone(child.rank)
        s._update_adaptive_parameters([child],reference_population=[parent,child])
        self.assertAlmostEqual(s.mean_F,.9*.65+.1*.8)
        self.assertAlmostEqual(s.mean_CR,.9*.5+.1*.2)
        s.mean_F=.65;s.mean_CR=.5;child.F=np.array([1.,2.]);child.rank=1
        s._update_adaptive_parameters([child],reference_population=[parent,child])
        self.assertEqual(s.mean_F,.65)
        self.assertEqual(s.mean_CR,.5)

    def test_success_rate_uses_normalized_operator_success(self):
        s=OADE_NSGAII(ProblemWrapper(get_problem('zdt1',n_var=10)))
        offspring=[]
        for mode,n,success in [(CreationMode.DE,8,4),(CreationMode.SBX,2,1)]:
            for i in range(n):
                child=_make_evaluated_individual(np.zeros(10),np.array([0.,1.] if i<success else [2.,2.]))
                child.creation_mode=mode
                offspring.append(child)
        s._update_adaptive_parameters(offspring,reference_population=offspring)
        self.assertEqual(s.prob_de,.5)


if __name__=='__main__':unittest.main()
