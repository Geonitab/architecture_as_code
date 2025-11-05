#!/usr/bin/env python3
"""
Diagram Brand Compliance Validator

This script validates that Mermaid diagrams comply with Kvadrat brand guidelines
for the Architecture as Code book.

Validation checks:
1. No inline theme configuration (%%{init: {...}}%%)
2. British English spelling (no American spellings)
3. No emojis in titles or labels
4. Proper use of CSS classes (:::kv-*)

Usage:
    python3 scripts/validate_diagram_branding.py                    # Check all diagrams
    python3 scripts/validate_diagram_branding.py --staged           # Check staged files only
    python3 scripts/validate_diagram_branding.py path/to/file.mmd   # Check specific file
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
import argparse


class BrandComplianceValidator:
    """Validates diagram files against brand compliance rules."""
    
    # American to British spelling mappings
    AMERICAN_SPELLINGS = {
        'organization': 'organisation',
        'organizations': 'organisations',
        'organizational': 'organisational',
        'optimize': 'optimise',
        'optimized': 'optimised',
        'optimizing': 'optimising',
        'optimization': 'optimisation',
        'optimizations': 'optimisations',
        'optimizer': 'optimiser',
        'color': 'colour',
        'colors': 'colours',
        'colored': 'coloured',
        'colorize': 'colourise',
        'center': 'centre',
        'centered': 'centred',
        'centers': 'centres',
        'behavior': 'behaviour',
        'behavioral': 'behavioural',
        'behaviors': 'behaviours',
        'digitization': 'digitisation',
        'digitalization': 'digitalisation',
        'containerization': 'containerisation',
        'modernization': 'modernisation',
        'standardization': 'standardisation',
    }
    
    # Emoji Unicode ranges to detect
    EMOJI_PATTERN = re.compile(
        r'[\U0001F300-\U0001F9FF]|'  # Misc Symbols and Pictographs
        r'[\U0001F600-\U0001F64F]|'  # Emoticons
        r'[\U0001F680-\U0001F6FF]|'  # Transport and Map
        r'[\U00002600-\U000027BF]|'  # Misc symbols
        r'[\U0001F1E0-\U0001F1FF]|'  # Flags
        r'[\U00002700-\U000027BF]|'  # Dingbats
        r'[\U0001F900-\U0001F9FF]|'  # Supplemental Symbols and Pictographs
        r'[\U00002B50]|'             # Star
        r'[\U00002764]|'             # Heart
        r'[\U0001F3FB-\U0001F3FF]'   # Skin tones
    )
    
    def __init__(self):
        self.issues: Dict[str, List[str]] = {}
    
    def check_inline_theme(self, content: str, filepath: str) -> List[str]:
        """Detect inline theme configuration blocks."""
        issues = []
        for i, line in enumerate(content.split('\n'), 1):
            if '%%{init:' in line:
                issues.append(
                    f"Line {i}: Inline theme configuration detected. "
                    f"Use central theme file (docs/mermaid-kvadrat-theme.json) instead."
                )
        return issues
    
    def check_american_spelling(self, content: str, filepath: str) -> List[str]:
        """Detect American English spellings."""
        issues = []
        content_lower = content.lower()
        
        for american, british in self.AMERICAN_SPELLINGS.items():
            # Use word boundaries to avoid false positives
            pattern = re.compile(r'\b' + re.escape(american) + r'\b', re.IGNORECASE)
            matches = pattern.finditer(content)
            
            for match in matches:
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                issues.append(
                    f"Line {line_num}: American spelling '{match.group()}' detected. "
                    f"Use British spelling '{british}' instead."
                )
        
        return issues
    
    def check_emojis(self, content: str, filepath: str) -> List[str]:
        """Detect emojis in content."""
        issues = []
        
        for i, line in enumerate(content.split('\n'), 1):
            if self.EMOJI_PATTERN.search(line):
                # Extract the emoji for display
                emojis_found = self.EMOJI_PATTERN.findall(line)
                issues.append(
                    f"Line {i}: Emoji detected: {' '.join(emojis_found)}. "
                    f"Remove emojis for professional brand compliance."
                )
        
        return issues
    
    def check_css_classes(self, content: str, filepath: str) -> List[str]:
        """Verify proper CSS class usage."""
        issues = []
        valid_classes = ['kv-primary', 'kv-accent', 'kv-highlight', 'kv-muted', 'kv-pattern', 'kv-outline']
        
        # Find all CSS class definitions
        class_pattern = re.compile(r':::([a-zA-Z0-9_-]+)')
        matches = class_pattern.finditer(content)
        
        for match in matches:
            class_name = match.group(1)
            if class_name.startswith('kv-') and class_name not in valid_classes:
                line_num = content[:match.start()].count('\n') + 1
                issues.append(
                    f"Line {line_num}: Invalid CSS class ':::{class_name}'. "
                    f"Valid classes: {', '.join(valid_classes)}"
                )
        
        return issues
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single diagram file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return False
        
        file_issues = []
        
        # Run all validation checks
        file_issues.extend(self.check_inline_theme(content, str(filepath)))
        file_issues.extend(self.check_american_spelling(content, str(filepath)))
        file_issues.extend(self.check_emojis(content, str(filepath)))
        file_issues.extend(self.check_css_classes(content, str(filepath)))
        
        if file_issues:
            self.issues[str(filepath)] = file_issues
            return False
        
        return True
    
    def print_report(self) -> int:
        """Print validation report and return exit code."""
        if not self.issues:
            print("✅ All diagrams pass brand compliance validation!")
            return 0
        
        print(f"\n❌ Brand compliance issues found in {len(self.issues)} file(s):\n")
        
        total_issues = 0
        for filepath, file_issues in sorted(self.issues.items()):
            print(f"📄 {filepath}")
            for issue in file_issues:
                print(f"   • {issue}")
                total_issues += 1
            print()
        
        print(f"Total issues: {total_issues}\n")
        print("Refer to docs/DIAGRAM_STYLE_GUIDE.md for brand compliance guidelines.")
        
        return 1


def get_diagram_files(args) -> List[Path]:
    """Get list of diagram files to validate."""
    if args.file:
        # Validate specific file
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        return [filepath]
    
    if args.staged:
        # Get staged files from git
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                capture_output=True,
                text=True,
                check=True
            )
            staged_files = result.stdout.strip().split('\n')
            diagram_files = [
                Path(f) for f in staged_files 
                if f.endswith('.mmd') and Path(f).exists()
            ]
            return diagram_files
        except subprocess.CalledProcessError as e:
            print(f"Error getting staged files: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Default: validate all diagram files
    docs_images = Path('docs/images')
    if not docs_images.exists():
        print(f"Error: Directory not found: {docs_images}", file=sys.stderr)
        sys.exit(1)
    
    return list(docs_images.glob('*.mmd'))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate diagram files against Kvadrat brand compliance rules',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_diagram_branding.py
  python3 scripts/validate_diagram_branding.py --staged
  python3 scripts/validate_diagram_branding.py docs/images/diagram_04_iac_tools_quadrant.mmd

For more information, see docs/DIAGRAM_STYLE_GUIDE.md
"""
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Specific diagram file to validate'
    )
    
    parser.add_argument(
        '--staged',
        action='store_true',
        help='Only validate staged files in git'
    )
    
    args = parser.parse_args()
    
    # Get files to validate
    diagram_files = get_diagram_files(args)
    
    if not diagram_files:
        print("No diagram files found to validate.")
        return 0
    
    print(f"Validating {len(diagram_files)} diagram file(s)...\n")
    
    # Run validation
    validator = BrandComplianceValidator()
    
    passed = 0
    failed = 0
    
    for filepath in diagram_files:
        if validator.validate_file(filepath):
            passed += 1
        else:
            failed += 1
    
    # Print summary
    print(f"Validated: {len(diagram_files)} files")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    
    # Print detailed report and return exit code
    return validator.print_report()


if __name__ == '__main__':
    sys.exit(main())
