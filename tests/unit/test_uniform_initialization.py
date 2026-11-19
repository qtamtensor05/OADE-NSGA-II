import unittest
from unittest.mock import patch
import numpy as np
from pymoo.problems import get_problem
from research.oade_nsga2.algorithm import OADE_NSGAII
from research.oade_nsga2.core import ProblemWrapper
from research.oade_nsga2.operators import initialize_uniform
from shared.evaluation import BudgetedProblem
from shared.population import make_initial_population


class UniformInitializationTests(unittest.TestCase):
    def test_seed_matches_benchmark_and_costs_only_population(self):
        problem=get_problem('zdt4',n_var=10)
        counter=BudgetedProblem(problem,20)
        np.random.seed(999);before=np.random.get_state()
        population=initialize_uniform(ProblemWrapper(counter),20,seed=42)
        after=np.random.get_state()
        np.testing.assert_array_equal(before[1],after[1]);self.assertEqual(before[2:],after[2:])
        np.testing.assert_array_equal([i.X for i in population],make_initial_population(problem,20,42))
        np.testing.assert_array_equal([i.F for i in population],problem.evaluate(np.array([i.X for i in population])))
        self.assertEqual(counter.n_eval,20)

    def test_default_research_initialization_is_seeded_uniform(self):
        problem=get_problem('zdt1',n_var=10);outputs=[]
        for _ in range(2):
            np.random.seed(42);counter=BudgetedProblem(problem,20)
            solver=OADE_NSGAII(ProblemWrapper(counter),pop_size=20,n_gen=0)
            population=solver._build_initial_population(None)
            outputs.append(np.array([i.X for i in population]));self.assertEqual(counter.n_eval,20)
        np.testing.assert_array_equal(*outputs)
        self.assertTrue(np.all((outputs[0]>=problem.xl)&(outputs[0]<=problem.xu)))

    def test_supplied_population_does_not_call_sampler(self):
        problem=get_problem('zdt1',n_var=10);counter=BudgetedProblem(problem,20)
        solver=OADE_NSGAII(ProblemWrapper(counter),pop_size=20,n_gen=0)
        initial=make_initial_population(problem,20,42)
        with patch('research.oade_nsga2.algorithm.initialize_uniform',side_effect=AssertionError('Unexpected resampling')):
            population=solver._build_initial_population(initial)
        self.assertEqual(counter.n_eval,20)
        self.assertEqual({tuple(i.X) for i in population},{tuple(x) for x in initial})


if __name__=='__main__':unittest.main()
