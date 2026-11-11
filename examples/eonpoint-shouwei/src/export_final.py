import sys, os, subprocess, shutil
from geo import *
import brand_f as BF
from brand_f import Brand, CW
from eptype import glyph, T
OUT = sys.argv[1]
B = Brand()
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.mjs")
jobs = []
def put(folder, name, items_box, cw, mode, pad=20, png=None):
    d_ = os.path.join(OUT, folder); os.makedirs(d_, exist_ok=True)
    s = BF.svg(*items_box, cw, mode, pad=pad)
    p = os.path.join(d_, name + ".svg"); open(p, "w").write(s)
    if png: jobs.append((p, p[:-4] + ".png", png))
locks = {"wordmark": B.wordmark, "stacked": B.stacked, "stacked-center": B.stacked_center, "inline": B.inline}
for cw in CW:
    for ln, fn in locks.items():
        for mode in ("light", "dark"):
            put(f"01_标志_Logo/{cw}", f"eonpoint-{cw}-{ln}-{mode}", fn(), cw, mode, png=2400)
    for mode in ("mono", "mono-rev", "on-head"):
        put(f"01_标志_Logo/{cw}", f"eonpoint-{cw}-stacked-{mode}", B.stacked(), cw, mode, png=None)
        put(f"01_标志_Logo/{cw}", f"eonpoint-{cw}-wordmark-{mode}", B.wordmark(), cw, mode, png=None)
    put(f"02_图标_Icon/{cw}", f"eonpoint-{cw}-app-icon-dark", B.tile(1024), cw, "light", pad=0, png=1024)
    put(f"02_图标_Icon/{cw}", f"eonpoint-{cw}-app-icon-light", B.tile(1024), cw, "dark", pad=0, png=1024)
    put(f"02_图标_Icon/{cw}", f"eonpoint-{cw}-avatar", B.tile(512, circle_tile=True), cw, "light", pad=0, png=512)
    put(f"02_图标_Icon/{cw}", f"eonpoint-{cw}-favicon", B.tile(32, radius=0.22, frac=0.6), cw, "light", pad=0)
    put(f"02_图标_Icon/{cw}", f"eonpoint-{cw}-symbol", B.symbol(), cw, "light", pad=6, png=1024)
# Chinese wordmark, two weights
for nm, g in (("large-9.4", B.cn_large), ("small-10.2", B.cn_small)):
    put("03_中文字标_Chinese", f"亿触点-{nm}", ([(g, "ink")], bounds(g)), "signal", "light", pad=8, png=1800)
# alphabet: one svg per glyph
gd = os.path.join(OUT, "04_品牌字体_EonPoint-Display", "glyphs"); os.makedirs(gd, exist_ok=True)
for c in "abcdefghijklmnopqrstuvwxyz":
    ink, dot, w = glyph(c)
    parts = [ink] + ([dot] if dot is not None else [])
    g = union(*parts)
    b = (0, -T["A"] - 4, w, T["D"] + 6)
    open(os.path.join(gd, f"{c}.svg"), "w").write(svg([(g, "#0E0F11")], b, pad=4))
for src, dst, w in jobs:
    subprocess.run(["node", R, src, dst, str(w)], check=True)
print(len(jobs), "png")
