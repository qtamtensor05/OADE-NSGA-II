# NSGA-II/SDR-OLS

Local reconstruction of NSGA-II/SDR-OLS based on the primary paper:

Zhang, Y.; Wang, G.; Wang, H. "NSGA-II/SDR-OLS: A Novel Large-Scale Many-Objective Optimization Method Using Opposition-Based Learning and Local Search." Mathematics 2023, 11, 1911.

[Official article and pseudocode](https://doi.org/10.3390/math11081911). See [corrections and unresolved pseudocode details](../baseline_paper_corrections.md) before claiming reproduction.

## What is included

- SDR non-dominated sorting with adaptive niche angle theta.
- OBL initialization using `x_opposite = xl + xu - x`.
- Gaussian local search using `omega+` and `omega-`.
- Basic GA variation implemented as binary tournament selection, SBX crossover, and polynomial mutation.
- No dependency on the existing `src/oade_nsga2` implementation.

## Usage

```python
from pymoo.problems import get_problem

from nsga2_sdr_ols import NSGAIISDROLS, ProblemAdapter

problem = ProblemAdapter(get_problem("zdt1", n_var=30))
solver = NSGAIISDROLS(
    problem,
    pop_size=100,
    n_gen=200,
    mu=0.0,
    sigma=0.1,
    seed=42,
)

population = solver.run()
F = solver.result_F()
X = solver.result_X()
```

The baseline visits every parent and variable, producing both neighbors. Its runner rejects a local-search cap. A standalone cap remains an explicitly modified experiment. A final partial neighborhood under a hard FE limit is sampled without replacement across the full neighborhood. The merged LS pool is ranked before GA and survives together with GA offspring. The paper's Algorithm 4 has inconsistent update statements, so this loop is a documented interpretation, not a verified author-code reproduction.

