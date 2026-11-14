import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from research.studies import initialization_comparison as study
from shared.paths import ROOT


class InitializationPipelineTests(unittest.TestCase):
    def test_smoke_resume_and_integrity(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            directory=Path(folder)/'study'
            args=['--config','config/smoke/smoke_initialization_comparison.yaml','--out-dir',str(directory),'--jobs','1']
            study.main([*args,'--stage','run'])
            manifest=json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(len(manifest['artifacts']),4)
            self.assertEqual(manifest['kind'],'initialization_comparison_v1')
            report=(directory/'derived/report.md').read_text(encoding='utf-8')
            self.assertIn('Sobol',report)
            self.assertIn('success-rate',report)
            self.assertTrue((directory/'derived/summary.csv').is_file())
            with patch.object(study,'run_task') as worker:
                study.main([*args,'--stage','run','--resume'])
                worker.assert_not_called()
            path=directory/next(iter(manifest['artifacts']))
            path.write_text('{}')
            with self.assertRaisesRegex(ValueError,'integrity'):
                study.main([*args,'--stage','report','--resume'])

    def test_plan_does_not_run_optimizer(self):
        with patch.object(study,'run_task') as worker:
            study.main(['--stage','plan'])
            worker.assert_not_called()


if __name__=='__main__': unittest.main()
