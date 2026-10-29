#!/usr/bin/env python3
"""Fig. 2 (system architecture), same visual language as Figure 1. Usage: arch.py OUT.html thumbs.json"""
import sys
exec(open(__file__.replace("arch.py", "helpers.py")).read())
W, H = 1504, 640
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
box(426, 234, 176, 40, "previous codes <i>&#375;</i><sub><i>t</i>&minus;1</sub>", "grey", fs=17)
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
text(CX + 160, 230, 170, "replaces vision<br>encoder + projection", 15, "#55606E", 600, "center", "; font-style:italic")
poly([(CX + 138, yc), (CX + 161, yc)])
poly([(CX + 322, yc), (CX + 343, yc)])
poly([(CX + 388, yc), (CX + 413, yc)])
poly([(CX + 499, 100), (CX + 499, yc - 47)])
# action chunk back to the robot
poly([(CX + 584, yc), (CX + 612, yc), (CX + 612, 326), (63, 326), (63, 82 + 3 * 64 - 5)], RET, dash="9 4 2 4")
text(560, 330, 400, "action chunk", 17, "#55606E", 600, "center", "; font-style:italic")

# ---------------- (b) training
TY = 372
text(16, TY - 12, 700, "(b) Training (policy frozen; only the frontend is updated)", 22, "#1C1B19", 700)
r1, r2 = TY + 62, TY + 172                     # row centres: teacher, frontend
out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:34px; top:{(r1+r2)//2-34}px; '
           f'width:68px; height:68px; border-radius:4px; box-shadow:0 0 0 1.5px #8F8A80; object-fit:cover">')
text(16, (r1 + r2) // 2 + 38, 104, "clean images", 15, "#55606E", 600, "center")
box(170, r1 - 32, 250, 64, SNOW + "Vision encoder + projection", "venc", fs=19)
box(170, r2 - 32, 250, 64, "Jointly learned frontend", "ours", fs=19)
poly([(102, (r1 + r2) // 2), (130, (r1 + r2) // 2), (130, r1), (169, r1)])
poly([(130, (r1 + r2) // 2), (130, r2), (169, r2)])
pill(520, r1, "tokens <i>z</i>")
pill(520, r2, "tokens <i>&#7825;</i>", BLUE)
box(620, r1 - 32, 150, 64, SNOW + "VLA policy", "vla", fs=19)
box(620, r2 - 32, 150, 64, SNOW + "VLA policy", "vla", fs=19)
pill(860, r1, "actions <i>a</i>")
pill(860, r2, "actions <i>&acirc;</i>", BLUE)
poly([(420, r1), (468, r1)]); poly([(572, r1), (619, r1)]); poly([(770, r1), (806, r1)])
poly([(420, r2), (468, r2)], BLUE); poly([(572, r2), (619, r2)], BLUE); poly([(770, r2), (806, r2)], BLUE)
# loss box
LX, LW = 980, 330
out.append(f'<div style="position:absolute; left:{LX}px; top:{r1-36}px; width:{LW}px; height:{r2-r1+72}px; box-sizing:border-box; '
           f'border:1.8px solid #5B6472; border-radius:12px; background:#FFFFFF; padding:14px 18px; font-size:20px; '
           f'line-height:30px; color:#1F2937; font-weight:600">'
           f'<div style="font-weight:700; margin-bottom:4px">Training objective</div>'
           f'<div>token: &nbsp;<i>&#7825;</i> vs. <i>z</i></div><div>action: &nbsp;<i>&acirc;</i> vs. <i>a</i></div>'
           f'<div>rate: &nbsp;bits of the codes</div></div>')
poly([(914, r1), (979, r1)]); poly([(914, r2), (979, r2)], BLUE)
# gradient back to the frontend
poly([(LX + LW / 2, r2 + 37), (LX + LW / 2, r2 + 62), (295, r2 + 62), (295, r2 + 33)], PURPLE, dash="6 4")
text(560, r2 + 66, 360, "gradients update the frontend only", 16, PURPLE, 700, "center")
# legend
text(1336, r1 - 34, 160, SNOW + "frozen", 17, "#3F4A5A", 600)
out.append(f'<div style="position:absolute; left:1336px; top:{r1+2}px; width:26px; height:18px; border-radius:4px; '
           f'background:#D6E7FA; border:1.8px solid {BLUE}"></div>')
text(1370, r1, 140, "trained", 17, "#3F4A5A", 600)

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
