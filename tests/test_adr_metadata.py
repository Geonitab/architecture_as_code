"""Validation tests for Architecture Decision Records."""
from __future__ import annotations

from pathlib import Path

from scripts.generate_adr_catalogue import render_catalogue
from scripts.validate_adrs import (
    ensure_references_have_records,
    find_referenced_adrs,
    load_adr_records,
)


def test_adr_records_are_valid() -> None:
    """All ADR files must parse and satisfy metadata expectations."""

    records = load_adr_records()
    assert records, "At least one ADR record must be present for validation."
    ensure_references_have_records(records=records, referenced_ids=find_referenced_adrs())


def test_catalogue_is_in_sync() -> None:
    """The committed ADR catalogue must match the generated output."""

    records = load_adr_records()
    expected = render_catalogue(records)
    catalogue_path = Path("docs/adr/adr_catalogue.md")
    assert catalogue_path.exists(), "ADR catalogue should exist in docs/adr/."
    observed = catalogue_path.read_text(encoding="utf-8")
    assert (
        observed == expected
    ), "Run `python3 scripts/generate_adr_catalogue.py` to refresh the ADR catalogue."
