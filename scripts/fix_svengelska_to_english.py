#!/usr/bin/env python3
"""
Script to fix "svengelska" (Swedish-English mixed) expressions in documentation
and convert them to proper English.

This script identifies and replaces common Svengelska patterns with proper English.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Comprehensive Svengelska to English translation dictionary
# Order matters - longer phrases first for better matching
SVENGELSKA_TO_ENGLISH = {
    # Common problematic patterns - Swedish words mixed in English text
    r'\bwhich\s+code\b': 'as code',
    r'\bwhich\s+a\b': 'as a',
    r'\bwhich\s+an\b': 'as an',
    r'\bwhich\s+the\b': 'as the',
    r'\b(\w+)\s+which\s+(\w+)\b': r'\1 as \2',  # Generic "which" -> "as" pattern
    
    # Swedish article remnants
    r'\bDen\s+': 'The ',
    r'\bDet\s+': 'The ',
    r'\bEtt\s+': 'A ',
    r'\bEn\s+': 'A ',
    r'\bdiagrammet\s+': 'diagram ',
    r'\bThe\s+diagram\s+shows\b': 'The diagram shows',
    r'\bDiagrammet\s+shows\b': 'The diagram shows',
    r'\bDiagrammet\s+visar\b': 'The diagram shows',
    
    # Common Swedish words in English context
    r'\bGrundläggande\b': 'Fundamental',
    r'\bgrundläggande\b': 'fundamental',
    r'\bprinciper\b': 'principles',
    r'\bprincip\b': 'principle',
    r'\bprinciples\s+diagram\b': 'principles diagram',
    
    # Mixed verb forms
    r'\bdeklarativ\b': 'declarative',
    r'\barkitekturdefinition\b': 'architecture definition',
    r'\bapproach\s+within\b': 'approach in',
    r'\bsystemtostånd\b': 'system state',
    r'\bsystemtillstånd\b': 'system state',
    r'\bapplikationskomponenter\b': 'application components',
    r'\binf raStructure\b': 'infrastructure',
    r'\binfraStructure\b': 'infrastructure',
    r'\btostånd\b': 'state',
    r'\btillstånd\b': 'state',
    r'\bomfatta\b': 'encompass',
    r'\befterwhich\s+the\s+is\b': 'that is',
    r'\beftersom\s+den\s+är\b': 'since it is',
    r'\bwhich\s+avsett\b': 'as intended',
    r'\bsom\s+avsett\b': 'as intended',
    
    # Swedish words that appear in English text
    r'\bStructureer\b': 'structures',
    r'\bStructure\b': 'structure',
    r'\bforändringar\b': 'changes',
    r'\bforändring\b': 'change',
    r'\bförändring\b': 'change',
    r'\bgenomföra\b': 'implement',
    r'\bgenomgång\b': 'review',
    r'\bimplementering\b': 'implementation',
    r'\bsäkerhetspolicies\b': 'security policies',
    r'\bsäkerhetsaspekter\b': 'security aspects',
    r'\barkitekturen\b': 'architecture',
    r'\barkitekturnivå\b': 'architecture level',
    r'\bsystemarkitekturen\b': 'system architecture',
    r'\barkitekturmönster\b': 'architecture patterns',
    r'\barkitekturpatterns\b': 'architecture patterns',
    r'\barkitekturbeslut\b': 'architecture decisions',
    r'\bdesignbeslut\b': 'design decisions',
    r'\bsystemkomplexitet\b': 'system complexity',
    r'\bendto-end-flows\b': 'end-to-end flows',
    r'\bend-to-end-flows\b': 'end-to-end flows',
    
    # Mixed sentences with Swedish grammar
    r'\bwhich\s+ensures\b': 'that ensures',
    r'\bencompasses\s+entire\b': 'encompasses the entire',
    r'\bcreates\s+a\s+holistic\b': 'creates a holistic',
    r'\bmeans\s+to\s+describe\b': 'means describing',
    r'\bto\s+describe\s+desired\b': 'describing the desired',
    r'\bThis\s+differs\s+itself\b': 'This differs',
    r'\benables\s+to\s+describe\b': 'enables describing',
    r'\bextends\s+to\s+to\b': 'extends to',
    r'\bmeans\s+to\s+entire\b': 'means the entire',
    r'\bis\s+managed\s+through\s+oforänderliga\b': 'is managed through immutable',
    r'\bfor\s+to\s+modify\b': 'to modify',
    r'\bfor\s+to\s+ge\b': 'to provide',
    r'\binstead\s+for\s+to\b': 'instead of',
    r'\bensures\s+to\s+entire\b': 'ensures the entire',
    r'\bensures\s+to\s+(\w+)\b': r'ensures \1',
    r'\bfungerar\s+which\s+avsett\b': 'functions as intended',
    r'\brepresenterar\s+principen\s+to\b': 'represents the principle of',
    r'\brepresenterar\s+principen\b': 'represents the principle',
    r'\bto\s+treat\b': 'treating',
    r'\bwhich\s+a\s+integrerad\s+del\b': 'as an integrated part',
    r'\bsnarare\s+än\s+which\s+ett\s+separat\b': 'rather than as a separate',
    r'\blagras\s+tosammans\s+with\b': 'stored together with',
    r'\bversionshanteras\s+with\s+same\b': 'version-controlled with the same',
    r'\bthroughgår\s+same\b': 'undergoes the same',
    r'\bwhich\s+applikationskoden\b': 'as the application code',
    
    # Common Swedish prepositions and articles mixed with English
    r'\bthrough\s+to\s+(\w+)\b': r'by \1',
    r'\bfor\s+to\s+(\w+)\b': r'to \1',
    r'\bat\s+all\s+levels\b': 'at all levels',
    r'\bat\s+(\w+)nivå\b': r'at \1 level',
    r'\bin\s+Git\s+or\s+andra\b': 'in Git or other',
    r'\bfår\s+organisationer\b': 'organizations get',
    r'\bautomatisk\s+spårbarhet\s+of\b': 'automatic traceability of',
    r'\bmöjlighet\s+to\s+återställa\b': 'ability to restore',
    r'\bprevious\s+versions\s+and\s+full\s+historik\s+over\b': 'previous versions and full history of',
    r'\bdokumentationens\s+utveckling\b': "documentation's development",
    r'\bmerge-processes\s+ensures\s+to\b': 'merge processes ensure that',
    r'\bdokumentationsändringar\s+granskas\s+innan\s+the\s+publiceras\b': 'documentation changes are reviewed before being published',
    r'\bförbättrar\s+kvaliteten\s+and\s+minskar\b': 'improves quality and reduces',
    r'\brisken\s+for\s+felaktig\s+or\s+föråldrad\b': 'the risk of incorrect or outdated',
    r'\bAutomatiserade\s+pipelines\s+can\b': 'Automated pipelines can',
    r'\bgenerera,\s+validera\s+and\s+publicera\b': 'generate, validate and publish',
    r'\bwhen\s+code\s+forändras\b': 'when code changes',
    r'\bThis\s+eliminates\s+manuella\s+step\b': 'This eliminates manual steps',
    r'\baltid\s+is\s+uppdaterad\b': 'always up-to-date',
    
    # Organizations and structure words
    r'\borganisationsStructureer\b': 'organizational structures',
    r'\borganisationsStructure\b': 'organizational structure',
    r'\borganisatoriska\s+strukturer\b': 'organizational structures',
    r'\bkomplexitet\s+and\b': 'complexity and',
    
    # Technical terms with Swedish endings
    r'\bkodbasen\b': 'codebase',
    r'\bverktyg\s+and\b': 'tools and',
    r'\bkvalitetssäkringsprocesser\b': 'quality assurance processes',
    r'\bversionskontrollsystem\b': 'version control systems',
    r'\bversion control\s+and\s+historik\b': 'version control and history',
    r'\bCollaboration\s+and\s+granskning\b': 'Collaboration and review',
    r'\bKollaboration\s+and\s+granskning\b': 'Collaboration and review',
    r'\bCI/CD-integration\b': 'CI/CD integration',
    
    # Documentation specific
    r'\bDokument\s+beskriver\b': 'Document describes',
    r'\bdokument\s+definierar\b': 'document defines',
    r'\bdokument\s+beskriver\b': 'document describes',
    r'\bÖversikt\b': 'Overview',
    r'\bBeskrivning\b': 'Description',
    r'\bbeskriver\s+den\s+logiska\b': 'describes the logical',
    r'\bwhich\s+is\s+organiserad\s+in\b': 'which is organized in',
    r'\bwhich\s+builds\s+on\s+varandra\s+for\s+to\s+ge\b': 'that build on each other to provide',
    r'\bkomplett\s+forståelse\s+of\b': 'complete understanding of',
    r'\bfor\s+svenska\s+organisationer\b': 'for Swedish organizations',
    
    # Chapter and section  
    r'\bKapitelstruktur\b': 'Chapter Structure',
    r'\bkapitel\s+(\d+)\b': r'chapter \1',
    r'\bKapitel\s+(\d+)\b': r'Chapter \1',
    r'\bDel\s+(\d+):\s+Grunder\s+and\s+fundamental\s+concepts\b': r'Part \1: Fundamentals and Core Concepts',
    r'\bDel\s+(\d+):\s+Kärnimplementering\b': r'Part \1: Core Implementation',
    r'\bDel\s+(\d+):\s+Security\s+and\s+compliance\b': r'Part \1: Security and Compliance',
    r'\bGrunder\s+and\s+fundamental\s+concepts\b': 'Fundamentals and Core Concepts',
    r'\bFundamental\s+concepts\b': 'Fundamental Concepts',
    
    # Table headers
    r'\bchapters\s+\|\s+Fil\s+\|\s+Titel\s+\|\s+Beskrivning\b': 'Chapter | File | Title | Description',
    r'\bKapitel\s+\|\s+Fil\s+\|\s+Titel\s+\|\s+Beskrivning\b': 'Chapter | File | Title | Description',
    
    # Common Swedish words that slip through
    r'\bIntroduktion\s+to\s+konceptet\b': 'Introduction to the concept',
    r'\band\s+dess\s+relation\s+to\b': 'and its relation to',
    r'\bfundamental\s+principles\s+which\s+deklarativ\b': 'fundamental principles like declarative',
    r'\bBest\s+practices\s+for\s+versionshantering\s+of\b': 'Best practices for version control of',
    r'\barkitekturkod\b': 'architecture code',
    r'\bStructureerad\s+documentation\s+of\b': 'Structured documentation of',
    r'\bHolistic\s+approach\s+to\b': 'Holistic approach to',
    r'\bCI/CD-praktiker\s+and\b': 'CI/CD practices and',
    r'\bDevOps-praktiker\s+and\b': 'DevOps practices and',
    r'\bIaC\s+in\s+molnmiljöer\b': 'IaC in cloud environments',
    r'\bCloudnativ\s+architecture\s+and\b': 'Cloud-native architecture and',
    r'\bContainer-baserad\b': 'Container-based',
    r'\bMicroservices-mönster\s+implementerat\s+through\b': 'Microservices patterns implemented through',
    r'\bSäkerhetsaspekter\s+and\s+best\s+practices\b': 'Security aspects and best practices',
    r'\bSäkerhet\s+in\b': 'Security in',
    r'\bDetaljerad\s+throughgång\s+of\b': 'Detailed review of',
    
    # File and technical terms  
    r'\bFil\b': 'File',
    r'\bTitel\b': 'Title',
    r'\bBeskrivning\b': 'Description',
    r'\bKapitel\b': 'Chapter',
    r'\bchapters\s+(\d+)-(\d+)\b': r'chapters \1-\2',
    
    # Common misspellings and artifacts
    r'\bwhichium\b': 'medium',
    r'\bWithium\b': 'Medium',
    r'\bwithia\b': 'media',
    r'\bKwhatrat\b': 'Kvadrat',
    r'\bwhich_kod\b': 'som_kod',
    
    # Remaining Swedish fragments
    r'\bforutsägbarhet\b': 'predictability',
    r'\bimplementerad\b': 'implemented',
    r'\bvaliderar\b': 'validates',
    r'\bensures\b': 'ensures',
    r'\bvalidera\b': 'validate',
    r'\bkvaliteten\b': 'quality',
    r'\bpubliceras\b': 'published',
    r'\beliminate\b': 'eliminate',
    r'\beliminar\b': 'eliminates',
    
    # Fix "systems" vs "system"
    r'\bsystems architects\b': 'system architects',
    r'\bsystems architecture\b': 'system architecture',
    r'\bsystems development\b': 'system development',
    r'\bsystems landscape\b': 'system landscape',
    r'\bsystems ecosystem\b': 'system ecosystem',
    
    # Additional Swedish words that appear in text
    r'\bdeklarativa\b': 'declarative',
    r'\bdeklarativ\b': 'declarative',
    r'\bHelhetsperspektiv\s+at\s+kodifiering\b': 'Holistic perspective on codification',
    r'\bat\s+kodifiering\b': 'on codification',
    r'\bPrincipen\s+about\b': 'The principle of',
    r'\bPrincip\s+about\b': 'Principle of',
    r'\bTestbarhet\s+at\s+architecture\s+level\b': 'Testability at architecture level',
    r'\bTestbarhet\s+at\b': 'Testability at',
    r'\bArkitekturtester\b': 'Architecture tests',
    r'\bfungerar\b': 'functions',
    r'\bavsett\b': 'intended',
    r'\bintegrerad\s+del\b': 'integrated part',
    r'\bintegrerad\b': 'integrated',
    r'\bsnarare\s+än\b': 'rather than',
    r'\bseparat\s+artefakt\b': 'separate artifact',
    r'\bkoden\b': 'the code',
    r'\bapplikationskoden\b': 'the application code',
    r'\blagra\b': 'store',
    r'\btidigare\s+versions\b': 'previous versions',
    r'\btidigare\b': 'previous',
    r'\bhistorik\s+over\b': 'history of',
    r'\bhistorik\b': 'history',
    
    # Grammar fixes
    r'\bmeans to documentation\b': 'means that documentation',
    r'\bby store documentation\b': 'by storing documentation',
    r'\bmeans describing the desired\b': 'means describing the desired',
    r'\bas a integrated\b': 'as an integrated',
    r'\bas A separate\b': 'as a separate',
    r'\benables describing\b': 'enables describing',
    r'\bthat ensures\b': 'that ensure',  # plural form for "principles that ensure"
    r'\bprinciples that ensures\b': 'principles that ensure',
    r'\bThese principles encompasses\b': 'These principles encompass',
    r'\band creates a\b': 'and create a',
    r'\bprinciples that ensure.*and creates\b': 'principles that ensure',  # Fix compound predicate
    r'\bcan propagate\b': 'can propagate',
    r'\binstead of modifying existing parts new\b': 'instead of modifying existing parts, new',
    r'\ball of as is defined\b': 'all of which is defined',
    r'\bvalidates design\b': 'validate design',  # plural subject
    r'\bArchitecture tests validates\b': 'Architecture tests validate',
    r'\bensures dokumentationen\b': 'ensures the documentation',
    r'\bensures the entire architecture functions\b': 'ensures the entire architecture functions',
    r'\bensures that documentation\b': 'ensures that documentation',
    r'\bensures documentation\b': 'ensures documentation',
    r'\bis stored\b': 'is stored',
    r'\bthat documentation stored\b': 'that documentation is stored',
    r'\bforbättrar quality\b': 'improves quality',
    r'\bminskar risken for\b': 'reduces the risk of',
    r'\bfelaktig or foråldrad\b': 'incorrect or outdated',
    r'\bdokumentationen alltid is\b': 'the documentation is always',
    r'\baltid is\b': 'is always',
    r'\buppdaterad\b': 'up-to-date',
    r'\bforbättrar\b': 'improves',
    r'\bminskar\b': 'reduces',
    r'\brisken for\b': 'the risk of',
    r'\bfelaktig\b': 'incorrect',
    r'\bforåldrad\b': 'outdated',
    r'\balltid is\b': 'is always',
    r'\balltid\b': 'always',
    
    # Sentence patterns with Swedish grammar
    r'\bas\s+ensures\b': 'that ensures',
    r'\bprinciples\s+as\s+ensures\b': 'principles that ensure',
    r'\bencompasses\s+the\s+entire\s+system\s+landscape\b': 'encompasses the entire system landscape',
    r'\bcreates\s+a\s+holistic\s+view\s+for\b': 'creates a holistic view of',
    r'\bthe\s+desired\s+system\s+state\b': 'the desired system state',
    r'\bmeans\s+describing\b': 'means describing',
    r'\bdescribing\s+desired\b': 'describing the desired',
    r'\bextends\s+to\s+encompass\b': 'extends to encompass',
    r'\borganizational\s+Structures\b': 'organizational structures',
    r'\bpractical\s+Example\b': 'practical example',
    r'\bA\s+practical\s+example\b': 'A practical example',
    r'\ba\s+change\s+in\s+a\s+application\b': 'a change in an application',
    r'\bthrough\s+entire\s+architecture\b': 'through the entire architecture',
    r'\ball\s+that\s+is\s+defined\s+as\s+code\b': 'all of which is defined as code',
    r'\bthe\s+entire\s+system\s+architecture\b': 'the entire system architecture',
    r'\bthrough\s+immutable\s+components\b': 'through immutable components',
    r'\binstead\s+to\s+modify\b': 'instead of modifying',
    r'\bare\s+created\s+new\s+versions\b': 'new versions are created',
    r'\bas\s+replace\s+old\b': 'that replace old ones',
    r'\bat\s+all\s+levels\b': 'at all levels',
    r'\bthe\s+entire\s+architecture\b': 'the entire architecture',
    r'\bof\s+treat\s+documentation\b': 'of treating documentation',
    r'\bstored\s+together\s+with\b': 'stored together with',
    r'\bversion-controlled\s+with\s+the\s+same\b': 'version-controlled using the same',
    r'\bundergoes\s+the\s+same\b': 'undergoes the same',
    r'\borganizations\s+get\s+automatic\b': 'organizations get automatic',
    r'\bability\s+to\s+restore\b': 'ability to restore',
}

def fix_svengelska_in_text(text: str) -> Tuple[str, List[str]]:
    """
    Fix Svengelska patterns in text and return fixed text and list of changes.
    
    Args:
        text: The text content to fix
        
    Returns:
        Tuple of (fixed_text, list_of_changes)
    """
    fixed_text = text
    changes = []
    
    # Apply replacements in order (longest matches first due to dict order)
    for pattern, replacement in SVENGELSKA_TO_ENGLISH.items():
        matches = list(re.finditer(pattern, fixed_text, re.IGNORECASE | re.MULTILINE))
        
        for match in reversed(matches):  # Reverse to maintain string positions
            original = match.group()
            
            # Apply the replacement
            if r'\1' in replacement or r'\2' in replacement:
                # Pattern with capture groups
                new_text = re.sub(pattern, replacement, original, flags=re.IGNORECASE)
            else:
                # Simple replacement - preserve case
                if original.isupper():
                    new_text = replacement.upper()
                elif original[0].isupper():
                    new_text = replacement[0].upper() + replacement[1:]
                else:
                    new_text = replacement
            
            if original != new_text:
                fixed_text = fixed_text[:match.start()] + new_text + fixed_text[match.end():]
                changes.append(f"{original} → {new_text}")
    
    return fixed_text, changes

def process_markdown_file(file_path: Path) -> Tuple[bool, int]:
    """
    Process a single markdown file and fix Svengelska.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Tuple of (was_modified, number_of_changes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content, changes = fix_svengelska_in_text(original_content)
        
        if fixed_content != original_content:
            # Write back the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"✅ {file_path.relative_to(Path.cwd())}: {len(changes)} fixes")
            # Show first 10 changes
            for change in changes[:10]:
                print(f"   • {change}")
            if len(changes) > 10:
                print(f"   ... and {len(changes) - 10} more changes")
            
            return True, len(changes)
        else:
            print(f"⚪ {file_path.relative_to(Path.cwd())}: No Svengelska found")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False, 0

def main():
    """Main function to process all markdown files."""
    base_path = Path.cwd()
    
    # Find all markdown files
    markdown_files = []
    
    # Root level markdown files (excluding some meta files)
    exclude_files = {
        'ENGLISH_MIGRATION_SUMMARY.md',
        'TRANSLATION_COMPLETION_SUMMARY.md',
        'TRANSLATION_PROJECT.md',
        '.github/copilot-instructions.md'
    }
    
    for md_file in base_path.glob('*.md'):
        if md_file.name not in exclude_files:
            markdown_files.append(md_file)
    
    # docs/ directory
    docs_dir = base_path / 'docs'
    if docs_dir.exists():
        markdown_files.extend(docs_dir.glob('*.md'))
    
    # exports/ directory
    exports_dir = base_path / 'exports'
    if exports_dir.exists():
        markdown_files.extend(exports_dir.rglob('*.md'))
    
    # releases/ directory
    releases_dir = base_path / 'releases'
    if releases_dir.exists():
        markdown_files.extend(releases_dir.glob('*.md'))
    
    # tests/ directory
    tests_dir = base_path / 'tests'
    if tests_dir.exists():
        markdown_files.extend(tests_dir.glob('*.md'))
    
    print("=" * 80)
    print(f"🔧 Fixing Svengelska in {len(markdown_files)} markdown files")
    print("=" * 80)
    print()
    
    total_modified = 0
    total_changes = 0
    
    for file_path in sorted(markdown_files):
        was_modified, num_changes = process_markdown_file(file_path)
        if was_modified:
            total_modified += 1
            total_changes += num_changes
        print()
    
    print("=" * 80)
    print(f"✨ Svengelska fix completed!")
    print(f"📊 Modified {total_modified} files with {total_changes} total changes")
    print("=" * 80)

if __name__ == "__main__":
    main()
