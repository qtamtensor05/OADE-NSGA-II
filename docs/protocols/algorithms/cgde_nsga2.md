# CGDE-NSGA-II

Nguồn: Qiu, X.; Xu, J.; Tan, K. C. (2014), [A Novel Differential Evolution (DE) Algorithm for Multi-objective Optimization](https://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2014/WCCI/CEC-2014/PROGRAM/E-14533.pdf), IEEE CEC, pp. 2391–2396.

Hai toán tử ở Eqs. 7–8 được chọn với xác suất bằng nhau:

$$v_{i,g}=x_{rn1,g}+F_{i,g}(x_{rn1,g}-x_{rn2,g-1}),$$
$$v_{i,g}=x_{i,g}+F_{i,g}(x_{rp1,g}-x_{rp2,g-1}).$$

Nhánh đầu lấy trong lân cận subrank; nhánh sau lấy từ toàn quần thể. Binomial crossover có tọa độ bắt buộc. Không có current-to-pbest hay polynomial mutation bổ sung.

Mỗi cá thể mang F; con kế thừa F của cha; sau chọn lọc F của cá thể sống được nhiễu và clip. Mặc định: 5 lân cận, F ban đầu U(0.2,0.9), nhiễu U(-0.2,0.2), CR ngẫu nhiên cho từng offspring. Thế hệ trước là đúng P(g-1).

CR dùng U(0,1), bootstrap, đồng hạng, biên và hệ tọa độ subrank là các quy ước chưa được bài xác định đầy đủ; xem [bản ghi sửa](../baseline_paper_corrections.md). Chưa xác nhận bằng mã tác giả.

```python
from cgde_nsga2 import CGDE_NSGAII, ProblemAdapter
from pymoo.problems import get_problem
solver = CGDE_NSGAII(ProblemAdapter(get_problem('zdt1', n_var=30)), seed=42)
X, F = solver.run()
```
