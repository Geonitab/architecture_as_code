#!/usr/bin/env python3
"""
Check that all headings in docs/ markdown files start with uppercase letters.

This script validates that headings (lines starting with #, ##, etc.) begin
with an uppercase letter to maintain consistent style across the documentation.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def check_heading_case(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Check if headings in a markdown file start with uppercase letters.
    
    Args:
        file_path: Path to the markdown file to check
        
    Returns:
        List of tuples (line_number, heading_level, heading_text) for violations
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove code blocks to avoid false positives
    # Remove fenced code blocks (```...```)
    content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove inline code (`...`)
    content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
    
    violations = []
    for i, line in enumerate(content_no_code.split('\n'), 1):
        # Check if line is a heading (starts with # followed by space)
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            heading_level = match.group(1)
            heading_text = match.group(2).strip()
            
            # Skip if heading has attributes like {.unnumbered}
            # Extract just the text before any attributes
            heading_text_clean = re.sub(r'\s*\{[^}]*\}$', '', heading_text)
            
            # Check if first character is lowercase
            if heading_text_clean and heading_text_clean[0].islower():
                violations.append((i, heading_level, heading_text))
    
    return violations


def main():
    """Main function to check all markdown files in docs/."""
    docs_dir = Path(__file__).parent.parent / "docs"
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all markdown files in docs/ (including subdirectories)
    md_files = sorted(docs_dir.rglob("*.md"))
    
    if not md_files:
        print("No markdown files found in docs/", file=sys.stderr)
        sys.exit(1)
    
    total_violations = 0
    files_with_violations = []
    
    for md_file in md_files:
        violations = check_heading_case(md_file)
        if violations:
            files_with_violations.append(md_file)
            total_violations += len(violations)
            
            # Print violations for this file
            rel_path = md_file.relative_to(docs_dir.parent)
            print(f"\n❌ {rel_path}:")
            for line_num, level, text in violations:
                print(f"   Line {line_num}: {level} {text}")
    
    # Print summary
    print("\n" + "=" * 70)
    if total_violations == 0:
        print("✅ All headings start with uppercase letters!")
        sys.exit(0)
    else:
        print(f"❌ Found {total_violations} heading(s) with lowercase initial letters")
        print(f"   in {len(files_with_violations)} file(s)")
        print("\nHeadings should start with uppercase letters for consistency.")
        sys.exit(1)


if __name__ == "__main__":
    main()
