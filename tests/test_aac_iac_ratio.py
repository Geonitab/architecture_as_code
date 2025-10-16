#!/usr/bin/env python3
"""
Validate that the AaC/IaC ratio matches the current editorial target.

This test ensures that "Infrastructure as Code (IaC)" is mentioned no more than
one fifth of the times that "Architecture as Code (AaC)" appears across the
canonical manuscript.
"""

import re
from pathlib import Path
import sys

import yaml


def _load_canonical_chapter_paths(docs_dir: Path) -> list[Path]:
    """Load the canonical chapter paths from the requirements specification."""
    requirements_path = docs_dir.parent / "BOOK_REQUIREMENTS.md"

    if not requirements_path.exists():
        return sorted([path for path in docs_dir.glob('[0-9]*.md') if path.is_file()])

    lines = requirements_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return sorted([path for path in docs_dir.glob('[0-9]*.md') if path.is_file()])

    front_matter = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_matter.append(line)

    data = yaml.safe_load("\n".join(front_matter)) or {}
    chapters = data.get("book", {}).get("chapters", [])

    canonical_names = [chapter.get("filename") for chapter in chapters if chapter.get("filename")]
    if not canonical_names:
        return sorted([path for path in docs_dir.glob('[0-9]*.md') if path.is_file()])

    chapter_paths = [docs_dir / name for name in canonical_names if (docs_dir / name).is_file()]
    return sorted(chapter_paths, key=lambda path: path.name)


def count_mentions(text: str, pattern: str, case_sensitive: bool = True) -> int:
    """Count occurrences of a pattern in text."""
    if case_sensitive:
        return len(re.findall(pattern, text))
    else:
        return len(re.findall(pattern, text, re.IGNORECASE))


def test_aac_iac_ratio():
    """Test that AaC/IaC ratio is at least 5:1 across canonical chapters."""
    docs_dir = Path(__file__).parent.parent / 'docs'
    chapter_files = _load_canonical_chapter_paths(docs_dir)
    
    assert len(chapter_files) > 0, "No chapter files found!"
    
    total_aac = 0
    total_iac_full = 0
    total_iac_abbrev = 0
    
    # Count mentions across all chapters
    for file_path in chapter_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        aac = count_mentions(content, r'\bArchitecture as Code\b', case_sensitive=False)
        iac_full = count_mentions(content, r'\bInfrastructure as Code\b', case_sensitive=False)
        iac_abbrev = count_mentions(content, r'\bIaC\b', case_sensitive=True)
        
        total_aac += aac
        total_iac_full += iac_full
        total_iac_abbrev += iac_abbrev
    
    total_iac = total_iac_full + total_iac_abbrev
    
    # Calculate ratio
    ratio = total_aac / total_iac if total_iac > 0 else float('inf')
    
    required_ratio = 5.0

    print(f"\n{'=' * 80}")
    print("AaC/IaC Ratio Validation Test")
    print(f"{'=' * 80}")
    print(f"\nResults:")
    print(f"  Architecture as Code mentions: {total_aac}")
    print(f"  Infrastructure as Code (full): {total_iac_full}")
    print(f"  IaC (abbreviation): {total_iac_abbrev}")
    print(f"  Total Infrastructure as Code mentions: {total_iac}")
    print(f"  Ratio (AaC:IaC): {ratio:.2f}:1")
    print(f"  Required ratio: {required_ratio:.0f}:1")
    print(f"  Status: {'✅ PASS' if ratio >= required_ratio else '❌ FAIL'}")
    print(f"{'=' * 80}\n")
    
    # Assert the ratio is at least 5:1
    assert ratio >= required_ratio, (
        f"AaC/IaC ratio is {ratio:.2f}:1, which is below the required {required_ratio:.0f}:1. "
        f"Found {total_aac} AaC mentions and {total_iac} IaC mentions. "
        f"Please reduce IaC mentions to at most {int(total_aac / required_ratio)}."
    )

    print(f"✅ Test passed! Ratio of {ratio:.2f}:1 meets the {required_ratio:.0f}:1 requirement.")


if __name__ == '__main__':
    try:
        test_aac_iac_ratio()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
