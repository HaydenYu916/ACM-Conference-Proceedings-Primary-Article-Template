# Figure 1: pixel fidelity vs. control fidelity.
# Data: ~/Desktop/Mobisys/paper_fig1/heat_fig1.npz (RoboCasa episode 165, 24 uploads x 3 cameras),
# exported on the A100 host. Shown: upload index 18 (median all-camera H.264 deviation), third-person left view.
# Deviation = 1 - cos between each post-projection pi0.5 token (16x16 grid) and its clean counterpart.
import sys, numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
npz = sys.argv[1] if len(sys.argv) > 1 else "heat_fig1.npz"
d = np.load(npz)
U, V, VMAX = 18, 0, 0.10
orig, h264 = d["u8"][U, V], d["h264"][U, V]
dev_h, dev_o = d["dev_h264"][U, V], d["dev_ours"][U, V]
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 6.5, "pdf.fonttype": 42})
cmap = plt.get_cmap("YlOrRd")
def overlay(img, dev):
    g = img.astype(float).mean(-1, keepdims=True) / 255.0          # greyscale context
    base = 0.55 + 0.45 * g                                           # lightened
    up = np.kron(np.clip(dev / VMAX, 0, 1), np.ones((14, 14)))       # 16x16 -> 224x224, nearest
    col = cmap(up)[..., :3]
    a = (0.15 + 0.85 * up)[..., None]
    return np.clip((1 - a) * base + a * col, 0, 1)
panels = [(orig, "Original", "Uncompressed\n291/480"),
          (h264, "H.264, 3.0 KB", "PSNR 33.0 dB\n0/480"),
          (overlay(orig, dev_h), "H.264", f"mean {dev_h.mean():.3f}"),
          (overlay(orig, dev_o), "Ours, 1.14 KB", f"mean {dev_o.mean():.3f}\n295/480")]
fig = plt.figure(figsize=(3.33, 1.30))
w, gap, left, bottom, h = 0.205, 0.012, 0.005, 0.25, 0.555
for i, (im, title, sub) in enumerate(panels):
    ax = fig.add_axes([left + i * (w + gap), bottom, w, h])
    ax.imshow(im, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_linewidth(0.4)
    ax.set_title(title, fontsize=6.5, pad=1.5)
    ax.text(0.5, -0.04, sub, transform=ax.transAxes, ha="center", va="top", fontsize=6.2, linespacing=1.1)
top = bottom + h + 0.13
fig.text(left + (2 * w + gap) / 2, top, "Pixels", ha="center", fontsize=6.8, weight="bold")
fig.text(left + 2 * (w + gap) + (2 * w + gap) / 2, top, "Policy tokens (deviation from clean)",
         ha="center", fontsize=6.8, weight="bold")
x_sep = left + 2 * (w + gap) - gap / 2
fig.add_artist(plt.Line2D([x_sep, x_sep], [0.04, 0.98], color="#999999", lw=0.5, ls=(0, (2, 1.5))))
cax = fig.add_axes([left + 4 * (w + gap) + 0.004, bottom, 0.018, h])
cb = fig.colorbar(ScalarMappable(Normalize(0, VMAX), cmap=cmap), cax=cax, ticks=[0, 0.05, 0.10], extend="max")
cb.ax.tick_params(labelsize=5.5, width=0.4, length=1.5, pad=1); cb.outline.set_linewidth(0.4)
cb.set_label(r"$1-\cos$", fontsize=6, labelpad=1)
fig.savefig("pixel-vs-control.pdf"); fig.savefig("pixel-vs-control.png", dpi=300)
print("ratio (this episode, all uploads and cameras):", float(d["dev_h264"].mean() / d["dev_ours"].mean()))
