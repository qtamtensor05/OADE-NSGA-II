"""Fixed-solver mechanism observations and paired leave-one-out ZDT study."""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

from oade_nsga2 import OADE_NSGAII, ProblemWrapper
from shared.evaluation import BudgetedProblem, EvaluationBudgetExceeded, validate_result
from shared.fronts import non_dominated_xy
from shared.io.csv_io import write_csv
from research.benchmarking.statistics import paired_wilcoxon_rows, holm_adjust

VARIANTS = ('full', 'no_obl', 'no_restart', 'fixed_f_cr', 'fixed_pde',
            'global_neighborhood', 'sbx_only', 'de_only')


class ObservedOADE(OADE_NSGAII):
    """Research-only interventions; production fixed policy remains untouched."""

    def __init__(self, *args, variant='full', **kwargs):
        super().__init__(*args, **kwargs)
        if variant not in VARIANTS:
            raise ValueError(variant)
        self.variant = variant
        self.events = []
        self.trace = []
        self.generation = 0
        self.collapse_checks = 0
        if variant == 'global_neighborhood':
            self.n_neighbors = self.pop_size - 1

    def _generate_offspring(self, gen):
        self.generation = gen + 1
        return super()._generate_offspring(gen)

    def _create_one_child(self, idx, neighbors):
        before = self.prob_de
        if self.variant in ('sbx_only', 'de_only'):
            self.prob_de = float(self.variant == 'de_only')
        try:
            return super()._create_one_child(idx, neighbors)
        finally:
            self.prob_de = before

    def _observe(self, mechanism, operation):
        counter = self.problem._prob
        event = dict(mechanism=mechanism, generation=len(self.trace)+1,
                     n_eval_before=counter.n_eval, status='error')
        try:
            result = operation()
            event['status'] = 'completed'
            return result
        except EvaluationBudgetExceeded:
            event['status'] = 'budget_blocked'
            raise
        finally:
            event['evaluations'] = counter.n_eval-event['n_eval_before']
            self.events.append(event)

    def _generate_periodic_obl(self, gen):
        if self.variant == 'no_obl' or gen % 10:
            return []
        return self._observe('obl', lambda: super(ObservedOADE, self)._generate_periodic_obl(gen))

    def _is_diversity_collapsed(self):
        self.collapse_checks += 1
        return super()._is_diversity_collapsed()

    def _adaptive_restart(self):
        if self.variant != 'no_restart':
            before = self.mean_F, self.mean_CR
            result = self._observe('restart', super()._adaptive_restart)
            if self.variant == 'fixed_f_cr':
                self.mean_F, self.mean_CR = before
            return result

    def _update_adaptive_parameters(self, offspring, *, reference_population=None):
        before = (self.mean_F, self.mean_CR, self.prob_de)
        super()._update_adaptive_parameters(offspring, reference_population=reference_population)
        if self.variant == 'fixed_f_cr':
            self.mean_F, self.mean_CR = before[:2]
        if self.variant in ('fixed_pde', 'sbx_only', 'de_only'):
            self.prob_de = before[2]
        survivors = {id(i) for i in self.population}
        row = dict(generation=self.generation, n_eval=self.problem._prob.n_eval,
                   mean_F=self.mean_F, mean_CR=self.mean_CR, pde=self.prob_de,
                   f_cr_changed=int(before[:2] != (self.mean_F, self.mean_CR)),
                   pde_changed=int(before[2] != self.prob_de))
        for mode in ('de', 'sbx', 'obl'):
            trials = [i for i in offspring if i.creation_mode == mode]
            row[mode+'_trials'] = len(trials)
            row[mode+'_retained'] = sum(id(i) in survivors for i in trials)
        self.trace.append(row)


def run_one(problem_name, seed, variant, population, budget):
    problem = get_problem(problem_name, n_var=10)
    reference = np.asarray(problem.pareto_front())
    igd, hv = IGD(reference), HV(ref_point=reference.max(axis=0)+.1)
    counter = BudgetedProblem(problem, budget)
    solver = ObservedOADE(ProblemWrapper(counter), pop_size=population,
                          n_gen=budget, seed=seed, variant=variant)
    start = time.perf_counter()
    try:
        solver.run()
    except EvaluationBudgetExceeded:
        pass
    x, f = non_dominated_xy(np.asarray([i.X for i in solver.population]),
                            np.asarray([i.F for i in solver.population]))
    valid = validate_result(x, f, problem).valid
    return dict(problem=problem_name, algorithm=variant, seed=seed, run_idx=seed,
                valid=valid, IGD=float(igd(f)) if valid else None,
                HV=float(hv(f)) if valid else None, n_eval=counter.n_eval,
                runtime_seconds=time.perf_counter()-start, generations=len(solver.trace),
                collapse_checks=solver.collapse_checks, final_x=x.tolist(), final_f=f.tolist(),
                reference=reference.tolist(), trace=solver.trace, events=solver.events)


def outputs(directory, records):
    derived = directory/'derived'
    raw = [{k:v for k,v in r.items() if not isinstance(v, list)} for r in records]
    write_csv(derived/'runs.csv', raw, list(raw[0]))
    for key in ('events', 'trace'):
        rows = [dict(problem=r['problem'], algorithm=r['algorithm'], seed=r['seed'], **t)
                for r in records for t in r[key]]
        write_csv(derived/(key+'.csv'), rows, list(rows[0]) if rows else ['problem','algorithm','seed'])
    rates = []
    for r in records:
        for mechanism in ('obl','restart','f_cr','pde','de','sbx'):
            events = [e for e in r['events'] if e['mechanism'] == mechanism]
            if mechanism in ('obl','restart'):
                numerator = sum(e['status']=='completed' for e in events)
            elif mechanism in ('f_cr','pde'):
                numerator = sum(t[mechanism+'_changed'] for t in r['trace'])
            else:
                numerator = sum(t[mechanism+'_trials'] > 0 for t in r['trace'])
            rates.append(dict(problem=r['problem'], algorithm=r['algorithm'], seed=r['seed'],
                              mechanism=mechanism, activations=numerator,
                              denominator=r['generations'] + int(any(e['generation'] > r['generations'] for e in r['events'])),
                              rate=numerator/(r['generations'] + int(any(e['generation'] > r['generations'] for e in r['events']))) if r['generations'] else None,
                              evaluations=sum(e['evaluations'] for e in events),
                              budget_blocked=sum(e['status']=='budget_blocked' for e in events)))
    write_csv(derived/'activation.csv', rates, list(rates[0]))
    comparisons = paired_wilcoxon_rows(raw, 'full')
    adjusted = holm_adjust([r['p_value'] for r in comparisons])
    for row, p in zip(comparisons, adjusted):
        row['p_adjusted_holm'] = p
        row['significant'] = p < .05
        row['excluded_pairs'] = len({r['seed'] for r in records})-row['n_pairs']
        # Override helper's per-metric decision after global correction.
        row['result'] = ('full_better' if row['rank_biserial_effect'] > 0 else 'ablation_better') if p < .05 else 'not_significant'
    write_csv(derived/'impact.csv', comparisons, list(comparisons[0]) if comparisons else ['problem'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path('results/experiments/oade_mechanism_zdt46'))
    parser.add_argument('--runs', type=int, default=30)
    parser.add_argument('--seed-base', type=int, default=42)
    parser.add_argument('--population', type=int, default=100)
    parser.add_argument('--budget', type=int, default=20000)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--stage', choices=('plan','run'), default='plan')
    args = parser.parse_args(argv)
    if args.runs < 2 or args.seed_base < 0 or args.population < 6 or args.budget < 2*args.population+2:
        parser.error('Require runs>=2, seed>=0, population>=6, budget>=2*population+2')
    source_paths = [Path(__file__), *Path(__file__).parents[2].joinpath('oade_nsga2').glob('*.py')]
    manifest = dict(runs=args.runs, seed_base=args.seed_base, population=args.population,
                    budget=args.budget, variants=VARIANTS, problems=['zdt4','zdt6'],
                    sources={str(p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths})
    manifest = json.loads(json.dumps(manifest))
    print(json.dumps(manifest, indent=2))
    if args.stage == 'plan':
        return
    directory = args.out_dir
    directory.mkdir(parents=True, exist_ok=True)
    path = directory/'manifest.json'
    if path.exists():
        if not args.resume or json.loads(path.read_text()) != manifest:
            raise ValueError('Existing output requires --resume and matching manifest')
    elif any(directory.iterdir()):
        raise ValueError('Output directory must be empty')
    else:
        path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    primary = directory/'primary'
    primary.mkdir(exist_ok=True)
    records = []
    for problem in manifest['problems']:
        for seed in range(args.seed_base, args.seed_base+args.runs):
            for variant in VARIANTS:
                target = primary/f'{problem}_{seed}_{variant}.json'
                if target.exists():
                    record = json.loads(target.read_text())
                else:
                    record = run_one(problem, seed, variant, args.population, args.budget)
                    temporary = target.with_suffix('.tmp')
                    temporary.write_text(json.dumps(record, allow_nan=False), encoding='utf-8')
                    temporary.replace(target)
                records.append(record)
                print(f'{problem} seed={seed} {variant}: n_eval={record["n_eval"]}', flush=True)
    outputs(directory, records)


if __name__ == '__main__':
    main()
