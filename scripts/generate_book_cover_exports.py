#!/usr/bin/env python3
"""
Book Cover Export Generator
Generates high-resolution exports of the book cover in multiple formats
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def setup_directories():
    """Create necessary output directories"""
    base_dir = Path(__file__).parent.parent
    exports_dir = base_dir / "exports" / "book-cover"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for different formats
    (exports_dir / "pdf").mkdir(exist_ok=True)
    (exports_dir / "png").mkdir(exist_ok=True)
    (exports_dir / "jpg").mkdir(exist_ok=True)
    (exports_dir / "svg").mkdir(exist_ok=True)
    (exports_dir / "source").mkdir(exist_ok=True)
    
    return exports_dir

def generate_pdf_from_html(html_file, output_file, dpi=300):
    """Generate PDF from HTML using headless Chrome/Chromium"""
    print(f"Generating PDF from {html_file}...")
    
    try:
        # Try different possible Chrome/Chromium executables
        chrome_commands = [
            "google-chrome",
            "chromium",
            "chromium-browser",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]
        
        chrome_cmd = None
        for cmd in chrome_commands:
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
                chrome_cmd = cmd
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        if not chrome_cmd:
            print("Warning: Chrome/Chromium not found. Cannot generate PDF.")
            return False
        
        # Chrome command for PDF generation
        cmd = [
            chrome_cmd,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--print-to-pdf=" + str(output_file),
            f"--print-to-pdf-no-header",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            f"file://{html_file.absolute()}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and output_file.exists():
            print(f"✓ PDF generated: {output_file}")
            return True
        else:
            print(f"✗ PDF generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        return False

def generate_png_from_html(html_file, output_file, width=2480, height=3508):
    """Generate high-resolution PNG from HTML (A4 at 300 DPI)"""
    print(f"Generating PNG from {html_file}...")
    
    try:
        chrome_commands = [
            "google-chrome",
            "chromium",
            "chromium-browser",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium"
        ]
        
        chrome_cmd = None
        for cmd in chrome_commands:
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
                chrome_cmd = cmd
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        if not chrome_cmd:
            print("Warning: Chrome/Chromium not found. Cannot generate PNG.")
            return False
        
        cmd = [
            chrome_cmd,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            f"--window-size={width},{height}",
            "--hide-scrollbars",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            f"--screenshot={output_file}",
            f"file://{html_file.absolute()}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and output_file.exists():
            print(f"✓ PNG generated: {output_file}")
            return True
        else:
            print(f"✗ PNG generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error generating PNG: {e}")
        return False

def convert_png_to_jpg(png_file, jpg_file, quality=95):
    """Convert PNG to JPEG using ImageMagick or PIL"""
    print(f"Converting PNG to JPEG...")
    
    try:
        # Try ImageMagick first
        result = subprocess.run([
            "convert", str(png_file), 
            "-quality", str(quality),
            "-background", "white",
            "-flatten",
            str(jpg_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ JPEG generated: {jpg_file}")
            return True
        else:
            print("ImageMagick not available, trying PIL...")
            
    except FileNotFoundError:
        pass
    
    # Fallback to PIL
    try:
        from PIL import Image
        
        with Image.open(png_file) as img:
            # Convert RGBA to RGB for JPEG
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.save(jpg_file, "JPEG", quality=quality, optimize=True)
            print(f"✓ JPEG generated: {jpg_file}")
            return True
            
    except ImportError:
        print("✗ Neither ImageMagick nor PIL available for JPEG conversion")
        return False
    except Exception as e:
        print(f"✗ Error converting to JPEG: {e}")
        return False

def copy_source_files(base_dir, exports_dir):
    """Copy source files to exports directory"""
    print("Copying source files...")
    
    import shutil
    
    source_files = [
        "templates/book-cover-final.html",
        "templates/book-cover.svg",
        "templates/book-cover.html",
        "BRAND_GUIDELINES.md",
        "DESIGN_SYSTEM.md"
    ]
    
    source_dir = exports_dir / "source"
    
    for file_path in source_files:
        src = base_dir / file_path
        if src.exists():
            dst = source_dir / src.name
            shutil.copy2(src, dst)
            print(f"✓ Copied: {src.name}")

def create_usage_documentation(exports_dir):
    """Create documentation for the exported files"""
    print("Creating usage documentation...")
    
    doc_content = """# Book Cover Design Files

## Overview
This directory contains the complete book cover design for "Arkitektur som kod" in multiple formats.

## Files Included

### High-Resolution Exports
- `pdf/book-cover-print.pdf` - Print-ready PDF (300 DPI)
- `pdf/book-cover-screen.pdf` - Screen-optimized PDF
- `png/book-cover-300dpi.png` - High-resolution PNG (2480x3508, 300 DPI)
- `png/book-cover-150dpi.png` - Medium-resolution PNG (1240x1754, 150 DPI)
- `jpg/book-cover-300dpi.jpg` - High-resolution JPEG (300 DPI)
- `jpg/book-cover-150dpi.jpg` - Medium-resolution JPEG (150 DPI)

### Editable Source Files
- `svg/book-cover.svg` - Vector SVG format (infinitely scalable)
- `source/book-cover-final.html` - Enhanced HTML/CSS version
- `source/book-cover.html` - Original HTML template
- `source/BRAND_GUIDELINES.md` - Kvadrat brand guidelines
- `source/DESIGN_SYSTEM.md` - Design system documentation

## Usage Guidelines

### For Print Production
- Use `pdf/book-cover-print.pdf` for professional printing
- Ensure printer supports CMYK color space
- Recommended paper: High-quality matte or glossy finish

### For Digital Distribution
- Use `pdf/book-cover-screen.pdf` for digital catalogs
- Use `png/book-cover-300dpi.png` for high-quality web display
- Use `jpg/book-cover-150dpi.jpg` for email or social media

### For Further Editing
- Use `svg/book-cover.svg` in Adobe Illustrator, Inkscape, or other vector editors
- Use `source/book-cover-final.html` for web-based modifications
- Follow `source/BRAND_GUIDELINES.md` for brand compliance

## Technical Specifications

### Dimensions
- Format: A4 (210mm × 297mm)
- Resolution: 300 DPI for print, 150 DPI for screen
- Color Space: RGB for digital, convert to CMYK for print

### Brand Colors (HSL format)
- Kvadrat Blue: hsl(221, 67%, 32%)
- Kvadrat Light Blue: hsl(217, 91%, 60%)
- Kvadrat Dark Blue: hsl(214, 32%, 18%)
- Success Green: hsl(160, 84%, 30%)

### Typography
- Primary Font: Inter (weights: 400, 500, 600, 700, 800, 900)
- Fallback: system-ui, -apple-system, sans-serif

## Brand Compliance
This design follows Kvadrat's official brand guidelines v1.0. Any modifications should maintain:
- Consistent color palette
- Proper logo placement and sizing
- Typography hierarchy
- Professional aesthetic aligned with code architecture theme

## Contact
For questions about usage or modifications, refer to the brand guidelines or contact the design team.

Generated: $(date)
Version: 1.0
"""
    
    doc_file = exports_dir / "README.md"
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    print(f"✓ Documentation created: {doc_file}")

def main():
    """Main export generation function"""
    print("=== Book Cover Export Generator ===\n")
    
    base_dir = Path(__file__).parent.parent
    exports_dir = setup_directories()
    
    # Source files
    html_final = base_dir / "templates" / "book-cover-final.html"
    svg_file = base_dir / "templates" / "book-cover.svg"
    
    if not html_final.exists():
        print(f"✗ Source file not found: {html_final}")
        return 1
    
    # Generate exports
    success_count = 0
    total_count = 0
    
    # PDF exports (print and screen)
    pdf_print = exports_dir / "pdf" / "book-cover-print.pdf"
    total_count += 1
    if generate_pdf_from_html(html_final, pdf_print):
        success_count += 1
    
    # PNG exports (multiple resolutions)
    png_300dpi = exports_dir / "png" / "book-cover-300dpi.png"
    total_count += 1
    if generate_png_from_html(html_final, png_300dpi, 2480, 3508):  # A4 at 300 DPI
        success_count += 1
    
    png_150dpi = exports_dir / "png" / "book-cover-150dpi.png"
    total_count += 1
    if generate_png_from_html(html_final, png_150dpi, 1240, 1754):  # A4 at 150 DPI
        success_count += 1
    
    # JPEG conversions
    if png_300dpi.exists():
        jpg_300dpi = exports_dir / "jpg" / "book-cover-300dpi.jpg"
        total_count += 1
        if convert_png_to_jpg(png_300dpi, jpg_300dpi):
            success_count += 1
    
    if png_150dpi.exists():
        jpg_150dpi = exports_dir / "jpg" / "book-cover-150dpi.jpg"
        total_count += 1
        if convert_png_to_jpg(png_150dpi, jpg_150dpi):
            success_count += 1
    
    # Copy SVG file
    if svg_file.exists():
        import shutil
        svg_dest = exports_dir / "svg" / "book-cover.svg"
        shutil.copy2(svg_file, svg_dest)
        print(f"✓ SVG copied: {svg_dest}")
        success_count += 1
        total_count += 1
    
    # Copy source files
    copy_source_files(base_dir, exports_dir)
    
    # Create documentation
    create_usage_documentation(exports_dir)
    
    # Summary
    print(f"\n=== Export Summary ===")
    print(f"✓ Successfully generated: {success_count}/{total_count} files")
    print(f"📁 Export directory: {exports_dir}")
    
    if success_count == total_count:
        print("🎉 All exports completed successfully!")
        return 0
    else:
        print("⚠️  Some exports failed. Check error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())