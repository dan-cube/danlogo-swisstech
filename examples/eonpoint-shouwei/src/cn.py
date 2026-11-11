"""Custom 亿触点 lettering, built segment by segment on a 100-unit em (y down).
Horizontals are drawn ~14% lighter than verticals/diagonals (optical compensation)."""
import math
from geo import *


def fillet(pts, i, R, n=20):
    """Replace vertex i of a polyline with a circular arc of radius R."""
    V = pts[i]; A = pts[i - 1]; B = pts[i + 1]
    ux, uy = A[0] - V[0], A[1] - V[1]; lu = math.hypot(ux, uy); ux, uy = ux / lu, uy / lu
    vx, vy = B[0] - V[0], B[1] - V[1]; lv = math.hypot(vx, vy); vx, vy = vx / lv, vy / lv
    th = math.acos(max(-1, min(1, ux * vx + uy * vy)))
    t = R / math.tan(th / 2)
    P1 = (V[0] + ux * t, V[1] + uy * t); P2 = (V[0] + vx * t, V[1] + vy * t)
    bx, by = ux + vx, uy + vy; lb = math.hypot(bx, by); bx, by = bx / lb, by / lb
    h = R / math.sin(th / 2)
    C = (V[0] + bx * h, V[1] + by * h)
    a1 = math.atan2(P1[1] - C[1], P1[0] - C[0]); a2 = math.atan2(P2[1] - C[1], P2[0] - C[0])
    da = a2 - a1
    while da > math.pi: da -= 2 * math.pi
    while da < -math.pi: da += 2 * math.pi
    arc = [(C[0] + R * math.cos(a1 + da * k / n), C[1] + R * math.sin(a1 + da * k / n)) for k in range(n + 1)]
    return pts[:i] + arc + pts[i + 1:]


def _isect(p, d, a, b):
    """Intersect ray p + t*d with line a-b; return point."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    den = d[0] * ey - d[1] * ex
    t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
    return (p[0] + d[0] * t, p[1] + d[1] * t)


def seg(p0, p1, w, e0=0.0, e1=0.0, cut0=None, cut1=None, cap="butt"):
    """Straight stroke. e0/e1 extend the ends; cut0/cut1 = a line ((x,y),(x,y)) to cut that end along."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    nx, ny = -uy * w / 2, ux * w / 2
    a = (p0[0] - ux * e0, p0[1] - uy * e0); b = (p1[0] + ux * e1, p1[1] + uy * e1)
    l0, r0 = (a[0] + nx, a[1] + ny), (a[0] - nx, a[1] - ny)
    l1, r1 = (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny)
    if cut0:
        l0 = _isect(l1, (-ux, -uy), *cut0); r0 = _isect(r1, (-ux, -uy), *cut0)
    if cut1:
        l1 = _isect(l0, (ux, uy), *cut1); r1 = _isect(r0, (ux, uy), *cut1)
    p = poly([l0, l1, r1, r0])
    if cap == "round":
        p = union(p, circle(*a, w / 2), circle(*b, w / 2))
    return p


def pline(pts, w, fil=(), join="miter", cap="butt"):
    pts = list(pts)
    for (vi, R) in sorted(fil, key=lambda x: -x[0]):
        pts = fillet(pts, vi, R)
    return stroke(pts, w, cap=cap, join=join, miter=6)


def box(x0, y0, x1, y1, wv, wh, cap="butt"):
    if cap == "round":
        p = Path(); p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
        return stroke_path(p, (wv + wh) / 2, cap="round", join="round")
    return union(seg((x0, y0), (x1, y0), wh, wv / 2, wv / 2), seg((x0, y1), (x1, y1), wh, wv / 2, wv / 2),
                 seg((x0, y0), (x0, y1), wv, wh / 2, wh / 2), seg((x1, y0), (x1, y1), wv, wh / 2, wh / 2))


def polar(p, ang, L):
    """Point at distance L from p, ang in degrees measured from +x, y down (so 120° = down-left)."""
    return (p[0] + L * math.cos(math.radians(ang)), p[1] + L * math.sin(math.radians(ang)))


PIE = 120     # 撇 direction: 60° below horizontal, leaning left
DOT = 70      # 点 direction: 70° below horizontal, leaning right


def build(ch, w=10.5, hr=0.86, cap="butt", dots=False):
    """dots=True renders the four 灬 and 虫's 丶 as round points."""
    wv, wh = w, w * hr
    r = cap == "round"
    jn = "round" if r else "miter"
    P = []
    if ch == "亿":
        a = (31.5, 4.5); b = polar(a, PIE, 51)
        P.append(seg(a, b, wv, cap=cap))
        top = _isect((22.6, 60), (0, -1), a, b)
        P.append(seg(top, (22.6, 96), wv, cap=cap) if r else seg(top, (22.6, 96), wv, cut0=(a, b)))
        P.append(pline([(40.5, 16.5), (84.5, 16.5), (46, 88.5), (90, 88.5), (90, 67)], wv, fil=[(2, 13)], join=jn, cap=cap))
    elif ch == "触":
        a = (23.5, 4); b = polar(a, PIE, 33.5)
        P.append(seg(a, b, wv, cap=cap))                                          # 撇
        h0 = _isect((0, 15), (1, 0), a, b)
        P.append(pline([h0, (37.5, 15), polar((37.5, 15), 115, 18.5)], wh, join=jn, cap=cap))  # 横撇
        top, m1, m2, bot = 32.5, 49.5, 66.5, 95.5
        xl, xr, xc = 15, 43.5, 29.25
        P.append(pline([(xl, top - (0 if r else wh / 2)), (xl, 72), polar((xl, 72), 108, 25)], wv, join=jn, cap=cap))  # 竖撇
        P.append(seg((xl, top), (xr, top), wh, 0 if r else wv / 2, 0 if r else wv / 2, cap=cap))
        P.append(seg((xr, top), (xr, bot), wv, 0 if r else wh / 2, 0, cap=cap))
        P.append(seg((xc, top), (xc, bot), wv, cap=cap))
        P.append(seg((xl, m1), (xr, m1), wh, cap=cap))
        P.append(seg((xl, m2), (xr, m2), wh, cap=cap))
        P.append(box(55.5, 28.5, 89, 58, wv, wh, cap=cap))                       # 口
        P.append(seg((72.25, 5), (72.25, 86), wv, cap=cap))                       # 中竖
        P.append(seg((51, 91.5), (91, 84.5), wh, cap=cap))                         # 提
        if dots:
            P.append(circle(83.6, 71.2, wv * 0.66))                               # 丶 as a true point
        else:
            P.append(seg((80, 65), polar((80, 65), 62, 13.5), wv, cap=cap))      # 丶
    elif ch == "点":
        P.append(seg((48.5, 4), (48.5, 39), wv, cap=cap))
        P.append(seg((48.5, 20.5), (89, 20.5), wh, cap=cap))
        P.append(box(21.5, 39, 79, 63.5, wv, wh, cap=cap))
        if dots:
            for x in (15, 38.3, 61.7, 85):
                P.append(circle(x, 84.5, wv * 0.7))
        else:
            P.append(seg((20, 72.5), polar((20, 72.5), PIE, 23), wv, cap=cap))
            for x in (38, 57.5, 77):
                P.append(seg((x, 72.5), polar((x, 72.5), DOT, 22.5), wv, cap=cap))
    return union(*P)


def word(chars="亿触点", w=10.5, track=4, **kw):
    return union(*[move(build(ch, w, **kw), i * (100 + track), 0) for i, ch in enumerate(chars)])
