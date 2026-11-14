"""Ablate periodic OBL injection, holding initialization/restart/pDE constant."""
import json
from shared.io.csv_io import write_csv
from . import initialization_comparison as measurements
from . import restart_comparison as base


def design(cfg):
    cfg=json.loads(json.dumps(cfg))
    common=cfg['common_settings']
    if 'enable_obl' in common:
        raise ValueError('enable_obl is the controlled ablation switch')
    if common.get('initialization_method')!='uniform':
        raise ValueError('This protocol fixes common uniform initialization')
    required={'restart_mode':'adaptive','enable_restart':True,'probability_update_mode':'success_rate',
              'enable_probability_adaptation':True,'enable_fcr_adaptation':True,'enable_neighborhood':True}
    if any(common.get(k)!=v for k,v in required.items()):
        raise ValueError('Keep adaptive restart, success_rate, F/CR and neighborhood in both arms')
    if 'initialization_seed' in common:
        raise ValueError('Initialization seed is controlled by the paired task seed')
    probe=json.loads(json.dumps(cfg))
    for k in ('restart_mode','restart_elite_ratio','enable_restart'):
        probe['common_settings'].pop(k,None)
    base.design(probe)
    candidates=[dict(id=name,parameter='enable_obl',level=enabled,
                     settings={**common,'pop_size':cfg['global']['pop_size'],'enable_obl':enabled})
                for name,enabled in [('obl_on',True),('obl_off',False)]]
    return cfg,candidates


def run_task(cfg,candidate,problem_cfg,seed):
    row=measurements.run_task(cfg,candidate,problem_cfg,seed)
    t=row['telemetry']; events=row['diversity_events']
    if not candidate['settings']['enable_obl'] and (events or t['injection_attempts'] or t['injection_evaluations']):
        raise ValueError('Disabled injection must perform no OBL calls')
    if t['injection_evaluations']!=sum(e['evaluations'] for e in events):
        raise ValueError('Injection evaluation accounting mismatch')
    row['injection_evaluation_fraction']=t['injection_evaluations']/row['n_eval']
    return row


def write_outputs(directory,manifest,cfg,candidates):
    rows,summaries,paired=measurements.write_measurements(directory,manifest,cfg,candidates,require_same_initial=True)
    derived=directory/'derived'
    # Prespecified multiplicity across all problem/metric endpoints (10 for full ZDT).
    ordered=sorted([r for r in paired if r['p_raw'] is not None],key=lambda r:r['p_raw'])
    previous=0.
    for i,r in enumerate(ordered):
        previous=max(previous,min(1.,(len(paired)-i)*r['p_raw']))
        r['p_holm_all_endpoints']=previous
    for r in paired:
        r.setdefault('p_holm_all_endpoints',None)
        r['interpretation_all_endpoints']=('no_valid_pairs' if r['p_holm_all_endpoints'] is None else
                                         'difference_detected' if r['p_holm_all_endpoints']<.05 else 'no_difference_detected')
    write_csv(derived/'comparisons.csv',paired,list(paired[0]))
    fields=['candidate','problem','seed','generation','generation_index','n_eval_before','status','candidates',
            'generation_completed','retained','n_eval_after','evaluations']
    events=[{k:r[k] for k in ('candidate','problem','seed')}|e for r in rows for e in r['diversity_events']]
    write_csv(derived/'diversity_events.csv',events,fields)
    restart_fields=['candidate','problem','seed','mode','generation','n_eval_before','status','n_eval_after','evaluations']
    restarts=[{k:r[k] for k in ('candidate','problem','seed')}|
              {k:e[k] for k in restart_fields if k in e} for r in rows for e in r['restart_events']]
    write_csv(derived/'restart_events.csv',restarts,restart_fields)
    text=['# Đối chứng bơm đa dạng OBL định kỳ','',
          '**SMOKE: chỉ kiểm tra pipeline, không phải bằng chứng cải thiện.**' if cfg.get('smoke') else 'Đối chứng ghép seed trên ZDT.',
          f"Đã đo **{len(rows)} run**, hợp lệ **{sum(r['valid'] for r in rows)}**.",'',
          '## Thiết kế','',
          '| Nhánh | OBL định kỳ | Các cơ chế chung |','|:---|:---|:---|',
          '| Bật | Chỉ số thế hệ 0, 10, 20, … | Uniform cùng quần thể đầu/seed, adaptive restart, success-rate, F/CR, neighborhood |',
          '| Tắt | Không gọi OBL định kỳ | Giữ nguyên các cơ chế còn lại |','',
          'Kernel OBL hiện có chọn từng cá thể với xác suất jump_rate=0,2 rồi phản chiếu theo bounds quần thể hoặc bounds bài toán (50/50). Chỉ các ứng viên được sinh mới tốn evaluation; không mặc định mỗi lần bơm có đủ 100 ứng viên.',
          'Tắt bơm định kỳ không tắt adaptive restart hoặc phần OBL/Gauss bên trong restart. Vì vậy nhánh tắt vẫn có thể được restart làm mới quần thể. Khởi tạo Sobol–OBL không tham gia cả hai nhánh.',
          '## Chất lượng cuối — median','',
          '| Bài | Nhánh | Valid/run | IGD ↓ | HV ↑ | Runtime (s) |','|:---|:---|---:|---:|---:|---:|']
    for s in summaries:
        fmt=lambda k: '—' if s[k] is None else f'{s[k]:.7f}'
        text.append(f"| {s['problem'].upper()} | {'Bật' if s['method']=='obl_on' else 'Tắt'} | {s['valid_runs']}/{s['runs']} | {fmt('IGD_median')} | {fmt('HV_median')} | {s['runtime_seconds_median']:.3f} |")
    text+=['','## Bằng chứng kích hoạt và chi phí','',
           '| Bài | Nhánh | Lần gọi / hoàn tất | Ứng viên OBL | Evaluation OBL | Được giữ sau chọn lọc | Restart |',
           '|:---|:---|---:|---:|---:|---:|---:|']
    for s in summaries:
        text.append(f"| {s['problem'].upper()} | {'Bật' if s['method']=='obl_on' else 'Tắt'} | {s['injection_attempts']} / {s['injection_completed']} | {s['injection_candidates']} | {s['injection_evaluations']} | {s['injection_retained']} | {s['restart_attempts']} |")
    text+=['','## Đọc kết quả','',
           'comparisons.csv dùng delta = bật − tắt: IGD âm hoặc HV dương ủng hộ bật. Wilcoxon signed-rank hai phía trên cặp seed hợp lệ, zero_method=wilcox, xấp xỉ chuẩn; toàn delta zero đặt p=1. Alpha=0,05. p_holm_all_endpoints hiệu chỉnh đồng thời mọi bài × 2 chỉ số (10 endpoint khi chạy đủ ZDT); p_holm giữ họ từng bài/metric cho truy vết. Không phát hiện khác biệt không chứng minh tương đương.',
           'Cả hai có cùng cap tổng, bao gồm khởi tạo, OBL định kỳ và restart. Nhánh bật trả evaluation cho OBL nên có thể hoàn tất ít thế hệ hơn; không bù thêm ngân sách. Batch nguyên tử có thể để dư, xem n_eval.',
           'diversity_events.csv ghi từng lần gọi, số ứng viên và evaluation, bị chặn ngân sách, thế hệ có hoàn tất chọn lọc hay không, số ứng viên còn lại trong quần thể sau chọn lọc. completed chỉ nghĩa đã sinh/xử lý OBL, không bảo đảm thế hệ đã hoàn tất; retained để trống khi chưa chọn lọc. Ứng viên được giữ không tự chứng minh đóng góp lâu dài.',
           'summary.csv lưu mean, SD, median, Q25/Q75; chất lượng đầu và cuối, chi phí, runtime và xác suất DE. Primary JSON chứa X/F đầu/cuối, probability trace, convergence và cả hai loại sự kiện. Tần suất và số giữ lại là mô tả; lợi ích ròng cần đọc chất lượng cuối ở cùng cap.',
           'Nếu khác biệt downstream làm restart kích hoạt khác nhau, đây là một phần tác động tổng của bật/tắt OBL định kỳ; thiết kế này chưa tách riêng cơ chế trung gian. Runtime mô tả máy/worker đang dùng, không suy ra độ phức tạp từ thời gian.', '']
    (derived/'report.md').write_text('\n'.join(text),encoding='utf-8')


def main(argv=None):
    base.main(argv,default_config='config/studies/diversity_injection.yaml',design_fn=design,
              output_writer=write_outputs,task_runner=run_task,study_kind='diversity_injection_v1')


if __name__=='__main__': main()
