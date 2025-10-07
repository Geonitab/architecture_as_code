"""Automated documentation response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Documentation Scope",
            [
                "- Identify impacted manuals, READMEs, API references, and inline docs.",
                "- Confirm the target audience and expected depth of explanation.",
                "- Capture assumptions, prerequisites, and terminology that must be defined.",
            ],
        ),
        (
            "Proposed Documentation Outline",
            [
                "1. Summarize the user problem or workflow the documentation must address.",
                "2. List the major sections and the sequence that best supports reader comprehension.",
                "3. Highlight examples, diagrams, or tables that should accompany the text.",
                "4. Define acceptance criteria for when the documentation update is complete.",
            ],
        ),
        (
            "Source Material & Stakeholders",
            [
                "- _List existing documents, SMEs, and systems that will inform the update._",
                "- _Call out reviewers who must sign off on the documentation changes._",
            ],
        ),
        (
            "Next Steps",
            [
                "- [ ] Draft the initial documentation update and link related resources.",
                "- [ ] Request editorial and technical reviews to validate accuracy.",
                "- [ ] Publish the approved update and communicate changes to consumers.",
            ],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Documentation Response",
        output_directory=Path("docs/documentation"),
        sections=sections,
    )
    print(f"Generated documentation response at {file_path}")

if __name__ == "__main__":
    main()
