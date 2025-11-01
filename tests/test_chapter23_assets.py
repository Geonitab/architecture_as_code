"""Validation tests for Chapter 23 image assets."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = PROJECT_ROOT / "docs" / "23_soft_as_code_interplay.md"

# Regex capturing diagram and mind map references that follow the naming convention.
IMAGE_REFERENCE_PATTERN = re.compile(
    r"!\[[^\]]*\]\((images/(?:diagram_23_[\w-]+|mindmap_23[a-z]_[\w-]+)\.png)\)"
)

# Regex enforcing the strict naming pattern for the assets.
DIAGRAM_NAME_PATTERN = re.compile(r"diagram_23_[a-z0-9_]+\.png$")
MINDMAP_NAME_PATTERN = re.compile(r"mindmap_23[a-z]_[a-z0-9_]+\.png$")


def _read_chapter() -> str:
    """Load the chapter text, raising an informative error when missing."""
    if not CHAPTER_PATH.exists():
        raise FileNotFoundError(f"Chapter file missing: {CHAPTER_PATH}")
    return CHAPTER_PATH.read_text(encoding="utf-8")


def test_chapter23_image_assets_exist() -> None:
    """Ensure every referenced Chapter 23 diagram or mind map image exists."""
    chapter_text = _read_chapter()
    matches = IMAGE_REFERENCE_PATTERN.findall(chapter_text)

    assert matches, "No Chapter 23 image references were detected."

    # Deduplicate to avoid repeated checks for the same asset.
    referenced_assets = {match for match in matches}

    for relative_path in referenced_assets:
        asset_path = PROJECT_ROOT / "docs" / relative_path

        assert asset_path.exists(), f"Missing image asset: {relative_path}"
        assert asset_path.is_file(), f"Referenced path is not a file: {relative_path}"

        filename = asset_path.name
        if filename.startswith("diagram_23_"):
            assert DIAGRAM_NAME_PATTERN.match(filename), (
                "Diagram asset name does not follow the expected pattern: "
                f"{filename}"
            )
        elif filename.startswith("mindmap_23"):
            assert MINDMAP_NAME_PATTERN.match(filename), (
                "Mind map asset name does not follow the expected pattern: "
                f"{filename}"
            )
        else:
            raise AssertionError(
                "Unexpected Chapter 23 asset naming: "
                f"{filename}"
            )


def test_chapter23_figures_are_sequential() -> None:
    """Verify that figure numbering for Chapter 23 remains sequential."""
    chapter_text = _read_chapter()
    figure_numbers = [int(number) for number in re.findall(r"Figure 23\.(\d+)", chapter_text)]

    assert figure_numbers, "No figure numbering detected for Chapter 23."

    expected_sequence = list(range(1, len(figure_numbers) + 1))
    assert figure_numbers == expected_sequence, (
        "Chapter 23 figure numbering is not sequential: "
        f"found {figure_numbers}, expected {expected_sequence}"
    )
