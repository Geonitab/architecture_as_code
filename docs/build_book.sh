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

# Ensure Pandoc is available, installing it when possible
ensure_pandoc() {
    if command -v pandoc >/dev/null 2>&1; then
        return 0
    fi

    echo "⚠️  Pandoc saknas – försöker installera automatiskt..."

    if command -v apt-get >/dev/null 2>&1; then
        if run_with_privileges env DEBIAN_FRONTEND=noninteractive apt-get update && \
           run_with_privileges env DEBIAN_FRONTEND=noninteractive apt-get install -y pandoc; then
            echo "✅ Pandoc installerat via apt-get"
            return 0
        fi
    elif command -v apt >/dev/null 2>&1; then
        if run_with_privileges env DEBIAN_FRONTEND=noninteractive apt update && \
           run_with_privileges env DEBIAN_FRONTEND=noninteractive apt install -y pandoc; then
            echo "✅ Pandoc installerat via apt"
            return 0
        fi
    elif command -v dnf >/dev/null 2>&1; then
        if run_with_privileges dnf install -y pandoc; then
            echo "✅ Pandoc installerat via dnf"
            return 0
        fi
    elif command -v yum >/dev/null 2>&1; then
        if run_with_privileges yum install -y pandoc; then
            echo "✅ Pandoc installerat via yum"
            return 0
        fi
    elif command -v pacman >/dev/null 2>&1; then
        if run_with_privileges pacman -Sy --noconfirm pandoc; then
            echo "✅ Pandoc installerat via pacman"
            return 0
        fi
    elif command -v zypper >/dev/null 2>&1; then
        if run_with_privileges zypper install -y pandoc; then
            echo "✅ Pandoc installerat via zypper"
            return 0
        fi
    elif command -v brew >/dev/null 2>&1; then
        if brew list pandoc >/dev/null 2>&1 || brew install pandoc; then
            echo "✅ Pandoc installerat via Homebrew"
            return 0
        fi
    fi

    echo "❌ Misslyckades med att installera Pandoc automatiskt. Installera Pandoc manuellt och kör skriptet igen."
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
OUTPUT_PDF="arkitektur_som_kod.pdf"
OUTPUT_EPUB="arkitektur_som_kod.epub"
OUTPUT_DOCX="arkitektur_som_kod.docx"
RELEASE_PDF="$RELEASE_DIR/$OUTPUT_PDF"
RELEASE_EPUB="$RELEASE_DIR/$OUTPUT_EPUB"
RELEASE_DOCX="$RELEASE_DIR/$OUTPUT_DOCX"
PANDOC_TEMPLATES_DIR="$HOME/.local/share/pandoc/templates"
EISVOGEL_TEMPLATE="$PANDOC_TEMPLATES_DIR/eisvogel.latex"

# Ensure Eisvogel template exists (install automatically if missing)
if [ ! -f "$EISVOGEL_TEMPLATE" ]; then
    echo "⚠️  Eisvogel template saknas – försöker installera automatiskt..."
    mkdir -p "$PANDOC_TEMPLATES_DIR"

    if command -v pandoc >/dev/null 2>&1 && pandoc --print-default-data-file eisvogel.latex > "$EISVOGEL_TEMPLATE" 2>/dev/null; then
        echo "✅ Eisvogel template installerad till $EISVOGEL_TEMPLATE"
    else
        echo "⚠️  Direkt installation misslyckades – försöker ladda ner från GitHub..."

        TEMP_DIR=$(mktemp -d)
        TEMPLATE_ARCHIVE="$TEMP_DIR/Eisvogel.tar.gz"

        if command -v curl >/dev/null 2>&1; then
            curl -fsSL "https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz" -o "$TEMPLATE_ARCHIVE"
        elif command -v wget >/dev/null 2>&1; then
            wget -qO "$TEMPLATE_ARCHIVE" "https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz"
        else
            echo "❌ Varken curl eller wget finns tillgängligt för att hämta mallen."
            echo "   Installera verktygen eller lägg till mallen manuellt."
            rm -rf "$TEMP_DIR"
            exit 1
        fi

        if [ -s "$TEMPLATE_ARCHIVE" ] && tar -xzf "$TEMPLATE_ARCHIVE" -C "$TEMP_DIR" 2>/dev/null; then
            FOUND_TEMPLATE=$(find "$TEMP_DIR" -name "eisvogel.latex" -print -quit)
            if [ -n "$FOUND_TEMPLATE" ] && cp "$FOUND_TEMPLATE" "$EISVOGEL_TEMPLATE"; then
                echo "✅ Eisvogel template nedladdad och installerad till $EISVOGEL_TEMPLATE"
            else
                echo "❌ Kunde inte extrahera Eisvogel template från nedladdat arkiv."
                rm -rf "$TEMP_DIR"
                exit 1
            fi
        else
            echo "❌ Misslyckades med att ladda ner Eisvogel template från GitHub."
            rm -rf "$TEMP_DIR"
            exit 1
        fi

        rm -rf "$TEMP_DIR"
    fi
fi

# Check if pandoc.yaml config exists
if [ ! -f "pandoc.yaml" ]; then
    echo "Fel: Pandoc-konfigurationsfil saknas (pandoc.yaml)"
    exit 1
fi

# Ensure release directory exists
mkdir -p "$RELEASE_DIR"

# Copy book cover to images directory for Pandoc
echo "Kopierar bokframsida..."
if [ -f "../exports/book-cover/png/book-cover-300dpi.png" ]; then
    cp "../exports/book-cover/png/book-cover-300dpi.png" "images/book-cover.png"
    echo "✅ Bokframsida kopierad till images/book-cover.png"
else
    echo "⚠️ Warning: Book cover not found at ../exports/book-cover/png/book-cover-300dpi.png"
fi

# Konvertera mermaid-filer till PNG med Kvadrat-tema
for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        
        # Check if Chrome flags are set (Docker/CI environment)
        CHROME_FLAGS="${CHROME_FLAGS:-}"
        conversion_success=false
        
        if [ -n "$CHROME_FLAGS" ]; then
            # Running in Docker/CI environment - use provided Chrome flags
            echo "Converting $mmd_file (Docker/CI mode)..."
            if PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" \
                -t default \
                -b transparent \
                --width 1400 \
                --height 900 \
                --puppeteerConfig "{\"args\": [\"--no-sandbox\", \"--disable-setuid-sandbox\", \"--disable-dev-shm-usage\", \"--disable-accelerated-2d-canvas\", \"--no-first-run\", \"--no-zygote\", \"--disable-gpu\"]}" \
                2>/dev/null; then
                conversion_success=true
            fi
        else
            # Local environment - use standard configuration
            echo "Converting $mmd_file (local mode)..."
            if PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" \
                -t default \
                -b transparent \
                --width 1400 \
                --height 900 \
                2>/dev/null; then
                conversion_success=true
            fi
        fi
        
        # Check conversion result and create placeholder if needed
        if [ "$conversion_success" = true ] && [ -f "$png_file" ] && [ -s "$png_file" ]; then
            echo "✅ Konverterade $mmd_file till $png_file med förbättrad styling"
        else
            echo "⚠️ Warning: Failed to convert $mmd_file, skipping (PDF generation will continue)"
            # Don't fail the build - PDF generation can continue with text placeholders
        fi
    fi
done

# Generera PDF med Pandoc använd konfigurationsfil
echo "Genererar PDF med Pandoc-konfiguration..."

# Build chapter list with descriptive names
CHAPTER_FILES=(
    "part_a_foundations.md"
    "01_introduction.md"
    "02_fundamental_principles.md"
    "03_version_control.md"
    "04_adr.md"
    "part_b_architecture_platform.md"
    "05_automation_devops_cicd.md"
    "06_cloud_architecture.md"
    "07_containerization.md"
    "08_microservices.md"
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
    "22_lovable_mockups.md"
    "23_soft_as_code_interplay.md"
    "24_best_practices.md"
    "part_g_future_wrap_up.md"
    "25_future_trends.md"
    "26_future_development.md"
    "27_conclusion.md"
    "part_h_appendices.md"
    "28_glossary.md"
    "29_about_the_authors.md"
    "30_appendix_code_examples.md"
    "31_technical_architecture.md"
)

pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o $OUTPUT_PDF 2>&1

# Check if PDF was actually generated
if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
    echo "✅ Bok genererad: $OUTPUT_PDF ($(ls -lh $OUTPUT_PDF | awk '{print $5}'))"
    
    # Copy to release directory
    if cp $OUTPUT_PDF "$RELEASE_PDF" 2>/dev/null; then
        echo "✅ Bok kopierad till release: $RELEASE_PDF"
    else
        echo "⚠️ Warning: Could not copy PDF to release directory"
    fi
else
    echo "❌ Error: PDF generation failed with Eisvogel template"
    echo "Attempting fallback with default template..."
    
    # Try with default LaTeX template
    if pandoc "${CHAPTER_FILES[@]}" \
        -o $OUTPUT_PDF \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --top-level-division=chapter \
        --pdf-engine=xelatex \
        --metadata title="Arkitektur som kod" \
        --metadata author="Kodarkitektur Bokverkstad" \
        --variable documentclass=book \
        --variable classoption=twoside \
        --variable geometry=margin=2.5cm \
        --variable fontsize=11pt \
        2>&1; then
        
        if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
            echo "✅ Fallback PDF generation succeeded: $OUTPUT_PDF ($(ls -lh $OUTPUT_PDF | awk '{print $5}'))"
            
            # Copy to release directory
            if cp $OUTPUT_PDF "$RELEASE_PDF" 2>/dev/null; then
                echo "✅ Fallback PDF kopierad till release: $RELEASE_PDF"
            else
                echo "⚠️ Warning: Could not copy fallback PDF to release directory"
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

# Funktioner för att validera EPUB-fil
validate_epub() {
    local epub_file="$1"
    
    echo "Validerar EPUB-fil med EPUBCheck..."
    
    # Check if EPUBCheck is available
    if ! command -v epubcheck >/dev/null 2>&1; then
        echo "⚠️  Warning: EPUBCheck inte installerat - EPUB-validering överhoppad"
        echo "    Installera EPUBCheck för full EPUB-validering"
        return 0
    fi
    
    # Create validation log file
    local validation_log="../releases/book/epub-validation.log"
    
    # Run EPUBCheck with detailed output
    if epubcheck "$epub_file" > "$validation_log" 2>&1; then
        echo "✅ EPUB-validering godkänd: $epub_file"
        echo "    Valideringslogg: $validation_log"
        return 0
    else
        local exit_code=$?
        echo "❌ EPUB-validering misslyckades för: $epub_file"
        echo "    Valideringslogg: $validation_log"
        
        # Show summary of errors
        echo "Sammanfattning av valideringsfel:"
        grep -E "(ERROR|FATAL|WARNING)" "$validation_log" | head -10
        
        if [ $exit_code -eq 1 ]; then
            echo "⚠️  EPUB har valideringsfel men kan fortfarande användas"
            echo "    Kontrollera valideringsloggen för detaljer"
            return 1
        else
            echo "❌ Kritiska fel i EPUB-filen"
            return 2
        fi
    fi
}

# Funktion för att generera andra format
generate_other_formats() {
    echo "Genererar EPUB-format..."
    
    # Generate EPUB with improved metadata
    if pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" \
        -t epub \
        -o $OUTPUT_EPUB \
        --metadata date="$(date +'%Y-%m-%d')" \
        --metadata language=sv \
        --epub-cover-image="images/book-cover.png" \
        2>&1; then
        
        echo "EPUB genererad: $OUTPUT_EPUB"
        
        # Validate the generated EPUB
        validate_epub "$OUTPUT_EPUB"
        validation_result=$?
        
        # Copy to release directory regardless of validation result
        cp $OUTPUT_EPUB "$RELEASE_EPUB"
        echo "EPUB kopierad till release: $RELEASE_EPUB"
        
        # Report validation status
        case $validation_result in
            0)
                echo "✅ EPUB-fil validerad och klar för distribution"
                ;;
            1)
                echo "⚠️  EPUB-fil har mindre valideringsfel men är användbar"
                ;;
            2)
                echo "❌ EPUB-fil har kritiska fel - kontrollera valideringsloggen"
                ;;
        esac
    else
        echo "❌ EPUB-generering misslyckades"
        return 1
    fi
    
    echo "Genererar DOCX-format..."
    pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -t docx -o $OUTPUT_DOCX
    echo "DOCX genererad: $OUTPUT_DOCX"
    cp $OUTPUT_DOCX "$RELEASE_DOCX"
    echo "DOCX kopierad till release: $RELEASE_DOCX"
}

# Generera andra format om begärt eller alltid för release
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