"""Exploratory bias check for OADE-NSGA-II (not a production study).

H1 (bound repair): DE trials are repaired by np.clip. On ZDT1/ZDT6 the optimum
    lies on the lower bound (x_i=0, i>=2), so clipping may help artificially.
    Prediction if H1 holds: clip >> bounce-back on original ZDT1/6, and the gap
    shrinks or vanishes when the optimum is moved inside the box.
H2 (OBL centre bias): on ZDT4 the optimum x_i=0 (i>=2) is the centre of
    [-5,5], so static OBL x' = xl+xu-x = -x maps near-optimal points to
    near-optimal points. Prediction if H2 holds: periodic OBL helps on original
    ZDT4 but the benefit vanishes or reverses on shifted ZDT4.

Shifted problems keep bounds, objectives and Pareto front unchanged; only the
location of the optimal distance variables moves (fixed offset vector, RNG 12345).

Usage:  python analysis/bias_location_exploratory.py --stage smoke|run|report [--jobs N]
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
OUT = ROOT / "results/experiments/bias_location_exploratory_v1"

import numpy as np  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

POP, BUDGET = 100, 20_000
SEEDS = list(range(9000, 9030))          # fresh seeds, not 42-71 / 7000-7029
PROBLEMS = [("zdt1", 30), ("zdt6", 10), ("zdt4", 10)]
VARIANTS = ["original", "shifted"]
ALGOS = ["OADE", "OADE_bounce", "OADE_noOBL", "NSGA2"]


# ----------------------------------------------------------------- problems
def offsets(name: str, n_var: int) -> np.ndarray:
    rng = np.random.default_rng(12345)
    if name == "zdt4":
        return rng.uniform(-2.5, 2.5, n_var - 1)
    return rng.uniform(0.2, 0.8, n_var - 1)


def make_problem(name: str, n_var: int, variant: str):
    from pymoo.core.problem import Problem
    from pymoo.problems import get_problem

    base = get_problem(name, n_var=n_var)
    if variant == "original":
        return base
    o = offsets(name, n_var)

    class Shifted(Problem):
        def __init__(self):
            super().__init__(n_var=base.n_var, n_obj=base.n_obj, xl=base.xl, xu=base.xu)

        def _evaluate(self, x, out, *args, **kwargs):
            x = np.atleast_2d(x)
            z = x.copy()
            if name == "zdt4":
                z[:, 1:] = x[:, 1:] - o          # optimum at x_i = o_i, inside box
            else:
                z[:, 1:] = np.abs(x[:, 1:] - o)  # optimum at x_i = o_i, z in [0,0.8]
            out["F"] = base.evaluate(z)

    return Shifted()


# ----------------------------------------------------------------- solvers
def _oade_classes():
    from oade_nsga2 import OADE_NSGAII
    from oade_nsga2 import algorithm as alg_mod

    class OADENoOBL(OADE_NSGAII):
        def _generate_periodic_obl(self, gen):
            return []

    class OADEBounce(OADE_NSGAII):
        """Same RNG order as production; only the DE trial repair differs.

        Out-of-bound genes are placed uniformly between the violated bound and
        the target's gene (standard DE midpoint/bounce style repair)."""

        def _create_one_child(self, idx, neighbor_indices):
            if np.random.rand() < self.prob_de:
                inf = np.full(self.n_var, np.inf)
                child = alg_mod.de_mutation(idx, self.population, neighbor_indices,
                                            -inf, inf, self.n_var, self.mean_F, self.mean_CR)
                t = self.population[idx].X
                x = child.X
                lo, hi = x < self.xl, x > self.xu
                if lo.any():
                    x[lo] = self.xl[lo] + np.random.rand(lo.sum()) * (t[lo] - self.xl[lo])
                if hi.any():
                    x[hi] = self.xu[hi] - np.random.rand(hi.sum()) * (self.xu[hi] - t[hi])
                child.X = x
                return child
            return alg_mod.sbx_crossover_mutation(
                alg_mod.tournament_selection(self.population),
                alg_mod.tournament_selection(self.population),
                self.xl, self.xu, self.n_var, self.pc, self.pm, self.eta_c, self.eta_m)

    return {"OADE": OADE_NSGAII, "OADE_bounce": OADEBounce, "OADE_noOBL": OADENoOBL}


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
        init = make_initial_population(problem, POP, seed)
        alg = NSGA2(pop_size=POP, sampling=FixedInitialSampling(init, seed))
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
        cls = _oade_classes()[algo]
        solver = cls(ProblemWrapper(budgeted), pop_size=POP, n_gen=BUDGET, seed=seed)
        try:
            solver.run()
        except EvaluationBudgetExceeded:
            pass
        x = np.asarray([i.X for i in solver.population], float)
        f = np.asarray([i.F for i in solver.population], float)
    runtime = time.perf_counter() - t0
    x, f = non_dominated_xy(x, f)
    # re-evaluate on a fresh problem instance to guard against state leaks
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


REF = json.loads((ROOT / "results/experiments/zdt_six_fixed_oade_v1/config/reference_fronts.json").read_text())


# ----------------------------------------------------------------- stages
def sanity():
    """The shifted optimum must map onto the unchanged Pareto front."""
    for name, n_var in PROBLEMS:
        p = make_problem(name, n_var, "shifted")
        x1 = np.linspace(0, 1, 11)
        x = np.column_stack([x1, np.tile(offsets(name, n_var), (11, 1))])
        f = p.evaluate(x)
        g = make_problem(name, n_var, "original")
        x0 = np.column_stack([x1, np.zeros((11, n_var - 1))])
        f0 = g.evaluate(x0)
        assert np.allclose(f, f0), name
        # and the original optimum is no longer optimal
        assert not np.allclose(p.evaluate(x0), f0), name
    print("sanity: shifted optimum reproduces the true front; original optimum is displaced")


def tasks(seeds):
    return [(a, n, d, v, s) for (n, d) in PROBLEMS for v in VARIANTS for a in ALGOS for s in seeds]


def execute(task_list, jobs, out_file):
    from concurrent.futures import ProcessPoolExecutor, as_completed
    done = {}
    if out_file.exists():
        for line in out_file.read_text().splitlines():
            r = json.loads(line)
            done[(r["algo"], r["problem"], r["variant"], r["seed"])] = r
    todo = [t for t in task_list if (t[0], t[1], t[3], t[4]) not in done]
    print(f"{len(task_list)} tasks, {len(todo)} to run, jobs={jobs}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=jobs) as ex, out_file.open("a") as fh:
        futs = [ex.submit(run_one, t) for t in todo]
        for i, fut in enumerate(as_completed(futs), 1):
            fh.write(json.dumps(fut.result()) + "\n")
            fh.flush()
            if i % 50 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)}  {time.time()-t0:.0f}s", flush=True)


def report(out_file):
    from scipy.stats import mannwhitneyu, wilcoxon
    rows = [json.loads(l) for l in out_file.read_text().splitlines()]
    data = {}
    for r in rows:
        data.setdefault((r["algo"], r["problem"], r["variant"]), {})[r["seed"]] = r
    n_invalid = sum(not r["valid"] for r in rows)
    lines = [f"# Bias check results\n", f"Runs: {len(rows)}; invalid: {n_invalid}; "
             f"max |F re-eval error|: {max(r['max_f_err'] for r in rows):.1e}; "
             f"max n_eval: {max(r['n_eval'] for r in rows)}\n"]

    def vals(a, p, v, m):
        d = data[(a, p, v)]
        return {s: d[s][m] for s in d if d[s]["valid"]}

    lines.append("## Median IGD (Q1-Q3) / median HV\n")
    lines.append("| Problem | Variant | " + " | ".join(ALGOS) + " |")
    lines.append("|---|---|" + "---:|" * len(ALGOS))
    for p, _ in PROBLEMS:
        for v in VARIANTS:
            cells = []
            for a in ALGOS:
                i = np.array(list(vals(a, p, v, "IGD").values()))
                h = np.array(list(vals(a, p, v, "HV").values()))
                q1, md, q3 = np.percentile(i, [25, 50, 75])
                cells.append(f"{md:.3e} ({q1:.2e}-{q3:.2e}) / {np.median(h):.4f}")
            lines.append(f"| {p} | {v} | " + " | ".join(cells) + " |")

    # Pre-specified paired family: 3 contrasts x 3 problems x 2 variants x 2 metrics = 36
    contrasts = [("OADE", "OADE_bounce"), ("OADE", "OADE_noOBL"), ("OADE", "NSGA2")]
    tests = []
    for ref_a, alt in contrasts:
        for p, _ in PROBLEMS:
            for v in VARIANTS:
                for m in ("IGD", "HV"):
                    A, B = vals(ref_a, p, v, m), vals(alt, p, v, m)
                    seeds = sorted(set(A) & set(B))
                    d = np.array([A[s] - B[s] for s in seeds])
                    pval = 1.0 if np.all(d == 0) else wilcoxon(d, zero_method="wilcox").pvalue
                    better = (d < 0) if m == "IGD" else (d > 0)
                    tests.append(dict(contrast=f"{ref_a} vs {alt}", problem=p, variant=v, metric=m,
                                      n=len(seeds), median_diff=float(np.median(d)),
                                      oade_wins=int(better.sum()), p=float(pval)))
    holm(tests)
    lines.append("\n## Paired Wilcoxon, global Holm over 36 endpoints (diff = OADE - other)\n")
    lines.append("| Contrast | Problem | Variant | Metric | median diff | OADE wins/30 | p Holm | verdict |")
    lines.append("|---|---|---|---|---:|---:|---:|---|")
    for t in tests:
        lines.append(f"| {t['contrast']} | {t['problem']} | {t['variant']} | {t['metric']} | "
                     f"{t['median_diff']:+.3e} | {t['oade_wins']} | {t['p_holm']:.3g} | {t['verdict']} |")

    # Interaction: does the per-seed log IGD ratio change when the optimum is moved?
    inter = []
    for ref_a, alt in contrasts:
        for p, _ in PROBLEMS:
            r = {}
            for v in VARIANTS:
                A, B = vals(ref_a, p, v, "IGD"), vals(alt, p, v, "IGD")
                r[v] = np.array([math.log(B[s] / A[s]) for s in sorted(set(A) & set(B))])
            pval = mannwhitneyu(r["original"], r["shifted"], alternative="two-sided").pvalue
            inter.append(dict(contrast=f"{ref_a} vs {alt}", problem=p,
                              ratio_orig=float(np.exp(np.median(r["original"]))),
                              ratio_shift=float(np.exp(np.median(r["shifted"]))), p=float(pval)))
    holm(inter)
    lines.append("\n## Interaction: median IGD(other)/IGD(OADE), original vs shifted "
                 "(Mann-Whitney on per-seed log ratios, Holm over 9)\n")
    lines.append("| Contrast | Problem | ratio original | ratio shifted | p Holm | verdict |")
    lines.append("|---|---|---:|---:|---:|---|")
    for t in inter:
        lines.append(f"| {t['contrast']} | {t['problem']} | {t['ratio_orig']:.3f} | "
                     f"{t['ratio_shift']:.3f} | {t['p_holm']:.3g} | {t['verdict']} |")
    lines.append("\nratio > 1: OADE (clip, with OBL) has lower IGD than the other algorithm.")

    # ZDT4 local-front trapping
    lines.append("\n## ZDT4 runs with IGD > 1e-2 (trapped on local fronts), out of 30\n")
    lines.append("| Variant | " + " | ".join(ALGOS) + " |")
    lines.append("|---|" + "---:|" * len(ALGOS))
    for v in VARIANTS:
        lines.append(f"| {v} | " + " | ".join(
            str(sum(x > 1e-2 for x in vals(a, "zdt4", v, "IGD").values())) for a in ALGOS) + " |")
    text = "\n".join(lines) + "\n"
    (OUT / "report.md").write_text(text, encoding="utf-8")
    json.dump(dict(paired=tests, interaction=inter), (OUT / "tests.json").open("w"), indent=1)
    print(text)


def holm(tests, alpha=0.05):
    order = sorted(range(len(tests)), key=lambda i: tests[i]["p"])
    m, running = len(tests), 0.0
    for k, i in enumerate(order):
        running = max(running, min(1.0, (m - k) * tests[i]["p"]))
        tests[i]["p_holm"] = running
    for t in tests:
        if t["p_holm"] >= alpha:
            t["verdict"] = "NS"
        elif "ratio_orig" in t:
            t["verdict"] = "differs"
        else:
            good = t["median_diff"] < 0 if t["metric"] == "IGD" else t["median_diff"] > 0
            t["verdict"] = "OADE better" if good else "other better"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["smoke", "run", "report"], required=True)
    ap.add_argument("--jobs", type=int, default=10)
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if a.stage == "smoke":
        sanity()
        f = ROOT / "tmp/smoke/bias_location_exploratory.jsonl"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.unlink(missing_ok=True)
        execute(tasks(SEEDS[:1]), a.jobs, f)
        for l in f.read_text().splitlines():
            r = json.loads(l)
            print(r["algo"], r["problem"], r["variant"], r["n_eval"], r["status"],
                  f"IGD={r.get('IGD', float('nan')):.3e}", f"{r['runtime']:.1f}s", f"err={r['max_f_err']:.0e}")
    elif a.stage == "run":
        execute(tasks(SEEDS), a.jobs, OUT / "runs.jsonl")
        report(OUT / "runs.jsonl")
    else:
        report(OUT / "runs.jsonl")
