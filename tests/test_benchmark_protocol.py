from __future__ import annotations

import numpy as np
import unittest

from src.benchmarking.evaluation import (
    BudgetedProblem,
    EvaluationBudgetExceeded,
    validate_result,
)
from src.benchmarking.statistics import (
    holm_adjust,
    paired_rank_biserial,
    paired_wilcoxon_rows,
)


class SphereProblem:
    n_var = 2
    n_obj = 2
    xl = np.asarray([-1.0, -1.0])
    xu = np.asarray([1.0, 1.0])

    def evaluate(self, x):
        x = np.atleast_2d(np.asarray(x, dtype=float))
        return np.column_stack([np.sum(x**2, axis=1), np.sum((x - 0.5) ** 2, axis=1)])


class BenchmarkProtocolTests(unittest.TestCase):
    def test_budgeted_problem_counts_and_blocks_overrun(self):
        problem = BudgetedProblem(SphereProblem(), max_evaluations=3)
        result = problem.evaluate(np.zeros((2, 2)))
        self.assertEqual(result.shape, (2, 2))
        self.assertEqual(problem.n_eval, 2)
        self.assertEqual(problem.remaining_evaluations, 1)
        with self.assertRaises(EvaluationBudgetExceeded):
            problem.evaluate(np.zeros((2, 2)))
        self.assertEqual(problem.n_eval, 2)

    def test_validate_result_detects_collapsed_front_and_bounds(self):
        problem = SphereProblem()
        collapsed = validate_result(np.zeros((2, 2)), np.zeros((2, 2)), problem)
        self.assertFalse(collapsed.valid)
        self.assertEqual(collapsed.status, "collapsed_front")

        out_of_bounds = validate_result(
            np.asarray([[0.0, 0.0], [2.0, 0.0]]),
            np.asarray([[0.0, 0.5], [1.0, 0.0]]),
            problem,
        )
        self.assertFalse(out_of_bounds.valid)
        self.assertEqual(out_of_bounds.status, "out_of_bounds")

    def test_holm_adjust_is_monotone_in_sorted_p_value_order(self):
        adjusted = holm_adjust([0.03, 0.001, 0.02])
        np.testing.assert_allclose(adjusted, [0.04, 0.003, 0.04])

    def test_rank_biserial_positive_always_favours_reference(self):
        reference = np.asarray([1.0, 2.0, 3.0])
        comparison = np.asarray([2.0, 3.0, 4.0])
        self.assertAlmostEqual(paired_rank_biserial(reference, comparison, "IGD"), 1.0)
        self.assertAlmostEqual(paired_rank_biserial(comparison, reference, "HV"), 1.0)

    def test_paired_rows_match_run_indices_and_adjust_by_metric(self):
        raw_rows = []
        for problem in ("p1", "p2"):
            for run_idx in range(5):
                raw_rows.extend(
                    [
                        {
                            "problem": problem,
                            "run_idx": run_idx,
                            "algorithm": "OADE",
                            "IGD": 1.0 + run_idx,
                            "HV": 10.0 - run_idx,
                            "valid": True,
                        },
                        {
                            "problem": problem,
                            "run_idx": run_idx,
                            "algorithm": "BASE",
                            "IGD": 2.0 + run_idx,
                            "HV": 9.0 - run_idx,
                            "valid": True,
                        },
                    ]
                )

        rows = paired_wilcoxon_rows(raw_rows, "OADE", alpha=0.05)
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["n_pairs"] for row in rows}, {5})
        self.assertTrue(all(abs(row["rank_biserial_effect"] - 1.0) < 1e-12 for row in rows))
        self.assertTrue(all(row["p_adjusted_holm"] >= row["p_value"] for row in rows))


if __name__ == "__main__":
    unittest.main()

