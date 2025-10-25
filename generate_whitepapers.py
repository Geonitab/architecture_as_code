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
import shutil
from collections import OrderedDict
from datetime import datetime, timezone
from html import escape
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


def get_release_metadata(requirements_path: Path = Path("BOOK_REQUIREMENTS.md")) -> dict:
    """Return structured release metadata for versioned collateral."""
    metadata = _load_requirements_metadata(requirements_path)
    release = metadata.get("release") or {}

    version = str(release.get("version") or "1.0").strip()
    codename = str(release.get("codename") or "").strip()

    build_number = (
        release.get("build_number")
        or os.environ.get("BUILD_NUMBER")
        or os.environ.get("GITHUB_RUN_NUMBER")
        or ""
    )
    build_number = str(build_number).strip()

    release_date = release.get("release_date") or release.get("date")
    if isinstance(release_date, datetime):
        release_date = release_date.isoformat()
    elif release_date:
        release_date = str(release_date).strip()

    feature_tags = release.get("feature_tags") or []
    if isinstance(feature_tags, str):
        feature_tags = [feature_tags]

    feature_tags = [
        str(tag).strip()
        for tag in feature_tags
        if str(tag).strip()
    ]

    return {
        "version": version or "1.0",
        "codename": codename,
        "build_number": build_number,
        "release_date": release_date,
        "feature_tags": feature_tags,
    }


def resolve_diagram_src(diagram_path: str | None, output_directory: Path) -> str | None:
    """Resolve diagram path relative to the generated whitepaper location."""
    if not diagram_path:
        return None

    # Diagrams are stored under docs/, ensure we reference that root
    source_path = Path(diagram_path)
    if not source_path.is_absolute():
        source_path = Path("docs") / source_path

    if not source_path.exists():
        print(f"Warning: Diagram {diagram_path} not found at {source_path}")
        return None

    relative_diagram_path = Path(diagram_path)
    if relative_diagram_path.is_absolute():
        relative_diagram_path = Path(relative_diagram_path.name)

    target_path = output_directory / relative_diagram_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(source_path, target_path)
    except shutil.SameFileError:
        pass

    return relative_diagram_path.as_posix()


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

def create_whitepaper_html(chapter_data, chapter_meta, book_overview, release_info, output_directory):
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
    
    page_title = f"{chapter_label} – {mapped_title}"
    subtitle_text = f'Key insights from {chapter_label} of "{book_overview["title"]}"'
    author_text = "Gunnar Nordqvist"

    release_info = release_info or {}
    build_number = str(release_info.get("build_number") or "").strip()
    version_text = build_number or str(release_info.get("version") or "1.0")
    codename_text = str(release_info.get("codename") or "").strip()
    raw_release_date = release_info.get("release_date") or release_info.get("date")

    published_date = None
    if raw_release_date:
        try:
            published_date = datetime.fromisoformat(str(raw_release_date)).strftime("%d %B %Y")
        except ValueError:
            # Accept already formatted dates
            published_date = str(raw_release_date)

    if not published_date:
        published_date = datetime.now(timezone.utc).strftime("%d %B %Y")

    if published_date.startswith("0"):
        published_date = published_date[1:]

    raw_feature_tags = release_info.get("feature_tags") or []
    if isinstance(raw_feature_tags, str):
        raw_feature_tags = [raw_feature_tags]
    feature_tags = [
        str(tag).strip()
        for tag in raw_feature_tags
        if str(tag).strip()
    ]

    escaped_page_title = escape(page_title)
    escaped_chapter_area = escape(chapter_area)
    escaped_chapter_title = escape(chapter_data['title'])
    escaped_mapped_title = escape(mapped_title)
    escaped_subtitle_text = escape(subtitle_text)
    escaped_author_text = escape(author_text)
    escaped_published_date = escape(published_date)
    escaped_version_text = escape(version_text)
    escaped_chapter_label = escape(chapter_label)
    escaped_codename = escape(codename_text) if codename_text else ""

    # Prepare content sections
    diagram_html = ""
    diagram_src = resolve_diagram_src(chapter_data.get('diagram_path'), output_directory)

    if not diagram_src and chapter_data.get('diagram_path'):
        # Fallback for unexpected path handling issues
        diagram_src = f"../docs/{chapter_data['diagram_path']}"

    if diagram_src:
        diagram_html = (
            "            <figure class=\"chapter-figure\">\n"
            f"                <img src=\"{escape(diagram_src)}\" alt=\"Chapter diagram for {escaped_chapter_title}\">\n"
            "            </figure>"
        )
    
    # Create condensed content sections
    content_sections = "\n".join(
        f"            <p>{escape(paragraph)}</p>"
        for paragraph in chapter_data['condensed_content']
    )
    
    # Create section overview
    section_overview = ""
    if chapter_data['section_headers']:
        section_list = "\n".join(
            f"                <li>{escape(header)}</li>"
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

    replacements = {
        "[[PAGE_TITLE]]": escaped_page_title,
        "[[CATEGORY]]": escaped_chapter_area,
        "[[TITLE]]": escaped_mapped_title,
        "[[SUBTITLE]]": escaped_subtitle_text,
        "[[AUTHOR]]": escaped_author_text,
        "[[DATE]]": escaped_published_date,
        "[[VERSION]]": escaped_version_text,
    }

    for placeholder, value in replacements.items():
        html_output = html_output.replace(placeholder, value)

    escaped_book_title = escape(book_overview['title'])
    escaped_book_description = escape(book_overview['description']).replace('\n', '<br>')
    escaped_target_audience = escape(book_overview['target_audience'])
    escaped_area_lower = escape(chapter_area.lower())

    feature_tags_html = ""
    if feature_tags:
        tag_markup = "\n".join(
            f'            <span class="feature-tag" role="listitem">{escape(tag)}</span>'
            for tag in feature_tags
        )
        feature_tags_html = (
            '            <div class="feature-tags" role="list" aria-label="Release feature tags">\n'
            f'{tag_markup}\n'
            '            </div>'
        )
    html_output = html_output.replace("            <!-- FEATURE_TAGS -->", feature_tags_html, 1)

    data_attributes = [f'data-release-version="{escaped_version_text}"']
    if feature_tags:
        joined_tags = ", ".join(feature_tags)
        escaped_joined_tags = escape(joined_tags)
        data_attributes.append(f'data-feature-tags="{escaped_joined_tags}"')
    if codename_text:
        data_attributes.append(f'data-release-codename="{escaped_codename}"')

    attribute_string = " ".join(data_attributes)
    html_output = html_output.replace('<div class="page">', f'<div class="page" {attribute_string}>', 1)
    
    # Create the new content sections
    new_content = f'''        <!-- Book Overview -->
        <section class="book-overview">
            <h1>About "{escaped_book_title}"</h1>
            <p class="lead">{escaped_book_description}</p>

            <div class="callout callout-info">
                <div class="callout-title">Who should read this</div>
                <p>{escaped_target_audience}</p>
            </div>
        </section>

        <!-- Chapter Content -->
        <section class="chapter-highlight">
            <h1>{escaped_chapter_label}: {escaped_chapter_title}</h1>
{diagram_html if diagram_html else ""}

{content_sections}

{section_overview}
        </section>

        <!-- Call to Action -->
        <section class="call-to-action">
            <h1>Continue your journey</h1>
            <div class="callout callout-success">
                <div class="callout-title">Read the full chapter</div>
                <p><strong>Discover {escaped_chapter_label} – "{escaped_chapter_title}" in "{escaped_book_title}"</strong> for detailed explanations, practical examples, and implementation patterns.</p>
            </div>

            <p>The complete manuscript spans {book_overview['chapters_count']} chapters, positioning this whitepaper within the {escaped_area_lower} focus of the programme.</p>

            <p><strong>Explore adjacent chapters:</strong> The surrounding sections expand upon the themes introduced here and provide complementary techniques.</p>
        </section>'''

    content_placeholder = "        <!-- WHITEPAPER_CONTENT -->"
    if content_placeholder in html_output:
        html_output = html_output.replace(content_placeholder, new_content)

    return html_output

def generate_whitepapers(release_mode=False):
    """Main function to generate whitepapers."""
    print("Generating whitepapers from book chapters...")
    
    # Set up output directories
    if release_mode:
        whitepapers_dir = Path("releases/whitepapers")
        print("Release mode: Generating whitepapers to releases/whitepapers/")
        secondary_dir = Path("whitepapers")
    else:
        whitepapers_dir = Path("whitepapers")
        secondary_dir = None
    
    # Ensure whitepapers directory exists
    whitepapers_dir.mkdir(exist_ok=True, parents=True)
    if secondary_dir:
        secondary_dir.mkdir(exist_ok=True, parents=True)
    
    # Get chapter mapping and book overview
    chapter_mapping = get_chapter_mapping()
    book_overview = get_book_overview()
    release_metadata = get_release_metadata()

    print(f"Release version: {release_metadata.get('version', '1.0')}")
    if release_metadata.get("feature_tags"):
        print("Feature tags: " + ", ".join(release_metadata["feature_tags"]))
    
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
        
        # Get chapter metadata
        chapter_meta = chapter_mapping[filename]
        
        # Write whitepaper file
        output_filename = filename.replace('.md', '_whitepaper.html')
        output_path = whitepapers_dir / output_filename
        
        # Generate whitepaper HTML
        html_content = create_whitepaper_html(
            chapter_data,
            chapter_meta,
            book_overview,
            release_metadata,
            whitepapers_dir
        )
        if not html_content:
            print(f"Failed to generate HTML for {filename}, skipping...")
            error_files.append((filename, "Failed to generate HTML"))
            continue
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Generated: {output_path}")
            generated_count += 1
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
            error_files.append((filename, f"Write error: {e}"))

        if secondary_dir:
            secondary_output_path = secondary_dir / output_filename
            secondary_html = create_whitepaper_html(
                chapter_data,
                chapter_meta,
                book_overview,
                release_metadata,
                secondary_dir
            )
            if not secondary_html:
                print(f"Warning: Failed to generate HTML for standard location: {filename}")
                error_files.append((filename, "Failed to generate HTML for standard location"))
            else:
                try:
                    with open(secondary_output_path, 'w', encoding='utf-8') as f:
                        f.write(secondary_html)
                    print(f"Generated: {secondary_output_path} (standard location)")
                except Exception as e:
                    print(f"Error writing {secondary_output_path}: {e}")
                    error_files.append((filename, f"Standard write error: {e}"))
    
    if release_mode:
        print("Standard whitepapers also generated in whitepapers/")

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
