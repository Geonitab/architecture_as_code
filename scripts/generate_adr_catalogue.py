"""Generate documentation assets derived from ADR metadata."""
from __future__ import annotations

from pathlib import Path
from textwrap import indent
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:  # pragma: no cover - defensive guard for CLI execution
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_adrs import AdrRecord, AdrValidationError, load_adr_records

CATALOGUE_PATH = REPO_ROOT / "docs" / "adr" / "adr_catalogue.md"


def _format_list(values: list[str]) -> str:
    return "<br>".join(values)


def _summarise_records(records: list[AdrRecord]) -> str:
    lines: list[str] = []
    lines.append("| ADR | Title | Status | Linked chapters | Backlog items | Next review |")
    lines.append("| --- | ----- | ------ | --------------- | ------------- | ----------- |")
    for record in records:
        chapter_values = [path.relative_to(REPO_ROOT).as_posix() for path in record.related_chapters]
        backlog_values = list(record.related_backlog_items)
        lines.append(
            "| {adr} | {title} | {status} | {chapters} | {backlog} | {review} |".format(
                adr=record.adr_id,
                title=record.title,
                status=record.status,
                chapters=_format_list(chapter_values),
                backlog=_format_list(backlog_values),
                review=record.next_review_due.strftime("%Y-%m-%d"),
            )
        )
    return "\n".join(lines)


def _detailed_section(record: AdrRecord) -> str:
    lines: list[str] = [f"### {record.adr_id} – {record.title}"]
    lines.append("")
    summary = record.front_matter.get("summary")
    if summary:
        lines.append(summary)
        lines.append("")

    lines.append("**Status:** {status} — initial decision recorded on {date:%Y-%m-%d}.".format(
        status=record.status,
        date=record.date,
    ))
    lines.append("**Review cadence:** Last reviewed on {last:%Y-%m-%d}; next review due {due:%Y-%m-%d}.".format(
        last=record.last_reviewed,
        due=record.next_review_due,
    ))

    lines.append("")
    lines.append("**Deciders:** " + ", ".join(record.deciders))
    lines.append("**Reviewers:** " + ", ".join(record.reviewers))
    lines.append("")

    chapter_lines = "\n".join(
        f"- `{path.relative_to(REPO_ROOT).as_posix()}`" for path in record.related_chapters
    )
    diagram_lines = "\n".join(
        f"- `{path.relative_to(REPO_ROOT).as_posix()}`" for path in record.related_diagrams
    )
    backlog_lines = "\n".join(f"- {item}" for item in record.related_backlog_items)

    lines.append("**Linked chapters**\n" + indent(chapter_lines, ""))
    lines.append("")
    lines.append("**Supporting diagrams**\n" + indent(diagram_lines, ""))
    lines.append("")
    lines.append("**Backlog alignment**\n" + indent(backlog_lines, ""))

    automation = record.front_matter.get("automation_hooks")
    if automation:
        lines.append("")
        lines.append("**Automation hooks**")
        if isinstance(automation, list):
            lines.extend(f"- {entry}" for entry in automation)
        else:
            lines.append(str(automation))

    history = record.front_matter.get("change_notes")
    if history:
        lines.append("")
        lines.append("**Change log**")
        if isinstance(history, list):
            lines.extend(f"- {entry}" for entry in history)
        else:
            lines.append(f"- {history}")

    return "\n".join(lines)


def render_catalogue(records: list[AdrRecord]) -> str:
    """Return the markdown catalogue for the supplied ADR records."""

    sorted_records = sorted(records, key=lambda record: record.adr_id)

    lines: list[str] = ["# Architecture Decision Record Catalogue {#adr-catalogue}", ""]
    lines.append(
        "This catalogue is generated from the structured ADR metadata committed to the repository. "
        "It keeps the documentation site, book manuscript, and automation backlog aligned by ensuring "
        "every referenced ADR includes links to chapters, diagrams, and delivery work items."
    )
    lines.append("")
    lines.append("## Summary overview")
    lines.append("")
    lines.append(_summarise_records(sorted_records))
    lines.append("")
    lines.append("## Detailed records")
    lines.append("")

    for record in sorted_records:
        lines.append(_detailed_section(record))
        lines.append("")

    lines.append(
        "---\n"
        "*Generated automatically via `python3 scripts/generate_adr_catalogue.py`. Do not edit manually.*"
    )

    return "\n".join(lines).rstrip() + "\n"


def write_catalogue(destination: Path = CATALOGUE_PATH) -> Path:
    """Generate the ADR catalogue and write it to disk."""

    try:
        records = load_adr_records()
    except AdrValidationError as exc:  # pragma: no cover - CLI guard
        raise SystemExit(f"Unable to load ADR metadata: {exc}") from exc

    destination.parent.mkdir(parents=True, exist_ok=True)
    content = render_catalogue(records)
    destination.write_text(content, encoding="utf-8")
    return destination


def main() -> int:
    write_catalogue()
    print(f"ADR catalogue updated at {CATALOGUE_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI passthrough
    raise SystemExit(main())
