"""One factor at a time (OFAT): explicit parameter lists, ZDT only."""
from copy import deepcopy
from pathlib import Path
import math

from shared.io.config import load_yaml_config
from research.benchmarking.provenance import digest

PARAMETERS = {"pop_size", "stagnation_patience", "stagnation_tolerance", "diversity_threshold",
              "restart_elite_ratio", "prob_de", "n_neighbors", "mean_F", "mean_CR"}
ZDT_DIMENSIONS = {"zdt1": 30, "zdt2": 30, "zdt3": 30, "zdt4": 10, "zdt6": 10}


def validate_settings(settings):
    if set(settings) != PARAMETERS | {"restart_mode"} or settings["restart_mode"] != "adaptive":
        raise ValueError("Expected explicit adaptive-v2 baseline settings")
    for key in PARAMETERS:
        value = settings[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Invalid number for {key}")
    for key in ("pop_size", "n_neighbors", "stagnation_patience"):
        if type(settings[key]) is not int or settings[key] < 1:
            raise ValueError(f"{key} must be a positive integer")
    if settings["pop_size"] < 4 or not 2 <= settings["n_neighbors"] <= settings["pop_size"]:
        raise ValueError("Need population >=4 and 2 <= n_neighbors <= population")
    for key in ("prob_de", "mean_F", "mean_CR", "diversity_threshold"):
        if not 0 < settings[key] <= 1:
            raise ValueError(f"{key} must be in (0, 1]")
    if settings["stagnation_tolerance"] <= 0:
        raise ValueError("stagnation_tolerance must be positive")
    if not 0.8 <= settings["restart_elite_ratio"] < 1:
        raise ValueError("Adaptive restart clamps elite ratio to >=0.8; levels below 0.8 are ineffective")


def design(cfg):
    if cfg.get("schema") != 1 or set(cfg) - {"schema", "study_id", "smoke", "algorithm_config", "global", "problems", "parameters"}:
        raise ValueError("Unsupported OFAT configuration; no selection, interaction or confirmation stages")
    baseline_file = load_yaml_config(Path(cfg["algorithm_config"]))
    if baseline_file.get("runner") != "local_oade":
        raise ValueError("Expected local OADE algorithm configuration")
    baseline = {"pop_size": cfg["global"]["pop_size"], **baseline_file["params"]}
    validate_settings(baseline)
    seeds = cfg["global"]["seeds"]
    if not seeds or len(seeds) != len(set(seeds)) or any(type(s) is not int or s < 0 for s in seeds):
        raise ValueError("Seeds must be unique nonnegative integers")
    if len(seeds) < 2:
        raise ValueError("Use at least two stochastic runs to describe variability")
    problems = cfg["problems"]
    if not problems or len({p["name"] for p in problems}) != len(problems):
        raise ValueError("Problems must be present and unique")
    for problem in problems:
        if set(problem) != {"name", "n_var"} or problem["name"] not in ZDT_DIMENSIONS or type(problem["n_var"]) is not int or problem["n_var"] < 2:
            raise ValueError("This pipeline accepts continuous ZDT1/2/3/4/6 with explicit dimensions only")
    grids = cfg["parameters"]
    if not grids or not set(grids) <= PARAMETERS:
        raise ValueError("Choose supported parameters and explicit lists of levels")
    candidates = [{"id": "baseline", "parameter": "baseline", "level": None, "settings": baseline}]
    for parameter, values in grids.items():
        if not isinstance(values, list) or not values or len(values) != len(set(values)) or baseline[parameter] not in values:
            raise ValueError(f"List for {parameter} must include its baseline exactly once")
        for value in values:
            settings = {**baseline, parameter: value}
            validate_settings(settings)
            if value != baseline[parameter]:
                candidates.append({"id": "level_" + digest([parameter, value])[:16],
                                   "parameter": parameter, "level": value, "settings": settings})
    cap = cfg["global"]["evaluation_budget"]
    if type(cap) is not int or cap < max(c["settings"]["pop_size"] for c in candidates):
        raise ValueError("Evaluation cap must cover the largest initial population")
    resolved = deepcopy(cfg)
    resolved["baseline_settings"] = baseline
    return resolved, candidates


def task_id(candidate_id, problem, seed):
    return digest([candidate_id, problem, seed])


def plan(cfg, candidates):
    runs = len(candidates) * len(cfg["problems"]) * len(cfg["global"]["seeds"])
    return {"method": "OFAT: change exactly one parameter at a time; no scoring or automatic selection",
            "parameters": len(cfg["parameters"]), "unique_configurations": len(candidates),
            "problems": [p["name"] for p in cfg["problems"]], "seeds_per_configuration_problem": len(cfg["global"]["seeds"]),
            "total_runs": runs, "evaluation_cap_per_run": cfg["global"]["evaluation_budget"],
            "evaluation_cap_total": runs * cfg["global"]["evaluation_budget"],
            "baseline_reuse": "one baseline run per problem/seed, referenced by each parameter list"}
