#!/usr/bin/env python3
"""
Post-process English translations to fix remaining Swedish words and improve quality.
"""

import re
from pathlib import Path
from typing import Dict

# Additional translation mappings for words that were missed
ADDITIONAL_TRANSLATIONS = {
    # Swedish words that need translation
    'bygger på': 'builds on',
    'fundamentala': 'fundamental',
    'principer': 'principles',
    'vilket': 'which',
    'säkerställer': 'ensures',
    'framgångsrik': 'successful',
    'implementation': 'implementation',
    'av': 'of',
    'kodifierad': 'codified',
    'systemarkitektur': 'system architecture',
    'omfattar': 'encompasses',
    'hela': 'entire',
    'systemlandskapet': 'system landscape',
    'skapar': 'creates',
    'en': 'a',
    'helhetssyn': 'holistic view',
    'arkitekturhantering': 'architecture management',
    'visar': 'shows',
    'det': 'the',
    'naturliga': 'natural',
    'flödet': 'flow',
    'versionskontroll': 'version control',
    'automatisering': 'automation',
    'reproducerbarhet': 'reproducibility',
    'skalbarhet': 'scalability',
    'de': 'the',
    'fem': 'five',
    'grundpelarna': 'fundamental pillars',
    'approachen': 'approach',
    'innebär': 'means',
    'att': 'to',
    'beskriva': 'describe',
    'önskat': 'desired',
    'tillstånd': 'state',
    'på': 'at',
    'alla': 'all',
    'nivåer': 'levels',
    'skiljer': 'differs',
    'sig': 'itself',
    'imperativ': 'imperative',
    'programmering': 'programming',
    'varje': 'each',
    'steg': 'step',
    'måste': 'must',
    'specificeras': 'be specified',
    'explicit': 'explicitly',
    'definition': 'definition',
    'möjliggör': 'enables',
    'arkitekturens': 'architecture\'s',
    'önskade': 'desired',
    'utvidgar': 'extends',
    'applikationsarkitektur': 'application architecture',
    'kontrakt': 'contracts',
    'organisatoriska': 'organizational',
    'strukturer': 'structures',
    'systemekosystemet': 'system ecosystem',
    'holistisk': 'holistic',
    'inkluderar': 'includes',
    'applikationslogik': 'application logic',
    'dataflöden': 'data flows',
    'regler': 'rules',
    'organisationsstrukturer': 'organizational structures',
    'praktiskt': 'practical',
    'exempel': 'example',
    'är': 'is',
    'hur': 'how',
    'förändring': 'change',
    'i': 'in',
    'en': 'a',
    'applikations': 'application\'s',
    'automatiskt': 'automatically',
    'kan': 'can',
    'propagera': 'propagate',
    'säkerhetskonfigurationer': 'security configurations',
    'dokumentation': 'documentation',
    'allt': 'all',
    'eftersom': 'as',
    'definierat': 'defined',
    'som': 'as',
    'kod': 'code',
    'om': 'about',
    'immutable': 'immutable',
    'arkitektur': 'architecture',
    'hanteras': 'is managed',
    'oföränderliga': 'immutable',
    'komponenter': 'components',
    'istället': 'instead',
    'modifiera': 'modify',
    'befintliga': 'existing',
    'delar': 'parts',
    'skapas': 'are created',
    'nya': 'new',
    'versioner': 'versions',
    'ersätter': 'replace',
    'gamla': 'old',
    'förutsägbarhet': 'predictability',
    'eliminerar': 'eliminates',
    'architectural drift': 'architectural drift',
    'system': 'systems',
    'gradvis': 'gradually',
    'divergerar': 'diverge',
    'från': 'from',
    'sin': 'their',
    'avsedda': 'intended',
    'design': 'design',
    'över': 'over',
    'tid': 'time',
    'testning': 'testing',
    'inte': 'not',
    'bara': 'only',
    'enskilda': 'individual',
    'validering': 'validation',
    'arkitekturmönster': 'architecture patterns',
    'designprinciper': 'design principles',
    'verifiering': 'verification',
    'flöden': 'flows',
    
    # Common verbs
    'transformerat': 'transformed',
    'tänker': 'think',
    'kring': 'about',
    'behandla': 'treat',
    'möjliggjort': 'enabled',
    'samma': 'same',
    'noggrannhet': 'precision',
    'processer': 'processes',
    'kvalitetskontroller': 'quality controls',
    'länge': 'long',
    'funnits': 'existed',
    'programvaruutveckling': 'software development',
    'resa': 'journey',
    'genom': 'through',
    'kapitel': 'chapters',
    'visat': 'shown',
    'vägen': 'the way',
    'koncept': 'concepts',
    'framtidens': 'future',
    'avancerade': 'advanced',
    'teknologier': 'technologies',
    
    # Nouns
    'lärdomar': 'lessons',
    'implementering': 'implementation',
    'kräver': 'requires',
    'både': 'both',
    'teknisk': 'technical',
    'excellens': 'excellence',
    'framgångsrika': 'successful',
    'transformationer': 'transformations',
    'kännetecknas': 'are characterized',
    'stark': 'strong',
    'ledningsengagemang': 'management commitment',
    'omfattande': 'comprehensive',
    'utbildningsprogram': 'training programs',
    'införandestrategi': 'implementation strategy',
    'minimerar': 'minimizes',
    'störningar': 'disruptions',
    'befintlig': 'existing',
    'verksamhet': 'operations',
    'enligt': 'according to',
    'utforskade': 'explored',
    
    # Additional phrases
    'aspekten': 'aspect',
    'djup': 'deep',
    'förståelse': 'understanding',
    'molnteknologier': 'cloud technologies',
    'automatiseringsverktyg': 'automation tools',
    'säkerhetsprinciper': 'security principles',
    'behandlade': 'covered',
    'samtidigt': 'simultaneously',
    'faktorer': 'factors',
    'ofta': 'often',
    'avgörande': 'crucial',
    'framgång': 'success',
    'inklusive': 'including',
    'kulturell': 'cultural',
    'kompetensutveckling': 'competence development',
    'processtandardisering': 'process standardization',
}


def improve_translation(text: str) -> str:
    """Apply additional translations to improve quality."""
    result = text
    
    # Sort by length (longest first)
    sorted_trans = sorted(
        ADDITIONAL_TRANSLATIONS.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )
    
    for swedish, english in sorted_trans:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(swedish) + r'\b'
        result = re.sub(pattern, english, result, flags=re.IGNORECASE)
    
    # Fix common patterns
    result = re.sub(r'\bwhich\b(?!\s+[a-z])', 'that', result)  # Fix standalone "which"
    result = re.sub(r'\bwith\b\s+\bwith\b', 'with', result)  # Fix duplicates
    result = re.sub(r'\bthe\b\s+\bthe\b', 'the', result)
    result = re.sub(r'\band\b\s+\band\b', 'and', result)
    
    # Fix "for" vs "to" in common patterns
    result = re.sub(r'\bfor\s+att\b', 'to', result)
    
    return result


def process_file(file_path: Path):
    """Process a single English file to improve translation."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Improve translation
        improved = improve_translation(content)
        
        # Only write if changed
        if improved != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(improved)
            return True, f"✅ Improved {file_path.name}"
        else:
            return False, f"⚪ No changes needed for {file_path.name}"
    
    except Exception as e:
        return False, f"❌ Error: {file_path.name}: {e}"


def main():
    """Main post-processing function."""
    print("=" * 70)
    print("🔧 Post-Processing English Translations")
    print("=" * 70)
    print()
    
    # Find all English files
    en_files = []
    
    # Root level
    for path in Path('.').glob('*_en.md'):
        en_files.append(path)
    
    # Docs directory
    docs_dir = Path('docs')
    if docs_dir.exists():
        for path in docs_dir.glob('*_en.md'):
            en_files.append(path)
    
    print(f"Found {len(en_files)} English files to process\n")
    
    improved_count = 0
    unchanged_count = 0
    
    for file_path in sorted(en_files):
        changed, message = process_file(file_path)
        print(message)
        if changed:
            improved_count += 1
        else:
            unchanged_count += 1
    
    print()
    print("=" * 70)
    print("📊 Post-Processing Summary")
    print("=" * 70)
    print(f"✅ Improved: {improved_count}")
    print(f"⚪ Unchanged: {unchanged_count}")
    print()
    print("✨ Post-processing complete!")


if __name__ == '__main__':
    main()
