"""HTML documents, and turning them into PDFs and PNGs with headless Chrome."""
import os
from concurrent.futures import ThreadPoolExecutor

from core.chrome import chrome, file_url, write_html
from core.config import BUILD, CARD_H, CARD_W, GOLD, MAROON, PREVIEW
from core.templates import read
from pieces.rules import ZINE_H, ZINE_W

STYLES = "".join(read(f"css/{name}.css") for name in ("page", "cards", "turn_card", "rules"))
VARIABLES = (f":root {{ --card-w:{CARD_W}mm; --card-h:{CARD_H}mm; --gold:{GOLD}; --maroon:{MAROON}; "
             f"--zine-w:{ZINE_W}mm; --zine-h:{ZINE_H}mm; }}")
FIT_TEXT = f"<script>{read('fit_text.js')}</script>"
POOL = 6   # Chrome instances at once


def document(pages, size="auto", css=""):
    """A printable HTML document; size is a CSS @page size."""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>@page {{ size: {size}; margin: 0; }}'
            f'{VARIABLES}{STYLES}{css}</style></head><body>{"".join(pages)}{FIT_TEXT}</body></html>')


def px(mm, dpi=96):
    return round(mm / 25.4 * dpi)


def shot(url, png, w, h, *flags):
    """Screenshot a page at w x h CSS px."""
    os.makedirs(os.path.dirname(png), exist_ok=True)
    chrome("--hide-scrollbars", "--virtual-time-budget=10000", f"--window-size={w},{h}", f"--screenshot={png}", *flags, url)


def screenshot(doc, png, w, h, *flags, name="_shot.html"):
    path = write_html(name, doc)
    shot(file_url(path), png, w, h, *flags)
    os.remove(path)


def pdf(job):
    """job = (folder, name, pages, (w, h) mm, preview): print to build/<folder>/<name>.pdf, and optionally screenshot
    the pages into preview/<name>.png."""
    folder, name, pages, size, preview = job
    out = os.path.join(BUILD, folder, name + ".pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = document(pages, f"{size[0]}mm {size[1]}mm")
    path = write_html(f"{name}_{folder}.html", doc)
    chrome("--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={out}", file_url(path))
    os.remove(path)
    if preview:
        screenshot(doc, os.path.join(PREVIEW, name + ".png"), px(size[0]), (px(size[1]) + 8) * len(pages),
                   name=f"{name}_{folder}_shot.html")
    print("wrote", os.path.relpath(out, BUILD))


def pdfs(jobs):
    with ThreadPoolExecutor(POOL) as pool:
        list(pool.map(pdf, jobs))


# Single-card images for print services, at 300 DPI.
IMAGE_SIZES = {"trim": ((px(CARD_W, 300), px(CARD_H, 300)), "none"),
               # 63.5 x 88.9 mm poker card + 3 mm bleed (the usual print-service template), filled with the card's
               # dark edge colour so a slightly off cut still lands on the border
               "bleed": ((822, 1122), "#4d3c13")}


def card_images(entries):
    """Every distinct face as build/cards/<size>/<group>/<name>.png. All faces share one page so the text fits as in
    the PDFs; each screenshot pulls one face into view with the URL fragment."""
    faces = {}
    for e in entries:
        faces[os.path.join(e.group, e.name + ".png")] = e.front
        faces[os.path.join(e.group, e.back_name + ".png")] = e.back
    body = "".join(f'<div class="one" id="c{i}">{svg}</div>' for i, svg in enumerate(faces.values()))
    cw, ch = IMAGE_SIZES["trim"][0]
    jobs, pages = [], []
    for variant, ((w, h), bg) in IMAGE_SIZES.items():
        css = (f".one{{position:absolute;left:-{2 * w}px;top:0;width:{w}px;height:{h}px;display:flex;align-items:center;"
               f"justify-content:center;background:{bg}}} .one:target{{left:0}} .one .card{{width:{cw}px;height:{ch}px}}"
               "body{background:none}")
        pages.append(write_html(f"cards_{variant}.html", document([body], css=css)))
        jobs += [(f"{file_url(pages[-1])}#c{i}", os.path.join(BUILD, "cards", variant, name), w, h,
                  "--default-background-color=00000000") for i, name in enumerate(faces)]
    with ThreadPoolExecutor(POOL) as pool:
        list(pool.map(lambda args: shot(*args), jobs))
    for page in pages:
        os.remove(page)
    print("wrote", len(jobs), "card images")
