#!/usr/bin/env Rscript

# Figure contract
# Benchmark: show where OADE-NSGA-II ranks under the common fixed budget.
# Ablation: show whether removing each component helps or harms Full OADE.
# Independent unit: one stochastic run; n = 30 paired runs per comparison.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(scales)
  library(tidyr)
})

output_dir <- "results/figures"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

algorithm_order <- c(
  "OADE_NSGAII", "NSGA2", "DNSGA2", "RNSGA2",
  "CGDE_NSGAII", "NSGAII_SDR_OLS", "CE_MOEA"
)
algorithm_labels <- c(
  OADE_NSGAII = "OADE",
  NSGA2 = "NSGA2",
  DNSGA2 = "DNSGA2",
  RNSGA2 = "RNSGA2",
  CGDE_NSGAII = "CGDE",
  NSGAII_SDR_OLS = "SDR-OLS",
  CE_MOEA = "CE-MOEA"
)

variant_order <- c(
  "OADE_NO_FCR_ADAPTATION",
  "OADE_NO_PROBABILITY_ADAPTATION",
  "OADE_NO_NEIGHBORHOOD",
  "OADE_NO_RESTART",
  "OADE_NO_OBL",
  "OADE_BASIC"
)
variant_labels <- c(
  OADE_NO_FCR_ADAPTATION = "F/CR",
  OADE_NO_PROBABILITY_ADAPTATION = "Prob.",
  OADE_NO_NEIGHBORHOOD = "Nbr.",
  OADE_NO_RESTART = "Restart",
  OADE_NO_OBL = "OBL",
  OADE_BASIC = "Basic"
)

problem_order <- c("zdt1", "zdt2", "zdt3", "zdt4", "zdt6")
row_order <- rev(as.vector(rbind(
  paste(toupper(problem_order), "IGD"),
  paste(toupper(problem_order), "HV")
)))

theme_report <- function(base_size = 8.5) {
  theme_minimal(base_size = base_size, base_family = "Helvetica") +
    theme(
      panel.grid = element_blank(),
      plot.title = element_text(size = 11, face = "bold", margin = margin(b = 5)),
      plot.subtitle = element_text(size = 8.5, colour = "#444444", margin = margin(b = 8)),
      plot.caption = element_text(size = 7, colour = "#555555", hjust = 0, margin = margin(t = 7)),
      axis.title = element_blank(),
      axis.text.x = element_text(size = 6.0, angle = 0, hjust = 0.5, vjust = 1),
      axis.text.y = element_text(size = 7.5, face = "bold"),
      legend.title = element_text(size = 7.5),
      legend.text = element_text(size = 7),
      legend.position = "bottom",
      plot.margin = margin(8, 10, 8, 8)
    )
}

save_figure <- function(plot, stem, width_mm = 180, height_mm = 125) {
  width_in <- width_mm / 25.4
  height_in <- height_mm / 25.4

  grDevices::pdf(
    paste0(stem, ".pdf"), width = width_in, height = height_in,
    family = "Helvetica", useDingbats = FALSE, compress = FALSE
  )
  print(plot)
  grDevices::dev.off()

  # Optional Cairo compatibility export. The default PDF device is retained
  # because it exposes individual text boxes to rendered collision QA.
  if (identical(Sys.getenv("OADE_CAIRO_PDF"), "1")) {
    grDevices::cairo_pdf(
      paste0(stem, ".cairo.pdf"), width = width_in, height = height_in,
      family = "Arial"
    )
    print(plot)
    grDevices::dev.off()
  }

  svglite::svglite(paste0(stem, ".svg"), width = width_in, height = height_in)
  print(plot)
  grDevices::dev.off()

  ragg::agg_png(
    paste0(stem, ".png"), width = width_in, height = height_in,
    units = "in", res = 300
  )
  print(plot)
  grDevices::dev.off()

  ragg::agg_tiff(
    paste0(stem, ".tiff"), width = width_in, height = height_in,
    units = "in", res = 600, compression = "lzw"
  )
  print(plot)
  grDevices::dev.off()
}

benchmark <- read.csv(
  "results/algorithm_benchmark/algorithm_benchmark_igd_hv_summary.csv",
  check.names = FALSE
)

benchmark_plot_data <- benchmark %>%
  select(problem, algorithm, IGD_mean, HV_mean) %>%
  pivot_longer(c(IGD_mean, HV_mean), names_to = "metric", values_to = "mean") %>%
  mutate(metric = if_else(metric == "IGD_mean", "IGD", "HV")) %>%
  group_by(problem, metric) %>%
  mutate(
    rank = if_else(metric == "IGD", min_rank(mean), min_rank(desc(mean))),
    score = 8 - rank
  ) %>%
  ungroup() %>%
  mutate(
    algorithm = factor(algorithm, levels = algorithm_order, labels = algorithm_labels[algorithm_order]),
    row = factor(paste(toupper(problem), metric), levels = row_order),
    proposed = algorithm == "OADE"
  )

write.csv(
  benchmark_plot_data,
  file.path(output_dir, "benchmark_rank_heatmap_source.csv"),
  row.names = FALSE
)

benchmark_plot <- ggplot(benchmark_plot_data, aes(algorithm, row)) +
  geom_tile(aes(fill = score), colour = "white", linewidth = 0.6) +
  geom_tile(
    data = filter(benchmark_plot_data, proposed),
    fill = NA, colour = "#D24B40", linewidth = 1.0
  ) +
  geom_text(aes(label = rank), size = 3.0, colour = "#1F1F1F") +
  scale_fill_gradient(
    low = "#F2F2F2", high = "#3182BD", limits = c(1, 7),
    breaks = c(1, 4, 7), labels = c("Worst", "Middle", "Best"),
    name = "Within-problem rank"
  ) +
  labs(
    title = "Fixed-budget benchmark: relative final-quality rank",
    subtitle = "Rank 1 is best; the red outline identifies OADE-NSGA-II",
    caption = paste0(
      "Mean IGD (lower is better) and HV (higher is better), n = 30 runs.\n",
      "Ranks summarize magnitude only; paired Holm-adjusted tests remain authoritative."
    )
  ) +
  guides(fill = guide_colorbar(
    title.position = "top", title.hjust = 0.5,
    barwidth = grid::unit(95, "mm"), barheight = grid::unit(4, "mm")
  )) +
  coord_fixed(ratio = 0.72, clip = "off") +
  theme_report()

save_figure(
  benchmark_plot,
  file.path(output_dir, "benchmark_rank_heatmap"),
  width_mm = 180,
  height_mm = 125
)

ablation <- read.csv(
  "results/ablation/algorithm_benchmark_paired_statistics.csv",
  check.names = FALSE
)

ablation_plot_data <- ablation %>%
  filter(comparison_algorithm %in% variant_order) %>%
  mutate(
    comparison_algorithm = factor(
      comparison_algorithm,
      levels = variant_order,
      labels = variant_labels[variant_order]
    ),
    row = factor(paste(toupper(problem), metric), levels = row_order),
    significant = as.logical(significant),
    label = sprintf("%+.2f%s", rank_biserial_effect, if_else(significant, "*", ""))
  )

write.csv(
  ablation_plot_data,
  file.path(output_dir, "ablation_effect_heatmap_source.csv"),
  row.names = FALSE
)

ablation_plot <- ggplot(ablation_plot_data, aes(comparison_algorithm, row)) +
  geom_tile(aes(fill = rank_biserial_effect), colour = "white", linewidth = 0.6) +
  geom_text(data = filter(ablation_plot_data, !significant), aes(label = label), size = 2.55) +
  geom_text(
    data = filter(ablation_plot_data, significant),
    aes(label = label), size = 2.55, fontface = "bold"
  ) +
  scale_fill_gradient2(
    low = "#3182BD", mid = "#F7F7F7", high = "#D95F0E",
    midpoint = 0, limits = c(-1, 1), breaks = c(-1, 0, 1),
    labels = c("Removal better", "No direction", "Full better"),
    name = "Rank-biserial effect"
  ) +
  labs(
    title = "Component ablation: paired effect relative to Full OADE",
    subtitle = "Blue favours removing the component; orange favours Full OADE",
    caption = paste0(
      "Values are matched-pairs rank-biserial effects; * indicates Holm-adjusted p < 0.05.\n",
      "Two-sided paired Wilcoxon tests, n = 30; correction family contains 30 comparisons per metric."
    )
  ) +
  guides(fill = guide_colorbar(
    title.position = "top", title.hjust = 0.5,
    barwidth = grid::unit(110, "mm"), barheight = grid::unit(4, "mm")
  )) +
  coord_fixed(ratio = 0.72, clip = "off") +
  theme_report()

save_figure(
  ablation_plot,
  file.path(output_dir, "ablation_effect_heatmap"),
  width_mm = 180,
  height_mm = 125
)

# Benchmark rank-count bar chart -------------------------------------------------

rank_count_data <- benchmark_plot_data %>%
  filter(rank <= 3) %>%
  count(algorithm, rank, name = "endpoint_count") %>%
  complete(algorithm, rank = 1:3, fill = list(endpoint_count = 0)) %>%
  mutate(rank = factor(rank, levels = c(3, 2, 1), labels = c("Rank 3", "Rank 2", "Rank 1")))

write.csv(
  rank_count_data,
  file.path(output_dir, "benchmark_top_rank_counts_source.csv"),
  row.names = FALSE
)

rank_count_plot <- ggplot(rank_count_data, aes(algorithm, endpoint_count, fill = rank)) +
  geom_col(width = 0.72, colour = "white", linewidth = 0.35) +
  geom_text(
    aes(label = if_else(endpoint_count > 0, as.character(endpoint_count), "")),
    position = position_stack(vjust = 0.5), size = 2.8
  ) +
  scale_fill_manual(
    values = c("Rank 3" = "#BDD7E7", "Rank 2" = "#6BAED6", "Rank 1" = "#2171B5"),
    name = NULL
  ) +
  scale_y_continuous(breaks = 0:10, expand = expansion(mult = c(0, 0.08))) +
  labs(
    title = "How often each algorithm reaches the top three",
    subtitle = "Counts across five problems and two final-quality metrics",
    x = NULL,
    y = "Number of problem-metric endpoints",
    caption = "Ranks use descriptive means across n = 30 runs; ten endpoints are counted in total."
  ) +
  theme_report() +
  theme(axis.title.y = element_text(size = 8), legend.position = "top")

save_figure(
  rank_count_plot,
  file.path(output_dir, "benchmark_top_rank_counts"),
  width_mm = 170,
  height_mm = 105
)

# Benchmark runtime bar chart ----------------------------------------------------

runtime_data <- read.csv(
  "results/algorithm_benchmark/algorithm_benchmark_cost_summary.csv",
  check.names = FALSE
) %>%
  group_by(algorithm) %>%
  summarise(
    runtime_mean_across_problems = mean(runtime_mean),
    runtime_min_problem = min(runtime_mean),
    runtime_max_problem = max(runtime_mean),
    .groups = "drop"
  ) %>%
  mutate(
    algorithm = factor(algorithm, levels = algorithm_order, labels = algorithm_labels[algorithm_order]),
    proposed = algorithm == "OADE"
  )

stopifnot(all(runtime_data$runtime_min_problem > 0))

write.csv(
  runtime_data,
  file.path(output_dir, "benchmark_runtime_source.csv"),
  row.names = FALSE
)

runtime_plot <- ggplot(runtime_data, aes(runtime_mean_across_problems, reorder(algorithm, runtime_mean_across_problems))) +
  geom_col(aes(fill = proposed), width = 0.62) +
  geom_errorbar(
    aes(xmin = runtime_min_problem, xmax = runtime_max_problem),
    orientation = "y", width = 0.22, linewidth = 0.45
  ) +
  scale_x_log10(labels = label_number(accuracy = 0.1)) +
  scale_fill_manual(values = c(`FALSE` = "#BDBDBD", `TRUE` = "#D24B40"), guide = "none") +
  labs(
    title = "Observed implementation runtime",
    subtitle = "Bars show the mean across five problems; whiskers show the problem-level range",
    x = "Seconds per run (log scale)",
    y = NULL,
    caption = "Runtime is implementation- and hardware-specific; it is not an algorithm-independent complexity estimate."
  ) +
  theme_report() +
  theme(axis.title.x = element_text(size = 8))

save_figure(
  runtime_plot,
  file.path(output_dir, "benchmark_runtime"),
  width_mm = 165,
  height_mm = 100
)

# Benchmark convergence plots ---------------------------------------------------

convergence <- read.csv(
  "results/algorithm_benchmark/algorithm_benchmark_convergence.csv",
  check.names = FALSE
)

convergence_specs <- list(
  zdt4 = c("OADE_NSGAII", "NSGA2", "DNSGA2", "CE_MOEA"),
  zdt6 = c("OADE_NSGAII", "NSGA2", "CGDE_NSGAII", "CE_MOEA")
)

convergence_palette <- c(
  OADE_NSGAII = "#D24B40",
  NSGA2 = "#4D4D4D",
  DNSGA2 = "#3182BD",
  CGDE_NSGAII = "#33A02C",
  CE_MOEA = "#9467BD"
)

convergence_source <- list()
for (problem_name in names(convergence_specs)) {
  selected_algorithms <- convergence_specs[[problem_name]]
  plot_data <- convergence %>%
    filter(problem == problem_name, algorithm %in% selected_algorithms) %>%
    group_by(problem, algorithm, checkpoint_fraction) %>%
    summarise(
      median_IGD = median(IGD),
      q25_IGD = quantile(IGD, 0.25),
      q75_IGD = quantile(IGD, 0.75),
      runs = n(),
      .groups = "drop"
    ) %>%
    mutate(
      algorithm_display = factor(
        algorithm,
        levels = selected_algorithms,
        labels = algorithm_labels[selected_algorithms]
      )
    )

  convergence_source[[problem_name]] <- plot_data

  convergence_plot <- ggplot(
    plot_data,
    aes(checkpoint_fraction, median_IGD, colour = algorithm_display, fill = algorithm_display)
  ) +
    geom_ribbon(aes(ymin = q25_IGD, ymax = q75_IGD), alpha = 0.10, colour = NA) +
    geom_line(linewidth = 0.85) +
    scale_x_continuous(labels = percent_format(), breaks = seq(0.2, 1.0, 0.2)) +
    scale_y_log10(labels = label_number(accuracy = 0.001)) +
    scale_colour_manual(
      values = setNames(convergence_palette[selected_algorithms], algorithm_labels[selected_algorithms]),
      name = NULL
    ) +
    scale_fill_manual(
      values = setNames(convergence_palette[selected_algorithms], algorithm_labels[selected_algorithms]),
      name = NULL
    ) +
    labs(
      title = paste0(toupper(problem_name), " convergence under the fixed evaluation budget"),
      subtitle = "Median IGD with interquartile bands across 30 runs",
      x = "Fraction of the 20,000-evaluation budget",
      y = "IGD (log scale)",
      caption = "Curves use recorded checkpoint fractions; lower IGD is better."
    ) +
    theme_report() +
    theme(
      axis.title = element_text(size = 8),
      legend.position = "top",
      legend.direction = "horizontal"
    )

  save_figure(
    convergence_plot,
    file.path(output_dir, paste0("benchmark_convergence_", problem_name)),
    width_mm = 165,
    height_mm = 105
  )
}

write.csv(
  bind_rows(convergence_source),
  file.path(output_dir, "benchmark_convergence_source.csv"),
  row.names = FALSE
)

# Ablation significant-outcome bar chart ----------------------------------------

ablation_outcomes <- ablation_plot_data %>%
  mutate(
    outcome = case_when(
      significant & result == "reference_better" ~ "Full better",
      significant & result == "comparison_better" ~ "Removal better",
      TRUE ~ "No corrected difference"
    )
  ) %>%
  count(comparison_algorithm, outcome, name = "endpoint_count") %>%
  complete(
    comparison_algorithm,
    outcome = c("Full better", "Removal better", "No corrected difference"),
    fill = list(endpoint_count = 0)
  ) %>%
  mutate(outcome = factor(
    outcome,
    levels = c("No corrected difference", "Removal better", "Full better")
  ))

write.csv(
  ablation_outcomes,
  file.path(output_dir, "ablation_outcome_counts_source.csv"),
  row.names = FALSE
)

ablation_outcome_plot <- ggplot(
  ablation_outcomes,
  aes(comparison_algorithm, endpoint_count, fill = outcome)
) +
  geom_col(width = 0.72, colour = "white", linewidth = 0.35) +
  geom_text(
    aes(label = if_else(endpoint_count > 0, as.character(endpoint_count), "")),
    position = position_stack(vjust = 0.5), size = 2.8
  ) +
  scale_fill_manual(
    values = c(
      "No corrected difference" = "#D9D9D9",
      "Removal better" = "#3182BD",
      "Full better" = "#D95F0E"
    ),
    name = NULL
  ) +
  scale_y_continuous(breaks = 0:10, expand = expansion(mult = c(0, 0.08))) +
  labs(
    title = "Corrected ablation outcomes by removed component",
    subtitle = "Ten problem-metric endpoints are counted for each component removal",
    x = "Removed component",
    y = "Number of endpoints",
    caption = "Two-sided paired Wilcoxon tests with Holm adjustment; n = 30 paired runs per endpoint."
  ) +
  theme_report() +
  theme(axis.title = element_text(size = 8), legend.position = "top")

save_figure(
  ablation_outcome_plot,
  file.path(output_dir, "ablation_outcome_counts"),
  width_mm = 165,
  height_mm = 105
)

# Restart paired-difference boxplot ---------------------------------------------

ablation_raw <- read.csv(
  "results/ablation/algorithm_benchmark_raw_runs.csv",
  check.names = FALSE
)

restart_pairs <- ablation_raw %>%
  filter(algorithm %in% c("OADE_FULL", "OADE_NO_RESTART")) %>%
  select(problem, run_idx, algorithm, IGD, HV) %>%
  pivot_wider(names_from = algorithm, values_from = c(IGD, HV)) %>%
  transmute(
    problem,
    run_idx,
    `IGD` = 100 * (IGD_OADE_FULL - IGD_OADE_NO_RESTART) / abs(IGD_OADE_FULL),
    `HV` = 100 * (HV_OADE_NO_RESTART - HV_OADE_FULL) / abs(HV_OADE_FULL)
  ) %>%
  pivot_longer(c(IGD, HV), names_to = "metric", values_to = "removal_improvement_percent") %>%
  mutate(endpoint = factor(
    paste(toupper(problem), metric),
    levels = rev(as.vector(rbind(
      paste(toupper(problem_order), "IGD"),
      paste(toupper(problem_order), "HV")
    )))
  ))

write.csv(
  restart_pairs,
  file.path(output_dir, "ablation_restart_paired_source.csv"),
  row.names = FALSE
)

restart_plot <- ggplot(restart_pairs, aes(removal_improvement_percent, endpoint)) +
  geom_vline(xintercept = 0, colour = "#555555", linewidth = 0.5) +
  geom_boxplot(
    width = 0.62, outlier.shape = NA,
    fill = "#9ECAE1", colour = "#2171B5", linewidth = 0.45
  ) +
  geom_point(
    position = position_jitter(height = 0.12, width = 0),
    alpha = 0.30, size = 1.0, colour = "#1F1F1F"
  ) +
  scale_x_continuous(labels = label_number(suffix = "%", accuracy = 1)) +
  labs(
    title = "Run-level change after removing restart",
    subtitle = "Positive values favour No Restart; each point is one paired seed",
    x = "Relative final-quality improvement",
    y = NULL,
    caption = "IGD improvement uses the proportional reduction; HV improvement uses the proportional increase. n = 30 paired runs."
  ) +
  theme_report() +
  theme(axis.title.x = element_text(size = 8))

save_figure(
  restart_plot,
  file.path(output_dir, "ablation_restart_paired"),
  width_mm = 165,
  height_mm = 115
)

message("Saved research figures to ", output_dir)
