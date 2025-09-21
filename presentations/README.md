# Book Presentations

This directory contains presentation materials generated from the book "Arkitektur som kod" without modifying the source content in the `docs/` directory.

## Generated Files

### presentation_outline.md
A comprehensive outline extracted from all book chapters, showing key points and summaries for each chapter.

### generate_pptx.py  
Enhanced Python script that creates a PowerPoint presentation with slides for each chapter, including:
- Title slide with book branding in Swedish theme
- Individual slides for each of the chapters
- Embedded PNG diagrams for visual support
- Key points per chapter with comprehensive summaries
- Professional Swedish styling and layout

### requirements.txt
Python dependencies needed to run the PowerPoint generation script.

## Usage

To regenerate the PowerPoint presentation:

```bash
# From project root
python3 generate_presentation.py

# Then create the PPTX file
cd presentations
pip install -r requirements.txt
python3 generate_pptx.py
```

This will create/update the PowerPoint presentation with slides for all book chapters.

## Design Principles

This implementation follows the docs protection guidelines:

✅ **READ-ONLY**: Only reads from `docs/` directory, never modifies it
✅ **EXTERNAL OUTPUT**: Creates all generated files outside the `docs/` directory  
✅ **PRESERVATION**: Maintains the integrity of the book's source content
✅ **AUTOMATION**: Provides reusable scripts that can regenerate presentations as the book evolves
✅ **DIAGRAMS**: Integrates existing PNG diagrams from docs/images/
✅ **SWEDISH STANDARDS**: Professional styling compliant with Swedish corporate standards

## Content Summary

The generated presentation includes slides for all book chapters covering Infrastructure as Code topics in Swedish, including:

- Introduction to Infrastructure as Code
- Fundamental principles  
- Version control and code structure
- Automation and CI/CD pipelines
- Cloud architecture as code
- Security in Infrastructure as Code
- DevOps and CI/CD best practices
- Practical implementation strategies
- Managing secrets and sensitive data
- Monitoring and logging
- And more comprehensive topics...

All content is professionally formatted and ready for presentations, training sessions, and educational purposes.