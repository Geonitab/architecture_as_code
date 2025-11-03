"""Utility functions for validating Architecture Decision Records."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from pathlib import Path
from typing import Iterable, List, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_DIRECTORY = REPO_ROOT / "adr"
DOCS_DIRECTORY = REPO_ROOT / "docs"

ADR_ID_PATTERN = re.compile(r"^ADR-(?P<number>\d{4})$")
REFERENCED_ADR_PATTERN = re.compile(r"\bADR-(?P<number>\d{4})\b")

SAMPLE_ADR_IDENTIFIERS = {"ADR-XXXX", "ADR-0001", "ADR-0002"}

REQUIRED_LIST_FIELDS = {
    "deciders",
    "reviewers",
    "related_chapters",
    "related_diagrams",
    "related_backlog_items",
}

REQUIRED_SCALAR_FIELDS = {
    "adr_id",
    "title",
    "status",
    "date",
    "last_reviewed",
    "next_review_due",
}

ALLOWED_STATUS = {"Proposed", "Accepted", "Deprecated", "Superseded"}


class AdrValidationError(RuntimeError):
    """Raised when ADR metadata fails validation."""


@dataclass(frozen=True)
class AdrRecord:
    """Container for parsed ADR metadata."""

    adr_id: str
    title: str
    status: str
    date: date
    last_reviewed: date
    next_review_due: date
    deciders: Sequence[str]
    reviewers: Sequence[str]
    related_chapters: Sequence[Path]
    related_diagrams: Sequence[Path]
    related_backlog_items: Sequence[str]
    source_path: Path
    front_matter: dict
    body: str


def _split_front_matter(text: str, *, source: Path) -> tuple[str, str]:
    """Split Markdown text into YAML front matter and body."""

    if not text.startswith("---\n"):
        raise AdrValidationError(f"{source} is missing YAML front matter header.")

    end_marker = text.find("\n---", 4)
    if end_marker == -1:
        raise AdrValidationError(f"{source} front matter is not terminated with '---'.")

    front_matter = text[4:end_marker]
    body_start = end_marker + 4
    body = text[body_start:].lstrip("\n")
    return front_matter, body


def _parse_date(value: str, *, field: str, source: Path) -> date:
    try:
        year, month, day = (int(part) for part in value.split("-"))
        return date(year, month, day)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise AdrValidationError(
            f"{source} field '{field}' must be formatted as YYYY-MM-DD."
        ) from exc


def _validate_required_fields(front_matter: dict, *, source: Path) -> None:
    missing_scalar = [key for key in REQUIRED_SCALAR_FIELDS if key not in front_matter]
    missing_list = [key for key in REQUIRED_LIST_FIELDS if key not in front_matter]

    if missing_scalar or missing_list:
        problems: List[str] = []
        if missing_scalar:
            problems.append(f"missing scalar fields: {', '.join(sorted(missing_scalar))}")
        if missing_list:
            problems.append(f"missing list fields: {', '.join(sorted(missing_list))}")
        raise AdrValidationError(f"{source} metadata incomplete ({'; '.join(problems)}).")

    for key in REQUIRED_LIST_FIELDS:
        if not isinstance(front_matter[key], list) or not front_matter[key]:
            raise AdrValidationError(
                f"{source} field '{key}' must be a non-empty list."
            )

    for key in REQUIRED_SCALAR_FIELDS:
        if not isinstance(front_matter[key], str) or not front_matter[key].strip():
            raise AdrValidationError(
                f"{source} field '{key}' must be a populated string."
            )


def _normalise_paths(paths: Iterable[str], *, base: Path, source: Path) -> list[Path]:
    resolved: list[Path] = []
    for entry in paths:
        candidate = Path(entry)
        if candidate.is_absolute():
            raise AdrValidationError(
                f"{source} field contains absolute path '{candidate}'. Use repository relative paths."
            )
        full = (base / candidate).resolve()
        if not full.exists():
            raise AdrValidationError(
                f"{source} references missing artefact '{candidate.as_posix()}'."
            )
        resolved.append(full)
    return resolved


def load_adr_records(directory: Path | None = None) -> list[AdrRecord]:
    """Parse and validate ADR files from the repository."""

    adr_directory = directory or ADR_DIRECTORY
    if not adr_directory.exists():
        raise AdrValidationError(f"ADR directory not found at {adr_directory}.")

    records: list[AdrRecord] = []
    for path in sorted(adr_directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        front_matter_text, body = _split_front_matter(text, source=path)
        try:
            front_matter = yaml.safe_load(front_matter_text) or {}
        except yaml.YAMLError as exc:  # pragma: no cover - YAML errors are rare
            raise AdrValidationError(f"{path} front matter could not be parsed.") from exc

        _validate_required_fields(front_matter, source=path)

        adr_id = front_matter["adr_id"].strip()
        if ADR_ID_PATTERN.fullmatch(adr_id) is None:
            raise AdrValidationError(
                f"{path} field 'adr_id' must match pattern ADR-0000."
            )

        expected_stem = adr_id.replace("-", "-")
        if not path.name.startswith(adr_id):
            raise AdrValidationError(
                f"{path.name} should start with '{adr_id}' to aid discoverability."
            )

        status = front_matter["status"].strip()
        if status not in ALLOWED_STATUS:
            raise AdrValidationError(
                f"{path} has unsupported status '{status}'. Allowed: {', '.join(sorted(ALLOWED_STATUS))}."
            )

        adr_date = _parse_date(front_matter["date"], field="date", source=path)
        last_reviewed = _parse_date(
            front_matter["last_reviewed"], field="last_reviewed", source=path
        )
        next_review_due = _parse_date(
            front_matter["next_review_due"], field="next_review_due", source=path
        )

        if last_reviewed < adr_date:
            raise AdrValidationError(
                f"{path} field 'last_reviewed' ({last_reviewed:%Y-%m-%d}) cannot precede 'date' ({adr_date:%Y-%m-%d})."
            )

        if next_review_due <= last_reviewed:
            raise AdrValidationError(
                f"{path} field 'next_review_due' ({next_review_due:%Y-%m-%d}) must be after 'last_reviewed' ({last_reviewed:%Y-%m-%d})."
            )

        related_chapters = _normalise_paths(
            front_matter["related_chapters"], base=REPO_ROOT, source=path
        )
        related_diagrams = _normalise_paths(
            front_matter["related_diagrams"], base=REPO_ROOT, source=path
        )

        backlog_items = front_matter["related_backlog_items"]
        backlog_pattern = re.compile(r"^[A-Z][A-Z0-9_-]+-\d+")
        for entry in backlog_items:
            if not isinstance(entry, str) or not entry.strip():
                raise AdrValidationError(
                    f"{path} field 'related_backlog_items' must contain reference strings."
                )
            if backlog_pattern.fullmatch(entry.strip()) is None:
                raise AdrValidationError(
                    f"{path} backlog reference '{entry}' must follow KEY-1234 format."
                )

        deciders = [str(value).strip() for value in front_matter["deciders"]]
        reviewers = [str(value).strip() for value in front_matter["reviewers"]]

        if any(not entry for entry in deciders):
            raise AdrValidationError(f"{path} deciders list contains blank entries.")
        if any(not entry for entry in reviewers):
            raise AdrValidationError(f"{path} reviewers list contains blank entries.")

        records.append(
            AdrRecord(
                adr_id=adr_id,
                title=front_matter["title"].strip(),
                status=status,
                date=adr_date,
                last_reviewed=last_reviewed,
                next_review_due=next_review_due,
                deciders=tuple(deciders),
                reviewers=tuple(reviewers),
                related_chapters=tuple(related_chapters),
                related_diagrams=tuple(related_diagrams),
                related_backlog_items=tuple(entry.strip() for entry in backlog_items),
                source_path=path,
                front_matter=front_matter,
                body=body,
            )
        )

    if not records:
        raise AdrValidationError("No ADR files were found for validation.")

    return records


def find_referenced_adrs(docs_directory: Path | None = None) -> set[str]:
    """Return the set of ADR identifiers referenced across the manuscript."""

    docs_path = docs_directory or DOCS_DIRECTORY
    referenced: set[str] = set()

    for markdown_path in docs_path.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for match in REFERENCED_ADR_PATTERN.finditer(text):
            referenced.add(match.group(0))

    return referenced


def ensure_references_have_records(
    *, records: Sequence[AdrRecord], referenced_ids: Iterable[str]
) -> None:
    """Ensure every referenced ADR has a corresponding record."""

    available = {record.adr_id for record in records}
    referenced = set(referenced_ids) - SAMPLE_ADR_IDENTIFIERS
    missing = sorted(referenced - available)
    if missing:
        raise AdrValidationError(
            "Missing ADR files for referenced identifiers: " + ", ".join(missing)
        )


def main() -> int:
    """Command-line entry point that validates ADR metadata."""

    try:
        records = load_adr_records()
        ensure_references_have_records(
            records=records, referenced_ids=find_referenced_adrs()
        )
    except AdrValidationError as exc:
        print(f"ADR validation failed: {exc}")
        return 1

    print(f"Validated {len(records)} ADR files with consistent metadata.")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI passthrough
    raise SystemExit(main())
