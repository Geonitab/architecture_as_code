"""Automated design response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Design Objectives",
            [
                "- Capture the user goals, brand considerations, and success metrics for the design work.",
                "- Note accessibility requirements, responsive breakpoints, and localization constraints.",
                "- Identify technical limitations or design tokens that must be reused.",
            ],
        ),
        (
            "Concept Exploration",
            [
                "1. Outline initial concepts or moodboards that will be produced.",
                "2. Describe interaction flows and state transitions to visualize.",
                "3. Highlight assets that require collaboration with illustration or content teams.",
            ],
        ),
        (
            "Deliverables",
            [
                "- _List expected outputs such as wireframes, high-fidelity mocks, prototypes, or design specs._",
                "- _Specify file formats, naming conventions, and storage locations._",
            ],
        ),
        (
            "Review & Sign-off Plan",
            [
                "- [ ] Schedule checkpoints with stakeholders for feedback loops.",
                "- [ ] Validate alignment with the design system and branding guidelines.",
                "- [ ] Document final approvals and handoff requirements for developers.",
            ],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Design Response",
        output_directory=Path("docs/design"),
        sections=sections,
    )
    print(f"Generated design response at {file_path}")


if __name__ == "__main__":
    main()
