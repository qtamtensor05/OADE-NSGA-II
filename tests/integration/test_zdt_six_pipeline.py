import copy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from shared.io.config import load_yaml_config
from research.benchmarking import zdt_six as study


class ZDTSixTests(unittest.TestCase):
    def test_plan_and_reject_removed_methods_or_unpaired_sampling(self):
        raw=load_yaml_config(Path('config/suites/zdt_six_fixed_oade.yaml'))
        cfg,candidates=study.design(raw)
        self.assertEqual(len(study.engine.tasks(cfg,candidates)),900)
        self.assertEqual({c['id'] for c in candidates},study.NAMES)
        with patch.object(study,'run_task') as worker:
            study.main(['--stage','plan']);worker.assert_not_called()
        specs=study.load_algorithm_specs(raw['algorithm_configs'])
        for bad in [replace(specs[-1],name='CE_MOEA'),replace(specs[-1],sampling=None),replace(specs[-1],params={})]:
            with patch.object(study,'load_algorithm_specs',return_value=[*specs[:-1],bad]):
                with self.assertRaises(ValueError):study.design(raw)

    def test_new_library_solvers_reproduce_and_respect_hard_budget(self):
        from pymoo.problems import get_problem
        cfg,candidates=study.design(load_yaml_config(Path('config/smoke/smoke_zdt_six.yaml')))
        cfg['global']['evaluation_budget']=307
        cfg['reference_fronts']={p['name']:get_problem(p['name'],n_var=p['n_var']).pareto_front().tolist() for p in cfg['problems']}
        for candidate in candidates:
            if candidate['id'] not in ('GDE3','NSDE'):continue
            first=study.run_task(cfg,candidate,cfg['problems'][0],9100)
            second=study.run_task(cfg,candidate,cfg['problems'][0],9100)
            self.assertTrue(first['valid'])
            self.assertLessEqual(first['n_eval'],307)
            np.testing.assert_array_equal(first['final_f'],second['final_f'])

    def test_checkpoint_resume_and_global_holm_report(self):
        from pymoo.problems import get_problem
        cfg=load_yaml_config(Path('config/smoke/smoke_zdt_six.yaml'))
        cfg['problems']=[dict(name='zdt6',n_var=10)]
        with tempfile.TemporaryDirectory() as temp:
            config=Path(temp)/'config.yaml'
            import yaml
            config.write_text(yaml.safe_dump(cfg))
            directory=Path(temp)/'study'
            args=['--config',str(config),'--out-dir',str(directory),'--jobs','1']
            worker=study.run_task;calls=0
            def interrupt(*task):
                nonlocal calls
                calls+=1
                if calls==3:raise RuntimeError('interrupted')
                return worker(*task)
            with patch.object(study,'run_task',side_effect=interrupt),self.assertRaisesRegex(RuntimeError,'interrupted'):
                study.main(args+['--stage','run'])
            m=json.loads((directory/'study_manifest.json').read_text())
            snapshot={n:(directory/n).read_bytes() for n in m['artifacts']}
            with patch.object(study,'run_task',wraps=worker) as resumed:
                study.main(args+['--stage','run','--resume'])
                self.assertEqual(resumed.call_count,10)
            for n,b in snapshot.items():self.assertEqual((directory/n).read_bytes(),b)
            m=json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(len(m['artifacts']),12)
            import csv
            with (directory/'derived/comparisons.csv').open() as f:paired=list(csv.DictReader(f))
            self.assertEqual(len(paired),10)
            pvalues=study.holm_adjust(float(r['p_value']) for r in paired)
            np.testing.assert_allclose(pvalues,[float(r['p_adjusted_holm']) for r in paired])
            report=(directory/'derived/report.md').read_text(encoding='utf-8')
            self.assertIn('IGD — mean (best)',report)
            self.assertNotIn('| Valid',report)
            primary=directory/next(iter(m['artifacts']))
            primary.write_bytes(primary.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'integrity mismatch'):
                study.main(args+['--stage','run','--resume'])


if __name__=='__main__':unittest.main()
