"""Check new/changed source placement and maintained Markdown file links."""
from __future__ import annotations
import argparse
import ast
from pathlib import Path
import re
import subprocess

from shared.paths import ROOT

ALGORITHM_PACKAGES = {"oade_nsga2", "nsga2", "rnsga2", "dnsga2", "cgde_nsga2", "nsga2_sdr_ols", "ce_moea"}


def check_source_boundaries(source_root=ROOT / "src") -> list[str]:
    errors = []
    for path in source_root.rglob("*.py"):
        package = path.relative_to(source_root).parts[0]
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules = [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else [a.name for a in node.names] if isinstance(node, ast.Import) else []
            for module in modules:
                top = module.split(".", 1)[0]
                if package in ALGORITHM_PACKAGES | {"shared"} and top == "research":
                    errors.append(f"Algorithm/shared code must not depend on research: {path}:{node.lineno}")
                if package in ALGORITHM_PACKAGES and top in ALGORITHM_PACKAGES - {package}:
                    errors.append(f"Algorithm must not import another algorithm's implementation: {path}:{node.lineno}")
                if module.startswith("pymoo.algorithms.") and package not in ALGORITHM_PACKAGES:
                    errors.append(f"Concrete pymoo solver must be selected in its algorithm package: {path}:{node.lineno}")
    return errors


def changed_files():
    paths = set()
    for command in (["git", "diff", "HEAD", "--name-only", "--diff-filter=ACMR", "-z"],
                    ["git", "ls-files", "--others", "--exclude-standard", "-z"]):
        result = subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
        paths.update(p.decode("utf-8") for p in result.stdout.split(b"\0") if p)
    return sorted(paths)


def check() -> list[str]:
    errors = check_source_boundaries()
    for name in changed_files():
        path = Path(name)
        if path.parts[0] in {"tmp", "scratch"}:
            errors.append(f"Disposable content must not be tracked: {name}")
        if len(path.parts) == 1 and path.suffix == ".log":
            errors.append(f"Root log must be in a session/execution: {name}")
        if path.parts[0] == "scripts" and re.match(r"(?:probe|merge|repair)_", path.name):
            errors.append(f"One-off script belongs in tmp; retain research recipes in analysis: {name}")
        if path.parts[0] == "results" and (path.name.startswith("smoke") or any(p.startswith("smoke") for p in path.parts)):
            errors.append(f"Smoke output must be under tmp/smoke: {name}")
        if path.suffix == ".py" and (ROOT / path).is_file():
            if not re.fullmatch(r"[a-z_][a-z0-9_]*\.py", path.name):
                errors.append(f"Python filename must use snake_case: {name}")
            tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules = [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else [a.name for a in node.names] if isinstance(node, ast.Import) else []
                if any(m == "src" or m.startswith("src.") or m == "algorithms" or m.startswith("algorithms.") for m in modules):
                    errors.append(f"Use installed top-level packages, not src/algorithms wrappers: {name}:{node.lineno}")
    documents = [ROOT / "README.md", ROOT / "README.vi.md", *(ROOT / "docs").rglob("*.md")]
    for document in documents:
        if document.name == "project_structure_proposal.md":
            continue # dated audit intentionally describes pre-migration paths
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            filename = target.split("#", 1)[0]
            if filename and not (document.parent / filename).exists():
                errors.append(f"Broken link in {document.relative_to(ROOT)}: {target}")
    return errors


def main(argv=None):
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    errors = check()
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print("Structure and maintained documentation links passed.")
