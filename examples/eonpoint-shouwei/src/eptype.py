"""EonPoint Display — a lowercase brand alphabet.
Rules: every round is the same squircle family; joins thin to a knife-cut crotch; terminals are cut
flat; only the points (i/j dots, full stop) are true circles."""
import math
from geo import *

T = dict(X=72, A=102, D=25, V=16.4, Vr=17.3, Hh=14.0, bar=13.0, ov=1.4, k=0.62, crotch=4.2, Dk=1.3, s=8.2)
BIG = 2000


def sq(cx, cy, rx, ry, k):
    return ellipse(cx, cy, rx, ry, k)


def R(x0, y0, x1, y1):
    return rect(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def half(side, v):
    return {"x>": R(v, -BIG, BIG, BIG), "x<": R(-BIG, -BIG, v, BIG), "y>": R(-BIG, v, BIG, BIG), "y<": R(-BIG, -BIG, BIG, v)}[side]


def mirror(p, W):
    return tf(p, -1, 0, 0, 1, W, 0)


def ring(cx, cy, rx, ry, S, k=None):
    k = k or S["k"]
    return diff(sq(cx, cy, rx, ry, k), sq(cx, cy, rx - S["Vr"], ry - S["Hh"], k + 0.012))


def o_dims(S):
    ry = S["X"] / 2 + S["ov"]; rx = ry + 0.6
    return rx, ry, -S["X"] / 2


# ── rounds ──
def g_o(S):
    rx, ry, cy = o_dims(S)
    return ring(rx, cy, rx, ry, S), 2 * rx


def g_c(S, half_angle=40):
    rx, ry, cy = o_dims(S)
    o = ring(rx, cy, rx, ry, S)
    a = math.radians(half_angle); L = 300
    wedge = poly([(rx + 6, cy), (rx + L * math.cos(a), cy - L * math.sin(a)), (rx + L, cy), (rx + L * math.cos(a), cy + L * math.sin(a))])
    return diff(o, wedge), 2 * rx


def e_geom(S):
    rx, ry, cy = o_dims(S)
    Vr, Hh = S["Vr"], S["Hh"]
    yb = cy - 1.6; ybb = yb + S["bar"] / 2
    Dd = S["V"] * S["Dk"]; r = Dd / 2
    mrx, mry = rx - Vr / 2, ry - Hh / 2
    c_y = ybb + r
    c_x = rx + mrx * math.sqrt(max(0.0, 1 - ((c_y - cy) / mry) ** 2))
    P = (rx, ybb)
    vx, vy = c_x - P[0], c_y - P[1]
    th = math.atan2(vy, vx) + math.asin(min(1.0, r / math.hypot(vx, vy)))
    return dict(rx=rx, ry=ry, cy=cy, yb=yb, ybb=ybb, D=Dd, c=(c_x, c_y), P=P, th=th)


def g_e(S):
    G = e_geom(S); rx, ry, cy = G["rx"], G["ry"], G["cy"]
    o = ring(rx, cy, rx, ry, S)
    bar = R(S["Vr"] - 1, G["yb"] - S["bar"] / 2, 2 * rx - S["Vr"] + 1, G["yb"] + S["bar"] / 2)
    P, th = G["P"], G["th"]; L = 300
    wedge = poly([P, (P[0] + L, P[1]), (P[0] + L * math.cos(th), P[1] + L * math.sin(th))])
    return diff(union(o, bar), wedge), 2 * rx


# ── bowl + stem family: a b d p q (g) ──
def bowlL(S):
    rx, ry, cy = o_dims(S); W = 2 * rx
    V, Vr, Hh, k = S["V"], S["Vr"], S["Hh"], S["k"]
    rxi = rx - Vr + S["crotch"]; cxi = W - Vr - rxi
    return diff(inter(sq(rx, cy, rx, ry, k), half("x>", V * 0.5)), sq(cxi, cy, rxi, ry - Hh, k + 0.012)), W


def g_p(S):
    b, W = bowlL(S); return union(R(0, -S["X"], S["V"], S["D"]), b), W


def g_b(S):
    b, W = bowlL(S); return union(R(0, -S["A"], S["V"], 0), b), W


def g_q(S):
    p, W = g_p(S); return mirror(p, W), W


def g_d(S):
    b, W = g_b(S); return mirror(b, W), W


def g_a(S):
    b, W = bowlL(S); return mirror(union(R(0, -S["X"], S["V"], 0), b), W), W


def hook_down_left(S, x_stem_right, y_top_of_hook, r_out, ext):
    """A descender hook: from a stem whose right edge is x_stem_right, curve down-left, ending flat."""
    V, Hh, k = S["V"], S["Hh"], S["k"]
    cx = x_stem_right - r_out; cy = y_top_of_hook
    rg = diff(sq(cx, cy, r_out, r_out, k), sq(cx, cy, r_out - V, r_out - Hh, k + 0.012))
    q = inter(rg, inter(half("x>", cx), half("y>", cy)))
    tail = R(cx - ext, cy + r_out - Hh, cx + 0.01, cy + r_out)
    return union(q, tail)


def g_g(S):
    b, W = bowlL(S); bowl = mirror(b, W)
    V, D = S["V"], S["D"] + 4
    r_out = 26
    stem = R(W - V, -S["X"], W, D - r_out + 0.01)
    hook = hook_down_left(S, W, D - r_out, r_out, ext=W * 0.42)
    return union(bowl, stem, hook), W


# ── arches: n h m r u ──
def g_n(S, W=58):
    X, V, Hh, ov, k = S["X"], S["V"], S["Hh"], S["ov"], S["k"]
    yc = -X * 0.5
    ry_o = X + ov + yc; rx_o = W / 2
    rx_i = rx_o - S["Vr"] + S["crotch"]; cx_i = W - V - rx_i; ry_i = ry_o - Hh
    outer = union(inter(sq(W / 2, yc, rx_o, ry_o, k), half("y<", yc)), R(W - V, yc - 0.01, W, 0))
    counter = union(inter(sq(cx_i, yc, rx_i, ry_i, k + 0.012), half("y<", yc)), R(cx_i - rx_i, yc - 0.01, W - V, 0))
    return union(R(0, -X, V, 0), diff(outer, counter)), W


def g_h(S):
    n, W = g_n(S); return union(n, R(0, -S["A"], S["V"], 0)), W


def g_m(S, Wa=47):
    n, _ = g_n(S, W=Wa)
    arch2 = diff(n, R(-1, -S["X"] - 5, S["V"], 1))          # second arch without its own stem
    return union(n, move(arch2, Wa - S["V"], 0)), 2 * Wa - S["V"]


def g_r(S):
    n, W = g_n(S, W=52)
    cut = W * 0.66
    return diff(n, half("x>", cut)), cut


def g_u(S):
    n, W = g_n(S); return tf(n, -1, 0, 0, -1, W, -S["X"]), W


# ── stems: i j l t f ──
def dot_at(S, x):
    Dd = S["V"] * S["Dk"]
    return circle(x, -S["X"] - S["V"] * 0.62 - Dd / 2, Dd / 2)


def g_i(S, with_dot=True):
    stem = R(0, -S["X"], S["V"], 0)
    return (stem, dot_at(S, S["V"] / 2)) if with_dot else stem, S["V"]


def g_j(S):
    V, D = S["V"], S["D"] + 4
    r_out = 22; ext = 12
    x0 = r_out - V + ext
    stem = R(x0, -S["X"], x0 + V, D - r_out + 0.01)
    hook = hook_down_left(S, x0 + V, D - r_out, r_out, ext)
    return (union(stem, hook), dot_at(S, x0 + V / 2)), x0 + V


def g_l(S):
    return R(0, -S["A"], S["V"], 0), S["V"]


def g_t(S, cl=9.0, cr=13.5, top=92):
    X, V, Hh = S["X"], S["V"], S["Hh"]
    return union(R(cl, -top, cl + V, 0), R(0, -X, cl + V + cr, -X + Hh)), cl + V + cr


def g_f(S, cl=9.0, cr=13.5):
    X, V, Hh, A, k = S["X"], S["V"], S["Hh"], S["A"], S["k"]
    r_out = 22
    cx = cl + r_out; cy = -A + r_out
    rg = diff(sq(cx, cy, r_out, r_out, k), sq(cx, cy, r_out - V, r_out - Hh, k + 0.012))
    q = inter(rg, inter(half("x<", cx), half("y<", cy)))
    tail = R(cx - 0.01, -A, cx + 10, -A + Hh)
    stem = R(cl, cy - 0.01, cl + V, 0)
    bar = R(0, -X, cl + V + cr, -X + Hh)
    return union(q, tail, stem, bar), max(cl + V + cr, cx + 10)


# ── diagonals: k v w x y z ──
def diag(x0, y0, x1, y1, wh):
    return poly([(x0 - wh / 2, y0), (x0 + wh / 2, y0), (x1 + wh / 2, y1), (x1 - wh / 2, y1)])


def wh_for(S, x0, y0, x1, y1, k=1.0):
    ang = math.atan2(abs(y1 - y0), abs(x1 - x0))
    return S["V"] * k / math.sin(ang)


def g_v(S, W=60):
    X = S["X"]
    wh = wh_for(S, 0, -X, W / 2, 0, 1.02)
    return union(diag(wh / 2, -X, W / 2, 0, wh), diag(W - wh / 2, -X, W / 2, 0, wh)), W


def g_w(S, W=88):
    X = S["X"]
    a = W / 4
    wh = wh_for(S, 0, -X, a, 0, 0.98)
    p = union(diag(wh / 2, -X, a, 0, wh), diag(2 * a, -X * 0.98, a, 0, wh), diag(2 * a, -X * 0.98, 3 * a, 0, wh), diag(W - wh / 2, -X, 3 * a, 0, wh))
    return inter(p, half("y>", -X)), W


def g_x(S, W=58):
    X = S["X"]
    wh = wh_for(S, 0, -X, W, 0, 1.0)
    return union(diag(wh / 2, -X, W - wh / 2, 0, wh), diag(W - wh / 2, -X, wh / 2, 0, wh)), W


def g_y(S, W=60):
    X, D = S["X"], S["D"]
    wh = wh_for(S, 0, -X, W / 2, 0, 1.02)
    slope = (W / 2 - (W - wh / 2)) / X           # dx per unit y on the right arm
    xb = W / 2 + slope * D
    return union(diag(wh / 2, -X, W / 2, 0, wh), diag(W - wh / 2, -X, xb, D, wh)), W


def g_z(S, W=54):
    X, Hh = S["X"], S["Hh"]
    wh = wh_for(S, W, -X + Hh, 0, -Hh, 1.0)
    d_ = diag(W - wh / 2, -X + Hh, wh / 2, -Hh, wh)
    return union(R(0, -X, W, -X + Hh), R(0, -Hh, W, 0), inter(d_, R(0, -X, W, 0))), W


def g_k(S, W=56):
    X, V, A = S["X"], S["V"], S["A"]
    wa = wh_for(S, V, -X * 0.32, W, -X, 0.96)
    arm = diag(V + wa * 0.15, -X * 0.30, W - wa / 2, -X, wa)
    jx = V + (W - V) * 0.36; jy = -X * 0.47
    wl = wh_for(S, jx, jy, W, 0, 1.0)
    leg = diag(jx, jy, W - wl / 2, 0, wl)
    body = inter(union(arm, inter(leg, half("y>", jy))), R(V - 1, -X, W, 0))
    return union(R(0, -A, V, 0), body), W


# ── s: two stacked squircle rings, spine where they overlap ──
def g_s(S, W=54):
    X, ov, Hh, k = S["X"], S["ov"], S["Hh"], S["k"]
    Tt = X + 2 * ov
    tot = (Tt + Hh) / 2
    ryu, ryl = tot * 0.485, tot * 0.515
    yu = -X - ov + ryu; yl = ov - ryl
    cx = W / 2
    up = ring(cx, yu, W / 2 - 1.6, ryu, S)
    lo = ring(cx, yl, W / 2, ryl, S)
    keep_u = union(half("x<", cx), half("y<", yu - ryu * 0.18))
    up = diff(inter(up, keep_u), inter(half("x>", cx), half("y>", yu - ryu * 0.18)))
    keep_l = union(half("x>", cx), half("y>", yl + ryl * 0.18))
    lo = diff(inter(lo, keep_l), inter(half("x<", cx), half("y<", yl + ryl * 0.18)))
    return union(up, lo), W


GLYPHS = dict(a=g_a, b=g_b, c=g_c, d=g_d, e=g_e, f=g_f, g=g_g, h=g_h, i=g_i, j=g_j, k=g_k, l=g_l, m=g_m,
              n=g_n, o=g_o, p=g_p, q=g_q, r=g_r, s=g_s, t=g_t, u=g_u, v=g_v, w=g_w, x=g_x, y=g_y, z=g_z)


def glyph(ch, S=T):
    """Returns (ink, dot_or_None, width)."""
    g, w = GLYPHS[ch](S)
    if isinstance(g, tuple):
        return g[0], g[1], w
    return g, None, w
