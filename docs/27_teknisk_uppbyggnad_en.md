# Teknisk uppbyggnad for bokproduktion

This chapter beskriver den technical infrastrukturen and arbetsflödet that används for to skapa, bygga and publicera "Architecture as Code". Systemet exemplifierar praktisk toämpning of Architecture as Code-principlesna through to använda code for to definiera and automate the entire bokproduktionsprocessen.

![Teknisk arkitektur for bokproduktion](images/diagram_27_teknisk_uppbyggnad.png)

*The diagram illustrates det comprehensive technical systemet that driver bokproduktionen, from markdown-Sources via automated pipelines to slutliga publikationer.*

![Architecture Data Model](images/diagram_27_er_architecture.png)

Ovanstående entitetsrelationsdiagram visar den logiska datastrukturen for how organizations, projekt, infrastructure and deployments relaterar to varandra in en Architecture as Code-Architecture as Code-implebuttation.

## Markdown-filer: Struktur and purpose

### Filorganization and namnkonvention

The book's innehåll is organiserat in 27 markdown-filer within `docs/`-katalogen, where varje fil representerar ett chapter:

```
docs/
├── 01_inledning.md # Introduktion and vision
├── 02_grundlaggande_principles.md # fundamental koncept
├── 03_versionhantering.md # Git and versionskontroll
├── ... # technical chapter (04-22)
├── 23_slutsats.md # Avslutning
├── 24_ordlista.md # Terminologi
├── 25_om_forfattarna.md # Författarinformation
├── 26_appendix_kodexempel.md # technical exempel
└── 27_teknisk_uppbyggnad.md # This chapter
```

### Markdown-struktur and semantik

Varje chapter följer en konsistent struktur that optimerar både läsbarhet and maskinell bearbetning:

```markdown
# Kapiteltitel (H1 - skapar ny sida in PDF)

Introduktionstext with kort beskrivning of kapitlets innehåll.

![Diagramtitel beskrivning](images/diagram_01_beskrivande_namn.png)

*Bildtext that förklarar diagrammets innehåll.*

## Huvudsektion (H2)
### Undersektion (H3)
#### Detaljsektion (H4)

- Listpunkter for strukturerat innehåll
- Kodexempel in fenced code blocks
- Referenser and Sources
```

### Automatisk innehållsgenerering

Systemet använder `generate_book.py` for to automatically generera and uppdatera kapitelinnehåll:

- **Iterativ generering**: Skapar innehåll in kontrollerade batch-processes
- **Mermaid-integration**: Automatisk generering of diagram-placeholders
- **Konsistenshållning**: ensures enhetlig struktur over all chapter
- **Versionskontroll**: all ändringar spåras through Git

## Pandoc: Konvertering and formatering

### Konfigurationssystem

Pandoc-konverteringen styrs of `pandoc.yaml` that definierar all format-specific inställningar:

```yaml
# Fundamental inställningar
standalone: true
toc: true
toc-depth: 3
number-sections: true
top-level-division: chapter

# Eisvogel-mall for professionell PDF-layout
template: eisvogel.latex
pdf-engine: xelatex

# Metadata and variabler
metadata:
 title: "Architecture as Code"
 subtitle: "Infrastructure as Code (Architecture as Code) in the practice"
 author: "Kodarkitektur Bokverkstad"
```

### Build-process and Architecture as Code-automation

`build_book.sh` orchestrerar the entire build-processen:

1. **Miljövalidering**: Kontrollerar Pandoc, XeLaTeX and Mermaid CLI
2. **Diagram-konvertering**: Konverterar `.mmd`-filer to PNG-format
3. **PDF-generering**: Sammanställer all chapter to en sammanhållen book
4. **Format-variationer**: Stöd for PDF, EPUB and DOCX-export

```bash
# Konvertera Mermaid-diagram
for mmd_file in images/*.mmd; do
 png_file="${mmd_file%.mmd}.png"
 mmdc -in "$mmd_file" -o "$png_file" \
 -t default -b transparent \
 --width 1400 --height 900
done

# Generera PDF with all chapter
pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o arkitektur_that_kod.pdf
```

### Kvalitetssäkring and validering

- **Template-validering**: Automatisk kontroll of Eisvogel-mall
- **Konfigurationskontroll**: Verifierar pandoc.yaml-inställningar
- **Bildhantering**: ensures all diagram-referenser is giltiga
- **Utdata-verifiering**: Kontrollerar genererade filer

## GitHub Actions: CI/CD-pipeline

### Huvudworkflow for bokproduktion

`build-book.yml` automatiserar the entire publikationsprocessen:

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

### Workflow-steg and optimeringar

1. **Miljöuppställning (15 minuter)**:
 - Python 3.12 installation
 - TeXLive and XeLaTeX (8+ minuter)
 - Pandoc 3.1.9 installation
 - Mermaid CLI with Chrome-dependencies

2. **Cachning and prestanda**:
 - APT-paket caching for snabbare builds
 - Pip-dependencies caching
 - Node.js modules caching

3. **Build-process (30 sekunder)**:
 - Diagram-generering from Mermaid-Sources
 - PDF-kompilering with Pandoc
 - Kvalitetskontroller and validering

4. **Publicering and distribution**:
 - Automatisk release-skapande at main-branch pushes
 - Artifact-lagring (30 dagar)
 - PDF-distribution via GitHub Releases

### Kompletterande workflows

**Content Validation** (`content-validation.yml`):
- Markdown-syntaxvalidering
- Länk-kontroll and bildvalidering
- Språklig kvalitetskontroll

**Presentation Generation** (`generate-presentations.yml`):
- PowerPoint-material from bokkapitel
- Strukturerade presentationsoutlines
- Kvadrat-branding and professionell styling

**Whitepaper Generation** (`generate-whitepapers.yml`):
- Individuella HTML-dokubutt per chapter
- Standalone-format for distribution
- SEO-optimerat and print-vänligt

## Presentation-material: Förberedelse and generering

### Automatisk outline-generering

`generate_presentation.py` skapar presentationsmaterial from bokinnehåll:

```python
def generate_presentation_outline():
 """Genererar presentationsoutline from all bokkapitel."""
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
- **Presentation outline**: Strukturerad markdown with nyckelbudskap
- **Python PowerPoint-script**: Automatisk slide-generering
- **Kvadrat-branding**: Konsistent visuell identitet
- **Innehållsoptimering**: Anpassat for muntlig presentation

### Distribution and användning

```bash
# Ladda ner artifacts from GitHub Actions
cd presentations
pip install -r requirebutts.txt
python generate_pptx.py
```

Resultatet is professionella PowerPoint-presentationer optimerade for:
- Konferenser and workshops
- Utbildningssyfte
- Marknadsföringsaktiviteter
- technical seminarier

## Omslag and whitepapers: Design and integration

### Omslag-designsystem

The book's omslag skapas through ett HTML/CSS-baserat designsystem:

```
exports/book-cover/
├── source/
│ ├── book-cover.html # Huvuddesign
│ ├── book-cover-light.html # Ljus variant
│ └── book-cover-minimal.html # Minimal design
├── pdf/ # Print-färdiga PDF-filer
├── png/ # Högupplösta PNG-exportar
└── scripts/
 └── generate_book_cover_exports.py
```

### Kvadrat-varumärkesintegrering

Designsystemet implebutterar Kvadrat-identiteten:

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

`generate_whitepapers.py` skapar standalone HTML-dokubutt:

- **26 individuella whitepapers**: Ett per chapter
- **Professionell HTML-design**: Responsiv and print-vänlig
- **Swedish anpassningar**: Optimerat for Swedish organizations
- **SEO-optimering**: Korrekt meta-data and struktur
- **Distribution-vänligt**: can delas via e-post, webb or print

## Teknisk arkitektur and systemintegration

### Helhetssyn on the architecture

the entire systemet exemplifierar Architecture as Code through:

1. **Kodifierad innehållshantering**: Markdown that källa for sanning
2. **Automatiserad pipeline**: Ingen manuell intervention krävs
3. **Versionskontroll**: complete historik over all ändringar
4. **Reproducerbarhet**: Identiska builds from samma källkod
5. **Skalbarhet**: Enkelt to lägga to nya chapter and format

### Kvalitetssäkring and testing

- **Automatiserad validering**: Kontinuerlig kontroll of innehåll and format
- **Build-verifiering**: ensures to all format genereras korrekt
- **Performance-monitoring**: Spårning of build-tider and resursanvändning
- **Error-hantering**: Robusta felmeddelanden and återställningsmekanismer

### Framtida utveckling

Systemet is designat for kontinuerlig förbättring:
- **Modulär arkitektur**: Enkelt to uppdatera enskilda komponenter
- **API-möjligheter**: Potential for integration with externa system
- **Skalning**: Stöd for fler format and distributionskanaler
- **Internationalisering**: Förberedelse for flerspråkig publicering

## Sammanfattning

Den moderna Architecture as Code-methodologyen representerar framtiden for infrastrukturhantering in Swedish organizations.
Den technical uppbyggnaden for "Architecture as Code" demonstrerar praktisk toämpning of The book's egna principles. Through to kodifiera the entire publikationsprocessen uppnås:

- **Architecture as Code-automation**: Komplett CI/CD for bokproduktion
- **Kvalitet**: Konsistent format and professionell presentation
- **Effektivitet**: Snabb iteration and feedback-loopar
- **Skalbarhet**: Enkelt to utöka with nytt innehåll and format
- **Transparens**: Öppen källkod and dokubutterad process

This technical system fungerar that en konkret illustration of how Architecture as Code-principlesna can toämpas also withoutför traditional IT-system, vilket skapar värde through automation, reproducerbarhet and kontinuerlig förbättring.

Sources:
- GitHub Actions Docubuttation. "Workflow syntax for GitHub Actions." GitHub, 2024.
- Pandoc User's Guide. "Creating docubutts with Pandoc." John MacFarlane, 2024.
- Mermaid Docubuttation. "Diagram syntax and examples." Mermaid Community, 2024.
- LaTeX Project. "The Eisvogel template docubuttation." LaTeX Community, 2024.