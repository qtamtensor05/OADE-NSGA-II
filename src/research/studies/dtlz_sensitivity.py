"""DTLZ1-4 OFAT parameter lists, objective-aware checkpoints and direct responses."""
from copy import deepcopy
from contextlib import redirect_stdout, redirect_stderr
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

from oade_nsga2.runner import run_instrumented
from shared.contracts import AlgorithmSpec
from shared.evaluation import validate_result
from shared.population import make_initial_population
from shared.paths import ROOT, repository_path
from shared.io.config import load_yaml_config
from research.benchmarking.convergence import ConvergenceRecorder
from research.benchmarking.runner import reference_front
from research.benchmarking.provenance import file_hash, digest
from research.maintenance.tmp_sessions import create, finish, session_lock, Tee
from . import zdt_sensitivity as engine
from .zdt_sensitivity_design import design as parameter_design, plan
from .zdt_sensitivity_analysis import report as response_report

DEFAULT_CONFIG = 'config/studies/dtlz_sensitivity.yaml'


def design(config):
    original = deepcopy(config)
    problems = original['problems']
    if not problems:
        raise ValueError('DTLZ problems must be present')
    normalized = []
    for p in problems:
        if (set(p) != {'name', 'n_obj', 'n_var'} or p['name'] not in {'dtlz1', 'dtlz2', 'dtlz3', 'dtlz4'}
                or type(p['n_obj']) is not int or p['n_obj'] not in {2, 3, 5}
                or type(p['n_var']) is not int or p['n_var'] <= p['n_obj']):
            raise ValueError('Use DTLZ1-4, M=2/3/5 and explicit n_var > M')
        normalized.append({**p, 'problem_name': p['name'], 'name': f"{p['name']}_m{p['n_obj']}"})
    if len({p['name'] for p in normalized}) != len(normalized):
        raise ValueError('Duplicate DTLZ problem/objective case')
    # Reuse the existing parameter-list contract independently of suite geometry.
    original['problems'] = [{'name': 'zdt1', 'n_var': 30}]
    cfg, candidates = parameter_design(original)
    cfg['problems'] = normalized
    return cfg, candidates


def identity(cfg, candidates):
    result = engine.identity(cfg, candidates)
    result['kind'] = 'dtlz_ofat_execution'
    result['source_hashes']['analysis/figures/plot_dtlz_sensitivity.R'] = file_hash(ROOT / 'analysis/figures/plot_dtlz_sensitivity.R')
    return result


def reference_fronts(directory, manifest, cfg):
    path = directory / 'config/reference_fronts.json'
    if manifest['reference_sha256']:
        if not path.is_file() or file_hash(path) != manifest['reference_sha256']:
            raise ValueError('DTLZ reference snapshot checksum mismatch')
        fronts = json.loads(path.read_text(encoding='utf-8'))
    else:
        if path.exists():
            raise ValueError('Uncommitted reference snapshot')
        fronts = {}
        for p in cfg['problems']:
            problem = get_problem(p['problem_name'], n_var=p['n_var'], n_obj=p['n_obj'])
            fronts[p['name']] = reference_front(problem, {**p, 'name': p['problem_name']}).tolist()
        engine.atomic_json(path, fronts)
        manifest['reference_sha256'] = file_hash(path)
        engine.atomic_json(directory / 'study_manifest.json', manifest)
    if set(fronts) != {p['name'] for p in cfg['problems']}:
        raise ValueError('Reference cases do not match configured objective dimensions')
    for p in cfg['problems']:
        f = np.asarray(fronts[p['name']], dtype=float)
        if f.ndim != 2 or f.shape[1] != p['n_obj'] or not len(f) or not np.all(np.isfinite(f)):
            raise ValueError('Invalid DTLZ reference front')
    return fronts


def run_task(cfg, candidate, p, seed):
    settings = candidate['settings']
    problem = get_problem(p['problem_name'], n_var=p['n_var'], n_obj=p['n_obj'])
    front = np.asarray(cfg['reference_fronts'][p['name']])
    igd, hv = IGD(front), HV(ref_point=np.max(front, axis=0) + .1)
    budget = cfg['global']['evaluation_budget']
    spec = AlgorithmSpec(name='OADE_NSGAII', runner='local_oade', params={k: v for k, v in settings.items() if k != 'pop_size'})
    outcome, observed = run_instrumented(spec, problem, settings['pop_size'], budget,
        make_initial_population(problem, settings['pop_size'], seed), seed, ConvergenceRecorder(budget, igd, hv))
    validation = validate_result(outcome.x, outcome.f, problem, expected_objectives=p['n_obj'])
    valid = validation.valid and 0 < outcome.n_eval <= budget
    a, b = (float(igd(outcome.f)), float(hv(outcome.f))) if valid else (None, None)
    if valid and not (np.isfinite(a) and np.isfinite(b)):
        valid, a, b = False, None, None
    return {'candidate': candidate['id'], 'parameter': candidate['parameter'], 'level': candidate['level'],
            'problem': p['name'], 'problem_name': p['problem_name'], 'n_obj': p['n_obj'], 'n_var': p['n_var'],
            'seed': seed, 'settings': settings, 'evaluation_budget': budget, 'n_eval': outcome.n_eval,
            'valid': valid, 'validation_status': validation.status if validation.valid == valid else 'invalid_metric_or_budget',
            'front_size': validation.front_size, 'IGD': a, 'HV': b, 'runtime_seconds': outcome.runtime_seconds,
            'reference_sha256': digest(front.tolist()), 'convergence': list(outcome.convergence), **observed}


def report(cfg, candidates, rows, summaries, comparisons):
    text = response_report(cfg, candidates, rows, summaries, comparisons).replace('trên ZDT', 'trên DTLZ1–4')
    text = text.split('## Cách diễn giải')[0]
    for parameter in cfg['parameters']:
        images = '\n\n'.join(f'![{parameter}, M={m}](../figures/{parameter}_m{m}.png)' for m in sorted({p['n_obj'] for p in cfg['problems']}))
        text = text.replace(f'![Đáp ứng {parameter}](../figures/{parameter}.png)', images)
    return text + ('\n## Phương pháp tổng hợp\n\nMỗi nhãn DTLZx_My là một trường hợp riêng. '
        'IGD/HV: median và Q25–Q75 qua các seed hợp lệ; bảng chênh lệch dùng cặp seed đều hợp lệ. '
        'Invalid được giữ trong dữ liệu gốc và số đếm. Q25–Q75 không phải khoảng tin cậy. '
        'Không so sánh HV tuyệt đối giữa số mục tiêu khác nhau. Baseline được tái sử dụng, không tạo thêm replicate. '
        'Runtime là số đo quan sát khi chạy song song. Không thực hiện kiểm định, chấm điểm hoặc chọn cấu hình tự động.\n')


def plot_outputs(directory):
    executable, env = engine.r_runtime()
    env['DTLZ_SENSITIVITY_DIR'] = str(directory)
    code = 'Sys.setlocale("LC_CTYPE","English_United States.utf8"); ' if os.name == 'nt' else ''
    result = subprocess.run([executable, '--vanilla', '-e', code + 'source("analysis/figures/plot_dtlz_sensitivity.R",encoding="UTF-8")'],
                            cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(result.stdout)
    if result.returncode:
        raise RuntimeError('DTLZ plot failed; primary measurements preserved. ' + result.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=DEFAULT_CONFIG)
    parser.add_argument('--stage', choices=('plan', 'run', 'report', 'plot', 'all'), default='plan')
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--jobs', type=int)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args(argv)
    cfg, candidates = design(load_yaml_config(Path(args.config)))
    if args.stage == 'plan':
        print(json.dumps(plan(cfg, candidates), indent=2)); return
    jobs = args.jobs if args.jobs is not None else cfg['global'].get('jobs', 1)
    if jobs < 1:
        raise ValueError('Workers must be positive')
    if args.stage in {'report', 'plot'} and not args.resume:
        raise ValueError('Existing measurements require --resume')
    if args.stage in {'plot', 'all'}:
        engine.check_plot_runtime()
    session = create('smoke', 'dtlz_ofat') if cfg.get('smoke') and args.out_dir is None else None
    if session and args.resume:
        finish(session, status='failed', disposable=True)
        raise ValueError('Resume smoke using its explicit output directory')
    directory = (args.out_dir or (session / 'output' if session else repository_path(cfg['global']['out_dir']))).resolve()
    lock = session or ROOT / 'tmp/study_locks' / digest(str(directory))
    lock.mkdir(parents=True, exist_ok=True)
    try:
        with session_lock(lock):
            current = identity(cfg, candidates)
            current.update(workers=jobs, invocation=[sys.executable, '-m', 'research', 'sensitivity-dtlz', *(argv or sys.argv[2:])])
            manifest = engine.open_study(directory, current, args.resume)
            cfg = {**cfg, 'reference_fronts': reference_fronts(directory, manifest, cfg)}
            (directory / 'logs').mkdir(exist_ok=True)
            with (directory / 'logs/run.log').open('a', encoding='utf-8') as handle:
                with redirect_stdout(Tee(sys.stdout, handle)), redirect_stderr(Tee(sys.stderr, handle)):
                    if args.stage in {'run', 'all'}:
                        engine.execute(directory, manifest, cfg, candidates, jobs, task_runner=run_task)
                    rows = engine.write_outputs(directory, manifest, cfg, candidates, report_writer=report)
                    if args.stage in {'plot', 'all'}:
                        plot_outputs(directory)
                    print(f'DTLZ OFAT complete: {len(rows)} runs; no automatic parameter selection.')
        print(f'Results: {directory}')
    except BaseException:
        if session: finish(session, status='failed', disposable=False)
        raise
    else:
        if session: finish(session, disposable=True)
