"""Single command entry point for the project."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

from research.benchmarking import algorithm_benchmark, dtlz_benchmark, pymoo_compare, wfg_benchmark
from research.plotting import algorithm_benchmark as algorithm_benchmark_plots
from research.plotting import convergence
from research.plotting import all_problems, parameter_sensitivity, wilcoxon_results
from research.studies import ablation, parameter_analysis, zdt_sensitivity, dtlz_sensitivity
from research.maintenance import tmp_sessions, inventory, check_structure
from research.benchmarking.reuse import run_benchmark_v2
from research.benchmarking import zdt_seven
from research.benchmarking import zdt_six
from research.benchmarking import deb_report
from research.studies import restart_comparison
from research.studies import probability_ablation
from research.studies import diversity_injection
from research.studies import mechanism_impact
from research.studies import mechanism_sensitivity


Command = Callable[[list[str] | None], None]


COMMANDS: dict[str, Command] = {
    "report-deb-metrics": deb_report.main,
    "benchmark-zdt-six": zdt_six.main,
    "sensitivity-mechanisms": mechanism_sensitivity.main,
    "mechanism-impact": mechanism_impact.main,
    "benchmark-zdt-seven": zdt_seven.main,
    "ablation-diversity": diversity_injection.main,
    "ablation-probability": probability_ablation.main,
    "restart-comparison": restart_comparison.main,
    "tmp": tmp_sessions.main,
    "inventory": inventory.main,
    "check-structure": check_structure.main,
    "reuse-baselines": run_benchmark_v2,
    "benchmark": algorithm_benchmark.main,
    "benchmark-algorithms": algorithm_benchmark.main,
    "benchmark-three-algorithms": algorithm_benchmark.main,
    "ablation": ablation.main,
    "benchmark-dtlz": dtlz_benchmark.main,
    "benchmark-wfg": wfg_benchmark.main,
    "benchmark-legacy": pymoo_compare.main,
    "plot-all": all_problems.main,
    "plot-algorithm-benchmark": algorithm_benchmark_plots.main,
    "plot-three-algorithms": algorithm_benchmark_plots.main,
    "plot-convergence": convergence.main,
    "plot-wilcoxon": wilcoxon_results.main,
    "sensitivity": parameter_analysis.main,
    "sensitivity-zdt": zdt_sensitivity.main,
    "sensitivity-dtlz": dtlz_sensitivity.main,
    "plot-sensitivity": parameter_sensitivity.main,
}


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="OADE-NSGA-II project runner")
    parser.add_argument("command", choices=COMMANDS)

    if not argv or argv[0] in {"-h", "--help"}:
        parser.parse_args(argv)
        return

    command = argv[0]
    if command not in COMMANDS:
        parser.parse_args([command])
        return

    COMMANDS[command](argv[1:])


if __name__ == "__main__":
    main()
