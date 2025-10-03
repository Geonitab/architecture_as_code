#!/usr/bin/env python3
"""
Comprehensive translation script for Swedish to English markdown files.
Uses extensive phrase mapping and pattern matching for technical content.
"""

import re
from pathlib import Path
from typing import Dict, List

# Comprehensive Swedish to English translation mappings
PHRASE_TRANSLATIONS = {
    # Full sentence patterns and common phrases
    'representerar ett paradigmskifte inom systemutveckling': 'represents a paradigm shift in system development',
    'där hela systemarkitekturen definieras': 'where the entire system architecture is defined',
    'versionshanteras och hanteras genom kod': 'version-controlled and managed through code',
    'Detta approach möjliggör samma metodiker som': 'This approach enables the same methodologies as',
    'traditionell mjukvaruutveckling för hela organisationens tekniska landskap': 'traditional software development for the organization\'s entire technical landscape',
    
    'Diagrammet illustrerar': 'The diagram illustrates',
    'evolutionen från manuella processer': 'the evolution from manual processes',
    'den omfattande visionen av': 'the comprehensive vision of',
    'där hela systemarkitekturen kodifieras': 'where the entire system architecture is codified',
    
    'Traditionella metoder för systemarkitektur har ofta varit manuella och dokumentbaserade': 'Traditional methods for system architecture have often been manual and document-based',
    'bygger på etablerade principer från': 'builds on established principles from',
    'mjukvaruutveckling och tillämpar dessa på': 'software development and applies them to',
    'hela systemlandskapet': 'the entire system landscape',
    
    'Detta inkluderar inte bara': 'This includes not only',
    'infrastrukturkomponenter, utan även': 'infrastructure components, but also',
    'applikationsarkitektur': 'application architecture',
    'dataflöden': 'data flows',
    'säkerhetspolicies': 'security policies',
    'compliance-regler': 'compliance rules',
    'organisatoriska strukturer': 'organizational structures',
    'allt definierat som kod': 'all defined as code',
    
    'definieras som praktiken att': 'is defined as the practice of',
    'beskriva, versionhantera och automatisera': 'describing, version-controlling, and automating',
    'genom maskinläsbar kod': 'through machine-readable code',
    'Detta omfattar': 'This encompasses',
    'applikationskomponenter': 'application components',
    'integrationsmönster': 'integration patterns',
    'dataarkitektur': 'data architecture',
    'infrastruktur och organisatoriska processer': 'infrastructure and organizational processes',
    
    'Denna holistiska approach möjliggör': 'This holistic approach enables',
    'end-to-end automatisering där': 'end-to-end automation where',
    'förändringar i krav automatiskt propagerar': 'changes in requirements automatically propagate',
    'genom hela arkitekturen': 'through the entire architecture',
    'från applikationslogik till deployment och monitering': 'from application logic to deployment and monitoring',
    
    'Denna bok vänder sig till': 'This book is aimed at',
    'systemarkitekter, utvecklare, projektledare och IT-beslutsfattare': 'system architects, developers, project managers, and IT decision-makers',
    'som vill förstå och implementera': 'who want to understand and implement',
    'i sina organisationer': 'in their organizations',
    
    'Läsaren kommer att få': 'The reader will gain',
    'omfattande kunskap om': 'comprehensive knowledge of',
    'hur hela systemarkitekturen kan kodifieras': 'how the entire system architecture can be codified',
    'från grundläggande principer till': 'from fundamental principles to',
    'avancerade arkitekturmönster': 'advanced architecture patterns',
    'som omfattar hela organisationens digitala ekosystem': 'that encompass the organization\'s entire digital ecosystem',
    
    # Common words and phrases
    'och': 'and',
    'eller': 'or',
    'för': 'for',
    'med': 'with',
    'till': 'to',
    'från': 'from',
    'genom': 'through',
    'inom': 'within',
    'under': 'during',
    'över': 'over',
    'mellan': 'between',
    'enligt': 'according to',
    'utan': 'without',
    'Detta': 'This',
    'Denna': 'This',
    'Dessa': 'These',
    'vilket': 'which',
    'som': 'which',
    'där': 'where',
    'när': 'when',
    'hur': 'how',
    'varför': 'why',
    'vad': 'what',
    
    # Section headings
    'Evolution mot': 'Evolution towards',
    'Definition och omfattning': 'Definition and Scope',
    'Bokens syfte och målgrupp': 'Purpose and Target Audience of the Book',
    'Källor': 'Sources',
    'Referenser': 'References',
    'Sammanfattning': 'Summary',
    'Bakgrund': 'Background',
    'Syfte': 'Purpose',
    'Målgrupp': 'Target Audience',
    'Innehåll': 'Contents',
    'Fördelar': 'Benefits',
    'Nackdelar': 'Disadvantages',
    'Utmaningar': 'Challenges',
    'Rekommendationer': 'Recommendations',
    'Exempel': 'Example',
    'Praktisk implementation': 'Practical Implementation',
    'Nästa steg': 'Next Steps',
    
    # Technical terms (preserve as-is or translate)
    'Arkitektur som kod': 'Architecture as Code',
    'Infrastruktur som kod': 'Infrastructure as Code',
    'Dokumentation som kod': 'Documentation as Code',
    'Krav som kod': 'Requirements as Code',
    'Policy som kod': 'Policy as Code',
    'allt som kod': 'everything as code',
    
    'versionskontroll': 'version control',
    'versionhantering': 'version control',
    'automatisering': 'automation',
    'molnarkitektur': 'cloud architecture',
    'containerisering': 'containerization',
    'orkestrering': 'orchestration',
    'mikrotjänster': 'microservices',
    'säkerhet': 'security',
    'efterlevnad': 'compliance',
    'teststrategier': 'testing strategies',
    'kostnadsoptimering': 'cost optimization',
    'resurshantering': 'resource management',
    'migration': 'migration',
    'organisatorisk förändring': 'organizational change',
    'kulturomställning': 'cultural transformation',
    'digitalisering': 'digitalization',
    'affärsnytta': 'business value',
    'framtida trender': 'future trends',
    'bästa metoder': 'best practices',
    'lärda läxor': 'lessons learned',
}


def translate_text(text: str) -> str:
    """
    Translate Swedish text to English using comprehensive phrase matching.
    Longer phrases are matched first to preserve context.
    """
    result = text
    
    # Sort by length (longest first) to match longer phrases before shorter ones
    sorted_phrases = sorted(PHRASE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for swedish, english in sorted_phrases:
        # Use case-insensitive matching for better coverage
        # But try to preserve the original case when possible
        pattern = re.compile(re.escape(swedish), re.IGNORECASE)
        
        def replace_with_case(match):
            original = match.group(0)
            # If original starts with capital, capitalize replacement
            if original and original[0].isupper():
                return english[0].upper() + english[1:] if english else english
            return english
        
        result = pattern.sub(replace_with_case, result)
    
    return result


def translate_markdown_file(input_path: Path) -> str:
    """
    Translate a Swedish markdown file to English while preserving structure.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    translated_lines = []
    in_code_block = False
    
    for line in lines:
        # Track code blocks - don't translate content inside
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue
        
        if in_code_block:
            translated_lines.append(line)
            continue
        
        # Translate image alt text but preserve path
        if line.strip().startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt_text = translate_text(match.group(1))
                path = match.group(2)
                translated_lines.append(f'![{alt_text}]({path})')
                continue
        
        # Translate the line
        translated_line = translate_text(line)
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)


def main():
    """Translate first chapter as a test"""
    input_file = Path('docs/01_inledning.md')
    output_file = Path('docs/01_inledning_en_auto.md')
    
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return
    
    print(f"Translating {input_file}...")
    translated_content = translate_markdown_file(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"✅ Created {output_file}")
    print("\nFirst 20 lines of translation:")
    print("-" * 60)
    for i, line in enumerate(translated_content.split('\n')[:20], 1):
        print(f"{i:2}. {line}")


if __name__ == '__main__':
    main()
