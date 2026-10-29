#!/usr/bin/env python3
"""Fig. 2 (system architecture), same visual language as Figure 1. Usage: arch.py OUT.html thumbs.json"""
import sys
exec(open(__file__.replace("arch.py", "helpers.py")).read())
W, H = 1504, 610
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

# ---------------- (a) deployment
text(16, 6, 600, "(a) Deployment", 22, "#1C1B19", 700)
EX, EY, EW, EH = 16, 40, 724, 270
CX, CW = 852, 636
region(EX, EY, EW, EH, "#F6F3EE", "#DCD5C9", "Edge (robot)", CHIP_ICON)
region(CX, EY, CW, EH, "#EEF2F7", "#C9D3DF", "Cloud", CLOUD_ICON)
frame(34, 82)
yc = 176                                   # main row centre
# frontend container (edge part)
out.append(f'<div style="position:absolute; left:110px; top:72px; width:618px; height:226px; border:1.8px dashed {BLUE}; '
           f'border-radius:14px; background:rgba(214,231,250,0.35)"></div>')
text(122, 78, 400, "Jointly learned frontend", 17, "#0D366B", 700)
box(124, yc - 40, 160, 80, "Light vision<br>encoder <i>s</i>", "ours", fs=20)
out.append(f'<div style="position:absolute; left:304px; top:104px; width:412px; height:184px; border:1.5px solid #9DBEE6; '
           f'border-radius:12px; background:#FFFFFF"></div>')
text(316, 110, 200, "Feature codec", 17, "#0D366B", 700)
box(318, yc - 34, 118, 68, "Feature<br>head <i>h</i>", "ours", fs=19)
box(462, yc - 34, 104, 68, "Quantize<br><i>Q</i>", "ours", fs=19)
box(592, yc - 34, 112, 68, "rANS<br>encode", "ours", fs=19)
box(426, 234, 176, 40, "previous codes <i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=18)
poly([(92, yc), (123, yc)])                                   # frames -> encoder
poly([(284, yc), (317, yc)])
poly([(436, yc), (461, yc)])
poly([(566, yc), (591, yc)])
poly([(514, yc + 34), (514, 233)], RET)                       # store dequantized codes
poly([(436, 254), (377, 254), (377, yc + 35)], RET)           # condition the head (inter uploads)
text(330, 258, 110, "inter", 15, "#55606E", 600, "left", "; font-style:italic")
# network
poly([(704, yc), (CX + 19, yc)], BLUE)
pill((740 + CX) / 2, yc - 22, "bitstream", BLUE)
# cloud
box(CX + 20, yc - 34, 118, 68, "rANS<br>decode", "ours", fs=19)
box(CX + 162, yc - 40, 160, 80, "Token<br>decoder <i>g<sub>s</sub></i>", "ours", fs=20)
for k in range(4):
    out.append(f'<div style="position:absolute; left:{CX+344}px; top:{yc-34+k*18}px; width:44px; height:12px; '
               f'border-radius:3px; background:#FDE2C8; border:1.4px solid #DC7A2E"></div>')
text(CX + 326, yc + 40, 80, "policy<br>tokens", 15, "#5A2C05", 600, "center")
box(CX + 414, yc - 46, 170, 92, SNOW + "VLA<br>policy", "vla", fs=22)
box(CX + 420, 56, 158, 44, "language + state", "grey", fs=17)
box(CX + 20, 234, 176, 40, "previous codes <i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=18)
poly([(CX + 79, yc + 34), (CX + 79, 233)], RET)
poly([(CX + 196, 254), (CX + 242, 254), (CX + 242, yc + 41)], RET)
text(CX + 262, 280, 330, "replaces vision encoder + projection", 15, "#55606E", 600, "left", "; font-style:italic")
poly([(CX + 138, yc), (CX + 161, yc)])
poly([(CX + 322, yc), (CX + 343, yc)])
poly([(CX + 388, yc), (CX + 413, yc)])
poly([(CX + 499, 100), (CX + 499, yc - 47)])
# action chunk back to the robot
poly([(CX + 584, yc), (CX + 612, yc), (CX + 612, 326), (63, 326), (63, 82 + 3 * 64 - 5)], RET, dash="9 4 2 4")
text(560, 330, 400, "action chunk", 17, "#55606E", 600, "center", "; font-style:italic")

# ---------------- (b) training
TY = 364
text(16, TY - 12, 700, "(b) Training (policy frozen; only the frontend is updated)", 22, "#1C1B19", 700)
r1, r2 = TY + 54, TY + 162                     # row centres: original path, frontend path
mid = (r1 + r2) // 2
out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:34px; top:{mid-34}px; '
           f'width:68px; height:68px; border-radius:4px; box-shadow:0 0 0 1.5px #8F8A80; object-fit:cover">')
text(16, mid + 36, 104, "clean images", 15, "#55606E", 600, "center")
# x layout spread across the full width
EB0, EBW = 160, 280; ECX = EB0 + EBW // 2      # encoder boxes
TKX = 590                                      # token pills
VB0, VBW = 700, 180                            # policy boxes
ACX = 1010                                     # action pills
SX = 1210                                      # sum node
box(EB0, r1 - 28, EBW, 56, SNOW + "Vision encoder + projection", "venc", fs=19)
box(EB0, r2 - 28, EBW, 56, "Jointly learned frontend", "ours", fs=19)
poly([(102, mid), (130, mid), (130, r1), (EB0 - 1, r1)])
poly([(130, mid), (130, r2), (EB0 - 1, r2)])
pill(TKX, r1, "tokens <i>z</i>")
pill(TKX, r2, "tokens <i>&#7825;</i>", BLUE)
box(VB0, r1 - 28, VBW, 56, SNOW + "VLA policy", "vla", fs=19)
box(VB0, r2 - 28, VBW, 56, SNOW + "VLA policy", "vla", fs=19)
pill(ACX, r1, "actions <i>a</i>")
pill(ACX, r2, "actions <i>&acirc;</i>", BLUE)
poly([(EB0 + EBW, r1), (TKX - 53, r1)]); poly([(TKX + 53, r1), (VB0 - 1, r1)]); poly([(VB0 + VBW, r1), (ACX - 55, r1)])
poly([(EB0 + EBW, r2), (TKX - 53, r2)], BLUE); poly([(TKX + 53, r2), (VB0 - 1, r2)], BLUE); poly([(VB0 + VBW, r2), (ACX - 55, r2)], BLUE)

# losses: three badges on one line, summed at the right
LBG, LBD, LTX = "#FFF1E4", PURPLE, "#7A3B0A"
def loss(cx, w, label):
    out.append(f'<div style="position:absolute; left:{cx-w/2}px; top:{mid-16}px; width:{w}px; height:32px; box-sizing:border-box; '
               f'background:{LBG}; border:1.8px solid {LBD}; border-radius:8px; display:flex; align-items:center; '
               f'justify-content:center; font-size:17px; font-weight:700; color:{LTX}; white-space:nowrap">{label}</div>')
loss(ECX, 112, "rate loss")
loss(TKX, 118, "token loss")
loss(ACX, 126, "action loss")
for x in (TKX, ACX):                          # what each loss compares
    poly([(x, r1 + 15), (x, mid - 17)], RET, dash="4 3", head=False)
    poly([(x, r2 - 15), (x, mid + 17)], RET, dash="4 3", head=False)
poly([(ECX, r2 - 28), (ECX, mid + 17)], RET, dash="4 3", head=False)
poly([(ECX + 57, mid), (TKX - 60, mid)], LBD); poly([(TKX + 60, mid), (ACX - 64, mid)], LBD); poly([(ACX + 64, mid), (SX - 23, mid)], LBD)
out.append(f'<div style="position:absolute; left:{SX-22}px; top:{mid-22}px; width:44px; height:44px; box-sizing:border-box; '
           f'border-radius:50%; background:{LBG}; border:2px solid {LBD}; display:flex; align-items:center; '
           f'justify-content:center; font-size:26px; font-weight:700; color:{LTX}">&Sigma;</div>')
text(SX + 30, mid - 12, 200, "training loss", 18, LTX, 700)
# gradient back to the frontend
poly([(SX, mid + 23), (SX, r2 + 52), (ECX, r2 + 52), (ECX, r2 + 29)], PURPLE, dash="6 4")
text((ECX + SX) / 2 - 200, r2 + 54, 400, "gradients update the frontend only", 16, PURPLE, 700, "center")
# legend, aligned with the two rows at the right edge
text(1386, r1 - 12, 120, SNOW + "frozen", 17, "#3F4A5A", 600)
out.append(f'<div style="position:absolute; left:1388px; top:{r2-9}px; width:26px; height:18px; border-radius:4px; '
           f'background:#D6E7FA; border:1.8px solid {BLUE}"></div>')
text(1422, r2 - 12, 100, "trained", 17, "#3F4A5A", 600)

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
