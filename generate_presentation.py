#!/usr/bin/env python3
"""
Generate PowerPoint presentation from book chapters.

This script reads the markdown files from docs/ directory (without modifying them)
and creates a PowerPoint presentation in the presentations/ directory.

Usage:
    python generate_presentation.py

Note: This script ONLY reads from docs/ and creates files outside the docs/ directory.
It should never modify any files in the docs/ directory.
"""

import os
import sys
import glob
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
        
        # Extract key points (headers and first paragraph of each section)
        key_points = []
        current_section = None
        paragraph_buffer = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('## '):
                if current_section and paragraph_buffer:
                    # Add previous section summary
                    summary = ' '.join(paragraph_buffer)[:200] + "..."
                    key_points.append(f"**{current_section}**: {summary}")
                current_section = line[3:].strip()
                paragraph_buffer = []
            elif line and not line.startswith('#') and not line.startswith('![') and current_section:
                if len(paragraph_buffer) < 2:  # Only first few lines
                    paragraph_buffer.append(line)
        
        # Add last section
        if current_section and paragraph_buffer:
            summary = ' '.join(paragraph_buffer)[:200] + "..."
            key_points.append(f"**{current_section}**: {summary}")
        
        return {
            'title': title,
            'key_points': key_points[:10]  # Limit to 10 key points as requested
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
PowerPoint Presentation Generator
Generated automatically from book content.
"""

# Note: This would require python-pptx library
# pip install python-pptx

from pptx import Presentation
from pptx.util import Inches

def create_presentation():
    """Create PowerPoint presentation with book content."""
    prs = Presentation()
    
    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Arkitektur som kod"
    subtitle.text = "En omfattande guide för svenska organisationer"
    
'''
    
    for item in presentation_data:
        chapter = item['chapter']
        script_content += f'''
    # Chapter: {chapter['title']}
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "{chapter['title']}"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
'''
        
        for i, point in enumerate(chapter['key_points']):
            # Clean the point for code generation
            clean_point = point.replace('"', '\\"').replace('\n', ' ')[:100] + "..."
            script_content += f'''    
    p = text_frame.add_paragraph()
    p.text = "• {clean_point}"
'''
    
    script_content += '''
    
    # Save presentation
    prs.save("presentations/arkitektur_som_kod_presentation.pptx")
    print("Presentation saved to presentations/arkitektur_som_kod_presentation.pptx")

if __name__ == "__main__":
    create_presentation()
'''
    
    return script_content

def main():
    """Main function to generate presentation materials."""
    print("Analyzing book content to generate presentation...")
    
    # Ensure presentations directory exists
    presentations_dir = Path("presentations")
    presentations_dir.mkdir(exist_ok=True)
    
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
    print("\n📝 To create the PowerPoint file:")
    print("   cd presentations")
    print("   pip install -r requirements.txt")
    print("   python generate_pptx.py")
    print("\n🚫 No files in docs/ directory were modified.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())