# Mighty Action Force: The Card Game (PnP)

[![Made with Claude Code](https://img.shields.io/badge/made_with-Claude_Code-D97757?logo=claude&logoColor=white)](https://claude.com/claude-code)

A two-player print-and-play version of the [Mighty Action Force card game][card-game] from [Poptropica][poptropica]'s
[PoptropiCon island][poptropicon]. This is an unofficial fan project and isn't affiliated with Poptropica. The code was
written with [Claude Code][claude-code], but the art is the game's own; none of it is generated (more on that under
[Credits](#credits)).

[card-game]: https://poptropica.fandom.com/wiki/Mighty_Action_Force_Card_Game
[poptropica]: https://www.poptropica.com/
[poptropicon]: https://poptropica.fandom.com/wiki/PoptropiCon_Island
[claude-code]: https://claude.com/claude-code

**[Download the latest release](https://github.com/20akshay00/MightyActionForceTCG/releases/latest)** to get the PDFs
for A4 and US Letter, plus single-card images if you'd rather order the cards from a printing service. The [README](templates/release_readme.md) in the release folder explains which files you need for each.

![The game set up on the table](preview/table_preview.png)

## Building

The game's artwork, fonts and card text aren't in this repository. You extract them from your own copy of the game
with [maf-extract](https://github.com/20akshay00/maf-extract), which is included as a submodule:

1. Clone with `git clone --recursive`, or run `git submodule update --init` in an existing clone.
2. Get the Poptropica Flash files, JPEXS and Python as described in
   [maf-extract's README](https://github.com/20akshay00/maf-extract#use).
3. Run `python external/maf-extract/extract.py pnp`. It fills `assets/` and writes `data/original_cards.json`.
4. Save the logo from the [Poptropica Wiki](https://poptropica.fandom.com/wiki/Mighty_Action_Force_Card_Game) as
   `assets/img/logo_card_game.png` (1000 × 538). It isn't in the game files.
5. Run `python -I src/build.py` with [Python 3](https://www.python.org/) and [Chrome](https://www.google.com/chrome/)
   installed (if Chrome isn't on your path, point the `CHROME` environment variable at it). Everything ends up in
   `build/`. The first run also measures the artwork and caches the result in `.cache/`.

Releases are built locally the same way, then zipped and published with the GitHub CLI:
`gh release create v1.x MightyActionForceTCG_PnP.zip --title "MightyActionForceTCG PnP v1.x"`, where the zip holds
`build/` renamed to `MightyActionForceTCG_PnP/`.

The project is roughly organized as follows. `assets/` holds the extracted artwork and fonts, along with
measurements of that artwork, `data/` holds the custom card list, decks and shared rules text, and `templates/` holds the CSS, the rules booklet
pages and the release README. The Python in `src/` only puts these together: `core/` loads files and drives Chrome,
`pieces/` builds the cards, tuck box and booklet, and `output/` lays them out on sheets and exports PDFs and images.
[`assets/README.md`](assets/README.md) and [`data/README.md`](data/README.md) describe each file.

## Custom cards

To add a card, give it an entry in `data/cards.json` and put its `id` in one of the lists in `data/decks.json`. For
example:

```json
{"id": "my_hero", "style": "clean", "name": "My Hero", "value": 5, "badge": "#22c8b8",
 "effect": "steal", "power_name": "Steal A Gem", "description": "Steal one gem from your opponent.",
 "art": "img/my_hero.png"}
```

The art can be a PNG, JPG or SVG anywhere under `assets/`; it's cropped to fill the card's picture window. Any
single-digit value works, and the optional `badge` colour lets you pick the badge's colour yourself. The full list of
fields is in [`data/README.md`](data/README.md).

## Credits

The characters, art, card text and rules all come from Poptropica's PoptropiCon island, and belong to their owners.
The card list and rules were checked against the
[Poptropica Wiki](https://poptropica.fandom.com/wiki/Mighty_Action_Force_Card_Game) and the decompiled game code.

The artwork, fonts and card data are extracted as vector files from the original Flash game, preserved by the
[Flashpoint Archive](https://flashpointarchive.org/), using [JPEXS](https://github.com/jindrapetrik/jpexs-decompiler)
and [maf-extract](https://github.com/20akshay00/maf-extract). They aren't included in this repository.
The one exception is the logo, which isn't in the game files and comes from the [Poptropica Wiki](https://poptropica.fandom.com/wiki/Mighty_Action_Force_Card_Game).

All of the extraction, layout and PDF generation was done with Claude Code. The cards are assembled from the original
layers, and the only change to the art itself is that the value badge was separated from the card frame so it can be
recoloured for each value. Nothing was generated or redrawn. The new pieces (turn cards, scoreboard, tuck box and
rules booklet) are simple shapes drawn in code around the original art.

Compared with the cards in the game, the text is set in Billy Serif rather than Arial Bold, the values use the game's
Grilled Cheese font, and each card has a small upside-down value in its bottom-left corner so your opponent can read
it across the table. [This image](preview/original_vs_print.png) shows an original card next to this version. The
turn cards, scoreboard, booklet, tuck box, the worn-style Omegon and the booklet's game variants are all additions.

## License

This isn't for sale or any commercial use. Poptropica's material isn't licensed by this project. Everything else may
be shared and adapted for non-commercial use, no credit needed. See [`LICENSE`](LICENSE).
