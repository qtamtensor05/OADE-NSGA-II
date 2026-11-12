"""R-NSGA-II aspiration points computed without a Pareto-front oracle."""
import numpy as np

def make_rnsga2_ref_points(problem, initial_x: np.ndarray) -> np.ndarray:
    """
    Tạo aspiration points cho R-NSGA-II từ objective values của quần thể ban đầu.
    Không dùng Pareto front thật để tránh lợi thế oracle khi benchmark.
    """
    F0 = np.asarray(problem.evaluate(initial_x))
    if F0.ndim != 2:
        raise ValueError("problem.evaluate(initial_x) must return a 2D objective matrix")

    f_min = F0.min(axis=0)
    f_max = F0.max(axis=0)
    span = np.where((f_max - f_min) < 1e-12, 1.0, f_max - f_min)
    n_obj = F0.shape[1]

    if n_obj == 1:
        return (f_min + 0.1 * span)[None, :]

    rp1 = f_min + 0.2 * span
    rp2 = f_min + 0.2 * span
    rp1[0] = f_min[0] + 0.05 * span[0]
    rp2[0] = f_min[0] + 0.45 * span[0]
    rp1[-1] = f_min[-1] + 0.45 * span[-1]
    rp2[-1] = f_min[-1] + 0.05 * span[-1]

    return np.vstack([rp1, rp2])
