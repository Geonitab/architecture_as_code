# Architecture as Code Book Workshop - Development Instructions

**ALWAYS follow these instructions first and fallback to additional search and context gathering ONLY if the information in these instructions is incomplete or found to be in error.**

## Project Overview

This repository focuses on a single goal:

1. **Book Publishing**: Automated generation and publishing of "Architecture as Code" - a comprehensive technical book on architecture as code principles. (Historical documentation may reference a React dashboard, but the front-end source code has been removed from the project.)

## Working Effectively

### Initial Setup and Dependencies

**NEVER CANCEL long-running installs.** Build processes can take 15+ minutes. Always use timeouts of 60+ minutes for installs.

```bash
# Optional: install Node.js dependencies for helper scripts (30 seconds)
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
Build and Test Commands
CRITICAL TIMING - NEVER CANCEL these operations:
# Book generation
python3 generate_book.py          # <1 second - generates markdown content
docs/build_book.sh                # 30 seconds (timeout: 300s) - full PDF build with diagrams

# Complete book publishing workflow (45 seconds total - NEVER CANCEL, timeout: 600s)
python3 generate_book.py && docs/build_book.sh
Validation Requirements
MANUAL VALIDATION: After ANY changes, you MUST test actual functionality:
Book Building Validation
# Generate and build complete book
python3 generate_book.py && docs/build_book.sh

# Verify outputs
ls -la docs/architecture_as_code.pdf  # Should be ~95KB
ls -la docs/images/*.png              # Should show 12 PNG files
file docs/architecture_as_code.pdf    # Should confirm valid PDF
Expected outputs:
	•	PDF file: docs/architecture_as_code.pdf (~95KB)
	•	12 Mermaid diagrams converted to PNG in docs/images/
	•	No errors during Pandoc PDF generation
Key Technical Details
Repository Structure
docs/                     # Book content
├── *.md                 # 15 markdown chapter files
├── images/*.mmd         # 12 Mermaid diagram source files
├── images/*.png         # Generated PNG diagrams
├── build_book.sh        # Local PDF build script
└── architecture_as_code.pdf # Generated book (95KB with images)

.github/workflows/       # CI/CD automation
└── build-book.yml      # Automated PDF publishing on push
Common Issues and Solutions
Mermaid CLI Chrome Error:
# If mmdc fails with Chrome error, ensure Chrome executable is available:
PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i input.mmd -o output.png
ESLint Warnings: Existing lint configurations are retained for historical reasons and may reference React refresh or TypeScript interfaces. These warnings are expected until the front-end is reinstated and do not prevent book builds.
TeXLive Installation: Takes 8+ minutes and includes kernel updates. This is normal - NEVER CANCEL.
Development Workflow
1. Test book generation first: `python3 generate_book.py && docs/build_book.sh`
2. Make minimal changes.
3. Re-validate immediately by rerunning the book build after each change.
4. Run additional scripts as needed (e.g., `npm run generate:whitepapers`).
Technology Stack
- **Publishing Toolchain**
  - Python 3.12: Content generation script
  - Pandoc 3.1.9: Markdown to PDF conversion
  - XeLaTeX: PDF rendering engine
  - Mermaid CLI: Diagram generation (`.mmd` → `.png`)
  - TeXLive: LaTeX distribution for PDF generation
- **Automation & Utilities**
  - Node.js/npm: Wrapper scripts and linting utilities (no front-end currently included)
  - GitHub Actions: Automated book building and publishing
  - Automatic releases: PDF published on main branch pushes
  - Artifact storage: PDF available for download after builds
GitHub Actions Integration
The .github/workflows/build-book.yml automatically:
	•	Triggers on changes to docs/**/*.md or docs/images/**/*.mmd
	•	Installs all dependencies (15+ minutes total)
	•	Converts Mermaid diagrams to PNG
	•	Generates PDF with Pandoc and Eisvogel template
	•	Creates GitHub releases with PDF attachments
	•	Stores artifacts for 30 days

### AI Bot Issue Label Matrix

Several specialized automation bots monitor GitHub issues and trigger workflows when specific labels are applied. Use the correct label so the intended bot responds automatically:

| Bot | Workflow File | Trigger Labels |
| --- | ------------- | -------------- |
| Architect Bot | `.github/workflows/architect-bot.yml` | `architecture` (case-insensitive) |
| Developer Bot | `.github/workflows/developer-bot.yml` | `dev` (case-insensitive) |
| Designer Bot | `.github/workflows/designer-bot.yml` | `design` (case-insensitive) |
| Editor Bot | `.github/workflows/editor-bot.yml` | `documentation` (case-insensitive) |
| QA Bot | `.github/workflows/qa-bot.yml` | `qa` (case-insensitive) |
| Requirements Bot | `.github/workflows/requirements-bot.yml` | `req` (case-insensitive) |

Each workflow listens for newly opened, reopened, or relabeled issues. Apply or update the appropriate label to dispatch the matching bot and generate the related automation response.
NEVER modify the GitHub Actions timeout values - they are set correctly for the long-running dependency installations.
Performance Expectations
	•	Book content generation: <1 second
	•	Complete book build with diagrams: 30 seconds
	•	Full CI/CD pipeline: 15+ minutes (due to dependency installs)
Critical Notes
	•	NEVER CANCEL builds or long-running commands - Dependency installs can take 15+ minutes
	•	Always use proper timeouts: 60+ minutes for installs, 5+ minutes for builds
	•	Chrome dependency required: Mermaid CLI needs Chrome browser for PNG generation
	•	English content: All manuscript text and automation outputs are maintained in English
	•	PDF generation works: Even if Mermaid fails, Pandoc will generate PDF with text placeholders

