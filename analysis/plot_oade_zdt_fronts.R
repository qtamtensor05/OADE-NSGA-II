# Contract: show geometric coverage against the true PF for minimum-IGD runs,
# selected per problem at the user's request. Best-case grid, R-only.
# Match color/marker roles in the requested visual, with readable report typography.
local_lib <- "renv/library/windows/R-4.6/x86_64-w64-mingw32"
if(dir.exists(local_lib)) .libPaths(c(local_lib,.libPaths()))
library(ggplot2)
library(patchwork)
options(device=function(...) grDevices::pdf(file=NULL,...))
source(".agents/skills/nature-figure/scripts/panel_alignment.R")
source("analysis/measure_r_panels.R")
out <- "docs/reports/figures/oade_zdt_best_fronts"
points <- read.csv(file.path(out,"solutions.source.csv"))
reference <- read.csv(file.path(out,"reference.source.csv"))
panels <- read.csv(file.path(out,"panels.source.csv"))
stopifnot(nrow(panels)==5,all(panels$selection=="best_igd"),all(is.finite(points$f1)),all(is.finite(points$f2)),
  length(unique(reference$segment[reference$problem=="zdt3"]))==5)
theme_set(theme_classic(base_size=8,base_family="sans")+theme(
  axis.text=element_text(size=7,colour="#333333"),axis.line=element_line(linewidth=.3),
  plot.title=element_text(size=9,face="bold"),plot.subtitle=element_text(size=7),
  plot.margin=margin(7,8,6,6),legend.position="none"))
build <- function(i) {
  meta <- panels[i,]; d <- points[points$panel==meta$panel,];ref <- reference[reference$problem==meta$problem,]
  stopifnot(nrow(d)==meta$n_points)
  ggplot()+
    geom_path(data=ref,aes(f1,f2,group=segment),colour="#CB54A0",linewidth=.55)+
    geom_point(data=ref,aes(f1,f2),shape=1,size=.65,stroke=.3,colour="#CB54A0")+
    geom_point(data=d,aes(f1,f2),shape=3,size=1.2,stroke=.45,colour="#225CB0")+
    labs(x=expression(f[1]),y=expression(f[2]),
      title=paste(meta$panel,toupper(meta$problem)),
      subtitle=paste0("Seed ",meta$seed,"; IGD = ",formatC(meta$IGD,format="e",digits=2),
        "\nHV = ",formatC(meta$HV,format="e",digits=2),"; n = ",meta$n_points))+
    scale_x_continuous(labels=scales::label_number())+
    scale_y_continuous(labels=scales::label_number())
}
save_plot <- function(p,stem,width_mm,height_mm,multi=FALSE) {
  path <- file.path(out,stem);w <- width_mm/25.4;h <- height_mm/25.4
  if(multi) require_patchwork_panel_alignment(p,manifest_path=paste0(path,".alignment-layout.json"),
    report_path=paste0(path,".alignment.json"),width_in=w,height_in=h,tolerance_pt=1.5,
    gutter_tolerance_pt=1.5,strict=TRUE,
    audit_script=".agents/skills/nature-figure/scripts/audit_panel_alignment.py",
    python=normalizePath(".venv/Scripts/python.exe"))
  # Base PDF preserves editable glyphs; cairo_pdf text grouping on this runtime
  # previously created false collision boxes. Final PDF geometry is audited.
  grDevices::pdf(paste0(path,".pdf"),width=w,height=h,family="Helvetica",useDingbats=FALSE)
  print(p);dev.off()
  svglite::svglite(paste0(path,".svg"),width=w,height=h);print(p);dev.off()
  ragg::agg_png(paste0(path,".png"),width=width_mm,height=height_mm,units="mm",res=300,background="white")
  print(p);dev.off()
}
plots <- lapply(seq_len(nrow(panels)),build)
overview <- wrap_plots(plots,ncol=3)+plot_annotation(
  caption="Pink circles/line: true Pareto front   Blue crosses: OADE final solutions\nMinimum-IGD run selected from 30 seeds per problem (best case, not typical performance)",
  theme=theme(plot.caption=element_text(size=8,hjust=.5)))
save_plot(overview,"oade_zdt_best_fronts",183,145,TRUE)
for(i in seq_len(nrow(panels))) {
  meta <- panels[i,]
  stem <- paste0(meta$problem,"_best_igd_seed",meta$seed)
  p <- plots[[i]]+labs(caption="Pink: true PF; blue crosses: final OADE solutions")+
    theme(plot.caption=element_text(size=7))
  save_plot(p,stem,100,90)
}
writeLines(capture.output(sessionInfo()),file.path(out,"R-session.txt"))
