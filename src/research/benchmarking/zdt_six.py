"""Current six-solver ZDT comparison; fresh evidence, unchanged production OADE."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from oade_nsga2 import FIXED_PARAMETERS
from shared.io.config import load_yaml_config
from shared.io.csv_io import write_csv
from shared.paths import ROOT, repository_path
from research.maintenance.tmp_sessions import session_lock
from research.studies import zdt_sensitivity as engine
from .runner import load_algorithm_specs
from .provenance import digest
from .statistics import paired_wilcoxon_rows, holm_adjust
from .zdt_seven import run_task  # Common measurement contract; no legacy solver is selected.

NAMES={'OADE_NSGAII','NSGA2','DNSGA2','CGDE_NSGAII','GDE3','NSDE'}
STUDY_KIND='zdt_six_fixed_oade_v1'
REVISION='pymoo_de_baselines_2026_11_19'
DE_PARAMS=dict(variant='DE/rand/1/bin',F=.5,CR=.5,gamma=.0001,de_repair='bounce-back')


def design(cfg):
    cfg=json.loads(json.dumps(cfg));g=cfg['global']
    if any(type(g[k]) is not int for k in ('runs','pop_size','evaluation_budget','seed_base')):
        raise ValueError('Run dimensions must be integers')
    if g['runs']<2 or not 0<=g['seed_base']<2**32-g['runs'] or g['pop_size']<10 or g['evaluation_budget']<=g['pop_size']+2:
        raise ValueError('Invalid seed, population or evaluation budget')
    dimensions={'zdt1':30,'zdt2':30,'zdt3':30,'zdt4':10,'zdt6':10}
    if not cfg['problems'] or len({p['name'] for p in cfg['problems']})!=len(cfg['problems']):
        raise ValueError('Require distinct continuous ZDT problems')
    for p in cfg['problems']:
        if set(p)!={'name','n_var'} or dimensions.get(p['name'])!=p['n_var']:
            raise ValueError('Use standard ZDT dimensions')
    specs=load_algorithm_specs(cfg['algorithm_configs'])
    if len(specs)!=6 or {s.name for s in specs}!=NAMES:
        raise ValueError('Require OADE, NSGA2, DNSGA2, CGDE_NSGAII, GDE3 and NSDE only')
    expected={
        'OADE_NSGAII':dict(runner='local_oade',class_path=None,sampling=None,params={}),
        'NSGA2':dict(runner='pymoo',class_path='pymoo.algorithms.moo.nsga2.NSGA2',sampling='initial_population',params={}),
        'DNSGA2':dict(runner='pymoo',class_path='pymoo.algorithms.moo.dnsga2.DNSGA2',sampling='initial_population',params={}),
        'CGDE_NSGAII':dict(runner='local_cgde_nsga2',class_path=None,sampling=None,
            params=dict(n_neighbors=5,f_bounds=[.2,.9],f_perturbation=.2,cr_bounds=[0.,1.])),
        'GDE3':dict(runner='pymoo',class_path='pymoo.algorithms.moo.gde3.GDE3',sampling='initial_population',params=DE_PARAMS),
        'NSDE':dict(runner='pymoo',class_path='pymoo.algorithms.moo.nsde.NSDE',sampling='initial_population',params=DE_PARAMS),
    }
    for s in specs:
        if s.auto_ref_points or any(getattr(s,key)!=value for key,value in expected[s.name].items()):
            raise ValueError(f'Unexpected baseline implementation/settings: {s.name}')
    if cfg.get('statistics')!={'alpha':.05,'reference_algorithm':'OADE_NSGAII'}:
        raise ValueError('Use OADE reference, alpha .05 and planned global Holm family')
    g['seeds']=list(range(g['seed_base'],g['seed_base']+g['runs']))
    cfg['baseline_revision']=REVISION;cfg['oade_fixed_parameters']=dict(FIXED_PARAMETERS)
    cfg.setdefault('execution_order_seed',20261119)
    return cfg,[dict(id=s.name,parameter='algorithm',level=s.name,settings=asdict(s)) for s in specs]


def sci(value):
    if value is None:return '—'
    if value==0:return '0'
    mantissa,exponent=f'{value:.3e}'.split('e')
    return f'{mantissa.rstrip("0").rstrip(".")}e{int(exponent)}'


def write_outputs(directory,manifest,cfg,candidates):
    rows=engine.load_records(directory,manifest);engine.validate_records(cfg,candidates,rows,complete=True)
    derived=directory/'derived';derived.mkdir(exist_ok=True)
    for p in cfg['problems']:
        for seed in cfg['global']['seeds']:
            block=[r for r in rows if r['problem']==p['name'] and r['seed']==seed]
            if len(block)!=6 or len({r['initial_x_sha256'] for r in block})!=1:
                raise ValueError('Paired initialization mismatch')
    raw=[{k:v for k,v in r.items() if not isinstance(v,(dict,list))} for r in rows]
    write_csv(derived/'raw_runs.csv',raw,list(raw[0]))
    summaries=[]
    for p in cfg['problems']:
        for c in candidates:
            group=[r for r in rows if r['problem']==p['name'] and r['algorithm']==c['id']]
            valid=[r for r in group if r['valid']]
            s=dict(problem=p['name'],algorithm=c['id'],runs=len(group),valid_runs=len(valid),invalid_runs=len(group)-len(valid))
            for metric in ('IGD','HV','runtime_seconds','n_eval'):
                values=[r[metric] for r in (valid if metric in ('IGD','HV') else group)]
                for label,fn in [('mean',np.mean),('sd',lambda v:np.std(v,ddof=1) if len(v)>1 else 0.),
                                 ('median',np.median),('min',np.min),('max',np.max)]:
                    s[metric+'_'+label]=float(fn(values)) if values else None
            summaries.append(s)
    write_csv(derived/'summary.csv',summaries,list(summaries[0]))
    paired=paired_wilcoxon_rows(rows,'OADE_NSGAII',alpha=.05)
    # Keep every configured endpoint in the Holm family, including no-valid-pair blocks.
    for p in cfg['problems']:
        for c in candidates:
            if c['id']=='OADE_NSGAII':continue
            for metric in ('IGD','HV'):
                if not any(r['problem']==p['name'] and r['comparison_algorithm']==c['id'] and r['metric']==metric for r in paired):
                    paired.append(dict(problem=p['name'],metric=metric,reference_algorithm='OADE_NSGAII',comparison_algorithm=c['id'],
                        n_pairs=0,reference_mean=None,comparison_mean=None,median_paired_difference=None,statistic=0.,p_value=1.,
                        p_adjusted_holm=1.,rank_biserial_effect=0.,alpha=.05,significant=False,result='no_valid_pairs'))
    for r,pvalue in zip(paired,holm_adjust(r['p_value'] for r in paired)):
        r.update(p_adjusted_holm=pvalue,significant=pvalue<.05,excluded_pairs=cfg['global']['runs']-r['n_pairs'])
        r['result']=('reference_better' if r['rank_biserial_effect']>0 else 'comparison_better') if pvalue<.05 else ('no_significant_difference' if r['n_pairs'] else 'no_valid_pairs')
    write_csv(derived/'comparisons.csv',paired,list(paired[0]))
    convergence=[dict(algorithm=r['algorithm'],problem=r['problem'],seed=r['seed'],**t) for r in rows for t in r['convergence']]
    write_csv(derived/'convergence.csv',convergence,['algorithm','problem','seed','checkpoint_fraction','target_evaluations','n_eval','IGD','HV'])
    text=['# Đối chứng mới sáu thuật toán trên ZDT','',
        '**SMOKE: chỉ kiểm tra pipeline, không phải bằng chứng chất lượng.**' if cfg.get('smoke') else 'Chạy mới toàn bộ sáu thuật toán, không ghép dữ liệu từ bộ bảy thuật toán cũ.',
        f'{len(rows)} run hoàn tất; {sum(r["valid"] for r in rows)} hợp lệ. Holm chung {len(paired)} endpoint, alpha=0,05.',
        'IGD thấp/HV cao tốt. Ô là mean (best run), không hiển thị SD/Valid/Runtime; số liệu đầy đủ giữ trong CSV. Best tính riêng trên các lượt hợp lệ; IGD min/HV max có thể thuộc seed khác nhau. In đậm mean và best riêng theo từng bài, xác định từ số chưa làm tròn.',
        'GDE3/NSDE dùng pymoo, DE/rand/1/bin, F=0.5, CR=0.5, jitter gamma=1e-4, bounce-back repair, RankAndCrowding mặc định và cùng uniform input. OADE/CGDE không đổi. D-NSGA-II được đo trên bài tĩnh; không suy ra hiệu quả thích ứng môi trường động.',
        'Wilcoxon hai phía theo cặp seed, zero_method=wilcox, method=auto; all-zero p=1. Invalid pairs được loại và đếm; no-valid-pair endpoint giữ p=1 trong họ. NS không chứng minh tương đương. Không so runtime giữa những môi trường/worker khác nhau.', '']
    lookup={(s['problem'],s['algorithm']):s for s in summaries}
    order=[c['id'] for c in candidates if c['id']!='OADE_NSGAII']+['OADE_NSGAII']
    for metric in ('IGD','HV'):
        text += [f'## {metric} — mean (best)','', '| Bài | '+' | '.join(order)+' |','|---|'+'---:|'*len(order)]
        for p in cfg['problems']:
            group=[lookup[p['name'],a] for a in order];choose=min if metric=='IGD' else max
            best_key=metric+('_min' if metric=='IGD' else '_max')
            mean_values=[s[metric+'_mean'] for s in group if s[metric+'_mean'] is not None]
            best_values=[s[best_key] for s in group if s[best_key] is not None]
            cells=[]
            for s in group:
                vals=[]
                for key,values in [(metric+'_mean',mean_values),(best_key,best_values)]:
                    v=s[key];label=sci(v)
                    vals.append(f'**{label}**' if v is not None and v==choose(values) else label)
                cells.append(f'{vals[0]} ({vals[1]})')
            text.append('| '+p['name'].upper()+' | '+' | '.join(cells)+' |')
        text.append('')
    (derived/'report.md').write_text('\n'.join(text),encoding='utf-8')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='config/suites/zdt_six_fixed_oade.yaml')
    parser.add_argument('--stage',choices=('plan','run','report'),default='plan')
    parser.add_argument('--jobs',type=int);parser.add_argument('--out-dir',type=Path);parser.add_argument('--resume',action='store_true')
    args=parser.parse_args(argv);cfg,candidates=design(load_yaml_config(Path(args.config)))
    jobs=args.jobs if args.jobs is not None else cfg['global'].get('jobs',8)
    if jobs<1:parser.error('--jobs must be positive')
    if args.stage=='plan':
        print(json.dumps(dict(runs=len(engine.tasks(cfg,candidates)),algorithms=[c['id'] for c in candidates],jobs=jobs,
            endpoints=len(cfg['problems'])*5*2,population=cfg['global']['pop_size'],budget=cfg['global']['evaluation_budget'],
            out_dir=str(args.out_dir or cfg['global']['out_dir'])),indent=2));return
    if args.stage=='report' and not args.resume:raise ValueError('Report requires --resume')
    directory=(args.out_dir or repository_path(cfg['global']['out_dir'])).resolve()
    lock=ROOT/'tmp/study_locks'/digest(str(directory));lock.mkdir(parents=True,exist_ok=True)
    with session_lock(lock):
        current=engine.identity(cfg,candidates);current['kind']=STUDY_KIND
        manifest=engine.open_study(directory,current,args.resume)
        cfg={**cfg,'reference_fronts':engine.reference_fronts(directory,manifest,cfg)}
        if args.stage=='run':
            pending=len(engine.tasks(cfg,candidates))-len(manifest['artifacts'])
            if pending:
                manifest.setdefault('execution_sessions',[]).append(dict(jobs=jobs,pending_runs=pending))
                engine.atomic_json(directory/'study_manifest.json',manifest)
            engine.execute(directory,manifest,cfg,candidates,jobs,task_runner=run_task,
                order_seed=cfg['execution_order_seed'],progress_label='ZDT6')
        write_outputs(directory,manifest,cfg,candidates)
    print(f'Results: {directory}')


if __name__=='__main__':main()
