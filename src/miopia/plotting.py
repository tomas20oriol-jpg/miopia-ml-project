"""Shared figure style: one colour per class everywhere, colour-blind safe, 300 dpi.

Colours are Okabe-Ito (Wong 2011, Nature Methods 8:441), in a validated order. Continuous
scales use viridis; a diverging scale (`DIVERGING_CMAP`) only around a meaningful centre.
"""

import matplotlib.pyplot as plt

from miopia.config import FIGURES

BLUE, VERMILLION, GREEN, ORANGE, PURPLE, SKY_BLUE = (
    "#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9")
CATEGORICAL = [BLUE, VERMILLION, GREEN, ORANGE, PURPLE, SKY_BLUE]

MISSING_GRAY = "#999999"  # neutral colour for "missing" / "other"; always add a label or marker

# Colour per class, per task. Myopia magna is always green and the control class always blue,
# so a reader comparing figures from different tasks never sees one group in two colours.
CLASS_COLORS = {
    "M": {"NO": BLUE, "SI": VERMILLION},
    "MM": {"NO": BLUE, "SI": GREEN},
    "Combo": {"C": BLUE, "M": VERMILLION, "MM": GREEN},
    "DCombo": {"C": BLUE, "M1": VERMILLION, "M2": ORANGE, "MM": GREEN},
}
# Second encoding for DCombo (4 classes, and orange has low contrast on white).
CLASS_MARKERS = {"C": "o", "M1": "s", "M2": "^", "MM": "D"}

SEQUENTIAL_CMAP = "viridis"
DIVERGING_CMAP = "RdBu_r"


def set_style() -> None:
    """Apply the project style to matplotlib (call once, in the setup cell)."""
    plt.rcParams.update({
        "figure.dpi": 110,           # on-screen size in the notebook
        "savefig.dpi": 300,
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "axes.prop_cycle": plt.cycler(color=CATEGORICAL),
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "legend.frameon": False,
    })


def save_fig(fig, name: str) -> None:
    """Save `fig` to `reports/figures/<name>.png` (300 dpi, white, tight)."""
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{name}.png")
