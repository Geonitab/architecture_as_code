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

# Konvertera mermaid-filer till PNG
for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" -t dark -b transparent --width 1200 --height 800
        echo "Konverterade $mmd_file till $png_file"
    fi
done

# Generera PDF med Pandoc använd konfigurationsfil
echo "Genererar PDF med Pandoc-konfiguration..."

# Function to check if new descriptive filename exists, otherwise use old
get_chapter_file() {
    local new_file="$1"
    local old_file="$2"
    if [ -f "$new_file" ]; then
        echo "$new_file"
    else
        echo "$old_file"
    fi
}

# Build chapter list with fallback to old names
CHAPTER_FILES=(
    "01_inledning.md"
    "$(get_chapter_file "02_grundlaggande_principer.md" "02_kapitel1.md")"
    "$(get_chapter_file "03_versionhantering.md" "03_kapitel2.md")"
    "$(get_chapter_file "04_adr.md" "04_adr_kapitel.md")"
    "$(get_chapter_file "05_automatisering_cicd.md" "05_kapitel3.md")"
    "$(get_chapter_file "06_devops_cicd.md" "08_kapitel6.md")"
    "$(get_chapter_file "07_molnarkitektur.md" "06_kapitel4.md")"
    "$(get_chapter_file "08_containerisering.md" "12_kapitel10.md")"
    "$(get_chapter_file "09_microservices.md" "14_kapitel12.md")"
    "$(get_chapter_file "10_sakerhet.md" "07_kapitel5.md")"
    "$(get_chapter_file "11_policy_sakerhet.md" "13_kapitel11.md")"
    "$(get_chapter_file "12_compliance.md" "15_kapitel13.md")"
    "$(get_chapter_file "13_teststrategier.md" "18_kapitel16.md")"
    "$(get_chapter_file "14_praktisk_implementation.md" "09_kapitel7.md")"
    "$(get_chapter_file "15_kostnadsoptimering.md" "17_kapitel15.md")"
    "$(get_chapter_file "16_migration.md" "19_kapitel17.md")"
    "$(get_chapter_file "17_organisatorisk_forandring.md" "11_kapitel9.md")"
    "$(get_chapter_file "18_team_struktur.md" "16_kapitel14.md")"
    "$(get_chapter_file "19_digitalisering.md" "10_kapitel8.md")"
    "$(get_chapter_file "20_lovable_mockups.md" "21_kapitel20.md")"
    "$(get_chapter_file "21_framtida_trender.md" "20_kapitel18.md")"
    "$(get_chapter_file "22_best_practices.md" "22_kapitel19.md")"
    "23_slutsats.md"
    "24_ordlista.md"
    "25_om_forfattarna.md"
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