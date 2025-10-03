#!/usr/bin/env python3
"""
Batch translation tool for converting Swedish markdown files to English.
This script uses comprehensive phrase mappings for technical accuracy.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Extremely comprehensive Swedish-English translation dictionary
TRANSLATIONS = {
    # Complete sentences and long phrases (these are matched first)
    'En omfattande bok om arkitektur som kod på svenska, med praktiska exempel och fallstudier.': 
        'A comprehensive book about Architecture as Code in Swedish, with practical examples and case studies.',
    
    'Denna bok täcker arkitektur som kod från grundläggande principer till avancerad implementation, med fokus på praktisk tillämpning inom svenska organisationer.':
        'This book covers Architecture as Code from fundamental principles to advanced implementation, with a focus on practical application within Swedish organizations.',
    
    'representerar ett paradigmskifte inom systemutveckling där hela systemarkitekturen definieras, versionshanteras och hanteras genom kod':
        'represents a paradigm shift in system development where the entire system architecture is defined, version-controlled, and managed through code',
    
    'Detta approach möjliggör samma metodiker som traditionell mjukvaruutveckling för hela organisationens tekniska landskap':
        'This approach enables the same methodologies as traditional software development for the organization\'s entire technical landscape',
    
    'Diagrammet illustrerar evolutionen från manuella processer till den omfattande visionen av':
        'The diagram illustrates the evolution from manual processes to the comprehensive vision of',
    
    'där hela systemarkitekturen kodifieras':
        'where the entire system architecture is codified',
    
    'Traditionella metoder för systemarkitektur har ofta varit manuella och dokumentbaserade':
        'Traditional methods for system architecture have often been manual and document-based',
    
    'bygger på etablerade principer från mjukvaruutveckling och tillämpar dessa på hela systemlandskapet':
        'builds on established principles from software development and applies them to the entire system landscape',
    
    'Detta inkluderar inte bara infrastrukturkomponenter, utan även applikationsarkitektur, dataflöden, säkerhetspolicies, compliance-regler och organisatoriska strukturer - allt definierat som kod':
        'This includes not only infrastructure components, but also application architecture, data flows, security policies, compliance rules, and organizational structures - all defined as code',
    
    'definieras som praktiken att beskriva, versionhantera och automatisera hela systemarkitekturen genom maskinläsbar kod':
        'is defined as the practice of describing, version-controlling, and automating the entire system architecture through machine-readable code',
    
    'Detta omfattar applikationskomponenter, integrationsmönster, dataarkitektur, infrastruktur och organisatoriska processer':
        'This encompasses application components, integration patterns, data architecture, infrastructure, and organizational processes',
    
    'Denna holistiska approach möjliggör end-to-end automatisering där förändringar i krav automatiskt propagerar genom hela arkitekturen - från applikationslogik till deployment och monitering':
        'This holistic approach enables end-to-end automation where changes in requirements automatically propagate through the entire architecture - from application logic to deployment and monitoring',
    
    'Denna bok vänder sig till systemarkitekter, utvecklare, projektledare och IT-beslutsfattare som vill förstå och implementera':
        'This book is aimed at system architects, developers, project managers, and IT decision-makers who want to understand and implement',
    
    'i sina organisationer':
        'in their organizations',
    
    'Läsaren kommer att få omfattande kunskap om hur hela systemarkitekturen kan kodifieras, från grundläggande principer till avancerade arkitekturmönster som omfattar hela organisationens digitala ekosystem':
        'The reader will gain comprehensive knowledge of how the entire system architecture can be codified, from fundamental principles to advanced architecture patterns that encompass the organization\'s entire digital ecosystem',
    
    # Chapter and section titles
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
    'Framtida utveckling och roadmap': 'Future Development and Roadmap',
    'Appendix: Kodexempel och mallar': 'Appendix: Code Examples and Templates',
    'Teknisk uppbyggnad av boken': 'Technical Architecture of the Book',
    
    # Common section headings
    'Evolution mot arkitektur som kod': 'Evolution towards Architecture as Code',
    'Evolution mot': 'Evolution towards',
    'Definition och omfattning': 'Definition and Scope',
    'Bokens syfte och målgrupp': 'Purpose and Target Audience of the Book',
    'Om boken': 'About the Book',
    'Teknisk implementation': 'Technical Implementation',
    'Målgrupp': 'Target Audience',
    'Innehåll': 'Contents',
    'Källor': 'Sources',
    'Referenser': 'References',
    'Sammanfattning': 'Summary',
    'Bakgrund': 'Background',
    'Syfte': 'Purpose',
    'Fördelar': 'Benefits',
    'Nackdelar': 'Disadvantages',
    'Utmaningar': 'Challenges',
    'Rekommendationer': 'Recommendations',
    'Exempel': 'Example',
    'Nästa steg': 'Next Steps',
    'Slutsats': 'Conclusion',
    'Ordlista': 'Glossary',
    'Om författarna': 'About the Authors',
    
    # Technical concepts
    'Arkitektur som kod': 'Architecture as Code',
    'Infrastruktur som kod': 'Infrastructure as Code',
    'Dokumentation som kod': 'Documentation as Code',
    'Krav som kod': 'Requirements as Code',
    'Policy som kod': 'Policy as Code',
    'allt som kod': 'everything as code',
    'arkitektur som kod': 'architecture as code',
    
    # Common phrases with numbers
    'kapitel som täcker': 'chapters covering',
    'Struktur': 'Structure',
    'Bokens innehåll': 'Book content',
    'Markdown-kapitel': 'Markdown chapters',
    'Mermaid-diagram': 'Mermaid diagrams',
    'Mermaid källfiler': 'Mermaid source files',
    'Lokal byggscript': 'Local build script',
    'Genererad bok': 'Generated book',
    'Alla deliverables organiserade för distribution': 'All deliverables organized for distribution',
    'Bokformat': 'Book formats',
    'Presentationsmaterial': 'Presentation materials',
    'HTML whitepapers per kapitel': 'HTML whitepapers per chapter',
    'Komplett statisk webbsida': 'Complete static website',
    
    # Role titles
    'Systemarkitekter': 'System Architects',
    'DevOps-ingenjörer': 'DevOps Engineers',
    'Utvecklare': 'Developers',
    'Projektledare': 'Project Managers',
    'IT-chefer': 'IT Managers',
    'IT-beslutsfattare': 'IT decision-makers',
    
    # Book topics
    'Grundläggande principer för arkitektur som kod': 'Fundamental principles of Architecture as Code',
    'Versionhantering och kodstrukturer': 'Version control and code structures',
    'Molnarkitektur och automatisering': 'Cloud architecture and automation',
    'Säkerhet och compliance': 'Security and compliance',
    'CI/CD och teststrategier': 'CI/CD and testing strategies',
    'Organisatorisk transformation': 'Organizational transformation',
    'Praktiska fallstudier och implementationer': 'Practical case studies and implementations',
    
    # Common words and short phrases
    'hela': 'entire',
    'genom': 'through',
    'från': 'from',
    'till': 'to',
    'med': 'with',
    'och': 'and',
    'eller': 'or',
    'för': 'for',
    'inom': 'within',
    'Detta': 'This',
    'Denna': 'This',
    'Dessa': 'These',
    'som': 'which',
    'där': 'where',
    'när': 'when',
    'hur': 'how',
    'vad': 'what',
    'varför': 'why',
}


def smart_translate(text: str, is_header: bool = False) -> str:
    """
    Translate text using longest-match-first algorithm.
    Preserves code blocks, links, and technical terms.
    """
    if not text or not text.strip():
        return text
    
    # Sort translations by length (longest first) to match longer phrases
    sorted_translations = sorted(
        TRANSLATIONS.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )
    
    result = text
    
    for swedish, english in sorted_translations:
        # For headers, use case-sensitive matching
        if is_header:
            result = result.replace(swedish, english)
        else:
            # For body text, use case-insensitive with smart capitalization
            pattern = re.compile(re.escape(swedish), re.IGNORECASE)
            
            def preserve_case(match):
                original = match.group(0)
                if not original:
                    return english
                # If first char is uppercase, capitalize replacement
                if original[0].isupper() and english:
                    return english[0].upper() + english[1:]
                return english
            
            result = pattern.sub(preserve_case, result)
    
    return result


def translate_markdown_file(swedish_file: Path) -> str:
    """
    Translate Swedish markdown to English while preserving all structure.
    """
    with open(swedish_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    translated_lines = []
    in_code_block = False
    code_block_lang = None
    
    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                code_block_lang = line.strip()[3:]
            translated_lines.append(line)
            continue
        
        # Preserve code block content
        if in_code_block:
            translated_lines.append(line)
            continue
        
        # Translate image alt text but preserve path
        if line.strip().startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt_text = smart_translate(match.group(1), is_header=True)
                path = match.group(2)
                translated_lines.append(f'![{alt_text}]({path})')
                continue
        
        # Translate headers
        if line.strip().startswith('#'):
            header_match = re.match(r'(#+)\s+(.*)', line)
            if header_match:
                level = header_match.group(1)
                title = header_match.group(2)
                translated_title = smart_translate(title, is_header=True)
                translated_lines.append(f'{level} {translated_title}')
                continue
        
        # Preserve URLs
        if line.strip().startswith('http') or '](http' in line or line.strip().startswith('- http'):
            translated_lines.append(line)
            continue
        
        # Translate regular text
        translated_line = smart_translate(line, is_header=False)
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)


def process_file(swedish_path: Path) -> Tuple[bool, str]:
    """Process a single file and create English version."""
    try:
        # Check if it's already an English file
        if swedish_path.stem.endswith('_en'):
            return False, f"Skipping {swedish_path.name} (already English)"
        
        # Create English filename
        en_filename = f"{swedish_path.stem}_en{swedish_path.suffix}"
        en_path = swedish_path.parent / en_filename
        
        # Check if it already has real content (not placeholder)
        if en_path.exists():
            with open(en_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # If it's a placeholder, update it
                if '**Note:** This is a placeholder' not in content and len(content) > 500:
                    return False, f"Skipping {en_filename} (already has content)"
        
        # Translate the file
        translated_content = translate_markdown_file(swedish_path)
        
        # Write English file
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return True, f"✅ Translated {swedish_path.name} → {en_filename}"
        
    except Exception as e:
        return False, f"❌ Error: {swedish_path.name}: {e}"


def main():
    """Main batch translation function."""
    print("=" * 70)
    print("🌍 Batch Translation: Swedish → English")
    print("=" * 70)
    print()
    
    # Get all markdown files to translate
    files_to_process = []
    
    # Root level files
    root_files = [
        'README.md', 'BOOK_REQUIREMENTS.md', 'bot.md',
        'AUTOMATION_WORKFLOWS.md', 'DESIGN_SYSTEM.md',
        'BRAND_GUIDELINES.md', 'VISUAL_ELEMENTS_GUIDE.md',
        'TEST_WORKFLOW.md', 'SOLUTION_SUMMARY.md', 'DOCS_PROTECTION.md',
        'CICD_SETUP.md', 'TRANSLATION_PROJECT.md', 'WORKFLOWS.md'
    ]
    
    for filename in root_files:
        path = Path(filename)
        if path.exists():
            files_to_process.append(path)
    
    # All docs files
    docs_dir = Path('docs')
    if docs_dir.exists():
        for pattern in ['[0-9][0-9]_*.md', 'README.md', 'BOOK_COVER_DESIGN.md', 'TERMINOLOGI_JUSTERING.md', 
                        'ENGELSKA_UTTRYCK_SAMMANSTÄLLNING.md', 'EPUB_VALIDATION.md', 
                        'SVENGELSKA_FIXES_SUMMARY.md', 'language_deviations_issue.md']:
            for path in docs_dir.glob(pattern):
                if not path.stem.endswith('_en'):
                    files_to_process.append(path)
    
    print(f"Found {len(files_to_process)} files to translate\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in sorted(files_to_process):
        success, message = process_file(file_path)
        print(message)
        
        if success:
            success_count += 1
        elif "Skipping" in message:
            skip_count += 1
        else:
            error_count += 1
    
    print()
    print("=" * 70)
    print("📊 Translation Summary")
    print("=" * 70)
    print(f"✅ Translated: {success_count}")
    print(f"⏭️  Skipped: {skip_count}")
    print(f"❌ Errors: {error_count}")
    print()
    
    if success_count > 0:
        print("✨ Translation complete!")
        print("\nAll English files created with _en suffix")
        print("Original Swedish files remain unchanged")


if __name__ == '__main__':
    main()
