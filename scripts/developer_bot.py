"""Automated development response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Functional Goals",
            [
                "_Note: Please use British English spelling (e.g., 'optimisation', 'colour', 'organisation') when completing this document._",
                "",
                "- Describe the user stories or system capabilities that must be delivered.",
                "- Capture constraints related to performance, security, or compatibility.",
                "- List cross-team dependencies or integrations that must be coordinated.",
            ],
        ),
        (
            "Implementation Plan",
            [
                "1. Outline the architectural approach and key technical decisions.",
                "2. Break down work into milestones or tasks with clear ownership.",
                "3. Identify new modules, APIs, database changes, or configuration updates.",
                "4. Define test strategies including unit, integration, and end-to-end coverage.",
            ],
        ),
        (
            "Validation Criteria",
            [
                "- _Document measurable acceptance criteria and telemetry needed to confirm success._",
                "- _List rollout steps, feature flags, or migration plans if applicable._",
            ],
        ),
        (
            "Action Items",
            [
                "- [ ] Create or update tracking issues for each implementation task.",
                "- [ ] Align with QA and documentation to plan supporting updates.",
                "- [ ] Schedule demos or checkpoints to review progress with stakeholders.",
            ],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Development Response",
        output_directory=Path("docs/development"),
        sections=sections,
    )
    print(f"Generated development response at {file_path}")


if __name__ == "__main__":
    main()
