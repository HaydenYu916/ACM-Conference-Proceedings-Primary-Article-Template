#!/usr/bin/env python3
"""Sec. 4.3 figure (single column): reference from a neural decoder vs. conditioning on the stored code."""
import sys
exec(open(__file__.replace("temporal.py", "helpers.py")).read())
W, H = 720, 400
C["grey"] = ("#F1F2F4", "#9AA1AB", "#2E3440")

def panel(x0, ours):
    out.append(f'<div style="position:absolute; left:{x0}px; top:10px; width:340px; height:316px; background:#F6F3EE; '
               f'border:1.5px solid #DCD5C9; border-radius:16px"></div>')
    text(x0 + 12, 18, 200, "robot", 20, "#5A554C", 700)
    cx, sx = x0 + 100, x0 + 262
    box(cx - 60, 52, 120, 50, "<i>g<sub>a</sub></i>", "ours", fs=24)
    box(cx - 60, 162, 120, 46, "<i>Q</i>", "grey", fs=24)
    box(cx - 60, 238, 120, 46, "rANS", "grey", fs=22)
    poly([(cx, 284), (cx, 330)])
    text(cx + 8, 300, 120, "to cloud", 19, "#55606E", 600)
    poly([(cx, 208), (cx, 237)])
    poly([(cx + 60, 185), (sx, 185), (sx, (126 if not ours else 103) + (26 if not ours else 0))], RET)
    if not ours:
        out.append(f'<div style="position:absolute; left:{cx-15}px; top:115px; width:30px; height:30px; border-radius:50%; '
                   f'border:2px solid #3A3833; background:#fff; display:flex; align-items:center; justify-content:center; '
                   f'font-size:24px; font-weight:700; color:#3A3833; line-height:24px">&minus;</div>')
        poly([(cx, 102), (cx, 114)]); poly([(cx, 146), (cx, 161)])
        box(sx - 66, 104, 132, 48, "neural<br>decoder", "venc", fs=20)
        poly([(sx - 66, 130), (cx + 16, 130)])
        text(x0 + 8, 336, 324, "(a) Reference from a neural<br>decoder, run on the robot", 20, "#1C1B19", 700, "center")
    else:
        poly([(cx, 102), (cx, 161)])
        box(sx - 54, 54, 108, 46, "<i>y</i><sub><i>t</i>&minus;1</sub>", "grey", fs=22)
        poly([(sx - 54, 77), (cx + 61, 77)], BLUE)
        text(sx - 40, 112, 120, "store", 18, "#55606E", 600, "left", "; font-style:italic")
        text(cx + 66, 38, 120, "condition", 18, BLUE, 600, "left", "; font-style:italic")
        text(x0 + 8, 336, 324, "(b) Condition on the stored<br>code (ours)", 20, "#1C1B19", 700, "center")

panel(10, False)
panel(370, True)
out.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0; '
           f'width:{W}px; height:{H}px; overflow:visible; pointer-events:none">{"".join(g)}</svg>')
body = "\n".join(out)
html = f"""<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,600&display=swap" rel="stylesheet">
<div style="position:relative; width:{W}px; height:{H}px; background:#FFFFFF; font-family:'Source Sans 3','Helvetica Neue',Arial,sans-serif; color:#1C1B19">
{body}
</div></body></html>"""
open(sys.argv[1], "w").write(html)
print("ok", W, H)
