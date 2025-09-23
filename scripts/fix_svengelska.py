#!/usr/bin/env python3
"""
Script to fix "svengelska" (Swedish-English mixed) expressions in documentation.
Technical terms remain in English, but ordinary language is translated to Swedish.
"""

import os
import re
from pathlib import Path

# Define replacements for common svengelska patterns
SVENGELSKA_REPLACEMENTS = {
    # Verb forms - Swedish infinitive + -a ending
    r'\bimplementera\b': 'implementera',  # Already correct
    r'\bdeplooya\b': 'distribuera',
    r'\bdeploya\b': 'distribuera', 
    r'\bmerga\b': 'sammanslå',
    r'\bpusha\b': 'skicka upp',
    r'\bcommita\b': 'checka in',
    r'\bsetuppa\b': 'konfigurera',
    r'\breleasa\b': 'släppa',
    r'\bbygga\b': 'bygga',  # Already correct Swedish
    r'\btesta\b': 'testa',  # Already correct Swedish
    r'\bköra\b': 'köra',    # Already correct Swedish
    r'\bexekvera\b': 'exekvera',  # Already correct Swedish
    r'\bmonitorera\b': 'övervaka',
    r'\bmonitora\b': 'övervaka',
    r'\bskala\b': 'skalera',
    r'\bmanagera\b': 'hantera',
    r'\bhandla\b': 'hantera',
    r'\bprocessa\b': 'bearbeta',
    r'\bvalidera\b': 'validera',  # Already correct Swedish
    r'\bgenerera\b': 'generera',  # Already correct Swedish
    r'\bcreatea\b': 'skapa',
    r'\bdeletea\b': 'ta bort',
    r'\buppdatera\b': 'uppdatera',  # Already correct Swedish
    r'\binstallera\b': 'installera',  # Already correct Swedish
    r'\bavinstallera\b': 'avinstallera',  # Already correct Swedish
    r'\brestorera\b': 'återställa',
    r'\boptimera\b': 'optimera',  # Already correct Swedish
    r'\banalysera\b': 'analysera',  # Already correct Swedish
    r'\bintegrera\b': 'integrera',  # Already correct Swedish
    r'\bautomatisera\b': 'automatisera',  # Already correct Swedish
    r'\bmigrera\b': 'migrera',  # Already correct Swedish
    r'\bupgradera\b': 'uppgradera',
    r'\bdegradGera\b': 'nedgradera',
    r'\bpatcha\b': 'uppdatera',
    r'\bfixa\b': 'åtgärda',
    r'\bdebugga\b': 'felsöka',
    r'\btroubleshoota\b': 'felsöka',
    r'\bbenchmarka\b': 'prestandatesta',
    
    # Nouns and other mixed terms
    r'\bbacka upp\b': 'säkerhetskopiera',
    r'\bsätta upp\b': 'konfigurera',
    
    # Common svengelska phrases  
    r'\bhandla\s+(\w+)\b': r'hantera \1',
    r'\bmanagera\s+(\w+)\b': r'hantera \1',
    r'\bmonitora\s+(\w+)\b': r'övervaka \1',
    r'\bdeplooya\s+(\w+)\b': r'distribuera \1',
    r'\bdeploya\s+(\w+)\b': r'distribuera \1',
    
    # Mixed English verbs in Swedish context
    r'(\w+)\s+deployad\b': r'\1 distribuerad',  
    r'(\w+)\s+deployed\b': r'\1 distribuerad',
    r'(\w+)\s+implementerad\b': r'\1 implementerad',  # Already correct
    r'(\w+)\s+managerad\b': r'\1 hanterad',
    r'(\w+)\s+optimerad\b': r'\1 optimerad',  # Already correct
    r'(\w+)\s+validerad\b': r'\1 validerad',  # Already correct
    
    # Specific svengelska verb corrections
    r'\bcommita\s+': 'checka in ',
    r'\bmerga\s+': 'sammanslå ',
    r'\bpusha\s+': 'skicka upp ',
    r'\bdeplooya\s+': 'distribuera ',
    r'\bdeploya\s+': 'distribuera ',
    r'\bsetuppa\s+': 'konfigurera ',
    r'\breleasa\s+': 'släppa ',
    r'\bmanagera\s+': 'hantera ',
    r'\bhandla\s+': 'hantera ',
    r'\bmonitora\s+': 'övervaka ',
    r'\bprocessa\s+': 'bearbeta ',
    r'\bcreatea\s+': 'skapa ',
    r'\bdeletea\s+': 'ta bort ',
    r'\brestorera\s+': 'återställa ',
    r'\bupgradera\s+': 'uppgradera ',
    r'\bpatcha\s+': 'uppdatera ',
    r'\bfixa\s+': 'åtgärda ',
    r'\bdebugga\s+': 'felsöka ',
    r'\btroubleshoota\s+': 'felsöka ',
    r'\bbenchmarka\s+': 'prestandatesta '
    
    # English gerunds in Swedish context  
    r'\bdeploying\b': 'distribution',
    r'\bmanaging\b': 'hantering',
    r'\bmonitoring\b': 'övervakning',
    r'\bscaling\b': 'skalning',
    r'\btesting\b': 'testning',
    r'\bbuilding\b': 'byggning',
    r'\bvalidating\b': 'validering',
    r'\bgenerating\b': 'generering',
    r'\boptimizing\b': 'optimering',
    r'\banalyzing\b': 'analys',
    r'\bintegrating\b': 'integrering',
    r'\bautomating\b': 'automatisering',
    r'\bmigrating\b': 'migrering',
    r'\bdebugging\b': 'felsökning',
    r'\btroubleshooting\b': 'felsökning',
    r'\bbenchmarking\b': 'prestandatestning',
    
    # Keep technical terms but fix grammatical integration
    r'\bCI/CD\s+pipeline\b': 'CI/CD-rörledning',
    r'\bCI/CD\s+pipelines\b': 'CI/CD-rörledningar',
    r'\bGit\s+commit\b': 'Git-incheckning',
    r'\bGit\s+commits\b': 'Git-incheckningar',
    r'\bPull\s+request\b': 'Pull request',  # Keep as technical term
    r'\bPull\s+requests\b': 'Pull requests',  # Keep as technical term
}

# Technical terms to keep in English (case insensitive)
KEEP_ENGLISH = {
    'api', 'apis', 'rest', 'graphql', 'json', 'yaml', 'xml',
    'docker', 'kubernetes', 'terraform', 'ansible', 'helm',
    'git', 'github', 'gitlab', 'bitbucket',
    'aws', 'azure', 'gcp', 'google cloud',
    'devops', 'cicd', 'ci/cd',
    'oauth', 'jwt', 'ssl', 'tls', 'https',
    'microservices', 'serverless',
    'infrastructure as code', 'iac',
    'architecture as code',
    'documentation as code', 'dac',
    'requirements as code', 'rac',
    'policy as code', 'pac'
}

def is_technical_context(text, position, window=50):
    """Check if position is in technical context where English is appropriate."""
    start = max(0, position - window)
    end = min(len(text), position + window)
    context = text[start:end].lower()
    
    # Check for technical keywords around the position
    for term in KEEP_ENGLISH:
        if term in context:
            return True
    
    # Check for code blocks
    if '```' in context or '`' in context:
        return True
        
    # Check for file extensions or technical paths
    if re.search(r'\.(yaml|yml|json|py|js|ts|tf|md|html|css)', context):
        return True
        
    return False

def process_file(file_path):
    """Process a single markdown file and fix svengelska."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        for pattern, replacement in SVENGELSKA_REPLACEMENTS.items():
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in reversed(matches):  # Reverse to maintain positions
                    # Check if it's in technical context
                    if not is_technical_context(content, match.start()):
                        original_text = match.group()
                        
                        # Apply replacement while preserving case
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
            
            print(f"✅ {file_path.name}: {len(changes_made)} svengelska fixes")
            for change in changes_made[:5]:  # Show first 5 changes
                print(f"   - {change}")
            if len(changes_made) > 5:
                print(f"   ... and {len(changes_made) - 5} more")
        else:
            print(f"⚪ {file_path.name}: No svengelska found")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def main():
    """Main function to process all markdown files."""
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print("❌ docs directory not found")
        return
    
    # Get all markdown files
    md_files = list(docs_dir.glob("*.md"))
    
    print(f"📚 Processing {len(md_files)} markdown files for svengelska...")
    print("=" * 60)
    
    for file_path in sorted(md_files):
        process_file(file_path)
    
    print("=" * 60)
    print("✨ Svengelska cleanup completed!")
    print("\nNote: Technical terms like API, Docker, Git, etc. kept in English")
    print("Ordinary language expressions converted to proper Swedish")

if __name__ == "__main__":
    main()