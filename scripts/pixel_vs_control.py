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
                     "font.size": 6, "pdf.fonttype": 42})
FW, FH = 3.33, 1.85
fig = plt.figure(figsize=(FW, FH))
L, W, G = 0.075, 0.172, 0.012
H = W * FW / FH                       # square panels
y1, y2 = 0.600, 0.170                 # bottom of pixel row / token row
blank = np.full((224, 224, 3), 0.95)
for i, (t, pix, dev, lab) in enumerate(cols):
    x = L + i * (W + G)
    a0 = fig.add_axes([x, y1, W, H]); a1 = fig.add_axes([x, y2, W, H])
    a0.imshow(pix if pix is not None else blank)
    if pix is None:
        a0.text(0.5, 0.5, "no image\nsent", ha="center", va="center", transform=a0.transAxes,
                fontsize=5.6, color="#666666")
    if dev is not None:
        a1.imshow(overlay(dev), interpolation="nearest")
    else:
        a1.axis("off")
    for ax in (a0, a1):
        ax.set_xticks([]); ax.set_yticks([])
        for s_ in ax.spines.values(): s_.set_linewidth(0.4)
    a0.set_title(t, fontsize=6.4, pad=1.5, weight="bold" if t == "Ours" else "normal")
    if lab[0]:
        a0.text(0.5, -0.04, lab[0] if pix is None else f"{lab[0]}\n{lab[1]}", transform=a0.transAxes, ha="center", va="top",
                fontsize=5.5, linespacing=1.1)
    if dev is not None:
        a1.text(0.5, -0.04, f"mean {dev.mean():.3f}\n{lab[2]}", transform=a1.transAxes, ha="center", va="top",
                fontsize=5.5, linespacing=1.1, color="#B8352A" if lab[2] == "0/480" else "#222222")
fig.text(0.035, y1 + H / 2, "Pixels", rotation=90, ha="center", va="center", fontsize=6.2)
fig.text(0.035, y2 + H / 2, "Policy tokens", rotation=90, ha="center", va="center", fontsize=6.2)
cax = fig.add_axes([L + W * 0.45, y2 + 0.02, W * 0.12, H - 0.04])
cb = fig.colorbar(ScalarMappable(Normalize(0, VMAX), cmap), cax=cax, ticks=[0, 0.05, 0.10])
cb.ax.tick_params(labelsize=5.2, width=0.3, length=1.5, pad=1); cb.outline.set_linewidth(0.3)
cax.yaxis.set_label_position("left")
cb.set_label("1 $-$ cos", fontsize=5.6, labelpad=1.5)
fig.savefig("pixel-vs-control.pdf")
fig.savefig("pixel-vs-control.png", dpi=300)
