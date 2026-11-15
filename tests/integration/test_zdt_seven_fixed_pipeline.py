import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from shared.paths import ROOT
from shared.io.config import load_yaml_config
from research.benchmarking import zdt_seven as study


class ZDTSevenTests(unittest.TestCase):
    def test_full_plan_fixed_oade_and_no_optimizer(self):
        cfg,candidates=study.design(load_yaml_config(Path('config/suites/zdt_seven_fixed_oade.yaml')))
        self.assertEqual(len(study.engine.tasks(cfg,candidates)),1050)
        self.assertEqual(cfg['global']['seeds'],list(range(42,72)))
        fixed=next(c for c in candidates if c['id']=='OADE_NSGAII')
        self.assertEqual(fixed['settings']['runner'],'local_oade')
        self.assertEqual(fixed['settings']['params'],{})
        self.assertEqual(cfg['baseline_revision'],study.BASELINE_REVISION)
        self.assertTrue(cfg['global']['out_dir'].endswith('_v2'))
        with patch.object(study,'run_task') as worker:
            study.main(['--stage','plan']);worker.assert_not_called()

    def test_research_or_override_config_rejected(self):
        cfg=load_yaml_config(Path('config/suites/zdt_seven_fixed_oade.yaml'))
        specs=study.load_algorithm_specs(cfg['algorithm_configs'])
        from dataclasses import replace
        for bad in [replace(specs[0],runner='local_oade_research'),replace(specs[0],params={'enable_obl':False})]:
            with patch.object(study,'load_algorithm_specs',return_value=[bad,*specs[1:]]):
                with self.assertRaisesRegex(ValueError,'fixed'):study.design(cfg)

    def test_old_baseline_parameters_rejected_before_running(self):
        from dataclasses import replace
        cfg=load_yaml_config(Path('config/suites/zdt_seven_fixed_oade.yaml'))
        specs=study.load_algorithm_specs(cfg['algorithm_configs'])
        for name,params in [('CGDE_NSGAII',{'F':.5,'CR':.9,'pbest_ratio':.2}),
                            ('NSGAII_SDR_OLS',{'local_search_max_neighbors_factor':2})]:
            bad=[replace(s,params=params) if s.name==name else s for s in specs]
            with patch.object(study,'load_algorithm_specs',return_value=bad):
                with self.assertRaisesRegex(ValueError,'corrected baseline'):study.design(cfg)

    def test_seven_solvers_checkpoint_resume_and_tamper(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            directory=Path(folder)/'study'
            args=['--config','config/smoke/smoke_zdt_seven_fixed_oade.yaml','--out-dir',str(directory),'--jobs','1']
            original=study.run_task;calls=0
            def interrupted(*task):
                nonlocal calls
                calls+=1
                if calls==3:raise RuntimeError('simulated interruption')
                return original(*task)
            with patch.object(study,'run_task',side_effect=interrupted),self.assertRaisesRegex(RuntimeError,'interruption'):
                study.main([*args,'--stage','run'])
            m=json.loads((directory/'study_manifest.json').read_text());self.assertEqual(len(m['artifacts']),2)
            snapshots={p:(directory/p).read_bytes() for p in m['artifacts']}
            with patch.object(study,'run_task',wraps=original) as worker:
                study.main([*args,'--stage','run','--resume']);self.assertEqual(worker.call_count,26)
            for p,before in snapshots.items():self.assertEqual((directory/p).read_bytes(),before)
            m=json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(len(m['artifacts']),28)
            self.assertEqual(m['kind'],'zdt_seven_fixed_oade_v2')
            self.assertFalse('reused_baseline' in m)
            rows=study.engine.load_records(directory,m)
            self.assertEqual({r['algorithm'] for r in rows},study.NAMES)
            for r in rows:
                self.assertLessEqual(r['n_eval'],400)
                self.assertEqual(len(r['final_x']),len(r['final_f']))
                self.assertTrue(r['final_f'])
                if r['algorithm']=='OADE_NSGAII':self.assertEqual(r['runner'],'local_oade')
            with patch.object(study,'run_task') as worker:
                study.main([*args,'--stage','run','--resume']);worker.assert_not_called()
            study.main([*args,'--stage','report','--resume'])
            self.assertTrue((directory/'derived/report.md').exists())
            first=directory/next(iter(m['artifacts']));first.write_text('{}')
            with self.assertRaisesRegex(ValueError,'integrity'):study.main([*args,'--stage','report','--resume'])


if __name__=='__main__':unittest.main()
