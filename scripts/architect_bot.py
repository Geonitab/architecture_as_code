"""Automated architecture response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Proposed Architecture Solution",
            [
                "1. Confirm the current baseline architecture that the change will impact.",
                "2. Design the target state, highlighting integration points and data flows.",
                "3. Document non-functional requirements and architecture guardrails that must be preserved.",
            ],
        ),
        (
            "Implementation Outline",
            [
                "- [ ] Validate the proposal with stakeholders and capture sign-offs.",
                "- [ ] Update architecture diagrams and supporting documentation.",
                "- [ ] Identify required code or infrastructure changes and owners.",
                "- [ ] Coordinate testing and rollout strategy with the broader team.",
            ],
        ),
        (
            "Risks & Mitigations",
            ["- _Add risks discovered during analysis along with mitigation owners._"],
        ),
        (
            "Follow-up Questions",
            ["- _List any clarifications needed before implementation proceeds._"],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Architecture Response",
        output_directory=Path("docs/architecture"),
        sections=sections,
    )
    print(f"Generated architecture response at {file_path}")


if __name__ == "__main__":
    main()
