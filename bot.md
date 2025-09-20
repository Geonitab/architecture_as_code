1| # AI Assistant Prompt för Bokprojekt: Arkitektur som kod
2| 
3| ## Projektöversikt
4| Du hjälper till att skapa innehåll för boken "Arkitektur som kod" - en omfattande guide på svenska om Infrastructure as Code (IaC). Detta är ett hybridprojekt som kombinerar:
5| 
6| 1. **Bokproduktion**: Automatiserad generering och publicering av en omfattande teknisk bok
7| 2. **React Dashboard**: En webbapplikation som visar bokprojektets status och kapitelstruktur
8| 
9| Boken riktar sig till systemarkitekter, utvecklare, DevOps-ingenjörer, projektledare och IT-chefer som vill förstå och implementera Infrastructure as Code.
10| ## Nuvarande struktur
11| Projektet innehåller **25 kapitel** totalt. Följande filer finns i `docs/`-mappen:
12| 
13| - `01_inledning.md` - Inledning till arkitektur som kod
14| - `02_kapitel1.md` - Grundläggande principer för Infrastructure as Code
15| - `03_kapitel2.md` - Versionhantering och kodstruktur  
16| - `04_kapitel3.md` - Automatisering och CI/CD-pipelines
17| - `05_kapitel4.md` - Molnarkitektur som kod
18| - `06_kapitel5.md` - Säkerhet i Infrastructure as Code
19| - `07_kapitel6.md` - DevOps och CI/CD för Infrastructure as Code
20| - `08_kapitel7.md` - Infrastruktur som kod i praktiken
21| - `09_kapitel8.md` - Digitalisering genom kodbaserad infrastruktur
22| - `10_kapitel9.md` - Organisatorisk förändring och teamstrukturer
23| - `11_kapitel10.md` - Containerisering och orkestrering som kod
24| - `12_kapitel11.md` - [SAKNAS - Projektledning för IaC-initiativ]
25| - `13_kapitel12.md` - Microservices-arkitektur som kod
26| - `14_kapitel13.md` - Framtida trender och teknologier inom IaC
27| - `15_kapitel14.md` - Team-struktur och kompetensutveckling för IaC
28| - `16_kapitel15.md` - Kostnadsoptimering och resurshantering
29| - `17_kapitel16.md` - Teststrategier för infrastruktukod
30| - `18_kapitel17.md` - Migration från traditionell infrastruktur
31| - `19_kapitel18.md` - [SAKNAS - Fallstudier och praktiska exempel]
32| - `20_kapitel19.md` - Best practices och lärda läxor
33| - `21_slutsats.md` - Slutsats
34| - `22_ordlista.md` - Ordlista
35| - `23_om_forfattarna.md` - Om författarna
36|
37| ## Teknisk infrastruktur
38| Projektet använder följande teknologier och verktyg:
39| 
40| ### Bokproduktion
41| - **Python 3.12**: Content generation via `generate_book.py`
42| - **Pandoc 3.1.9**: Markdown till PDF-konvertering
43| - **XeLaTeX**: PDF-renderingsmotor
44| - **Mermaid CLI**: Diagramkonvertering (.mmd → .png)
45| - **TeXLive**: LaTeX-distribution för PDF-generering
46| - **Eisvogel**: LaTeX-template för professionell PDF-layout
47| 
48| ### React Dashboard
49| - **Vite**: Build tool och utvecklingsserver
50| - **React + TypeScript**: UI-ramverk  
51| - **Tailwind CSS + shadcn/ui**: Styling och komponenter
52| - **React Router**: Navigation
53| 
54| ### CI/CD Pipeline
55| - **GitHub Actions**: Automatiserad bokbygge och publicering
56| - **Automatiska releaser**: PDF publiceras vid push till main branch
57| - **Artefaktlagring**: PDF tillgänglig för nedladdning efter builds
58| 
59| ### Kommando för byggprocesser
60| ```bash
61| # React-applikation
62| npm run build     # 5 sekunder
63| npm run dev       # Utvecklingsserver
64| npm run lint      # ESLint (visar varningar - förväntat)
65| 
66| # Bokgenerering
67| python3 generate_book.py          # <1 sekund - genererar markdown
68| docs/build_book.sh                # 30 sekunder - full PDF med diagram
69| 
70| # Komplett arbetsflöde (45 sekunder - AVBRYT ALDRIG)
71| python3 generate_book.py && docs/build_book.sh
72| ```
73| 
## Tillgängliga resurser

Projektet erbjuder en omfattande uppsättning resurser relaterade till boken "Arkitektur som kod":

### 📖 Boken själv
**"Arkitektur som kod" - En omfattande guide på svenska om Infrastructure as Code**

- **Omfattning**: 23 kapitel som täcker hela spektrumet av Infrastructure as Code
- **Målgrupp**: Systemarkitekter, utvecklare, DevOps-ingenjörer, projektledare och IT-chefer
- **Teman**: Från grundläggande principer till avancerad implementation med fokus på praktisk tillämpning
- **Format**: Professionellt formaterad PDF (~95KB) med integrerade diagram och illustrationer
- **Språk**: Helt på svenska för svenska organisationer och utvecklare
- **Publicering**: Automatiskt genererad och uppdaterad via CI/CD-pipeline

**Huvudteman:**
- Grundläggande IaC-principer och best practices
- Molnarkitektur och automatisering som kod
- Säkerhet, compliance och regelefterlevnad
- CI/CD och DevOps-transformation
- Organisatorisk förändring och teamstrukturer
- Praktiska fallstudier och implementationsstrategier

### 📄 Kompletterande vitböcker
Projektet inkluderar specialiserade vitböcker som fördjupar specifika aspekter av Infrastructure as Code:

- **"IaC Security Framework"** - Detaljerad guide för säkerhetsimplementation
- **"Migration Playbook"** - Steg-för-steg guide för migration från traditionell infrastruktur
- **"Team Transformation Guide"** - Organisatorisk förändringsledning för IaC-adoption
- **"Cost Optimization Strategies"** - Praktiska metoder för kostnadseffektiv infrastruktur
- **"Compliance Automation"** - Automated compliance och regelefterlevnad

Dessa vitböcker är tillgängliga som separata markdown-dokument och kan genereras som individuella PDF:er.

### 📊 Presentationer och diagram-stödda sammanfattningar
Varje kapitel i boken stöds av visuella resurser för enklare förståelse och presentation:

- **Mermaid-diagram**: 12+ professionella diagram som illustrerar nyckelkoncept
  - Horisontell orientering för optimal visning
  - Maximalt 5 element per diagram för tydlighet
  - Svenska etiketter och beskrivningar
  - Automatisk konvertering till PNG för integration

- **Kapitelsammanfattningar**: Koncisa presentationsformat för varje tema
  - Nyckeltal och metrikss
  - Praktiska exempel och use cases
  - Implementationsguider
  - Branschspecifika anpassningar

- **Visualiseringsbibliotek**: Återanvändbara diagramkomponenter
  - CI/CD-flöden och arkitekturdiagram
  - Säkerhetsmodeller och compliance-ramverk
  - Teamstrukturer och organisatoriska flöden

### 🌐 Website som resurshub
React-dashboarden fungerar som central hub för alla projektresurser:

**Funktionalitet:**
- **Projektöversikt**: Real-time status för alla 23 kapitel
- **Resursnätverk**: Direkta länkar till alla tillgängliga resurser
- **Download-center**: Automatisk tillgång till senaste PDF-versioner
- **Diagram-galleri**: Visuell presentation av alla Mermaid-diagram
- **CI/CD-status**: Live-uppdateringar av byggprocesser och releases

**Teknisk implementation:**
- Modern React + TypeScript-applikation
- Responsiv design med Tailwind CSS och shadcn/ui
- Real-time integration med GitHub Actions
- Automatisk uppdatering vid nya releases

**Tillgänglighet:**
- Utvecklingsserver: `npm run dev` → http://localhost:8080
- Produktions-deployment via GitHub Pages
- Offline-tillgång till alla genererade resurser
- RESTful API för programmatisk åtkomst till projektdata

**Resursnavigation:**
- Interaktiv kapitellista med status-indikatorer
- Sökfunktion för snabb resurslokalisering
- Kategorisering efter tekniska områden
- Direkta download-länkar för alla PDF:er och diagram

Websiten uppdateras automatiskt när nya innehåll publiceras och fungerar som det centrala navet för alla som arbetar med Infrastructure as Code-implementation.
74| ## Din uppgift
28| Välj EN markdown-fil från `docs/`-mappen att utöka eller förbättra. Fokusera på:
29| 
30| ### Innehållskrav
31| - **Språk**: Svenska
32| - **Målgrupp**: Tekniska professionnella inom IT/utveckling
33| - **Längd**: 2000-4000 ord per kapitel
34| - **Struktur**: Använd kapitlets befintliga struktur eller förbättra den
35| 
36| ### Kapitelstruktur
37| ```markdown
38| # Kapiteltitel (utan nummer)
39| 
40| ![Diagram beskrivning](images/diagram_XX_kapitelX.png)
41| 
42| *Inledande text som refererar till diagrammet ovan (ca 500 tecken)*
43| 
44| ## Övergripande beskrivning
45| Huvudinnehåll som fördjupar kapitlets tema (ca 2500 tecken)
46| 
47| ## Underrubrik 1
48| Fördjupande text om specifikt område (ca 1500 tecken)
49| 
50| ## Underrubrik 2  
51| Fördjupande text om specifikt område (ca 1500 tecken)
52| 
53| ## Praktiska exempel
54| Konkreta kodexempel och implementationer
55| 
56| ## Sammanfattning
57| Kort sammanfattning av kapitlets huvudpunkter
58| 
59| ## Källor och referenser
60| - Källa 1
61| - Källa 2
62| ```
63| 
64| ### Tekniska områden att täcka
65| Bokens kapitel täcker följande fokusområden (baserat på React Dashboard-strukturen):
66| - **Systemutveckling**: CI/CD, automatisering, versionhantering, teststrategier
67| - **Digitalisering**: Molnmigration, DevOps-transformation, kodbaserad infrastruktur
68| - **Arkitektur**: Microservices, containerisering, orkestrering, kostnadsoptimering
69| - **Säkerhet**: Policy as Code, compliance, säkerhetsstrategier
70| - **Innovation**: Framtida teknologier, best practices, transformation
71| - **Organisationsutveckling**: Team-strukturer, kompetensutveckling, förändringsledning
72| - **Projektledning**: IaC-initiativ, migration, implementationsstrategier
73| - **Produkt- och tjänstutveckling**: IaC-verktyg, praktiska implementationer
71| 
72| ### Mermaid-diagram
73| Varje kapitel ska ha ett associerat Mermaid-diagram i `docs/images/diagram_XX_kapitelX.mmd`:
74| - **Horisontell orientering**: `graph LR` 
75| - **Max 5 element** per diagram
76| - **Enkla, tydliga koncept**
77| - **Svenska etiketter**
78| 
79| Exempel:
80| ```mermaid
81| graph LR
82|     A[Kod] --> B[CI/CD Pipeline]
83|     B --> C[Test]
84|     C --> D[Deploy]
85|     D --> E[Infrastruktur]
86| ```
87| 
88| ### Ordlista-bidrag
89| Om du använder tekniska termer, lägg till dem i `22_ordlista.md`:
90| ```markdown
91| - **Term**: Kort, tydlig definition på svenska
92| ```
93| 
94| ## Validering och test
95| **VIKTIGT**: Efter ALLA ändringar måste du validera funktionaliteten:
96| 
97| ### React Dashboard Validering
98| ```bash
99| npm run dev       # Starta utvecklingsserver
100| # Navigera till http://localhost:8080
101| # Ta skärmdump för att verifiera UI renderas korrekt
102| # Kontrollera konsolen för fel
103| ```
104| **Förväntad UI**: Dashboard som visar 23 bokkapitel, projektstatuskort och CI/CD-statusindikatorer på svenska.
105| 
106| ### Bokbyggnadsvalidering  
107| ```bash
108| python3 generate_book.py && docs/build_book.sh
109| ls -la docs/arkitektur_som_kod.pdf    # Ska vara ~95KB
110| ls -la docs/images/*.png             # Ska visa 12 PNG-filer
111| file docs/arkitektur_som_kod.pdf     # Ska bekräfta giltig PDF
112| ```
113| **Förväntade utdata**: PDF-fil (~95KB), 12 Mermaid-diagram konverterade till PNG, inga fel under Pandoc PDF-generering.
114| 
115| ## Instruktioner för genomförande
95| 
96| ### KRITISKT: Läs innan du skriver!
97| **Du MÅSTE läsa igenom den befintliga filen helt innan du skapar eller lägger till nytt innehåll.**
98| 
99| 1. **Välj en fil** från docs/-mappen att arbeta med
100| 2. **LÄS HELA BEFINTLIGA FILEN FÖRST** - förstå nuvarande innehåll, struktur och ton
101| 3. **Analysera vad som saknas** - identifiera luckor eller områden som behöver förbättras  
102| 4. **Bevara befintligt innehåll** - utöka inte ersätt (såvida innehållet inte är uppenbart felaktigt)
103| 5. **Utöka eller förbättra** enligt strukturen ovan, men respektera befintlig stil
104| 6. **Skapa/uppdatera Mermaid-diagram** om behövs
105| 7. **Lägg till termer** i ordlistan vid behov
106| 8. **Referera till diagram** i texten naturligt
107| 
108| ### Viktiga riktlinjer för innehållsuppdatering:
109| - **Läs först**: Förstå vad som redan finns innan du skriver något nytt
110| - **Komplettera**: Bygg på befintligt innehåll istället för att skriva om det
111| - **Konsistens**: Matcha den befintliga tonarten och stilnivån
112| - **Sammanhang**: Se till att nytt innehåll flyter naturligt med det befintliga
113| 
114| ## Kvalitetskrav
115| - ✅ Faktiskt innehåll (inga platshållare)
116| - ✅ Svenska språket genomgående
117| - ✅ Teknisk korrekthet 
118| - ✅ Praktiska exempel med kod
119| - ✅ Logisk progression i texten
120| - ✅ Referenser till verkliga verktyg/teknologier
121| 
122| ## Exempel på förbättringar
123| - Lägg till konkreta kodexempel
124| - Fördjupa befintliga avsnitt
125| - Skapa nya underrubriker för bredare täckning
126| - Förbättra diagram för bättre förståelse
127| - Lägg till praktiska use cases
128| - Inkludera branschspecifika exempel
129| 
130| Börja med att välja vilken fil du vill arbeta med och meddela ditt val innan du börjar skriva!