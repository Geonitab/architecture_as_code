# Whitepaper Design Guidelines for Architecture as Code
## Professional Technical Documentation with Modern Visual Standards

## Purpose
This document defines the design standards for all whitepapers generated from the Architecture as Code book content. It ensures that every whitepaper is professionally formatted, visually accessible, and aligned with modern technical documentation best practices whilst maintaining the Kvadrat brand identity.

---

## Core Design Principles

### 1. Professional Authority
- **Credibility Through Design**: Clean, structured layout that establishes technical expertise
- **Consistent Branding**: Kvadrat colour palette and typography throughout all materials
- **Academic Rigour**: Proper citations, versioning, and metadata visible on every document
- **Print-Ready Quality**: A4/Letter formatting (210mm × 297mm) optimised for both screen and print

### 2. Reading Experience
- **Scannable Structure**: Clear headings, logical flow, and visual hierarchy
- **Progressive Information**: Lead paragraph → detailed content → section topics → call to action
- **Visual Relief**: Diagrams, callouts, and white space prevent text fatigue
- **Optimal Line Length**: Maximum 80 characters per line for comfortable reading

### 3. Accessibility and Standards
- **WCAG AA Compliance**: Minimum 4.5:1 contrast ratio for all text
- **Semantic HTML5**: Proper heading hierarchy, figure captions, and ARIA labels
- **Responsive Design**: Graceful degradation on mobile devices (min-width: 320px)
- **Print Optimisation**: Clean page breaks, removal of unnecessary UI elements when printing

---

## Document Format and Structure

### Standard Dimensions
- **Page Size**: A4 (210mm × 297mm) or US Letter (8.5" × 11")
- **Page Margins**: 25mm (approximately 1 inch) on all sides
- **Content Width**: 160mm maximum for optimal readability
- **Safe Print Zone**: Keep critical content within 20mm from edges

### Typography Standards

#### Font Families
- **Primary Font**: [Inter](https://fonts.google.com/specimen/Inter) – modern sans-serif optimised for screen and print
  - **Weights Used**: 300 (Light), 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold), 800 (Extra-Bold)
- **Monospace Font**: [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) – code samples and technical references
  - **Weights Used**: 400 (Regular), 500 (Medium), 600 (Semi-Bold)

#### Type Scale and Hierarchy
| Element | Size | Weight | Line Height | Colour | Usage |
|---------|------|--------|-------------|--------|-------|
| **H1 (Main Title)** | 36px (2.25rem) | 800 | 1.2 | Kvadrat Blue Dark | Document title, primary heading |
| **H1 (Section Title)** | 28px (1.75rem) | 700 | 1.3 | Kvadrat Blue Dark | Major section headings |
| **H2** | 24px (1.5rem) | 600 | 1.3 | Kvadrat Blue | Subsection headings |
| **H3** | 20px (1.25rem) | 600 | 1.4 | Kvadrat Blue Dark | Minor subsection headings |
| **Body Text** | 16px (1rem) | 400 | 1.6 | Kvadrat Blue Dark | Main content paragraphs |
| **Lead Paragraph** | 18px (1.125rem) | 400 | 1.5 | Kvadrat Muted | Opening/summary paragraphs |
| **Captions** | 14px (0.875rem) | 400 | 1.4 | Kvadrat Muted | Figure captions, metadata |
| **Labels** | 12px (0.75rem) | 600 | 1.2 | Kvadrat Blue | Metadata labels, badges |
| **Code Inline** | 14px (0.875rem) | 400 | 1.5 | Kvadrat Blue Dark | Inline code snippets |
| **Code Block** | 14px (0.875rem) | 400 | 1.5 | Light Grey (#d1d5db) | Multi-line code samples |

### Colour Palette (Kvadrat Brand)

#### Core Colours
```css
--aac-primary: hsl(221, 67%, 32%)           /* Kvadrat Blue: #2A4A8C */
--aac-primary-light: hsl(217, 91%, 60%)     /* Kvadrat Blue Light: #3B82F6 */
--aac-primary-dark: hsl(214, 32%, 18%)      /* Kvadrat Blue Dark: #1F2937 */
--aac-muted: hsl(215, 20%, 46%)             /* Kvadrat Grey: #6B7280 */
```

#### Surface and Background Colours
```css
--surface-soft: hsl(214, 32%, 97%)          /* Light Background: #F8F9FA */
--surface-border: rgba(23, 37, 84, 0.15)    /* Border: Semi-transparent Blue */
--white: hsl(0, 0%, 100%)                   /* Pure White: #FFFFFF */
--black: hsl(0, 0%, 0%)                     /* Pure Black: #000000 */
```

#### Semantic Colours
```css
--success: hsl(160, 84%, 30%)               /* Success Green: #0D9488 */
--warning: hsl(32, 95%, 44%)                /* Warning Orange: #F59E0B */
--info: hsl(217, 91%, 60%)                  /* Info Blue: #3B82F6 */
```

#### Contrast Requirements
- **Body Text on White**: 4.72:1 (WCAG AA Pass) – `#1F2937` on `#FFFFFF`
- **Headings on White**: 7.84:1 (WCAG AAA Pass) – `#2A4A8C` on `#FFFFFF`
- **Muted Text on White**: 4.54:1 (WCAG AA Pass) – `#6B7280` on `#FFFFFF`

---

## Whitepaper Components

### 1. Document Header
The header establishes the whitepaper's identity and metadata.

**Required Elements**:
- **Series Badge**: Small pill-shaped badge indicating category (e.g., "Security and Governance")
  - Background: `var(--aac-primary)`
  - Text: White, 12px, font-weight 600, uppercase, letter-spacing 0.4px
  - Padding: 6px 16px
  - Border-radius: 999px (fully rounded)
- **Main Title**: 36px, font-weight 800, Kvadrat Blue Dark
  - Format: `[Chapter Label] – [Chapter Title]`
  - Example: "Chapter 9 – Security Fundamentals for Architecture as Code"
- **Subtitle**: 20px, font-weight 400, Kvadrat Muted
  - Format: Key insights from [Chapter Label] of "[Book Title]"
  - Max-width: 85% to prevent overly long lines
- **Metadata Row**: Flex layout with 32px gaps
  - **Author**: Name(s) of contributor(s)
  - **Published**: Date in format "23 October 2025" (British English, no leading zero)
  - **Build Number**: Version or build identifier (e.g., "2025.10" or "Build 342")
- **Feature Tags** (optional): Visual pills indicating release features
  - Background: `var(--surface-soft)`
  - Text: Kvadrat Blue, 12px, font-weight 600, uppercase
  - Layout: Flex wrap with 8px gaps

**Spacing**:
- Header section: 40px bottom margin
- Elements within header: 20px vertical gap

### 2. Book Overview Section
Provides context about the source material.

**Structure**:
```html
<section class="book-overview">
    <h1>About "Architecture as Code"</h1>
    <p class="lead">[Book description paragraph]</p>
    
    <div class="callout callout-info">
        <div class="callout-title">Who should read this</div>
        <p>[Target audience description]</p>
    </div>
</section>
```

**Styling**:
- **Section Heading**: 28px, font-weight 700
- **Lead Paragraph**: 18px body text with 4px left border in Kvadrat Blue
- **Callout Box**: 
  - Background: `var(--surface-soft)`
  - Border-left: 4px solid `var(--aac-primary-light)`
  - Padding: 20px
  - Border-radius: 8px
  - Margin: 24px vertical

### 3. Chapter Highlight Section
The main content area showcasing chapter insights.

**Structure**:
```html
<section class="chapter-highlight">
    <h1>[Chapter Label]: [Chapter Title]</h1>
    
    <figure class="chapter-figure">
        <img src="[diagram-path]" alt="Chapter diagram for [title]">
    </figure>
    
    <p>[Condensed content paragraph 1]</p>
    <p>[Condensed content paragraph 2]</p>
    <p>[Condensed content paragraph 3]</p>
    
    <h2>Primary topics explored</h2>
    <ul>
        <li>[Section header 1]</li>
        <li>[Section header 2]</li>
        <li>[Section header 3]</li>
        ...
    </ul>
</section>
```

**Content Guidelines**:
- **Opening Paragraphs**: 2–3 substantial paragraphs (minimum 30 characters each)
- **Section List**: Maximum 6 primary topics to prevent overwhelming readers
- **Diagram Placement**: Centred, full-width within content area
- **Alt Text**: Descriptive alternative text for all images

**Figure Styling**:
- **Container**: Text-align centre, 30px vertical margin
- **Image**: 
  - Max-width: 100%
  - Height: Auto (preserve aspect ratio)
  - Border: 1px solid `var(--surface-border)`
  - Border-radius: 8px
  - Box-shadow: Optional subtle shadow for depth

### 4. Call to Action Section
Encourages reader engagement with the full book.

**Structure**:
```html
<section class="call-to-action">
    <h1>Continue your journey</h1>
    
    <div class="callout callout-success">
        <div class="callout-title">Read the full chapter</div>
        <p><strong>Discover [Chapter Label] – "[Title]" in "[Book Title]"</strong> 
        for detailed explanations, practical examples, and implementation patterns.</p>
    </div>
    
    <p>The complete manuscript spans [X] chapters, positioning this whitepaper 
    within the [area] focus of the programme.</p>
    
    <p><strong>Explore adjacent chapters:</strong> The surrounding sections expand 
    upon the themes introduced here and provide complementary techniques.</p>
</section>
```

**Styling**:
- **Success Callout**: Use `--success` colour for border-left (4px)
- **Strong Text**: Font-weight 600, same colour as body text
- **Contextual Information**: Regular paragraphs linking to broader book structure

---

## Code Samples and Technical Content

### Inline Code
- **Font**: JetBrains Mono, 14px
- **Background**: `var(--surface-soft)`
- **Padding**: 2px 6px
- **Border-radius**: 4px
- **Colour**: Inherit from surrounding text

### Code Blocks
- **Syntax Highlighting**: Prism.js with "Tomorrow" theme (`prism-tomorrow.min.css`)
- **Background**: Dark grey (`#2d2d2d`)
- **Text Colour**: Light grey (`#d1d5db`)
- **Border-left**: 4px solid Kvadrat Blue for visual consistency
- **Padding**: 16px
- **Border-radius**: 8px
- **Margin**: 16px vertical
- **Font**: JetBrains Mono, 14px, line-height 1.5
- **Line Numbers** (optional): Enabled via Prism.js plugin

**Supported Languages**:
- YAML, JSON
- Python, Bash
- JavaScript, TypeScript
- Docker, Terraform

### Lists
- **Unordered Lists**: Standard bullet points
- **Ordered Lists**: Numeric sequence
- **Padding-left**: 24px from container edge
- **Item Spacing**: 8px between list items
- **Colour**: Kvadrat Blue Dark for consistency

---

## Responsive and Print Considerations

### Responsive Breakpoints
```css
/* Mobile: 320px – 767px */
@media (max-width: 768px) {
    .page {
        padding: 20px;
        width: 100%;
    }
    
    .title {
        font-size: 30px;
    }
    
    .meta-info {
        gap: 16px;
        flex-direction: column;
    }
}
```

**Mobile Optimisations**:
- Reduce page padding from 25mm to 20px
- Decrease title size from 36px to 30px
- Stack metadata items vertically instead of horizontally
- Maintain minimum tap target size of 44px × 44px for interactive elements

### Print Styles
```css
@media print {
    body {
        background: var(--white);
    }
    
    .page {
        padding: 20mm;
        box-shadow: none;
    }
    
    .page-break {
        page-break-before: always;
    }
}
```

**Print Optimisations**:
- Remove page shadows and decorative backgrounds
- Reduce padding to 20mm for better paper usage
- Ensure diagrams fit within printable area
- Force page breaks before major sections if needed

---

## Accessibility Standards

### Semantic HTML5
All whitepapers must use proper semantic markup:
- `<section>` for major content blocks
- `<h1>` through `<h3>` for heading hierarchy (never skip levels)
- `<figure>` and `<figcaption>` for diagrams
- `<strong>` for emphasis (not `<b>`)
- `<code>` and `<pre>` for code samples

### ARIA Labels
- **Feature Tags**: `role="list"` and `role="listitem"` for non-semantic elements
- **Images**: Always include descriptive `alt` text
- **Metadata Attributes**: Use `data-*` attributes for version, tags, codename

**Example**:
```html
<div class="page" 
     data-release-version="2025.10" 
     data-feature-tags="diagram-refresh, governance-automation" 
     data-release-codename="Alpha">
```

### Keyboard Navigation
- All interactive elements must be keyboard-accessible
- Tab order follows logical reading flow
- Focus indicators clearly visible (outline or background change)

---

## File Naming and Organisation

### Generated Whitepaper Files
- **Pattern**: `[chapter-filename]_whitepaper.html`
- **Example**: `09_security_fundamentals_whitepaper.html`
- **Location**: `releases/whitepapers/` (release mode) or `whitepapers/` (standard mode)

### Diagram Path Resolution
- **Relative Paths**: Always use relative paths from the whitepaper location
- **Source Directory**: `docs/images/`
- **Naming Convention**: `diagram_[chapter]_[name].png`
- **Fallback**: If diagram not found, omit the figure element gracefully

---

## Version Control and Metadata

### Release Information
Whitepapers must display:
- **Version Number**: e.g., "2025.10" (from `BOOK_REQUIREMENTS.md`)
- **Build Number**: CI/CD build identifier (optional)
- **Release Date**: British English format, no leading zero (e.g., "5 November 2025")
- **Codename**: Release codename (e.g., "Alpha")
- **Feature Tags**: Visual tags highlighting key release features

### Data Attributes
Store metadata in HTML `data-*` attributes for programmatic access:
```html
<div class="page" 
     data-release-version="2025.10" 
     data-feature-tags="diagram-refresh, governance-automation, ai-collaboration"
     data-release-codename="Alpha">
```

---

## Quality Checklist

Before publishing a whitepaper, verify:

### Content Quality
- [ ] Title and subtitle accurately reflect chapter content
- [ ] Author and publication date are correct
- [ ] 2–3 condensed content paragraphs present
- [ ] Maximum 6 section topics listed
- [ ] Call-to-action section encourages full chapter reading
- [ ] Diagram (if available) is properly displayed and captioned

### Design and Accessibility
- [ ] All text meets WCAG AA contrast requirements (4.5:1 minimum)
- [ ] Heading hierarchy follows semantic order (H1 → H2 → H3)
- [ ] Images include descriptive `alt` text
- [ ] Code samples use syntax highlighting
- [ ] Responsive layout tested on mobile (min-width 320px)
- [ ] Print layout tested with clean page breaks

### Technical Validation
- [ ] HTML validates against HTML5 standard
- [ ] All CSS variables are defined and used consistently
- [ ] External fonts load correctly (Inter, JetBrains Mono)
- [ ] Prism.js syntax highlighting initialises properly
- [ ] Diagram paths resolve correctly (no 404 errors)

### Metadata and Versioning
- [ ] Release version displayed in metadata section
- [ ] Build number (if available) shown correctly
- [ ] Publication date formatted in British English
- [ ] Feature tags (if present) render as visual pills
- [ ] `data-*` attributes contain correct version information

---

## Future Enhancements

### Planned Improvements
- **PDF Export**: Direct PDF generation from HTML whitepaper
- **Interactive Diagrams**: Clickable/zoomable Mermaid diagrams
- **Dark Mode**: Alternative colour scheme for low-light reading
- **Multi-Language Support**: Localised whitepapers in Swedish, German, etc.
- **Bookmark Functionality**: Allow readers to save reading progress
- **Social Sharing**: Open Graph and Twitter Card metadata

### Experimental Features
- **Progressive Web App (PWA)**: Offline reading capability
- **Table of Contents**: Auto-generated navigation sidebar
- **Search Functionality**: Full-text search across all whitepapers
- **Related Content**: Automatic linking to related chapters

---

## References and Standards

### Design Standards
- **WCAG 2.1 Level AA**: Web Content Accessibility Guidelines
- **ISO 216**: International standard paper sizes (A4)
- **ISO 8601**: Date and time format (YYYY-MM-DD)

### Typography Resources
- [Inter Font Family](https://fonts.google.com/specimen/Inter) – Rasmus Andersson
- [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) – JetBrains
- [Practical Typography](https://practicaltypography.com/) – Matthew Butterick

### Code Highlighting
- [Prism.js](https://prismjs.com/) – Lightweight, extensible syntax highlighter
- [Prism Tomorrow Theme](https://github.com/PrismJS/prism-themes) – Dark code theme

### Colour and Contrast
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Palette Generator](https://coolors.co/)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 5 November 2025 | Gunnar Nordqvist | Initial whitepaper design guidelines created |

---

**Note**: These guidelines align with the existing [PRESENTATION_DESIGN_GUIDELINES.md](PRESENTATION_DESIGN_GUIDELINES.md) and [STYLE_GUIDE.md](STYLE_GUIDE.md) to ensure visual consistency across all Architecture as Code collateral.
