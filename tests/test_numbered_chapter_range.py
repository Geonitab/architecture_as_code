"""Ensure numbered manuscript files stay within the supported range."""

import re
from pathlib import Path

import pytest


DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


@pytest.mark.parametrize("path", sorted(DOCS_DIR.glob("[0-9]*_*.md")))
def test_numbered_files_do_not_exceed_range(path: Path) -> None:
    """Assert that numbered markdown files do not exceed chapter 33."""
    number_match = re.match(r"^(?P<digits>\d+)", path.name)
    if not number_match:  # pragma: no cover - defensive guard for unexpected filenames
        pytest.fail(f"Numbered manuscript file has invalid prefix: {path.name}")
    number = int(number_match.group("digits"))
    assert number <= 33, f"{path.name} exceeds the supported chapter/appendix range"
