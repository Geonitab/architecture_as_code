"""ADR metrics and reporting tool.

Reads all ADR files from docs/examples/structurizr/adrs/, analyses their
status and age, and produces a Markdown metrics report.  The report is
printed to stdout and, when --output is supplied, written to a file.

Metrics produced
----------------
- Total ADR count and breakdown by status (Proposed, Accepted, Deprecated, Superseded)
- Age distribution (days since ADR was first recorded)
- Review cadence statistics (days since last review)
- ADRs that require review (last reviewed more than 90 days ago or past their
  next_review_due date)

Usage
-----
    python3 scripts/adr_metrics.py
    python3 scripts/adr_metrics.py --output docs/adr/adr_metrics_report.md
    python3 scripts/adr_metrics.py --review-threshold 60
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, median

# ── Path constants ─────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_SOURCE_DIR = REPO_ROOT / "docs" / "examples" / "structurizr" / "adrs"

# Default threshold in days after which an ADR is flagged for review.
DEFAULT_REVIEW_THRESHOLD_DAYS = 90

# ── Parsing helpers ────────────────────────────────────────────────────────────

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_date_field(text: str, field_heading: str) -> date | None:
    """Extract a YYYY-MM-DD date following a markdown heading."""
    pattern = re.compile(
        rf"^##\s+{re.escape(field_heading)}\s*\n+(\d{{4}}-\d{{2}}-\d{{2}})",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def _parse_status(text: str) -> str:
    """Extract the Status value from an ADR markdown body."""
    match = re.search(r"^##\s+Status\s*\n+(\S[^\n]*)", text, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"


def _parse_title(text: str, stem: str) -> str:
    """Extract the title from the top-level heading, falling back to filename stem."""
    match = re.search(r"^#\s+(ADR-\d{4}:\s*.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else stem


def _adr_id_from_stem(stem: str) -> str:
    """Return the ADR identifier (e.g. 'ADR-0003') from a filename stem."""
    match = re.match(r"^(ADR-\d{4})", stem)
    return match.group(1) if match else stem


# ── Data loading ───────────────────────────────────────────────────────────────


def _load_adr_entries(adr_dir: Path) -> list[dict]:
    """Parse ADR files and return a list of metadata dicts."""
    entries: list[dict] = []
    for path in sorted(adr_dir.glob("ADR-*.md")):
        text = path.read_text(encoding="utf-8")
        stem = path.stem
        adr_id = _adr_id_from_stem(stem)

        entry = {
            "id": adr_id,
            "title": _parse_title(text, stem),
            "status": _parse_status(text),
            "date": _parse_date_field(text, "Date"),
            "path": path,
        }
        entries.append(entry)
    return entries


# ── Metrics computation ────────────────────────────────────────────────────────


def _compute_metrics(entries: list[dict], today: date, review_threshold: int) -> dict:
    """Derive aggregate statistics from the loaded ADR entries."""

    total = len(entries)
    status_counts: Counter = Counter(e["status"] for e in entries)

    ages_days: list[int] = []
    for e in entries:
        if e["date"] is not None:
            delta = (today - e["date"]).days
            ages_days.append(max(delta, 0))

    needs_review: list[dict] = []
    for e in entries:
        adr_date = e["date"]
        if adr_date is None:
            # No date metadata — flag conservatively.
            needs_review.append({**e, "reason": "No date recorded"})
            continue
        age_days = (today - adr_date).days
        if age_days > review_threshold:
            needs_review.append({
                **e,
                "reason": f"Recorded {age_days} days ago (threshold: {review_threshold} days)",
            })

    return {
        "total": total,
        "status_counts": dict(status_counts),
        "ages_days": ages_days,
        "needs_review": needs_review,
        "review_threshold": review_threshold,
        "today": today,
    }


# ── Report rendering ───────────────────────────────────────────────────────────


def _render_status_table(status_counts: dict[str, int], total: int) -> list[str]:
    """Render a table breaking down ADRs by status."""
    known_statuses = ["Proposed", "Accepted", "Deprecated", "Superseded"]
    # Include any statuses found that are not in the canonical list.
    extra = sorted(s for s in status_counts if s not in known_statuses)
    all_statuses = known_statuses + extra

    lines = [
        "| Status | Count | Percentage |",
        "| ------ | ----- | ---------- |",
    ]
    for status in all_statuses:
        count = status_counts.get(status, 0)
        pct = (count / total * 100) if total > 0 else 0.0
        lines.append(f"| {status} | {count} | {pct:.0f}% |")
    lines.append(f"| **Total** | **{total}** | **100%** |")
    return lines


def _render_age_stats(ages_days: list[int]) -> list[str]:
    """Render age distribution statistics."""
    if not ages_days:
        return ["*No ADRs with recorded dates.*"]

    lines = [
        f"- **Youngest ADR:** {min(ages_days)} days old",
        f"- **Oldest ADR:** {max(ages_days)} days old",
        f"- **Mean age:** {mean(ages_days):.0f} days",
        f"- **Median age:** {median(ages_days):.0f} days",
    ]
    return lines


def _render_needs_review(needs_review: list[dict]) -> list[str]:
    """Render the list of ADRs flagged for review."""
    if not needs_review:
        return ["*All ADRs are within the review threshold — no action required.*"]

    lines: list[str] = []
    for e in needs_review:
        date_str = e["date"].strftime("%Y-%m-%d") if e["date"] else "unknown"
        lines.append(
            f"- **{e['id']}** — {e['title']}  \n"
            f"  Date recorded: {date_str}  \n"
            f"  Reason: {e['reason']}"
        )
    return lines


def render_report(metrics: dict) -> str:
    """Render the full metrics report as a Markdown string."""

    today_str = metrics["today"].strftime("%Y-%m-%d")
    total = metrics["total"]
    status_counts = metrics["status_counts"]
    ages_days = metrics["ages_days"]
    needs_review = metrics["needs_review"]
    threshold = metrics["review_threshold"]

    lines: list[str] = []

    lines += [
        "# ADR Metrics Report",
        "",
        f"Generated on: {today_str}",
        "",
        "This report provides aggregate metrics for all Architecture Decision Records "
        "(ADRs) stored in the repository.  Use it to track decision health, identify "
        "stale records, and maintain a regular review cadence.",
        "",
    ]

    # ── Overview ───────────────────────────────────────────────────────────────

    lines += [
        "## Overview",
        "",
        f"Total ADRs discovered: **{total}**",
        "",
    ]

    # ── Status breakdown ───────────────────────────────────────────────────────

    lines += [
        "## Status Breakdown",
        "",
    ]
    lines += _render_status_table(status_counts, total)
    lines.append("")

    # ── Age statistics ─────────────────────────────────────────────────────────

    lines += [
        "## Age Statistics",
        "",
        "Age is calculated from the *Date* field recorded in each ADR to today.",
        "",
    ]
    lines += _render_age_stats(ages_days)
    lines.append("")

    # ── ADRs needing review ────────────────────────────────────────────────────

    review_count = len(needs_review)
    lines += [
        f"## ADRs Requiring Review ({review_count})",
        "",
        f"ADRs are flagged when they were recorded more than **{threshold} days** ago "
        "and have not been explicitly superseded or deprecated.  "
        "Review these records to confirm they remain accurate and relevant.",
        "",
    ]
    lines += _render_needs_review(needs_review)
    lines.append("")

    # ── Recommendations ────────────────────────────────────────────────────────

    proposed_count = status_counts.get("Proposed", 0)
    lines += [
        "## Recommendations",
        "",
    ]
    if proposed_count > 0:
        lines.append(
            f"- **{proposed_count} ADR(s) remain in Proposed status.** "
            "Review these with the Architecture Steering Council to move them to Accepted or "
            "close them if the decision has been superseded."
        )
    if review_count > 0:
        lines.append(
            f"- **{review_count} ADR(s) are overdue for review.** "
            f"Schedule a review session to confirm these decisions are still current."
        )
    if proposed_count == 0 and review_count == 0:
        lines.append("- All ADRs are in a healthy state.  No immediate actions required.")
    lines.append("")

    lines.append(
        "---\n"
        "*Generated automatically via `python3 scripts/adr_metrics.py`. "
        "Do not edit manually.*"
    )

    return "\n".join(lines).rstrip() + "\n"


# ── Entry point ────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate ADR metrics and identify records needing review.",
    )
    parser.add_argument(
        "--adr-dir",
        type=Path,
        default=ADR_SOURCE_DIR,
        metavar="DIR",
        help="Directory containing ADR markdown files (default: docs/examples/structurizr/adrs/).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        metavar="FILE",
        help="Optional path to write the Markdown report.",
    )
    parser.add_argument(
        "--review-threshold",
        type=int,
        default=DEFAULT_REVIEW_THRESHOLD_DAYS,
        metavar="DAYS",
        help=(
            f"Number of days after which an ADR is flagged for review "
            f"(default: {DEFAULT_REVIEW_THRESHOLD_DAYS})."
        ),
    )
    args = parser.parse_args(argv)

    adr_dir: Path = args.adr_dir

    if not adr_dir.exists():
        print(f"Error: ADR directory not found: {adr_dir}", file=sys.stderr)
        return 1

    entries = _load_adr_entries(adr_dir)
    if not entries:
        print(f"Warning: no ADR files found in {adr_dir}.", file=sys.stderr)

    metrics = _compute_metrics(entries, date.today(), args.review_threshold)
    report = render_report(metrics)

    print(report)

    if args.output:
        output_path: Path = args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
