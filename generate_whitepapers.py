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
        
        # Check if file is empty or too short
        if len(content.strip()) < 10:
            print(f"Warning: {chapter_file} appears to be empty or too short")
            return None
        
        # Extract chapter title (first h1)
        lines = content.split('\n')
        title = "Untitled Chapter"
        title_found = False
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                title_found = True
                break
        
        # If no H1 title found, try to extract from filename
        if not title_found:
            filename = os.path.basename(chapter_file)
            # Convert filename to readable title
            title_base = filename.replace('.md', '').replace('_', ' ')
            # Capitalize words
            title = ' '.join(word.capitalize() for word in title_base.split())
            print(f"Warning: No H1 title found in {chapter_file}, using filename-based title: {title}")
        
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
            
            # Skip markdown code blocks, bullet points, and other formatting
            if (line.startswith('```') or line.startswith('*') or 
                line.startswith('-') or line.startswith('>')):
                continue
            
            # Collect first few substantial paragraphs
            if paragraph_count < 3 and len(line) > 30:  # Lowered from 50 to 30 for edge cases
                condensed_content.append(line)
                paragraph_count += 1
        
        # If we don't have enough content, try to extract from any substantial text
        if paragraph_count == 0:
            print(f"Warning: No substantial paragraphs found in {chapter_file}, extracting any available text")
            for line in lines:
                line = line.strip()
                # Skip headers, empty lines, images, and short lines
                if (not line or line.startswith('#') or line.startswith('![') or 
                    line.startswith('```') or len(line) < 20):
                    continue
                if len(condensed_content) < 2:  # Get at least something
                    condensed_content.append(line)
                else:
                    break
        
        # Provide fallback content if still empty
        if not condensed_content:
            condensed_content = [f"Detta kapitel behandlar {title.lower()} inom Infrastructure as Code för svenska organisationer."]
            print(f"Warning: Using fallback content for {chapter_file}")
        
        # Provide fallback section headers if none found
        if not section_headers:
            section_headers = ["Introduktion", "Implementering", "Best Practices"]
            print(f"Warning: No section headers found in {chapter_file}, using fallback headers")
        
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
        'chapters_count': 31
    }

def get_chapter_mapping():
    """Return mapping of chapter files to readable chapter numbers."""
    return {
        '01_introduction.md': 'Kapitel 1',
        '02_fundamental_principles.md': 'Kapitel 2',
        '03_version_control.md': 'Kapitel 3',
        '04_adr.md': 'Kapitel 4',
        '05_automation_devops_cicd.md': 'Kapitel 5',
        '07_containerization.md': 'Kapitel 7',
        '09_security.md': 'Kapitel 9',
        '10_policy_and_security.md': 'Kapitel 10',
        '11_governance_as_code.md': 'Kapitel 11',
        '12_compliance.md': 'Kapitel 12',
        '13_testing_strategies.md': 'Kapitel 13',
        '14_practical_implementation.md': 'Kapitel 14',
        '15_cost_optimization.md': 'Kapitel 15',
        '16_migration.md': 'Kapitel 16',
        '17_organizational_change.md': 'Kapitel 17',
        '18_team_structure.md': 'Kapitel 18',
        '19_management_as_code.md': 'Kapitel 19',
        '20_ai_agent_team.md': 'Kapitel 20',
        '21_digitalization.md': 'Kapitel 21',
        '23_soft_as_code_interplay.md': 'Kapitel 23',
        '24_best_practices.md': 'Kapitel 24',
        '25_future_trends_development.md': 'Kapitel 25',
        '27_conclusion.md': 'Kapitel 27',
        '28_glossary.md': 'Ordlista',
        '29_about_the_authors.md': 'Om författaren',
        '30_appendix_code_examples.md': 'Appendix A',
        '31_technical_architecture.md': 'Appendix B'
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

def generate_whitepapers(release_mode=False):
    """Main function to generate whitepapers."""
    print("Generating whitepapers from book chapters...")
    
    # Set up output directories
    if release_mode:
        whitepapers_dir = Path("releases/whitepapers")
        print("Release mode: Generating whitepapers to releases/whitepapers/")
    else:
        whitepapers_dir = Path("whitepapers")
    
    # Ensure whitepapers directory exists
    whitepapers_dir.mkdir(exist_ok=True, parents=True)
    
    # Get chapter mapping and book overview
    chapter_mapping = get_chapter_mapping()
    book_overview = get_book_overview()
    
    # Find all chapter markdown files
    docs_dir = Path("docs")
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    
    print(f"Found {len(chapter_files)} markdown files in docs/ directory")
    print(f"Chapter mapping contains {len(chapter_mapping)} entries")
    
    generated_count = 0
    skipped_files = []
    error_files = []
    
    for chapter_file in chapter_files:
        filename = os.path.basename(chapter_file)
        
        # Skip files that aren't in our mapping (like build artifacts)
        if filename not in chapter_mapping:
            # Log the reason for skipping
            if filename.startswith('README') or filename.isupper() or filename.startswith('BOOK_') or filename.startswith('EPUB_') or filename.startswith('TERMINOLOGI_'):
                print(f"Skipping non-chapter file: {filename}")
                skipped_files.append((filename, "Non-chapter file (README, metadata, etc.)"))
            else:
                print(f"WARNING: Chapter file {filename} not found in mapping - this chapter will not have a whitepaper!")
                skipped_files.append((filename, "Missing from chapter mapping"))
            continue
            
        print(f"Processing {filename}...")
        
        # Read chapter content
        chapter_data = read_chapter_content(chapter_file)
        if not chapter_data:
            print(f"Failed to read {filename}, skipping...")
            error_files.append((filename, "Failed to read chapter content"))
            continue
        
        # Get chapter reference
        chapter_ref = chapter_mapping[filename]
        
        # Generate whitepaper HTML
        html_content = create_whitepaper_html(chapter_data, chapter_ref, book_overview)
        if not html_content:
            print(f"Failed to generate HTML for {filename}, skipping...")
            error_files.append((filename, "Failed to generate HTML"))
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
            error_files.append((filename, f"Write error: {e}"))
    
    # Copy to standard location if in release mode to maintain backward compatibility
    if release_mode:
        standard_dir = Path("whitepapers")
        standard_dir.mkdir(exist_ok=True)
        import shutil
        for html_file in whitepapers_dir.glob("*.html"):
            shutil.copy2(html_file, standard_dir / html_file.name)
        print(f"Whitepapers also copied to standard location: {standard_dir}/")
    
    # Print summary
    print(f"\n=== WHITEPAPER GENERATION SUMMARY ===")
    print(f"Generated {generated_count} whitepapers in {whitepapers_dir}/")
    print(f"Total files processed: {len(chapter_files)}")
    print(f"Files skipped: {len(skipped_files)}")
    print(f"Files with errors: {len(error_files)}")
    
    if skipped_files:
        print(f"\nSkipped files:")
        for filename, reason in skipped_files:
            print(f"  - {filename}: {reason}")
    
    if error_files:
        print(f"\nFiles with errors:")
        for filename, reason in error_files:
            print(f"  - {filename}: {reason}")
    
    print(f"\nExpected chapter files based on mapping: {len(chapter_mapping)}")
    if generated_count != len(chapter_mapping):
        missing_count = len(chapter_mapping) - generated_count
        print(f"WARNING: {missing_count} chapters did not generate whitepapers!")
    else:
        print("SUCCESS: All chapters have whitepapers!")
    
    return generated_count > 0

def main():
    """Main function."""
    try:
        # Check for --release flag
        release_mode = "--release" in sys.argv
        success = generate_whitepapers(release_mode)
        return 0 if success else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())