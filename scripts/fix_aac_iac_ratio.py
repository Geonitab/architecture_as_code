#!/usr/bin/env python3
"""
Fix Architecture as Code (AaC) to Infrastructure as Code (IaC) ratio.

This script ensures that IaC is mentioned no more than 1/20th of the times
that Architecture as Code is mentioned, as per the requirement.

Target ratio: 20:1 (AaC:IaC)
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Technical contexts where IaC should be preserved
PRESERVE_IAC_CONTEXTS = [
    'terraform',
    'cloudformation',
    'ansible',
    'puppet',
    'chef',
    'code block',
    '```',
    'infrastructure as code tools',
    'iac tools',
    'traditional iac',
    'historical context',
]


def count_mentions(text: str, pattern: str, case_sensitive: bool = True) -> int:
    """Count occurrences of a pattern in text."""
    if case_sensitive:
        return len(re.findall(pattern, text))
    else:
        return len(re.findall(pattern, text, re.IGNORECASE))


def is_in_code_block(text: str, position: int) -> bool:
    """Check if position is inside a code block."""
    # Count code block markers before this position
    before_text = text[:position]
    triple_backticks = before_text.count('```')
    single_backticks = before_text.count('`') - (triple_backticks * 3)
    
    # If odd number of triple backticks, we're inside a code block
    if triple_backticks % 2 == 1:
        return True
    
    # Check for inline code (single backticks)
    last_backtick = before_text.rfind('`')
    if last_backtick >= 0:
        # Count backticks between last one and current position
        between = before_text[last_backtick+1:]
        if '`' not in between and len(between) < 100:  # Likely inline code
            return True
    
    return False


def should_preserve_iac(text: str, match_position: int, window: int = 100) -> bool:
    """Determine if an IaC mention should be preserved based on context."""
    start = max(0, match_position - window)
    end = min(len(text), match_position + window)
    context = text[start:end].lower()
    
    # Check if in code block
    if is_in_code_block(text, match_position):
        return True
    
    # Only preserve in very specific technical tool contexts
    specific_preserve_terms = [
        'terraform',
        'cloudformation',
        'ansible',
        'puppet',
        'chef',
    ]
    
    for preserve_term in specific_preserve_terms:
        if preserve_term in context:
            return True
    
    return False


def replace_iac_with_aac(text: str, aggressive: bool = False) -> Tuple[str, int]:
    """
    Replace IaC mentions with Architecture as Code where appropriate.
    Returns modified text and count of replacements.
    """
    replacements = 0
    result = text
    
    # Pattern 1: "Infrastructure as Code" -> "Architecture as Code"
    pattern1 = r'\bInfrastructure as Code\b'
    matches = list(re.finditer(pattern1, result, re.IGNORECASE))
    
    for match in reversed(matches):  # Reverse to maintain positions
        if not should_preserve_iac(result, match.start()):
            # Preserve case
            original = match.group()
            if original.isupper():
                replacement = "ARCHITECTURE AS CODE"
            elif original.istitle() or original[0].isupper():
                replacement = "Architecture as Code"
            else:
                replacement = "architecture as code"
            
            result = result[:match.start()] + replacement + result[match.end():]
            replacements += 1
    
    # Pattern 2: "IaC" -> "Architecture as Code" (more aggressive)
    if aggressive:
        pattern2 = r'\bIaC\b'
        matches = list(re.finditer(pattern2, result))
        
        for match in reversed(matches):
            if not should_preserve_iac(result, match.start()):
                # Always use full form
                result = result[:match.start()] + "Architecture as Code" + result[match.end():]
                replacements += 1
    
    return result, replacements


def analyze_file(file_path: Path) -> Dict:
    """Analyze a markdown file for AaC and IaC mentions."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    aac_count = count_mentions(content, r'\bArchitecture as Code\b', case_sensitive=False)
    iac_full_count = count_mentions(content, r'\bInfrastructure as Code\b', case_sensitive=False)
    iac_abbrev_count = count_mentions(content, r'\bIaC\b')
    
    total_iac = iac_full_count + iac_abbrev_count
    ratio = aac_count / total_iac if total_iac > 0 else float('inf')
    
    return {
        'file': file_path.name,
        'aac_count': aac_count,
        'iac_full_count': iac_full_count,
        'iac_abbrev_count': iac_abbrev_count,
        'total_iac': total_iac,
        'ratio': ratio,
        'content': content
    }


def fix_file(file_path: Path, aggressive: bool = False, dry_run: bool = False) -> Dict:
    """Fix AaC/IaC ratio in a file."""
    analysis = analyze_file(file_path)
    
    if analysis['total_iac'] == 0:
        return {
            'file': file_path.name,
            'status': 'no_iac',
            'replacements': 0,
            'old_ratio': analysis['ratio'],
            'new_ratio': analysis['ratio']
        }
    
    # Calculate how many replacements we need
    target_ratio = 20.0
    current_ratio = analysis['ratio']
    
    if current_ratio >= target_ratio:
        return {
            'file': file_path.name,
            'status': 'already_compliant',
            'replacements': 0,
            'old_ratio': current_ratio,
            'new_ratio': current_ratio
        }
    
    # Try to fix
    new_content, replacements = replace_iac_with_aac(analysis['content'], aggressive=aggressive)
    
    if replacements > 0 and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    # Re-analyze to get new ratio
    if replacements > 0:
        new_analysis = analyze_file(file_path) if not dry_run else {
            'aac_count': analysis['aac_count'],
            'iac_full_count': max(0, analysis['iac_full_count'] - replacements),
            'iac_abbrev_count': analysis['iac_abbrev_count'],
            'total_iac': max(1, analysis['total_iac'] - replacements)
        }
        new_ratio = new_analysis['aac_count'] / new_analysis['total_iac'] if new_analysis['total_iac'] > 0 else float('inf')
    else:
        new_ratio = current_ratio
    
    return {
        'file': file_path.name,
        'status': 'fixed' if replacements > 0 else 'no_changes',
        'replacements': replacements,
        'old_ratio': current_ratio,
        'new_ratio': new_ratio
    }


def main():
    """Main function to fix AaC/IaC ratio across all markdown files."""
    docs_dir = Path(__file__).parent.parent / 'docs'
    
    # Find all markdown chapter files
    chapter_files = sorted([
        f for f in docs_dir.glob('*.md')
        if f.name[0].isdigit() and not f.name.startswith('.')
    ])
    
    print("=" * 80)
    print("AaC/IaC Ratio Analysis and Fix")
    print("=" * 80)
    print()
    
    # Phase 1: Analyze current state
    print("Phase 1: Analyzing current state...")
    print("-" * 80)
    
    total_aac = 0
    total_iac = 0
    file_analyses = []
    
    for file_path in chapter_files:
        analysis = analyze_file(file_path)
        file_analyses.append(analysis)
        total_aac += analysis['aac_count']
        total_iac += analysis['total_iac']
    
    current_ratio = total_aac / total_iac if total_iac > 0 else float('inf')
    
    print(f"\nCurrent Status:")
    print(f"  Architecture as Code mentions: {total_aac}")
    print(f"  Infrastructure as Code mentions: {total_iac}")
    print(f"  Current ratio: {current_ratio:.2f}:1")
    print(f"  Target ratio: 20:1")
    print(f"  Compliant: {'✅ YES' if current_ratio >= 20 else '❌ NO'}")
    
    if current_ratio >= 20:
        print("\n✅ Repository already meets the 20:1 ratio requirement!")
        return
    
    # Calculate needed changes
    max_allowed_iac = int(total_aac / 20)
    needed_reductions = total_iac - max_allowed_iac
    
    print(f"\nRequired Changes:")
    print(f"  Maximum allowed IaC mentions: {max_allowed_iac}")
    print(f"  Need to reduce IaC mentions by: {needed_reductions}")
    
    # Phase 2: Fix files
    print("\n" + "=" * 80)
    print("Phase 2: Fixing files...")
    print("-" * 80)
    
    total_replacements = 0
    files_modified = 0
    
    for file_path in chapter_files:
        result = fix_file(file_path, aggressive=True, dry_run=False)
        
        if result['status'] == 'fixed':
            files_modified += 1
            total_replacements += result['replacements']
            print(f"✓ {result['file']:40s} - {result['replacements']:3d} replacements "
                  f"(ratio: {result['old_ratio']:.2f}:1 → {result['new_ratio']:.2f}:1)")
        elif result['status'] == 'already_compliant':
            print(f"✓ {result['file']:40s} - already compliant ({result['old_ratio']:.2f}:1)")
    
    # Phase 3: Final verification
    print("\n" + "=" * 80)
    print("Phase 3: Final verification...")
    print("-" * 80)
    
    final_aac = 0
    final_iac = 0
    
    for file_path in chapter_files:
        analysis = analyze_file(file_path)
        final_aac += analysis['aac_count']
        final_iac += analysis['total_iac']
    
    final_ratio = final_aac / final_iac if final_iac > 0 else float('inf')
    
    print(f"\nFinal Status:")
    print(f"  Architecture as Code mentions: {final_aac}")
    print(f"  Infrastructure as Code mentions: {final_iac}")
    print(f"  Final ratio: {final_ratio:.2f}:1")
    print(f"  Target ratio: 20:1")
    print(f"  Compliant: {'✅ YES' if final_ratio >= 20 else '❌ NO'}")
    
    print(f"\nSummary:")
    print(f"  Files modified: {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print(f"  Ratio improvement: {current_ratio:.2f}:1 → {final_ratio:.2f}:1")
    
    print("\n" + "=" * 80)
    
    if final_ratio >= 20:
        print("✅ SUCCESS: Repository now meets the 20:1 ratio requirement!")
    else:
        print("⚠️  WARNING: Ratio still below target. Manual review may be needed.")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
