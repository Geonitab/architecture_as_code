#!/usr/bin/env python3
"""
Script to translate the remaining documentation files that aren't covered by batch_translate.py
"""

import sys
from pathlib import Path

# Import translation functionality from batch_translate
sys.path.insert(0, str(Path(__file__).parent))
from batch_translate import translate_markdown_file

def main():
    """Translate remaining documentation files."""
    
    # Files to translate
    files_to_translate = [
        Path('exports/book-cover/README.md'),
        Path('releases/README.md'),
        Path('tests/README.md'),
    ]
    
    print("=" * 70)
    print("📚 Translating Remaining Documentation Files")
    print("=" * 70)
    print()
    
    success_count = 0
    error_count = 0
    
    for swedish_path in files_to_translate:
        if not swedish_path.exists():
            print(f"⚠️  File not found: {swedish_path}")
            continue
        
        try:
            # Create English filename
            en_filename = f"{swedish_path.stem}_en{swedish_path.suffix}"
            en_path = swedish_path.parent / en_filename
            
            # Check if already exists
            if en_path.exists():
                print(f"⏭️  Skipping {swedish_path} (already exists: {en_path.name})")
                continue
            
            # Translate the file
            print(f"🔄 Translating {swedish_path}...")
            translated_content = translate_markdown_file(swedish_path)
            
            # Write English file
            with open(en_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"✅ Created {en_path}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error translating {swedish_path}: {e}")
            error_count += 1
    
    print()
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"✅ Successfully translated: {success_count}")
    print(f"❌ Errors: {error_count}")
    print()

if __name__ == "__main__":
    main()
