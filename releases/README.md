# Releases Folder

This folder contains all deliverables generated during the build process, organized for easy distribution and deployment.

## Structure

### `/book/`
Contains book formats generated from the markdown source:
- `architecture_as_code.pdf` - Complete book in PDF format
- `architecture_as_code.epub` - EPUB format for e-readers
- `architecture_as_code.docx` - Microsoft Word format

### `/presentation/`
Contains presentation materials:
- `architecture_as_code_presentation.pptx` - PowerPoint presentation
- `presentation_outline.md` - Presentation content outline
- `generate_pptx.py` - Script to regenerate presentation
- `requirements.txt` - Python dependencies for presentation generation

### `/whitepapers/`
Contains individual chapter whitepapers:
- `*.html` - HTML whitepaper files for each chapter
- `whitepapers_combined.pdf` - All whitepapers combined into a single PDF

### `/website/`
Contains a complete copy of the static website build:
- Static website files ready for deployment
- All assets and dependencies included

## Build Process

All content in this folder is automatically generated during the build process. The build scripts ensure that:

1. All formats are generated with consistent content
2. Files are properly validated for integrity
3. Distribution-ready outputs are created
4. Version information is maintained

## Usage

After running the build process, all deliverables will be available in their respective folders for:
- Distribution to stakeholders
- Publishing to various platforms
- Archive and backup purposes
- Deployment workflows

## Automation

This folder structure is maintained by:
- `build_release.sh` - Main build script
- `unified-build-release.yml` - GitHub Actions workflow
- Individual component generation scripts