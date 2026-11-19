"""Audit current PDF exports and record input provenance, without plotting."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
HELPERS=ROOT/'.agents/skills/nature-figure/scripts'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for folder in ['zdt_six','oade_zdt_fronts_latest']:
        out=ROOT/'docs/reports/figures'/folder; rows=[]
        for pdf in sorted(out.glob('*.pdf')):
            def audit(script,args):
                r=subprocess.run([sys.executable,str(HELPERS/script),str(pdf),*args],capture_output=True,text=True,encoding='utf-8',check=True)
                return json.loads(r.stdout)
            text=audit('audit_pdf_text.py',['--min-pt','5','--json'])
            collisions=audit('audit_figure_collisions.py',['--json'])
            (out/(pdf.stem+'.text-audit.json')).write_text(json.dumps(text,indent=2),encoding='utf-8')
            (out/(pdf.stem+'.collision-audit.json')).write_text(json.dumps(collisions,indent=2),encoding='utf-8')
            assert text['below_minimum_count']==0
            assert collisions['summary']['fail']==collisions['summary']['warn']==0,(pdf,collisions['summary'])
            assert '<text' in pdf.with_suffix('.svg').read_text(encoding='utf-8')
            assert pdf.with_suffix('.png').stat().st_size>10000
            rows.append(dict(figure=pdf.stem,pdf_sha256=sha(pdf),minimum_font_pt=text['minimum_found_pt'],collision_summary=collisions['summary']))
        assert len(rows)==(5 if folder=='zdt_six' else 6),(folder,len(rows))
        provenance={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'results/experiments/zdt_six_fixed_oade_v1/derived').glob('audited_*.csv')}
        if folder=='oade_zdt_fronts_latest':provenance['extraction.json']=sha(out/'extraction.json')
        (out/'export_audit.json').write_text(json.dumps(dict(figures=rows,inputs=provenance,scope='PDF text/collision and SVG checks; visual review recorded in QA.md. Base PDF editable text verified; preferred cairo device static exception.'),indent=2),encoding='utf-8')
        print(folder,':',len(rows),'PDF exports passed',flush=True)
if __name__=='__main__':main()
