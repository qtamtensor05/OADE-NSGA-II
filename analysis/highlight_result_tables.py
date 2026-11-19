"""Bold descriptive best central values in existing Markdown result tables.

Never rank p-values, SDs, CIs, event counts or effects across unrelated contrasts.
"""
from pathlib import Path
from decimal import Decimal
import re

ROOT=Path(__file__).resolve().parents[1]
NUMBER=re.compile(r'[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?')


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def number(cell):
    match=NUMBER.match(cell.replace('**',''))
    return Decimal(match[0].replace(',','.')) if match else None


def bold_center(cell):
    cell=cell.replace('**','')
    match=NUMBER.match(cell)
    return '**'+match[0]+'**'+cell[match.end():]


def format_table(lines):
    header=cells(lines[0]); data=[cells(line) for line in lines[2:]]
    if not data or any(len(row)!=len(header) for row in data):return lines
    columns=[i for i,h in enumerate(header) if h.startswith(('IGD','HV','Runtime','Median runtime'))]
    # Keep inferential tables untouched. A descriptive quality column must
    # begin with a number; no p-value/CI/effect is assigned a "best" rank.
    for col in columns:
        if '%' in header[col] or any(term in header[col].lower() for term in ('giảm','tăng','reduction','increase')):
            for row in data:row[col]=row[col].replace('**','')
            continue
        if not all(number(row[col]) is not None for row in data):continue
        maximize=header[col].startswith('HV')
        if all('→' in row[col] for row in data):
            for row in data:
                pair=[s.strip().replace('**','') for s in row[col].split('→')]
                if len(pair)!=2 or any(number(s) is None for s in pair):continue
                target=(max if maximize else min)(number(s) for s in pair)
                row[col]=' → '.join(bold_center(s) if number(s)==target else s for s in pair)
        elif header[col].startswith('IGD OADE /'):
            for row in data:
                pair=[s.strip().replace('**','') for s in row[col].split('/')]
                if len(pair)!=2:continue
                target=min(number(s) for s in pair)
                row[col]=' / '.join(bold_center(s) if number(s)==target else s for s in pair)
        elif any('→' in row[col] or '/' in row[col] for row in data):
            continue
        else:
            # Separate repeated problems in a single table. Otherwise the
            # surrounding table/heading already defines one problem.
            by_problem=header[0] in ('Bài','Problem')
            groups={row[0] if by_problem else 'table' for row in data}
            for group in groups:
                subset=[row for row in data if (row[0] if by_problem else 'table')==group]
                target=(max if maximize else min)(number(row[col]) for row in subset)
                for row in subset:
                    row[col]=row[col].replace('**','')
                    if number(row[col])==target:row[col]=bold_center(row[col])
    output=lines[:2]+['| '+' | '.join(row)+' |' for row in data]
    # Formatting may add emphasis only; never alter a displayed value.
    assert [line.replace('**','') for line in lines]==[line.replace('**','') for line in output]
    return output


def main():
    # The source-backed formatter preserves unrounded winners after compact
    # scientific display and adds the requested per-run extrema.
    from format_result_tables import main as render
    render()


if __name__=='__main__':main()
