1| # AI Assistant Prompt för Bokprojekt: Arkitektur som kod
2| 
3| ## Projektöversikt
4| Du hjälper till att skapa innehåll för boken "Arkitektur som kod" - en omfattande guide på svenska om Infrastructure as Code (IaC). Boken riktar sig till systemarkitekter, utvecklare, DevOps-in[...]
5| 
6| ## Nuvarande struktur
7| Följande filer finns i `docs/`-mappen:
8| - `01_inledning.md` - Introduktion till IaC
9| - `02_kapitel1.md` - Grundläggande principer  
10| - `03_kapitel2.md` - Verktyg och teknologier
11| - `04_kapitel3.md` - Molnarkitektur som kod
12| - `05_kapitel4.md` - Säkerhet och policy som kod
13| - `06_kapitel5.md` - [Behöver innehåll]
14| - `07_kapitel6.md` - DevOps och CI/CD
15| - `08_kapitel7.md` - Infrastruktur som kod i praktiken
16| - `09_kapitel8.md` - Versionshantering och kodstandarder
17| - `10_kapitel9.md` - Automatisering av molntjänster
18| - `11_kapitel10.md` - Containerisering och orkestrering
19| - `12_kapitel11.md` - Policy och säkerhet som kod i detalj
20| - `13_kapitel12.md` - Microservices-arkitektur
21| - `14_kapitel13.md` - Framtida trender inom IaC
22| - `15_kapitel14.md` - Team-struktur och kompetensutveckling
23| - `21_slutsats.md` - Sammanfattning
24| - `22_ordlista.md` - Teknisk ordlista
25| - `23_om_forfattarna.md` - Författarpresentationer
26| 
27| ## Din uppgift
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
65| - **Systemutveckling**: CI/CD, automatisering, versionhantering
66| - **Digitalisering**: Molnmigration, DevOps-transformation
67| - **Arkitektur**: Microservices, containerisering, orkestrering
68| - **Säkerhet**: Policy as Code, secrets management, compliance
69| - **Innovation**: Emerging technologies, best practices
70| - **Organisationsutveckling**: Team-strukturer, kompetensutveckling
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
94| ## Instruktioner för genomförande
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