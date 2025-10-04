# Architecture as Code - Book Project

A comprehensive book about Architecture as Code, with practical examples and case studies.

## 📚 About the Book

This book covers Architecture as Code from fundamental principles to advanced implementation, with a focus on practical application.

### Target Audience
- system architects
- DevOps Engineers  
- Developers
- Project Managers
- IT Managers

### Contents
27 chapters covering:
- Fundamental principles of Architecture as Code
- Version control and code structures
- Cloud architecture and automation
- Security and compliance
- CI/CD and testing strategies
- Organizational transformation
- Practical case studies and implementations

## 🛠️ Technical implementation

### Structure
```
docs/                    # Book content
├── *.md                # Markdown chapters (01_inledning.md, 02_grundlaggande_principer.md, etc.)
├── images/             # Mermaid diagrams
│   └── *.mmd          # Mermaid source files
├── build_book.sh      # Local build script
└── arkitektur_som_kod.pdf  # Generated book

releases/                 # All deliverables organized for distribution
├── book/               # Book formats (PDF, EPUB, DOCX)
├── presentation/       # Presentation materials (PPTX, PDF)
├── whitepapers/        # HTML whitepapers per chapter
└── website/           # Complete static website

.github/workflows/      # CI/CD automation
├── unified-build-release.yml    # Unified comprehensive workflow (ALL formats)
├── generate-whitepapers.yml    # Standalone whitepaper generation
├── generate-presentations.yml  # Standalone presentation generation  
└── content-validation.yml      # Repository content validation
```

### Release Deliverables

All releases are automatically generated and published through GitHub Actions workflows.

**Book Formats:**
- PDF (using Pandoc + Eisvogel template)
- EPUB (electronic book format)
- DOCX (Microsoft Word format)

**Presentation Materials:**
- PowerPoint (PPTX) with speaker notes
- PDF version for easy sharing
- Individual chapter slides

**Whitepapers:**
- HTML whitepapers for each chapter
- Responsive design for web publishing
- Includes diagrams and code examples

**Website:**
- Complete static site with all content
- Chapter navigation
- Search functionality
- Mobile-responsive design

## 🚀 Building the Book

### Prerequisites

**For PDF Generation:**
```bash
# Install Pandoc (3.1.9 or later)
wget https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-1-amd64.deb
sudo dpkg -in pandoc-3.1.9-1-amd64.deb

# Install LaTeX (for PDF generation)
sudo apt-get update
sudo apt-get install -y texlive-xetex texlive-fonts-recommended texlive-plain-generic

# Install Mermaid CLI (for diagram conversion)
npm install -g @mermaid-js/mermaid-cli
```

**For Web Dashboard:**
```bash
# Install Node.js dependencies
# Note: Requires --legacy-peer-deps due to @toast-ui/react-editor React 17 compatibility
npm install --legacy-peer-deps
```

**Known Security Issues:**
- The `markdown` package has a ReDoS vulnerability (GHSA-wx77-rp39-c6vg) with no fix available. The impact is minimal as it's only used for static content rendering.
- Some dependencies require `--legacy-peer-deps` due to React version compatibility. See [package.json](package.json) for details.

### Build Commands

**Generate Book Content:**
```bash
# Generate all markdown files
python3 generate_book.py

# Build PDF with diagrams
cd docs && ./build_book.sh
```

**Run Web Dashboard:**
```bash
# Development server
npm run dev

# Production build
npm run build
```

**Generate All Formats:**
```bash
# Complete release build
./build_release.sh
```

## 📖 Chapter Overview

1. **Introduction** - Introduction to Architecture as Code
2. **Fundamental Principles** - Core principles of Architecture as Code
3. **Version Control** - Version management and code structure
4. **ADR** - Architecture Decision Records
5. **Automation & CI/CD** - Automation, DevOps and CI/CD
6. **Cloud Architecture** - Cloud architecture as code
7. **Containerization** - Containerization and orchestration
8. **Microservices** - Microservices and API design
9. **Security** - Security in Architecture as Code
10. **Policy as Code** - Policy as code and security automation
11. **Compliance** - Compliance and regulatory adherence
12. **Testing** - Testing strategies for architecture code
13. **implementation** - Practical implementation
14. **Cost Optimization** - Cost optimization and resource management
15. **Migration** - Migration from traditional infrastructure
16. **Organizational Change** - Organizational change and cultural transformation
17. **Team Structure** - Team structure and competencies
18. **Digitalization** - Digitalization and business value
19. **Lovable Mockups** - Lovable mockups and user-centered design
20. **Future Trends** - Future trends in Architecture as Code
21. **Best Practices** - Best practices and lessons learned
22. **Conclusion** - Conclusion
23. **Glossary** - Glossary of terms
24. **About Authors** - About the authors
25. **Future Development** - Future development and roadmap
26. **Appendix** - Code examples and templates
27. **Technical Architecture** - Technical architecture of the book

## 🎨 React Dashboard

The project includes a React-based web dashboard that provides:
- Book project status overview
- Chapter structure visualization
- CI/CD pipeline status
- Build artifacts and downloads

**Technologies:**
- React + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui components
- React Router

**Design System:**
- Kvadrat-aligned design tokens for consistent branding
- Comprehensive color, typography, and spacing system
- Dark mode support
- See [DESIGN_TOKENS.md](DESIGN_TOKENS.md) for detailed documentation

## 🔄 CI/CD Workflows

All builds are automated through GitHub Actions:

### Unified Build & Release
Triggers on push to main branch or docs changes:
- Builds all book formats (PDF, EPUB, DOCX)
- Generates presentations
- Creates whitepapers
- Builds static website
- Creates GitHub release with all artifacts

### Individual Workflows
- `generate-whitepapers.yml` - Standalone whitepaper generation
- `generate-presentations.yml` - Standalone presentation generation
- `content-validation.yml` - Validates markdown and structure

## 📝 Contributing

To contribute to the book content:

1. Edit markdown files in `docs/` directory
2. Follow the existing structure and style
3. Test locally with `python3 generate_book.py && cd docs && ./build_book.sh`
4. Submit a pull request

## 🎨 Design System

The project uses a comprehensive design token system for consistent UI design:

### Design Tokens
- **Colors**: Kvadrat brand colors, semantic colors, neutral tones
- **Typography**: Inter and JetBrains Mono font families
- **Spacing**: Consistent spacing scale
- **Shadows**: Custom Kvadrat-branded shadows
- **Animations**: Smooth, performant animations

### Documentation
- [DESIGN_TOKENS.md](DESIGN_TOKENS.md) - Complete design token reference
- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) - Visual design guidelines

### Example Usage
```tsx
// Using design tokens in components
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

<Card className="shadow-kvadrat border-primary/20">
  <Badge className="bg-success text-success-foreground">
    Active
  </Badge>
</Card>
```

See the [DesignTokensExample component](src/components/examples/DesignTokensExample.tsx) for a comprehensive showcase of all design tokens in action.

## 🔍 Link Verification

The repository includes a comprehensive link verification tool to ensure all links in documentation are valid.

**Run link verification:**
```bash
python3 scripts/verify_links.py
```

This generates three reports:
- `link-verification-report.md` - Markdown summary
- `link-verification-report.html` - Interactive HTML report
- `link-verification-report.json` - Machine-readable JSON

**Advanced options:**
```bash
# Custom timeout for slow connections
python3 scripts/verify_links.py --timeout 20

# Verbose output
python3 scripts/verify_links.py --verbose

# Custom output location
python3 scripts/verify_links.py --output reports/links
```

For complete documentation, see [LINK_VERIFICATION.md](LINK_VERIFICATION.md)

## 📄 License

This book project is maintained by Geonit AB.

## 🔗 Related Resources

- [Architecture as Code Principles](https://www.thoughtworks.com/radar/techniques/architecture-as-code)
- [Infrastructure as Code Best Practices](https://www.terraform.io/docs)
- [Documentation as Code](https://www.writethedocs.org/guide/docs-as-code/)

---

## 🌍 Language

All book content is in English.

