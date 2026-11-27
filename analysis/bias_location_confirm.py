"""Confirmation round for the OADE bias check (written BEFORE running).

Round 1 (bias_location_exploratory.py, seeds 9000-9029, one offset vector) was exploratory.
This round uses FRESH seeds 9100-9129, all five ZDT problems, three independent
offset vectors and a boundary-neutral repair. Nothing from round 1 is reused.

Pre-specified hypotheses and tests
----------------------------------
P1  OBL centre bias (ZDT4): the per-seed log ratio IGD(noOBL)/IGD(OADE) is
    larger on original ZDT4 than on each shifted ZDT4 (3 Mann-Whitney tests).
P2  Location dependence vs NSGA-II: for each problem and each shift, the per-seed
    log ratio IGD(NSGA2)/IGD(OADE) differs between original and shifted
    (5 problems x 3 shifts = 15 tests).
P3  Bound repair: replacing clip with uniform random re-initialisation of
    violated DE genes (no pull towards the bound) changes the clip advantage
    between original and shifted (15 tests). Midpoint/bounce repair is kept as
    a secondary arm (15 tests).
Interaction family (P1+P2+P3 incl. bounce and noOBL on all problems):
    4 contrasts x 5 problems x 3 shifts = 60 Mann-Whitney tests, one Holm family.
Paired family: 4 contrasts x 5 problems x 4 variants x 2 metrics = 160
    Wilcoxon signed-rank tests (pairs = seeds), one Holm family.
Descriptive: ZDT4 runs with IGD > 1e-2 (local-front trapping).

Usage: python analysis/bias_location_confirm.py --stage smoke|run|report [--jobs N]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "results/experiments/bias_location_confirm_v1"

import numpy as np  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

POP, BUDGET = 100, 20_000
SEEDS = list(range(9100, 9130))
PROBLEMS = [("zdt1", 30), ("zdt2", 30), ("zdt3", 30), ("zdt4", 10), ("zdt6", 10)]
SHIFT_RNG = {"shift_a": 12345, "shift_b": 2024, "shift_c": 777}
VARIANTS = ["original", *SHIFT_RNG]
ALGOS = ["OADE", "OADE_random", "OADE_bounce", "OADE_noOBL", "NSGA2"]
CONTRASTS = ["OADE_random", "OADE_bounce", "OADE_noOBL", "NSGA2"]
REF = json.loads((ROOT / "results/experiments/zdt_six_fixed_oade_v1/config/reference_fronts.json").read_text())


def offsets(name, n_var, variant):
    rng = np.random.default_rng(SHIFT_RNG[variant])
    if name == "zdt4":
        return rng.uniform(-2.5, 2.5, n_var - 1)
    return rng.uniform(0.2, 0.8, n_var - 1)


def make_problem(name, n_var, variant):
    from pymoo.core.problem import Problem
    from pymoo.problems import get_problem

    base = get_problem(name, n_var=n_var)
    if variant == "original":
        return base
    o = offsets(name, n_var, variant)

    class Shifted(Problem):
        def __init__(self):
            super().__init__(n_var=base.n_var, n_obj=base.n_obj, xl=base.xl, xu=base.xu)

        def _evaluate(self, x, out, *args, **kwargs):
            x = np.atleast_2d(x)
            z = x.copy()
            z[:, 1:] = (x[:, 1:] - o) if name == "zdt4" else np.abs(x[:, 1:] - o)
            out["F"] = base.evaluate(z)

    return Shifted()


def _oade_classes():
    from oade_nsga2 import OADE_NSGAII
    from oade_nsga2 import algorithm as alg_mod

    class OADENoOBL(OADE_NSGAII):
        def _generate_periodic_obl(self, gen):
            return []

    class _Repair(OADE_NSGAII):
        def _repair(self, x, t, lo, hi):
            raise NotImplementedError

        def _create_one_child(self, idx, neighbor_indices):
            if np.random.rand() < self.prob_de:
                inf = np.full(self.n_var, np.inf)
                child = alg_mod.de_mutation(idx, self.population, neighbor_indices,
                                            -inf, inf, self.n_var, self.mean_F, self.mean_CR)
                x = child.X
                lo, hi = x < self.xl, x > self.xu
                if lo.any() or hi.any():
                    self._repair(x, self.population[idx].X, lo, hi)
                child.X = x
                return child
            return alg_mod.sbx_crossover_mutation(
                alg_mod.tournament_selection(self.population),
                alg_mod.tournament_selection(self.population),
                self.xl, self.xu, self.n_var, self.pc, self.pm, self.eta_c, self.eta_m)

    class OADEBounce(_Repair):
        """Uniform between violated bound and target gene (pulls towards bound)."""

        def _repair(self, x, t, lo, hi):
            x[lo] = self.xl[lo] + np.random.rand(lo.sum()) * (t[lo] - self.xl[lo])
            x[hi] = self.xu[hi] - np.random.rand(hi.sum()) * (self.xu[hi] - t[hi])

    class OADERandom(_Repair):
        """Uniform re-initialisation over the whole range (no bound attraction)."""

        def _repair(self, x, t, lo, hi):
            m = lo | hi
            x[m] = self.xl[m] + np.random.rand(m.sum()) * (self.xu[m] - self.xl[m])

    return {"OADE": OADE_NSGAII, "OADE_random": OADERandom, "OADE_bounce": OADEBounce,
            "OADE_noOBL": OADENoOBL}


def run_one(task):
    algo, name, n_var, variant, seed = task
    from pymoo.indicators.hv import HV
    from pymoo.indicators.igd import IGD
    from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded, validate_result
    from shared.fronts import non_dominated_xy

    problem = make_problem(name, n_var, variant)
    budgeted = BudgetedProblem(problem, BUDGET)
    t0 = time.perf_counter()
    if algo == "NSGA2":
        from pymoo.algorithms.moo.nsga2 import NSGA2
        from pymoo.optimize import minimize
        from shared.pymoo_execution import FixedInitialSampling
        from shared.population import make_initial_population
        alg = NSGA2(pop_size=POP, sampling=FixedInitialSampling(make_initial_population(problem, POP, seed), seed))
        res = None
        try:
            res = minimize(budgeted, alg, termination=("n_eval", BUDGET), seed=seed,
                           verbose=False, copy_algorithm=False)
        except EvaluationBudgetExceeded:
            pass
        if res is not None and res.X is not None:
            x, f = np.atleast_2d(res.X), np.atleast_2d(res.F)
        else:
            x, f = alg.pop.get("X"), alg.pop.get("F")
    else:
        from oade_nsga2 import ProblemWrapper
        solver = _oade_classes()[algo](ProblemWrapper(budgeted), pop_size=POP, n_gen=BUDGET, seed=seed)
        try:
            solver.run()
        except EvaluationBudgetExceeded:
            pass
        x = np.asarray([i.X for i in solver.population], float)
        f = np.asarray([i.F for i in solver.population], float)
    runtime = time.perf_counter() - t0
    x, f = non_dominated_xy(x, f)
    f_check = np.atleast_2d(make_problem(name, n_var, variant).evaluate(x))
    ref = np.asarray(REF[name])
    v = validate_result(x, f, problem)
    row = dict(algo=algo, problem=name, variant=variant, seed=seed, n_eval=budgeted.n_eval,
               runtime=runtime, valid=bool(v.valid), status=v.status,
               max_f_err=float(np.max(np.abs(f_check - f))))
    if v.valid:
        row["IGD"] = float(IGD(ref)(f))
        row["HV"] = float(HV(ref_point=ref.max(axis=0) + 0.1)(f))
    return row


def sanity():
    for name, n_var in PROBLEMS:
        x1 = np.linspace(0, 1, 11)
        f0 = make_problem(name, n_var, "original").evaluate(np.column_stack([x1, np.zeros((11, n_var - 1))]))
        for v in SHIFT_RNG:
            p = make_problem(name, n_var, v)
            f = p.evaluate(np.column_stack([x1, np.tile(offsets(name, n_var, v), (11, 1))]))
            assert np.allclose(f, f0), (name, v)
    print("sanity: every shifted optimum reproduces the unchanged Pareto front")


def tasks(seeds):
    return [(a, n, d, v, s) for (n, d) in PROBLEMS for v in VARIANTS for a in ALGOS for s in seeds]


def execute(task_list, jobs, out_file):
    from concurrent.futures import ProcessPoolExecutor, as_completed
    done = set()
    if out_file.exists():
        for line in out_file.read_text().splitlines():
            r = json.loads(line)
            done.add((r["algo"], r["problem"], r["variant"], r["seed"]))
    todo = [t for t in task_list if (t[0], t[1], t[3], t[4]) not in done]
    print(f"{len(task_list)} tasks, {len(todo)} to run, jobs={jobs}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=jobs) as ex, out_file.open("a") as fh:
        futs = [ex.submit(run_one, t) for t in todo]
        for i, fut in enumerate(as_completed(futs), 1):
            fh.write(json.dumps(fut.result()) + "\n")
            fh.flush()
            if i % 100 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)}  {time.time()-t0:.0f}s", flush=True)


def holm(tests, alpha=0.05):
    order = sorted(range(len(tests)), key=lambda i: tests[i]["p"])
    m, running = len(tests), 0.0
    for k, i in enumerate(order):
        running = max(running, min(1.0, (m - k) * tests[i]["p"]))
        tests[i]["p_holm"] = running
        tests[i]["sig"] = running < alpha


def report(out_file):
    from scipy.stats import mannwhitneyu, wilcoxon
    rows = [json.loads(l) for l in out_file.read_text().splitlines()]
    data = {}
    for r in rows:
        data.setdefault((r["algo"], r["problem"], r["variant"]), {})[r["seed"]] = r

    def vals(a, p, v, m):
        d = data[(a, p, v)]
        return {s: d[s][m] for s in d if d[s]["valid"]}

    L = ["# Confirmation round: results\n",
         f"Runs: {len(rows)}; invalid: {sum(not r['valid'] for r in rows)}; "
         f"max |F re-eval error|: {max(r['max_f_err'] for r in rows):.1e}; max n_eval: {max(r['n_eval'] for r in rows)}; "
         f"seeds {SEEDS[0]}-{SEEDS[-1]}\n"]

    L.append("## Median IGD per group\n")
    L.append("| Problem | Variant | " + " | ".join(ALGOS) + " |")
    L.append("|---|---|" + "---:|" * len(ALGOS))
    for p, _ in PROBLEMS:
        for v in VARIANTS:
            L.append(f"| {p} | {v} | " + " | ".join(
                f"{np.median(list(vals(a, p, v, 'IGD').values())):.3e}" for a in ALGOS) + " |")

    paired = []
    for alt in CONTRASTS:
        for p, _ in PROBLEMS:
            for v in VARIANTS:
                for m in ("IGD", "HV"):
                    A, B = vals("OADE", p, v, m), vals(alt, p, v, m)
                    ss = sorted(set(A) & set(B))
                    d = np.array([A[s] - B[s] for s in ss])
                    pv = 1.0 if np.all(d == 0) else wilcoxon(d, zero_method="wilcox").pvalue
                    good = (d < 0) if m == "IGD" else (d > 0)
                    paired.append(dict(alt=alt, problem=p, variant=v, metric=m, n=len(ss),
                                       median_diff=float(np.median(d)), oade_wins=int(good.sum()), p=float(pv)))
    holm(paired)

    def sym(t):
        if not t["sig"]:
            return "≈"
        good = t["median_diff"] < 0 if t["metric"] == "IGD" else t["median_diff"] > 0
        return "+" if good else "−"

    inter = []
    ratios = {}
    for alt in CONTRASTS:
        for p, _ in PROBLEMS:
            r = {}
            for v in VARIANTS:
                A, B = vals("OADE", p, v, "IGD"), vals(alt, p, v, "IGD")
                r[v] = np.array([math.log(B[s] / A[s]) for s in sorted(set(A) & set(B))])
                ratios[(alt, p, v)] = float(np.exp(np.median(r[v])))
            for v in SHIFT_RNG:
                pv = mannwhitneyu(r["original"], r[v], alternative="two-sided").pvalue
                inter.append(dict(alt=alt, problem=p, shift=v, ratio_orig=ratios[(alt, p, "original")],
                                  ratio_shift=ratios[(alt, p, v)], p=float(pv)))
    holm(inter)

    L.append("\n## OADE versus each arm\n")
    L.append("Cell: median per-seed IGD(arm)/IGD(OADE) [>1 favours OADE]; symbols IGD/HV after Holm over "
             "160 paired Wilcoxon tests: + OADE better, − arm better, ≈ NS.\n")
    for alt in CONTRASTS:
        L.append(f"### OADE vs {alt}\n")
        L.append("| Problem | " + " | ".join(VARIANTS) + " |")
        L.append("|---|" + "---|" * len(VARIANTS))
        for p, _ in PROBLEMS:
            cells = []
            for v in VARIANTS:
                ti = next(t for t in paired if (t["alt"], t["problem"], t["variant"], t["metric"]) == (alt, p, v, "IGD"))
                th = next(t for t in paired if (t["alt"], t["problem"], t["variant"], t["metric"]) == (alt, p, v, "HV"))
                cells.append(f"{ratios[(alt, p, v)]:.3g} ({sym(ti)}/{sym(th)}, {ti['oade_wins']}/30)")
            L.append(f"| {p} | " + " | ".join(cells) + " |")
        L.append("")

    L.append("## Interaction: original vs each shift (Mann-Whitney on per-seed log IGD ratios, Holm over 60)\n")
    L.append("| Arm | Problem | " + " | ".join(f"p Holm {v}" for v in SHIFT_RNG) + " |")
    L.append("|---|---|" + "---:|" * len(SHIFT_RNG))
    for alt in CONTRASTS:
        for p, _ in PROBLEMS:
            ts = [t for t in inter if t["alt"] == alt and t["problem"] == p]
            L.append(f"| {alt} | {p} | " + " | ".join(
                f"{t['p_holm']:.2g}{' *' if t['sig'] else ''}" for t in ts) + " |")

    L.append("\n## ZDT4 runs with IGD > 1e-2, out of 30\n")
    L.append("| Variant | " + " | ".join(ALGOS) + " |")
    L.append("|---|" + "---:|" * len(ALGOS))
    for v in VARIANTS:
        L.append(f"| {v} | " + " | ".join(
            str(sum(x > 1e-2 for x in vals(a, "zdt4", v, "IGD").values())) for a in ALGOS) + " |")

    text = "\n".join(L) + "\n"
    (OUT / "report.md").write_text(text, encoding="utf-8")
    json.dump(dict(paired=paired, interaction=inter), (OUT / "tests.json").open("w"), indent=1)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["smoke", "run", "report"], required=True)
    ap.add_argument("--jobs", type=int, default=10)
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if a.stage == "smoke":
        sanity()
        f = ROOT / "tmp/smoke/bias_location_confirm.jsonl"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.unlink(missing_ok=True)
        smoke = [t for t in tasks(SEEDS[:1]) if t[1] in ("zdt2", "zdt3") or t[0] == "OADE_random"]
        execute(smoke, a.jobs, f)
        for l in f.read_text().splitlines():
            r = json.loads(l)
            print(r["algo"], r["problem"], r["variant"], r["n_eval"], r["status"],
                  f"IGD={r.get('IGD', float('nan')):.3e}", f"err={r['max_f_err']:.0e}")
    elif a.stage == "run":
        execute(tasks(SEEDS), a.jobs, OUT / "runs.jsonl")
        report(OUT / "runs.jsonl")
    else:
        report(OUT / "runs.jsonl")
