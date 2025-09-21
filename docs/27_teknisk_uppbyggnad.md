# Teknisk uppbyggnad för bokproduktion

Detta kapitel beskriver den tekniska infrastrukturen och arbetsflödet som används för att skapa, bygga och publicera "Arkitektur som kod". Systemet exemplifierar praktisk tillämpning av Architecture as Code-principerna genom att använda kod för att definiera och automatisera hela bokproduktionsprocessen.

![Teknisk arkitektur för bokproduktion](images/diagram_27_teknisk_uppbyggnad.png)

*Diagrammet illustrerar det omfattande tekniska systemet som driver bokproduktionen, från markdown-källor via automatiserade pipelines till slutliga publikationer.*

## Markdown-filer: Struktur och syfte

### Filorganisation och namnkonvention

Bokens innehåll är organiserat i 27 markdown-filer inom `docs/`-katalogen, där varje fil representerar ett kapitel:

```
docs/
├── 01_inledning.md                    # Introduktion och vision
├── 02_grundlaggande_principer.md      # Grundläggande koncept
├── 03_versionhantering.md             # Git och versionskontroll
├── ...                                # Tekniska kapitel (04-22)
├── 23_slutsats.md                     # Avslutning
├── 24_ordlista.md                     # Terminologi
├── 25_om_forfattarna.md               # Författarinformation
├── 26_appendix_kodexempel.md          # Tekniska exempel
└── 27_teknisk_uppbyggnad.md           # Detta kapitel
```

### Markdown-struktur och semantik

Varje kapitel följer en konsistent struktur som optimerar både läsbarhet och maskinell bearbetning:

```markdown
# Kapiteltitel (H1 - skapar ny sida i PDF)

Introduktionstext med kort beskrivning av kapitlets innehåll.

![Diagram titel](images/diagram_XX_filnamn.png)

*Bildtext som förklarar diagrammets innehåll.*

## Huvudsektion (H2)
### Undersektion (H3)
#### Detaljsektion (H4)

- Listpunkter för strukturerat innehåll
- Kodexempel i fenced code blocks
- Referenser och källor
```

### Automatisk innehållsgenerering

Systemet använder `generate_book.py` för att automatiskt generera och uppdatera kapitelinnehåll:

- **Iterativ generering**: Skapar innehåll i kontrollerade batch-processer
- **Mermaid-integration**: Automatisk generering av diagram-placeholders
- **Konsistenshållning**: Säkerställer enhetlig struktur över alla kapitel
- **Versionskontroll**: Alla ändringar spåras genom Git

## Pandoc: Konvertering och formatering

### Konfigurationssystem

Pandoc-konverteringen styrs av `pandoc.yaml` som definierar alla format-specifika inställningar:

```yaml
# Grundläggande inställningar
standalone: true
toc: true
toc-depth: 3
number-sections: true
top-level-division: chapter

# Eisvogel-mall för professionell PDF-layout
template: eisvogel.latex
pdf-engine: xelatex

# Metadata och variabler
metadata:
  title: "Arkitektur som kod"
  subtitle: "Infrastructure as Code i praktiken"
  author: "Kodarkitektur Bokverkstad"
```

### Build-process och automatisering

`build_book.sh` orchestrerar hela build-processen:

1. **Miljövalidering**: Kontrollerar Pandoc, XeLaTeX och Mermaid CLI
2. **Diagram-konvertering**: Konverterar `.mmd`-filer till PNG-format
3. **PDF-generering**: Sammanställer alla kapitel till en sammanhållen bok
4. **Format-variationer**: Stöd för PDF, EPUB och DOCX-export

```bash
# Konvertera Mermaid-diagram
for mmd_file in images/*.mmd; do
    png_file="${mmd_file%.mmd}.png"
    mmdc -i "$mmd_file" -o "$png_file" \
         -t default -b transparent \
         --width 1400 --height 900
done

# Generera PDF med alla kapitel
pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o arkitektur_som_kod.pdf
```

### Kvalitetssäkring och validering

- **Template-validering**: Automatisk kontroll av Eisvogel-mall
- **Konfigurationskontroll**: Verifierar pandoc.yaml-inställningar
- **Bildhantering**: Säkerställer alla diagram-referenser är giltiga
- **Utdata-verifiering**: Kontrollerar genererade filer

## GitHub Actions: CI/CD-pipeline

### Huvudworkflow för bokproduktion

`build-book.yml` automatiserar hela publikationsprocessen:

```yaml
name: Build Book
on:
  push:
    branches: [main]
    paths:
      - 'docs/**/*.md'
      - 'docs/images/**/*.mmd'
  pull_request:
    branches: [main]
  workflow_dispatch: {}

jobs:
  build-book:
    runs-on: ubuntu-latest
    timeout-minutes: 90
```

### Workflow-steg och optimeringar

1. **Miljöuppställning (15 minuter)**:
   - Python 3.12 installation
   - TeXLive och XeLaTeX (8+ minuter)
   - Pandoc 3.1.9 installation
   - Mermaid CLI med Chrome-dependencies

2. **Cachning och prestanda**:
   - APT-paket caching för snabbare builds
   - Pip-dependencies caching
   - Node.js modules caching

3. **Build-process (30 sekunder)**:
   - Diagram-generering från Mermaid-källor
   - PDF-kompilering med Pandoc
   - Kvalitetskontroller och validering

4. **Publicering och distribution**:
   - Automatisk release-skapande vid main-branch pushes
   - Artifact-lagring (30 dagar)
   - PDF-distribution via GitHub Releases

### Kompletterande workflows

**Content Validation** (`content-validation.yml`):
- Markdown-syntaxvalidering
- Länk-kontroll och bildvalidering
- Språklig kvalitetskontroll

**Presentation Generation** (`generate-presentations.yml`):
- PowerPoint-material från bokkapitel
- Strukturerade presentationsoutlines
- Kvadrat-branding och professionell styling

**Whitepaper Generation** (`generate-whitepapers.yml`):
- Individuella HTML-dokument per kapitel
- Standalone-format för distribution
- SEO-optimerat och print-vänligt

## Presentation-material: Förberedelse och generering

### Automatisk outline-generering

`generate_presentation.py` skapar presentationsmaterial från bokinnehåll:

```python
def generate_presentation_outline():
    """Genererar presentationsoutline från alla bokkapitel."""
    docs_dir = Path("docs")
    chapter_files = sorted(glob.glob(str(docs_dir / "*.md")))
    
    presentation_data = []
    for chapter_file in chapter_files:
        chapter_data = read_chapter_content(chapter_file)
        if chapter_data:
            presentation_data.append({
                'file': Path(chapter_file).name,
                'chapter': chapter_data
            })
    
    return presentation_data
```

### PowerPoint-integration

Systemet genererar:
- **Presentation outline**: Strukturerad markdown med nyckelbudskap
- **Python PowerPoint-script**: Automatisk slide-generering
- **Kvadrat-branding**: Konsistent visuell identitet
- **Innehållsoptimering**: Anpassat för muntlig presentation

### Distribution och användning

```bash
# Ladda ner artifacts från GitHub Actions
cd presentations
pip install -r requirements.txt
python generate_pptx.py
```

Resultatet är professionella PowerPoint-presentationer optimerade för:
- Konferenser och workshops
- Utbildningssyfte
- Marknadsföringsaktiviteter
- Tekniska seminarier

## Omslag och whitepapers: Design och integration

### Omslag-designsystem

Bokens omslag skapas genom ett HTML/CSS-baserat designsystem:

```
exports/book-cover/
├── source/
│   ├── book-cover.html              # Huvuddesign
│   ├── book-cover-light.html        # Ljus variant
│   └── book-cover-minimal.html      # Minimal design
├── pdf/                             # Print-färdiga PDF-filer
├── png/                             # Högupplösta PNG-exportar
└── scripts/
    └── generate_book_cover_exports.py
```

### Kvadrat-varumärkesintegrering

Designsystemet implementerar Kvadrat-identiteten:

```css
:root {
    --kvadrat-blue: hsl(221, 67%, 32%);
    --kvadrat-blue-light: hsl(217, 91%, 60%);
    --kvadrat-blue-dark: hsl(214, 32%, 18%);
    --success: hsl(160, 84%, 30%);
}

.title {
    font-size: 72px;
    font-weight: 800;
    line-height: 0.9;
    letter-spacing: -2px;
}
```

### Whitepaper-generering

`generate_whitepapers.py` skapar standalone HTML-dokument:

- **26 individuella whitepapers**: Ett per kapitel
- **Professionell HTML-design**: Responsiv och print-vänlig
- **Svenska anpassningar**: Optimerat för svenska organisationer
- **SEO-optimering**: Korrekt meta-data och struktur
- **Distribution-vänligt**: Kan delas via e-post, webb eller print

## Teknisk arkitektur och systemintegration

### Helhetssyn på arkitekturen

Hela systemet exemplifierar Architecture as Code genom:

1. **Kodifierad innehållshantering**: Markdown som källa för sanning
2. **Automatiserad pipeline**: Ingen manuell intervention krävs
3. **Versionskontroll**: Fullständig historik över alla ändringar
4. **Reproducerbarhet**: Identiska builds från samma källkod
5. **Skalbarhet**: Enkelt att lägga till nya kapitel och format

### Kvalitetssäkring och testning

- **Automatiserad validering**: Kontinuerlig kontroll av innehåll och format
- **Build-verifiering**: Säkerställer att alla format genereras korrekt
- **Performance-monitoring**: Spårning av build-tider och resursanvändning
- **Error-hantering**: Robusta felmeddelanden och återställningsmekanismer

### Framtida utveckling

Systemet är designat för kontinuerlig förbättring:
- **Modulär arkitektur**: Enkelt att uppdatera enskilda komponenter
- **API-möjligheter**: Potential för integration med externa system
- **Skalning**: Stöd för fler format och distributionskanaler
- **Internationalisering**: Förberedelse för flerspråkig publicering

## Sammanfattning

Den tekniska uppbyggnaden för "Arkitektur som kod" demonstrerar praktisk tillämpning av bokens egna principer. Genom att kodifiera hela publikationsprocessen uppnås:

- **Automatisering**: Komplett CI/CD för bokproduktion
- **Kvalitet**: Konsistent format och professionell presentation
- **Effektivitet**: Snabb iteration och feedback-loopar
- **Skalbarhet**: Enkelt att utöka med nytt innehåll och format
- **Transparens**: Öppen källkod och dokumenterad process

Detta tekniska system fungerar som en konkret illustration av hur Architecture as Code-principerna kan tillämpas även utanför traditionella IT-system, vilket skapar värde genom automation, reproducerbarhet och kontinuerlig förbättring.

Källor:
- GitHub Actions Documentation. "Workflow syntax for GitHub Actions." GitHub, 2024.
- Pandoc User's Guide. "Creating documents with Pandoc." John MacFarlane, 2024.
- Mermaid Documentation. "Diagram syntax and examples." Mermaid Community, 2024.
- LaTeX Project. "The Eisvogel template documentation." LaTeX Community, 2024.