import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.studies.restart_comparison import main
from shared.paths import ROOT


class RestartPipelineTests(unittest.TestCase):
    def test_checkpoint_report_resume_and_tamper_rejection(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            directory = Path(folder)/'study'
            args = ['--config','config/smoke/smoke_restart_comparison.yaml',
                    '--out-dir',str(directory),'--jobs','1']
            main([*args,'--stage','run'])
            manifest = json.loads((directory/'study_manifest.json').read_text())
            self.assertEqual(len(manifest['artifacts']),6)
            import csv
            paired=list(csv.DictReader((directory/'derived/comparisons.csv').open()))
            self.assertEqual(len(paired),6)
            self.assertTrue(all(float(r['p_holm_all_endpoints'])>=float(r['p_raw']) for r in paired))
            self.assertTrue((directory/'derived/summary.csv').is_file())
            self.assertTrue((directory/'derived/probability_trace.csv').is_file())
            self.assertTrue((directory/'derived/diversity_events.csv').is_file())
            self.assertTrue((directory/'derived/restart_events.csv').exists())
            with patch('research.studies.restart_comparison.run_task') as worker:
                main([*args,'--stage','run','--resume'])
                worker.assert_not_called()
            main([*args,'--stage','report','--resume'])
            source = directory/next(iter(manifest['artifacts']))
            source.write_text('{}')
            with self.assertRaisesRegex(ValueError,'integrity'):
                main([*args,'--stage','report','--resume'])

    def test_plan_never_starts_solver(self):
        with patch('research.studies.restart_comparison.run_task') as worker:
            main(['--stage','plan'])
            worker.assert_not_called()


if __name__ == '__main__':
    unittest.main()
