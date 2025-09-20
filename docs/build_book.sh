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
pandoc --defaults=pandoc.yaml \
  01_inledning.md \
  02_kapitel1.md \
  03_kapitel2.md \
  04_adr_kapitel.md \
  05_kapitel3.md \
  06_kapitel4.md \
  07_kapitel5.md \
  08_kapitel6.md \
  09_kapitel7.md \
  10_kapitel8.md \
  11_kapitel9.md \
  12_kapitel10.md \
  13_kapitel11.md \
  14_kapitel12.md \
  15_kapitel13.md \
  16_kapitel14.md \
  17_kapitel15.md \
  18_kapitel16.md \
  19_kapitel17.md \
  20_kapitel18.md \
  21_kapitel20.md \
  22_kapitel19.md \
  23_slutsats.md \
  24_ordlista.md \
  25_om_forfattarna.md \
  -o $OUTPUT_PDF

echo "Bok genererad: $OUTPUT_PDF"

# Funktion för att generera andra format
generate_other_formats() {
    echo "Genererar EPUB-format..."
    pandoc --defaults=pandoc.yaml \
      01_inledning.md 02_kapitel1.md 03_kapitel2.md 04_adr_kapitel.md 05_kapitel3.md \
      06_kapitel4.md 07_kapitel5.md 08_kapitel6.md 09_kapitel7.md 10_kapitel8.md \
      11_kapitel9.md 12_kapitel10.md 13_kapitel11.md 14_kapitel12.md 15_kapitel13.md \
      16_kapitel14.md 17_kapitel15.md 18_kapitel16.md 19_kapitel17.md 20_kapitel18.md \
      21_kapitel20.md 22_kapitel19.md 23_slutsats.md 24_ordlista.md 25_om_forfattarna.md \
      -t epub -o $OUTPUT_EPUB
    echo "EPUB genererad: $OUTPUT_EPUB"
    
    echo "Genererar DOCX-format..."
    pandoc --defaults=pandoc.yaml \
      01_inledning.md 02_kapitel1.md 03_kapitel2.md 04_adr_kapitel.md 05_kapitel3.md \
      06_kapitel4.md 07_kapitel5.md 08_kapitel6.md 09_kapitel7.md 10_kapitel8.md \
      11_kapitel9.md 12_kapitel10.md 13_kapitel11.md 14_kapitel12.md 15_kapitel13.md \
      16_kapitel14.md 17_kapitel15.md 18_kapitel16.md 19_kapitel17.md 20_kapitel18.md \
      21_kapitel20.md 22_kapitel19.md 23_slutsats.md 24_ordlista.md 25_om_forfattarna.md \
      -t docx -o $OUTPUT_DOCX
    echo "DOCX genererad: $OUTPUT_DOCX"
}

# Generera andra format om begärt
if [ "$1" = "--all-formats" ]; then
    generate_other_formats
fi