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
74| ## Diagram och bilder
75| Alla diagram skapas med [Mermaid](https://mermaid.js.org/) och sparas som `.mmd`-filer i `docs/images/`.
76| Dessa konverteras automatiskt till `.png` under byggprocessen.
77| 
78| ### Konvertera diagram manuellt
79| ```bash
80| mermaid docs/images/diagram_01_inledning.mmd -o docs/images/diagram_01_inledning.png
81| ```
82| 
83| ## Generera thumbnails
84| För att generera thumbnails för alla diagram (för React-dashboard):
85| 
86| ```bash
87| npm run thumbnails
88| ```
89| 
90| Detta skript använder `scripts/generate_thumbnails.py` för att skapa skalade versioner av alla diagram.
91| 
92| ## Viktiga filer
93| - `generate_book.py`: Huvudskript för att generera bokens innehåll
94| - `docs/build_book.sh`: Skript för att bygga PDF-versionen av boken
95| - `react-app/src/components/Chapter.tsx`: React-komponent för att visa ett kapitel
96| - `react-app/src/App.tsx`: Huvudapplikation för React-dashboard
97| 
98| ## Arbeta lokalt
99| 
100| ### Krav
101| - Python 3.12
102| - NodeJS (för React-applikationen)
103| - TeXLive (för PDF-generering)
104| - Mermaid CLI
105| 
106| ### Setup
107| 1. Installera Python-beroenden:
108|    ```bash
109|    pip install -r requirements.txt
110|    ```
111| 2. Installera NodeJS-beroenden:
112|    ```bash
113|    cd react-app
114|    npm install
115|    ```
116| 
117| ### Utvecklingsserver (React)
118| ```bash
119| cd react-app
120| npm run dev
121| ```
122| 
123| ### Bygg bok lokalt
124| ```bash
125| python3 generate_book.py && docs/build_book.sh
126| ```
127| 
128| ## Felsökning
129| - **Problem med PDF-generering**: Kontrollera att TeXLive är korrekt installerat och konfigurerat.
130| - **Problem med React-applikationen**: Se till att alla NodeJS-beroenden är installerade.
131| - **Problem med diagram**: Verifiera att Mermaid CLI är installerat och att sökvägen är korrekt.
132| 
133| ## Tillgängliga resurser
134| - **GitHub repository**: [https://github.com/kvardrat/arkitektur-som-kod](https://github.com/kvardrat/arkitektur-som-kod)
135| - **React Dashboard**: (kommer snart)
136| - **Boken som PDF**: (kommer snart)
137| - **Slack kanal**: #arkitektur-som-kod (internt på Kvadrat)
138| 
139| ## Bidra
140| Alla bidrag är välkomna! Skapa en pull request med dina ändringar.
141| 
142| ### Riktlinjer
143| - Följ projektets kodstil
144| - Skriv tydliga commit-meddelanden
145| - Uppdatera dokumentationen vid behov
146| - Skapa tester för ny funktionalitet
147| 
148| ## Licens
149| Projektet är licensierat under [MIT License](LICENSE).
150| 
151| ## Kontakt
152| För frågor eller förslag, kontakta [johannes@kvardrat.se](mailto:johannes@kvardrat.se).
153| 
154| ## Tack
155| Tack till alla som bidrar till detta projekt!
156| ## Din uppgift
157| Välj EN markdown-fil från `docs/`-mappen att utöka eller förbättra. Fokusera på:
158| 
159| ### Innehållskrav
160| - **Språk**: Svenska
161| - **Målgrupp**: Tekniska professionnella inom IT/utveckling
162| - **Längd**: 2000-4000 ord per kapitel
163| - **Struktur**: Använd kapitlets befintliga struktur eller förbättra den
164| - **Content ratio**: 20% kod, 80% förklarande text som eftersträvas per kapitel
165| 
166| ### Kapitelstruktur
167| ```markdown
168| # Kapiteltitel (utan nummer)
169| 
170| ![Diagram beskrivning](images/diagram_XX_kapitelX.png)
171| 
172| *Inledande text som refererar till diagrammet ovan (ca 500 tecken)*
173| 
174| ## Övergripande beskrivning
175| Huvudinnehåll som fördjupar kapitlets tema (ca 2500 tecken)
176| 
177| ## Underrubrik 1
178| Fördjupande text om specifikt område (ca 1500 tecken)
179| 
180| ## Underrubrik 2  
181| Fördjupande text om specifikt område (ca 1500 tecken)
182| 
183| ## Praktiska exempel
184| Konkreta kodexempel och implementationer
185| 
186| ## Sammanfattning
187| Kort sammanfattning av kapitlets huvudpunkter
188| 
189| ## Källor och referenser
190| - Källa 1
191| - Källa 2
192| ```
193| 
194| ### Exempel på kod
195| ```python
196| def hello_world():
197|     print("Hello, world!")
198| 
199| hello_world()
200| ```
201| 
202| ## Checklista för innehåll
203| 
204| ### Allmänt
205| - [ ] Kapitlet har en tydlig titel
206| - [ ] Inledningen ger en bra överblick
207| - [ ] Sammanfattningen knyter ihop kapitlet
208| - [ ] Källor och referenser är angivna
209| 
210| ### Struktur
211| - [ ] Logisk indelning i underrubriker
212| - [ ] Användning av punktlistor och numrering
213| - [ ] Diagram och bilder för visualisering
214| 
215| ### Detaljer
216| - [ ] Korrekt användning av svenska språket
217| - [ ] Teknisk korrekthet i beskrivningar
218| - [ ] Praktiska och relevanta exempel
219| - [ ] Anpassat för målgruppen
220| 
221| ### Kodexempel
222| - [ ] Välformaterad kod
223| - [ ] Kommentarer som förklarar koden
224| - [ ] Användning av relevanta bibliotek
225| - [ ] Möjlighet att köra koden lokalt
226| 
227| ## Verktyg och resurser
228| 
229| ### Markdown editor
230| - [Visual Studio Code](https://code.visualstudio.com/)
231| - [Typora](https://typora.io/)
232| - [Obsidian](https://obsidian.md/)
233| 
234| ### Mermaid editor
235| - [Mermaid Live Editor](https://mermaid.live/)
236| - [PlantUML](https://plantuml.com/)
237| 
238| ### LaTeX editor
239| - [TeXstudio](https://www.texstudio.org/)
240| - [Overleaf](https://www.overleaf.com/)
241| 
242| ### Färgpalett
243| - Primär: #004A99 (Kvadratblå)
244| - Sekundär: #66B2FF (Ljusblå)
245| - Accent: #FF9933 (Orange)
246| - Bakgrund: #F0F0F0 (Ljusgrå)
247| 
248| ### Typsnitt
249| - Rubriker: Inter Bold
250| - Brödtext: Inter Regular
251| - Kod: Fira Code
252| 
253| ## Tips för att skriva
254| - Börja med en tydlig struktur
255| - Skriv kort och koncist
256| - Använd exempel för att förklara koncept
257| - Tänk på läsarens perspektiv
258| - Läs igenom och korrigera texten
259| 
260| ## Vanliga misstag
261| - Otydlig struktur
262| - För långa stycken
263| - Svårtolkade exempel
264| - Grammatiska fel
265| - Inaktuell information
266| 
267| ## Kvalitetskrav
268| - ✅ Faktiskt innehåll (inga platshållare)
269| - ✅ Svenska språket genomgående
270| - ✅ Teknisk korrekthet 
271| - ✅ Praktiska exempel med kod
272| - ✅ Logisk progression i texten
273| - ✅ Referenser till verkliga verktyg/teknologier
274| 
275| ## Exempel på förbättringar
276| - Lägg till konkreta kodexempel
277| - Fördjupa befintliga avsnitt
278| - Skapa nya underrubriker för bredare täckning
279| - Förbättra diagram för bättre förståelse
280| - Lägg till praktiska use cases
281| - Inkludera branschspecifika exempel
282| 
283| Börja med att välja vilken fil du vill arbeta med och meddela ditt val innan du börjar skriva!
