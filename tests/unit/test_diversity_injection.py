import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from pymoo.problems import get_problem
from research.oade_nsga2.telemetry import InstrumentedOADE
from research.oade_nsga2.core import ProblemWrapper
from shared.evaluation import BudgetedProblem,EvaluationBudgetExceeded
from shared.population import make_initial_population
from shared.io.config import load_yaml_config
from research.studies.diversity_injection import design,run_task
from research.studies.uniform_measurements import run_task as baseline_task


class DiversityTests(unittest.TestCase):
    def config(self):
        cfg=load_yaml_config(Path('config/smoke/smoke_diversity_injection.yaml'))
        cfg['reference_fronts']={'zdt1':get_problem('zdt1',n_var=10).pareto_front().tolist()}
        return cfg

    def test_same_initial_population_and_only_injection_differs(self):
        cfg,candidates=design(self.config())
        rows=[run_task(cfg,c,cfg['problems'][0],42) for c in candidates]
        self.assertEqual(rows[0]['initialization_evidence'],rows[1]['initialization_evidence'])
        self.assertEqual(rows[0]['initial_x_sha256'],rows[1]['initial_x_sha256'])
        a,b=[{k:v for k,v in c['settings'].items() if k!='enable_obl'} for c in candidates]
        self.assertEqual(a,b)
        for r in rows:
            self.assertLessEqual(r['n_eval'],520)
            self.assertEqual(r['initialization_evaluations'],20)
            self.assertEqual(r['settings']['restart_mode'],'adaptive')
            self.assertTrue(all(t['mode']=='success_rate' for t in r['probability_trace']))
        on,off=rows
        self.assertGreater(on['telemetry']['injection_candidates'],0)
        self.assertGreaterEqual(on['telemetry']['injection_attempts'],2)
        self.assertEqual(on['telemetry']['injection_evaluations'],sum(e['evaluations'] for e in on['diversity_events']))
        self.assertEqual(on['telemetry']['injection_evaluations'],on['telemetry']['injection_candidates'])
        self.assertTrue(all(e['generation_index']%10==0 for e in on['diversity_events']))
        self.assertEqual(off['diversity_events'],[])
        self.assertEqual(off['telemetry']['injection_evaluations'],0)
        for e in on['diversity_events']:
            if e['generation_completed']:
                self.assertLessEqual(e['retained'],e['candidates'])

    def test_enabled_arm_keeps_existing_search_results(self):
        cfg,candidates=design(self.config())
        actual=run_task(cfg,candidates[0],cfg['problems'][0],42)
        expected=baseline_task(cfg,candidates[0],cfg['problems'][0],42)
        self.assertEqual(actual['final_f'],expected['final_f'])
        self.assertEqual(actual['final_x'],expected['final_x'])
        self.assertEqual(actual['n_eval'],expected['n_eval'])

    def test_blocked_injection_is_counted_without_spending_budget(self):
        problem=get_problem('zdt1',n_var=10)
        counter=BudgetedProblem(problem,20)
        solver=InstrumentedOADE(ProblemWrapper(counter),pop_size=20,n_gen=20)
        solver.population=solver._build_initial_population(make_initial_population(problem,20,42))
        with patch('research.oade_nsga2.algorithm.generate_obl_offspring',side_effect=lambda *args:counter.evaluate(np.zeros((2,10)))):
            with self.assertRaises(EvaluationBudgetExceeded): solver._generate_periodic_obl(0)
        self.assertEqual(solver.telemetry['injection_budget_blocked'],1)
        self.assertEqual(solver.telemetry['injection_evaluations'],0)
        self.assertFalse(solver.diversity_events[0]['generation_completed'])
        self.assertIsNone(solver.diversity_events[0]['retained'])

    def test_disabled_and_unscheduled_injection_do_not_call_kernel(self):
        problem=get_problem('zdt1',n_var=10)
        solver=InstrumentedOADE(ProblemWrapper(BudgetedProblem(problem,100)),pop_size=20)
        with patch('research.oade_nsga2.algorithm.generate_obl_offspring') as kernel:
            self.assertEqual(solver._generate_periodic_obl(1),[])
            solver.enable_obl=False
            self.assertEqual(solver._generate_periodic_obl(0),[])
            kernel.assert_not_called()
        self.assertEqual(solver.diversity_events,[])


if __name__=='__main__': unittest.main()
