"""Loading and placing the SVG assets in assets/svg/."""
import html
import json
import math
import os
import re

from core.chrome import chrome, file_url, write_html
from core.config import ASSETS, CACHE

_uid = [0]


def new_id(prefix):
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


def esc(s):
    return html.escape(s or "")


def recolor(s, colors):
    for old, new in (colors or {}).items():
        s = s.replace(old, new)
    return s


def frag(path, colors=None):
    """An FFDec SVG export (path under assets/svg/) as an embeddable fragment: no <svg> wrapper or white stage, ids
    made unique. colors maps hex colours to replacements."""
    with open(os.path.join(ASSETS, "svg", path), encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"<\?xml[^>]*>|<svg[^>]*>|</svg>|<rect fill=\"#ffffff\" height=\"400\.0px\" width=\"550\.0px\"/>", "", s)
    prefix = new_id("u") + "_"
    s = re.sub(r'\bid="([^"]+)"', rf'id="{prefix}\1"', s)
    s = re.sub(r'((?:xlink:)?href)="#([^"]+)"', rf'\1="#{prefix}\2"', s)
    s = re.sub(r"url\(#([^)]+)\)", rf"url(#{prefix}\1)", s)
    return recolor(s.strip(), colors)


MEASURED = ("backs", "badges", "pieces")   # folders whose pieces get placed by their bounding box


def measure():
    """Bounding boxes of the placeable pieces in their own coordinates. Measured in Chrome and cached in
    .cache/bounds.json; anything new or changed since (by size and modification time) is measured again."""
    cache = os.path.join(CACHE, "bounds.json")
    names = [f"{d}/{f}" for d in MEASURED for f in sorted(os.listdir(os.path.join(ASSETS, "svg", d))) if f.endswith(".svg")]
    stamps = {n: "%d-%d" % ((st := os.stat(os.path.join(ASSETS, "svg", n))).st_size, st.st_mtime_ns) for n in names}
    cached = {}
    if os.path.exists(cache):
        with open(cache) as f:
            cached = json.load(f)
    if cached.get("stamps") == stamps:
        return cached["bounds"]
    parts = "".join(f'<svg data-name="{n}" width="10" height="10" viewBox="-3000 -3000 6000 6000">'
                    f'<g class="root">{frag(n)}</g></svg>' for n in names)
    page = (f"<!doctype html><body>{parts}<pre id=o></pre><script>const r={{}};"
            "document.querySelectorAll('svg[data-name]').forEach(s=>{"
            "const b=s.querySelector('g.root').getBBox();r[s.dataset.name]=[b.x,b.y,b.width,b.height]});"
            "document.getElementById('o').textContent='BBOX'+JSON.stringify(r)+'END'</script>")
    tmp = write_html("_measure.html", page)
    out = chrome("--virtual-time-budget=5000", "--dump-dom", file_url(tmp)).stdout
    os.remove(tmp)
    data = json.loads(out[out.index("BBOX") + 4: out.index("END")])
    os.makedirs(CACHE, exist_ok=True)
    with open(cache, "w") as f:
        json.dump({"stamps": stamps, "bounds": data}, f, indent=1)
    return data


BOUNDS = measure()


def piece(name, x, y, w=None, h=None):
    """A piece placed in HTML with its bounding box at (x, y) mm, width w or height h."""
    bx, by, bw, bh = BOUNDS[name]
    w = w if w is not None else h * bw / bh
    h = h if h is not None else w * bh / bw
    return (f'<svg class="piece" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm" '
            f'viewBox="{bx} {by} {bw} {bh}" preserveAspectRatio="none">{frag(name)}</svg>')


def nested(name, x, y, w, colors=None):
    """A piece placed inside another SVG (user units), bounding box at (x, y), width w."""
    bx, by, bw, bh = BOUNDS[name]
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{w * bh / bw:.2f}" '
            f'viewBox="{bx} {by} {bw} {bh}" overflow="visible">{frag(name, colors)}</svg>')


def star(cx, cy, r_out, r_in, points=8, **attrs):
    pts = " ".join(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}"
                   for i in range(points * 2)
                   for r, a in [(r_out if i % 2 == 0 else r_in, math.pi * i / points - math.pi / 2)])
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polygon points="{pts}" {extra}/>'
