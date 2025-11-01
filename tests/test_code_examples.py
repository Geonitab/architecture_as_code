"""
Code example appendix validation tests.

Ensures that code example listings keep stable anchors and that cross references
throughout the manuscript remain valid.
"""
import re

import pytest


def test_code_example_anchor_consistency(docs_directory):
    """Verify that appendix code example headings expose stable anchors."""
    appendix_path = docs_directory / "appendix_c_code_examples.md"

    if not appendix_path.exists():
        pytest.skip("Code Examples appendix not available")

    content = appendix_path.read_text(encoding="utf-8")
    heading_pattern = re.compile(r"^###\s+(?P<identifier>\d{2}_CODE_[A-Z0-9]+):.*$", re.MULTILINE)

    anchors = set()
    missing_anchors = []
    duplicate_identifiers = []
    seen_identifiers = set()

    for match in heading_pattern.finditer(content):
        identifier = match.group("identifier")
        if identifier in seen_identifiers:
            duplicate_identifiers.append(identifier)
            continue
        seen_identifiers.add(identifier)

        line = match.group(0)
        anchor_match = re.search(r"\{#([^\}]+)\}", line)

        if not anchor_match:
            missing_anchors.append(identifier)
            continue

        anchor_id = anchor_match.group(1).lower()
        canonical_id = identifier.lower()

        if not anchor_id.startswith(canonical_id):
            missing_anchors.append(identifier)

        anchors.add(anchor_id)
        anchors.add(canonical_id)

    assert not duplicate_identifiers, (
        "Duplicate code example identifiers detected: "
        f"{duplicate_identifiers}"
    )

    assert not missing_anchors, (
        "Code example headings missing canonical anchors: "
        f"{missing_anchors}"
    )

    link_pattern = re.compile(r"appendix_c_code_examples\.md#([^\s\)]+)")
    invalid_links = []

    for path in docs_directory.rglob("*.md"):
        if path.name == "appendix_c_code_examples.md":
            continue

        text = path.read_text(encoding="utf-8")
        for anchor in link_pattern.findall(text):
            anchor_lower = anchor.lower()
            if anchor_lower not in anchors:
                invalid_links.append({
                    "file": path.relative_to(docs_directory).as_posix(),
                    "anchor": anchor,
                })

    assert not invalid_links, (
        "Broken code example cross references found: "
        f"{invalid_links}"
    )
