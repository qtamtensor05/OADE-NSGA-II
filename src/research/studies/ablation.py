"""Entry point for the fixed-budget OADE ablation study."""

from __future__ import annotations

from research.benchmarking import algorithm_benchmark


def main(argv: list[str] | None = None) -> None:
    args = list(argv or [])
    if "--config" not in args:
        args = ["--config", "config/studies/ablation.yaml", *args]
    algorithm_benchmark.main(args)


if __name__ == "__main__":
    main()
