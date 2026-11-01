"""Build the print-and-play: python -I src/build.py

Writes build/ (the release folder: A4 and Letter PDFs, single-card images, README, LICENSE) and preview/.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I leaves the script's folder off the path
from core.config import BUILD, PAPERS, ROOT  # noqa: E402
from output.export import card_images, pdfs  # noqa: E402
from output.layout import all_entries, sheets  # noqa: E402
from output.previews import comparison_preview, table_preview  # noqa: E402
from pieces.rules import zine_sheet  # noqa: E402

if __name__ == "__main__":
    shutil.rmtree(BUILD, ignore_errors=True)
    entries = all_entries()
    jobs = []
    for name, paper in PAPERS.items():
        fronts, backs = sheets(entries, paper)
        preview = name == "A4"
        jobs += [(name, "cards_fronts", fronts, paper, preview), (name, "cards_backs", backs, paper, preview),
                 (name, "rules_booklet", [zine_sheet(paper)], paper[::-1], preview)]
    pdfs(jobs)
    card_images(entries)
    for src, dst in (("templates/release_readme.md", "README.md"), ("LICENSE", "LICENSE")):
        shutil.copy(os.path.join(ROOT, src), os.path.join(BUILD, dst))
    table_preview()
    comparison_preview()
