"""OFAT parameter levels around production OADE with passive telemetry.

No production changes, no automatic parameter selection, no optimization in plan.
"""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED

import numpy as np
import yaml
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from oade_nsga2 import ProblemWrapper
from oade_nsga2.configuration import FIXED_PARAMETERS
from oade_nsga2.operators import generate_obl_offspring
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded, validate_result
from shared.fronts import non_dominated_xy
from research.studies.mechanism_impact import ObservedOADE
from research.benchmarking.statistics import paired_wilcoxon_rows, holm_adjust

ROOT = Path(__file__).resolve().parents[3]
PARAMETERS = set(FIXED_PARAMETERS) - {'initialization', 'restart', 'probability_update'}
ADAPTIVE = {'mean_F', 'mean_CR', 'prob_de'}
INTEGER = {'n_neighbors', 'stagnation_patience', 'obl_interval'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ['empty'])
        writer.writeheader()
        writer.writerows(rows)


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, allow_nan=False, indent=2), encoding='utf-8')
    temp.replace(path)


def design(cfg):
    if set(cfg) != {'schema', 'population', 'budget', 'seeds', 'problems', 'parameters'} or cfg['schema'] != 1:
        raise ValueError('Unsupported configuration schema')
    pop, budget, seeds = cfg['population'], cfg['budget'], cfg['seeds']
    if type(pop) is not int or pop < 6 or type(budget) is not int or budget < 2*pop+2:
        raise ValueError('Need population >=6 and budget >=2*population+2')
    if not isinstance(seeds,list) or len(seeds)<2 or any(type(s) is not int or s<0 or s>=2**32 for s in seeds) or len(set(seeds))!=len(seeds):
        raise ValueError('Need >=2 distinct uint32 seeds')
    if not cfg['problems'] or len(set(cfg['problems']))!=len(cfg['problems']) or not set(cfg['problems']) <= {'zdt4','zdt6'}:
        raise ValueError('Choose distinct ZDT4/ZDT6 (D=10)')
    if not cfg['parameters'] or not set(cfg['parameters']) <= PARAMETERS:
        raise ValueError('Unknown or empty parameter grids')
    candidates = [{'id':'full', 'parameter':'baseline', 'level':None, 'mode':'initial'}]
    contrasts = []
    for parameter, spec in cfg['parameters'].items():
        if set(spec) != {'levels','mode'} or spec['mode'] not in {'initial','held'}:
            raise ValueError('Each grid needs levels and mode initial/held')
        if spec['mode']=='held' and parameter not in ADAPTIVE:
            raise ValueError('Held mode applies only to mean_F, mean_CR, prob_de')
        values = spec['levels']
        if not isinstance(values,list) or len(values)<2:
            raise ValueError('Need at least two levels')
        for v in values:
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):
                raise ValueError('Levels must be finite numbers')
            if parameter in INTEGER and (type(v) is not int or v<1):
                raise ValueError('Integer parameter must be positive')
            if parameter=='n_neighbors' and not 2<=v<pop:
                raise ValueError('Need 2 <= n_neighbors < population')
            if parameter=='restart_elite_ratio' and (not .8<=v<1 or int(pop*v)>=pop):
                raise ValueError('Adaptive restart clamps ratios below .8; require .8 <= ratio <1')
            if parameter in {'mean_F','stagnation_tolerance','diversity_threshold'} and not 0<v<=1:
                raise ValueError('Level must be in (0,1]')
            if parameter in {'mean_CR','prob_de','obl_jump_rate'} and not 0<=v<=1:
                raise ValueError('Level must be in [0,1]')
        base = FIXED_PARAMETERS[parameter]
        if len(set(values))!=len(values) or sum(v==base for v in values)!=1:
            raise ValueError('Distinct levels must include the production reference exactly once')
        reference = 'full'
        if spec['mode']=='held':
            reference = f'held_{parameter}_reference'
            candidates.append(dict(id=reference,parameter=parameter,level=base,mode='held'))
        for v in values:
            if v==base:
                continue
            cid = 'level_'+digest([parameter,spec['mode'],v])[:16]
            candidates.append(dict(id=cid,parameter=parameter,level=v,mode=spec['mode']))
            contrasts.append(dict(parameter=parameter,level=v,mode=spec['mode'],reference=reference,candidate=cid))
    return candidates, contrasts


class LevelOADE(ObservedOADE):
    def __init__(self, *args, candidate, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate = candidate
        self.settings = dict(FIXED_PARAMETERS)
        if candidate['parameter']!='baseline':
            self.settings[candidate['parameter']] = candidate['level']
        for key in PARAMETERS-ADAPTIVE-{'obl_interval','obl_jump_rate'}:
            setattr(self,key,self.settings[key])

    def _build_initial_population(self):
        # Production run() resets these immediately before this hook.
        for key in ADAPTIVE:
            setattr(self,key,self.settings[key])
        result = super()._build_initial_population()
        self.initial_x_sha256 = digest([i.X.tolist() for i in result])
        return result

    def _generate_periodic_obl(self,gen):
        if gen % self.settings['obl_interval']:
            return []
        return self._observe('obl',lambda: generate_obl_offspring(self.population,self.problem,
            self.xl,self.xu,jump_rate=self.settings['obl_jump_rate']))

    def _restore_held(self):
        if self.candidate['mode']=='held':
            key = self.candidate['parameter']
            setattr(self,key,self.settings[key])

    def _adaptive_restart(self):
        try:
            return super()._adaptive_restart()
        finally:
            self._restore_held()

    def _update_adaptive_parameters(self,offspring,*,reference_population=None):
        before = self.mean_F,self.mean_CR,self.prob_de
        super()._update_adaptive_parameters(offspring,reference_population=reference_population)
        self._restore_held()
        row = self.trace[-1]
        row.update(mean_F=self.mean_F,mean_CR=self.mean_CR,pde=self.prob_de,
            f_cr_changed=int(before[:2]!=(self.mean_F,self.mean_CR)),pde_changed=int(before[2]!=self.prob_de))


def run_one(problem_name,seed,candidate,population,budget,reference):
    problem = get_problem(problem_name,n_var=10)
    counter = BudgetedProblem(problem,budget)
    solver = LevelOADE(ProblemWrapper(counter),pop_size=population,n_gen=budget,seed=seed,candidate=candidate)
    start = time.perf_counter()
    try:
        solver.run()
    except EvaluationBudgetExceeded:
        pass
    x,f = non_dominated_xy(np.asarray([i.X for i in solver.population]),np.asarray([i.F for i in solver.population]))
    valid = validate_result(x,f,problem).valid
    ref = np.asarray(reference)
    return dict(problem=problem_name,algorithm=candidate['id'],seed=seed,run_idx=seed,
        candidate=candidate,settings=solver.settings,valid=valid,n_eval=counter.n_eval,
        runtime_seconds=time.perf_counter()-start,IGD=float(IGD(ref)(f)) if valid else None,
        HV=float(HV(ref_point=ref.max(0)+.1)(f)) if valid else None,
        initial_x_sha256=solver.initial_x_sha256,reference_sha256=digest(reference),
        final_x=x.tolist(),final_f=f.tolist(),trace=solver.trace,events=solver.events)


def execute_tasks(tasks, jobs):
    """Bound pending work; only the parent writes primary records/manifest.

    Spawn isolates NumPy/Python global RNG and matches Windows semantics.
    Yield completed records promptly, independently of submission order.
    """
    if jobs == 1:
        for name, args in tasks:
            yield name, run_one(*args)
        return
    remaining = iter(tasks)
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context('spawn')) as pool:
        pending = {}

        def fill():
            while len(pending) < 2 * jobs:
                item = next(remaining, None)
                if item is None:
                    break
                name, args = item
                pending[pool.submit(run_one, *args)] = name

        fill()
        try:
            while pending:
                done, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    name = pending.pop(future)
                    yield name, future.result()
                fill()
        finally:
            for future in pending:
                future.cancel()


def report(directory,records,contrasts,seeds):
    out = directory/'derived'
    raw = [{k:r[k] for k in ('problem','algorithm','seed','run_idx','valid','n_eval','runtime_seconds','IGD','HV')} for r in records]
    write_csv(out/'runs.csv',raw)
    comparisons=[]
    for c in contrasts:
        subset=[r for r in raw if r['algorithm'] in (c['reference'],c['candidate'])]
        rows=paired_wilcoxon_rows(subset,c['reference'])
        # Preserve the configured multiplicity family even if every pair in an
        # endpoint is invalid; absence of valid pairs is not a zero effect.
        for problem in sorted({r['problem'] for r in raw}):
            for metric in ('IGD','HV'):
                if not any(r['problem']==problem and r['metric']==metric for r in rows):
                    rows.append(dict(problem=problem,metric=metric,reference_algorithm=c['reference'],
                        comparison_algorithm=c['candidate'],n_pairs=0,reference_mean=None,comparison_mean=None,
                        median_paired_difference=None,statistic=0.,p_value=1.,p_adjusted_holm=1.,
                        rank_biserial_effect=0.,alpha=.05,significant=False,result='no_valid_pairs'))
        for row in rows:
            row.update(parameter=c['parameter'],level=c['level'],mode=c['mode'],excluded_pairs=len(seeds)-row['n_pairs'])
            comparisons.append(row)
    if comparisons:
        for r,p in zip(comparisons,holm_adjust(r['p_value'] for r in comparisons)):
            r['p_adjusted_holm']=p
            r['significant']=p<.05
            r['result']=('reference_better' if r['rank_biserial_effect']>0 else 'level_better') if p<.05 else ('not_significant' if r['n_pairs'] else 'no_valid_pairs')
    write_csv(out/'comparisons.csv',comparisons)
    summaries=[]
    for p,a in sorted({(r['problem'],r['algorithm']) for r in raw}):
        group=[r for r in raw if (r['problem'],r['algorithm'])==(p,a)]
        good=[r for r in group if r['valid']]
        candidate=next(r['candidate'] for r in records if r['problem']==p and r['algorithm']==a) if 'candidate' in records[0] else {}
        row=dict(problem=p,algorithm=a,parameter=candidate.get('parameter'),level=candidate.get('level'),
            mode=candidate.get('mode'),runs=len(group),valid_runs=len(good),
            runtime_median=float(np.median([r['runtime_seconds'] for r in group])),
            n_eval_min=min(r['n_eval'] for r in group),n_eval_max=max(r['n_eval'] for r in group))
        for metric in ('IGD','HV'):
            vals=[r[metric] for r in good]
            row.update({metric+'_mean':float(np.mean(vals)) if vals else None,
                metric+'_sd':float(np.std(vals,ddof=1)) if len(vals)>1 else None,
                metric+'_median':float(np.median(vals)) if vals else None})
        summaries.append(row)
    write_csv(out/'summary.csv',summaries)
    for key in ('trace','events'):
        write_csv(out/(key+'.csv'),[dict(problem=r['problem'],algorithm=r['algorithm'],seed=r['seed'],**t) for r in records for t in r[key]])
    activations=[]
    for r in records:
        for mech in ('obl','restart'):
            ev=[e for e in r['events'] if e['mechanism']==mech]
            activations.append(dict(problem=r['problem'],algorithm=r['algorithm'],seed=r['seed'],mechanism=mech,
                completed=sum(e['status']=='completed' for e in ev),budget_blocked=sum(e['status']=='budget_blocked' for e in ev),
                evaluations=sum(e['evaluations'] for e in ev)))
    write_csv(out/'activation.csv',activations)
    lines=['# Parameter-level sensitivity results','',f'{len(records)} completed runs; {sum(r["valid"] for r in records)} valid.',
        f'{len(comparisons)} paired endpoints; Holm across the complete configured family; alpha=0.05.',
        'Reference is full adaptive production for initial mode, or the same held parameter at its production value for held mode.',
        'Invalid pairs are excluded and counted. NS does not establish equivalence. No automatic selection; OFAT does not identify interactions.',
        '', '| Problem | Parameter | Mode | Level | Metric | Pairs | Median(reference-level) | Holm p | Result |',
        '|---|---|---|---:|---|---:|---:|---:|---|']
    for r in comparisons:
        delta='NA' if r['median_paired_difference'] is None else f'{r["median_paired_difference"]:.6g}'
        lines.append(f'| {r["problem"]} | {r["parameter"]} | {r["mode"]} | {r["level"]} | {r["metric"]} | {r["n_pairs"]} | {delta} | {r["p_adjusted_holm"]:.6g} | {r["result"]} |')
    (out/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=Path('config/studies/mechanism_sensitivity.yaml'))
    parser.add_argument('--stage',choices=('plan','run','report'),default='plan')
    parser.add_argument('--out-dir',type=Path,default=Path('results/experiments/mechanism_sensitivity_v1'))
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--jobs',type=int,default=1,help='Independent solver processes (default: 1)')
    args=parser.parse_args(argv)
    if args.jobs < 1:
        parser.error('--jobs must be >= 1')
    cfg=yaml.safe_load(args.config.read_text(encoding='utf-8'))
    candidates,contrasts=design(cfg)
    total=len(candidates)*len(cfg['problems'])*len(cfg['seeds'])
    print(json.dumps(dict(configurations=len(candidates),runs=total,endpoints=len(contrasts)*len(cfg['problems'])*2,max_evaluations=total*cfg['budget'],jobs=args.jobs),indent=2))
    if args.stage=='plan':
        return
    sources=[*sorted((ROOT/'src/oade_nsga2').glob('*.py')),Path(__file__),
        ROOT/'src/research/studies/mechanism_impact.py',ROOT/'src/research/benchmarking/statistics.py',
        *sorted((ROOT/'src/shared').rglob('*.py'))]
    protocol=dict(config=cfg,candidates=candidates,contrasts=contrasts,
        sources={p.relative_to(ROOT).as_posix():sha(p) for p in sources},
        environment=dict(python=platform.python_version(),packages={p:importlib.metadata.version(p) for p in ('numpy','scipy','pymoo','PyYAML')},
            threads={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')}),
        references={p:get_problem(p,n_var=10).pareto_front().tolist() for p in cfg['problems']})
    directory=args.out_dir
    manifest=directory/'manifest.json'
    if manifest.exists():
        stored=json.loads(manifest.read_text())
        if not args.resume or stored['protocol']!=protocol:
            raise ValueError('Resume requires identical config, sources, references and environment')
    else:
        if args.stage=='report' or (directory.exists() and any(directory.iterdir())):
            raise ValueError('Need existing manifest for report or empty output for run')
        directory.mkdir(parents=True,exist_ok=True)
        stored=dict(protocol=protocol,artifacts={})
        atomic_json(manifest,stored)
    primary=directory/'primary'; primary.mkdir(exist_ok=True)
    if {p.name for p in primary.glob('*.json')} != set(stored['artifacts']):
        raise ValueError('Primary inventory mismatch; uncommitted/interrupted artifact needs inspection')
    planned={f'{p}_{s}_{c["id"]}.json' for p in cfg['problems'] for s in cfg['seeds'] for c in candidates}
    if not set(stored['artifacts']) <= planned:
        raise ValueError('Unexpected task in manifest')
    for name,expected_hash in stored['artifacts'].items():
        if sha(primary/name)!=expected_hash:
            raise ValueError(f'Checksum mismatch: {name}')
    tasks=[]
    expected_tasks={}
    records_by_name={}
    initial_hashes={}

    def validate(name,r):
        problem,seed,candidate=expected_tasks[name]
        if (r['problem'],r['seed'],r['candidate'])!=(problem,seed,candidate) or not 0<r['n_eval']<=cfg['budget']:
            raise ValueError('Task identity or budget mismatch')
        block=(problem,seed)
        initial_hashes.setdefault(block,r['initial_x_sha256'])
        if r['initial_x_sha256']!=initial_hashes[block]:
            raise ValueError('Initial population mismatch within paired block')

    for problem in cfg['problems']:
        for seed in cfg['seeds']:
            for candidate in candidates:
                name=f'{problem}_{seed}_{candidate["id"]}.json'; target=primary/name
                expected_tasks[name]=(problem,seed,candidate)
                if name in stored['artifacts']:
                    r=json.loads(target.read_text())
                    validate(name,r)
                    records_by_name[name]=r
                elif args.stage=='report':
                    raise ValueError('Study incomplete; report does not run missing tasks')
                else:
                    tasks.append((name,(problem,seed,candidate,cfg['population'],cfg['budget'],protocol['references'][problem])))
    if tasks:
        stored.setdefault('execution_sessions',[]).append(dict(jobs=args.jobs,pending_runs=len(tasks)))
        atomic_json(manifest,stored)
    for name,r in execute_tasks(tasks,args.jobs):
        validate(name,r)
        r['execution_jobs']=args.jobs
        atomic_json(primary/name,r)
        stored['artifacts'][name]=sha(primary/name)
        atomic_json(manifest,stored)
        records_by_name[name]=r
        print(f'{len(records_by_name)}/{total} {r["problem"]} seed={r["seed"]} {r["algorithm"]}: FE={r["n_eval"]}, valid={r["valid"]}',flush=True)
    # Reports retain planned order even when workers finish out of order.
    records=[records_by_name[name] for name in expected_tasks]
    report(directory,records,contrasts,cfg['seeds'])


if __name__=='__main__':
    main()
