"""Team figure style guide (M2 cross-cutting duty).

Every notebook calls `apply_style()` once and saves figures with `save_fig()`,
so all exported figures share fonts, colours, size and resolution.
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

# One standard size for slide figures (16:9 friendly) and one for square panels.
FIGSIZE = (10, 5.625)
FIGSIZE_SQUARE = (7, 7)
DPI = 200

# Colours: colour-blind-safe (Okabe-Ito based).
STATE_COLORS = {
    "Gujarat": "#E69F00",
    "Odisha": "#0072B2",
    "West Bengal": "#009E73",
}
POLLUTANT_COLORS = {
    "SO2": "#CC79A7",
    "NO2": "#D55E00",
    "PM10": "#56B4E9",
    "PM25": "#000000",
}
SEASON_COLORS = {
    "Winter": "#0072B2",
    "Summer": "#E69F00",
    "Monsoon": "#009E73",
    "Post-monsoon": "#CC79A7",
}
ACCENT = "#D55E00"
NEUTRAL = "#7F7F7F"
SEQ_CMAP = "viridis"
DIV_CMAP = "RdBu_r"

LABELS = {
    "SO2": "SO$_2$ (µg/m³)",
    "NO2": "NO$_2$ (µg/m³)",
    "PM10": "PM$_{10}$ (µg/m³)",
    "PM25": "PM$_{2.5}$ (µg/m³)",
    "AQI": "AQI (NAQI scale)",
}


def apply_style():
    mpl.rcParams.update({
        "figure.figsize": FIGSIZE,
        "figure.dpi": 100,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "-",
    })


def save_fig(fig, name):
    """Save a figure as PNG into figures/ with the team settings."""
    FIG_DIR.mkdir(exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path)
    return path


def save_table(df, name, index=False):
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / f"{name}.csv"
    df.to_csv(path, index=index)
    return path
