# Arkitektur som kod - Bokprojekt

En omfattande bok om Architecture as Code på svenska, med Infrastructure as Code som praktiskt exempel.

## 📚 Om boken

Denna bok täcker Architecture as Code från grundläggande principer till avancerad implementation, med fokus på praktisk tillämpning inom svenska organisationer. Infrastructure as Code behandlas som ett viktigt praktiskt exempel inom den bredare Architecture as Code-ramen.

### Målgrupp
- Systemarkitekter
- DevOps-ingenjörer  
- Utvecklare
- Projektledare
- IT-chefer

### Innehåll
25 kapitel som täcker:
- Grundläggande Architecture as Code-principer
- Infrastructure as Code som praktiskt exempel
- Molnarkitektur som kod
- Säkerhet och compliance
- CI/CD och automatisering
- Organisatorisk transformation
- Praktiska fallstudier

## 🛠️ Teknisk implementation

### Struktur
```
docs/                    # Bokens innehåll
├── *.md                # Markdown-kapitel (01_inledning.md, 02_grundlaggande_principer.md, osv)
├── images/             # Mermaid-diagram
│   └── *.mmd          # Mermaid källfiler
├── build_book.sh      # Lokal byggscript
└── arkitektur_som_kod.pdf  # Genererad bok

releases/                 # Alla deliverables organiserade för distribution
├── book/               # Bokformat (PDF, EPUB, DOCX)
├── presentation/       # Presentationsmaterial (PPTX, PDF)
├── whitepapers/        # HTML whitepapers per kapitel
└── website/           # Komplett statisk webbsida

.github/workflows/      # CI/CD automation
├── unified-build-release.yml    # Unified comprehensive workflow (ALL formats)
├── generate-whitepapers.yml    # Standalone whitepaper generation
├── generate-presentations.yml  # Standalone presentation generation  
└── content-validation.yml      # Repository content validation
```

### Release-leveranser

Alla deliverables samlas automatiskt i `releases/`-mappen för enkel distribution:

#### 📚 Bokformat (`releases/book/`)
- **PDF**: `arkitektur_som_kod.pdf` - Fullständig bok
- **EPUB**: `arkitektur_som_kod.epub` - E-läsarformat  
- **DOCX**: `arkitektur_som_kod.docx` - Microsoft Word-format

#### 🎤 Presentationer (`releases/presentation/`)
- **PPTX**: `arkitektur_som_kod_presentation.pptx` - PowerPoint-presentation
- **PDF**: Presentation i PDF-format (manuell konvertering krävs)

#### 📄 Whitepapers (`releases/whitepapers/`)
- **HTML**: Individuella whitepapers per kapitel
- **PDF**: `whitepapers_combined.pdf` - Kombinerad whitepaper-samling

#### 🌐 Webbsida (`releases/website/`)
- Komplett kopia av den statiska webbsidan
- Redo för deployment till webbserver

### Komplett release-byggprocess

#### Automatiska GitHub Actions workflows

**Rekommenderat: Använd Unified Workflow för automatisk byggning**

1. **Unified Build & Release Workflow** (`unified-build-release.yml`):
   ```
   Trigger: Push/PR till main branch med ändringar i relevanta filer
   Output: Komplett GitHub Release med alla format
   Strategier: Traditional (~90 min) och Docker (~60 min)
   Inkluderar: PDF + EPUB + DOCX + PPTX + HTML + Website
   Flexibilitet: Välj leveranser och byggstrategi via manual trigger
   ```

#### Manuell lokal byggning

För att generera alla leveranser lokalt:

```bash
# Automatisk release-byggprocess (kräver alla dependencies)
./build_release.sh

# Eller steg för steg:
python3 generate_book.py                    # Generera bokinnehåll
docs/build_book.sh --release               # Bygg alla bokformat
python3 generate_whitepapers.py --release  # Generera whitepapers
python3 generate_presentation.py --release # Generera presentation
npm run build                              # Bygg webbsida
cp -r dist/* releases/website/              # Kopiera till release
```

### Automatisk byggprocess

Boken byggs automatiskt via GitHub Actions när:
- Markdown-filer ändras i `docs/` mappen
- Mermaid-diagram uppdateras i `docs/images/`
- CI/CD konfiguration modifieras

#### Byggprocessen:
1. **Mermaid → PNG**: Konverterar diagram till bilder
2. **Pandoc**: Genererar PDF/EPUB/DOCX med konfigurerad Pandoc-yaml
3. **Artifact**: Sparar PDF för nedladdning
4. **Release**: Skapar automatisk release på main branch

### Lokalt byggande

För att bygga boken lokalt:

```bash
# Krav: pandoc, texlive-xetex, mermaid-cli
cd docs
chmod +x build_book.sh
./build_book.sh

# För att generera alla format (PDF, EPUB, DOCX):
./build_book.sh --all-formats

# För release-byggning med utdata till releases/book/:
./build_book.sh --release
```

#### Komplett release-byggning

```bash
# Bygg alla deliverables och organisera i releases/
chmod +x build_release.sh
./build_release.sh
```

Detta skapar:
- Alla bokformat i `releases/book/`
- Presentationsmaterial i `releases/presentation/`
- HTML whitepapers i `releases/whitepapers/`
- Statisk webbsida i `releases/website/`

#### Pandoc-konfiguration

Projektet använder en dedikerad Pandoc-konfigurationsfil (`docs/pandoc.yaml`) som säkerställer:

- **Kapitel på nya sidor**: `top-level-division: chapter` gör att varje H1-rubrik (kapitel) börjar på en ny sida
- **Enhetlig formatering**: Samma inställningar för alla utdataformat (PDF, EPUB, DOCX)
- **Svensk språkstöd**: Rätt språkinställningar för svenska texten
- **Automatisk innehållsförteckning**: Med 3 nivåers djup
- **Kapitelinumrering**: Automatisk numrering av alla kapitel

Konfigurationen stöder:
- **PDF**: Via XeLaTeX med Eisvogel-template för professionell layout
- **EPUB**: Med kapitelindelning på H1-nivå för e-läsare
- **DOCX**: För redigering i Microsoft Word eller kompatibla program

## 📊 Diagram och illustrationer

Alla diagram skapas med Mermaid och följer dessa riktlinjer:
- Maximalt 5 element per diagram
- Horisontell orientering (LR)
- Konverteras automatiskt till PNG i CI/CD

Exempel:
```mermaid
graph LR
    A[Infrastructure] --> B[as Code]
    B --> C[Automation]
    C --> D[Scalability]
    D --> E[Reliability]
```

## 🔄 Bidrag och uppdateringar

### Workflow för ändringar:
1. Skapa branch för ändringar
2. Modifiera markdown-filer i `docs/`
3. Commit och push
4. GitHub Actions bygger automatiskt PDF
5. Merge till main → automatisk release

### Kapitelstruktur:
Varje kapitel följer samma struktur:
- H1 huvudrubrik
- Diagram med beskrivning
- Inledande text (500 tecken)
- Fördjupande sektioner
- Källor

## 🏗️ CI/CD Pipeline

### Unified Workflow Architecture

Projektet använder en unified GitHub Actions workflow för effektiv byggprocess:

#### 🎯 Unified Build & Release (`unified-build-release.yml`) - **REKOMMENDERAD**
Konsoliderad workflow som ersätter tidigare separata workflows:
- **Triggers**: Push/PR på alla relevanta filer, manual dispatch med parametrar
- **Strategier**: Traditional build (~90 min) och Docker-optimized (~60 min)
- **Leveranser**: PDF + EPUB + DOCX + Presentations + Whitepapers + Website
- **Flexibilitet**: Välj byggstrategi och leveranser via manual trigger
- **Output**: Komplett release med alla format organiserade i `releases/` struktur
- **GitHub Release**: Unified comprehensive release (`v{number}-unified`)
- **Fallback**: Om en byggstrategi misslyckas kan den andra fortfarande slutföras

#### Workflow-funktioner
- **Selective Building**: Bygg endast specifika leveranser (book-only, presentations-only, etc.)
- **Multi-strategy**: Kör traditional och Docker builds parallellt eller individuellt
- **Advanced Caching**: GitHub Actions cache för dependencies och Docker layers
- **Error Resilience**: Graceful fallback mellan byggstrategier

### Tidigare workflows (nu ersatta)
- ~~`complete-release.yml`~~ → Integrerad i unified workflow
- ~~`build-book-fast.yml`~~ → Docker-strategi i unified workflow
- ~~`build-book.yml`~~ → Book-only option i unified workflow

### Workflow-jämförelse

| Workflow | Tid | PDF | EPUB | DOCX | Presentations | Whitepapers | Website | Docker | Strategies |
|----------|-----|-----|------|------|---------------|-------------|---------|--------|------------|
| unified-build-release.yml | 60-90min | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Multiple |
| ~~complete-release.yml~~ | ~~90min~~ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ~~Replaced~~ |
| ~~build-book-fast.yml~~ | ~~60min~~ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ~~Replaced~~ |

### Status badges:
![Unified Build & Release](https://github.com/Geonitab/kodarkitektur-bokverkstad/workflows/Unified%20Build%20&%20Release/badge.svg)

## 📖 Kapitellista

1. Inledning till arkitektur som kod
2. Grundläggande principer för Architecture as Code
3. Versionhantering och kodstruktur
4. Automatisering och CI/CD-pipelines
5. Molnarkitektur som kod
6. Säkerhet i Infrastructure as Code
7. Monitering och observabilitet
8. Skalbarhet och prestanda
9. Digitalisering genom kodbaserad infrastruktur
10. Organisatorisk förändring och teamstrukturer
11. Projektledning för IaC-initiativ
12. Innovation genom infrastrukturtransformation
13. Produktutveckling med IaC-verktyg
14. Compliance och regelefterlevnad
15. Kostnadsoptimering och resurshantering
16. Teststrategier för infrastrukturkod
17. Migration från traditionell infrastruktur
18. Framtida trender och teknologier
19. Best practices och lärda läxor
20. Fallstudier och praktiska exempel
21. Slutsats
22. Ordlista
23. Om författarna

## 👥 Författare

**Dr. Anna Bergström** - Senior Cloud Architect  
**Marcus Andersson** - DevOps Engineer och Automation Specialist

## 📄 Licens

Detta verk är licensierat under Creative Commons Attribution-ShareAlike 4.0 International License.

## 🚀 Kom igång

1. Klona repository
2. Gör ändringar i markdown-filer
3. Push till GitHub
4. Ladda ner genererad PDF från Actions artifacts eller Releases

---

*Automatiskt byggt med GitHub Actions och Pandoc*