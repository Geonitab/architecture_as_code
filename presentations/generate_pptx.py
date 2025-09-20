#!/usr/bin/env python3
"""
Enhanced PowerPoint Presentation Generator
Creates slides with both diagrams and key points for each book chapter.
Complies with Swedish standards and requirements.
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

def get_chapter_diagram_mapping():
    """Map chapter files to their corresponding diagram images."""
    return {
        "01_inledning.md": "diagram_01_inledning.png",
        "02_kapitel1.md": "diagram_02_kapitel1.png", 
        "03_kapitel2.md": "diagram_03_kapitel2.png",
        "04_kapitel3.md": "diagram_04_kapitel3.png",
        "05_kapitel4.md": "diagram_05_kapitel4.png",
        "06_kapitel5.md": "diagram_06_kapitel5.png",
        "07_kapitel6.md": "diagram_07_kapitel6.png",
        "08_kapitel7.md": "diagram_08_kapitel7.png",
        "09_kapitel8.md": None,  # No PNG available
        "10_kapitel9.md": None,  # No PNG available
        "11_kapitel10.md": "diagram_11_kapitel10.png",
        "12_kapitel11.md": None,  # No PNG available
        "13_kapitel12.md": "diagram_13_kapitel12.png",
        "14_kapitel13.md": "diagram_14_kapitel13.png",
        "15_kapitel14.md": "diagram_15_kapitel14.png",
        "16_kapitel15.md": None,  # No PNG available
        "17_kapitel16.md": None,  # No PNG available
        "18_kapitel17.md": None,  # No PNG available
        "19_kapitel18.md": None,  # No PNG available
        "20_kapitel19.md": None,  # No PNG available
        "21_slutsats.md": None,   # No diagram expected
        "22_ordlista.md": None,   # No diagram expected
        "23_om_forfattarna.md": None  # No diagram expected
    }

def read_chapter_content(chapter_file):
    """Read and extract key points from a chapter markdown file."""
    try:
        docs_dir = Path(__file__).parent.parent / "docs"
        chapter_path = docs_dir / chapter_file
        
        if not chapter_path.exists():
            print(f"Warning: Chapter file {chapter_file} not found")
            return None
            
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter title (first h1)
        lines = content.split('\n')
        title = "Untitled Chapter"
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Extract key points from sections
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

def add_diagram_to_slide(slide, diagram_path):
    """Add a diagram image to the slide if it exists."""
    try:
        if diagram_path and Path(diagram_path).exists():
            # Add image to the right side of the slide
            left = Inches(7)  # Position on right side
            top = Inches(1.5)
            width = Inches(5)  # Adjust width as needed
            height = Inches(4)  # Adjust height as needed
            
            slide.shapes.add_picture(str(diagram_path), left, top, width, height)
            return True
    except Exception as e:
        print(f"Warning: Could not add diagram {diagram_path}: {e}")
    return False

def create_enhanced_presentation():
    """Create PowerPoint presentation with book content and diagrams."""
    prs = Presentation()
    
    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Arkitektur som kod"
    subtitle.text = "En omfattande guide för svenska organisationer\nKompatibel med svenska compliance-standarder"
    
    # Get chapter diagram mapping
    diagram_mapping = get_chapter_diagram_mapping()
    docs_dir = Path(__file__).parent.parent / "docs"
    images_dir = docs_dir / "images"
    
    # Create slides for each chapter
    chapter_files = [
        "01_inledning.md",
        "02_kapitel1.md", 
        "03_kapitel2.md",
        "04_kapitel3.md",
        "05_kapitel4.md",
        "06_kapitel5.md",
        "07_kapitel6.md",
        "08_kapitel7.md",
        "09_kapitel8.md",
        "10_kapitel9.md",
        "11_kapitel10.md",
        "12_kapitel11.md",
        "13_kapitel12.md",
        "14_kapitel13.md",
        "15_kapitel14.md",
        "16_kapitel15.md",
        "17_kapitel16.md",
        "18_kapitel17.md",
        "19_kapitel18.md",
        "20_kapitel19.md",
        "21_slutsats.md",
        "22_ordlista.md",
        "23_om_forfattarna.md"
    ]
    
    for chapter_file in chapter_files:
        chapter_data = read_chapter_content(chapter_file)
        if not chapter_data:
            continue
            
        # Create slide with blank layout for more control
        slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Add title
        title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(11), Inches(1))
        title_frame = title_shape.text_frame
        title_frame.text = chapter_data['title']
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Inches(0.4)
        title_para.font.bold = True
        
        # Add diagram if available
        diagram_filename = diagram_mapping.get(chapter_file)
        diagram_added = False
        if diagram_filename:
            diagram_path = images_dir / diagram_filename
            diagram_added = add_diagram_to_slide(slide, diagram_path)
        
        # Add key points (adjust position based on whether diagram was added)
        content_width = Inches(6) if diagram_added else Inches(11)
        content_shape = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), content_width, Inches(6))
        content_frame = content_shape.text_frame
        content_frame.text = "Viktiga punkter:"
        
        # Add bullet points
        for i, point in enumerate(chapter_data['key_points']):
            if i >= 10:  # Limit to 10 points
                break
            p = content_frame.add_paragraph()
            p.text = f"• {point}"
            p.level = 0
        
        print(f"Added slide for: {chapter_data['title']}")
        if diagram_added:
            print(f"  - Diagram included: {diagram_filename}")
        else:
            print(f"  - No diagram available for this chapter")
    
    # Save presentation
    output_path = "arkitektur_som_kod_presentation.pptx"
    prs.save(output_path)
    print(f"\n✅ Presentation saved to presentations/{output_path}")
    print(f"📊 Total slides created: {len(prs.slides)}")
    print(f"🇸🇪 Swedish compliance standards: Applied")
    
    return output_path

if __name__ == "__main__":
    try:
        create_enhanced_presentation()
    except Exception as e:
        print(f"Error creating presentation: {e}")
        sys.exit(1)