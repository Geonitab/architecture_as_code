# Presentation Quality Checklist
## Ensuring Compliance with PRESENTATION_DESIGN_GUIDELINES.md

This checklist ensures that all generated presentations meet the standards defined in `PRESENTATION_DESIGN_GUIDELINES.md`.

---

## Pre-Generation Validation

### Content Preparation
- [ ] All chapters have meaningful titles (maximum 10 words)
- [ ] Key points are extracted from section headings and first sentences
- [ ] Each bullet point is limited to 20 words maximum
- [ ] Chapters are assigned to appropriate parts/sections
- [ ] Front matter and part introductions are complete

### Diagram Readiness
- [ ] All Mermaid `.mmd` files include Kvadrat theme configuration
- [ ] Diagrams are rendered to PNG format in `docs/images/`
- [ ] Each chapter has at least one diagram (run `--validate-diagrams`)
- [ ] Diagram types are balanced (flowcharts, sequence, class diagrams present)
- [ ] All diagram files are accessible and not corrupted

### Validation Commands
```bash
# Validate diagram coverage and types
python3 generate_presentation.py --validate-diagrams

# Validate presentation guidelines compliance
python3 scripts/validate_presentation_guidelines.py

# Generate validation report
python3 scripts/validate_presentation_guidelines.py --report reports/presentation_validation.md
```

---

## Post-Generation Review

### Visual Design Compliance

#### Typography
- [ ] Title slide main title: 72px, font-weight 800, white colour
- [ ] Title slide subtitle: 32px, font-weight 400, white 90% opacity
- [ ] Section divider titles: 64px, font-weight 700, Kvadrat Blue
- [ ] Slide titles (H1): 36-48px, font-weight 700, Kvadrat Blue Dark
- [ ] Body text: 18-20px minimum, font-weight 400, Kvadrat Blue Dark
- [ ] Captions: 12-14px, font-weight 500, Kvadrat Grey
- [ ] Line height: 1.4 for body text, 1.2 for headings
- [ ] Font family: Inter (primary), JetBrains Mono (code)

#### Colour Usage
- [ ] Kvadrat Blue (#1e3a8a) used for primary headings and branding
- [ ] Kvadrat Blue Dark (#1e293b) used for primary body text
- [ ] Kvadrat Grey (#64748b) used for muted text and captions
- [ ] Accent Orange (#d97706) used for keyword banners
- [ ] White (#ffffff) used for inverted text on dark backgrounds
- [ ] All colour combinations meet WCAG AA contrast standards (4.5:1 minimum)

#### Layout and Spacing
- [ ] Slide dimensions: 1280×720px or 1920×1080px (16:9 aspect ratio)
- [ ] Margins: Minimum 48px from all edges
- [ ] Border radius: 12px for rounded elements
- [ ] Safe zone: Critical content within 10% margin from edges
- [ ] Consistent spacing between elements (8px, 16px, 24px, 48px scale)

#### Slide Types
- [ ] Title slide uses full gradient background with centred text
- [ ] Section dividers use minimal text with optional geometric shapes
- [ ] Hero layouts feature full-width diagrams (12.2" × 3.6")
- [ ] Side layouts balance diagrams (5.8" × 4.2") with text equally
- [ ] Keyword banners positioned appropriately (not overlapping content)

### Content Quality

#### Text Content
- [ ] No slide has more than 4 bullet points (hero layout)
- [ ] No slide has more than 8 bullet points (side layout)
- [ ] All bullet points are under 20 words
- [ ] First word of each bullet is bolded (keyword emphasis)
- [ ] Slide titles are descriptive and action-oriented
- [ ] No duplicate slide titles (confuses screen readers)

#### Diagram Integration
- [ ] Each diagram has a type label above it (e.g., "Flowchart", "Sequence Diagram")
- [ ] Source reference below diagram (e.g., "Source: diagram_05_01.mmd")
- [ ] Explanation caption (1-2 sentences, maximum 18 words)
- [ ] Diagrams are centred and scaled to fit within bounds
- [ ] Aspect ratio preserved (no distortion)
- [ ] Placeholder shown if diagram is missing ("Diagram pending")

#### Speaker Notes
- [ ] Every slide has speaker notes
- [ ] Notes include slide title
- [ ] Notes list key talking points (3-5 sentences)
- [ ] Diagram explanations included in notes
- [ ] Transition cues provided (how to segue to next slide)

---

## Accessibility Validation

### Visual Accessibility
- [ ] Colour contrast minimum 4.5:1 for normal text (WCAG AA)
- [ ] Text size minimum 18pt for body text
- [ ] Font weight minimum 400 for body, 600-700 for headings
- [ ] Links distinguished by underline or bold in addition to colour
- [ ] Focus indicators visible (2px solid outline for keyboard navigation)

### Cognitive Accessibility
- [ ] Consistent layout throughout presentation
- [ ] Clear visual hierarchy (size and colour indicate importance)
- [ ] No auto-playing media or rapid animations
- [ ] Readable sans-serif fonts with clear character distinction
- [ ] Generous white space to prevent cognitive overload

### Screen Reader Compatibility
- [ ] Alt text provided for all diagrams (in speaker notes)
- [ ] Logical reading order (top-to-bottom, left-to-right)
- [ ] Semantic structure with appropriate heading levels
- [ ] No reliance on colour alone to convey information

---

## Technical Validation

### File Format Compatibility
- [ ] PowerPoint file opens without errors in Microsoft PowerPoint 2016+
- [ ] PowerPoint file opens without errors in LibreOffice Impress 7.0+
- [ ] PDF export preserves formatting and embedded fonts
- [ ] HTML presentation displays correctly in Chrome, Firefox, Safari
- [ ] Mobile/tablet view is functional (responsive design)

### File Size and Performance
- [ ] PowerPoint file size under 50MB (for email distribution)
- [ ] Diagrams optimised (PNG compression applied)
- [ ] No unnecessary embedded objects
- [ ] Fonts embedded or using web-safe alternatives
- [ ] HTML presentation loads within 3 seconds on standard connection

### Metadata and Properties
- [ ] Presentation metadata populated (author, title, date)
- [ ] Language set to "en-GB" (British English)
- [ ] Slide numbering accurate
- [ ] Version/revision tracked in metadata

---

## Delivery Preparation

### Pre-Presentation Testing
- [ ] Rehearsed with actual slides (not just notes)
- [ ] Timing verified (1-2 minutes per slide average)
- [ ] PDF backup created and accessible
- [ ] Equipment tested with target projector/screen
- [ ] Resolution compatibility verified (1920×1080 or 1280×720)

### Accessibility During Delivery
- [ ] Plan to describe visuals briefly for low-vision attendees
- [ ] Prepared to read key points aloud
- [ ] PDF with speaker notes available for attendees who need them
- [ ] Recording enabled with captions if recording for later viewing

### Distribution Preparation
- [ ] PowerPoint file tested on multiple systems
- [ ] PDF version generated for universal compatibility
- [ ] HTML version published if web distribution needed
- [ ] Handout version created (6 slides per page recommended)

---

## Continuous Improvement

### Post-Presentation Review
- [ ] Gathered feedback from attendees
- [ ] Tracked which slides prompted most questions (may need clarification)
- [ ] Monitored time spent per slide (adjust content density)
- [ ] Noted technical issues for future prevention

### Version Control
- [ ] Presentation source files committed to Git
- [ ] Version tagged with semantic versioning (e.g., `presentation-v1.2.0`)
- [ ] Changes documented in changelog
- [ ] Regenerated from source after updates

### Brand Guideline Alignment
- [ ] Reviewed against latest Kvadrat brand guidelines
- [ ] Colour constants updated in `generate_presentation.py` if changed
- [ ] Regenerated all presentations with `--release` flag
- [ ] Sample slides reviewed for consistency

---

## Automated Validation

Run these commands to automatically validate compliance:

```bash
# 1. Validate diagram coverage
python3 generate_presentation.py --validate-diagrams

# 2. Validate presentation guidelines
python3 scripts/validate_presentation_guidelines.py

# 3. Generate detailed validation report
python3 scripts/validate_presentation_guidelines.py --report reports/presentation_validation.md

# 4. Strict validation (exit with error on warnings)
python3 scripts/validate_presentation_guidelines.py --strict
```

---

## Quick Reference: Common Issues

| Issue | Guideline Violated | Fix |
|-------|-------------------|-----|
| Bullet point has 25 words | Maximum 20 words | Shorten to focus on key insight |
| Title text is 14pt | Minimum 36pt for titles | Increase font size in code |
| 6 bullets on hero layout | Maximum 4 for hero | Move to side layout or reduce bullets |
| Diagram without caption | Metadata required | Add type, source, explanation |
| Low contrast grey on white | Minimum 4.5:1 ratio | Use Kvadrat Grey (#64748b) |
| Duplicate slide titles | Confuses screen readers | Make titles unique and descriptive |
| Missing speaker notes | Required for all slides | Add notes with talking points |
| Slide has 150 words of text | Cognitive overload | Use bullet points, limit to 80 words total |

---

## Document Metadata

**Version:** 1.0  
**Last Updated:** 5 November 2025  
**Maintained By:** Architecture as Code Editorial Team  
**Related Documentation:**
- [PRESENTATION_DESIGN_GUIDELINES.md](PRESENTATION_DESIGN_GUIDELINES.md)
- [STYLE_GUIDE.md](STYLE_GUIDE.md)
- [Kvadrat Brand Guidelines](archive/book-cover/source/BRAND_GUIDELINES.md)
