import json,csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from shared.paths import ROOT
from research.studies import diversity_injection as study


class DiversityPipelineTests(unittest.TestCase):
    def test_complete_resume_report_and_integrity(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            directory=Path(folder)/'study'
            args=['--config','config/smoke/smoke_diversity_injection.yaml','--out-dir',str(directory),'--jobs','1']
            study.main([*args,'--stage','run'])
            manifest=json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(len(manifest['artifacts']),4)
            self.assertEqual(manifest['kind'],'diversity_injection_v1')
            self.assertTrue((directory/'derived/diversity_events.csv').exists())
            pairs=list(csv.DictReader((directory/'derived/comparisons.csv').open()))
            self.assertEqual(len(pairs),2)
            self.assertTrue(all(float(r['p_holm_all_endpoints'])>=float(r['p_raw']) for r in pairs))
            with patch.object(study,'run_task') as worker:
                study.main([*args,'--stage','run','--resume'])
                worker.assert_not_called()
            study.main([*args,'--stage','report','--resume'])
            path=directory/next(iter(manifest['artifacts']))
            path.write_text('{}')
            with self.assertRaisesRegex(ValueError,'integrity'):
                study.main([*args,'--stage','report','--resume'])

    def test_plan_does_not_start_optimizer(self):
        with patch.object(study,'run_task') as worker:
            study.main(['--stage','plan'])
            worker.assert_not_called()


if __name__=='__main__': unittest.main()
