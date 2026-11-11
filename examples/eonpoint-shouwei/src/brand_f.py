"""EonPoint 首尾 — final identity system: parts, lockups, colourways, SVG output."""
import sys
sys.path.insert(0, '.')
from geo import *
from eptype import T, glyph
from wm import wordmark
import cn

# ── colourways ──
CW = {
    "signal":   dict(name="信号橙 × 碳黑", en="Signal", head="#FF4F1F", ink="#0E0F11", paper="#F4F5F6", fog="#E6E7E9", graphite="#2A2C30", steel="#8A8F96"),
    "klein":    dict(name="克莱因蓝 × 骨白", en="Klein", head="#2133E8", ink="#111214", paper="#ECEAE4", fog="#DEDBD3", graphite="#2A2B2F", steel="#8C8A85"),
    "infrared": dict(name="红外 × 银灰", en="Infrared", head="#E23D16", ink="#121314", paper="#D7D9DC", fog="#C6C9CD", graphite="#2A2C30", steel="#7E838A"),
}

CN_W = 10.8


class Brand:
    def __init__(self):
        W = wordmark(T)
        self.e, self.rest, self.period = W["e"], W["rest"], W["period"]
        self.w, self.top, self.bot, self.D = W["width"], W["top"], W["bottom"], W["D"]
        self.cn_small = union(*[move(cn.build(ch, 10.2, dots=True), i * 108, 0) for i, ch in enumerate("亿触点")])
        self.cn_large = union(*[move(cn.build(ch, 9.4, dots=True), i * 108, 0) for i, ch in enumerate("亿触点")])
        self.cn = self.cn_small
        self.cn_w = 308
        e_ink, _, ew = glyph("e")
        self.e_alone, self.e_w = e_ink, ew

    # roles: head / point / ink / rule / tile / on-tile
    def wordmark(self):
        return [(self.rest, "ink"), (self.e, "head"), (self.period, "point")], (0, self.top, self.w, self.bot)

    def stacked(self, scale=0.6, gap=40):
        y = self.bot + gap
        items = self.wordmark()[0] + [(tf(self.cn, scale, 0, 0, scale, 0, y), "ink")]
        return items, (0, self.top, self.w, y + 100 * scale)

    def stacked_center(self, scale=0.6, gap=40):
        y = self.bot + gap
        cw = self.cn_w * scale
        items = self.wordmark()[0] + [(tf(self.cn, scale, 0, 0, scale, (self.w - cw) / 2, y), "ink")]
        return items, (0, self.top, self.w, y + 100 * scale)

    def inline(self, scale=0.98):
        xr = self.w + 42
        items = self.wordmark()[0] + [(rect(xr, -72, xr + 2.4, 24), "rule"),
                                      (tf(self.cn_large, scale, 0, 0, scale, xr + 42, -76), "ink")]
        return items, (0, self.top, xr + 42 + self.cn_w * scale, max(self.bot, 24))

    def icon_parts(self):
        e = self.e_alone; b = bounds(e); Dd = self.D
        dot = circle(b[2] + T["V"] * 0.42 + Dd / 2, -Dd / 2, Dd / 2)
        return e, dot

    def symbol(self):
        e, dot = self.icon_parts()
        return [(e, "head"), (dot, "point")], bounds(union(e, dot))

    def tile(self, size=120, radius=0.225, frac=0.5, circle_tile=False, head_role="head"):
        e, dot = self.icon_parts()
        gb = bounds(union(e, dot)); h = gb[3] - gb[1]; w = gb[2] - gb[0]
        sc = size * frac / max(h, w * 0.82)
        tx = size / 2 - (gb[0] + gb[2]) / 2 * sc + size * 0.012
        ty = size / 2 - (gb[1] + gb[3]) / 2 * sc
        e2, d2 = tf(e, sc, 0, 0, sc, tx, ty), tf(dot, sc, 0, 0, sc, tx, ty)
        bg = circle(size / 2, size / 2, size / 2) if circle_tile else rrect(0, 0, size, size, size * radius, k=0.64)
        return [(bg, "tile"), (e2, head_role), (d2, "point")], (0, 0, size, size)


def fills(cw, mode):
    c = CW[cw]
    if mode == "light":        # on paper
        return dict(ink=c["ink"], head=c["head"], point=c["head"], rule=c["steel"], tile=c["ink"], **{"on-tile": c["paper"]})
    if mode == "dark":         # on ink
        return dict(ink=c["paper"], head=c["head"], point=c["head"], rule=c["graphite"], tile=c["paper"], **{"on-tile": c["ink"]})
    if mode == "on-head":      # everything in paper/ink on the head colour
        return dict(ink=c["ink"], head=c["paper"], point=c["paper"], rule=c["ink"], tile=c["ink"], **{"on-tile": c["head"]})
    if mode == "mono":
        return dict(ink=c["ink"], head=c["ink"], point=c["ink"], rule=c["ink"], tile=c["ink"], **{"on-tile": c["paper"]})
    if mode == "mono-rev":
        return dict(ink=c["paper"], head=c["paper"], point=c["paper"], rule=c["paper"], tile=c["paper"], **{"on-tile": c["ink"]})
    raise KeyError(mode)


def svg(items, box, cw="signal", mode="light", pad=0, bg=None, extra_fill=None):
    f = dict(fills(cw, mode)); f.update(extra_fill or {})
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    body = f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ""
    groups, order = {}, []
    for p, r in items:
        col = f[r]
        if col not in groups:
            groups[col] = []; order.append(col)
        groups[col].append(p)
    for col in order:
        ps = groups[col]
        body += f'<path d="{d(union(*ps) if len(ps) > 1 else ps[0])}" fill="{col}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}">{body}</svg>')
