#!/bin/bash
# Change to docs directory only if not already there
if [ "$(basename "$PWD")" != "docs" ]; then
    cd docs || exit 1
fi

OUTPUT_PDF="arkitektur_som_kod.pdf"
OUTPUT_EPUB="arkitektur_som_kod.epub"
OUTPUT_DOCX="arkitektur_som_kod.docx"
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

# Konvertera mermaid-filer till PNG med Kvadrat-tema
for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        # Use default theme with enhanced diagrams that include custom styling
        PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" \
            -t default \
            -b transparent \
            --width 1400 \
            --height 900
        echo "Konverterade $mmd_file till $png_file med förbättrad styling"
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

pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o $OUTPUT_PDF

echo "Bok genererad: $OUTPUT_PDF"

# Funktion för att generera andra format
generate_other_formats() {
    echo "Genererar EPUB-format..."
    pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -t epub -o $OUTPUT_EPUB
    echo "EPUB genererad: $OUTPUT_EPUB"
    
    echo "Genererar DOCX-format..."
    pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -t docx -o $OUTPUT_DOCX
    echo "DOCX genererad: $OUTPUT_DOCX"
}

# Generera andra format om begärt
if [ "$1" = "--all-formats" ]; then
    generate_other_formats
fi