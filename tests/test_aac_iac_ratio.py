#!/usr/bin/env python3
"""
Test to validate that the AaC/IaC ratio meets the 20:1 requirement.

This test ensures that "Infrastructure as Code (IaC)" is mentioned no more than
1/20th of the times that "Architecture as Code (AaC)" is mentioned in the book.
"""

import re
from pathlib import Path
import sys


def count_mentions(text: str, pattern: str, case_sensitive: bool = True) -> int:
    """Count occurrences of a pattern in text."""
    if case_sensitive:
        return len(re.findall(pattern, text))
    else:
        return len(re.findall(pattern, text, re.IGNORECASE))


def test_aac_iac_ratio():
    """Test that AaC/IaC ratio is at least 20:1."""
    # Get all chapter markdown files
    docs_dir = Path(__file__).parent.parent / 'docs'
    chapter_files = sorted([
        f for f in docs_dir.glob('[0-9]*.md')
        if f.is_file()
    ])
    
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
    
    # Print results
    print(f"\n{'=' * 80}")
    print("AaC/IaC Ratio Validation Test")
    print(f"{'=' * 80}")
    print(f"\nResults:")
    print(f"  Architecture as Code mentions: {total_aac}")
    print(f"  Infrastructure as Code (full): {total_iac_full}")
    print(f"  IaC (abbreviation): {total_iac_abbrev}")
    print(f"  Total Infrastructure as Code mentions: {total_iac}")
    print(f"  Ratio (AaC:IaC): {ratio:.2f}:1")
    print(f"  Required ratio: 20:1")
    print(f"  Status: {'✅ PASS' if ratio >= 20 else '❌ FAIL'}")
    print(f"{'=' * 80}\n")
    
    # Assert the ratio is at least 20:1
    assert ratio >= 20.0, (
        f"AaC/IaC ratio is {ratio:.2f}:1, which is below the required 20:1. "
        f"Found {total_aac} AaC mentions and {total_iac} IaC mentions. "
        f"Please reduce IaC mentions to at most {int(total_aac / 20)}."
    )
    
    print(f"✅ Test passed! Ratio of {ratio:.2f}:1 meets the 20:1 requirement.")
    return True


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
