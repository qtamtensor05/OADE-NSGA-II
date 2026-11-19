# Phụ lục: độ nhạy tham số cơ chế OADE

[Báo cáo kết luận](mechanism_sensitivity_report.md). Tạo từ các bảng đã audit; giữ đủ 124 endpoint và 70 nhóm, không chỉ chọn kết quả có ý nghĩa.

## Toàn bộ so sánh

n=30 cặp seed mỗi dòng, không loại cặp. Δ=median(tham chiếu−mức thử); IGD dương/HV âm thiên về mức thử. Rank-biserial dương thiên về tham chiếu. CI 95% percentile (20.000 bootstrap cặp seed) chưa hiệu chỉnh đa kiểm định; p Holm hiệu chỉnh chung 124 endpoint. Thắng/thua/hòa theo hướng có lợi cho mức thử. Mốc initial là full; mốc held là cùng tham số held tại mức production (F=0,65; CR=0,5; pDE=0,5). NS là chưa phát hiện khác biệt, không phải tương đương.

| Bài | Tham số | Mode | Mức | Metric | Δ [CI 95%] | W | p thô | p Holm | Rank-biserial | Mức thử thắng/thua/hòa | Kết luận |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| zdt4 | obl_interval | initial | 5 | IGD | 6.008e-5 [-2.225e-4; 8.316e-4] | 1.81e2 | 2.988e-1 | 1e0 | -2.215e-1 | 15/15/0 | NS |
| zdt4 | obl_interval | initial | 5 | HV | -3.765e-4 [-1.133e-3; 4.9e-4] | 1.73e2 | 2.286e-1 | 1e0 | -2.559e-1 | 17/13/0 | NS |
| zdt6 | obl_interval | initial | 5 | IGD | -1.039e-4 [-2.725e-4; 2.748e-5] | 1.55e2 | 1.142e-1 | 1e0 | 3.333e-1 | 10/20/0 | NS |
| zdt6 | obl_interval | initial | 5 | HV | 6.223e-5 [-1.081e-4; 2.994e-4] | 1.82e2 | 3.085e-1 | 1e0 | 2.172e-1 | 14/16/0 | NS |
| zdt4 | obl_interval | initial | 20 | IGD | -1.611e-3 [-3.027e-2; 7.242e-4] | 1.4e2 | 5.769e-2 | 1e0 | 3.978e-1 | 12/18/0 | NS |
| zdt4 | obl_interval | initial | 20 | HV | 3.77e-3 [-1.489e-3; 5.017e-2] | 1.39e2 | 5.492e-2 | 1e0 | 4.022e-1 | 12/18/0 | NS |
| zdt6 | obl_interval | initial | 20 | IGD | 1.711e-5 [-1.423e-4; 1.404e-4] | 2.2e2 | 8.078e-1 | 1e0 | -5.376e-2 | 16/14/0 | NS |
| zdt6 | obl_interval | initial | 20 | HV | -1.868e-5 [-9.308e-5; 1.084e-4] | 2.19e2 | 7.922e-1 | 1e0 | -5.806e-2 | 16/14/0 | NS |
| zdt4 | obl_interval | initial | 40 | IGD | -8.302e-3 [-1.21e-1; -4.823e-4] | 9.6e1 | 4.032e-3 | 4.072e-1 | 5.871e-1 | 7/23/0 | NS |
| zdt4 | obl_interval | initial | 40 | HV | 1.535e-2 [1.359e-3; 1.826e-1] | 9.6e1 | 4.032e-3 | 4.072e-1 | 5.871e-1 | 7/23/0 | NS |
| zdt6 | obl_interval | initial | 40 | IGD | -3.567e-5 [-1.936e-4; 1.425e-4] | 2.08e2 | 6.263e-1 | 1e0 | 1.054e-1 | 14/16/0 | NS |
| zdt6 | obl_interval | initial | 40 | HV | 7.693e-5 [-1.079e-4; 1.062e-4] | 2.31e2 | 9.838e-1 | 1e0 | -6.452e-3 | 13/17/0 | NS |
| zdt4 | obl_jump_rate | initial | 0.05 | IGD | -3.735e-2 [-1.216e-1; -2.912e-3] | 4.8e1 | 4.408e-5 | 5.069e-3 | 7.935e-1 | 5/25/0 | Mốc tốt hơn |
| zdt4 | obl_jump_rate | initial | 0.05 | HV | 6.036e-2 [4.204e-3; 1.873e-1] | 5.1e1 | 6.287e-5 | 6.915e-3 | 7.806e-1 | 5/25/0 | Mốc tốt hơn |
| zdt6 | obl_jump_rate | initial | 0.05 | IGD | -2.762e-5 [-2.288e-4; 6.567e-5] | 1.63e2 | 1.579e-1 | 1e0 | 2.989e-1 | 13/17/0 | NS |
| zdt6 | obl_jump_rate | initial | 0.05 | HV | 8.325e-5 [-3.617e-5; 2.41e-4] | 1.84e2 | 3.285e-1 | 1e0 | 2.086e-1 | 13/17/0 | NS |
| zdt4 | obl_jump_rate | initial | 0.1 | IGD | -1.463e-3 [-6.458e-3; -3.429e-4] | 1.17e2 | 1.643e-2 | 1e0 | 4.968e-1 | 10/20/0 | NS |
| zdt4 | obl_jump_rate | initial | 0.1 | HV | 2.723e-3 [8.762e-4; 1.172e-2] | 1.15e2 | 1.454e-2 | 1e0 | 5.054e-1 | 9/21/0 | NS |
| zdt6 | obl_jump_rate | initial | 0.1 | IGD | -5.513e-5 [-1.218e-4; 7.226e-5] | 2.03e2 | 5.561e-1 | 1e0 | 1.269e-1 | 13/17/0 | NS |
| zdt6 | obl_jump_rate | initial | 0.1 | HV | -4.139e-5 [-2.353e-4; 2.074e-4] | 2.23e2 | 8.553e-1 | 1e0 | -4.086e-2 | 17/13/0 | NS |
| zdt4 | obl_jump_rate | initial | 0.4 | IGD | 3.815e-4 [-3.12e-4; 7.999e-4] | 1.96e2 | 4.645e-1 | 1e0 | -1.57e-1 | 18/12/0 | NS |
| zdt4 | obl_jump_rate | initial | 0.4 | HV | -7.755e-4 [-2.278e-3; -7.837e-5] | 1.84e2 | 3.285e-1 | 1e0 | -2.086e-1 | 20/10/0 | NS |
| zdt6 | obl_jump_rate | initial | 0.4 | IGD | 9.424e-6 [-9.702e-5; 6.953e-5] | 2.06e2 | 5.978e-1 | 1e0 | 1.14e-1 | 16/14/0 | NS |
| zdt6 | obl_jump_rate | initial | 0.4 | HV | 3.796e-5 [-9.158e-5; 1.769e-4] | 2.07e2 | 6.12e-1 | 1e0 | 1.097e-1 | 13/17/0 | NS |
| zdt4 | stagnation_patience | initial | 5 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | stagnation_patience | initial | 5 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | stagnation_patience | initial | 5 | IGD | 0 [0; 2.666e-5] | 9.2e1 | 9.039e-1 | 1e0 | -3.158e-2 | 10/9/11 | NS |
| zdt6 | stagnation_patience | initial | 5 | HV | 0 [0; 5.312e-5] | 8.6e1 | 7.172e-1 | 1e0 | 9.474e-2 | 8/11/11 | NS |
| zdt4 | stagnation_patience | initial | 10 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | stagnation_patience | initial | 10 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | stagnation_patience | initial | 10 | IGD | 0 [0; 0] | 2.1e1 | 5.076e-1 | 1e0 | -2.364e-1 | 6/4/20 | NS |
| zdt6 | stagnation_patience | initial | 10 | HV | 0 [0; 0] | 2.2e1 | 5.751e-1 | 1e0 | 2e-1 | 4/6/20 | NS |
| zdt4 | stagnation_patience | initial | 40 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | stagnation_patience | initial | 40 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | stagnation_patience | initial | 40 | IGD | 0 [0; 0] | 1e1 | 9.165e-1 | 1e0 | -4.762e-2 | 2/4/24 | NS |
| zdt6 | stagnation_patience | initial | 40 | HV | 0 [0; 0] | 6e0 | 3.454e-1 | 1e0 | -4.286e-1 | 5/1/24 | NS |
| zdt4 | stagnation_tolerance | initial | 1e-05 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | stagnation_tolerance | initial | 1e-05 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | stagnation_tolerance | initial | 1e-05 | IGD | 0 [0; 0] | 0 | 1.088e-1 | 1e0 | 1e0 | 0/3/27 | NS |
| zdt6 | stagnation_tolerance | initial | 1e-05 | HV | 0 [0; 0] | 3e0 | 1e0 | 1e0 | 0 | 2/1/27 | NS |
| zdt4 | stagnation_tolerance | initial | 0.001 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | stagnation_tolerance | initial | 0.001 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | stagnation_tolerance | initial | 0.001 | IGD | 0 [0; 0] | 1.5e1 | 6.744e-1 | 1e0 | 1.667e-1 | 4/4/22 | NS |
| zdt6 | stagnation_tolerance | initial | 0.001 | HV | 0 [0; 0] | 8e0 | 1.614e-1 | 1e0 | 5.556e-1 | 3/5/22 | NS |
| zdt4 | diversity_threshold | initial | 0.01 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | diversity_threshold | initial | 0.01 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | diversity_threshold | initial | 0.01 | IGD | 0 [0; 0] | 1e1 | 9.165e-1 | 1e0 | -4.762e-2 | 2/4/24 | NS |
| zdt6 | diversity_threshold | initial | 0.01 | HV | 0 [0; 0] | 6e0 | 3.454e-1 | 1e0 | -4.286e-1 | 5/1/24 | NS |
| zdt4 | diversity_threshold | initial | 0.05 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | diversity_threshold | initial | 0.05 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | diversity_threshold | initial | 0.05 | IGD | -2.493e-5 [-1.937e-4; 7.599e-5] | 1.52e2 | 3.74e-1 | 1e0 | 1.958e-1 | 12/15/3 | NS |
| zdt6 | diversity_threshold | initial | 0.05 | HV | 0 [-1.169e-4; 1.73e-4] | 1.59e2 | 4.711e-1 | 1e0 | 1.587e-1 | 13/14/3 | NS |
| zdt4 | diversity_threshold | initial | 0.1 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | diversity_threshold | initial | 0.1 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | diversity_threshold | initial | 0.1 | IGD | 1.026e-5 [-1.837e-4; 1.451e-4] | 1.95e2 | 6.266e-1 | 1e0 | 1.034e-1 | 15/14/1 | NS |
| zdt6 | diversity_threshold | initial | 0.1 | HV | -9.588e-6 [-1.169e-4; 1.404e-4] | 1.94e2 | 6.114e-1 | 1e0 | 1.08e-1 | 15/14/1 | NS |
| zdt4 | restart_elite_ratio | initial | 0.9 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | restart_elite_ratio | initial | 0.9 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | restart_elite_ratio | initial | 0.9 | IGD | 0 [0; 0] | 6e0 | 3.454e-1 | 1e0 | -4.286e-1 | 5/1/24 | NS |
| zdt6 | restart_elite_ratio | initial | 0.9 | HV | 0 [0; 0] | 7e0 | 4.631e-1 | 1e0 | -3.333e-1 | 3/3/24 | NS |
| zdt4 | restart_elite_ratio | initial | 0.95 | IGD | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt4 | restart_elite_ratio | initial | 0.95 | HV | 0 [0; 0] | 0 | 1e0 | 1e0 | 0 | 0/0/30 | NS |
| zdt6 | restart_elite_ratio | initial | 0.95 | IGD | 0 [0; 0] | 5e0 | 2.489e-1 | 1e0 | -5.238e-1 | 4/2/24 | NS |
| zdt6 | restart_elite_ratio | initial | 0.95 | HV | 0 [0; 0] | 9e0 | 7.532e-1 | 1e0 | -1.429e-1 | 4/2/24 | NS |
| zdt4 | n_neighbors | initial | 3 | IGD | -3.35e-4 [-3.784e-3; 3.816e-4] | 1.85e2 | 3.387e-1 | 1e0 | 2.043e-1 | 12/18/0 | NS |
| zdt4 | n_neighbors | initial | 3 | HV | 4.531e-4 [-8.432e-4; 5.476e-3] | 1.89e2 | 3.818e-1 | 1e0 | 1.871e-1 | 13/17/0 | NS |
| zdt6 | n_neighbors | initial | 3 | IGD | -5.861e-6 [-1.23e-4; 1.495e-4] | 1.94e2 | 4.4e-1 | 1e0 | -1.656e-1 | 14/16/0 | NS |
| zdt6 | n_neighbors | initial | 3 | HV | -8.614e-5 [-1.596e-4; 2.314e-6] | 1.66e2 | 1.772e-1 | 1e0 | -2.86e-1 | 19/11/0 | NS |
| zdt4 | n_neighbors | initial | 10 | IGD | -3.862e-5 [-9.327e-4; 7.842e-4] | 2.23e2 | 8.553e-1 | 1e0 | -4.086e-2 | 14/16/0 | NS |
| zdt4 | n_neighbors | initial | 10 | HV | 1.918e-5 [-2.325e-3; 2.495e-3] | 2.21e2 | 8.236e-1 | 1e0 | -4.946e-2 | 15/15/0 | NS |
| zdt6 | n_neighbors | initial | 10 | IGD | 6.614e-6 [-2.04e-4; 1.233e-4] | 1.99e2 | 5.028e-1 | 1e0 | 1.441e-1 | 15/15/0 | NS |
| zdt6 | n_neighbors | initial | 10 | HV | 8.264e-5 [-8.982e-5; 3.872e-4] | 1.5e2 | 9.195e-2 | 1e0 | 3.548e-1 | 12/18/0 | NS |
| zdt4 | n_neighbors | initial | 20 | IGD | -1.068e-5 [-7.856e-4; 6.598e-4] | 2.32e2 | 1e0 | 1e0 | 2.151e-3 | 15/15/0 | NS |
| zdt4 | n_neighbors | initial | 20 | HV | -1.526e-6 [-1.052e-3; 1.778e-3] | 2.32e2 | 1e0 | 1e0 | 2.151e-3 | 15/15/0 | NS |
| zdt6 | n_neighbors | initial | 20 | IGD | -7.621e-5 [-2.479e-4; 1.972e-5] | 1.52e2 | 1.004e-1 | 1e0 | 3.462e-1 | 11/19/0 | NS |
| zdt6 | n_neighbors | initial | 20 | HV | 2.413e-4 [3.019e-5; 2.855e-4] | 1.26e2 | 2.774e-2 | 1e0 | 4.581e-1 | 9/21/0 | NS |
| zdt4 | mean_F | held | 0.4 | IGD | 2.223e-4 [6.506e-5; 4.223e-4] | 9.6e1 | 4.032e-3 | 4.072e-1 | -5.871e-1 | 23/7/0 | NS |
| zdt4 | mean_F | held | 0.4 | HV | -7.512e-4 [-1.341e-3; -3.211e-4] | 5.7e1 | 1.233e-4 | 1.332e-2 | -7.548e-1 | 23/7/0 | Mức thử tốt hơn |
| zdt6 | mean_F | held | 0.4 | IGD | -1.956e-4 [-3.281e-4; -8.562e-5] | 8.6e1 | 1.864e-3 | 1.92e-1 | 6.301e-1 | 7/23/0 | NS |
| zdt6 | mean_F | held | 0.4 | HV | 3.828e-4 [1.8e-4; 6.025e-4] | 4.8e1 | 4.408e-5 | 5.069e-3 | 7.935e-1 | 6/24/0 | Mốc tốt hơn |
| zdt4 | mean_F | held | 0.5 | IGD | 3.519e-4 [1.838e-4; 5.382e-4] | 4.9e1 | 4.968e-5 | 5.565e-3 | -7.892e-1 | 25/5/0 | Mức thử tốt hơn |
| zdt4 | mean_F | held | 0.5 | HV | -8.086e-4 [-1.438e-3; -6.453e-4] | 1e1 | 8.009e-8 | 9.691e-6 | -9.57e-1 | 27/3/0 | Mức thử tốt hơn |
| zdt6 | mean_F | held | 0.5 | IGD | -1.309e-4 [-2.446e-4; -9.905e-5] | 5e1 | 5.593e-5 | 6.208e-3 | 7.849e-1 | 6/24/0 | Mốc tốt hơn |
| zdt6 | mean_F | held | 0.5 | HV | 2.358e-4 [8.214e-5; 4.007e-4] | 4.8e1 | 4.408e-5 | 5.069e-3 | 7.935e-1 | 5/25/0 | Mốc tốt hơn |
| zdt4 | mean_F | held | 0.8 | IGD | -1.62e-3 [-7.034e-3; -5.314e-4] | 3.8e1 | 1.218e-5 | 1.425e-3 | 8.366e-1 | 3/27/0 | Mốc tốt hơn |
| zdt4 | mean_F | held | 0.8 | HV | 3.403e-3 [1.405e-3; 1.338e-2] | 4e1 | 1.598e-5 | 1.853e-3 | 8.28e-1 | 4/26/0 | Mốc tốt hơn |
| zdt6 | mean_F | held | 0.8 | IGD | -8.912e-5 [-2.424e-4; -8.367e-6] | 1.33e2 | 4.049e-2 | 1e0 | 4.28e-1 | 9/21/0 | NS |
| zdt6 | mean_F | held | 0.8 | HV | 4.542e-5 [-1.463e-4; 1.211e-4] | 2.17e2 | 7.611e-1 | 1e0 | 6.667e-2 | 13/17/0 | NS |
| zdt4 | mean_F | held | 0.9 | IGD | -2.859e-3 [-7.769e-3; -1.733e-3] | 1.3e1 | 1.639e-7 | 1.967e-5 | 9.441e-1 | 4/26/0 | Mốc tốt hơn |
| zdt4 | mean_F | held | 0.9 | HV | 6.267e-3 [3.166e-3; 1.379e-2] | 5e0 | 1.863e-8 | 2.291e-6 | 9.785e-1 | 1/29/0 | Mốc tốt hơn |
| zdt6 | mean_F | held | 0.9 | IGD | -7.196e-5 [-2.166e-4; 2.471e-5] | 1.86e2 | 3.492e-1 | 1e0 | 2e-1 | 10/20/0 | NS |
| zdt6 | mean_F | held | 0.9 | HV | -5.823e-5 [-1.65e-4; 4.971e-5] | 1.98e2 | 4.898e-1 | 1e0 | -1.484e-1 | 18/12/0 | NS |
| zdt4 | mean_CR | held | 0.1 | IGD | -5.042e-4 [-2.686e-2; 6.275e-4] | 1.75e2 | 2.449e-1 | 1e0 | 2.473e-1 | 12/18/0 | NS |
| zdt4 | mean_CR | held | 0.1 | HV | 1.453e-3 [-1.705e-3; 3.84e-2] | 1.82e2 | 3.085e-1 | 1e0 | 2.172e-1 | 12/18/0 | NS |
| zdt6 | mean_CR | held | 0.1 | IGD | 1.714e-5 [-1.494e-4; 1.492e-4] | 2.31e2 | 9.838e-1 | 1e0 | 6.452e-3 | 16/14/0 | NS |
| zdt6 | mean_CR | held | 0.1 | HV | 1.606e-4 [-1.502e-4; 2.846e-4] | 1.7e2 | 2.054e-1 | 1e0 | 2.688e-1 | 13/17/0 | NS |
| zdt4 | mean_CR | held | 0.3 | IGD | 5.298e-4 [-2.664e-4; 1.73e-3] | 1.77e2 | 2.621e-1 | 1e0 | -2.387e-1 | 19/11/0 | NS |
| zdt4 | mean_CR | held | 0.3 | HV | -1.011e-3 [-3.849e-3; 7.935e-4] | 1.79e2 | 2.801e-1 | 1e0 | -2.301e-1 | 19/11/0 | NS |
| zdt6 | mean_CR | held | 0.3 | IGD | 9.402e-5 [-4.484e-5; 2.595e-4] | 1.37e2 | 4.971e-2 | 1e0 | -4.108e-1 | 17/13/0 | NS |
| zdt6 | mean_CR | held | 0.3 | HV | -3.223e-4 [-5.159e-4; -1.563e-4] | 7e1 | 4.601e-4 | 4.831e-2 | -6.989e-1 | 23/7/0 | Mức thử tốt hơn |
| zdt4 | mean_CR | held | 0.7 | IGD | -7.03e-4 [-2.903e-3; 3.11e-4] | 1.86e2 | 3.492e-1 | 1e0 | 2e-1 | 11/19/0 | NS |
| zdt4 | mean_CR | held | 0.7 | HV | 1.833e-3 [-1.049e-3; 6.287e-3] | 1.92e2 | 4.161e-1 | 1e0 | 1.742e-1 | 11/19/0 | NS |
| zdt6 | mean_CR | held | 0.7 | IGD | -1.743e-4 [-3.395e-4; -1.249e-5] | 1.1e2 | 1.06e-2 | 1e0 | 5.269e-1 | 9/21/0 | NS |
| zdt6 | mean_CR | held | 0.7 | HV | 3.626e-4 [1.461e-4; 5.423e-4] | 5.2e1 | 7.057e-5 | 7.692e-3 | 7.763e-1 | 6/24/0 | Mốc tốt hơn |
| zdt4 | mean_CR | held | 0.9 | IGD | -3.803e-4 [-1.921e-3; 1.668e-4] | 2.09e2 | 6.408e-1 | 1e0 | 1.011e-1 | 11/19/0 | NS |
| zdt4 | mean_CR | held | 0.9 | HV | 1.169e-3 [-1.508e-4; 3.276e-3] | 2.12e2 | 6.85e-1 | 1e0 | 8.817e-2 | 10/20/0 | NS |
| zdt6 | mean_CR | held | 0.9 | IGD | -3.754e-4 [-4.678e-4; -2.853e-4] | 2.7e1 | 2.349e-6 | 2.772e-4 | 8.839e-1 | 5/25/0 | Mốc tốt hơn |
| zdt6 | mean_CR | held | 0.9 | HV | 7.094e-4 [5.695e-4; 8.468e-4] | 8e0 | 4.657e-8 | 5.681e-6 | 9.656e-1 | 3/27/0 | Mốc tốt hơn |
| zdt4 | prob_de | held | 0.2 | IGD | -2.087e-2 [-9.82e-2; -2.758e-3] | 6.4e1 | 2.563e-4 | 2.717e-2 | 7.247e-1 | 3/27/0 | Mốc tốt hơn |
| zdt4 | prob_de | held | 0.2 | HV | 3.597e-2 [6.63e-3; 1.56e-1] | 6.2e1 | 2.091e-4 | 2.238e-2 | 7.333e-1 | 3/27/0 | Mốc tốt hơn |
| zdt6 | prob_de | held | 0.2 | IGD | -2.244e-4 [-3.045e-4; -1.118e-4] | 7.9e1 | 1.038e-3 | 1.08e-1 | 6.602e-1 | 7/23/0 | NS |
| zdt6 | prob_de | held | 0.2 | HV | 4.937e-4 [4.06e-4; 6.482e-4] | 4e0 | 1.304e-8 | 1.617e-6 | 9.828e-1 | 2/28/0 | Mốc tốt hơn |
| zdt4 | prob_de | held | 0.35 | IGD | -5.021e-4 [-3.374e-3; 5.864e-4] | 1.74e2 | 2.367e-1 | 1e0 | 2.516e-1 | 13/17/0 | NS |
| zdt4 | prob_de | held | 0.35 | HV | 8.073e-4 [-3.736e-4; 6.088e-3] | 1.64e2 | 1.642e-1 | 1e0 | 2.946e-1 | 11/19/0 | NS |
| zdt6 | prob_de | held | 0.35 | IGD | -1.921e-4 [-2.568e-4; -9.216e-5] | 1.45e2 | 7.324e-2 | 1e0 | 3.763e-1 | 9/21/0 | NS |
| zdt6 | prob_de | held | 0.35 | HV | 2.768e-4 [3.815e-5; 4.97e-4] | 8.8e1 | 2.188e-3 | 2.232e-1 | 6.215e-1 | 9/21/0 | NS |
| zdt4 | prob_de | held | 0.65 | IGD | 3.664e-4 [-7.219e-4; 1.012e-3] | 2.2e2 | 8.078e-1 | 1e0 | -5.376e-2 | 17/13/0 | NS |
| zdt4 | prob_de | held | 0.65 | HV | -7.444e-4 [-2.099e-3; 1.628e-3] | 2.19e2 | 7.922e-1 | 1e0 | -5.806e-2 | 18/12/0 | NS |
| zdt6 | prob_de | held | 0.65 | IGD | 9.378e-5 [-4.382e-5; 1.635e-4] | 1.88e2 | 3.707e-1 | 1e0 | -1.914e-1 | 17/13/0 | NS |
| zdt6 | prob_de | held | 0.65 | HV | -7.271e-5 [-2.762e-4; 9.051e-5] | 1.63e2 | 1.579e-1 | 1e0 | -2.989e-1 | 19/11/0 | NS |
| zdt4 | prob_de | held | 0.8 | IGD | 5.52e-4 [1.302e-4; 1.331e-3] | 1.19e2 | 1.853e-2 | 1e0 | -4.882e-1 | 21/9/0 | NS |
| zdt4 | prob_de | held | 0.8 | HV | -1.632e-3 [-2.796e-3; -8.143e-4] | 1.01e2 | 5.776e-3 | 5.661e-1 | -5.656e-1 | 23/7/0 | NS |
| zdt6 | prob_de | held | 0.8 | IGD | 6.762e-5 [-9.344e-5; 3.019e-4] | 1.41e2 | 6.057e-2 | 1e0 | -3.935e-1 | 17/13/0 | NS |
| zdt6 | prob_de | held | 0.8 | HV | -4.902e-4 [-7.739e-4; -3.207e-4] | 1.5e1 | 2.552e-7 | 3.037e-5 | -9.355e-1 | 28/2/0 | Mức thử tốt hơn |

## Đủ 70 nhóm

Mỗi nhóm 30/30 lượt hợp lệ. Ô mean (best) ghi trung bình và giá trị tốt nhất trong 30 run: IGD min, HV max; hai best có thể thuộc hai seed khác nhau. SD không hiển thị, vẫn giữ trong CSV nguồn. Median [Q1; Q3] mô tả phân bố, không phải CI. Full chỉ chạy một lần mỗi bài/seed dù dùng chung trong nhiều contrast. Runtime là median giây/lượt trong môi trường tám worker có telemetry. In đậm giá trị tốt nhất trong 35 cấu hình của cùng bài: IGD/runtime nhỏ nhất, HV lớn nhất; xét riêng mean, median và best-run trên số liệu chưa làm tròn, giữ mọi đồng hạng. Số hiển thị 4 chữ số có nghĩa; số nhìn bằng nhau sau làm tròn không nhất thiết đồng hạng. In đậm không phải kết luận kiểm định hay tham số tối ưu.

| Bài | Algorithm ID | Tham số | Mức | Mode | IGD mean (best) | IGD median [Q1; Q3] | HV mean (best) | HV median [Q1; Q3] | Runtime (s) | FE min–max |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| zdt4 | full | baseline | — | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.332e0 | 19901–20000 |
| zdt4 | level_bc857e0271b391b7 | obl_interval | 5 | initial | 9.756e-3 (4.67e-3) | 5.202e-3 [4.962e-3; 6.273e-3] | 8.61e-1 (8.696e-1) | 8.682e-1 [8.658e-1; 8.691e-1] | 5.281e0 | 19901–20000 |
| zdt4 | level_b9e41374078f1def | obl_interval | 20 | initial | 4.736e-2 (4.466e-3) | 8.112e-3 [5.238e-3; 4.966e-2] | 8.006e-1 (8.698e-1) | 8.62e-1 [7.909e-1; 8.683e-1] | 5.357e0 | 19901–20000 |
| zdt4 | level_da967aa31e1c53de | obl_interval | 40 | initial | 8.029e-2 (4.81e-3) | 3.119e-2 [5.735e-3; 1.3e-1] | 7.539e-1 (8.688e-1) | 8.246e-1 [6.786e-1; 8.669e-1] | 5.285e0 | 19901–20000 |
| zdt4 | level_3c6496cae0000993 | obl_jump_rate | 0.05 | initial | 1.233e-1 (4.858e-3) | 7.216e-2 [6.452e-3; 1.555e-1] | 6.984e-1 (8.693e-1) | 7.627e-1 [6.196e-1; 8.652e-1] | 5.326e0 | 19901–20000 |
| zdt4 | level_71437a93f3d42084 | obl_jump_rate | 0.1 | initial | 4.168e-2 (4.702e-3) | 7.858e-3 [5.648e-3; 3.081e-2] | 8.129e-1 (8.694e-1) | 8.63e-1 [8.324e-1; 8.668e-1] | 5.352e0 | 19902–20000 |
| zdt4 | level_21521e2a1326e190 | obl_jump_rate | 0.4 | initial | 4.718e-2 (4.552e-3) | 5.023e-3 [4.701e-3; 6.186e-3] | 8.137e-1 (8.701e-1) | 8.689e-1 [8.665e-1; 8.693e-1] | 5.175e0 | 19901–20000 |
| zdt4 | level_fad6779d34994396 | stagnation_patience | 5 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.414e0 | 19901–20000 |
| zdt4 | level_fd9743e30c6b7e4c | stagnation_patience | 10 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.37e0 | 19901–20000 |
| zdt4 | level_605e5e1df48d2f0b | stagnation_patience | 40 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.321e0 | 19901–20000 |
| zdt4 | level_081a970edcd7d9c0 | stagnation_tolerance | 1e-05 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.288e0 | 19901–20000 |
| zdt4 | level_0f6357b99e389c0c | stagnation_tolerance | 0.001 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.302e0 | 19901–20000 |
| zdt4 | level_6660b9018786355d | diversity_threshold | 0.01 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.19e0 | 19901–20000 |
| zdt4 | level_75acf398f87065c5 | diversity_threshold | 0.05 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.331e0 | 19901–20000 |
| zdt4 | level_e711d25086fadbb2 | diversity_threshold | 0.1 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.255e0 | 19901–20000 |
| zdt4 | level_68ad8d9eb2cc0549 | restart_elite_ratio | 0.9 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.268e0 | 19901–20000 |
| zdt4 | level_2b9171e95155c918 | restart_elite_ratio | 0.95 | initial | 1.719e-2 (4.68e-3) | 5.414e-3 [5.012e-3; 9.372e-3] | 8.483e-1 (8.696e-1) | 8.677e-1 [8.604e-1; 8.686e-1] | 5.266e0 | 19901–20000 |
| zdt4 | level_7faf73034731b468 | n_neighbors | 3 | initial | 3.342e-2 (4.529e-3) | 5.66e-3 [5.031e-3; 1.31e-2] | 8.244e-1 (8.696e-1) | 8.668e-1 [8.538e-1; 8.686e-1] | 5.364e0 | 19903–20000 |
| zdt4 | level_a156103ae6274204 | n_neighbors | 10 | initial | 1.595e-2 (4.779e-3) | 5.587e-3 [5.166e-3; 6.714e-3] | 8.504e-1 (8.695e-1) | 8.669e-1 [8.647e-1; 8.683e-1] | 5.351e0 | 19903–20000 |
| zdt4 | level_abd1724bac55d08a | n_neighbors | 20 | initial | 2.077e-2 (4.211e-3) | 5.283e-3 [4.89e-3; 7.052e-3] | 8.423e-1 (8.702e-1) | 8.678e-1 [8.643e-1; 8.687e-1] | 5.383e0 | 19901–19997 |
| zdt4 | held_mean_F_reference | mean_F | 0.65 | held | 5.294e-3 (**3.89e-3**) | 4.805e-3 [4.6e-3; 5.241e-3] | 8.682e-1 (8.704e-1) | 8.692e-1 [8.686e-1; 8.698e-1] | 5.337e0 | 19903–20000 |
| zdt4 | level_47f86f0c8500b69a | mean_F | 0.4 | held | 4.597e-3 (4.142e-3) | 4.576e-3 [4.459e-3; 4.76e-3] | 8.699e-1 (8.709e-1) | 8.7e-1 [8.694e-1; 8.703e-1] | 5.279e0 | 19901–19999 |
| zdt4 | level_86f962e53a0cfbc1 | mean_F | 0.5 | held | **4.497e-3** (3.995e-3) | **4.516e-3** [4.384e-3; 4.634e-3] | **8.702e-1** (**8.71e-1**) | **8.702e-1** [8.7e-1; 8.704e-1] | **5.088e0** | 19902–19999 |
| zdt4 | level_dda0a86b9a080c09 | mean_F | 0.8 | held | 5.228e-2 (4.828e-3) | 6.205e-3 [5.561e-3; 1.917e-2] | 7.969e-1 (8.69e-1) | 8.662e-1 [8.436e-1; 8.676e-1] | 5.223e0 | 19901–20000 |
| zdt4 | level_7a2d8b1f7c840cdc | mean_F | 0.9 | held | 4.178e-2 (4.663e-3) | 7.729e-3 [6.612e-3; 5.376e-2] | 8.095e-1 (8.687e-1) | 8.631e-1 [7.831e-1; 8.655e-1] | 5.273e0 | 19901–20000 |
| zdt4 | held_mean_CR_reference | mean_CR | 0.5 | held | 5.114e-2 (4.721e-3) | 5.839e-3 [5.053e-3; 1.742e-2] | 7.978e-1 (8.696e-1) | 8.666e-1 [8.465e-1; 8.68e-1] | 5.218e0 | 19901–19999 |
| zdt4 | level_7d49cd421ae53773 | mean_CR | 0.1 | held | 7.2e-2 (4.141e-3) | 2.178e-2 [5.936e-3; 1.27e-1] | 7.689e-1 (8.702e-1) | 8.397e-1 [6.837e-1; 8.664e-1] | 5.161e0 | 19901–20000 |
| zdt4 | level_29dcc1e221680b9e | mean_CR | 0.3 | held | 3.405e-2 (4.128e-3) | 5.258e-3 [4.857e-3; 6.56e-3] | 8.26e-1 (8.706e-1) | 8.676e-1 [8.65e-1; 8.688e-1] | 5.173e0 | 19902–19997 |
| zdt4 | level_6e0adc44ec0256bd | mean_CR | 0.7 | held | 5.663e-2 (4.948e-3) | 7.586e-3 [5.785e-3; 2.399e-2] | 7.941e-1 (8.686e-1) | 8.631e-1 [8.362e-1; 8.668e-1] | 5.287e0 | 19901–19996 |
| zdt4 | level_5f16e5985fbb30c2 | mean_CR | 0.9 | held | 2.342e-2 (4.791e-3) | 6.403e-3 [5.388e-3; 1.042e-2] | 8.384e-1 (8.688e-1) | 8.656e-1 [8.581e-1; 8.679e-1] | 5.256e0 | 19901–19999 |
| zdt4 | held_prob_de_reference | prob_de | 0.5 | held | 2.886e-2 (4.35e-3) | 5.461e-3 [5.015e-3; 7.11e-3] | 8.344e-1 (8.695e-1) | 8.676e-1 [8.647e-1; 8.687e-1] | 5.286e0 | 19902–20000 |
| zdt4 | level_18446fb110863082 | prob_de | 0.2 | held | 9.718e-2 (5.183e-3) | 2.627e-2 [1.045e-2; 1.306e-1] | 7.333e-1 (8.684e-1) | 8.316e-1 [6.669e-1; 8.582e-1] | 5.216e0 | 19902–20000 |
| zdt4 | level_99507c2b4a67b45a | prob_de | 0.35 | held | 3.946e-2 (4.749e-3) | 6.08e-3 [5.172e-3; 2.998e-2] | 8.137e-1 (8.688e-1) | 8.661e-1 [8.237e-1; 8.68e-1] | 5.268e0 | 19901–19999 |
| zdt4 | level_b26107a506bffc86 | prob_de | 0.65 | held | 1.915e-2 (4.096e-3) | 5.217e-3 [4.72e-3; 6.334e-3] | 8.458e-1 (8.703e-1) | 8.681e-1 [8.655e-1; 8.695e-1] | 5.399e0 | 19901–19998 |
| zdt4 | level_f5f38b20dc397b0a | prob_de | 0.8 | held | 1.131e-2 (4.191e-3) | 4.797e-3 [4.633e-3; 5.254e-3] | 8.584e-1 (8.703e-1) | 8.695e-1 [8.68e-1; 8.7e-1] | 5.411e0 | 19905–20000 |
| zdt6 | full | baseline | — | initial | 3.835e-3 (3.481e-3) | 3.824e-3 [3.693e-3; 3.896e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.781e0 | 19901–20000 |
| zdt6 | level_bc857e0271b391b7 | obl_interval | 5 | initial | 3.921e-3 (3.471e-3) | 3.986e-3 [3.784e-3; 4.068e-3] | 4.38e-1 (4.384e-1) | 4.38e-1 [4.378e-1; 4.382e-1] | 3.793e0 | 19901–20000 |
| zdt6 | level_b9e41374078f1def | obl_interval | 20 | initial | 3.81e-3 (3.403e-3) | 3.857e-3 [3.611e-3; 3.957e-3] | 4.381e-1 (4.387e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.735e0 | 19902–20000 |
| zdt6 | level_da967aa31e1c53de | obl_interval | 40 | initial | 3.849e-3 (3.292e-3) | 3.865e-3 [3.687e-3; 4.009e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.38e-1; 4.382e-1] | 3.829e0 | 19901–19999 |
| zdt6 | level_3c6496cae0000993 | obl_jump_rate | 0.05 | initial | 3.92e-3 (3.525e-3) | 3.894e-3 [3.759e-3; 4.041e-3] | 4.38e-1 (4.384e-1) | 4.381e-1 [4.378e-1; 4.382e-1] | 3.808e0 | 19901–20000 |
| zdt6 | level_71437a93f3d42084 | obl_jump_rate | 0.1 | initial | 3.862e-3 (3.533e-3) | 3.846e-3 [3.733e-3; 3.938e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.38e-1; 4.383e-1] | 3.803e0 | 19901–19999 |
| zdt6 | level_21521e2a1326e190 | obl_jump_rate | 0.4 | initial | 3.883e-3 (3.494e-3) | 3.834e-3 [3.716e-3; 3.964e-3] | 4.381e-1 (4.387e-1) | 4.381e-1 [4.379e-1; 4.382e-1] | 3.778e0 | 19901–20000 |
| zdt6 | level_fad6779d34994396 | stagnation_patience | 5 | initial | 3.831e-3 (3.534e-3) | 3.825e-3 [3.7e-3; 3.892e-3] | 4.381e-1 (4.387e-1) | 4.38e-1 [4.379e-1; 4.382e-1] | 3.761e0 | 19903–20000 |
| zdt6 | level_fd9743e30c6b7e4c | stagnation_patience | 10 | initial | 3.821e-3 (3.481e-3) | 3.83e-3 [3.686e-3; 3.896e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.806e0 | 19901–20000 |
| zdt6 | level_605e5e1df48d2f0b | stagnation_patience | 40 | initial | 3.819e-3 (3.361e-3) | 3.824e-3 [3.685e-3; 3.896e-3] | 4.381e-1 (4.386e-1) | 4.382e-1 [4.379e-1; 4.383e-1] | 3.774e0 | 19901–20000 |
| zdt6 | level_081a970edcd7d9c0 | stagnation_tolerance | 1e-05 | initial | 3.844e-3 (3.481e-3) | 3.824e-3 [3.694e-3; 3.914e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.769e0 | 19901–20000 |
| zdt6 | level_0f6357b99e389c0c | stagnation_tolerance | 0.001 | initial | 3.837e-3 (3.481e-3) | 3.839e-3 [3.689e-3; 3.914e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.786e0 | 19901–20000 |
| zdt6 | level_6660b9018786355d | diversity_threshold | 0.01 | initial | 3.819e-3 (3.361e-3) | 3.824e-3 [3.685e-3; 3.896e-3] | 4.381e-1 (4.386e-1) | 4.382e-1 [4.379e-1; 4.383e-1] | 3.807e0 | 19901–20000 |
| zdt6 | level_75acf398f87065c5 | diversity_threshold | 0.05 | initial | 3.887e-3 (3.501e-3) | 3.864e-3 [3.765e-3; 3.99e-3] | 4.381e-1 (4.389e-1) | 4.38e-1 [4.379e-1; 4.381e-1] | 3.787e0 | 19903–19997 |
| zdt6 | level_e711d25086fadbb2 | diversity_threshold | 0.1 | initial | 3.872e-3 (3.583e-3) | 3.853e-3 [3.713e-3; 3.962e-3] | 4.381e-1 (4.384e-1) | 4.381e-1 [4.38e-1; 4.382e-1] | 3.801e0 | 19904–19993 |
| zdt6 | level_68ad8d9eb2cc0549 | restart_elite_ratio | 0.9 | initial | 3.824e-3 (3.481e-3) | 3.824e-3 [3.68e-3; 3.896e-3] | 4.381e-1 (4.386e-1) | 4.382e-1 [4.379e-1; 4.383e-1] | 3.79e0 | 19901–20000 |
| zdt6 | level_2b9171e95155c918 | restart_elite_ratio | 0.95 | initial | 3.816e-3 (3.416e-3) | 3.839e-3 [3.687e-3; 3.914e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.379e-1; 4.383e-1] | 3.784e0 | 19901–20000 |
| zdt6 | level_7faf73034731b468 | n_neighbors | 3 | initial | 3.757e-3 (3.465e-3) | 3.779e-3 [3.699e-3; 3.847e-3] | 4.382e-1 (4.385e-1) | 4.382e-1 [4.38e-1; 4.384e-1] | 3.769e0 | 19901–20000 |
| zdt6 | level_a156103ae6274204 | n_neighbors | 10 | initial | 3.889e-3 (3.434e-3) | 3.887e-3 [3.817e-3; 4.016e-3] | 4.38e-1 (4.384e-1) | 4.379e-1 [4.378e-1; 4.382e-1] | 3.786e0 | 19903–20000 |
| zdt6 | level_abd1724bac55d08a | n_neighbors | 20 | initial | 3.919e-3 (3.519e-3) | 3.946e-3 [3.713e-3; 4.055e-3] | 4.38e-1 (4.384e-1) | 4.38e-1 [4.377e-1; 4.381e-1] | 3.856e0 | 19901–19999 |
| zdt6 | held_mean_F_reference | mean_F | 0.65 | held | 3.842e-3 (3.442e-3) | 3.829e-3 [3.718e-3; 3.98e-3] | 4.38e-1 (4.385e-1) | 4.381e-1 [4.379e-1; 4.382e-1] | 3.784e0 | 19901–20000 |
| zdt6 | level_47f86f0c8500b69a | mean_F | 0.4 | held | 4.021e-3 (3.532e-3) | 3.961e-3 [3.87e-3; 4.185e-3] | 4.376e-1 (4.382e-1) | 4.376e-1 [4.374e-1; 4.379e-1] | 3.806e0 | 19904–19991 |
| zdt6 | level_86f962e53a0cfbc1 | mean_F | 0.5 | held | 4.063e-3 (3.613e-3) | 4.028e-3 [3.943e-3; 4.164e-3] | 4.377e-1 (4.382e-1) | 4.377e-1 [4.375e-1; 4.378e-1] | 3.835e0 | 19903–19999 |
| zdt6 | level_dda0a86b9a080c09 | mean_F | 0.8 | held | 3.969e-3 (3.459e-3) | 3.903e-3 [3.834e-3; 4.073e-3] | 4.38e-1 (4.384e-1) | 4.381e-1 [4.378e-1; 4.382e-1] | 3.732e0 | 19901–19999 |
| zdt6 | level_7a2d8b1f7c840cdc | mean_F | 0.9 | held | 3.882e-3 (3.304e-3) | 3.874e-3 [3.768e-3; 3.981e-3] | 4.381e-1 (4.386e-1) | 4.381e-1 [4.38e-1; 4.383e-1] | 3.763e0 | 19904–20000 |
| zdt6 | held_mean_CR_reference | mean_CR | 0.5 | held | 3.765e-3 (3.44e-3) | 3.739e-3 [3.618e-3; 3.887e-3] | 4.382e-1 (4.387e-1) | 4.382e-1 [4.38e-1; 4.384e-1] | 3.768e0 | 19902–20000 |
| zdt6 | level_7d49cd421ae53773 | mean_CR | 0.1 | held | 3.772e-3 (3.362e-3) | 3.719e-3 [3.613e-3; 3.889e-3] | 4.381e-1 (4.387e-1) | 4.382e-1 [4.381e-1; 4.382e-1] | 3.789e0 | 19901–19998 |
| zdt6 | level_29dcc1e221680b9e | mean_CR | 0.3 | held | 3.66e-3 (3.28e-3) | 3.669e-3 [3.53e-3; 3.783e-3] | 4.385e-1 (4.391e-1) | 4.385e-1 [4.383e-1; 4.386e-1] | 3.716e0 | 19901–19997 |
| zdt6 | level_6e0adc44ec0256bd | mean_CR | 0.7 | held | 3.925e-3 (3.493e-3) | 3.994e-3 [3.732e-3; 4.081e-3] | 4.379e-1 (4.386e-1) | 4.378e-1 [4.377e-1; 4.381e-1] | 3.786e0 | 19902–19999 |
| zdt6 | level_5f16e5985fbb30c2 | mean_CR | 0.9 | held | 4.111e-3 (3.721e-3) | 4.124e-3 [3.956e-3; 4.238e-3] | 4.375e-1 (4.381e-1) | 4.375e-1 [4.373e-1; 4.378e-1] | 3.79e0 | 19903–19999 |
| zdt6 | held_prob_de_reference | prob_de | 0.5 | held | 3.801e-3 (3.31e-3) | 3.812e-3 [3.644e-3; 3.922e-3] | 4.382e-1 (4.387e-1) | 4.382e-1 [4.381e-1; 4.383e-1] | 3.832e0 | 19901–20000 |
| zdt6 | level_18446fb110863082 | prob_de | 0.2 | held | 3.985e-3 (3.63e-3) | 3.969e-3 [3.741e-3; 4.119e-3] | 4.377e-1 (4.382e-1) | 4.377e-1 [4.375e-1; 4.378e-1] | **3.607e0** | 19903–19995 |
| zdt6 | level_99507c2b4a67b45a | prob_de | 0.35 | held | 3.913e-3 (3.411e-3) | 3.962e-3 [3.75e-3; 4.058e-3] | 4.38e-1 (4.386e-1) | 4.38e-1 [4.377e-1; 4.382e-1] | 3.718e0 | 19901–20000 |
| zdt6 | level_b26107a506bffc86 | prob_de | 0.65 | held | 3.76e-3 (3.258e-3) | 3.759e-3 [3.629e-3; 3.852e-3] | 4.383e-1 (4.388e-1) | 4.383e-1 [4.382e-1; 4.385e-1] | 3.87e0 | 19903–19999 |
| zdt6 | level_f5f38b20dc397b0a | prob_de | 0.8 | held | **3.655e-3** (**3.034e-3**) | **3.663e-3** [3.529e-3; 3.811e-3] | **4.388e-1** (**4.395e-1**) | **4.388e-1** [4.385e-1; 4.389e-1] | 3.881e0 | 19901–19999 |
