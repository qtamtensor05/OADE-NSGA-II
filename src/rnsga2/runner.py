"""Own the RNSGA2 library invocation and algorithm-specific setup."""
from pymoo.algorithms.moo.rnsga2 import RNSGA2
from shared.pymoo_execution import run_pymoo
from .reference_points import make_rnsga2_ref_points

def configure_reference_points(problem, params, initial_x):
    if "ref_points" not in params:
        params["ref_points"] = make_rnsga2_ref_points(problem, initial_x)


def run(spec, problem, pop_size, budget, initial_x, seed, recorder):
    configure = configure_reference_points if spec.auto_ref_points else None
    return run_pymoo(RNSGA2, spec, problem, pop_size, budget, initial_x, seed, recorder, configure=configure, warning_module=r"pymoo\.algorithms\.moo\.rnsga2")
