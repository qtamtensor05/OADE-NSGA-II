"""
Vòng lặp tiến hoá chính của NSGA-II cải tiến.
"""

from __future__ import annotations

from typing import Callable, List, Optional

import random

import numpy as np

from .core import CreationMode, Individual, ProblemWrapper
from .configuration import FIXED_PARAMETERS
from shared.population import make_initial_population
from .operators import (
    _make_evaluated_individual,
    de_mutation,
    generate_obl_offspring,
    get_neighborhood_indices,
    initialize_from_data,
    sbx_crossover_mutation,
    tournament_selection,
)
from .selection import environmental_selection, remove_duplicates


class OADE_NSGAII:
    """Fixed OADE: uniform initialization, adaptive restart, periodic OBL,
    neighborhood DE/SBX, corrected F/CR learning and success-rate pDE.

    Only run dimensions and the seed are arguments; no ablation switches.
    """

    def __init__(self, problem: ProblemWrapper, pop_size: int = 100, n_gen: int = 100, *, seed: int = 42) -> None:
        self.seed = seed
        self.problem  = problem
        self.pop_size = pop_size
        self.n_gen    = n_gen
        self.n_var    = problem.n_var
        self.n_obj    = problem.n_obj
        self.xl       = problem.xl
        self.xu       = problem.xu

        # Trạng thái thích nghi khởi đầu theo cấu hình cố định
        self.mean_F  = FIXED_PARAMETERS["mean_F"]  # trung bình phân phối Cauchy của scale factor F
        self.mean_CR = FIXED_PARAMETERS["mean_CR"]  # trung bình phân phối Normal của crossover rate CR
        self.prob_de = FIXED_PARAMETERS["prob_de"]  # xác suất chọn DE thay vì SBX
        self.n_neighbors = FIXED_PARAMETERS["n_neighbors"]

        # Tham số SBX và Polynomial Mutation
        self.pc    = 0.9                                           # xác suất lai ghép
        self.pm    = 1.0 / (self.n_var * np.log(max(pop_size, 2)))  # xác suất đột biến mỗi gene
        self.eta_c = 20.0
        self.eta_m = 20.0

        self.stagnation_patience = FIXED_PARAMETERS["stagnation_patience"]
        self.stagnation_tolerance = FIXED_PARAMETERS["stagnation_tolerance"]
        self.restart_elite_ratio = FIXED_PARAMETERS["restart_elite_ratio"]
        self.diversity_threshold = FIXED_PARAMETERS["diversity_threshold"]

        # Trạng thái runtime
        self.population: List[Individual] = []
        self.history:    List[np.ndarray] = []  # lịch sử F mỗi thế hệ

    # Vòng lặp chính
    def run(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> np.ndarray:
        """Run with reproducible uniform initialization and the fixed mechanisms."""
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.mean_F = FIXED_PARAMETERS["mean_F"]
        self.mean_CR = FIXED_PARAMETERS["mean_CR"]
        self.prob_de = FIXED_PARAMETERS["prob_de"]
        self.population = self._build_initial_population()
        self.history.clear()

        last_ideal         = None
        stagnation_counter = 0

        for gen in range(self.n_gen):
            stagnation_counter, last_ideal = self._check_and_handle_stagnation(
                stagnation_counter, last_ideal
            )

            offspring = self._generate_offspring(gen)
            self._evaluate_unevaluated(offspring)

            adaptation_pool = self.population + offspring
            combined        = remove_duplicates(adaptation_pool)
            combined        = self._fill_if_too_small(combined)
            self.population = environmental_selection(combined, self.pop_size, self.n_obj)

            self._update_adaptive_parameters(offspring, reference_population=adaptation_pool)
            self.history.append(np.array([ind.F for ind in self.population]))

            if progress_callback is not None:
                progress_callback(gen + 1, self.n_gen)

        return np.array([ind.F for ind in self.population])

    # Khởi tạo
    def _build_initial_population(self) -> List[Individual]:
        initial_x = make_initial_population(self.problem, self.pop_size, self.seed)
        pop = initialize_from_data(self.problem, initial_x)
        return environmental_selection(pop, self.pop_size, self.n_obj)

    # Sinh con lai
    def _generate_offspring(self, gen: int) -> List[Individual]:
        """Sinh toàn bộ con lai cho thế hệ này: DE hoặc SBX theo prob_de, thêm OBL mỗi 10 thế hệ."""
        neighbor_count = self.n_neighbors
        neighbor_indices = get_neighborhood_indices(self.population, neighbor_count)

        offspring = [
            self._create_one_child(i, neighbor_indices)
            for i in range(self.pop_size)
        ]

        offspring += self._generate_periodic_obl(gen)

        return offspring

    def _generate_periodic_obl(self, gen: int) -> List[Individual]:
        """Periodic injection only; independent of initialization and restart."""
        if gen % FIXED_PARAMETERS["obl_interval"] == 0:
            return generate_obl_offspring(self.population, self.problem, self.xl, self.xu,
                                          jump_rate=FIXED_PARAMETERS["obl_jump_rate"])
        return []

    def _create_one_child(self, idx: int, neighbor_indices: np.ndarray) -> Individual:
        """Tạo một con lai bằng DE (theo prob_de) hoặc SBX."""
        if np.random.rand() < self.prob_de:
            return de_mutation(
                idx, self.population, neighbor_indices,
                self.xl, self.xu, self.n_var, self.mean_F, self.mean_CR,
            )
        return sbx_crossover_mutation(
            tournament_selection(self.population),
            tournament_selection(self.population),
            self.xl, self.xu, self.n_var, self.pc, self.pm, self.eta_c, self.eta_m,
        )

    def _evaluate_unevaluated(self, offspring: List[Individual]) -> None:
        """Đánh giá batch tất cả con lai chưa có F. OBL offspring đã được đánh giá trước."""
        unevaluated = [ind for ind in offspring if ind.F is None]
        if not unevaluated:
            return

        x_batch = np.array([ind.X for ind in unevaluated])
        f_batch = self.problem.evaluate(x_batch)
        for ind, f in zip(unevaluated, f_batch):
            ind.F = f.flatten().copy()

    # Trì trệ và partial restart
    def _check_and_handle_stagnation(
        self, stagnation_counter: int, last_ideal: Optional[np.ndarray]
    ) -> tuple[int, np.ndarray]:
        """Đếm thế hệ trì trệ; restart khi đủ kiên nhẫn. Trả về (counter, ideal_point) mới."""
        current_ideal = np.min([ind.F for ind in self.population], axis=0)

        if last_ideal is not None:
            improved       = np.linalg.norm(current_ideal - last_ideal) >= self.stagnation_tolerance
            stagnation_counter = 0 if improved else stagnation_counter + 1

        if stagnation_counter >= self.stagnation_patience:
            if self._is_diversity_collapsed():
                self._adaptive_restart()
                stagnation_counter = 0
            else:
                stagnation_counter = self.stagnation_patience // 2

        return stagnation_counter, current_ideal

    def _is_diversity_collapsed(self) -> bool:
        """Kiểm tra xem quần thể có thực sự bị sụp đổ đa dạng không."""
        if len(self.population) < 2:
            return True
        f_mat = np.array([ind.F for ind in self.population])
        f_min = np.min(f_mat, axis=0)
        f_max = np.max(f_mat, axis=0)
        if float(np.max(f_max - f_min)) < 1e-3:
            return True

        x_mat = np.array([ind.X for ind in self.population])
        span = np.where((self.xu - self.xl) > 1e-12, self.xu - self.xl, 1.0)
        norm_x = (x_mat - self.xl) / span
        max_dim_std = float(np.max(np.std(norm_x, axis=0)))
        return max_dim_std < self.diversity_threshold

    def _adaptive_restart(self) -> None:
        """
        Conservative adaptive restart: giữ lại đa số cá thể ưu tú (80%),
        chỉ làm mới phần còn lại bằng đột biến OBL/Gauss quanh elite,
        bảo toàn tham số thích nghi DE.
        """
        n_keep = max(int(self.pop_size * self.restart_elite_ratio), int(self.pop_size * 0.8))
        elite = self.population[:n_keep]
        n_new = self.pop_size - len(elite)
        if n_new <= 0:
            return

        x_elite = np.array([ind.X for ind in elite])
        new_xs = []
        for _ in range(n_new):
            base = x_elite[np.random.randint(len(x_elite))]
            if np.random.rand() < 0.5:
                cand = self.xl + self.xu - base + np.random.normal(0, 0.05, self.n_var) * (self.xu - self.xl)
            else:
                cand = base + np.random.normal(0, 0.1, self.n_var) * (self.xu - self.xl)
            cand = np.clip(cand, self.xl, self.xu)
            new_xs.append(cand)

        x_new = np.array(new_xs)
        f_new = self.problem.evaluate(x_new)
        new_inds = [_make_evaluated_individual(x_new[i], f_new[i]) for i in range(n_new)]

        self.population = environmental_selection(elite + new_inds, self.pop_size, self.n_obj)
        self.mean_F = 0.8 * self.mean_F + 0.2 * 0.5
        self.mean_CR = 0.8 * self.mean_CR + 0.2 * 0.5

    def _fill_if_too_small(self, population: List[Individual]) -> List[Individual]:
        """Bổ sung cá thể ngẫu nhiên nếu remove_duplicates làm quần thể thiếu hụt."""
        missing = self.pop_size - len(population)
        if missing <= 0:
            return population

        x_fill = self.xl + np.random.rand(missing, self.n_var) * (self.xu - self.xl)
        f_fill = self.problem.evaluate(x_fill)
        extras = [_make_evaluated_individual(x_fill[i], f_fill[i]) for i in range(missing)]
        return population + extras

    # Cập nhật tham số thích nghi
    def _update_adaptive_parameters(
        self, offspring: List[Individual], *, reference_population: Optional[List[Individual]] = None
    ) -> None:
        """
        Cập nhật prob_de theo tỷ lệ thành công; F/CR theo DE không bị trội.

        prob_de : success-rate only.
        success_rate chuẩn hóa tỷ lệ không bị trội theo số trial từng toán tử;
        giữ nguyên nếu thiếu toán tử hoặc cả hai không thành công.
        mean_F  : Lehmer mean của F — ưu giá trị lớn, khuyến khích khám phá
        mean_CR : trung bình cộng của CR

        F/CR success means nondominated in the evaluated parent/offspring pool
        BEFORE objective-space duplicate removal or crowding truncation. Each DE
        trial contributes once, including duplicate trials. Selection metadata
        may be missing/stale on discarded individuals and is not a success test.
        """
        de_offspring  = [ind for ind in offspring if ind.creation_mode == CreationMode.DE]
        sbx_offspring = [ind for ind in offspring if ind.creation_mode == CreationMode.SBX]
        successful_de = []
        successful_sbx = []
        if de_offspring or sbx_offspring:
            pool = reference_population if reference_population is not None else self.population + offspring
            objectives = np.asarray([ind.F for ind in pool])
            for ind in de_offspring + sbx_offspring:
                dominated = np.any(np.all(objectives <= ind.F, axis=1)
                                   & np.any(objectives < ind.F, axis=1))
                if not dominated:
                    (successful_de if ind.creation_mode == CreationMode.DE else successful_sbx).append(ind)

        total = len(de_offspring) + len(sbx_offspring)
        before = self.prob_de
        target = None
        if total > 0:
            if de_offspring and sbx_offspring:
                rate_de = len(successful_de) / len(de_offspring)
                rate_sbx = len(successful_sbx) / len(sbx_offspring)
                if rate_de + rate_sbx > 0:
                    target = rate_de / (rate_de + rate_sbx)
            if target is not None:
                self.prob_de = float(np.clip(0.9 * before + 0.1 * target, 0.2, 0.8))
        if successful_de:
            f_values     = np.array([ind.used_F  for ind in successful_de])
            cr_values    = np.array([ind.used_CR for ind in successful_de])
            lehmer_mean_F = float(np.mean(f_values ** 2) / np.mean(f_values))
            self.mean_F  = 0.9 * self.mean_F  + 0.1 * lehmer_mean_F
            self.mean_CR = 0.9 * self.mean_CR + 0.1 * float(np.mean(cr_values))
