# One plotting panel: paired effect sizes, with global-Holm test outcomes.
.libPaths(c("renv/library/windows/R-4.6/x86_64-w64-mingw32", .libPaths()))
library(ggplot2)
library(svglite)
library(ragg)
d <- read.csv("results/experiments/zdt_six_fixed_oade_v1/derived/audited_comparisons.csv")
out <- "docs/reports/figures/zdt_six"
dir.create(out, recursive=TRUE, showWarnings=FALSE)
names <- c("NSGA2", "DNSGA2", "CGDE_NSGAII", "GDE3", "NSDE")
short <- c("NSGA-II", "D-NSGA-II", "CGDE-NSGA-II", "GDE3", "NSDE")
d$label <- paste(short[match(d$comparison_algorithm, names)], d$metric, sep="  |  ")
levels <- unlist(lapply(short, function(x) paste(x, c("IGD", "HV"), sep="  |  ")))
d$label <- factor(d$label, levels=rev(levels))
d$problem <- factor(toupper(d$problem), levels=c("ZDT1", "ZDT2", "ZDT3", "ZDT4", "ZDT6"))
d$outcome <- ifelse(d$result=="reference_better", "+", ifelse(d$result=="comparison_better", "-", "NS"))
p <- ggplot(d, aes(problem, label, fill=rank_biserial_effect)) +
  geom_tile(color="white", linewidth=0.7) +
  geom_text(aes(label=outcome), size=2.8, family="sans") +
  scale_fill_gradient2(low="#B97C5A", mid="white", high="#69AFA1", midpoint=0,
                       limits=c(-1,1), breaks=c(-1,0,1), name="Rank-biserial effect") +
  scale_x_discrete(expand=c(0,0)) + scale_y_discrete(expand=c(0,0)) +
  coord_fixed(ratio=0.55, clip="off") +
  labs(x=NULL, y=NULL) +
  theme_minimal(base_size=9, base_family="sans") +
  theme(panel.grid=element_blank(), axis.text=element_text(color="black"),
        axis.text.y=element_text(size=8), legend.position="bottom",
        legend.title=element_text(size=8), legend.text=element_text(size=8),
        legend.key.width=grid::unit(20,"mm"), plot.margin=margin(6,8,5,5))
ggsave(file.path(out,"paired_effects.png"), p, width=183, height=153, units="mm", dpi=300, device=ragg::agg_png, bg="white")
ggsave(file.path(out,"paired_effects.pdf"), p, width=183, height=153, units="mm", device=grDevices::pdf, family="Helvetica", useDingbats=FALSE)
ggsave(file.path(out,"paired_effects.svg"), p, width=183, height=153, units="mm", device=svglite::svglite, bg="white")
writeLines(capture.output(sessionInfo()), file.path(out,"sessionInfo.txt"))
write.csv(d, file.path(out,"source_data.csv"), row.names=FALSE)
writeLines(c("Single plotting panel; multipanel alignment: not applicable.",
             "Input: audited_comparisons.csv; all 50 planned endpoints retained.",
             "PDF uses base R Helvetica with editable text; cairo_pdf static rule exception follows project workflow.",
             "Positive rank-biserial favors OADE. +/NS encode global-Holm results, not effect thresholds."),
           file.path(out,"figure_notes.txt"))
