import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import yaml
from pymoo.problems import get_problem
from oade_nsga2 import OADE_NSGAII, ProblemWrapper
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded
from research.studies.mechanism_sensitivity import LevelOADE, design, main, run_one, report, atomic_json


class MechanismSensitivityTests(unittest.TestCase):
    def test_atomic_json_retries_lock_and_preserves_checkpoint_on_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'manifest.json'
            target.write_text('{"old": true}')
            replace=Path.replace
            calls=[]
            def briefly_locked(source,destination):
                calls.append(1)
                if len(calls)<3:
                    raise PermissionError('temporarily locked')
                return replace(source,destination)
            with patch.object(Path,'replace',briefly_locked), patch('research.studies.mechanism_sensitivity.time.sleep'):
                atomic_json(target,{'new':True})
            self.assertEqual(len(calls),3)
            self.assertEqual(json.loads(target.read_text()),{'new':True})
            with patch.object(Path,'replace',side_effect=PermissionError('locked')), patch('research.studies.mechanism_sensitivity.time.sleep'):
                with self.assertRaises(PermissionError):
                    atomic_json(target,{'pending':True})
            self.assertEqual(json.loads(target.read_text()),{'new':True})
            self.assertEqual(json.loads(target.with_suffix('.tmp').read_text()),{'pending':True})

    def setUp(self):
        self.cfg=yaml.safe_load(Path('config/smoke/smoke_mechanism_sensitivity.yaml').read_text())

    def test_default_reproduces_production_and_held_values_survive_reset(self):
        candidate=dict(id='full',parameter='baseline',level=None,mode='initial')
        ref=get_problem('zdt6',n_var=10).pareto_front().tolist()
        observed=run_one('zdt6',42,candidate,10,300,ref)
        counter=BudgetedProblem(get_problem('zdt6',n_var=10),300)
        solver=OADE_NSGAII(ProblemWrapper(counter),pop_size=10,n_gen=300,seed=42)
        try:
            solver.run()
        except EvaluationBudgetExceeded:
            pass
        # Compare the nondominated exported front, not incidental population order.
        from shared.fronts import non_dominated_xy
        x,f=non_dominated_xy(np.array([i.X for i in solver.population]),np.array([i.F for i in solver.population]))
        np.testing.assert_array_equal(observed['final_f'],f)
        self.assertEqual(observed['n_eval'],counter.n_eval)
        for param,value,field in [('mean_F',.4,'mean_F'),('mean_CR',.1,'mean_CR'),('prob_de',.2,'pde')]:
            c=dict(id='test',parameter=param,level=value,mode='held')
            r=run_one('zdt6',42,c,10,300,ref)
            self.assertTrue(r['trace'])
            self.assertTrue(all(t[field]==value for t in r['trace']))
            self.assertEqual(observed['initial_x_sha256'],r['initial_x_sha256'])

    def test_obl_interval_really_changes_schedule(self):
        c=dict(id='test',parameter='obl_interval',level=2,mode='initial')
        ref=get_problem('zdt4',n_var=10).pareto_front().tolist()
        r=run_one('zdt4',42,c,10,300,ref)
        generations=[e['generation'] for e in r['events'] if e['mechanism']=='obl']
        self.assertIn(3,generations)  # generation index starts at one; schedule uses gen=2.
        self.assertTrue(all((g-1)%2==0 for g in generations))

    def test_held_parameter_survives_restart(self):
        c=dict(id='held',parameter='mean_F',level=.4,mode='held')
        counter=BudgetedProblem(get_problem('zdt6',n_var=10),500)
        solver=LevelOADE(ProblemWrapper(counter),pop_size=10,n_gen=1,seed=42,candidate=c)
        solver.run()
        solver._adaptive_restart()
        self.assertEqual(solver.mean_F,.4)
        self.assertTrue(any(e['mechanism']=='restart' for e in solver.events))

    def test_invalid_pairs_preserve_multiplicity_family(self):
        records=[]
        for algorithm in ('full','level'):
            for seed in (1,2):
                records.append(dict(problem='zdt4',algorithm=algorithm,seed=seed,run_idx=seed,
                    valid=False,n_eval=100,runtime_seconds=1.,IGD=None,HV=None,events=[],trace=[]))
        contrasts=[dict(parameter='obl_interval',level=5,mode='initial',reference='full',candidate='level')]
        with tempfile.TemporaryDirectory() as temp:
            report(Path(temp),records,contrasts,[1,2])
            import csv
            with (Path(temp)/'derived/comparisons.csv').open() as stream:
                rows=list(csv.DictReader(stream))
            self.assertEqual(len(rows),2)
            self.assertTrue(all(r['result']=='no_valid_pairs' and int(r['excluded_pairs'])==2 for r in rows))

    def test_invalid_ineffective_and_unsupported_levels(self):
        for key,levels in [('restart_elite_ratio',[.7,.8]),('n_neighbors',[5,10]),('obl_interval',[0,10]),('mean_F',[.65,float('nan')])]:
            cfg=copy.deepcopy(self.cfg)
            cfg['parameters']={key:dict(levels=levels,mode='initial')}
            with self.assertRaises(ValueError):
                design(cfg)

    def test_plan_resume_report_and_checksum_guard(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['parameters']={'mean_F':dict(levels=[.4,.65],mode='held')}
        cfg['problems']=['zdt6']
        with tempfile.TemporaryDirectory() as temp:
            config=Path(temp)/'config.yaml'; config.write_text(yaml.safe_dump(cfg))
            out=Path(temp)/'output'
            args=['--config',str(config),'--out-dir',str(out)]
            main(args+['--stage','plan'])
            self.assertFalse(out.exists())
            main(args+['--stage','run'])
            before={p.name:p.read_bytes() for p in (out/'primary').glob('*.json')}
            main(args+['--stage','report','--resume'])
            main(args+['--stage','run','--resume'])
            self.assertEqual(before,{p.name:p.read_bytes() for p in (out/'primary').glob('*.json')})
            manifest=json.loads((out/'manifest.json').read_text())
            self.assertEqual(len(manifest['artifacts']),6)
            self.assertTrue((out/'derived/report.md').exists())
            primary=next((out/'primary').glob('*.json'))
            primary.write_text(primary.read_text()+' ')
            with self.assertRaisesRegex(ValueError,'Checksum mismatch'):
                main(args+['--stage','run','--resume'])

    def test_process_workers_match_serial_and_resume_only_missing(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['parameters']={'mean_F':dict(levels=[.4,.65],mode='held')}
        cfg['problems']=['zdt6']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            config=root/'config.yaml'; config.write_text(yaml.safe_dump(cfg))
            for name,jobs in [('serial',1),('parallel',2)]:
                main(['--config',str(config),'--out-dir',str(root/name),'--stage','run','--jobs',str(jobs)])
            serial=root/'serial'; parallel=root/'parallel'
            for p in (serial/'primary').glob('*.json'):
                first=json.loads(p.read_text())
                second=json.loads((parallel/'primary'/p.name).read_text())
                for record in (first,second):
                    record.pop('runtime_seconds')
                    record.pop('execution_jobs')
                self.assertEqual(first,second)
            for name in ('comparisons.csv','activation.csv','events.csv','trace.csv'):
                self.assertEqual((serial/'derived'/name).read_bytes(),(parallel/'derived'/name).read_bytes())
            # Simulate a checkpoint missing exactly one task. Resume may change
            # worker count without recomputing committed primary records.
            manifest_path=parallel/'manifest.json'
            manifest=json.loads(manifest_path.read_text())
            missing=next(iter(manifest['artifacts']))
            (parallel/'primary'/missing).unlink()
            del manifest['artifacts'][missing]
            manifest_path.write_text(json.dumps(manifest))
            before={p.name:p.read_bytes() for p in (parallel/'primary').glob('*.json')}
            main(['--config',str(config),'--out-dir',str(parallel),'--stage','run','--jobs','1','--resume'])
            for name,data in before.items():
                self.assertEqual(data,(parallel/'primary'/name).read_bytes())
            after=json.loads(manifest_path.read_text())
            self.assertEqual(len(after['artifacts']),6)
            self.assertEqual([s['jobs'] for s in after['execution_sessions']],[2,1])

    def test_nonpositive_jobs_rejected_before_output(self):
        with self.assertRaises(SystemExit):
            main(['--jobs','0'])


if __name__=='__main__':
    unittest.main()
