#!/usr/bin/env python3
"""
Validate that all figure captions in markdown files start with uppercase "Figure".

This script scans all markdown files in the docs/ directory and checks that
each figure caption (italic text after image references) begins with an uppercase
"Figure" followed by a number.

Exit codes:
  0 - All figure captions are properly capitalized
  1 - One or more figure captions start with lowercase letters
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def is_figure_caption_properly_capitalized(line: str) -> bool:
    """
    Check if a figure caption starts with uppercase "Figure".
    
    Args:
        line: A line from a markdown file (should be italic text)
        
    Returns:
        True if the caption is properly capitalized, False otherwise
    """
    # Match italic figure captions: *Figure X.Y ...* or *figure X.Y ...*
    match = re.match(r'^\*([Ff]igure)\s+\d+\.\d+', line)
    
    if not match:
        return True  # Not a figure caption
    
    figure_word = match.group(1)
    
    # Check if "Figure" starts with uppercase F
    return figure_word[0].isupper()


def check_file(file_path: Path) -> List[Tuple[int, str]]:
    """
    Check a single markdown file for figure caption capitalization issues.
    
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
                
                # Check if it's a figure caption and validate capitalization
                if line_stripped.startswith('*') and 'igure' in line_stripped:
                    if not is_figure_caption_properly_capitalized(line_stripped):
                        issues.append((line_num, line_stripped))
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return issues


def main() -> int:
    """
    Main function to scan all markdown files in docs/ directory.
    
    Returns:
        Exit code: 0 if all figure captions are valid, 1 if issues found
    """
    # Find the docs directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    docs_dir = repo_root / 'docs'
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}", file=sys.stderr)
        return 1
    
    # Find all markdown files (excluding archive directory)
    md_files = sorted([f for f in docs_dir.rglob('*.md') if 'archive' not in str(f)])
    
    if not md_files:
        print(f"Warning: No markdown files found in {docs_dir}", file=sys.stderr)
        return 0
    
    print(f"Checking {len(md_files)} markdown files for figure caption capitalization...")
    
    total_issues = 0
    files_with_issues = []
    
    for md_file in md_files:
        issues = check_file(md_file)
        if issues:
            total_issues += len(issues)
            files_with_issues.append((md_file, issues))
    
    if files_with_issues:
        print("\n❌ Found figure captions starting with lowercase 'figure':\n")
        for file_path, issues in files_with_issues:
            rel_path = file_path.relative_to(repo_root)
            print(f"📄 {rel_path}")
            for line_num, line in issues:
                print(f"  Line {line_num}: {line}")
            print()
        
        print(f"Total issues found: {total_issues} in {len(files_with_issues)} file(s)")
        print("\n💡 All figure captions should start with uppercase 'Figure'.")
        return 1
    else:
        print("✅ All figure captions are properly capitalized!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
