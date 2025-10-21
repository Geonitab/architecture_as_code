"""
Validation tests for the glossary dataset.

Ensures the human-readable glossary and the structured relationship database
stay in sync so automation can rely on consistent terminology.
"""
from pathlib import Path
import json
import re


def _extract_glossary_terms():
    """Collect all glossary terms defined in the markdown chapter."""
    doc_path = Path("docs/28_glossary.md")
    content = doc_path.read_text(encoding="utf-8")

    terms = set()

    # Capture table rows where the first column holds the term
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        term, definition = parts[:2]
        if term in {"Term", "------"} or definition == "Definition":
            continue
        terms.add(term)

    # Capture standalone highlighted terms (e.g. **Digital Twin**: ...)
    for match in re.finditer(r"\*\*([^*]+?)\*\*:", content):
        terms.add(match.group(1).strip())

    return terms


def _load_relationship_terms():
    """Load the structured glossary dataset."""
    data_path = Path("references/glossary_terms_relationships.json")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    return data["terms"]


def test_glossary_terms_match_dataset():
    """Verify that glossary markdown terms align with the dataset."""
    doc_terms = _extract_glossary_terms()
    dataset_terms = {entry["name"] for entry in _load_relationship_terms()}

    missing_in_dataset = sorted(doc_terms - dataset_terms)
    missing_in_doc = sorted(dataset_terms - doc_terms)

    message_lines = []
    if missing_in_dataset:
        message_lines.append(
            "Terms present in docs/28_glossary.md but missing from "
            "references/glossary_terms_relationships.json: "
            f"{missing_in_dataset}"
        )
    if missing_in_doc:
        message_lines.append(
            "Terms present in references/glossary_terms_relationships.json but "
            "missing from docs/28_glossary.md: "
            f"{missing_in_doc}"
        )

    assert not message_lines, "\n".join(message_lines)


def test_relationship_targets_exist():
    """Ensure every relationship points to a defined glossary term."""
    entries = _load_relationship_terms()
    valid_ids = {entry["id"] for entry in entries}

    missing_targets = []
    for entry in entries:
        for related in entry.get("related", []):
            if related["term"] not in valid_ids:
                missing_targets.append(
                    f"{entry['id']} -> {related['term']}"
                )

    assert not missing_targets, (
        "Relationship targets missing from dataset: "
        f"{missing_targets}"
    )
