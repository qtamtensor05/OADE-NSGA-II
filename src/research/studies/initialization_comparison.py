"""Compare common uniform warm start with native seeded Sobol–OBL."""
from __future__ import annotations

import json
import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

from oade_nsga2.runner import run_instrumented
from shared.contracts import AlgorithmSpec
from shared.evaluation import validate_result
from shared.population import make_initial_population
from shared.io.csv_io import write_csv
from research.benchmarking.convergence import ConvergenceRecorder
from research.benchmarking.provenance import digest
from . import restart_comparison as base


def design(cfg):
    cfg = json.loads(json.dumps(cfg))
    common = cfg['common_settings']
    expected = {'restart_mode':'adaptive', 'enable_restart':True,
                'probability_update_mode':'success_rate', 'enable_probability_adaptation':True,
                'enable_obl':True}
    if any(common.get(k) != v for k,v in expected.items()):
        raise ValueError('Require adaptive restart, success_rate and periodic OBL in both arms')
    if 'initialization_method' in common or 'initialization_seed' in common:
        raise ValueError('Initialization is controlled by the study and paired seed')
    probe = json.loads(json.dumps(cfg))
    for k in ('restart_mode','restart_elite_ratio','enable_restart'):
        probe['common_settings'].pop(k,None)
    base.design(probe)
    if cfg['global']['evaluation_budget'] <= 2*cfg['global']['pop_size']:
        raise ValueError('Budget must exceed 2*population for Sobol–OBL plus evolution')
    candidates = [dict(id=mode,parameter='initialization_method',level=mode,
                       settings={**common,'pop_size':cfg['global']['pop_size'],
                                 'initialization_method':mode})
                  for mode in ('uniform','sobol_obl')]
    return cfg,candidates


def run_task(cfg,candidate,problem_cfg,seed):
    problem = get_problem(problem_cfg['name'],n_var=problem_cfg['n_var'])
    ref = np.asarray(cfg['reference_fronts'][problem_cfg['name']])
    igd,hv = IGD(ref),HV(ref_point=np.max(ref,axis=0)+.1)
    budget,pop = cfg['global']['evaluation_budget'],cfg['global']['pop_size']
    mode = candidate['settings']['initialization_method']
    initial = make_initial_population(problem,pop,seed) if mode=='uniform' else None
    params = {k:v for k,v in candidate['settings'].items() if k not in {'pop_size','initialization_method'}}
    params['initialization_seed'] = seed
    spec = AlgorithmSpec(candidate['id'],'local_oade',params)

    def metrics(f):
        return {'IGD':float(igd(f)), 'HV':float(hv(f))}

    outcome,observed = run_instrumented(spec,problem,pop,budget,initial,seed,
                                        ConvergenceRecorder(budget,igd,hv),restart_metric=metrics)
    evidence = observed['initialization_evidence']
    initial_quality = metrics(np.asarray(evidence['f']))
    validation = validate_result(outcome.x,outcome.f,problem)
    quality = metrics(outcome.f)
    valid = validation.valid and all(np.isfinite(v) for v in quality.values())
    expected = pop if mode=='uniform' else 2*pop
    if evidence['evaluations'] != expected:
        raise ValueError('Initialization evaluations were not charged exactly once')
    return {'candidate':candidate['id'],'parameter':candidate['parameter'],'level':candidate['level'],
            'problem':problem_cfg['name'],'n_var':problem_cfg['n_var'],'seed':seed,
            'settings':candidate['settings'],'evaluation_budget':budget,'n_eval':outcome.n_eval,
            'valid':valid,'validation_status':validation.status if valid else 'invalid_quality',
            'front_size':validation.front_size,**(quality if valid else {'IGD':None,'HV':None}),
            'runtime_seconds':outcome.runtime_seconds,'reference_sha256':digest(ref.tolist()),
            'initial_x_sha256':digest(evidence['x']),'initialization_seed':seed,
            'initialization_evaluations':expected,'initial_IGD':initial_quality['IGD'],
            'initial_HV':initial_quality['HV'],'final_x':outcome.x.tolist(),'final_f':outcome.f.tolist(),
            'convergence':list(outcome.convergence),**observed}


def write_outputs(directory,manifest,cfg,candidates):
    rows = base.engine.load_records(directory,manifest)
    base.engine.validate_records(cfg,candidates,rows,complete=True)
    # Same seeds, intentionally different initial populations: do not use the
    # equal-initial-X condition of restart/probability controlled ablations.
    paired = base.comparisons(cfg,candidates,rows,require_same_initial=False)
    derived = directory/'derived'
    derived.mkdir(exist_ok=True)
    scalar = [{k:v for k,v in r.items() if not isinstance(v,(dict,list))}|r['telemetry'] for r in rows]
    write_csv(derived/'raw_runs.csv',scalar,list(scalar[0]))
    write_csv(derived/'comparisons.csv',paired,list(paired[0]))
    summaries=[]
    for p in cfg['problems']:
        for c in candidates:
            group=[r for r in rows if r['problem']==p['name'] and r['candidate']==c['id']]
            valid=[r for r in group if r['valid']]
            s={'problem':p['name'],'method':c['id'],'runs':len(group),'valid_runs':len(valid),
               'restart_attempts':sum(r['telemetry']['restart_attempts'] for r in group),
               'initialization_evaluations':group[0]['initialization_evaluations']}
            for metric in ('IGD','HV','initial_IGD','initial_HV','runtime_seconds','n_eval','final_prob_de'):
                values=[r[metric] for r in (valid if metric in {'IGD','HV'} else group)]
                for label,fn in [('mean',np.mean),('median',np.median),('q25',lambda x:np.quantile(x,.25)),
                                 ('q75',lambda x:np.quantile(x,.75)),('sd',lambda x:np.std(x,ddof=1) if len(x)>1 else 0.)]:
                    s[metric+'_'+label]=float(fn(values)) if values else None
            summaries.append(s)
    write_csv(derived/'summary.csv',summaries,list(summaries[0]))
    for key,name,fields in [
        ('probability_trace','probability_trace.csv',['candidate','problem','seed','generation','n_eval','mode','enabled','n_de','n_sbx','success_de','success_sbx','target','prob_before','prob_after']),
        ('convergence','convergence.csv',['candidate','problem','seed','checkpoint_fraction','target_evaluations','n_eval','IGD','HV'])]:
        trace=[{k:r[k] for k in ('candidate','problem','seed')}|t for r in rows for t in r[key]]
        write_csv(derived/name,trace,fields)
    text=['# Đối chứng khởi tạo Uniform và Sobol–OBL','',
          '**SMOKE: chỉ kiểm tra pipeline, không dùng làm bằng chứng cải thiện.**' if cfg.get('smoke') else 'Thí nghiệm ghép seed trên ZDT.',
          f"Tổng số run: **{len(rows)}**; hợp lệ: **{sum(r['valid'] for r in rows)}**.",'',
          '## Hai phương pháp khởi tạo','',
          '| Phương pháp | Cách tạo quần thể | Chi phí ban đầu |',
          '|:---|:---|---:|',
          '| Uniform | Uniform theo seed, cùng cách khởi tạo benchmark đối chứng trước đây | $N$ evaluation |',
          '| Sobol–OBL | Scrambled Sobol + GOBL của OADE hiện có; chọn $N$ cá thể từ $2N$ ứng viên | $2N$ evaluation |','',
          'Sobol và GOBL dùng seed tường minh, RNG khởi tạo riêng; không rút số từ RNG tiến hóa. Sau khởi tạo, cả hai nhánh reset cùng seed tìm kiếm; quỹ đạo có thể phân kỳ do quần thể khác nhau. Ghép seed không có nghĩa cùng quần thể đầu.',
          'Cả hai giữ adaptive restart, success-rate, F/CR adaptation, neighborhood và OBL định kỳ. Chỉ thay cách khởi tạo. Gói Sobol–OBL được đo như một thành phần kết hợp, chưa tách đóng góp Sobol và OBL.',
          '## Kết quả cuối — median','',
          '| Bài | Phương pháp | Valid/run | IGD ↓ | HV ↑ | Runtime (s) |',
          '|:---|:---|---:|---:|---:|---:|']
    for s in summaries:
        def fmt(key): return '—' if s[key] is None else f'{s[key]:.7f}'
        text.append(f"| {s['problem'].upper()} | {s['method']} | {s['valid_runs']}/{s['runs']} | {fmt('IGD_median')} | {fmt('HV_median')} | {s['runtime_seconds_median']:.3f} |")
    text+=['','## Cách đọc đối chứng','',
           'Một cặp uniform–sobol_obl trên mỗi bài và chỉ số. Wilcoxon signed-rank hai phía, zero_method=wilcox, xấp xỉ chuẩn; toàn delta bằng 0 đặt p=1. Holm theo cặp/bài/metric; với một cặp, p hiệu chỉnh bằng p thô. Alpha=0,05. Không phát hiện khác biệt không chứng minh tương đương. Nếu tổng hợp kết luận chung qua nhiều bài/metric, cần xem xét thêm đa kiểm định.',
           'Trong comparisons.csv, delta = uniform − sobol_obl: IGD dương ủng hộ Sobol–OBL; HV âm ủng hộ Sobol–OBL. Các cặp chất lượng chỉ gồm run hợp lệ, có ghi số cặp bị loại.',
           'So sánh ở cùng cap tổng, không cùng số thế hệ: Sobol–OBL trả chi phí khởi tạo cao hơn và còn ít ngân sách tiến hóa hơn. Tất cả objective calls (khởi tạo, OBL định kỳ và restart) tính vào cap; batch nguyên tử có thể để dư, phải đọc n_eval thực.',
           'summary.csv chứa chất lượng sau khởi tạo và chất lượng cuối, mean/SD/median/Q25/Q75, thời gian và số restart. Chất lượng đầu tốt hơn chưa bảo đảm kết quả cuối tốt hơn. Runtime chứa cả khởi tạo, tìm kiếm và instrumentation trên máy/worker đang dùng.',
           'Primary JSON lưu X/F đầu được chọn, chi phí khởi tạo, X/F cuối, convergence, probability trace và restart events. Manifest lưu hash mã/môi trường/reference và checkpoint; không trộn dữ liệu lịch sử hay resume sau đổi mã.', '']
    (derived/'report.md').write_text('\n'.join(text),encoding='utf-8')


def main(argv=None):
    base.main(argv,default_config='config/studies/initialization_comparison.yaml',design_fn=design,
              output_writer=write_outputs,task_runner=run_task,study_kind='initialization_comparison_v1')


if __name__=='__main__': main()
