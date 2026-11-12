"""Build reproducible, source-traceable per-problem research folders.

Run from any directory: python scripts/organize_by_problem.py
Only standard-library modules are required. Source evidence is never moved.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
from collections import defaultdict
from problem_reports import generate_reports
from csv_archives import archive_lookup, verify

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/by_problem"
ARCHIVED = archive_lookup()
SOURCES = {
    "benchmark_classic": "results/algorithm_benchmark",
    "benchmark_adaptive": "results/algorithm_benchmark_v2",
    "restart_confirmation": "results/restart_confirmation",
    "ablation_classic": "results/ablation",
    "sensitivity_classic": "results/sensitivity",
    "sensitivity_adaptive": "results/experiments/zdt_sensitivity_ofat_v1/derived",
    "benchmark_dtlz": "results/dtlz_benchmark",
    "benchmark_wfg_m2": "results/wfg_m2_7algo_benchmark",
    "benchmark_wfg_scaling": "results/wfg_compact_benchmark",
    "sensitivity_dtlz": "results/experiments/dtlz_sensitivity_ofat_v1/derived",
}
REPORTS = {
    "zdt": ["docs/reports/benchmark_v2_results_report.md",
            "docs/reports/restart_confirmation_report.md",
            "docs/reports/ablation_results_report.md",
            "docs/reports/zdt_parameter_sensitivity_report.md",
            "docs/reports/sensitivity_analysis.md",
            "docs/protocols/zdt_sensitivity.md",
            "docs/protocols/experiment_registry.md",
            "results/provenance/zdt_composition.json",
            "results/provenance/zdt_validation.json",
            "results/experiments/zdt_sensitivity_ofat_v1/study_manifest.json"],
    "dtlz": ["docs/reports/dtlz_results_report.md", "docs/protocols/dtlz_sensitivity.md"],
    "wfg": ["docs/reports/wfg_compact_report.md"],
}


def link(base, path):
    path = ARCHIVED.get(path, path)
    return os.path.relpath(ROOT / path, base).replace("\\", "/")


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if any(not (ROOT / path).exists() for path in ARCHIVED):
        verify(restore=True)
    evidence = defaultdict(list)
    coverage = []
    for category, source_dir in SOURCES.items():
        for source in sorted((ROOT / source_dir).glob("*.csv")):
            with source.open(newline="", encoding="utf-8-sig") as stream:
                reader = csv.DictReader(stream)
                fields = reader.fieldnames or []
                if "problem" not in fields:
                    continue
                groups = defaultdict(list)
                for row in reader:
                    problem = row["problem"].lower()
                    if re.fullmatch(r"(?:zdt|dtlz|wfg)\d+(?:_m\d+)?", problem):
                        groups[problem].append(row)
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            for problem, rows in sorted(groups.items()):
                family = "zdt" if problem.startswith("zdt") else "dtlz" if problem.startswith("dtlz") else "wfg"
                destination = OUT / family / problem / category / source.name
                write_csv(destination, fields, rows)
                record = {"category": category, "source": source.relative_to(ROOT).as_posix(),
                          "source_sha256": source_hash,
                          "output": destination.relative_to(ROOT).as_posix(),
                          "output_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                          "rows": len(rows), "filter": {"problem": problem}}
                evidence[(family, problem)].append(record)
                if source.name.endswith("raw_runs.csv"):
                    coverage.append({"family": family, "problem": problem, "study": category,
                                     "rows": len(rows),
                                     "algorithms": ";".join(sorted({r.get("algorithm", "OADE_NSGAII") for r in rows})),
                                     "seeds": len({r.get("seed", "") for r in rows}),
                                     "source": record["source"]})

    for (family, problem), records in sorted(evidence.items()):
        base = OUT / family / problem
        generate_reports(base, family, problem, records, REPORTS[family], link)
        (base / "manifest.json").write_text(json.dumps({
            "problem": problem, "artifacts": records,
            "note": "Filtered views, not new independent executions. Original statistical correction families are preserved."
        }, indent=2) + "\n", encoding="utf-8")
        lines = [f"# {problem.upper()} — hồ sơ nghiên cứu", "",
                 "Dữ liệu đã lọc riêng theo bài toán; giữ nguyên cột, giá trị và thứ tự dòng từ nguồn.", "",
                 "| Nhóm thí nghiệm | Số dòng raw | Số seed |", "|---|---:|---:|"]
        lines[2:2] = ["[Báo cáo riêng của bài toán](reports/README.md)", ""]
        for item in coverage:
            if item["family"] == family and item["problem"] == problem:
                lines.append(f"| [{item['study']}](reports/{item['study']}.md) | {item['rows']} | {item['seeds']} |")
        lines += ["", "## Bảng và dữ liệu", ""]
        for record in records:
            target = ROOT / record["output"]
            lines.append(f"- [{record['category']}/{target.name}]({link(base, record['output'])}) ({record['rows']} dòng)")
        if family == "zdt":
            summaries = {}
            for category in ("benchmark_classic", "benchmark_adaptive"):
                path = base / category / "algorithm_benchmark_igd_hv_summary.csv"
                if path.exists():
                    with path.open(newline="", encoding="utf-8") as stream:
                        summaries[category] = list(csv.DictReader(stream))
            if len(summaries) == 2:
                lines += ["", "## Classic và adaptive trên benchmark 7 thuật toán", "",
                          "Hai bảng dùng chung các block đối chứng; không cộng thành các lượt chạy độc lập mới.", "",
                          "| Thuật toán | IGD classic | IGD adaptive | HV classic | HV adaptive |",
                          "|---|---:|---:|---:|---:|"]
                adaptive = {r["algorithm"]: r for r in summaries["benchmark_adaptive"]}
                for classic in summaries["benchmark_classic"]:
                    current = adaptive[classic["algorithm"]]
                    lines.append(f"| {classic['algorithm']} | {float(classic['IGD_mean']):.6g} | {float(current['IGD_mean']):.6g} | {float(classic['HV_mean']):.6g} | {float(current['HV_mean']):.6g} |")
                lines += ["", "Đây là trung bình mô tả từ benchmark seed 42–71. Để đánh giá trực tiếp classic/adaptive/no-restart trên seed 1000–1029, xem `restart_confirmation/`. Không diễn giải chênh lệch mô tả như kiểm định mới."]
        lines += ["", "## Báo cáo, hình và nguồn dùng chung", ""]
        for report in REPORTS[family]:
            if (ROOT / report).exists():
                lines.append(f"- [{Path(report).name}]({link(base, report)})")
        if family == "zdt":
            lines += [f"- [Hình tổng hợp các bài toán]({link(base, 'results/figures')}/)",
                      f"- [Hình độ nhạy adaptive OFAT]({link(base, 'results/experiments/zdt_sensitivity_ofat_v1/figures')}/)",
                      "", "Độ nhạy classic và adaptive có seed, thiết kế khác nhau; giữ riêng hai thư mục. Các hình trên là hình nhiều bài toán, không phải hình đã lọc riêng."]
        lines += ["", "## Truy vết và bổ sung", "",
                  "`manifest.json` ghi nguồn, SHA-256 và số dòng của từng tệp. P-value/Holm được giữ theo họ kiểm định gốc, không hiệu chỉnh lại theo thư mục.",
                  "Các bảng khác số mục tiêu/kích thước vẫn giữ cột n_obj/n_var; không gộp thành một điều kiện.",
                  "Bổ sung kết quả vào nguồn theo đúng giao thức, rồi chạy `python scripts/organize_by_problem.py`. Không chỉnh trực tiếp bản tách được sinh tự động.", ""]
        (base / "README.md").write_text("\n".join(lines), encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "coverage.csv", ["family", "problem", "study", "rows", "algorithms", "seeds", "source"], coverage)
    for family in ("zdt", "dtlz", "wfg"):
        base = OUT / family
        base.mkdir(exist_ok=True)
        problems = sorted(p for f, p in evidence if f == family)
        (base / "README.md").write_text(f"# {family.upper()}\n\n" +
            "\n".join(f"- [{p.upper()}]({p}/README.md)" for p in problems) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("""# Hồ sơ nghiên cứu theo bài toán

Ưu tiên nghiên cứu hiện tại: **ZDT1, ZDT2, ZDT3, ZDT4, ZDT6**. Không có dữ liệu ZDT5 trong các đợt được tuyển chọn.

| Bộ bài toán | Vai trò | Hồ sơ |
|---|---|---|
| ZDT | Trọng tâm: benchmark 7 thuật toán classic/adaptive, xác nhận restart, ablation, độ nhạy | [ZDT](zdt/README.md) |
| DTLZ | Bằng chứng mở rộng hiện có, tiếp tục chạy và bổ sung | [DTLZ](dtlz/README.md) |
| WFG | Bằng chứng mở rộng hiện có, tách benchmark M=2 và scaling | [WFG](wfg/README.md) |

Mỗi hồ sơ có thư mục `reports/` chứa báo cáo Markdown riêng cho từng nhóm thí nghiệm, với bảng số liệu chỉ của bài toán tương ứng. ZDT có thêm `reports/classic_vs_adaptive.md`. Báo cáo được tái tạo cùng dữ liệu khi chạy script.

Mỗi bài toán có thư mục thí nghiệm riêng, README, CSV đã lọc và manifest SHA-256. [coverage.csv](coverage.csv) thống kê số dòng raw theo bài toán/đợt, không phải tổng lượt thực thi độc lập.

Nguồn gốc và đường dẫn thực thi giữ nguyên; đây là lớp tổ chức để đọc và phân tích. Không lấy smoke, correction trung gian hoặc benchmark legacy làm bằng chứng chính. Các báo cáo/hình nhiều bài toán được liên kết thay vì sao chép và đổi nhãn thành hình riêng.

ZDT: benchmark classic/adaptive mỗi bộ 1.050 dòng (5 × 7 × 30), dùng chung 6 block đối chứng; restart confirmation 450 dòng; adaptive OFAT 2.850 dòng duy nhất. Sensitivity classic là bằng chứng lịch sử riêng.

Tái tạo sau khi bổ sung dữ liệu: `python scripts/organize_by_problem.py`. Thêm nguồn nghiên cứu mới vào `SOURCES` của script; mọi bài toán xuất hiện trong cột `problem` sẽ được tách vào đúng bộ. Nguồn chưa có CSV derived sẽ chưa được đánh dấu có kết quả. Không dùng thư mục này làm nơi ghi checkpoint của các lượt đang chạy.
""", encoding="utf-8")
    index = OUT / "README.md"
    index.write_text(index.read_text(encoding="utf-8") + "\n[Tải CSV dạng ZIP và hướng dẫn khôi phục](../CSV_DOWNLOADS.md).\n", encoding="utf-8")
    print(f"Organized {len(evidence)} problems, {sum(len(v) for v in evidence.values())} CSV views in {OUT}")


if __name__ == "__main__":
    main()
