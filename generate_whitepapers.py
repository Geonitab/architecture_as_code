#!/usr/bin/env python3
"""
Generate whitepaper versions from book chapters.

This script reads the markdown files from docs/ directory (without modifying them)
and creates individual whitepaper HTML files in the whitepapers/ directory.

Design Compliance:
    All generated whitepapers follow the design standards defined in:
    docs/WHITEPAPER_DESIGN_GUIDELINES.md
    
    Key features:
    - A4/Letter format (210mm × 297mm) optimised for screen and print
    - Kvadrat brand colours and typography (Inter and JetBrains Mono)
    - WCAG AA accessibility compliance (4.5:1 minimum contrast)
    - Semantic HTML5 with proper heading hierarchy
    - Responsive design with mobile breakpoints (min-width: 320px)
    - Professional document structure with metadata and feature tags

Usage:
    python generate_whitepapers.py              # Generate to whitepapers/
    python generate_whitepapers.py --release    # Generate to releases/whitepapers/

Note: This script ONLY reads from docs/ and creates files in the whitepapers/ directory.
It should never modify any files in the docs/ directory.
"""

import os
import sys
import re
import shutil
from collections import OrderedDict
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import yaml

from scripts.navigation import get_whitepaper_chapter_files

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
                title = strip_anchor(line[2:])
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
        diagram_caption = None
        for index, line in enumerate(lines):
            if line.startswith('![') and 'images/' in line:
                # Extract diagram path and caption from markdown image syntax
                match = re.search(r'!\[(.*?)\]\((.*?)\)', line)
                if match:
                    diagram_path = match.group(2)
                    following = [candidate.strip() for candidate in lines[index + 1:index + 4] if candidate.strip()]
                    if following and re.match(r'^\*?Figure\b', following[0]):
                        diagram_caption = following[0]
                    else:
                        diagram_caption = match.group(1).strip() or None
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
                    section_headers.append(strip_anchor(line[3:]))
                continue
            
            # Skip markdown code blocks, bullet points, and other formatting
            if (line.startswith('```') or line.startswith('*') or 
                line.startswith('-') or line.startswith('>') or
                line.startswith('|') or line.startswith('<')):
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
            'diagram_caption': diagram_caption,
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
    """
    Return a relative path from the output directory to the diagram in docs/.
    """
    if not diagram_path:
        return None

    source_path = Path(diagram_path)
    if not source_path.is_absolute():
        source_path = Path("docs") / source_path

    try:
        relative_path = os.path.relpath(source_path, output_directory)
        return Path(relative_path).as_posix()
    except ValueError:
        return source_path.as_posix()


def get_chapter_mapping():
    """Return mapping of chapter files to readable chapter identifiers."""
    metadata = _load_requirements_metadata()
    chapters = metadata.get("book", {}).get("chapters", [])
    chapter_lookup = {
        str(chapter.get("filename")): chapter
        for chapter in chapters
        if chapter.get("filename")
    }

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
            "area": chapter.get("area") or "Architecture as Code",
        }

    return mapping

ANCHOR_PATTERN = re.compile(r"\s*\{#[^}]*\}")
HEX_COLOUR = re.compile(r"^#[0-9A-Fa-f]{3,8}$")
PALETTE_TOKENS = ("dark", "primary", "strong", "accent", "tint", "paper")


def strip_anchor(text):
    """Remove Pandoc heading anchors such as ``{#chapter-anchor}``."""
    return ANCHOR_PATTERN.sub("", text).strip()


def author_byline_html():
    """Byline with the author's portrait, embedded so the whitepaper stays a single file."""
    import base64
    photo = Path(__file__).resolve().parent / "docs" / "images" / "gunnar_nordqvist.jpg"
    if not photo.exists():
        return ""
    data = base64.b64encode(photo.read_bytes()).decode("ascii")
    return (
        '\n            <div class="author-portrait" style="display:flex;gap:20px;align-items:center;margin-top:24px">'
        f'<img src="data:image/jpeg;base64,{data}" alt="Portrait of Gunnar Nordqvist" width="96" height="96" '
        'style="width:96px;height:96px;border-radius:50%;object-fit:cover;flex:none">'
        '<div><p style="margin:0"><strong>Gunnar Nordqvist</strong></p>'
        '<p style="margin:0">Conceived, directed and published the books of The Transformed Architecture.</p></div></div>'
    )



def render_inline(text):
    """Render the inline Markdown that occurs in chapter prose as safe HTML.

    Code spans, bold and italics are kept; links are reduced to their text
    (citations then read "(30, Nordqvist, 2025)" and links to other chapters
    would be dead in a stand-alone whitepaper); images and Pandoc anchors are
    dropped. Everything else is escaped.
    """
    code_spans = []

    def stash_code(match):
        code_spans.append(match.group(1))
        return f"\x00{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\([^)]*\)", r"\1", text)
    text = ANCHOR_PATTERN.sub("", text)
    text = escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(
        r"\x00(\d+)\x00",
        lambda match: f"<code>{escape(code_spans[int(match.group(1))], quote=False)}</code>",
        text,
    )


def split_title(title):
    """Split a chapter title at its first colon when what precedes it is a real heading."""
    main, separator, deck = title.partition(": ")
    if separator and len(main.split()) >= 3:
        return main.strip(), deck.strip()
    return title.strip(), ""


def read_site_url(root):
    """Return the book's website from the repository's CNAME file, or an empty string."""
    try:
        host = (root / "CNAME").read_text(encoding="utf-8").split()[0]
    except (OSError, IndexError):
        return ""
    return f"https://{host}" if re.fullmatch(r"[A-Za-z0-9.-]+", host) else ""


def load_book_palette(root):
    """Return a ``:root`` block with the book's colours, or an empty string.

    The colours are the ``--book-*`` tokens of docs/stylesheets/series-colours.css,
    the file that gives the website and the diagrams the palette of the cover.
    Without that file the template keeps its defaults.
    """
    try:
        text = (root / "docs" / "stylesheets" / "series-colours.css").read_text(encoding="utf-8")
    except OSError:
        return ""
    block = re.search(r":root\s*\{(.*?)\}", text, re.S)
    if not block:
        return ""
    tokens = dict(re.findall(r"--book-([a-z]+)\s*:\s*(#[0-9A-Fa-f]{3,8})\s*;", block.group(1)))
    declarations = [
        f"--book-{name}: {tokens[name]};"
        for name in PALETTE_TOKENS
        if name in tokens and HEX_COLOUR.match(tokens[name])
    ]
    return ":root { " + " ".join(declarations) + " }" if declarations else ""


def split_paragraphs(text):
    """Split a hard-wrapped block of text into paragraphs at blank lines."""
    return [
        re.sub(r"\s*\n\s*", " ", paragraph).strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]


def create_whitepaper_html(chapter_data, chapter_meta, book_overview, release_info, output_directory, chapter_file=None):
    """Create HTML content for a whitepaper."""

    root = Path(__file__).resolve().parent
    template_path = root / "templates" / "whitepaper-template.html"

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Template not found at {template_path}")
        return None

    book_title = book_overview['title']

    if isinstance(chapter_meta, dict):
        chapter_label = chapter_meta.get("label") or "Chapter"
        chapter_area = chapter_meta.get("area") or book_title
        mapped_title = chapter_meta.get("title") or chapter_data['title']
    else:
        chapter_label = str(chapter_meta)
        chapter_area = book_title
        mapped_title = chapter_data['title']

    page_title = f"{chapter_label} – {mapped_title}"
    main_title, deck_text = split_title(mapped_title)
    author_text = "Gunnar Nordqvist"

    number_match = re.fullmatch(r"Chapter\s+(\w+)", chapter_label)
    chapter_number = number_match.group(1) if number_match else ""
    kicker_text = chapter_label if chapter_area == book_title else f"{chapter_label} · {chapter_area}"
    if chapter_number:
        fallback_subtitle = f'Key insights from {chapter_label} of "{book_title}"'
    else:
        fallback_subtitle = f'{chapter_label} from "{book_title}"'
    subtitle_text = deck_text or fallback_subtitle

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

    year_match = re.search(r"\b(20\d\d)\b", published_date)
    year_text = year_match.group(1) if year_match else str(datetime.now(timezone.utc).year)

    raw_feature_tags = release_info.get("feature_tags") or []
    if isinstance(raw_feature_tags, str):
        raw_feature_tags = [raw_feature_tags]
    feature_tags = [
        str(tag).strip()
        for tag in raw_feature_tags
        if str(tag).strip()
    ]

    site_url = read_site_url(root)
    chapter_url = f"{site_url}/{Path(chapter_file).stem}/" if site_url and chapter_file else site_url

    escaped_book_title = escape(book_title)
    escaped_chapter_title = escape(chapter_data['title'])
    escaped_chapter_label = escape(chapter_label)
    escaped_area = escape(chapter_area)
    escaped_version_text = escape(version_text)
    escaped_codename = escape(codename_text) if codename_text else ""

    footer_right = escaped_book_title
    if site_url:
        footer_right += f' · <a href="{escape(site_url)}">{escape(site_url.removeprefix("https://"))}</a>'

    replacements = {
        "/* [[PALETTE_OVERRIDE]] */": load_book_palette(root),
        "[[PAGE_TITLE]]": escape(page_title),
        "[[EYEBROW]]": f"{escaped_book_title} · Whitepaper",
        "[[CHAPTER_NUMBER]]": escape(chapter_number),
        "[[CATEGORY]]": escape(kicker_text),
        "[[TITLE]]": escape(main_title),
        "[[SUBTITLE]]": escape(subtitle_text),
        "[[AUTHOR]]": escape(author_text),
        "[[DATE]]": escape(published_date),
        "[[VERSION]]": escaped_version_text,
        "[[FOOTER_LEFT]]": f"<strong>© {year_text} Gunnar Nordqvist.</strong> Published by GEON IT AB.",
        "[[FOOTER_RIGHT]]": footer_right,
    }

    html_output = template
    for placeholder, value in replacements.items():
        html_output = html_output.replace(placeholder, value)

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

    # Chapter content: figure, opening paragraphs, topics
    diagram_html = ""
    diagram_src = resolve_diagram_src(chapter_data.get('diagram_path'), output_directory)

    if diagram_src:
        caption = (chapter_data.get('diagram_caption') or "").strip().strip('*').strip()
        alt_text = escape(re.sub(r"\s+", " ", caption)) if caption else f"Chapter diagram for {escaped_chapter_title}"
        caption_html = f"\n                <figcaption>{render_inline(caption)}</figcaption>" if caption else ""
        diagram_html = (
            "            <figure class=\"chapter-figure\">\n"
            f"                <img src=\"{escape(diagram_src)}\" alt=\"{alt_text}\">{caption_html}\n"
            "            </figure>\n"
        )

    paragraphs = chapter_data['condensed_content']
    paragraph_lines = []
    for index, paragraph in enumerate(paragraphs):
        css_class = ' class="lead"' if index == 0 else ""
        paragraph_lines.append(f"            <p{css_class}>{render_inline(paragraph)}</p>")
    content_sections = "\n".join(paragraph_lines)

    section_overview = ""
    if chapter_data['section_headers']:
        section_list = "\n".join(
            f"                <li>{render_inline(header)}</li>"
            for header in chapter_data['section_headers']
        )
        section_overview = (
            "\n            <h2>Primary topics explored</h2>\n"
            "            <ol class=\"topics\">\n"
            f"{section_list}\n"
            "            </ol>"
        )

    description_html = "\n".join(
        f"            <p>{escape(paragraph)}</p>"
        for paragraph in split_paragraphs(book_overview['description'])
    )
    audience = book_overview['target_audience'].strip()
    if audience and audience[-1] not in ".!?":
        audience += "."

    area_sentence = "" if chapter_area == book_title else f" belongs to “{escaped_area}” and"
    button_html = (
        f'            <p><a class="button" href="{escape(chapter_url)}">Read the full chapter online</a></p>\n'
        if chapter_url else ""
    )

    new_content = f'''        <section class="chapter-highlight">
{diagram_html}{content_sections}{section_overview}
        </section>

        <section class="book-overview">
            <h2>About <em>{escaped_book_title}</em></h2>
{description_html}

            <div class="callout">
                <div class="callout-title">Who should read this</div>
                <p>{escape(audience)}</p>
            </div>{author_byline_html()}
        </section>

        <section class="call-to-action">
            <h2>Continue with the full chapter</h2>
{button_html}            <p><strong>{escaped_chapter_label}: {escaped_chapter_title}</strong> in <em>{escaped_book_title}</em> gives the detailed explanations, practical examples and implementation patterns behind this summary.</p>

            <p>This whitepaper{area_sentence} is one of {book_overview['chapters_count']} drawn from the manuscript.</p>
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
    chapter_files: list[Path] = []
    missing_files: list[str] = []

    for filename in get_whitepaper_chapter_files():
        candidate = docs_dir / filename
        if candidate.exists():
            chapter_files.append(candidate)
        else:
            print(
                f"WARNING: Chapter file {filename} referenced by navigation is missing on disk"
            )
            missing_files.append(filename)

    print(
        f"Resolved {len(chapter_files)} markdown files via canonical navigation (missing: {len(missing_files)})"
    )
    print(f"Chapter mapping contains {len(chapter_mapping)} entries")
    
    generated_count = 0
    skipped_files = []
    error_files = []
    
    for chapter_path in chapter_files:
        filename = chapter_path.name

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
        chapter_data = read_chapter_content(chapter_path)
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
            whitepapers_dir,
            chapter_file=filename,
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
                secondary_dir,
                chapter_file=filename,
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
