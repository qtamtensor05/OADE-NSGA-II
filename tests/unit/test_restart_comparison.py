"""Mechanism/accounting tests; tiny forced triggers are not research evidence."""
import unittest
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from shared.contracts import AlgorithmSpec
from shared.population import make_initial_population
from oade_nsga2.runner import run, run_instrumented
from research.benchmarking.convergence import ConvergenceRecorder
from research.studies.restart_comparison import design, run_task, comparisons


class RestartComparisonTests(unittest.TestCase):
    def config(self):
        return {'global':{'pop_size':20,'evaluation_budget':240,'seeds':[42]},
                'problems':[{'name':'zdt1','n_var':10}],
                'common_settings':{'stagnation_patience':1,'stagnation_tolerance':1e6,
                                   'diversity_threshold':1e6}}

    def test_three_variants_account_for_both_restart_kernels(self):
        cfg, candidates = design(self.config())
        cfg['reference_fronts'] = {'zdt1': get_problem('zdt1',n_var=10).pareto_front().tolist()}
        rows = [run_task(cfg,c,cfg['problems'][0],42) for c in candidates]
        self.assertEqual(len({r['initial_x_sha256'] for r in rows}),1)
        for r in rows[:2]:
            t = r['telemetry']
            self.assertGreater(t['restart_completed'],0)
            self.assertEqual(t['restart_evaluations'],sum(e['evaluations'] for e in r['restart_events']))
            self.assertLessEqual(r['n_eval'],240)
            self.assertTrue(all('before' in e and 'after' in e for e in r['restart_events']))
        self.assertEqual(rows[2]['telemetry']['restart_attempts'],0)
        self.assertGreater(rows[2]['telemetry']['stagnation_eligible'],0)
        self.assertEqual(len(comparisons(cfg,candidates,rows)),6)

    def test_instrumentation_preserves_random_stream(self):
        problem = get_problem('zdt1',n_var=10)
        initial = make_initial_population(problem,20,42)
        for mode in ('classic','adaptive'):
            spec = AlgorithmSpec(mode,'local_oade',{'restart_mode':mode,'stagnation_patience':1,
                                  'stagnation_tolerance':1e6,'diversity_threshold':1e6})
            def recorder():
                return ConvergenceRecorder(240,IGD(problem.pareto_front()),HV(ref_point=np.array([2.,12.])))
            plain = run(spec,problem,20,240,initial,42,recorder())
            measured, _ = run_instrumented(spec,problem,20,240,initial,42,recorder())
            np.testing.assert_array_equal(plain.x, measured.x)
            np.testing.assert_array_equal(plain.f, measured.f)
            self.assertEqual(plain.n_eval,measured.n_eval)

    def test_zero_trigger_variants_remain_identical(self):
        cfg = self.config()
        cfg['common_settings']['stagnation_patience'] = 10000
        cfg,candidates = design(cfg)
        cfg['reference_fronts'] = {'zdt1':get_problem('zdt1',n_var=10).pareto_front().tolist()}
        rows = [run_task(cfg,c,cfg['problems'][0],42) for c in candidates]
        for row in rows:
            self.assertEqual(row['telemetry']['restart_attempts'],0)
            self.assertEqual(row['final_f'],rows[0]['final_f'])
        for comparison in comparisons(cfg,candidates,rows):
            self.assertEqual(comparison['p_holm'],1.)
            self.assertEqual(comparison['both_zero_restart_pairs'],1)

    def test_budget_blocked_restart_is_not_completed(self):
        from oade_nsga2.telemetry import InstrumentedOADE
        from oade_nsga2.core import ProblemWrapper
        from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
        problem = get_problem('zdt1',n_var=10)
        counter = BudgetedProblem(problem,21)
        solver = InstrumentedOADE(ProblemWrapper(counter),pop_size=20,n_gen=10)
        solver.population = solver._build_initial_population(make_initial_population(problem,20,42))
        solver.restart_mode = 'classic'
        solver.restart_elite_ratio = .3
        solver.stagnation_patience = 1
        ideal = np.min([i.F for i in solver.population],axis=0)
        with self.assertRaises(EvaluationBudgetExceeded):
            solver._check_and_handle_stagnation(0,ideal)
        self.assertEqual(solver.telemetry['restart_budget_blocked'],1)
        self.assertEqual(solver.telemetry['restart_completed'],0)
        self.assertEqual(solver.restart_events[0]['evaluations'],0)


if __name__ == '__main__':
    unittest.main()
