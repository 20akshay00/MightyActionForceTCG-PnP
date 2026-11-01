"""Cards added for the tabletop version: the shared scoreboard and each player's turn card. Their fronts are laid out
in code (positions depend on the score track and the player's side); the backs are fixed and come from
assets/svg/added/ and templates/."""
from core.config import DARK, GOLD, LOGO_IMG, LOGO_RATIO, PLAYER
from core.data import RULES
from core.svg import frag, nested, star
from core.templates import fill
from pieces.cards import portrait


def framed(*layers):
    """A card-sized SVG on the gold frame and maroon panel."""
    return f'<svg class="card" viewBox="0 0 280 400" overflow="visible">{frag("added/card_frame.svg")}{"".join(layers)}</svg>'


def reveal_order(cls):
    """The reveal order as numbered rows; the last word of each step is highlighted."""
    def step(text):
        head, _, last = text.rpartition(" ")
        return f"{head} <b>{last}</b>".strip()
    return "".join(f'<div class="{cls}"><span>{i}</span>{step(t)}</div>' for i, t in enumerate(RULES["reveal_order"], 1))


def scoreboard(clips=None):
    """Shared scoreboard, lying landscape between the players. Both gem tracks run side by side and share one
    numbering; a number row along each long edge reads upright for the player on that side.
    Drawn in landscape units (400 x 280), red at the bottom, then turned onto the portrait card.
    clips = {"red": n, "yellow": n} draws paperclips at those scores (for the table preview)."""
    x0, x1 = 44.0, 356.0
    step = (x1 - x0) / 13
    rows = {"red": 160.0, "yellow": 120.0}
    out = []
    for color, cy in rows.items():
        p = PLAYER[color]
        out.append(f'<rect x="26" y="{cy - 17}" width="348" height="34" rx="17" fill="{DARK}" opacity=".85"/>')
        for n in range(14):
            x = x0 + n * step
            if n == 13:
                out.append(star(x, cy, 18, 12, fill=p["accent"], stroke=GOLD, stroke_width="1.6"))
            out.append(f'<circle cx="{x:.1f}" cy="{cy}" r="10.5" fill="{DARK}" stroke="{GOLD}" stroke-width="1.6"/>')
            if n > 0:
                out.append(nested(p["gem"], x - 9, cy - 9, 18))
    for n in range(14):
        x = x0 + n * step
        major = n % 5 == 0 or n == 13
        tick = f'stroke="{GOLD}" stroke-width="2" stroke-linecap="round" opacity="{1 if major else .5}"'
        out.append(f'<text x="{x:.1f}" y="210.5" class="num" text-anchor="middle">{n}</text>'
                   f'<line x1="{x:.1f}" y1="222" x2="{x:.1f}" y2="{267 if major else 248}" {tick}/>'
                   f'<text x="{x:.1f}" y="82.5" class="num" text-anchor="middle" transform="rotate(180 {x:.1f} 76)">{n}</text>'
                   f'<line x1="{x:.1f}" y1="58" x2="{x:.1f}" y2="{13 if major else 32}" {tick}/>')
    for color, n in (clips or {}).items():
        # resting flat: tip on the score socket, the rest pointing off the owner's edge
        cy, sgn = rows[color], (1 if color == "red" else -1)
        cx, end, sweep = x0 + n * step, cy + sgn * 86, 1 if sgn > 0 else 0
        d = (f"M{cx - 5:.1f} {cy} a5 5 0 0 {sweep} 10 0 V{end} a5 5 0 0 {sweep} -10 0 Z "
             f"M{cx - 2.3:.1f} {cy + sgn * 8} V{end - sgn * 4} a2.3 2.3 0 0 {1 - sweep} 4.6 0 V{cy + sgn * 14}")
        out.append(f'<g style="filter:drop-shadow(0 1.5px 1px rgba(0,0,0,.5))" fill="none" stroke-linecap="round">'
                   f'<path d="{d}" stroke="#5b616b" stroke-width="3.4"/><path d="{d}" stroke="#c9ced6" stroke-width="1.7"/></g>')
    return framed(f'<g transform="translate(280 0) rotate(90)">{"".join(out)}</g>')


def scoreboard_back():
    return f'<svg class="card" viewBox="0 0 280 400">{frag("added/scoreboard_back.svg")}</svg>'


def turn_card(color):
    """Lies between a player's two face-down cards, its arrows pointing at the Attack and Bounty slots. Yellow's is
    mirrored so that across the table Attack faces Attack."""
    p = PLAYER[color]
    sides = ("ATTACK", "BOUNTY") if color == "red" else ("BOUNTY", "ATTACK")
    cy, ah, sh = 245.0, 46.0, 25.0   # arrow centre line, head half-height, shaft half-height
    left = f"26,{cy} 70,{cy - ah} 70,{cy - sh} 136,{cy - sh} 136,{cy + sh} 70,{cy + sh} 70,{cy + ah}"
    right = f"254,{cy} 210,{cy - ah} 210,{cy - sh} 144,{cy - sh} 144,{cy + sh} 210,{cy + sh} 210,{cy + ah}"
    gy = 329.0
    out = [f'<image href="{LOGO_IMG}" x="40" y="29" width="200" height="{200 * LOGO_RATIO:.1f}"/>',
           f'<rect x="34" y="152" width="212" height="31" rx="5" fill="{p["accent"]}" stroke="{GOLD}" stroke-width="2"/>',
           f'<text x="140" y="174" text-anchor="middle" class="tname">{color.upper()} PLAYER</text>',
           f'<polygon points="{left}" class="tarrow"/><polygon points="{right}" class="tarrow"/>',
           f'<text x="91" y="{cy + 5.5}" text-anchor="middle" class="tlabel">{sides[0]}</text>',
           f'<text x="189" y="{cy + 5.5}" text-anchor="middle" class="tlabel">{sides[1]}</text>']
    gems = [(p["other"], "−", "they lose gems"), (p["gem"], "+", "you gain gems")]
    if color == "yellow":
        gems.reverse()
    for x, (gem, sign, cap) in zip((81, 199), gems):
        out += [f'<circle cx="{x}" cy="{gy}" r="22" fill="{DARK}" stroke="{GOLD}" stroke-width="2.2"/>',
                nested(gem, x - 17, gy - 17, 34),
                f'<circle cx="{x + 18}" cy="{gy + 15}" r="9" fill="{DARK}" stroke="{GOLD}" stroke-width="1.6"/>',
                f'<text x="{x + 18}" y="{gy + 20.5}" text-anchor="middle" class="tsign">{sign}</text>',
                f'<text x="{x}" y="{gy + 41}" text-anchor="middle" class="tcap">{cap}</text>']
    return framed(*out)


def turn_card_back(color):
    """Reference side: the reveal order and the five effects."""
    effects = "".join(f'<div class="tfx">{portrait(e["card"], 6.6)}<div><b>{e["name"]}</b> {e["short"]}</div></div>'
                      for e in RULES["effects"])
    body = fill("turn_card_back.html", reveal_order=reveal_order("tlink"), effects=effects)
    return framed(f'<foreignObject x="13" y="13" width="254" height="374">{body}</foreignObject>')
