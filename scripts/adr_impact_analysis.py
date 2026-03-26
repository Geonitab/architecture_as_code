"""ADR impact analysis tool.

Scans all ADR files in docs/examples/structurizr/adrs/ and all chapter files in
docs/ to produce a report showing which chapters reference which ADRs.  The
report is written to stdout and, when --output is supplied, to a Markdown file.

Usage
-----
    python3 scripts/adr_impact_analysis.py
    python3 scripts/adr_impact_analysis.py --output docs/adr/adr_impact_report.md
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── Path constants ─────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_SOURCE_DIR = REPO_ROOT / "docs" / "examples" / "structurizr" / "adrs"
DOCS_DIR = REPO_ROOT / "docs"

# Matches ADR-NNNN identifiers in prose, e.g. "ADR-0001" or "ADR-0003".
ADR_REF_PATTERN = re.compile(r"\bADR-(\d{4})\b")

# Heading pattern used to extract the title line from ADR files.
ADR_TITLE_PATTERN = re.compile(r"^#\s+(ADR-\d{4}:\s*.+)", re.MULTILINE)

# ── Data helpers ───────────────────────────────────────────────────────────────


def _discover_adrs(adr_dir: Path) -> dict[str, dict]:
    """Return a mapping of ADR identifier → metadata dict for every ADR file found."""

    adrs: dict[str, dict] = {}
    for path in sorted(adr_dir.glob("ADR-*.md")):
        text = path.read_text(encoding="utf-8")
        title_match = ADR_TITLE_PATTERN.search(text)
        title = title_match.group(1) if title_match else path.stem

        # Attempt to extract the Status field from the markdown body.
        status_match = re.search(r"^##\s+Status\s*\n+(\S[^\n]*)", text, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else "Unknown"

        # Extract the Date field when present.
        date_match = re.search(r"^##\s+Date\s*\n+(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        adr_date = date_match.group(1) if date_match else "Unknown"

        # Derive ADR identifier from filename prefix, e.g. "ADR-0001".
        stem = path.stem
        id_match = re.match(r"^(ADR-\d{4})", stem)
        adr_id = id_match.group(1) if id_match else stem

        adrs[adr_id] = {
            "id": adr_id,
            "title": title,
            "status": status,
            "date": adr_date,
            "path": path,
        }

    return adrs


def _scan_chapters(docs_dir: Path) -> dict[str, list[str]]:
    """Return a mapping of chapter path (repo-relative) → list of ADR IDs referenced."""

    chapter_refs: dict[str, list[str]] = {}

    # Collect top-level chapter markdown files only (not ADR files themselves).
    chapter_files = sorted(
        f
        for f in docs_dir.glob("*.md")
        if f.is_file()
    )

    for chapter_path in chapter_files:
        text = chapter_path.read_text(encoding="utf-8")
        found = sorted(set(f"ADR-{m}" for m in ADR_REF_PATTERN.findall(text)))
        if found:
            rel = chapter_path.relative_to(REPO_ROOT).as_posix()
            chapter_refs[rel] = found

    return chapter_refs


def _build_adr_to_chapters(
    chapter_refs: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Invert the chapter→ADR mapping to produce ADR→chapters."""

    adr_to_chapters: dict[str, list[str]] = defaultdict(list)
    for chapter, adr_ids in chapter_refs.items():
        for adr_id in adr_ids:
            adr_to_chapters[adr_id].append(chapter)
    return dict(adr_to_chapters)


# ── Report rendering ───────────────────────────────────────────────────────────


def _render_report(
    adrs: dict[str, dict],
    chapter_refs: dict[str, list[str]],
    adr_to_chapters: dict[str, list[str]],
    generated_on: str,
) -> str:
    """Render the full impact analysis report as a Markdown string."""

    lines: list[str] = []

    lines += [
        "# ADR Impact Analysis Report",
        "",
        f"Generated on: {generated_on}",
        "",
        "This report maps each Architecture Decision Record (ADR) to the manuscript "
        "chapters that reference it, and lists chapters alongside the ADRs they mention.  "
        "Use this analysis to assess the blast radius of ADR changes and to identify "
        "chapters requiring updates when a decision is revised or superseded.",
        "",
    ]

    # ── Summary table ──────────────────────────────────────────────────────────

    lines += [
        "## Summary",
        "",
        "| ADR | Status | Referenced in chapters |",
        "| --- | ------ | ---------------------- |",
    ]
    for adr_id in sorted(adrs):
        meta = adrs[adr_id]
        chapters = adr_to_chapters.get(adr_id, [])
        chapter_cell = ", ".join(f"`{c}`" for c in chapters) if chapters else "*(none)*"
        lines.append(f"| {adr_id} | {meta['status']} | {chapter_cell} |")
    lines.append("")

    # ── ADR-to-chapter detail ──────────────────────────────────────────────────

    lines += [
        "## ADR-to-Chapter Mapping",
        "",
        "Each subsection lists the chapters that explicitly mention a given ADR.",
        "",
    ]
    for adr_id in sorted(adrs):
        meta = adrs[adr_id]
        chapters = adr_to_chapters.get(adr_id, [])
        lines += [
            f"### {meta['title']}",
            "",
            f"**Status:** {meta['status']}  ",
            f"**Date:** {meta['date']}  ",
            f"**Source file:** `{meta['path'].relative_to(REPO_ROOT).as_posix()}`",
            "",
        ]
        if chapters:
            lines.append("Chapters referencing this ADR:")
            for chapter in chapters:
                lines.append(f"- `{chapter}`")
        else:
            lines.append("*No chapters currently reference this ADR.*")
        lines.append("")

    # ── Chapter-to-ADR detail ──────────────────────────────────────────────────

    lines += [
        "## Chapter-to-ADR Mapping",
        "",
        "Each row lists the ADRs mentioned within a given chapter.",
        "",
        "| Chapter | ADRs referenced |",
        "| ------- | --------------- |",
    ]
    for chapter in sorted(chapter_refs):
        adr_list = ", ".join(chapter_refs[chapter])
        lines.append(f"| `{chapter}` | {adr_list} |")
    lines.append("")

    # ── Orphaned ADRs ──────────────────────────────────────────────────────────

    orphaned = sorted(adr_id for adr_id in adrs if adr_id not in adr_to_chapters)
    lines += [
        "## Orphaned ADRs (no chapter references)",
        "",
    ]
    if orphaned:
        lines.append(
            "The following ADRs are not referenced in any chapter.  "
            "Consider adding cross-references or reviewing whether the ADR is still relevant."
        )
        lines.append("")
        for adr_id in orphaned:
            meta = adrs[adr_id]
            lines.append(f"- **{adr_id}** – {meta['title']} *(Status: {meta['status']})*")
    else:
        lines.append("All ADRs are referenced in at least one chapter.")
    lines.append("")

    # ── Unresolved references ──────────────────────────────────────────────────

    known_ids = set(adrs.keys())
    all_referenced = {adr_id for ids in chapter_refs.values() for adr_id in ids}
    unresolved = sorted(all_referenced - known_ids)

    lines += [
        "## Unresolved ADR References",
        "",
    ]
    if unresolved:
        lines.append(
            "The following ADR identifiers appear in chapters but do not have a "
            "corresponding ADR file in the ADR directory."
        )
        lines.append("")
        for adr_id in unresolved:
            chapters_mentioning = [c for c, ids in chapter_refs.items() if adr_id in ids]
            chapter_str = ", ".join(f"`{c}`" for c in chapters_mentioning)
            lines.append(f"- **{adr_id}** — referenced in: {chapter_str}")
    else:
        lines.append("All ADR references resolve to known ADR files.")
    lines.append("")

    lines.append(
        "---\n"
        "*Generated automatically via `python3 scripts/adr_impact_analysis.py`. "
        "Do not edit manually.*"
    )

    return "\n".join(lines).rstrip() + "\n"


# ── Entry point ────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyse ADR references across manuscript chapters.",
    )
    parser.add_argument(
        "--adr-dir",
        type=Path,
        default=ADR_SOURCE_DIR,
        metavar="DIR",
        help="Directory containing ADR markdown files (default: docs/examples/structurizr/adrs/).",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DOCS_DIR,
        metavar="DIR",
        help="Directory containing chapter markdown files (default: docs/).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        metavar="FILE",
        help="Optional path to write the Markdown report (e.g. docs/adr/adr_impact_report.md).",
    )
    args = parser.parse_args(argv)

    adr_dir: Path = args.adr_dir
    docs_dir: Path = args.docs_dir

    if not adr_dir.exists():
        print(f"Error: ADR directory not found: {adr_dir}", file=sys.stderr)
        return 1
    if not docs_dir.exists():
        print(f"Error: docs directory not found: {docs_dir}", file=sys.stderr)
        return 1

    adrs = _discover_adrs(adr_dir)
    if not adrs:
        print(f"Warning: no ADR files found in {adr_dir}.", file=sys.stderr)

    chapter_refs = _scan_chapters(docs_dir)
    adr_to_chapters = _build_adr_to_chapters(chapter_refs)
    generated_on = date.today().strftime("%Y-%m-%d")

    report = _render_report(adrs, chapter_refs, adr_to_chapters, generated_on)

    print(report)

    if args.output:
        output_path: Path = args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
