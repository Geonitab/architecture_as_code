# Standardise Documentation on British English Spelling and Grammar

## Summary
Repository guidelines require British English across all reader-facing content, but numerous markdown chapters and supporting documents still contain American spellings and idioms. Examples include "organized" in `docs/06_structurizr.md`, "color" references within Structurizr snippets, and "digitalization" phrasing in `README.md`. The inconsistency weakens the editorial tone and contradicts the documented language standard.

## Tasks
- Audit every file under `docs/` and the root documentation set (e.g., `README.md`, `BOOK_REQUIREMENTS.md`, `VISUAL_ELEMENTS_GUIDE.md`) for American spellings, idioms, and grammar patterns.
- Replace each instance with the Oxford-standard British equivalent (e.g., organise, colour, digitalisation) while ensuring technical keywords that are intentionally American remain unchanged.
- Update diagrams or code snippets embedded in markdown where text output is affected to keep rendered artefacts consistent.
- Create `docs/STYLE_GUIDE.md` capturing the British English standard, examples of approved spellings, and guidance for future contributions.
- Run the existing build scripts to ensure the language updates do not break automated exports.

## Acceptance Criteria
- All markdown and rendered text assets in the repository read naturally in British English with no lingering American spellings.
- The new `docs/STYLE_GUIDE.md` exists, documents the British English requirements, and is referenced from the contributing section of `README.md`.
- Automated builds (`python3 generate_book.py && docs/build_book.sh`) complete without content regressions after the language updates.
