#!/bin/bash
# Change to docs directory only if not already there
if [ "$(basename "$PWD")" != "docs" ]; then
    cd docs || exit 1
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

# Check if Eisvogel template exists
if [ ! -f "$EISVOGEL_TEMPLATE" ]; then
    echo "Fel: Pandoc-mall Eisvogel saknas ($EISVOGEL_TEMPLATE)"
    echo "Installera med: pandoc --print-default-data-file eisvogel.latex > $EISVOGEL_TEMPLATE"
    exit 1
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
    "01_inledning_en.md"
    "02_grundlaggande_principer_en.md"
    "03_versionhantering_en.md"
    "04_adr_en.md"
    "05_automatisering_devops_cicd_en.md"
    "06_molnarkitektur_en.md"
    "07_containerisering_en.md"
    "08_microservices_en.md"
    "09_sakerhet_en.md"
    "10_policy_sakerhet_en.md"
    "11_compliance_en.md"
    "12_teststrategier_en.md"
    "13_praktisk_implementation_en.md"
    "14_kostnadsoptimering_en.md"
    "15_migration_en.md"
    "16_organisatorisk_forandring_en.md"
    "17_team_struktur_en.md"
    "18_digitalisering_en.md"
    "19_lovable_mockups_en.md"
    "20_framtida_trender_en.md"
    "21_best_practices_en.md"
    "22_slutsats_en.md"
    "23_ordlista_en.md"
    "24_om_forfattarna_en.md"
    "25_framtida_utveckling_en.md"
    "26_appendix_kodexempel_en.md"
    "27_teknisk_uppbyggnad_en.md"
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
        --variable classoption=oneside \
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