"""The game content in data/, and the measurements that sit next to the assets they describe."""
import json
import os

from core.config import ASSETS, DATA


def load_json(name, folder=DATA):
    with open(os.path.join(folder, name), encoding="utf-8") as f:
        return json.load(f)


# The game's cards (built by external/maf-extract/extract.py), then custom cards, which can also override them.
CARDS = {(c["id"], c["style"]): c for c in load_json("original_cards.json") + load_json("cards.json")}
DECKS = load_json("decks.json")
RULES = load_json("rules.json")
BADGES = load_json("svg/badges/badges.json", ASSETS)
FRAMES = load_json("svg/frames/frames.json", ASSETS)


def card(card_id, style):
    """A card's data in a style ("clean" or "worn"). Cards that only exist in the clean style (e.g. Omegon) are
    reused in the worn one."""
    return CARDS.get((card_id, style)) or CARDS[(card_id, "clean")]
