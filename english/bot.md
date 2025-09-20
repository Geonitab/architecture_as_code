# AI Assistant Prompt for Book Project: Architecture as Code

## Project Overview
You help create content for the book "Architecture as Code" - a comprehensive English guide about Infrastructure as Code (IaC). This is a hybrid project that combines:

1. **Book Production**: Automated generation and publishing of a comprehensive technical book
2. **React Dashboard**: A web application that displays book project status and chapter structure

The book targets system architects, developers, DevOps engineers, project managers, and IT managers who want to understand and implement Infrastructure as Code.

## Current Structure
The English version of the project contains **23 chapters**. The following files exist in `english/docs/` directory:

- `01_introduction.md` - Introduction to Architecture as Code
- `02_chapter1.md` - Basic principles for Infrastructure as Code
- `03_chapter2.md` - Version control and code structure
- `04_chapter3.md` - [PLANNED] Automation and CI/CD pipelines
- `05_chapter4.md` - [PLANNED] Cloud architecture as code
- `06_chapter5.md` - [PLANNED] Security in Infrastructure as Code
- `07_chapter6.md` - [PLANNED] DevOps and CI/CD for Infrastructure as Code
- `08_chapter7.md` - [PLANNED] Infrastructure as code in practice
- `09_chapter8.md` - [PLANNED] Digitalization through code-based infrastructure
- `10_chapter9.md` - [PLANNED] Organizational change and team structures
- `11_chapter10.md` - [PLANNED] Containerization and orchestration as code
- `12_chapter11.md` - [PLANNED] Project management for IaC initiatives
- `13_chapter12.md` - [PLANNED] Microservices architecture as code
- `14_chapter13.md` - [PLANNED] Future trends and technologies in IaC
- `15_chapter14.md` - [PLANNED] Team structure and competency development for IaC
- `16_chapter15.md` - [PLANNED] Cost optimization and resource management
- `17_chapter16.md` - [PLANNED] Testing strategies for infrastructure code
- `18_chapter17.md` - [PLANNED] Migration from traditional infrastructure
- `19_chapter18.md` - [PLANNED] Case studies and practical examples
- `20_chapter19.md` - [PLANNED] Best practices and lessons learned
- `21_conclusion.md` - Conclusion
- `22_glossary.md` - Glossary
- `23_about_authors.md` - About the authors

## Technical Infrastructure
The project uses the following technologies and tools:

### Book Production
- **Python 3.12**: Content generation via `generate_book_en.py`
- **Pandoc 3.1.9**: Markdown to PDF conversion
- **XeLaTeX**: PDF rendering engine
- **Mermaid CLI**: Diagram conversion (.mmd → .png)
- **TeXLive**: LaTeX distribution for PDF generation
- **Eisvogel**: LaTeX template for professional PDF layout

### React Dashboard
- **Vite**: Build tool and development server
- **React + TypeScript**: UI framework
- **Tailwind CSS + shadcn/ui**: Styling and components
- **React Router**: Navigation
- **ESLint**: Code linting

### CI/CD
- **GitHub Actions**: Automated book building and publishing
- **Automatic releases**: PDF published on main branch pushes
- **Artifact storage**: PDF available for download after builds

## Build and Validation Commands

**CRITICAL TIMING - NEVER CANCEL these operations:**

```bash
# React web application
npm run build     # 5 seconds (timeout: 60s)
npm run dev       # Ready in <1 second, runs indefinitely
npm run lint      # 2 seconds (timeout: 30s) - NOTE: Will show warnings, this is expected

# English book generation
python3 generate_book_en.py       # <1 second - generates markdown content
english/docs/build_book_en.sh     # 30 seconds (timeout: 300s) - full PDF build with diagrams

# Complete English book publishing workflow (45 seconds total - NEVER CANCEL, timeout: 600s)
python3 generate_book_en.py && english/docs/build_book_en.sh
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

**Expected UI**: Dashboard showing 23 book chapters, project status cards, and CI/CD status indicators in English.

### English Book Building Validation
```bash
# Generate and build complete English book
python3 generate_book_en.py && english/docs/build_book_en.sh

# Verify outputs
ls -la english/docs/architecture_as_code.pdf  # Should be generated PDF
ls -la english/docs/images/*.png              # Should show PNG files
file english/docs/architecture_as_code.pdf    # Should confirm valid PDF
```

**Expected outputs**:
- PDF file: `english/docs/architecture_as_code.pdf`
- Mermaid diagrams converted to PNG in `english/docs/images/`
- No errors during Pandoc PDF generation

## Key Technical Details

### Repository Structure
```
english/                  # English translation content
├── docs/                # Book content (English)
│   ├── *.md            # English markdown chapter files
│   ├── images/*.mmd    # Mermaid diagram source files  
│   ├── images/*.png    # Generated PNG diagrams
│   ├── build_book_en.sh # English PDF build script
│   └── architecture_as_code.pdf # Generated English book
├── src/                 # React web application (English UI)
│   ├── components/ui/   # shadcn/ui components
│   ├── pages/Index.tsx  # Main dashboard page (English)
│   └── App.tsx         # React router setup
├── .github/workflows/   # CI/CD automation
│   └── build-book-en.yml # Automated English PDF publishing
└── README.md           # English documentation

docs/                     # Original Swedish content
├── *.md                 # Swedish markdown chapter files
├── images/*.mmd         # Swedish Mermaid diagram source files  
├── images/*.png         # Generated PNG diagrams
├── build_book.sh        # Swedish PDF build script
└── arkitektur_som_kod.pdf # Generated Swedish book

src/                      # Original Swedish React app
├── components/ui/       # shadcn/ui components
├── pages/Index.tsx      # Main dashboard page (Swedish)
└── App.tsx             # React router setup

.github/workflows/       # CI/CD automation
└── build-book.yml      # Automated Swedish PDF publishing on push
```

## Your Task

Choose ONE area to work on for English content expansion. Focus on:

### Content Requirements
- **Language**: English
- **Target audience**: Technical professionals in IT/development
- **Length**: 2000-4000 words per chapter
- **Technical accuracy**: Proper Infrastructure as Code terminology
- **Code examples**: Real-world, executable examples with English comments
- **Diagrams**: Mermaid diagrams with English labels (max 5 elements, horizontal orientation)

### Implementation Instructions

1. **Always run existing validation first**: `npm run build && npm run lint`
2. **Test English book generation**: `python3 generate_book_en.py && english/docs/build_book_en.sh`
3. **Make minimal changes**
4. **Re-validate immediately**: Re-run builds after each change
5. **Test UI changes manually**: Start dev server and verify English UI in browser
6. **ALWAYS run linting before committing**: `npm run lint`

### Critical Process Instructions

**BUILD COMMANDS AND TIMING:**
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

**Expected UI**: Dashboard showing 23 book chapters, project status cards, and CI/CD status indicators in English.

### English Book Building Validation  
```bash
python3 generate_book_en.py && english/docs/build_book_en.sh
ls -la english/docs/architecture_as_code.pdf    # Should be valid PDF
ls -la english/docs/images/*.png                # Should show PNG files
file english/docs/architecture_as_code.pdf      # Should confirm valid PDF
```
**Expected outputs**: PDF file, English Mermaid diagrams converted to PNG, no errors during Pandoc PDF generation.

## Implementation Instructions

### CRITICAL: Read before you write!

1. **Check structure**: Look at existing English chapters (01_introduction.md, 02_chapter1.md, etc.)
2. **Follow patterns**: Use same structure as completed chapters
3. **Technical accuracy**: Ensure Infrastructure as Code terminology is correct
4. **English proficiency**: Use proper English grammar and technical writing style
5. **Code examples**: Include realistic, executable code snippets
6. **Cross-references**: Link to other relevant chapters when appropriate

### Choose ONE area:

#### A) Complete missing chapters (4-20)
Expand the `generate_book_en.py` script to include chapters 4-20 with comprehensive English content

#### B) Enhance existing chapters (1-3, 21-23)
Add more detailed content, better examples, or improved explanations to existing English chapters

#### C) Improve English React UI
Enhance the English/src/pages/Index.tsx with better UX, additional features, or improved translations

### Quality Standards

- **Technical accuracy**: All code examples must be syntactically correct
- **English quality**: Professional technical writing with proper grammar
- **Consistency**: Follow established patterns from existing content
- **Completeness**: Each chapter should be comprehensive and self-contained
- **Cross-references**: Include links to related chapters where appropriate

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
2. **Test English book generation**: `python3 generate_book_en.py && english/docs/build_book_en.sh`
3. **Make minimal changes**
4. **Re-validate immediately**: Re-run builds after each change
5. **Test UI changes manually**: Start dev server and verify English UI in browser
6. **ALWAYS run linting before committing**: `npm run lint`

## GitHub Actions Integration

The `english/.github/workflows/build-book-en.yml` automatically:
- Triggers on changes to `english/docs/**/*.md` or `english/docs/images/**/*.mmd`
- Installs all dependencies (15+ minutes total)
- Converts English Mermaid diagrams to PNG
- Generates English PDF with Pandoc and Eisvogel template
- Creates GitHub releases with English PDF attachments
- Stores artifacts for 30 days

**NEVER modify the GitHub Actions timeout values** - they are set correctly for the long-running dependency installations.

## Performance Expectations

- **React build**: 5 seconds
- **React dev server startup**: 1 second
- **Complete English book build with diagrams**: 30 seconds
- **Full CI/CD pipeline**: 15+ minutes (due to dependency installs)

## Critical Notes

- **NEVER CANCEL builds or long-running commands** - Dependency installs can take 15+ minutes
- **Always use proper timeouts**: 60+ minutes for installs, 5+ minutes for builds
- **Chrome dependency required**: Mermaid CLI needs Chrome browser for PNG generation
- **English content**: All book content should be in proper technical English
- **PDF generation works**: Even if Mermaid fails, Pandoc will generate PDF with text placeholders