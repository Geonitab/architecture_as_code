# Book Cover design - "Architecture as Code"

## Overview
Professional book cover design for Kvadrat's "Architecture as Code" publication. The design follows Kvadrat's brand guidelines and incorporates modern visual elements that reflect the theme of code architecture.

## Active Cover Template

### Primary Design (Vector Format)
**File:** `templates/book-cover.svg`
- Infinitely scalable SVG format
- Modern gradient background (Kvadrat Blue to Dark Blue)
- Advanced code architecture visual elements
- Professional typography with highlighted "code" text
- Perfect for editing in vector graphics software
- Suitable for both digital and print formats
- Includes metadata and structured elements

This is the **single approved front cover** used in the book build process.

## Single Cover Guarantee

The book build process ensures that exactly **one front cover** appears in all output formats:

### PDF Generation
- The cover is included via the `include-before` section in `docs/pandoc.yaml`
- The Eisvogel template's default `cover-image` variable is NOT used to avoid duplication
- Result: Single custom title page with cover image, title, subtitle, and metadata

### EPUB Generation
- The cover is specified via `--epub-cover-image="images/book-cover.png"` flag
- Result: Single EPUB cover page

### Build Process
1. `templates/book-cover.svg` is converted to PNG by `docs/build_book.sh`
2. The PNG is saved as `docs/images/book-cover.png`
3. Pandoc includes the cover and release information page in PDF output
4. EPUB and DOCX builds insert a markdown cover page so non-PDF formats ship with the same metadata
5. EPUB generation uses the same PNG file as its cover

This architecture guarantees no duplicate or redundant cover variants in distribution artifacts.

## Export Formats

The design is available in multiple high-resolution formats:

### Print-Ready Files
- **PDF**: 300 DPI print-ready format
- **PNG**: High-resolution raster (2480×3508 pixels at 300 DPI)
- **JPEG**: Compressed format for digital distribution

### Digital Formats
- **PNG**: Medium resolution for web use (150 DPI)
- **JPEG**: Optimised for social media and email
- **SVG**: Vector format for infinite scalability

## Technical Specifications

### Dimensions
- **Format**: A4 (210mm × 297mm)
- **Aspect Ratio**: Standard book cover proportions
- **Resolution**: 300 DPI for print, 150 DPI for screen

### Brand Compliance
The design strictly follows Kvadrat Brand Guidelines:

#### Colour Palette
```css
--kvadrat-blue: hsl(221, 67%, 32%)        /* Primary brand colour */
--kvadrat-blue-light: hsl(217, 91%, 60%)  /* Accent and highlights */
--kvadrat-blue-dark: hsl(214, 32%, 18%)   /* Text and contrast */
--success: hsl(160, 84%, 30%)             /* Gradient accent */
```

#### Typography
- **Font**: Inter (weights: 400, 500, 600, 700, 800, 900)
- **Fallback**: systems-ui, -apple-systems, sans-serif
- **Hierarchy**: Clear typography scale with proper contrast

#### Logo
- Kvadrat "K" logo in white rounded square
- Proper spacing and brand text
- Consistent placement and sizing

### Design Elements

#### Code Architecture Theme
- Geometric patterns suggesting network connectivity
- Subtle grid background representing infrastructure
- Modern visual elements reflecting technical nature
- Professional gradient overlays

#### Layout Structure
- **Header**: Logo and brand information
- **Main Content**: Title with emphasized "code" highlight
- **Subtitle**: Comprehensive description
- **Footer**: Author and edition information

## Usage Instructions

### For Print Production
1. Use `exports/book-cover/pdf/book-cover-print.pdf`
2. Ensure printer supports RGB colour space (convert to CMYK if needed)
3. Recommended paper: High-quality matte or glossy finish

### For Digital Distribution
1. **High-quality web**: Use PNG 300 DPI version
2. **Social media**: Use JPEG 150 DPI version
3. **Email attachments**: Use compressed JPEG format

### For Further Editing
1. **Vector editing**: Use SVG file in Adobe Illustrator or Inkscape
2. **Web modifications**: Edit HTML/CSS files
3. **Brand compliance**: Follow included brand guidelines

## Build Integration

The book cover is automatically processed during the PDF build:

1. The build script (`docs/build_book.sh`) converts `templates/book-cover.svg` to PNG
2. The PNG is embedded in the PDF via pandoc configuration (`docs/pandoc.yaml`)
3. The same cover image is used for EPUB generation

## File Structure
```
templates/
└── book-cover.svg             # Single approved cover template

exports/book-cover/
├── pdf/                       # Print-ready PDF files
├── png/                       # High-resolution PNG files
├── jpg/                       # JPEG exports
├── svg/                       # Vector files
├── source/                    # Editable source files for designers
│   ├── book-cover-final.html  # HTML/CSS source (for design editing)
│   ├── book-cover.html        # HTML/CSS source (alternate version)
│   ├── book-cover.svg         # SVG source (editable)
│   ├── BRAND_GUIDELINES.md    # Brand compliance guidelines
│   └── DESIGN_SYSTEM.md       # Design system documentation
└── README.md                  # Usage documentation
```

## Quality Assurance

### Brand Guidelines Compliance
- ✅ Kvadrat colour palette strictly followed
- ✅ Typography hierarchy maintained
- ✅ Logo placement and sizing correct
- ✅ Professional aesthetic aligned with brand

### Technical Quality
- ✅ High-resolution outputs (300 DPI for print)
- ✅ Multiple format support
- ✅ Print-ready specifications
- ✅ Cross-browser compatibility

### Accessibility
- ✅ Sufficient colour contrast ratios
- ✅ Readable typography at all sizes
- ✅ Clean, professional design
- ✅ Semantic HTML structure

## Maintenance

### Updating the design
1. Modify `templates/book-cover.svg` directly in a vector editor (Inkscape, Adobe Illustrator)
2. Optionally, edit the HTML/CSS source files in `exports/book-cover/source/` for web-based design work
3. Test the build process: `docs/build_book.sh`
4. Verify the cover appears correctly in the generated PDF and EPUB

### Brand Updates
If Kvadrat brand guidelines change:
1. Update the SVG file in `templates/book-cover.svg`
2. Update source files in `exports/book-cover/source/` if needed
3. Regenerate the book to verify changes
4. Update brand documentation if necessary

## Support

For questions about the design or technical implementation:
- Review brand guidelines in `exports/book-cover/source/`
- Check design systems documentation
- Follow established colour and typography standards

---

**design Version**: 1.0  
**Created**: December 2024  
**Brand Guidelines**: Kvadrat v1.0  
**Formats**: HTML/CSS, SVG, PDF, PNG, JPEG
