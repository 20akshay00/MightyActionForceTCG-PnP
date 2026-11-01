"""What gets printed: every card as an Entry, laid out 3 x 3 on print sheets."""
from collections import namedtuple

from core.config import CARD_H, CARD_W
from core.data import DECKS
from pieces.box import BOX_D, BOX_W, tuck_box
from pieces.cards import card_back, card_front
from pieces.table_cards import scoreboard, scoreboard_back, turn_card, turn_card_back

# group: "red", "yellow" or "" (shared); name/back_name: image file names for the front and back.
Entry = namedtuple("Entry", "front back group name back_name")
PER_SHEET = 9


def player_set(color):
    """A player's deck, extras and turn card, in their deck's style."""
    style = DECKS[color]["style"]
    ids = DECKS[color]["deck"] + DECKS["extras"]
    back = card_back(style)
    cards = [Entry(card_front(i, style), back, color, f"{n:02}_{i}", "back") for n, i in enumerate(ids, 1)]
    return cards + [Entry(turn_card(color), turn_card_back(color), color, f"{len(ids) + 1:02}_turn_card", "turn_card_back")]


def all_entries():
    """Both players' sets, then the shared scoreboard and a spare."""
    board = Entry(scoreboard(), scoreboard_back(), "", "scoreboard", "scoreboard_back")
    return player_set("red") + player_set("yellow") + [board, board]


def describe(chunk, entries):
    """Sheet title part like "RED 10–14 · YELLOW 1–4 · scoreboard ×2"."""
    groups = {}
    for e in chunk:
        groups.setdefault(e.group, []).append([x for x in entries if x.group == e.group].index(e) + 1)
    return " · ".join(f"{g.upper()} {n[0]}" + (f"–{n[-1]}" if len(n) > 1 else "") if g else f"scoreboard ×{len(n)}"
                      for g, n in groups.items())


def card_sheet(cards, title, paper, rows=3, top=None, extra=""):
    """Cards butted 3 per row on a portrait page, with cut guides and crop marks. `top` places the grid (default:
    centred); `extra` is more page content (the tuck box). Notes go above and below, or up the side margins when
    there's no room (Letter)."""
    pw, ph = paper
    gx = (pw - 3 * CARD_W) / 2
    gy = (ph - rows * CARD_H) / 2 if top is None else top
    gb = gy + rows * CARD_H
    cells = "".join(f'<div style="position:absolute;left:{gx + i % 3 * CARD_W}mm;top:{gy + i // 3 * CARD_H}mm">{svg}</div>'
                    for i, svg in enumerate(cards) if svg)
    lines = []
    for k in range(4):
        x = gx + k * CARD_W
        lines += [f'<line x1="{x}" y1="{max(gy - 7, 0)}" x2="{x}" y2="{gy - 1.5}"/>',
                  f'<line x1="{x}" y1="{gb + 1.5}" x2="{x}" y2="{min(gb + 7, ph)}"/>',
                  f'<line class="g" x1="{x}" y1="{gy}" x2="{x}" y2="{gb}"/>']
    for k in range(rows + 1):
        y = gy + k * CARD_H
        lines += [f'<line x1="{gx - 7}" y1="{y}" x2="{gx - 1.5}" y2="{y}"/>',
                  f'<line x1="{pw - gx + 1.5}" y1="{y}" x2="{pw - gx + 7}" y2="{y}"/>',
                  f'<line class="g" x1="{gx}" y1="{y}" x2="{pw - gx}" y2="{y}"/>']
    marks = (f'<svg class="piece" style="left:0;top:0;width:{pw}mm;height:{ph}mm" viewBox="0 0 {pw} {ph}">'
             '<style>line{stroke:#000;stroke-width:.2} line.g{stroke:#9a9a9a;stroke-width:.12;stroke-dasharray:1.2 .8}</style>'
             f'{"".join(lines)}</svg>') if cards else ""
    foot = f'{CARD_W:.1f} × {CARD_H} mm cards · print at 100% / actual size'
    if gy >= 8 and ph - gb >= 8:
        notes = (f'<div class="note sheetnote" style="left:{gx}mm;top:{gy - 7}mm;font-weight:bold;color:#222">{title}</div>'
                 f'<div class="note sheetnote" style="left:{gx}mm;top:{gb + 2.5}mm;color:#777">{foot}</div>')
    else:
        side = 'top:{}mm;left:{}mm;width:{}mm;transform-origin:0 0;transform:rotate(-90deg)'.format
        notes = (f'<div class="note" style="{side(gb, gx / 2 - 2.5, gb - gy)};font-weight:bold;color:#222">{title}</div>'
                 f'<div class="note" style="{side(gb, pw - gx / 2 - 2.5, gb - gy)};color:#777">{foot}</div>')
    return f'<div class="page" style="width:{pw}mm;height:{ph}mm">{extra}{cells}{marks}{notes}</div>'


def mirrored(cards):
    """Long-edge duplex flips each row left to right, so the back of column c sits behind column 2 - c."""
    rows = [(cards[i:i + 3] + [None] * 3)[:3] for i in range(0, len(cards), 3)]
    return [c for row in rows for c in reversed(row)]


def sheets(entries, paper):
    """(front pages, back pages) for one paper size. The tuck box shares the last sheet if at most one row of cards
    is left, otherwise it gets its own."""
    chunks = [entries[i:i + PER_SHEET] for i in range(0, len(entries), PER_SHEET)]
    if len(chunks[-1]) > 3:
        chunks.append([])
    box, _, box_h = tuck_box((paper[0] - (2 * BOX_D + 2 * BOX_W + 10)) / 2, 12)
    fronts, backs = [], []
    for n, chunk in enumerate(chunks, 1):
        last = n == len(chunks)
        parts = [f"Sheet {n} of {len(chunks)}"] + ([describe(chunk, entries)] if chunk else []) + (["tuck box"] if last else [])
        layout = dict(rows=1, top=12 + box_h + 14) if last else {}
        fronts.append(card_sheet([e.front for e in chunk], " · ".join(parts), paper, extra=box if last else "", **layout))
        backs.append(card_sheet([e and e.back for e in mirrored(chunk)], f"Backs for sheet {n} · duplex, flip on long edge",
                                paper, **layout))
    return fronts, backs
