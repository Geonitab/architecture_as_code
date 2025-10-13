# Syntax Highlighting Implementation

This document describes the syntax highlighting implementation for all deliverables in the Kodarkitektur Bokverkstad project.

## Overview

The project uses different syntax highlighting solutions for different output formats:

### HTML Deliverables (Whitepapers & Presentations)

**Technology**: Prism.js via CDN

**Implementation**:
- Prism.js CSS and JavaScript are loaded from CloudFlare CDN in HTML templates
- No local installation or build step required
- Templates automatically include Prism.js resources

**Files Modified**:
- `templates/whitepaper-template.html` - Whitepaper HTML template
- `templates/presentation-template.html` - Presentation HTML template

**Prism.js Configuration**:
- **Theme**: `prism-tomorrow` (dark theme for better contrast)
- **Plugins**: 
  - Line numbers support
  - Autoloader for dynamic language loading
- **Languages Supported**:
  - YAML
  - JSON
  - Python
  - Bash/Shell
  - JavaScript
  - TypeScript
  - Docker
  - Terraform

**CDN Resources**:
```html
<!-- CSS -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css" rel="stylesheet" />

<!-- JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
```

### PDF/EPUB/DOCX Deliverables (Book Formats)

**Technology**: Pandoc's built-in Skylighting engine

**Implementation**:
- Pandoc automatically provides syntax highlighting using the Skylighting library
- Configured via `docs/pandoc.yaml`
- No additional dependencies required

**Files Modified**:
- `docs/pandoc.yaml` - Added `highlight-style: tango`

**Configuration**:
```yaml
# Syntax highlighting configuration
highlight-style: tango
# Alternative highlight styles: pygments, kate, monochrome, espresso, zenburn, haddock, breezedark, tango
```

**Available Highlight Styles**:
- `tango` - Default, balanced colors (currently selected)
- `pygments` - Classic Python syntax highlighter style
- `kate` - KDE Kate editor style
- `monochrome` - Black and white
- `espresso` - Dark theme
- `zenburn` - Low-contrast dark theme
- `haddock` - Haskell documentation style
- `breezedark` - KDE Breeze dark theme

### React Web Application

**Technology**: react-syntax-highlighter with Prism.js

**Implementation**:
- Already implemented in the React dashboard
- Uses `react-syntax-highlighter` package with Prism.js engine
- Supports VS Code Dark+ theme

**Files**:
- Package dependency in `package.json`
- Used in React components for code preview

## Workflow Integration

The `.github/workflows/unified-build-release.yml` workflow has been updated to:

1. **Document** syntax highlighting configuration
2. **Include** template files in workflow triggers
3. **Include** `docs/pandoc.yaml` in workflow triggers

No additional installation steps are required in the workflow because:
- Prism.js is loaded via CDN (no installation needed)
- Pandoc's Skylighting is built-in (comes with Pandoc)

## Usage Examples

### For Markdown Code Blocks

Simply use standard markdown code fences with language identifiers:

\`\`\`python
def example():
    print("This will be syntax highlighted")
\`\`\`

\`\`\`yaml
apiVersion: v1
kind: Service
metadata:
  name: example
\`\`\`

\`\`\`bash
#!/bin/bash
echo "Shell script with syntax highlighting"
\`\`\`

### For HTML Templates

Code blocks in HTML templates should use Prism.js class naming:

```html
<pre><code class="language-python">
def example():
    print("Syntax highlighted code")
</code></pre>
```

Or with line numbers:

```html
<pre class="line-numbers"><code class="language-yaml">
apiVersion: v1
kind: Service
</code></pre>
```

## Testing

To verify syntax highlighting works:

1. **Whitepapers**: Generate whitepapers and open in browser
   ```bash
   python3 generate_whitepapers.py --release
   # Open releases/whitepapers/*.html in browser
   ```

2. **Book Formats**: Generate book and check PDF
   ```bash
   python3 generate_book.py && cd docs && ./build_book.sh --release
   # Check releases/book/architecture_as_code.pdf for colored code blocks
   ```

3. **Presentations**: Generate presentations
   ```bash
   python3 generate_presentation.py --release
   # Check any HTML presentation files
   ```

## Customization

### Changing Prism.js Theme

Edit the theme link in the HTML templates:

```html
<!-- Current: prism-tomorrow (dark) -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />

<!-- Alternative: prism-okaidia (dark) -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" rel="stylesheet" />

<!-- Alternative: prism (light) -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
```

### Changing Pandoc Highlight Style

Edit `docs/pandoc.yaml`:

```yaml
# Change from tango to another style
highlight-style: zenburn  # or pygments, kate, espresso, etc.
```

### Adding More Languages to Prism.js

Add language components to HTML templates:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-rust.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-go.min.js"></script>
```

## References

- [Prism.js Official Documentation](https://prismjs.com/)
- [Prism.js CDN (CloudFlare)](https://cdnjs.com/libraries/prism)
- [Pandoc User Guide - Syntax Highlighting](https://pandoc.org/MANUAL.html#syntax-highlighting)
- [Skylighting (Pandoc's highlighting library)](https://github.com/jgm/skylighting)

## Troubleshooting

### Code blocks not highlighted in HTML

1. Check browser console for CDN loading errors
2. Verify code blocks use correct class names (`language-*`)
3. Ensure Prism.js scripts are loaded (check page source)

### Code blocks not highlighted in PDF

1. Verify `highlight-style` is set in `docs/pandoc.yaml`
2. Check Pandoc version supports syntax highlighting (3.1.9+)
3. Try alternative highlight styles if colors don't appear

### Missing language support

1. Add the specific language component script to HTML template
2. For Pandoc, check if Skylighting supports the language
3. Use generic code blocks if language not supported
