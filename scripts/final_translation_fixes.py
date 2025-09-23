#!/usr/bin/env python3
"""
Final manual fixes for the most critical translation issues
"""

import os
import re
from pathlib import Path

def apply_final_fixes(content):
    """Apply final manual fixes to translation"""
    
    # Critical fixes for readability
    fixes = [
        # Fix version control terminology
        ('versionsis managed', 'version controlled'),
        ('version control and is managed', 'version controlled and managed'),
        
        # Fix remaining Swedish words
        ('traditionell', 'traditional'),
        ('den comprehensive', 'the comprehensive'),
        ('Evolution mot', 'Evolution towards'),
        ('omfattning', 'scope'),
        ('automatiskt', 'automatically'),
        ('applikationskomponenter', 'application components'),
        ('knowledge om how', 'knowledge of how'),
        ('want understand implement', 'want to understand and implement'),
        
        # Fix grammatical issues
        ('this book', 'This book'),
        ('this holistic', 'This holistic'),
        ('without also', 'but also'),
        ('that want', 'who want'),
        ('can is codified', 'can be codified'),
        
        # Fix sentence structure
        ('The reader will gain comprehensive knowledge of how the entire system architecture can be codified',
         'The reader will gain comprehensive knowledge of how the entire system architecture can be codified'),
    ]
    
    result = content
    for old, new in fixes:
        result = result.replace(old, new)
    
    # Fix header capitalization
    result = re.sub(r'^# ([a-z])', lambda m: '# ' + m.group(1).upper(), result, flags=re.MULTILINE)
    result = re.sub(r'^## ([a-z])', lambda m: '## ' + m.group(1).upper(), result, flags=re.MULTILINE)
    result = re.sub(r'^### ([a-z])', lambda m: '### ' + m.group(1).upper(), result, flags=re.MULTILINE)
    
    # Clean up whitespace
    result = re.sub(r'\n\n\n+', '\n\n', result)
    result = re.sub(r'  +', ' ', result)
    
    return result

def main():
    """Apply final fixes to all English files"""
    docs_dir = Path("docs")
    english_files = list(docs_dir.glob("*_en.md"))
    
    print(f"🔧 Applying final fixes to {len(english_files)} English files...")
    
    for file_path in english_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content = apply_final_fixes(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"✅ Fixed: {file_path.name}")
        
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
    
    print("✨ Final fixes completed!")

if __name__ == "__main__":
    main()