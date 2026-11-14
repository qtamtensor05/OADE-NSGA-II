import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.studies.probability_ablation import main, design
from research.studies import restart_comparison as base
from shared.io.config import load_yaml_config
from shared.paths import ROOT


class ProbabilityPipelineTests(unittest.TestCase):
    def test_two_mode_protocol_uses_one_comparison_per_metric(self):
        cfg,candidates=design(load_yaml_config(Path('config/studies/probability_ablation.yaml')))
        self.assertEqual([c['id'] for c in candidates],['fixed','success_rate'])
        rows=[]
        for c in candidates:
            for seed in (1,2,3):
                rows.append({'candidate':c['id'],'problem':'zdt1','seed':seed,'valid':True,
                             'IGD':float(seed)+(1 if c['id']=='fixed' else 0),
                             'HV':float(seed)+(0 if c['id']=='fixed' else 1),
                             'initial_x_sha256':'same','final_f':[[seed]],
                             'telemetry':{'restart_attempts':0}})
        cfg['problems']=cfg['problems'][:1]
        comparisons=base.comparisons(cfg,candidates,rows)
        self.assertEqual(len(comparisons),2)
        for r in comparisons:
            self.assertEqual(r['p_holm'],r['p_raw'])

    def test_smoke_resume_and_trace(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            directory=Path(folder)/'study'
            args=['--config','config/smoke/smoke_probability_ablation.yaml','--out-dir',str(directory),'--jobs','1']
            main([*args,'--stage','run'])
            manifest=json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(manifest['kind'],'probability_ablation_v1')
            rows=base.engine.load_records(directory,manifest)
            self.assertEqual(len(rows),4)
            for row in rows:
                self.assertEqual(row['parameter'],'probability_update_mode')
                self.assertTrue(row['probability_trace'])
                self.assertTrue(all(t['mode']==row['candidate'] for t in row['probability_trace']))
                if row['candidate']=='fixed':
                    self.assertTrue(all(t['prob_after']==.5 for t in row['probability_trace']))
            self.assertTrue((directory/'derived/probability_trace.csv').is_file())
            self.assertIn('Probability adaptation', (directory/'derived/report.md').read_text())
            with patch.object(base,'run_task') as worker:
                main([*args,'--stage','run','--resume'])
                worker.assert_not_called()
            source=directory/next(iter(manifest['artifacts']))
            source.write_text('{}')
            with self.assertRaisesRegex(ValueError,'integrity'):
                main([*args,'--stage','report','--resume'])

    def test_only_probability_mode_differs(self):
        _,candidates=design(load_yaml_config(Path('config/studies/probability_ablation.yaml')))
        settings=[{k:v for k,v in c['settings'].items() if k!='probability_update_mode'} for c in candidates]
        self.assertEqual(settings[0],settings[1])
        self.assertEqual(len(candidates),2)
        with patch.object(base,'run_task') as worker:
            main(['--stage','plan'])
            worker.assert_not_called()

    def test_unknown_mode_not_accepted_by_study(self):
        cfg=load_yaml_config(Path('config/studies/probability_ablation.yaml'))
        cfg['probability_modes']=['invalid_mode','success_rate']
        with self.assertRaisesRegex(ValueError,'fixed and success_rate'):
            design(cfg)
