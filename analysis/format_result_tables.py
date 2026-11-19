"""Render quality cells as central (best run), from unrounded run data."""
import csv
from collections import defaultdict
from pathlib import Path
import re
from result_display import sci
from highlight_result_tables import cells

ROOT=Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def main():
    benchmark=ROOT/'results/experiments/zdt_seven_fixed_oade_v2/derived'
    summaries={(r['problem'],r['algorithm']):r for r in read(benchmark/'audited_summary.csv')}
    runs=defaultdict(list)
    for r in read(benchmark/'raw_runs.csv'):
        if r['valid'].lower()=='true':runs[r['problem'],r['algorithm']].append(r)
    extrema={(p,a,m):(min if m=='IGD' else max)(float(r[m]) for r in group)
             for (p,a),group in runs.items() for m in ('IGD','HV')}
    sensitivity=read(ROOT/'results/experiments/mechanism_sensitivity_v1/derived/audited_summary.csv')
    sens={(r['problem'],r['algorithm']):r for r in sensitivity}
    contrasts=read(ROOT/'results/experiments/mechanism_sensitivity_v1/derived/audited_comparisons.csv')
    def mark(v,win):return f'**{sci(v)}**' if win else sci(v)
    def bench_cell(problem,algorithm,metric,stat):
        center=float(summaries[problem,algorithm][f'{metric}_{stat}']);best=extrema[problem,algorithm,metric]
        choose=min if metric=='IGD' else max
        center_winner=choose(float(r[f'{metric}_{stat}']) for (p,a),r in summaries.items() if p==problem)
        best_winner=choose(v for (p,a,m),v in extrema.items() if p==problem and m==metric)
        return f'{mark(center,center==center_winner)} ({mark(best,best==best_winner)})'
    paths=[ROOT/'README.md',ROOT/'README.vi.md',ROOT/'docs/reports/zdt_seven_fixed_oade_v2_report.md',benchmark/'report.md']
    for path in paths:
        lines=path.read_text(encoding='utf-8').splitlines();out=[];problem=None;i=0
        while i<len(lines):
            heading=re.match(r'^### (ZDT[12346])$',lines[i])
            if heading:problem=heading[1].lower()
            if not lines[i].startswith('|') or i+1==len(lines) or not re.match(r'^\|[ :|-]+\|$',lines[i+1]):
                out.append(lines[i]);i+=1;continue
            end=i+2
            while end<len(lines) and lines[end].startswith('|'):end+=1
            header=cells(lines[i]);rows=[cells(s) for s in lines[i+2:end]]
            algorithm_col=next((j for j,h in enumerate(header) if h in ('Algorithm','Thuật toán')),None)
            quality_cols=[j for j,h in enumerate(header) if h.startswith(('IGD','HV')) and '%' not in h]
            if algorithm_col is not None:
                for row in rows:
                    p=row[0].lower() if header[0] in ('Bài','Problem') else problem
                    for j in quality_cols:
                        metric='IGD' if header[j].startswith('IGD') else 'HV'
                        stat='median' if 'median' in header[j].lower() else 'mean'
                        row[j]=bench_cell(p,row[algorithm_col],metric,stat)
                for j in quality_cols:
                    metric='IGD' if header[j].startswith('IGD') else 'HV'
                    stat='median' if 'median' in header[j].lower() else 'mean'
                    header[j]=f'{metric} {"↓" if metric=="IGD" else "↑"} {stat} (best)'
            elif any('→' in c for row in rows for c in row) and any('median' in h.lower() and h.startswith('IGD') for h in header):
                for row in rows:
                    p=row[0].lower();label=row[1].lower()
                    parameter='obl_jump_rate' if 'obl' in label else 'mean_F' if 'mean f' in label else 'mean_CR' if 'mean cr' in label else 'prob_de'
                    level=.05 if parameter=='obl_jump_rate' else .5 if parameter=='mean_F' else .3 if parameter=='mean_CR' else .8
                    for j in quality_cols:
                        metric='IGD' if header[j].startswith('IGD') else 'HV'
                        r=next(r for r in contrasts if r['problem']==p and r['parameter']==parameter and float(r['level'])==level and r['metric']==metric)
                        ids=(r['reference_algorithm'],r['comparison_algorithm']);values=[sens[p,a] for a in ids]
                        k=f'{metric}_median';b=f'{metric}_{"min" if metric=="IGD" else "max"}'
                        choose=min if metric=='IGD' else max
                        central=choose(float(v[k]) for v in values);best=choose(float(v[b]) for v in values)
                        row[j]=' → '.join(f'{mark(v[k],float(v[k])==central)} ({mark(v[b],float(v[b])==best)})' for v in values)
                for j in quality_cols:header[j]=header[j].replace('median','median (best)') if '(best)' not in header[j] else header[j]
            out+=['| '+' | '.join(header)+' |',lines[i+1]]+['| '+' | '.join(row)+' |' for row in rows]
            i=end
        path.write_text('\n'.join(out)+'\n',encoding='utf-8')
        print(path.relative_to(ROOT))


if __name__=='__main__':main()
