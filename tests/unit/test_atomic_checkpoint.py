import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from research.studies.zdt_sensitivity import atomic_json
from shared.paths import ROOT


class AtomicCheckpointTests(unittest.TestCase):
    def test_transient_permission_error_retries_same_complete_payload(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            target=Path(folder)/'manifest.json'
            target.write_text('{"old":1}')
            original=Path.replace
            attempts=[]
            def flaky(source,destination):
                attempts.append(source.read_bytes())
                if len(attempts)<3:
                    self.assertEqual(json.loads(target.read_text()),{'old':1})
                    raise PermissionError('Simulated Windows sharing violation')
                return original(source,destination)
            with patch.object(Path,'replace',flaky),patch('research.studies.zdt_sensitivity.time.sleep') as sleep:
                atomic_json(target,{'new':2})
                self.assertEqual(sleep.call_count,2)
            self.assertEqual(json.loads(target.read_text()),{'new':2})
            self.assertEqual(len(set(attempts)),1)

    def test_permanent_permission_error_preserves_old_and_pending_evidence(self):
        (ROOT/'tmp/tests').mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'tmp/tests') as folder:
            target=Path(folder)/'manifest.json'
            target.write_text('{"old":1}')
            with patch.object(Path,'replace',side_effect=PermissionError('locked')) as replace,patch('research.studies.zdt_sensitivity.time.sleep'):
                with self.assertRaises(PermissionError): atomic_json(target,{'new':2})
                self.assertEqual(replace.call_count,8)
            self.assertEqual(json.loads(target.read_text()),{'old':1})
            self.assertEqual(json.loads(target.with_suffix('.json.tmp').read_text()),{'new':2})


if __name__=='__main__': unittest.main()
