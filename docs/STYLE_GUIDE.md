# Architecture as Code Editorial Style Guide {#style-guide}

## Purpose
This guide defines the editorial standards for all reader-facing content in the Architecture as Code repository. It ensures that every manuscript chapter, supporting document, and diagram text is written in consistent British English while respecting technical terminology and brand language.

## Language Standard
- Use Oxford-standard British English spelling and grammar across all Markdown, HTML, and diagram annotations.
- Retain original spelling for proper nouns, trademarks, API fields, CLI commands, configuration keys, and code identifiers.
- Prefer inclusive, internationally recognisable phrasing and avoid colloquialisms.

## Preferred Spellings
The following table lists common conversions that must be applied during reviews:

| American English | British English |
| ---------------- | --------------- |
| organize, organized, organizing | organise, organised, organising |
| organization, organizations, organizational | organisation, organisations, organisational |
| optimize, optimized, optimizing | optimise, optimised, optimising |
| optimization, optimizations, optimizer | optimisation, optimisations, optimiser |
| color, colors, color-coded | colour, colours, colour-coded |
| center, centered, centers | centre, centred, centres |
| behavior, behavioral | behaviour, behavioural |
| digitization, digitalization | digitisation, digitalisation |
| containerization | containerisation |
| modernization, standardization | modernisation, standardisation |

> **Note:** When a spelling appears inside code samples, configuration files, or API responses, keep the source spelling. Update accompanying prose and comments to British English instead.

## Grammar and Punctuation
- Apply the serial (Oxford) comma in lists for clarity.
- Use single quotation marks (`‘ ’`) for quotations within quotations; otherwise prefer double quotation marks.
- Write dates in ISO format (`2025-10-15`) or in long-form style (`15 October 2025`).
- Hyphenate compound adjectives where it improves readability (e.g., “code-first mindset”).

## Terminology and Tone
- Always refer to the discipline and book title as **Architecture as Code**, keeping “as” in lower case and capitalising “Architecture” and “Code”. Avoid variations such as “Architecture As Code” or “architecture as code” unless quoting another source.
- Refer to audiences collectively as “teams”, “practitioners”, or “organisations” rather than region-specific labels unless the chapter explicitly targets a geography.
- Use “programme” for initiatives and “programme owners” in keeping with British usage.
- Maintain formal, instructional tone that suits professional and academic readers.

## Diagram and Asset Text
- When editing Mermaid, Structurizr, or image annotations, ensure on-screen captions, callouts, and labels follow British English.
- Regenerate images or diagrams after updating embedded text to keep rendered assets in sync.

### Gantt Chart Best Practices
When creating or updating Gantt chart diagrams:
1. **Theme Configuration**: Always include the Kvadrat theme init block at the top of `.mmd` files:
   ```mermaid
   %%{init: {'theme':'base', 'themeVariables': {...}}}%%
   ```
2. **Colour Palette**: Use approved Kvadrat colours for consistency:
   - Done tasks: `#1E3A8A` (Kvadrat Blue Dark) with white text `#F8FAFC`
   - Active tasks: `#2563EB` (Kvadrat Blue) with white text `#F8FAFC`
   - Future tasks: `#60A5FA` (Kvadrat Blue Light) with dark text `#0F172A`
   - Backgrounds: `#E0F2FE` (Ice Blue) and `#F8FAFF` (Ice Blue Light)
3. **Accessibility**: Ensure all text has sufficient contrast (WCAG AA minimum 4.5:1 for normal text)
4. **Typography**: Use Inter font family matching the book's design system
5. **British English**: Task labels must use British spelling (e.g., "Optimisation" not "Optimization")
6. **Regeneration**: Run `npx mmdc -i <file>.mmd -o <file>.png -b transparent` after any changes

## Citation and Reference Style

All chapters must follow a single consistent citation standard throughout the manuscript.

### Inline citations

Use numbered source links pointing to `33_references.md`:

```markdown
[Source [4]](33_references.md#source-4)
```

Where a readable author–year reference is more natural in prose, use the format `Surname (Year)` on first mention, followed by a numbered source link:

```markdown
Skelton & Pais (2019) [Source [7]](33_references.md#source-7)
```

Do **not** use bare attributions such as `Red Hat (2023)` without an accompanying source link.

### End-of-chapter sources sections

Each chapter should close with a `## Sources` section listing cited works as an ordered list. Each entry must include:
- Author(s) and year in **bold**
- Full title in *italics*
- Publisher or URL
- Source link anchor matching `33_references.md`

Example:
```markdown
## Sources

1. **Skelton, M. & Pais, M. (2019).** *Team Topologies.* IT Revolution Press. [Source [7]](33_references.md#source-7)
2. **Forsgren, N., Humble, J. & Kim, G. (2018).** *Accelerate.* IT Revolution Press. [Source [8]](33_references.md#source-8)
```

### Bibliography anchor format

When adding or editing entries in `33_references.md`, use pandoc-native span syntax for numbered source anchors:

```markdown
[**Source [N]:**]{#source-N}
```

This format (using the `bracketed_spans` extension) works consistently across all output formats: MkDocs, PDF, EPUB, and DOCX.

**Do not** use HTML `<a id="source-N"></a>` anchors — they are not reliably processed by all pandoc output backends.

When adding a new source:
1. Assign the next available source number N
2. Add `[**Source [N]:**]{#source-N} Author. *Title.* Publisher, Year.` to the numbered index in `33_references.md`
3. Add the full entry to the appropriate alphabetical section
4. Update the chapter `## Sources` sections that reference it

### Prohibited citation forms

- Category descriptions such as "Industry reports on Architecture as Code adoption trends" are **not** acceptable citations — replace with the actual document or remove.
- Placeholder text such as "Best practice documentation from leading organisations" must not appear in published content.
- Unresolved template strings such as `YYYYMM` in evidence file paths must be replaced with concrete values or explained in prose.

### Chapter 33 (References)

`docs/33_references.md` is the canonical bibliography. Every source cited inline must have a corresponding entry there. Source anchor IDs must follow the pattern `source-N` (e.g., `#source-4`).

## Review Checklist
Before submitting or approving a pull request:
1. Re-read modified content for British spelling and consistent terminology using this guide as the reference.
2. Confirm that any intentional American spellings are limited to code elements or quoted material.
3. Update diagrams and captions after changing text embedded in source files.
4. Run `python3 generate_book.py && docs/build_book.sh` when manuscript content changes to verify outputs.

## Further Reading
- `README.md` – project overview, contribution workflow, and automation commands.
- `AUTHOR_PERSONA.md` – authorial voice, technical register, and IT architect vocabulary.
- `VISUAL_ELEMENTS_GUIDE.md` – colour palette, typography, and diagram presentation standards.
- `BRAND_GUIDELINES.md` – brand language and tone requirements.
