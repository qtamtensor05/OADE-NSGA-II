"""Disposable sessions with cooperative process locks and fail-closed cleanup."""
from __future__ import annotations

import argparse
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import uuid

from shared.paths import ROOT

CATEGORIES = {"smoke", "one_off", "tests", "figure_qa"}


def now():
    return datetime.now(timezone.utc)


def linked(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & 0x400)


def safe_session(path: Path, root: Path = ROOT) -> Path:
    """Require a direct category/session descendant, without links at any level."""
    root = root.resolve()
    candidate = Path(os.path.abspath(path))
    relative = candidate.relative_to(root)
    if len(relative.parts) != 3 or relative.parts[0] != "tmp" or relative.parts[1] not in CATEGORIES:
        raise ValueError("Expected tmp/<category>/<session> inside repository")
    current = root
    for part in relative.parts:
        current /= part
        if current.exists() or current.is_symlink():
            if linked(current):
                raise ValueError(f"Linked/reparse path is not allowed: {current}")
    if not candidate.is_dir():
        raise ValueError(f"Session does not exist: {candidate}")
    return candidate


@contextmanager
def session_lock(path: Path):
    """All session users/cleaners acquire the same nonblocking OS lock."""
    for entry in (path / ".lock", path / "session.json"):
        if (entry.exists() or entry.is_symlink()) and linked(entry):
            raise ValueError("Linked lock or session metadata is not allowed")
    with (path / ".lock").open("a+b") as handle:
        handle.seek(0, io.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def save(path: Path, metadata: dict):
    temporary = path / "session.json.tmp"
    temporary.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path / "session.json")


def create(category: str, purpose: str, *, root: Path = ROOT) -> Path:
    if category not in CATEGORIES:
        raise ValueError("Unknown session category")
    slug = re.sub(r"[^a-z0-9]+", "_", purpose.lower()).strip("_")[:40] or "session"
    session_id = f"{now():%Y%m%dT%H%M%SZ}_{slug}_{uuid.uuid4().hex[:8]}"
    path = root.resolve() / "tmp" / category / session_id
    # Check parent links before mkdir so creation never writes through a junction.
    for parent in (root / "tmp", root / "tmp" / category):
        if (parent.exists() or parent.is_symlink()) and linked(parent):
            raise ValueError("Linked tmp parent is not allowed")
    path.mkdir(parents=True)
    safe_session(path, root)
    save(path, {"schema": 1, "purpose": purpose, "created_utc": now().isoformat(),
                "status": "active", "disposable": False,
                "retention_days": 14 if category == "one_off" else 7,
                "promoted_to": [], "command": ""})
    return path


def finish(path: Path, *, status="completed", disposable=False, root=ROOT):
    path = safe_session(path, root)
    with session_lock(path):
        metadata = json.loads((path / "session.json").read_text(encoding="utf-8"))
        if status not in {"completed", "failed"}:
            raise ValueError("Only completed/failed sessions can be closed")
        metadata.update(status=status, disposable=disposable, closed_utc=now().isoformat())
        save(path, metadata)


def eligible(path: Path, *, root=ROOT, at=None) -> dict:
    path = safe_session(path, root)
    for entry in path.rglob("*"):
        if linked(entry):
            raise ValueError(f"Linked/reparse descendant: {entry}")
    metadata = json.loads((path / "session.json").read_text(encoding="utf-8"))
    retention = metadata.get("retention_days")
    if (metadata.get("schema") != 1 or metadata.get("status") not in {"completed", "failed"}
            or metadata.get("disposable") is not True
            or type(retention) is not int or retention < 0):
        raise ValueError("Session is active, retained, or has invalid metadata")
    closed = datetime.fromisoformat(metadata["closed_utc"])
    if closed.tzinfo is None or (at or now()) < closed + timedelta(days=retention):
        raise ValueError("Retention has not elapsed or closing time has no timezone")
    tracked = subprocess.run(["git", "ls-files", "--", path.relative_to(root.resolve()).as_posix()],
                             cwd=root, check=True, capture_output=True, text=True)
    if tracked.stdout.strip():
        raise ValueError("Session contains tracked files")
    return metadata


def clean(path: Path, *, apply=False, root=ROOT, at=None) -> int:
    path = safe_session(path, root)
    eligible(path, root=root, at=at)
    with session_lock(path):
        eligible(path, root=root, at=at)
        size = sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
        if apply:
            # Keep the lock open while removing contents. Windows cannot remove
            # an open lock file, so remove the empty shell after releasing it.
            for child in path.iterdir():
                if child.name != ".lock":
                    shutil.rmtree(child) if child.is_dir() else child.unlink()
            log = root / "tmp/cleanup.jsonl"
            with log.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"deleted_utc": now().isoformat(),
                                         "session": str(path), "bytes": size}) + "\n")
    if apply:
        # Only lock remains: another cooperating user cannot reopen this
        # session (its session.json has gone). rmdir refuses nonempty paths.
        (path / ".lock").unlink()
        path.rmdir()
    return size


class Tee:
    def __init__(self, console, log):
        self.console, self.log = console, log

    def write(self, value):
        self.console.write(value)
        self.log.write(value)
        return len(value)

    def flush(self):
        self.console.flush()
        self.log.flush()


def run_configured(callback, argv):
    """Smoke config opts into an isolated session; explicit --out-dir opts out."""
    from shared.io.config import load_yaml_config
    args = list(sys.argv[1:] if argv is None else argv)
    if any(value in {"-h", "--help"} for value in args):
        return callback(args)
    config = None
    for index, value in enumerate(args):
        if value == "--config" and index + 1 < len(args):
            config = args[index + 1]
        elif value.startswith("--config="):
            config = value.split("=", 1)[1]
    cfg = load_yaml_config(Path(config)) if config else {}
    if not cfg.get("temporary_session") or any(a in {"--out-dir", "--experiment"} or a.startswith(("--out-dir=", "--experiment=")) for a in args):
        return callback(args)
    if "--resume" in args:
        raise ValueError("Resume smoke with the previous session's explicit --out-dir")
    path = create("smoke", Path(config).stem)
    with session_lock(path):
        metadata = json.loads((path / "session.json").read_text(encoding="utf-8"))
        metadata["command"] = [sys.executable, "-m", "research", *args]
        save(path, metadata)
        (path / "config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        try:
            with (path / "run.log").open("w", encoding="utf-8") as log:
                with redirect_stdout(Tee(sys.stdout, log)), redirect_stderr(Tee(sys.stderr, log)):
                    result = callback([*args, "--out-dir", str(path / "output")])
        except BaseException as error:
            metadata.update(status="failed", disposable=False, closed_utc=now().isoformat(), error=repr(error))
            save(path, metadata)
            raise
        metadata.update(status="completed", disposable=True, closed_utc=now().isoformat())
        save(path, metadata)
    print(f"Smoke session: {path}")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Manage disposable repository sessions")
    sub = parser.add_subparsers(dest="action", required=True)
    new = sub.add_parser("create")
    new.add_argument("category", choices=sorted(CATEGORIES))
    new.add_argument("purpose")
    close = sub.add_parser("close")
    close.add_argument("session", type=Path)
    close.add_argument("--failed", action="store_true")
    close.add_argument("--disposable", action="store_true")
    cleanup = sub.add_parser("clean")
    cleanup.add_argument("--session", type=Path)
    cleanup.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.action == "create":
        print(create(args.category, args.purpose))
    elif args.action == "close":
        finish(args.session, status="failed" if args.failed else "completed", disposable=args.disposable)
    else:
        paths = [args.session] if args.session else [p for category in sorted(CATEGORIES)
                  for p in sorted((ROOT / "tmp" / category).glob("*")) if p.is_dir()]
        for path in paths:
            try:
                size = clean(path, apply=args.apply)
                print(f"{'Deleted' if args.apply else 'Would delete'} {path} ({size} bytes)")
            except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
                print(f"Kept {path}: {error}")
