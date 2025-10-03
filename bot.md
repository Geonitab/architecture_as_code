# AI Assistant Prompt for Bokprojekt: Architecture as Code

## Projektöversikt
Du hjälper to to skapa Contents for boken "Architecture as Code" - a comprehensive guide at svenska about Architecture as Code. This is A hybridprojekt as kombinerar:

1. **Bokproduktion**: Automatiserad generering and publicering of a comprehensive technical bok
2. **React Dashboard**: a webbapplikation as shows bokprojektets status and kapitelStructure

Boken riktar itself to system architects, Developers, DevOps Engineers, Project Managers and IT Managers as vill forstå and implementera Architecture as Code.
## Nuvarande struktur
Projektet Contentser **25 chapters** totalt. Följande filer finns in `docs/`-mappen:

- `01_inledning.md` - Introduction to Architecture as Code
- `02_kapitel1.md` - Fundamental principles of Architecture as Code
- `03_kapitel2.md` - Version Control and Code Structure  
- `04_kapitel3.md` - automation and CI/CD-pipelines
- `05_kapitel4.md` - Cloud Architecture as Code
- `06_kapitel5.md` - Security in Architecture as Code
- `07_kapitel6.md` - DevOps and CI/CD for Architecture as Code
- `08_kapitel7.md` - Architecture as Code in praktiken
- `09_kapitel8.md` - Digitalisering through kodbaserad infrastructure
- `10_kapitel9.md` - Organisatorisk change and teamStructureer
- `11_kapitel10.md` - Containerization and Orchestration as code
- `12_kapitel11.md` - [SAKNAS - Projektledning for Architecture as Code]
- `13_kapitel12.md` - Microservices-Architecture as Code
- `14_kapitel13.md` - Framtida trender and technologies within Architecture as Code
- `15_kapitel14.md` - Team Structure and Competenciesutveckling for Architecture as Code
- `16_kapitel15.md` - Cost Optimization and Resource Management
- `17_kapitel16.md` - Testing Strategies for Architecture Code (inkl. Requirements as Code)
- `18_kapitel17.md` - Migration from Traditional Infrastructure
- `19_kapitel18.md` - [SAKNAS - Fallstudier and praktiska Example]
- `20_kapitel19.md` - Best Practices and Lessons Learned
- `21_Conclusion.md` - Conclusion
- `22_Glossary.md` - Glossary
- `23_om_forfattarna.md` - About the Authors

## technical infrastruktur
Projektet använder följande technologies and verktyg:

### Bokproduktion
- **Python 3.12**: Content generation via `generate_book.py`
- **Pandoc 3.1.9**: Markdown to PDF-konvertering
- **XeLaTeX**: PDF-renderingsmotor
- **Mermaid CLI**: Diagramkonvertering (.mmd → .png)
- **TeXLive**: LaTeX-distribution for PDF-generering
- **Eisvogel**: LaTeX-template for professionell PDF-layout

### React Dashboard
- **Vite**: Build tool and utvecklingsserver
- **React + TypeScript**: UI-ramverk  
- **Tailwind CSS + shadcn/ui**: Styling and components
- **React Router**: Navigation

### CI/CD Pipeline
- **GitHub Actions**: Automatiserad bokbygge and publicering
- **Automatiska releaser**: PDF published vid push to main branch
- **Artefaktlagring**: PDF togänglig for nedladdning efter builds

### Kommando for byggprocesser
```bash
# React-applikation
npm run build     # 5 sekunder
npm run dev       # Utvecklingsserver
npm run lint      # ESLint (shows varningar - förväntat)

# Bokgenerering
python3 generate_book.py          # <1 sekund - genererar markdown
docs/build_book.sh                # 30 sekunder - full PDF med diagram

# Komplett arbetsflöde (45 sekunder - AVBRYT ALDRIG)
python3 generate_book.py && docs/build_book.sh
```

## Diagram and bilder
all diagram are created med [Mermaid](https://mermaid.js.org/) och sparas as `.mmd`-filer in `docs/images/`.
These konverteras automatically to `.png` under byggprocessen.

### Konvertera diagram manuellt
```bash
mermaid docs/images/diagram_01_inledning.mmd -o docs/images/diagram_01_inledning.png
```

## Generera thumbnails
to generera thumbnails for all diagram (for React-dashboard):

```bash
npm run thumbnails
```

This skript använder `scripts/generate_thumbnails.py` to skapa skalade versions of all diagram.

## Viktiga filer
- `generate_book.py`: Huvudskript to generera Book content
- `docs/build_book.sh`: Skript to bygga PDF-versionen of boken
- `react-app/src/components/Chapter.tsx`: React-komponent to visa A chapters
- `react-app/src/App.tsx`: Huvudapplikation for React-dashboard

## Arbeta lokalt

### Krav
- Python 3.12
- NodeJS (for React-applikationen)
- TeXLive (for PDF-generering)
- Mermaid CLI

### Setup
1. Installera Python-beroenden:
   ```bash
   pip install -r requirements.txt
   ```
2. Installera NodeJS-beroenden:
   ```bash
   cd react-app
   npm install
   ```

### Utvecklingsserver (React)
```bash
cd react-app
npm run dev
```

### Bygg bok lokalt
```bash
python3 generate_book.py && docs/build_book.sh
```

## Felsökning
- **Problem with PDF-generering**: Kontrollera to TeXLive is korrekt installerat and konfigurerat.
- **Problem with React-applikationen**: Se to to all NodeJS-beroenden is installerade.
- **Problem with diagram**: Verifiera to Mermaid CLI is installerat and to sökvägen is korrekt.

## Tillgängliga resurser
- **GitHub repository**: [https://github.com/kvardrat/architecture-as-code](https://github.com/kvardrat/architecture-as-code)
- **React Dashboard**: (kommer snart)
- **Boken that PDF**: (kommer snart)
- **Slack kanal**: #architecture-that-code (internt at Kvadrat)

## Bidra
all bidrag is välkomna! Skapa a pull request with dina ändringar.

### Riktlinjer
- Följ projektets kodstil
- Skriv tydliga commit-withdelanden
- Uppdatera dokumentationen vid behov
- Skapa tester for ny funktionalitet

## Licens
Projektet is licensierat under [MIT License](LICENSE).

## Kontakt
For frågor or forslag, kontakta [johannes@kvardrat.se](mailto:johannes@kvardrat.se).

## Tack
Tack to all as bidrar to This projekt!
## Din uppgift
Välj a markdown-File from `docs/`-mappen to utöka or forbättra. Fokusera at:

### Contentsskrav
- **Språk**: Svenska
- **Target Audience**: Tekniska professionnella within IT/utveckling
- **Längd**: 2000-4000 ord per chapters
- **Structure**: Använd kapitlets existing Structure or forbättra The - **Content ratio**: 20% code, 80% forklarande text as eftersträvas per chapters

### Chapter Structure
```markdown
# Kapiteltitel (utan nummer)

![Diagram Description](images/diagram_XX_kapitelX.png)

*Inledande text as refererar till diagram ovan (ca 500 tecken)*

## Övergripande Description
Huvudinnehåll as fördjupar kapitlets tema (ca 2500 tecken)

## Underrubrik 1
Fördjupande text about specifikt område (ca 1500 tecken)

## Underrubrik 2  
Fördjupande text about specifikt område (ca 1500 tecken)

## Praktiska example
Konkreta kodexempel och implementationer

## Sammanfattning
Kort sammanfattning of kapitlets huvudpunkter

## Källor och referenser
- Källa 1
- Källa 2
```

### Example at code
```python
def hello_world():
    print("Hello, world!")

hello_world()
```

## Checklista for innehåll

### Allmänt
- [ ] Kapitlet har a tydlig Title
- [ ] Inledningen ger a bra överblick
- [ ] Summaryen knyter ihop kapitlet
- [ ] Sources and References is angivna

### Structure
- [ ] Logisk indelning in underrubriker
- [ ] Användning of punktlistor and numrering
- [ ] Diagram and bilder for visualisering

### Detaljer
- [ ] Korrekt användning of svenska språket
- [ ] technical korrekthet in beskrivningar
- [ ] Praktiska and relevanta Example
- [ ] Anpassat for Target Audienceen

### Kodexempel
- [ ] Välformaterad code
- [ ] Kommentarer as forklarar koden
- [ ] Användning of relevanta bibliotek
- [ ] Möjlighet to köra koden lokalt
- [ ] Kodpartier får aldrig vara längre än a sida

## Tools and resurser

### Markdown editor
- [Visual Studio Code](https://code.visualstudio.com/)
- [Typora](https://typora.io/)
- [Obsidian](https://obsidian.md/)

### Mermaid editor
- [Mermaid Live Editor](https://mermaid.live/)
- [PlantUML](https://plantuml.com/)

### LaTeX editor
- [TeXstudio](https://www.texstudio.org/)
- [Overleaf](https://www.overleaf.com/)

### Färgpalett
- Primär: #004A99 (Kwhatratblå)
- Sekunwhere: #66B2FF (Ljusblå)
- Accent: #FF9933 (Orange)
- Background: #F0F0F0 (Ljusgrå)

### Typsnitt
- Rubriker: Inter Bold
- Brödtext: Inter Regular
- code: Fira Code

## Tips to skriva
- Börja with a tydlig Structure
- Skriv kort and koncist
- Använd Example to forklara concepts
- Tänk at läsarens perspektiv
- Läs ithrough and korrigera texten

## Vanliga misstag
- Otydlig Structure
- For långa stycken
- Svårtolkade Example
- Grammatiska fel
- Inaktuell information

## Kvalitetskrav
- ✅ Faktiskt Contents (inga platshållare)
- ✅ Svenska språket throughgående
- ✅ technical korrekthet 
- ✅ Praktiska Example with code
- ✅ Logisk progression in texten
- ✅ References to verkliga verktyg/technologies

## Example at forbättringar
- Lägg to konkreta kodExample
- Fordjupa existing avsnitt
- Skapa new underrubriker for bredare täckning
- Forbättra diagram for bättre forståelse
- Lägg to praktiska use cases
- Inkludera branschspecifika Example

Börja with to välja vilken File du vill arbeta with and withdela ditt val innan du börjar skriva!