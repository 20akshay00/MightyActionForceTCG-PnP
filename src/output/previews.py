"""README images: the game set up on a table, and an original card next to this version."""
import os

from core.config import CARD_H, CARD_W, PREVIEW
from core.templates import read
from output.export import document, px, screenshot
from pieces.cards import card_back, card_front, original_card
from pieces.table_cards import scoreboard, turn_card

SHADOW = "filter:drop-shadow(0 1mm 1.5mm rgba(0,0,0,.45))"
CSS = read("css/previews.css")


def table_preview():
    """Both players' setups as they lie on a table, the far side turned 180 degrees, the scoreboard between."""
    gap, wide, pad, mid = 8.0, 14.0, 12.0, CARD_W + 16
    row_w = 5 * CARD_W + 2 * gap + 2 * wide
    tw, th = row_w + 2 * pad, 2 * (CARD_H + 9) + 2 * pad + mid

    def at(svg, x, y, rot=0):
        return (f'<div style="position:absolute;left:{x:.1f}mm;top:{y:.1f}mm;width:{CARD_W}mm;height:{CARD_H}mm;'
                f'transform:rotate({rot}deg);{SHADOW}">{svg}</div>')

    def side(color, style, attack, bounty, used, pos):
        out = [at(card_back(style), 0, 0), at(card_back(style), 1.2, -1.2)]
        x = CARD_W + wide
        for svg in ((attack, turn_card(color), bounty) if color == "red" else (bounty, turn_card(color), attack)):
            out.append(at(svg, x, 0))
            x += CARD_W + gap
        x += wide - gap
        out += [at(card_front(c, style), x + dx, dy, r) for c, dx, dy, r in zip(used, (0, 1.5, -1), (0, -1, -1.5), (-4, 3, -1))]
        left, right = ("ATTACK", "BOUNTY") if color == "red" else ("BOUNTY", "ATTACK")
        labels = [("DECK", CARD_W / 2), (left, CARD_W + wide + CARD_W / 2),
                  (right, CARD_W + wide + 2 * (CARD_W + gap) + CARD_W / 2), ("DISCARD", x + CARD_W / 2)]
        out += [f'<div class="tl" style="left:{cx - 20:.1f}mm;top:{CARD_H + 2.5}mm">{t}</div>' for t, cx in labels]
        return f'<div style="position:absolute;width:{row_w}mm;height:{CARD_H}mm;{pos}">{"".join(out)}</div>'

    board_top = pad + CARD_H + 9 + (mid - CARD_W) / 2
    body = (f'<div class="page" style="width:{tw}mm;height:{th}mm;background:radial-gradient(ellipse at 50% 50%,#6b4a2f,#3b2716)">'
            + side("yellow", "worn", card_back("worn"), card_front("gold_face", "worn"), ["k_man", "mutton_chops", "pony_girl"],
                   f"left:{pad}mm;top:{pad}mm;transform:rotate(180deg)")
            + side("red", "clean", card_front("elf_archer", "clean"), card_back("clean"), ["meow_bot", "hench_bot"],
                   f"left:{pad}mm;top:{th - pad - CARD_H - 9}mm")
            + at(scoreboard({"red": 5, "yellow": 8}), tw / 2 - CARD_W / 2, board_top - (CARD_H - CARD_W) / 2, -90)
            + f'<div class="tl" style="left:{tw / 2 + CARD_H / 2 + 4}mm;top:{board_top + CARD_W / 2 - 3}mm;width:auto;text-align:left">'
              'SCOREBOARD<br><span style="font-size:7pt;color:#fde8b4">red 5 · yellow 8</span></div></div>')
    screenshot(document([body], f"{tw}mm {th}mm", CSS), os.path.join(PREVIEW, "table_preview.png"),
               px(tw) + 1, px(th) + 1, "--force-device-scale-factor=1.5")


def comparison_preview(card_id="pony_girl"):
    w = 2 * CARD_W + 26

    def column(svg, label, sub):
        return f'<div><div style="{SHADOW}">{svg}</div><div class="lab">{label}</div><div class="sub">{sub}</div></div>'

    body = (f'<div class="cmp" style="width:{w}mm">{column(original_card(card_id), "ORIGINAL", "rebuilt from the game files")}'
            f'{column(card_front(card_id, "clean"), "PRINT &amp; PLAY", "this version")}</div>')
    screenshot(document([body], css=CSS), os.path.join(PREVIEW, "original_vs_print.png"),
               px(w + 16), px(CARD_H + 25), "--force-device-scale-factor=2")
