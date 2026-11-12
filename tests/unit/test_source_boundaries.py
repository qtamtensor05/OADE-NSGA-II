from pathlib import Path
import tempfile
import unittest

from research.maintenance.check_structure import check_source_boundaries
from shared.paths import ROOT


class SourceBoundaryTests(unittest.TestCase):
    def test_actual_algorithm_and_shared_packages_do_not_depend_on_research(self):
        self.assertEqual(check_source_boundaries(), [])

    def test_guard_rejects_analysis_in_algorithm_and_concrete_solver_in_benchmark(self):
        (ROOT / "tmp/tests").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp/tests") as directory:
            root = Path(directory)
            for package, content in {
                "nsga2": "from research.plotting import common\n",
                "shared": "from research.benchmarking import statistics\n",
                "research": "from pymoo.algorithms.moo.nsga2 import NSGA2\n",
            }.items():
                (root / package).mkdir()
                (root / package / "incorrect.py").write_text(content)
            self.assertEqual(len(check_source_boundaries(root)), 3)
