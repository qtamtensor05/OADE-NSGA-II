"""Independent audit of six-solver primary evidence; no optimization executed."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import platform
import zipfile
import numpy as np
import scipy
from scipy.stats import wilcoxon,rankdata
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'results/experiments/zdt_six_fixed_oade_v1'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()


def read(name):
    with (D/'derived'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def write(name,rows):
    with (D/'derived'/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    manifest_hash=sha(D/'study_manifest.json');m=json.loads((D/'study_manifest.json').read_text())
    cfg=m['protocol'];g=cfg['global'];names=[c['id'] for c in m['candidates']]
    assert m['kind']=='zdt_six_fixed_oade_v1'
    assert set(names)=={'OADE_NSGAII','NSGA2','DNSGA2','CGDE_NSGAII','GDE3','NSDE'}
    assert cfg['baseline_revision']=='pymoo_de_baselines_2026_11_19'
    changed=[p for p,h in m['source_hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    # Maintenance may remove unused code after execution. Verify historical bytes
    # against the original manifest, never replace its hashes with current ones.
    if changed:
        with zipfile.ZipFile(D/'config/execution_sources.zip') as archive:
            for p in changed:
                assert hashlib.sha256(archive.read(p)).hexdigest()==m['source_hashes'][p],p
    assert sha(D/'config/reference_fronts.json')==m['reference_sha256']
    refs=json.loads((D/'config/reference_fronts.json').read_text())
    assert set(m['artifacts'])=={p.relative_to(D).as_posix() for p in (D/'primary').glob('*.json')}
    records=[];max_objective=max_metric=0.
    for name,h in m['artifacts'].items():
        data=(D/name).read_bytes();assert hashlib.sha256(data).hexdigest()==h,name
        records.append(json.loads(data))
    lookup={(r['problem'],r['algorithm'],r['seed']):r for r in records}
    expected={(p['name'],a,s) for p in cfg['problems'] for a in names for s in g['seeds']}
    assert len(records)==len(lookup)==len(expected)==900 and set(lookup)==expected
    for p in cfg['problems']:
        problem=get_problem(p['name'],n_var=p['n_var']);ref=np.asarray(refs[p['name']])
        np.testing.assert_array_equal(ref,problem.pareto_front())
        for seed in g['seeds']:
            initial=np.random.default_rng(seed).uniform(problem.xl,problem.xu,size=(g['pop_size'],p['n_var']))
            for a in names:
                r=lookup[p['name'],a,seed]
                assert r['settings']==next(c['settings'] for c in m['candidates'] if c['id']==a)
                assert r['run_idx']==seed-g['seed_base'] and r['n_obj']==2 and r['n_var']==p['n_var']
                assert 0<r['n_eval']<=g['evaluation_budget']
                assert r['initial_x_sha256']==digest(initial.tolist()) and r['reference_sha256']==digest(ref.tolist())
                x=np.asarray(r['final_x']);f=np.asarray(r['final_f'])
                assert x.shape==(len(f),p['n_var']) and f.shape==(len(x),2)
                assert np.isfinite(x).all() and np.isfinite(f).all() and ((x>=problem.xl)&(x<=problem.xu)).all()
                err=float(np.max(abs(problem.evaluate(x)-f)));max_objective=max(max_objective,err);assert err<1e-10
                assert not ((f[:,None]<=f[None,:]).all(2)&(f[:,None]<f[None,:]).any(2)).any()
                if r['valid']:
                    assert len(np.unique(f,axis=0))>1
                    for metric,value in [('IGD',IGD(ref)(f)),('HV',HV(ref_point=ref.max(0)+.1)(f))]:
                        err=abs(float(value)-r[metric]);max_metric=max(max_metric,err);assert err<1e-10
                else:
                    assert (a,p['name'],seed)==('CGDE_NSGAII','zdt4',63)
                    assert len(np.unique(f,axis=0))==1 and r['IGD'] is None and r['HV'] is None
                assert all(0<t['n_eval']<=g['evaluation_budget'] for t in r['convergence'])
    raw=read('raw_runs.csv');assert len(raw)==900
    for r in raw:
        original=lookup[r['problem'],r['algorithm'],int(r['seed'])]
        assert r['valid'].lower()==str(original['valid']).lower()
        for k in ('n_eval','runtime_seconds','IGD','HV'):
            assert (r[k]=='' and original[k] is None) or float(r[k])==original[k]
    summaries=[]
    for p in cfg['problems']:
        for a in names:
            group=[lookup[p['name'],a,s] for s in g['seeds']];valid=[r for r in group if r['valid']]
            row=dict(problem=p['name'],algorithm=a,runs=len(group),valid_runs=len(valid),invalid_runs=len(group)-len(valid),zero_hv_runs=sum(r['HV']==0 for r in valid))
            for metric in ('IGD','HV','runtime_seconds','n_eval'):
                values=np.asarray([r[metric] for r in (valid if metric in ('IGD','HV') else group)])
                for label,fn in [('mean',np.mean),('sd',lambda v:np.std(v,ddof=1)),('median',np.median),('min',np.min),('max',np.max)]:
                    row[metric+'_'+label]=float(fn(values))
            summaries.append(row)
    previous={(r['problem'],r['algorithm']):r for r in read('summary.csv')};assert len(previous)==30
    for r in summaries:
        for k,v in r.items():
            if k in previous[r['problem'],r['algorithm']] and isinstance(v,(int,float)):
                assert np.isclose(v,float(previous[r['problem'],r['algorithm']][k]),rtol=1e-12,atol=1e-14)
    rng=np.random.default_rng(20261119);comparisons=[]
    for p in cfg['problems']:
        for a in names:
            if a=='OADE_NSGAII':continue
            seeds=[s for s in g['seeds'] if lookup[p['name'],a,s]['valid'] and lookup[p['name'],'OADE_NSGAII',s]['valid']]
            for metric in ('IGD','HV'):
                ref=np.array([lookup[p['name'],'OADE_NSGAII',s][metric] for s in seeds]);alt=np.array([lookup[p['name'],a,s][metric] for s in seeds])
                delta=ref-alt;benefit=-delta if metric=='IGD' else delta;nz=benefit[benefit!=0];ranks=rankdata(abs(nz))
                effect=float(np.sum(ranks*np.sign(nz))/sum(ranks)) if len(nz) else 0.
                stat,pvalue=(0.,1.) if not np.any(delta) else wilcoxon(delta,zero_method='wilcox',alternative='two-sided',method='auto')
                bootstrap=np.median(delta[rng.integers(0,len(delta),size=(20000,len(delta)))],axis=1)
                lo,hi=np.quantile(bootstrap,[.025,.975])
                comparisons.append(dict(problem=p['name'],metric=metric,reference_algorithm='OADE_NSGAII',comparison_algorithm=a,n_pairs=len(seeds),excluded_pairs=len(g['seeds'])-len(seeds),
                    reference_mean=float(ref.mean()),comparison_mean=float(alt.mean()),reference_median=float(np.median(ref)),comparison_median=float(np.median(alt)),
                    median_paired_difference=float(np.median(delta)),ci_low=float(lo),ci_high=float(hi),statistic=float(stat),p_value=float(pvalue),rank_biserial_effect=effect,
                    reference_wins=int(sum(benefit>0)),comparison_wins=int(sum(benefit<0)),ties=int(sum(benefit==0))))
    running=0.
    for rank,i in enumerate(sorted(range(50),key=lambda i:comparisons[i]['p_value'])):
        r=comparisons[i];running=max(running,min(1.,(50-rank)*r['p_value']))
        r['p_adjusted_holm']=running;r['result']=('reference_better' if r['rank_biserial_effect']>0 else 'comparison_better') if running<.05 else 'no_significant_difference'
    old={(r['problem'],r['metric'],r['comparison_algorithm']):r for r in read('comparisons.csv')};assert len(old)==50
    for r in comparisons:
        o=old[r['problem'],r['metric'],r['comparison_algorithm']]
        for k in ('n_pairs','excluded_pairs','reference_mean','comparison_mean','median_paired_difference','statistic','p_value','rank_biserial_effect','p_adjusted_holm'):
            assert np.isclose(r[k],float(o[k]),rtol=1e-12,atol=1e-14),(r,k,o[k])
        assert r['result']==o['result']
    assert sha(D/'study_manifest.json')==manifest_hash
    write('audited_summary.csv',summaries);write('audited_comparisons.csv',comparisons)
    write('audited_raw_runs.csv',[{k:r[k] for k in ('problem','algorithm','seed','valid','n_eval','runtime_seconds','IGD','HV')} for r in records])
    audit=dict(records=900,valid_runs=sum(r['valid'] for r in records),validity_counts=dict(Counter(r['validation_status'] for r in records)),
        primary_checksums_verified=900,source_hashes_verified=len(m['source_hashes']),summary_rows_verified=30,comparison_rows_verified=50,
        source_snapshot_files_verified=len(changed),
        paired_initialization_blocks_verified=150,max_objective_error=max_objective,max_metric_error=max_metric,
        total_evaluations=sum(r['n_eval'] for r in records),manifest_sha256=manifest_hash,results=dict(Counter(r['result'] for r in comparisons)),
        bootstrap=dict(seed=20261119,resamples=20000,unit='paired seed within problem and comparison',interval='percentile 95%, marginal not multiplicity-adjusted'),
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        scope='Independent calculation path using the same analyst and pymoo objective/indicator libraries; no solver rerun or full transition trace audit.')
    (D/'derived/audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps(audit,indent=2))


if __name__=='__main__':main()
