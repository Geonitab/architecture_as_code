# Faktagranskning av *Architecture as Code* – samlad rapport

**Datum:** 2026-10-30
**Underlag:** manuskriptet i `docs/` vid commit `df6bd77` (alla 41 filer som `docs/book_index.json` pekar ut: 31 kapitel, 7 bilagor, 3 supplement och 7 delintroduktioner, cirka 107 000 ord).
**Delrapporter:** elva filer i denna katalog (se avsnitt 10). Varje fynd har ett ID (t.ex. `B2-04`) som leder till fullständig beskrivning, evidens med URL och ett konkret ändringsförslag i respektive delrapport. `fynd_tabell.md` listar samtliga fynd sorterade efter allvarlighet.

---

## 1. Sammanfattning

Bokens tekniska resonemang håller i stort: de övergripande beskrivningarna av C4-modellen, Infrastructure as Code, GitOps, DORA-forskningen, Team Topologies, NIST SP 800-53, FINOS CALM och de flesta verktygskoncepten är korrekta. Problemen ligger i tre lager som en läsare eller recensent kommer att slå ner på:

1. **Källapparaten är inte tillförlitlig.** Bokens två mest använda källor finns inte: Thoughtworks "Architecture as Code: The Next Evolution" (Source [1], citerad i sju kapitel) och Radar-blippen "Governance as Code" (Source [2], citerad i sex kapitel) går inte att återfinna hos Thoughtworks. Utöver dessa har omkring 60 enskilda källposter i kapitlens källistor titlar som inte motsvarar någon känd publikation (Red Hat, GitLab, McKinsey, Gartner, FinOps Foundation, OWASP, ENISA, IEEE, CNCF, Microsoft, AXELOS, SANS m.fl.). Sju av bokens åtta ISBN är fel. Kapitel 33 påstår att alla citat ingår, men cirka 114 källposter från kapitlen saknas där, och "Referenced in"-fälten stämmer inte.
2. **Många kodexempel går inte att köra.** Rego-exemplen använder syntax som OPA 1.0 (december 2024) inte accepterar; Structurizr-DSL-exempel innehåller påhittade nyckelord; en Terraform-mall kan inte initieras; ett AWS CLI-kommando och ett npm-paket existerar inte; flera GitHub Actions-steg saknar obligatoriska parametrar. Bilaga A, som presenteras som "complete, working code samples", står ensam för 29 högallvarliga fynd: båda Go-listningarna och båda Rego-listningarna fungerar inte, och tre av fyra Terraform-listningar refererar odeklarerade resurser. Boken lär dessutom ut mönster som är avvecklade (DynamoDB-låsning av Terraform-state, Structurizr Lite/CLI/cloud, Terrascan, tfsec, Linux Academy, HashiCorp Learn).
3. **Ett antal fakta är fel eller föråldrade.** GDPR kallas direktiv, NIST CSF beskrivs med fem funktioner i stället för sex, en ISO 27001-kontroll anges med 2013-numrering, Spotify/Netflix/Capital One beskrivs som molnbaserade "från start", en investeringssiffra är fel med mer än en tiopotens, och statistik tillskrivs en CNCF-rapport som inte har någon 2024-utgåva och som mäter utvecklare, inte organisationer.

| Allvarlighet | Antal fynd | Innebörd |
|---|---|---|
| Hög | 106 | Felaktig uppgift, fantomkälla, felaktigt regelverksinnehåll eller kod som inte fungerar |
| Medel | 175 | Föråldrad uppgift, missvisande förenkling, fel år/upplaga/ISBN, bruten länk |
| Låg | 124 | Mindre precisionsbrist |
| **Totalt** | **405** | |

Siffrorna räknar fynd, inte enskilda fel: ett fynd kan omfatta flera rader eller flera kapitel (t.ex. räknas Source [1] som ett fynd per delrapport trots att det berör sju kapitel).

---

## 2. Omfattning och metod

- **Fullständig läsning.** Varje fil i bokens kanoniska filordning lästes rad för rad av en granskare med ansvar för en bokdel (elva granskare: Del A, kap. 5–6, kap. 7–9B, kap. 9C–15A, Del D, kap. 17–19, kap. 23/20/21, Del F–G, Del H, Bilaga A, kap. 33). Granskarna är AI-agenter med webbåtkomst; deras fynd innehåller evidens med URL så att varje påstående kan efterprövas.
- **Inventering och verifiering.** Granskarna inventerade sammanlagt över 1 100 kontrollerbara påståenden (statistik, attributioner, standarder och regelverk, verktygs-API:er, historik, korsreferenser, URL:er) och verifierade omkring 700 av dem mot primärkällor: officiell dokumentation, standardiseringsorgan, EUR-Lex, förlagssidor, Open Library, npm/PyPI/Docker Hub, GitHub-källkod samt Thoughtworks Radar-PDF:er (vol. 21, 28–32 och 34) och CNCF/SlashData-rapporterna i fulltext. Kodblock parsades lokalt (YAML, JSON, Python) där det var möjligt.
- **Egna tvärgående kontroller** (utförda separat från delrapporterna): ISBN-kontrollsiffror för alla åtta ISBN, interna länkar i samtliga manuskriptfiler, inventering av alla "Chapter N"-korsreferenser mot `book_index.json`, körning av `scripts/verify_sources.py` och `scripts/audit_references.py`, test av Thoughtworks Radar-slugs mot en nonsens-slug, uppslag av ISBN i Open Library, rendering av docs.structurizr.com i headless-webbläsare samt jämförelse av Appendix B:s påståenden med repots faktiska arbetsflöden och filer.
- **Bedömningsskala.** FEL (sakfel), FELCITERAT (källan finns inte, säger något annat eller har fel titel/år), FÖRÅLDRAT (sant 2023–2024 men inte längre), TVEKSAMT (otillräckligt stöd eller överdrift), INKONSEKVENT (motsäger annan del av boken eller repot), EJ VERIFIERBART.

---

## 3. Resultat i siffror

### Per delrapport

| Delrapport | Filer | Fynd | Hög | Medel | Låg |
|---|---|---|---|---|---|
| [Del A – Foundations](del_A_foundations.md) | part_a, 01, 26a, 02, 03, 04 | 39 | 7 | 20 | 12 |
| [Del B – kap. 5–6](del_B_kap05-06.md) | part_b, 05, 06 | 36 | 12 | 13 | 11 |
| [Kap. 7, 8, 9, 9B](del_B-C_kap07-09B.md) | 07, 08, part_c, 09, 09b | 51 | 10 | 20 | 21 |
| [Del C – kap. 9C–15A](del_C_kap09C-15A.md) | 09c, 10, 11, 12, 15a | 29 | 9 | 16 | 4 |
| [Del D – Delivery](del_D_delivery.md) | part_d, 13, 14, 15, 16 | 30 | 7 | 12 | 11 |
| [Del E – kap. 17–19](del_E_kap17-19.md) | part_e, 17, 18, 19 | 22 | 3 | 8 | 11 |
| [Del E – kap. 23, 20, 21](del_E_kap23-20-21.md) | 23, 20, 21 | 35 | 8 | 12 | 15 |
| [Del F–G](del_F-G_kap22-27.md) | part_f, 22, 24, part_g, 25, 26b, 27 | 36 | 6 | 15 | 15 |
| [Del H – bilagor](del_H_bilagor.md) | part_h, 28, 29, 31, 32, appendix_templates, maturity_model, control_matrix, radar | 28 | 6 | 15 | 7 |
| [Bilaga A – kodexempel](bilaga_A_kodexempel.md) | 30 (33 kodblock) | 65 | 29 | 22 | 14 |
| [Kap. 33 – källförteckning](kap33_kallforteckning.md) | 33 (74 poster) | 34 | 9 | 22 | 3 |
| **Totalt** | | **405** | **106** | **175** | **124** |

### Per tema (ett fynd kan tillhöra flera teman)

| Tema | Fynd (ca) | Kommentar |
|---|---|---|
| Fantomkällor och felciterade källor | 34 fynd, ~60 källposter | Se 4.1 |
| Standarder och regelverk (ISO, NIST, GDPR, SLSA, PCI, OSCAL, NIS2/DORA/AI Act) | 70 | Se 4.5 |
| Terraform/AWS-kod och -påståenden | 79 | Se 4.4 |
| Strukturella inkonsekvenser och korsreferenser | 50 | Se 4.6 |
| Structurizr (DSL, CLI, produktutbud) | 51 | Se 4.4 |
| Årtal och datering av källor | 37 | |
| Brutna eller omdirigerade URL:er | 38 | |
| Rego/OPA | 37 | Se 4.4 |
| ISBN | 21 fynd, 7 av 8 ISBN fel | Se 4.2 |

---

## 4. Systemiska problem (bokövergripande)

### 4.1 Fantomkällor och felciterade källor

Detta är det allvarligaste problemet eftersom det är bokövergripande och lätt för en recensent att upptäcka.

**Källor i den numrerade förteckningen (kap. 33) som inte finns eller inte säger det boken påstår**

| Källa | Problem | Berörda kapitel | Fynd-ID |
|---|---|---|---|
| [1] Thoughtworks (2024) *Architecture as Code: The Next Evolution*, Technology Radar | Ingen sådan blipp eller publikation. Slugen `/radar/techniques/architecture-as-code` ger samma generiska sida som en påhittad slug. Fulltextsökning i Radar vol. 30–31 (2024) ger noll träffar. Det enda Thoughtworks-materialet med liknande namn är ett poddavsnitt från februari 2025. | 1, 2, 4, 5, 26A, 29, 32 | A-01, B1-10, H-03, R-01 |
| [2] Thoughtworks Radar *Governance as Code*, Vol. 21 (2019) | Blippen finns inte. Vol. 21 innehåller "Security policy as code" (Trial); "governance as code" nämns bara i temaöversikten. URL:en omdirigeras till en generisk nyhetssida. Kapitlen anger 2024, kap. 33 anger 2019. Wayback-länkar med jokertecken (`/web/2024*/`) är sökvyer, inte arkiverade sidor. | 3, 5, 8, 11, 23, 26A | A-03, B1-09, B2-02, C-05, E2-13/14, R-02 |
| [29] Red Hat (2023) *Architecture as Code Principles and Best Practices* | Titeln är påhittad; URL:en ger 404; den flyttade sidan är en allmän IaC-förklaring utan de tre "principerna" (adoptability, extensibility, productivity) som kap. 1–2 tillskriver Red Hat. | 1, 2 | A-02, R-03 |
| [7] CNCF *State of Cloud Native Development 2024* | Ingen 2024-utgåva finns; serien produceras av SlashData för CNCF och mäter utvecklare, inte organisationer. Siffrorna 67 %/58 %/52 % och "two thirds" återfinns inte i någon utgåva (Q3 2025: 46 % av backend-utvecklarna använder mikrotjänster, 27 % händelsedrivet). Slutsatser om styrning och revisionsspår som tillskrivs rapporten saknar stöd. | 1, 7, 8, 26A | A-04, B2-01 |
| [15] Pulumi (2024) *Testing Infrastructure as Code Programs* | Finns inte. Innehållet som tillskrivs källan (kontrasten mot Terratest/`terraform test`) finns i ett Pulumi-inlägg daterat 30 juni 2026. | 13, 14 | D-01 |
| [20] HashiCorp (2023) *Terraform Security Best Practices* | Sidan heter "Learn Terraform recommended practices" och handlar om arbetsflödesmognad, inte nyckelhantering eller hemligheter. | 9, 9B | B2-03 |
| Brown, S. (2022) *Documenting Software Architecture with Structurizr*, Structurizr Blog | `blog.structurizr.com` saknar DNS-post, Wayback har inga ögonblicksbilder, och termen "diagram decay" som citeras finns inte hos Brown. | 6, 24 | B1-11, R-07 |
| NIST (2023) *Requirements Engineering for Secure Systems*, SP 800-160 | SP 800-160 Vol. 1 Rev. 1 heter *Engineering Trustworthy Secure Systems* (nov 2022). | 2 | A-05, R-08 |
| GitLab (2024) ×2, "GitHub Open Source Community", Kvadrat *Technology Consulting Excellence* | Oåterfinnbara titlar; GitLab-SSOT-posten citeras inte ens i något kapitel; Kvadrat-profilen ger 404. | 2, 11, 29 | A-06, R-04–R-06, H-06 |

**Kapitelkällor med titlar som inte motsvarar någon känd publikation** (saknar genomgående URL och finns inte i kap. 33):

- Kap. 9/9B: ENISA *Cloud Security Guidelines for EU Organisations* (2023), OWASP *Application Security Architecture Guide* (2023) – B2-09, B2-10
- Kap. 12: IEEE CS *Quantum Computing Impact on Infrastructure*, GSF *Sustainable Infrastructure Patterns*, CNCF *Future of Cloud Native Infrastructure*; Gartner-titeln fel – C-09
- Kap. 13: AWS *Infrastructure Testing Strategy Guide*, NIST *Security Testing for Cloud Infrastructure*, CSA *Cloud Security Testing Guidelines* – D-05
- Kap. 15: FinOps Foundation *FinOps Framework and Architecture as Code Best Practices*, CSA *Cloud Cost Optimisation Security Guidelines*, Microsoft *Azure Cost Management Architecture as Code Best Practices* – D-06
- Kap. 16: Microsoft *Azure Migration Framework and Architecture as Code Best Practices*, Gartner *Infrastructure Migration Trends in European Markets*, AXELOS *ITIL Foundation: IT Service Management for Cloud Migration* – D-07
- Kap. 17: McKinsey *Organisational Transformation Best Practices* (2023); "Spotify Technology (2023) *Spotify Engineering Culture*" är Knibergs videor från 2014 – E1-01, E1-02
- Kap. 18: HashiCorp (2024) *Infrastructure as Code Maturity Model*, HashiCorp Learn (plattformen nedlagd 2022) – E1-08
- Kap. 21: sex poster (Gartner, McKinsey, AWS CAF med fel titel, Microsoft, "HashiCorp Learn", SANS) – E2-06
- Kap. 24: CNCF *Infrastructure as Code Best Practices*, HashiCorp *Terraform Maturity Model*, FinOps Foundation *Cloud Financial Management Playbook* – FG-03
- Kap. 25: McKinsey Global Institute *The Future of Infrastructure*, "MIT Technology Review … MIT Press", IEEE CS *Edge Computing and 5G Integration*, GSF *Carbon-Aware Computing Guidelines* – FG-02
- Kap. 26B: FinOps Foundation *Cloud Cost Management for Sustainable Delivery*, OPA *Policy as Code Cookbook* – FG-04

Ett mönster: bokens eget nyckelbegrepp "Architecture as Code" förekommer i flera leverantörstitlar (FinOps Foundation, Microsoft, Red Hat, Thoughtworks), vilket inga av leverantörerna har publicerat. Dessa titlar bör betraktas som konstruerade tills motsatsen bevisats.

**Källförteckningens integritet (kap. 33)** – R-17 till R-33, D-18, FG-20, E1-06: cirka 114 källposter från kapitlens egna källistor saknas trots påståendet "All citations in the manuscript are included in this compiled list"; "Referenced in" har 8 falska positiva och 12 falska negativa; fyra länkade kapitelfiler finns inte (`26a_future_trends.md` ×3, `20_team_structures.md`, `10_policy_as_code.md`, `32_index.md`); minst nio kapitelrubriker avviker från `book_index.json`; HashiCorp *State of Cloud Strategy Survey 2024* listas men citeras ingenstans i manuskriptet.

### 4.2 ISBN

Sju av åtta ISBN är fel. Fyra klarar inte ens kontrollsiffran, och det ISBN som anges för *Clean Architecture* tillhör en annan bok. `scripts/verify_sources.py` kontrollerar bara formatet, vilket förklarar varför detta inte fångats.

| Verk | ISBN i boken | Korrekt ISBN | Fynd-ID |
|---|---|---|---|
| Martin, *Clean Architecture* | 978-0-13-468599-1 (= Bloch, *Effective Java*, 3 uppl.) | 978-0-13-449416-6 | A-08, R-09 |
| Skelton & Pais, *Team Topologies* | 978-1-942788-81-4 (ogiltig kontrollsiffra) | 978-1-942788-81-2 | E1-04, FG-07, R-11 |
| Bass, Clements & Kazman, *Software Architecture in Practice*, 4 uppl. | 978-0-13-688580-4 (ogiltig) | 978-0-13-688609-9 | FG-07, R-12 |
| Chung et al., *Non-Functional Requirements in Software Engineering* | 978-0-7923-8666-6 (ogiltig) | 978-0-7923-8666-7 (Kluwer/Springer, 1999/2000) | R-13 |
| Richardson, *Microservices Patterns* | 978-1-617-29454-1 (ogiltig) | 978-1-61729-454-9 | FG-07, R-14 |
| Beyer et al., *The Site Reliability Workbook* | 978-1-4920-2974-8 (giltig men oregistrerad) | 978-1-492-02950-2 | B1-23, R-10 |
| Ford, Parsons & Kua, *Building Evolutionary Architectures* | 978-1-491-98634-9 (giltig men oregistrerad) | 978-1-491-98636-3 (1 uppl. 2017; 2 uppl. 2022 bör övervägas) | R-15 |
| Forsgren, Humble & Kim, *Accelerate* | 978-1-942788-33-1 | Korrekt | – |

Open Library bekräftade 978-0-13-449416-6 (*Clean Architecture*), 978-0-13-688609-9 (*Software Architecture in Practice*), 978-1-61729-454-9 (*Microservices Patterns*) och 978-0-7923-8666-7 (Chung et al.) i en oberoende kontroll.

### 4.3 Statistik, fallstudier och företagspåståenden utan stöd

- **"Over £500 billion in five years"** i digital transformation (kap. 21:38). IDC:s Spending Guide anger nära 4 biljoner USD enbart för 2027; femårssumman överstiger 10 biljoner USD. Fel med mer än en tiopotens – E2-01.
- **Spotify, Netflix och Capital One "cloud-native from inception"** (kap. 21:70, 196). Alla tre migrerade från egna datacenter (Spotify till GCP 2016–2018, Netflix klart januari 2016, Capital One stängde sista datacentret 2020) – E2-02.
- **Capital One 99,99 %/40 %/70 %** (kap. 21:76). Inga primärkällor; siffrorna hör delvis till andra kunders fallstudier; Capital One uppger själva att kostnaderna steg – E2-03.
- **Backstage möjliggjorde tillväxten 1 → 500 miljoner användare** (kap. 21:198). Kronologiskt omöjligt: 1 miljon användare 2009, Backstage internt cirka 2016, öppen källkod 2020 – E2-04.
- **CNCF 67 %/58 %/52 % och "two thirds"** (kap. 1, 7, 8) – se 4.1.
- **Gartner USD 679 miljarder (+20,4 %)** (kap. 15:75, 25:229). Siffran är från Gartners pressmeddelande 13 november 2023, inte en 2024-prognos, och reviderades i november 2024 till 595,7 miljarder för 2024 – D-08, FG-08.
- **MarketsandMarkets** (kap. 15, 25): siffrorna 0,8 → 2,3 miljarder USD (CAGR 24 %) stämmer, men rapporten är från augusti 2022 och titeln är inte rapportens – D-20, FG-32, R-25.
- **"Studies demonstrate that IaC reduces manual effort by up to 70 %"** (kap. 21:44) saknar källa – se delrapport E2.

### 4.4 Kod som inte fungerar eller lär ut avvecklade mönster

**Rego/OPA.** OPA 1.0 (december 2024) gjorde nyckelorden `if` och `contains` obligatoriska. Exempel i kap. 2 (A-07), 9B (B2-05), 10 (C-01, C-02) och Bilaga A (rad 3289 ff.) använder `deny[msg] { … }`-formen och ger parsefel. Kap. 10 blandar dessutom `import rego.v1` med gammal regelsyntax i samma fil. Kap. 11:s OPA-testmodul refererar en annan package utan `data.`-prefix (C-03) och CI-steget skriver `--format pretty` till en fil som sedan läses som JSON (C-04). Kap. 11 i övrigt använder korrekt v1-syntax.

**Terraform/AWS.**
- DynamoDB-låsning av S3-backend (`dynamodb_table`) är avvecklad sedan Terraform 1.11 till förmån för `use_lockfile = true`; mönstret återkommer i kap. 9, 9B, 13 och 21 – B2-12, D-12, E2-05.
- Terraform-mallen i kap. 21 kan inte initieras: variabler i `backend`-blocket är förbjudna och `versioning` är inget backend-argument – E2-05.
- CloudTrail-exemplet använder `AWS::KMS::Key` som `data_resource`-typ, vilket inte är tillåtet; `terraform apply` misslyckas – B2-04.
- `aws cloudformation import-resources-to-stack` existerar inte, och importmallen saknar obligatorisk `DeletionPolicy` samt blandar import med nyskapade resurser – D-03, D-04.
- `@pulumi/pulumi/testing` existerar inte (rätt API är `pulumi.runtime.setMocks`) – D-02.
- Regionmappningen i kap. 25 anger eu-west-1 som Frankrike och eu-south-1 som Spanien (Irland respektive Milano) – FG-05. Electricity Maps-koden läser ett fält som ändpunkten inte returnerar, så förnybarhetsfaktorn blir alltid 0,40 – FG-06.
- `kubectl apply --server-side --dry-run=client` avbryts med fel – B2-07.

**Structurizr.** Deployment-vyn i kap. 6 är skriven med modellsyntax (B1-01), `autoLayout lr rankSeparation 450` och `paperSize` finns inte (B1-02), manuella koordinater via `element webApp 100 100` finns inte i DSL:n (B1-03), och CLI:n anropas med exportformaten `png`/`structurizr` och versionen 2024.03.01 som inte existerar; repots eget `scripts/render_structurizr_diagrams.sh` har samma fel (B1-04). Produktutbudet är föråldrat: Structurizr CLI, Lite och cloud service har alla nått end of life enligt docs.structurizr.com (verifierat 2026-10-30 i rendrad sida) och ersatts av `structurizr local`, `server` och `export` – B1-12, A-21.

**CI/CD- och leverantörsexempel.**
- `npm install -g @swagger-api/swagger-validator`: paketet finns inte – B1-05.
- `pip3 install terrascan` installerar ett övergivet Python-paket från 2020; Terrascan är arkiverat – B1-06.
- `conftest verify` kör Rego-enhetstester; rätt kommando för att validera filer är `conftest test` – B1-07.
- `anchore/scan-action@v3` har ingen `output-file`-indata (införd i v6) – evidensartefakten som texten beskriver skapas aldrig – C-07.
- SLSA-provenance-exemplet blandar v1-`predicateType` (felstavad) med v0.2-schemats fält – C-06.
- `pulls.createReviewComment` anropas utan obligatoriskt `commit_id` och utan `pull-requests: write` – E2-07.
- CALM-exemplet i kap. 22 bryter mot CALM-schemat (`relationship-type` ska vara objekt, fältet `parties` finns inte, protokollet `PostgreSQL` saknas i enumerationen) trots att kapitlet lyfter fram maskinell validering som CALM:s styrka – FG-01.
- Python-exemplen i kap. 2 och Appendix D anropar odefinierade metoder och kan inte köras (A-17, H-07).
- "Private Issue" i GitHub (kap. 19) finns inte som funktion; ärenden följer repots synlighet. Exemplet riskerar att få läsare att publicera sårbarhetsdetaljer – E1-03.

**Bilaga A (kap. 30).** Bilagan presenteras som "complete, working code samples", men 65 fynd (29 Hög) visar att en stor andel av de 33 listningarna inte går att köra i den form de står: båda Go-listningarna kompilerar inte (K-05, K-06); båda Rego-listningarna misslyckas under OPA 1.x, `math.max` finns inte som builtin och 13_CODE_J:s tester kan aldrig bli gröna eftersom en mängd indexeras med `results[0]` (K-01–K-04); tre av fyra Terraform-listningar refererar odeklarerade resurser eller använder ogiltiga argument – `aws_rds_instance` är ingen resurstyp (sju ställen), azurerm-providern har inget `location`-argument, `timeadd("30*24h")` är ogiltigt och `cost_filters` är borttaget (K-08, K-12–K-14, K-24); CloudFormation-mallen använder `!Contains` i `Conditions` där det inte är tillåtet (K-07); två Python-listningar kraschar bevisat vid körning (K-10, K-11); Kubernetes-testsviten letar Pod Security-etiketter på poddar i stället för namespaces och testar därmed ingenting (K-16); OSCAL-dokumenten ger 25 schemafel mot NIST:s officiella OSCAL 1.1.2-schema (K-17, K-18); Structurizr-workspacet laddas inte eftersom fyra relationer i den dynamiska vyn saknas i modellen (K-19); Jenkins-pipelinen använder `conftest verify` med fel namespace så att grinden aldrig utvärderar policyn, och flaggorna `--output-file` och `--currency` finns inte (K-20–K-23). `upload/download-artifact@v3` slutade fungera 2025-01-30 (K-15).

### 4.5 Standarder och regelverk: fel eller föråldrat

| Påstående i boken | Korrekt läge | Fynd-ID |
|---|---|---|
| GDPR anges som "Directive (EU) 2016/679" (kap. 9, 9B) | GDPR är en förordning (Regulation) | B2-06 |
| NIST CSF med fem funktioner (kap. 9) | CSF 2.0 (feb 2024) har sex, inklusive Govern | B2-08 |
| ISO 27001-kontroll "A.12.6.1" (kap. 15A) | 2013-numrering; i 27001:2022 är det kontroll 8.8 | C-08 |
| A.5/A.8 beskrivs som kontroller (kap. 10, 12) | De är teman i Annex A 2022 | se delrapport C |
| ISO/IEC 42010:2011 (kap. 26B) | Ersatt av ISO/IEC/IEEE 42010:2022 | FG-10 |
| EU:s AI-förordning som "emerging proposals" (kap. 27) | I kraft sedan augusti 2024 | FG-15 |
| Post-kvantkryptografi "when available" | FIPS 203/204/205 publicerade 13 augusti 2024 | se delrapport C |
| SLSA-provenance v1.0 | Specifikationen är v1.2; v1.0 markerad "Retired" | C-06 |
| DORA-måtten som fyra mått med "mean time to restore" (kap. 17, 18) | Fem mått sedan 2023 (failed deployment recovery time, rework rate 2024) | E1-09 |
| SSDF-mappning PO.1.3/PS.3.1 för SBOM (kap. 15A) | SBOM-praktiken är PS.3.2 | C-14 |
| IEEE 1012-2016 "Software Verification and Validation" | Titeln är *System, Software, and Hardware Verification and Validation*; ersatt av 1012-2024 | R-16 |
| Terraform som öppen källkod (kap. 27) | BUSL sedan augusti 2023; OpenTofu nämns inte i boken | FG-16 |
| Azure Sentinel, AWS Fault Injection Simulator, Linux Academy, HashiCorp Learn, Kubecost som open source, Node 18, Amazon Linux 2, Lambda python3.9 | Omdöpta, nedlagda eller avvecklade | C, E1-10, D-10, D-11, A-20 |

### 4.6 Strukturella inkonsekvenser

- **Delintroduktioner mot `book_index.json`.** Del D-intron räknar in kap. 15A (ligger i Del C), Del E-intron nämner inte kap. 23 och `mkdocs.yml` placerar det under en annan del (indexet lägger det i Del E), Del F-intron räknar in kap. 23, Del G-intron räknar in kap. 26A (ligger i Del A), kap. 21 placerar kap. 23 i Del F och tillskriver det "Requirements as Code" som kapitlet aldrig behandlar – D-13, E1-11, FG-12, FG-13, E2-12.
- **Kap. 26A:s påståenden om andra kapitel** ("Chapter 14 warns …", "Chapter 19 argues narratives anchor change", "Chapter 15 warns that automation without cost transparency becomes an expensive hobby") saknar stöd i de kapitlen; kap. 19 argumenterar tvärtom för deklarativa specifikationer framför narrativ. Hänvisningar till kap. 20 är inaktuella efter omnumreringen (kap. 20 är nu AI-agentteamet) – A-24, A-25.
- **Appendix B mot repot.** Arbetsflödena `build-book.yml`, `generate-presentations.yml` och `generate-whitepapers.yml` finns inte (konsoliderade i `unified-build-release.yml`, Docker-baserad, 60 minuters timeout); `content-validation.yml` kör pytest, inte länkvalidering; "31 Markdown files" och "Twenty-six whitepapers" stämmer inte; `aacplatform/aac` finns inte – H-02, H-05, H-08, H-12.
- **Appendix C "FINOS Project Blueprint"** beskrivs som ett existerande CALM-baserat initiativ. `finos/project-blueprint` är en repositorymall med licens- och styrningsfiler; innehållet i appendixet kommer från bokens egna kapitel – H-01.
- **AaC kontra CALM.** Beskrivningen "YAML-definitioner och plugin-arkitektur" (kap. 6, 31, 33) matchar projektet DevOps-MBSE/AaC men källsätts till FINOS CALM, som är JSON-schemabaserat – B1-08, H-02.
- **Kap. 20 och `CLAUDE.md`** beskriver bot-arbetsflöden (`architect-bot.yml`, `editor-bot.yml`, `qa-bot.yml`, `developer-bot.yml`, `designer-bot.yml`) som inte finns i `.github/workflows/`; det enda etikettstyrda flödet är `mermaid-designer-bot.yml` – E2-08.
- **Licens.** Kap. 29 anger CC BY 4.0, men repot saknar LICENSE-fil och `docs/pandoc.yaml` trycker "All rights reserved" i varje PDF – H-04.
- **Renderingsfel.** CoP-mallen i kap. 18 ligger som riktiga rubriker utanför kodblock och blir ett spökkapitel i PDF/EPUB (E1-05); kap. 9 och 9B innehåller 96 hårda radbrytningar mitt i ord (B2-28).

---

## 5. Prioriterad åtgärdslista

Ordningen speglar synlighet för läsaren och arbetsinsats. ID i parentes.

1. **Ersätt eller stryk Source [1] och [2] i alla kapitel** och skriv om de meningar som tillskriver Thoughtworks specifika ståndpunkter (A-01, A-03, B1-09/10, B2-02, C-05, E2-13/14, H-03, R-01, R-02). Verkliga alternativ: Radar-blipparna "Security policy as code" (vol. 21/23), "Diagrams as code" (vol. 23), "Infrastructure as code"; FINOS CALM-dokumentationen.
2. **Rätta Source [29] Red Hat och de tre "Red Hat-principerna" i kap. 1–2** (A-02, R-03).
3. **Byt ut CNCF-statistiken** i kap. 1, 7, 8, 26A mot verifierbara siffror med exakt utgåva och population (A-04, B2-01).
4. **Rätta de sju ISBN** enligt tabellen i 4.2 och låt `verify_sources.py` slå upp ISBN mot Open Library i stället för att bara kontrollera formatet (R-09–R-15).
5. **Gå igenom alla kapitelkällistor** och ersätt eller stryk de cirka 60 poster med oåterfinnbara titlar (listan i 4.1). Lägg in kvarvarande poster i kap. 33 och generera "Referenced in" automatiskt (`scripts/audit_references.py` har redan ankarparsningen).
6. **Konvertera alla Rego-exempel till OPA 1.0-syntax** och kör `opa check --v1-compatible` i CI (A-07, B2-05, C-01–C-04, Bilaga A).
7. **Uppdatera Terraform-state-mönstret** till `use_lockfile` i kap. 9, 9B, 13, 21 och rätta backend-blocket i kap. 21 (B2-12, D-12, E2-05).
8. **Rätta Structurizr-kapitlet**: DSL-syntaxen (B1-01–03), CLI-anrop och version (B1-04, inklusive `scripts/render_structurizr_diagrams.sh`), produktutbudet local/server/export (B1-12), samt Brown-citatet (B1-11).
9. **Rätta regelverksuppgifterna**: GDPR som förordning, NIST CSF 2.0, ISO 27001:2022-numrering, ISO/IEC/IEEE 42010:2022, AI-förordningen i kraft, FIPS 203–205, DORA:s fem mått (B2-06, B2-08, C-08, FG-10, FG-15, E1-09).
10. **Rätta kap. 21:s fallstudier och siffror** (E2-01–E2-04) och kap. 19:s "private Issue" (E1-03).
11. **Rätta AWS-exemplen**: CloudTrail-datatyp (B2-04), CloudFormation-import (D-03, D-04), Pulumi-API (D-02), regionmappning och Electricity Maps (FG-05, FG-06).
12. **Rätta CI-exemplen**: `conftest test`, existerande npm-paket, Terrascan bort, `anchore/scan-action@v7`, `commit_id` och `permissions` i GitHub Actions, `kubectl --dry-run=server` (B1-05–07, C-07, E2-07, B2-07).
13. **Rätta CALM-exemplet** i kap. 22 och kör `calm validate` på det (FG-01).
14. **Harmonisera delintroduktioner, kap. 1, kap. 21 och `mkdocs.yml` med `book_index.json`** (D-13, E1-11, FG-12, FG-13, E2-12) och skriv om kap. 26A:s korsreferenser (A-24, A-25).
15. **Skriv om Appendix C** som ett eget förslag inspirerat av CALM och rätta AaC/CALM-förväxlingen i kap. 6, 31 och 33 (H-01, H-02, B1-08).
16. **Uppdatera Appendix B, kap. 20 och `CLAUDE.md`** så att de beskriver repots faktiska arbetsflöden och filantal (H-05, H-08, H-12, E2-08).
17. **Besluta om licens** och lägg till LICENSE-fil; synkronisera `pandoc.yaml` med kap. 29 (H-04).
18. **Datera om marknadssiffrorna** (Gartner nov 2023/nov 2024, MarketsandMarkets aug 2022) eller uppdatera dem (D-08, FG-08, D-20, R-25).
19. **Rätta renderingsfelen** i kap. 18 (CoP-mallen) och de hårda radbrytningarna i kap. 9/9B (E1-05, B2-28).
20. **Ta bort alla `web.archive.org/web/2024*/`-länkar** (sökvyer, inte arkiv) och ersätt med riktiga ögonblicksbilder eller aktuella URL:er (A-03, B1-09, B1-11).

---

## 6. Resultat per delrapport

**Del A (kap. 1, 26A, 2, 3, 4)** – 39 fynd. Tyngdpunkten ligger på källapparaten: Source [1], [2], [29] och NIST SP 800-160 (A-01–A-05), GitLab-källorna (A-06) samt ISBN för *Clean Architecture* (A-08). Rego-exemplen i kap. 2 parsar inte i OPA 1.0 (A-07), Python-validatorn kan inte köras (A-17), CODEOWNERS saknar `@org/`-prefix (A-18) och ett AWS CLI-kommando saknar obligatorisk flagga (A-19). Kap. 26A:s hänvisningar till andra kapitel saknar stöd (A-24, A-25). Verifierat korrekt: Nygard 2011, GitHub protected branches, CDK assertions, `az deployment what-if`, OMG MDA 2001, Schmidt 2006, Selic 2003.

**Del B, kap. 5–6** – 36 fynd, flest Hög av alla delrapporter (12). Kap. 6 har fyra Structurizr-fel som gör exemplen okörbara (B1-01–B1-04) och ett föråldrat produktutbud (B1-12). Kap. 5 har tre CI-exempel som inte fungerar (B1-05–B1-07). Microsoft Learn-titeln "Design multi-stage release pipelines with approvals" finns inte och den riktiga dokumentationen säger att approvals inte definieras i YAML (B1-21). SRE Workbook-ISBN fel (B1-23), gdpr.eu-URL 404 (B1-22).

**Kap. 7, 8, 9, 9B** – 51 fynd. CNCF-statistiken (B2-01), Source [2] och [20] (B2-02, B2-03), CloudTrail- och Rego-kod (B2-04, B2-05), GDPR som direktiv (B2-06), kubectl-flaggor (B2-07), NIST CSF (B2-08), två fantomkällor (B2-09, B2-10). I Medel: fel årtal för EDPB, EBA, CSA CCM v4, CIS v8, Azure Security Benchmark, ENISA; GDPR art. 30 är inte revisionsloggning; AWS App Mesh nedlagt; `kubeval` nedlagt.

**Del C, kap. 9C, 10, 11, 12, 15A** – 29 fynd. Rego-syntaxen (C-01, C-02), OPA-testmodulen och CI-steget i kap. 11 (C-03, C-04), SLSA-provenance (C-06), `anchore/scan-action` (C-07), ISO 27001-numreringen (C-08), kap. 12:s källista (C-09), SSDF-mappningen (C-14). I Medel: STIX/TAXII-namn och år, Azure/Microsoft Sentinel, AWS FIS, PQC-formuleringen, odefinierad `tls_self_signed_cert`, kontroll-ID:n som skiljer sig mellan kapitel och bilaga.

**Del D, kap. 13, 14, 15, 16** – 30 fynd. Source [15] (D-01), Pulumi-API (D-02), CloudFormation-import (D-03, D-04), nio fabricerade källtitlar (D-05–D-07). I Medel: Gartner-dateringen (D-08), `terraform test` saknas i beskrivningen av Terraforms testbarhet (D-09), Kubecost/OpenCost (D-10), Amazon Linux 2 (D-11), DynamoDB-låsning (D-12), Del D-intron räknar in 15A (D-13), referenslistans ofullständighet (D-18).

**Del E, kap. 17, 18, 19** – 22 fynd. McKinsey- och Spotify-källorna (E1-01, E1-02), "private Issue" (E1-03), Team Topologies-ISBN (E1-04), CoP-mallen som spökkapitel (E1-05), bibliografins falska "Referenced in" (E1-06), Puppet Labs-namnet (E1-07), HashiCorp Learn (E1-08), DORA-måtten (E1-09), Linux Academy (E1-10), Del E-intron saknar kap. 23 (E1-11). Verifierat korrekt: *Accelerate* (ISBN, år, förlag), *The DevOps Handbook* 2016, Conways lag (Datamation, april 1968), CODEOWNERS, Discussions, opengitops.dev, dora.dev.

**Del E, kap. 23, 20, 21** – 35 fynd. Kap. 21 står för de flesta Hög-fynden: investeringssiffran (E2-01), "from inception" (E2-02), Capital One-siffrorna (E2-03), Backstage (E2-04), Terraform-mallen (E2-05), sex fantomkällor (E2-06). Kap. 20: GitHub Actions-anropet (E2-07) och bot-tabellen som inte motsvarar repot (E2-08). I Medel: AWS European Sovereign Cloud beskrivs som kommande trots GA januari 2026 (E2-09), Googles "carbon-neutral" övergivet sedan 2023 (E2-10), kap. 23 placeras i fel del (E2-12), källtitlarna "Policy as Code Overview" (E2-13, E2-14).

**Del F och G, kap. 22, 24, 25, 26B, 27** – 36 fynd. CALM-exemplet (FG-01), fantomkällor i kap. 25, 24 och 26B (FG-02–FG-04), regionmappning och Electricity Maps (FG-05, FG-06), tre ISBN (FG-07), Gartner (FG-08), ENISA-rapportens år (FG-09), ISO 42010 (FG-10), NCSC-titlar (FG-11), delintron F och G (FG-12, FG-13), "idempotent configuration in chapter 2" som kap. 2 inte nämner (FG-14), AI-förordningen (FG-15), Terraform som open source (FG-16), `github.com/structurizr/dsl` nedlagt (FG-17). Verifierat korrekt: C4-nivåer, PlantUML/Mermaid, FIPS 203–205, Quantum Flagship, EuroQCI, Climate Neutral Data Centre Pact, MarketsandMarkets-siffrorna.

**Del H, bilagor och supplement** – 28 fynd. FINOS Project Blueprint (H-01), AaC/CALM och `aacplatform/aac` (H-02), Source [1] (H-03), licensen (H-04), arbetsflödena (H-05), biografins källor (H-06), Appendix D-koden med åtta odefinierade metoder (H-07), filantal (H-08, H-12), odefinierad källa [13] i mognadsmodellen (H-14), sju brutna ankare i radarverktyget och ordlistans JSON-dataset som saknar fem termer (H-16, H-17). Biografin i kap. 29 kunde inte verifieras mot publika källor eftersom Kvadrat-profilen ger 404; inga ytterligare efterforskningar gjordes. Verifierat korrekt: CALM-definitionen mot calm.finos.org, FINOS-projektets Graduated-status, mognadsmodell ↔ radar (10 discipliner, 50 identiska frågor, nivåer 0–5), aac.geon.se live.

**Bilaga A, kodexempel (kap. 30)** – 65 fynd, flest Hög av alla delrapporter (29). 25 av 33 kodblock validerades med verktyg (`py_compile` och körning, PyYAML, `tsc --strict`, `gofmt`/`go vet`/`go test -c` mot riktiga moduler, `jsonschema` mot OSCAL 1.1.2, OPA:s builtin-register) och 8 genom läsning mot primärkällor; terraform-, opa- och conftest-binärer kunde inte köras i granskningsmiljön. De viktigaste fynden sammanfattas i 4.4. I Medel: föråldrade action-versioner, Bitnami-bildernas flytt till `bitnamilegacy`, EOL för Kubernetes 1.29 och Node 20, aws-sdk-go v1 utan support, en Jenkinsfile felmärkt som YAML, död Structurizr-URL i källistan, två saknade navigationsankare och fem listningar som inte refereras från sina kapitel (K-46–K-48). Ej verifierbart: "MSB 3.2.1/3.2.2"-referenserna, Structurizr-temats URL (värden blockerad från miljön) och om `jq` ingår i `bitnami/kubectl`-bilden.

**Kap. 33, källförteckning** – 34 fynd över 74 poster (66 unika verk). Nio sannolikt fiktiva publikationer (R-01–R-08 m.fl.), sju påhittade titlar på verkliga sidor (Atlassian [3], HashiCorp [16] [20], Pulumi [15], Microsoft Learn [12], GDPR.eu [27], Kvadrat), sex döda eller omdirigerade URL:er, fel uppgifter för NIST SP 800-160, IEEE 1012, Forsberg & Mooz (venue/år), Thoughtworks ADR-blippen (heter "Lightweight Architecture Decision Records", 2016–2018, inte 2023) och MarketsandMarkets. Cirka 30 poster verifierade som korrekta, bland dem CNCF:s definition, FINOS/CALM, NIST SP 800-53 Rev. 5, OMG MDA (ormsc/2001-07-01), Nygard 2011, Schmidt 2006, Selic 2003, *Accelerate*, HashiCorp-undersökningen 2024 och "Diagrams as code" (vol. 23).

---

## 7. Verifierat korrekt (urval)

För att ge en rättvis bild: följande centrala påståenden kontrollerades mot primärkällor och håller.

- Conways lag (Datamation, april 1968), Nygards ADR-artikel (2011), C4-modellens nivåer, Team Topologies fyra teamtyper och tre interaktionssätt, Westrums kulturtypologi.
- *Accelerate* (IT Revolution 2018, ISBN 978-1-942788-33-1), *The DevOps Handbook* (2016), OMG MDA-dokumentet (2001), Schmidt (IEEE Computer 2006), Selic (IEEE Software 2003), IEEE 1012 som standard.
- NIST SP 800-53 Rev. 5 (2020), NIST SP 800-218 SSDF, OpenGitOps v1.0.0:s fyra principer, Kubernetes PSP-avvecklingen (deprecated 1.21, borttagen 1.25), Pod Security Admission.
- CNCF:s cloud-native-definition (DEFINITION.md), FINOS Architecture as Code-projektets Graduated-status, CALM:s komponenter (CLI, Hub, docify), FIPS 203/204/205 (augusti 2024), EU Quantum Flagship, EuroQCI, Climate Neutral Data Centre Pact.
- GitHub protected branches, CODEOWNERS, Discussions, AWS CDK assertions-modulen, `az deployment what-if`, Terraform `import`-block (1.5), `terraform test` (1.6).
- MarketsandMarkets IaC-prognosen (0,8 → 2,3 miljarder USD, CAGR 24 %) och Gartner-siffran 678,8 miljarder USD som sådana (men se 4.3 om dateringen).
- Mognadsmodellen och radarverktyget är konsistenta (10 discipliner, 50 frågor, nivåer 0–5); alla kodlistningar som kapitlen hänvisar till (13-A till 13-L, 05_CODE_1, 10_CODE_1–4, 14_CODE_1–3, 15_CODE_1–3, 17_CODE_1–3, 21_CODE_1) finns i Bilaga A.

---

## 8. Begränsningar

- Granskarna är AI-agenter. Alla fynd är belagda med URL:er eller repo-sökvägar, och ett urval har kontrollerats oberoende (Thoughtworks-slugs, Open Library-ISBN, Structurizr-sidorna, repots arbetsflöden, LICENSE och `pandoc.yaml`, interna länkar). Kontrollera ändå evidensen innan massändringar görs, särskilt för fynd märkta TVEKSAMT.
- Den delade webbsökbudgeten tog slut för flertalet granskare i slutfasen; resterande kontroller gjordes med direkta hämtningar av leverantörsdokumentation. Poster som inte kunde avgöras är listade under "Ej verifierbart" i varje delrapport (bl.a. IDC-rapporten bakom betalvägg, Structurizr-bloggen, Scaleway-påståendet i kap. 21).
- Från granskningsmiljön blockerades github.com (HTTP 403, kringgått via raw.githubusercontent.com), iso.org, gartner.com och web.archive.org. GitHub-repon kunde därför bara verifieras via råfiler och API-svar.
- Uppgifter daterade efter mitten av 2026 (t.ex. Structurizr cloud services slutdatum, Pulumi-inlägget 30 juni 2026, GitHubs changelog 2026) kommer från hämtade sidor och bör dubbelkollas av en människa.
- Biografiska påståenden i kap. 29 kunde inte verifieras mot publika källor och har inte efterforskats vidare.
- `docs/book_structure.md`, `docs/index.md` och `README.md` ingår inte i bokens byggordning och har inte granskats, bortsett från att "Thirty-eight chapters" där avser 31 kapitel plus 7 bilagor.

---

## 9. Rekommendationer för processen

1. Låt `scripts/verify_sources.py` slå upp varje ISBN mot Open Library/Google Books och varje URL med `-L` och innehållskontroll av sidtiteln; i dag kontrolleras bara ISBN-format och HTTP-status.
2. Generera "Referenced in" i kap. 33 automatiskt från kapitlens `#source-n`-ankare och låt CI falla när en kapitelkälla saknar motsvarighet i kap. 33.
3. Extrahera alla kodblock i CI och validera dem: `opa check --v1-compatible` för Rego, `terraform validate`/`tflint` för HCL, `yamllint` plus `kubeconform` för Kubernetes-manifest, `python3 -m py_compile` för Python, `structurizr-cli`/`structurizr export` för DSL och `calm validate` för CALM.
4. Förbjud `web.archive.org/web/<år>*/`-länkar i stilguiden; kräv URL + hämtningsdatum för webbkällor och förbjud kategoribeskrivningar som titlar (vilket `docs/STYLE_GUIDE.md` redan gör på rad 117).
5. Uppdatera `CLAUDE.md`: bot-tabellen listar arbetsflöden som inte finns, och `scripts/verify_links.py` som nämns där existerar inte.
6. Lägg till en `book_index.json`-konsistenstest för delintroduktionerna, kap. 1:s översikt, kap. 27:s sammanfattning och `mkdocs.yml`.

---

## 10. Filer i denna katalog

| Fil | Innehåll |
|---|---|
| `README.md` | Denna sammanställning |
| `fynd_tabell.md` | Alla fynd i en tabell, sorterade efter allvarlighet |
| `del_A_foundations.md` | Del A: part_a, kap. 1, 26A, 2, 3, 4 |
| `del_B_kap05-06.md` | Del B: part_b, kap. 5, 6 |
| `del_B-C_kap07-09B.md` | Kap. 7, 8, part_c, 9, 9B |
| `del_C_kap09C-15A.md` | Del C: kap. 9C, 10, 11, 12, 15A |
| `del_D_delivery.md` | Del D: part_d, kap. 13, 14, 15, 16 |
| `del_E_kap17-19.md` | Del E: part_e, kap. 17, 18, 19 |
| `del_E_kap23-20-21.md` | Del E: kap. 23, 20, 21 |
| `del_F-G_kap22-27.md` | Del F och G: part_f, kap. 22, 24, part_g, 25, 26B, 27 |
| `del_H_bilagor.md` | Del H: part_h, kap. 28, 29, 31, 32, Appendix D, mognadsmodell, kontrollmatris, radarverktyg |
| `bilaga_A_kodexempel.md` | Bilaga A: kap. 30 |
| `kap33_kallforteckning.md` | Kap. 33 med tabell över alla 74 poster |
