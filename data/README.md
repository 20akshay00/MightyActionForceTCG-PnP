# Data

This folder holds the game content: the cards, the decks and the bits of rules text used in more than one place.
Measurements of the artwork live next to the assets they describe, in `assets/svg/`.

`original_cards.json` is the game's card list, extracted from its card XML by `python external/maf-extract/extract.py pnp`
(it isn't in version control). `cards.json` is for your own cards, in the same format; an entry with the same `id`
and `style` as an original card replaces it. Each card appears once per style it exists in:
`clean` for the red deck and `worn` for the yellow deck. A card with only a clean entry (like Omegon) is reused in
the worn frame when a worn deck needs it.

The fields are:

- `id`: a short snake_case name, used to refer to the card in `decks.json`.
- `style`: `clean` or `worn`.
- `name` and `value`: the title and the number in the badge. Values can be any single digit.
- `badge` (optional): a hex colour for the badge. Without it, the colour comes from the value's entry in
  `assets/svg/badges/badges.json`.
- `effect`: one of `none`, `block`, `steal`, `draw`, `skip` or `both`. Cards with an effect print their `power_name`
  and `description`; cards without one print their `quotation`. The effect itself is only text on the card, since the
  rules live in the booklet.
- `art`: a path under `assets/`. Paths in `svg/art/` are treated as original game art; any other image is scaled to
  fill the card's picture window.

`decks.json` lists each player's ten-card deck and its style, plus the extras both players get.

`rules.json` holds the reveal order and the five effects, with a short description for the turn card and a longer
one for the booklet. The rest of the booklet's text is in `templates/rules/`.
