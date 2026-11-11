"""Drawing kit for presentation assets: placement, text, brand type setting, export."""
import os, subprocess, html
from geo import *
from eptype import T, glyph
from brand_f import Brand, CW, fills

B = Brand()
C = CW["signal"]
HEAD, INK, PAPER, FOG, GRAPH, STEEL = C["head"], C["ink"], C["paper"], C["fog"], C["graphite"], C["steel"]
OUT = os.environ.get("ASSET_OUT", "assets")
os.makedirs(OUT, exist_ok=True)
RENDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.mjs")


def fit(items, box, x, y, w=None, h=None, align="center"):
    """Scale items (path, role) whose bounds are `box` into rect (x,y,w,h). Returns (items, scale, (x0,y0,x1,y1))."""
    bx0, by0, bx1, by1 = box
    bw, bh = bx1 - bx0, by1 - by0
    s = min(w / bw if w else 1e9, h / bh if h else 1e9)
    ox = x + ((w - bw * s) / 2 if (w and align == "center") else 0) - bx0 * s
    oy = y + ((h - bh * s) / 2 if h else 0) - by0 * s
    out = [(tf(p, s, 0, 0, s, ox, oy), r) for p, r in items]
    return out, s, (bx0 * s + ox, by0 * s + oy, bx1 * s + ox, by1 * s + oy)


def paint(items, f):
    groups, order = {}, []
    for p, r in items:
        col = f[r] if r in f else r
        if col not in groups:
            groups[col] = []; order.append(col)
        groups[col].append(p)
    return "".join(f'<path d="{d(union(*ps) if len(ps) > 1 else ps[0])}" fill="{col}"/>' for col, ps in ((c, groups[c]) for c in order))


def P(path, fill, extra=""):
    return f'<path d="{d(path)}" fill="{fill}" {extra}/>'


def txt(x, y, s, size, fill, family="Helvetica Neue", weight=400, anchor="start", ls=0, opacity=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-family="{family}" font-weight="{weight}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{opacity}">{html.escape(s)}</text>')


def zh(x, y, s, size, fill, weight=500, anchor="start", ls=0, opacity=1):
    fam = "STHeiti" if weight >= 500 else "Hiragino Sans GB"
    return txt(x, y, s, size, fill, fam, 700 if weight >= 600 else weight, anchor, ls, opacity)


def mono(x, y, s, size, fill, anchor="start", opacity=1, ls=0):
    return txt(x, y, s, size, fill, "Menlo", 400, anchor, ls, opacity)


def brand_text(s, size, S=T, track=0.0):
    """Set a lowercase string in EonPoint Display. Returns (ink_path, dots_path, width) with x-height = size."""
    sc = size / S["X"]
    x = 0; inks, dots = [], []
    for ch in s:
        if ch == " ":
            x += S["s"] * 3.4 * sc; continue
        if ch == ".":
            Dd = S["V"] * S["Dk"]
            dots.append(tf(circle(Dd / 2, -Dd / 2, Dd / 2), sc, 0, 0, sc, x, 0)); x += (Dd + S["s"]) * sc; continue
        ink, dot, w = glyph(ch, S)
        inks.append(tf(ink, sc, 0, 0, sc, x, 0))
        if dot is not None:
            dots.append(tf(dot, sc, 0, 0, sc, x, 0))
        x += (w + S["s"] * (1 + track)) * sc
    ink = union(*inks) if inks else None
    dt = union(*dots) if dots else None
    return ink, dt, x - S["s"] * sc


def shadow_def(id_="sh", dy=18, blur=26, op=0.18, color="#000"):
    return (f'<filter id="{id_}" x="-30%" y="-30%" width="160%" height="170%">'
            f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="{color}" flood-opacity="{op}"/></filter>')


def save(name, w, h, body, bg=None, defs="", png_w=None, svg_only=False):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
         + (f"<defs>{defs}</defs>" if defs else "")
         + (f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else "") + body + "</svg>")
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(s)
    if not svg_only:
        subprocess.run(["node", RENDER, p, os.path.join(OUT, name + ".png"), str(png_w or w), "--fonts"], check=True)
    return p
