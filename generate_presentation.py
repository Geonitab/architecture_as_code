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
from pathlib import Path
import json

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
            content = mmd_file.read_text(encoding='utf-8').strip()
            first_lines = content.split('\n')[:3]  # Check first 3 lines
            
            diagram_type = 'other'
            
            for line in first_lines:
                line = line.strip().lower()
                if line.startswith('graph ') or line.startswith('flowchart '):
                    diagram_type = 'flowchart'
                    break
                elif line.startswith('sequencediagram'):
                    diagram_type = 'sequence'
                    break
                elif line.startswith('classdiagram'):
                    diagram_type = 'class'
                    break
                elif line.startswith('statediagram'):
                    diagram_type = 'state'
                    break
                elif line.startswith('erdiagram'):
                    diagram_type = 'entity_relationship'
                    break
                elif line.startswith('journey'):
                    diagram_type = 'user_journey'
                    break
                elif line.startswith('gantt'):
                    diagram_type = 'gantt'
                    break
                elif line.startswith('pie'):
                    diagram_type = 'pie'
                    break
                elif line.startswith('quadrantchart'):
                    diagram_type = 'quadrant'
                    break
                elif line.startswith('requirementdiagram'):
                    diagram_type = 'requirement'
                    break
                elif line.startswith('gitgraph'):
                    diagram_type = 'gitgraph'
                    break
                elif line.startswith('mindmap'):
                    diagram_type = 'mindmap'
                    break
                elif line.startswith('timeline'):
                    diagram_type = 'timeline'
                    break
                elif line.startswith('sankey'):
                    diagram_type = 'sankey'
                    break
                elif line.startswith('xychart'):
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

def validate_chapter_diagrams():
    """Validate that each chapter has at least one diagram."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return {}
    
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    validation_results = {
        'chapters_with_diagrams': [],
        'chapters_without_diagrams': [],
        'total_chapters': 0,
        'chapters_with_diagram_count': 0
    }
    
    for chapter_file in chapter_files:
        chapter_name = Path(chapter_file).name
        
        # Skip non-chapter files
        if chapter_name in ['README.md', 'arkitektur_som_kod.md', 'BOOK_COVER_DESIGN.md']:
            continue
            
        validation_results['total_chapters'] += 1
        
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for diagram references
            has_diagram = False
            diagram_refs = []
            
            for line in content.split('\n'):
                if line.startswith('![') and 'images/' in line:
                    match = re.search(r'!\[.*?\]\((.*?)\)', line)
                    if match:
                        diagram_refs.append(match.group(1))
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
    diagram_info['source'] = f"Källa: {mmd_filename}"
    
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
                    diagram_info['type'] = 'Flödesschema'
                    diagram_info['purpose'] = 'Visualiserar processflöde och systemarbetsflöde'
                    diagram_type_found = True
                    break
                elif line.startswith('sequencediagram'):
                    diagram_info['type'] = 'Sekvensdiagram'
                    diagram_info['purpose'] = 'Visar interaktionssekvenser och meddelandeflöden'
                    diagram_type_found = True
                    break
                elif line.startswith('classdiagram'):
                    diagram_info['type'] = 'Klassdiagram'
                    diagram_info['purpose'] = 'Beskriver objektrelationer och systemstruktur'
                    diagram_type_found = True
                    break
                elif line.startswith('erdiagram'):
                    diagram_info['type'] = 'ER-diagram'
                    diagram_info['purpose'] = 'Visualiserar datamodellrelationer och entiteter'
                    diagram_type_found = True
                    break
                elif line.startswith('journey'):
                    diagram_info['type'] = 'Användarresa'
                    diagram_info['purpose'] = 'Kartlägger användarupplevelse och kontaktpunkter'
                    diagram_type_found = True
                    break
                elif line.startswith('gantt'):
                    diagram_info['type'] = 'Gantt-schema'
                    diagram_info['purpose'] = 'Presenterar projekttidslinjer och schemaläggning'
                    diagram_type_found = True
                    break
                elif line.startswith('pie'):
                    diagram_info['type'] = 'Cirkeldiagram'
                    diagram_info['purpose'] = 'Visar fördelning och procentuella uppdelningar'
                    diagram_type_found = True
                    break
                elif line.startswith('quadrantchart'):
                    diagram_info['type'] = 'Kvadrantdiagram'
                    diagram_info['purpose'] = 'Illustrerar beslutsmatriser och positionering'
                    diagram_type_found = True
                    break
                elif line.startswith('mindmap'):
                    diagram_info['type'] = 'Mindmap'
                    diagram_info['purpose'] = 'Strukturerar konceptuella relationer och kunskapskartor'
                    diagram_type_found = True
                    break
            
            if not diagram_type_found:
                diagram_info['type'] = 'Arkitekturdiagram'
                diagram_info['purpose'] = 'Visualiserar systemarkitektur och komponenter'
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
        if 'kapitel' in png_filename.lower():
            chapter_num = re.search(r'kapitel(\d+)', png_filename.lower())
            if chapter_num:
                diagram_info['explanation'] = f"Diagram: Kapitel {chapter_num.group(1)} - {diagram_info['purpose']}"
            else:
                diagram_info['explanation'] = f"Diagram: {diagram_info['purpose']}"
        else:
            diagram_info['explanation'] = f"Diagram: {diagram_info['purpose']}"
        
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
        
        # Extract diagram path - support multiple images, pick the first one
        diagram_path = None
        diagram_metadata = None
        for line in lines:
            if line.startswith('![') and 'images/' in line:
                # Extract diagram path from markdown image syntax
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    relative_path = match.group(1)
                    # Convert to absolute path from script location
                    if relative_path.endswith('.png'):
                        diagram_path = os.path.join("docs", relative_path)
                        # Extract metadata for this diagram
                        diagram_metadata = extract_diagram_metadata(diagram_path, content)
                        # Take the first diagram found
                        break
        
        # Extract key points with 20-word limit for presentation slides
        key_points = []
        current_section = None
        section_content = []
        in_code_block = False
        
        for line in lines:
            line = line.strip()
            
            # Handle code blocks
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
                
            if line.startswith('## '):
                # Process previous section
                if current_section and section_content:
                    # Get the first meaningful sentence and limit to 20 words
                    meaningful_content = []
                    for content_line in section_content:
                        if (content_line and 
                            not content_line.startswith('#') and 
                            not content_line.startswith('![') and
                            not content_line.startswith('```') and
                            len(content_line.strip()) > 20):
                            meaningful_content.append(content_line)
                    
                    if meaningful_content:
                        # Take first sentence or meaningful phrase, limit to 20 words
                        first_sentence = meaningful_content[0].split('.')[0].strip()
                        if not first_sentence:
                            first_sentence = meaningful_content[0][:150]  # Fallback to character limit
                        
                        limited_point = limit_words(first_sentence, 20)
                        key_points.append(limited_point)
                
                current_section = line[3:].strip()
                section_content = []
            elif line and current_section:
                section_content.append(line)
        
        # Add last section
        if current_section and section_content:
            meaningful_content = []
            for content_line in section_content:
                if (content_line and 
                    not content_line.startswith('#') and 
                    not content_line.startswith('![') and
                    not content_line.startswith('```') and
                    len(content_line.strip()) > 20):
                    meaningful_content.append(content_line)
            
            if meaningful_content:
                first_sentence = meaningful_content[0].split('.')[0].strip()
                if not first_sentence:
                    first_sentence = meaningful_content[0][:150]
                
                limited_point = limit_words(first_sentence, 20)
                key_points.append(limited_point)
        
        # Ensure we have at least 5 key points but no more than 10, all with 20-word limit
        while len(key_points) < 5 and len(key_points) > 0:
            # Add some general points if we don't have enough, all limited to 20 words
            if len(key_points) == 1:
                key_points.append(limit_words(f"Praktisk implementation av {title.lower()} i svenska organisationer", 20))
            elif len(key_points) == 2:
                key_points.append(limit_words(f"Säkerhetsaspekter och best practices inom {title.lower()}", 20))
            elif len(key_points) == 3:
                key_points.append(limit_words(f"Automatisering och CI/CD för {title.lower()}", 20))
            elif len(key_points) == 4:
                key_points.append(limit_words(f"Kostnadsoptimering och skalbarhet för {title.lower()}", 20))
        
        return {
            'title': title,
            'key_points': key_points[:10],  # Limit to 10 key points max, each with 20-word limit
            'diagram_path': diagram_path,
            'diagram_metadata': diagram_metadata
        }
    
    except Exception as e:
        print(f"Error reading {chapter_file}: {e}")
        return None

def generate_presentation_outline():
    """Generate presentation outline from all book chapters."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("Error: docs/ directory not found")
        return False
    
    # Find all chapter markdown files
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    
    presentation_data = []
    
    for chapter_file in chapter_files:
        if Path(chapter_file).name in ['README.md', 'arkitektur_som_kod.md']:
            continue  # Skip non-chapter files
            
        chapter_data = read_chapter_content(chapter_file)
        if chapter_data:
            presentation_data.append({
                'file': Path(chapter_file).name,
                'chapter': chapter_data
            })
    
    return presentation_data

def create_presentation_script(presentation_data):
    """Create a script that would generate the PowerPoint presentation."""
    script_content = '''#!/usr/bin/env python3
"""
PowerPoint Presentation Generator for Arkitektur som kod
Generated automatically from book content.
Complies with Swedish standards and book theme.
All key points limited to 20 words maximum per slide.
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE

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

def create_presentation():
    """Create PowerPoint presentation with book content."""
    prs = Presentation()
    
    # Set up Swedish theme colors (inspired by Swedish flag and professional standards)
    # Blue: #006AA7 (Swedish blue), Yellow: #FECC00 (Swedish yellow), Gray: #333333
    
    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Arkitektur som kod"
    subtitle.text = "En omfattande guide för svenska organisationer"
    
    # Style the title slide
    title.text_frame.paragraphs[0].font.size = Pt(44)
    title.text_frame.paragraphs[0].font.bold = True
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
    
    subtitle.text_frame.paragraphs[0].font.size = Pt(24)
    subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(51, 51, 51)  # Dark gray

'''
    
    for item in presentation_data:
        chapter = item['chapter']
        diagram_path = chapter.get('diagram_path', '')
        diagram_metadata = chapter.get('diagram_metadata', {})
        
        # Escape quotes and clean text for Python string generation
        clean_title = chapter['title'].replace('"', '\\"').replace("'", "\\'")
        
        script_content += f'''
    # Chapter: {clean_title}
    slide_layout = prs.slide_layouts[6]  # Blank layout for custom positioning
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "{clean_title}"
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
    
'''
        
        # Add diagram if available
        if diagram_path:
            diagram_source = diagram_metadata.get('source', 'Källa: diagram').replace('"', '\\"').replace("'", "\\'")
            diagram_explanation = diagram_metadata.get('explanation', '').replace('"', '\\"').replace("'", "\\'")
            
            script_content += f'''
    # Add diagram with reference and explanation
    diagram_path = "{diagram_path}"
    if os.path.exists(diagram_path):
        try:
            slide.shapes.add_picture(diagram_path, Inches(0.5), Inches(1.2), Inches(4), Inches(3))
            
            # Add diagram reference and explanation
            diagram_ref_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.4), Inches(4), Inches(0.8))
            diagram_ref_frame = diagram_ref_box.text_frame
            diagram_ref_frame.text = "{diagram_source}"
            diagram_ref_frame.paragraphs[0].font.size = Pt(10)
            diagram_ref_frame.paragraphs[0].font.color.rgb = RGBColor(102, 102, 102)  # Gray
            
            # Add diagram explanation
            if "{diagram_explanation}":
                p = diagram_ref_frame.add_paragraph()
                p.text = "{diagram_explanation}"
                p.font.size = Pt(10)
                p.font.color.rgb = RGBColor(51, 51, 51)  # Dark gray
        except Exception as e:
            print(f"Warning: Could not add diagram {{diagram_path}}: {{e}}")
    
'''
        
        script_content += '''
    # Add key points
    points_box = slide.shapes.add_textbox(Inches(5), Inches(1.2), Inches(4.5), Inches(6))
    points_frame = points_box.text_frame
    points_frame.text = "Viktiga punkter:"
    points_frame.paragraphs[0].font.size = Pt(16)
    points_frame.paragraphs[0].font.bold = True
    points_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
    
'''
        
        for i, point in enumerate(chapter['key_points']):
            # Ensure each point is limited to 20 words and clean for code generation
            clean_point = limit_words(point, 20).replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
            
            script_content += f'''
    p = points_frame.add_paragraph()
    p.text = "• {clean_point}"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(51, 51, 51)  # Dark gray
'''
    
    script_content += '''
    
    # Save presentation
    output_path = "arkitektur_som_kod_presentation.pptx"
    prs.save(output_path)
    print(f"✅ Presentation saved to {output_path}")
    print(f"📊 Total slides created: {len(prs.slides)}")
    print("🎨 Styled with Swedish theme colors")
    print("📋 Each slide includes chapter title, diagram (when available), and key points")
    print("📏 All key points limited to 20 words maximum for optimal readability")
    print("🔗 All diagrams include source references and explanatory captions")
    print("📖 Diagram explanations provide context and purpose within 20-word limit")

if __name__ == "__main__":
    create_presentation()
'''
    
    return script_content

def create_presentation_directly(presentation_data, output_path="arkitektur_som_kod_presentation.pptx"):
    """Create PowerPoint presentation directly without generating a script."""
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
    except ImportError:
        print("❌ Error: python-pptx library not installed")
        print("   Install with: pip install python-pptx>=0.6.21")
        return False
    
    try:
        prs = Presentation()
        
        # Set up Swedish theme colors (inspired by Swedish flag and professional standards)
        # Blue: #006AA7 (Swedish blue), Yellow: #FECC00 (Swedish yellow), Gray: #333333
        
        # Title slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = "Arkitektur som kod"
        subtitle.text = "En omfattande guide för svenska organisationer"
        
        # Style the title slide
        title.text_frame.paragraphs[0].font.size = Pt(44)
        title.text_frame.paragraphs[0].font.bold = True
        title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
        
        subtitle.text_frame.paragraphs[0].font.size = Pt(24)
        subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(51, 51, 51)  # Dark gray
        
        # Create slides for each chapter
        for item in presentation_data:
            chapter = item['chapter']
            diagram_path = chapter.get('diagram_path', '')
            diagram_metadata = chapter.get('diagram_metadata', {})
            
            # Chapter slide
            slide_layout = prs.slide_layouts[6]  # Blank layout for custom positioning
            slide = prs.slides.add_slide(slide_layout)
            
            # Add title
            title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
            title_frame = title_box.text_frame
            title_frame.text = chapter['title']
            title_frame.paragraphs[0].font.size = Pt(32)
            title_frame.paragraphs[0].font.bold = True
            title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
            
            # Add diagram if available
            if diagram_path and os.path.exists(diagram_path):
                try:
                    slide.shapes.add_picture(diagram_path, Inches(0.5), Inches(1.2), Inches(4), Inches(3))
                    
                    # Add diagram reference and explanation
                    diagram_ref_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.4), Inches(4), Inches(0.8))
                    diagram_ref_frame = diagram_ref_box.text_frame
                    diagram_ref_frame.text = diagram_metadata.get('source', 'Källa: diagram')
                    diagram_ref_frame.paragraphs[0].font.size = Pt(10)
                    diagram_ref_frame.paragraphs[0].font.color.rgb = RGBColor(102, 102, 102)  # Gray
                    
                    # Add diagram explanation
                    if diagram_metadata.get('explanation'):
                        p = diagram_ref_frame.add_paragraph()
                        p.text = diagram_metadata.get('explanation')
                        p.font.size = Pt(10)
                        p.font.color.rgb = RGBColor(51, 51, 51)  # Dark gray
                        
                except Exception as e:
                    print(f"Warning: Could not add diagram {diagram_path}: {e}")
            
            # Add key points
            points_box = slide.shapes.add_textbox(Inches(5), Inches(1.2), Inches(4.5), Inches(6))
            points_frame = points_box.text_frame
            points_frame.text = "Viktiga punkter:"
            points_frame.paragraphs[0].font.size = Pt(16)
            points_frame.paragraphs[0].font.bold = True
            points_frame.paragraphs[0].font.color.rgb = RGBColor(0, 106, 167)  # Swedish blue
            
            for point in chapter['key_points']:
                p = points_frame.add_paragraph()
                # Ensure each point is limited to 20 words
                limited_point = limit_words(point, 20)
                p.text = f"• {limited_point}"
                p.font.size = Pt(12)
                p.font.color.rgb = RGBColor(51, 51, 51)  # Dark gray
        
        # Save presentation
        prs.save(output_path)
        print(f"✅ Presentation saved to {output_path}")
        print(f"📊 Total slides created: {len(prs.slides)}")
        print("🎨 Styled with Swedish theme colors")
        print("📋 Each slide includes chapter title, diagram (when available), and key points")
        print("📏 All key points limited to 20 words maximum for optimal readability")
        print("🔗 All diagrams include source references and explanatory captions")
        print("📖 Diagram explanations provide context and purpose within 20-word limit")
        return True
        
    except Exception as e:
        print(f"❌ Error creating PowerPoint presentation: {e}")
        return False

def main():
    """Main function to generate presentation materials."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PowerPoint presentation from book chapters")
    parser.add_argument("--create-pptx", action="store_true", 
                       help="Create PowerPoint file directly (requires python-pptx)")
    parser.add_argument("--output", default="arkitektur_som_kod_presentation.pptx",
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
    
    # Create presentation outline
    outline_content = "# Presentation Outline\n\n"
    outline_content += "This presentation is generated from the book chapters in docs/\n\n"
    
    for item in presentation_data:
        chapter = item['chapter']
        outline_content += f"## {chapter['title']}\n\n"
        for point in chapter['key_points']:
            outline_content += f"- {point}\n"
        outline_content += "\n"
    
    # Write outline (outside docs directory)
    with open(presentations_dir / "presentation_outline.md", 'w', encoding='utf-8') as f:
        f.write(outline_content)
    
    # Create PowerPoint generator script
    pptx_script = create_presentation_script(presentation_data)
    with open(presentations_dir / "generate_pptx.py", 'w', encoding='utf-8') as f:
        f.write(pptx_script)
    
    # Create requirements file for presentation generation
    requirements = "python-pptx>=0.6.21\n"
    with open(presentations_dir / "requirements.txt", 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ Presentation materials generated in presentations/ directory:")
    print("   - presentation_outline.md")
    print("   - generate_pptx.py")
    print("   - requirements.txt")
    
    # If --create-pptx flag is provided, create the PowerPoint file directly
    if args.create_pptx:
        print("\n📊 Creating PowerPoint file directly...")
        output_path = presentations_dir / args.output
        if create_presentation_directly(presentation_data, output_path):
            print(f"✅ PowerPoint file created: {output_path}")
            
            # In release mode, also copy to standard location for backward compatibility
            if args.release:
                import shutil
                standard_dir = Path("presentations")
                standard_dir.mkdir(exist_ok=True)
                shutil.copy2(output_path, standard_dir / args.output)
                print(f"Presentation also copied to standard location: {standard_dir / args.output}")
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
    
    print("\n🚫 No files in docs/ directory were modified.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())