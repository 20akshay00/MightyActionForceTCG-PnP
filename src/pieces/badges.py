"""Value badges: one badge design recoloured per value, Omegon's special badge, and the number drawn on top."""
import colorsys

from core.data import BADGES, FRAMES
from core.svg import BOUNDS, frag, new_id

CARD_RING = BADGES["card_ring"]   # where the badge's disc sits on the card (card units)


def _shade(hex_color, lightness, saturation):
    """hex_color with its HLS lightness and saturation mapped through the given functions."""
    hue, lum, sat = colorsys.rgb_to_hls(*(int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)))
    return "#" + "".join(f"{round(v * 255):02x}" for v in colorsys.hls_to_rgb(hue, lightness(lum), saturation(sat)))


def palette(c):
    """light, dark and outline colours for a card's badge. A card's own "badge" colour wins over the value's palette;
    missing shades are derived from light with ratios measured from the original blue and green badges."""
    p = {"light": c["badge"]} if "badge" in c else dict(BADGES["palette"].get(str(c["value"]), {}))
    p.setdefault("light", "#9aa3ad")
    p.setdefault("dark", _shade(p["light"], lambda v: v * .7, lambda v: v * .8))
    p.setdefault("outline", _shade(p["light"], lambda v: .18, lambda v: .38))
    return p


def badge(c):
    """(badge SVG, colour swaps, digit outline colour) for a card."""
    p = palette(c)
    special = BADGES["special"].get(str(c["value"]))
    if special and "badge" not in c:
        return special, None, p["outline"]
    base = BADGES["palette"]["4"]   # the base badge's own colours
    return BADGES["base"], {base[k]: p[k] for k in ("light", "dark", "outline")}, p["outline"]


def placed(name, ring, colors=None, digits=False):
    """A badge SVG scaled and moved so its disc lands on ring (x0, y0, x1, y1). digits keeps the original number."""
    bx, by, bw, bh = BOUNDS[name]
    rx0, ry0, rx1, _ = BADGES["rings"][name]
    k = (ring[2] - ring[0]) / (rx1 - rx0)
    svg = frag(name, colors)
    if digits:
        svg = svg.replace(' class="dg"', "")
    return (f'<svg x="{ring[0] - (rx0 - bx) * k:.2f}" y="{ring[1] - (ry0 - by) * k:.2f}" width="{bw * k:.2f}" '
            f'height="{bh * k:.2f}" viewBox="{bx} {by} {bw} {bh}" overflow="visible">{svg}</svg>')


def _centring(n, key):
    """Per-glyph centring from badges.json, measured so each number's ink lands on the badge's star. Glyphs
    that weren't measured use the average."""
    table = {d: v[key] for d, v in BADGES["digits"].items()}
    return table.get(n) or [sum(v[i] for v in table.values()) / len(table) for i in (0, 1)]


def value_digit(n, ring, outline):
    """The value in Grilled Cheese, centred on the badge's star, softened to sit in the art rather than on top of it."""
    n = str(n)
    x0, y0, x1, y1 = ring
    rh = y1 - y0
    fx, fy = _centring(n, "fix")
    star = 0.0674   # the starburst's rays meet 5.2 units up and right of the disc centre on every badge
    cx, cy = (x0 + x1) / 2 + rh * (star + 0.055 + fx), (y0 + y1) / 2 + rh * (-star - 0.035 + fy)
    size = rh * 0.64
    dx, dy = _centring(n, "ink")
    x, y = cx - dx * size, cy - dy * size
    sw, sh = size * 0.11, size * 0.045
    font = f"font:{size:.1f}px GrilledCheese;stroke-width:{sw:.2f}px"
    return (f'<text x="{x + sh:.2f}" y="{y + sh:.2f}" text-anchor="middle" style="{font};fill:#1c2a47;fill-opacity:.22;'
            f'stroke:#1c2a47;stroke-opacity:.22">{n}</text>'
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" style="{font};fill:#f6ecd0;stroke:{outline};'
            f'stroke-opacity:.8;paint-order:stroke;stroke-linejoin:round">{n}</text>')


def value_badge(c):
    name, colors, outline = badge(c)
    return placed(name, CARD_RING, colors) + value_digit(c["value"], CARD_RING, outline)


def corner_badge(c):
    """The top-right badge turned upside down into the bottom-left corner, so it can be read from across the table.
    The badge is drawn to sit flush in the card's corner, so it is scaled down from the corner point to stay flush
    with both edges, and clipped to the card's rounded outline to follow its curve."""
    k = BADGES["corner_scale"]
    rx, ry = FRAMES["corner_radius"]
    clip = new_id("cc")
    return (f'<clipPath id="{clip}"><rect width="280" height="400" rx="{rx}" ry="{ry}"/></clipPath>'
            f'<g clip-path="url(#{clip})"><g transform="translate(0 400) scale({k}) translate(0 -400) rotate(180 140 200)">'
            f'{value_badge(c)}</g></g>')


def original_badge(c):
    """The game's own badge, with its own number, for the original-card comparison."""
    return placed(f"badges/badge_{c['value']}.svg", CARD_RING, digits=True)
