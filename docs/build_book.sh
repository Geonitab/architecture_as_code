#!/bin/bash
cd docs || exit 1

OUTPUT_PDF="arkitektur_som_kod.pdf"
PANDOC_TEMPLATES_DIR="$HOME/.local/share/pandoc/templates"
EISVOGEL_TEMPLATE="$PANDOC_TEMPLATES_DIR/eisvogel.latex"

if [ ! -f "$EISVOGEL_TEMPLATE" ]; then
    echo "Fel: Pandoc-mall Eisvogel saknas ($EISVOGEL_TEMPLATE)"
    echo "Installera med: pandoc --print-default-data-file eisvogel.latex > $EISVOGEL_TEMPLATE"
    exit 1
fi

# Konvertera mermaid-filer till PNG
for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        mmdc -i "$mmd_file" -o "$png_file" -t dark -b transparent
        echo "Konverterade $mmd_file till $png_file"
    fi
done

# Generera PDF med Pandoc
pandoc --standalone --template="$EISVOGEL_TEMPLATE" --toc --toc-depth=3 --number-sections --pdf-engine=xelatex -s -o $OUTPUT_PDF 01_inledning.md 02_kapitel1.md 03_kapitel2.md 04_kapitel3.md 21_slutsats.md 22_ordlista.md 23_om_forfattarna.md

echo "Bok genererad: $OUTPUT_PDF"