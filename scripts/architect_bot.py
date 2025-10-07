"""Automated architecture response generator with optional AI assistance."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from issue_bot_base import blockquote, load_issue_context, write_document


SectionContent = list[str]
Sections = list[tuple[str, SectionContent]]


def _fallback_sections(issue_body: str) -> Sections:
    """Return the legacy hand-authored outline when AI is unavailable."""

    return [
        ("Issue Overview", [blockquote(issue_body)]),
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


def _trimmed_issue_body(raw_body: str, *, max_length: int = 6000) -> str:
    """Prepare the issue body for prompts while keeping context concise."""

    normalized = (raw_body or "").strip()
    if len(normalized) <= max_length:
        return normalized
    truncated = normalized[:max_length].rsplit(" ", 1)[0]
    return f"{truncated}\n\n[Issue body truncated for brevity]"


def _json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _extract_message_content(message: Any) -> str:
    """Return the textual content from a chat completion message payload."""

    if isinstance(message, dict):
        content = message.get("content")
    else:
        content = message

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                elif "content" in item:
                    parts.append(str(item["content"]))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(part.strip() for part in parts if part.strip())

    if content is None:
        return ""

    return str(content).strip()


def _format_pillars(pillars: Iterable[Any]) -> SectionContent:
    lines: SectionContent = []
    for pillar in pillars:
        if isinstance(pillar, dict):
            title = str(pillar.get("title") or pillar.get("name") or "Key focus").strip()
            details = str(pillar.get("details") or pillar.get("summary") or "").strip()
            if details:
                lines.append(f"- **{title}**: {details}")
            else:
                lines.append(f"- **{title}**")
        else:
            lines.append(f"- {str(pillar)}")
    return lines


def _format_simple_list(items: Iterable[Any], *, numbered: bool = False) -> SectionContent:
    lines: SectionContent = []
    for index, item in enumerate(items, start=1):
        text = str(item).strip()
        if not text:
            continue
        if numbered:
            lines.append(f"{index}. {text}")
        else:
            prefix = "- " if text[0] not in {"-", "*"} else ""
            lines.append(f"{prefix}{text}")
    return lines


def _format_risks(risks: Iterable[Any]) -> SectionContent:
    lines: SectionContent = []
    for risk in risks:
        if isinstance(risk, dict):
            description = str(risk.get("risk") or risk.get("description") or "").strip()
            mitigation = str(risk.get("mitigation") or risk.get("response") or "").strip()
            owner = str(risk.get("owner") or "").strip()
            parts = [description] if description else []
            if mitigation:
                parts.append(f"Mitigation: {mitigation}")
            if owner:
                parts.append(f"Owner: {owner}")
            if parts:
                lines.append(f"- {' | '.join(parts)}")
        else:
            text = str(risk).strip()
            if text:
                lines.append(f"- {text}")
    return lines


# Additional functions and the main() function can be explored further in the provided link.