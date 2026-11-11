# Presentation Design Guidelines

## Purpose

The presentation generated from this book (`generate_presentation.py`, drawing code in `presentation_deck.py`) follows the same graphic profile as the book: the cover, the website and the diagrams. This document records that profile so that the deck, the book and the website stay recognisably one family.

## One profile, taken from the cover

The deck reads its colours from `templates/book-cover.svg`, so a change to the cover changes the deck. Nothing is hard-coded per book; the same generator serves every book in the series.

| Role | Source | Use |
|---|---|---|
| Primary | first stop of `primaryGradient` | gradient start, panels, kickers, links |
| Dark | last stop of `primaryGradient` | gradient end, slide titles |
| Accent | first stop of `accentGradient` | left bar, rules, the first word of the title, year |
| Accent 2 | last stop of `accentGradient` | bullets |
| Tint, paper | `docs/stylesheets/series-colours.css` (or primary mixed with white) | takeaway card, hairlines |

Typeface: **Inter** throughout, as on the cover and the website. Accent colours are used for shapes and for text on dark backgrounds only; on white the text is dark or primary, which keeps the contrast at WCAG AA.

## Slide types

1. **Title slide.** The cover as a slide: diagonal gradient, accent bar on the left edge, the series line, the title in two lines with the first word in the accent colour, the book number as a faint numeral, subtitle, "Conceived and directed by" and the year.
2. **Part divider.** Dark gradient, the part numeral in accent, the part title, the first sentences of the part introduction and a panel listing the part's chapters.
3. **Chapter slide.** One message per slide: the chapter title, the chapter's sections ("In this chapter", at most six) and a takeaway card with the first sentences of the chapter's Summary.
4. **Diagram slide.** The chapter's first figure as large as the slide allows, with its caption. Every picture carries alt text from the manuscript.
5. **Closing slide.** Where to read the book and the series landing page.

Every content slide has the left accent bar, a kicker with chapter and part, a title placeholder (so that outline view and screen readers work), a footer with the book and series, and a slide number. Speaker notes carry the chapter title and the first paragraph of its Summary.

## Content rules

* Structure comes from `docs/book_index.json` (parts and chapters), never from a second list.
* Text is cleaned of markdown, anchors and citations; a takeaway is whole sentences, at most 34 words.
* Body text is at least 18 pt; titles 26-34 pt; footers and captions 10-14 pt.
* Never show raw source paths, diagram types or file names to the audience.
* British English, as in the manuscript.

## Checks

Generate and inspect the deck after any change to the cover palette or to the generator:

```bash
python3 generate_presentation.py --create-pptx
soffice --headless --convert-to pdf presentations/*.pptx   # optional visual check
```
