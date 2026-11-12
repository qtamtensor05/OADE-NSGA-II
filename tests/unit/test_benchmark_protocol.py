from __future__ import annotations

import numpy as np
import unittest

from research.benchmarking.evaluation import (
    BudgetedProblem,
    EvaluationBudgetExceeded,
    validate_result,
)
from research.benchmarking.statistics import (
    holm_adjust,
    paired_rank_biserial,
    paired_wilcoxon_rows,
)
from research.benchmarking.algorithm_benchmark import (
    AlgorithmSpec, summarize, summarize_costs, ConvergenceRecorder, _run_pymoo,
)
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV


class SphereProblem:
    n_var = 2
    n_obj = 2
    xl = np.asarray([-1.0, -1.0])
    xu = np.asarray([1.0, 1.0])

    def evaluate(self, x):
        x = np.atleast_2d(np.asarray(x, dtype=float))
        return np.column_stack([np.sum(x**2, axis=1), np.sum((x - 0.5) ** 2, axis=1)])


class BenchmarkProtocolTests(unittest.TestCase):
    def test_rnsga2_reference_setup_is_in_actual_budget_count(self):
        class CountingProblem:
            def __init__(self):
                self.problem = get_problem("zdt1", n_var=3)
                self.actual = 0

            def evaluate(self, x, *args, **kwargs):
                self.actual += len(np.atleast_2d(x))
                return self.problem.evaluate(x, *args, **kwargs)

            def __getattr__(self, name):
                return getattr(self.problem, name)

        problem = CountingProblem()
        front = problem.pareto_front()
        recorder = ConvergenceRecorder(200, IGD(front), HV(ref_point=np.max(front, axis=0) + 0.1))
        spec = AlgorithmSpec("RNSGA2", "pymoo", {},
                             class_path="pymoo.algorithms.moo.rnsga2.RNSGA2",
                             sampling="initial_population", auto_ref_points=True)
        outcome = _run_pymoo(spec, problem, 20, 200,
                             np.random.default_rng(42).uniform(size=(20, 3)), 42, recorder)
        self.assertEqual(outcome.n_eval, problem.actual)
        self.assertLessEqual(problem.actual, 200)
        self.assertGreater(problem.actual, 20)

    def test_paired_rows_allow_empty_resume_preflight(self):
        self.assertEqual(paired_wilcoxon_rows([], "OADE_FULL"), [])

    def test_summary_accepts_resumed_csv_strings_and_new_numeric_rows(self):
        spec = AlgorithmSpec(name="OADE", runner="local_oade", params={})
        base = {
            "problem": "zdt1",
            "n_var": "30",
            "n_obj": "2",
            "algorithm": "OADE",
            "runner": "local_oade",
            "valid": "True",
            "IGD": "0.2",
            "HV": "0.8",
            "runtime_seconds": "1.5",
            "n_eval": "20000",
            "budget_utilization": "1.0",
            "front_size": "20",
        }
        numeric = dict(base)
        numeric.update(
            n_var=30,
            n_obj=2,
            valid=True,
            IGD=0.1,
            HV=0.9,
            runtime_seconds=1.0,
            n_eval=20000,
            budget_utilization=1.0,
            front_size=20,
        )
        rows = summarize([base, numeric], [spec])
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["IGD_mean"], 0.15)
        self.assertAlmostEqual(rows[0]["HV_mean"], 0.85)
        costs = summarize_costs([base, numeric])
        self.assertEqual(len(costs), 1)
        self.assertAlmostEqual(costs[0]["n_eval_mean"], 20000.0)
        self.assertAlmostEqual(costs[0]["front_size_mean"], 20.0)

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

    def test_holm_adjust_treats_nan_as_one_without_corrupting_other_values(self):
        adjusted = holm_adjust([0.003, float("nan"), 0.0001, 0.2])
        np.testing.assert_allclose(adjusted, [0.009, 1.0, 0.0004, 0.4])

    def test_all_zero_paired_differences_do_not_poison_subsequent_problems(self):
        raw_rows = []
        for run_idx in range(10):
            raw_rows.extend(
                [
                    {"problem": "p1_zero", "run_idx": run_idx, "algorithm": "OADE", "IGD": 1.0, "HV": 0.0, "valid": True},
                    {"problem": "p1_zero", "run_idx": run_idx, "algorithm": "BASE", "IGD": 2.0, "HV": 0.0, "valid": True},
                    {"problem": "p2_diff", "run_idx": run_idx, "algorithm": "OADE", "IGD": 1.0 + run_idx, "HV": 0.9 - 0.01 * run_idx, "valid": True},
                    {"problem": "p2_diff", "run_idx": run_idx, "algorithm": "BASE", "IGD": 2.0 + run_idx, "HV": 0.1 - 0.01 * run_idx, "valid": True},
                ]
            )
        rows = paired_wilcoxon_rows(raw_rows, "OADE", alpha=0.05)
        hv_zero = next(row for row in rows if row["problem"] == "p1_zero" and row["metric"] == "HV")
        hv_diff = next(row for row in rows if row["problem"] == "p2_diff" and row["metric"] == "HV")
        self.assertEqual(hv_zero["p_value"], 1.0)
        self.assertEqual(hv_zero["p_adjusted_holm"], 1.0)
        self.assertLess(hv_diff["p_adjusted_holm"], 0.05)
        self.assertEqual(hv_diff["result"], "reference_better")

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

