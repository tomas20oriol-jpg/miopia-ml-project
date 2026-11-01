"""Draw the simplified figures used on the slides, from values printed in the executed notebooks.

Run from the project root with the project venv. Sources: notebook 04 cells with the model scores, the final table
and the group table; notebook 05 cells with the confusion matrices, importances and expected accuracy.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from miopia.config import FIGURES
from miopia.plotting import BLUE, CLASS_COLORS, MISSING_GRAY, VERMILLION, set_style

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
set_style()
plt.rcParams.update({"font.size": 14, "axes.titlesize": 15, "axes.labelsize": 14})
TARGETS = ["M", "MM", "Combo", "DCombo"]
INK = "#16323F"


def save(fig, name):
    fig.savefig(OUT / f"{name}.png")
    plt.close(fig)


# Balanced accuracy of each model (notebook 04, section 4)
MODELS = ["Logistic\naxial only", "Logistic\nall 33", "Logistic\ntuned", "SVM", "Random\nforest", "XGBoost"]
SCORES = {"M": [0.77, 0.77, 0.75, 0.71, 0.73, 0.73], "MM": [0.81, 0.79, 0.77, 0.75, 0.61, 0.65],
          "Combo": [0.71, 0.68, 0.65, 0.66, 0.73, 0.71], "DCombo": [0.60, 0.51, 0.49, 0.49, 0.59, 0.55]}
MAJORITY_BA = {"M": 0.5, "MM": 0.5, "Combo": 0.33, "DCombo": 0.25}
fig, axes = plt.subplots(1, 4, figsize=(13, 4.8), sharey=True, sharex=True)
for ax, target in zip(axes, TARGETS):
    values = SCORES[target]
    y = np.arange(len(MODELS))
    ax.hlines(y, MAJORITY_BA[target], values, color="0.85", lw=2, zorder=1)
    ax.scatter(values[1:], y[1:], s=110, color=BLUE, zorder=2)
    ax.scatter(values[0], y[0], s=170, color=VERMILLION, zorder=3)
    ax.axvline(MAJORITY_BA[target], color="0.35", ls="--", lw=1.2)
    for v, yy in zip(values, y):
        ax.text(v + 0.025, yy, f"{v:.2f}", va="center", fontsize=12)
    ax.set_title(target, fontweight="bold")
    ax.set_xlim(0.2, 1.0)
axes[0].set_yticks(range(len(MODELS)), MODELS)
axes[0].invert_yaxis()
fig.supxlabel("Mean balanced accuracy in cross-validation (dashed line: majority class)", fontsize=13)
fig.tight_layout()
save(fig, "models")

# Baseline to final model (notebook 04, final table)
BASE = {"Balanced accuracy": [0.77, 0.81, 0.71, 0.60], "Accuracy": [0.77, 0.82, 0.65, 0.56]}
FINAL = {"Balanced accuracy": [0.80, 0.89, 0.77, 0.65], "Accuracy": [0.80, 0.97, 0.75, 0.63]}
fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.6), sharey=True)
for ax, metric in zip(axes, BASE):
    y = np.arange(4)
    ax.hlines(y, BASE[metric], FINAL[metric], color="0.75", lw=3, zorder=1)
    ax.scatter(BASE[metric], y, s=130, color=VERMILLION, zorder=2, label="Logistic, axial length only")
    ax.scatter(FINAL[metric], y, s=130, color=BLUE, zorder=2, label="Final model")
    for b, f, yy in zip(BASE[metric], FINAL[metric], y):
        ax.text(f + 0.02, yy, f"{f:.2f}", va="center", fontsize=13, fontweight="bold")
        ax.text(b - 0.02, yy, f"{b:.2f}", va="center", ha="right", fontsize=12, color="0.35")
    ax.set_xlim(0.42, 1.08)
    ax.set_title(metric, fontweight="bold")
axes[0].set_yticks(range(4), TARGETS)
axes[0].invert_yaxis()
fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", ncol=2, frameon=False, fontsize=12)
fig.tight_layout(rect=(0, 0.08, 1, 1))
save(fig, "results")

# Optimism check (notebook 04, section 11)
GROUPS = ["M", "MM", "DCombo"]
fig, ax = plt.subplots(figsize=(7.4, 3.9))
series = {"Axial length alone": ([0.77, 0.81, 0.59], VERMILLION, "o"), "Repeating all the selection": ([0.79, 0.82, 0.59], "#E69F00", "D"),
          "Notebook score, final model": ([0.80, 0.89, 0.65], BLUE, "s")}
for offset, (label, (values, color, marker)) in zip([-0.14, 0, 0.14], series.items()):
    ax.scatter(values, np.arange(3) + offset, s=170, color=color, marker=marker, label=label, zorder=3, alpha=0.9)
for i, (low, high) in enumerate([(0.77, 0.80), (0.81, 0.89), (0.59, 0.65)]):
    ax.plot([low, high], [i - 0.14, i + 0.14], color="0.8", lw=3, zorder=1)
ax.set_yticks(range(3), GROUPS)
ax.invert_yaxis()
ax.set_ylim(2.5, -0.5)
ax.set_xlim(0.55, 0.92)
ax.set_xlabel("Balanced accuracy")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1, frameon=False, fontsize=12)
save(fig, "optimism")

# The eight inconsistent students (notebook 04, section 8)
LABELS = ["MM = SI\n(n = 10)", "The 8", "Combo = M\n(n = 70)", "Combo = C\n(n = 44)"]
COLORS = [CLASS_COLORS["Combo"]["MM"], VERMILLION, "0.45", "0.65"]
PANELS = {"Axial length (mm)": [26.35, 26.52, 24.47, 23.47], "Keratometry (D)": [43.40, 41.28, 43.55, 43.27], "Axial/corneal ratio": [3.39, 3.24, 3.16, 3.01]}
fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.3), sharey=True)
for ax, (title, values) in zip(axes, PANELS.items()):
    ax.scatter(values, range(4), s=190, color=COLORS, zorder=3)
    span = max(values) - min(values)
    ax.set_xlim(min(values) - 0.22 * span, max(values) + 0.34 * span)
    for v, y in zip(values, range(4)):
        ax.text(v + 0.09 * span, y, f"{v:.2f}", va="center", fontsize=13)
    ax.set_title(title, fontweight="bold")
    ax.set_ylim(3.5, -0.5)
axes[0].set_yticks(range(4), LABELS)
fig.tight_layout()
save(fig, "eight_students")

# Errors and what the models use (notebook 05, sections 3 and 4)
MATRIX = np.array([[0.72, 0.25, 0.02, 0.00], [0.30, 0.49, 0.21, 0.01], [0.00, 0.22, 0.59, 0.19], [0.06, 0.00, 0.14, 0.81]])
CLASSES = ["C", "M1", "M2", "MM"]
fig, ax = plt.subplots(figsize=(4.9, 4.7))
ax.imshow(MATRIX, cmap="viridis", vmin=0, vmax=1)
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{MATRIX[i, j]:.2f}", ha="center", va="center", fontsize=15, color="0.1" if MATRIX[i, j] >= 0.5 else "white")
ax.set_xticks(range(4), CLASSES)
ax.set_yticks(range(4), CLASSES)
ax.set_xlabel("Predicted")
ax.set_ylabel("True class (rows sum to 1)")
ax.set_title("DCombo, validation students", fontweight="bold")
ax.spines[:].set_visible(False)
save(fig, "dcombo_errors")

IMPORTANCE = {"Axial length": 0.296, "Axial/corneal ratio": 0.129, "Nasal SD": 0.007, "Sport hours": 0.005, "Mother myopic": 0.003}
fig, ax = plt.subplots(figsize=(6.4, 3.0))
y = np.arange(len(IMPORTANCE))
values = list(IMPORTANCE.values())
ax.hlines(y, 0, values, color="0.8", lw=3)
ax.scatter(values, y, s=130, color=BLUE, zorder=3)
for v, yy in zip(values, y):
    ax.text(v + 0.012, yy, f"{v:.3f}", va="center", fontsize=13)
ax.set_yticks(y, list(IMPORTANCE))
ax.invert_yaxis()
ax.set_xlim(0, 0.36)
ax.set_xlabel("Drop in balanced accuracy when shuffled")
ax.set_title("Combo forest, top 5 of 34 features (means)", fontweight="bold")
save(fig, "importance")

# Expected accuracy on the test set (notebook 05, section 6)
CV = [0.80, 0.97, 0.75, 0.63]
WHOLE = [0.79, 0.92, 0.68, 0.57]
MAJORITY = [0.67, 0.92, 0.53, 0.33]
RANGES = [(15, 23), (21, 24), (14, 22), (11, 20)]
fig, ax = plt.subplots(figsize=(7.6, 4.2))
for i, (low, high) in enumerate(RANGES):
    ax.hlines(i, low / 24, high / 24, color="0.82", lw=9, zorder=1, label="95% sampling range, 24 students" if i == 0 else None)
ax.scatter(MAJORITY, range(4), marker="|", s=420, linewidths=3, color="0.25", zorder=2, label="Majority class")
ax.scatter(WHOLE, range(4), marker="D", s=120, color="#E69F00", zorder=3, label="Sober estimate")
ax.scatter(CV, range(4), s=130, color=BLUE, zorder=4, label="Optimistic estimate")
ax.set_yticks(range(4), TARGETS)
ax.invert_yaxis()
ax.set_xlim(0.25, 1.03)
ax.set_xlabel("Accuracy on the test set")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=12)
save(fig, "expected")

# The reviewed ratio figure, without its title because the slide states the message
ratio = Image.open(FIGURES / "04_ratio_by_class.png")
width, height = ratio.size
ratio.crop((0, int(height * 0.075), width, height)).save(OUT / "ratio.png")
print("saved", sorted(p.name for p in OUT.glob("*.png")))
