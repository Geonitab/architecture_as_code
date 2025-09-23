#!/usr/bin/env python3
"""
Script to systematically replace English terms with Swedish equivalents
throughout the book documentation.
"""

import os
import re
from pathlib import Path

# Define the replacement mappings
REPLACEMENTS = {
    # High priority replacements
    r'\bstakeholder\b': 'intressent',
    r'\bstakeholders\b': 'intressenter',
    r'\bguidelines\b': 'riktlinjer',
    r'\bguideline\b': 'riktlinje',
    r'\bend-to-end\b': 'fullständig',
    r'\bcross-functional\b': 'tvärfunktionell',
    r'\brollout\b': 'utrullning',
    r'\brollouts\b': 'utrullningar',
    r'\brollback\b': 'återställning',
    r'\brollbacks\b': 'återställningar',
    r'\btimeline\b': 'tidslinje',
    r'\btimelines\b': 'tidslinjer',
    
    # Medium priority replacements
    r'\bframework\b': 'ramverk',
    r'\bframeworks\b': 'ramverk',
    r'\bplatform\b': 'plattform',
    r'\bplatforms\b': 'plattformar',
    r'\btools\b': 'verktyg',
    r'\btool\b': 'verktyg',
    r'\bsetup\b': 'konfiguration',
    r'\bsetups\b': 'konfigurationer',
    r'\btesting\b': 'testning',
    r'\bmigration\b': 'migrering',
    r'\bmigrations\b': 'migreringar',
    
    # Compliance-related terms
    r'\bcompliance\b': 'efterlevnad',
    r'\bcompliant\b': 'efterlevande',
    
    # Best practices
    r'\bbest practices\b': 'bästa metoder',
    r'\bbest practice\b': 'bästa metod',
}

def process_file(file_path):
    """Process a single markdown file and apply replacements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        for pattern, replacement in REPLACEMENTS.items():
            # Use case-insensitive matching but preserve original case
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in reversed(matches):  # Reverse to maintain positions
                    original_text = match.group()
                    
                    # Preserve capitalization
                    if original_text.isupper():
                        new_text = replacement.upper()
                    elif original_text.istitle():
                        new_text = replacement.capitalize()
                    else:
                        new_text = replacement
                    
                    content = content[:match.start()] + new_text + content[match.end():]
                    changes_made.append(f"{original_text} → {new_text}")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {file_path.name}: {len(changes_made)} changes")
            for change in changes_made[:5]:  # Show first 5 changes
                print(f"   - {change}")
            if len(changes_made) > 5:
                print(f"   ... and {len(changes_made) - 5} more")
        else:
            print(f"⚪ {file_path.name}: No changes needed")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def main():
    """Main function to process all markdown files."""
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print("❌ docs directory not found")
        return
    
    # Get all markdown files except images directory
    md_files = []
    for file_path in docs_dir.glob("*.md"):
        if file_path.name not in ["ENGELSKA_UTTRYCK_SAMMANSTÄLLNING.md"]:
            md_files.append(file_path)
    
    print(f"📚 Processing {len(md_files)} markdown files...")
    print("=" * 50)
    
    for file_path in sorted(md_files):
        process_file(file_path)
    
    print("=" * 50)
    print("✨ Swedish term replacement completed!")

if __name__ == "__main__":
    main()