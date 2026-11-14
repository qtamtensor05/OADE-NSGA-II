"""Paired restart ablation with event evidence and fail-closed checkpoints."""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from pymoo.problems import get_problem
from scipy.stats import wilcoxon

from oade_nsga2.runner import run_instrumented
from shared.contracts import AlgorithmSpec
from shared.evaluation import validate_result
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv
from shared.population import make_initial_population
from shared.paths import ROOT, repository_path
from shared.fronts import non_dominated_xy
from research.benchmarking.convergence import ConvergenceRecorder
from research.benchmarking.provenance import digest
from research.maintenance.tmp_sessions import session_lock
from . import zdt_sensitivity as engine


def design(cfg):
    cfg = json.loads(json.dumps(cfg))
    g = cfg['global']
    if (not g['seeds'] or len(set(g['seeds'])) != len(g['seeds'])
            or any(type(s) is not int or s < 0 for s in g['seeds'])
            or g['pop_size'] < 10 or g['evaluation_budget'] <= g['pop_size']):
        raise ValueError('Require unique nonnegative seeds, population >=10 and budget > population')
    names = [p['name'] for p in cfg['problems']]
    if not names or len(set(names)) != len(names) or any(n not in {'zdt1','zdt2','zdt3','zdt4','zdt6'} for n in names):
        raise ValueError('This protocol supports unique ZDT1/2/3/4/6 problems')
    common = cfg['common_settings']
    if set(common) & {'restart_mode', 'enable_restart', 'restart_elite_ratio'}:
        raise ValueError('Restart switches belong to the fixed variants')
    if common['stagnation_patience'] < 1:
        raise ValueError('Patience must be positive')
    variants = [('classic', True, 'classic', .30), ('adaptive', True, 'adaptive', .80),
                ('no_restart', False, 'classic', .30)]
    candidates = [dict(id=name, parameter='restart', level=name,
                       settings={**common, 'pop_size': g['pop_size'], 'enable_restart': enabled,
                                 'restart_mode': mode, 'restart_elite_ratio': ratio})
                  for name, enabled, mode, ratio in variants]
    return cfg, candidates


def run_task(cfg, candidate, problem_cfg, seed):
    problem = get_problem(problem_cfg['name'], n_var=problem_cfg['n_var'])
    front = np.asarray(cfg['reference_fronts'][problem_cfg['name']])
    igd, hv = IGD(front), HV(ref_point=np.max(front, axis=0) + .1)
    budget, pop = cfg['global']['evaluation_budget'], cfg['global']['pop_size']
    initial = make_initial_population(problem, pop, seed)

    def metrics(f):
        _, nd = non_dominated_xy(np.zeros((len(f), 1)), f)
        return {'IGD': float(igd(nd)), 'HV': float(hv(nd))}

    spec = AlgorithmSpec(candidate['id'], 'local_oade',
                         {k: v for k, v in candidate['settings'].items() if k != 'pop_size'})
    outcome, observed = run_instrumented(spec, problem, pop, budget, initial, seed,
                                        ConvergenceRecorder(budget, igd, hv), restart_metric=metrics)
    validation = validate_result(outcome.x, outcome.f, problem)
    quality = metrics(outcome.f)
    valid = validation.valid and all(np.isfinite(v) for v in quality.values())
    t = observed['telemetry']
    return {'candidate': candidate['id'], 'parameter': candidate['parameter'], 'level': candidate['id'],
            'problem': problem_cfg['name'], 'n_var': problem_cfg['n_var'], 'seed': seed,
            'settings': candidate['settings'], 'evaluation_budget': budget, 'n_eval': outcome.n_eval,
            'valid': valid, 'validation_status': validation.status, 'front_size': validation.front_size,
            **(quality if valid else {'IGD': None, 'HV': None}),
            'runtime_seconds': outcome.runtime_seconds, 'reference_sha256': digest(front.tolist()),
            'initial_x_sha256': digest(initial.tolist()), 'final_x': outcome.x.tolist(),
            'final_f': outcome.f.tolist(), 'convergence': list(outcome.convergence), **observed,
            'restart_per_100_checks': 100*t['restart_attempts']/max(1,t['trigger_checks']),
            'restart_evaluation_fraction': t['restart_evaluations']/outcome.n_eval}


def comparisons(cfg, candidates, rows, *, require_same_initial=True):
    output = []
    for problem in cfg['problems']:
        for metric in ('IGD', 'HV'):
            family = []
            for a, b in combinations([c['id'] for c in candidates], 2):
                left = {r['seed']: r for r in rows if r['candidate'] == a and r['problem'] == problem['name']}
                right = {r['seed']: r for r in rows if r['candidate'] == b and r['problem'] == problem['name']}
                pairs = [(left[s], right[s]) for s in sorted(left.keys() & right.keys())
                         if left[s]['valid'] and right[s]['valid']]
                if require_same_initial and any(x['initial_x_sha256'] != y['initial_x_sha256'] for x, y in pairs):
                    raise ValueError('Paired initialization mismatch')
                delta = np.array([x[metric]-y[metric] for x,y in pairs])
                p = float(wilcoxon(delta, zero_method='wilcox', alternative='two-sided', method='approx').pvalue) if np.any(delta) else 1.0
                family.append({'problem': problem['name'], 'metric': metric, 'a': a, 'b': b,
                               'n_pairs': len(pairs), 'excluded_pairs': len(left)-len(pairs),
                               'median_paired_delta_a_minus_b': float(np.median(delta)) if len(delta) else None,
                               'p_raw': p if len(delta) else None,
                               'identical_final_f_pairs': sum(x['final_f'] == y['final_f'] for x,y in pairs),
                               'both_zero_restart_pairs': sum(x['telemetry']['restart_attempts'] == y['telemetry']['restart_attempts'] == 0 for x,y in pairs)})
            ordered = sorted([r for r in family if r['p_raw'] is not None], key=lambda r:r['p_raw'])
            previous = 0.
            for i, r in enumerate(ordered):
                previous = max(previous, min(1., (len(family)-i)*r['p_raw']))
                r['p_holm'] = previous
            for r in family:
                r.setdefault('p_holm', None)
                r['interpretation'] = ('no_valid_pairs' if r['p_holm'] is None else
                                       'difference_detected' if r['p_holm'] < .05 else 'no_difference_detected')
            output.extend(family)
    return output


def write_outputs(directory, manifest, cfg, candidates):
    rows = engine.load_records(directory, manifest)
    engine.validate_records(cfg, candidates, rows, complete=True)
    derived = directory / 'derived'
    derived.mkdir(exist_ok=True)
    scalar = [{k:v for k,v in r.items() if not isinstance(v,(dict,list))} | r['telemetry'] for r in rows]
    write_csv(derived/'raw_runs.csv', scalar, list(scalar[0]))
    paired = comparisons(cfg, candidates, rows)
    write_csv(derived/'comparisons.csv', paired, list(paired[0]))
    events = []
    for r in rows:
        for e in r['restart_events']:
            events.append({k:r[k] for k in ('candidate','problem','seed')} |
                          {k:v for k,v in e.items() if k not in {'before','after'}} |
                          {f'{when}_{m}':e[when][m] for when in ('before','after') for m in ('IGD','HV')})
    fields = ['candidate','problem','seed','mode','generation','n_eval_before','status','n_eval_after','evaluations','before_IGD','before_HV','after_IGD','after_HV']
    write_csv(derived/'restart_events.csv', events, fields)
    trace = [{k:r[k] for k in ('candidate','problem','seed')} | c for r in rows for c in r['convergence']]
    write_csv(derived/'convergence.csv', trace, ['candidate','problem','seed','checkpoint_fraction','target_evaluations','n_eval','IGD','HV'])
    text = ['# Restart comparison', '', f'Runs: {len(rows)}; invalid: {sum(not r["valid"] for r in rows)}.',
            'SMOKE: pipeline validation only.' if cfg.get('smoke') else 'Paired seed-controlled ablation.', '',
            '| Problem | Variant | Valid / runs | Median IGD | Median HV | Restarts attempted / completed | Restart evaluations |',
            '|---|---|---:|---:|---:|---:|---:|']
    for p in cfg['problems']:
        for c in candidates:
            group = [r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']]
            valid = [r for r in group if r['valid']]
            med = lambda m: f'{np.median([r[m] for r in valid]):.6g}' if valid else 'NA'
            totals = {k:sum(r['telemetry'][k] for r in group) for k in ('restart_attempts','restart_completed','restart_evaluations')}
            text.append(f'| {p["name"]} | {c["id"]} | {len(valid)} / {len(group)} | {med("IGD")} | {med("HV")} | {totals["restart_attempts"]} / {totals["restart_completed"]} | {totals["restart_evaluations"]} |')
    text += ['', 'See comparisons.csv for all three paired comparisons. IGD lower / HV higher is better.',
             'Two-sided paired Wilcoxon signed-rank, zero_method=wilcox, normal approximation; all-zero differences p=1. Holm family: three pairs per problem and metric, alpha=0.05. Invalid pairs excluded and counted. No detected difference is not equivalence.',
             'Classic keeps 30% elite, uses uniform immigrants and resets F/CR. Adaptive keeps >=80%, uses OBL/Gaussian immigrants and shrinks F/CR toward 0.5. These are whole restart policies, not an isolated diversity-gate comparison.',
             'No-restart retains stagnation monitoring but performs no restart or extra random draws. Zero-restart identical pairs provide no evidence of restart benefit.',
             'Event before/after changes are descriptive immediate effects, not proof of lasting benefit. Do not infer causality from trigger frequency correlations. Use paired no-restart final quality and event timing together.',
             'All objective calls, including restart, count toward the strict cap. Atomic batches may leave unused budget; inspect n_eval. Convergence checkpoints record actual n_eval and may overshoot targets; no interpolation.',
             'Primary JSON preserves final X/F, initial population hash, events, convergence and validity. Manifest captures sources/environment/references and checks resume integrity.', '']
    (derived/'report.md').write_text('\n'.join(text), encoding='utf-8')


def main(argv=None, *, default_config='config/studies/restart_comparison.yaml',
         design_fn=None, output_writer=None, study_kind='restart_comparison_v1', task_runner=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=default_config)
    parser.add_argument('--stage', choices=('plan','run','report'), default='plan')
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--jobs', type=int)
    args = parser.parse_args(argv)
    cfg, candidates = (design_fn or design)(load_yaml_config(Path(args.config)))
    if args.stage == 'plan':
        print(json.dumps({'runs':len(engine.tasks(cfg,candidates)), 'variants':candidates,
                          'evaluation_cap':cfg['global']['evaluation_budget']}, indent=2))
        return
    jobs = args.jobs if args.jobs is not None else cfg['global'].get('jobs',1)
    if jobs < 1 or args.stage == 'report' and not args.resume:
        raise ValueError('Positive jobs required; report requires --resume')
    directory = (args.out_dir or repository_path(cfg['global']['out_dir'])).resolve()
    lock = ROOT/'tmp/study_locks'/digest(str(directory))
    lock.mkdir(parents=True, exist_ok=True)
    with session_lock(lock):
        current = engine.identity(cfg,candidates)
        current['kind'] = study_kind
        manifest = engine.open_study(directory,current,args.resume)
        cfg = {**cfg,'reference_fronts':engine.reference_fronts(directory,manifest,cfg)}
        if args.stage == 'run':
            engine.execute(directory,manifest,cfg,candidates,jobs,task_runner=task_runner or run_task)
        (output_writer or write_outputs)(directory,manifest,cfg,candidates)
    print(f'Results: {directory}')


if __name__ == '__main__':
    main()
