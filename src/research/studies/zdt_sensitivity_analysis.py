"""Direct per-problem responses, without ranks, composite scores or winners."""
from collections import defaultdict
import numpy as np


def describe(values):
    if not values:
        return {key: None for key in ("mean", "std", "median", "q25", "q75")}
    return {"mean": float(np.mean(values)), "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
            "median": float(np.median(values)), "q25": float(np.quantile(values, .25)), "q75": float(np.quantile(values, .75))}


def analyze(cfg, candidates, records):
    groups = defaultdict(list)
    for row in records:
        groups[(row["candidate"], row["problem"])].append(row)
    summaries, comparisons = [], []
    for parameter, values in cfg["parameters"].items():
        baseline_value = cfg["baseline_settings"][parameter]
        for level in sorted(values):
            candidate = next(c for c in candidates if c["id"] == "baseline") if level == baseline_value else next(
                c for c in candidates if c["parameter"] == parameter and c["level"] == level)
            for problem in cfg["problems"]:
                name = problem["name"]
                rows = groups[(candidate["id"], name)]
                reference = {r["seed"]: r for r in groups[("baseline", name)]}
                valid = [r for r in rows if r["valid"]]
                summary = {"parameter": parameter, "level": level, "baseline_level": baseline_value,
                           "change": "baseline" if level == baseline_value else "increase" if level > baseline_value else "decrease",
                           "candidate": candidate["id"], "problem": name, "runs": len(rows),
                           "valid_runs": len(valid), "invalid_runs": len(rows) - len(valid),
                           "restart_attempts": sum(r["telemetry"]["restart_attempts"] for r in rows),
                           "restart_completed": sum(r["telemetry"]["restart_completed"] for r in rows),
                           "restart_evaluations": sum(r["telemetry"]["restart_evaluations"] for r in rows),
                           "collapse_checks": sum(r["telemetry"]["collapse_checks"] for r in rows),
                           "n_eval_min": min(r["n_eval"] for r in rows), "n_eval_max": max(r["n_eval"] for r in rows),
                           "n_eval_mean": float(np.mean([r["n_eval"] for r in rows]))}
                for metric in ("IGD", "HV", "runtime_seconds"):
                    source = valid if metric in {"IGD", "HV"} else rows
                    summary.update({metric + "_" + key: value for key, value in describe([r[metric] for r in source]).items()})
                for key in ("final_mean_F", "final_mean_CR", "final_prob_de"):
                    summary[key + "_median"] = float(np.median([r[key] for r in rows]))
                summaries.append(summary)
                paired = [(r, reference[r["seed"]]) for r in rows if r["valid"] and reference[r["seed"]]["valid"]]
                for metric in ("IGD", "HV", "runtime_seconds"):
                    pairs = list(zip(rows, [reference[r["seed"]] for r in rows])) if metric == "runtime_seconds" else paired
                    a, b = [r[metric] for r, _ in pairs], [r[metric] for _, r in pairs]
                    current, base = (float(np.median(a)), float(np.median(b))) if a else (None, None)
                    delta = current - base if a else None
                    comparisons.append({"parameter": parameter, "level": level, "baseline_level": baseline_value,
                                        "change": summary["change"], "problem": name, "metric": metric,
                                        "n_pairs": len(pairs), "baseline_median": base, "level_median": current,
                                        "absolute_change": delta, "percent_change": 100 * delta / abs(base) if a and base != 0 else None,
                                        "percent_status": "defined" if a and base != 0 else "baseline_zero" if a else "no_valid_pairs",
                                        "direction": "no_valid_pairs" if not a else "unchanged" if current == base else "lower" if current < base else "higher",
                                        "lower_is_better": metric != "HV"})
    return summaries, comparisons


def report(cfg, candidates, rows, summaries, comparisons):
    text = ["# Độ nhạy tham số v2 trên ZDT: tăng/giảm từng tham số", "",
            "**SMOKE: chỉ kiểm tra pipeline, không dùng để lựa chọn tham số.**" if cfg.get("smoke") else
            "Đo trực tiếp tác động của từng mức tham số. Không có điểm tổng, thứ hạng hoặc cấu hình thắng tự động.", "",
            f"Đã hoàn tất {len(rows)} run; {len(candidates)} cấu hình duy nhất; {len(cfg['global']['seeds'])} seed mỗi cấu hình/bài.",
            f"Cap: {cfg['global']['evaluation_budget']} evaluation/run; invalid: {sum(not r['valid'] for r in rows)}.", "",
            "IGD giảm là tốt; HV tăng là tốt. Thời gian là số đo mô tả trên máy/worker đang dùng.",
            "Mỗi lần chỉ thay một tham số; các tham số còn lại giữ theo baseline adaptive v2.",
            "Population khác nhau dùng cùng seed và khởi tạo theo prefix, không có cùng số cá thể ban đầu.", ""]
    for parameter in cfg["parameters"]:
        baseline = cfg["baseline_settings"][parameter]
        text += [f"## {parameter} — mức hiện tại: {baseline}", "",
                 f"Các mức đã chạy: {sorted(cfg['parameters'][parameter])}.", "",
                 "| Bài | Mức thử | Thay đổi | IGD median | Δ IGD (%) | HV median | Δ HV (%) | Thời gian median (s) | Valid/run | Restart |",
                 "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
        for summary in summaries:
            if summary["parameter"] != parameter:
                continue
            def number(value):
                return "—" if value is None else f"{value:.6g}"
            def percent(metric):
                row = next(r for r in comparisons if r["parameter"] == parameter and r["level"] == summary["level"] and r["problem"] == summary["problem"] and r["metric"] == metric)
                return "không xác định" if row["percent_change"] is None else f"{row['percent_change']:+.2f}"
            change = {"baseline": "mốc", "increase": "tăng", "decrease": "giảm"}[summary["change"]]
            text.append(f"| {summary['problem'].upper()} | {summary['level']} | {change} | {number(summary['IGD_median'])} | {percent('IGD')} | {number(summary['HV_median'])} | {percent('HV')} | {summary['runtime_seconds_median']:.3f} | {summary['valid_runs']}/{summary['runs']} | {summary['restart_completed']} |")
        text += ["", f"![Đáp ứng {parameter}](../figures/{parameter}.png)", ""]
    text += ["## Cách diễn giải", "",
             "Đọc từng bài: mức tăng/giảm nào làm IGD giảm hoặc HV tăng; xem IQR/std và invalid để đánh giá độ dao động. Không gộp các bài thành điểm.",
             "Median tốt hơn chỉ là chênh lệch mô tả; báo cáo này không gọi đó là thắng thống kê hoặc chứng minh tối ưu.",
             "Các tham số F/CR/probability là giá trị khởi tạo và có thể được adaptation cập nhật trong run.",
             "Nếu restart không xảy ra, chưa có bằng chứng về tác động của các mức tham số restart. Kernel giữ elite tối thiểu 0.8; mức thấp hơn bị từ chối.",
             "Baseline được chạy một lần mỗi seed/bài và tham chiếu lại trong từng bảng, không tính như các replicate độc lập mới.",
             "Hình: mỗi chấm là median, dải là Q25–Q75; không phải CI. Đường nối chỉ hướng dẫn đọc các mức rời rạc, không ước lượng các mức chưa đo.",
             "Bảng CSV đầy đủ: summary.csv (mean, std, median, Q25/Q75), comparisons.csv (chênh lệch ghép seed), raw_runs.csv (từng run).",
             "Không tự đổi cấu hình v2 sau báo cáo. Giữ toàn bộ invalid, kể cả khi không thể tính chất lượng trên cặp hợp lệ."]
    return "\n".join(text) + "\n"
