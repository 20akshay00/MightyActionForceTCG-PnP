"""The rules booklet: eight pages from templates/rules/, folded from one landscape sheet."""
import os

from core.config import LOGO_IMG, PLAYER, TEMPLATES
from core.data import DECKS, RULES, card
from core.svg import esc, piece
from core.templates import fill
from pieces.box import arrows, card_fan
from pieces.cards import portrait
from pieces.table_cards import reveal_order

ZINE_W, ZINE_H = 66.0, 90.0   # folded page size: fits in the tuck box


def card_list(ids, style):
    cards = sorted((card(i, style) for i in ids), key=lambda c: -c["value"])
    return " · ".join(f'<span>{esc(c["name"])} {c["value"]}</span>' for c in cards)


def deck_lists():
    """The base decks and extras by name and value."""
    red, yellow = DECKS["red"], DECKS["yellow"]
    both = [c for c in red["deck"] if c in yellow["deck"]]
    rows = [("Both decks", card_list(both, red["style"])),
            ("Red only", card_list([c for c in red["deck"] if c not in both], red["style"])),
            ("Yellow only", card_list([c for c in yellow["deck"] if c not in both], yellow["style"])),
            ("Extras", card_list(DECKS["extras"], "clean"))]
    return '<div class="decks">' + "".join(f"<p><b>{k}</b> {v}</p>" for k, v in rows) + "</div>"


def zine_pages():
    """The eight pages, in reading order, with everything that depends on the decks filled in."""
    deck_size = len(DECKS["red"]["deck"])
    extras = sorted((card(i, "clean") for i in DECKS["extras"]), key=lambda c: c["value"])   # unlock order
    values = dict(
        arrows=arrows(ZINE_W, ZINE_H), logo=LOGO_IMG, fan=card_fan(ZINE_W / 2, 52, 21),
        card_back=piece("backs/clean.svg", (ZINE_W - 36) / 2, 7, w=36),
        gem_red=f'<span class="zgem">{piece(PLAYER["red"]["gem"], 0, 0, w=3.4)}</span>',
        gem_yellow=f'<span class="zgem">{piece(PLAYER["yellow"]["gem"], 0, 0, w=3.4)}</span>',
        deck_size=deck_size, extras_count=len(extras), collection_size=deck_size + len(extras),
        deck_lists=deck_lists(), reveal_order=reveal_order("link"),
        effects="".join(f'<div class="fx">{portrait(e["card"], 9.5)}<div><b>{e["name"]}</b> <i>{e["powers"]}</i>'
                        f'<br>{e["long"]}</div></div>' for e in RULES["effects"]),
        extras_portraits="".join(portrait(c["id"], 9.5) for c in reversed(extras)),
        unlock_order=", then ".join(esc(c["name"]) for c in extras))
    return [fill(f"rules/{name}", **values) for name in sorted(os.listdir(os.path.join(TEMPLATES, "rules")))]


def zine_sheet(paper):
    """The booklet on one landscape page. The top row is printed upside down; cut the centre slit and fold."""
    ph, pw = paper
    x0, y0 = (pw - 4 * ZINE_W) / 2, (ph - 2 * ZINE_H) / 2
    pages = zine_pages()
    parts = []
    for r, row in enumerate([[5, 4, 3, 2], [6, 7, 8, 1]]):
        for c, n in enumerate(row):
            rot = "transform:rotate(180deg);" if r == 0 else ""
            num = f'<div class="znum">{n}</div>' if n not in (1, 8) else ""
            parts.append(f'<div class="zp" style="left:{x0 + c * ZINE_W}mm;top:{y0 + r * ZINE_H}mm;{rot}">{pages[n - 1]}{num}</div>')
    cx0, cx1, cy = x0 + ZINE_W, x0 + 3 * ZINE_W, y0 + ZINE_H
    folds = ([f'<line x1="{x0 + k * ZINE_W}" y1="{y0}" x2="{x0 + k * ZINE_W}" y2="{y0 + 2 * ZINE_H}" class="fold"/>' for k in (1, 2, 3)]
             + [f'<line x1="{x0}" y1="{cy}" x2="{cx0}" y2="{cy}" class="fold"/>',
                f'<line x1="{cx1}" y1="{cy}" x2="{x0 + 4 * ZINE_W}" y2="{cy}" class="fold"/>'])
    lines = (f'<svg class="piece" style="left:0;top:0;width:{pw}mm;height:{ph}mm" viewBox="0 0 {pw} {ph}">'
             '<style>.cut{fill:none;stroke:#000;stroke-width:.3}.fold{stroke:#777;stroke-width:.2;stroke-dasharray:1.5 1.2}'
             '.slit{stroke:#c0392b;stroke-width:.6}</style>'
             f'<rect x="{x0}" y="{y0}" width="{4 * ZINE_W}" height="{2 * ZINE_H}" class="cut"/>{"".join(folds)}'
             f'<line x1="{cx0}" y1="{cy}" x2="{cx1}" y2="{cy}" class="slit"/></svg>')
    note = (f'<div class="note" style="left:{x0}mm;top:4mm;width:{4 * ZINE_W}mm;font-size:7.5pt">'
            '<b>Rules booklet.</b> Cut the outer border. Fold in half lengthwise, cut the '
            '<b style="color:#c0392b">red slit</b> through the fold, then push the ends together and flatten into an '
            f'8-page booklet. Folded: {ZINE_W:.0f} × {ZINE_H:.0f} mm, fits in the tuck box.</div>')
    return f'<div class="page" style="width:{pw}mm;height:{ph}mm">{"".join(parts)}{lines}{note}</div>'
