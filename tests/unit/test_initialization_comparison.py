import unittest
import numpy as np
from pymoo.problems import get_problem
from research.oade_nsga2.operators import initialize_obl
from research.oade_nsga2.core import ProblemWrapper
from shared.evaluation import BudgetedProblem
from shared.io.config import load_yaml_config
from pathlib import Path
from research.studies.initialization_comparison import design,run_task


class InitializationTests(unittest.TestCase):
    def config(self):
        cfg=load_yaml_config(Path('config/smoke/smoke_initialization_comparison.yaml'))
        cfg['reference_fronts']={'zdt1':get_problem('zdt1',n_var=10).pareto_front().tolist()}
        return cfg

    def test_seeded_sobol_obl_is_reproducible_and_isolates_rng(self):
        problem=get_problem('zdt1',n_var=10)
        outputs=[]
        for global_seed in (100,999):
            np.random.seed(global_seed)
            before=np.random.get_state()
            counter=BudgetedProblem(problem,100)
            pop=initialize_obl(ProblemWrapper(counter),20,seed=42)
            after=np.random.get_state()
            np.testing.assert_array_equal(before[1],after[1])
            self.assertEqual(before[2:],after[2:])
            self.assertEqual(counter.n_eval,40)
            self.assertEqual(len(pop),20)
            outputs.append(np.array([i.X for i in pop]))
        np.testing.assert_array_equal(*outputs)

    def test_uniform_vs_native_costs_and_repeatability(self):
        cfg,candidates=design(self.config())
        rows=[run_task(cfg,c,cfg['problems'][0],42) for c in candidates]
        self.assertEqual([r['initialization_evaluations'] for r in rows],[20,40])
        self.assertNotEqual(rows[0]['initial_x_sha256'],rows[1]['initial_x_sha256'])
        for r,c in zip(rows,candidates):
            again=run_task(cfg,c,cfg['problems'][0],42)
            self.assertEqual(r['final_f'],again['final_f'])
            self.assertEqual(r['initialization_evidence'],again['initialization_evidence'])
            self.assertLessEqual(r['n_eval'],240)
            self.assertTrue(all(t['mode']=='success_rate' for t in r['probability_trace']))
        a,b=[{k:v for k,v in c['settings'].items() if k!='initialization_method'} for c in candidates]
        self.assertEqual(a,b)
        self.assertEqual(a['restart_mode'],'adaptive')

    def test_native_seed_changes_initial_population(self):
        cfg,candidates=design(self.config())
        rows=[run_task(cfg,candidates[1],cfg['problems'][0],seed) for seed in (42,43)]
        self.assertNotEqual(rows[0]['initial_x_sha256'],rows[1]['initial_x_sha256'])

    def test_uniform_arm_matches_existing_warm_start_runner(self):
        from research.studies.restart_comparison import run_task as warm_start
        cfg,candidates=design(self.config())
        row=run_task(cfg,candidates[0],cfg['problems'][0],42)
        baseline=warm_start(cfg,candidates[0],cfg['problems'][0],42)
        self.assertEqual(row['final_x'],baseline['final_x'])
        self.assertEqual(row['final_f'],baseline['final_f'])
        self.assertEqual(row['n_eval'],baseline['n_eval'])

    def test_protocol_rejects_underfunded_initialization_or_wrong_defaults(self):
        cfg=self.config();cfg['global']['evaluation_budget']=40
        with self.assertRaisesRegex(ValueError,'Budget'):
            design(cfg)
        cfg=self.config();cfg['common_settings']['restart_mode']='classic'
        with self.assertRaisesRegex(ValueError,'adaptive'):
            design(cfg)


if __name__=='__main__': unittest.main()
