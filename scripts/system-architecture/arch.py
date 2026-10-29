#!/usr/bin/env python3
"""Overview figure, multi-layer paradigm (deployment / training), names and section tags match Sec. 4."""
import sys
exec(open(__file__.replace("arch2.py", "helpers.py")).read())
W, H = 1504, 628
SNOW = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6DB0EE" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:6px">'
        + "".join(f'<g transform="rotate({60*k} 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g>'
                  for k in range(6)) + '</svg>')
C["grey"] = ("#F1F2F4", "#9AA1AB", "#2E3440")
TAG = "#8A6D1F"

def region(x, y, w, h, bg, bd, label, icon=""):
    out.append(f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:{bg}; '
               f'border:1.5px solid {bd}; border-radius:18px"></div>')
    out.append(f'<div style="position:absolute; left:{x+14}px; top:{y+10}px; display:flex; gap:7px; align-items:center; '
               f'font-size:22px; line-height:24px; color:#3F4A5A; font-weight:700">{icon}<span>{label}</span></div>')

def pill(cx, cy, html, color=INK, fs=21):
    out.append(f'<div style="position:absolute; left:{cx}px; top:{cy-15}px; transform:translateX(-50%); white-space:nowrap; '
               f'background:#FFFFFF; border:1.6px solid {color}; border-radius:15px; padding:1px 12px; font-size:{fs}px; '
               f'line-height:26px; font-weight:600; color:{color}">{html}</div>')

def tag(x, y, s):
    text(x, y, 80, s, 19, TAG, 700)

def loop(cx, top, label_x):
    """previous-codes store below a module whose bottom edge is at `top`: store down, condition up."""
    box(cx - 62, top + 34, 124, 42, "<i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=22)
    poly([(cx - 30, top), (cx - 30, top + 33)], RET)
    poly([(cx + 30, top + 34), (cx + 30, top + 1)], RET)
    tag(label_x, top + 42, "&sect;4.3")

# ---------------- (a) deployment
text(14, 4, 700, "(a) Deployment", 24, "#1C1B19", 700)
EX, EW, CX, CW, RY, RH = 12, 668, 800, 692, 44, 270
region(EX, RY, EW, RH, "#F6F3EE", "#DCD5C9", "Edge (robot)", CHIP_ICON)
region(CX, RY, CW, RH, "#EEF2F7", "#C9D3DF", "Cloud", CLOUD_ICON)
yc, BH = 160, 100                      # row centre and module height
for k, c in enumerate(["cam1", "cam2", "cam0"]):
    out.append(f'<img src="data:image/jpeg;base64,{TH[c]}" style="position:absolute; left:{30+k*14}px; top:{yc-58+k*14}px; '
               f'width:76px; height:76px; border:2px solid #fff; border-radius:5px; box-sizing:border-box; '
               f'box-shadow:0 0 0 1.4px #8F8A80; object-fit:cover">')
out.append(f'<div style="position:absolute; left:150px; top:84px; width:516px; height:220px; border:2px dashed {BLUE}; '
           f'border-radius:14px; background:rgba(214,231,250,0.30)"></div>')
text(164, 90, 420, "Jointly learned frontend", 20, "#0D366B", 700)
tag(580, 90, "&sect;4.1")
box(168, yc - BH // 2 + 12, 210, BH, "Light vision<br>encoder <i>s</i>", "ours", fs=24)
box(418, yc - BH // 2 + 12, 230, BH, "Feature codec<br><span style='font-weight:500;font-size:20px'><i>h</i> &middot; "
    "<i>Q</i> &middot; rANS</span>", "ours", fs=24)
yr = yc + 12
loop(533, yr + BH // 2, 600)
poly([(122, yr), (167, yr)])
poly([(378, yr), (417, yr)])
poly([(648, yr), (CX + 29, yr)], BLUE)
pill((EX + EW + CX) / 2, yr - 26, "bitstream", BLUE)
box(CX + 30, yr - BH // 2, 230, BH, "Token decoder<br><i>g<sub>s</sub></i>", "ours", fs=24)
loop(CX + 145, yr + BH // 2, CX + 212)
for k in range(4):
    out.append(f'<div style="position:absolute; left:{CX+292}px; top:{yr-38+k*20}px; width:46px; height:13px; '
               f'border-radius:3px; background:#FDE2C8; border:1.4px solid #DC7A2E"></div>')
text(CX + 268, yr + 46, 96, "policy<br>tokens", 19, "#5A2C05", 600, "center")
box(CX + 380, yr - 56, 200, 112, SNOW + "VLA<br>policy", "vla", fs=26)
box(CX + 380, 56, 200, 42, "language + state", "grey", fs=19)
text(CX + 300, 270, 380, "replaces the vision encoder + projection", 19, "#55606E", 600, "left", "; font-style:italic")
poly([(CX + 260, yr), (CX + 291, yr)])
poly([(CX + 338, yr), (CX + 379, yr)])
poly([(CX + 480, 98), (CX + 480, yr - 57)])
poly([(CX + 580, yr), (CX + 640, yr), (CX + 640, 334), (60, 334), (60, yc + 33)], RET, dash="9 4 2 4")
text(560, 338, 400, "action chunk", 20, "#55606E", 600, "center", "; font-style:italic")

# ---------------- (b) training
TY = 372
text(14, TY, 900, "(b) Training: the policy stays frozen, only the frontend is updated", 24, "#1C1B19", 700)
tag(716, TY + 3, "&sect;4.2")
r1, r2 = TY + 82, TY + 166
out.append(f'<img src="data:image/jpeg;base64,{TH["cam0"]}" style="position:absolute; left:30px; top:{(r1+r2)//2-38}px; '
           f'width:76px; height:76px; border-radius:5px; box-shadow:0 0 0 1.4px #8F8A80; object-fit:cover">')
box(168, r1 - 30, 300, 60, SNOW + "Vision encoder + projection", "venc", fs=21)
box(168, r2 - 30, 300, 60, "Jointly learned frontend", "ours", fs=22)
poly([(106, (r1 + r2) // 2), (132, (r1 + r2) // 2), (132, r1), (167, r1)])
poly([(132, (r1 + r2) // 2), (132, r2), (167, r2)])
pill(560, r1, "tokens <i>z</i>")
pill(560, r2, "tokens <i>&#7825;</i>", BLUE)
box(660, r1 - 30, 180, 60, SNOW + "VLA policy", "vla", fs=21)
box(660, r2 - 30, 180, 60, SNOW + "VLA policy", "vla", fs=21)
pill(940, r1, "actions <i>a</i>")
pill(940, r2, "actions <i>&acirc;</i>", BLUE)
poly([(468, r1), (506, r1)]); poly([(614, r1), (659, r1)]); poly([(840, r1), (880, r1)])
poly([(468, r2), (506, r2)], BLUE); poly([(614, r2), (659, r2)], BLUE); poly([(840, r2), (880, r2)], BLUE)
LX, LW = 1060, 300
out.append(f'<div style="position:absolute; left:{LX}px; top:{r1-36}px; width:{LW}px; height:{r2-r1+72}px; box-sizing:border-box; '
           f'border:1.8px solid #5B6472; border-radius:12px; background:#FFFFFF; padding:10px 18px; font-size:21px; '
           f'line-height:28px; color:#1F2937; font-weight:600"><div style="font-weight:700">Objective</div>'
           f'<div>token: <i>&#7825;</i> vs. <i>z</i></div><div>action: <i>&acirc;</i> vs. <i>a</i></div>'
           f'<div>rate: bits of the codes</div></div>')
poly([(1000, r1), (1059, r1)]); poly([(1000, r2), (1059, r2)], BLUE)
poly([(LX + LW / 2, r2 + 37), (LX + LW / 2, r2 + 58), (318, r2 + 58), (318, r2 + 31)], PURPLE, dash="6 4")
text(560, r2 + 60, 380, "gradients reach the frontend only", 19, PURPLE, 700, "center")
text(1386, r1 - 26, 120, SNOW + "frozen", 20, "#3F4A5A", 600)
out.append(f'<div style="position:absolute; left:1388px; top:{r1+12}px; width:26px; height:20px; border-radius:4px; '
           f'background:#D6E7FA; border:1.8px solid {BLUE}"></div>')
text(1422, r1 + 10, 90, "trained", 20, "#3F4A5A", 600)

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
