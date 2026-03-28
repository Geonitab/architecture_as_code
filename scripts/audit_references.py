#!/usr/bin/env python3
"""
Audit citation deviations across all canonical manuscript chapters.

Scans every chapter in the canonical chapter list (from navigation.py /
mkdocs.yml) and reports:

  - Chapters missing a ``## Sources`` section entirely
  - Non-standard reference-section headers (e.g. ``## References``,
    ``## Sources and References``)
  - Inline citations not matching ``[Source [N]](33_references.md#source-N)``
  - Cited source numbers that have no corresponding anchor in
    ``docs/33_references.md``
  - Anchors defined in ``docs/33_references.md`` that are never cited in any
    chapter

Output is written to ``reports/reference_audit.md`` and a summary is also
printed to stdout.

Usage:
    python3 scripts/audit_references.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# Path setup — allow running from repo root or scripts/
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from navigation import REPO_ROOT, get_book_build_files  # noqa: E402

DOCS_DIR = REPO_ROOT / "docs"
REFERENCES_FILE = DOCS_DIR / "33_references.md"
REPORTS_DIR = REPO_ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "reference_audit.md"

# ---------------------------------------------------------------------------
# Compiled regular expressions
# ---------------------------------------------------------------------------

# The canonical sources header is exactly ``## Sources`` (nothing after it).
_STANDARD_SOURCES_RE = re.compile(r"^## Sources\s*$", re.MULTILINE)

# Non-standard variants that look like a references section but are wrong.
_NON_STANDARD_HEADER_RE = re.compile(
    r"^(#{1,3})\s+"
    r"(References?|Sources?\s+and\s+[Rr]eferences?|Sources?\s+and\s+[Ss]ources?)"
    r"\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# A well-formed inline citation: [Source [N]](33_references.md#source-N)
# Captures the cited number from the link text and the anchor number.
_STANDARD_INLINE_RE = re.compile(
    r"\[Source \[(\d+)\]\]\(33_references\.md#source-(\d+)\)"
)

# Any ``[Source [`` token — used to find *all* citation-like patterns so we
# can flag those that do not satisfy the standard form above.
_ANY_SOURCE_BRACKET_RE = re.compile(r"\[Source \[")

# Anchors in 33_references.md — both HTML and Pandoc/Commonmark formats.
# HTML:   <a id="source-N">
# Pandoc span: [anything]{#source-N} — matched by looking for ]{#source-N}
#   because the span text may contain nested brackets (e.g. [**Source [1]:**])
_ANCHOR_HTML_RE = re.compile(r'<a\s+id="source-(\d+)"')
_ANCHOR_PANDOC_RE = re.compile(r"\]\{#source-(\d+)\}")

# ---------------------------------------------------------------------------
# Data collection helpers
# ---------------------------------------------------------------------------


def load_reference_anchors(references_path: Path) -> Set[int]:
    """Return the set of source numbers declared as anchors in references.md."""
    if not references_path.exists():
        return set()
    text = references_path.read_text(encoding="utf-8")
    html_ids = {int(m) for m in _ANCHOR_HTML_RE.findall(text)}
    pandoc_ids = {int(m) for m in _ANCHOR_PANDOC_RE.findall(text)}
    return html_ids | pandoc_ids


def audit_chapter(
    chapter_path: Path,
) -> Dict:
    """
    Audit a single chapter file and return a dict of findings:

    ``missing_sources_section`` : bool
    ``non_standard_headers``    : list of (line_number, header_text) tuples
    ``malformed_citations``     : list of (line_number, raw_text) tuples
    ``cited_source_numbers``    : set of ints (numbers from standard citations)
    """
    findings: Dict = {
        "missing_sources_section": False,
        "non_standard_headers": [],
        "malformed_citations": [],
        "cited_source_numbers": set(),
    }

    if not chapter_path.exists():
        findings["missing_sources_section"] = True
        return findings

    text = chapter_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Check for standard ## Sources section.
    if not _STANDARD_SOURCES_RE.search(text):
        findings["missing_sources_section"] = True

    # 2. Detect non-standard reference headers.
    for match in _NON_STANDARD_HEADER_RE.finditer(text):
        line_no = text[: match.start()].count("\n") + 1
        findings["non_standard_headers"].append((line_no, match.group(0).strip()))

    # 3. Collect standard citations and detect malformed ones.
    for line_no, line in enumerate(lines, start=1):
        # Collect all well-formed citations on this line first.
        for std_match in _STANDARD_INLINE_RE.finditer(line):
            text_num = int(std_match.group(1))
            anchor_num = int(std_match.group(2))
            # Both numbers should match; if they differ, flag as malformed.
            if text_num == anchor_num:
                findings["cited_source_numbers"].add(text_num)
            else:
                findings["malformed_citations"].append(
                    (
                        line_no,
                        std_match.group(0),
                        "Citation text number and anchor number do not match",
                    )
                )

        # Find any ``[Source [`` tokens not covered by the standard pattern.
        # We do this by removing all standard hits from the line and checking
        # whether any ``[Source [`` tokens remain.
        stripped = _STANDARD_INLINE_RE.sub("", line)
        for _ in _ANY_SOURCE_BRACKET_RE.finditer(stripped):
            findings["malformed_citations"].append(
                (
                    line_no,
                    line.strip(),
                    "Citation does not match [Source [N]](33_references.md#source-N)",
                )
            )
            break  # one report per line is enough to keep the report readable

    return findings


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def _chapter_display_name(rel_path: str) -> str:
    """Return a short display name for a chapter relative path."""
    return Path(rel_path).name


def generate_report(
    chapter_findings: List[Tuple[str, Dict]],
    defined_anchors: Set[int],
    all_cited: Set[int],
) -> Tuple[str, str]:
    """
    Build the Markdown report and a plain-text summary.

    Returns ``(markdown_report, stdout_summary)``.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    missing_sources: List[str] = []
    non_standard: List[Tuple[str, List]] = []
    malformed: List[Tuple[str, List]] = []

    for rel_path, findings in chapter_findings:
        name = _chapter_display_name(rel_path)
        if findings["missing_sources_section"]:
            missing_sources.append(name)
        if findings["non_standard_headers"]:
            non_standard.append((name, findings["non_standard_headers"]))
        if findings["malformed_citations"]:
            malformed.append((name, findings["malformed_citations"]))

    # Anchors cited but not defined in references.md
    missing_anchors = sorted(all_cited - defined_anchors)

    # Anchors defined but never cited
    orphaned_anchors = sorted(defined_anchors - all_cited)

    # ---- Markdown report -----------------------------------------------
    md_lines: List[str] = []
    md_lines.append("# Reference Audit Report\n")
    md_lines.append(f"**Generated:** {now}\n")
    md_lines.append("")
    md_lines.append("## Summary\n")
    md_lines.append(f"| Check | Count |")
    md_lines.append(f"|-------|-------|")
    md_lines.append(f"| Chapters missing `## Sources` section | {len(missing_sources)} |")
    md_lines.append(f"| Chapters with non-standard reference headers | {len(non_standard)} |")
    md_lines.append(f"| Chapters with malformed inline citations | {len(malformed)} |")
    md_lines.append(f"| Cited source numbers missing from `33_references.md` | {len(missing_anchors)} |")
    md_lines.append(f"| Anchors in `33_references.md` never cited | {len(orphaned_anchors)} |")
    md_lines.append("")

    # Missing Sources sections
    md_lines.append("## Chapters Missing `## Sources` Section\n")
    if missing_sources:
        for name in missing_sources:
            md_lines.append(f"- `{name}`")
    else:
        md_lines.append("_None — all chapters have a `## Sources` section._")
    md_lines.append("")

    # Non-standard headers
    md_lines.append("## Non-Standard Reference Section Headers\n")
    if non_standard:
        md_lines.append(
            "These chapters use a header other than `## Sources` for their reference section:\n"
        )
        for name, headers in non_standard:
            md_lines.append(f"### `{name}`\n")
            for line_no, header_text in headers:
                md_lines.append(f"- Line {line_no}: `{header_text}`")
            md_lines.append("")
    else:
        md_lines.append("_None — all reference headers use the standard `## Sources` form._")
    md_lines.append("")

    # Malformed inline citations
    md_lines.append("## Malformed Inline Citations\n")
    if malformed:
        md_lines.append(
            "These chapters contain citation-like patterns that do not conform to "
            "`[Source [N]](33_references.md#source-N)`:\n"
        )
        for name, cites in malformed:
            md_lines.append(f"### `{name}`\n")
            for line_no, raw, reason in cites:
                # Truncate long raw lines for readability
                display = raw[:120] + "…" if len(raw) > 120 else raw
                md_lines.append(f"- Line {line_no} — {reason}:")
                md_lines.append(f"  ```")
                md_lines.append(f"  {display}")
                md_lines.append(f"  ```")
            md_lines.append("")
    else:
        md_lines.append("_None — all inline citations are well-formed._")
    md_lines.append("")

    # Missing anchors
    md_lines.append("## Cited Sources Missing Anchors in `33_references.md`\n")
    if missing_anchors:
        md_lines.append(
            "These source numbers are cited in chapter text but have no corresponding "
            "`<a id=\"source-N\">` or `[]{#source-N}` anchor in `docs/33_references.md`:\n"
        )
        for n in missing_anchors:
            md_lines.append(f"- Source [{n}]")
    else:
        md_lines.append("_None — every cited source number has an anchor in `33_references.md`._")
    md_lines.append("")

    # Orphaned anchors
    md_lines.append("## Anchors in `33_references.md` Never Cited\n")
    if orphaned_anchors:
        md_lines.append(
            "These anchors are defined in `docs/33_references.md` but are not referenced "
            "by any inline citation in any chapter:\n"
        )
        for n in orphaned_anchors:
            md_lines.append(f"- Source [{n}]")
    else:
        md_lines.append(
            "_None — every anchor in `33_references.md` is cited at least once._"
        )
    md_lines.append("")

    markdown_report = "\n".join(md_lines)

    # ---- Stdout summary -------------------------------------------------
    sep = "=" * 70
    summary_lines = [
        sep,
        "Reference Audit Summary",
        sep,
        f"Chapters missing ## Sources section:         {len(missing_sources)}",
        f"Chapters with non-standard headers:          {len(non_standard)}",
        f"Chapters with malformed inline citations:    {len(malformed)}",
        f"Cited sources missing anchors in refs file:  {len(missing_anchors)}",
        f"Orphaned anchors in refs file (never cited): {len(orphaned_anchors)}",
        sep,
    ]
    stdout_summary = "\n".join(summary_lines)

    return markdown_report, stdout_summary


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> int:
    print("Reference Audit — Architecture as Code")
    print("=" * 70)

    # Resolve canonical chapter list.
    try:
        book_files = get_book_build_files()
    except Exception as exc:
        print(f"Error: could not load canonical chapter list — {exc}", file=sys.stderr)
        return 1

    # Load anchors defined in 33_references.md.
    defined_anchors = load_reference_anchors(REFERENCES_FILE)
    print(
        f"Loaded {len(defined_anchors)} source anchors from "
        f"{REFERENCES_FILE.relative_to(REPO_ROOT)}"
    )

    # Audit each chapter (skip part intros and the references file itself).
    chapter_findings: List[Tuple[str, Dict]] = []
    all_cited: Set[int] = set()

    skip_stems = {"33_references"}  # the references file is not a chapter

    for rel_path in book_files:
        path_obj = Path(rel_path)
        stem = path_obj.stem

        # Skip part introduction pages — they don't carry citations.
        if stem.startswith("part_"):
            continue

        # Skip the references file itself.
        if stem in skip_stems:
            continue

        chapter_path = DOCS_DIR / rel_path
        findings = audit_chapter(chapter_path)
        chapter_findings.append((rel_path, findings))
        all_cited |= findings["cited_source_numbers"]

    print(f"Audited {len(chapter_findings)} chapter files")

    # Generate report.
    markdown_report, stdout_summary = generate_report(
        chapter_findings, defined_anchors, all_cited
    )

    # Write Markdown report.
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(markdown_report, encoding="utf-8")
    print(f"Report written to {REPORT_FILE.relative_to(REPO_ROOT)}")

    # Print summary.
    print()
    print(stdout_summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
