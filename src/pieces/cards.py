"""Character cards: frame + art + value badge + text."""
from core.config import ASSET_URL
from core.data import FRAMES, card
from core.svg import BOUNDS, esc, frag, new_id
from pieces.badges import corner_badge, original_badge, value_badge

# Card units: frame top-left = (0, 0), 280 x 400. The original art is drawn around the centre (140, 200).


def art(c):
    """Original art (assets/svg/art/, drawn around the card centre) inline; any other image fills the art window."""
    if c["art"].startswith("svg/art/"):
        return f'<g transform="translate(140 200)">{frag(c["art"][4:])}</g>'
    x, y, w, h = FRAMES["art_box"]
    return (f'<image href="{ASSET_URL}{c["art"]}" x="{x}" y="{y}" width="{w}" height="{h}" '
            'preserveAspectRatio="xMidYMid slice"/>')


def portrait(card_id, size):
    """Round portrait cut from a card's art, with a gold ring. size in mm."""
    clip = new_id("pc")
    return (f'<svg class="por" viewBox="-62 -112 124 124" style="width:{size}mm;height:{size}mm">'
            f'<defs><clipPath id="{clip}"><circle cx="0" cy="-50" r="60"/></clipPath></defs>'
            f'<circle cx="0" cy="-50" r="60" fill="#3d1636"/>'
            f'<g clip-path="url(#{clip})"><g transform="translate(-140 -200)">{art(card(card_id, "clean"))}</g></g>'
            '<circle cx="0" cy="-50" r="58" fill="none" stroke="#f5c242" stroke-width="6"/></svg>')


def _text(c, cls=""):
    """Title and body (power + description, or the quotation) as HTML in a foreignObject."""
    if c["effect"] != "none":
        body = f'<div class="{cls}power">{esc(c["power_name"])}</div><div class="{cls}desc">{esc(c["description"])}</div>'
    else:
        body = f'<div class="{cls}quote">{esc(c["quotation"])}</div>'
    return (f'<foreignObject x="0" y="0" width="280" height="400"><div xmlns="http://www.w3.org/1999/xhtml" '
            f'class="{cls}text"><div class="{cls}title">{esc(c["name"])}</div>{body}</div></foreignObject>')


def _card(style, *layers):
    return f'<svg class="card" viewBox="0 0 280 400">{frag(f"frames/{style}.svg")}{"".join(layers)}</svg>'


def card_front(card_id, style):
    c = card(card_id, style)
    return _card(style, value_badge(c), art(c), corner_badge(c), _text(c))


def original_card(card_id, style="clean"):
    """The card as the game drew it: original badge and digits, Arial Bold text at the XML's positions."""
    c = card(card_id, style)
    return _card(style, original_badge(c), art(c), _text(c, "o-"))


def card_back(style):
    name = f"backs/{style}.svg"
    return (f'<svg class="card" viewBox="{" ".join(map(str, BOUNDS[name]))}" preserveAspectRatio="none">'
            f'{frag(name)}</svg>')

