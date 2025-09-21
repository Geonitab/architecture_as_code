# AI Assistant Prompt för Bokprojekt: Arkitektur som kod

## Projektöversikt
Du hjälper till att skapa innehåll för boken "Arkitektur som kod" - en omfattande guide på svenska om Infrastructure as Code (IaC). Detta är ett hybridprojekt som kombinerar:

1. **Bokproduktion**: Automatiserad generering och publicering av en omfattande teknisk bok
2. **React Dashboard**: En webbapplikation som visar bokprojektets status och kapitelstruktur

Boken riktar sig till systemarkitekter, utvecklare, DevOps-ingenjörer, projektledare och IT-chefer som vill förstå och implementera Infrastructure as Code.
## Nuvarande struktur
Projektet innehåller **25 kapitel** totalt. Följande filer finns i `docs/`-mappen:

- `01_inledning.md` - Inledning till arkitektur som kod
- `02_kapitel1.md` - Grundläggande principer för Infrastructure as Code
- `03_kapitel2.md` - Versionhantering och kodstruktur  
- `04_kapitel3.md` - Automatisering och CI/CD-pipelines
- `05_kapitel4.md` - Molnarkitektur som kod
- `06_kapitel5.md` - Säkerhet i Infrastructure as Code
- `07_kapitel6.md` - DevOps och CI/CD för Infrastructure as Code
- `08_kapitel7.md` - Infrastruktur som kod i praktiken
- `09_kapitel8.md` - Digitalisering genom kodbaserad infrastruktur
- `10_kapitel9.md` - Organisatorisk förändring och teamstrukturer
- `11_kapitel10.md` - Containerisering och orkestrering som kod
- `12_kapitel11.md` - [SAKNAS - Projektledning för IaC-initiativ]
- `13_kapitel12.md` - Microservices-arkitektur som kod
- `14_kapitel13.md` - Framtida trender och teknologier inom IaC
- `15_kapitel14.md` - Team-struktur och kompetensutveckling för IaC
- `16_kapitel15.md` - Kostnadsoptimering och resurshantering
- `17_kapitel16.md` - Teststrategier för infrastruktukod
- `18_kapitel17.md` - Migration från traditionell infrastruktur
- `19_kapitel18.md` - [SAKNAS - Fallstudier och praktiska exempel]
- `20_kapitel19.md` - Best practices och lärda läxor
- `21_slutsats.md` - Slutsats
- `22_ordlista.md` - Ordlista
- `23_om_forfattarna.md` - Om författarna

## Teknisk infrastruktur
Projektet använder följande teknologier och verktyg:

### Bokproduktion
- **Python 3.12**: Content generation via `generate_book.py`
- **Pandoc 3.1.9**: Markdown till PDF-konvertering
- **XeLaTeX**: PDF-renderingsmotor
- **Mermaid CLI**: Diagramkonvertering (.mmd → .png)
- **TeXLive**: LaTeX-distribution för PDF-generering
- **Eisvogel**: LaTeX-template för professionell PDF-layout

### React Dashboard
- **Vite**: Build tool och utvecklingsserver
- **React + TypeScript**: UI-ramverk  
- **Tailwind CSS + shadcn/ui**: Styling och komponenter
- **React Router**: Navigation

### CI/CD Pipeline
- **GitHub Actions**: Automatiserad bokbygge och publicering
- **Automatiska releaser**: PDF publiceras vid push till main branch
- **Artefaktlagring**: PDF tillgänglig för nedladdning efter builds

### Kommando för byggprocesser
```bash
# React-applikation
npm run build     # 5 sekunder
npm run dev       # Utvecklingsserver
npm run lint      # ESLint (visar varningar - förväntat)

# Bokgenerering
python3 generate_book.py          # <1 sekund - genererar markdown
docs/build_book.sh                # 30 sekunder - full PDF med diagram

# Komplett arbetsflöde (45 sekunder - AVBRYT ALDRIG)
python3 generate_book.py && docs/build_book.sh
```

## Diagram och bilder
Alla diagram skapas med [Mermaid](https://mermaid.js.org/) och sparas som `.mmd`-filer i `docs/images/`.
Dessa konverteras automatiskt till `.png` under byggprocessen.

### Konvertera diagram manuellt
```bash
mermaid docs/images/diagram_01_inledning.mmd -o docs/images/diagram_01_inledning.png
```

## Generera thumbnails
För att generera thumbnails för alla diagram (för React-dashboard):

```bash
npm run thumbnails
```

Detta skript använder `scripts/generate_thumbnails.py` för att skapa skalade versioner av alla diagram.

## Viktiga filer
- `generate_book.py`: Huvudskript för att generera bokens innehåll
- `docs/build_book.sh`: Skript för att bygga PDF-versionen av boken
- `react-app/src/components/Chapter.tsx`: React-komponent för att visa ett kapitel
- `react-app/src/App.tsx`: Huvudapplikation för React-dashboard

## Arbeta lokalt

### Krav
- Python 3.12
- NodeJS (för React-applikationen)
- TeXLive (för PDF-generering)
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
- **Problem med PDF-generering**: Kontrollera att TeXLive är korrekt installerat och konfigurerat.
- **Problem med React-applikationen**: Se till att alla NodeJS-beroenden är installerade.
- **Problem med diagram**: Verifiera att Mermaid CLI är installerat och att sökvägen är korrekt.

## Tillgängliga resurser
- **GitHub repository**: [https://github.com/kvardrat/arkitektur-som-kod](https://github.com/kvardrat/arkitektur-som-kod)
- **React Dashboard**: (kommer snart)
- **Boken som PDF**: (kommer snart)
- **Slack kanal**: #arkitektur-som-kod (internt på Kvadrat)

## Bidra
Alla bidrag är välkomna! Skapa en pull request med dina ändringar.

### Riktlinjer
- Följ projektets kodstil
- Skriv tydliga commit-meddelanden
- Uppdatera dokumentationen vid behov
- Skapa tester för ny funktionalitet

## Licens
Projektet är licensierat under [MIT License](LICENSE).

## Kontakt
För frågor eller förslag, kontakta [johannes@kvardrat.se](mailto:johannes@kvardrat.se).

## Tack
Tack till alla som bidrar till detta projekt!
## Din uppgift
Välj EN markdown-fil från `docs/`-mappen att utöka eller förbättra. Fokusera på:

### Innehållskrav
- **Språk**: Svenska
- **Målgrupp**: Tekniska professionnella inom IT/utveckling
- **Längd**: 2000-4000 ord per kapitel
- **Struktur**: Använd kapitlets befintliga struktur eller förbättra den
- **Content ratio**: 20% kod, 80% förklarande text som eftersträvas per kapitel

### Kapitelstruktur
```markdown
# Kapiteltitel (utan nummer)

![Diagram beskrivning](images/diagram_XX_kapitelX.png)

*Inledande text som refererar till diagrammet ovan (ca 500 tecken)*

## Övergripande beskrivning
Huvudinnehåll som fördjupar kapitlets tema (ca 2500 tecken)

## Underrubrik 1
Fördjupande text om specifikt område (ca 1500 tecken)

## Underrubrik 2  
Fördjupande text om specifikt område (ca 1500 tecken)

## Praktiska exempel
Konkreta kodexempel och implementationer

## Sammanfattning
Kort sammanfattning av kapitlets huvudpunkter

## Källor och referenser
- Källa 1
- Källa 2
```

### Exempel på kod
```python
def hello_world():
    print("Hello, world!")

hello_world()
```

## Checklista för innehåll

### Allmänt
- [ ] Kapitlet har en tydlig titel
- [ ] Inledningen ger en bra överblick
- [ ] Sammanfattningen knyter ihop kapitlet
- [ ] Källor och referenser är angivna

### Struktur
- [ ] Logisk indelning i underrubriker
- [ ] Användning av punktlistor och numrering
- [ ] Diagram och bilder för visualisering

### Detaljer
- [ ] Korrekt användning av svenska språket
- [ ] Teknisk korrekthet i beskrivningar
- [ ] Praktiska och relevanta exempel
- [ ] Anpassat för målgruppen

### Kodexempel
- [ ] Välformaterad kod
- [ ] Kommentarer som förklarar koden
- [ ] Användning av relevanta bibliotek
- [ ] Möjlighet att köra koden lokalt
- [ ] Kodpartier får aldrig vara längre än en sida

## Verktyg och resurser

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
- Primär: #004A99 (Kvadratblå)
- Sekundär: #66B2FF (Ljusblå)
- Accent: #FF9933 (Orange)
- Bakgrund: #F0F0F0 (Ljusgrå)

### Typsnitt
- Rubriker: Inter Bold
- Brödtext: Inter Regular
- Kod: Fira Code

## Tips för att skriva
- Börja med en tydlig struktur
- Skriv kort och koncist
- Använd exempel för att förklara koncept
- Tänk på läsarens perspektiv
- Läs igenom och korrigera texten

## Vanliga misstag
- Otydlig struktur
- För långa stycken
- Svårtolkade exempel
- Grammatiska fel
- Inaktuell information

## Kvalitetskrav
- ✅ Faktiskt innehåll (inga platshållare)
- ✅ Svenska språket genomgående
- ✅ Teknisk korrekthet 
- ✅ Praktiska exempel med kod
- ✅ Logisk progression i texten
- ✅ Referenser till verkliga verktyg/teknologier

## Exempel på förbättringar
- Lägg till konkreta kodexempel
- Fördjupa befintliga avsnitt
- Skapa nya underrubriker för bredare täckning
- Förbättra diagram för bättre förståelse
- Lägg till praktiska use cases
- Inkludera branschspecifika exempel

Börja med att välja vilken fil du vill arbeta med och meddela ditt val innan du börjar skriva!