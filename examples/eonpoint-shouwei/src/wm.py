"""The eonpoint. wordmark set in EonPoint Display."""
import sys
sys.path.insert(0, '.')
from geo import *
from eptype import *

KERN = [0.5, 0.62, 1.02, 0.58, 0.62, 1.0, 0.62]   # e-o o-n n-p p-o o-i i-n n-t


def wordmark(S=T, period_gap=0.42):
    s = S["s"]; V = S["V"]
    seq = []
    for c in "eonpoint":
        ink, dot, w = glyph(c, S)
        seq.append((c, ink, dot, w))
    x = 0; e = None; rest = []; ix = 0; pos = []
    for idx, (c, ink, dot, w) in enumerate(seq):
        pos.append((c, x, w))
        p = move(ink, x, 0)
        if c == "e": e = p
        else: rest.append(p)
        if dot is not None: rest.append(move(dot, x, 0))
        x += w + (s * KERN[idx] if idx < len(KERN) else 0)
    Dd = V * S["Dk"]
    per = circle(x + V * period_gap + Dd / 2, -Dd / 2, Dd / 2)
    width = x + V * period_gap + Dd
    top = -S["X"] - V * 0.62 - Dd
    return dict(e=e, rest=union(*rest), period=per, width=width, top=top, bottom=S["D"], D=Dd, pos=pos)
