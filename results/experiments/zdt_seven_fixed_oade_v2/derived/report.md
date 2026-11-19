# So sánh mới 7 thuật toán trên ZDT

In đậm giá trị tốt nhất trong cùng bài và cột: IGD nhỏ nhất, HV lớn nhất; giữ đồng hạng. Nhấn mạnh số học không đồng nghĩa có ý nghĩa thống kê.

Ô chất lượng là mean (best run), số dạng e với 4 chữ số có nghĩa. Best run tính riêng IGD min/HV max trên 30 lượt, CGDE ZDT4 có 29 lượt hợp lệ. Hai cực trị có thể thuộc hai seed khác nhau. Không hiển thị SD cạnh giá trị trong bảng; dữ liệu gốc vẫn giữ nguyên.

Toàn bộ 7 thuật toán được chạy mới; không ghép block lịch sử.
Tổng run: **1050**; invalid: **1**.

OADE dùng bản chính oade_nsga2, runner local_oade, một cấu hình uniform + adaptive restart + OBL định kỳ + success-rate. Không dùng research.oade_nsga2. Các bản sửa duplicate/stale rank và objective budget được giữ.
Mỗi run có cùng uniform input theo bài/seed, cùng cap tổng; RNSGA2 aspiration-point setup tính cả objective calls. Task được xáo thứ tự theo seed cố định; runtime vẫn chịu ảnh hưởng máy/worker. X/F cuối, hash initial/reference và convergence lưu trong primary JSON.
Nguồn và giới hạn tái dựng: [baseline registry](../../../../docs/protocols/baselines.md), [sửa theo bài báo](../../../../docs/protocols/baseline_paper_corrections.md). CGDE dùng NCG/PCG và F theo cá thể; CR range/bootstrap/subrank ties là quy ước công khai. SDR-OLS bỏ cap 2N, dùng cả pool LS, nhưng Algorithm 4 gốc chưa nhất quán. CE-MOEA trên ZDT là adaptation lõi tìm kiếm, PM dùng số mũ in trong bản v2. Không chứng nhận tái lập đầy đủ ba thuật toán.
Wilcoxon signed-rank hai phía, zero_method=wilcox, SciPy method=auto; all-zero p=1. OADE so với 6 đối chứng: Holm riêng từng metric trên 30 cặp bài/đối chứng để so với cách báo cáo cũ; cột p_holm_all_endpoints bổ sung họ chung 60 endpoint. Alpha=0,05. Các cặp invalid bị loại và đếm; không phát hiện khác biệt không chứng minh tương đương.

### Bảng 1. Giá trị IGD

| Bài toán | NSGA-II | R-NSGA-II | D-NSGA-II | CGDE | SDR-OLS | CE-MOEA | OADE-NSGA-II |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZDT1 | 5.175e-3 (4.417e-3) | 6.33e-1 (4.845e-1) | 5.633e-3 (4.97e-3) | 5.202e-3 (4.584e-3) | 1.845e0 (1.493e0) | 6.8e-3 (5.543e-3) | **4.47e-3** (**3.952e-3**) |
| ZDT2 | 5.405e-3 (4.938e-3) | 5.235e-1 (4.467e-1) | 5.881e-3 (5.189e-3) | 5.539e-3 (4.774e-3) | 3.042e0 (2.344e0) | 7.8e-3 (5.356e-3) | **4.71e-3** (**4.149e-3**) |
| ZDT3 | 7.191e-3 (4.695e-3) | 7.406e-1 (5.024e-1) | 5.568e-3 (5.049e-3) | 6.126e-3 (5.246e-3) | 1.575e0 (1.128e0) | 8.813e-3 (6.121e-3) | **4.998e-3** (**4.453e-3**) |
| ZDT4 | **9.953e-3** (4.767e-3) | 6.206e-1 (2.416e-1) | 1.997e-2 (**4.574e-3**) | 2.32e0 (4.666e-1) | 2.384e1 (1.233e1) | 2.884e-1 (1.337e-2) | 3.979e-2 (4.636e-3) |
| ZDT6 | 1.637e-2 (1.299e-2) | 1.858e-1 (2.775e-2) | 2.259e-2 (1.699e-2) | 4.828e-3 (4.24e-3) | 5.257e0 (4.394e0) | 4.887e-3 (4.268e-3) | **3.881e-3** (**3.461e-3**) |

### Bảng 2. Giá trị HV

| Bài toán | NSGA-II | R-NSGA-II | D-NSGA-II | CGDE | SDR-OLS | CE-MOEA | OADE-NSGA-II |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZDT1 | 8.681e-1 (8.686e-1) | 3.481e-1 (4.932e-1) | 8.671e-1 (8.683e-1) | 8.699e-1 (8.706e-1) | 0 (0) | 8.646e-1 (8.67e-1) | **8.708e-1** (**8.713e-1**) |
| ZDT2 | 5.341e-1 (5.349e-1) | 1.209e-1 (1.46e-1) | 5.327e-1 (5.345e-1) | 5.365e-1 (5.373e-1) | 0 (0) | 5.293e-1 (5.338e-1) | **5.377e-1** (**5.38e-1**) |
| ZDT3 | 1.047e0 (1.049e0) | 4.01e-1 (6.188e-1) | 1.047e0 (1.048e0) | 1.051e0 (1.051e0) | 8.119e-4 (1.219e-2) | 1.034e0 (1.045e0) | **1.051e0** (**1.052e0**) |
| ZDT4 | **8.594e-1** (8.686e-1) | 3.511e-1 (6.767e-1) | 8.467e-1 (8.688e-1) | 1.647e-2 (2.453e-1) | 0 (0) | 4.653e-1 (8.518e-1) | 8.139e-1 (**8.693e-1**) |
| ZDT6 | 4.179e-1 (4.226e-1) | 2.676e-1 (3.977e-1) | 4.089e-1 (4.17e-1) | 4.379e-1 (4.385e-1) | 0 (0) | 4.378e-1 (4.385e-1) | **4.381e-1** (**4.385e-1**) |

Đây là so sánh các bản triển khai cụ thể trong repository, không chứng minh ưu thế so với mọi thuật toán cùng tên trong tài liệu. CGDE/SDR-OLS/CE-MOEA có các điều chỉnh cục bộ; xem registry baselines. Batch nguyên tử có thể để dư budget; xem n_eval thực. Convergence không nội suy.
