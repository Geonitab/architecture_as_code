# Releases Folder

This folder contains all deliverables generated during the build process, organized for easy distribution and deployment.

## Structure

### `/book/`
Contains book formats generated from the markdown source:
- `arkitektur_som_kod.pdf` - Complete book in PDF format
- `arkitektur_som_kod.epub` - EPUB format for e-readers
- `arkitektur_som_kod.docx` - Microsoft Word format

### `/presentation/`
Contains presentation materials:
- `arkitektur_som_kod_presentation.pptx` - PowerPoint presentation
- `arkitektur_som_kod_presentation.pdf` - PDF version of presentation

### `/whitepapers/`
Contains individual chapter whitepapers:
- `*.html` - HTML whitepaper files for each chapter
- `whitepapers_combined.pdf` - All whitepapers combined into a single PDF

### `/website/`
Contains a complete copy of the static website build:
- Static website files for deployment

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