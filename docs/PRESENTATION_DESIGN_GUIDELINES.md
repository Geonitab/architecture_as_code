# Presentation Design Guidelines for Architecture as Code
## Modern and Visually Engaging Presentations

## Purpose
This document defines the design standards for all presentations generated from the Architecture as Code book content. It ensures that every presentation is visually appealing, professionally structured, and aligned with modern presentation best practices whilst maintaining the Kvadrat brand identity.

---

## Core Design Principles

### 1. Visual Hierarchy
- **Clear Information Architecture**: Use size, colour, and spacing to guide the viewer's eye through content in a logical order
- **Rule of Thirds**: Position key elements along imaginary lines that divide the slide into thirds horizontally and vertically
- **Focal Points**: Each slide should have one clear focal point that captures immediate attention
- **White Space**: Embrace generous spacing (minimum 48px margins) to prevent cognitive overload

### 2. Cognitive Load Management
- **One Message Per Slide**: Each slide should communicate a single, clear idea
- **6×6 Rule**: Maximum 6 bullet points with 6 words each (or 20 words total per point for Architecture as Code presentations)
- **Progressive Disclosure**: Reveal information gradually rather than overwhelming with dense slides
- **Visual Anchors**: Use diagrams, icons, and graphics to support (not replace) spoken narrative

### 3. Accessibility and Inclusivity
- **Colour Contrast**: Minimum 4.5:1 ratio for normal text (WCAG AA standard)
- **Readable Typography**: Minimum 18pt body text, 24pt for headings
- **Colour-Blind Friendly**: Never rely solely on colour to convey information
- **Alt Text Ready**: All diagrams should have descriptive captions suitable for screen readers

---

## Slide Format and Layout

### Standard Dimensions
- **Aspect Ratio**: 16:9 widescreen (1280×720px or 1920×1080px)
- **Safe Zone**: Keep critical content within 10% margin from all edges
- **Grid System**: 12-column responsive grid for consistent element alignment

### Slide Types and Layouts

#### 1. Title Slide
**Purpose**: Establish presentation context and brand identity

**Layout**:
- **Full-screen gradient background**: Kvadrat Blue to Kvadrat Blue Dark (135-degree angle)
- **Main title**: 72px, font-weight 800, white colour, centred
- **Subtitle**: 32px, font-weight 400, white 90% opacity
- **Presenter info**: 20px, bottom-aligned, white 80% opacity
- **No header bar**: Full-screen immersive design

**Example Structure**:
```
[Full gradient background]
  Main Title (72px bold)
  Subtitle (32px regular)
  
  Presenter Name · Date
```

#### 2. Section Divider Slide
**Purpose**: Signal transitions between major presentation sections

**Layout**:
- **Blank slide** with minimal text
- **Section title**: 64px, font-weight 700, Kvadrat Blue
- **Optional tagline**: 24px, Kvadrat Grey, positioned below title
- **Optional visual element**: Abstract geometric shape or gradient overlay (10% opacity)

#### 3. Content Slide – Hero Layout
**Purpose**: Feature a single diagram prominently with supporting points

**Layout**:
- **Header bar**: 80px height, Kvadrat Blue gradient
  - Logo and brand text: Left-aligned
  - Slide number: Right-aligned
- **Title**: 36px, font-weight 700, Kvadrat Blue Dark, 48px top margin
- **Diagram area**: 12.2" width × 3.6" height (1280×384px), centred horizontally
- **Caption**: Below diagram, 12-14px, diagram type and source
- **Key points**: Below caption, 4 bullet points maximum, 18-20px text

**Use When**:
- Showcasing complex diagrams that need maximum visibility
- Presenting flowcharts, architecture diagrams, or sequence diagrams
- Visual content is primary focus

#### 4. Content Slide – Side Layout
**Purpose**: Balance diagram and text content equally

**Layout**:
- **Header bar**: Standard 80px Kvadrat Blue gradient
- **Title**: 36px, font-weight 700, Kvadrat Blue Dark
- **Two-column grid**:
  - **Left column** (image on left for even-numbered slides): 5.8" width × 4.2" height
  - **Right column** (text): 5.8" width, 8 bullet points maximum, 18px text
  - **Gap**: 48px between columns
- **Alternating layout**: Odd slides have image right, even slides have image left

**Use When**:
- Multiple key points require detailed explanation
- Diagram complexity is moderate
- Balance between visual and textual information

#### 5. Two-Column Comparison Slide
**Purpose**: Present contrasting concepts or before/after scenarios

**Layout**:
- **Header bar**: Standard
- **Title**: 36px centred or left-aligned
- **Two equal columns**: 48px gap
- **Column headers**: 28px, font-weight 600, colour-coded (Kvadrat Blue vs. Success Green)
- **Bullet lists**: 20px text, 6 points maximum per column

**Use When**:
- Comparing traditional vs. Architecture as Code approaches
- Showing benefits vs. challenges
- Technical vs. business perspectives

#### 6. Statistics and Data Slide
**Purpose**: Present quantitative information with visual impact

**Layout**:
- **Header bar**: Standard
- **Title**: 36px
- **Stat cards**: 3-column grid, equal width
  - **Number**: 48px, font-weight 800, Kvadrat Blue, centred
  - **Label**: 18px, Kvadrat Grey, centred below number
  - **Background**: Kvadrat Grey Light with 2px Kvadrat Blue Light border
  - **Padding**: 32px vertical, 16px horizontal
  - **Border radius**: 12px

**Visual Enhancements**:
- Optional: Mini chart or icon above number
- Optional: Progress bar or trend indicator

#### 7. Process/Timeline Slide
**Purpose**: Illustrate sequential steps or project phases

**Layout**:
- **Header bar**: Standard
- **Title**: 36px
- **Step indicators**: Circular badges (48px diameter) with numbers
  - **Completed**: Success Green background
  - **Current**: Warning Orange background
  - **Future**: Kvadrat Blue Light background
- **Step descriptions**: 20px text, left-aligned next to badge
- **Connecting lines**: Optional, 2px Kvadrat Grey

#### 8. Code Example Slide
**Purpose**: Display code snippets with syntax highlighting

**Layout**:
- **Header bar**: Standard
- **Title**: 36px
- **Code block**: 
  - **Background**: `#2d2d2d` (dark grey)
  - **Font**: JetBrains Mono, 18px, line-height 1.6
  - **Syntax highlighting**: Prism.js with Tomorrow Night theme
  - **Padding**: 32px
  - **Border radius**: 12px
  - **Max height**: 400px (scroll if longer)
  - **Line numbers**: Optional, 12px grey
- **Caption**: Above or below code, explaining purpose

**Best Practices**:
- Show complete, runnable examples
- Highlight changed lines with subtle background colour
- Include language identifier badge (top-right corner)

#### 9. Thank You / Closing Slide
**Purpose**: End presentation professionally with contact information

**Layout**:
- **Full gradient background**: Success Green to Kvadrat Blue (135-degree angle)
- **Main message**: "Tack!" or "Thank you!" 64px, font-weight 700, white, centred
- **Secondary message**: "Frågor och diskussion" / "Questions and Discussion", 24px, white 90% opacity
- **Contact grid**: 2×2 grid, 48px gap
  - Email, phone, website, location
  - Icon (32px) + text (20px)
- **No header bar**

---

## Typography Standards

### Font Families
- **Primary**: Inter (Google Fonts or system fallback)
  - Modern, highly legible, excellent for presentations
- **Monospace**: JetBrains Mono (for code examples)
  - Clear character distinction, programming-optimised
- **Fallback Stack**: `'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

### Type Scale
```
Title Slide Main Title:     72px / font-weight: 800 / white
Title Slide Subtitle:       32px / font-weight: 400 / white 90%
Section Divider Title:      64px / font-weight: 700 / Kvadrat Blue
Slide Title (H1):           36-48px / font-weight: 700 / Kvadrat Blue Dark
Slide Subtitle (H2):        24-28px / font-weight: 600 / Kvadrat Blue
Section Heading (H3):       22-24px / font-weight: 600 / Kvadrat Blue
Body Text:                  18-20px / font-weight: 400 / Kvadrat Blue Dark
Bullet Points:              18-20px / font-weight: 400 / line-height: 1.4
Captions:                   12-14px / font-weight: 500 / Kvadrat Grey
Footer/Metadata:            12px / font-weight: 400 / Kvadrat Grey
```

### Typography Best Practices
- **Line Height**: 1.4 for body text, 1.2 for headings
- **Letter Spacing**: -0.025em for large headings (≥48px)
- **Maximum Line Length**: 65-75 characters for optimal readability
- **Text Alignment**: Left-aligned for body text, centred for titles/statistics
- **Emphasis**: Use bold (font-weight 600-700) rather than ALL CAPS or italics

---

## Colour Palette and Usage

### Primary Colours
```css
--kvadrat-blue:         hsl(221, 67%, 32%)    /* #1e3a8a */
--kvadrat-blue-light:   hsl(217, 91%, 60%)    /* #3b82f6 */
--kvadrat-blue-dark:    hsl(214, 32%, 18%)    /* #1e293b */
```

### Neutral Colours
```css
--kvadrat-grey:         hsl(215, 20%, 46%)    /* #64748b */
--kvadrat-grey-light:   hsl(214, 32%, 97%)    /* #f1f5f9 */
--white:                hsl(0, 0%, 100%)      /* #ffffff */
--text-primary:         hsl(214, 32%, 18%)    /* #1e293b */
```

### Accent Colours
```css
--success:              hsl(160, 84%, 30%)    /* #059669 */
--warning:              hsl(32, 95%, 44%)     /* #d97706 */
--error:                hsl(0, 84%, 51%)      /* #dc2626 */
--info:                 hsl(217, 91%, 60%)    /* #3b82f6 */
```

### Colour Application Guidelines

#### Backgrounds
- **Slide background**: White (`#ffffff`) default
- **Header bar**: Linear gradient `linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%)`
- **Highlight boxes**: Kvadrat Blue (`#1e3a8a`) for primary, Kvadrat Grey Light (`#f1f5f9`) for secondary
- **Code blocks**: Dark grey (`#2d2d2d`)

#### Text
- **Primary headings**: Kvadrat Blue Dark (`#1e293b`)
- **Secondary headings**: Kvadrat Blue (`#1e3a8a`)
- **Body text**: Kvadrat Blue Dark (`#1e293b`)
- **Muted text**: Kvadrat Grey (`#64748b`)
- **Inverted (on dark)**: White (`#ffffff`)

#### Interactive Elements
- **Keyword banners**: Kvadrat Accent (`#d97706`) background, Kvadrat Blue text
- **Progress indicators**: Kvadrat Blue (default), Success Green (completed), Warning Orange (current)
- **Links**: Kvadrat Blue Light (`#3b82f6`) with underline on hover

#### Colour Contrast Validation
All colour combinations must meet WCAG AA standards:
- Kvadrat Blue on White: ✅ 8.2:1 ratio
- Kvadrat Grey on White: ✅ 4.7:1 ratio
- White on Kvadrat Blue: ✅ 8.2:1 ratio
- Kvadrat Blue Dark on White: ✅ 12.3:1 ratio

---

## Diagram and Visual Integration

### Diagram Presentation Standards

#### Diagram Metadata
Every diagram should include:
1. **Type label**: Small banner above diagram (e.g., "Flowchart", "Sequence Diagram")
2. **Source reference**: Below diagram, 11px, grey text (e.g., "Source: diagram_05_01.mmd")
3. **Explanation**: 1-2 sentence caption, 12px, limited to 18 words

#### Diagram Sizing
- **Hero layout**: 1280px width × 384px height maximum
- **Side layout**: 608px width × 441px height maximum
- **Scaling**: Preserve aspect ratio, centre within bounds
- **Placeholder**: If diagram missing, show rounded rectangle with "Flowchart pending" text

#### Diagram Types Prioritisation
When multiple diagrams exist in a chapter:
1. **Flowcharts** (preferred for presentations)
2. Sequence diagrams
3. Class diagrams
4. Entity-relationship diagrams
5. Other types

### Mermaid Diagram Standards
All Mermaid diagrams embedded in presentations must follow Kvadrat theme:
```yaml
%%{init: {
  'theme':'base',
  'themeVariables': {
    'primaryColor':'#1e3a8a',
    'primaryTextColor':'#ffffff',
    'primaryBorderColor':'#1e293b',
    'lineColor':'#64748b',
    'secondaryColor':'#3b82f6',
    'tertiaryColor':'#f1f5f9',
    'background':'#ffffff',
    'mainBkg':'#1e3a8a',
    'secondBkg':'#3b82f6',
    'labelBackground':'#f1f5f9',
    'labelTextColor':'#1e293b',
    'fontFamily':'Inter'
  }
}}%%
```

### Icon and Illustration Guidelines
- **Style**: Outline icons (Lucide React library preferred)
- **Size**: 16px, 20px, 24px, 32px (use standardised sizes)
- **Colour**: Kvadrat Blue for primary icons, Kvadrat Grey for secondary
- **Stroke width**: 2px for consistency
- **Usage**: Support text, never replace it

---

## Content Guidelines

### Writing for Slides

#### Slide Titles
- **Descriptive**: Clearly state slide content (e.g., "Security Fundamentals" not "Overview")
- **Concise**: Maximum 10 words
- **Action-oriented**: Use active voice when appropriate (e.g., "Implementing CI/CD Pipelines")

#### Bullet Points
- **Maximum 20 words per point** (Architecture as Code presentations allow longer technical descriptions)
- **Lead with keywords**: Bold the first word or phrase of each bullet
- **Parallel structure**: Use consistent grammatical form across bullets
- **Minimum 6-point leading**: Ensure adequate spacing between bullets

#### Key Highlights Extraction
- Extract from section headings and first meaningful sentence of each section
- Exclude boilerplate text (headings, image captions, code blocks)
- Focus on actionable insights and core concepts
- Limit to 4 highlights for hero layouts, 8 for side layouts

### Speaker Notes
Every slide should include speaker notes with:
1. **Slide title** (reiterated)
2. **Key talking points** (3-5 sentences)
3. **Diagram explanation** (if applicable)
4. **Transition cue** (how to segue to next slide)

---

## Animation and Transition Guidelines

### Slide Transitions
- **Default**: None (instant transition for professional presentations)
- **Optional**: Fade (300ms duration) for section dividers only
- **Avoid**: Wipes, spins, zooms, and other distracting effects

### Content Animations
- **Progressive Disclosure**: Fade in bullet points sequentially (200ms delay between)
- **Diagram Entry**: Fade in (400ms) after title appears
- **Emphasis**: Subtle scale (1.0 → 1.05) and shadow for interactive elements
- **Avoid**: Fly-ins, bounces, and complex multi-step animations

### Timing Recommendations
- **Slide dwell time**: 60-90 seconds average (adjust based on content density)
- **Animation duration**: 200-400ms (fast enough to feel responsive, slow enough to perceive)
- **Pause after title**: 500ms before revealing content

---

## Accessibility Requirements

### Visual Accessibility
- **Colour contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (WCAG AA)
- **Text size**: Minimum 18pt for body text
- **Font weight**: Minimum 400 (regular) for body, 600-700 for headings
- **Link distinction**: Underline or bold in addition to colour
- **Focus indicators**: 2px solid outline for keyboard navigation

### Cognitive Accessibility
- **Consistent layout**: Use same slide types throughout presentation
- **Clear hierarchy**: Size and colour indicate importance
- **Minimal distractions**: Avoid auto-playing media or rapid animations
- **Readable fonts**: Sans-serif with clear character distinction

### Screen Reader Compatibility
- **Alt text**: Provide for all diagrams and images
- **Logical reading order**: Ensure content flows top-to-bottom, left-to-right
- **Semantic structure**: Use heading levels appropriately
- **Table headers**: Mark row/column headers in data tables

---

## Technical Implementation

### PowerPoint (python-pptx) Configuration

#### Presentation Setup
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Configure presentation
prs = Presentation()
prs.slide_width = Inches(13.3333)  # 16:9 aspect ratio
prs.slide_height = Inches(7.5)

# Set metadata
props = prs.core_properties
props.author = "Gunnar Nordqvist"
props.title = "Architecture as Code"
props.language = "en-GB"
```

#### Colour Constants
```python
THEME_BLUE = RGBColor(30, 58, 138)          # #1e3a8a
THEME_BLUE_LIGHT = RGBColor(59, 130, 246)   # #3b82f6
THEME_BLUE_DARK = RGBColor(30, 41, 59)      # #1e293b
THEME_GREY = RGBColor(100, 116, 139)        # #64748b
THEME_GREY_LIGHT = RGBColor(241, 245, 249)  # #f1f5f9
THEME_ACCENT = RGBColor(217, 119, 6)        # #d97706
THEME_SUCCESS = RGBColor(5, 150, 105)       # #059669
```

### HTML/CSS Presentation Template

#### Container Structure
```html
<div class="presentation-container">
  <div class="slide [title-slide|content-slide|section-slide]">
    <div class="slide-header">
      <div class="logo-section">
        <div class="logo">K</div>
        <div class="brand-text">Kvadrat</div>
      </div>
      <div class="slide-number">2 / 45</div>
    </div>
    <div class="slide-content">
      <!-- Slide-specific content -->
    </div>
  </div>
</div>
```

#### CSS Variables
```css
:root {
  --kvadrat-blue: hsl(221, 67%, 32%);
  --kvadrat-blue-light: hsl(217, 91%, 60%);
  --kvadrat-blue-dark: hsl(214, 32%, 18%);
  --kvadrat-grey: hsl(215, 20%, 46%);
  --kvadrat-grey-light: hsl(214, 32%, 97%);
  --slide-width: 1280px;
  --slide-height: 720px;
  --slide-padding: 48px;
  --slide-border-radius: 12px;
}
```

### Prezi/Reveal.js Integration

#### Slide Data Structure (JSON)
```json
{
  "id": "slide-01-introduction",
  "title": "Introduction to Architecture as Code",
  "type": "content-hero",
  "diagram": {
    "path": "docs/images/diagram_01_01.png",
    "type": "Flowchart",
    "caption": "Architecture as Code workflow"
  },
  "keyPoints": [
    "Architecture as Code enables version-controlled system design",
    "Declarative approach ensures reproducible infrastructure",
    "Automation reduces manual configuration errors",
    "Integration with CI/CD pipelines accelerates delivery"
  ],
  "speakerNotes": "Introduce Architecture as Code as evolution from manual processes..."
}
```

---

## Quality Assurance Checklist

### Pre-Generation Validation
- [ ] All chapters have at least one diagram (run `python generate_presentation.py --validate-diagrams`)
- [ ] Diagram types are balanced (flowcharts, sequence, class diagrams present)
- [ ] Source images exist in `docs/images/` directory
- [ ] Mermaid source files (`.mmd`) include Kvadrat theme configuration

### Post-Generation Review
- [ ] Slide count is reasonable (1 slide per 2-3 minutes of presentation)
- [ ] All diagrams render correctly with proper aspect ratios
- [ ] Text is readable at projected size (minimum 18pt)
- [ ] Colour contrast meets WCAG AA standards (4.5:1 minimum)
- [ ] No orphaned bullet points (minimum 2 bullets per list)
- [ ] Speaker notes are complete and informative
- [ ] Slide numbering is accurate
- [ ] Brand elements (logo, colours, fonts) are consistent

### Accessibility Audit
- [ ] Alt text present for all diagrams
- [ ] Colour is not sole means of conveying information
- [ ] Font sizes meet minimum requirements (18pt body, 36pt titles)
- [ ] Sufficient contrast between text and background
- [ ] Logical reading order (top-to-bottom, left-to-right)
- [ ] No flashing or rapidly changing content

### Technical Validation
- [ ] PowerPoint file opens without errors in Microsoft PowerPoint
- [ ] PowerPoint file opens without errors in LibreOffice Impress
- [ ] PDF export preserves formatting and embedded fonts
- [ ] HTML presentation displays correctly in Chrome, Firefox, Safari
- [ ] Mobile/tablet view is functional (responsive design)

---

## Presentation Delivery Best Practices

### Preparation
- **Rehearse**: Practice with actual slides, not notes
- **Time**: Aim for 1-2 minutes per slide (adjust based on complexity)
- **Backup**: Have PDF export ready in case of technical issues
- **Equipment check**: Test projector resolution (1920×1080 or 1280×720)

### During Presentation
- **Pace**: Allow time for audience to read slides
- **Engagement**: Ask rhetorical questions, acknowledge reactions
- **Navigation**: Use arrow keys (not mouse clicks) for professional appearance
- **Pointer use**: Laser pointer or built-in presenter tools only when necessary

### Accessibility During Delivery
- **Describe visuals**: Briefly explain diagrams and charts for low-vision attendees
- **Read key points**: Don't assume everyone can read slides clearly
- **Provide handouts**: Offer PDF with speaker notes for attendees who need them
- **Record**: Enable captions if recording for later viewing

---

## Maintenance and Evolution

### Version Control
- Store presentation source files in `presentations/` directory
- Version presentation data files (`presentation_data.json`) in Git
- Tag releases with semantic versioning (e.g., `presentation-v1.2.0`)
- Document changes in `CHANGELOG.md`

### Continuous Improvement
- Gather feedback after each presentation delivery
- Track which slides prompt most questions (may need clarification)
- Monitor time spent per slide (adjust content density)
- Update diagrams when underlying architecture changes

### Brand Guideline Updates
When Kvadrat brand guidelines change:
1. Update colour constants in `generate_presentation.py`
2. Regenerate all presentations with `--release` flag
3. Review sample slides for consistency
4. Update this document to reflect changes

---

## Examples and Templates

### Example: Architecture Decision Records Slide

**Layout**: Content Slide – Hero Layout

**Title**: "Architecture Decision Records (ADR)"

**Diagram**: `diagram_04_02_adr_workflow.png` (Flowchart showing ADR creation process)

**Caption**: "Diagram: ADR lifecycle from proposal to implementation"

**Key Points**:
- ADRs capture architectural decisions in version-controlled documents
- Structured format: Context, Decision, Consequences, Status
- Integrated with pull request workflows for collaborative review
- Immutable once accepted, superseded rather than modified

**Speaker Notes**:
"Architecture Decision Records provide a systematic way to document why we made specific architectural choices. The diagram shows how ADRs flow from proposal through review and acceptance. Key benefit: new team members can understand historical context by reading the ADR catalogue."

---

### Example: Two-Column Comparison Slide

**Layout**: Two-Column Comparison Slide

**Title**: "Traditional Infrastructure vs. Architecture as Code"

**Left Column** (Traditional – highlighted in Kvadrat Grey):
- Manual provisioning processes
- Inconsistent environments across teams
- Configuration drift over time
- Limited audit trails
- Slow disaster recovery
- Knowledge locked in individual expertise

**Right Column** (Architecture as Code – highlighted in Success Green):
- Automated provisioning from declarative code
- Identical environments via version control
- Immutable infrastructure prevents drift
- Complete audit history in Git
- Rapid recovery from versioned templates
- Knowledge embedded in repository

**Speaker Notes**:
"The contrast between traditional and Architecture as Code approaches is stark. On the left, we see the challenges of manual infrastructure management. On the right, Architecture as Code addresses each of these pain points through automation, version control, and declarative configuration."

---

### Example: Statistics Slide

**Layout**: Statistics and Data Slide

**Title**: "Impact of Architecture as Code Adoption"

**Stat Cards** (3-column grid):
1. **90%** / Fewer configuration errors
2. **75%** / Faster deployment cycles
3. **60%** / Reduced infrastructure costs

**Source Citation**: "Based on 2024 DevOps Research and Assessment (DORA) report"

**Speaker Notes**:
"Industry data confirms the transformative impact of Architecture as Code. Organisations report dramatic reductions in configuration errors because infrastructure is tested and validated before deployment. Deployment cycles accelerate thanks to automation. And costs decrease as teams eliminate waste and optimise resource allocation."

---

## Appendix: Related Documentation

### Internal References
- [STYLE_GUIDE.md](STYLE_GUIDE.md) – Editorial standards for British English
- [BRAND_GUIDELINES.md](docs/archive/book-cover/source/BRAND_GUIDELINES.md) – Kvadrat brand identity
- [generate_presentation.py](../generate_presentation.py) – Presentation generation script
- [presentation-template.html](../templates/presentation-template.html) – HTML presentation template

### External Standards
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) – Web accessibility standards
- [Material Design](https://material.io/design/communication/data-visualization.html) – Data visualisation best practices
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/presentations) – Presentation design principles

---

## Document Metadata

**Version**: 1.0  
**Last Updated**: 5 November 2025  
**Maintained By**: Architecture as Code Editorial Team  
**Contact**: For questions about presentation design standards, create an issue in the GitHub repository  
**Licence**: This document follows the same licence as the main Architecture as Code repository
