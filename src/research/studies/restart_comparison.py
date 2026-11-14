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

from research.oade_nsga2.runner import run_instrumented
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
    for key,value in {'probability_update_mode':'success_rate','enable_probability_adaptation':True,
                      'enable_obl':True,'enable_fcr_adaptation':True,'enable_neighborhood':True}.items():
        common.setdefault(key,value)
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

    spec = AlgorithmSpec(candidate['id'], 'local_oade_research',
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
    previous = 0.
    ordered = sorted([r for r in paired if r['p_raw'] is not None],key=lambda r:r['p_raw'])
    for i,row in enumerate(ordered):
        previous = max(previous,min(1.,(len(paired)-i)*row['p_raw']))
        row['p_holm_all_endpoints'] = previous
    for row in paired:
        row.setdefault('p_holm_all_endpoints',None)
        row['interpretation_all_endpoints'] = ('no_valid_pairs' if row['p_holm_all_endpoints'] is None else
                                               'difference_detected' if row['p_holm_all_endpoints']<.05 else 'no_difference_detected')
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
    probability_trace = [{k:r[k] for k in ('candidate','problem','seed')} | t for r in rows for t in r['probability_trace']]
    write_csv(derived/'probability_trace.csv',probability_trace,
              ['candidate','problem','seed','generation','n_eval','mode','enabled','n_de','n_sbx','success_de','success_sbx','target','prob_before','prob_after'])
    injection_trace = [{k:r[k] for k in ('candidate','problem','seed')} | t for r in rows for t in r['diversity_events']]
    write_csv(derived/'diversity_events.csv',injection_trace,
              ['candidate','problem','seed','generation','generation_index','n_eval_before','status','candidates','generation_completed','retained','n_eval_after','evaluations'])
    summaries = []
    text = ['# Đối chứng không restart, classic và adaptive', '',
            f'Tổng run: **{len(rows)}**; invalid: **{sum(not r["valid"] for r in rows)}**.',
            '**SMOKE: chỉ kiểm tra pipeline, không phải bằng chứng cải thiện.**' if cfg.get('smoke') else 'Đối chứng ghép seed trên ZDT.', '',
            'Cả ba nhánh dùng cùng uniform initial population, success-rate, OBL định kỳ, adaptation F/CR và neighborhood. Chỉ thay toàn bộ chính sách restart.', '',
            '| Bài | Nhánh | Valid/run | IGD median ↓ | HV median ↑ | Restart bắt đầu / hoàn tất | Evaluation restart |',
            '|:---|:---|---:|---:|---:|---:|---:|']
    for p in cfg['problems']:
        for c in candidates:
            group = [r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']]
            valid = [r for r in group if r['valid']]
            med = lambda m: f'{np.median([r[m] for r in valid]):.6g}' if valid else 'NA'
            totals = {k:sum(r['telemetry'][k] for r in group) for k in ('restart_attempts','restart_completed','restart_evaluations')}
            summary = {'problem':p['name'],'variant':c['id'],'runs':len(group),'valid_runs':len(valid),**totals}
            for key in ('trigger_checks','stagnation_eligible','collapse_checks','collapse_positive','restart_budget_blocked',
                        'injection_attempts','injection_evaluations'):
                summary[key] = sum(r['telemetry'][key] for r in group)
            summary['runs_with_restart'] = sum(r['telemetry']['restart_attempts']>0 for r in group)
            summary['adaptive_healthy_rejections'] = summary['collapse_checks']-summary['collapse_positive']
            for metric in ('IGD','HV','runtime_seconds','n_eval','final_prob_de','restart_per_100_checks','restart_evaluation_fraction'):
                values = [r[metric] for r in (valid if metric in {'IGD','HV'} else group)]
                for label,fn in [('mean',np.mean),('median',np.median),('sd',lambda v:np.std(v,ddof=1) if len(v)>1 else 0.),
                                 ('q25',lambda v:np.quantile(v,.25)),('q75',lambda v:np.quantile(v,.75))]:
                    summary[metric+'_'+label] = float(fn(values)) if values else None
            summaries.append(summary)
            text.append(f'| {p["name"]} | {c["id"]} | {len(valid)} / {len(group)} | {med("IGD")} | {med("HV")} | {totals["restart_attempts"]} / {totals["restart_completed"]} | {totals["restart_evaluations"]} |')
    write_csv(derived/'summary.csv',summaries,list(summaries[0]))
    text += ['', '## Các chính sách được đo', '',
             '| Nhánh | Điều kiện kích hoạt | Cách làm mới |',
             '|:---|:---|:---|',
             '| Không restart | Không kích hoạt | Chỉ theo dõi stagnation, không tốn RNG/evaluation restart |',
             '| Classic | Đủ patience stagnation | Giữ 30% elite, sinh uniform phần còn lại, reset F/CR về 0,5 |',
             '| Adaptive | Đủ patience và diversity collapse | Giữ ít nhất 80% elite, sinh OBL/Gauss, kéo F/CR về 0,5 |','',
             'Theo mã hiện có, stagnation đo độ lớn thay đổi ideal point giữa hai thế hệ (chuẩn Euclid), không phải điều kiện cải thiện đơn điệu từng mục tiêu. Nếu thay đổi dưới tolerance thì tăng counter; đủ patience mới xét restart. Adaptive coi collapse khi objective range lớn nhất < 0,001 hoặc max std của biến quyết định chuẩn hóa < diversity_threshold. Nếu diversity khỏe, counter giảm về patience//2, không restart.',
             '## Đọc đối chứng', '',
             'comparisons.csv chứa đủ classic–adaptive, classic–no_restart và adaptive–no_restart; delta = a − b. IGD thấp hơn tốt, HV cao hơn tốt. Wilcoxon signed-rank hai phía, zero_method=wilcox, xấp xỉ chuẩn; toàn delta zero đặt p=1. Cột p_holm giữ họ ba cặp/bài/metric; p_holm_all_endpoints hiệu chỉnh đồng thời mọi bài × 2 metric × 3 cặp (30 endpoint khi chạy đủ ZDT), alpha=0,05. Invalid được giữ và đếm, loại riêng khỏi cặp chất lượng. Không phát hiện khác biệt không chứng minh tương đương.',
             'summary.csv ghi số lần đủ stagnation, số xét collapse/dương tính/từ chối do diversity khỏe, số run có restart, tần suất, chi phí và chất lượng mean/SD/median/Q25/Q75. restart_events.csv ghi generation, evaluations trước/sau, trạng thái và IGD/HV tức thời trước/sau restart.',
             'Nếu adaptive không trigger và trùng no-restart, không có bằng chứng về lợi ích của restart đã kích hoạt. Classic kém no-restart không tự chứng minh adaptive chủ động cải thiện. Đây là đối chứng toàn bộ chính sách restart, không tách riêng gate, elite ratio, kernel và F/CR reset.',
             'Cùng cap tổng, gồm khởi tạo, OBL định kỳ và restart; batch nguyên tử có thể để dư nên phải xem n_eval. Convergence dùng mốc observation thực, không nội suy. Tác động trước/sau event chỉ là mô tả tức thời, chưa chứng minh lợi ích cuối.',
             'Primary JSON lưu X/F đầu và cuối, hash quần thể đầu, các event và probability trace. Manifest chụp source/environment/reference và kiểm tra resume; writer có bounded retry cho lỗi Windows tạm thời. Giữ dữ liệu nếu lỗi checkpoint kéo dài, không xóa primary để ép resume.', '']
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
