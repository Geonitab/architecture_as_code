"""Automated architecture response generator.

This script composes a markdown outline for addressing an
architecture-labelled GitHub issue. The resulting file lives in
``docs/architecture`` so that subsequent automation can convert it into a
pull request that documents the proposed solution.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str, *, max_length: int = 80) -> str:
    """Convert value to a filesystem-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug or "issue"


def blockquote(text: str) -> str:
    """Format free-form text as a Markdown blockquote."""
    if not text:
        return "> _Issue description was empty when the automation ran._"

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    formatted = [f"> {line.strip()}" if line.strip() else ">" for line in lines]
    return "\n".join(formatted)


def main() -> None:
    issue_number = os.environ.get("ISSUE_NUMBER")
    if not issue_number:
        raise SystemExit("ISSUE_NUMBER environment variable is required")

    issue_title = (os.environ.get("ISSUE_TITLE") or "Untitled Issue").strip()
    issue_body_env = os.environ.get("ISSUE_BODY")
    if issue_body_env is None:
        issue_body = ""
    else:
        body_candidate = str(issue_body_env)
        issue_body = "" if body_candidate.strip().lower() in {"", "null", "none", "undefined"} else body_candidate

    repo_slug = os.environ.get("GITHUB_REPOSITORY", "")
    issue_url = f"https://github.com/{repo_slug}/issues/{issue_number}" if repo_slug else ""

    output_dir = Path("docs/architecture")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{issue_number}-{slugify(issue_title)}.md"
    file_path = output_dir / file_name

    generated_at = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sections = [
        f"# Architecture Response for Issue #{issue_number}: {issue_title}",
        "",
        f"_Generated automatically on {generated_at}._",
    ]

    if issue_url:
        sections.extend(["", f"Issue link: [{issue_url}]({issue_url})"])

    sections.extend(
        [
            "",
            "## Issue Overview",
            blockquote((issue_body or "").strip()),
            "",
            "## Proposed Architecture Solution",
            "1. Confirm the current baseline architecture that the change will impact.",
            "2. Design the target state, highlighting integration points and data flows.",
            "3. Document non-functional requirements and architecture guardrails that must be preserved.",
            "",
            "## Implementation Outline",
            "- [ ] Validate the proposal with stakeholders and capture sign-offs.",
            "- [ ] Update architecture diagrams and supporting documentation.",
            "- [ ] Identify required code or infrastructure changes and owners.",
            "- [ ] Coordinate testing and rollout strategy with the broader team.",
            "",
            "## Risks & Mitigations",
            "- _Add risks discovered during analysis along with mitigation owners._",
            "",
            "## Follow-up Questions",
            "- _List any clarifications needed before implementation proceeds._",
        ]
    )

    content = "\n".join(sections).strip() + "\n"

    file_path.write_text(content, encoding="utf-8")
    print(f"Generated architecture response at {file_path}")


if __name__ == "__main__":
    main()
