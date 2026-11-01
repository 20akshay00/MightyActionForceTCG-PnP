# Assets

Almost everything in `svg/`, plus `fonts/`, is extracted from the original game's Flash files by
`python external/maf-extract/extract.py pnp` (see the main README) and isn't in version control. The art is the game's own,
with one change: the card frames came with a value badge baked in, which is left out so it can be drawn separately
in any colour. What *is* in version control: this README, the measurements `frames/frames.json` and
`badges/badges.json`, and the `added/` folder, which holds the few pieces drawn for this version. `img/` holds the
logo, which you download yourself.

Card frames and character art are drawn in card units (280 × 400, origin at the top left; the art is drawn around
its own origin, so the build places it at the card centre, 140, 200). Badges are in card units too, at the card's
top-right corner. Everything else is placed by its bounding box, which the build measures
in Chrome and caches in `.cache/bounds.json`.

| File | What it is |
| --- | --- |
| `svg/frames/clean.svg`, `worn.svg` | The card frame in the clean style (red deck) and the worn style (yellow deck) |
| `svg/badges/badge_4.svg` | The value badge. It's recoloured for every value except 6 |
| `svg/badges/badge_6.svg` | Omegon's rainbow badge |
| `svg/badges/badge_1.svg` to `badge_3.svg` | The game's other badges, kept only so the comparison preview can show an untouched original card |
| `svg/art/<id>.svg` | Character art, one file per card |
| `svg/backs/clean.svg`, `worn.svg` | Card backs |
| `svg/pieces/gem_red.svg`, `gem_yellow.svg` | The score gems, used on the scoreboard, turn cards and in the rules |
| `svg/pieces/arrow_large.svg`, `arrow_small.svg` | Arrows from the card back, scattered over the tuck box and booklet panels |
| `svg/added/card_frame.svg` | Gold frame and maroon panel behind the turn cards and scoreboard |
| `svg/added/scoreboard_back.svg` | The back of the scoreboard |
| `fonts/` | The game's fonts: Grilled Cheese for titles and numbers, Billy Serif for text, Creative Block for small labels |
| `img/logo_card_game.png` | The logo, from the [Poptropica Wiki](https://poptropica.fandom.com/wiki/Mighty_Action_Force_Card_Game) (it isn't in the game files) |

Two folders also have a JSON file with measurements of their artwork, so anyone swapping an SVG knows what to update.

`svg/frames/frames.json` gives the position of the picture window on the card (`art_box`, in card units) and the
radius of the card's rounded corners.

`svg/badges/badges.json` describes how badges are drawn. `palette` gives each value's colours: a light and a dark
shade for the gradient and an outline colour. If a value only has `light`, the other two are worked out from it, and
values with no entry at all are grey. `base` is the badge that gets recoloured and `special` lists values with a badge
of their own. `card_ring` is where the badge's disc sits on the card and `rings` is the disc's position inside each
badge file (in card units, where the game draws it), which together let any badge be placed in the same spot. `corner_scale` sets the size of the small
upside-down badge, and `digits` holds per-number offsets that centre each value on the badge's star.

The badges still contain the game's own digits, tagged `class="dg"`. They're hidden in print because the value is
drawn on top as text, which keeps every number in the same font.

Art for custom cards can live anywhere under `assets/`, for example in `img/`.
