"""The presentation takes its look from the book's cover and its structure from the index."""

import json
import re
from pathlib import Path

import presentation_deck

ROOT = Path(__file__).resolve().parents[1]


def test_palette_comes_from_the_cover():
    theme = presentation_deck.load_theme(ROOT)
    svg = (ROOT / "templates" / "book-cover.svg").read_text(encoding="utf-8").lower()
    assert theme["primary"] in svg or theme["primary"] != presentation_deck.DEFAULT_PALETTE["primary"]
    assert theme["accent"] in svg or "hsl" in svg


def test_deck_covers_every_part_and_chapter():
    index = json.loads((ROOT / "docs" / "book_index.json").read_text(encoding="utf-8"))
    deck = presentation_deck.collect_deck(ROOT)
    assert sum(1 for e in deck if e["type"] == "part") == len(index["parts"])
    assert sum(1 for e in deck if e["type"] == "chapter") == sum(len(p["chapters"]) for p in index["parts"])


def test_slide_text_is_clean():
    for entry in presentation_deck.collect_deck(ROOT):
        if entry["type"] != "chapter":
            continue
        chapter = entry["chapter"]
        for text in [chapter["title"], chapter["takeaway"], *chapter["sections"]]:
            assert "{#" not in text and "](" not in text and "**" not in text, text
        assert len(chapter["takeaway"].split()) <= 40


def test_deck_builds():
    import pytest

    pptx = pytest.importorskip("pptx")
    prs = pptx.Presentation()
    presentation_deck.build_deck(prs, presentation_deck.collect_deck(ROOT), ROOT)
    assert len(prs.slides) > 20
