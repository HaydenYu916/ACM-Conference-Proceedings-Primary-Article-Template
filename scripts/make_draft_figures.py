"""Render first-draft figures from the supplied aggregate result tables.

Sources:
  ../paper_notes/libero_tables.md, Table B and CRF23 supplement
  ../paper_notes/realrobot_latency_table.md, block-checkpoint replay rows
These are plots of existing summaries, not recomputed raw-data estimates.
Run from the project folder with a Python environment containing matplotlib.
"""
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images"
PREVIEWS = ROOT / "build" / "figure-previews"
OUT.mkdir(exist_ok=True)
PREVIEWS.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
})
BLUE = "#416c8a"
GRAY = "#969696"


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(PREVIEWS / f"{stem}.png", dpi=220,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


# Difference = method minus reference, in percentage points.
names = ["Ours", "SPARC", "H.264 / CRF 23", "H.264 / CRF 30"]
diff = [-0.20, -0.80, -0.55, -1.10]
low = [-1.21, -1.91, -1.49, -2.11]
high = [0.81, 0.29, 0.39, -0.11]
fig, ax = plt.subplots(figsize=(3.35, 1.8))
for y, (d, lo, hi) in enumerate(zip(diff, low, high)):
    color = BLUE if y == 0 else "#555555"
    ax.errorbar(d, y, xerr=[[d - lo], [hi - d]], fmt="o",
                color=color, markersize=4, capsize=2.5, linewidth=1.1)
ax.axvline(0, color="#999999", linestyle="--", linewidth=0.7)
ax.set_yticks(range(len(names)), names)
ax.set_ylim(3.6, -0.6)
ax.set_xlim(-2.4, 1.0)
ax.set_xticks([-2, -1, 0, 1])
ax.set_xlabel("Success difference vs. reference (pp)")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#eeeeee", linewidth=0.5)
ax.set_axisbelow(True)
fig.tight_layout(pad=0.5)
save(fig, "libero-paired-differences")

# SPARC uses its task-specific block checkpoint in both layouts.
names = ["Raw", "JPEG q90", "H.264 / CRF 30",
         "SPARC / original", "SPARC / GPU", "Ours"]
median = [397.1, 282.3, 272.4, 856.3, 431.3, 228.4]
p95 = [815.6, 301.1, 285.9, 933.1, 438.0, 237.5]
fig, ax = plt.subplots(figsize=(3.35, 2.15))
ax.barh(range(len(names)), median, height=0.48,
        color=[BLUE if n == "Ours" else "#c5c5c5" for n in names])
ax.scatter(p95, range(len(names)), s=16, color="#333333", zorder=3)
ax.set_yticks(range(len(names)), names)
ax.set_ylim(5.65, -0.75)
ax.set_xlim(0, 1000)
ax.set_xticks([0, 250, 500, 750, 1000])
ax.set_xlabel("End-to-end request latency (ms)")
ax.grid(axis="x", color="#eeeeee", linewidth=0.5)
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.legend(handles=[
    Patch(facecolor="#c5c5c5", label="p50"),
    Line2D([0], [0], marker="o", color="none",
           markerfacecolor="#333333", markeredgecolor="#333333",
           markersize=4, label="p95"),
], loc="lower right", frameon=False, fontsize=7)
fig.tight_layout(pad=0.5)
save(fig, "replay-request-latency")
print("Rendered two summary figures (PDF + PNG).")
