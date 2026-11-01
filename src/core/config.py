"""Paths, paper and card sizes, shared colours."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(ROOT, ".cache")
BUILD = os.path.join(ROOT, "build")
PREVIEW = os.path.join(ROOT, "preview")
TEMPLATES = os.path.join(ROOT, "templates")

# Pages are rendered from build/, so asset URLs in the HTML are relative to it.
ASSET_URL = "../assets/"
LOGO_IMG = ASSET_URL + "img/logo_card_game.png"   # 1000 x 538
LOGO_RATIO = 538 / 1000

PAPERS = {"A4": (210.0, 297.0), "Letter": (215.9, 279.4)}   # portrait, mm

# The original card is 280 x 400 units; printed at poker height, keeping its proportions.
CARD_H = 88.9
CARD_W = CARD_H * 280 / 400    # 62.2 mm

GOLD = "#f5c242"
DARK = "#2a0d22"
MAROON = "linear-gradient(155deg,#3d1636 0%,#7d2034 55%,#b5452e 100%)"
PLAYER = {"red": {"accent": "#b3261e", "gem": "pieces/gem_red.svg", "other": "pieces/gem_yellow.svg"},
          "yellow": {"accent": "#c48f00", "gem": "pieces/gem_yellow.svg", "other": "pieces/gem_red.svg"}}
