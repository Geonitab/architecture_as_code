#!/usr/bin/env python3
"""Presentation deck in the graphic profile of the book.

The deck takes its look from the book's own cover (``templates/book-cover.svg``):
the cover's colour gradient and accent colours, Inter as typeface, the accent bar
along the left edge, the series line and the title in two lines with the first
word in the accent colour. Structure comes from ``docs/book_index.json``, the
title, subtitle and series from ``BOOK_REQUIREMENTS.md``. Nothing in this module
is specific to one book, so the same file serves every book in the series.

Slide types
-----------
* Title slide     - the cover, as a slide.
* Part divider    - the part's title, a short description and its chapters.
* Chapter slide   - the chapter's sections and its takeaway (one message).
* Diagram slide   - the chapter's first figure, as large as the slide allows.
* Closing slide   - where to read the book.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FONT = "Inter"

# Neutral fallback palette (the series' Kvadrat colours), used only when the
# cover cannot be read.
DEFAULT_PALETTE = {
    "primary": "#1e3a8a",
    "dark": "#1e293b",
    "accent": "#f4c35a",
    "accent2": "#e8893a",
}

AUTHOR_LINE_1 = "Conceived and directed by"
AUTHOR_NAME = "Gunnar Nordqvist"
AUTHOR_LINE_2 = "Text written by AI agents"
SERIES_LANDING = "books.geon.se"

SKIP_SECTIONS = {"summary", "sources", "contents", "references"}


# --------------------------------------------------------------------------
# Colour helpers
# --------------------------------------------------------------------------
def _hex_to_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a: str, b: str, amount: float) -> str:
    """Return ``a`` blended towards ``b`` by ``amount`` (0..1) as a hex string."""
    ra, ga, ba = _hex_to_rgb(a)
    rb, gb, bb = _hex_to_rgb(b)
    mixed = (
        round(ra + (rb - ra) * amount),
        round(ga + (gb - ga) * amount),
        round(ba + (bb - ba) * amount),
    )
    return "#%02x%02x%02x" % mixed


def _contrast(a: str, b: str) -> float:
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _legible(colour: str, ground: str, minimum: float = 4.5) -> str:
    """``colour`` moved towards black or white until it reads on ``ground``."""
    target = "#000000" if _luminance(ground) > 0.4 else "#ffffff"
    amount = 0.0
    while _contrast(colour, ground) < minimum and amount < 1.0:
        amount += 0.05
        colour = _mix(colour, target, 0.05)
    return colour


def _luminance(value: str) -> float:
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in _hex_to_rgb(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _to_hex(value: str):
    """Hex or hsl() colour to '#rrggbb', or None."""
    value = value.strip()
    if re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        return value.lower()
    found = re.fullmatch(r"hsl\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)", value)
    if not found:
        return None
    import colorsys

    h, s_, l_ = float(found.group(1)) / 360, float(found.group(2)) / 100, float(found.group(3)) / 100
    r, g, b = colorsys.hls_to_rgb(h, l_, s_)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def _gradient_stops(svg: str, gradient_id: str):
    match = re.search(
        r'<linearGradient[^>]*id="%s"[^>]*>(.*?)</linearGradient>' % gradient_id,
        svg,
        re.S,
    )
    if not match:
        return []
    raw = re.findall(r'stop-color[=:]\s*"?(#[0-9a-fA-F]{6}|hsl\([^)]*\))', match.group(1))
    return [c for c in (_to_hex(r) for r in raw) if c]


def _light_cover_palette(svg: str):
    """Palette of a light cover without gradients: left bar and title colours."""
    bar = re.search(r'<rect x="0" y="0" width="\d+"[^>]*fill="(#[0-9a-fA-F]{6})"', svg)
    title = re.search(r'font-weight="800"[^>]*fill="(#[0-9a-fA-F]{6})"', svg)
    if bar and title:
        return title.group(1).lower(), bar.group(1).lower()
    return None


def load_theme(root: Path = ROOT) -> dict:
    """Read the book palette from the cover SVG (and the website stylesheet)."""
    palette = dict(DEFAULT_PALETTE)
    cover = root / "templates" / "book-cover.svg"
    if cover.exists():
        svg = cover.read_text(encoding="utf-8")
        primary = next((g for g in (_gradient_stops(svg, i) for i in ("primaryGradient", "bg")) if g), [])
        accent = next((g for g in (_gradient_stops(svg, i) for i in ("accentGradient", "acc")) if g), [])
        bar = re.search(r'<rect x="0" y="0" width="\d+"[^>]*fill="(#[0-9a-fA-F]{6})"', svg)
        if len(primary) >= 2 and _luminance(primary[0]) < 0.35:
            palette["primary"] = primary[0].lower()
            palette["dark"] = primary[-1].lower()
            if len(accent) >= 2:
                palette["accent"], palette["accent2"] = accent[0].lower(), accent[-1].lower()
            elif bar:
                palette["accent"] = palette["accent2"] = bar.group(1).lower()
        else:
            light = _light_cover_palette(svg)
            if light:
                palette["primary"] = light[0]
                palette["dark"] = _mix(light[0], "#000000", 0.45)
                palette["accent"] = palette["accent2"] = light[1]
                palette["light"] = True
            elif len(accent) >= 2 and _luminance(accent[0]) < 0.35:
                # Light cover with an ink gradient (navy to green): ink is primary.
                palette["primary"] = accent[0].lower()
                palette["dark"] = _mix(accent[0], "#000000", 0.4)
                palette["accent"] = palette["accent2"] = accent[-1].lower()
                palette["light"] = True

    tint = _mix(palette["primary"], "#ffffff", 0.88)
    paper = _mix(palette["primary"], "#ffffff", 0.96)
    ground = re.search(r'<rect width="794" height="1123" fill="(#[0-9a-fA-F]{6})"', svg) if cover.exists() else None
    if palette.get("light") and ground:
        paper = ground.group(1).lower()
    css = root / "docs" / "stylesheets" / "series-colours.css"
    if css.exists():
        text = css.read_text(encoding="utf-8")
        for name, key in (("--book-tint", "tint"), ("--book-paper", "paper")):
            found = re.search(name + r":\s*(#[0-9a-fA-F]{6})", text)
            if found:
                if key == "tint":
                    tint = found.group(1).lower()
                else:
                    paper = found.group(1).lower()

    palette.setdefault("light", False)
    palette.update(
        {
            "tint": tint,
            "paper": paper,
            "text": _mix(palette["dark"], "#000000", 0.25),
            "muted": "#5b6776",
            "white": "#ffffff",
            "ghost": _mix(palette["primary"], "#ffffff", 0.07),
        }
    )
    return palette


# --------------------------------------------------------------------------
# Text cleaning
# --------------------------------------------------------------------------
_CITATION = re.compile(r"\s*\(\[\d+[^\]]*\]\([^)]*\)(?:;\s*\[\d+[^\]]*\]\([^)]*\))*\)")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_ANCHOR = re.compile(r"\s*\{#[^}]*\}")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9*(])")


def clean(text: str) -> str:
    """Strip markdown, anchors and citations from a line of manuscript text."""
    text = _CITATION.sub("", text)
    text = _LINK.sub(r"\1", text)
    text = _ANCHOR.sub("", text)
    text = re.sub(r"\[\^[^\]]*\]", "", text)
    text = re.sub(r"[*`]+", "", text)
    text = re.sub(r"(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])", "", text)  # emphasis markers, not identifiers
    text = text.replace("\\", "")
    return re.sub(r"\s+", " ", text).strip()


def _trim_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    cut = " ".join(words[:max_words])
    # End at the last natural pause, if there is one in the second half.
    pause = max(cut.rfind(", "), cut.rfind("; "), cut.rfind(": "))
    if pause > len(cut) * 0.55:
        cut = cut[:pause]
    return cut.rstrip(",;: ") + "."


_QUALIFIER = re.compile(r"source|retrieved|illustrative|sample|estimate|survey|vendor", re.I)


def figure_caption(text: str, max_words: int = 26) -> str:
    """A caption shortened for a slide, keeping what qualifies the data.

    Sentences that name the source, the retrieval year or that mark a figure as
    illustrative, a sample or an estimate are never dropped.
    """
    sentences = [x for x in _SENTENCE_END.split(clean(text)) if x]
    explanation, count = [], 0
    for sentence in sentences:
        if _QUALIFIER.search(sentence):
            continue
        words = len(sentence.split())
        if explanation and count + words > max_words:
            break
        explanation.append(sentence)
        count += words
    qualifiers = [x for x in sentences if _QUALIFIER.search(x)]
    return " ".join(explanation + qualifiers)


def lead_sentences(text: str, max_words: int, min_words: int = 9) -> str:
    """The first whole sentences of ``text`` that fit in ``max_words`` words.

    Introductory sentences shorter than ``min_words`` are skipped when a longer
    one follows. A sentence is never cut: if none fits, the first clause that
    ends at a semicolon or colon is used, and failing that the sentence is
    shown in full with an ellipsis only where it was shortened.
    """
    sentences = [x for x in _SENTENCE_END.split(clean(text)) if x]
    complete = [x for x in sentences if not x.endswith(":")] or sentences  # a lead-in to a list is no conclusion
    substantive = [x for x in complete if len(x.split()) >= min_words] or complete
    chosen, count = [], 0
    for sentence in substantive:
        words = len(sentence.split())
        if not chosen and words > max_words:
            clause = re.split(r"(?<=[;:])\s+", sentence)[0]
            if len(clause.split()) <= max_words and len(clause.split()) >= min_words:
                return clause.rstrip(";:") + "."
            return _trim_words(sentence, max_words).rstrip(".") + "\u2026"
        if chosen and count + words > max_words:
            break
        chosen.append(sentence)
        count += words
        if count >= max_words * 0.55:
            break
    return " ".join(chosen)


# --------------------------------------------------------------------------
# Reading the book
# --------------------------------------------------------------------------
def _read_requirements(root: Path) -> dict:
    text = (root / "BOOK_REQUIREMENTS.md").read_text(encoding="utf-8")
    info = {}
    for key in ("title", "subtitle", "series"):
        match = re.search(r'^  %s:\s*"([^"]*)"' % key, text, re.M)
        info[key] = match.group(1) if match else ""
    year = re.search(r'release_date:\s*"(\d{4})', text)
    info["year"] = year.group(1) if year else str(datetime.now().year)
    return info


def load_book(root: Path = ROOT) -> dict:
    info = _read_requirements(root)
    series = info.get("series") or "The Architecture as Code Series"
    number = re.search(r"Book\s+(\d+)", series)
    cname = root / "CNAME"
    return {
        "title": info.get("title") or "Book",
        "subtitle": info.get("subtitle") or "",
        "series": series,
        "series_name": series.split(",")[0].strip(),
        "number": number.group(1) if number else "",
        "year": info["year"],
        "cover": next((str(c) for c in (root / "docs" / "images" / "book-cover-web.png", root / "docs" / "images" / "book-cover.png") if c.exists()), ""),
        "site": cname.read_text(encoding="utf-8").strip() if cname.exists() else "",
    }


def _paragraphs(lines):
    """Yield body paragraphs (no headings, images, lists or code) from lines."""
    buffer = []
    in_code = False
    for raw in lines:
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            if buffer:
                yield " ".join(buffer)
                buffer = []
            continue
        if line.startswith(("#", "![", "|", "- ", "* ", "\\", ">", "<")) or re.match(r"\d+\.\s", line):
            if buffer:
                yield " ".join(buffer)
                buffer = []
            continue
        if line.startswith("*Figure") or line.startswith("**What you will learn"):
            continue
        buffer.append(line)
    if buffer:
        yield " ".join(buffer)


def _section(lines, heading):
    """Lines of the ``## heading`` section."""
    out, active = [], False
    for line in lines:
        if line.startswith("## "):
            if active:
                break
            active = clean(line[3:]).lower() == heading
            continue
        if active:
            out.append(line)
    return out


def read_chapter(path: Path, identifier: str, part_title: str, root: Path = ROOT) -> dict:
    lines = path.read_text(encoding="utf-8").split("\n")
    title = next((clean(l[2:]) for l in lines if l.startswith("# ")), path.stem)

    sections, in_code = [], False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            heading = clean(line[3:])
            if heading.lower() not in SKIP_SECTIONS:
                sections.append(heading)

    summary = list(_paragraphs(_section(lines, "summary")))
    takeaway = lead_sentences(summary[0], 34) if summary else ""
    if not takeaway:
        intro = list(_paragraphs(lines))
        takeaway = lead_sentences(intro[0], 34) if intro else ""

    figure = None
    for index, line in enumerate(lines):
        found = re.match(r"!\[(.*?)\]\((images/[^)]+\.png)\)", line.strip())
        if not found:
            continue
        image = root / "docs" / found.group(2)
        if not image.exists():
            continue
        alt = clean(found.group(1))
        caption = ""
        for follow in lines[index + 1:index + 4]:
            cap = re.match(r"\*Figure[^:]*:\s*(.*)\*\s*$", follow.strip())
            if cap:
                caption = clean(cap.group(1))
                break
        figure = {"path": str(image.relative_to(root)), "alt": alt, "caption": caption}
        break

    return {
        "identifier": identifier,
        "title": title,
        "part": part_title,
        "sections": sections[:6],
        "takeaway": takeaway,
        "figure": figure,
        "notes": "\n\n".join([title] + summary[:1]).strip() if summary else title,
    }


def collect_deck(root: Path = ROOT) -> list:
    """Return the ordered deck: one entry per part and per chapter."""
    index = json.loads((root / "docs" / "book_index.json").read_text(encoding="utf-8"))
    deck = []
    for part in index.get("parts", []):
        part_id = part.get("id", "")
        intro_files = sorted((root / "docs").glob(part_id + "_*.md"))
        description, bullets = "", []
        if intro_files:
            lines = intro_files[0].read_text(encoding="utf-8").split("\n")
            body = list(_paragraphs(lines))
            description = lead_sentences(body[0], 48) if body else ""
        chapters = part.get("chapters", [])
        deck.append(
            {
                "type": "part",
                "part": {
                    "id": part_id,
                    "title": part.get("title", ""),
                    "description": description,
                    "chapters": [
                        {"identifier": str(c.get("identifier", "")), "title": c.get("title", "")}
                        for c in chapters
                    ],
                },
            }
        )
        for chapter in chapters:
            path = root / chapter["file"]
            if path.exists():
                deck.append(
                    {
                        "type": "chapter",
                        "file": chapter["file"],
                        "chapter": read_chapter(path, str(chapter.get("identifier", "")), part.get("title", ""), root),
                    }
                )
    appendices = [
        a for a in index.get("appendices", [])
        if re.match(r"Appendix\s+[A-Z0-9]+", a.get("title", "")) and (root / a["file"]).exists()
    ]
    if appendices:
        entries = []
        for a in appendices:
            label, _, rest = a["title"].partition(":")
            chapter = read_chapter(root / a["file"], label.split()[-1], "Appendices", root)
            chapter["label"], chapter["title"] = label.strip(), (rest.strip() or chapter["title"])
            entries.append({"type": "chapter", "file": a["file"], "chapter": chapter})
        deck.append(
            {
                "type": "part",
                "part": {
                    "id": "appendices",
                    "title": "Appendices",
                    "description": "",
                    "chapters": [
                        {"identifier": e["chapter"]["identifier"], "title": e["chapter"]["title"]} for e in entries
                    ],
                },
            }
        )
        deck.extend(entries)
    return deck


# --------------------------------------------------------------------------
# Drawing
# --------------------------------------------------------------------------
def _pptx():
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Emu, Inches, Pt

    return RGBColor, MSO_SHAPE, MSO_ANCHOR, PP_ALIGN, Emu, Inches, Pt


class Deck:
    """Draws the slides of one presentation."""

    def __init__(self, prs, theme: dict, book: dict, root: Path = ROOT):
        self.root = root
        (self.RGB, self.SHAPE, self.ANCHOR, self.ALIGN, self.Emu, self.In, self.Pt) = _pptx()
        self.prs = prs
        self.t = theme
        self.book = book
        self.W = 13.333
        self.H = 7.5
        prs.slide_width = self.In(self.W)
        prs.slide_height = self.In(self.H)
        self.number = 0
        # Slides that are dark on a dark cover are light on a light cover.
        self.hero = dict(theme)
        if theme.get("light"):
            self.hero.update({"white": theme["dark"], "tint": theme["muted"], "ghost": theme["tint"]})
        ground = theme["paper"] if theme.get("light") else theme["primary"]
        self.hero["accent_text"] = _legible(theme["accent"], ground)
        self.panel_text = _legible(theme["accent"], theme["primary"]) if not theme.get("light") else theme["tint"]

    # -- primitives ---------------------------------------------------------
    def rgb(self, value):
        return self.RGB(*_hex_to_rgb(value))

    def new_slide(self, title_text, notes=""):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])  # Title Only
        self.number += 1
        title = slide.shapes.title
        title.text_frame.text = title_text  # kept for navigation and screen readers
        if notes:
            slide.notes_slide.notes_text_frame.text = notes
        return slide, title

    def rect(self, slide, x, y, w, h, fill, line=None, shape=None):
        shp = slide.shapes.add_shape(shape or self.SHAPE.RECTANGLE, self.In(x), self.In(y), self.In(w), self.In(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = self.rgb(fill)
        if line:
            shp.line.color.rgb = self.rgb(line)
            shp.line.width = self.Pt(1)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def background(self, slide, colour=None, gradient=False):
        fill = slide.background.fill
        if gradient and self.t.get("light"):
            fill.solid()
            fill.fore_color.rgb = self.rgb(self.t["paper"])
        elif gradient:
            fill.gradient()
            fill.gradient_angle = 35
            fill.gradient_stops[0].color.rgb = self.rgb(self.t["primary"])
            fill.gradient_stops[1].color.rgb = self.rgb(self.t["dark"])
        else:
            fill.solid()
            fill.fore_color.rgb = self.rgb(colour or self.t["white"])

    def style_runs(self, paragraph, runs, size, colour, bold=False, spacing=None):
        for text, opts in runs:
            run = paragraph.add_run()
            run.text = text
            font = run.font
            font.name = FONT
            font.size = self.Pt(opts.get("size", size))
            font.bold = opts.get("bold", bold)
            font.italic = opts.get("italic", False)
            font.color.rgb = self.rgb(opts.get("colour", colour))
            spc = opts.get("spc", spacing)
            if spc:
                run._r.get_or_add_rPr().set("spc", str(spc))

    def bullet(self, paragraph, colour, size):
        """A square bullet in ``colour`` with a hanging indent."""
        from lxml import etree

        ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
        ppr = paragraph._p.get_or_add_pPr()
        indent = int(self.In(0.32))
        ppr.set("marL", str(indent))
        ppr.set("indent", str(-indent))
        for tag, attrs in (
            ("buClr", None),
            ("buSzPct", {"val": "70000"}),
            ("buFont", {"typeface": "Arial"}),
            ("buChar", {"char": "\u25a0"}),
        ):
            element = etree.SubElement(ppr, "{%s}%s" % (ns, tag), attrs or {})
            if tag == "buClr":
                etree.SubElement(element, "{%s}srgbClr" % ns, {"val": colour.lstrip("#")})

    def text(self, slide, x, y, w, h, paragraphs, anchor=None, shape=None):
        """paragraphs: list of dicts(text|runs, size, colour, bold, align, after, line)."""
        box = shape or slide.shapes.add_textbox(self.In(x), self.In(y), self.In(w), self.In(h))
        if shape is not None:
            box.left, box.top, box.width, box.height = self.In(x), self.In(y), self.In(w), self.In(h)
        frame = box.text_frame
        frame.word_wrap = True
        frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
        frame.vertical_anchor = anchor or self.ANCHOR.TOP
        for i, spec in enumerate(paragraphs):
            para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            runs = spec.get("runs") or [(spec["text"], {})]
            self.style_runs(para, runs, spec["size"], spec["colour"], spec.get("bold", False), spec.get("spc"))
            para.alignment = {"right": self.ALIGN.RIGHT, "centre": self.ALIGN.CENTER}.get(spec.get("align"), self.ALIGN.LEFT)
            para.space_after = self.Pt(spec.get("after", 0))
            if spec.get("bullet"):
                self.bullet(para, spec["bullet"], spec["size"])
            para.line_spacing = spec.get("line", 1.0)
        return box

    def title_placeholder(self, title, x, y, w, h, text, size, colour):
        title.left, title.top, title.width, title.height = self.In(x), self.In(y), self.In(w), self.In(h)
        frame = title.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
        frame.vertical_anchor = self.ANCHOR.TOP
        para = frame.paragraphs[0]
        para.alignment = self.ALIGN.LEFT
        para.line_spacing = 0.95
        self.style_runs(para, [(text, {})], size, colour, bold=True, spacing=-30)

    def accent_bar(self, slide):
        bar = self.rect(slide, 0, 0, 0.13, self.H, self.t["accent"])
        return bar

    def footer(self, slide):
        self.rect(slide, 0.8, 6.98, self.W - 1.6, 0.012, self.t["tint"])
        self.text(
            slide, 0.8, 7.05, 9.5, 0.3,
            [{"text": f"{self.book['title']}  |  {self.book['series']}", "size": 10, "colour": self.t["muted"]}],
        )
        self.text(
            slide, self.W - 2.3, 7.05, 1.5, 0.3,
            [{"text": str(self.number), "size": 10, "colour": self.t["muted"], "bold": True, "align": "right"}],
        )

    def kicker(self, slide, text, y=0.5, colour=None):
        self.text(
            slide, 0.8, y, 11.7, 0.3,
            [{"text": text.upper(), "size": 12, "bold": True, "colour": colour or self.t["primary"], "spc": 200}],
        )

    # -- slide types --------------------------------------------------------
    def cover_picture(self, slide, x, y, height, alt):
        """The book's front cover, with a soft offset shadow. Returns the width used."""
        path = self.book.get("cover")
        if not path:
            return 0
        from PIL import Image

        with Image.open(path) as image:
            width = height * image.width / image.height
        self.rect(slide, x + 0.1, y + 0.12, width, height, self.t["dark"])
        picture = slide.shapes.add_picture(path, self.In(x), self.In(y), self.In(width), self.In(height))
        picture._element.nvPicPr.cNvPr.set("descr", alt)
        return width

    def title_slide(self):
        b, t = self.book, self.hero
        slide, title = self.new_slide(
            b["title"],
            f"{b['title']}. {AUTHOR_LINE_1} {AUTHOR_NAME}. {AUTHOR_LINE_2}.",
        )
        self.background(slide, gradient=True)
        has_cover = bool(b.get("cover"))
        if has_cover:
            self.cover_picture(slide, 8.65, 0.7, 6.1, f"Front cover of {b['title']}")
        elif b["number"]:
            self.text(
                slide, 8.0, 4.3, 4.7, 3.0,
                [{"text": b["number"], "size": 190 if len(b["number"]) == 1 else 150, "bold": True, "colour": t["ghost"], "align": "right", "line": 0.8}],
            )
        self.accent_bar(slide)
        self.rect(slide, 1.0, 0.95, 0.6, 0.06, t["accent"])
        self.text(
            slide, 1.8, 0.82, 10, 0.3,
            [{"text": b["series_name"].upper(), "size": 13 if len(b["series_name"]) < 32 else 11, "bold": True, "colour": t["tint"], "spc": 300 if len(b["series_name"]) < 32 else 180}],
        )

        first, _, rest = b["title"].partition(" ")
        rest = rest or ""
        size = 80 if len(rest) <= 10 else 64 if len(rest) <= 14 else 44
        self.title_placeholder(title, 1.0, 1.9, 7.2 if has_cover else 11.3, 2.8, first, size, t["accent_text"])
        paragraph = title.text_frame.add_paragraph()
        paragraph.alignment = self.ALIGN.LEFT
        paragraph.line_spacing = 0.95
        self.style_runs(paragraph, [(rest, {})], size, t["white"], bold=True, spacing=-30)

        if b["subtitle"]:
            self.text(slide, 1.0, 4.9, 7.0, 1.3, [{"text": b["subtitle"], "size": 20, "colour": t["tint"], "line": 1.1}])

        self.text(
            slide, 1.0, 6.25, 6, 0.9,
            [
                {"text": AUTHOR_LINE_1, "size": 12, "colour": t["tint"], "after": 2},
                {"text": AUTHOR_NAME, "size": 20, "bold": True, "colour": t["white"], "after": 2},
                {"text": AUTHOR_LINE_2, "size": 12, "colour": t["tint"]},
            ],
        )
        self.text(
            slide, 4.5, 6.55, 3.5, 0.6,
            [{"text": b["year"], "size": 28, "bold": True, "colour": t["accent_text"], "align": "right"}],
        )

    def part_slide(self, part):
        t = self.hero
        slide, title = self.new_slide(f"{part['title']}", part["description"])
        self.background(slide, gradient=True)
        self.accent_bar(slide)

        numeral = part["id"].replace("part_", "").upper()
        self.kicker(slide, "Appendices" if part["id"] == "appendices" else f"Part {numeral}", y=1.75, colour=t["accent_text"])
        self.title_placeholder(title, 0.9, 2.2, 7.6, 2.0, part["title"], 46, t["white"])
        if part["description"]:
            lines = -(-len(part["title"]) // 20)
            self.text(slide, 0.9, 2.2 + 0.8 * lines + 0.35, 7.4, 2.5, [{"text": part["description"], "size": 18, "colour": t["tint"], "line": 1.15}])

        # Chapter list panel: the type size is chosen so that the wrapped list fits.
        chapters = part["chapters"]
        base = self.t
        size, panel_h = 14, 1.1
        for size in (14, 13, 12, 11, 10):
            per_line = int(3.2 * 72 / (size * 0.56))
            lines = sum(-(-(len(c["title"]) + 4) // per_line) for c in chapters)
            panel_h = 0.9 + lines * size * 1.3 / 72 + len(chapters) * 8 / 72
            if panel_h <= 5.6:
                break
        panel_h = min(panel_h, 6.4)
        top = (self.H - panel_h) / 2
        self.rect(slide, 9.0, top, 3.8, panel_h, t["primary"])
        self.rect(slide, 9.0, top, 3.8, 0.07, t["accent"])
        items = [{"text": "IN THIS PART", "size": 11, "bold": True, "colour": self.panel_text, "spc": 200, "after": 10}]
        for chapter in chapters:
            items.append(
                {
                    "runs": [(f"{chapter['identifier']}  ", {"bold": True, "colour": self.panel_text}), (chapter["title"], {})],
                    "size": size, "colour": base["white"], "after": 8,
                }
            )
        self.text(slide, 9.3, top + 0.35, 3.2, panel_h - 0.5, items)

    def chapter_slide(self, chapter):
        t = self.t
        slide, title = self.new_slide(f"{chapter['title']}", chapter["notes"])
        self.background(slide)
        self.accent_bar(slide)
        self.kicker(slide, f"{chapter.get('label') or 'Chapter ' + chapter['identifier']}  ·  {chapter['part']}")
        self.title_placeholder(title, 0.8, 0.85, 11.7, 1.3, chapter["title"], 34, t["dark"])
        lines = -(-len(chapter["title"]) // 42)
        rule_y = 0.85 + 0.58 * lines + 0.12
        self.rect(slide, 0.8, rule_y, 1.2, 0.06, t["accent"])
        top = rule_y + 0.4

        has_takeaway = bool(chapter["takeaway"])
        width = 6.7 if has_takeaway else 11.7
        total_lines = sum(-(-len(x) // 40) for x in chapter["sections"])
        size = 22 if total_lines <= 8 else 19
        items = [{"text": "IN THIS CHAPTER", "size": 12, "bold": True, "colour": t["primary"], "spc": 200, "after": 10}]
        for section in chapter["sections"]:
            items.append(
                {
                    "text": section, "bullet": t["accent2"],
                    "size": size, "colour": t["text"], "after": 9, "line": 1.05,
                }
            )
        self.text(slide, 0.8, top, width, 6.85 - top, items)

        if has_takeaway:
            tsize = 18 if len(chapter["takeaway"].split()) <= 34 else 16
            card_h = min(6.7 - top, 1.35 + (0.31 if tsize == 18 else 0.28) * -(-len(chapter["takeaway"]) // (28 if tsize == 18 else 31)))
            self.rect(slide, 7.9, top, 4.65, card_h, t["tint"])
            self.rect(slide, 7.9, top, 0.08, card_h, t["primary"])
            self.text(
                slide, 8.25, top + 0.3, 4.0, card_h - 0.5,
                [
                    {"text": "TAKEAWAY", "size": 12, "bold": True, "colour": t["primary"], "spc": 200, "after": 10},
                    {"text": chapter["takeaway"], "size": tsize, "colour": t["dark"], "line": 1.15},
                ],
            )
        self.footer(slide)

    def figure_slide(self, chapter):
        figure = chapter["figure"]
        t = self.t
        caption = figure["caption"] or figure["alt"]
        caption = re.sub(r"^Figure\s*[\d.]+:\s*", "", caption)
        headline, _, rest = caption.partition(". ")
        headline = headline.rstrip(".")
        if len(headline) > 80:
            # Too long for a slide title: the chapter title leads, the caption explains.
            headline, rest = chapter["title"], caption
        slide, title = self.new_slide(headline, chapter["notes"])
        self.background(slide)
        self.accent_bar(slide)
        self.kicker(slide, f"{chapter.get('label') or 'Chapter ' + chapter['identifier']}  ·  {chapter['part']}")
        self.title_placeholder(title, 0.8, 0.85, 11.7, 0.95, headline, 28, t["dark"])

        box_x, box_y, box_w, box_h = 0.8, 1.9, 11.7, 4.25
        self.rect(slide, box_x, box_y, box_w, box_h, t["white"], line=t["tint"])

        from PIL import Image

        figure_path = str(self.root / figure["path"])
        with Image.open(figure_path) as image:
            ratio = image.width / image.height
        pad = 0.2
        max_w, max_h = box_w - 2 * pad, box_h - 2 * pad
        w, h = (max_w, max_w / ratio) if max_w / ratio <= max_h else (max_h * ratio, max_h)
        picture = slide.shapes.add_picture(
            figure_path, self.In(box_x + (box_w - w) / 2), self.In(box_y + (box_h - h) / 2), self.In(w), self.In(h)
        )
        picture._element.nvPicPr.cNvPr.set("descr", figure["alt"] or headline)

        if rest:
            self.text(slide, 0.8, 6.28, 11.7, 0.66, [{"text": figure_caption(rest), "size": 13, "colour": t["muted"], "line": 1.05}])
        self.footer(slide)

    def closing_slide(self):
        b, t = self.book, self.hero
        slide, title = self.new_slide("Read the book", "")
        self.background(slide, gradient=True)
        self.accent_bar(slide)
        self.cover_picture(slide, 9.2, 1.4, 4.7, f"Front cover of {b['title']}")
        self.kicker(slide, b["series_name"], y=2.2, colour=t["accent_text"])
        self.title_placeholder(title, 0.9, 2.65, 8.0, 1.8, b["title"], 44 if len(b["title"]) > 18 else 54, t["white"])
        lines = []
        if b["site"]:
            lines.append({"text": f"Read it at {b['site']}", "size": 24, "bold": True, "colour": t["accent_text"], "after": 6})
        lines.append({"text": f"All books in the series: {SERIES_LANDING}", "size": 18, "colour": t["tint"], "after": 18})
        lines.append({"text": f"{AUTHOR_LINE_1} {AUTHOR_NAME}. {AUTHOR_LINE_2}.", "size": 13, "colour": t["tint"]})
        self.text(slide, 0.9, 4.6, 7.8, 2.2, lines)


def build_deck(prs, deck: list, root: Path = ROOT):
    """Render ``deck`` (from :func:`collect_deck`) into ``prs``."""
    theme = load_theme(root)
    book = load_book(root)
    drawer = Deck(prs, theme, book, root)

    now = datetime.utcnow()
    props = prs.core_properties
    props.author = f"{AUTHOR_LINE_1} {AUTHOR_NAME}; {AUTHOR_LINE_2.lower()}."
    props.title = book["title"]
    props.subject = book["subtitle"] or book["title"]
    props.keywords = f"{book['title']}; {book['series_name']}; presentation"
    props.language = "en-GB"
    props.modified = now

    drawer.title_slide()
    for entry in deck:
        if entry["type"] == "part":
            drawer.part_slide(entry["part"])
        elif entry["type"] == "chapter":
            chapter = entry["chapter"]
            drawer.chapter_slide(chapter)
            if chapter.get("figure"):
                drawer.figure_slide(chapter)
    drawer.closing_slide()
    return prs
