#!/bin/bash
# Change to docs directory only if not already there
if [ "$(basename "$PWD")" != "docs" ]; then
    cd docs || exit 1
fi

# Helper to run package manager commands with sudo when necessary
run_with_privileges() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        return 1
    fi
}

# Resolve the best available Chrome/Chromium binary for Mermaid CLI
find_chrome_executable() {
    local candidate
    for candidate in google-chrome google-chrome-stable chromium-browser chromium; do
        if command -v "$candidate" >/dev/null 2>&1; then
            command -v "$candidate"
            return 0
        fi
    done

    return 1
}

# Ensure Pandoc is available, installing it when possible
ensure_pandoc() {
    if command -v pandoc >/dev/null 2>&1; then
        return 0
    fi

    echo "⚠️  Pandoc is missing – attempting automatic installation..."

    if command -v apt-get >/dev/null 2>&1; then
        if run_with_privileges env DEBIAN_FRONTEND=noninteractive apt-get update && \
           run_with_privileges env DEBIAN_FRONTEND=noninteractive apt-get install -y pandoc; then
            echo "✅ Pandoc installed via apt-get"
            return 0
        fi
    elif command -v apt >/dev/null 2>&1; then
        if run_with_privileges env DEBIAN_FRONTEND=noninteractive apt update && \
           run_with_privileges env DEBIAN_FRONTEND=noninteractive apt install -y pandoc; then
            echo "✅ Pandoc installed via apt"
            return 0
        fi
    elif command -v dnf >/dev/null 2>&1; then
        if run_with_privileges dnf install -y pandoc; then
            echo "✅ Pandoc installed via dnf"
            return 0
        fi
    elif command -v yum >/dev/null 2>&1; then
        if run_with_privileges yum install -y pandoc; then
            echo "✅ Pandoc installed via yum"
            return 0
        fi
    elif command -v pacman >/dev/null 2>&1; then
        if run_with_privileges pacman -Sy --noconfirm pandoc; then
            echo "✅ Pandoc installed via pacman"
            return 0
        fi
    elif command -v zypper >/dev/null 2>&1; then
        if run_with_privileges zypper install -y pandoc; then
            echo "✅ Pandoc installed via zypper"
            return 0
        fi
    elif command -v brew >/dev/null 2>&1; then
        if brew list pandoc >/dev/null 2>&1 || brew install pandoc; then
            echo "✅ Pandoc installed via Homebrew"
            return 0
        fi
    fi

    echo "❌ Failed to install Pandoc automatically. Install Pandoc manually and rerun the script."
    return 1
}

# Render the SVG cover into a PNG that Pandoc can embed
render_cover_from_svg() {
    local svg_path="$1"
    local output_path="$2"

    # Prefer librsvg for consistent rendering (available in Docker build image)
    if command -v rsvg-convert >/dev/null 2>&1; then
        if rsvg-convert -w 2480 -h 3508 -o "$output_path" "$svg_path"; then
            return 0
        fi
    fi

    # Fallback to Inkscape if it is available locally
    if command -v inkscape >/dev/null 2>&1; then
        if inkscape "$svg_path" \
            --export-type=png \
            --export-filename="$output_path" \
            --export-width=2480 \
            --export-height=3508 >/dev/null 2>&1; then
            return 0
        fi
    fi

    # As a final fallback, attempt ImageMagick convert if present
    if command -v convert >/dev/null 2>&1; then
        if convert "$svg_path" -resize 2480x3508 "$output_path"; then
            return 0
        fi
    fi

    return 1
}

# Ensure Pandoc is available before continuing
if ! command -v pandoc >/dev/null 2>&1; then
    if ! ensure_pandoc; then
        exit 1
    fi
fi

# Determine the release directory path (relative to docs directory)
RELEASE_DIR="../releases/book"
OUTPUT_PDF="architecture_as_code.pdf"
OUTPUT_EPUB="architecture_as_code.epub"
OUTPUT_DOCX="architecture_as_code.docx"
RELEASE_PDF="$RELEASE_DIR/$OUTPUT_PDF"
RELEASE_EPUB="$RELEASE_DIR/$OUTPUT_EPUB"
RELEASE_DOCX="$RELEASE_DIR/$OUTPUT_DOCX"
PANDOC_TEMPLATES_DIR="$HOME/.local/share/pandoc/templates"
EISVOGEL_TEMPLATE="$PANDOC_TEMPLATES_DIR/eisvogel.latex"

# Ensure Eisvogel template exists (install automatically if missing)
if [ ! -f "$EISVOGEL_TEMPLATE" ]; then
    echo "⚠️  Eisvogel template missing – attempting automatic installation..."
    mkdir -p "$PANDOC_TEMPLATES_DIR"

    if command -v pandoc >/dev/null 2>&1 && pandoc --print-default-data-file eisvogel.latex > "$EISVOGEL_TEMPLATE" 2>/dev/null; then
        echo "✅ Eisvogel template installed at $EISVOGEL_TEMPLATE"
    else
        echo "⚠️  Direct installation failed – downloading from GitHub..."

        TEMP_DIR=$(mktemp -d)
        TEMPLATE_ARCHIVE="$TEMP_DIR/Eisvogel.tar.gz"

        if command -v curl >/dev/null 2>&1; then
            curl -fsSL "https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz" -o "$TEMPLATE_ARCHIVE"
        elif command -v wget >/dev/null 2>&1; then
            wget -qO "$TEMPLATE_ARCHIVE" "https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz"
        else
            echo "❌ Neither curl nor wget is available to download the template."
            echo "   Install one of those tools or add the template manually."
            rm -rf "$TEMP_DIR"
            exit 1
        fi

        if [ -s "$TEMPLATE_ARCHIVE" ] && tar -xzf "$TEMPLATE_ARCHIVE" -C "$TEMP_DIR" 2>/dev/null; then
            FOUND_TEMPLATE=$(find "$TEMP_DIR" -name "eisvogel.latex" -print -quit)
            if [ -n "$FOUND_TEMPLATE" ] && cp "$FOUND_TEMPLATE" "$EISVOGEL_TEMPLATE"; then
                echo "✅ Eisvogel template downloaded and installed at $EISVOGEL_TEMPLATE"
            else
                echo "❌ Could not extract the Eisvogel template from the downloaded archive."
                rm -rf "$TEMP_DIR"
                exit 1
            fi
        else
            echo "❌ Failed to download the Eisvogel template from GitHub."
            rm -rf "$TEMP_DIR"
            exit 1
        fi

        rm -rf "$TEMP_DIR"
    fi
fi

# Check if pandoc.yaml config exists
if [ ! -f "pandoc.yaml" ]; then
    echo "Error: Missing Pandoc configuration file (pandoc.yaml)"
    exit 1
fi

# Ensure release directory exists
mkdir -p "$RELEASE_DIR"

# Copy book cover to images directory for Pandoc
echo "Preparing book cover..."
COVER_OUTPUT_PATH="images/book-cover.png"
COVER_SVG_SOURCE="../templates/book-cover.svg"
COVER_PNG_FALLBACK="../exports/book-cover/png/book-cover-300dpi.png"

if [ -f "$COVER_SVG_SOURCE" ]; then
    if render_cover_from_svg "$COVER_SVG_SOURCE" "$COVER_OUTPUT_PATH"; then
        echo "✅ Book cover rendered from templates/book-cover.svg"
    else
        echo "⚠️  Warning: Failed to render book cover from SVG."
        if [ -f "$COVER_PNG_FALLBACK" ]; then
            cp "$COVER_PNG_FALLBACK" "$COVER_OUTPUT_PATH"
            echo "✅ Fallback cover copied from exports/book-cover/png/book-cover-300dpi.png"
        else
            echo "❌ No fallback PNG cover available at $COVER_PNG_FALLBACK"
        fi
    fi
elif [ -f "$COVER_PNG_FALLBACK" ]; then
    cp "$COVER_PNG_FALLBACK" "$COVER_OUTPUT_PATH"
    echo "✅ Fallback cover copied from exports/book-cover/png/book-cover-300dpi.png"
else
    echo "⚠️  Warning: Book cover not found at $COVER_SVG_SOURCE or $COVER_PNG_FALLBACK"
fi

CHROME_FLAGS="${CHROME_FLAGS:-}"
CHROME_EXECUTABLE=""
PUPPETEER_CONFIG_FILE=""

if CHROME_EXECUTABLE=$(find_chrome_executable); then
    export PUPPETEER_EXECUTABLE_PATH="$CHROME_EXECUTABLE"
else
    echo "⚠️  Warning: No Chrome or Chromium executable found in PATH. Mermaid CLI will rely on its bundled Chromium."
    unset PUPPETEER_EXECUTABLE_PATH
fi

if [ -n "$CHROME_FLAGS" ]; then
    read -r -a CHROME_FLAGS_ARRAY <<< "$CHROME_FLAGS"
    if [ ${#CHROME_FLAGS_ARRAY[@]} -gt 0 ]; then
        PUPPETEER_CONFIG_FILE=$(mktemp)
        {
            echo '{'
            echo '  "args": ['
            for i in "${!CHROME_FLAGS_ARRAY[@]}"; do
                flag=${CHROME_FLAGS_ARRAY[$i]}
                if [ "$i" -gt 0 ]; then
                    printf ',\n'
                fi
                printf '    "%s"' "$flag"
            done
            printf '\n'
            echo '  ]'
            echo '}'
        } > "$PUPPETEER_CONFIG_FILE"
        trap 'if [ -n "$PUPPETEER_CONFIG_FILE" ]; then rm -f "$PUPPETEER_CONFIG_FILE"; fi' EXIT
    fi
fi

# Convert Mermaid files to PNG with Kvadrat styling
MERMAID_THEME_FILE="mermaid-kvadrat-theme.json"

if [ ! -f "$MERMAID_THEME_FILE" ]; then
    echo "⚠️  Warning: Mermaid theme file '$MERMAID_THEME_FILE' not found. Falling back to default styling."
fi

for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        conversion_success=false

        if [ -n "$PUPPETEER_CONFIG_FILE" ]; then
            echo "Converting $mmd_file (Docker/CI mode)..."
            if mmdc -i "$mmd_file" -o "$png_file" \
                -t default \
                ${MERMAID_THEME_FILE:+-c "$MERMAID_THEME_FILE"} \
                -b transparent \
                --width 1400 \
                --height 900 \
                --puppeteerConfigFile "$PUPPETEER_CONFIG_FILE" \
                2>/dev/null; then
                conversion_success=true
            fi
        else
            echo "Converting $mmd_file (local mode)..."
            if mmdc -i "$mmd_file" -o "$png_file" \
                -t default \
                ${MERMAID_THEME_FILE:+-c "$MERMAID_THEME_FILE"} \
                -b transparent \
                --width 1400 \
                --height 900 \
                2>/dev/null; then
                conversion_success=true
            fi
        fi

        if [ "$conversion_success" = true ] && [ -f "$png_file" ] && [ -s "$png_file" ]; then
            echo "✅ Converted $mmd_file to $png_file with enhanced styling"
        else
            echo "⚠️  Warning: Failed to convert $mmd_file, skipping (PDF generation will continue)"
        fi
    fi
done

# Generate PDF using the Pandoc configuration file
echo "Generating PDF with Pandoc defaults..."

# Build chapter list with descriptive names
CHAPTER_FILES=(
    "part_a_foundations.md"
    "01_introduction.md"
    "02_fundamental_principles.md"
    "03_version_control.md"
    "04_adr.md"
    "part_b_architecture_platform.md"
    "05_automation_devops_cicd.md"
    "07_containerization.md"
    "part_c_security_governance.md"
    "09_security.md"
    "10_policy_and_security.md"
    "11_governance_as_code.md"
    "12_compliance.md"
    "part_d_delivery_operations.md"
    "13_testing_strategies.md"
    "14_practical_implementation.md"
    "15_cost_optimization.md"
    "16_migration.md"
    "part_e_organization_leadership.md"
    "17_organizational_change.md"
    "18_team_structure.md"
    "19_management_as_code.md"
    "20_ai_agent_team.md"
    "21_digitalization.md"
    "part_f_experience_best_practices.md"
    "23_soft_as_code_interplay.md"
    "24_best_practices.md"
    "part_g_future_wrap_up.md"
    "25_future_trends_development.md"
    "27_conclusion.md"
    "part_h_appendices.md"
    "28_glossary.md"
    "30_appendix_code_examples.md"
    "31_technical_architecture.md"
    "33_references.md"
    "29_about_the_authors.md"
)

# Build a sanitized list that excludes LaTeX-only part markers for non-LaTeX formats
NON_LATEX_CHAPTER_FILES=()
for chapter_file in "${CHAPTER_FILES[@]}"; do
    if [[ $chapter_file == part_*.md ]]; then
        continue
    fi
    NON_LATEX_CHAPTER_FILES+=("$chapter_file")
done

pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o "$OUTPUT_PDF" 2>&1

# Check if PDF was actually generated
if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
    echo "✅ Book generated: $OUTPUT_PDF ($(ls -lh "$OUTPUT_PDF" | awk '{print $5}'))"

    # Copy to release directory
    if cp "$OUTPUT_PDF" "$RELEASE_PDF" 2>/dev/null; then
        echo "✅ Book copied to release directory: $RELEASE_PDF"
    else
        echo "⚠️  Warning: Could not copy PDF to release directory"
    fi
else
    echo "❌ Error: PDF generation failed with the Eisvogel template"
    echo "Attempting fallback with the default template..."

    # Try with default LaTeX template
    # Reuse the shared pandoc defaults so LaTeX helpers like \setbookpart stay defined
    if pandoc --defaults=pandoc.yaml \
        --template=default \
        "${CHAPTER_FILES[@]}" \
        -o "$OUTPUT_PDF" \
        2>&1; then

        if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
            echo "✅ Fallback PDF generation succeeded: $OUTPUT_PDF ($(ls -lh "$OUTPUT_PDF" | awk '{print $5}'))"

            # Copy to release directory
            if cp "$OUTPUT_PDF" "$RELEASE_PDF" 2>/dev/null; then
                echo "✅ Fallback PDF copied to release directory: $RELEASE_PDF"
            else
                echo "⚠️  Warning: Could not copy fallback PDF to release directory"
            fi
        else
            echo "❌ Error: Even fallback PDF generation failed"
            exit 1
        fi
    else
        echo "❌ Error: All PDF generation attempts failed"
        exit 1
    fi
fi

# Function to validate EPUB files
validate_epub() {
    local epub_file="$1"
    
    echo "Validating EPUB file with EPUBCheck..."
    
    # Check if EPUBCheck is available
    if ! command -v epubcheck >/dev/null 2>&1; then
        echo "⚠️  Warning: EPUBCheck is not installed - skipping EPUB validation"
        echo "    Install EPUBCheck to enable full EPUB validation"
        return 0
    fi
    
    # Create validation log file
    local validation_log="../releases/book/epub-validation.log"
    
    # Run EPUBCheck with detailed output
    if epubcheck "$epub_file" > "$validation_log" 2>&1; then
        echo "✅ EPUB validation passed: $epub_file"
        echo "    Validation log: $validation_log"
        return 0
    else
        local exit_code=$?
        echo "❌ EPUB validation failed for: $epub_file"
        echo "    Validation log: $validation_log"

        echo "Summary of validation issues:"
        grep -E "(ERROR|FATAL|WARNING)" "$validation_log" | head -10

        if [ $exit_code -eq 1 ]; then
            echo "⚠️  EPUB contains validation warnings but can still be distributed"
            echo "    Review the validation log for additional details"
            return 1
        else
            echo "❌ Critical errors detected in the EPUB file"
            return 2
        fi
    fi
}

# Function to generate other formats
generate_other_formats() {
    echo "Generating EPUB format..."

    # Generate EPUB with improved metadata
    if pandoc --defaults=pandoc.yaml "${NON_LATEX_CHAPTER_FILES[@]}" \
        -t epub \
        -o "$OUTPUT_EPUB" \
        --metadata date="$(date +'%Y-%m-%d')" \
        --metadata language=en \
        --metadata lang=en-GB \
        --epub-cover-image="images/book-cover.png" \
        2>&1; then

        echo "EPUB generated: $OUTPUT_EPUB"

        # Validate the generated EPUB
        validate_epub "$OUTPUT_EPUB"
        validation_result=$?

        # Copy to release directory regardless of validation result
        cp "$OUTPUT_EPUB" "$RELEASE_EPUB"
        echo "EPUB copied to release directory: $RELEASE_EPUB"

        # Report validation status
        case $validation_result in
            0)
                echo "✅ EPUB file validated and ready for distribution"
                ;;
            1)
                echo "⚠️  EPUB file has minor validation issues but remains usable"
                ;;
            2)
                echo "❌ EPUB file contains critical issues - review the validation log"
                ;;
        esac
    else
        echo "❌ EPUB generation failed"
        return 1
    fi

    echo "Generating DOCX format..."
    pandoc --defaults=pandoc.yaml "${NON_LATEX_CHAPTER_FILES[@]}" -t docx -o "$OUTPUT_DOCX"
    echo "DOCX generated: $OUTPUT_DOCX"
    cp "$OUTPUT_DOCX" "$RELEASE_DOCX"
    echo "DOCX copied to release directory: $RELEASE_DOCX"
}

# Generate additional formats when requested or for release builds
if [ "$1" = "--all-formats" ] || [ "$1" = "--release" ]; then
    generate_other_formats
fi

# Information about release directory
if [ "$1" = "--release" ] || [ "$1" = "--all-formats" ]; then
    echo ""
    echo "=== RELEASE DELIVERABLES ==="
    echo "Book formats saved to: $RELEASE_DIR"
    ls -la "$RELEASE_DIR"
fi
