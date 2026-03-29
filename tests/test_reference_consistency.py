"""
Reference and citation consistency validator for book content.

Validates that all chapters follow the standardised citation format defined
in docs/STYLE_GUIDE.md:
- Every canonical chapter has a '## Sources' section
- No non-standard reference headers are used
- Inline citations use [Source [N]](33_references.md#source-N) format
- Cited source numbers exist as anchors in docs/33_references.md
- No prohibited placeholder citation strings appear
"""
from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
REFERENCES_FILE = DOCS_DIR / "33_references.md"

# Ensure scripts/ is importable when running from any working directory.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.navigation import get_book_build_files  # noqa: E402


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

# Files that are legitimately exempt from the '## Sources' requirement because
# they are reference material, templates, or technical catalogues rather than
# narrative research chapters.
_SOURCES_EXEMPT: frozenset[str] = frozenset({
    "33_references.md",               # IS the bibliography
    "28_glossary.md",                  # reference lookup table
    "29_about_the_author.md",          # author biography
    "30_appendix_code_examples.md",    # code-only appendix
    "appendix_templates_and_tools.md", # templates appendix
    "appendix_d_control_mapping_matrix_template.md",  # template
    "adr_catalogue.md",                # ADR technical catalogue
    "migration_plan.md",               # ADR migration plan
})


def _get_canonical_chapter_paths() -> list[Path]:
    """Return the absolute paths of all canonical chapter files (no part intros)."""
    filenames = get_book_build_files()
    return [
        DOCS_DIR / name
        for name in filenames
        if not Path(name).stem.startswith("part_")
    ]


def _get_narrative_chapter_paths() -> list[Path]:
    """Return canonical chapter paths excluding files exempt from Sources checks."""
    return [
        p for p in _get_canonical_chapter_paths()
        if p.name not in _SOURCES_EXEMPT
    ]


def _strip_fenced_code_blocks(text: str) -> str:
    """Remove fenced (```) code blocks from *text*, leaving other content intact."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _strip_indented_code_blocks(text: str) -> str:
    """Remove indented (4-space / tab) code blocks from *text*."""
    return re.sub(r"^(?: {4}|\t).*$", "", text, flags=re.MULTILINE)


def _strip_code_blocks(text: str) -> str:
    """Remove both fenced and indented code blocks from *text*."""
    text = _strip_fenced_code_blocks(text)
    text = _strip_indented_code_blocks(text)
    return text


def _load_source_anchors() -> set[int]:
    """Return the set of source numbers that have an anchor in 33_references.md."""
    if not REFERENCES_FILE.exists():
        return set()
    content = REFERENCES_FILE.read_text(encoding="utf-8")
    # Anchors use pandoc span syntax:  {#source-N}
    matches = re.findall(r"\{#source-(\d+)\}", content)
    return {int(n) for n in matches}


# ---------------------------------------------------------------------------
# Test 1 – every chapter has a '## Sources' section
# ---------------------------------------------------------------------------

class TestSourcesSection:
    """Validate that every canonical chapter contains a '## Sources' header."""

    def test_all_chapters_have_sources_section(self) -> None:
        """Every narrative chapter file must contain a line starting with '## Sources'."""
        chapter_paths = _get_narrative_chapter_paths()
        failures: list[str] = []

        for path in chapter_paths:
            if not path.exists():
                failures.append(f"{path.name}: file not found on disk")
                continue

            content = path.read_text(encoding="utf-8")
            lines = content.splitlines()
            has_sources = any(
                line.rstrip() == "## Sources" or line.startswith("## Sources\n")
                # also handle trailing spaces / CRLF
                or re.match(r"^## Sources\s*$", line)
                for line in lines
            )
            if not has_sources:
                failures.append(
                    f"{path.name}: missing '## Sources' section"
                    f" (found headers: "
                    f"{[l for l in lines if l.startswith('## ')]})"
                )

        if failures:
            warnings.warn(
                f"Chapters missing '## Sources' section ({len(failures)}):\n"
                + "\n".join(f"  - {msg}" for msg in failures),
                UserWarning,
                stacklevel=2,
            )
            pytest.fail(
                f"{len(failures)} chapter(s) are missing a '## Sources' section:\n"
                + "\n".join(f"  - {msg}" for msg in failures)
            )


# ---------------------------------------------------------------------------
# Test 2 – no non-standard reference section headers
# ---------------------------------------------------------------------------

# Headers that are explicitly prohibited by the style guide.
_PROHIBITED_HEADERS: list[re.Pattern[str]] = [
    re.compile(r"^##\s+References\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^##\s+Sources\s+and\s+References\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^##\s+Sources\s+and\s+references\s*$", re.MULTILINE),
    re.compile(r"^###\s+References\s*$", re.MULTILINE | re.IGNORECASE),
]


class TestSourcesHeaderStandardisation:
    """Validate that non-standard reference section headers are not used."""

    def test_sources_headers_are_standardised(self) -> None:
        """No chapter may use a reference section header other than '## Sources'."""
        chapter_paths = _get_canonical_chapter_paths()
        failures: list[str] = []

        for path in chapter_paths:
            if not path.exists():
                continue

            content = path.read_text(encoding="utf-8")
            for pattern in _PROHIBITED_HEADERS:
                found = pattern.findall(content)
                for match in found:
                    failures.append(
                        f"{path.name}: non-standard header found: {match.strip()!r}"
                        f" (use '## Sources' instead)"
                    )

        if failures:
            warnings.warn(
                f"Non-standard reference headers detected ({len(failures)}):\n"
                + "\n".join(f"  - {msg}" for msg in failures),
                UserWarning,
                stacklevel=2,
            )
            pytest.fail(
                f"{len(failures)} non-standard reference header(s) found:\n"
                + "\n".join(f"  - {msg}" for msg in failures)
            )


# ---------------------------------------------------------------------------
# Test 3 – inline citations use the standard linked format
# ---------------------------------------------------------------------------

# Matches bare (unlinked) occurrences of Source [N] in prose.
# e.g.  (Source [4])  or  Source [15]  — without a preceding markdown link.
# The negative lookbehind ensures we skip already-linked citations that look
# like  [Source [4]](33_references.md#source-4).
_BARE_CITATION_RE = re.compile(
    r"(?<!\[)"           # not preceded by '[' (i.e. not already part of a link)
    r"\bSource\s*\[(\d+)\]"
    r"(?!\(33_references\.md#source-\d+\))"  # not followed by a proper link
)


class TestInlineCitationFormat:
    """Validate that inline citations use the standard hyperlinked format."""

    def test_inline_citations_use_standard_format(self) -> None:
        """Bare 'Source [N]' occurrences in prose must be linked to 33_references.md.

        33_references.md itself is excluded: its numbered index entries contain
        the definition lines  '[**Source [N]:**]{#source-N} ...'  which are not
        inline citations and would produce false positives.
        """
        chapter_paths = [
            p for p in _get_canonical_chapter_paths()
            if p.name != "33_references.md"
        ]
        failures: list[str] = []

        for path in chapter_paths:
            if not path.exists():
                continue

            raw_content = path.read_text(encoding="utf-8")
            prose = _strip_code_blocks(raw_content)

            for match in _BARE_CITATION_RE.finditer(prose):
                # Find approximate line number in the *raw* file for reporting.
                char_offset = match.start()
                # Re-count lines in the stripped text up to the match position.
                line_no = prose[:char_offset].count("\n") + 1
                failures.append(
                    f"{path.name}:{line_no}: bare citation {match.group()!r}"
                    f" — should be"
                    f" [Source [{match.group(1)}]](33_references.md#source-{match.group(1)})"
                )

        if failures:
            warnings.warn(
                f"Bare (unlinked) inline citations found ({len(failures)}):\n"
                + "\n".join(f"  - {msg}" for msg in failures),
                UserWarning,
                stacklevel=2,
            )
            pytest.fail(
                f"{len(failures)} bare inline citation(s) found"
                f" (expected '[Source [N]](33_references.md#source-N)' format):\n"
                + "\n".join(f"  - {msg}" for msg in failures)
            )


# ---------------------------------------------------------------------------
# Test 4 – every cited source number exists in the bibliography
# ---------------------------------------------------------------------------

# Matches both linked and bare occurrences so we can collect all cited numbers.
_ANY_SOURCE_REF_RE = re.compile(r"\bSource\s*\[(\d+)\]")


class TestCitedSourcesExistInBibliography:
    """Validate that every cited source number has a matching anchor in 33_references.md."""

    def test_cited_source_numbers_exist_in_bibliography(self) -> None:
        """Every Source [N] cited in any chapter must have {#source-N} in 33_references.md."""
        chapter_paths = _get_canonical_chapter_paths()
        available_anchors = _load_source_anchors()

        failures: list[str] = []

        for path in chapter_paths:
            if not path.exists():
                continue

            raw_content = path.read_text(encoding="utf-8")
            prose = _strip_code_blocks(raw_content)

            cited_numbers: set[int] = set()
            for match in _ANY_SOURCE_REF_RE.finditer(prose):
                cited_numbers.add(int(match.group(1)))

            for number in sorted(cited_numbers):
                if number not in available_anchors:
                    failures.append(
                        f"{path.name}: cites Source [{number}]"
                        f" but {{#source-{number}}} is not in {REFERENCES_FILE.name}"
                    )

        if failures:
            warnings.warn(
                f"Cited source numbers without bibliography anchors ({len(failures)}):\n"
                + "\n".join(f"  - {msg}" for msg in failures),
                UserWarning,
                stacklevel=2,
            )
            pytest.fail(
                f"{len(failures)} cited source number(s) have no matching anchor"
                f" in {REFERENCES_FILE.name}:\n"
                + "\n".join(f"  - {msg}" for msg in failures)
            )


# ---------------------------------------------------------------------------
# Test 5 – no prohibited citation placeholder strings
# ---------------------------------------------------------------------------

_PROHIBITED_STRINGS: list[str] = [
    "Best practice documentation from leading organisations",
    "Industry reports on Architecture as Code adoption trends",
]

# Matches the literal string YYYYMM appearing outside code blocks.
_YYYYMM_RE = re.compile(r"\bYYYYMM\b")


class TestNoProhibitedCitationForms:
    """Validate that no prohibited placeholder citation strings appear in chapters."""

    def test_no_prohibited_citation_forms(self) -> None:
        """Chapters must not contain prohibited placeholder citation strings."""
        chapter_paths = _get_canonical_chapter_paths()
        failures: list[str] = []

        for path in chapter_paths:
            if not path.exists():
                continue

            raw_content = path.read_text(encoding="utf-8")
            prose = _strip_code_blocks(raw_content)

            for prohibited in _PROHIBITED_STRINGS:
                if prohibited in prose:
                    failures.append(
                        f"{path.name}: contains prohibited placeholder"
                        f" string: {prohibited!r}"
                    )

            for match in _YYYYMM_RE.finditer(prose):
                line_no = prose[: match.start()].count("\n") + 1
                failures.append(
                    f"{path.name}:{line_no}: contains unresolved template"
                    f" variable 'YYYYMM' in prose — replace with a concrete"
                    f" value (e.g. '202501') or remove"
                )

        if failures:
            warnings.warn(
                f"Prohibited citation placeholder strings found ({len(failures)}):\n"
                + "\n".join(f"  - {msg}" for msg in failures),
                UserWarning,
                stacklevel=2,
            )
            pytest.fail(
                f"{len(failures)} prohibited citation placeholder(s) found:\n"
                + "\n".join(f"  - {msg}" for msg in failures)
            )
