# So sánh mới 7 thuật toán trên ZDT

In đậm giá trị tốt nhất trong cùng bài và cột: IGD/runtime nhỏ nhất, HV lớn nhất; giữ đồng hạng. Nhấn mạnh số học không đồng nghĩa có ý nghĩa thống kê.

Toàn bộ 7 thuật toán được chạy mới; không ghép block lịch sử.
Tổng run: **1050**; invalid: **1**.

OADE dùng bản chính oade_nsga2, runner local_oade, một cấu hình uniform + adaptive restart + OBL định kỳ + success-rate. Không dùng research.oade_nsga2. Các bản sửa duplicate/stale rank và objective budget được giữ.
Mỗi run có cùng uniform input theo bài/seed, cùng cap tổng; RNSGA2 aspiration-point setup tính cả objective calls. Task được xáo thứ tự theo seed cố định; runtime vẫn chịu ảnh hưởng máy/worker. X/F cuối, hash initial/reference và convergence lưu trong primary JSON.
Nguồn và giới hạn tái dựng: [baseline registry](../../../../docs/protocols/baselines.md), [sửa theo bài báo](../../../../docs/protocols/baseline_paper_corrections.md). CGDE dùng NCG/PCG và F theo cá thể; CR range/bootstrap/subrank ties là quy ước công khai. SDR-OLS bỏ cap 2N, dùng cả pool LS, nhưng Algorithm 4 gốc chưa nhất quán. CE-MOEA trên ZDT là adaptation lõi tìm kiếm, PM dùng số mũ in trong bản v2. Không chứng nhận tái lập đầy đủ ba thuật toán.
Wilcoxon signed-rank hai phía, zero_method=wilcox, SciPy method=auto; all-zero p=1. OADE so với 6 đối chứng: Holm riêng từng metric trên 30 cặp bài/đối chứng để so với cách báo cáo cũ; cột p_holm_all_endpoints bổ sung họ chung 60 endpoint. Alpha=0,05. Các cặp invalid bị loại và đếm; không phát hiện khác biệt không chứng minh tương đương.

| Bài | Thuật toán | Valid/run | IGD median ↓ | HV median ↑ | Runtime median (s) |
|:---|:---|---:|---:|---:|---:|
| ZDT1 | OADE_NSGAII | 30/30 | **0.0045200** | **0.8708196** | 7.398 |
| ZDT1 | NSGA2 | 30/30 | 0.0051711 | 0.8681347 | 3.484 |
| ZDT1 | RNSGA2 | 30/30 | 0.6182285 | 0.3670533 | 3.610 |
| ZDT1 | DNSGA2 | 30/30 | 0.0056257 | 0.8670929 | **3.257** |
| ZDT1 | CGDE_NSGAII | 30/30 | 0.0051226 | 0.8700059 | 118.025 |
| ZDT1 | NSGAII_SDR_OLS | 30/30 | 1.8425605 | 0.0000000 | 38.268 |
| ZDT1 | CE_MOEA | 30/30 | 0.0066998 | 0.8648527 | 178.953 |
| ZDT2 | OADE_NSGAII | 30/30 | **0.0047112** | **0.5377178** | 7.897 |
| ZDT2 | NSGA2 | 30/30 | 0.0053317 | 0.5342459 | **2.778** |
| ZDT2 | RNSGA2 | 30/30 | 0.5257034 | 0.1195632 | 3.858 |
| ZDT2 | DNSGA2 | 30/30 | 0.0058570 | 0.5326901 | 3.399 |
| ZDT2 | CGDE_NSGAII | 30/30 | 0.0055153 | 0.5364662 | 156.693 |
| ZDT2 | NSGAII_SDR_OLS | 30/30 | 3.1340548 | 0.0000000 | 41.547 |
| ZDT2 | CE_MOEA | 30/30 | 0.0077322 | 0.5292446 | 180.302 |
| ZDT3 | OADE_NSGAII | 30/30 | **0.0049100** | **1.0512594** | 7.426 |
| ZDT3 | NSGA2 | 30/30 | 0.0053192 | 1.0483671 | 3.804 |
| ZDT3 | RNSGA2 | 30/30 | 0.7543563 | 0.3900166 | 5.867 |
| ZDT3 | DNSGA2 | 30/30 | 0.0055091 | 1.0470732 | **2.980** |
| ZDT3 | CGDE_NSGAII | 30/30 | 0.0061623 | 1.0506602 | 178.629 |
| ZDT3 | NSGAII_SDR_OLS | 30/30 | 1.5626822 | 0.0000000 | 40.696 |
| ZDT3 | CE_MOEA | 30/30 | 0.0081307 | 1.0362999 | 117.514 |
| ZDT4 | OADE_NSGAII | 30/30 | **0.0062593** | **0.8656197** | 9.062 |
| ZDT4 | NSGA2 | 30/30 | 0.0080904 | 0.8618234 | **3.273** |
| ZDT4 | RNSGA2 | 30/30 | 0.6600946 | 0.3241071 | 5.031 |
| ZDT4 | DNSGA2 | 30/30 | 0.0121375 | 0.8559660 | 3.765 |
| ZDT4 | CGDE_NSGAII | 29/30 | 1.9218188 | 0.0000000 | 118.540 |
| ZDT4 | NSGAII_SDR_OLS | 30/30 | 23.1223901 | 0.0000000 | 15.735 |
| ZDT4 | CE_MOEA | 30/30 | 0.2721372 | 0.4756044 | 206.108 |
| ZDT6 | OADE_NSGAII | 30/30 | **0.0038624** | **0.4380475** | 7.923 |
| ZDT6 | NSGA2 | 30/30 | 0.0160421 | 0.4182419 | 3.054 |
| ZDT6 | RNSGA2 | 30/30 | 0.2123083 | 0.2440791 | 5.488 |
| ZDT6 | DNSGA2 | 30/30 | 0.0224441 | 0.4095034 | **2.542** |
| ZDT6 | CGDE_NSGAII | 30/30 | 0.0047742 | 0.4379353 | 114.378 |
| ZDT6 | NSGAII_SDR_OLS | 30/30 | 5.2579797 | 0.0000000 | 15.004 |
| ZDT6 | CE_MOEA | 30/30 | 0.0049292 | 0.4378224 | 138.853 |

Đây là so sánh các bản triển khai cụ thể trong repository, không chứng minh ưu thế so với mọi thuật toán cùng tên trong tài liệu. CGDE/SDR-OLS/CE-MOEA có các điều chỉnh cục bộ; xem registry baselines. Batch nguyên tử có thể để dư budget; xem n_eval thực. Convergence không nội suy.
