"""Observe adaptive-restart execution without changing search decisions."""
from .algorithm import OADE_NSGAII
import numpy as np
from shared.evaluation import EvaluationBudgetExceeded


class InstrumentedOADE(OADE_NSGAII):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telemetry = dict(trigger_checks=0, collapse_checks=0, collapse_positive=0,
                              restart_attempts=0, restart_completed=0, restart_evaluations=0,
                              stagnation_eligible=0, restart_budget_blocked=0)
        self.restart_events = []
        self.restart_metric = None
        self.initialization_evidence = {}

    def _build_initial_population(self, initial_x):
        counter = self.problem._prob
        before = counter.n_eval
        population = super()._build_initial_population(initial_x)
        self.initialization_evidence = {
            "evaluations": counter.n_eval - before,
            "x": [i.X.tolist() for i in population],
            "f": [i.F.tolist() for i in population]}
        return population

    def _check_and_handle_stagnation(self, stagnation_counter, last_ideal):
        self.telemetry["trigger_checks"] += 1
        ideal = np.min([ind.F for ind in self.population], axis=0)
        count = (0 if np.linalg.norm(ideal - last_ideal) >= self.stagnation_tolerance
                 else stagnation_counter + 1) if last_ideal is not None else stagnation_counter
        self.telemetry["stagnation_eligible"] += int(count >= self.stagnation_patience)
        return super()._check_and_handle_stagnation(stagnation_counter, last_ideal)

    def _is_diversity_collapsed(self):
        self.telemetry["collapse_checks"] += 1
        collapsed = super()._is_diversity_collapsed()
        self.telemetry["collapse_positive"] += int(collapsed)
        return collapsed

    def _adaptive_restart(self):
        return self._observe_restart(super()._adaptive_restart, "adaptive")

    def _partial_restart(self):
        return self._observe_restart(super()._partial_restart, "classic")

    def _observe_restart(self, operation, mode):
        self.telemetry["restart_attempts"] += 1
        counter = self.problem._prob
        before = counter.n_eval
        event = {"mode": mode, "generation": self.telemetry["trigger_checks"],
                 "n_eval_before": before, "status": "error"}
        if self.restart_metric:
            event["before"] = self.restart_metric(np.asarray([i.F for i in self.population]))
        try:
            operation()
        except EvaluationBudgetExceeded:
            event["status"] = "budget_blocked"
            self.telemetry["restart_budget_blocked"] += 1
            raise
        else:
            self.telemetry["restart_completed"] += 1
            event["status"] = "completed" if counter.n_eval > before else "no_op"
        finally:
            self.telemetry["restart_evaluations"] += counter.n_eval - before
            event["n_eval_after"] = counter.n_eval
            event["evaluations"] = counter.n_eval - before
            if self.restart_metric:
                event["after"] = self.restart_metric(np.asarray([i.F for i in self.population]))
            self.restart_events.append(event)
