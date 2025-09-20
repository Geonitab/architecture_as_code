# Book Presentations

This directory contains presentation materials generated from the book "Arkitektur som kod" without modifying the source content in the `docs/` directory.

## Generated Files

### presentation_outline.md
A comprehensive outline extracted from all 23 book chapters, showing key points and summaries for each chapter.

### generate_pptx.py  
Python script that creates a PowerPoint presentation with slides for each chapter, including:
- Title slide with book information
- Individual slides for each of the 23 chapters
- Key points and diagrams for each chapter

### requirements.txt
Python dependencies needed to run the PowerPoint generation script.

## Usage

To generate the PowerPoint presentation:

```bash
cd presentations
pip install -r requirements.txt
python generate_pptx.py
```

This will create `arkitektur_som_kod_presentation.pptx` with slides for all book chapters.

## Design Principles

This implementation follows the docs protection guidelines:

✅ **READ-ONLY**: Only reads from `docs/` directory, never modifies it
✅ **EXTERNAL OUTPUT**: Creates all generated files outside the `docs/` directory  
✅ **PRESERVATION**: Maintains the integrity of the book's source content
✅ **AUTOMATION**: Provides reusable scripts that can regenerate presentations as the book evolves

## Original Intent (PR #16)

This solution addresses the original intent of PR #16 to create presentations from book content, but does so correctly by:

1. **NOT** modifying any files in the `docs/` directory
2. **Reading** the book content as source material
3. **Generating** presentation files in the appropriate `presentations/` directory
4. **Providing** reusable automation for future presentation updates

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

Each slide contains carefully extracted key points that summarize the main concepts from the corresponding book chapter.