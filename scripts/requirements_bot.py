"""Automated requirements response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Requirement Inventory",
            [
                "_Note: Please use British English spelling (e.g., 'optimisation', 'colour', 'organisation') when completing this document._",
                "",
                "- Catalogue functional requirements derived from the issue statement and stakeholders.",
                "- Capture non-functional constraints such as scalability, security, and compliance.",
                "- Note assumptions, dependencies, and out-of-scope elements for clarity.",
            ],
        ),
        (
            "Traceability Plan",
            [
                "1. Map requirements to planned test cases and validation checkpoints.",
                "2. Link requirements to architecture decisions and implementation tasks.",
                "3. Define how changes will be versioned and communicated to downstream teams.",
            ],
        ),
        (
            "Acceptance Criteria",
            [
                "- _List measurable conditions that confirm the requirement is satisfied._",
                "- _Highlight data sources or metrics used to verify completion._",
            ],
        ),
        (
            "Follow-up Actions",
            [
                "- [ ] Review requirements with stakeholders for completeness and accuracy.",
                "- [ ] Update requirement repositories or documents with the approved changes.",
                "- [ ] Share the finalized requirements with QA to seed test design.",
            ],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Requirements Response",
        output_directory=Path("docs/requirements"),
        sections=sections,
    )
    print(f"Generated requirements response at {file_path}")


if __name__ == "__main__":
    main()
