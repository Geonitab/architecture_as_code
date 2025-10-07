"""Shared helpers for issue-driven automation bots."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence, Tuple


@dataclass(frozen=True)
class IssueContext:
    """Data extracted from the GitHub issue event."""

    number: str
    title: str
    body: str
    repo_slug: str

    @property
    def issue_url(self) -> str:
        """Return the GitHub issue URL if the repository is known."""
        if self.repo_slug:
            return f"https://github.com/{self.repo_slug}/issues/{self.number}"
        return ""


def slugify(value: str, *, max_length: int = 80) -> str:
    """Convert a string into a filesystem-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug or "issue"


def blockquote(text: str) -> str:
    """Format free-form text as a Markdown blockquote."""
    if not text.strip():
        return "> _Issue description was empty when the automation ran._"

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    formatted = [f"> {line.strip()}" if line.strip() else ">" for line in lines]
    return "\n".join(formatted)


def load_issue_context() -> IssueContext:
    """Construct an IssueContext from environment variables."""
    issue_number = os.environ.get("ISSUE_NUMBER")
    if not issue_number:
        raise SystemExit("ISSUE_NUMBER environment variable is required")

    issue_title = (os.environ.get("ISSUE_TITLE") or "Untitled Issue").strip()
    issue_body_env = os.environ.get("ISSUE_BODY")
    if issue_body_env is None:
        issue_body = ""
    else:
        body_candidate = str(issue_body_env)
        issue_body = (
            ""
            if body_candidate.strip().lower() in {"", "null", "none", "undefined"}
            else body_candidate
        )

    repo_slug = os.environ.get("GITHUB_REPOSITORY", "")
    return IssueContext(number=issue_number, title=issue_title, body=issue_body, repo_slug=repo_slug)


def build_document(
    context: IssueContext,
    *,
    document_type: str,
    sections: Sequence[Tuple[str, Sequence[str]]],
) -> str:
    """Render a Markdown document from the supplied sections."""
    generated_at = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = [
        f"# {document_type} for Issue #{context.number}: {context.title}",
        "",
        f"_Generated automatically on {generated_at}._",
    ]

    issue_url = context.issue_url
    if issue_url:
        lines.extend(["", f"Issue link: [{issue_url}]({issue_url})"])

    for heading, body_lines in sections:
        lines.append("")
        lines.append(f"## {heading}")
        if body_lines:
            lines.extend(body_lines)
        else:
            lines.append("_Add details to this section before finalizing the response._")

    return "\n".join(lines).strip() + "\n"


def write_document(
    context: IssueContext,
    *,
    document_type: str,
    output_directory: Path | str,
    sections: Sequence[Tuple[str, Sequence[str]]],
) -> Path:
    """Write the rendered document to disk and return the resulting path."""
    directory_path = Path(output_directory)
    directory_path.mkdir(parents=True, exist_ok=True)

    file_name = f"{context.number}-{slugify(context.title)}.md"
    file_path = directory_path / file_name

    content = build_document(context, document_type=document_type, sections=sections)
    file_path.write_text(content, encoding="utf-8")

    return file_path
