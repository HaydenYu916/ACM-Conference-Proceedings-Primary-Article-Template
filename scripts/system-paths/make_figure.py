#!/usr/bin/env python3
"""Figure 1 v4: three side-by-side panels, uniform strokes, uniform corner radius, larger type."""
import json, sys

TH = json.load(open(sys.argv[2]))
PW, PH = 484, 448
GAP = 16
X0, Y0 = 10, 8
W = X0 * 2 + PW * 3 + GAP * 2
H = Y0 * 2 + PH

SW = 2.4          # every connector uses this width
R = 10            # every bend uses this radius
C = {
    "light": ("#FFF3C4", "#C9A227", "#4F3D05"),
    "venc": ("#FADDE6", "#C2507A", "#5E1A33"),
    "vla": ("#FDE2C8", "#DC7A2E", "#5A2C05"),
    "ours": ("#D6E7FA", "#2A78D6", "#0D366B"),
}
INK = "#3A3833"
RET = "#6F7B8A"
RED = "#D03B3B"
BLUE = "#2A78D6"
PURPLE = "#DC7A2E"   # training signal comes from the (orange) policy

out, g = [], []


def box(x, y, w, h, html, kind, ghost=False, fs=21):
    if ghost:
        st = ("background: rgba(255,255,255,0.6); border: 1.8px dashed #A8A39A; color: #9C978E; "
              "text-decoration: line-through; text-decoration-thickness: 1.8px")
    else:
        bg, bd, fg = C[kind]
        st = f"background: {bg}; border: 1.8px solid {bd}; color: {fg}"
    out.append(f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; '
               f'box-sizing: border-box; padding: 2px 6px; display: flex; align-items: center; justify-content: center; '
               f'text-align: center; border-radius: 10px; font-size: {fs}px; line-height: {fs+3}px; font-weight: 700; '
               f'{st}"><span>{html}</span></div>')


def text(x, y, w, html, fs=17, color=INK, weight=600, align="left", extra=""):
    out.append(f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; font-size: {fs}px; '
               f'line-height: {fs+3}px; color: {color}; font-weight: {weight}; text-align: {align}{extra}">{html}</div>')


mk = [0]


def poly(pts, color=INK, dash=None, head=True):
    """Orthogonal polyline through pts with uniform rounded corners and an optional filled head."""
    d = f"M {pts[0][0]} {pts[0][1]}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        def toward(ax, ay, bx, by, r):
            dx, dy = bx - ax, by - ay
            L = abs(dx) + abs(dy)
            return ax + dx / L * r, ay + dy / L * r
        ax, ay = toward(x1, y1, x0, y0, R)
        bx, by = toward(x1, y1, x2, y2, R)
        d += f" L {ax:g} {ay:g} Q {x1} {y1} {bx:g} {by:g}"
    d += f" L {pts[-1][0]} {pts[-1][1]}"
    defs = me = ""
    if head:
        mk[0] += 1
        defs = (f'<defs><marker id="h{mk[0]}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" '
                f'markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/>'
                f'</marker></defs>')
        me = f' marker-end="url(#h{mk[0]})"'
    da = f' stroke-dasharray="{dash}"' if dash else ""
    g.append(f'{defs}<path d="{d}" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linejoin="round" '
             f'stroke-linecap="butt"{da}{me}/>')


ROBOT = '''<svg width="120" height="111" viewBox="0 0 130 120" style="position:absolute; left:{x}px; top:{y}px; overflow:visible">
<g stroke="#2B2F36" stroke-linejoin="round" stroke-linecap="round">
  
  <rect x="8" y="106" width="86" height="10" rx="3" fill="#C9CFD8" stroke-width="2"/>
  <path d="M26 106 L30 88 H66 L70 106 Z" fill="#E6EAF0" stroke-width="2.2"/>
  <rect x="34" y="80" width="28" height="10" rx="3" fill="#D3D9E2" stroke-width="2"/>
  
  <path d="M48 76 L36 38" stroke-width="19"/>
  <path d="M48 76 L36 38" stroke="#F4F6F9" stroke-width="14"/>
  <path d="M43.5 72 L33 40" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>
  
  <path d="M36 38 L86 26" stroke-width="15"/>
  <path d="M36 38 L86 26" stroke="#F4F6F9" stroke-width="10.5"/>
  <path d="M40 34.5 L84 24" stroke="#FFFFFF" stroke-width="2.4" opacity="0.9"/>
  
  <path d="M56 78 C 60 60, 48 48, 46 42 C 56 40, 70 38, 82 33" fill="none" stroke="#5B6472" stroke-width="1.4" opacity="0.7"/>
  
  <circle cx="48" cy="76" r="11.5" fill="#F4F6F9" stroke-width="2.2"/>
  <circle cx="48" cy="76" r="5.5" fill="#8FA3BF" stroke-width="1.6"/>
  <circle cx="36" cy="38" r="10" fill="#F4F6F9" stroke-width="2.2"/>
  <circle cx="36" cy="38" r="4.6" fill="#8FA3BF" stroke-width="1.5"/>
  <circle cx="86" cy="26" r="7.5" fill="#F4F6F9" stroke-width="2"/>
  <circle cx="86" cy="26" r="3.2" fill="#8FA3BF" stroke-width="1.3"/>
  
  <path d="M90 27 L100 30" stroke-width="9"/>
  <path d="M90 27 L100 30" stroke="#E6EAF0" stroke-width="5.5"/>
  <rect x="99" y="20" width="7" height="22" rx="2" fill="#D3D9E2" stroke-width="1.8" transform="rotate(16 102.5 31)"/>
  
  <path d="M106 24 L118 26 L119 30 L107 29 Z" fill="#B9C2CE" stroke-width="1.6"/>
  <path d="M103 36 L115 39 L114 43 L102 40 Z" fill="#B9C2CE" stroke-width="1.6"/>
  
  <rect x="83" y="9" width="15" height="10" rx="2" fill="#3D4652" stroke-width="1.6" transform="rotate(16 90.5 14)"/>
  <circle cx="91.5" cy="14.5" r="2.6" fill="#9FC4EE" stroke-width="1"/>
</g>
</svg>'''

CHIP_ICON = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3F4A5A" stroke-width="1.7" '
             'stroke-linecap="round" stroke-linejoin="round" style="flex:none"><rect x="6" y="6" width="12" height="12" rx="2"/>'
             '<path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>')
CLOUD_ICON = ('<svg width="30" height="20" viewBox="0 0 24 16" fill="none" stroke="#3F4A5A" stroke-width="1.6" '
              'stroke-linejoin="round" style="flex:none"><path d="M6.5 15h11a4.5 4.5 0 0 0 .6-8.96A6 6 0 0 0 6.6 '
              '5.2 4.9 4.9 0 0 0 6.5 15z"/></svg>')


def thumbs(x, y, s=64):
    for k, c in enumerate(["cam0", "cam2", "cam1"]):
        out.append(f'<img src="data:image/jpeg;base64,{TH[c]}" style="position: absolute; left: {x+k*(s+3)}px; '
                   f'top: {y}px; width: {s}px; height: {s}px; border-radius: 4px; box-shadow: 0 0 0 1.5px #8F8A80; '
                   f'object-fit: cover">')


def half(x, y, w, h, side, sub):
    """One half of the same vision encoder; the cut side is a wavy edge (~) that matches the other half."""
    bd = "#C2507A"
    if side == "left":
        b = f"border: 1.8px solid {bd}; border-right: none; border-radius: 10px 0 0 10px"
        wx = x + w - 5
    else:
        b = f"border: 1.8px solid {bd}; border-left: none; border-radius: 0 10px 10px 0"
        wx = x - 5
    out.append(f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; '
               f'box-sizing: border-box; display: flex; align-items: center; justify-content: center; text-align: center; '
               f'background: #FADDE6; {b}; color: #5E1A33; font-size: 21px; line-height: 24px; font-weight: 700">'
               f'<span>Vision encoder<br><span style="font-weight:500;font-size:18px">{sub}</span></span></div>')
    d, yy, up = "M 5 0", 0, True
    while yy < h:
        ny = min(yy + 8.5, h)
        d += f" Q {9 if up else 1} {yy + (ny - yy)/2:.1f} 5 {ny:.1f}"
        yy, up = ny, not up
    fill = f'<path d="{d} L {0 if side == "left" else 10} {h} L {0 if side == "left" else 10} 0 Z" fill="#FADDE6"/>'
    out.append(f'<svg width="10" height="{h}" viewBox="0 0 10 {h}" style="position: absolute; left: {wx}px; top: {y}px; '
               f'overflow: visible">{fill}<path d="{d}" fill="none" stroke="{bd}" stroke-width="2"/></svg>')


PANELS = [
    dict(title="(a) Image Offloading", kind="a",
         payload="compressed frames", pcolor=INK,
         notes=[("x", "Low rate can break control"), ("x", "Cloud re-encodes images")]),
    dict(title="(b) Split Inference", kind="b",
         payload="intermediate features", pcolor=INK,
         notes=[("x", "Large intermediate features"), ("x", "Encoder cost on both sides")]),
    dict(title="(c) Ours: Policy-Aligned Feature Streaming", kind="c",
         payload="compact codes", pcolor=BLUE,
         notes=[("v", "Light edge, small uplink"), ("v", "Cloud skips vision encoder")]),
]

for p_i, P in enumerate(PANELS):
    ox, oy = X0 + p_i * (PW + GAP), Y0
    k = P["kind"]
    if p_i > 0:
        out.append(f'<div style="position: absolute; left: {ox - GAP//2}px; top: {oy+40}px; width: 0; '
                   f'height: {PH-56}px; border-left: 1.5px dashed #CFCAC0"></div>')
    text(ox, oy, PW, P["title"], 24, "#1C1B19", 700, "center")

    # ---- cloud region
    cx0, cy0, cw, ch = ox + 234, oy + 74, 246, 250
    out.append(f'<div style="position: absolute; left: {cx0}px; top: {cy0}px; width: {cw}px; height: {ch}px; '
               f'background: #EEF2F7; border: 1.5px solid #C9D3DF; border-radius: 18px"></div>')
    out.append(f'<div style="position: absolute; left: {cx0+14}px; top: {cy0+10}px; display: flex; gap: 7px; '
               f'align-items: center; font-size: 20px; line-height: 22px; color: #3F4A5A; font-weight: 700">'
               f'{CLOUD_ICON}<span>Cloud</span></div>')
    mx, mw = cx0 + (246 - 184) // 2, 184
    mcx = mx + mw // 2
    S0, S1, S2 = (oy + 112, 46), (oy + 174, 46), (oy + 236, 56)

    # ---- robot side
    out.append(f'<div style="position: absolute; left: {ox}px; top: {cy0}px; width: 220px; height: {ch}px; '
               f'background: #F6F3EE; border: 1.5px solid #DCD5C9; border-radius: 18px"></div>')
    out.append(f'<div style="position: absolute; left: {ox+14}px; top: {cy0+10}px; display: flex; gap: 7px; '
               f'align-items: center; font-size: 20px; line-height: 22px; color: #3F4A5A; font-weight: 700">'
               f'{CHIP_ICON}<span>Edge</span></div>')
    out.append(ROBOT.format(x=ox + 2, y=oy + 330))
    thumbs(ox + 8, oy + 244)
    tcx = ox + 8 + 67 + 32                   # back thumbnail centre x
    ecx = ox + 112                       # uplink leaves edge module here
    if k == "a":
        box(ox + 16, oy + 112, 188, 68, "Image encoder<br><span style='font-weight:500;font-size:18px'>"
            "(H.264 / JPEG)</span>", "light")
        e_top, e_bot = oy + 112, oy + 180
    elif k == "b":
        half(ox + 16, oy + 112, 188, 68, "left", "layers 1&ndash;<i>k</i>")
        e_top, e_bot = oy + 112, oy + 180
    else:
        # one jointly learned block, split into two stages that share a border
        out.append(f'<div style="position: absolute; left: {ox+6}px; top: {oy+112}px; width: 210px; height: 104px; '
                   f'box-sizing: border-box; border: 1.8px solid {BLUE}; border-radius: 12px; background: #CDE2FB; '
                   f'"></div>')
        text(ox + 6, oy + 115, 210, "Jointly learned frontend", 17, "#0D366B", 700, "center",
             "; letter-spacing: 0.02em")
        seg = ("position: absolute; box-sizing: border-box; display: flex; align-items: center; justify-content: center; "
               "text-align: center; background: #EEF5FE; border: 1.4px solid #2A78D6; color: #0D366B; font-weight: 700")
        out.append(f'<div style="{seg}; left: {ox+14}px; top: {oy+138}px; width: 194px; height: 36px; '
                   f'border-radius: 8px 8px 0 0; font-size: 19px; line-height: 22px"><span>Light vision encoder</span></div>')
        out.append(f'<div style="{seg}; left: {ox+14}px; top: {oy+173}px; width: 194px; height: 36px; '
                   f'border-radius: 0 0 8px 8px; font-size: 19px; line-height: 22px"><span>Feature codec</span></div>')
        e_top, e_bot = oy + 112, oy + 216

    # ---- cloud modules
    if k == "a":
        box(mx, S0[0], mw, S0[1], "Image decoder", "light")
        box(mx, S1[0], mw, S1[1], "Vision encoder", "venc")
    elif k == "c":
        box(mx, S0[0], mw, S0[1], "Token decoder", "ours")
        box(mx, S1[0], 140, S1[1], "Vision encoder", "venc", ghost=True, fs=19)
    else:
        half(mx, oy + 112, mw, 68, "right", "layers <i>k</i>+1&ndash;<i>N</i>")
    VLA = S2
    SNOW = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6DB0EE" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:6px">'
            '<g transform="rotate(0 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g><g transform="rotate(60 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g><g transform="rotate(120 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g><g transform="rotate(180 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g><g transform="rotate(240 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g><g transform="rotate(300 12 12)"><path d="M12 12 V2.5 M9.6 4.6 L12 7 L14.4 4.6"/></g></svg>')
    box(mx, VLA[0], mw, VLA[1], SNOW + "VLA policy", "vla", fs=23)

    # ---- connectors (all SW wide, all bends radius R)
    poly([(tcx, oy + 242), (tcx, e_bot + 1)])                      # cameras -> edge encoder
    yU = oy + 56
    pc = P["pcolor"]
    first = oy + 112 if k == "b" else S0[0]
    poly([(ecx, e_top), (ecx, yU), (mcx, yU), (mcx, first - 1)], pc)
    out.append(f'<div style="position: absolute; left: {(ecx + mcx) // 2}px; top: {yU - 14}px; '
               f'transform: translateX(-50%); white-space: nowrap; background: #FFFFFF; border: 1.6px solid {pc}; '
               f'border-radius: 14px; padding: 2px 12px; font-size: 18px; line-height: 22px; font-weight: 600; '
               f'color: {pc}">{P["payload"]}</div>')
    if k == "a":
        poly([(mcx, S0[0] + S0[1]), (mcx, S1[0] - 1)])
    if k == "a":
        poly([(mcx, S1[0] + S1[1]), (mcx, S2[0] - 1)])
    if k == "b":
        poly([(mcx, oy + 180), (mcx, S2[0] - 1)])
    if k == "c":
        xa = mx + mw - 22
        poly([(xa, S0[0] + S0[1]), (xa, S2[0] - 1)], BLUE)
        poly([(mx, S2[0] + 26), (ox + 211, S2[0] + 26), (ox + 211, e_bot + 1)], PURPLE, dash="6 4")
        text(ox + 104, e_bot + 5, 98, "action loss", 18, PURPLE, 700, "right")
    yR = oy + 412
    poly([(mx, VLA[0] + 44), (ox + 227, VLA[0] + 44), (ox + 227, yR), (ox + 110, yR)], RET, dash="9 4 2 4")
    text(ox + 100, yR - 26, 114, "action chunk", 18, "#55606E", 600, "right", "; font-style: italic")
    for li, (ic, tx) in enumerate(P["notes"]):
        col = RED if ic == "x" else BLUE
        glyph = ('<path d="M6 6 L12 12 M12 6 L6 12"/>' if ic == "x" else '<path d="M5.5 9.5 L8 12 L12.5 6.5"/>')
        icon = (f'<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#FFFFFF" stroke-width="2.2" '
                f'stroke-linecap="round" stroke-linejoin="round" style="flex:none"><circle cx="9" cy="9" r="9" '
                f'fill="{col}" stroke="none"/>{glyph}</svg>')
        out.append(f'<div style="position: absolute; left: {cx0 + 6}px; top: {cy0 + ch + 10 + li*28}px; left: {cx0 + 8}px; display: flex; '
                   f'gap: 7px; align-items: center; white-space: nowrap; font-size: 18px; line-height: 22px; '
                   f'font-weight: 600; color: {col}">{icon}<span>{tx}</span></div>')

pills = [o for o in out if 'translateX(-50%)' in o]
out = [o for o in out if 'translateX(-50%)' not in o]
out.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position: absolute; left: 0; top: 0; '
           f'width: {W}px; height: {H}px; overflow: visible; pointer-events: none">{"".join(g)}</svg>')

out += pills
body = "\n".join(out)
html = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>body{{margin:0}}</style>
</helmet>
<div style="position: relative; width: {W}px; height: {H}px; background: #FFFFFF; font-family: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif; color: #1C1B19">
{body}
</div>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>class Component extends DCLogic {{ renderVals(){{return {{}};}} }}</script>
</x-dc>
</body>
</html>
'''
open(sys.argv[1], "w").write(html)
print("ok", W, H)
