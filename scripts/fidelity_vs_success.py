# Sec. 2.3 figure: frames that look the same vs. closed-loop success (RoboCasa, pi0.5, 480 paired episodes).
# Frames: paper_fig1/heat_fig1.npz (episode 165, upload 18, left third-person view).
# Success counts: results/rc_tables.md, Table R1 (fair protocol, same machine).
import sys, numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
d = np.load(sys.argv[1] if len(sys.argv) > 1 else "heat_fig1.npz")
U, V = 18, 0
orig, h264, psnr = d["u8"][U, V], d["h264"][U, V], d["psnr"][U, V]
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 6.5, "pdf.fonttype": 42, "axes.linewidth": 0.5})
fig = plt.figure(figsize=(3.33, 1.30))
w, h, b = 0.200, 0.60, 0.20
for i, (im, title, sub) in enumerate([(orig, "Original", ""),
                                      (h264, "H.264, 3.0 KB", f"PSNR {psnr:.1f} dB")]):
    ax = fig.add_axes([0.005 + i * (w + 0.012), b, w, h])
    ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_linewidth(0.4)
    ax.set_title(title, fontsize=6.6, pad=1.5)
    ax.text(0.5, -0.04, sub, transform=ax.transAxes, ha="center", va="top", fontsize=6.2)
rows = [("Uncompressed$^{*}$", 291, "#9A9A9A"),
        ("SPARC, 0.97 KB", 277, "#D4AC2E"),
        ("H.264, 3.0 KB", 0, "#C2507A"),
        ("H.264, 1.1 KB", 4, "#C2507A")]
ax = fig.add_axes([0.715, b, 0.255, h])
for k, (lab, v, c) in enumerate(rows):
    y = len(rows) - 1 - k
    ax.barh(y, v, color=c, height=0.6)
    ax.text(v + 6, y, f"{v}", va="center", fontsize=6.2,
            color="#B8352A" if v < 10 else "#333333", weight="bold" if v < 10 else "normal")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=6.2)
ax.set_xlim(0, 480); ax.set_xticks([0, 240, 480])
ax.set_xlabel("Successes / 480", fontsize=6.2, labelpad=1)
ax.set_title("RoboCasa, $\\pi_{0.5}$", fontsize=6.6, pad=1.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(width=0.4, length=2, pad=1)
fig.savefig("fidelity-vs-success.pdf")
fig.savefig("fidelity-vs-success.png", dpi=300)
