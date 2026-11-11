# Rà soát nghiên cứu OADE-NSGA-II — 12/11/2026

## Kết luận và phạm vi

Dự án có cấu trúc triển khai nghiên cứu hợp lý và dữ liệu kết quả nhất quán với pipeline thống kê hiện tại, nhưng chưa thể xác nhận toàn bộ báo cáo và phương pháp là chính xác hoặc sẵn sàng nộp bài. Các vấn đề cần ưu tiên là định danh baseline, mô tả khởi tạo, ý nghĩa của probability adaptation và đóng gói tái lập.

Áp dụng nature-writing (nghiên cứu thuật toán; kiểm tra lập luận, phương pháp, thí nghiệm và thảo luận; chưa chọn tạp chí cụ thể), nature-statistics (audit thống kê) và nature-figure (kiểm tra giới hạn hồ sơ hình). Không áp đặt quy định riêng của Nature/NMI lên dự án.

Đã đọc README, bảy báo cáo trong docs, cấu hình benchmark/algorithm, runner, bộ đếm ngân sách, kiểm định, các phần thuật toán liên quan, danh sách file được Git theo dõi, hồ sơ QA và hình integrated_7algo_landscape.png. Đã đối chiếu bảy bộ CSV, tính lại kiểm định đã lưu bằng pipeline hiện tại và chạy unit test. Không chạy lại thuật toán, không thực hiện phân tích suy luận mới, không xác nhận tính mới từ một tổng quan tài liệu đầy đủ, không kiểm toán toàn bộ baseline theo từng phương trình bài gốc, không kiểm tra trực quan toàn bộ PDF ở kích thước in.

## Bằng chứng kiểm tra

| Bộ kết quả | Run records | Nhóm problem–algorithm | Không hợp lệ | Thắng / không phát hiện khác biệt / thua của reference |
|---|---:|---:|---:|---:|
| algorithm_benchmark | 1.050 | 35 | 0 | 39 / 20 / 1 |
| algorithm_benchmark_v2 | 1.050 | 35 | 0 | 58 / 1 / 1 |
| dtlz_benchmark | 2.520 | 84 | 18 | 91 / 40 / 13 |
| wfg_m2_7algo_benchmark | 840 | 28 | 0 | 42 / 0 / 6 |
| wfg_compact_benchmark | 1.800 | 60 | 0 | 56 / 11 / 29 |
| restart_confirmation | 450 | 15 | 0 | 0 / 4 / 16 |
| ablation | 1.050 | 35 | 0 | 4 / 45 / 11 |

Reference là OADE_NSGAII cho benchmark và Full OADE cho ablation/restart. Tổng 8.760 record trên bảy thư mục có bao gồm baseline được sao chép giữa các phiên bản; không phải 8.760 lần chạy độc lập mới.

- Mỗi nhóm có 30 record; không thấy trùng khóa (problem, algorithm, run_idx), không thấy n_eval vượt evaluation_budget.
- Tính lại Wilcoxon/Holm bằng src/benchmarking/statistics.py cho tất cả bảy bộ: không có sai lệch outcome hoặc adjusted p-value lớn hơn 1e-12 so với CSV. Đây là kiểm tra tính nhất quán với implementation, chưa phải xác minh độc lập mọi giả định thống kê.
- 900 baseline record của v2 giống hoàn toàn baseline tương ứng trong v1, bao gồm metadata từng record.
- DTLZ có 18 record collapsed_front: 15 SDR-OLS và 3 CGDE. Có 16 dòng kiểm định sử dụng 26–29 cặp thay vì 30. Báo cáo tích hợp đã công khai loại trừ và tính điều kiện trên valid output.
- `python -m unittest discover -s tests -v`: 13/13 test qua. Test chỉ bao phủ các tính chất được kiểm tra, không chứng minh toàn bộ thuật toán đúng.
- Runtime kiểm tra hiện tại: NumPy 2.5.4, SciPy 1.18.1, pymoo 0.6.2; không suy ngược đây là phiên bản dùng để tạo các kết quả cũ.

## Phát hiện theo mức ưu tiên

### P1 — Định danh baseline không khớp mã và tài liệu nguồn

Bằng chứng: README.md phần baseline và docs/benchmark_v2_results_report.md bảng thiết kế ghi CE-MOEA là Cross-Entropy, DNSGA2 là Direction-based, CGDE là Competitive & Guided và SDR-OLS là Orthogonal Local Search.

- config/algorithms/dnsga2.yaml gọi pymoo.algorithms.moo.dnsga2.DNSGA2. Đây là Dynamic NSGA-II, theo tài liệu pymoo, không phải Direction-based NSGA-II.
- algorithms/ce_moea/README.md và algorithm.py mô tả Continuous Encoding MOEA cho community detection. Bài nguồn cũng định nghĩa CE-MOEA là continuous encoding. Runner benchmark dùng CEMOEA trực tiếp trên bài toán liên tục; cần gọi rõ đây là bản điều chỉnh phần tìm kiếm cho ZDT/DTLZ/WFG, không ngụ ý đang đánh giá đầy đủ phương pháp graph encoding gốc hoặc Cross-Entropy MOEA.
- algorithms/cgde_nsga2/README.md định nghĩa Cross-Generation DE. Tên Competitive & Guided trong báo cáo không có căn cứ từ mô tả implementation này; cần chốt bài nguồn trước khi gắn tên phương pháp công bố.
- algorithms/nsga2_sdr_ols/README.md và operators.py mô tả opposition-based learning và local search với omega+/omega-, nhiễu Gaussian. Mô tả Orthogonal Local Search trong README tổng không được implementation này hỗ trợ.

Ảnh hưởng: kết quả vẫn mô tả các implementation đã chạy, nhưng chưa hỗ trợ kết luận thắng đúng các phương pháp được gọi tên trong báo cáo. Nếu tác giả thực sự định so với Cross-Entropy hoặc Direction-based, đổi nhãn không giải quyết được; phải chọn implementation đúng và thí nghiệm lại phần đó.

Sửa: lập bảng baseline gồm tên chuẩn, citation, nguồn code/version, phương trình, sai khác so với bản gốc và cấu hình. Sửa nhất quán văn bản, hình và caption sau khi xác định đối tượng thực sự.

Nguồn chính: [pymoo algorithm catalogue](https://pymoo.org/), [Sun et al., arXiv:2006.03996](https://arxiv.org/abs/2006.03996).

### P1 — Benchmark bỏ qua khởi tạo Sobol/OBL nhưng báo cáo còn đưa nó vào diễn giải

Bằng chứng: src/benchmarking/pymoo_compare.py::make_initial_population sinh rng.uniform; algorithm_benchmark.py::run_single_seed truyền initial_x cho OADE; algorithm.py::_build_initial_population trả về initialize_from_data khi initial_x tồn tại. Nhánh initialize_obl chỉ chạy khi không có initial_x.

Vì vậy benchmark fixed-budget đang đánh giá OADE với common uniform warm start, không phải khởi tạo Sobol + initial OBL. Periodic OBL vẫn có thể hoạt động, kể cả ở gen=0; nó khác initial Sobol/OBL selection.

Sửa: tách mô tả khả năng standalone khỏi cấu hình thực nghiệm. Trong kết luận ablation, giới hạn hiệu ứng vào OBL được bật trên đường chạy benchmark. Không dùng các benchmark này làm bằng chứng tác dụng Sobol. Nếu muốn kiểm tra khởi tạo, cần một thí nghiệm riêng với cách tính ngân sách và chính sách common-start được quy định rõ.

### P1 — Probability adaptation không cập nhật theo tỷ lệ thành công như docstring mô tả

Bằng chứng: algorithm.py::_update_adaptive_parameters tính de_ratio = len(de_offspring) / total, không sử dụng successful_de để tính prob_de. Do đó cập nhật này theo tỷ phần con được sinh bằng DE; nó không tự điều chỉnh dựa trên lợi thế thành công tương đối DE/SBX.

mean_F dùng Lehmer mean, mean_CR dùng trung bình cộng. README nói cả F và CR dùng Lehmer-mean updates là không đúng.

Sửa: ghi đúng công thức hiện có. Nếu chủ đích là success-based operator adaptation, thiết kế lại định nghĩa thành công, denominator và xử lý trường hợp không có success; gắn phiên bản thuật toán mới và kiểm tra lại. Không sửa công thức rồi tiếp tục gán kết quả cũ cho mã mới.

### P1 — Tái lập từ Git chưa đầy đủ

Bằng chứng: .gitignore loại tests/, analysis/, renv.lock, script render hình và manifest QA. git ls-files không có tests hoặc analysis, trong khi figure_qa.md nêu backend R và project-local renv. requirements.txt chỉ đặt khoảng phiên bản, chưa có snapshot môi trường thí nghiệm hoặc commit/config hash đi kèm từng bộ CSV.

Ảnh hưởng: clone mới không có 13 test vừa chạy, mã sinh các hình chính và lockfile R. Người khác có thể dùng built-in plotter nhưng chưa tái tạo được đầy đủ bộ hình báo cáo từ Git.

Sửa: theo dõi test, mã phân tích/hình, lockfile và một manifest kết quả gồm commit, config snapshot/hash, package versions, seed policy, PF/ref-point, máy và thread settings. Chỉ bỏ cache và artifact nặng có thể tái tạo. README có badge MIT nhưng không thấy LICENSE được theo dõi; cần làm rõ giấy phép dự án và nguồn baseline trước khi phát hành.

### P1 — Runner v2/resume thiếu xác minh provenance khi tái sử dụng kết quả

Bằng chứng: scripts/run_benchmark_v2.py đọc baseline cũ và ghép vào run mới. read_rows trả [] khi không có file; runner không kiểm tra đủ 900 baseline, seed/config hash hay validation completeness trước khi chạy. Dòng thông báo cuối luôn ghi “0 invalid” thay vì đếm. Resume trong algorithm_benchmark.py chủ yếu xác minh schema và số record từng problem; chưa chứng minh cấu hình hiện tại giống cấu hình của các record đã lưu.

Hiện trạng: dữ liệu v2 hiện có đủ và 900 baseline trùng v1; đây là rủi ro cho lần tái chạy, không phải bằng chứng bộ v2 hiện tại sai.

Sửa: preflight fail-fast về tập khóa mong đợi, seed, validation, budget và fingerprint cấu hình/mã. Tách thông báo số liệu thực tế khỏi giá trị hard-code. Cho phép recompute báo cáo mà không ghi đè dữ liệu gốc.

### P1 — Adaptive restart và tính mới chưa được chứng minh ở mức cơ chế

Báo cáo restart đã nêu đúng: Adaptive và No Restart trùng final IGD/HV ở 148/150 cặp problem–seed và không lưu trigger counts. Unit test xác nhận hai tình huống trigger tổng hợp, không chứng minh trigger đã tạo lợi ích trong các benchmark.

Sửa: giữ claim ở mức cấu hình v2 cho kết quả tốt trên các trường hợp được thử. Nếu đóng góp chính là adaptive restart, cần log số lần kiểm tra, kích hoạt, evaluations dùng cho restart và trạng thái đa dạng, rồi thiết kế thí nghiệm phân biệt với No Restart. Các cơ chế giải thích crowding saturation hoặc nguyên nhân WFG stagnation cần giữ là giả thuyết. docs/benchmark_v2_results_report.md phần mở rộng vẫn có câu “crowding-distance saturation still limits…” mạnh hơn bằng chứng cô lập hiện có.

Chưa đủ căn cứ xác nhận novelty hoặc mức cạnh tranh với state of the art: cần literature matrix, baseline đúng nguồn và câu hỏi nghiên cứu rõ, không chỉ số lượng win.

### P1 — Hoàn thiện suy luận thống kê và định nghĩa thất bại

Điểm đúng: paired run là đơn vị phân tích; Wilcoxon hai phía, Holm theo metric/suite; effect direction rõ; non-significance không bị đồng nhất với equivalence; sensitivity công khai omnibus chưa hiệu chỉnh toàn cục.

Điểm cần hoàn thiện:

- README ghi n=30 paired runs mỗi endpoint nhưng một số DTLZ comparison thực tế n=26–29. Viết “30 scheduled; 26–30 valid matched pairs” cho tổng quan, giữ n cụ thể trong bảng.
- 18 collapsed_front bị loại đã được công khai; vẫn cần đánh giá độ nhạy nếu muốn kết luận chất lượng bao gồm cả tỷ lệ thất bại. Không tự gán penalty hoặc loại thêm run sau khi nhìn kết quả.
- Tách “invalid collapsed_front” (tất cả F trùng sau rounding, áp dụng khi len(F)>1) trong evaluation.py khỏi “corner collapse” chẩn đoán chất lượng được kể cho các NSGA2 run vẫn valid. Một front chỉ có một điểm hiện không bị validator đánh dấu collapsed. Cần định nghĩa và nguồn tính từng tỷ lệ, tránh dùng chung một nhãn cho hai tiêu chuẩn.
- Chưa có CI cho paired effects và mức cải thiện; SD/IQR phản ánh phân tán run, không thay thế khoảng bất định của effect.
- Ghi zero_method, alternative và method thực tế của SciPy, cách xử lý zero/ties, n nonzero khi HV nhiều số 0; version hiện tại không thay thế version lịch sử. Wilcoxon signed-rank không tự bảo đảm các giả định phân phối sai khác; cần giải thích tính phù hợp và robustness khi phân phối lệch.
- Seed 42–71 xuất hiện ở nhiều suite và giai đoạn phát triển. Không gộp endpoint hoặc baseline tái sử dụng thành các replication độc lập; giữ tổng win là mô tả. Held-out restart chỉ xác nhận trên bộ ZDT mới, không phải xác nhận độc lập toàn bộ v2 trên mọi suite.

### P2 — Cấu trúc phần mềm hợp lý, cấu trúc hồ sơ nghiên cứu còn phân tán

src/oade_nsga2, benchmarking, plotting, sensitivity, config, results và docs đã phân tách phù hợp cho nghiên cứu thuật toán. Không có lý do phải chuyển sang hạ tầng production.

Tuy nhiên, docs hiện chủ yếu là báo cáo từng batch, chưa thành một bản thảo thống nhất có question/gap, related work, formulation/pseudocode, protocol, Results, Discussion và limitations. research_results_report.md là báo cáo lịch sử v1 dù tên tổng quát; đã có status warning nhưng cần một index chỉ rõ tài liệu chính, lịch sử và nguồn dữ liệu.

Đề nghị bổ sung docs/index.md, một manuscript chính, references.bib, experiment registry và reproducibility guide. Liên kết tới các báo cáo chi tiết như phụ lục, tránh chép lại mọi bảng vào main text.

### P2 — Hồ sơ QA hình cần cập nhật theo phạm vi thực tế

figure_qa.md ghi toàn bộ deliverable chỉ có một plot area, trong khi integrated_7algo_landscape có các panel a–c; cần làm rõ record nào áp dụng cho các hình cũ và thêm record cho hình mới.

Quan sát PNG integrated: có mã panel, chú giải effect direction và label, nhưng trục runtime chỉ dùng DTLZ4 trong khi rank gộp 34 endpoint. Trục đã ghi DTLZ4 và caption đã giới hạn ý nghĩa, song tiêu đề “Accuracy-speed trade-off” vẫn dễ bị hiểu thành trade-off chung toàn suite. Nên dùng runtime tổng hợp tương ứng cùng tập hoặc nhấn rõ đây là DTLZ4 runtime proxy. Không suy ra lợi thế runtime tổng quát từ hình này.

Lần audit này chưa chạy lại collision/alignment audit và chưa xem mọi PDF ở kích thước vật lý. Không tái xác nhận các dòng PASS cũ hoặc kết luận bộ hình đạt chuẩn nộp bài.

## Đoạn mô tả phương pháp có thể dùng sau khi đồng bộ baseline

> Các benchmark fixed-budget đánh giá cấu hình OADE-NSGA-II với quần thể khởi tạo uniform dùng chung theo seed, periodic opposition injection, các toán tử DE/SBX và các cập nhật tham số được định nghĩa trong mã. Nhánh khởi tạo standalone Sobol/OBL không được sử dụng trong giao thức này. Mỗi cấu hình được lên lịch 30 run; kiểm định ghép cặp sử dụng các run hợp lệ có cùng chỉ số, với 26–30 cặp trong bộ DTLZ. Wilcoxon signed-rank hai phía và hiệu chỉnh Holm được áp dụng riêng theo suite và metric. Tổng số kết quả thắng/thua qua nhiều suite là mô tả. Kết quả hiện tại so sánh các cấu hình hoàn chỉnh; chưa xác nhận đóng góp cơ chế riêng của adaptive restart.

## Thứ tự xử lý

1. Sửa định danh baseline và mô tả phương pháp theo đường chạy thực tế; chốt contribution cùng phạm vi claim.
2. Đưa test, mã figure và environment snapshot vào hồ sơ tái lập; bảo vệ reuse/resume bằng manifest.
3. Đồng bộ n, định nghĩa failure, QA hình và tổ chức một báo cáo/manuscript chính.
4. Chỉ sau đó quyết định thí nghiệm bổ sung nào cần cho claim: baseline đúng nguồn, restart telemetry/No Restart, uncertainty và robustness. Không cần chạy lại mọi benchmark chỉ để sửa lỗi tên hoặc văn bản.

AUTHOR_INPUT_NEEDED trước khi chốt bản thảo: baseline bài gốc dự định so sánh; contribution chính muốn bảo vệ; snapshot môi trường/commit dùng tạo kết quả nếu còn lưu; tiêu chí corner collapse và tạp chí đích nếu có. Các điểm chưa có thông tin không được suy đoán thành sự thật.
