#!/usr/bin/env python3
"""Fig. 2 (system architecture), same visual language as Figure 1. Usage: arch.py OUT.html thumbs.json"""
import sys
exec(open(__file__.replace("arch.py", "helpers.py")).read())
W, H = 620, 808
SNOW = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6DB0EE" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:6px">'
        + "".join(f'<g transform="rotate({60*k} 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g>'
                  for k in range(6)) + '</svg>')
GREY = ("#F1F2F4", "#9AA1AB", "#2E3440")
C["grey"] = GREY

def region(x, y, w, h, bg, bd, label, icon=""):
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:{bg}; '
               f'border:1.5px solid {bd}; border-radius:18px"></div>')
    out.append(f'<div style="position:absolute; left:{x+14}px; top:{y+10}px; display:flex; gap:7px; align-items:center; '
               f'font-size:20px; line-height:22px; color:#3F4A5A; font-weight:700">{icon}<span>{label}</span></div>')

def pill(cx, cy, html, color=INK, bg="#FFFFFF", fs=18):
    out.append(f'<div style="position:absolute; left:{cx}px; top:{cy-14}px; transform:translateX(-50%); white-space:nowrap; '
               f'background:{bg}; border:1.6px solid {color}; border-radius:14px; padding:2px 12px; font-size:{fs}px; '
               f'line-height:22px; font-weight:600; color:{color}">{html}</div>')

def frame(x, y, s=58):
    for k, c in enumerate(["cam0", "cam2", "cam1"]):
        out.append(f'<img src="data:image/jpeg;base64,{TH[c]}" style="position:absolute; left:{x}px; top:{y+k*(s+6)}px; '
                   f'width:{s}px; height:{s}px; border-radius:4px; box-shadow:0 0 0 1.5px #8F8A80; object-fit:cover">')

# single-column layout: edge on top, cloud below (flow returns right-to-left), training underneath
NAVY, CARD, CARDB, INNER, INNERB, CELL = "#0D366B", "#DCEAFB", BLUE, "#F5F9FE", "#7FA9DD", "#A9CBF2"
def card(x, y, w, h, title, fs=19):
    for k in (2, 1):
        out.append(f'<div style="position:absolute; left:{x+5*k}px; top:{y+5*k}px; width:{w}px; height:{h}px; box-sizing:border-box; '
                   f'background:{CARD}; border:1.5px solid {CARDB}; border-radius:11px"></div>')
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; '
               f'background:{CARD}; border:1.8px solid {CARDB}; border-radius:11px"></div>')
    text(x, y + 6, w, title, fs, NAVY, 700, "center")
def inner(x, y, w, h, split):
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; '
               f'background:{INNER}; border:1.5px solid {INNERB}; border-radius:8px"></div>')
    out.append(f'<div style="position:absolute; left:{split}px; top:{y+7}px; width:0; height:{h-14}px; border-left:1.5px solid {INNERB}"></div>')
def cells(cx, y, n, w, h, gap=4):
    x0 = cx - (n * w + (n - 1) * gap) / 2
    for k in range(n):
        out.append(f'<div style="position:absolute; left:{x0+k*(w+gap)}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; '
                   f'background:{CELL}; border:1.3px solid {BLUE}; border-radius:3px"></div>')
def region2(x, y, w, h, bg, bd, label, icon):
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:{bg}; '
               f'border:1.5px solid {bd}; border-radius:16px"></div>')
    out.append(f'<div style="position:absolute; left:{x+12}px; top:{y+8}px; display:flex; gap:6px; align-items:center; '
               f'font-size:18px; line-height:20px; color:#3F4A5A; font-weight:700">{icon}<span>{label}</span></div>')

# ---------------- (a) deployment
text(6, 2, 600, "(a) Deployment", 20, "#1C1B19", 700)
region2(6, 30, 608, 248, "#F6F3EE", "#DCD5C9", "Edge (robot)", CHIP_ICON)
for k, c in enumerate(["cam0", "cam2", "cam1"]):
    out.append(f'<img src="data:image/jpeg;base64,{TH[c]}" style="position:absolute; left:18px; top:{66+k*54}px; '
               f'width:50px; height:50px; border-radius:4px; box-shadow:0 0 0 1.5px #8F8A80; object-fit:cover">')
FX, FY, FW, FH = 86, 62, 432, 128
card(FX, FY, FW, FH, "Jointly learned frontend")
IX, IY, IW, IH = FX + 12, FY + 34, FW - 24, 82
SPL = IX + 206
inner(IX, IY, IW, IH, SPL)
text(IX, IY + 7, SPL - IX, "Light vision encoder <i>s</i>", 18, NAVY, 700, "center")
cells((IX + SPL) / 2, IY + 44, 6, 18, 20)
text(SPL, IY + 7, IX + IW - SPL, "Feature codec", 18, NAVY, 700, "center")
text(SPL, IY + 29, IX + IW - SPL, "<i>h</i> &middot; <i>Q</i> &middot; rANS", 15, "#3F5E86", 600, "center")
cells((SPL + IX + IW) / 2, IY + 56, 4, 10, 10, 4)
ye = IY + IH // 2
poly([(68, ye), (FX - 1, ye)])
PB = SPL + 6
box(PB, 222, 172, 36, "previous codes <i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=16)
poly([(PB + 136, FY + FH + 11), (PB + 136, 221)], RET)        # store
poly([(PB + 36, 221), (PB + 36, FY + FH + 12)], RET)          # condition (inter uploads)

# bitstream down to the cloud
BXL = 566
poly([(FX + FW + 11, ye), (BXL, ye), (BXL, 337)], BLUE)
pill(BXL, 292, "bitstream", BLUE, fs=16)

# ---------------- cloud: token decoder on the right, flow back to the left
region2(6, 300, 608, 236, "#EEF2F7", "#C9D3DF", "Cloud", CLOUD_ICON)
TX, TY, TW, TCH = 382, 338, 214, 128
card(TX, TY, TW, TCH, "Token decoder")
TIX, TIY, TIW, TIH = TX + 12, TY + 34, TW - 24, 82
TSP = TIX + 84
inner(TIX, TIY, TIW, TIH, TSP)
text(TIX, TIY + 7, TSP - TIX, "rANS<br>decode", 16, NAVY, 700, "center")
cells((TIX + TSP) / 2, TIY + 56, 3, 10, 10, 4)
text(TSP, TIY + 7, TIX + TIW - TSP, "<i>g<sub>s</sub></i>", 20, NAVY, 700, "center")
cells((TSP + TIX + TIW) / 2, TIY + 44, 4, 18, 20)
yc2 = TIY + TIH // 2
box(TX + 20, 488, 172, 36, "previous codes <i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=16)
poly([(TX + 56, TY + TCH + 11), (TX + 56, 487)], RET)
poly([(TX + 156, 487), (TX + 156, TY + TCH + 12)], RET)
# policy tokens and the frozen policy
PTX = 316
for k in range(4):
    out.append(f'<div style="position:absolute; left:{PTX}px; top:{yc2-32+k*17}px; width:42px; height:11px; '
               f'border-radius:3px; background:#FDE2C8; border:1.4px solid #DC7A2E"></div>')
text(PTX - 20, yc2 + 38, 82, "policy<br>tokens", 14, "#5A2C05", 600, "center")
poly([(TX - 1, yc2), (PTX + 43, yc2)])
VX0, VX1 = 120, 286
box(VX0, yc2 - 44, VX1 - VX0, 88, SNOW + "VLA policy", "vla", fs=20)
poly([(PTX - 1, yc2), (VX1 + 1, yc2)])
box(VX0 + 12, 488, VX1 - VX0 - 24, 36, "language + state", "grey", fs=16)
poly([((VX0 + VX1) / 2, 487), ((VX0 + VX1) / 2, yc2 + 45)])
# action chunk back to the robot (left side)
poly([(VX0 - 1, yc2), (43, yc2), (43, 66 + 3 * 54 - 3)], RET, dash="8 4 2 4")
text(14, yc2 + 6, 100, "action<br>chunk", 15, "#55606E", 600, "center", "; font-style:italic")

# ---------------- (b) training
TY0 = 556
text(6, TY0, 610, "(b) Training (policy frozen; only the frontend is updated)", 19, "#1C1B19", 700)
r1, r2 = TY0 + 84, TY0 + 182
mid = (r1 + r2) // 2
out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:8px; top:{mid-24}px; '
           f'width:48px; height:48px; border-radius:4px; box-shadow:0 0 0 1.5px #8F8A80; object-fit:cover">')
EB0, EBW = 84, 150
box(EB0, r1 - 28, EBW, 56, SNOW + "Vision encoder<br>+ projection", "venc", fs=16)
box(EB0, r2 - 28, EBW, 56, "Jointly learned<br>frontend", "ours", fs=16)
poly([(56, mid), (68, mid), (68, r1), (EB0 - 1, r1)])
poly([(68, mid), (68, r2), (EB0 - 1, r2)])
TKX, VB0, VBW, ACX, SX = 290, 346, 92, 494, 588
pill(TKX, r1, "tokens <i>z</i>", fs=16)
pill(TKX, r2, "tokens <i>&#7825;</i>", BLUE, fs=16)
box(VB0, r1 - 24, VBW, 48, SNOW + "VLA", "vla", fs=17)
box(VB0, r2 - 24, VBW, 48, SNOW + "VLA", "vla", fs=17)
pill(ACX, r1, "actions <i>a</i>", fs=16)
pill(ACX, r2, "actions <i>&acirc;</i>", BLUE, fs=16)
poly([(EB0 + EBW, r1), (TKX - 44, r1)]); poly([(TKX + 44, r1), (VB0 - 1, r1)]); poly([(VB0 + VBW, r1), (ACX - 49, r1)])
poly([(EB0 + EBW, r2), (TKX - 44, r2)], BLUE); poly([(TKX + 44, r2), (VB0 - 1, r2)], BLUE); poly([(VB0 + VBW, r2), (ACX - 49, r2)], BLUE)
LBG, LBD, LTX = "#FFF1E4", PURPLE, "#7A3B0A"
def loss(cx, w, label):
    out.append(f'<div style="position:absolute; left:{cx-w/2}px; top:{mid-14}px; width:{w}px; height:28px; box-sizing:border-box; '
               f'background:{LBG}; border:1.6px solid {LBD}; border-radius:7px; display:flex; align-items:center; '
               f'justify-content:center; font-size:15px; font-weight:700; color:{LTX}; white-space:nowrap">{label}</div>')
ECX = EB0 + EBW // 2
loss(ECX, 80, "rate")
loss(TKX, 80, "token")
loss(ACX, 80, "action")
for x in (TKX, ACX):
    poly([(x, r1 + 14), (x, mid - 15)], RET, dash="4 3", head=False)
    poly([(x, r2 - 14), (x, mid + 15)], RET, dash="4 3", head=False)
poly([(ECX, r2 - 28), (ECX, mid + 15)], RET, dash="4 3", head=False)
poly([(ECX + 41, mid), (TKX - 42, mid)], LBD); poly([(TKX + 41, mid), (ACX - 42, mid)], LBD); poly([(ACX + 41, mid), (SX - 19, mid)], LBD)
out.append(f'<div style="position:absolute; left:{SX-18}px; top:{mid-18}px; width:36px; height:36px; box-sizing:border-box; '
           f'border-radius:50%; background:{LBG}; border:2px solid {LBD}; display:flex; align-items:center; '
           f'justify-content:center; font-size:21px; font-weight:700; color:{LTX}">&Sigma;</div>')
text(SX - 40, mid - 44, 80, "loss", 15, LTX, 700, "center")
poly([(SX, mid + 19), (SX, r2 + 46), (ECX, r2 + 46), (ECX, r2 + 29)], PURPLE, dash="6 4")
text(ECX + 20, r2 + 48, 360, "gradients update the frontend only", 15, PURPLE, 700, "center")
# legend
text(380, TY0 + 28, 100, SNOW + "frozen", 15, "#3F4A5A", 600)
out.append(f'<div style="position:absolute; left:470px; top:{TY0+31}px; width:22px; height:15px; border-radius:4px; '
           f'background:#D6E7FA; border:1.6px solid {BLUE}"></div>')
text(498, TY0 + 28, 90, "trained", 15, "#3F4A5A", 600)

out.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0; '
           f'width:{W}px; height:{H}px; overflow:visible; pointer-events:none">{"".join(g)}</svg>')
pills = [o for o in out if "translateX(-50%)" in o]
out = [o for o in out if "translateX(-50%)" not in o] + pills
body = "\n".join(out)
html = f"""<!doctype html><html><head><meta charset="utf-8"><script src="./support.js"></script></head><body><x-dc>
<helmet><link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>body{{margin:0}}</style></helmet>
<div style="position:relative; width:{W}px; height:{H}px; background:#FFFFFF; font-family:'Source Sans 3','Helvetica Neue',Arial,sans-serif; color:#1C1B19">
{body}
</div>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>class Component extends DCLogic {{ renderVals(){{return {{}};}} }}</script>
</x-dc></body></html>"""
open(sys.argv[1], "w").write(html)
print("ok", W, H)
