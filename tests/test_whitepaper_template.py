#!/usr/bin/env python3
"""
Test the whitepaper template and the helpers that fill it.

The whitepaper takes the look of the book's cover (palette, cover band, accent
rules). These tests keep the parts of that design that can break silently:
Pandoc anchors and Markdown must not leak into the text, the palette comes from
``docs/stylesheets/series-colours.css``, and every tag in the body stays on one
line because the release pipeline builds the combined whitepapers PDF by
stripping tags line by line.
"""

import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_whitepapers import (
    create_whitepaper_html,
    load_book_palette,
    read_chapter_content,
    render_inline,
    split_title,
    strip_anchor,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def sample_html(**overrides):
    chapter_data = {
        "title": "Test Chapter Title: A Subtitle",
        "diagram_path": None,
        "condensed_content": [
            "Opening paragraph with **bold**, *italic* and `code` text.",
            "Second paragraph cites ([30, Nordqvist, 2025](30_references.md#source-30)).",
        ],
        "section_headers": ["Section A", "Section B"],
        "word_count": 4400,
    }
    chapter_meta = {"label": "Chapter 99", "area": "Foundations", "title": "Test Chapter Title: A Subtitle"}
    book_overview = {
        "title": "Test Book",
        "subtitle": "A subtitle",
        "description": "First paragraph\nwrapped over two lines.\n\nSecond paragraph.",
        "target_audience": "Test audience",
        "chapters_count": 34,
    }
    release = {"version": "2026.01", "release_date": "2026-01-15"}
    chapter_data.update(overrides)
    return create_whitepaper_html(
        chapter_data, chapter_meta, book_overview, release, Path("whitepapers"), chapter_file="99_test.md"
    )


class TestWhitepaperText(unittest.TestCase):
    def test_strip_anchor(self):
        self.assertEqual(strip_anchor("Chapter Title {#chapter-anchor}"), "Chapter Title")
        self.assertEqual(strip_anchor("No anchor"), "No anchor")

    def test_read_chapter_content_strips_anchors(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# Test Chapter {#test-chapter}\n\n")
            f.write("An opening paragraph that is comfortably longer than thirty characters.\n\n")
            f.write("## First section {#first}\n")
            temp_file = f.name
        try:
            result = read_chapter_content(temp_file)
            self.assertEqual(result["title"], "Test Chapter")
            self.assertEqual(result["section_headers"], ["First section"])
        finally:
            os.unlink(temp_file)

    def test_read_chapter_content_takes_the_figure_caption(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# Test Chapter\n\n![Alt text](images/diagram_01.png)\n\n")
            f.write("*Figure 1.1: The caption under the figure.*\n\n")
            f.write("An opening paragraph that is comfortably longer than thirty characters.\n")
            temp_file = f.name
        try:
            result = read_chapter_content(temp_file)
            self.assertEqual(result["diagram_path"], "images/diagram_01.png")
            self.assertIn("Figure 1.1: The caption under the figure.", result["diagram_caption"])
        finally:
            os.unlink(temp_file)

    def test_render_inline_keeps_emphasis_and_drops_link_targets(self):
        html = render_inline(
            "**M3 Consequence** and *Architecture as Code* ([30, Nordqvist, 2025](30_references.md#source-30)) in `a.yaml`"
        )
        self.assertIn("<strong>M3 Consequence</strong>", html)
        self.assertIn("<em>Architecture as Code</em>", html)
        self.assertIn("(30, Nordqvist, 2025)", html)
        self.assertIn("<code>a.yaml</code>", html)
        self.assertNotIn("](", html)
        self.assertNotIn("**", html)

    def test_render_inline_handles_nested_brackets_in_citations(self):
        html = render_inline("GDPR ([Source [43]](33_references.md#source-43)), enforced nationally")
        self.assertIn("(Source [43])", html)
        self.assertNotIn("](", html)

    def test_condensed_content_skips_table_rows_and_html_comments(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# Test Chapter\n\n<!-- An internal drafting note that is longer than thirty characters. -->\n")
            f.write("| Column one | Column two | A table row that is longer than thirty characters |\n")
            f.write("An opening paragraph that is comfortably longer than thirty characters.\n")
            temp_file = f.name
        try:
            result = read_chapter_content(temp_file)
            self.assertEqual(result["condensed_content"],
                             ["An opening paragraph that is comfortably longer than thirty characters."])
        finally:
            os.unlink(temp_file)

    def test_render_inline_escapes_html(self):
        html = render_inline("<script>alert(1)</script> and `<b>`")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("<code>&lt;b&gt;</code>", html)

    def test_split_title_only_splits_real_headings(self):
        self.assertEqual(split_title("Contestability by Design: Explanation, Appeal and Correction"),
                         ("Contestability by Design", "Explanation, Appeal and Correction"))
        self.assertEqual(split_title("Introduction: Who Is the Boss?"), ("Introduction: Who Is the Boss?", ""))
        self.assertEqual(split_title("Glossary"), ("Glossary", ""))


class TestWhitepaperPalette(unittest.TestCase):
    def test_palette_is_read_from_series_colours(self):
        with tempfile.TemporaryDirectory() as root:
            css_dir = Path(root) / "docs" / "stylesheets"
            css_dir.mkdir(parents=True)
            (css_dir / "series-colours.css").write_text(
                ":root {\n  --book-dark: #2A0E30;\n  --book-primary: #5A2363;\n  --book-accent: red;\n"
                "  --book-unknown: #123456;\n}\n.x { --book-strong: #000000; }\n",
                encoding="utf-8",
            )
            block = load_book_palette(Path(root))
        self.assertIn("--book-dark: #2A0E30;", block)
        self.assertIn("--book-primary: #5A2363;", block)
        self.assertNotIn("accent", block, "a value that is not a hex colour must be ignored")
        self.assertNotIn("unknown", block)
        self.assertNotIn("strong", block, "only the first :root block is read")

    def test_missing_palette_file_keeps_template_defaults(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(load_book_palette(Path(root)), "")

    def test_generated_page_uses_the_books_palette(self):
        css = REPO_ROOT / "docs" / "stylesheets" / "series-colours.css"
        if not css.exists():
            self.skipTest("this book has no series-colours.css; the template defaults apply")
        primary = re.search(r"--book-primary:\s*(#[0-9A-Fa-f]{6})", css.read_text(encoding="utf-8")).group(1)
        self.assertIn(f"--book-primary: {primary};", sample_html())


class TestWhitepaperStructure(unittest.TestCase):
    def test_header_is_a_cover_band_with_the_chapter_number(self):
        html = sample_html()
        self.assertIn('class="whitepaper-header" data-chapter-number="99"', html)
        self.assertIn("Test Book · Whitepaper", html)
        self.assertIn("Chapter 99 · Foundations", html)
        self.assertIn('<h1 class="title">Test Chapter Title</h1>', html)
        self.assertIn('<p class="subtitle">A Subtitle</p>', html)

    def test_subtitle_fallback_depends_on_whether_it_is_a_chapter(self):
        book = {"title": "Test Book", "subtitle": "", "description": "Text.", "target_audience": "Readers", "chapters_count": 3}
        data = {"title": "Plain Title", "diagram_path": None, "condensed_content": ["A paragraph of some length here."],
                "section_headers": ["A"], "word_count": 10}
        chapter = create_whitepaper_html(
            data, {"label": "Chapter 99", "area": "Foundations", "title": "Plain Title"}, book, {"version": "1"}, Path("whitepapers"),
        )
        self.assertIn('Key insights from Chapter 99 of &quot;Test Book&quot;', chapter)
        appendix = create_whitepaper_html(
            {"title": "Glossary", "diagram_path": None, "condensed_content": ["A paragraph of some length here."],
             "section_headers": ["A"], "word_count": 10},
            {"label": "Glossary", "area": "Appendices", "title": "Glossary"},
            {"title": "Test Book", "subtitle": "", "description": "Text.", "target_audience": "Readers", "chapters_count": 3},
            {"version": "1"}, Path("whitepapers"),
        )
        self.assertIn('Glossary from &quot;Test Book&quot;', appendix)
        self.assertIn('data-chapter-number=""', appendix)

    def test_single_h1_and_no_placeholders_left(self):
        html = sample_html()
        self.assertEqual(html.count("<h1"), 1)
        self.assertNotIn("[[", html)
        self.assertNotIn("{#", html)

    def test_markdown_does_not_leak_into_the_page(self):
        html = sample_html()
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("(30, Nordqvist, 2025)", html)
        self.assertNotIn("](", html)

    def test_footer_names_author_and_publisher(self):
        html = sample_html()
        self.assertIn("© 2026 Gunnar Nordqvist.", html)
        self.assertIn("Published by GEON IT AB.", html)

    def test_book_description_is_not_hard_wrapped(self):
        html = sample_html()
        self.assertIn("<p>First paragraph wrapped over two lines.</p>", html)
        self.assertNotIn("<br>", html)

    def test_call_to_action_links_to_the_chapter_on_the_book_site(self):
        cname = REPO_ROOT / "CNAME"
        if not cname.exists():
            self.skipTest("no CNAME file")
        host = cname.read_text(encoding="utf-8").split()[0]
        self.assertIn(f'href="https://{host}/99_test/"', sample_html())

    def test_every_tag_in_the_body_is_on_one_line(self):
        """The combined whitepapers PDF is built by stripping tags line by line."""
        html = sample_html(diagram_path="images/example.png", diagram_caption="*Figure 1.1: A caption.*")
        lines = html.splitlines()
        # The workflow runs: grep -A 99999 "<body" | grep -B 99999 "</body"
        first = next(i for i, line in enumerate(lines) if "<body" in line)
        last = next(i for i, line in enumerate(lines) if "</body" in line)
        self.assertTrue(lines[first].lstrip().startswith("<body"), "text before the real body tag mentions <body")
        self.assertFalse(any("<style" in line or "{" in line for line in lines[first:last]),
                         "stylesheet text would end up in the combined PDF")
        for line in lines[first:last + 1]:
            self.assertEqual(line.count("<"), line.count(">"), f"tag split over lines: {line!r}")


if __name__ == "__main__":
    unittest.main()
