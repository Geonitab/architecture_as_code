#!/bin/bash
cd english/docs || exit 1

OUTPUT_PDF="architecture_as_code.pdf"
PANDOC_TEMPLATES_DIR="$HOME/.local/share/pandoc/templates"
EISVOGEL_TEMPLATE="$PANDOC_TEMPLATES_DIR/eisvogel.latex"

if [ ! -f "$EISVOGEL_TEMPLATE" ]; then
    echo "Error: Pandoc template Eisvogel missing ($EISVOGEL_TEMPLATE)"
    echo "Install with: pandoc --print-default-data-file eisvogel.latex > $EISVOGEL_TEMPLATE"
    exit 1
fi

# Convert mermaid files to PNG
for mmd_file in images/*.mmd; do
    if [ -f "$mmd_file" ]; then
        png_file="${mmd_file%.mmd}.png"
        PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" -t dark -b transparent --width 1200 --height 800
        echo "Converted $mmd_file to $png_file"
    fi
done

# Generate PDF with Pandoc
pandoc --standalone --template="$EISVOGEL_TEMPLATE" --toc --toc-depth=3 --number-sections --pdf-engine=xelatex -s -o $OUTPUT_PDF 01_introduction.md 02_chapter1.md

echo "English book generated: $OUTPUT_PDF"