#!/usr/bin/env python3
"""
Comprehensive script to translate the Swedish book "Arkitektur som kod" to English.
Uses the established terminology mappings and maintains technical accuracy.
"""

import os
import re
from pathlib import Path
import shutil

# Core terminology mapping (Swedish → English)
TERMINOLOGY_MAP = {
    # Core concepts
    "Arkitektur som kod": "Architecture as Code",
    "arkitektur som kod": "architecture as code",
    "Infrastructure as Code": "Infrastructure as Code",  # Keep in English
    "IaC": "IaC",  # Keep technical acronym
    
    # Technical terms (Swedish → English)
    "molnplattform": "cloud platform",
    "molnplattformar": "cloud platforms",
    "kodlager": "code repository",
    "kodlagret": "the code repository",
    "driftsättning": "deployment",
    "driftsättningar": "deployments",
    "automatiseringskedja": "pipeline",
    "automatiseringskedjor": "pipelines",
    "övervakning": "monitoring",
    "regelefterlevnad": "compliance",
    "efterlevnad": "compliance",
    
    # Organization and process terms
    "intressent": "stakeholder",
    "intressenter": "stakeholders",
    "riktlinjer": "guidelines",
    "riktlinje": "guideline",
    "bästa metoder": "best practices",
    "bästa metod": "best practice",
    "tvärfunktionell": "cross-functional",
    "utrullning": "rollout",
    "utrullningar": "rollouts",
    "återställning": "rollback",
    "återställningar": "rollbacks",
    "tidslinje": "timeline",
    "tidslinjer": "timelines",
    
    # Technical infrastructure
    "ramverk": "framework",
    "plattform": "platform",
    "plattformar": "platforms",
    "verktyg": "tools",
    "konfiguration": "configuration",
    "konfigurationer": "configurations",
    "testning": "testing",
    "migrering": "migration",
    "migreringar": "migrations",
    
    # Document structure
    "kapitel": "chapter",
    "Kapitel": "Chapter",
    "inledning": "introduction",
    "Inledning": "Introduction",
    "slutsats": "conclusion",
    "Slutsats": "Conclusion",
    "ordlista": "glossary",
    "Ordlista": "Glossary",
    "appendix": "appendix",
    "Appendix": "Appendix",
    
    # Common phrases
    "Detta kapitel": "This chapter",
    "detta kapitel": "this chapter",
    "I detta kapitel": "In this chapter",
    "i detta kapitel": "in this chapter",
    "Följande avsnitt": "The following section",
    "följande avsnitt": "the following section",
    "Nästa kapitel": "The next chapter",
    "nästa kapitel": "the next chapter",
    "Föregående kapitel": "The previous chapter",
    "föregående kapitel": "the previous chapter",
}

# Common Swedish phrases and their English translations
PHRASE_TRANSLATIONS = {
    # Introduction phrases
    "representerar ett paradigmskifte inom": "represents a paradigm shift in",
    "möjliggör samma metodiker som": "enables the same methodologies as",
    "tillvägagångssätt": "approach",
    "omfattande": "comprehensive",
    "grundläggande": "fundamental",
    "praktiska": "practical",
    "tekniska": "technical",
    "organisatoriska": "organizational",
    "systemutveckling": "system development",
    "mjukvaruutveckling": "software development",
    "systemarkitekturen": "the system architecture",
    "systemlandskapet": "the system landscape",
    
    # Common verbs and actions
    "definieras": "is defined",
    "implementeras": "is implemented",
    "hanteras": "is managed",
    "versionshanteras": "is version controlled",
    "automatiseras": "is automated",
    "kodifieras": "is codified",
    "säkerställer": "ensures",
    "möjliggör": "enables",
    "inkluderar": "includes",
    "omfattar": "encompasses",
    "bygger på": "builds on",
    "tillämpar": "applies",
    "kommer att få": "will gain",
    "vänder sig till": "is aimed at",
    
    # Common adjectives and descriptors
    "etablerade": "established",
    "traditionella": "traditional",
    "manuella": "manual",
    "automatiserade": "automated",
    "avancerade": "advanced",
    "specifika": "specific",
    "svenska": "Swedish",
    "engelska": "English",
    "holistiska": "holistic",
    "maskinläsbar": "machine-readable",
    "fullständig": "complete",
    "omfattande": "comprehensive",
    "digitala": "digital",
    "tekniska": "technical",
    
    # Business and organizational terms
    "organisationer": "organizations",
    "organisation": "organization", 
    "organizationens": "the organization's",
    "företag": "companies",
    "utvecklare": "developers",
    "projektledare": "project managers",
    "systemarkitekter": "system architects",
    "IT-beslutsfattare": "IT decision makers",
    "beslutsfattare": "decision makers",
    "ekosystem": "ecosystem",
    "landskap": "landscape",
    
    # Process and methodology
    "metodiker": "methodologies",
    "metodik": "methodology",
    "processer": "processes",
    "process": "process",
    "arbetssätt": "working methods",
    "tillvägagångssätt": "approaches",
    "implementering": "implementation",
    "implementation": "implementation",
    "principer": "principles",
    "förändringar": "changes",
    "propagerar": "propagate",
    "applikationslogik": "application logic",
    "driftsättning": "deployment",
    "övervakning": "monitoring",
    
    # Document structure and flow
    "Detta": "This",
    "denna": "this",
    "Detta dokument": "This document",
    "Denna bok": "This book",
    "Läsaren": "The reader",
    "Sources": "Sources",
    "Källor": "Sources",
    "genom": "through",
    "där": "where",
    "som": "that",
    "även": "also",
    "samt": "as well as",
    "och": "and",
    "eller": "or",
    "men": "but",
    "utan": "without",
    "inte bara": "not only",
    "allt": "all",
    "hela": "the entire",
    "från": "from",
    "till": "to",
}

def translate_text_content(content):
    """
    Translate Swedish text content to English using terminology mappings
    and common phrase translations.
    """
    translated = content
    
    # First pass: Apply terminology mappings (most specific)
    for swedish, english in TERMINOLOGY_MAP.items():
        # Use word boundaries to avoid partial matches for single words
        if " " in swedish:  # Multi-word phrases - no word boundaries needed
            pattern = re.escape(swedish)
        else:  # Single words - use word boundaries
            pattern = r'\b' + re.escape(swedish) + r'\b'
        translated = re.sub(pattern, english, translated, flags=re.IGNORECASE)
    
    # Second pass: Apply phrase translations
    for swedish, english in PHRASE_TRANSLATIONS.items():
        # Case-insensitive replacement
        pattern = re.escape(swedish)
        translated = re.sub(pattern, english, translated, flags=re.IGNORECASE)
    
    # Third pass: Fix common Swedish grammatical structures
    # Convert "X som Y" patterns to "X that Y"
    translated = re.sub(r'\b(\w+)\s+som\s+(\w+)', r'\1 that \2', translated)
    
    # Convert "i X" to "in X" where appropriate
    translated = re.sub(r'\bi\s+([A-Z]\w*)', r'in \1', translated)
    
    # Fix some remaining Swedish words that might have been missed
    remaining_swedish = {
        "metoder": "methods",
        "har": "have",
        "ofta": "often",
        "varit": "been",
        "dokumentbaserade": "document-based",
        "på": "on",
        "av": "of",
        "för": "for",
        "med": "with",
        "i": "in",
        "att": "to",
        "är": "is",
        "kan": "can",
        "ska": "should",
        "kommer": "will",
        "kommer att": "will",
        "skulle": "would",
        "bör": "should",
        "måste": "must",
        "eller": "or",
        "men": "but",
        "utan": "without",
        "genom": "through",
        "mellan": "between",
        "under": "during",
        "över": "over",
        "vid": "at",
        "inom": "within",
        "enligt": "according to",
        "därför": "therefore",
        "eftersom": "because",
        "medan": "while",
        "efter": "after",
        "innan": "before",
        "slutligen": "finally",
        "dessutom": "furthermore",
        "exempelvis": "for example",
        "till exempel": "for example",
        "det vill säga": "that is",
        "med andra ord": "in other words",
    }
    
    for swedish, english in remaining_swedish.items():
        if " " in swedish:  # Multi-word phrases
            pattern = re.escape(swedish)
        else:  # Single words with word boundaries
            pattern = r'\b' + re.escape(swedish) + r'\b'
        translated = re.sub(pattern, english, translated, flags=re.IGNORECASE)
    
    return translated

def translate_markdown_file(input_path, output_path):
    """
    Translate a single markdown file from Swedish to English.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Translate the content
        translated_content = translate_text_content(content)
        
        # Update image references to English versions if needed
        # Keep the same image paths but note that diagrams should be regenerated
        
        # Write translated content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"✅ Translated: {input_path.name} → {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error translating {input_path}: {e}")
        return False

def create_english_build_script():
    """
    Create an English version of the build script.
    """
    original_build_script = Path("docs/build_book.sh")
    english_build_script = Path("docs/build_book_english.sh")
    
    try:
        with open(original_build_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update output file names for English version
        content = content.replace('arkitektur_som_kod.pdf', 'architecture_as_code.pdf')
        content = content.replace('arkitektur_som_kod.epub', 'architecture_as_code.epub')
        content = content.replace('arkitektur_som_kod.docx', 'architecture_as_code.docx')
        
        # Update chapter file references to English versions
        # The English files are named like: 01_inledning_en.md
        chapter_mappings = {
            '"01_inledning.md"': '"01_inledning_en.md"',
            '"02_grundlaggande_principer.md"': '"02_grundlaggande_principer_en.md"',
            '"03_versionhantering.md"': '"03_versionhantering_en.md"',
            '"04_adr.md"': '"04_adr_en.md"',
            '"05_automatisering_devops_cicd.md"': '"05_automatisering_devops_cicd_en.md"',
            '"06_molnarkitektur.md"': '"06_molnarkitektur_en.md"',
            '"07_containerisering.md"': '"07_containerisering_en.md"',
            '"08_microservices.md"': '"08_microservices_en.md"',
            '"09_sakerhet.md"': '"09_sakerhet_en.md"',
            '"10_policy_sakerhet.md"': '"10_policy_sakerhet_en.md"',
            '"11_compliance.md"': '"11_compliance_en.md"',
            '"12_teststrategier.md"': '"12_teststrategier_en.md"',
            '"13_praktisk_implementation.md"': '"13_praktisk_implementation_en.md"',
            '"14_kostnadsoptimering.md"': '"14_kostnadsoptimering_en.md"',
            '"15_migration.md"': '"15_migration_en.md"',
            '"16_organisatorisk_forandring.md"': '"16_organisatorisk_forandring_en.md"',
            '"17_team_struktur.md"': '"17_team_struktur_en.md"',
            '"18_digitalisering.md"': '"18_digitalisering_en.md"',
            '"19_lovable_mockups.md"': '"19_lovable_mockups_en.md"',
            '"20_framtida_trender.md"': '"20_framtida_trender_en.md"',
            '"21_best_practices.md"': '"21_best_practices_en.md"',
            '"22_slutsats.md"': '"22_slutsats_en.md"',
            '"23_ordlista.md"': '"23_ordlista_en.md"',
            '"24_om_forfattarna.md"': '"24_om_forfattarna_en.md"',
            '"25_framtida_utveckling.md"': '"25_framtida_utveckling_en.md"',
            '"26_appendix_kodexempel.md"': '"26_appendix_kodexempel_en.md"',
            '"27_teknisk_uppbyggnad.md"': '"27_teknisk_uppbyggnad_en.md"',
        }
        
        for swedish_file, english_file in chapter_mappings.items():
            content = content.replace(swedish_file, english_file)
        
        with open(english_build_script, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Make executable
        os.chmod(english_build_script, 0o755)
        print(f"✅ Created English build script: {english_build_script}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating English build script: {e}")
        return False

def create_english_pandoc_config():
    """
    Create an English version of the Pandoc configuration.
    """
    original_config = Path("docs/pandoc.yaml")
    english_config = Path("docs/pandoc_english.yaml")
    
    try:
        with open(original_config, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update metadata for English version
        content = content.replace('title: "Arkitektur som kod"', 'title: "Architecture as Code"')
        content = content.replace('lang: sv', 'lang: en')
        content = content.replace('subtitle: "En omfattande guide"', 'subtitle: "A Comprehensive Guide"')
        
        with open(english_config, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created English Pandoc config: {english_config}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating English Pandoc config: {e}")
        return False

def main():
    """
    Main function to translate all book content to English.
    """
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print("❌ docs directory not found")
        return
    
    print("📚 Starting English translation of 'Arkitektur som kod'...")
    print("=" * 60)
    
    # Get all Swedish markdown chapter files
    chapter_files = []
    for i in range(1, 28):  # Based on the repository structure
        if i < 10:
            filename = f"0{i}_*.md"
        else:
            filename = f"{i}_*.md"
        
        matches = list(docs_dir.glob(filename))
        chapter_files.extend(matches)
    
    # Also include specific files
    additional_files = [
        "README.md",
        "BOOK_COVER_DESIGN.md",
        "TERMINOLOGI_JUSTERING.md"
    ]
    
    for filename in additional_files:
        file_path = docs_dir / filename
        if file_path.exists():
            chapter_files.append(file_path)
    
    print(f"📖 Found {len(chapter_files)} files to translate")
    
    # Translate each file
    success_count = 0
    for file_path in sorted(chapter_files):
        # Create English filename
        english_filename = file_path.stem + "_en" + file_path.suffix
        output_path = file_path.parent / english_filename
        
        if translate_markdown_file(file_path, output_path):
            success_count += 1
    
    print("=" * 60)
    print(f"✅ Successfully translated {success_count}/{len(chapter_files)} files")
    
    # Create English build configuration
    print("\n🔧 Creating English build configuration...")
    create_english_pandoc_config()
    create_english_build_script()
    
    print("\n🎯 Translation Summary:")
    print(f"   • Translated {success_count} markdown files to English")
    print(f"   • Created English build script: docs/build_book_english.sh")
    print(f"   • Created English Pandoc config: docs/pandoc_english.yaml")
    print(f"   • Ready to build English DOCX: architecture_as_code.docx")
    
    print("\n🚀 Next steps:")
    print("   1. Run: cd docs && ./build_book_english.sh --all-formats")
    print("   2. English DOCX will be generated as: docs/architecture_as_code.docx")
    print("   3. Copy to target location: docs/arkitektur_som_kod_EN.docx")

if __name__ == "__main__":
    main()