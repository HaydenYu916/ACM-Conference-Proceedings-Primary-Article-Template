#!/usr/bin/env python3
"""System architecture, compact card style (after ActECC Fig. 3a).
Usage: arch.py OUT.html thumbs.json single|double"""
import sys
exec(open(__file__.replace("arch.py", "helpers.py")).read())
MODE = sys.argv[3]
SW, R = 1.7, 7
NAVY = "#0D366B"
SNOW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6DB0EE" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:4px">'
        + "".join(f'<g transform="rotate({60*k} 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g>'
                  for k in range(6)) + '</svg>')
C["grey"] = ("#F1F2F4", "#9AA1AB", "#2E3440")
PAL = {"ours": ("#DCEAFB", BLUE, "#F5F9FE", "#7FA9DD", "#A9CBF2"),
       "vla": ("#FDE6CF", "#DC7A2E", "#FFF6EC", "#E8A66B", "#FAD3AE")}

def div(x, y, w, h, style):
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; {style}"></div>')

def card(x, y, w, h, title, kind="ours", fs=15, icon=None, stack=True):
    bg, bd = PAL[kind][:2]
    if stack:
        for k in (2, 1):
            div(x + 4 * k, y + 4 * k, w, h, f"background:{bg}; border:1.4px solid {bd}; border-radius:9px")
    div(x, y, w, h, f"background:{bg}; border:1.7px solid {bd}; border-radius:9px")
    if title:
        text(x, y + 4, w, title, fs, NAVY if kind == "ours" else "#5A2C05", 700, "center")
    if icon:
        out.append(f'<div style="position:absolute; left:{x-12}px; top:{y-12}px; width:30px; height:30px; border-radius:50%; '
                   f'background:#FFFFFF; border:1.5px solid #9AA1AB; display:flex; align-items:center; justify-content:center">{icon}</div>')

def inner(x, y, w, h, split, kind="ours"):
    _, _, ib, ibd, _ = PAL[kind]
    div(x, y, w, h, f"background:{ib}; border:1.3px solid {ibd}; border-radius:6px")
    if split:
        div(split, y + 6, 0, h - 12, f"border-left:1.3px solid {ibd}")

def cells(cx, y, n, w, h, gap=3, kind="ours", fill=None, bd=None):
    x0 = cx - (n * w + (n - 1) * gap) / 2
    for k in range(n):
        div(x0 + k * (w + gap), y, w, h, f"background:{fill or PAL[kind][4]}; border:1.2px solid {bd or PAL[kind][1]}; border-radius:2px")

def label(x, y, w, html, fs=12.5, color="#55606E", align="center", italic=True):
    text(x, y, w, html, fs, color, 600, align, "; font-style:italic" if italic else "")

def pill(cx, cy, html, color=INK, fs=13):
    out.append(f'<div style="position:absolute; left:{cx}px; top:{cy-11}px; transform:translateX(-50%); white-space:nowrap; '
               f'background:#FFFFFF; border:1.4px solid {color}; border-radius:11px; padding:1px 8px; font-size:{fs}px; '
               f'line-height:18px; font-weight:600; color:{color}">{html}</div>')

ICON_CHIP = CHIP_ICON.replace('width="22" height="22"', 'width="18" height="18"')
ICON_CLOUD = CLOUD_ICON.replace('width="30" height="20"', 'width="22" height="15"')

# ------------------------------------------------------------------ (a) deployment, 470 x 384
def panel_a(ox, oy):
    text(ox, oy, 460, "(a) Deployment", 17, "#1C1B19", 700)
    X0, X1 = ox + 62, ox + 352
    CM = (X0 + X1) // 2
    # cameras
    for k, c in enumerate(["cam0", "cam2", "cam1"]):
        out.append(f'<img src="data:image/jpeg;base64,{TH[c]}" style="position:absolute; left:{ox}px; top:{oy+38+k*44}px; '
                   f'width:40px; height:40px; border-radius:3px; box-shadow:0 0 0 1.3px #8F8A80; object-fit:cover">')
    # edge card
    EY, EH = oy + 34, 98
    card(X0, EY, X1 - X0, EH, "Edge: jointly learned frontend", icon=ICON_CHIP)
    IY, IH = EY + 26, 62
    SP = X0 + 10 + 148
    inner(X0 + 10, IY, X1 - X0 - 20, IH, SP)
    text(X0 + 10, IY + 4, SP - X0 - 10, "Light vision encoder <i>s</i>", 13.5, NAVY, 700, "center")
    cells((X0 + 10 + SP) / 2, IY + 36, 6, 15, 15)
    text(SP, IY + 4, X1 - 10 - SP, "Feature codec", 13.5, NAVY, 700, "center")
    text(SP, IY + 21, X1 - 10 - SP, "<i>h</i> &middot; <i>Q</i> &middot; rANS", 12, "#3F5E86", 600, "center")
    cells((SP + X1 - 10) / 2, IY + 42, 4, 8, 8)
    ye = IY + IH // 2
    poly([(ox + 41, ye), (X0 - 1, ye)])
    # previous codes, edge
    def prev(yc):
        cells(ox + 421, yc - 6, 4, 13, 12, fill="#E4E7EB", bd="#8C949E")
        label(ox + 372, yc + 9, 100, "previous<br>codes <i>y</i><sub><i>t</i>&minus;1</sub>", 12, "#55606E", "center", False)
        poly([(X1 + 9, yc - 4), (ox + 390, yc - 4)], RET)
        poly([(ox + 390, yc + 4), (X1 + 10, yc + 4)], RET)
    prev(ye)
    # bitstream down to the cloud
    TY, TH_ = oy + 176, 98
    poly([(CM, EY + EH + 9), (CM, TY - 1)], BLUE)
    label(CM + 6, EY + EH + 14, 120, "bitstream", 13, BLUE, "left", False)
    # token decoder card
    card(X0, TY, X1 - X0, TH_, "Cloud: token decoder", icon=ICON_CLOUD)
    TIY = TY + 26
    TSP = X0 + 10 + 100
    inner(X0 + 10, TIY, X1 - X0 - 20, IH, TSP)
    text(X0 + 10, TIY + 4, TSP - X0 - 10, "rANS decode", 13.5, NAVY, 700, "center")
    cells((X0 + 10 + TSP) / 2, TIY + 36, 4, 8, 8)
    text(TSP, TIY + 4, X1 - 10 - TSP, "<i>g<sub>s</sub></i>", 15, NAVY, 700, "center")
    cells((TSP + X1 - 10) / 2, TIY + 30, 6, 15, 15)
    prev(TIY + IH // 2)
    # policy tokens -> frozen VLA policy
    VY, VH = oy + 316, 56
    poly([(CM, TY + TH_ + 9), (CM, VY - 1)])
    cells(CM + 44, TY + TH_ + 17, 4, 13, 10, fill="#FDE2C8", bd="#DC7A2E")
    label(CM + 80, TY + TH_ + 12, 100, "policy tokens", 12.5, "#5A2C05", "left", False)
    card(X0, VY, X1 - X0, VH, None, kind="vla")
    text(X0, VY + 16, X1 - X0, SNOW + "VLA policy (frozen)", 16, "#5A2C05", 700, "center")
    box(ox + 372, VY + 6, 92, 44, "language<br>+ state", "grey", fs=12.5)
    poly([(ox + 371, VY + 28), (X1 + 9, VY + 28)])
    # action chunk back to the robot
    poly([(X0 - 1, VY + 28), (ox + 20, VY + 28), (ox + 20, oy + 38 + 3 * 44 - 3)], RET, dash="6 3 1.5 3")
    out.append(f'<div style="position:absolute; left:{ox+26}px; top:{oy+262}px; transform:rotate(-90deg); transform-origin:left top; '
               f'white-space:nowrap; font-size:12.5px; font-weight:600; font-style:italic; color:#55606E">action chunk</div>')

# ------------------------------------------------------------------ (b) training
LBG, LBD, LTX = "#FFF1E4", PURPLE, "#7A3B0A"
def loss(cx, cy, w, lab):
    out.append(f'<div style="position:absolute; left:{cx-w/2}px; top:{cy-12}px; width:{w}px; height:24px; box-sizing:border-box; '
               f'background:{LBG}; border:1.5px solid {LBD}; border-radius:6px; display:flex; align-items:center; '
               f'justify-content:center; font-size:12.5px; font-weight:700; color:{LTX}; white-space:nowrap">{lab}</div>')
def sigma(cx, cy):
    out.append(f'<div style="position:absolute; left:{cx-15}px; top:{cy-15}px; width:30px; height:30px; box-sizing:border-box; '
               f'border-radius:50%; background:{LBG}; border:1.7px solid {LBD}; display:flex; align-items:center; '
               f'justify-content:center; font-size:17px; font-weight:700; color:{LTX}">&Sigma;</div>')
def legend(x, y):
    text(x, y, 80, SNOW + "frozen", 12.5, "#3F4A5A", 600)
    div(x + 70, y + 3, 18, 13, f"background:#D6E7FA; border:1.4px solid {BLUE}; border-radius:3px")
    text(x + 93, y, 70, "trained", 12.5, "#3F4A5A", 600)

def panel_b_h(ox, oy):          # two rows, for the single-column figure (470 x 210)
    text(ox, oy, 470, "(b) Training: policy frozen, only the frontend is updated", 15.5, "#1C1B19", 700)
    r1, r2 = oy + 60, oy + 140
    mid = (r1 + r2) // 2
    out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:{ox}px; top:{mid-20}px; '
               f'width:40px; height:40px; border-radius:3px; box-shadow:0 0 0 1.3px #8F8A80; object-fit:cover">')
    E0, EW = ox + 58, 112
    box(E0, r1 - 22, EW, 44, "Vision encoder<br>" + SNOW + "+ projection", "venc", fs=12.5)
    box(E0, r2 - 22, EW, 44, "Jointly learned<br>frontend", "ours", fs=12.5)
    poly([(ox + 41, mid), (ox + 48, mid), (ox + 48, r1), (E0 - 1, r1)])
    poly([(ox + 48, mid), (ox + 48, r2), (E0 - 1, r2)])
    TK, V0, VW, AC, SX = ox + 214, ox + 252, 64, ox + 362, ox + 450
    pill(TK, r1, "tokens <i>z</i>"); pill(TK, r2, "tokens <i>&#7825;</i>", BLUE)
    box(V0, r1 - 18, VW, 36, SNOW + "VLA", "vla", fs=13.5); box(V0, r2 - 18, VW, 36, SNOW + "VLA", "vla", fs=13.5)
    pill(AC, r1, "actions <i>a</i>"); pill(AC, r2, "actions <i>&acirc;</i>", BLUE)
    poly([(E0 + EW, r1), (TK - 33, r1)]); poly([(TK + 33, r1), (V0 - 1, r1)]); poly([(V0 + VW, r1), (AC - 36, r1)])
    poly([(E0 + EW, r2), (TK - 33, r2)], BLUE); poly([(TK + 33, r2), (V0 - 1, r2)], BLUE); poly([(V0 + VW, r2), (AC - 36, r2)], BLUE)
    EC = E0 + EW // 2
    loss(EC, mid, 48, "rate"); loss(TK, mid, 52, "token"); loss(AC, mid, 56, "action")
    for x in (TK, AC):
        poly([(x, r1 + 11), (x, mid - 13)], RET, dash="3 2", head=False)
        poly([(x, r2 - 11), (x, mid + 13)], RET, dash="3 2", head=False)
    poly([(EC, r2 - 22), (EC, mid + 13)], RET, dash="3 2", head=False)
    poly([(EC + 25, mid), (TK - 27, mid)], LBD); poly([(TK + 27, mid), (AC - 29, mid)], LBD); poly([(AC + 29, mid), (SX - 16, mid)], LBD)
    sigma(SX, mid)
    poly([(SX, mid + 16), (SX, r2 + 34), (EC, r2 + 34), (EC, r2 + 23)], PURPLE, dash="5 3")
    label(EC + 20, r2 + 36, 230, "gradients update the frontend only", 12.5, PURPLE, "left", False)
    legend(ox + 300, oy + 22)

def panel_b_v(ox, oy):          # columns, for the double-column figure (470 x 384)
    text(ox, oy, 470, "(b) Training: policy frozen, only the frontend is updated", 15.5, "#1C1B19", 700)
    c1, c2 = ox + 92, ox + 352               # original path | frontend path
    lc = (c1 + c2) // 2                       # loss column
    out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:{lc-22}px; top:{oy+34}px; '
               f'width:44px; height:44px; border-radius:3px; box-shadow:0 0 0 1.3px #8F8A80; object-fit:cover">')
    label(lc + 26, oy + 50, 90, "clean image", 12, "#55606E", "left")
    ey = oy + 120
    box(c1 - 75, ey - 22, 150, 44, SNOW + "Vision encoder<br>+ projection", "venc", fs=13)
    box(c2 - 75, ey - 22, 150, 44, "Jointly learned<br>frontend", "ours", fs=13)
    poly([(lc, oy + 79), (lc, oy + 88), (c1, oy + 88), (c1, ey - 23)])
    poly([(lc, oy + 88), (c2, oy + 88), (c2, ey - 23)])
    tky, vy, acy = oy + 184, oy + 238, oy + 292
    pill(c1, tky, "tokens <i>z</i>"); pill(c2, tky, "tokens <i>&#7825;</i>", BLUE)
    box(c1 - 45, vy - 18, 90, 36, SNOW + "VLA", "vla", fs=13.5); box(c2 - 45, vy - 18, 90, 36, SNOW + "VLA", "vla", fs=13.5)
    pill(c1, acy, "actions <i>a</i>"); pill(c2, acy, "actions <i>&acirc;</i>", BLUE)
    for c, col in ((c1, INK), (c2, BLUE)):
        poly([(c, ey + 22), (c, tky - 12)], col); poly([(c, tky + 12), (c, vy - 19)], col); poly([(c, vy + 18), (c, acy - 12)], col)
    loss(lc, ey, 50, "rate"); loss(lc, tky, 54, "token"); loss(lc, acy, 58, "action")
    poly([(c2 - 75, ey), (lc + 26, ey)], RET, dash="3 2", head=False)
    for y in (tky, acy):
        poly([(c1 + 40, y), (lc - 29, y)], RET, dash="3 2", head=False)
        poly([(c2 - 42, y), (lc + 29, y)], RET, dash="3 2", head=False)
    sy = oy + 340
    poly([(lc, ey + 13), (lc, tky - 13)], LBD); poly([(lc, tky + 13), (lc, acy - 13)], LBD); poly([(lc, acy + 13), (lc, sy - 16)], LBD)
    sigma(lc, sy)
    label(lc - 112, sy - 8, 90, "training loss", 12.5, LTX, "right", False)
    poly([(lc + 16, sy), (ox + 452, sy), (ox + 452, ey), (c2 + 76, ey)], PURPLE, dash="5 3")
    label(lc + 22, sy + 4, 200, "gradients update<br>the frontend only", 12.5, PURPLE, "left", False)
    legend(ox + 4, oy + 362)

if MODE == "single":
    W, H = 476, 600
    panel_a(4, 4)
    panel_b_h(4, 404)
else:
    W, H = 980, 392
    panel_a(4, 4)
    div(490, 8, 0, 376, "border-left:1.4px dashed #B8BDC4")
    panel_b_v(504, 4)

out.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0; '
           f'width:{W}px; height:{H}px; overflow:visible; pointer-events:none">{"".join(g)}</svg>')
pills = [o for o in out if "translateX(-50%)" in o]
out = [o for o in out if "translateX(-50%)" not in o] + pills
body = "\n".join(out)
html = f"""<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,600&display=swap" rel="stylesheet">
<div style="position:relative; width:{W}px; height:{H}px; background:#FFFFFF; font-family:'Source Sans 3','Helvetica Neue',Arial,sans-serif; color:#1C1B19">
{body}
</div></body></html>"""
open(sys.argv[1], "w").write(html)
print(W, H)
