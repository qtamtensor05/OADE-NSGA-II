"""Observe adaptive-restart execution without changing search decisions."""
from .algorithm import OADE_NSGAII


class InstrumentedOADE(OADE_NSGAII):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telemetry = dict(trigger_checks=0, collapse_checks=0, collapse_positive=0,
                              restart_attempts=0, restart_completed=0, restart_evaluations=0)

    def _check_and_handle_stagnation(self, stagnation_counter, last_ideal):
        self.telemetry["trigger_checks"] += 1
        return super()._check_and_handle_stagnation(stagnation_counter, last_ideal)

    def _is_diversity_collapsed(self):
        self.telemetry["collapse_checks"] += 1
        collapsed = super()._is_diversity_collapsed()
        self.telemetry["collapse_positive"] += int(collapsed)
        return collapsed

    def _adaptive_restart(self):
        self.telemetry["restart_attempts"] += 1
        counter = self.problem._prob
        before = counter.n_eval
        try:
            super()._adaptive_restart()
        except BaseException:
            raise
        else:
            self.telemetry["restart_completed"] += 1
        finally:
            self.telemetry["restart_evaluations"] += counter.n_eval - before
