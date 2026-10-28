# Per-request latency breakdown on the SO-101 deployment (Orin edge -> real link -> A40 cloud, pi0.5).
# Source: paper_notes/realrobot_latency_table.md (p50 over 195 uploads).
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 7.5, "pdf.fonttype": 42, "axes.linewidth": 0.5})
rows = [  # label, bytes, edge, network, cloud_total, e2e
    ("Uncompressed", "220.5 KB", 0.0, 189.8, 203.2, 397.1),
    ("JPEG q90",     "15.2 KB",  1.3, 58.4, 222.2, 282.3),
    ("H.264 CRF30",  "1.2 KB",   2.9, 29.8, 240.3, 272.4),
]
c_edge, c_net, c_cloud = "#E69F00", "#56B4E9", "#7F7F7F"   # Okabe-Ito orange / sky blue, grey
fig, ax = plt.subplots(figsize=(3.3, 1.25))
for i, (lab, b, e, n, c, tot) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, e, color=c_edge, height=0.55, edgecolor="white", linewidth=0.4)
    ax.barh(y, n, left=e, color=c_net, height=0.55, edgecolor="white", linewidth=0.4, hatch="////")
    ax.barh(y, c, left=e + n, color=c_cloud, height=0.55, edgecolor="white", linewidth=0.4)
    ax.text(e + n + c + 6, y, f"{tot:.0f} ms", va="center", fontsize=7)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([f"{r[0]}\n({r[1]})" for r in reversed(rows)], fontsize=7)
ax.set_xlim(0, 450)
ax.set_xlabel("Median request latency (ms)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(width=0.5, length=2)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c_edge, label="Edge"),
                   Patch(facecolor=c_net, edgecolor="white", hatch="////", label="Network"),
                   Patch(color=c_cloud, label="Cloud")],
          ncol=3, frameon=False, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, 1.0),
          handlelength=1.2, columnspacing=1.0)
fig.tight_layout(pad=0.2)
fig.savefig("request-breakdown.pdf")
fig.savefig("request-breakdown.png", dpi=250)
