"""Entry point for DTLZ benchmarks with 2, 3, and 5 objectives."""

from __future__ import annotations

from research.benchmarking import algorithm_benchmark


def main(argv: list[str] | None = None) -> None:
    args = list(argv or [])
    if "--config" not in args:
        args = ["--config", "config/suites/dtlz_benchmark.yaml", *args]
    algorithm_benchmark.main(args)


if __name__ == "__main__":
    main()
