"""Resolve repository-owned inputs independently of the working directory."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def repository_path(value: str | Path) -> Path:
    """Relative research inputs are anchored to the checkout, not the shell cwd."""
    path = Path(value)
    return path if path.is_absolute() else ROOT / path
