"""Assets: colourways, colour modes, misuse, posters, motion, and application scenes."""
import math
from kit import *
import brand_f as BF
from eptype import T, glyph

FL = fills("signal", "light"); FD = fills("signal", "dark")


def X_mark(x, y, r, col="#D43A1A", w=6):
    return (f'<line x1="{x - r}" y1="{y - r}" x2="{x + r}" y2="{y + r}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<line x1="{x + r}" y1="{y - r}" x2="{x - r}" y2="{y + r}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


# ── colourways ──
def colourways():
    W, H = 3328, 1500
    gap = 40; pw = (W - 2 * gap) / 3
    sets = [("signal", "dark", "主色 · 信号橙 × 碳黑", "推荐"), ("klein", "light", "变色 · 克莱因蓝 × 骨白", "艺术先锋"),
            ("infrared", "light", "变色 · 红外 × 银灰", "工业")]
    body = ""
    for i, (cw, mode, label, tag) in enumerate(sets):
        c = CW[cw]; x = i * (pw + gap)
        bg = c["ink"] if mode == "dark" else c["paper"]
        fg = c["paper"] if mode == "dark" else c["ink"]
        body += f'<rect x="{x:.0f}" y="0" width="{pw:.0f}" height="{H}" rx="28" fill="{bg}"/>'
        it, s, bb = fit(*B.stacked(), x + 120, 300, w=pw - 240)
        body += paint(it, fills(cw, mode))
        body += zh(x + 70, 110, label, 44, fg, 600) + mono(x + pw - 70, 108, tag, 32, c["steel"], "end")
        sw = [(c["head"], "首尾色"), (c["ink"], "墨"), (c["paper"], "底"), (c["steel"], "灰")]
        sx = x + 70; sy = H - 360
        for col, nm in sw:
            body += f'<circle cx="{sx + 60:.0f}" cy="{sy + 60:.0f}" r="60" fill="{col}" stroke="{c["steel"]}" stroke-opacity="0.35" stroke-width="2"/>'
            body += mono(sx + 60, sy + 175, col, 26, fg, "middle", 0.75) + zh(sx + 60, sy + 222, nm, 28, c["steel"], 400, "middle")
            sx += (pw - 140) / 4
    save("colourways", W, H, body)


# ── colour modes ──
def modes():
    W, H = 3328, 1400
    gap = 40; cw = (W - 2 * gap) / 3; ch = (H - gap) / 2
    silver = ('<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1">'
              '<stop offset="0" stop-color="#F2F3F5"/><stop offset="0.45" stop-color="#9DA3AB"/>'
              '<stop offset="0.6" stop-color="#E4E6E9"/><stop offset="1" stop-color="#7C828A"/></linearGradient>')
    cards = [("light", PAPER, "标准 · 浅底"), ("dark", INK, "标准 · 深底"), ("on-head", HEAD, "品牌色底"),
             ("mono", "#FFFFFF", "单色 · 黑"), ("mono-rev", INK, "单色 · 反白"), ("foil", "#16171A", "特殊工艺 · 烫银")]
    body = ""
    for i, (mode, bg, label) in enumerate(cards):
        r, k = divmod(i, 3)
        x, y = k * (cw + gap), r * (ch + gap)
        body += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="26" fill="{bg}" stroke="#D9DBDE" stroke-width="{2 if bg == "#FFFFFF" else 0}"/>'
        it, s, bb = fit(*B.wordmark(), x + 120, y + 130, w=cw - 240, h=ch - 300)
        if mode == "foil":
            body += paint(it, {"ink": "url(#ag)", "head": "url(#ag)", "point": "url(#ag)"})
        else:
            body += paint(it, fills("signal", mode))
        lc = STEEL if bg in (PAPER, "#FFFFFF") else ("#FFFFFF" if bg == HEAD else "#8A8F96")
        body += zh(x + 44, y + ch - 44, label, 38, lc, 500)
    save("modes", W, H, body, defs=silver)


# ── misuse ──
def donts():
    W, H = 3328, 1300
    gap = 40; cw = (W - 2 * gap) / 3; ch = (H - gap) / 2
    items, box = B.wordmark()
    body = ""
    specs = ["拉伸变形", "首尾只着色一处", "更换首尾颜色", "添加描边或阴影", "随意调整字距", "低对比背景"]
    for i, label in enumerate(specs):
        r, k = divmod(i, 3)
        x, y = k * (cw + gap), r * (ch + gap)
        bg = PAPER if i != 5 else "#B9BCC1"
        body += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="26" fill="{bg}"/>'
        f = dict(FL)
        its = items
        if i == 2:
            f["head"] = "#2BB673"; f["point"] = "#2BB673"
        if i == 1:
            f["head"] = INK
        it, s, bb = fit(its, box, x + 140, y + 120, w=cw - 280, h=ch - 300)
        if i == 0:
            cxm = (bb[0] + bb[2]) / 2; cym = (bb[1] + bb[3]) / 2
            it = [(tf(p, 1.25, 0, 0, 0.72, cxm - 1.25 * cxm, cym - 0.72 * cym), rr) for p, rr in it]
        if i == 3:
            body += paint([(move(p, 14, 18), "#9AA0A8") for p, rr in it], {})
        if i == 4:
            # spread letters apart
            new = []
            xs = [bounds(p)[0] for p, rr in it]
            for j, (p, rr) in enumerate(it):
                new.append((p, rr))
            it = new
            body += ""
        if i == 5:
            f = {"ink": "#8E9298", "head": "#C9784E", "point": "#C9784E"}
        if i == 4:
            ws = BF.Brand()
            # reset with a tracked version made from separate letters
            from wm import wordmark as _wm
            from eptype import glyph as _g
            xx = 0; parts = []
            for c in "eonpoint":
                g, dt, w = _g(c)
                parts.append((move(g, xx, 0), "head" if c == "e" else "ink"))
                if dt is not None: parts.append((move(dt, xx, 0), "ink"))
                xx += w + 30
            Dd = T["V"] * T["Dk"]
            parts.append((circle(xx + Dd / 2, -Dd / 2, Dd / 2), "point"))
            it, s, bb = fit(parts, (0, -104, xx + Dd, 25), x + 100, y + 120, w=cw - 200, h=ch - 300)
        body += paint(it, f)
        if i == 3:
            pass
        body += X_mark(x + cw - 70, y + 70, 22)
        body += zh(x + 44, y + ch - 44, label, 38, STEEL if i != 5 else "#2A2C30", 500)
    save("donts", W, H, body)


# ── posters ──
def posters():
    W, H = 3328, 1560
    gap = 60; pw = (W - 2 * gap) / 3; ph = H
    body = ""
    defs = "".join(f'<clipPath id="pc{i}"><rect x="{i * (pw + gap):.0f}" y="0" width="{pw:.0f}" height="{ph}" rx="8"/></clipPath>' for i in range(3))
    defs += shadow_def("psh", 24, 30, 0.22)
    # P1: giant e on carbon
    x = 0
    body += f'<g filter="url(#psh)"><rect x="{x}" y="0" width="{pw:.0f}" height="{ph}" rx="8" fill="{INK}"/></g><g clip-path="url(#pc0)">'
    e, _, ew = glyph("e")
    body += P(tf(e, 15.5, 0, 0, 15.5, x - 520, ph + 180), HEAD)
    body += zh(x + 70, 150, "从亿，到点。", 76, PAPER, 600)
    body += mono(x + 72, 214, "EON → POINT", 30, STEEL, ls=4)
    it, s, bb = fit(*B.inline(), x + pw - 520, ph - 120, w=450)
    body += paint(it, FD) + "</g>"
    # P2: point. on paper
    x = pw + gap
    body += f'<g filter="url(#psh)"><rect x="{x:.0f}" y="0" width="{pw:.0f}" height="{ph}" rx="8" fill="{PAPER}"/></g><g clip-path="url(#pc1)">'
    ink, dots, w = brand_text("point", 190)
    body += P(move(ink, x + 70, 860), INK) + P(move(dots, x + 70, 860), INK)
    Dd = T["V"] * T["Dk"] * 190 / T["X"]
    body += f'<circle cx="{x + 70 + w + 40 + Dd / 2:.0f}" cy="{860 - Dd / 2:.0f}" r="{Dd / 2:.0f}" fill="{HEAD}"/>'
    body += zh(x + 70, 1180, "每一个任务，", 64, INK, 600) + zh(x + 70, 1268, "都以一个确定的点结束。", 64, INK, 600)
    body += mono(x + 72, 150, "AI · AGENT · CLOUD · SAAS", 30, STEEL, ls=3)
    it, s, bb = fit(*B.wordmark(), x + 70, ph - 150, w=330)
    body += paint(it, FL) + "</g>"
    # P3: a field of points on signal orange
    x = 2 * (pw + gap)
    body += f'<g filter="url(#psh)"><rect x="{x:.0f}" y="0" width="{pw:.0f}" height="{ph}" rx="8" fill="{HEAD}"/></g><g clip-path="url(#pc2)">'
    step = 46; r0 = 5
    for j in range(5, 26):
        for k in range(1, 22):
            cx, cy = x + k * step, j * step + 40
            body += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r0}" fill="{INK}" opacity="0.22"/>'
    body += f'<circle cx="{x + 14 * step:.0f}" cy="{16 * step + 40:.0f}" r="34" fill="{INK}"/>'
    body += zh(x + 70, 150, "亿万个触点，", 72, INK, 600) + zh(x + 70, 240, "落于一点。", 72, INK, 600)
    it, s, bb = fit(*B.inline(), x + 70, ph - 120, w=450)
    body += paint(it, {"ink": INK, "head": PAPER, "point": PAPER, "rule": INK}) + "</g>"
    save("posters", W, H, body, defs=defs)


# ── motion storyboard ──
def motion():
    W, H = 3328, 900
    gap = 36; fw = (W - 3 * gap) / 4; fh = fw * 9 / 16
    items, box = B.wordmark()
    body = ""
    labels = ["起笔 · e 出现", "书写 · 字母依次展开", "落点 · 句点从 i 上落下", "定格 · 中英组合"]
    for i in range(4):
        x = i * (fw + gap)
        body += f'<rect x="{x:.0f}" y="0" width="{fw:.0f}" height="{fh:.0f}" rx="18" fill="{INK}"/>'
        if i == 0:
            it, s, bb = fit([(B.e, "head")], bounds(B.e), x + fw / 2 - 80, fh / 2 - 80, w=160, h=160)
            body += paint(it, FD)
        elif i in (1, 2):
            it, s, bb = fit(items, box, x + 60, 0, w=fw - 120, h=fh)
            if i == 1:
                it = [it[0], it[1]]
            else:
                it = [it[0], it[1]]
                pb = bounds(fit(items, box, x + 60, 0, w=fw - 120, h=fh)[0][2][0])
                pc = ((pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2)
                # i-dot location ≈ 0.69 of word width, above x-height
                bbw = fit(items, box, x + 60, 0, w=fw - 120, h=fh)[2]
                ix = bbw[0] + (bbw[2] - bbw[0]) * 0.672; iy = bbw[1] + (pb[3] - pb[1]) * 0.55
                body += (f'<path d="M{ix:.0f} {iy:.0f} Q{(ix + pc[0]) / 2:.0f} {iy - 120:.0f} {pc[0] - 8:.0f} {pc[1] - 30:.0f}" fill="none" '
                         f'stroke="{HEAD}" stroke-width="4" stroke-dasharray="3 12" stroke-linecap="round"/>')
                r = (pb[2] - pb[0]) / 2
                body += f'<circle cx="{(ix + pc[0]) / 2 + 40:.0f}" cy="{iy - 50:.0f}" r="{r:.1f}" fill="{HEAD}"/>'
            body += paint(it, FD)
        else:
            it, s, bb = fit(*B.stacked(), x + 120, 40, w=fw - 240, h=fh - 80)
            body += paint(it, FD)
        body += mono(x + 6, fh + 70, f"0{i + 1}", 34, HEAD) + zh(x + 70, fh + 70, labels[i], 38, INK, 500)
    save("motion", W, H, body)


# ── digital: website + agent chat ──
def digital():
    W, H = 3328, 1700
    body = f'<rect width="{W}" height="{H}" fill="{FOG}"/>'
    defs = shadow_def("ds", 30, 40, 0.18)
    # browser
    bx, by, bw, bh = 120, 130, 2140, 1420
    body += f'<g filter="url(#ds)"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="#FFFFFF"/></g>'
    for j, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        body += f'<circle cx="{bx + 50 + j * 36}" cy="{by + 44}" r="11" fill="#D5D7DA"/>'
    body += f'<rect x="{bx + 180}" y="{by + 18}" width="420" height="54" rx="14" fill="{FOG}"/>'
    it = [(move(p, bx + 198, by + 27), r) for p, r in B.tile(36, radius=0.22, frac=0.6)[0]]
    body += paint(it, FL) + zh(bx + 250, by + 56, "亿触点 · 企业 AI 触点", 26, INK, 500)
    hx, hy, hw, hh = bx, by + 90, bw, bh - 90
    defs += f'<clipPath id="hero"><rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="0"/></clipPath>'
    body += f'<g clip-path="url(#hero)"><rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" fill="{INK}"/>'
    e, _, ew = glyph("e")
    body += P(tf(e, 11.5, 0, 0, 11.5, hx + hw - 760, hy + hh + 140), HEAD, 'opacity="0.95"')
    it, s, bb = fit(*B.inline(), hx + 80, hy + 54, w=420)
    body += paint(it, FD)
    for j, m in enumerate(["产品", "解决方案", "授权代理", "关于我们"]):
        body += zh(hx + 1120 + j * 165, hy + 92, m, 30, "#AEB2B8", 500)
    body += f'<rect x="{hx + hw - 300}" y="{hy + 56}" width="200" height="60" rx="30" fill="{HEAD}"/>' + zh(hx + hw - 200, hy + 96, "预约演示", 28, "#FFFFFF", 600, "middle")
    body += zh(hx + 80, hy + 470, "让每一家企业，", 104, PAPER, 600)
    body += zh(hx + 80, hy + 610, "都拥有自己的 AI 触点", 104, PAPER, 600) + zh(hx + 80 + 984, hy + 610, "。", 104, HEAD, 600)
    body += zh(hx + 84, hy + 720, "Agent 研发 · AI 软件 · 企业软件授权与实施", 36, "#9DA2A9", 400)
    body += f'<rect x="{hx + 80}" y="{hy + 800}" width="260" height="76" rx="38" fill="{HEAD}"/>' + zh(hx + 210, hy + 850, "开始对话", 32, "#FFFFFF", 600, "middle")
    body += f'<rect x="{hx + 360}" y="{hy + 800}" width="260" height="76" rx="38" fill="none" stroke="#4A4D52" stroke-width="2"/>' + zh(hx + 490, hy + 850, "了解方案", 32, PAPER, 500, "middle")
    body += mono(hx + 80, hy + hh - 70, "AI · AGENT · CLOUD · SAAS · SOFTWARE · LICENSING", 26, "#6C7077", ls=4)
    body += "</g>"
    # phone with agent chat
    px, py, pw, ph = 2420, 70, 760, 1560
    body += f'<g filter="url(#ds)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="96" fill="#111214"/></g>'
    sx, sy, sw, sh = px + 22, py + 22, pw - 44, ph - 44
    body += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="76" fill="#F6F7F8"/>'
    body += f'<rect x="{px + pw / 2 - 90}" y="{py + 44}" width="180" height="44" rx="22" fill="#111214"/>'
    body += mono(sx + 70, sy + 74, "9:41", 30, INK)
    body += f'<rect x="{sx}" y="{sy + 120}" width="{sw}" height="120" fill="#FFFFFF"/>'
    it = [(move(p, sx + 40, sy + 140), r) for p, r in B.tile(80, circle_tile=True)[0]]
    body += paint(it, FL) + zh(sx + 140, sy + 188, "亿触点 Agent", 34, INK, 600) + zh(sx + 140, sy + 226, "在线", 24, STEEL, 400)
    def bubble(y, text, me=False, w=520, lines=None):
        lines = lines or [text]
        h = 40 + 46 * len(lines)
        x = sx + sw - 40 - w if me else sx + 130
        out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{INK if me else "#FFFFFF"}"/>'
        for k, ln in enumerate(lines):
            out += zh(x + 30, y + 58 + 46 * k, ln, 28, PAPER if me else INK, 400)
        if not me:
            it2 = [(move(p, sx + 40, y), r) for p, r in B.tile(66, circle_tile=True)[0]]
            out += paint(it2, FL)
        return out, h
    y = sy + 300
    for text, me, lines in [("", False, ["本周 3 场会议纪要已整理，", "共 5 项待办，已同步到日程"]),
                            ("", True, ["好的，把待办发给项目组"]), ("", False, ["已发送给 12 位成员"])]:
        b_, h = bubble(y, text, me, 540 if not me else 460, lines); body += b_; y += h + 40
    # the brand moment: a finished task ends with the point
    body += f'<rect x="{sx + 130}" y="{y}" width="300" height="86" rx="28" fill="#FFFFFF"/>'
    it2 = [(move(p, sx + 40, y), r) for p, r in B.tile(66, circle_tile=True)[0]]
    body += paint(it2, FL) + zh(sx + 160, y + 56, "任务完成", 28, INK, 600) + f'<circle cx="{sx + 300}" cy="{y + 48}" r="9" fill="{HEAD}"/>'
    body += f'<rect x="{sx + 40}" y="{sy + sh - 150}" width="{sw - 80}" height="86" rx="43" fill="#FFFFFF" stroke="#E1E3E6" stroke-width="2"/>'
    body += zh(sx + 80, sy + sh - 94, "给 Agent 发消息…", 28, "#A3A7AD", 400)
    body += f'<circle cx="{sx + sw - 92}" cy="{sy + sh - 107}" r="30" fill="{HEAD}"/>'
    save("digital", W, H, body, defs=defs)


# ── print: business cards, letterhead, badge ──
def printed():
    W, H = 3328, 1700
    body = f'<rect width="{W}" height="{H}" fill="#D9DBDE"/>'
    defs = shadow_def("ps", 22, 30, 0.22)
    # letterhead (A4)
    lx, ly, lw = 120, 120, 1040; lh = lw * 1.414
    body += f'<g filter="url(#ps)"><rect x="{lx}" y="{ly}" width="{lw}" height="{lh:.0f}" fill="#FFFFFF"/></g>'
    it, s, bb = fit(*B.stacked(), lx + 90, ly + 100, w=300)
    body += paint(it, FL)
    body += zh(lx + lw - 90, ly + 140, "亿触点 EonPoint", 22, STEEL, 400, "end")
    body += mono(lx + lw - 90, ly + 176, "AI · AGENT · CLOUD · SAAS", 18, STEEL, "end")
    yy = ly + 420
    for k in range(13):
        ww = lw - 180 - (220 if k % 4 == 3 else 0)
        body += f'<rect x="{lx + 90}" y="{yy}" width="{ww}" height="12" rx="6" fill="#E6E7E9"/>'; yy += 44 + (40 if k % 4 == 3 else 0)
    body += f'<rect x="{lx + 90}" y="{ly + lh - 120:.0f}" width="{lw - 180}" height="2" fill="#E6E7E9"/>'
    body += mono(lx + 90, ly + lh - 76, "AI · AGENT · CLOUD · SAAS · SOFTWARE · LICENSING", 18, STEEL, ls=3)
    body += f'<circle cx="{lx + lw - 100}" cy="{ly + lh - 82:.0f}" r="8" fill="{HEAD}"/>'
    # business cards (90 x 54)
    cw_, chh = 1000, 600
    cx1, cy1 = 1300, 160
    body += f'<g filter="url(#ps)"><rect x="{cx1}" y="{cy1}" width="{cw_}" height="{chh}" rx="16" fill="{INK}"/></g>'
    it, s, bb = fit(*B.wordmark(), cx1 + 200, cy1 + 150, w=cw_ - 400, h=chh - 300)
    body += paint(it, FD)
    cx2, cy2 = 1420, 860
    body += f'<g filter="url(#ps)"><rect x="{cx2}" y="{cy2}" width="{cw_}" height="{chh}" rx="16" fill="{PAPER}"/></g>'
    it, s, bb = fit(*B.inline(), cx2 + 70, cy2 + 70, w=420)
    body += paint(it, FL)
    body += zh(cx2 + 70, cy2 + 330, "姓名 Name", 52, INK, 600) + zh(cx2 + 70, cy2 + 384, "解决方案顾问 · Solutions Consultant", 28, STEEL, 400)
    body += mono(cx2 + 70, cy2 + 488, "[联系方式占位]", 24, INK)
    body += zh(cx2 + 70, cy2 + 536, "[所在城市 · 占位]", 24, STEEL, 400)
    body += f'<circle cx="{cx2 + cw_ - 70}" cy="{cy2 + chh - 70}" r="12" fill="{HEAD}"/>'
    # badge
    bx, by, bw, bh = 2560, 300, 620, 940
    body += f'<rect x="{bx + bw / 2 - 40}" y="0" width="80" height="{by + 40}" fill="{HEAD}"/>'
    body += f'<g filter="url(#ps)"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="30" fill="{INK}"/></g>'
    body += f'<rect x="{bx + bw / 2 - 70}" y="{by + 40}" width="140" height="22" rx="11" fill="#2A2C30"/>'
    it = [(move(p, bx + 70, by + 140), r) for p, r in B.tile(150)[0]]
    body += paint(it, FD)
    body += zh(bx + 70, by + 560, "姓名", 72, PAPER, 600) + zh(bx + 70, by + 630, "Agent 产品部", 32, "#9DA2A9", 400)
    it, s, bb = fit(*B.wordmark(), bx + 70, by + bh - 150, w=300)
    body += paint(it, FD)
    save("print", W, H, body, defs=defs)


# ── space: reception wall, booth, tote ──
def space():
    W, H = 3328, 1700
    body = ""
    defs = shadow_def("ws", 14, 10, 0.28) + shadow_def("ss", 26, 34, 0.22)
    # reception wall
    body += f'<rect width="2100" height="{H}" fill="#E4E5E7"/>'
    body += f'<rect x="0" y="1230" width="2100" height="{H - 1230}" fill="#CFD1D4"/>'
    it, s, bb = fit(*B.stacked(), 330, 360, w=1440)
    body += f'<g filter="url(#ws)">' + paint(it, FL) + '</g>'
    body += f'<rect x="560" y="1110" width="980" height="240" rx="12" fill="{INK}"/>'
    body += f'<rect x="560" y="1110" width="980" height="22" rx="8" fill="#2A2C30"/>'
    body += f'<circle cx="1490" cy="1240" r="14" fill="{HEAD}"/>'
    # booth panel
    x0 = 2160
    body += f'<rect x="{x0}" y="0" width="{W - x0}" height="{H}" fill="#C9CCD0"/>'
    body += f'<g filter="url(#ss)"><rect x="{x0 + 90}" y="120" width="580" height="1380" rx="10" fill="{INK}"/></g>'
    defs += f'<clipPath id="bp"><rect x="{x0 + 90}" y="120" width="580" height="1380" rx="10"/></clipPath>'
    e, _, ew = glyph("e")
    body += f'<g clip-path="url(#bp)">' + P(tf(e, 9.6, 0, 0, 9.6, x0 + 30, 1060), HEAD)
    Dd = T["V"] * T["Dk"] * 9.6
    body += f'<circle cx="{x0 + 30 + (ew + 7) * 9.6 + Dd / 2:.0f}" cy="{1060 - Dd / 2:.0f}" r="{Dd / 2:.0f}" fill="{HEAD}"/>'
    body += zh(x0 + 150, 1230, "让每一家企业，", 46, PAPER, 600) + zh(x0 + 150, 1296, "都拥有 AI 触点。", 46, PAPER, 600)
    it, s, bb = fit(*B.wordmark(), x0 + 150, 1380, w=260)
    body += paint(it, FD) + "</g>"
    # tote
    tx, ty = x0 + 740, 620
    body += f'<path d="M{tx + 90} {ty} C{tx + 90} {ty - 230} {tx + 330} {ty - 230} {tx + 330} {ty}" fill="none" stroke="#D8D1C4" stroke-width="26"/>'
    body += f'<g filter="url(#ss)"><rect x="{tx}" y="{ty}" width="420" height="520" rx="8" fill="#ECE7DD"/></g>'
    it = [(move(p, tx + 110, ty + 150), r) for p, r in B.tile(200, frac=0.52)[0]]
    body += paint([(p, r) for p, r in it if r != "tile"], {"head": HEAD, "point": HEAD})
    it, s, bb = fit(*B.wordmark(), tx + 110, ty + 420, w=200)
    body += paint(it, FL)
    save("space", W, H, body, defs=defs)


if __name__ == "__main__":
    colourways(); modes(); donts(); posters(); motion(); digital(); printed(); space()
    print("ok")
