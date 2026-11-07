# Whitepaper Design Guidelines for Architecture as Code
## One-chapter summaries that look like the book

## Purpose
This document defines the design standards for the whitepapers generated from the content of *Architecture as Code*, one HTML file per chapter. A whitepaper is the book's shop window for that chapter, so it takes the look of the book itself: the palette of the cover, the cover band as its header, Inter for text and JetBrains Mono for code. It is professionally formatted, accessible, and prints to A4.

The implementation is `templates/whitepaper-template.html` (design) and `generate_whitepapers.py` (content). The tests are `tests/test_whitepaper_generation.py` and `tests/test_whitepaper_template.py`.

---

## Core Design Principles

### 1. The whitepaper belongs to the book
- **One palette per book**: the six `--book-*` colours below, taken from the cover. Nothing else carries colour.
- **Cover band**: the header repeats the cover's construction (two-tone gradient over the 40 px series grid, an accent edge, an uppercase eyebrow, a large faint chapter number), so a reader who has seen the cover recognises the page.
- **Accent colours decorate, they do not carry text on white.** Accents are light on several books (amber, lime, pink), so they are used for rules, numbers, the left edge, button fills and text on the dark band only.

### 2. Reading experience
- **Scannable structure**: the chapter first (figure, opening paragraphs, topics), then the book (what it is, who should read it), then the call to action.
- **Progressive information**: a lead paragraph in a larger size, then the body, then the topic list.
- **Visual relief**: one figure with its caption, tinted topic cards, white space.
- **Optimal line length**: the text column is 160 mm wide on A4, about 85 characters at 16 px.

### 3. Accessibility and standards
- **WCAG AA contrast** for all text (see the measured table below).
- **Semantic HTML5**: one `h1` (the title in the header), `h2` for sections, `figure` and `figcaption` for diagrams, `header`, `main` and `footer` landmarks.
- **Responsive**: usable from 320 px; the cover band and the topic grid collapse to one column.
- **Print**: A4, full-bleed first page, clean page breaks.

---

## Document Format and Structure

### Standard Dimensions
- **Page size**: A4 (210 mm x 297 mm) on screen and in print.
- **Text margins**: 25 mm on both sides; the cover band is full-bleed.
- **Print margins**: `@page` has 18 mm top and bottom margins, and none on the first page so that the cover band reaches the edge.

### Typography Standards

#### Font Families
- **Primary**: [Inter](https://fonts.google.com/specimen/Inter), weights 300 to 900 (the cover uses 900 for titles; whitepapers use 800).
- **Monospace**: [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono), weights 400 to 600, for code and for the feature tags.

#### Type Scale
| Element | Size | Weight | Colour | Usage |
|---|---|---|---|---|
| **Title** (`h1`) | 38px | 800 | White on the band | Chapter title before the first colon (see below) |
| **Subtitle** | 19px | 400 | White at 84% | Chapter title after the colon, or "Key insights from ..." |
| **Eyebrow** | 11.5px | 700, uppercase, 0.16em | White | Book title and "Whitepaper", with the accent bar |
| **Kicker** | 13.5px | 600 | Accent | Chapter label and part |
| **Section title** (`h2`) | 24px | 800 | `--book-primary` | With a 36 x 4 px accent bar above |
| **Lead paragraph** | 17.5px | 400 | Ink | First paragraph, accent rule on the left |
| **Body** | 16px | 400 | Ink | Line height 1.65 |
| **Caption** | 13px | 400 | Muted | Under the figure |
| **Labels** | 10.5 to 12px | 700, uppercase | Accent on the band, `--book-primary` on white | Metadata and callout titles |
| **Inline code** | 0.88em | 400 | `--book-primary` on `--book-tint` | |
| **Code block** | 14px | 400 | `#E5E7EB` on `--book-dark` | Prism.js token colours |

### Colour Palette
The palette is read at generation time from the Book 1 cover (this book's website keeps the MkDocs default theme, so there is no `series-colours.css`). `generate_whitepapers.py` writes it into the template as a `:root` override; the template's own defaults are the Book 1 cover.

| Token | Architecture as Code | Use |
|---|---|---|
| `--book-dark` | `#1F2A3C` | Dark end of the gradient, code blocks, footer |
| `--book-primary` | `#1B3A7A` | Light end of the gradient, headings |
| `--book-strong` | `#1D4ED8` | Links, topic numbers, callout edge |
| `--book-accent` | `#60A5FA` | Edge, rules, kicker, button fill, tags |
| `--book-tint` | `#E6EEFB` | Topic cards, callouts, inline code |
| `--book-paper` | `#F6F8FB` | Page background on screen, book panel |

Neutrals are shared by every book: `--ink: #182033`, `--muted: #4F5B71`, `--rule: #DFE5EE`.

#### Contrast (measured for this book's palette)
| Pair | Colours | Ratio | WCAG |
|---|---|---|---|
| Body text on white | `#182033` on `#FFFFFF` | 16.2:1 | AAA |
| Muted text (figure captions) on white | `#4F5B71` on `#FFFFFF` | 6.8:1 | AA |
| Headings and links on white | `#1B3A7A` on `#FFFFFF` | 10.9:1 | AAA |
| Link colour on white | `#1D4ED8` on `#FFFFFF` | 6.7:1 | AA |
| White text on the cover band (darkest end) | `#FFFFFF` on `#1F2A3C` | 14.4:1 | AAA |
| White text on the cover band (lightest end) | `#FFFFFF` on `#1B3A7A` | 10.9:1 | AAA |
| Accent text on the cover band (kicker, labels) | `#60A5FA` on `#1F2A3C` | 5.7:1 | AA |
| Button text on the accent colour | `#1F2A3C` on `#60A5FA` | 5.7:1 | AA |

`generate_whitepapers.py` does not check contrast. When the palette changes, recompute this table; every pair must reach 4.5:1.

---

## Whitepaper Components

### 1. Cover band (header)
```html
<header class="whitepaper-header" data-chapter-number="6">
    <p class="eyebrow">Architecture as Code · Whitepaper</p>
    <p class="kicker">Chapter 6 · Architecture Platform</p>
    <h1 class="title">Structurizr: Architecture Modelling as Code</h1>
    <p class="subtitle">Key insights from Chapter 6 of "Architecture as Code"</p>
    <div class="meta-info">...</div>
    <div class="feature-tags">...</div>
</header>
```
- **Title and subtitle**: the chapter title is split at its first colon when what precedes it has at least three words ("Contestability by Design: Explanation, Appeal and Correction" gives a title and a subtitle). Shorter openings ("Introduction: Who Is the Boss?") stay whole. With no colon, the subtitle is "Key insights from [label] of "[book]"" for a chapter and "[label] from "[book]"" for an appendix.
- **Chapter number**: shown large and faint at the bottom right of the band, from `data-chapter-number` through a CSS pseudo-element, only for labels of the form "Chapter N". Appendices have none.
- **Kicker**: chapter label and part, separated by a middle dot.
- **Metadata**: author, published date (British English, no leading zero) and build number, on a hairline.
- **Feature tags**: outlined pills in JetBrains Mono, written as in `BOOK_REQUIREMENTS.md` (for example `ai-agents`).
- **Left edge**: a 6 px accent border, as on the cover.

### 2. Chapter content
```html
<section class="chapter-highlight">
    <figure class="chapter-figure">
        <img src="../docs/images/diagram_06_....png" alt="Figure 6.1: ...">
        <figcaption>Figure 6.1: ...</figcaption>
    </figure>
    <p class="lead">[First paragraph]</p>
    <p>[Second and third paragraphs]</p>
    <h2>Primary topics explored</h2>
    <ol class="topics"><li>[Section heading]</li> ...</ol>
</section>
```
- **Source of the text**: the first three prose paragraphs of the chapter, and its first six `##` headings. Table rows, list items, block quotes, code, HTML comments and the line under the figure are skipped.
- **Inline Markdown** is rendered (bold, italics, code); citations lose their link and read "(30, Nordqvist, 2025)"; links to other chapters become plain text; Pandoc anchors such as `{#chapter-anchor}` are removed.
- **Figure**: the caption is the chapter's own "Figure N.M" line, falling back to the image's alt text.
- **Topics**: numbered cards in two columns (one on mobile), at most six.

### 3. About the book
A tinted panel with the accent edge: a section title "About *Architecture as Code*", the book description in paragraphs (the description in `get_book_overview()` is wrapped at blank lines, never at line ends), and a callout "Who should read this".

### 4. Call to action
A dark panel in the cover's gradient with a button, "Read the full chapter online", that links to the chapter on the book's site (`https://[CNAME]/[chapter-file-stem]/`, which is where MkDocs publishes it with `use_directory_urls`), a sentence naming the chapter, and a sentence placing the whitepaper in its part and in the set of N whitepapers. Without a `CNAME` file the button is omitted.

### 5. Footer
A dark band with the accent rule: "© [year] Gunnar Nordqvist. Published by GEON IT AB." on the left, and the book title and its website on the right.

---

## Code Samples and Technical Content

### Inline Code
JetBrains Mono at 0.88em on `--book-tint`, colour `--book-primary`.

### Code Blocks
- **Syntax highlighting**: Prism.js with the "Tomorrow" theme, loaded from cdnjs.
- **Background**: `--book-dark`, with a 4 px `--book-accent` left border, 16 px padding and 8 px radius.
- **Supported languages**: YAML, JSON, Python, Bash, JavaScript, TypeScript, Docker, Terraform.

---

## Responsive and Print Considerations

### Responsive
At 768 px and below the page is full width, the cover band has 20 px side padding, the title drops to 29 px, the topic grid and the metadata stack, and the faint chapter number shrinks.

### Print
```css
@page { size: A4; margin: 18mm 0; }
@page :first { margin: 0; }
@media print {
    .page { width: auto; box-shadow: none; }
    h2, h3 { break-after: avoid; }
    .chapter-figure, .callout, .topics li, .call-to-action, .book-overview, pre { break-inside: avoid; }
}
```
Backgrounds are printed (`print-color-adjust: exact`), so the cover band, the footer and the call to action keep their colour. A whitepaper normally runs to four A4 pages.

---

## Release pipeline constraints
The combined whitepapers PDF in the release is made by a shell step that takes everything from the first line containing the opening body tag to the line containing the closing body tag, strips the tags line by line, and gives the text to Pandoc. Three rules follow, and `tests/test_whitepaper_template.py` enforces them:
1. The opening body tag appears once, as the real tag. No comment, script or style mentions it before that.
2. Every tag in the body is complete on its own line.
3. Decorative text (the chapter number, the topic numbers) is produced by CSS pseudo-elements, so it does not end up in the PDF text. Styles stay in `head`.

---

## Accessibility Standards

### Semantic HTML5
- `header`, `main` and `footer` landmarks; `section` for content blocks.
- One `h1`; `h2` for section titles; `h3` is available inside content.
- `figure` and `figcaption` for diagrams; `strong` and `em` for emphasis.

### ARIA and metadata
- Feature tags use `role="list"` and `role="listitem"`.
- Images always carry descriptive `alt` text (the figure caption).
- The page element carries `data-release-version`, `data-feature-tags` and `data-release-codename` for programmatic access.

---

## File Naming and Organisation
- **Pattern**: `[chapter-filename]_whitepaper.html`, for example `06_structurizr_whitepaper.html`.
- **Location**: `releases/whitepapers/` (release mode) or `whitepapers/` (standard mode).
- **Diagrams**: `docs/images/`, referenced by a path relative to the whitepaper; the figure is omitted when a chapter has none.

---

## Quality Checklist

### Content
- [ ] The title, subtitle and kicker match the chapter; no Pandoc anchor or Markdown marker is visible.
- [ ] The opening paragraphs are prose (no table rows or drafting comments).
- [ ] The figure shows the chapter's own caption.
- [ ] The call to action links to the chapter on the book's site.

### Design
- [ ] The colours are the book's cover palette, read from `series-colours.css`.
- [ ] The cover band reaches the page edge in print and keeps its colour.
- [ ] Text meets WCAG AA contrast (table above).
- [ ] The layout works at 390 px width and prints to four A4 pages or fewer.

### Technical
- [ ] `python3 -m unittest tests.test_whitepaper_generation tests.test_whitepaper_template` passes.
- [ ] The body tag rules of the release pipeline hold (test above).
- [ ] Fonts and Prism.js load from their CDNs.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 5 November 2025 | Gunnar Nordqvist | Initial whitepaper design guidelines created |
| 2.0 | 7 November 2026 | Claude Code | Redesigned to follow the book's cover: per-book palette, cover band, chapter first, footer naming the author and GEON IT AB, release-pipeline rules |

---

**Note**: These guidelines align with [PRESENTATION_DESIGN_GUIDELINES.md](PRESENTATION_DESIGN_GUIDELINES.md) and [STYLE_GUIDE.md](STYLE_GUIDE.md) and with the series website at https://books.geon.se.
