"""Geometry kernel: build glyph/symbol shapes as skia paths, boolean them, emit SVG.
Coordinates are SVG-style (y down)."""
import math
import pathops
from pathops import Path, PathOp, LineCap, LineJoin
from fontTools.pens.svgPathPen import SVGPathPen

K = 0.5523  # circle tension


def rect(x0, y0, x1, y1):
    p = Path()
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p


def ellipse(cx, cy, rx, ry, k=K):
    """Ellipse/superellipse made of 4 cubics; k>0.5523 squares it up."""
    p = Path()
    p.moveTo(cx + rx, cy)
    p.cubicTo(cx + rx, cy + ry * k, cx + rx * k, cy + ry, cx, cy + ry)
    p.cubicTo(cx - rx * k, cy + ry, cx - rx, cy + ry * k, cx - rx, cy)
    p.cubicTo(cx - rx, cy - ry * k, cx - rx * k, cy - ry, cx, cy - ry)
    p.cubicTo(cx + rx * k, cy - ry, cx + rx, cy - ry * k, cx + rx, cy)
    p.close()
    return p


def circle(cx, cy, r):
    return ellipse(cx, cy, r, r)


def rrect(x0, y0, x1, y1, r, k=K):
    """Rounded rectangle; k>0.5523 gives a smoother (squircle-ish) corner."""
    p = Path()
    p.moveTo(x0 + r, y0)
    p.lineTo(x1 - r, y0); p.cubicTo(x1 - r + r * k, y0, x1, y0 + r - r * k, x1, y0 + r)
    p.lineTo(x1, y1 - r); p.cubicTo(x1, y1 - r + r * k, x1 - r + r * k, y1, x1 - r, y1)
    p.lineTo(x0 + r, y1); p.cubicTo(x0 + r - r * k, y1, x0, y1 - r + r * k, x0, y1 - r)
    p.lineTo(x0, y0 + r); p.cubicTo(x0, y0 + r - r * k, x0 + r - r * k, y0, x0 + r, y0)
    p.close()
    return p


def poly(pts):
    p = Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


_CAP = {"butt": LineCap.BUTT_CAP, "round": LineCap.ROUND_CAP, "square": LineCap.SQUARE_CAP}
_JOIN = {"miter": LineJoin.MITER_JOIN, "round": LineJoin.ROUND_JOIN, "bevel": LineJoin.BEVEL_JOIN}


def stroke(pts, w, cap="butt", join="miter", miter=10, closed=False):
    p = Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    p.stroke(w, _CAP[cap], _JOIN[join], miter)
    p.convertConicsToQuads(0.01)
    return pathops.simplify(p)


def stroke_path(p, w, cap="butt", join="miter", miter=10):
    q = Path(p)
    q.stroke(w, _CAP[cap], _JOIN[join], miter)
    q.convertConicsToQuads(0.01)
    return pathops.simplify(q)


def arc_pts(cx, cy, rx, ry, a0, a1, n=48):
    """Points on an ellipse arc, angles in degrees (0 = +x, 90 = +y i.e. downward)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def union(*ps):
    ps = [p for p in ps if p is not None]
    out = ps[0]
    for p in ps[1:]:
        out = pathops.op(out, p, PathOp.UNION)
    return out


def diff(a, *bs):
    for b in bs:
        a = pathops.op(a, b, PathOp.DIFFERENCE)
    return a


def inter(a, b):
    return pathops.op(a, b, PathOp.INTERSECTION)


def tf(p, a=1, b=0, c=0, d=1, e=0, f=0):
    return p.transform(a, b, c, d, e, f)


def move(p, dx, dy):
    return p.transform(1, 0, 0, 1, dx, dy)


def scale(p, s, ox=0, oy=0):
    return p.transform(s, 0, 0, s, ox - ox * s, oy - oy * s)


def bounds(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)


def d(p, prec=2):
    pen = SVGPathPen(None, ntos=lambda v: (f"{v:.{prec}f}").rstrip("0").rstrip(".") if "." in f"{v:.{prec}f}" else f"{v:.{prec}f}")
    p.draw(pen)
    s = pen.getCommands()
    return s.replace("-0 ", "0 ").replace(" -0Z", " 0Z")


def svg(items, box, bg=None, pad=0):
    """items: list of (path, fill). box: (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    body = ""
    if bg:
        body += f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>'
    for p, fill in items:
        body += f'<path d="{d(p)}" fill="{fill}"/>' if isinstance(p, Path) else p
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}">{body}</svg>')
