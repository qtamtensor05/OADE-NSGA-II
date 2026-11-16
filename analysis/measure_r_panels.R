# Measure the final rendered viewports: converting unresolved gtable null units
# outside their layout yields zero-sized boxes on the current R/patchwork stack.
write_patchwork_panel_layout <- function(plot, manifest_path, width_in, height_in,
    panel_ids = NULL, row_groups = NULL, column_groups = NULL, exemptions = list()) {
  grob <- patchwork::patchworkGrob(plot)
  rows <- .nature_alignment_panel_rows(grob)
  if (is.null(panel_ids)) panel_ids <- letters[seq_len(nrow(rows))]
  probe <- tempfile(fileext = ".pdf")
  grDevices::cairo_pdf(probe, width = width_in, height = height_in, family = "sans")
  on.exit({dev.off(); unlink(probe)}, add = TRUE)
  grid::grid.newpage(); grid::grid.draw(grob); grid::grid.force()
  panels <- lapply(seq_len(nrow(rows)), function(i) {
    r <- rows[i, ]
    vp <- paste0(r$name, ".", r$t, "-", r$l, "-", r$b, "-", r$r)
    grid::seekViewport(vp)
    lo <- grid::deviceLoc(grid::unit(0, "npc"), grid::unit(0, "npc"), valueOnly = TRUE)
    hi <- grid::deviceLoc(grid::unit(1, "npc"), grid::unit(1, "npc"), valueOnly = TRUE)
    grid::upViewport(0)
    list(id = panel_ids[i], bbox_pt = c(lo$x, lo$y, hi$x, hi$y) * 72,
      grid_id = "patchwork-grid-1", row_start = r$t - 1L, row_stop = r$b,
      col_start = r$l - 1L, col_stop = r$r)
  })
  manifest <- list(schema_version = 1L, backend = "r-patchwork",
    figure = list(width_pt = width_in * 72, height_pt = height_in * 72),
    panels = panels, exemptions = exemptions)
  if (!is.null(row_groups)) manifest$row_groups <- row_groups
  if (!is.null(column_groups)) manifest$column_groups <- column_groups
  jsonlite::write_json(manifest, manifest_path, auto_unbox = TRUE, pretty = TRUE, digits = NA)
  invisible(manifest)
}
