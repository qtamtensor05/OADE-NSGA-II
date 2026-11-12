#!/usr/bin/env Rscript
# Within-seed DE-probability effects complement marginal response curves.
suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(jsonlite)})
source("analysis/figures/helpers/panel_alignment.R")
directory <- Sys.getenv("ZDT_SENSITIVITY_DIR", "results/experiments/zdt_sensitivity_ofat_v1")
d <- read.csv(file.path(directory, "derived/paired_seed_changes.csv"))
d <- d[d$parameter == "prob_de" & d$metric %in% c("IGD", "HV"), ]
stopifnot(nrow(d) == 600, all(d$valid_pair %in% c("True", "TRUE")), all(is.finite(d$percent_change)))
groups <- split(d, interaction(d$level, d$problem, d$metric, drop = TRUE))
s <- do.call(rbind, lapply(groups, function(x) {
  stopifnot(nrow(x) == 30)
  data.frame(level = x$level[1], problem = x$problem[1], metric = x$metric[1], n = nrow(x),
             median = median(x$percent_change), low = unname(quantile(x$percent_change, .25)),
             high = unname(quantile(x$percent_change, .75)))
}))
write.csv(s, file.path(directory, "derived/prob_de_paired_plot_data.csv"), row.names = FALSE)
# Express both indicators in the same direction: positive means improvement.
s$improvement <- ifelse(s$metric == "IGD", -s$median, s$median)
s$improvement_low <- ifelse(s$metric == "IGD", -s$high, s$low)
s$improvement_high <- ifelse(s$metric == "IGD", -s$low, s$high)
write.csv(s, file.path(directory, "derived/prob_de_paired_plot_data.csv"), row.names = FALSE)
theme_set(theme_minimal(base_family = "Arial", base_size = 11) + theme(
  panel.grid.minor = element_blank(), panel.grid.major.x = element_blank(),
  axis.text = element_text(size = 9, colour = "#273540"),
  axis.text.y = element_text(family = "Consolas"),
  legend.position = "none", plot.title = element_text(size = 12, face = "bold"),
  plot.subtitle = element_text(size = 9), plot.margin = margin(10, 10, 10, 10)))
panels <- list()
for (metric in c("IGD", "HV")) {
  for (problem in c("zdt1", "zdt2", "zdt3", "zdt4", "zdt6")) {
    x <- s[s$metric == metric & s$problem == problem, ]
    x$level_label <- factor(x$level, levels = c(.2, .8), labels = c("Giảm: 0,2", "Tăng: 0,8"))
    panels[[length(panels) + 1]] <- ggplot(x, aes(level_label, improvement, fill = factor(level))) +
      geom_hline(yintercept = 0, colour = "#273540", linewidth = .5) +
      geom_col(width = .55, alpha = .85) +
      geom_errorbar(aes(ymin = improvement_low, ymax = improvement_high), width = .15, linewidth = .55) +
      scale_fill_manual(values = c("0.2" = "#C27A42", "0.8" = "#306A86")) +
      scale_y_continuous(labels = function(v) sprintf("%9.3f", v), expand = expansion(mult = c(.1, .12))) +
      labs(title = paste(toupper(problem), "·", metric),
           subtitle = "Trên 0: tốt hơn; dưới 0: kém hơn", x = NULL,
           y = paste("Cải thiện", metric, "(%)"))
  }
}
p <- wrap_plots(panels, ncol = 5) + plot_annotation(
  title = "Giảm hoặc tăng xác suất DE có cải thiện chất lượng nghiệm?",
  subtitle = "So với prob_de = 0,5. Mỗi bài có thang riêng; cột trên đường 0 biểu thị cải thiện.",
  caption = "Cột: trung vị mức cải thiện của 30 cặp seed; thanh mảnh: Q25–Q75, không phải khoảng tin cậy.\nIGD: mức cải thiện = −% thay đổi; HV: mức cải thiện = +% thay đổi. Các tham số khác giữ nguyên.",
  theme = theme(plot.title = element_text(size = 16, face = "bold"),
                plot.subtitle = element_text(size = 11), plot.caption = element_text(size = 10, hjust = 0)))
stem <- file.path(directory, "figures/prob_de_paired")
python <- normalizePath(".venv/Scripts/python.exe")
require_patchwork_panel_alignment(p, paste0(stem, ".alignment-layout.json"), paste0(stem, ".alignment.json"),
  width_in = 16, height_in = 8, python = python, audit_script = "scripts/figure_qa/audit_panel_alignment.py", strict = TRUE)
ggsave(paste0(stem, ".png"), p, width = 16, height = 8, dpi = 300, device = ragg::agg_png, bg = "white")
ggsave(paste0(stem, ".pdf"), p, width = 16, height = 8, device = cairo_pdf, family = "Arial")
svglite::svglite(paste0(stem, ".svg"), width = 16, height = 8); print(p); dev.off()
for (audit in c("audit_figure_collisions", "audit_pdf_text")) {
  args <- c(paste0("scripts/figure_qa/", audit, ".py"), shQuote(paste0(stem, ".pdf")))
  if (audit == "audit_figure_collisions") args <- c(args, "--json-out", shQuote(paste0(stem, ".collision-audit.json"))) else args <- c(args, "--json")
  result <- suppressWarnings(system2(python, args, stdout = TRUE, stderr = TRUE))
  if (!is.null(attr(result, "status")) && attr(result, "status") != 0) stop(paste(result, collapse = "\n"))
  if (audit == "audit_pdf_text") writeLines(result, paste0(stem, ".font-audit.json"), useBytes = TRUE)
}
