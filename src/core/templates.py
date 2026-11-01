"""Text files in templates/: CSS, the rules booklet pages and other HTML with $placeholders."""
import os
from string import Template

from core.config import TEMPLATES


def read(name):
    with open(os.path.join(TEMPLATES, name), encoding="utf-8") as f:
        return f.read()


def fill(name, **values):
    """A template with its $placeholders filled in."""
    return Template(read(name)).substitute(values)
