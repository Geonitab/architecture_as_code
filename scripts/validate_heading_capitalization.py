#!/usr/bin/env python3
"""
Validate that all headings in markdown files start with uppercase letters.

This script scans all markdown files in the docs/ directory and checks that
each heading (lines starting with #, ##, ###, etc.) begins with an uppercase
letter after the hash marks and any whitespace.

Exit codes:
  0 - All headings are properly capitalized
  1 - One or more headings start with lowercase letters
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def is_heading_properly_capitalized(line: str) -> bool:
    """
    Check if a markdown heading starts with an uppercase letter.
    
    Args:
        line: A line from a markdown file
        
    Returns:
        True if the heading is properly capitalized, False otherwise
    """
    # Match markdown headings: one or more # followed by space and text
    match = re.match(r'^(#+)\s+(.+)$', line)
    
    if not match:
        return True  # Not a heading
    
    heading_text = match.group(2)
    
    # Skip if heading starts with a special character, number, or backtick (code)
    if heading_text and heading_text[0] in '`0123456789#@$%^&*()[]{}|\\/<>=+-_~':
        return True
    
    # Check if first character is uppercase
    if heading_text and heading_text[0].isalpha():
        return heading_text[0].isupper()
    
    return True  # Non-alphabetic first character is acceptable


def check_file(file_path: Path) -> List[Tuple[int, str]]:
    """
    Check a single markdown file for heading capitalization issues.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        List of tuples (line_number, line_content) for lines with issues
    """
    issues = []
    in_code_block = False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                line_stripped = line.rstrip()
                
                # Track code blocks (``` or ~~~)
                if line_stripped.startswith('```') or line_stripped.startswith('~~~'):
                    in_code_block = not in_code_block
                    continue
                
                # Skip lines inside code blocks
                if in_code_block:
                    continue
                
                # Check if it's a heading and validate capitalization
                if line_stripped.startswith('#') and not is_heading_properly_capitalized(line_stripped):
                    issues.append((line_num, line_stripped))
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return issues


def main() -> int:
    """
    Main function to scan all markdown files in docs/ directory.
    
    Returns:
        Exit code: 0 if all headings are valid, 1 if issues found
    """
    # Find the docs directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    docs_dir = repo_root / 'docs'
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}", file=sys.stderr)
        return 1
    
    # Find all markdown files
    md_files = sorted(docs_dir.rglob('*.md'))
    
    if not md_files:
        print(f"Warning: No markdown files found in {docs_dir}", file=sys.stderr)
        return 0
    
    print(f"Checking {len(md_files)} markdown files for heading capitalization...")
    
    total_issues = 0
    files_with_issues = []
    
    for md_file in md_files:
        issues = check_file(md_file)
        if issues:
            total_issues += len(issues)
            files_with_issues.append((md_file, issues))
    
    if files_with_issues:
        print("\n❌ Found headings starting with lowercase letters:\n")
        for file_path, issues in files_with_issues:
            rel_path = file_path.relative_to(repo_root)
            print(f"📄 {rel_path}")
            for line_num, line in issues:
                print(f"  Line {line_num}: {line}")
            print()
        
        print(f"Total issues found: {total_issues} in {len(files_with_issues)} file(s)")
        print("\n💡 All headings should start with an uppercase letter.")
        return 1
    else:
        print("✅ All headings are properly capitalized!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
