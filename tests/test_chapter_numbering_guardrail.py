"""Guardrail tests for numbered chapter files."""
from pathlib import Path
import re

MAX_ALLOWED_PREFIX = 33


def test_no_numbered_markdown_beyond_supported_range():
    """Ensure markdown filenames do not introduce numbered chapters beyond the curated range."""
    docs_dir = Path("docs")
    offending = []

    for path in docs_dir.glob("*.md"):
        match = re.match(r"(\d{2})", path.name)
        if match:
            prefix = int(match.group(1))
            if prefix > MAX_ALLOWED_PREFIX:
                offending.append(path.name)

    assert not offending, (
        f"Found numbered markdown files beyond {MAX_ALLOWED_PREFIX}: {sorted(offending)}. "
        "Append new reference material without extending the numbered chapter range."
    )
