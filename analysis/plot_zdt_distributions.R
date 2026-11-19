# Reproduce from the repository root with Rscript --vanilla.
# Quantitative-grid contract: show quality, paired evidence and measured cost;
# retain failed-quality tails, exclude only the prespecified collapsed front.
local_lib <- "renv/library/windows/R-4.6/x86_64-w64-mingw32"
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
library(ggplot2)
library(patchwork)
# Layout calculations may request a default device before the export opens.
options(device = function(...) grDevices::pdf(file = NULL, ...))
source(".agents/skills/nature-figure/scripts/panel_alignment.R")
source("analysis/measure_r_panels.R")
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "docs/reports/figures/zdt_six"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
data_dir <- "results/experiments/zdt_six_fixed_oade_v1/derived"
raw <- read.csv(file.path(data_dir, "audited_raw_runs.csv"))
effects <- read.csv(file.path(data_dir, "audited_comparisons.csv"))
stopifnot(nrow(raw) == 900, nrow(effects) == 50,
          !anyDuplicated(raw[c("problem", "algorithm", "seed")]))
valid <- tolower(as.character(raw$valid)) == "true"
stopifnot(sum(valid) == 899, sum(!valid) == 1,
          raw$algorithm[!valid] == "CGDE_NSGAII", raw$seed[!valid] == 63)
algorithms <- c("OADE_NSGAII", "NSGA2", "DNSGA2", "CGDE_NSGAII", "GDE3", "NSDE")
labels <- c("OADE", "NSGA-II", "D-NSGA-II", "CGDE", "GDE3", "NSDE")
names(labels) <- algorithms
problems <- c("zdt1", "zdt2", "zdt3", "zdt4", "zdt6")
raw$algorithm <- factor(raw$algorithm, levels = rev(algorithms))
raw$highlight <- ifelse(raw$algorithm == "OADE_NSGAII", "OADE", "Baseline")
theme_set(theme_classic(base_size = 8, base_family = "sans") +
  theme(axis.line = element_line(linewidth = 0.3),
        axis.ticks = element_line(linewidth = 0.3),
        axis.text = element_text(size = 7, colour = "#333333"),
        plot.title = element_text(size = 9, face = "bold"),
        plot.margin = margin(5, 7, 4, 5), legend.position = "none"))
save_plot <- function(p, stem, width_mm = 183, height_mm = 220) {
  path <- file.path(out, stem)
  w <- width_mm / 25.4; h <- height_mm / 25.4
  if (inherits(p, "patchwork")) {
    require_patchwork_panel_alignment(p,
      manifest_path = paste0(path, ".alignment-layout.json"),
      report_path = paste0(path, ".alignment.json"),
      width_in = w, height_in = h, tolerance_pt = 1.5,
      gutter_tolerance_pt = 1.5, strict = TRUE,
      audit_script = ".agents/skills/nature-figure/scripts/audit_panel_alignment.py",
      python = normalizePath(".venv/Scripts/python.exe"))
  }
  grDevices::pdf(paste0(path, ".pdf"), width = w, height = h,
                family = "Helvetica", useDingbats = FALSE)
  print(p); dev.off()
  svglite::svglite(paste0(path, ".svg"), width = w, height = h)
  print(p); dev.off()
  ragg::agg_png(paste0(path, ".png"), width = width_mm, height = height_mm,
                units = "mm", res = 300, background = "white")
  print(p); dev.off()
}
distribution <- function(metric, stem, axis_title, log_axis = FALSE) {
  # All completed runs contribute runtime; quality uses only valid runs.
  d <- if (metric == "runtime_seconds") raw else raw[valid, ]
  stopifnot(all(is.finite(d[[metric]])), !log_axis || all(d[[metric]] > 0))
  panels <- lapply(seq_along(problems), function(i) {
    sub <- d[d$problem == problems[i], ]
    p <- ggplot(sub, aes(x = .data[[metric]], y = algorithm)) +
      geom_boxplot(aes(fill = highlight), orientation = "y", width = 0.55,
                   linewidth = 0.3, outlier.shape = NA, colour = "#555555") +
      geom_point(aes(colour = highlight), size = 0.7, alpha = 0.65,
        position = position_jitter(width = 0, height = 0.13, seed = 20261117)) +
      scale_fill_manual(values = c(OADE = "#B5D9E8", Baseline = "#E7E7E7")) +
      scale_colour_manual(values = c(OADE = "#0072B2", Baseline = "#777777")) +
      scale_y_discrete(labels = labels, drop = FALSE) +
      labs(title = paste0(letters[i], "  ", toupper(problems[i])),
           x = if (i == 5) axis_title else NULL, y = NULL)
    if (log_axis) p <- p + scale_x_continuous(breaks = scales::breaks_log(n = 5),
      labels = scales::label_number()) + coord_transform(x = "log10")
    if (metric == "HV") p <- p + scale_x_continuous(limits = c(0, NA),
                                                  expand = expansion(mult = c(0.02, 0.04)))
    p
  })
  save_plot(wrap_plots(panels, ncol = 1), stem)
  write.csv(d[c("problem", "algorithm", "seed", metric)],
            file.path(out, paste0(stem, ".source.csv")), row.names = FALSE)
}
distribution("IGD", "igd_distribution", "IGD (log scale; lower is better)", TRUE)
distribution("HV", "hv_distribution", "Hypervolume (higher is better)")
distribution("runtime_seconds", "runtime_distribution", "Measured runtime (seconds; log scale)", TRUE)
# Median and IQR remain positive on a logarithmic scale, including skewed ZDT4
# groups for which mean minus SD is negative. No pseudocount is introduced.
groups <- split(raw[valid, ], list(raw$problem[valid], raw$algorithm[valid]), drop = TRUE)
log_data <- do.call(rbind, lapply(groups, function(g) data.frame(
  problem = g$problem[1], algorithm = as.character(g$algorithm[1]), n = nrow(g),
  median = median(g$IGD), q1 = unname(quantile(g$IGD, 0.25)),
  q3 = unname(quantile(g$IGD, 0.75)))))
stopifnot(nrow(log_data) == 30, sum(log_data$n) == 899,
          all(is.finite(log_data$median)), all(log_data$q1 > 0))
log_data$algorithm <- factor(log_data$algorithm, levels = rev(algorithms))
log_data$highlight <- ifelse(log_data$algorithm == "OADE_NSGAII", "OADE", "Baseline")
limits <- range(log_data$q1, log_data$q3) * c(0.8, 1.3)
panels <- lapply(seq_along(problems), function(i) {
  sub <- log_data[log_data$problem == problems[i], ]
  ggplot(sub, aes(x = median, y = algorithm, colour = highlight)) +
    geom_segment(aes(x = q1, xend = q3, yend = algorithm), linewidth = 0.8) +
    geom_point(size = 2) +
    scale_colour_manual(values = c(OADE = "#0072B2", Baseline = "#777777")) +
    scale_x_log10(limits = limits, breaks = c(0.003, 0.01, 0.1, 1, 10),
                  labels = c("0.003", "0.01", "0.1", "1", "10")) +
    scale_y_discrete(labels = labels) +
    labs(title = paste0(letters[i], "  ", toupper(problems[i])), y = NULL,
         x = if (i == 5) "IGD median and IQR (log10 scale; lower is better)" else NULL) +
    theme(panel.grid.major.x = element_line(colour = "#EEEEEE", linewidth = 0.3))
})
save_plot(wrap_plots(panels, ncol = 1), "igd_log_comparison")
write.csv(log_data, file.path(out, "igd_log_comparison.source.csv"), row.names = FALSE)
cat("Exported IGD log-scale comparison\n")
