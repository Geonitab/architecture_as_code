# Docs Folder Audit

This audit summarises the current structure of the `docs/` directory, highlights which markdown files participate in the automated build, and identifies content that has been archived for later review.

## Canonical Chapter Set

The PDF/EPUB build script enumerates the 36 markdown chapters and appendices that make up the active manuscript. Only files listed in `CHAPTER_FILES` are rendered into book outputs, which keeps the production pipeline aligned with the official table of contents.【F:docs/build_book.sh†L189-L222】

## Archived Material

`docs/archive/` stores manuscripts that are no longer part of the canonical chapter run. At present it contains the former Chapter 32, retained as background reading while similar organisational guidance is refined elsewhere.【F:docs/book_structure.md†L81-L108】【F:docs/archive/README.md†L1-L9】

## Supporting Directories

The remaining subdirectories (`images/`, `design/`, `documentation/`, `development/`, `quality/`, `requirements/`, `agents/`, and `architecture/`) provide diagrams, automation stubs, or bot-generated planning notes. These resources complement the chapters but are intentionally excluded from the chapter list that feeds the publishing workflow.【F:docs/book_structure.md†L7-L139】【F:docs/development/README.md†L1-L6】【F:docs/architecture/178-new-architecture.md†L1-L18】

Maintainers can revisit this audit whenever chapter scope changes to ensure the build pipeline and directory layout stay in sync.
