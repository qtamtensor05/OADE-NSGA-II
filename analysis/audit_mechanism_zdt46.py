"""Independently inspect existing primary records; never execute a solver.

Writes new audited derivatives, leaving original primary/manifest/CSV unchanged.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import platform
import numpy as np
import scipy
from scipy.stats import wilcoxon, rankdata
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'results/experiments/oade_mechanism_zdt46'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(name, rows):
    with (D/'derived'/name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    m = json.loads((D/'manifest.json').read_text())
    paths = [ROOT/'src/research/studies/mechanism_impact.py',
             *sorted((ROOT/'src/oade_nsga2').glob('*.py'))]
    source_mismatches = [p.name for p in paths if m['sources'].get(p.name) != sha(p)]
    assert not source_mismatches, source_mismatches
    files = sorted((D/'primary').glob('*.json'))
    hashes = {p.name: sha(p) for p in files}
    records = [json.loads(p.read_text()) for p in files]
    lookup = {(r['problem'], r['algorithm'], r['seed']): r for r in records}
    expected = {(p, a, s) for p in m['problems'] for a in m['variants']
                for s in range(m['seed_base'], m['seed_base']+m['runs'])}
    assert len(records) == len(lookup) == 480 and set(lookup) == expected
    max_f = max_metric = 0.
    summaries, pairs, effects, activations = [], [], [], []
    for p in m['problems']:
        problem = get_problem(p, n_var=10)
        reference = np.asarray(problem.pareto_front())
        for a in m['variants']:
            group = [lookup[p, a, s] for s in range(42, 72)]
            for r in group:
                x, f = np.asarray(r['final_x']), np.asarray(r['final_f'])
                assert x.shape == (len(f), 10) and f.shape == (len(x), 2)
                assert np.isfinite(x).all() and np.isfinite(f).all()
                assert ((x >= problem.xl) & (x <= problem.xu)).all()
                assert r['valid'] and len(np.unique(f, axis=0)) > 1
                assert not ((f[:, None] <= f[None, :]).all(2) & (f[:, None] < f[None, :]).any(2)).any()
                assert np.array_equal(reference, r['reference'])
                assert 0 < r['n_eval'] <= m['budget'] and r['run_idx'] == r['seed']
                err = float(np.max(abs(problem.evaluate(x)-f)))
                max_f = max(max_f, err)
                assert err < 1e-10
                for metric, value in [('IGD', IGD(reference)(f)), ('HV', HV(ref_point=reference.max(0)+.1)(f))]:
                    err = abs(float(value)-r[metric])
                    max_metric = max(max_metric, err)
                    assert err < 1e-10
                assert r['generations'] == len(r['trace'])
                for e in r['events']:
                    assert e['status'] in ('completed', 'budget_blocked')
                    assert 0 <= e['evaluations'] <= r['n_eval']
                for mech in ('obl', 'restart'):
                    events = [e for e in r['events'] if e['mechanism'] == mech]
                    activations.append(dict(problem=p, algorithm=a, seed=r['seed'], mechanism=mech,
                        activations=sum(e['status']=='completed' for e in events),
                        evaluations=sum(e['evaluations'] for e in events)))
            row = dict(problem=p, algorithm=a, runs=30, valid_runs=sum(r['valid'] for r in group),
                       n_eval_min=min(r['n_eval'] for r in group), n_eval_max=max(r['n_eval'] for r in group))
            for metric in ('IGD', 'HV'):
                v = [r[metric] for r in group]
                row.update({metric+'_mean':float(np.mean(v)), metric+'_sd':float(np.std(v, ddof=1)),
                            metric+'_median':float(np.median(v))})
            summaries.append(row)
            if a == 'full':
                continue
            for metric in ('IGD', 'HV'):
                ref = np.array([lookup[p, 'full', r['seed']][metric] for r in group])
                alt = np.array([r[metric] for r in group])
                delta = ref-alt
                benefit = -delta if metric == 'IGD' else delta
                nz = benefit[benefit != 0]
                ranks = rankdata(abs(nz))
                effect = float(np.sum(ranks*np.sign(nz))/sum(ranks)) if len(nz) else 0.
                stat, pv = (0., 1.) if not np.any(delta) else wilcoxon(delta, zero_method='wilcox', method='auto', alternative='two-sided')
                effects.append(dict(problem=p, metric=metric, comparison_algorithm=a, n_pairs=30,
                    reference_mean=float(ref.mean()), comparison_mean=float(alt.mean()),
                    median_paired_difference=float(np.median(delta)), statistic=float(stat),
                    p_value=float(pv), rank_biserial_effect=effect))
                pairs.extend(dict(problem=p, metric=metric, comparison_algorithm=a, seed=r['seed'],
                    difference=float(d), benefit_full=float(b)) for r,d,b in zip(group,delta,benefit))
    order = sorted(range(28), key=lambda i: effects[i]['p_value'])
    running = 0.
    for rank, i in enumerate(order):
        running = max(running, min(1., (28-rank)*effects[i]['p_value']))
        effects[i]['p_adjusted_holm'] = running
        effects[i]['result'] = ('full_better' if effects[i]['rank_biserial_effect'] > 0 else 'ablation_better') if running < .05 else 'not_significant'
    original = list(csv.DictReader((D/'derived/impact.csv').open()))
    old = {(r['problem'],r['metric'],r['comparison_algorithm']):r for r in original}
    assert len(old) == 28
    for r in effects:
        o = old[r['problem'],r['metric'],r['comparison_algorithm']]
        for k in ('n_pairs','reference_mean','comparison_mean','median_paired_difference','statistic','p_value','rank_biserial_effect','p_adjusted_holm'):
            assert np.isclose(r[k], float(o[k]), rtol=1e-12, atol=1e-14), (r,k,o[k])
        assert r['result'] == o['result'] and int(o['excluded_pairs']) == 0
    raw = list(csv.DictReader((D/'derived/runs.csv').open()))
    assert len(raw) == 480
    for r in raw:
        primary = lookup[r['problem'],r['algorithm'],int(r['seed'])]
        for k in ('IGD','HV','n_eval','runtime_seconds','generations','collapse_checks'):
            assert float(r[k]) == primary[k]
        assert r['valid'].lower() == str(primary['valid']).lower()
    # These checksums establish an audit-time inventory, not execution-time provenance.
    assert hashes == {p.name:sha(p) for p in files}
    write('audited_summary.csv', summaries)
    write('audited_impact.csv', effects)
    write('audited_pairs.csv', pairs)
    write('audited_activation.csv', activations)
    audit = dict(records=480, valid_runs=480, comparison_rows_verified=28,
        source_files_verified=len(paths), max_objective_error=max_f, max_metric_error=max_metric,
        results=dict(Counter(r['result'] for r in effects)), total_evaluations=sum(r['n_eval'] for r in records),
        manifest_sha256=sha(D/'manifest.json'), primary_sha256=hashes,
        provenance_boundary='Manifest has source hashes but no execution-time primary checksums, environment or initial-population hashes. Audit-time hashes do not establish historical immutability.',
        environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))
    (D/'derived/audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='primary_sha256'},indent=2))


if __name__ == '__main__':
    main()
