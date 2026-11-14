"""Controlled comparison of fixed and success-rate pDE."""
import json

from shared.io.csv_io import write_csv
from . import restart_comparison as base


def design(cfg):
    # Reuse validation of populations, seeds and supported problem families.
    common = cfg['common_settings']
    controlled = {'probability_update_mode','enable_probability_adaptation'}
    if controlled & set(common):
        raise ValueError('Probability switches are controlled by the study')
    if not 0.2 <= common.get('prob_de',.5) <= .8:
        raise ValueError('Initial pDE must be in [0.2, 0.8]')
    probe = json.loads(json.dumps(cfg))
    for k in ('restart_mode','restart_elite_ratio','enable_restart'):
        probe['common_settings'].pop(k,None)
    base.design(probe)
    modes = cfg.get('probability_modes', ['fixed','success_rate'])
    if len(modes) != 2 or set(modes) != {'fixed','success_rate'}:
        raise ValueError('Choose fixed and success_rate')
    candidates = [dict(id=mode, parameter='probability_update_mode', level=mode,
                       settings={**common,'pop_size':cfg['global']['pop_size'],
                                 'enable_probability_adaptation':True,
                                 'probability_update_mode':mode})
                  for mode in modes]
    return cfg,candidates


def write_outputs(directory,manifest,cfg,candidates):
    base.write_outputs(directory,manifest,cfg,candidates)
    rows = base.engine.load_records(directory,manifest)
    trace = [{k:r[k] for k in ('candidate','problem','seed')} | t
             for r in rows for t in r['probability_trace']]
    fields = ['candidate','problem','seed','generation','n_eval','mode','enabled','n_de','n_sbx',
              'success_de','success_sbx','target','prob_before','prob_after']
    write_csv(directory/'derived/probability_trace.csv',trace,fields)
    text = ['# Probability adaptation ablation','',
            '**SMOKE only; not evidence of improvement.**' if cfg.get('smoke') else 'Paired seed-controlled measurements.',
            f'Runs: {len(rows)}; invalid: {sum(not r["valid"] for r in rows)}.', '',
            'Only probability_update_mode differs: ' + ', '.join(c['id'] for c in candidates) + '.',
            'Success: nondominated in the complete evaluated parent/offspring pool before deduplication. Each trial counts once. OBL/initial/restart individuals are not DE/SBX trials but can dominate trials.',
            'rDE=sDE/nDE; rSBX=sSBX/nSBX; q=rDE/(rDE+rSBX); p <- clip(0.9*p+0.1*q,0.2,0.8). Hold p if either operator has zero trials or both rates are zero. Fixed holds initial p. F/CR adaptation is unchanged.',
            'Initialization is common uniform, bypassing native Sobol/OBL. This controlled ablation does not evaluate complete native-initialized OADE. Restart and all other settings are shared across variants.',
            f'comparisons.csv: all {len(candidates)*(len(candidates)-1)//2} pairs per problem/metric, paired valid seeds, median paired delta a-b and two-sided Wilcoxon (wilcox zeros, normal approximation; all zero p=1), Holm across pairs per problem/metric, alpha=0.05. Excluded pairs are counted. IGD lower / HV higher is better. No detected difference is not equivalence.',
            'raw_runs.csv contains per-run quality, runtime, validity and final pDE; probability_trace.csv contains every completed generation, trial/success counts, target and before/after pDE. Fixed success counts are blank, not measured as zero.',
            'Primary JSON contains final X/F and reference snapshot hashes for recomputation. All objective calls count against the cap; atomic batches may leave unused evaluations. Read n_eval. Convergence has actual observation budgets; no interpolation.', '',
            '| Problem | Mode | Valid/runs | Median IGD | Median HV | Median final pDE |',
            '|---|---|---:|---:|---:|---:|']
    for p in cfg['problems']:
        for c in candidates:
            group = [r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']]
            valid = [r for r in group if r['valid']]
            def median(key,source):
                return f'{base.np.median([r[key] for r in source]):.6g}' if source else 'NA'
            text.append(f'| {p["name"]} | {c["id"]} | {len(valid)}/{len(group)} | {median("IGD",valid)} | {median("HV",valid)} | {median("final_prob_de",group)} |')
    (directory/'derived/report.md').write_text('\n'.join(text)+'\n',encoding='utf-8')


def main(argv=None):
    base.main(argv,default_config='config/studies/probability_ablation.yaml',
              design_fn=design,output_writer=write_outputs,study_kind='probability_ablation_v1')


if __name__ == '__main__':
    main()
