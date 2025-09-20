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
# Check if all required files exist, otherwise use available files
required_files="01_introduction.md 02_chapter1.md 03_chapter2.md 21_conclusion.md 22_glossary.md 23_about_authors.md"
available_files=""
missing_files=""

for file in $required_files; do
    if [ -f "$file" ]; then
        available_files="$available_files $file"
    else
        missing_files="$missing_files $file"
    fi
done

if [ -n "$missing_files" ]; then
    echo "Warning: Missing files:$missing_files"
    echo "Building with available files..."
    # Build with all available markdown files
    all_md_files=$(ls *.md 2>/dev/null | sort)
    if [ -n "$all_md_files" ]; then
        pandoc --standalone --template="$EISVOGEL_TEMPLATE" --toc --toc-depth=3 --number-sections --pdf-engine=xelatex -s -o $OUTPUT_PDF $all_md_files
    else
        echo "Error: No markdown files found"
        exit 1
    fi
else
    echo "All required files found, building complete book..."
    pandoc --standalone --template="$EISVOGEL_TEMPLATE" --toc --toc-depth=3 --number-sections --pdf-engine=xelatex -s -o $OUTPUT_PDF $available_files
fi

echo "English book generated: $OUTPUT_PDF"