"""Fresh seven-solver ZDT benchmark with per-run evidence and fixed OADE only."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from oade_nsga2 import FIXED_PARAMETERS
from shared.contracts import AlgorithmSpec
from shared.population import make_initial_population
from shared.evaluation import validate_result
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv
from shared.paths import ROOT,repository_path
from research.maintenance.tmp_sessions import session_lock
from research.studies import zdt_sensitivity as engine
from .runner import load_algorithm_specs
from .adapters import run_algorithm
from .convergence import ConvergenceRecorder
from .provenance import digest
from .statistics import paired_wilcoxon_rows,holm_adjust

NAMES={'OADE_NSGAII','NSGA2','RNSGA2','DNSGA2','CGDE_NSGAII','NSGAII_SDR_OLS','CE_MOEA'}
STUDY_KIND='zdt_seven_fixed_oade_v2'
BASELINE_REVISION='paper_corrections_2026_11_14'


def design(cfg):
    cfg=json.loads(json.dumps(cfg));g=cfg['global']
    if any(type(g[k]) is not int for k in ('runs','seed_base','pop_size','evaluation_budget')):
        raise ValueError('Run dimensions must be integers')
    if g['runs']<2 or g['seed_base']<0 or g['pop_size']<10 or g['evaluation_budget']<=g['pop_size']+2:
        raise ValueError('Need >=2 runs, nonnegative seeds, population >=10 and budget > population+2')
    expected={'zdt1':30,'zdt2':30,'zdt3':30,'zdt4':10,'zdt6':10}
    if not cfg['problems'] or len({p['name'] for p in cfg['problems']})!=len(cfg['problems']):
        raise ValueError('Require unique ZDT problems')
    for p in cfg['problems']:
        if set(p)!={'name','n_var'} or p['name'] not in expected or p['n_var']!=expected[p['name']]:
            raise ValueError('Use standard ZDT1/2/3 D=30 and ZDT4/6 D=10')
    specs=load_algorithm_specs(cfg['algorithm_configs'])
    if {s.name for s in specs}!=NAMES:raise ValueError('Require exactly the seven configured algorithms')
    oade=next(s for s in specs if s.name=='OADE_NSGAII')
    if oade.runner!='local_oade' or oade.params or oade.class_path is not None or oade.sampling is not None or oade.auto_ref_points:
        raise ValueError('Use fixed oade_nsga2 via local_oade with no overrides; research OADE is forbidden')
    if any(s.runner=='local_oade_research' for s in specs):raise ValueError('Research solver is forbidden')
    updated={
        'CGDE_NSGAII':('local_cgde_nsga2', {'n_neighbors':5,'f_bounds':[.2,.9],
                                         'f_perturbation':.2,'cr_bounds':[0.,1.]}),
        'NSGAII_SDR_OLS':('local_nsga2_sdr_ols', {'mu':0.,'sigma':.1,'crossover_prob':.9,
                                              'mutation_prob':None,'eta_c':20.,'eta_m':20.}),
        'CE_MOEA':('local_ce_moea', {'F_DE':.7,'CR':.5,'p_m':.02,'eta_m':20.}),
    }
    for spec in specs:
        if spec.name in updated:
            runner,params=updated[spec.name]
            if spec.runner!=runner or spec.params!=params or spec.class_path is not None:
                raise ValueError(f'Use corrected baseline configuration for {spec.name}')
    g['seeds']=list(range(g['seed_base'],g['seed_base']+g['runs']))
    cfg['baseline_revision']=BASELINE_REVISION
    cfg['oade_fixed_parameters']=dict(FIXED_PARAMETERS)
    cfg.setdefault('execution_order_seed',20261114)
    return cfg,[dict(id=s.name,parameter='algorithm',level=s.name,settings=asdict(s)) for s in specs]


def run_task(cfg,candidate,p,seed):
    problem=get_problem(p['name'],n_var=p['n_var'])
    ref=np.asarray(cfg['reference_fronts'][p['name']]);igd=IGD(ref);hv=HV(ref_point=ref.max(axis=0)+.1)
    initial=make_initial_population(problem,cfg['global']['pop_size'],seed)
    spec=AlgorithmSpec(**candidate['settings']);budget=cfg['global']['evaluation_budget']
    outcome=run_algorithm(spec,problem,cfg['global']['pop_size'],budget,initial,seed,ConvergenceRecorder(budget,igd,hv))
    validation=validate_result(outcome.x,outcome.f,problem)
    valid=validation.valid and 0<outcome.n_eval<=budget
    quality={'IGD':float(igd(outcome.f)),'HV':float(hv(outcome.f))} if valid else {'IGD':None,'HV':None}
    if valid and not all(np.isfinite(v) for v in quality.values()):valid=False;quality={'IGD':None,'HV':None}
    return {'candidate':candidate['id'],'parameter':'algorithm','level':candidate['id'],'settings':candidate['settings'],
            'algorithm':spec.name,'runner':spec.runner,'problem':p['name'],'n_var':p['n_var'],'n_obj':2,'seed':seed,
            'run_idx':seed-cfg['global']['seed_base'],'evaluation_budget':budget,'n_eval':outcome.n_eval,
            'valid':valid,'validation_status':validation.status if valid else 'invalid_'+validation.status,
            'front_size':validation.front_size,'duplicate_fraction':validation.duplicate_fraction,
            'budget_utilization':outcome.n_eval/budget,'runtime_seconds':outcome.runtime_seconds,**quality,
            'initial_x_sha256':digest(initial.tolist()),'reference_sha256':digest(ref.tolist()),
            'final_x':outcome.x.tolist(),'final_f':outcome.f.tolist(),'convergence':list(outcome.convergence),
            'telemetry':{'objective_evaluations':outcome.n_eval}}


def write_outputs(directory,manifest,cfg,candidates):
    rows=engine.load_records(directory,manifest);engine.validate_records(cfg,candidates,rows,complete=True)
    derived=directory/'derived';derived.mkdir(exist_ok=True)
    for p in cfg['problems']:
        for seed in cfg['global']['seeds']:
            block=[r for r in rows if r['problem']==p['name'] and r['seed']==seed]
            if len({r['initial_x_sha256'] for r in block})!=1:raise ValueError('Paired initialization mismatch')
    raw=[{k:v for k,v in r.items() if not isinstance(v,(dict,list))} for r in rows]
    write_csv(derived/'raw_runs.csv',raw,list(raw[0]))
    summaries=[]
    for p in cfg['problems']:
        for c in candidates:
            group=[r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']];valid=[r for r in group if r['valid']]
            s={'problem':p['name'],'algorithm':c['id'],'runs':len(group),'valid_runs':len(valid),'invalid_runs':len(group)-len(valid)}
            for metric in ('IGD','HV','runtime_seconds','n_eval'):
                values=[r[metric] for r in (valid if metric in {'IGD','HV'} else group)]
                for label,fn in [('mean',np.mean),('sd',lambda v:np.std(v,ddof=1) if len(v)>1 else 0.),('median',np.median),('q25',lambda v:np.quantile(v,.25)),('q75',lambda v:np.quantile(v,.75))]:s[metric+'_'+label]=float(fn(values)) if values else None
            summaries.append(s)
    write_csv(derived/'summary.csv',summaries,list(summaries[0]))
    paired=paired_wilcoxon_rows(rows,'OADE_NSGAII',alpha=.05)
    for r in paired:r['excluded_pairs']=cfg['global']['runs']-r['n_pairs']
    for metric in ('IGD','HV'):
        block=[r for r in paired if r['metric']==metric]
        padded=[r['p_value'] for r in block]+[1.]*(len(cfg['problems'])*6-len(block))
        for r,pvalue in zip(block,holm_adjust(padded)):
            r['p_adjusted_holm']=pvalue;r['significant']=pvalue<.05
            r['result']=('no_significant_difference' if not r['significant'] else
                         'reference_better' if r['rank_biserial_effect']>0 else 'comparison_better')
    # Preserve the full planned 60-endpoint family even if invalid blocks lack pairs.
    planned=len(cfg['problems'])*6*2
    full=holm_adjust([r['p_value'] for r in paired]+[1.]*(planned-len(paired)))
    for r,pvalue in zip(paired,full):
        r['p_holm_all_endpoints']=pvalue
        r['significant_all_endpoints']=pvalue<.05
        r['result_all_endpoints']=('no_significant_difference' if not r['significant_all_endpoints'] else
                                  'reference_better' if r['rank_biserial_effect']>0 else 'comparison_better')
    if paired:write_csv(derived/'comparisons.csv',paired,list(paired[0]))
    else:write_csv(derived/'comparisons.csv',[],['problem','metric','reference_algorithm','comparison_algorithm','n_pairs','p_value','p_adjusted_holm','p_holm_all_endpoints','excluded_pairs'])
    convergence=[{k:r[k] for k in ('algorithm','problem','seed')}|t for r in rows for t in r['convergence']]
    write_csv(derived/'convergence.csv',convergence,['algorithm','problem','seed','checkpoint_fraction','target_evaluations','n_eval','IGD','HV'])
    text=['# So sánh mới 7 thuật toán trên ZDT','',
          '**SMOKE: kiểm tra pipeline, không phải kết quả nghiên cứu.**' if cfg.get('smoke') else 'Toàn bộ 7 thuật toán được chạy mới; không ghép block lịch sử.',
          f"Tổng run: **{len(rows)}**; invalid: **{sum(not r['valid'] for r in rows)}**.",'',
          'OADE dùng bản chính oade_nsga2, runner local_oade, một cấu hình uniform + adaptive restart + OBL định kỳ + success-rate. Không dùng research.oade_nsga2. Các bản sửa duplicate/stale rank và objective budget được giữ.',
          'Mỗi run có cùng uniform input theo bài/seed, cùng cap tổng; RNSGA2 aspiration-point setup tính cả objective calls. Task được xáo thứ tự theo seed cố định; runtime vẫn chịu ảnh hưởng máy/worker. X/F cuối, hash initial/reference và convergence lưu trong primary JSON.',
          'Nguồn và giới hạn tái dựng: [baseline registry](../../../../docs/protocols/baselines.md), [sửa theo bài báo](../../../../docs/protocols/baseline_paper_corrections.md). CGDE dùng NCG/PCG và F theo cá thể; CR range/bootstrap/subrank ties là quy ước công khai. SDR-OLS bỏ cap 2N, dùng cả pool LS, nhưng Algorithm 4 gốc chưa nhất quán. CE-MOEA trên ZDT là adaptation lõi tìm kiếm, PM dùng số mũ in trong bản v2. Không chứng nhận tái lập đầy đủ ba thuật toán.',
          'Wilcoxon signed-rank hai phía, zero_method=wilcox, SciPy method=auto; all-zero p=1. OADE so với 6 đối chứng: Holm riêng từng metric trên 30 cặp bài/đối chứng để so với cách báo cáo cũ; cột p_holm_all_endpoints bổ sung họ chung 60 endpoint. Alpha=0,05. Các cặp invalid bị loại và đếm; không phát hiện khác biệt không chứng minh tương đương.', '',
          '| Bài | Thuật toán | Valid/run | IGD median ↓ | HV median ↑ | Runtime median (s) |','|:---|:---|---:|---:|---:|---:|']
    for s in summaries:
        fmt=lambda k:'—' if s[k] is None else f'{s[k]:.7f}'
        text.append(f"| {s['problem'].upper()} | {s['algorithm']} | {s['valid_runs']}/{s['runs']} | {fmt('IGD_median')} | {fmt('HV_median')} | {s['runtime_seconds_median']:.3f} |")
    text+=['','Đây là so sánh các bản triển khai cụ thể trong repository, không chứng minh ưu thế so với mọi thuật toán cùng tên trong tài liệu. CGDE/SDR-OLS/CE-MOEA có các điều chỉnh cục bộ; xem registry baselines. Batch nguyên tử có thể để dư budget; xem n_eval thực. Convergence không nội suy.', '']
    (derived/'report.md').write_text('\n'.join(text),encoding='utf-8')
    from .deb_report import export_tables
    export_tables(rows, derived/'deb_metrics', cfg)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='config/suites/zdt_seven_fixed_oade.yaml')
    parser.add_argument('--stage',choices=('plan','run','report'),default='plan')
    parser.add_argument('--out-dir',type=Path);parser.add_argument('--jobs',type=int);parser.add_argument('--resume',action='store_true')
    args=parser.parse_args(argv);cfg,candidates=design(load_yaml_config(Path(args.config)))
    if args.stage=='plan':
        print(json.dumps({'runs':len(engine.tasks(cfg,candidates)),'algorithms':[c['settings'] for c in candidates],
                          'oade_fixed_parameters':dict(FIXED_PARAMETERS),'seeds':cfg['global']['seeds'],
                          'problems':cfg['problems'],'cap':cfg['global']['evaluation_budget'],
                          'baseline_revision':cfg['baseline_revision'],
                          'out_dir':str(args.out_dir or cfg['global']['out_dir'])},indent=2));return
    jobs=args.jobs if args.jobs is not None else cfg['global'].get('jobs',4)
    if jobs<1 or args.stage=='report' and not args.resume:raise ValueError('Positive jobs required; report requires --resume')
    directory=(args.out_dir or repository_path(cfg['global']['out_dir'])).resolve()
    lock=ROOT/'tmp/study_locks'/digest(str(directory));lock.mkdir(parents=True,exist_ok=True)
    with session_lock(lock):
        current=engine.identity(cfg,candidates);current['kind']=STUDY_KIND
        manifest=engine.open_study(directory,current,args.resume)
        cfg={**cfg,'reference_fronts':engine.reference_fronts(directory,manifest,cfg)}
        if args.stage=='run':engine.execute(directory,manifest,cfg,candidates,jobs,task_runner=run_task,
                                           order_seed=cfg['execution_order_seed'],progress_label='ZDT7')
        write_outputs(directory,manifest,cfg,candidates)
    print(f'Results: {directory}')


if __name__=='__main__':main()
