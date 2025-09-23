#!/usr/bin/env python3
"""
Post-processing script to clean up and perfect the English translation
"""

import os
import re
from pathlib import Path

def clean_translation_issues(content):
    """Clean up common translation artifacts and incomplete translations"""
    
    # Fix badly translated words
    fixes = {
        'developbutt': 'development',
        'deploybutt': 'deployment',
        'buttta': 'ment',
        'butttal': 'mental',
        'monitering': 'monitoring',
        'dokubuttbaserade': 'document-based',
        'implebuttera': 'implement',
        'fundabuttal': 'fundamental',
        'arquitectura that kod': 'architecture as code',
        'system developbutt': 'system development',
        'software developbutt': 'software development',
        'automatisering': 'automation',
        
        # Fix incomplete Swedish words
        'kod': 'code',
        'krav': 'requirements',
        'dessa': 'these',
        'detta': 'this',
        'denna': 'this',
        'alla': 'all',
        'allt': 'all',
        'hela': 'entire',
        'där': 'where',
        'från': 'from',
        'till': 'to',
        'med': 'with',
        'som': 'as',
        'att': 'to',
        'som Y': 'as Y',
        'för': 'for',
        'på': 'on',
        'av': 'of',
        'i': 'in',
        'är': 'is',
        'har': 'has',
        'kan': 'can',
        'ska': 'should',
        'vill': 'want',
        'sina': 'their',
        'hur': 'how',
        'och': 'and',
        'eller': 'or',
        'men': 'but',
        'utan': 'without',
        'inte': 'not',
        'bara': 'only',
        
        # Fix remaining Swedish compound words and phrases
        'systemarkitektur': 'system architecture',
        'infrastrukturkomponenter': 'infrastructure components',
        'applikationsarkitektur': 'application architecture',
        'dataflöden': 'data flows',
        'säkerhetspolicies': 'security policies',
        'compliance-regler': 'compliance rules',
        'strukturer': 'structures',
        'definierat': 'defined',
        'praktiken': 'the practice',
        'beskriva': 'describe',
        'versionhantera': 'version control',
        'automatisera': 'automate',
        'integrationsmönster': 'integration patterns',
        'dataarkitektur': 'data architecture',
        'infrastruktur': 'infrastructure',
        'arkitekturen': 'the architecture',
        'arkitekturmönster': 'architecture patterns',
        'kunskap': 'knowledge',
        'syfte': 'purpose',
        'målgrupp': 'target audience',
        'förstå': 'understand',
        'ekosystem': 'ecosystem',
        
        # Fix document structure words
        'bok': 'book',
        'Bokens': 'The book\'s',
        'bokens': 'the book\'s',
        'Diagrammet illustrerar': 'The diagram illustrates',
        'diagrammet illustrerar': 'the diagram illustrates',
        'evolutionen': 'the evolution',
        'visionen': 'the vision',
        
        # Clean up redundant phrases
        'the entire the ': 'the entire ',
        'the the ': 'the ',
        'is defined that': 'is defined as',
        'that vill': 'who want to',
        'that that': 'that',
        'with with': 'with',
        'and and': 'and',
        'in in': 'in',
        'to to': 'to',
        'can can': 'can',
        ' that  ': ' that ',
        '  ': ' ',  # Remove double spaces
    }
    
    result = content
    for swedish, english in fixes.items():
        # Use word boundaries for single words, direct replacement for phrases
        if ' ' in swedish or swedish in ['developbutt', 'deploybutt', 'buttta']:
            result = result.replace(swedish, english)
        else:
            pattern = r'\b' + re.escape(swedish) + r'\b'
            result = re.sub(pattern, english, result, flags=re.IGNORECASE)
    
    # Fix specific grammatical issues
    result = re.sub(r'\bthat the (\w+) architecture', r'as the \1 architecture', result)
    result = re.sub(r'\bthat code\b', 'as code', result)
    result = re.sub(r'\binfrared(\w*)', r'infrastructure\1', result)
    
    # Capitalize sentences after periods
    result = re.sub(r'(\. )([a-z])', lambda m: m.group(1) + m.group(2).upper(), result)
    
    # Fix title capitalization for headers
    result = re.sub(r'^# ([a-z])', lambda m: '# ' + m.group(1).upper(), result, flags=re.MULTILINE)
    result = re.sub(r'^## ([a-z])', lambda m: '## ' + m.group(1).upper(), result, flags=re.MULTILINE)
    
    return result

def process_english_files():
    """Process all English translation files to clean up issues"""
    docs_dir = Path("docs")
    english_files = list(docs_dir.glob("*_en.md"))
    
    print(f"🔧 Post-processing {len(english_files)} English files...")
    
    for file_path in english_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean up translation issues
            cleaned_content = clean_translation_issues(content)
            
            # Write back cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Cleaned: {file_path.name}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

def fix_pandoc_config():
    """Fix the English Pandoc configuration"""
    config_path = Path("docs/pandoc_english.yaml")
    
    if not config_path.exists():
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix language settings
        content = content.replace('language: sv', 'language: en')
        content = content.replace('lang: en-SE', 'lang: en-US')
        content = content.replace('subtitle: "Infrastructure as Code i praktiken"', 
                                'subtitle: "A Comprehensive Guide"')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed Pandoc English configuration")
    
    except Exception as e:
        print(f"❌ Error fixing Pandoc config: {e}")

if __name__ == "__main__":
    print("🧹 Starting post-processing of English translations...")
    print("=" * 50)
    
    process_english_files()
    fix_pandoc_config()
    
    print("=" * 50)
    print("✨ Post-processing completed!")