from __future__ import annotations
from datetime import timedelta
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from shared.paths import ROOT
from research.maintenance import tmp_sessions as sessions


class TmpSessionTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "tmp/tests").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tmp/tests")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.path = sessions.create("smoke", "cleanup safety", root=self.root)
        (self.path / "output.txt").write_text("disposable")
        self.future = sessions.now() + timedelta(days=30)

    def close(self):
        sessions.finish(self.path, disposable=True, root=self.root)

    def test_only_expired_disposable_sessions_are_deleted_and_dry_run_preserves(self):
        with self.assertRaises(ValueError):
            sessions.clean(self.path, root=self.root, at=self.future)
        self.close()
        with self.assertRaises(ValueError):
            sessions.clean(self.path, root=self.root)
        sessions.clean(self.path, root=self.root, at=self.future)
        self.assertTrue((self.path / "output.txt").exists())
        sessions.clean(self.path, apply=True, root=self.root, at=self.future)
        self.assertFalse(self.path.exists())
        self.assertTrue((self.root / "tmp/cleanup.jsonl").is_file())

    def test_tracked_files_are_kept(self):
        self.close()
        subprocess.run(["git", "add", str(self.path / "output.txt")], cwd=self.root, check=True)
        with self.assertRaises(ValueError):
            sessions.clean(self.path, apply=True, root=self.root, at=self.future)
        self.assertTrue(self.path.exists())

    def test_missing_malformed_and_retained_metadata_are_kept(self):
        for content in ('{}', 'invalid json'):
            (self.path / "session.json").write_text(content)
            with self.assertRaises(ValueError):
                sessions.clean(self.path, root=self.root, at=self.future)
        (self.path / "session.json").unlink()
        with self.assertRaises(FileNotFoundError):
            sessions.clean(self.path, root=self.root, at=self.future)

    def test_escape_root_and_category_are_rejected(self):
        for path in (self.root, self.root / "tmp", self.root / "results", self.root.parent):
            with self.assertRaises(ValueError):
                sessions.clean(path, apply=True, root=self.root, at=self.future)

    def test_session_lock_prevents_cleanup(self):
        self.close()
        with sessions.session_lock(self.path):
            with self.assertRaises(OSError):
                sessions.clean(self.path, apply=True, root=self.root, at=self.future)
        self.assertTrue(self.path.exists())

    def test_junction_or_symlink_inside_session_is_rejected(self):
        self.close()
        outside = self.root / "protected"
        outside.mkdir()
        (outside / "evidence.txt").write_text("preserve")
        link = self.path / "linked"
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest("Junction creation unavailable")
        else:
            link.symlink_to(outside, target_is_directory=True)
        try:
            with self.assertRaises(ValueError):
                sessions.clean(self.path, apply=True, root=self.root, at=self.future)
            self.assertTrue((outside / "evidence.txt").exists())
        finally:
            os.rmdir(link) if os.name == "nt" else link.unlink()

    def test_create_rejects_linked_tmp_parent(self):
        outside = self.root / "outside"
        outside.mkdir()
        parent = self.root / "tmp/one_off"
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(parent), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest("Junction creation unavailable")
        else:
            parent.symlink_to(outside, target_is_directory=True)
        try:
            with self.assertRaises(ValueError):
                sessions.create("one_off", "escape", root=self.root)
            self.assertEqual(list(outside.iterdir()), [])
        finally:
            os.rmdir(parent) if os.name == "nt" else parent.unlink()

    def test_failed_session_is_retained_by_default(self):
        sessions.finish(self.path, status="failed", root=self.root)
        with self.assertRaises(ValueError):
            sessions.clean(self.path, apply=True, root=self.root, at=self.future)
