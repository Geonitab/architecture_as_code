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
        PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) mmdc -i "$mmd_file" -o "$png_file" -t dark -b transparent --width 1200 --height 800
        echo "Konverterade $mmd_file till $png_file"
    fi
done

# Generera PDF med Pandoc - all chapters in logical order
pandoc --standalone --template="$EISVOGEL_TEMPLATE" --toc --toc-depth=3 --number-sections --pdf-engine=xelatex -s -o $OUTPUT_PDF \
  01_inledning.md \
  02_grundlaggande_principer.md \
  03_versionhantering.md \
  04_adr.md \
  05_automatisering_cicd.md \
  06_devops_cicd.md \
  07_molnarkitektur.md \
  08_containerisering.md \
  09_microservices.md \
  10_sakerhet.md \
  11_policy_sakerhet.md \
  12_compliance.md \
  13_teststrategier.md \
  14_praktisk_implementation.md \
  15_kostnadsoptimering.md \
  16_migration.md \
  17_organisatorisk_forandring.md \
  18_team_struktur.md \
  19_digitalisering.md \
  20_lovable_mockups.md \
  21_framtida_trender.md \
  22_best_practices.md \
  23_slutsats.md \
  24_ordlista.md \
  25_om_forfattarna.md

echo "Bok genererad: $OUTPUT_PDF"