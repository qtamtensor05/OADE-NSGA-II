"""Route solver contracts to the owning algorithm package; no solver bodies here."""
from oade_nsga2.runner import run as _run_oade
from cgde_nsga2.runner import run as _run_cgde
from nsga2_sdr_ols.runner import run as _run_sdr
from ce_moea.runner import run as _run_ce
from nsga2.runner import run as run_nsga2
from rnsga2.runner import run as run_rnsga2
from dnsga2.runner import run as run_dnsga2
from shared.pymoo_execution import FixedInitialSampling, PymooConvergenceCallback
from shared.fronts import non_dominated_xy
from .convergence import ConvergenceRecorder

PYMOO_RUNNERS = {
    "pymoo.algorithms.moo.nsga2.NSGA2": run_nsga2,
    "pymoo.algorithms.moo.rnsga2.RNSGA2": run_rnsga2,
    "pymoo.algorithms.moo.dnsga2.DNSGA2": run_dnsga2,
}

def _run_pymoo(spec, problem, pop_size, budget, initial_x, seed, recorder):
    if spec.class_path not in PYMOO_RUNNERS:
        raise ValueError(f"No algorithm package registered for pymoo class: {spec.class_path}")
    return PYMOO_RUNNERS[spec.class_path](spec, problem, pop_size, budget, initial_x, seed, recorder)

RUNNERS = {
    "pymoo": _run_pymoo, "local_oade": _run_oade, "local_cgde_nsga2": _run_cgde,
    "local_nsga2_sdr_ols": _run_sdr, "local_ce_moea": _run_ce,
}

def run_algorithm(spec, problem, pop_size, budget, initial_x, seed, recorder, *, runners=None):
    available = RUNNERS if runners is None else runners
    if spec.runner not in available:
        raise ValueError(f"unsupported runner: {spec.runner}")
    return available[spec.runner](spec, problem, pop_size, budget, initial_x, seed, recorder)

__all__ = ["ConvergenceRecorder", "FixedInitialSampling", "PymooConvergenceCallback",
           "non_dominated_xy", "run_algorithm", "RUNNERS"]
