#!/usr/bin/env python3
"""
Final comprehensive cleanup for remaining Swedish words and artifacts
"""

import os
import re
from pathlib import Path

def comprehensive_final_cleanup(content):
    """Apply comprehensive final cleanup to remove all Swedish artifacts"""
    
    # Comprehensive Swedish -> English mappings
    comprehensive_fixes = {
        # Technical terms still in Swedish
        'implebuttation': 'implementation',
        'implebuttta': 'implement',
        'implebuttationen': 'implementation',
        'Architecture as Code-Architecture as Code-implebuttationen': 'Architecture as Code implementation',
        'Architecture as Code-implebuttationsaspekter': 'Architecture as Code implementation aspects',
        'Architecture as Code-automatiseringsverktyg': 'Architecture as Code automation tools',
        'Architecture as Code-capabilities': 'Architecture as Code capabilities',
        'Architecture as Code-automatisering_cicd': 'Architecture as Code automation and CI/CD',
        'fundabuttala': 'fundamental',
        'requirebutts': 'requirements',
        'butts': 'ments',
        'butt': 'ment',
        'improvebutt': 'improvement',
        
        # Common Swedish words still present
        'transformerat': 'transformed',
        'tänker kring': 'think about',
        'hanterar': 'manage',
        'behandla': 'treat',
        'möjliggjort': 'enabled',
        'noggrannhet': 'precision',
        'kvalitetskontroller': 'quality controls',
        'länge funnits': 'have long existed',
        'programvaruutveckling': 'software development',
        'resa': 'journey',
        'visat vägen': 'shown the way',
        'kräver': 'requires',
        'förändring': 'change',
        'kännetecknas': 'characterized',
        'ledningsengagemang': 'management commitment',
        'utbildningsprogram': 'training programs',
        'införandestrategi': 'implementation strategy',
        'störningar': 'disruptions',
        'befintlig verksamhet': 'existing operations',
        'utforskade': 'explored',
        'förståelse': 'understanding',
        'molnteknologier': 'cloud technologies',
        'säkerhetsprinciples': 'security principles',
        'behandlade': 'covered',
        'organisatorisk': 'organizational',
        'avgörande': 'crucial',
        'framgång': 'success',
        'inklusive': 'including',
        'kulturell': 'cultural',
        'kompetensutveckling': 'skills development',
        'processtandardisering': 'process standardization',
        
        # Document flow and structure
        'throughgång': 'review',
        'började with': 'began with',
        'utvecklades through': 'developed through',
        'kulminerade': 'culminated',
        'introducerades': 'were introduced',
        'fördjupades': 'were deepened',
        'vilket visar': 'which shows',
        'throughsyra': 'permeate',
        'står inför': 'face',
        'utmaningar': 'challenges',
        'möjligheter': 'opportunities',
        'belyste': 'highlighted',
        'enables': 'enables',
        'throughgår': 'undergo',
        'utforskade djupgående': 'explored in depth',
        'förenkla': 'simplify',
        'förbättra': 'improve',
        
        # Specific Swedish terms and phrases
        'Viktiga lärdomar': 'Important lessons learned',
        'Framgångsrika transformationer': 'Successful transformations',
        'teknisk excellens': 'technical excellence',
        'teknisk mognad': 'technical maturity',
        'Progressionen through': 'The progression through',
        'Säkerhetsaspekterna': 'The security aspects',
        'svensk': 'Swedish',
        'svenska': 'Swedish',
        'Swedish organizationss': 'Swedish organizations\'',
        'Swedish organizations': 'Swedish organizations',
        'organizationss': 'organizations\'',
        'unika': 'unique',
        'specific': 'specific',
        'regleringar': 'regulations',
        'särskild uppmärksamhet': 'special attention',
        'dataskydd': 'data protection',
        'klimatneutralitetsmål': 'climate neutrality goals',
        'hållbar': 'sustainable',
        'hållbarhet': 'sustainability',
        'digitaliseringsstrategi': 'digitalization strategy',
        'digital transformation': 'digital transformation',
        'Framtida utveckling': 'Future development',
        'teknologiska trender': 'technological trends',
        'nästa generation': 'next generation',
        'ytterligare': 'further',
        
        # Fix specific phrases
        'have transformerat how': 'have transformed how',
        'Through to behandla': 'By treating',
        'have vi möjliggjort': 'we have enabled',
        'that länge funnits within': 'that have long existed in',
        'This resa through': 'This journey through',
        'have visat vägen from': 'have shown the way from',
        'to framtidens': 'to the future\'s',
        'of stark': 'by strong',
        'and gradvis': 'and gradual',
        'that minimerar': 'that minimizes',
        'of befintlig': 'to existing',
        'according to de principles': 'according to the principles',
        'Den technical aspekten': 'The technical aspect',
        'for molnteknologier': 'of cloud technologies',
        'that vi behandlade': 'that we covered',
        'As well asidigt is': 'Equally important are',
        'för framgång': 'for success',
        'that deklarativ code': 'such as declarative code',
        'through practical': 'through practical',
        'and kulminerade in': 'and culminated in',
        'that introducerades in': 'that were introduced in',
        'vilket visar how': 'which shows how',
        'must throughsyra': 'must permeate',
        'from design to drift': 'from design to operations',
        'throughout The book\'s': 'throughout the book\'s',
        'have vi sett how': 'we have seen how',
        'driver innovation within': 'drives innovation in',
        'visade how': 'showed how',
        'that vi utforskade': 'that we explored',
        'will to ytterligare': 'will further',
        
        # Remove redundancies and fix grammar
        'The book\'s chapter have': 'The book\'s chapters have',
        'chapter have vi': 'chapters we have',
        'koncept that': 'concepts such as',
        'topics that': 'topics such as',
        'technologies that': 'technologies such as',
        'aspects that': 'aspects that',
        'factors that': 'factors such as',
        
        # Common remaining words
        'genom': 'through',
        'från': 'from',
        'till': 'to',
        'med': 'with',
        'för': 'for',
        'av': 'of',
        'på': 'on',
        'inom': 'within',
        'under': 'during',
        'över': 'over',
        'enligt': 'according to',
        'between': 'between',
        'efter': 'after',
        'innan': 'before',
        'samtidigt': 'simultaneously',
        'dessutom': 'furthermore',
        'därför': 'therefore',
        'eftersom': 'because',
        'medan': 'while',
        'dock': 'however',
        'alltså': 'thus',
        'istället': 'instead',
        'snarare': 'rather',
        'även om': 'even if',
        'trots att': 'despite',
        'så att': 'so that',
        'för att': 'to',
        'utan att': 'without',
        'genom att': 'by',
    }
    
    result = content
    
    # Apply all comprehensive fixes
    for swedish, english in comprehensive_fixes.items():
        result = result.replace(swedish, english)
    
    # Fix specific patterns
    result = re.sub(r'\b(vi|Vi)\b', 'we', result)
    result = re.sub(r'\bhave\s+(\w+)', r'have \1', result)
    result = re.sub(r'\bthat\s+(\w+ed)\b', r'that \1', result)
    result = re.sub(r'\bthrough\s+(The|the)\b', r'throughout \1', result)
    
    # Clean up grammar and syntax
    result = re.sub(r'(\w+)\s+(genom|från|till|med|för|av|på|inom)\s+', r'\1 ', result)
    result = re.sub(r'\s+', ' ', result)  # Remove extra spaces
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)  # Fix excessive line breaks
    
    # Capitalize sentences
    result = re.sub(r'(\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), result)
    result = re.sub(r'(^\s*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), result, flags=re.MULTILINE)
    
    return result

def main():
    """Apply comprehensive final cleanup to all English files"""
    docs_dir = Path("docs")
    english_files = list(docs_dir.glob("*_en.md"))
    
    print(f"🧹 Applying comprehensive final cleanup to {len(english_files)} English files...")
    
    for file_path in english_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned_content = comprehensive_final_cleanup(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Cleaned: {file_path.name}")
        
        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")
    
    print("✨ Comprehensive cleanup completed!")

if __name__ == "__main__":
    main()