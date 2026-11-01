"""Headless Chrome: measuring SVGs, printing PDFs, taking screenshots."""
import os
import shutil
import subprocess
import tempfile

from core.config import BUILD

CHROME = os.environ.get("CHROME") or next(
    (p for p in (shutil.which("google-chrome"), shutil.which("chrome"), shutil.which("chromium"),
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") if p and os.path.exists(p)),
    "chrome")


def chrome(*args):
    # A fresh profile per call lets several Chrome instances run side by side.
    with tempfile.TemporaryDirectory() as profile:
        return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={profile}", *args],
                              capture_output=True, text=True, encoding="utf-8")


def file_url(path):
    return "file:///" + path.replace("\\", "/")


def write_html(name, doc):
    """Write a page into build/ (where its relative asset URLs resolve) and return its path."""
    os.makedirs(BUILD, exist_ok=True)
    path = os.path.join(BUILD, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path
