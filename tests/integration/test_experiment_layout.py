from __future__ import annotations
import csv
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

from shared.paths import ROOT
from research.benchmarking import runner, layout
from research.benchmarking.models import RAW_CSV, SUMMARY_CSV
from shared.io.config import load_yaml_config
from shared.io.csv_io import read_csv
from research.benchmarking.reuse import run_benchmark_v2


class ExperimentLayoutTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "tmp/tests").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tmp/tests")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / "tiny.json"
        self.config.write_text(json.dumps({
            "global": {"runs": 2, "pop_size": 10, "evaluation_budget": 40, "seed_base": 42,
                       "out_dir": str(self.root / "flat")},
            "problems": [{"name": "zdt1", "n_var": 30}],
            "algorithm_configs": ["config/algorithms/oade_nsga2.yaml", "config/algorithms/nsga2.yaml"],
            "statistics": {"reference_algorithm": "OADE_NSGAII", "alpha": 0.05},
        }))

    def test_new_layout_resume_integrity_and_derived_readers(self):
        with patch.object(layout, "ROOT", self.root):
            runner.main(["--config", str(self.config), "--experiment", "tiny_budget40_v1"])
        execution = next((self.root / "results/experiments/tiny_budget40_v1").iterdir())
        primary = execution / "primary" / RAW_CSV
        before = primary.read_bytes()
        self.assertTrue((execution / "derived" / SUMMARY_CSV).exists())
        self.assertTrue((execution / "environment/runtime.json").exists())
        self.assertTrue((execution / "logs/run.log").exists())
        self.assertEqual(json.loads((execution / "logs/status.json").read_text())["status"], "completed")
        self.assertEqual(len(read_csv(execution / RAW_CSV)), 4)
        self.assertEqual(len(read_csv(execution / SUMMARY_CSV)), 2)
        runner.main(["--config", str(self.config), "--out-dir", str(execution), "--resume"])
        self.assertEqual(before, primary.read_bytes())
        run_benchmark_v2(["--config", str(self.config), "--baseline-dir", str(execution), "--preflight-only"])
        with self.assertRaises(ValueError):
            runner.main(["--config", str(self.config), "--out-dir", str(execution)])
        primary.write_bytes(before + b"tampered")
        with self.assertRaises(ValueError):
            runner.main(["--config", str(self.config), "--out-dir", str(execution), "--resume"])

    def test_historical_config_aliases_still_resolve(self):
        self.assertEqual(load_yaml_config(Path("config/algorithm_benchmark_v2.yaml")),
                         load_yaml_config(Path("config/suites/algorithm_benchmark_v2.yaml")))

    def test_flat_output_contract_still_works(self):
        runner.main(["--config", str(self.config)])
        self.assertTrue((self.root / "flat" / RAW_CSV).exists())
        self.assertTrue((self.root / "flat" / SUMMARY_CSV).exists())

    def test_cli_and_compatibility_entrypoint_work_outside_checkout(self):
        for command in ([sys.executable, "-m", "research", "--help"],
                        [sys.executable, str(ROOT / "main.py"), "--help"]):
            result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("benchmark-dtlz", result.stdout)
