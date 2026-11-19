# So sánh mới 7 thuật toán trên ZDT

In đậm giá trị tốt nhất trong cùng bài và cột: IGD/runtime nhỏ nhất, HV lớn nhất; giữ đồng hạng. Nhấn mạnh số học không đồng nghĩa có ý nghĩa thống kê.

Ô chất lượng là median (best run), số dạng e với 4 chữ số có nghĩa. Best run tính riêng IGD min/HV max trên 30 lượt, CGDE ZDT4 có 29 lượt hợp lệ. Hai cực trị có thể thuộc hai seed khác nhau. Không hiển thị SD cạnh giá trị trong bảng; dữ liệu gốc vẫn giữ nguyên.

Toàn bộ 7 thuật toán được chạy mới; không ghép block lịch sử.
Tổng run: **1050**; invalid: **1**.

OADE dùng bản chính oade_nsga2, runner local_oade, một cấu hình uniform + adaptive restart + OBL định kỳ + success-rate. Không dùng research.oade_nsga2. Các bản sửa duplicate/stale rank và objective budget được giữ.
Mỗi run có cùng uniform input theo bài/seed, cùng cap tổng; RNSGA2 aspiration-point setup tính cả objective calls. Task được xáo thứ tự theo seed cố định; runtime vẫn chịu ảnh hưởng máy/worker. X/F cuối, hash initial/reference và convergence lưu trong primary JSON.
Nguồn và giới hạn tái dựng: [baseline registry](../../../../docs/protocols/baselines.md), [sửa theo bài báo](../../../../docs/protocols/baseline_paper_corrections.md). CGDE dùng NCG/PCG và F theo cá thể; CR range/bootstrap/subrank ties là quy ước công khai. SDR-OLS bỏ cap 2N, dùng cả pool LS, nhưng Algorithm 4 gốc chưa nhất quán. CE-MOEA trên ZDT là adaptation lõi tìm kiếm, PM dùng số mũ in trong bản v2. Không chứng nhận tái lập đầy đủ ba thuật toán.
Wilcoxon signed-rank hai phía, zero_method=wilcox, SciPy method=auto; all-zero p=1. OADE so với 6 đối chứng: Holm riêng từng metric trên 30 cặp bài/đối chứng để so với cách báo cáo cũ; cột p_holm_all_endpoints bổ sung họ chung 60 endpoint. Alpha=0,05. Các cặp invalid bị loại và đếm; không phát hiện khác biệt không chứng minh tương đương.

| Bài | Thuật toán | Valid/run | IGD ↓ median (best) | HV ↑ median (best) | Runtime median (s) |
|:---|:---|---:|---:|---:|---:|
| ZDT1 | OADE_NSGAII | 30/30 | **4.52e-3** (**3.952e-3**) | **8.708e-1** (**8.713e-1**) | 7.398 |
| ZDT1 | NSGA2 | 30/30 | 5.171e-3 (4.417e-3) | 8.681e-1 (8.686e-1) | 3.484 |
| ZDT1 | RNSGA2 | 30/30 | 6.182e-1 (4.845e-1) | 3.671e-1 (4.932e-1) | 3.610 |
| ZDT1 | DNSGA2 | 30/30 | 5.626e-3 (4.97e-3) | 8.671e-1 (8.683e-1) | **3.257** |
| ZDT1 | CGDE_NSGAII | 30/30 | 5.123e-3 (4.584e-3) | 8.7e-1 (8.706e-1) | 118.025 |
| ZDT1 | NSGAII_SDR_OLS | 30/30 | 1.843e0 (1.493e0) | 0 (0) | 38.268 |
| ZDT1 | CE_MOEA | 30/30 | 6.7e-3 (5.543e-3) | 8.649e-1 (8.67e-1) | 178.953 |
| ZDT2 | OADE_NSGAII | 30/30 | **4.711e-3** (**4.149e-3**) | **5.377e-1** (**5.38e-1**) | 7.897 |
| ZDT2 | NSGA2 | 30/30 | 5.332e-3 (4.938e-3) | 5.342e-1 (5.349e-1) | **2.778** |
| ZDT2 | RNSGA2 | 30/30 | 5.257e-1 (4.467e-1) | 1.196e-1 (1.46e-1) | 3.858 |
| ZDT2 | DNSGA2 | 30/30 | 5.857e-3 (5.189e-3) | 5.327e-1 (5.345e-1) | 3.399 |
| ZDT2 | CGDE_NSGAII | 30/30 | 5.515e-3 (4.774e-3) | 5.365e-1 (5.373e-1) | 156.693 |
| ZDT2 | NSGAII_SDR_OLS | 30/30 | 3.134e0 (2.344e0) | 0 (0) | 41.547 |
| ZDT2 | CE_MOEA | 30/30 | 7.732e-3 (5.356e-3) | 5.292e-1 (5.338e-1) | 180.302 |
| ZDT3 | OADE_NSGAII | 30/30 | **4.91e-3** (**4.453e-3**) | **1.051e0** (**1.052e0**) | 7.426 |
| ZDT3 | NSGA2 | 30/30 | 5.319e-3 (4.695e-3) | 1.048e0 (1.049e0) | 3.804 |
| ZDT3 | RNSGA2 | 30/30 | 7.544e-1 (5.024e-1) | 3.9e-1 (6.188e-1) | 5.867 |
| ZDT3 | DNSGA2 | 30/30 | 5.509e-3 (5.049e-3) | 1.047e0 (1.048e0) | **2.980** |
| ZDT3 | CGDE_NSGAII | 30/30 | 6.162e-3 (5.246e-3) | 1.051e0 (1.051e0) | 178.629 |
| ZDT3 | NSGAII_SDR_OLS | 30/30 | 1.563e0 (1.128e0) | 0 (1.219e-2) | 40.696 |
| ZDT3 | CE_MOEA | 30/30 | 8.131e-3 (6.121e-3) | 1.036e0 (1.045e0) | 117.514 |
| ZDT4 | OADE_NSGAII | 30/30 | **6.259e-3** (4.636e-3) | **8.656e-1** (**8.693e-1**) | 9.062 |
| ZDT4 | NSGA2 | 30/30 | 8.09e-3 (4.767e-3) | 8.618e-1 (8.686e-1) | **3.273** |
| ZDT4 | RNSGA2 | 30/30 | 6.601e-1 (2.416e-1) | 3.241e-1 (6.767e-1) | 5.031 |
| ZDT4 | DNSGA2 | 30/30 | 1.214e-2 (**4.574e-3**) | 8.56e-1 (8.688e-1) | 3.765 |
| ZDT4 | CGDE_NSGAII | 29/30 | 1.922e0 (4.666e-1) | 0 (2.453e-1) | 118.540 |
| ZDT4 | NSGAII_SDR_OLS | 30/30 | 2.312e1 (1.233e1) | 0 (0) | 15.735 |
| ZDT4 | CE_MOEA | 30/30 | 2.721e-1 (1.337e-2) | 4.756e-1 (8.518e-1) | 206.108 |
| ZDT6 | OADE_NSGAII | 30/30 | **3.862e-3** (**3.461e-3**) | **4.38e-1** (**4.385e-1**) | 7.923 |
| ZDT6 | NSGA2 | 30/30 | 1.604e-2 (1.299e-2) | 4.182e-1 (4.226e-1) | 3.054 |
| ZDT6 | RNSGA2 | 30/30 | 2.123e-1 (2.775e-2) | 2.441e-1 (3.977e-1) | 5.488 |
| ZDT6 | DNSGA2 | 30/30 | 2.244e-2 (1.699e-2) | 4.095e-1 (4.17e-1) | **2.542** |
| ZDT6 | CGDE_NSGAII | 30/30 | 4.774e-3 (4.24e-3) | 4.379e-1 (4.385e-1) | 114.378 |
| ZDT6 | NSGAII_SDR_OLS | 30/30 | 5.258e0 (4.394e0) | 0 (0) | 15.004 |
| ZDT6 | CE_MOEA | 30/30 | 4.929e-3 (4.268e-3) | 4.378e-1 (4.385e-1) | 138.853 |

Đây là so sánh các bản triển khai cụ thể trong repository, không chứng minh ưu thế so với mọi thuật toán cùng tên trong tài liệu. CGDE/SDR-OLS/CE-MOEA có các điều chỉnh cục bộ; xem registry baselines. Batch nguyên tử có thể để dư budget; xem n_eval thực. Convergence không nội suy.
