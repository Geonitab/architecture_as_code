# Book Presentations

This directory contains presentation materials generated from the book "Arkitektur som kod" without modifying the source content in the `docs/` directory.

## ✅ COMPLETED: PowerPoint Presentation

**File**: `arkitektur_som_kod_presentation.pptx` (180 KB)
**Status**: Successfully generated and verified
**Content**: 24 slides with diagrams and Swedish theme

### Key Features
- 🎯 **24 slides total**: 1 title slide + 23 chapter slides
- 🖼️ **12 embedded diagrams** from book chapters (PNG format)
- 📝 **10 key points per chapter** with comprehensive summaries
- 🇸🇪 **Swedish theme styling** with professional blue colors (#006AA7)
- 📐 **Custom layout** with title, diagram, and bullet points
- ✅ **Verified format**: Valid Microsoft PowerPoint 2007+ (.pptx)

## Generated Files

### presentation_outline.md
A comprehensive outline extracted from all 23 book chapters, showing key points and summaries for each chapter.

### generate_pptx.py  
Enhanced Python script that creates a PowerPoint presentation with slides for each chapter, including:
- Title slide with book branding in Swedish theme
- Individual slides for each of the 23 chapters
- Embedded PNG diagrams for visual support
- 10 meaningful key points per chapter
- Professional Swedish styling and layout

### requirements.txt
Python dependencies needed to run the PowerPoint generation script.

### arkitektur_som_kod_presentation.pptx ✨ NEW
**The final PowerPoint presentation file** ready for use in meetings, training, and presentations.

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

This will create/update `arkitektur_som_kod_presentation.pptx` with slides for all book chapters.

## Design Principles

This implementation follows the docs protection guidelines:

✅ **READ-ONLY**: Only reads from `docs/` directory, never modifies it
✅ **EXTERNAL OUTPUT**: Creates all generated files outside the `docs/` directory  
✅ **PRESERVATION**: Maintains the integrity of the book's source content
✅ **AUTOMATION**: Provides reusable scripts that can regenerate presentations as the book evolves
✅ **DIAGRAMS**: Integrates existing PNG diagrams from docs/images/
✅ **SWEDISH STANDARDS**: Professional styling compliant with Swedish corporate standards

## Content Summary

The generated presentation includes slides for:

1. **Inledning till arkitektur som kod** - Introduction to Infrastructure as Code
2. **Grundläggande principer** - Fundamental principles  
3. **Versionhantering och kodstruktur** - Version control and code structure
4. **Automatisering och CI/CD-pipelines** - Automation and CI/CD pipelines
5. **Molnarkitektur som kod** - Cloud architecture as code
6. **Säkerhet i Infrastructure as Code** - Security in Infrastructure as Code
7. **DevOps och CI/CD** - DevOps and CI/CD for Infrastructure as Code
8. **Infrastruktur som kod i praktiken** - Infrastructure as Code in practice
9. **Hantering av secrets och känslig data** - Managing secrets and sensitive data
10. **Övervakning och logging** - Monitoring and logging
11. **Kostnadsoptimering** - Cost optimization
12. **Skalning och prestanda** - Scaling and performance
13. **Multi-cloud strategier** - Multi-cloud strategies
14. **Säkerhet och compliance** - Security and compliance
15. **Disaster recovery och backup** - Disaster recovery and backup
16. **Automatisering av drift** - Operations automation
17. **Migration från traditionell infrastruktur** - Migration from traditional infrastructure
18. **Framtida trender och teknologier** - Future trends and technologies
19. **Best practices och lärda läxor** - Best practices and lessons learned
20. **Fallstudier och praktiska exempel** - Case studies and practical examples
21. **Slutsats** - Conclusion
22. **Ordlista** - Glossary
23. **Om författarna** - About the authors

Each slide contains 10 carefully extracted key points that summarize the main concepts from the corresponding book chapter, along with the chapter's diagram when available.