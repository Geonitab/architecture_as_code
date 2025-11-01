# Archive Index

This directory stores manuscript material that has been retired from the primary publication flow described in `docs/book_structure.md`. Items remain valuable for research and translation reference but are excluded from `docs/build_book.sh` so that only the canonical chapters are rendered.

## Archive policy

- Use descriptive filenames **without leading numerals**. Numeric prefixes are reserved for active chapters and interfere with tooling that enumerates the live table of contents.
- Record the archival date and motivation in the inventory below whenever content is moved into this directory.
- When reviving an archived piece, move it back to `docs/`, restore any required numbering, and update both `docs/build_book.sh` and the book structure tables accordingly.

## Inventory

| File | Archived | Origin | Reason for archival |
| --- | --- | --- | --- |
| `cloud_architecture.md` | 2025-10-23 | Former Chapter 06 (Swedish draft) | Superseded when the cloud coverage was rewritten and integrated into the current English chapters. |
| `microservices_architecture_en.md` | 2025-10-23 | English translation of the retired Chapter 08 draft | Retained only as a translation reference after the live microservices chapter was rewritten. |
| `lovable_mockups_sv.md` | 2025-10-23 | Former Chapter 20 workshop material | Case-study specifics about the Lovable tooling no longer fit the general-purpose narrative of Part D. |
| `future_trends_sv.md` | 2025-10-23 | Swedish-language draft of Chapter 25 | Replaced by the current English Chapter 25 focused on future trends. |
| `future_development_sv.md` | 2025-10-23 | Swedish-language continuation of Chapter 26 | Folded into the updated anti-patterns and conclusion chapters, leaving this draft as background context. |


> **Historical note:** The former Chapter 32 on code-oriented organisations was previously archived here. Should it return, rename it to a descriptive filename (for example, `code_oriented_organisations.md`) before re-adding it to this index.
