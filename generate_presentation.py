#!/usr/bin/env python3
"""
Generate PowerPoint presentation from book chapters with comprehensive diagram validation.

This script reads the markdown files from docs/ directory (without modifying them)
and creates a PowerPoint presentation in the presentations/ directory.

Enhanced Features:
- Validates that each chapter has at least one diagram
- Ensures all types of Mermaid diagrams are represented across the presentation
- Provides comprehensive diagram type analysis and reporting
- Supports validation-only mode for checking coverage without generation

Supported Mermaid Diagram Types:
- Flowchart (graph LR/TB): Process flows and system workflows
- Sequence Diagram: Interaction sequences and message flows
- Class Diagram: Object relationships and system structure
- Entity Relationship: Data model relationships
- User Journey: User experience flows and touchpoints
- Gantt Chart: Project timelines and scheduling
- Pie Chart: Distribution and percentage breakdowns
- Quadrant Chart: Decision matrices and positioning
- Mindmap: Conceptual relationships and knowledge mapping
- And more...

Usage:
    python generate_presentation.py                    # Generate presentation materials
    python generate_presentation.py --create-pptx      # Generate PowerPoint file directly
    python generate_presentation.py --validate-diagrams # Validate diagram coverage only
    python generate_presentation.py --create-pptx --validate-diagrams  # Full generation with validation

Note: This script ONLY reads from docs/ and creates files outside the docs/ directory.
It should never modify any files in the docs/ directory.
"""

import os
import sys
import glob
import re
import unicodedata
from datetime import datetime
from pathlib import Path
import json
import importlib.util
from types import SimpleNamespace

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency check
    print("❌ Error: PyYAML library not installed")
    print("   Install with: pip install PyYAML>=6.0")
    sys.exit(1)

_PPTX_SPEC = importlib.util.find_spec("pptx")
PPTX_AVAILABLE = _PPTX_SPEC is not None

if PPTX_AVAILABLE:
    from pptx import Presentation
else:  # pragma: no cover - optional dependency shim
    Presentation = None

import presentation_deck


def ensure_pptx_available():
    """Raise a helpful error when python-pptx is required but missing."""

    if not PPTX_AVAILABLE:
        raise RuntimeError(
            "python-pptx is required for PowerPoint generation. "
            "Install it with 'pip install python-pptx>=0.6.21'."
        )

def build_presentation_document(prs, presentation_data):
    """Render the deck in the graphic profile of the book (see presentation_deck.py)."""
    ensure_pptx_available()
    return presentation_deck.build_deck(prs, presentation_data)


def generate_presentation_outline():
    """Read the book (parts and chapters from docs/book_index.json) into deck data."""
    deck = presentation_deck.collect_deck()
    for entry in deck:
        if entry.get("type") == "chapter":
            chapter = entry["chapter"]
            chapter["key_points"] = list(chapter.get("sections", []))
        elif entry.get("type") == "part":
            entry["part"]["key_points"] = [
                f"Chapter {c['identifier']}: {c['title']}" for c in entry["part"].get("chapters", [])
            ]
    return deck



def limit_words(text, max_words=20):
    """Limit text to maximum number of words while preserving meaning."""
    if not text:
        return text

    words = text.split()
    if len(words) <= max_words:
        return text

    # Take the first max_words and add ellipsis if needed
    limited = ' '.join(words[:max_words])
    if len(words) > max_words:
        limited += "..."

    return limited


def _slugify_heading(text):
    """Convert a heading into an anchor-friendly slug similar to MkDocs."""
    if not text:
        return ""

    normalised = unicodedata.normalize("NFKD", text).strip().lower()
    # Remove combining characters and unsupported punctuation
    without_diacritics = "".join(ch for ch in normalised if not unicodedata.combining(ch))
    cleaned = re.sub(r"[^0-9a-z\s-]", "", without_diacritics)
    slug = re.sub(r"[\s-]+", "-", cleaned).strip("-")
    return slug


def _collect_highlights_from_lines(lines, minimum_length=20):
    """Extract highlight sentences from markdown lines using section structure."""
    key_points = []
    current_section = None
    section_content = []
    in_code_block = False

    for raw_line in lines:
        line = raw_line.strip()

        if line.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        if line.startswith('## '):
            if current_section and section_content:
                meaningful = [
                    candidate.strip()
                    for candidate in section_content
                    if candidate
                    and not candidate.startswith('#')
                    and not candidate.startswith('![')
                    and not candidate.startswith('```')
                    and len(candidate.strip()) > minimum_length
                ]

                if meaningful:
                    first_sentence = meaningful[0].split('.')[0].strip() or meaningful[0][:150]
                    key_points.append(limit_words(first_sentence, 20))

            current_section = line[3:].strip()
            section_content = []
        elif line and current_section:
            section_content.append(line)

    if current_section and section_content:
        meaningful = [
            candidate.strip()
            for candidate in section_content
            if candidate
            and not candidate.startswith('#')
            and not candidate.startswith('![')
            and not candidate.startswith('```')
            and len(candidate.strip()) > minimum_length
        ]

        if meaningful:
            first_sentence = meaningful[0].split('.')[0].strip() or meaningful[0][:150]
            key_points.append(limit_words(first_sentence, 20))

    return key_points


def _load_maturity_aspects(html_path: Path):
    """Extract maturity radar aspects from the standalone HTML tool."""
    if not html_path.exists():
        return []

    text = html_path.read_text(encoding="utf-8")
    match = re.search(r"const\s+aspects\s*=\s*(\[[\s\S]*?\]);", text)
    if not match:
        return []

    aspects_block = match.group(1)
    aspects_block = re.sub(r"(?m)(\s*)([A-Za-z_][A-Za-z0-9_]*):", r'\1"\2":', aspects_block)

    try:
        return json.loads(aspects_block)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive guardrail
        print("⚠️  Unable to parse maturity radar configuration:", exc)
        return []


def generate_prezi_slides(output_path=Path("docs/prezi/slides.json")):
    """Generate slides.json for the Prezi-style presentation."""
    prezi_dir = output_path.parent
    prezi_dir.mkdir(parents=True, exist_ok=True)

    aspects = _load_maturity_aspects(Path("docs/maturity_model_radar.html"))
    if not aspects:
        output_path.write_text("[]", encoding="utf-8")
        return output_path, 0

    slides = []
    x = y = 0
    col_w, row_h, cols = 620, 460, 4

    for aspect in aspects:
        aspect_key = aspect.get("key") or "aspect"
        slide_id = f"maturity-{aspect_key}"
        slides.append(
            {
                "id": slide_id,
                "title": aspect.get("name", "Maturity aspect"),
                "mdPath": f"/maturity_model_radar.html#{aspect_key}",
                "x": x,
                "y": y,
                "zoom": 1,
            }
        )

        for question_index, question in enumerate(aspect.get("questions", []), start=1):
            zero_based = question_index - 1
            slides.append(
                {
                    "id": f"{slide_id}--{question_index}",
                    "title": question,
                    "mdPath": f"/maturity_model_radar.html#{aspect_key}_{zero_based}",
                    "x": x + 220 + ((question_index - 1) % 2) * 160,
                    "y": y + 140 + ((question_index - 1) // 2) * 120,
                    "zoom": 1,
                    "parentId": slide_id,
                }
            )

        x += col_w
        if x > col_w * (cols - 1):
            x = 0
            y += row_h

    output_path.write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path, len(slides)

def analyze_mermaid_diagram_types():
    """Analyze available Mermaid diagram types in the images directory."""
    diagram_types = {
        'flowchart': [],      # graph LR, graph TD, graph TB
        'sequence': [],       # sequenceDiagram
        'class': [],          # classDiagram
        'state': [],          # stateDiagram
        'entity_relationship': [], # erDiagram
        'user_journey': [],   # journey
        'gantt': [],          # gantt
        'pie': [],            # pie
        'quadrant': [],       # quadrantChart
        'requirement': [],    # requirementDiagram
        'gitgraph': [],       # gitGraph
        'mindmap': [],        # mindmap
        'timeline': [],       # timeline
        'sankey': [],         # sankey
        'xy_chart': [],       # xyChart
        'other': []
    }
    
    images_dir = Path("docs/images")
    if not images_dir.exists():
        return diagram_types
    
    mermaid_files = list(images_dir.glob("*.mmd"))

    for mmd_file in mermaid_files:
        try:
            content = mmd_file.read_text(encoding='utf-8').split('\n')

            filtered_lines = []
            in_front_matter = False

            for raw_line in content:
                stripped = raw_line.strip()

                if not stripped:
                    continue

                if stripped == '---':
                    in_front_matter = not in_front_matter
                    continue

                if in_front_matter:
                    continue

                if stripped.startswith('%%'):
                    continue

                filtered_lines.append(stripped.lower())
                if len(filtered_lines) >= 20:
                    break

            diagram_type = 'other'

            for line in filtered_lines:
                if line.startswith('graph ') or line.startswith('flowchart '):
                    diagram_type = 'flowchart'
                    break
                if line.startswith('sequencediagram'):
                    diagram_type = 'sequence'
                    break
                if line.startswith('classdiagram'):
                    diagram_type = 'class'
                    break
                if line.startswith('statediagram'):
                    diagram_type = 'state'
                    break
                if line.startswith('erdiagram'):
                    diagram_type = 'entity_relationship'
                    break
                if line.startswith('journey'):
                    diagram_type = 'user_journey'
                    break
                if line.startswith('gantt'):
                    diagram_type = 'gantt'
                    break
                if line.startswith('pie'):
                    diagram_type = 'pie'
                    break
                if line.startswith('quadrantchart'):
                    diagram_type = 'quadrant'
                    break
                if line.startswith('requirementdiagram'):
                    diagram_type = 'requirement'
                    break
                if line.startswith('gitgraph'):
                    diagram_type = 'gitgraph'
                    break
                if line.startswith('mindmap'):
                    diagram_type = 'mindmap'
                    break
                if line.startswith('timeline'):
                    diagram_type = 'timeline'
                    break
                if line.startswith('sankey'):
                    diagram_type = 'sankey'
                    break
                if line.startswith('xychart'):
                    diagram_type = 'xy_chart'
                    break

            diagram_types[diagram_type].append(str(mmd_file))

        except Exception as e:
            print(f"Warning: Could not analyze {mmd_file}: {e}")
    
    return diagram_types

def get_missing_diagram_types():
    """Identify which Mermaid diagram types are missing from the collection."""
    diagram_analysis = analyze_mermaid_diagram_types()
    
    # Define essential diagram types for a comprehensive presentation
    essential_types = [
        'flowchart', 'sequence', 'class', 'entity_relationship', 
        'user_journey', 'gantt', 'pie', 'quadrant', 'mindmap'
    ]
    
    missing_types = []
    available_types = []
    
    for diagram_type in essential_types:
        if not diagram_analysis.get(diagram_type):
            missing_types.append(diagram_type)
        else:
            available_types.append(diagram_type)
    
    return {
        'missing': missing_types,
        'available': available_types,
        'analysis': diagram_analysis
    }

def _iter_primary_markdown_files(docs_dir: Path):
    """Return top-level markdown files and one-level nested index.md pages."""
    files = list(docs_dir.glob("*.md"))
    files.extend(docs_dir.glob("*/index.md"))

    seen = set()
    ordered = []
    for path in files:
        key = str(path.relative_to(docs_dir))
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path)

    ordered.sort(key=lambda p: str(p.relative_to(docs_dir)))
    return ordered

def validate_presentation_guidelines(presentation_data):
    """Validate that presentation follows PRESENTATION_DESIGN_GUIDELINES.md standards.
    
    Checks:
    - Minimum text sizes (18pt body, 36pt titles)
    - Maximum bullet points per slide (4 hero, 8 side)
    - Maximum words per bullet point (20 words)
    - Colour contrast requirements
    - Diagram metadata presence
    """
    issues = []
    warnings = []
    
    for idx, entry in enumerate(presentation_data):
        entry_type = entry.get('type')
        slide_num = idx + 1
        
        if entry_type == 'chapter':
            chapter = entry.get('chapter', {})
            key_points = chapter.get('key_points', [])
            
            # Check maximum words per bullet point
            for point_idx, point in enumerate(key_points):
                word_count = len(point.split())
                if word_count > 20:
                    warnings.append(
                        f"Slide {slide_num}: Bullet point {point_idx + 1} has {word_count} words "
                        f"(maximum 20 recommended per PRESENTATION_DESIGN_GUIDELINES.md)"
                    )
            
            # Check diagram metadata presence
            diagram_path = chapter.get('diagram_path')
            diagram_metadata = chapter.get('diagram_metadata')
            if diagram_path and not diagram_metadata:
                issues.append(
                    f"Slide {slide_num}: Diagram present but missing metadata "
                    f"(type, source, explanation required per PRESENTATION_DESIGN_GUIDELINES.md)"
                )
            
            # Check bullet point limits (4 for hero, 8 for side)
            layout_style = 'hero' if slide_num % 2 == 1 else 'side'
            max_points = 4 if layout_style == 'hero' else 8
            if len(key_points) > max_points:
                warnings.append(
                    f"Slide {slide_num}: {len(key_points)} bullet points exceeds "
                    f"recommended maximum of {max_points} for {layout_style} layout"
                )
    
    return {
        'issues': issues,
        'warnings': warnings,
        'compliant': len(issues) == 0
    }

def validate_chapter_diagrams():
    """Validate that each chapter has at least one diagram."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return {}

    chapter_files = _iter_primary_markdown_files(docs_dir)
    canonical_filenames = _load_canonical_chapter_filenames()
    validation_results = {
        'chapters_with_diagrams': [],
        'chapters_without_diagrams': [],
        'total_chapters': 0,
        'chapters_with_diagram_count': 0
    }
    
    for chapter_file in chapter_files:
        chapter_rel = chapter_file.relative_to(docs_dir)
        chapter_name = str(chapter_rel)

        # Skip files that are not part of the canonical manuscript
        if canonical_filenames:
            if chapter_name not in canonical_filenames:
                continue
        else:
            # Fallback filters if requirements file is unavailable
            if chapter_name.startswith('part_'):
                continue

        if chapter_name in ['README.md', 'architecture_as_code.md']:
            continue

        validation_results['total_chapters'] += 1
        
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for diagram references
            has_diagram = False
            diagram_refs = []
            
            for line in content.split('\n'):
                stripped = line.strip()

                if stripped.startswith('![') and 'images/' in stripped:
                    match = re.search(r'!\[.*?\]\((.*?)\)', stripped)
                    if match:
                        diagram_refs.append(match.group(1))
                        has_diagram = True
                        continue

                # Treat explicit diagram source references as diagrams even without PNG embeds
                if 'diagram source' in stripped.lower() and 'images/' in stripped:
                    matches = re.findall(r'\(images/(diagram_[^\)]+)\)', stripped, re.IGNORECASE)
                    if matches:
                        for ref in matches:
                            diagram_refs.append(f"images/{ref}")
                        has_diagram = True
            
            if has_diagram:
                validation_results['chapters_with_diagrams'].append({
                    'file': chapter_name,
                    'diagrams': diagram_refs
                })
                validation_results['chapters_with_diagram_count'] += 1
            else:
                validation_results['chapters_without_diagrams'].append(chapter_name)
                
        except Exception as e:
            print(f"Warning: Could not analyze {chapter_file}: {e}")
            validation_results['chapters_without_diagrams'].append(chapter_name)
    
    return validation_results

def extract_diagram_metadata(diagram_path, chapter_content):
    """Extract metadata and context for a diagram from its source file and chapter context."""
    diagram_info = {
        'source': None,
        'type': 'unknown',
        'purpose': None,
        'explanation': None
    }
    
    if not diagram_path:
        return diagram_info
    
    # Extract base filename and find corresponding .mmd file
    png_filename = os.path.basename(diagram_path)
    mmd_filename = png_filename.replace('.png', '.mmd')
    mmd_path = os.path.join("docs/images", mmd_filename)
    
    # Set source information
    diagram_info['source'] = f"Source: {mmd_filename}"
    
    # Try to read the mermaid source file to determine type and content
    if os.path.exists(mmd_path):
        try:
            with open(mmd_path, 'r', encoding='utf-8') as f:
                mmd_content = f.read().strip()
            
            # Determine diagram type from mermaid content - check multiple lines
            content_lines = [line.strip().lower() for line in mmd_content.split('\n') if line.strip()]
            diagram_type_found = False
            
            for line in content_lines:
                if line.startswith('graph ') or line.startswith('flowchart '):
                    diagram_info['type'] = 'Flowchart'
                    diagram_info['purpose'] = 'Illustrates process flows and system workflows'
                    diagram_type_found = True
                    break
                elif line.startswith('sequencediagram'):
                    diagram_info['type'] = 'Sequence diagram'
                    diagram_info['purpose'] = 'Shows interaction sequences and message flows'
                    diagram_type_found = True
                    break
                elif line.startswith('classdiagram'):
                    diagram_info['type'] = 'Class diagram'
                    diagram_info['purpose'] = 'Describes object relationships and system structure'
                    diagram_type_found = True
                    break
                elif line.startswith('erdiagram'):
                    diagram_info['type'] = 'Entity-relationship diagram'
                    diagram_info['purpose'] = 'Illustrates data model relationships and entities'
                    diagram_type_found = True
                    break
                elif line.startswith('journey'):
                    diagram_info['type'] = 'User journey'
                    diagram_info['purpose'] = 'Maps user experience and touchpoints'
                    diagram_type_found = True
                    break
                elif line.startswith('gantt'):
                    diagram_info['type'] = 'Gantt chart'
                    diagram_info['purpose'] = 'Presents project timelines and scheduling'
                    diagram_type_found = True
                    break
                elif line.startswith('pie'):
                    diagram_info['type'] = 'Pie chart'
                    diagram_info['purpose'] = 'Shows distribution and percentage breakdowns'
                    diagram_type_found = True
                    break
                elif line.startswith('quadrantchart'):
                    diagram_info['type'] = 'Quadrant chart'
                    diagram_info['purpose'] = 'Illustrates decision matrices and positioning'
                    diagram_type_found = True
                    break
                elif line.startswith('mindmap'):
                    diagram_info['type'] = 'Mind map'
                    diagram_info['purpose'] = 'Structures conceptual relationships and knowledge mapping'
                    diagram_type_found = True
                    break
            
            if not diagram_type_found:
                diagram_info['type'] = 'Architecture diagram'
                diagram_info['purpose'] = 'Illustrates system architecture and component relationships'
        except Exception as e:
            print(f"Warning: Could not read diagram source {mmd_path}: {e}")
    
    # Extract contextual explanation from chapter content around diagram reference
    if chapter_content and diagram_path:
        lines = chapter_content.split('\n')
        for i, line in enumerate(lines):
            if 'images/' in line and png_filename.replace('.png', '') in line:
                # Look for explanation in the line after the diagram
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('#') and not next_line.startswith('!['):
                        # Found explanation, limit to 20 words
                        diagram_info['explanation'] = limit_words(next_line, 18)  # Leave room for "Diagram:" prefix
                        break
                
                # Look for explanation in the line before the diagram
                if i > 0:
                    prev_line = lines[i - 1].strip()
                    if prev_line and not prev_line.startswith('#') and not prev_line.startswith('!['):
                        diagram_info['explanation'] = limit_words(prev_line, 18)
                        break
    
    # If no specific explanation found, create one based on diagram type and context
    if not diagram_info['explanation']:
        filename_lower = png_filename.lower()
        purpose_text = diagram_info['purpose'] or 'Highlights a key architecture concept'
        chapter_match = re.search(r'(chapter|kapitel)(\d+)', filename_lower)
        if chapter_match:
            diagram_info['explanation'] = f"Diagram: Chapter {chapter_match.group(2)} - {purpose_text}"
        else:
            diagram_info['explanation'] = f"Diagram: {purpose_text}"
        
        # Ensure it's within word limit
        diagram_info['explanation'] = limit_words(diagram_info['explanation'], 18)
    
    return diagram_info

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
        
        # Extract diagram paths - prefer flowchart representations
        diagram_path = None
        diagram_metadata = None
        selected_reference = None
        diagram_candidates = []
        for line in lines:
            if line.startswith('![') and 'images/' in line:
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    relative_path = match.group(1)
                    if relative_path.endswith('.png'):
                        full_path = os.path.join("docs", relative_path)
                        metadata = extract_diagram_metadata(full_path, content)
                        diagram_candidates.append((full_path, metadata, relative_path))

        for candidate in diagram_candidates:
            candidate_metadata = candidate[1] or {}
            diagram_type = (candidate_metadata.get('type') or '').lower()
            if 'flowchart' in diagram_type:
                diagram_path, diagram_metadata, selected_reference = candidate
                break

        if diagram_path is None and diagram_candidates:
            diagram_path, diagram_metadata, selected_reference = diagram_candidates[0]

        # Extract key points with 20-word limit for presentation slides
        key_points = _collect_highlights_from_lines(lines)
        if not key_points:
            fallback_sentence = limit_words(f"Core ideas from {title.lower()} for modern organisations", 20)
            key_points = [fallback_sentence]

        # Ensure we have at least 5 key points but no more than 10, all with 20-word limit
        while len(key_points) < 5 and len(key_points) > 0:
            # Add some general points if we don't have enough, all limited to 20 words
            if len(key_points) == 1:
                key_points.append(limit_words(f"Practical implementation of {title.lower()} across modern organisations", 20))
            elif len(key_points) == 2:
                key_points.append(limit_words(f"Security considerations and best practices for {title.lower()}", 20))
            elif len(key_points) == 3:
                key_points.append(limit_words(f"Automation and CI/CD enablers for {title.lower()}", 20))
            elif len(key_points) == 4:
                key_points.append(limit_words(f"Cost optimisation and scalability guidance for {title.lower()}", 20))
        
        selected_filename = os.path.basename(selected_reference) if selected_reference else None

        if diagram_metadata is None:
            diagram_metadata = {
                'type': 'Architecture diagram',
                'purpose': 'Highlights a key architecture concept',
                'source': 'Architecture as Code diagrams',
                'explanation': '',
            }

        # Extract contextual explanation from chapter content around diagram reference
        if content and diagram_path and selected_filename:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if selected_filename.replace('.png', '') in line and 'images/' in line:
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('#') and not next_line.startswith('!['):
                            diagram_metadata['explanation'] = limit_words(next_line, 18)
                            break

                    if i > 0:
                        prev_line = lines[i - 1].strip()
                        if prev_line and not prev_line.startswith('#') and not prev_line.startswith('!['):
                            diagram_metadata['explanation'] = limit_words(prev_line, 18)
                            break

        if not diagram_metadata.get('explanation'):
            filename_lower = (selected_filename or '').lower()
            purpose_text = diagram_metadata.get('purpose') or 'Highlights a key architecture concept'
            chapter_match = re.search(r'(chapter|kapitel)(\d+)', filename_lower)
            if chapter_match:
                diagram_metadata['explanation'] = limit_words(
                    f"Diagram: Chapter {chapter_match.group(2)} - {purpose_text}", 18
                )
            else:
                diagram_metadata['explanation'] = limit_words(f"Diagram: {purpose_text}", 18)

        notes_lines = [title]
        notes_lines.append('')
        notes_lines.append('Highlights:')
        for point in key_points[:10]:
            notes_lines.append(f"- {point}")

        if diagram_path:
            notes_lines.append('')
            diagram_type = diagram_metadata.get('type') or 'Diagram'
            notes_lines.append(f"Diagram type: {diagram_type}")
            if diagram_metadata.get('explanation'):
                notes_lines.append(diagram_metadata['explanation'])

        return {
            'title': title,
            'key_points': key_points[:10],
            'diagram_path': diagram_path,
            'diagram_metadata': diagram_metadata,
            'notes': '\n'.join(notes_lines).strip(),
        }

    except Exception as e:
        print(f"Error reading {chapter_file}: {e}")
        return None

def create_presentation_script(presentation_data):
    """Create a standalone script that renders the presentation using shared helpers."""
    script_content = '''#!/usr/bin/env python3
"""Generate the Architecture as Code presentation from cached data."""

import json
import sys
from pathlib import Path

from pptx import Presentation

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from generate_presentation import build_presentation_document

DATA_FILE = Path(__file__).with_name("presentation_data.json")


def load_presentation_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Presentation data not found: {DATA_FILE}")
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(output_path: Path) -> None:
    presentation_data = load_presentation_data()
    prs = Presentation()
    build_presentation_document(prs, presentation_data)
    prs.save(output_path)
    print(f"✅ Presentation saved to {output_path}")
    print(f"📊 Total slides created: {len(prs.slides)}")


if __name__ == "__main__":
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_FILE.with_name("architecture_as_code_presentation.pptx")
    main(target_path)
'''

    return script_content


def create_presentation_directly(presentation_data, output_path="architecture_as_code_presentation.pptx"):
    """Create PowerPoint presentation directly without generating a script."""
    if not PPTX_AVAILABLE:
        print("⚠️  python-pptx is not installed. Install it with 'pip install python-pptx>=0.6.21'.")
        print("   The script and supporting materials are still generated.")
        return "missing_dependency"

    try:
        prs = Presentation()
        build_presentation_document(prs, presentation_data)
        prs.save(output_path)
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"❌ Failed to create PowerPoint file: {exc}")
        return "error"

    print(f"✅ PowerPoint file created: {output_path}")
    print(f"📊 Total slides created: {len(prs.slides)}")
    print("🎨 Slides follow the Architecture as Code theme and 16:9 layout.")
    return "success"


def main():
    """Main function to generate presentation materials."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PowerPoint presentation from book chapters")
    parser.add_argument("--create-pptx", action="store_true", 
                       help="Create PowerPoint file directly (requires python-pptx)")
    parser.add_argument("--output", default="architecture_as_code_presentation.pptx",
                       help="Output filename for PowerPoint file")
    parser.add_argument("--validate-diagrams", action="store_true",
                       help="Validate that all chapters have diagrams and check diagram type coverage")
    parser.add_argument("--release", action="store_true",
                       help="Generate presentation materials to release folder")
    
    args = parser.parse_args()
    
    print("Analyzing book content to generate presentation...")
    
    # Diagram validation and analysis
    if args.validate_diagrams:
        print("\n🔍 Validating diagram coverage...")
        
        # Check chapter diagram coverage
        chapter_validation = validate_chapter_diagrams()
        print(f"📊 Chapter diagram analysis:")
        print(f"   - Total chapters analyzed: {chapter_validation['total_chapters']}")
        print(f"   - Chapters with diagrams: {chapter_validation['chapters_with_diagram_count']}")
        print(f"   - Coverage: {(chapter_validation['chapters_with_diagram_count']/chapter_validation['total_chapters']*100):.1f}%")
        
        if chapter_validation['chapters_without_diagrams']:
            print(f"⚠️  Chapters missing diagrams: {chapter_validation['chapters_without_diagrams']}")
        
        # Check diagram type coverage
        missing_types = get_missing_diagram_types()
        print(f"\n🎨 Mermaid diagram type analysis:")
        print(f"   - Available types: {missing_types['available']}")
        print(f"   - Missing types: {missing_types['missing']}")
        
        if missing_types['missing']:
            print(f"⚠️  Missing essential diagram types: {missing_types['missing']}")
            print("   Consider adding these types for comprehensive presentation coverage")
        
        # Detailed analysis
        print(f"\n📋 Detailed diagram inventory:")
        for diagram_type, files in missing_types['analysis'].items():
            if files:
                print(f"   - {diagram_type}: {len(files)} diagrams")
        
        print("\n" + "="*60)
    
    # Ensure presentations directory exists
    if args.release:
        presentations_dir = Path("releases/presentation")
        print("Release mode: Generating presentation materials to releases/presentation/")
    else:
        presentations_dir = Path("presentations")
    
    presentations_dir.mkdir(exist_ok=True, parents=True)
    
    # Read all chapters WITHOUT modifying them
    presentation_data = generate_presentation_outline()

    if not presentation_data:
        print("Error: Could not read chapter data")
        return 1

    print(f"Found {len(presentation_data)} chapters to include in presentation")
    
    # Validate presentation against PRESENTATION_DESIGN_GUIDELINES.md
    print("\n🎨 Validating presentation guidelines compliance...")
    validation_result = validate_presentation_guidelines(presentation_data)
    
    if validation_result['issues']:
        print("❌ Issues found:")
        for issue in validation_result['issues']:
            print(f"   - {issue}")
    
    if validation_result['warnings']:
        print("⚠️  Warnings:")
        for warning in validation_result['warnings']:
            print(f"   - {warning}")
    
    if validation_result['compliant']:
        print("✅ Presentation follows PRESENTATION_DESIGN_GUIDELINES.md standards")
    else:
        print("⚠️  Presentation has guideline compliance issues (see above)")
    
    print()

    slides_path, slide_count = generate_prezi_slides()
    if slide_count:
        print(f"✅ Prezi slides generated at {slides_path} ({slide_count} slides)")
    else:
        print(
            "⚠️ Prezi slides were not generated because the maturity radar configuration was unavailable"
        )
    
    # Create presentation outline
    outline_content = "# Presentation Outline\n\n"
    outline_content += "This presentation is generated from the book chapters in docs/\n\n"
    
    for item in presentation_data:
        item_type = item.get('type')

        if item_type == 'chapter':
            chapter = item.get('chapter') or {}
            title = chapter.get('title') or item.get('file', 'Chapter')
            outline_content += f"## {title}\n\n"
            for point in chapter.get('key_points') or []:
                outline_content += f"- {point}\n"
            outline_content += "\n"
            continue

        if item_type == 'part':
            part = item.get('part') or {}
            title = part.get('title') or item.get('file', 'Part Introduction')
            outline_content += f"## {title} (Part Introduction)\n\n"
            for point in part.get('key_points') or []:
                outline_content += f"- {point}\n"
            outline_content += "\n"
            continue

        if item_type == 'front_matter':
            front = item.get('front_matter') or {}
            title = front.get('title') or item.get('file', 'Front Matter')
            outline_content += f"## {title}\n\n"
            for point in front.get('key_points') or []:
                outline_content += f"- {point}\n"
            outline_content += "\n"
    
    # Write outline (outside docs directory)
    with open(presentations_dir / "presentation_outline.md", 'w', encoding='utf-8') as f:
        f.write(outline_content)

    data_file = presentations_dir / "presentation_data.json"
    data_file.write_text(json.dumps(presentation_data, ensure_ascii=False, indent=2), encoding='utf-8')

    # Create PowerPoint generator script
    pptx_script = create_presentation_script(presentation_data)
    with open(presentations_dir / "generate_pptx.py", 'w', encoding='utf-8') as f:
        f.write(pptx_script)
    
    # Create requirements file for presentation generation
    requirements = "\n".join(
        [
            "python-pptx>=0.6.21",
            "PyYAML>=6.0",
        ]
    ) + "\n"
    with open(presentations_dir / "requirements.txt", 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ Presentation materials generated in presentations/ directory:")
    print("   - presentation_outline.md")
    print("   - presentation_data.json")
    print("   - generate_pptx.py")
    print("   - requirements.txt")
    print("\n📐 Design standards: docs/PRESENTATION_DESIGN_GUIDELINES.md")
    print("   - 16:9 aspect ratio (1280×720px)")
    print("   - The book's own colours and typography (taken from templates/book-cover.svg)")
    print("   - Minimum 18pt body text (WCAG AA compliant)")
    print("   - Maximum 20 words per bullet point")
    
    # If --create-pptx flag is provided, create the PowerPoint file directly
    if args.create_pptx:
        print("\n📊 Creating PowerPoint file directly...")
        output_path = presentations_dir / args.output
        creation_result = create_presentation_directly(presentation_data, output_path)

        if creation_result == "success":
            print(f"✅ PowerPoint file created: {output_path}")

            # In release mode, also copy to standard location for backward compatibility
            if args.release:
                import shutil
                standard_dir = Path("presentations")
                standard_dir.mkdir(exist_ok=True)
                shutil.copy2(output_path, standard_dir / args.output)
                print(f"Presentation also copied to standard location: {standard_dir / args.output}")
        elif creation_result == "missing_dependency":
            print("⚠️  PowerPoint file not created because python-pptx is unavailable.")
            print("   Install the optional dependency to enable direct generation.")
            print("📝 You can still use the generated script:")
            print(f"   cd {presentations_dir}")
            print("   pip install -r requirements.txt")
            print("   python generate_pptx.py")
        else:
            print("❌ Failed to create PowerPoint file")
            print("📝 You can still use the generated script:")
            print(f"   cd {presentations_dir}")
            print("   pip install -r requirements.txt")
            print("   python generate_pptx.py")
            return 1
    else:
        print("\n📝 To create the PowerPoint file:")
        print(f"   cd {presentations_dir}")
        print("   pip install -r requirements.txt")
        print("   python generate_pptx.py")
        print("\n💡 Or use: python generate_presentation.py --create-pptx")
    
    print("\n📁 Prezi slide data stored in docs/prezi/slides.json.")
    print("🚫 No other files in docs/ directory were modified.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
