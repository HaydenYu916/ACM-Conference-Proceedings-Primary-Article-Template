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
c = np.load(sys.argv[3] if len(sys.argv) > 3 else "codes_fig1.npz")   # our transmitted integer codes
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
                     "font.size": 6, "pdf.fonttype": 42})
# Single-column figure: four codecs x two rows, colour bar on the far right (original frame omitted;
# PSNR under each decoded frame states its distance from it).
cols = cols[1:]
P, GAP, LEFT = 0.655, 0.045, 0.20
FW = 3.33
TOP, ROWGAP, BOT = 0.15, 0.27, 0.13
FH = TOP + P + ROWGAP + P + BOT
def ax_at(xi, yi):
    return fig.add_axes([xi / FW, 1 - (yi + P) / FH, P / FW, P / FH])
fig = plt.figure(figsize=(FW, FH))
blank = np.full((224, 224, 3), 0.95)
y_row1, y_row2 = TOP, TOP + P + ROWGAP
for i, (t, pix, dev, lab) in enumerate(cols):
    x = LEFT + i * (P + GAP)
    a0, a1 = ax_at(x, y_row1), ax_at(x, y_row2)
    if pix is not None:
        a0.imshow(pix)
    else:   # ours: no image exists; show how many non-zero code symbols each token carries
        nz = (c["codes_q"][U, V] != 0).sum(-1).reshape(16, 16)
        a0.imshow(nz, cmap="Blues", vmin=0, vmax=8, interpolation="nearest")
    a1.imshow(overlay(dev), interpolation="nearest")
    for ax in (a0, a1):
        ax.set_xticks([]); ax.set_yticks([])
        for s_ in ax.spines.values(): s_.set_linewidth(0.4)
    a0.set_title(t, fontsize=6.6, pad=1.5, weight="bold" if t == "Ours" else "normal")
    a0.text(0.5, -0.03, f"{lab[0]}\ncodes" if pix is None else f"{lab[0]}\n{lab[1]}", transform=a0.transAxes,
            ha="center", va="top", fontsize=5.8, linespacing=1.1)
    a1.text(0.5, -0.03, f"mean {dev.mean():.3f}", transform=a1.transAxes, ha="center", va="top", fontsize=5.8)
fig.text(0.07 / FW, 1 - (y_row1 + P / 2) / FH, "Received", rotation=90, ha="center", va="center", fontsize=6.4)
fig.text(0.07 / FW, 1 - (y_row2 + P / 2) / FH, "Policy tokens", rotation=90, ha="center", va="center",
         fontsize=6.4)
xc = LEFT + 4 * (P + GAP) + 0.0
cax = fig.add_axes([xc / FW, 1 - (y_row2 + P) / FH, 0.07 / FW, P / FH])
cb = fig.colorbar(ScalarMappable(Normalize(0, VMAX), cmap), cax=cax, ticks=[0, 0.05, 0.10])
cb.ax.tick_params(labelsize=5.6, width=0.3, length=1.5, pad=1); cb.outline.set_linewidth(0.3)
cax.set_title("1 $-$ cos", fontsize=5.8, pad=5)
fig.savefig("pixel-vs-control.pdf")
fig.savefig("pixel-vs-control.png", dpi=300)
