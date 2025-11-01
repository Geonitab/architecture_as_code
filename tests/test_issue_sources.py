"""
Validation tests for Architecture as Code source verification issues.

These tests ensure that the curated GitHub issue drafts under `Issues/`
reference only approved sources, follow the expected structure, and stay
in sync with the published references catalogue.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ISSUES_DIR = Path("Issues")
CATALOGUE_FILE = ISSUES_DIR / "source_catalogue.json"
REFERENCES_FILE = Path("docs/appendix_f_references.md")


@pytest.fixture(scope="module")
def source_catalogue() -> dict[int, dict]:
    """Load the source catalogue into a keyed dictionary."""
    assert CATALOGUE_FILE.exists(), "Missing Issues/source_catalogue.json"

    data = json.loads(CATALOGUE_FILE.read_text(encoding="utf-8"))
    sources = data.get("sources")
    assert isinstance(sources, list), "source_catalogue.json must contain a list of sources"

    catalogue = {}
    for entry in sources:
        entry_id = entry.get("id")
        assert isinstance(entry_id, int), f"Source entry missing numeric id: {entry}"
        assert entry_id not in catalogue, f"Duplicate source id detected: {entry_id}"
        catalogue[entry_id] = entry

    return catalogue


class TestIssueSourceCatalogue:
    """Verify the integrity of the source catalogue."""

    def test_catalogue_contains_all_source_ids(self, source_catalogue):
        """Ensure Source IDs 1–16 are present exactly once."""
        expected_ids = set(range(1, 17))
        assert set(source_catalogue.keys()) == expected_ids, (
            "Source catalogue must define Source IDs 1–16 exactly once"
        )

    def test_catalogue_entries_have_required_fields(self, source_catalogue):
        """Ensure each catalogue entry exposes the required metadata."""
        required_fields = {"title", "type", "year", "url", "summary", "supports_chapters"}

        for source_id, entry in source_catalogue.items():
            missing = required_fields - set(entry.keys())
            assert not missing, (
                f"Source {source_id} missing fields: {sorted(missing)}"
            )
            assert entry["supports_chapters"], (
                f"Source {source_id} must reference at least one supporting chapter"
            )

    def test_catalogue_titles_exist_in_references_chapter(self, source_catalogue):
        """Ensure every catalogue title is captured in the references chapter."""
        assert REFERENCES_FILE.exists(), "Missing references file docs/appendix_f_references.md"
        references_text = REFERENCES_FILE.read_text(encoding="utf-8")

        for source_id, entry in source_catalogue.items():
            title = entry["title"]
            # Use a relaxed match to ignore punctuation differences
            escaped = re.escape(title.split(" – ")[0])
            assert re.search(escaped, references_text, re.IGNORECASE), (
                f"Source {source_id} title '{title}' not found in references chapter"
            )


class TestIssueTemplates:
    """Validate the structure and content of issue drafts."""

    REQUIRED_SECTIONS = [
        "## Source IDs",
        "## Relevant Manuscript Sections",
        "## Problem Statement",
        "## Acceptance Criteria",
        "## Recommended Labels",
    ]

    def test_issue_files_exist(self):
        """Ensure the curated issue markdown files are present."""
        issue_files = sorted(ISSUES_DIR.glob("issue_*.md"))
        assert issue_files, "No issue templates found in Issues/"

    def test_issue_sections_and_sources(self, source_catalogue):
        """Verify each issue file structure and Source IDs."""
        issue_files = sorted(ISSUES_DIR.glob("issue_*.md"))
        seen_ids: set[int] = set()

        for path in issue_files:
            text = path.read_text(encoding="utf-8")

            for section in self.REQUIRED_SECTIONS:
                assert section in text, f"{path.name} missing section '{section}'"

            source_section = self._extract_section(text, "## Source IDs")
            ids = {int(match) for match in re.findall(r"\[(\d+)\]", source_section)}
            assert ids, f"{path.name} must declare at least one Source ID"

            unknown = ids - set(source_catalogue.keys())
            assert not unknown, (
                f"{path.name} references undefined Source IDs: {sorted(unknown)}"
            )

            seen_ids.update(ids)

        expected_ids = set(source_catalogue.keys())
        assert seen_ids == expected_ids, (
            "Combined issue templates must reference Source IDs 1–16\n"
            f"Missing: {sorted(expected_ids - seen_ids)}\n"
            f"Unexpected: {sorted(seen_ids - expected_ids)}"
        )

    def test_readme_issue_listing_is_consistent(self):
        """Ensure Issues/README.md enumerates the curated issue files."""
        readme = (ISSUES_DIR / "README.md").read_text(encoding="utf-8")
        listed_files = re.findall(r"\[([^\]]+\.md)\]", readme)
        issue_files = sorted(f.name for f in ISSUES_DIR.glob("issue_*.md"))

        # Filter hyperlinks that refer to issue files
        listed_issue_files = sorted(
            name for name in listed_files if name.startswith("issue_")
        )
        assert listed_issue_files == issue_files, (
            "Issues/README.md issue list is out of sync with available templates"
        )

    def _extract_section(self, text: str, heading: str) -> str:
        """Return the text belonging to a heading until the next heading."""
        pattern = rf"{re.escape(heading)}\s*\n(.*?)(?:\n## |\Z)"
        match = re.search(pattern, text, re.DOTALL)
        assert match, f"Could not parse section '{heading}'"
        return match.group(1)

