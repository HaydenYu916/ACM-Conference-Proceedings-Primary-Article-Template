# Figure 1: pixel fidelity vs. control fidelity (RoboCasa, episode 165, upload 18, third-person left view).
# Panels exported on the A100 host into ~/Desktop/Mobisys/paper_fig1/ (copy panel*.png next to this script to rebuild);
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 6.5, "pdf.fonttype": 42})
panels = [("panel1_original.png",  "Original",      "Uncompressed\n291/480"),
          ("panel2_h264crf34.png", "H.264, 3.0 KB", "PSNR 33.0 dB\n0/480"),
          ("panel3_dev_h264.png",  "H.264",         "mean 0.032"),
          ("panel4_dev_ours.png",  "Ours, 1.14 KB", "mean 0.006\n295/480")]
fig = plt.figure(figsize=(3.33, 1.30))
w, gap, left, bottom, h = 0.205, 0.012, 0.005, 0.25, 0.555
for i, (f, title, sub) in enumerate(panels):
    ax = fig.add_axes([left + i * (w + gap), bottom, w, h])
    ax.imshow(mpimg.imread(f)); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_linewidth(0.4)
    ax.set_title(title, fontsize=6.5, pad=1.5)
    ax.text(0.5, -0.04, sub, transform=ax.transAxes, ha="center", va="top", fontsize=6.2, linespacing=1.1)
# group headers
top = bottom + h + 0.13
fig.text(left + (2 * w + gap) / 2, top, "Pixels", ha="center", fontsize=6.8, weight="bold")
fig.text(left + 2 * (w + gap) + (2 * w + gap) / 2, top, "Policy tokens (deviation from clean)", ha="center",
         fontsize=6.8, weight="bold")
x_sep = left + 2 * (w + gap) - gap / 2
fig.add_artist(plt.Line2D([x_sep, x_sep], [0.04, 0.98], color="#999999", lw=0.5, ls=(0, (2, 1.5))))
cax = fig.add_axes([left + 4 * (w + gap) + 0.004, bottom, 0.018, h])
cb = fig.colorbar(ScalarMappable(Normalize(0, 0.144), cmap="inferno"), cax=cax, ticks=[0, 0.05, 0.10])
cb.ax.tick_params(labelsize=5.5, width=0.4, length=1.5, pad=1); cb.outline.set_linewidth(0.4)
cb.set_label(r"$1-\cos$", fontsize=6, labelpad=1)
fig.savefig("pixel-vs-control.pdf"); fig.savefig("pixel-vs-control.png", dpi=300)
