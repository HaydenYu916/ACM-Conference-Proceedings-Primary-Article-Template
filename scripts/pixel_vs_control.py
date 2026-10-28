# Sec. 2.3 figure: pixel fidelity vs. what the policy sees (RoboCasa, pi0.5, episode 165, upload 18, left view).
# Data: paper_fig1/heat_fig1.npz (original, H.264 CRF34, ours) and paper_fig1/heat_fig1_more.npz
# (JPEG q20, SPARC q1 checkpoint of Table R1), both exported on the A100 host with the same pi0.5 checkpoint.
# Deviation = 1 - cos between each post-projection pi0.5 token (16x16 grid) and its clean counterpart.
# Closed-loop counts: results/rc_tables.md, Table R1 (480 paired episodes); JPEG was not run closed loop.
import sys, numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
a = np.load(sys.argv[1] if len(sys.argv) > 1 else "heat_fig1.npz")
b = np.load(sys.argv[2] if len(sys.argv) > 2 else "heat_fig1_more.npz")
U, V, VMAX = 18, 0, 0.10
orig = a["u8"][U, V]
def psnr(x, y):
    return 10 * np.log10(255.0 ** 2 / ((x.astype(float) - y.astype(float)) ** 2).mean())
cmap = plt.get_cmap("YlOrRd")
def overlay(dev):
    g = orig.astype(float).mean(-1, keepdims=True) / 255.0
    base = 0.55 + 0.45 * g
    up = np.kron(np.clip(dev / VMAX, 0, 1), np.ones((14, 14)))
    a_ = (0.15 + 0.85 * up)[..., None]
    return np.clip((1 - a_) * base + a_ * cmap(up)[..., :3], 0, 1)
cols = [  # title, pixels, deviation, label lines
    ("Original", orig, None, ["", "", ""]),
    ("H.264", a["h264"][U, V], a["dev_h264"][U, V],
     [f"{a['h264_bytes'][U]/1000:.2f} KB", f"{psnr(orig, a['h264'][U, V]):.1f} dB", "0/480"]),
    ("JPEG", b["jpeg"][U, V], b["dev_jpeg"][U, V],
     [f"{b['jpeg_bytes'][U]/1000:.2f} KB", f"{psnr(orig, b['jpeg'][U, V]):.1f} dB", "not run"]),
    ("SPARC", b["sparc"][U, V], b["dev_sparc"][U, V],
     [f"{b['sparc_bytes'][U]/1000:.2f} KB", f"{psnr(orig, b['sparc'][U, V]):.1f} dB", "277/480"]),
    ("Ours", None, a["dev_ours"][U, V],
     [f"{a['ours_bytes'][U]/1000:.2f} KB", "no image", "295/480"]),
]
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 7, "pdf.fonttype": 42})
# Full-width figure (figure*): two rows x five columns, colour bar on the far right.
P, GAP = 0.94, 0.10
LEFT = (7.0 - (0.30 + 5 * P + 4 * GAP + 0.62)) / 2 + 0.30
FW, FH = 7.0, 0.20 + P + 0.30 + P + 0.22
TOP, ROWGAP = 0.20, 0.30                  # title space, space for labels under row 1
def ax_at(xi, yi):                        # xi, yi: inches from left / top of the panel's top-left corner
    return fig.add_axes([xi / FW, 1 - (yi + P) / FH, P / FW, P / FH])
fig = plt.figure(figsize=(FW, FH))
blank = np.full((224, 224, 3), 0.95)
y_row1, y_row2 = TOP, TOP + P + ROWGAP
for i, (t, pix, dev, lab) in enumerate(cols):
    x = LEFT + i * (P + GAP)
    a0, a1 = ax_at(x, y_row1), ax_at(x, y_row2)
    a0.imshow(pix if pix is not None else blank)
    if pix is None:
        a0.text(0.5, 0.5, "no image\nsent", ha="center", va="center", transform=a0.transAxes,
                fontsize=7, color="#666666")
    if dev is not None:
        a1.imshow(overlay(dev), interpolation="nearest")
    else:
        a1.axis("off")
    for ax in (a0, a1):
        ax.set_xticks([]); ax.set_yticks([])
        for s_ in ax.spines.values(): s_.set_linewidth(0.5)
    a0.set_title(t, fontsize=8, pad=2, weight="bold" if t == "Ours" else "normal")
    if lab[0]:
        a0.text(0.5, -0.04, lab[0] if pix is None else f"{lab[0]} · {lab[1]}", transform=a0.transAxes,
                ha="center", va="top", fontsize=7)
    if dev is not None:
        a1.text(0.5, -0.04, f"mean {dev.mean():.3f}", transform=a1.transAxes, ha="center",
                va="top", fontsize=7)
fig.text((LEFT - 0.22) / FW, 1 - (y_row1 + P / 2) / FH, "Pixels", rotation=90, ha="center", va="center", fontsize=8)
fig.text((LEFT - 0.22) / FW, 1 - (y_row2 + P / 2) / FH, "Policy tokens", rotation=90, ha="center", va="center",
         fontsize=8)
xc = LEFT + 5 * (P + GAP) + 0.02
cax = fig.add_axes([xc / FW, 1 - (y_row2 + P) / FH, 0.10 / FW, P / FH])
cb = fig.colorbar(ScalarMappable(Normalize(0, VMAX), cmap), cax=cax, ticks=[0, 0.05, 0.10])
cb.ax.tick_params(labelsize=7, width=0.4, length=2, pad=1.5); cb.outline.set_linewidth(0.4)
cb.set_label("1 $-$ cos", fontsize=7.5, labelpad=2)
fig.savefig("pixel-vs-control.pdf")
fig.savefig("pixel-vs-control.png", dpi=200)
