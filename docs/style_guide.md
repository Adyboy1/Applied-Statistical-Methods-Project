# Figure style guide (M2)

Implemented in `src/style.py`. Every notebook starts with `apply_style()` and saves figures with `save_fig(fig, name)`.

| Setting | Value |
|---|---|
| Slide figure size | 10 × 5.625 in (16:9) |
| Square panel size | 7 × 7 in |
| Export | PNG, 200 dpi, tight bounding box, saved to `figures/` |
| Font | DejaVu Sans; title 14 bold, axis labels 12, ticks 10, legend 10 |
| Axes | no top/right spines, light grid (alpha 0.3) |
| Units | always in axis labels, e.g. `PM2.5 (µg/m³)` |

## Colours (colour-blind safe, Okabe–Ito)

| Group | Colour |
|---|---|
| Gujarat | `#E69F00` orange |
| Odisha | `#0072B2` blue |
| West Bengal | `#009E73` green |
| Winter / Summer / Monsoon / Post-monsoon | `#0072B2` / `#E69F00` / `#009E73` / `#CC79A7` |
| SO2 / NO2 / PM10 / PM2.5 | `#CC79A7` / `#D55E00` / `#56B4E9` / `#000000` |
| Highlight / reference lines | `#D55E00` |
| Heatmaps | `viridis` (sequential), `RdBu_r` (correlations, centred at 0) |

## Rules

- One message per figure; the title states the finding where possible.
- The same state always has the same colour in every figure.
- Order categories the same way everywhere: states alphabetical; seasons Winter → Summer → Monsoon → Post-monsoon.
- File names: `<module>_<content>.png`, e.g. `m2_boxplot_pm25_by_city.png`.
