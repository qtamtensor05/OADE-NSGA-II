"""Commit the prepared CSV bundles and per-problem reports from a local terminal.

Keeps extracted CSVs on disk; removes only their Git index entries.
Does not push or modify Git history.
"""
from pathlib import Path
import subprocess
from csv_archives import ROOT, catalog, verify


def git(*args, capture=False):
    return subprocess.run(['git', *args], cwd=ROOT, check=True,
                          capture_output=capture, text=True)


def main():
    count = verify()
    data = catalog()
    archived = {f['path'] for a in data['archives'] for f in a['files']}
    tracked = git('ls-files', '-z', 'results', capture=True).stdout.split('\0')
    csvs = [p for p in tracked if p.endswith('.csv')]
    if not set(csvs) <= archived:
        raise ValueError('Some tracked CSVs are not archived; stopping before staging.')
    paths = ['.gitignore', 'README.md', 'README.vi.md', 'docs/index.md',
             'docs/reports/zdt_parameter_sensitivity_report.md',
             'results/by_problem', 'results/CSV_DOWNLOADS.md', 'results/csv_archives.json',
             'scripts/csv_archives.py', 'scripts/commit_csv_results.py',
             'scripts/organize_by_problem.py', 'scripts/problem_reports.py',
             'tests/unit/test_csv_archives.py',
             *[a['archive'] for a in data['archives']]]
    staged = git('diff', '--cached', '--name-only', '-z', capture=True).stdout.split('\0')
    allowed = [*paths, *csvs]
    unrelated = [p for p in staged if p and not any(p == a or p.startswith(a + '/') for a in allowed)]
    if unrelated:
        raise ValueError(f'Unrelated changes already staged; commit them separately first: {unrelated}')
    if csvs:
        git('rm', '--cached', '--', *csvs, capture=True)
    git('add', '--', *paths)
    git('diff', '--cached', '--check')
    git('commit', '-m', 'Organize per-problem reports and distribute CSV evidence as verified ZIP bundles')
    print(f'Committed {count} archived CSVs and per-problem reports. Local extracted CSVs retained.')


if __name__ == '__main__':
    try:
        main()
    except (subprocess.CalledProcessError, ValueError) as error:
        raise SystemExit(str(error)) from None
