"""Audit completed OFAT evidence and export within-seed changes; never run solvers."""
import csv
import json
from pathlib import Path

import numpy as np

from research.studies.zdt_sensitivity import (
    identity, load_records, open_study, reference_fronts, validate_records,
)
from research.studies.zdt_sensitivity_analysis import analyze
from research.studies.zdt_sensitivity_design import design
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv


def main():
    cfg, candidates = design(load_yaml_config(Path('config/studies/zdt_sensitivity.yaml')))
    directory = Path(cfg['global']['out_dir'])
    manifest = open_study(directory, identity(cfg, candidates), True)
    cfg = {**cfg, 'reference_fronts': reference_fronts(directory, manifest, cfg)}
    records = load_records(directory, manifest)
    validate_records(cfg, candidates, records, complete=True)
    summaries, comparisons = analyze(cfg, candidates, records)
    # Independently compare regenerated quantities with the delivered CSVs.
    for name, expected in [('summary.csv', summaries), ('comparisons.csv', comparisons)]:
        with (directory / 'derived' / name).open(encoding='utf-8', newline='') as handle:
            actual = list(csv.DictReader(handle))
        assert len(actual) == len(expected)
        for row, check in zip(actual, expected):
            for key, value in check.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    assert np.isclose(float(row[key]), value, rtol=1e-12, atol=1e-15), (name, key)
                else:
                    assert row[key] == ('' if value is None else str(value)), (name, key)
    baseline = {(r['problem'], r['seed']): r for r in records if r['candidate'] == 'baseline'}
    paired, diagnostics = [], []
    for candidate in candidates:
        if candidate['id'] == 'baseline':
            continue
        for problem in cfg['problems']:
            group = [r for r in records if r['candidate'] == candidate['id'] and r['problem'] == problem['name']]
            diagnostics.append({
                'parameter': candidate['parameter'], 'level': candidate['level'], 'problem': problem['name'],
                'runs': len(group), 'exact_same_IGD_HV': sum(
                    all(r[m] == baseline[r['problem'], r['seed']][m] for m in ('IGD', 'HV')) for r in group),
                'runs_with_restart': sum(r['telemetry']['restart_completed'] > 0 for r in group),
                'restart_completed': sum(r['telemetry']['restart_completed'] for r in group),
                'zero_HV_runs': sum(r['HV'] == 0 for r in group),
            })
            for row in group:
                base = baseline[row['problem'], row['seed']]
                for metric in ('IGD', 'HV', 'runtime_seconds'):
                    valid = metric == 'runtime_seconds' or row['valid'] and base['valid']
                    delta = row[metric] - base[metric] if valid else None
                    paired.append({'parameter': candidate['parameter'], 'level': candidate['level'],
                                   'baseline_level': cfg['baseline_settings'][candidate['parameter']],
                                   'problem': row['problem'], 'seed': row['seed'], 'metric': metric,
                                   'valid_pair': valid, 'baseline_value': base[metric], 'level_value': row[metric],
                                   'absolute_change': delta,
                                   'percent_change': 100 * delta / abs(base[metric]) if valid and base[metric] != 0 else None})
    for name, rows in [('paired_seed_changes.csv', paired), ('response_diagnostics.csv', diagnostics)]:
        write_csv(directory / 'derived' / name, rows, list(rows[0]))
    audit = {'status': 'PASS', 'primary_checksums_verified': len(records), 'complete_unique_tasks': len(records),
             'valid': sum(r['valid'] for r in records), 'invalid': sum(not r['valid'] for r in records),
             'configurations': len(candidates), 'seeds_per_problem_configuration': len(cfg['global']['seeds']),
             'n_eval_min': min(r['n_eval'] for r in records), 'n_eval_max': max(r['n_eval'] for r in records),
             'workers': manifest['workers'], 'derived_tables_recomputed_and_matched': True,
             'paired_rows': len(paired), 'excluded_primary_rows': 0,
             'statistics': 'descriptive OFAT; no composite scores, tests or automatic selection',
             'runtime_caveat': 'Concurrent observational timings; not an isolated speed benchmark.'}
    (directory / 'derived/analysis_audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
