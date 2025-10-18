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
import math
import re
import textwrap
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

import yaml

def read_chapter_content(chapter_file):
    """Read and parse a chapter markdown file."""
    try:
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file is empty or too short
        if len(content.strip()) < 10:
            print(f"Warning: {chapter_file} appears to be empty or too short")
            return None
        
        word_count = len(re.findall(r'\w+', content))
        
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
            condensed_content = [f"This chapter covers {title.lower()} within Infrastructure as Code for organisations."]
            print(f"Warning: Using fallback content for {chapter_file}")
        
        # Provide fallback section headers if none found
        if not section_headers:
            section_headers = ["Introduction", "Implementation", "Best Practises"]
            print(f"Warning: No section headers found in {chapter_file}, using fallback headers")
        
        return {
            'title': title,
            'diagram_path': diagram_path,
            'condensed_content': condensed_content,
            'section_headers': section_headers[:6],  # Limit to 6 main sections
            'word_count': word_count
        }
    
    except Exception as e:
        print(f"Error reading {chapter_file}: {e}")
        return None

def get_book_overview():
    """Return the book overview and purpose description."""
    chapter_total = len(get_chapter_mapping())

    return {
        'title': 'Architecture as Code',
        'subtitle': 'Infrastructure as Code for organisations',
        'description': '''
Infrastructure as Code represents a fundamental change in how we manage and develop IT infrastructure.
This book provides organisations with practical guidance for implementing IaC principles whilst
fulfilling local compliance requirements and optimising costs.

The book covers everything from fundamental principles and tools to advanced implementation strategies,
security aspects, and organisational changes required for successful IaC adoption.
        '''.strip(),
        'target_audience': 'IT architects, DevOps teams, developers, and decision-makers within organisations',
        'chapters_count': chapter_total
    }

def _load_requirements_metadata(requirements_path: Path = Path("BOOK_REQUIREMENTS.md")) -> dict:
    """Load requirements front matter from the markdown specification."""
    if not requirements_path.exists():
        return {}

    lines = requirements_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    front_matter = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_matter.append(line)

    return yaml.safe_load("\n".join(front_matter)) or {}


def get_chapter_mapping():
    """Return mapping of chapter files to readable chapter identifiers."""
    metadata = _load_requirements_metadata()
    chapters = metadata.get("book", {}).get("chapters", [])

    mapping = OrderedDict()
    for index, chapter in enumerate(chapters, start=1):
        filename = chapter.get("filename")
        if not filename:
            continue

        label = chapter.get("label") or chapter.get("title")
        if not label:
            label = f"Chapter {index}"

        mapping[filename] = {
            "label": label,
            "title": chapter.get("title") or label,
            "area": chapter.get("area") or "Architecture as Code"
        }

    return mapping

def get_supplemental_chapters():
    """Return supplemental chapter metadata defined in requirements."""
    metadata = _load_requirements_metadata()
    supplemental_chapters = (
        metadata.get("book", {}).get("supplemental_chapters")
        or metadata.get("supplemental_chapters")
        or []
    )

    mapping = OrderedDict()
    for chapter in supplemental_chapters:
        filename = chapter.get("filename")
        if not filename:
            continue

        description = chapter.get("description", "").strip()
        area = chapter.get("area") or "Supplemental Material"

        mapping[filename] = {
            "label": chapter.get("label") or "Supplemental Chapter",
            "title": chapter.get("title"),
            "area": area,
            "description": description,
            "supplemental": True
        }

    return mapping

def get_all_chapter_mapping():
    """Return ordered mapping of canonical and supplemental chapters."""
    combined_mapping = OrderedDict()

    for filename, meta in get_chapter_mapping().items():
        meta_copy = dict(meta)
        meta_copy.setdefault("supplemental", False)
        combined_mapping[filename] = meta_copy

    for filename, meta in get_supplemental_chapters().items():
        if filename in combined_mapping:
            continue
        meta_copy = dict(meta)
        meta_copy.setdefault("supplemental", True)
        combined_mapping[filename] = meta_copy

    return combined_mapping

def create_whitepaper_html(chapter_data, chapter_meta, book_overview):
    """Create HTML content for a whitepaper."""
    
    # Read the template
    template_path = Path(__file__).parent / "templates" / "whitepaper-template.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Template not found at {template_path}")
        return None

    if isinstance(chapter_meta, dict):
        chapter_label = chapter_meta.get("label") or "Chapter"
        chapter_area = chapter_meta.get("area") or "Architecture as Code"
        mapped_title = chapter_meta.get("title") or chapter_data['title']
    else:
        chapter_label = str(chapter_meta)
        chapter_area = "Architecture as Code"
        mapped_title = chapter_data['title']
    
    page_title = f"{chapter_label} – {chapter_data['title']}"
    subtitle_text = f'Key insights from {chapter_label} of "{book_overview["title"]}"'
    author_text = "Architecture as Code Editorial Team"
    published_date = datetime.now().strftime("%d %B %Y")
    if published_date.startswith("0"):
        published_date = published_date[1:]
    reading_minutes = chapter_data.get('word_count') or 0
    if reading_minutes:
        reading_minutes = max(3, math.ceil(reading_minutes / 220))
    else:
        reading_minutes = 3
    reading_label = f"{reading_minutes} minute{'s' if reading_minutes != 1 else ''}"
    version_text = "1.0"
    
    # Prepare content sections
    diagram_html = ""
    if chapter_data['diagram_path']:
        # Adjust path for whitepaper directory
        diagram_src = f"../docs/{chapter_data['diagram_path']}"
        diagram_html = (
            "            <div style=\"text-align: center; margin: 30px 0;\">\n"
            f"                <img src=\"{diagram_src}\" alt=\"Chapter diagram for {chapter_data['title']}\" style=\"max-width: 100%; height: auto; border: 1px solid var(--kvadrat-gray-light); border-radius: 8px;\">\n"
            "            </div>"
        )
    
    # Create condensed content sections
    content_sections = "\n".join(
        f"            <p>{paragraph}</p>"
        for paragraph in chapter_data['condensed_content']
    )
    
    # Create section overview
    section_overview = ""
    if chapter_data['section_headers']:
        section_list = "\n".join(
            f"                <li>{header}</li>"
            for header in chapter_data['section_headers']
        )
        section_overview = (
            "            <h2>Primary topics explored</h2>\n"
            "            <ul>\n"
            f"{section_list}\n"
            "            </ul>"
        )
    
    # Replace the title and content in template
    html_output = template

    html_output = html_output.replace('{{PAGE_TITLE}}', page_title)
    html_output = html_output.replace('{{TITLE}}', chapter_data['title'])
    html_output = html_output.replace('{{SUBTITLE}}', subtitle_text)
    html_output = html_output.replace('{{CATEGORY}}', chapter_area)
    html_output = html_output.replace('{{AUTHOR}}', author_text)
    html_output = html_output.replace('{{DATE}}', published_date)
    html_output = html_output.replace('{{VERSION}}', version_text)
    html_output = html_output.replace('{{READING_TIME}}', reading_label)
    html_output = html_output.replace('{{MAPPED_TITLE}}', mapped_title)
    html_output = html_output.replace('{{CHAPTER_LABEL}}', chapter_label)
    
    # Create the new content sections
    new_content = f'''        <!-- Book Overview -->
        <section>
            <h1>About the book "{book_overview['title']}"</h1>
            <p class="lead"><strong>{book_overview['title']}</strong> – {book_overview['subtitle']}</p>
            
            <p>{book_overview['description']}</p>
            
            <div class="callout callout-info">
                <div class="callout-title">Target Audience</div>
                <p>{book_overview['target_audience']}</p>
            </div>
        </section>

        <!-- Chapter Content -->
        <section>
            <h1>{chapter_label}: {chapter_data['title']}</h1>
{diagram_html if diagram_html else ""}
            
{content_sections}
            
{section_overview}
        </section>

        <!-- Call to Action -->
        <section>
            <h1>Continue Your Journey</h1>
            <div class="callout callout-success">
                <div class="callout-title">Complete Chapter</div>
                <p><strong>Read {chapter_label} – "{chapter_data['title']}" in "{book_overview['title']}"</strong> for detailed explanations, practical examples, and implementation patterns.</p>
            </div>
            
            <p>The full manuscript explores {book_overview['chapters_count']} chapters, positioning this whitepaper within the {chapter_area.lower()} focus of the programme.</p>
            
            <p><strong>Explore adjacent chapters:</strong> The surrounding sections expand upon the themes introduced here and provide complementary techniques.</p>
        </section>'''
    
    # Replace the existing content sections
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
    supplemental_mapping = get_supplemental_chapters()
    all_chapter_mapping = get_all_chapter_mapping()
    book_overview = get_book_overview()
    
    # Find all chapter markdown files
    docs_dir = Path("docs")
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    
    print(f"Found {len(chapter_files)} markdown files in docs/ directory")
    print(f"Chapter mapping contains {len(chapter_mapping)} canonical entries")
    if supplemental_mapping:
        print(f"Supplemental chapter mapping contains {len(supplemental_mapping)} entries")
    
    generated_count = 0
    canonical_generated = 0
    supplemental_generated = 0
    skipped_files = []
    error_files = []
    processed_files = set()
    
    for chapter_file in chapter_files:
        filename = os.path.basename(chapter_file)
        
        # Skip files that aren't in our mapping (like build artifacts)
        if filename not in all_chapter_mapping:
            # Log the reason for skipping
            chapter_name_no_ext = filename.rsplit('.', 1)[0]
            if (filename.startswith('README') or chapter_name_no_ext.isupper() or filename.startswith('BOOK_') 
                or filename.startswith('EPUB_') or filename.startswith('TERMINOLOGI_') 
                or filename.startswith('part_') or filename in ("book_structure.md", "index.md")):
                print(f"Skipping non-chapter file: {filename}")
                skipped_files.append((filename, "Non-chapter file (README, metadata, part introduction, etc.)"))
            else:
                print(f"WARNING: Chapter file {filename} not found in mapping - this chapter will not have a whitepaper!")
                skipped_files.append((filename, "Missing from chapter mapping"))
            continue
            
        processed_files.add(filename)
        print(f"Processing {filename}...")
        
        # Read chapter content
        chapter_data = read_chapter_content(chapter_file)
        if not chapter_data:
            print(f"Failed to read {filename}, skipping...")
            error_files.append((filename, "Failed to read chapter content"))
            continue
        
        # Get chapter metadata
        chapter_meta = all_chapter_mapping[filename]
        
        # Generate whitepaper HTML
        html_content = create_whitepaper_html(chapter_data, chapter_meta, book_overview)
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
            if chapter_meta.get("supplemental"):
                supplemental_generated += 1
            else:
                canonical_generated += 1
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
            error_files.append((filename, f"Write error: {e}"))
    
    # Check for any mapped files missing from docs directory
    missing_mapped = [fname for fname in all_chapter_mapping.keys() if fname not in processed_files]
    for missing_file in missing_mapped:
        chapter_meta = all_chapter_mapping[missing_file]
        if chapter_meta.get("supplemental"):
            print(f"WARNING: Supplemental chapter file {missing_file} missing from docs/ directory.")
            skipped_files.append((missing_file, "Supplemental chapter missing from docs/ directory"))
        else:
            print(f"ERROR: Required chapter file {missing_file} missing from docs/ directory!")
            error_files.append((missing_file, "Required chapter file missing"))

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
    print(f"Canonical chapters generated: {canonical_generated}/{len(chapter_mapping)}")
    if supplemental_mapping:
        print(f"Supplemental chapters generated: {supplemental_generated}/{len(supplemental_mapping)}")
    
    if skipped_files:
        print(f"\nSkipped files:")
        for filename, reason in skipped_files:
            print(f"  - {filename}: {reason}")
    
    if error_files:
        print(f"\nFiles with errors:")
        for filename, reason in error_files:
            print(f"  - {filename}: {reason}")
    
    print(f"\nExpected chapter files based on mapping: {len(all_chapter_mapping)}")
    missing_total = len(all_chapter_mapping) - generated_count
    if missing_total > 0:
        print(f"WARNING: {missing_total} chapters did not generate whitepapers!")
    else:
        print("SUCCESS: All chapters have whitepapers!")
    
    success = canonical_generated == len(chapter_mapping) and generated_count > 0 and not error_files
    return success

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
