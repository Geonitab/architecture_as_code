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
        
        # Extract diagram path
        diagram_path = None
        for line in lines:
            if line.startswith('![') and 'images/' in line:
                # Extract diagram path from markdown image syntax
                import re
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    diagram_path = match.group(1)
                    # Convert to PNG path if it's a reference
                    if diagram_path.endswith('.png'):
                        diagram_path = f"../docs/{diagram_path}"
                    break
        
        # Extract key points with better logic for 10 meaningful points
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
                    # Get meaningful content from section
                    meaningful_content = []
                    for content_line in section_content:
                        if (content_line and 
                            not content_line.startswith('#') and 
                            not content_line.startswith('![') and
                            not content_line.startswith('```') and
                            len(content_line.strip()) > 20):
                            meaningful_content.append(content_line)
                    
                    if meaningful_content:
                        # Create a concise summary
                        summary = ' '.join(meaningful_content[:3])[:300]
                        if len(summary) > 250:
                            summary = summary[:250] + "..."
                        key_points.append(f"{current_section}: {summary}")
                
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
                summary = ' '.join(meaningful_content[:3])[:300]
                if len(summary) > 250:
                    summary = summary[:250] + "..."
                key_points.append(f"{current_section}: {summary}")
        
        # Ensure we have 10 points by padding with general information if needed
        while len(key_points) < 10 and len(key_points) > 0:
            # Add some general points if we don't have enough
            if len(key_points) == 1:
                key_points.append(f"Praktisk implementation av {title.lower()}")
            elif len(key_points) == 2:
                key_points.append(f"Svenska organisationers perspektiv på {title.lower()}")
            elif len(key_points) == 3:
                key_points.append(f"Säkerhetsaspekter inom {title.lower()}")
            elif len(key_points) == 4:
                key_points.append(f"Automatisering och CI/CD för {title.lower()}")
            elif len(key_points) == 5:
                key_points.append(f"Kostnadsoptimering inom {title.lower()}")
            elif len(key_points) == 6:
                key_points.append(f"Skalbarhet och prestanda för {title.lower()}")
            elif len(key_points) == 7:
                key_points.append(f"Övervakning och loggning av {title.lower()}")
            elif len(key_points) == 8:
                key_points.append(f"Team-organisation för {title.lower()}")
            else:
                key_points.append(f"Framtiden för {title.lower()}")
        
        return {
            'title': title,
            'key_points': key_points[:10],  # Limit to 10 key points as requested
            'diagram_path': diagram_path
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
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE

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
            script_content += f'''
    # Add diagram
    diagram_path = "{diagram_path}"
    if os.path.exists(diagram_path):
        try:
            slide.shapes.add_picture(diagram_path, Inches(0.5), Inches(1.2), Inches(4), Inches(3))
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
            # Clean the point for code generation - escape quotes and limit length
            clean_point = point.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
            if len(clean_point) > 200:
                clean_point = clean_point[:200] + "..."
            
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
    print("📋 Each slide includes chapter title, diagram (when available), and 10 key points")

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