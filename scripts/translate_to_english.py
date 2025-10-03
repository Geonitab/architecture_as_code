#!/usr/bin/env python3
"""
Script to create English markdown file templates from Swedish originals.
Creates English versions with _en suffix while preserving Swedish originals.

This script creates TEMPLATE files that preserve structure and require
manual translation or professional translation service for content accuracy.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Comprehensive translation dictionary for technical terms and chapter titles
TRANSLATIONS = {
    # Chapter titles (from build_book.sh and generate_book.py)
    'Inledning till arkitektur som kod': 'Introduction to Architecture as Code',
    'Grundläggande principer för Architecture as Code': 'Fundamental Principles of Architecture as Code',
    'Versionhantering och kodstruktur': 'Version Control and Code Structure',
    'Architecture Decision Records (ADR)': 'Architecture Decision Records (ADR)',
    'Automatisering, DevOps och CI/CD': 'Automation, DevOps and CI/CD',
    'Molnarkitektur som kod': 'Cloud Architecture as Code',
    'Containerisering och orkestrering': 'Containerization and Orchestration',
    'Mikrotjänster och API-design': 'Microservices and API Design',
    'Säkerhet i arkitektur som kod': 'Security in Architecture as Code',
    'Policy som kod och säkerhetsautomatisering': 'Policy as Code and Security Automation',
    'Compliance och regelefterlevnad': 'Compliance and Regulatory Adherence',
    'Teststrategier för arkitekturkod': 'Testing Strategies for Architecture Code',
    'Praktisk implementation': 'Practical Implementation',
    'Kostnadsoptimering och resurshantering': 'Cost Optimization and Resource Management',
    'Migration från traditionell infrastruktur': 'Migration from Traditional Infrastructure',
    'Organisatorisk förändring och kulturomställning': 'Organizational Change and Cultural Transformation',
    'Team-struktur och kompetens': 'Team Structure and Competencies',
    'Digitalisering och affärsnytta': 'Digitalization and Business Value',
    'Lovable Mockups och användarcentrerad design': 'Lovable Mockups and User-Centered Design',
    'Framtida trender inom Architecture as Code': 'Future Trends in Architecture as Code',
    'Best practices och lärda läxor': 'Best Practices and Lessons Learned',
    'Slutsats': 'Conclusion',
    'Ordlista': 'Glossary',
    'Om författarna': 'About the Authors',
    'Framtida utveckling och roadmap': 'Future Development and Roadmap',
    'Appendix: Kodexempel och mallar': 'Appendix: Code Examples and Templates',
    'Teknisk uppbyggnad av boken': 'Technical Architecture of the Book',
    
    # Common headings
    'Sammanfattning': 'Summary',
    'Bakgrund': 'Background',
    'Syfte': 'Purpose',
    'Målgrupp': 'Target Audience',
    'Innehåll': 'Contents',
    'Definition och omfattning': 'Definition and Scope',
    'Källor': 'Sources',
    'Referenser': 'References',
    'Exempel': 'Example',
    'Fördelar': 'Benefits',
    'Nackdelar': 'Disadvantages',
    'Utmaningar': 'Challenges',
    'Rekommendationer': 'Recommendations',
    
    # Architecture concepts
    'Arkitektur som kod': 'Architecture as Code',
    'Infrastruktur som kod': 'Infrastructure as Code',
    'Dokumentation som kod': 'Documentation as Code',
    'Krav som kod': 'Requirements as Code',
    'Policy som kod': 'Policy as Code',
    'Allt som kod': 'Everything as Code',
}


def translate_heading(text: str) -> str:
    """Translate a heading or title using the translation dictionary."""
    # Try exact match first
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    
    # Try partial matches for longer headings
    result = text
    for swedish, english in TRANSLATIONS.items():
        if swedish in result:
            result = result.replace(swedish, english)
    
    return result


def create_english_template(content: str, filename: str) -> str:
    """
    Create an English template from Swedish markdown content.
    
    This function:
    1. Preserves all code blocks, images, links
    2. Translates known headings and terms
    3. Marks other content for manual translation
    
    Args:
        content: Swedish markdown content
        filename: Name of the file being translated
        
    Returns:
        English template content with translation markers
    """
    lines = content.split('\n')
    translated_lines = []
    in_code_block = False
    
    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue
        
        # Preserve code block content as-is
        if in_code_block:
            translated_lines.append(line)
            continue
        
        # Preserve images (update alt text but keep path)
        if line.strip().startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt_text = translate_heading(match.group(1))
                path = match.group(2)
                translated_lines.append(f'![{alt_text}]({path})')
                continue
        
        # Preserve links
        if line.strip().startswith('http') or '](http' in line:
            translated_lines.append(line)
            continue
        
        # Translate headers
        if line.strip().startswith('#'):
            header_match = re.match(r'(#+)\s+(.*)', line)
            if header_match:
                level = header_match.group(1)
                title = header_match.group(2)
                translated_title = translate_heading(title)
                translated_lines.append(f'{level} {translated_title}')
                continue
        
        # For non-header, non-code content, mark for manual translation
        # but translate known terms
        if line.strip():
            translated_line = line
            # Only translate exact standalone terms to avoid breaking text
            for swedish, english in TRANSLATIONS.items():
                # Avoid replacing parts of words
                if swedish in ['och', 'eller', 'för', 'med', 'till', 'från', 'som']:
                    continue  # Skip common words that might break sentences
                pattern = r'\b' + re.escape(swedish) + r'\b'
                translated_line = re.sub(pattern, english, translated_line)
            translated_lines.append(translated_line)
        else:
            translated_lines.append(line)
    
    # Add header note
    header = f"""<!-- 
English Translation Template
Original: {filename}
Status: REQUIRES MANUAL TRANSLATION

This file contains:
- Translated headings and known technical terms
- Preserved code blocks and images
- Swedish text that needs professional translation

Please review and translate all Swedish text for technical accuracy.
-->

"""
    
    return header + '\n'.join(translated_lines)


def translate_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Translate a single markdown file to English.
    
    Args:
        file_path: Path to the Swedish markdown file
        dry_run: If True, don't write files, just report what would be done
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Read the Swedish content
        with open(file_path, 'r', encoding='utf-8') as f:
            swedish_content = f.read()
        
        # Skip if already an English file
        if file_path.stem.endswith('_en'):
            return False, f"Skipping {file_path.name} (already English)"
        
        # Create English filename
        stem = file_path.stem
        suffix = file_path.suffix
        en_filename = f"{stem}_en{suffix}"
        en_path = file_path.parent / en_filename
        
        # Check if English version already exists
        if en_path.exists() and not dry_run:
            return False, f"Skipping {file_path.name} (English version exists)"
        
        if dry_run:
            return True, f"Would create: {en_path}"
        
        # Create English template
        english_content = create_english_template(swedish_content, file_path.name)
        
        # Write English file
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(english_content)
        
        return True, f"✅ Created {en_filename}"
        
    except Exception as e:
        return False, f"❌ Error processing {file_path}: {e}"


def get_files_to_translate() -> List[Path]:
    """
    Get list of all markdown files that should be translated.
    
    Returns:
        List of Path objects for files to translate
    """
    base_dir = Path('.')
    files_to_translate = []
    
    # Root level markdown files
    root_md_files = [
        'README.md',
        'BOOK_REQUIREMENTS.md',
        'AUTOMATION_WORKFLOWS.md',
        'DESIGN_SYSTEM.md',
        'BRAND_GUIDELINES.md',
        'VISUAL_ELEMENTS_GUIDE.md',
        'TEST_WORKFLOW.md',
        'SOLUTION_SUMMARY.md',
        'DOCS_PROTECTION.md',
        'bot.md',
        'CICD_SETUP.md',
        'TRANSLATION_PROJECT.md',
        'WORKFLOWS.md',
    ]
    
    for filename in root_md_files:
        file_path = base_dir / filename
        if file_path.exists():
            files_to_translate.append(file_path)
    
    # All numbered chapter files in docs/
    docs_dir = base_dir / 'docs'
    if docs_dir.exists():
        # Get all numbered chapter files (01-27)
        for i in range(1, 28):
            pattern = f"{i:02d}_*.md"
            for file_path in docs_dir.glob(pattern):
                if not file_path.stem.endswith('_en'):
                    files_to_translate.append(file_path)
        
        # Additional docs files
        docs_support_files = [
            'README.md',
            'BOOK_COVER_DESIGN.md',
            'TERMINOLOGI_JUSTERING.md',
            'ENGELSKA_UTTRYCK_SAMMANSTÄLLNING.md',
            'EPUB_VALIDATION.md',
            'SVENGELSKA_FIXES_SUMMARY.md',
            'language_deviations_issue.md',
        ]
        
        for filename in docs_support_files:
            file_path = docs_dir / filename
            if file_path.exists():
                files_to_translate.append(file_path)
    
    return sorted(files_to_translate)


def main():
    """Main function to translate all markdown files."""
    print("=" * 70)
    print("📚 Markdown Translation: Swedish → English")
    print("=" * 70)
    print()
    
    # Get files to translate
    files = get_files_to_translate()
    
    print(f"Found {len(files)} files to translate\n")
    
    # First pass: dry run to show what will be done
    print("🔍 Dry run - showing what will be created:")
    print("-" * 70)
    for file_path in files:
        success, message = translate_file(file_path, dry_run=True)
        if success:
            print(f"  {message}")
    
    print()
    print("=" * 70)
    print("⚠️  NOTE: This is a TEMPLATE generator only!")
    print("=" * 70)
    print("""
The script creates English file templates with:
- Preserved markdown structure (headers, code blocks, links)
- Basic term translations for common technical terms
- Original Swedish text for manual translation

NEXT STEPS REQUIRED:
1. Review each generated *_en.md file
2. Manually translate or use professional translation service
3. Verify technical accuracy
4. Update generate_book.py for English book generation
5. Update build_book.sh for English PDF building

This ensures translation quality and technical correctness.
""")
    
    # Ask for confirmation
    response = input("\nProceed with creating template files? (y/N): ").strip().lower()
    
    if response != 'y':
        print("\n❌ Translation cancelled.")
        return
    
    print("\n" + "=" * 70)
    print("🚀 Creating English template files...")
    print("=" * 70)
    print()
    
    # Actual translation
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in files:
        success, message = translate_file(file_path, dry_run=False)
        print(f"  {message}")
        
        if success:
            success_count += 1
        elif "Skipping" in message or "exists" in message:
            skip_count += 1
        else:
            error_count += 1
    
    print()
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"  ✅ Created: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    print()
    
    if success_count > 0:
        print("✨ Template files created successfully!")
        print()
        print("⚠️  IMPORTANT: All *_en.md files need manual translation review!")
        print("   The files contain structure and basic term translations only.")
        print()


if __name__ == "__main__":
    main()
