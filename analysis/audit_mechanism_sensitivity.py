"""Independent read-only-primary audit of the completed parameter-level study.

No solver or pipeline statistics helper is called. New audited derivatives only.
"""
from pathlib import Path
from collections import Counter, defaultdict
import ast
import csv
import hashlib
import json
import platform
import numpy as np
import scipy
from scipy.stats import rankdata, wilcoxon
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'results/experiments/mechanism_sensitivity_v1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def write(name,rows):
    with (D/'derived'/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    manifest_hash=sha(D/'manifest.json')
    m=json.loads((D/'manifest.json').read_text()); protocol=m['protocol']; cfg=protocol['config']
    for name,h in protocol['sources'].items():
        assert sha(ROOT/name)==h,name
    for history in m.get('io_recovery_history',[]):
        old=D/history['previous_source_snapshot']; current=ROOT/history['source']
        assert sha(old)==history['previous_source_sha256']
        assert sha(current)==history['new_source_sha256']
        def stripped(path):
            tree=ast.parse(path.read_text(encoding='utf-8'))
            tree.body=[n for n in tree.body if not isinstance(n,ast.FunctionDef) or n.name!='atomic_json']
            return ast.dump(tree,include_attributes=False)
        assert stripped(old)==stripped(current)
    candidates={c['id']:c for c in protocol['candidates']}
    expected={(p,c,s) for p in cfg['problems'] for c in candidates for s in cfg['seeds']}
    assert len(expected)==2100 and len(protocol['contrasts'])==31
    assert set(m['artifacts'])=={p.name for p in (D/'primary').glob('*.json')}
    lookup={}; activations=[]; blocks={}; max_f=max_metric=0.; total_fe=0
    for name,h in m['artifacts'].items():
        data=(D/'primary'/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==h,name
        r=json.loads(data); key=(r['problem'],r['algorithm'],r['seed'])
        assert key in expected and key not in lookup
        assert name==f'{key[0]}_{key[2]}_{key[1]}.json'
        c=candidates[key[1]]; assert r['candidate']==c and r['run_idx']==r['seed']
        assert r['execution_jobs']==8 and 0<r['n_eval']<=cfg['budget']
        assert r['valid']; total_fe+=r['n_eval']
        problem=get_problem(key[0],n_var=10); ref=np.asarray(protocol['references'][key[0]])
        np.testing.assert_array_equal(ref,problem.pareto_front())
        assert r['reference_sha256']==digest(ref.tolist())
        x=np.asarray(r['final_x']); f=np.asarray(r['final_f'])
        assert x.shape==(len(f),10) and f.shape==(len(x),2) and np.isfinite(x).all() and np.isfinite(f).all()
        assert ((x>=problem.xl)&(x<=problem.xu)).all() and len(np.unique(f,axis=0))>1
        assert not ((f[:,None]<=f[None,:]).all(2)&(f[:,None]<f[None,:]).any(2)).any()
        err=float(np.max(abs(problem.evaluate(x)-f))); max_f=max(max_f,err); assert err<1e-10
        for metric,value in [('IGD',IGD(ref)(f)),('HV',HV(ref_point=ref.max(0)+.1)(f))]:
            err=abs(float(value)-r[metric]);max_metric=max(max_metric,err);assert err<1e-10
        block=(key[0],key[2]);blocks.setdefault(block,r['initial_x_sha256']);assert blocks[block]==r['initial_x_sha256']
        if c['mode']=='held':
            field='pde' if c['parameter']=='prob_de' else c['parameter']
            assert all(t[field]==c['level'] for t in r['trace'])
        for mech in ('obl','restart'):
            events=[e for e in r['events'] if e['mechanism']==mech]
            assert all(e['status'] in ('completed','budget_blocked') and 0<=e['evaluations']<=r['n_eval'] for e in events)
            activations.append(dict(problem=key[0],algorithm=key[1],seed=key[2],mechanism=mech,
                completed=sum(e['status']=='completed' for e in events),
                budget_blocked=sum(e['status']=='budget_blocked' for e in events),
                evaluations=sum(e['evaluations'] for e in events)))
        lookup[key]={k:r[k] for k in ('problem','algorithm','seed','run_idx','valid','n_eval','runtime_seconds','IGD','HV')}
    assert set(lookup)==expected
    raw=read_csv(D/'derived/runs.csv'); assert len(raw)==2100
    for row in raw:
        r=lookup[row['problem'],row['algorithm'],int(row['seed'])]
        for k in ('IGD','HV','n_eval','runtime_seconds','run_idx'):
            assert float(row[k])==r[k]
        assert row['valid'].lower()=='true'
    summaries=[]
    for p in cfg['problems']:
        for a,c in candidates.items():
            group=[lookup[p,a,s] for s in cfg['seeds']]
            row=dict(problem=p,algorithm=a,parameter=c['parameter'],level=c['level'],mode=c['mode'],runs=len(group),valid_runs=len(group),
                runtime_median=float(np.median([r['runtime_seconds'] for r in group])),
                n_eval_min=min(r['n_eval'] for r in group),n_eval_max=max(r['n_eval'] for r in group))
            for metric in ('IGD','HV'):
                values=np.array([r[metric] for r in group])
                for stat,func in [('mean',np.mean),('sd',lambda v:np.std(v,ddof=1)),('median',np.median),
                                  ('q1',lambda v:np.quantile(v,.25)),('q3',lambda v:np.quantile(v,.75)),('min',np.min),('max',np.max)]:
                    row[metric+'_'+stat]=float(func(values))
            summaries.append(row)
    rng=np.random.default_rng(20261119); comparisons=[]
    for contrast in protocol['contrasts']:
        for p in cfg['problems']:
            for metric in ('IGD','HV'):
                ref=np.array([lookup[p,contrast['reference'],s][metric] for s in cfg['seeds']])
                alt=np.array([lookup[p,contrast['candidate'],s][metric] for s in cfg['seeds']])
                delta=ref-alt; benefit=-delta if metric=='IGD' else delta
                nz=benefit[benefit!=0]; ranks=rankdata(abs(nz))
                effect=float(np.sum(ranks*np.sign(nz))/sum(ranks)) if len(nz) else 0.
                stat,pv=(0.,1.) if not np.any(delta) else wilcoxon(delta,zero_method='wilcox',alternative='two-sided',method='auto')
                sample=rng.integers(0,len(delta),size=(20000,len(delta)))
                low,high=np.quantile(np.median(delta[sample],axis=1),[.025,.975])
                comparisons.append(dict(problem=p,parameter=contrast['parameter'],level=contrast['level'],mode=contrast['mode'],metric=metric,
                    reference_algorithm=contrast['reference'],comparison_algorithm=contrast['candidate'],n_pairs=len(delta),excluded_pairs=0,
                    reference_mean=float(ref.mean()),comparison_mean=float(alt.mean()),reference_median=float(np.median(ref)),comparison_median=float(np.median(alt)),
                    median_paired_difference=float(np.median(delta)),ci_low=float(low),ci_high=float(high),
                    statistic=float(stat),p_value=float(pv),rank_biserial_effect=effect,
                    reference_wins=int(sum(benefit>0)),level_wins=int(sum(benefit<0)),ties=int(sum(benefit==0))))
    assert len(comparisons)==124
    running=0.
    for rank,i in enumerate(sorted(range(124),key=lambda i:comparisons[i]['p_value'])):
        r=comparisons[i];running=max(running,min(1.,(124-rank)*r['p_value']))
        r['p_adjusted_holm']=running;r['result']=('reference_better' if r['rank_biserial_effect']>0 else 'level_better') if running<.05 else 'not_significant'
    old=read_csv(D/'derived/comparisons.csv');assert len(old)==124
    previous={(r['problem'],r['parameter'],float(r['level']),r['metric']):r for r in old}
    for r in comparisons:
        o=previous[r['problem'],r['parameter'],r['level'],r['metric']]
        for k in ('n_pairs','excluded_pairs','reference_mean','comparison_mean','median_paired_difference','statistic','p_value','rank_biserial_effect','p_adjusted_holm'):
            assert np.isclose(r[k],float(o[k]),rtol=1e-12,atol=1e-14),(r,k,o[k])
        assert r['result']==o['result']
    old_summary=read_csv(D/'derived/summary.csv');assert len(old_summary)==70
    previous={(r['problem'],r['algorithm']):r for r in old_summary}
    for r in summaries:
        for k,v in r.items():
            if k in previous[r['problem'],r['algorithm']] and isinstance(v,(int,float)):
                assert np.isclose(v,float(previous[r['problem'],r['algorithm']][k]),rtol=1e-12,atol=1e-14)
    old_activation=read_csv(D/'derived/activation.csv');assert len(old_activation)==4200
    previous={(r['problem'],r['algorithm'],int(r['seed']),r['mechanism']):r for r in old_activation}
    for r in activations:
        o=previous[r['problem'],r['algorithm'],r['seed'],r['mechanism']]
        for k in ('completed','budget_blocked','evaluations'):assert int(o[k])==r[k]
    activation_summary=[]
    for p,a,mech in sorted({(r['problem'],r['algorithm'],r['mechanism']) for r in activations}):
        group=[r for r in activations if (r['problem'],r['algorithm'],r['mechanism'])==(p,a,mech)]
        c=candidates[a]
        activation_summary.append(dict(problem=p,algorithm=a,parameter=c['parameter'],level=c['level'],mode=c['mode'],mechanism=mech,
            runs=30,active_runs=sum(r['completed']>0 for r in group),completed=sum(r['completed'] for r in group),
            budget_blocked=sum(r['budget_blocked'] for r in group),evaluations=sum(r['evaluations'] for r in group)))
    write('audited_summary.csv',summaries);write('audited_comparisons.csv',comparisons);write('audited_activation_summary.csv',activation_summary)
    assert sha(D/'manifest.json')==manifest_hash
    audit=dict(records=2100,valid_runs=2100,source_hashes_verified=len(protocol['sources']),primary_checksums_verified=2100,
        summaries_verified=70,comparisons_verified=124,activation_rows_verified=4200,max_objective_error=max_f,max_metric_error=max_metric,
        total_evaluations=total_fe,manifest_sha256=manifest_hash,results=dict(Counter(r['result'] for r in comparisons)),
        bootstrap=dict(seed=20261119,resamples=20000,unit='paired seed within problem and contrast',interval='percentile 95%; marginal, not multiplicity-adjusted'),
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        scope='Independent analysis path, same analyst and pymoo objective/indicator implementation; not an independent solver rerun. Initial hashes agree within blocks, not reconstructed. I/O-only source migration checked by AST. Raw events/trace CSV not exhaustively audited.')
    (D/'derived/audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps(audit,indent=2))


if __name__=='__main__':main()
