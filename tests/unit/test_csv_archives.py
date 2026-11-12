"""Archive round-trip integrity and restore boundaries (stdlib-only fixtures)."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('csv_archives', Path(__file__).resolve().parents[2] / 'scripts/csv_archives.py')
archives = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archives)


class CsvArchivesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.payload = b'problem,IGD\r\nzdt1,0.004\r\n'
        self.zip = self.root / 'results/example/csv_results.zip'
        self.zip.parent.mkdir(parents=True)
        with zipfile.ZipFile(self.zip, 'w') as bundle:
            bundle.writestr('raw.csv', self.payload)
        self.entry = {'archive': 'results/example/csv_results.zip',
                      'sha256': archives.digest(self.zip.read_bytes()),
                      'files': [{'path': 'results/example/raw.csv', 'member': 'raw.csv',
                                 'bytes': len(self.payload), 'sha256': archives.digest(self.payload)}]}
        self.save_catalog()

    def save_catalog(self):
        (self.root / 'results/csv_archives.json').write_text(json.dumps({'archives': [self.entry]}), encoding='utf-8')

    def test_clean_restore_is_exact_and_repeatable(self):
        self.assertEqual(archives.verify(self.root), 1)
        self.assertFalse((self.zip.parent / 'raw.csv').exists())
        self.assertEqual(archives.verify(self.root, restore=True), 1)
        self.assertEqual((self.zip.parent / 'raw.csv').read_bytes(), self.payload)
        self.assertEqual(archives.verify(self.root, restore=True), 1)

    def test_local_edits_are_preserved(self):
        target = self.zip.parent / 'raw.csv'
        target.write_bytes(b'local edit')
        with self.assertRaisesRegex(ValueError, 'will not overwrite'):
            archives.verify(self.root, restore=True)
        self.assertEqual(target.read_bytes(), b'local edit')

    def test_corrupted_zip_rejected(self):
        self.zip.write_bytes(self.zip.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'ZIP checksum'):
            archives.verify(self.root, restore=True)

    def test_corrupted_member_rejected(self):
        self.entry['files'][0]['sha256'] = hashlib.sha256(b'wrong').hexdigest()
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'CSV checksum'):
            archives.verify(self.root, restore=True)

    def test_path_escape_rejected(self):
        self.entry['files'][0]['path'] = '../escape.csv'
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
            archives.verify(self.root, restore=True)


if __name__ == '__main__':
    unittest.main()
