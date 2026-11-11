"""Assets: logos, concept, construction, alphabet, Chinese, lockups, icons, clear space."""
import math
from kit import *
from wm import wordmark
from eptype import T, glyph, e_geom, g_n
import brand_f as BF

FL = fills("signal", "light"); FD = fills("signal", "dark")
WM = wordmark(T)


# ── logo files for the deck (transparent SVG) ──
def logos():
    for name, (items, box), mode in [("logo_stacked_dark", B.stacked(), "dark"), ("logo_stacked_light", B.stacked(), "light"),
                                     ("logo_inline_dark", B.inline(), "dark"), ("logo_inline_light", B.inline(), "light"),
                                     ("logo_word_dark", B.wordmark(), "dark"), ("logo_word_light", B.wordmark(), "light")]:
        s = BF.svg(items, box, "signal", mode, pad=4)
        open(os.path.join(OUT, name + ".svg"), "w").write(s)


# ── 01 concept: head and tail ──
def concept():
    W, H = 3328, 1300
    items, box = B.wordmark()
    it, s, bb = fit(items, box, 300, 360, w=2728)
    body = paint(it, FL)
    eb = bounds(it[1][0]); pb = bounds(it[2][0])
    ex, px = (eb[0] + eb[2]) / 2, (pb[0] + pb[2]) / 2
    top = bb[1]
    # arc from head to tail
    y0 = eb[1] - 70; y1 = pb[1] - 60; peak = top - 230
    body += (f'<path d="M{ex:.0f} {y0:.0f} C{ex + 400:.0f} {peak:.0f} {px + 330:.0f} {peak + 60:.0f} {px + 6:.0f} {y1:.0f}" fill="none" '
             f'stroke="{HEAD}" stroke-width="5" stroke-dasharray="4 18" stroke-linecap="round"/>')
    body += f'<circle cx="{px:.0f}" cy="{y1:.0f}" r="9" fill="{HEAD}"/><circle cx="{ex:.0f}" cy="{y0:.0f}" r="9" fill="none" stroke="{HEAD}" stroke-width="5"/>'
    base = bb[3]
    for cx_, t1, t2, anchor in [(ex, "首 · e", "Eon / Enterprise / 开端", "middle"), (px, "尾 · 句点", "Point / 落点 / 完成", "middle")]:
        body += f'<line x1="{cx_:.0f}" y1="{base + 40:.0f}" x2="{cx_:.0f}" y2="{base + 110:.0f}" stroke="{STEEL}" stroke-width="4"/>'
        body += zh(cx_, base + 190, t1, 64, INK, 600, anchor)
        body += mono(cx_, base + 256, t2, 36, STEEL, anchor)
    save("concept", W, H, body)


# ── 02 construction rules ──
def type_rules():
    W, H = 3328, 1400
    items, box = B.wordmark()
    it, s, bb = fit(items, box, 300, 380, w=2728)
    body = paint(it, FL)
    ox = bb[0] - box[0] * s; oy = 0
    # baseline offset: wordmark baseline maps to y where box y=0
    by = (0 - box[1]) * s + bb[1]
    pos = {(c, i): x for i, (c, x, w) in enumerate(WM["pos"])}
    X, V = T["X"], T["V"]
    def P_(x, y):
        return (bb[0] + (x - box[0]) * s, bb[1] + (y - box[1]) * s)
    # ① squircle outline on the first o
    o_x = WM["pos"][1][1]
    ry = X / 2 + T["ov"]; rx = ry + 0.6
    cx, cy = P_(o_x + rx, -X / 2)
    sq = ellipse(cx, cy, (rx + 7) * s, (ry + 7) * s, T["k"])
    body += f'<path d="{d(sq)}" fill="none" stroke="{STEEL}" stroke-width="4" stroke-dasharray="14 12"/>'
    body += zh(cx, bb[1] - 150, "① 超椭圆", 58, INK, 600, "middle") + mono(cx, bb[1] - 92, "所有圆形同一族 · k 0.62", 34, STEEL, "middle")
    # ② knife-cut crotches on n and p
    n_x = WM["pos"][2][1]; p_x = WM["pos"][3][1]
    Wn = 58; yc = -X * 0.5; ry_o = X + T["ov"] + yc; rx_i = Wn / 2 - T["Vr"] + T["crotch"]; cx_i = Wn - V - rx_i; ry_i = ry_o - T["Hh"]
    ny = yc - ry_i * math.sqrt(max(0, 1 - ((V - cx_i) / rx_i) ** 2))
    marks = [P_(n_x + V, ny + 2)]
    rxb = rx - T["Vr"] + T["crotch"]; cxb = 2 * rx - T["Vr"] - rxb
    dy = (ry - T["Hh"]) * math.sqrt(max(0, 1 - ((V - cxb) / rxb) ** 2))
    marks += [P_(p_x + V, -X / 2 - dy + 2), P_(p_x + V, -X / 2 + dy - 2)]
    for mx, my in marks:
        body += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="34" fill="none" stroke="{HEAD}" stroke-width="5"/>'
    lx = (marks[0][0] + marks[1][0]) / 2
    body += zh(lx, bb[3] + 150, "② 细刀口", 58, INK, 600, "middle") + mono(lx, bb[3] + 208, "笔画交汇处收细，小字号依然透气", 34, STEEL, "middle")
    # ③ true circles: i-dot and full stop
    i_x = WM["pos"][5][1]
    Dd = WM["D"]
    idc = P_(i_x + V / 2, -X - V * 0.62 - Dd / 2)
    pb = bounds(it[2][0]); pc = ((pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2)
    for (qx, qy) in (idc, pc):
        body += f'<circle cx="{qx:.0f}" cy="{qy:.0f}" r="{Dd * s / 2 + 26:.0f}" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="3 12" stroke-linecap="round"/>'
    rx3 = (idc[0] + pc[0]) / 2 + 60
    body += zh(rx3, bb[1] - 150, "③ 正圆", 58, INK, 600, "middle") + mono(rx3, bb[1] - 92, "只有“点”是正圆", 34, STEEL, "middle")
    save("type_rules", W, H, body)


# ── 03 the e opens exactly one point wide ──
def e_rule():
    W, H = 1800, 1500
    e, _, ew = glyph("e")
    G = e_geom(T)
    s = 11.6
    tx, ty = 150, 1080
    def Q(x, y):
        return (tx + x * s, ty + y * s)
    body = P(tf(e, s, 0, 0, s, tx, ty), HEAD)
    cx, cy = Q(*G["c"]); r = G["D"] / 2 * s
    P0 = Q(*G["P"]); th = G["th"]; L = 760
    body += f'<line x1="{P0[0]:.0f}" y1="{P0[1]:.0f}" x2="{P0[0] + L:.0f}" y2="{P0[1]:.0f}" stroke="{INK}" stroke-width="3"/>'
    body += f'<line x1="{P0[0]:.0f}" y1="{P0[1]:.0f}" x2="{P0[0] + L * math.cos(th):.0f}" y2="{P0[1] + L * math.sin(th):.0f}" stroke="{INK}" stroke-width="3"/>'
    body += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="10 9"/>'
    # the point it answers
    ppx = tx + (ew + T["V"] * 0.42) * s + r + 110
    body += f'<circle cx="{ppx:.0f}" cy="{ty - r:.0f}" r="{r:.0f}" fill="{HEAD}"/>'
    body += f'<line x1="60" y1="{ty:.0f}" x2="{W - 60}" y2="{ty:.0f}" stroke="{STEEL}" stroke-width="3" stroke-dasharray="10 10"/>'
    ax = P0[0] + 640 * math.cos(th / 2); ay = P0[1] + 640 * math.sin(th / 2)
    body += mono(ax + 10, ay + 14, f"{math.degrees(th):.0f}°", 44, INK)
    body += mono(cx + r + 30, cy - r - 20, "⌀ = 句点", 40, INK)
    body += mono(ppx, ty + 80, "句点", 40, STEEL, "middle")
    save("e_rule", W, H, body)


# ── 04 alphabet specimen ──
def alphabet():
    W, H = 3328, 1260
    cols, rows = 9, 3
    cw, ch = W / cols, H / rows
    xh = 150; sc = xh / T["X"]
    body = ""
    letters = list("abcdefghijklmnopqrstuvwxyz") + ["."]
    for r in range(rows):
        base = r * ch + ch * 0.66
        body += f'<line x1="0" y1="{base:.0f}" x2="{W}" y2="{base:.0f}" stroke="{FOG}" stroke-width="3"/>'
        body += f'<line x1="0" y1="{base - xh:.0f}" x2="{W}" y2="{base - xh:.0f}" stroke="{FOG}" stroke-width="3"/>'
    for i, c in enumerate(letters):
        r, k = divmod(i, cols)
        base = r * ch + ch * 0.66
        if c == ".":
            Dd = T["V"] * T["Dk"]
            ink = circle(Dd / 2, -Dd / 2, Dd / 2); dot = None; w = Dd
            col = HEAD
        else:
            ink, dot, w = glyph(c)
            col = HEAD if c == "e" else INK
        x = k * cw + (cw - w * sc) / 2
        body += P(tf(ink, sc, 0, 0, sc, x, base), col)
        if dot is not None:
            body += P(tf(dot, sc, 0, 0, sc, x, base), INK)
    save("alphabet", W, H, body)


# ── 05 Chinese lettering ──
def chinese():
    W, H = 1900, 1150
    g = B.cn_large
    s = 5.1
    tx, ty = 90, 150
    body = P(tf(g, s, 0, 0, s, tx, ty), INK)
    # mark the true points: 触's dot and 点's four dots
    pts = [(108 + 83.6, 71.2)] + [(216 + x, 84.5) for x in (15, 38.3, 61.7, 85)]
    for (x, y) in pts:
        body += f'<circle cx="{tx + x * s:.0f}" cy="{ty + y * s:.0f}" r="{9.4 * 0.7 * s + 16:.0f}" fill="none" stroke="{HEAD}" stroke-width="4"/>'
    body += mono(tx, ty + 100 * s + 120, "点画 = 正圆   ·   横画比竖画轻 14%   ·   与英文同一套笔画", 38, STEEL)
    save("chinese", W, H, body)


# ── 06 lockups ──
def lockups():
    W, H = 3328, 1420
    gap = 40
    cw = (W - gap) / 2; ch = (H - gap) / 2
    cards = [(B.stacked(), "中英组合 · 左对齐（主标志）"), (B.stacked_center(), "中英组合 · 居中"),
             (B.inline(), "单行组合"), (B.wordmark(), "英文字标")]
    body = ""
    for i, ((items, box), label) in enumerate(cards):
        r, k = divmod(i, 2)
        x, y = k * (cw + gap), r * (ch + gap)
        body += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="28" fill="{FOG}"/>'
        it, s, bb = fit(items, box, x + 160, y + 90, w=cw - 320, h=ch - 230)
        body += paint(it, FL)
        body += zh(x + 48, y + ch - 48, label, 40, STEEL, 500)
    save("lockups", W, H, body)


# ── 07 icon family ──
def icons():
    W, H = 3328, 1150
    body = ""
    S1 = 600
    xs = [0, 700, 1400]
    for x, (items, box), mode, label in [(xs[0], B.tile(S1), "light", "App 图标 · 深色"),
                                         (xs[1], B.tile(S1), "dark", "App 图标 · 浅色"),
                                         (xs[2], B.tile(S1, circle_tile=True), "light", "头像 · 企业微信 / 社媒")]:
        bgcard = f'<rect x="{x:.0f}" y="0" width="{S1 + 40}" height="{S1 + 40}" rx="40" fill="{INK if mode == "dark" else FOG}"/>'
        it = [(move(p, x + 20, 20), r) for p, r in items]
        body += bgcard + paint(it, fills("signal", mode))
        body += zh(x + 20, S1 + 140, label, 44, STEEL, 500)
    # favicon in a browser tab, real sizes at 2x
    fx = 2160
    body += f'<rect x="{fx}" y="0" width="1168" height="{S1 + 40}" rx="40" fill="{FOG}"/>'
    body += f'<rect x="{fx + 60}" y="80" width="1048" height="120" rx="22" fill="#FFFFFF"/>'
    it = [(move(p, fx + 92, 108), r) for p, r in B.tile(64, radius=0.22, frac=0.6)[0]]
    body += paint(it, FL) + zh(fx + 184, 158, "亿触点 · AI 触点服务", 40, INK, 500)
    xx = fx + 90
    for sz in (32, 48, 64, 96, 160):
        it = [(move(p, xx, 520 - sz), r) for p, r in B.tile(sz, radius=0.22, frac=0.6)[0]]
        body += paint(it, FL)
        body += mono(xx + sz / 2, 580, f"{sz // 2}", 30, STEEL, "middle")
        xx += sz + 60
    body += zh(fx + 20, S1 + 140, "Favicon · 16 / 24 / 32 / 48 / 80 px", 44, STEEL, 500)
    save("icons", W, H, body)


# ── 08 clear space & minimum size ──
def clearspace():
    W, H = 2000, 1250
    items, box = B.stacked()
    it, s, bb = fit(items, box, 360, 230, w=1280)
    unit = T["X"] / 2 * s            # half the x-height
    body = f'<rect x="{bb[0] - unit:.0f}" y="{bb[1] - unit:.0f}" width="{bb[2] - bb[0] + 2 * unit:.0f}" height="{bb[3] - bb[1] + 2 * unit:.0f}" fill="none" stroke="{STEEL}" stroke-width="3" stroke-dasharray="12 10"/>'
    body += f'<rect x="{bb[0]:.0f}" y="{bb[1]:.0f}" width="{bb[2] - bb[0]:.0f}" height="{bb[3] - bb[1]:.0f}" fill="none" stroke="{FOG}" stroke-width="3"/>'
    body += paint(it, FL)
    for (x, y) in [(bb[0] - unit, bb[1] - unit), (bb[2], bb[1] - unit), (bb[0] - unit, bb[3]), (bb[2], bb[3])]:
        body += f'<rect x="{x:.0f}" y="{y:.0f}" width="{unit:.0f}" height="{unit:.0f}" fill="{HEAD}" opacity="0.16"/>'
    body += mono(bb[0] - unit, bb[1] - unit - 26, "安全空间 = ½ x 高", 34, STEEL)
    save("clearspace", W, H, body)


if __name__ == "__main__":
    logos(); concept(); type_rules(); e_rule(); alphabet(); chinese(); lockups(); icons(); clearspace()
    print("ok")
