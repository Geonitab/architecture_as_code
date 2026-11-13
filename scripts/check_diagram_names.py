#!/usr/bin/env python3
"""Check that Mermaid sources follow the naming convention of the diagram style guide.

Convention: ``diagram_<chapter>_<description>.mmd`` (or ``<topic>_<kind>.mmd`` for
shared diagrams). A description must say what the diagram shows, so names that
encode a chapter number again (``diagram_05_chapter3``) are rejected.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Legacy name still referenced from archived documents and reports.
LEGACY_ALLOWED = {"diagram_21_chapter20"}
CHAPTER_STUB = re.compile(r"chapter\d+", re.IGNORECASE)


def main() -> int:
    images_dir = Path(__file__).resolve().parents[1] / "docs" / "images"
    failures = [
        path.name
        for path in sorted(images_dir.glob("*.mmd"))
        if CHAPTER_STUB.search(path.stem) and path.stem not in LEGACY_ALLOWED
    ]
    if failures:
        print("Diagram names must describe the content, not repeat a chapter number:")
        for name in failures:
            print(f"  - {name}")
        return 1
    print("All diagram names follow the naming convention.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
