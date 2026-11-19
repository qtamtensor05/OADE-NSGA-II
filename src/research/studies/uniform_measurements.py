"""Uniform-initialized run measurement for controlled periodic-injection studies."""
from __future__ import annotations

import json
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

from research.oade_nsga2.runner import run_instrumented
from shared.contracts import AlgorithmSpec
from shared.evaluation import validate_result
from shared.population import make_initial_population
from shared.io.csv_io import write_csv
from research.benchmarking.convergence import ConvergenceRecorder
from research.benchmarking.provenance import digest
from . import restart_comparison as base


def run_task(cfg,candidate,problem_cfg,seed):
    problem = get_problem(problem_cfg['name'],n_var=problem_cfg['n_var'])
    ref = np.asarray(cfg['reference_fronts'][problem_cfg['name']])
    igd,hv = IGD(ref),HV(ref_point=np.max(ref,axis=0)+.1)
    budget,pop = cfg['global']['evaluation_budget'],cfg['global']['pop_size']
    mode = candidate['settings']['initialization_method']
    if mode != 'uniform':
        raise ValueError('Only uniform initialization is supported')
    initial = make_initial_population(problem,pop,seed)
    params = {k:v for k,v in candidate['settings'].items() if k not in {'pop_size','initialization_method'}}
    spec = AlgorithmSpec(candidate['id'],'local_oade_research',params)

    def metrics(f):
        return {'IGD':float(igd(f)), 'HV':float(hv(f))}

    outcome,observed = run_instrumented(spec,problem,pop,budget,initial,seed,
                                        ConvergenceRecorder(budget,igd,hv),restart_metric=metrics)
    evidence = observed['initialization_evidence']
    initial_quality = metrics(np.asarray(evidence['f']))
    validation = validate_result(outcome.x,outcome.f,problem)
    quality = metrics(outcome.f)
    valid = validation.valid and all(np.isfinite(v) for v in quality.values())
    expected = pop
    if evidence['evaluations'] != expected:
        raise ValueError('Initialization evaluations were not charged exactly once')
    return {'candidate':candidate['id'],'parameter':candidate['parameter'],'level':candidate['level'],
            'problem':problem_cfg['name'],'n_var':problem_cfg['n_var'],'seed':seed,
            'settings':candidate['settings'],'evaluation_budget':budget,'n_eval':outcome.n_eval,
            'valid':valid,'validation_status':validation.status if valid else 'invalid_quality',
            'front_size':validation.front_size,**(quality if valid else {'IGD':None,'HV':None}),
            'runtime_seconds':outcome.runtime_seconds,'reference_sha256':digest(ref.tolist()),
            'initial_x_sha256':digest(evidence['x']),'initialization_seed':seed,
            'initialization_evaluations':expected,'initial_IGD':initial_quality['IGD'],
            'initial_HV':initial_quality['HV'],'final_x':outcome.x.tolist(),'final_f':outcome.f.tolist(),
            'convergence':list(outcome.convergence),**observed}


def write_measurements(directory,manifest,cfg,candidates,*,require_same_initial=True):
    rows = base.engine.load_records(directory,manifest)
    base.engine.validate_records(cfg,candidates,rows,complete=True)
    # Uniform controlled studies compare the same initial population per seed.
    paired = base.comparisons(cfg,candidates,rows,require_same_initial=require_same_initial)
    derived = directory/'derived'
    derived.mkdir(exist_ok=True)
    scalar = [{k:v for k,v in r.items() if not isinstance(v,(dict,list))}|r['telemetry'] for r in rows]
    write_csv(derived/'raw_runs.csv',scalar,list(scalar[0]))
    write_csv(derived/'comparisons.csv',paired,list(paired[0]))
    summaries=[]
    for p in cfg['problems']:
        for c in candidates:
            group=[r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']]
            valid=[r for r in group if r['valid']]
            s={'problem':p['name'],'method':c['id'],'runs':len(group),'valid_runs':len(valid),
               'restart_attempts':sum(r['telemetry']['restart_attempts'] for r in group),
               'initialization_evaluations':group[0]['initialization_evaluations']}
            for key in ('injection_attempts','injection_completed','injection_budget_blocked',
                        'injection_candidates','injection_evaluations','injection_retained'):
                s[key]=sum(r['telemetry'].get(key,0) for r in group)
            for metric in ('IGD','HV','initial_IGD','initial_HV','runtime_seconds','n_eval','final_prob_de'):
                values=[r[metric] for r in (valid if metric in {'IGD','HV'} else group)]
                for label,fn in [('mean',np.mean),('median',np.median),('q25',lambda x:np.quantile(x,.25)),
                                 ('q75',lambda x:np.quantile(x,.75)),('sd',lambda x:np.std(x,ddof=1) if len(x)>1 else 0.)]:
                    s[metric+'_'+label]=float(fn(values)) if values else None
            summaries.append(s)
    write_csv(derived/'summary.csv',summaries,list(summaries[0]))
    for key,name,fields in [
        ('probability_trace','probability_trace.csv',['candidate','problem','seed','generation','n_eval','mode','enabled','n_de','n_sbx','success_de','success_sbx','target','prob_before','prob_after']),
        ('convergence','convergence.csv',['candidate','problem','seed','checkpoint_fraction','target_evaluations','n_eval','IGD','HV'])]:
        trace=[{k:r[k] for k in ('candidate','problem','seed')}|t for r in rows for t in r[key]]
        write_csv(derived/name,trace,fields)
    return rows,summaries,paired


