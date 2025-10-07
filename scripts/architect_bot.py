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


def _call_chat_completion(
    payload: dict[str, Any],
    *,
    base_url: str,
    token: str,
    token_name: str,
) -> dict[str, Any] | None:
    """Invoke a chat completion endpoint and return the parsed response."""

    data = json.dumps(payload).encode("utf-8")
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    request = Request(endpoint, data=data, method="POST")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Content-Type", "application/json")

    try:
        with urlopen(request, timeout=60) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
        print(
            "Failed to call chat completion API",
            json.dumps(
                {
                    "token": token_name,
                    "status": exc.code,
                    "reason": exc.reason,
                    "body": error_body,
                }
            ),
        )
        return None
    except URLError as exc:
        print(f"Failed to reach chat completion API using {token_name}: {exc}")
        return None

    try:
        return json.loads(response_body)
    except json.JSONDecodeError:
        print(f"Received a non-JSON response from chat completion API using {token_name}")
        return None


def _github_models_payload(
    *,
    issue_title: str,
    repo_slug: str,
    prompt_body: str,
    model: str,
) -> dict[str, Any]:
    context_payload = {
        "repository": repo_slug,
        "issue_title": issue_title,
        "issue_body": prompt_body or "(No issue description provided)",
    }

    return {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an experienced software architect. Always respond in English. "
                    "Generate actionable architecture plans grounded in the provided GitHub issue. "
                    "Respond ONLY in JSON using the schema that the user provides."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return a JSON object with the following keys: summary (string), architecture_pillars (array), "
                    "system_changes (array), implementation_steps (array), risks (array), open_questions (array). "
                    "Each array element should be either a string or an object with descriptive fields.\n\n"
                    f"Context: {json.dumps(context_payload, ensure_ascii=False)}"
                ),
            },
        ],
    }


def _openai_payload(
    *,
    issue_title: str,
    repo_slug: str,
    prompt_body: str,
    model: str,
) -> dict[str, Any]:
    payload = _github_models_payload(
        issue_title=issue_title,
        repo_slug=repo_slug,
        prompt_body=prompt_body,
        model=model,
    )
    # The OpenAI API expects the model name without the openai/ prefix.
    payload["model"] = model.split("/", 1)[-1]
    return payload


def _generate_ai_sections(issue_body: str, *, issue_title: str, repo_slug: str) -> Sections:
    prompt_body = _trimmed_issue_body(issue_body)

    github_token = os.environ.get("GITHUB_TOKEN")
    github_model = (os.environ.get("GITHUB_MODELS_MODEL") or "openai/gpt-4o").strip()
    github_base_url = os.environ.get("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")

    payload = _github_models_payload(
        issue_title=issue_title,
        repo_slug=repo_slug,
        prompt_body=prompt_body,
        model=github_model or "openai/gpt-4o",
    )

    if github_token:
        response_json = _call_chat_completion(
            payload,
            base_url=github_base_url,
            token=github_token,
            token_name="GITHUB_TOKEN",
        )
        if response_json:
            sections = _parse_ai_sections(response_json, issue_body)
            if sections:
                return sections

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return []

    openai_model = (
        os.environ.get("OPENAI_MODEL")
        or os.environ.get("ARCHITECT_BOT_MODEL")
        or "gpt-4o-mini"
    ).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    openai_payload = _openai_payload(
        issue_title=issue_title,
        repo_slug=repo_slug,
        prompt_body=prompt_body,
        model=openai_model or "gpt-4o-mini",
    )

    response_json = _call_chat_completion(
        openai_payload,
        base_url=base_url,
        token=api_key,
        token_name="OPENAI_API_KEY",
    )
    if not response_json:
        return []

    return _parse_ai_sections(response_json, issue_body)


def _parse_ai_sections(response_json: dict[str, Any], issue_body: str) -> Sections:
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        print("Chat completion response did not include choices")
        return []

    message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
    content = message.get("content", "") if isinstance(message, dict) else ""
    if not content:
        print("Chat completion response did not include message content")
        return []

    try:
        ai_plan = json.loads(content)
    except json.JSONDecodeError:
        print("Chat completion message content was not valid JSON")
        return []

    sections: Sections = [("Issue Overview", [blockquote(issue_body)])]

    summary = str(ai_plan.get("summary") or "").strip()
    if summary:
        sections.append(("AI Summary", [summary]))

    pillars = _format_pillars(_json_list(ai_plan.get("architecture_pillars")))
    if pillars:
        sections.append(("Architecture Pillars", pillars))

    system_changes = _format_simple_list(_json_list(ai_plan.get("system_changes")), numbered=True)
    if system_changes:
        sections.append(("System Changes", system_changes))

    implementation = _format_simple_list(_json_list(ai_plan.get("implementation_steps")), numbered=True)
    if implementation:
        sections.append(("Implementation Outline", implementation))

    risks = _format_risks(_json_list(ai_plan.get("risks")))
    if risks:
        sections.append(("Risks & Mitigations", risks))

    questions = _format_simple_list(_json_list(ai_plan.get("open_questions")))
    if questions:
        sections.append(("Follow-up Questions", questions))

    return sections


def main() -> None:
    context = load_issue_context()
    issue_body = (context.body or "").strip()

    ai_sections = _generate_ai_sections(issue_body, issue_title=context.title, repo_slug=context.repo_slug)
    if ai_sections:
        sections = ai_sections
        print("Generated architecture response with AI assistance")
    else:
        sections = _fallback_sections(issue_body)
        print("Generated architecture response using fallback template")

    file_path = write_document(
        context,
        document_type="Architecture Response",
        output_directory=Path("docs/architecture"),
        sections=sections,
    )
    print(f"Generated architecture response at {file_path}")


if __name__ == "__main__":
    main()
