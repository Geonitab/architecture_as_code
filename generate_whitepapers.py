#!/usr/bin/env python3
"""
Generate whitepaper versions from book chapters.

This script reads the markdown files from docs/ directory (without modifying them)
and creates individual whitepaper HTML files in the whitepapers/ directory.

Usage:
    python generate_whitepapers.py

Note: This script ONLY reads from docs/ and creates files in the whitepapers/ directory.
It should never modify any files in the docs/ directory.
"""

import os
import sys
import glob
import re
from pathlib import Path

def read_chapter_content(chapter_file):
    """Read and parse a chapter markdown file."""
    try:
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter title (first h1)
        lines = content.split('\n')
        title = "Untitled Chapter"
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Extract diagram reference
        diagram_path = None
        for line in lines:
            if line.startswith('![') and 'images/' in line:
                # Extract diagram path from markdown image syntax
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    diagram_path = match.group(1)
                    break
        
        # Extract condensed content (first 2-3 paragraphs + key section headers)
        condensed_content = []
        section_headers = []
        paragraph_count = 0
        
        for line in lines:
            line = line.strip()
            
            # Skip title, empty lines, and image lines
            if (line.startswith('# ') or not line or 
                line.startswith('![') or line.startswith('##')):
                
                # Collect section headers for summary
                if line.startswith('## '):
                    section_headers.append(line[3:].strip())
                continue
            
            # Collect first few substantial paragraphs
            if paragraph_count < 3 and len(line) > 50:
                condensed_content.append(line)
                paragraph_count += 1
        
        return {
            'title': title,
            'diagram_path': diagram_path,
            'condensed_content': condensed_content,
            'section_headers': section_headers[:6]  # Limit to 6 main sections
        }
    
    except Exception as e:
        print(f"Error reading {chapter_file}: {e}")
        return None

def get_book_overview():
    """Return the book overview and purpose description."""
    return {
        'title': 'Arkitektur som kod',
        'subtitle': 'Infrastructure as Code för svenska organisationer',
        'description': '''
Infrastructure as Code representerar en fundamental förändring i hur vi hanterar och utvecklar IT-infrastruktur. 
Denna bok ger svenska organisationer praktisk vägledning för att implementera IaC-principer samtidigt som de 
uppfyller lokala compliance-krav och optimerar kostnader.

Boken täcker allt från grundläggande principer och verktyg till avancerade implementationsstrategier, 
säkerhetsaspekter och organisatoriska förändringar som krävs för framgångsrik IaC-adoption.
        '''.strip(),
        'target_audience': 'IT-arkitekter, DevOps-team, utvecklare och beslutsfattare inom svenska organisationer',
        'chapters_count': 25
    }

def get_chapter_mapping():
    """Return mapping of chapter files to readable chapter numbers."""
    return {
        '01_inledning.md': 'Inledning',
        '02_grundlaggande_principer.md': 'Kapitel 1',
        '03_versionhantering.md': 'Kapitel 2', 
        '04_adr.md': 'Kapitel 3',
        '05_automatisering_cicd.md': 'Kapitel 4',
        '06_devops_cicd.md': 'Kapitel 5',
        '07_molnarkitektur.md': 'Kapitel 6',
        '08_containerisering.md': 'Kapitel 7',
        '09_microservices.md': 'Kapitel 8',
        '10_sakerhet.md': 'Kapitel 9',
        '11_policy_sakerhet.md': 'Kapitel 10',
        '12_compliance.md': 'Kapitel 11',
        '13_teststrategier.md': 'Kapitel 12',
        '14_praktisk_implementation.md': 'Kapitel 13',
        '15_kostnadsoptimering.md': 'Kapitel 14',
        '16_migration.md': 'Kapitel 15',
        '17_organisatorisk_forandring.md': 'Kapitel 16',
        '18_team_struktur.md': 'Kapitel 17',
        '19_digitalisering.md': 'Kapitel 18',
        '20_lovable_mockups.md': 'Kapitel 19',
        '21_framtida_trender.md': 'Kapitel 20',
        '22_best_practices.md': 'Kapitel 21',
        '23_slutsats.md': 'Slutsats',
        '24_ordlista.md': 'Ordlista',
        '25_om_forfattarna.md': 'Om författarna'
    }

def create_whitepaper_html(chapter_data, chapter_ref, book_overview):
    """Create HTML content for a whitepaper."""
    
    # Read the template
    template_path = Path(__file__).parent / "templates" / "whitepaper-template.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Template not found at {template_path}")
        return None
    
    # Prepare content sections
    diagram_html = ""
    if chapter_data['diagram_path']:
        # Adjust path for whitepaper directory
        diagram_src = f"../docs/{chapter_data['diagram_path']}"
        diagram_html = f'''
            <div style="text-align: center; margin: 30px 0;">
                <img src="{diagram_src}" alt="Kapiteldiagram för {chapter_data['title']}" style="max-width: 100%; height: auto; border: 1px solid var(--kvadrat-gray-light); border-radius: 8px;">
            </div>
        '''
    
    # Create condensed content sections
    content_sections = []
    for paragraph in chapter_data['condensed_content']:
        content_sections.append(f"            <p>{paragraph}</p>")
    
    # Create section overview
    section_overview = ""
    if chapter_data['section_headers']:
        section_list = "".join([f"                <li>{header}</li>" for header in chapter_data['section_headers']])
        section_overview = f'''
            <h2>Huvudämnen som behandlas</h2>
            <ul>
{section_list}
            </ul>
        '''
    
    # Replace the title and content in template
    html_output = template
    
    # Replace title
    html_output = html_output.replace(
        'Modernisering av IT-infrastruktur genom kodbaserade lösningar',
        chapter_data['title']
    )
    
    # Replace subtitle
    html_output = html_output.replace(
        'En strategisk guide för organisationer som vill implementera Infrastructure as Code',
        f'Whitepaper från {chapter_ref} av boken "Arkitektur som kod"'
    )
    
    # Create the new content sections
    new_content = f'''        <!-- Book Overview -->
        <section>
            <h1>Om boken "Arkitektur som kod"</h1>
            <p class="lead"><strong>{book_overview['title']}</strong> - {book_overview['subtitle']}</p>
            
            <p>{book_overview['description']}</p>
            
            <div class="callout callout-info">
                <div class="callout-title">Målgrupp</div>
                <p>{book_overview['target_audience']}</p>
            </div>
        </section>

        <!-- Chapter Content -->
        <section>
            <h1>Kapitelöversikt: {chapter_data['title']}</h1>
{diagram_html}
            
{"".join(content_sections)}
            
{section_overview}
        </section>

        <!-- Call to Action -->
        <section>
            <h1>Läs mer</h1>
            <div class="callout callout-success">
                <div class="callout-title">Fullständigt innehåll</div>
                <p><strong>Läs mer i {chapter_ref} av boken "Arkitektur som kod"</strong> för djupgående förklaringar, praktiska exempel och detaljerade implementationsguider.</p>
            </div>
            
            <p>Boken innehåller totalt {book_overview['chapters_count']} kapitel som täcker alla aspekter av Infrastructure as Code för svenska organisationer, från grundläggande principer till avancerade implementationsstrategier.</p>
            
            <p><strong>Andra relevanta kapitel:</strong> Utforska hela bokens innehåll för en komplett förståelse av Infrastructure as Code-implementationer anpassade för svenska organisationer.</p>
        </section>'''
    
    # Replace the existing content sections
    import re
    
    # Find and replace everything from "Executive Summary" to just before "Footer"
    pattern = r'(<!-- Executive Summary -->.*?)(<!-- Footer -->)'
    match = re.search(pattern, html_output, re.DOTALL)
    
    if match:
        html_output = html_output.replace(match.group(1), new_content + '\n\n        ')
    else:
        # Fallback: replace all sections
        section_pattern = r'(<!-- Whitepaper Content -->.*?)<section>(.*?)</section>(.*?)<footer'
        section_match = re.search(section_pattern, html_output, re.DOTALL)
        if section_match:
            html_output = html_output.replace(
                section_match.group(0),
                f'{section_match.group(1)}{new_content}\n\n        <footer'
            )
    
    return html_output

def generate_whitepapers():
    """Main function to generate whitepapers."""
    print("Generating whitepapers from book chapters...")
    
    # Ensure whitepapers directory exists
    whitepapers_dir = Path("whitepapers")
    whitepapers_dir.mkdir(exist_ok=True)
    
    # Get chapter mapping and book overview
    chapter_mapping = get_chapter_mapping()
    book_overview = get_book_overview()
    
    # Find all chapter markdown files
    docs_dir = Path("docs")
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    
    generated_count = 0
    
    for chapter_file in chapter_files:
        filename = os.path.basename(chapter_file)
        
        # Skip files that aren't in our mapping (like build artifacts)
        if filename not in chapter_mapping:
            continue
            
        print(f"Processing {filename}...")
        
        # Read chapter content
        chapter_data = read_chapter_content(chapter_file)
        if not chapter_data:
            print(f"Failed to read {filename}, skipping...")
            continue
        
        # Get chapter reference
        chapter_ref = chapter_mapping[filename]
        
        # Generate whitepaper HTML
        html_content = create_whitepaper_html(chapter_data, chapter_ref, book_overview)
        if not html_content:
            print(f"Failed to generate HTML for {filename}, skipping...")
            continue
        
        # Write whitepaper file
        output_filename = filename.replace('.md', '_whitepaper.html')
        output_path = whitepapers_dir / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Generated: {output_path}")
            generated_count += 1
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
    
    print(f"\nGenerated {generated_count} whitepapers in {whitepapers_dir}/")
    return generated_count > 0

def main():
    """Main function."""
    try:
        success = generate_whitepapers()
        return 0 if success else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())