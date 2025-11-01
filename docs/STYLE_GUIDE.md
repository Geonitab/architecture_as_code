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

## Review Checklist
Before submitting or approving a pull request:
1. Re-read modified content for British spelling and consistent terminology using this guide as the reference.
2. Confirm that any intentional American spellings are limited to code elements or quoted material.
3. Update diagrams and captions after changing text embedded in source files.
4. Run `python3 generate_book.py && docs/build_book.sh` when manuscript content changes to verify outputs.

## Further Reading
- `README.md` – project overview, contribution workflow, and automation commands.
- `VISUAL_ELEMENTS_GUIDE.md` – colour palette, typography, and diagram presentation standards.
- `BRAND_GUIDELINES.md` – brand language and tone requirements.
