"""Extract the minimum-IGD OADE run on each ZDT problem, as requested.

Checks original checksums/objectives/metrics. Never runs an optimizer or plots.
"""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'results/experiments/zdt_six_fixed_oade_v1'
OUT=ROOT/'docs/reports/figures/oade_zdt_fronts_latest'


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()


def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    m=json.loads((D/'study_manifest.json').read_text())
    reference_path=D/'config/reference_fronts.json'
    assert hashlib.sha256(reference_path.read_bytes()).hexdigest()==m['reference_sha256']
    refs=json.loads(reference_path.read_text())
    with (D/'derived/raw_runs.csv').open() as f:
        runs=[r for r in csv.DictReader(f) if r['algorithm']=='OADE_NSGAII']
    selection=[]
    for p in ('zdt1','zdt2','zdt3','zdt4','zdt6'):
        group=[r for r in runs if r['problem']==p]
        assert len(group)==30 and all(r['valid'].lower()=='true' for r in group)
        best=min(group,key=lambda r:(float(r['IGD']),int(r['seed'])))
        selection.append((p,int(best['seed']),'best_igd'))
    points=[];metadata=[];hashes={}
    for i,(p,seed,rule) in enumerate(selection):
        name='primary/'+digest(['OADE_NSGAII',p,seed])+'.json';path=D/name
        data=path.read_bytes();assert hashlib.sha256(data).hexdigest()==m['artifacts'][name]
        r=json.loads(data);assert (r['problem'],r['algorithm'],r['seed'])==(p,'OADE_NSGAII',seed) and r['valid']
        problem=get_problem(p,n_var=10 if p in ('zdt4','zdt6') else 30)
        x=np.asarray(r['final_x']);f=np.asarray(r['final_f']);ref=np.asarray(refs[p])
        np.testing.assert_array_equal(problem.evaluate(x),f)
        assert abs(float(IGD(ref)(f))-r['IGD'])<1e-12
        assert abs(float(HV(ref_point=ref.max(0)+.1)(f))-r['HV'])<1e-12
        assert np.isfinite(f).all() and f.shape[1]==2
        panel='abcdef'[i]
        points.extend(dict(panel=panel,problem=p,seed=seed,selection=rule,individual=j,f1=float(v[0]),f2=float(v[1])) for j,v in enumerate(f))
        metadata.append(dict(panel=panel,problem=p,seed=seed,selection=rule,n_points=len(f),IGD=r['IGD'],HV=r['HV'],n_eval=r['n_eval']))
        hashes[name]=m['artifacts'][name]
    reference=[]
    for p,values in refs.items():
        if p not in ('zdt1','zdt2','zdt3','zdt4','zdt6'):continue
        ordered=sorted(values,key=lambda v:v[0]);segment=0
        dx=np.diff([v[0] for v in ordered]);positive=dx[dx>0]
        threshold=5*float(np.median(positive))
        for i,v in enumerate(ordered):
            if p=='zdt3' and i and v[0]-ordered[i-1][0]>threshold:segment+=1
            reference.append(dict(problem=p,segment=segment,point=i,f1=v[0],f2=v[1]))
        if p=='zdt3':assert segment==4,'Expected five disconnected ZDT3 components'
    write('solutions.source.csv',points);write('reference.source.csv',reference);write('panels.source.csv',metadata)
    (OUT/'extraction.json').write_text(json.dumps(dict(study='zdt_six_fixed_oade_v1',
        selection_rule='Minimum final IGD among all 30 OADE runs per problem; tie broken by smallest seed',
        selected_primary_hashes=hashes,reference_sha256=m['reference_sha256'],points=len(points),
        caveat='Best-case selection requested by user, not a typical run. Best IGD need not mean best HV. Stored final nondominated solution set, not unexported dominated population members. One run per panel, not 30-run uncertainty.'),indent=2))
    print(json.dumps(metadata,indent=2))


if __name__=='__main__':main()
