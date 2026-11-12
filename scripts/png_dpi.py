#!/usr/bin/env python3
"""Stamp a print resolution into PNG files.

Mermaid renders diagrams at twice the logical size (``--scale 2``). A PNG without a resolution
is placed by LaTeX at 96 ppi, which prints a narrow diagram at about 30 pt and shrinks a wide
one below 8 pt. At 300 ppi the labels (20 px logical, 40 px in the file) print at 9.6 pt at the
natural size of the figure, whatever its width; a diagram up to about 950 logical px wide fits
the text column without being scaled.

Usage: python3 scripts/png_dpi.py file.png [more.png ...]
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

DPI = 300


def stamp_dpi(path, dpi: int = DPI) -> None:
    from PIL import Image

    target = Path(path)
    with Image.open(target) as image:
        image.load()
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", dpi=(dpi, dpi), optimize=True)
    target.write_bytes(buffer.getvalue())


if __name__ == "__main__":
    for name in sys.argv[1:]:
        stamp_dpi(name)
