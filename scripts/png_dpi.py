#!/usr/bin/env python3
"""Stamp a print resolution (300 ppi) into PNG files, without any dependency.

Mermaid renders diagrams at twice the logical size (``--scale 2``), so a label of 20 px is 40 px
in the file. A PNG without a resolution is placed by LaTeX at 96 ppi; at 300 ppi the labels print
at 9.6 pt at the natural size of the figure, whatever its shape. docs/pandoc.yaml sets figures at
natural size and shrinks only what exceeds the text column (about 945 logical px wide) or 80 % of
the text height (about 1170 logical px tall).

The tag is a pHYs chunk inserted after IHDR; the image data are not touched.

Usage: python3 scripts/png_dpi.py file.png [more.png ...]
"""
from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

DPI = 300
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def stamp_dpi(path, dpi: int = DPI) -> None:
    target = Path(path)
    data = target.read_bytes()
    if not data.startswith(SIGNATURE):
        raise ValueError(f"{target} is not a PNG file")
    per_metre = round(dpi / 0.0254)
    phys = _chunk(b"pHYs", struct.pack(">IIB", per_metre, per_metre, 1))
    out, pos, done = [SIGNATURE], len(SIGNATURE), False
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if kind != b"pHYs":
            out.append(data[pos:end])
            if kind == b"IHDR" and not done:
                out.append(phys)
                done = True
        pos = end
    target.write_bytes(b"".join(out))


if __name__ == "__main__":
    for name in sys.argv[1:]:
        stamp_dpi(name)
