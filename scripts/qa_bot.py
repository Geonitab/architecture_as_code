"""Automated quality assurance response generator."""
from __future__ import annotations

from pathlib import Path

from issue_bot_base import blockquote, load_issue_context, write_document


def main() -> None:
    context = load_issue_context()

    sections = [
        ("Issue Overview", [blockquote((context.body or "").strip())]),
        (
            "Quality Objectives",
            [
                "_Note: Please use British English spelling (e.g., 'optimisation', 'colour', 'organisation') when completing this document._",
                "",
                "- Enumerate the quality attributes that must be validated (reliability, usability, performance, etc.).",
                "- Note compliance, regulatory, or documentation requirements tied to the change.",
                "- Capture entry and exit criteria for each testing phase.",
            ],
        ),
        (
            "Test Strategy",
            [
                "1. Define test environments, data sets, and tooling required.",
                "2. Outline manual and automated coverage expectations by test type.",
                "3. Identify risk-based test scenarios and mitigation actions.",
            ],
        ),
        (
            "Metrics & Reporting",
            [
                "- _List KPIs, dashboards, or checklists that will track quality status._",
                "- _Specify owners responsible for triage, defect management, and sign-off._",
            ],
        ),
        (
            "Planned Activities",
            [
                "- [ ] Align with development and requirements teams to confirm readiness.",
                "- [ ] Prepare regression suites and update test documentation as needed.",
                "- [ ] Communicate release criteria and go/no-go decision points.",
            ],
        ),
    ]

    file_path = write_document(
        context,
        document_type="Quality Assurance Response",
        output_directory=Path("docs/quality"),
        sections=sections,
    )
    print(f"Generated quality assurance response at {file_path}")


if __name__ == "__main__":
    main()
