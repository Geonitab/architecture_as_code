# Kodarkitektur Bokverkstad - Development Instructions

**ALWAYS follow these instructions first and fallback to additional search and context gathering ONLY if the information in these instructions is incomplete or found to be in error.**

## Project Overview

This is a hybrid repository serving two primary purposes:

1. **Book Publishing**: Automated generation and publishing of "Arkitektur som kod" - a comprehensive technical book on architecture as code principles
2. **React Dashboard**: A web application that displays book project status and chapter structure

## Working Effectively

### Initial Setup and Dependencies

**NEVER CANCEL long-running installs.** Build processes can take 15+ minutes. Always use timeouts of 60+ minutes for installs.

```bash
# Install Node.js dependencies (30 seconds)
npm install

# Install book publishing dependencies (8+ minutes - NEVER CANCEL, timeout: 1800s)
sudo apt-get update
sudo apt-get install -y texlive-xetex texlive-fonts-recommended texlive-plain-generic

# Install Pandoc (1 minute)
wget https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-1-amd64.deb
sudo dpkg -i pandoc-3.1.9-1-amd64.deb

# Install Mermaid CLI (1 minute)
PUPPETEER_SKIP_DOWNLOAD=true npm install -g @mermaid-js/mermaid-cli

# Install Pandoc template
mkdir -p ~/.local/share/pandoc/templates
pandoc --print-default-template=latex > ~/.local/share/pandoc/templates/eisvogel.latex
```

### Build and Test Commands

**CRITICAL TIMING - NEVER CANCEL these operations:**

```bash
# React web application
npm run build     # 5 seconds (timeout: 60s)
npm run dev       # Ready in <1 second, runs indefinitely
npm run lint      # 2 seconds (timeout: 30s) - NOTE: Will show warnings, this is expected

# Book generation
python3 generate_book.py          # <1 second - generates markdown content
docs/build_book.sh                # 30 seconds (timeout: 300s) - full PDF build with diagrams

# Complete book publishing workflow (45 seconds total - NEVER CANCEL, timeout: 600s)
python3 generate_book.py && docs/build_book.sh
```

## Validation Requirements

**MANUAL VALIDATION**: After ANY changes, you MUST test actual functionality:

### React Application Validation
```bash
# Start dev server and verify it loads correctly
npm run dev
# Navigate to http://localhost:8080 in browser
# Take screenshot to verify UI renders properly
# Check console for errors
```

**Expected UI**: Dashboard showing 23 book chapters, project status cards, and CI/CD status indicators in Swedish.

### Book Building Validation
```bash
# Generate and build complete book
python3 generate_book.py && docs/build_book.sh

# Verify outputs
ls -la docs/arkitektur_som_kod.pdf  # Should be ~95KB
ls -la docs/images/*.png           # Should show 12 PNG files
file docs/arkitektur_som_kod.pdf   # Should confirm valid PDF
```

**Expected outputs**:
- PDF file: `docs/arkitektur_som_kod.pdf` (~95KB)
- 12 Mermaid diagrams converted to PNG in `docs/images/`
- No errors during Pandoc PDF generation

## Key Technical Details

### Repository Structure
```
docs/                     # Book content
├── *.md                 # 15 markdown chapter files
├── images/*.mmd         # 12 Mermaid diagram source files  
├── images/*.png         # Generated PNG diagrams
├── build_book.sh        # Local PDF build script
└── arkitektur_som_kod.pdf # Generated book (95KB with images)

src/                      # React web application
├── components/ui/       # shadcn/ui components
├── pages/Index.tsx      # Main dashboard page
└── App.tsx             # React router setup

.github/workflows/       # CI/CD automation
└── build-book.yml      # Automated PDF publishing on push
```

### Common Issues and Solutions

**Mermaid CLI Chrome Error**: 
```bash
# If mmdc fails with Chrome error, ensure Chrome executable is available:
PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i input.mmd -o output.png
```

**ESLint Warnings**: The linting will show warnings about React refresh and TypeScript interfaces. This is expected and does not prevent builds.

**TeXLive Installation**: Takes 8+ minutes and includes kernel updates. This is normal - NEVER CANCEL.

## Development Workflow

1. **Always run existing validation first**: `npm run build && npm run lint`
2. **Test book generation**: `python3 generate_book.py && docs/build_book.sh`
3. **Make minimal changes**
4. **Re-validate immediately**: Re-run builds after each change
5. **Test UI changes manually**: Start dev server and verify in browser
6. **ALWAYS run linting before committing**: `npm run lint`

## Technology Stack

### React Web Application
- **Vite**: Build tool and dev server
- **React + TypeScript**: UI framework
- **Tailwind CSS + shadcn/ui**: Styling and components
- **React Router**: Navigation
- **ESLint**: Code linting

### Book Publishing
- **Python 3.12**: Content generation script
- **Pandoc 3.1.9**: Markdown to PDF conversion
- **XeLaTeX**: PDF rendering engine
- **Mermaid CLI**: Diagram generation (.mmd → .png)
- **TeXLive**: LaTeX distribution for PDF generation

### CI/CD
- **GitHub Actions**: Automated book building and publishing
- **Automatic releases**: PDF published on main branch pushes
- **Artifact storage**: PDF available for download after builds

## GitHub Actions Integration

The `.github/workflows/build-book.yml` automatically:
- Triggers on changes to `docs/**/*.md` or `docs/images/**/*.mmd`
- Installs all dependencies (15+ minutes total)
- Converts Mermaid diagrams to PNG
- Generates PDF with Pandoc and Eisvogel template
- Creates GitHub releases with PDF attachments
- Stores artifacts for 30 days

**NEVER modify the GitHub Actions timeout values** - they are set correctly for the long-running dependency installations.

## Performance Expectations

- **React build**: 5 seconds
- **React dev server startup**: <1 second  
- **Book content generation**: <1 second
- **Complete book build with diagrams**: 30 seconds
- **Full CI/CD pipeline**: 15+ minutes (due to dependency installs)

## Critical Notes

- **NEVER CANCEL builds or long-running commands** - Dependency installs can take 15+ minutes
- **Always use proper timeouts**: 60+ minutes for installs, 5+ minutes for builds
- **Chrome dependency required**: Mermaid CLI needs Chrome browser for PNG generation
- **Swedish content**: All book content is in Swedish, UI labels are in Swedish
- **PDF generation works**: Even if Mermaid fails, Pandoc will generate PDF with text placeholders