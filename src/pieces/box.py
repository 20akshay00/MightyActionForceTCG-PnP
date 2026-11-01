"""The card-back look (maroon panels with gold arrows) and the tuck box."""
from core.config import CARD_H, CARD_W, GOLD, LOGO_IMG, MAROON
from core.svg import piece
from pieces.cards import card_front

BOX_W, BOX_H, BOX_D, TUCK = 68.0, 93.0, 20.0, 15.0   # inner size fits 30 cards in 66 x 91 mm sleeves


def arrows(w, h, opacity=.45):
    """Faint gold arrows, like on the card back, scattered over a w x h mm panel."""
    spots = [("pieces/arrow_large.svg", .55, .08, .5), ("pieces/arrow_small.svg", .05, .78, .32),
             ("pieces/arrow_small.svg", .6, .86, .28), ("pieces/arrow_large.svg", -.1, .35, .38)]
    return "".join(f'<div style="position:absolute;left:0;top:0;opacity:{opacity}">{piece(n, fx * w, fy * h, w=fw * w)}</div>'
                   for n, fx, fy, fw in spots)


def panel(x, y, w, h, inner="", border=True):
    frame = (f'<div style="position:absolute;inset:1.6mm;border:.7mm solid {GOLD};border-radius:1.6mm"></div>'
             if border else "")
    return (f'<div style="position:absolute;left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm;'
            f'overflow:hidden;background:{MAROON}">{arrows(w, h)}{frame}{inner}</div>')


def card_fan(cx, y, w):
    """Elf Archer, Omegon and K-Man fanned like a held hand, each w mm wide."""
    cards = [card_front("elf_archer", "clean"), card_front("omegon", "clean"), card_front("k_man", "worn")]
    s = w / CARD_W
    return "".join(
        f'<div style="position:absolute;left:{cx - w / 2 + dx * w:.2f}mm;top:{y + abs(rot) * 0.03 * w:.2f}mm;width:{w:.2f}mm;'
        f'height:{CARD_H * s:.2f}mm;transform-origin:50% 100%;transform:rotate({rot}deg);'
        f'filter:drop-shadow(0 .8mm 1mm rgba(0,0,0,.45))"><div style="transform-origin:0 0;transform:scale({s:.3f})">{svg}</div></div>'
        for svg, dx, rot in zip(cards, (-0.42, 0, 0.42), (-14, 0, 14)))


def tuck_box(x0, y0):
    """Printable tuck box net (cut solid, fold dashed). Returns (html, width, height) in mm."""
    W, H, D, T = BOX_W, BOX_H, BOX_D, TUCK
    df = D * 0.8
    ty, by = T + D, T + D + H
    xs = [0, D, D + W, 2 * D + W, 2 * D + 2 * W, 2 * D + 2 * W + 10]
    r = 9
    outline = (f"M0 {ty} L2 {ty - df} L{D - 2} {ty - df} L{D} {ty} "
               f"L{D + W / 2 - r} {ty} A{r} {r} 0 0 0 {D + W / 2 + r} {ty} L{D + W} {ty} "
               f"L{D + W + 2} {ty - df} L{2 * D + W - 2} {ty - df} L{2 * D + W} {ty} "
               f"L{2 * D + W} {ty - D} L{2 * D + W + 3} {ty - D - T + 3} Q{2 * D + W + 4} {ty - D - T} {2 * D + W + 8} {ty - D - T} "
               f"L{2 * D + 2 * W - 8} {ty - D - T} Q{2 * D + 2 * W - 4} {ty - D - T} {2 * D + 2 * W - 3} {ty - D - T + 3} "
               f"L{2 * D + 2 * W} {ty - D} L{2 * D + 2 * W} {ty} "
               f"L{xs[5]} {ty + 6} L{xs[5]} {by - 6} L{2 * D + 2 * W} {by} "
               f"L{2 * D + 2 * W} {by + D} L{2 * D + W} {by + D} L{2 * D + W} {by} "
               f"L{2 * D + W - 2} {by + df} L{D + W + 2} {by + df} L{D + W} {by} "
               f"L{D + W} {by + D} L{D} {by + D} L{D} {by} L{D - 2} {by + df} L2 {by + df} L0 {by} Z")
    folds = [f"M{x} {ty} V{by}" for x in xs[1:5]]
    folds += [f"M0 {ty} H{D}", f"M{D + W} {ty} H{2 * D + 2 * W}", f"M{2 * D + W} {ty - D} H{2 * D + 2 * W}",
              f"M0 {by} H{2 * D + 2 * W}"]

    def layer(inner):
        return (f'<svg class="piece" style="left:{x0}mm;top:{y0}mm;width:{xs[5]}mm;height:{by + D}mm" '
                f'viewBox="0 0 {xs[5]} {by + D}">{inner}</svg>')

    fx, bx = x0 + D, x0 + 2 * D + W
    title = (f'<div class="lbl" style="left:0;top:{H / 2 - 3.5}mm;width:{H}mm;margin-left:{D / 2 - H / 2}mm;text-align:center;'
             f'font:9.5pt GrilledCheese;color:{GOLD};transform:rotate(-90deg)">MIGHTY ACTION FORCE</div>')
    front = f'<img src="{LOGO_IMG}" style="position:absolute;left:3mm;top:5mm;width:{W - 6}mm">{card_fan(W / 2, 41, 25)}'
    back = (f'{piece("backs/clean.svg", (W - 52) / 2, 5, w=52)}'
            f'<div class="lbl" style="left:0;bottom:4.2mm;width:{W}mm;text-align:center;font:8pt GrilledCheese;color:{GOLD}">'
            '2 PLAYERS</div>')
    top = f'<img src="{LOGO_IMG}" style="position:absolute;left:{W / 2 - 17}mm;top:1.4mm;width:34mm">'
    parts = [layer(f'<path d="{outline}" fill="#e3ad3f"/>'),
             panel(x0, y0 + ty, D, H, title, border=False),
             panel(fx, y0 + ty, W, H, front),
             panel(x0 + D + W, y0 + ty, D, H, title, border=False),
             panel(bx, y0 + ty, W, H, back),
             panel(bx, y0 + ty - D, W, D, top, border=False),
             # thumb notch
             f'<div style="position:absolute;left:{fx + W / 2 - r}mm;top:{y0 + ty - r}mm;width:{2 * r}mm;height:{2 * r}mm;'
             'border-radius:50%;background:#fff"></div>',
             layer(f'<path d="{outline}" fill="none" stroke="#000" stroke-width=".3"/>'
                   f'<path d="{" ".join(folds)}" fill="none" stroke="#000" stroke-width=".25" stroke-dasharray="2 1.5"/>'),
             f'<div class="lbl" style="left:{x0 + 2 * D + 2 * W + 1}mm;top:{y0 + ty + H / 2 - 3}mm;font-size:6pt;'
             'color:#6b4a10;writing-mode:vertical-rl">glue</div>']
    return "".join(parts), xs[5], by + D
