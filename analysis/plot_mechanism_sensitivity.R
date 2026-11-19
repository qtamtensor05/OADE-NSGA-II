# Quantitative-grid contract: show conditional level effects without selecting
# favorable seeds or suggesting a universal optimum. Overview = paired evidence;
# detail = raw distributions and failure tails. R-only, 183 mm vector report assets.
local_lib <- "renv/library/windows/R-4.6/x86_64-w64-mingw32"
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
library(ggplot2)
library(patchwork)
options(device=function(...) grDevices::pdf(file=NULL,...))
source(".agents/skills/nature-figure/scripts/panel_alignment.R")
source("analysis/measure_r_panels.R")
data_dir <- "results/experiments/mechanism_sensitivity_v1/derived"
out <- "docs/reports/figures/mechanism_sensitivity"
dir.create(out,recursive=TRUE,showWarnings=FALSE)
effects <- read.csv(file.path(data_dir,"audited_comparisons.csv"))
raw <- read.csv(file.path(data_dir,"runs.csv"))
summary <- read.csv(file.path(data_dir,"audited_summary.csv"))
stopifnot(nrow(raw)==2100,nrow(effects)==124,nrow(summary)==70,
  all(tolower(as.character(raw$valid))=="true"),all(effects$n_pairs==30),!anyDuplicated(raw[c("problem","algorithm","seed")]))
parameters <- c("obl_interval","obl_jump_rate","stagnation_patience","stagnation_tolerance",
  "diversity_threshold","restart_elite_ratio","n_neighbors","mean_F","mean_CR","prob_de")
titles <- c("OBL interval","OBL jump rate","Stagnation patience","Stagnation tolerance",
  "Diversity threshold","Restart elite ratio","DE neighbors","Mean F (held)","Mean CR (held)","pDE (held)")
names(titles) <- parameters
baseline <- c(obl_interval=10,obl_jump_rate=.2,stagnation_patience=20,
  stagnation_tolerance=.0001,diversity_threshold=.02,restart_elite_ratio=.8,
  n_neighbors=5,mean_F=.65,mean_CR=.5,prob_de=.5)
palette <- c(ZDT4="#277F8E",ZDT6="#AD673C")
theme_set(theme_classic(base_size=8,base_family="sans")+theme(
  axis.text=element_text(size=7,colour="#333333"),
  axis.line=element_line(linewidth=.3),axis.ticks=element_line(linewidth=.3),
  plot.title=element_text(size=9,face="bold"),plot.subtitle=element_text(size=7),
  plot.margin=margin(6,8,6,6),legend.position="bottom",legend.text=element_text(size=7)))
save_plot <- function(plot,stem,height_mm) {
  path <- file.path(out,stem); width_mm <- 183
  w <- width_mm/25.4;h <- height_mm/25.4
  require_patchwork_panel_alignment(plot,manifest_path=paste0(path,".alignment-layout.json"),
    report_path=paste0(path,".alignment.json"),width_in=w,height_in=h,
    tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=TRUE,
    audit_script=".agents/skills/nature-figure/scripts/audit_panel_alignment.py",
    python=normalizePath(".venv/Scripts/python.exe"))
  # Base PDF preserves editable text and separate auditable labels on this runtime;
  # cairo_pdf has previously merged distant labels into large text-trace boxes.
  grDevices::pdf(paste0(path,".pdf"),width=w,height=h,family="Helvetica",useDingbats=FALSE)
  print(plot);dev.off()
  svglite::svglite(paste0(path,".svg"),width=w,height=h);print(plot);dev.off()
  ragg::agg_png(paste0(path,".png"),width=width_mm,height=height_mm,units="mm",res=300,background="white")
  print(plot);dev.off()
}
level_labels <- function(x) format(x,trim=TRUE,scientific=FALSE,digits=6)
# Levels are ordered categories: equal visual spacing is not a numeric dose axis.
# CI scaling uses the observed reference median as a fixed display denominator.
effects$problem_display <- toupper(effects$problem)
stopifnot(all(effects$reference_median>0))
direction <- ifelse(effects$metric=="IGD",1,-1)
effects$benefit_percent <- direction*effects$median_paired_difference/effects$reference_median*100
lo <- direction*effects$ci_low/effects$reference_median*100
hi <- direction*effects$ci_high/effects$reference_median*100
effects$benefit_low <- pmin(lo,hi);effects$benefit_high <- pmax(lo,hi)
effects$decision <- ifelse(effects$p_adjusted_holm<.05,"Holm p < 0.05","Not significant")
for (metric in c("IGD","HV")) {
  panels <- lapply(seq_along(parameters),function(i) {
    parameter <- parameters[i]; d <- effects[effects$parameter==parameter & effects$metric==metric,]
    levels <- sort(unique(c(d$level,baseline[parameter])))
    d$level_factor <- factor(d$level,levels=levels,labels=level_labels(levels))
    ref <- data.frame(level_factor=factor(baseline[parameter],levels=levels,labels=level_labels(levels)),zero=0)
    dodge <- position_dodge(width=.38)
    panel <- ggplot(d,aes(level_factor,benefit_percent,colour=problem_display,group=problem_display))+
      geom_hline(yintercept=0,colour="#AAAAAA",linewidth=.3)+
      geom_linerange(aes(ymin=benefit_low,ymax=benefit_high),position=dodge,linewidth=.4)+
      geom_point(aes(shape=decision),position=dodge,size=1.8,stroke=.65)+
      geom_point(data=ref,aes(level_factor,zero),inherit.aes=FALSE,shape=18,size=2,colour="#333333")+
      scale_x_discrete(limits=level_labels(levels),drop=FALSE)+
      scale_colour_manual(values=palette,limits=c("ZDT4","ZDT6"),name="Problem")+
      scale_shape_manual(values=c("Holm p < 0.05"=16,"Not significant"=1),
        limits=c("Holm p < 0.05","Not significant"),name="Holm test")+
      labs(x=NULL,y="Paired benefit / ref. median (%)",title=paste(letters[i],titles[parameter]))+
      guides(colour="none",shape="none")
    extent <- max(abs(c(d$benefit_low,d$benefit_high)))
    if(metric=="IGD") {
      ticks <- if(extent<1) c(-.5,0,.5) else if(extent<5) c(-2,0,2) else c(-1000,-100,-10,0,10,100)
      panel <- panel+scale_y_continuous(trans=scales::transform_pseudo_log(sigma=1),
        breaks=ticks,labels=scales::label_number())+labs(y="Paired benefit (%; signed log)")
    }
    panel
  })
  p <- wrap_plots(panels,ncol=2)+plot_annotation(
    caption=paste("Teal: ZDT4   Brown: ZDT6   Black diamond: reference",
      "Filled: Holm p < 0.05   Open: not significant; intervals: unadjusted 95% CI",sep="\n"),
    theme=theme(plot.caption=element_text(size=8,hjust=.5)))
  save_plot(p,paste0("paired_",tolower(metric),"_overview"),265)
  write.csv(effects[effects$metric==metric,],file.path(out,paste0("paired_",tolower(metric),"_overview.source.csv")),row.names=FALSE)
}
if (!"--overview-only" %in% commandArgs(trailingOnly=TRUE)) for (parameter in parameters) {
  comparison <- effects[effects$parameter==parameter,]
  ref_id <- unique(comparison$reference_algorithm);stopifnot(length(ref_id)==1)
  ids <- unique(c(ref_id,comparison$comparison_algorithm))
  group <- summary[summary$algorithm %in% ids,]
  group$level[group$algorithm==ref_id] <- baseline[parameter]
  d <- merge(raw,group[c("problem","algorithm","level")],by=c("problem","algorithm"))
  levels <- sort(unique(group$level))
  stopifnot(nrow(d)==length(levels)*60,all(is.finite(d$IGD)),all(d$IGD>0))
  d$level_factor <- factor(d$level,levels=levels,labels=level_labels(levels))
  d$is_reference <- d$algorithm==ref_id
  panels <- list();index <- 0
  for (problem in c("zdt4","zdt6")) for (metric in c("IGD","HV")) {
    index <- index+1;sub <- d[d$problem==problem,]
    col <- palette[toupper(problem)]
    p <- ggplot(sub,aes(level_factor,.data[[metric]]))+
      geom_vline(xintercept=match(baseline[parameter],levels),linetype="dotted",linewidth=.4,colour="#666666")+
      geom_boxplot(width=.48,outlier.shape=NA,fill=col,alpha=.15,linewidth=.35)+
      geom_point(position=position_jitter(width=.09,height=0,seed=42),size=.55,alpha=.48,colour=col)+
      stat_summary(fun=median,geom="point",shape=18,size=2,colour="#222222")+
      labs(x=paste0(titles[parameter]," level"),y=if(metric=="IGD") "IGD (log10; lower is better)" else "HV (higher is better)",
        title=paste(letters[index],toupper(problem),metric),
        subtitle=if(ref_id=="full") "Dotted line: full production reference" else paste0("Dotted line: held reference = ",baseline[parameter]))
    # Transform coordinates after the statistics, retaining raw-scale medians
    # and quartiles rather than computing quantiles on log-transformed values.
    if(metric=="IGD") p <- p+scale_y_continuous(breaks=scales::breaks_log(n=4),labels=scales::label_number())+
      coord_transform(y="log10")
    panels[[index]] <- p
  }
  save_plot(wrap_plots(panels,ncol=2),paste0("levels_",parameter),170)
  write.csv(d,file.path(out,paste0("levels_",parameter,".source.csv")),row.names=FALSE)
}
writeLines(capture.output(sessionInfo()),file.path(out,"R-session.txt"))
inputs <- file.path(data_dir,c("audited_comparisons.csv","audited_summary.csv","runs.csv","audit.json"))
write.csv(data.frame(input=basename(inputs),md5=unname(tools::md5sum(inputs))),file.path(out,"input-checksums.csv"),row.names=FALSE)
