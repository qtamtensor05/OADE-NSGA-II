"""The single supported OADE mechanism configuration; not an options API."""
from types import MappingProxyType

FIXED_PARAMETERS = MappingProxyType({
    "initialization": "uniform",
    "restart": "adaptive",
    "probability_update": "success_rate",
    "stagnation_patience": 20,
    "stagnation_tolerance": 1e-4,
    "diversity_threshold": .02,
    "restart_elite_ratio": .8,
    "prob_de": .5,
    "n_neighbors": 5,
    "mean_F": .65,
    "mean_CR": .5,
    "obl_interval": 10,
    "obl_jump_rate": .2,
})
