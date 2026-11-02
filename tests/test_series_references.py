"""The series builds strictly in publication order.

*The Architecture as Code Series* avoids circular reasoning between its books:
Book 1 refers to no other volume, Book 2 only to Book 1, Book 3 only to
Books 1-2, and so on. A book may build on the conclusions of an earlier
volume, but never on a later one, so no claim can rest on a book that itself
rests on the book making the claim. This test fails if any manuscript file of
this book mentions a later volume of the series.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

THIS_BOOK = 1

# Patterns that identify each volume of the series (title, website, repository).
VOLUMES = {
    1: [r"\*Architecture as Code\*", r"aac\.geon\.se", r"Geonitab/architecture_as_code"],
    2: [r"\*AI Governance[*:]", r"aig\.geon\.se", r"Geonitab/AI-governance"],
    3: [r"AI Platform and Security", r"aips\.geon\.se", r"Geonitab/AI-platform-security"],
    4: [r"\*AI Red Team[*:]", r"aired\.geon\.se", r"Geonitab/Ai-red"],
    5: [r"\*AI Threat[*:]", r"aithreat\.geon\.se", r"Geonitab/Ai-threat"],
}
SERIES_BOOK = re.compile(r"Architecture as Code Series,? Book (\d+)")

DOCS = Path(__file__).resolve().parent.parent / "docs"


def manuscript_files() -> list[Path]:
    """Reader-facing Markdown: chapters, part introductions, index and front matter.

    Editorial guides with upper-case names (STYLE_GUIDE.md and the like) state the
    rule itself and are not part of the published book.
    """
    files = []
    for path in sorted(DOCS.glob("*.md")):
        stem = path.stem
        if stem.upper() == stem:
            continue
        files.append(path)
    return files


FORBIDDEN = [
    (number, re.compile(pattern))
    for number, patterns in VOLUMES.items()
    if number != THIS_BOOK and (number > THIS_BOOK or THIS_BOOK == 1)
    for pattern in patterns
]


@pytest.mark.parametrize("path", manuscript_files(), ids=lambda p: p.name)
def test_no_reference_to_later_volumes(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    problems = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for number, pattern in FORBIDDEN:
            if pattern.search(line):
                problems.append(f"line {lineno}: refers to Book {number} ({pattern.pattern})")
        for match in SERIES_BOOK.finditer(line):
            number = int(match.group(1))
            if number != THIS_BOOK and (number > THIS_BOOK or THIS_BOOK == 1):
                problems.append(f"line {lineno}: refers to Book {number} of the series")
    assert not problems, (
        f"{path.name} refers to a volume this book may not build on "
        + ("(Book 1 may refer to no other volume)" if THIS_BOOK == 1
           else f"(Book {THIS_BOOK} may refer only to Books 1-{THIS_BOOK - 1})")
        + ":\n  " + "\n  ".join(problems)
    )
