# Figure contract: mechanism benefits depend on problem; full is not uniformly best.
# R-only quantitative grid; all 30 paired seeds retained; no journal-specific claim.
local_lib <- "renv/library/windows/R-4.6/x86_64-w64-mingw32"
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
library(ggplot2)
library(patchwork)
options(device = function(...) grDevices::pdf(file = NULL, ...))
source(".agents/skills/nature-figure/scripts/panel_alignment.R")
source("analysis/measure_r_panels.R")
d <- "results/experiments/oade_mechanism_zdt46/derived"
out <- "docs/reports/figures/mechanism_zdt46"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
effects <- read.csv(file.path(d, "audited_impact.csv"))
pairs <- read.csv(file.path(d, "audited_pairs.csv"))
stopifnot(nrow(effects) == 28, nrow(pairs) == 840)
variants <- c("no_obl", "no_restart", "fixed_f_cr", "fixed_pde", "global_neighborhood", "sbx_only", "de_only")
labels <- c("No OBL", "No restart", "Fixed F/CR", "Fixed pDE", "Global neighbors", "SBX only", "DE only")
theme_set(theme_classic(base_size=8, base_family="sans") + theme(
  axis.text=element_text(size=7, colour="#333333"), plot.title=element_text(size=9, face="bold"),
  plot.margin=margin(7,9,7,7), legend.position="bottom"))
save_plot <- function(p, stem, height_mm) {
  path <- file.path(out, stem); w <- 183/25.4; h <- height_mm/25.4
  if (stem != "mechanism_effects") require_patchwork_panel_alignment(p, manifest_path=paste0(path,".alignment-layout.json"),
    report_path=paste0(path,".alignment.json"), width_in=w,height_in=h,
    tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=TRUE,
    audit_script=".agents/skills/nature-figure/scripts/audit_panel_alignment.py",
    python=normalizePath(".venv/Scripts/python.exe"))
  # cairo_pdf coalesces distant labels into traces on this runtime; base PDF
  # preserves editable Helvetica text with individually auditable text boxes.
  grDevices::pdf(paste0(path,".pdf"),width=w,height=h,family="Helvetica",useDingbats=FALSE); print(p); dev.off()
  svglite::svglite(paste0(path,".svg"),width=w,height=h); print(p); dev.off()
  ragg::agg_png(paste0(path,".png"),width=183,height=height_mm,units="mm",res=300,background="white"); print(p); dev.off()
}
effects$comparison_algorithm <- factor(effects$comparison_algorithm, levels=rev(variants),labels=rev(labels))
effects$endpoint <- paste(toupper(effects$problem), effects$metric)
effects$endpoint <- factor(effects$endpoint,levels=c("ZDT4 IGD","ZDT4 HV","ZDT6 IGD","ZDT6 HV"))
effects$mark <- ifelse(effects$p_adjusted_holm < .05, "*", "NS")
hero <- ggplot(effects,aes(endpoint,comparison_algorithm,fill=rank_biserial_effect)) +
  geom_tile(width=.9,height=.9) + geom_text(aes(label=mark),size=2.6) +
  scale_fill_gradient2(low="#C89D75",mid="white",high="#428B97",limits=c(-1,1),name="Rank-biserial effect (positive favors full)") +
  labs(x=NULL,y=NULL,title="a  Conditional effects across 28 comparisons") +
  theme(axis.line=element_blank(),axis.ticks=element_blank())
# One panel is wrapped for the same export interface; alignment is not applicable.
save_plot(wrap_plots(hero), "mechanism_effects", 105)
panels <- list()
for (problem in c("zdt4","zdt6")) {
  sub <- pairs[pairs$problem==problem & pairs$metric=="IGD",]
  sub$comparison_algorithm <- factor(sub$comparison_algorithm,levels=rev(variants),labels=rev(labels))
  panels[[problem]] <- ggplot(sub,aes(benefit_full,comparison_algorithm)) +
    geom_vline(xintercept=0,linewidth=.3,colour="#999999") +
    geom_point(position=position_jitter(height=.12,width=0,seed=42),size=.8,alpha=.55,colour="#428B97") +
    stat_summary(fun=median,geom="point",size=2,colour="#222222") +
    scale_x_continuous(trans=scales::transform_pseudo_log(sigma=.001),
      breaks=if(problem=="zdt4") c(-2,-.1,-.01,0,.01,.1,2) else c(-.001,0,.001),
      labels=if(problem=="zdt4") scales::label_number() else scales::label_number(accuracy=.001)) +
    labs(x="IGD benefit of full (ablation - full)",y=NULL,
         title=paste(ifelse(problem=="zdt4","a","b"),toupper(problem)))
}
save_plot(wrap_plots(panels,ncol=1), "paired_igd", 175)
write.csv(effects,file.path(out,"mechanism_effects.source.csv"),row.names=FALSE)
write.csv(pairs,file.path(out,"paired_igd.source.csv"),row.names=FALSE)
writeLines(capture.output(sessionInfo()),file.path(out,"R-session.txt"))
