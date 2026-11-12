#!/usr/bin/env Rscript
# Direct OFAT response curves. Each panel is one ZDT problem and one metric;
# lines connect measured parameter levels only. No scores or winner selection.
suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(jsonlite)
})
source("analysis/figures/helpers/panel_alignment.R")
directory <- Sys.getenv("ZDT_SENSITIVITY_DIR")
if (!nzchar(directory)) stop("Set ZDT_SENSITIVITY_DIR to a completed OFAT study")
data <- read.csv(file.path(directory, "derived/summary.csv"), stringsAsFactors = FALSE)
configuration <- read_json(file.path(directory, "config/resolved.json"), simplifyVector = TRUE)
is_smoke <- isTRUE(configuration$protocol$smoke)
out <- file.path(directory, "figures")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
python <- normalizePath(".venv/Scripts/python.exe")
problems <- c("zdt1", "zdt2", "zdt3", "zdt4", "zdt6")
problems <- problems[problems %in% data$problem]
theme_set(theme_minimal(base_size = 10, base_family = "Arial") + theme(
  panel.grid = element_blank(), axis.text = element_text(size = 9, colour = "#273540"),
  axis.text.x = element_text(margin = margin(t = 7)),
  axis.title = element_text(size = 9), plot.title = element_text(size = 10, face = "bold"),
  plot.caption = element_text(size = 9, hjust = 0), plot.margin = margin(8, 12, 8, 12)))

for (parameter in unique(data$parameter)) {
  subset <- data[data$parameter == parameter, ]
  levels <- sort(unique(subset$level))
  baseline <- unique(subset$baseline_level)
  stopifnot(length(baseline) == 1, baseline %in% levels)
  panels <- list()
  for (problem in problems) {
    current <- subset[subset$problem == problem, ]
    current <- current[order(current$level), ]
    stopifnot(nrow(current) == length(levels), all(current$runs >= 2))
    for (metric in c("IGD", "HV")) {
      panel <- data.frame(x = match(current$level, levels), median = current[[paste0(metric, "_median")]],
                          low = current[[paste0(metric, "_q25")]], high = current[[paste0(metric, "_q75")]])
      p <- ggplot(panel, aes(x, median)) +
        geom_vline(xintercept = match(baseline, levels), linetype = "dashed", colour = "#C27A42", linewidth = .5)
      if (length(levels) > 1) {
        p <- p + geom_ribbon(aes(ymin = low, ymax = high), fill = "#8FB7C8", alpha = .35, na.rm = TRUE) +
          geom_line(colour = "#306A86", linewidth = .65, na.rm = TRUE)
      } else {
        p <- p + geom_errorbar(aes(ymin = low, ymax = high), width = .1, colour = "#306A86", na.rm = TRUE)
      }
      p <- p + geom_point(colour = "#306A86", size = 2, na.rm = TRUE) +
        scale_x_continuous(breaks = seq_along(levels), labels = format(levels, digits = 4, trim = TRUE),
                           limits = c(.8, length(levels) + .2)) +
        labs(title = paste(toupper(problem), if (metric == "IGD") "· IGD ↓ (thấp hơn tốt hơn)" else "· HV ↑ (cao hơn tốt hơn)"),
             x = parameter, y = metric)
      positive_range <- any(is.finite(panel$high) & panel$high > 0)
      p <- p + scale_y_continuous(limits = c(0, if (positive_range) NA_real_ else 1),
                                  expand = expansion(mult = c(0, .08)))
      if (any(current$valid_runs == 0)) {
        # Keep the measured level in the source table and identify its missing
        # quality result explicitly; do not interpolate through failed levels.
        p <- p + labs(subtitle = "Có mức không có output hợp lệ; xem bảng invalid")
      }
      panels[[length(panels) + 1]] <- p
    }
  }
  plot <- wrap_plots(panels, ncol = 2) + plot_annotation(
    title = paste(if (is_smoke) "SMOKE — Tăng/giảm" else "Tăng/giảm", parameter, "ảnh hưởng gì trên ZDT?"),
    subtitle = paste0("Chỉ đổi một tham số. ", if (is_smoke) "Mốc smoke: " else "Mức v2 hiện tại: ", baseline, "; đường đứt màu cam đánh dấu mức này."),
    caption = paste0("Chấm/đường: median; dải: Q25–Q75 qua ", unique(subset$runs)[1], " seed mỗi mức/bài, không phải CI.\n",
                     "Các mức là rời rạc; đường nối chỉ hướng dẫn đọc. Invalid được giữ trong bảng, không có điểm tổng hoặc cấu hình thắng."),
    theme = theme(plot.title = element_text(size = 15, face = "bold"),
                  plot.subtitle = element_text(size = 10), plot.caption = element_text(size = 9)))
  stem <- file.path(out, parameter)
  width <- 12
  height <- 2.5 * length(problems) + 1.3
  require_patchwork_panel_alignment(plot, paste0(stem, ".alignment-layout.json"), paste0(stem, ".alignment.json"),
                                    width_in = width, height_in = height, python = python,
                                    audit_script = "scripts/figure_qa/audit_panel_alignment.py", strict = TRUE)
  ggsave(paste0(stem, ".png"), plot, width = width, height = height, dpi = 300, device = ragg::agg_png, bg = "white")
  ggsave(paste0(stem, ".pdf"), plot, width = width, height = height, device = cairo_pdf, family = "Arial")
  svglite::svglite(paste0(stem, ".svg"), width = width, height = height)
  print(plot)
  dev.off()
  collision <- suppressWarnings(system2(python, c("scripts/figure_qa/audit_figure_collisions.py", shQuote(paste0(stem, ".pdf")),
                                                 "--json-out", shQuote(paste0(stem, ".collision-audit.json"))), stdout = TRUE, stderr = TRUE))
  status <- attr(collision, "status")
  if (!is.null(status) && status != 0) stop(paste(collision, collapse = "\n"))
  font <- suppressWarnings(system2(python, c("scripts/figure_qa/audit_pdf_text.py", shQuote(paste0(stem, ".pdf")), "--json"),
                                  stdout = TRUE, stderr = TRUE))
  status <- attr(font, "status")
  if (!is.null(status) && status != 0) stop(paste(font, collapse = "\n"))
  writeLines(font, paste0(stem, ".font-audit.json"), useBytes = TRUE)
  message("Figure ready: ", parameter)
}
write_json(list(method = "OFAT", smoke = is_smoke, input = "derived/summary.csv", plots = unique(data$parameter),
                uncertainty = "Q25-Q75 across stochastic seeds, not CI", scores = FALSE),
           file.path(out, "figure_methods.json"), pretty = TRUE, auto_unbox = TRUE)
