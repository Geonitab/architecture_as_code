#!/bin/bash
# Change to docs directory only if not already there
if [ "$(basename "$PWD")" != "docs" ]; then
    cd docs || exit 1
fi

# Determine the release directory path (relative to docs directory)
RELEASE_DIR="../release/book"
OUTPUT_PDF="arkitektur_som_kod.pdf"
OUTPUT_EPUB="arkitektur_som_kod.epub"
OUTPUT_DOCX="arkitektur_som_kod.docx"
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
    "01_inledning.md"
    "02_grundlaggande_principer.md"
    "03_versionhantering.md"
    "04_adr.md"
    "05_automatisering_devops_cicd.md"
    "06_molnarkitektur.md"
    "07_containerisering.md"
    "08_microservices.md"
    "09_sakerhet.md"
    "10_policy_sakerhet.md"
    "11_compliance.md"
    "12_teststrategier.md"
    "13_praktisk_implementation.md"
    "14_kostnadsoptimering.md"
    "15_migration.md"
    "16_organisatorisk_forandring.md"
    "17_team_struktur.md"
    "18_digitalisering.md"
    "19_lovable_mockups.md"
    "20_framtida_trender.md"
    "21_best_practices.md"
    "22_slutsats.md"
    "23_ordlista.md"
    "24_om_forfattarna.md"
    "25_framtida_utveckling.md"
    "26_appendix_kodexempel.md"
    "27_teknisk_uppbyggnad.md"
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

# Funktion för att generera andra format
generate_other_formats() {
    echo "Genererar EPUB-format..."
    pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -t epub -o $OUTPUT_EPUB
    echo "EPUB genererad: $OUTPUT_EPUB"
    cp $OUTPUT_EPUB "$RELEASE_EPUB"
    echo "EPUB kopierad till release: $RELEASE_EPUB"
    
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