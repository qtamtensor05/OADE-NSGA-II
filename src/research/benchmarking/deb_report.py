"""Export additional comparison tables from existing per-run objective evidence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile
import numpy as np
from .deb_metrics import convergence_metric, diversity_metric, zdt_reference


def write_xlsx(path, sheets):
    """Dependency-free OOXML export for the repeatable Python reporting CLI."""
    with ZipFile(path, 'w') as z:
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(sheets)+1))+'</Types>')
        z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,_) in enumerate(sheets,1))+'</sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+'</Relationships>')
        for i,(_,rows) in enumerate(sheets,1):
            body = ''.join('<row>'+''.join(f'<c><v>{v}</v></c>' if isinstance(v,(int,float)) else '<c t="inlineStr"><is><t>'+escape(str(v if v is not None else 'N/A'))+'</t></is></c>' for v in row)+'</row>' for row in rows)
            z.writestr(f'xl/worksheets/sheet{i}.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+body+'</sheetData></worksheet>')


def export_tables(rows, directory, cfg):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    problems = [p['name'] for p in cfg['problems']]
    refs = {}; reasons = {}
    for name in problems:
        try:
            refs[name] = zdt_reference(name)
        except ValueError as exc:
            reasons[name] = str(exc)
    detailed = []; seen = set()
    for r in rows:
        key = (r['algorithm'],r['problem'],r['seed'])
        if key in seen:
            raise ValueError('Duplicate algorithm/problem/seed')
        seen.add(key)
        name = r['problem']; u = d = None
        status = 'invalid_run' if not r['valid'] else reasons.get(name, 'ok')
        if status == 'ok':
            ref, extremes = refs[name]
            u = convergence_metric(r['final_f'], ref)
            d = diversity_metric(r['final_f'], extremes)
            if u is None or d is None:
                status = 'undefined_empty_or_degenerate_front'
        detailed.append(dict(algorithm=r['algorithm'], benchmark=name, encoding='real', seed=r['seed'],
                             generations=r.get('n_gen'), population_size=cfg['global']['pop_size'],
                             n_eval=r['n_eval'], evaluation_budget=r['evaluation_budget'],
                             upsilon=u, delta=d, runtime_seconds=r['runtime_seconds'], status=status))
    def save_csv(name, matrix):
        with (directory/name).open('w',encoding='utf-8',newline='') as f:
            csv.writer(f).writerows(matrix)
    detail_matrix = [list(detailed[0])] + [list(r.values()) for r in detailed] if detailed else [['algorithm']]
    save_csv('detailed_run_results.csv', detail_matrix)
    sheets=[]; markdown=['# Deb (2002) performance metrics', '',
        'Raw objective Euclidean distance; H=500; population variance (ddof=0) across valid run metrics. Lower is better.',
        'N/A means missing/invalid/undefined. Counts are reported separately for each metric. Generations are N/A when not recorded; n_eval is authoritative.',
        'Analytical ZDT fronts sampled approximately uniformly by arc length; ZDT3 gaps excluded from reference sampling. Delta still includes gaps between obtained consecutive points.', '']
    for metric, filename, title in [('upsilon','convergence_metric_results','TABLE II: Convergence Upsilon'),('delta','diversity_metric_results','TABLE III: Diversity Delta')]:
        matrix=[['Algorithm / statistic']+[p.upper() for p in problems]]
        for alg in sorted({r['algorithm'] for r in rows}):
            groups=[[r[metric] for r in detailed if r['algorithm']==alg and r['benchmark']==p and r[metric] is not None] for p in problems]
            for label, fn in [('Mean', np.mean), ('Variance', lambda x: np.var(x,ddof=0)), ('Valid runs',len)]:
                matrix.append([alg+' '+label]+[float(fn(g)) if g else ('N/A' if label!='Valid runs' else 0) for g in groups])
        save_csv(filename+'.csv',matrix); sheets.append((metric,matrix))
        markdown += ['## '+title, '', '| '+' | '.join(matrix[0])+' |', '| '+' | '.join(['---']*len(matrix[0]))+' |']
        markdown += ['| '+' | '.join(f'{v:.8g}' if isinstance(v,float) else str(v) for v in row)+' |' for row in matrix[1:]]
        markdown.append('')
        latex=['\\begin{table*}[t]', '\\centering', '\\caption{'+title+' (population variance; valid runs reported).}', '\\begin{tabular}{l'+'r'*len(problems)+'}', '\\hline']
        latex += [' & '.join(str(v).replace('_',r'\_') for v in row)+r' \\' for row in matrix]
        latex += ['\\hline', '\\end{tabular}', '\\end{table*}']
        (directory/(filename+'.tex')).write_text('\n'.join(latex),encoding='utf-8')
    sheets.append(('Runs',detail_matrix)); write_xlsx(directory/'experimental_results.xlsx',sheets)
    (directory/'deb_metrics.md').write_text('\n'.join(markdown),encoding='utf-8')
    (directory/'deb_reference_fronts.json').write_text(json.dumps({k:{'points':v[0].tolist(),'extremes':v[1].tolist(),'sha256':hashlib.sha256(v[0].tobytes()).hexdigest()} for k,v in refs.items()},indent=2),encoding='utf-8')
    return detailed


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study',type=Path,required=True)
    args=parser.parse_args(argv)
    from research.studies.zdt_sensitivity import load_records
    manifest=json.loads((args.study/'study_manifest.json').read_text(encoding='utf-8'))
    cfg=manifest['protocol']
    for name, checksum in manifest['artifacts'].items():
        if hashlib.sha256((args.study/name).read_bytes()).hexdigest() != checksum:
            raise ValueError('Primary evidence checksum mismatch: '+name)
    rows=load_records(args.study,manifest)
    from research.studies.zdt_sensitivity import validate_records, reference_fronts
    cfg={**cfg, 'reference_fronts':reference_fronts(args.study,manifest,cfg)}
    validate_records(cfg,manifest['candidates'],rows,complete=True)
    export_tables(rows,args.study/'derived/deb_metrics',cfg)
