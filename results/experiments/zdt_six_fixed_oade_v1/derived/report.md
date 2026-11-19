# Đối chứng mới sáu thuật toán trên ZDT

Chạy mới toàn bộ sáu thuật toán, không ghép dữ liệu từ bộ bảy thuật toán cũ.
900 run hoàn tất; 899 hợp lệ. Holm chung 50 endpoint, alpha=0,05.
IGD thấp/HV cao tốt. Ô là mean (best run), không hiển thị SD/Valid/Runtime; số liệu đầy đủ giữ trong CSV. Best tính riêng trên các lượt hợp lệ; IGD min/HV max có thể thuộc seed khác nhau. In đậm mean và best riêng theo từng bài, xác định từ số chưa làm tròn.
GDE3/NSDE dùng pymoo, DE/rand/1/bin, F=0.5, CR=0.5, jitter gamma=1e-4, bounce-back repair, RankAndCrowding mặc định và cùng uniform input. OADE/CGDE không đổi. D-NSGA-II được đo trên bài tĩnh; không suy ra hiệu quả thích ứng môi trường động.
Wilcoxon hai phía theo cặp seed, zero_method=wilcox, method=auto; all-zero p=1. Invalid pairs được loại và đếm; no-valid-pair endpoint giữ p=1 trong họ. NS không chứng minh tương đương. Không so runtime giữa những môi trường/worker khác nhau.

## IGD — mean (best)

| Bài | NSGA2 | DNSGA2 | CGDE_NSGAII | GDE3 | NSDE | OADE_NSGAII |
|---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 5.175e-3 (4.417e-3) | 5.633e-3 (4.97e-3) | 5.202e-3 (4.584e-3) | 4.961e-3 (4.469e-3) | 4.872e-3 (4.373e-3) | **4.47e-3** (**3.952e-3**) |
| ZDT2 | 5.405e-3 (4.938e-3) | 5.881e-3 (5.189e-3) | 5.539e-3 (4.774e-3) | 8.597e-2 (4.764e-3) | 1.665e-1 (4.535e-3) | **4.71e-3** (**4.149e-3**) |
| ZDT3 | 7.191e-3 (4.695e-3) | 5.568e-3 (5.049e-3) | 6.126e-3 (5.246e-3) | 5.349e-3 (4.917e-3) | 5.186e-3 (4.565e-3) | **4.998e-3** (**4.453e-3**) |
| ZDT4 | **9.953e-3** (4.767e-3) | 1.997e-2 (**4.574e-3**) | 2.32e0 (4.666e-1) | 8.542e0 (5.599e0) | 6.938e0 (3.668e0) | 3.979e-2 (4.636e-3) |
| ZDT6 | 1.637e-2 (1.299e-2) | 2.259e-2 (1.699e-2) | 4.828e-3 (4.24e-3) | 1.154e-2 (8.408e-3) | 2.588e-2 (7.242e-3) | **3.881e-3** (**3.461e-3**) |

## HV — mean (best)

| Bài | NSGA2 | DNSGA2 | CGDE_NSGAII | GDE3 | NSDE | OADE_NSGAII |
|---|---:|---:|---:|---:|---:|---:|
| ZDT1 | 8.681e-1 (8.686e-1) | 8.671e-1 (8.683e-1) | 8.699e-1 (8.706e-1) | 8.686e-1 (8.693e-1) | 8.689e-1 (8.695e-1) | **8.708e-1** (**8.713e-1**) |
| ZDT2 | 5.341e-1 (5.349e-1) | 5.327e-1 (5.345e-1) | 5.365e-1 (5.373e-1) | 4.78e-1 (5.356e-1) | 4.218e-1 (5.359e-1) | **5.377e-1** (**5.38e-1**) |
| ZDT3 | 1.047e0 (1.049e0) | 1.047e0 (1.048e0) | 1.051e0 (1.051e0) | 1.048e0 (1.049e0) | 1.048e0 (1.049e0) | **1.051e0** (**1.052e0**) |
| ZDT4 | **8.594e-1** (8.686e-1) | 8.467e-1 (8.688e-1) | 1.647e-2 (2.453e-1) | 0 (0) | 0 (0) | 8.139e-1 (**8.693e-1**) |
| ZDT6 | 4.179e-1 (4.226e-1) | 4.089e-1 (4.17e-1) | 4.379e-1 (4.385e-1) | 4.249e-1 (4.297e-1) | 4.175e-1 (4.315e-1) | **4.381e-1** (**4.385e-1**) |
