<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del B, kapitel 5–6

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, inga ändringar gjorda i repot).

## Omfattning

Lästa filer (varje rad, i sin helhet):

- `docs/part_b_platform.md` (22 rader)
- `docs/05_automation_devops_cicd.md` (593 rader)
- `docs/06_structurizr.md` (1 278 rader)

Stödmaterial som lästs för korskontroll: `docs/33_references.md`, `docs/book_index.json`, `mkdocs.yml`, `BOOK_REQUIREMENTS.md`, `docs/examples/structurizr/*` (DSL, README, manifest, ADR-mapp), `scripts/render_structurizr_diagrams.sh`, `.github/workflows/structurizr-diagrams.yml`, `docs/30_appendix_code_examples.md` (anchors) samt rubrikrader i de kapitel som korsrefereras.

Inventering: cirka 125 kontrollerbara påståenden (statistik/siffror, källhänvisningar, standarder, verktygs- och syntaxpåståenden i kodblock, korsreferenser, URL:er). Cirka 70 av dem verifierades mot primärkällor på webben (officiell Structurizr-dokumentation och källkod, npm-/PyPI-/Docker Hub-register, Thoughtworks Radar-PDF:er Vol. 21/30/31/32, Open Library, Microsoft Learn, GitHub-dokumentation, conftest-källkod, Fowler, gdpr-info.eu, c4model.com m.fl.); resten kontrollerades internt i repot (anchors, filexistens, titlar, numrering).

Begränsningar: GitHub-API via `gh`/MCP var spärrat för externa repon (ersattes med `raw.githubusercontent.com` och Docker Hub); nedladdning/körning av structurizr-cli nekades av sandboxen, så DSL-exemplen har validerats mot språkreferensen och parserkällkoden i stället för genom körning; webbsökbudgeten tog slut efter åtta sökningar; `blog.structurizr.com`, `static.structurizr.com` och Patreon kunde inte nås från sandboxen.

## Sammanfattning

Kapitel 5 är i sin prosa huvudsakligen korrekt (GDPR art. 25, DevOps-historik i stort, pipelineprinciper), men dess kodexempel innehåller flera verktygsfel som en läsare som kopierar dem direkt drabbas av: ett npm-paket som inte existerar (`@swagger-api/swagger-validator`), `conftest verify` använt för att validera konfigurationsfiler (kommandot kör Rego-enhetstester), `pip3 install terrascan` som installerar ett övergivet Python-verktyg från 2020, och ett Infracost-installationssteg som flyttar en fil från en sökväg där den aldrig hamnar. Källapparaten i kapitel 5 har allvarliga brister: Thoughtworks-blippen "Governance as Code" finns inte som Radar-teknik (konceptet nämns bara i temattext i Vol. 21), källan "Architecture as Code: The Next Evolution" (Thoughtworks 2024) kan inte hittas i någon Radar-volym, Microsoft Learn-titeln "Design multi-stage release pipelines with approvals" finns inte och den riktiga Microsoft-dokumentationen säger motsatsen till det kapitlet hävdar om kodifierade godkännanden, GDPR.eu-länken ger 404 och ISBN för The Site Reliability Workbook är fel.

Kapitel 6 är det mest problematiska. Flera Structurizr DSL-exempel använder syntax som inte finns (deploymentNode inuti en vy, `autoLayout lr rankSeparation 450 columnSeparation 350`, `paperSize`, manuella koordinater med `element webApp 100 100`, `!include` med jokertecken, radslutskommentarer), structurizr-cli anropas med exportformat som den gamla CLI:n aldrig haft (`png`, `structurizr`) och med en versionstagg (2024.03.01) som inte existerar – vilket också gör repots eget `render_structurizr_diagrams.sh` och det beskrivna CI-flödet obrukbara. Produktbilden är föråldrad: Structurizr cloud service har nått end-of-life (30 september 2026), on-premises/CLI/Lite har ersatts av den konsoliderade `structurizr`-distributionen (`local`, `server`, `export`), men kapitlet beskriver fortfarande Cloud och On-Premises som aktuella alternativ. Två av kapitlets källor är fantomer (Structurizr-bloggposten "Documenting Software Architecture with Structurizr" 2022 med termen "diagram decay"; AaC-beskrivningen som tillskrivs FINOS trots att den beskriver ett annat projekt). Delintroduktionen (part_b) innehåller inga sakfel, bara stavnings- och täckningsinkonsekvenser.

## Fynd

### B1-01 Deployment-vy definierad med modellsyntax (deploymentNode/containerInstance inuti views)
- **Fil:rad:** docs/06_structurizr.md:208–224
- **Påstående:** "deployment ecommerce "Production" "DeploymentProduction" { deploymentNode "Customer Device" { containerInstance webApp } deploymentNode "AWS Cloud" { ... } }"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Språkreferensen definierar `deploymentEnvironment <name> {`, `deploymentNode <name> [description] [technology] [tags] [instances] {` och `containerInstance <identifier> ...` som barn till **model**, medan vysyntaxen är `deployment <*|software system identifier> <environment> [key] [description] {` med `include`/`exclude`/`autoLayout` som innehåll (https://docs.structurizr.com/dsl/language). Kokboksexemplet visar mönstret: `development = deploymentEnvironment "Development" { deploymentNode ... }` i modellen och `deployment * development { include * }` i vyerna (https://docs.structurizr.com/dsl/cookbook/deployment-view/). Dessutom finns ingen deployment-miljö "Production" definierad i modellen, så vyn kan inte skapas ens med korrekt syntax.
- **Förslag:** Lägg till `production = deploymentEnvironment "Production" { deploymentNode "Customer Device" { containerInstance webApp } deploymentNode "AWS Cloud" { deploymentNode "ECS Cluster" { containerInstance apiGateway ... } deploymentNode "RDS" { containerInstance database } } }` i `model {}` och ersätt vyn med `deployment ecommerce production "DeploymentProduction" { include * autoLayout }`.

### B1-02 Ogiltig autoLayout-syntax och icke-existerande `paperSize`-nyckelord
- **Fil:rad:** docs/06_structurizr.md:393–397 (används via `!include` på rad 402)
- **Påstående:** "autoLayout lr rankSeparation 450 columnSeparation 350" och "paperSize A3_Landscape"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Språkreferensen: `autoLayout [tb|bt|lr|rl] [rankSeparation] [nodeSeparation]` – "The second property is the separation of ranks in pixels (default: 300), while the third property is the separation of nodes in the same rank in pixels (default: 300)" – parametrarna är positionella heltal, inga nyckelord (https://docs.structurizr.com/dsl/language). Nyckelordet `paperSize` förekommer inte någonstans i språkreferensen (grep i hela sidan ger noll träffar); pappersstorlek sätts i diagramredigeraren och lagras i workspace.json.
- **Förslag:** Skriv `autoLayout lr 450 350` och ta bort `paperSize`-raden (eller förklara att pappersstorlek sätts i `local`/`server`-redigeraren och sparas i workspace.json).

### B1-03 Manuella koordinater via `element <id> x y` finns inte i DSL:n
- **Fil:rad:** docs/06_structurizr.md:1066–1075
- **Påstående:** "# Manual coordinates (x, y) element webApp 100 100 element apiGateway 300 100 element database 500 100"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** I språkreferensen används `element` endast för att definiera egna modellelement (`element <name> [metadata] [description] [tags] {`) och för stilar (`element <tag> {`); det finns ingen syntax för att ange elementpositioner i en vy. Layoutinformation lagras i workspace.json och referensen varnar: "automatically generated view keys are not guaranteed to be stable over time, and you will likely lose manual layout information" (https://docs.structurizr.com/dsl/language). Arbetsflödet för manuell layout är `local` ("provides a way to view diagrams and modify their layout", https://docs.structurizr.com/local), inte DSL-satser.
- **Förslag:** Ersätt alternativ 2 med en beskrivning av det faktiska arbetsflödet: redigera layouten i `local`/`server`-redigeraren och versionshantera den genererade `workspace.json` tillsammans med `workspace.dsl` (så som https://docs.structurizr.com/getting-started/local rekommenderar).

### B1-04 structurizr-cli anropas med exportformat som inte finns (`png`, `structurizr`) och med en obefintlig version (2024.03.01)
- **Fil:rad:** docs/06_structurizr.md:418, 466, 471, 631–633 (samt repots `scripts/render_structurizr_diagrams.sh` som kapitlet beskriver på rad 467–471 och 498–530)
- **Påstående:** "structurizr.sh export -workspace "$workspace" -format structurizr -output "$output_dir"" (418); "Install the Structurizr CLI (version `2024.03.01` or later)" (466); "The script validates the workspace, exports PNG and Structurizr JSON files" (471); "structurizr/cli export ... -f png -o /workspace/preview/" (633)
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Källkoden för den fristående CLI:n vid tagg v2024.03.03 (`src/main/java/com/structurizr/cli/export/ExportCommand.java`) registrerar exakt dessa format: `json`, `theme`, `plantuml`, `plantuml/structurizr`, `plantuml/c4plantuml`, `mermaid`, `dot`, `websequencediagrams`, `ilograph`, `d2` samt fullständigt klassnamn; hjälptexten lyder "Export format: plantuml[/structurizr|c4plantuml]|websequencediagrams|mermaid|dot|ilograph|json|theme|fqcn". Varken `png` eller ett fristående `structurizr` finns (okänt format ger "unknown export format"). Docker Hub listar taggarna `2024.02.22`, `2024.03.02`, `2024.03.03` … `2025.11.09` men ingen `2024.03.01` (https://hub.docker.com/v2/repositories/structurizr/cli/tags). Repots skript använder både `structurizr/cli:2024.03.01` och `-f png,structurizr`, så det beskrivna CI-flödet kan inte köras. Först i den nya konsoliderade `export`-kommandot finns `png`/`svg`, och då "using the Structurizr browser-based renderer" och "currently only available by building from source or using the preview version of the Java .war file" (https://docs.structurizr.com/export, https://docs.structurizr.com/export/png-and-svg).
- **Förslag:** Byt `-format structurizr` till `-format json` (JSON-exporten är Structurizr-workspaceformatet), ta bort `-f png` ur CLI-exemplen eller visa den faktiska vägen (PlantUML/Mermaid-export + rendering, eller nya `export -format png` med dess förbehåll), ange en verklig version (t.ex. `2024.03.03` eller den nya `structurizr/structurizr`-distributionen) och rätta skriptet/README/DSL-egenskapen `structurizr.cli.version` i `docs/examples/structurizr/`.

### B1-05 npm-paketet `@swagger-api/swagger-validator` existerar inte
- **Fil:rad:** docs/05_automation_devops_cicd.md:198, 213
- **Påstående:** "npm install -g @asyncapi/cli @swagger-api/swagger-validator" och "find architecture/applications -name "*.openapi.yml" -exec swagger-validator {} \;"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** npm-registret svarar 404 för `https://registry.npmjs.org/@swagger-api%2Fswagger-validator` (2026-10-30); `@asyncapi/cli` finns (senaste 6.2.2) och `asyncapi validate [SPEC-FILE]` är ett giltigt kommando (https://www.asyncapi.com/docs/tools/cli/usage). Installationssteget misslyckas därmed och hela jobbet faller.
- **Förslag:** Använd ett existerande verktyg, t.ex. `npm install -g @redocly/cli` med `redocly lint <fil>`, eller `@stoplight/spectral-cli` med `spectral lint <fil>`, eller `@apidevtools/swagger-cli` med `swagger-cli validate <fil>`.

### B1-06 `pip3 install terrascan` installerar ett övergivet Python-verktyg från 2020 – och Terrascan är arkiverat
- **Fil:rad:** docs/05_automation_devops_cicd.md:434–439 (jfr 316, 393)
- **Påstående:** "RUN pip3 install \ checkov \ terrascan \ boto3 \ pytest \ requests"
- **Bedömning:** FEL / FÖRÅLDRAT
- **Allvarlighet:** Hög
- **Evidens:** PyPI-paketet `terrascan` är version 0.2.3 (Accurics), senaste release 2020-07-24, "Security best practice static code analysis for terraform" – den gamla Python-implementationen, inte den Go-baserade Terrascan som distribueras som binär/Docker-image (https://pypi.org/pypi/terrascan/json). Tenables Terrascan-repo inleder dessutom sin README med "⚠️ Archived – This project is no longer maintained. The repository is archived and no further updates, issues, or pull requests will be accepted" (https://raw.githubusercontent.com/tenable/terrascan/master/README.md). `checkov` på PyPI är korrekt (3.4.0).
- **Förslag:** Ta bort `terrascan` ur pip-raden. Ersätt Terrascan i tabellerna (rad 316, 393) med ett underhållet verktyg (t.ex. Trivy eller Checkov) och nämn att Terrascan är arkiverat.

### B1-07 `conftest verify` används för att validera konfigurationsfiler – kommandot kör Rego-enhetstester
- **Fil:rad:** docs/05_automation_devops_cicd.md:217, 225, 239, 251
- **Påstående:** "conftest verify --policy policies/gdpr-service-policies.rego architecture/applications/"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** conftest-dokumentationen: `conftest test deployment.yaml` utvärderar indata mot policyer, medan `verify` beskrivs med "You can then use conftest verify to execute them [Rego unit tests] and report on the results" (https://www.conftest.dev/). Källkoden: `Use: "verify <path> [path [...]]"`, `Short: "Verify Rego unit tests"`, beskrivning "This command executes Rego unit tests. Any file with a '_test' postfix and '.rego' extension will be compiled and any Rego tests inside of them will be executed" (https://raw.githubusercontent.com/open-policy-agent/conftest/master/internal/commands/verify.go). Exemplet validerar alltså inga arkitekturfiler.
- **Förslag:** Skriv `conftest test architecture/applications/ --policy policies/gdpr-service-policies.rego` (motsvarande för de övriga tre raderna) och reservera `conftest verify --policy policies/` för ett separat steg som kör policyernas egna enhetstester.

### B1-08 AaC-projektets beskrivning (YAML + plugin-arkitektur) tillskrivs FINOS architecture-as-code
- **Fil:rad:** docs/06_structurizr.md:19 och 1278 (jfr docs/33_references.md:42–43)
- **Påstående:** "The open-source Architecture-as-Code (AaC) project ... an open-source platform for modelling architecture definitions in YAML and automating validation and generation steps, with every capability delivered through discoverable plugins ... (AaC Open Source Project)" – källförteckningen pekar på "FINOS Architecture as Code Project ... https://github.com/finos/architecture-as-code"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** FINOS-repot är Common Architecture Language Model (CALM): "This repository contains the Common Architecture Language Model (CALM) Specification" (https://raw.githubusercontent.com/finos/architecture-as-code/main/README.md); CALM-arkitekturer skrivs i JSON ("trading-system.architecture.json", https://calm.finos.org/). Beskrivningen i kapitlet matchar i stället DevOps-MBSE/AaC: "AaC ... allows a system modeller to define a system in simple yaml" och "plugin: Allows you to easily extend the AaC DSL itself and create tailored aac commands" (https://raw.githubusercontent.com/DevOps-MBSE/AaC/main/README.md) – ett projekt som för närvarande inte tar emot externa bidrag.
- **Förslag:** Antingen byt källa till https://github.com/DevOps-MBSE/AaC (och nämn FINOS/CALM separat som JSON-baserad specifikation), eller skriv om stycket så att det beskriver CALM korrekt. Rätta även posten i `docs/33_references.md`.

### B1-09 Thoughtworks "Governance as Code" finns inte som Radar-teknik; arkivlänken är ogiltig
- **Fil:rad:** docs/05_automation_devops_cicd.md:17
- **Påstående:** "Thoughtworks frames Governance as Code as an architectural responsibility that encodes policy decisions directly into automation ... ([Thoughtworks Technology Radar – Governance as Code](https://web.archive.org/web/2024*/https://www.thoughtworks.com/radar/techniques/governance-as-code) [archived])"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** https://www.thoughtworks.com/radar/techniques/governance-as-code omdirigeras till teknikindexet (/radar/techniques) – blippsidan finns inte. Wayback Machine har ingen ögonblicksbild av adressen (`archive.org/wayback/available` → tomt), och `web.archive.org/web/2024*/…` är en söksyntax, inte en arkiverad sida. Vol. 21 (nov 2019), som `docs/33_references.md` Source [2] anger som ursprung, innehåller inga blippar med namnet; "as code"-blipparna där är "Pipelines for infrastructure as code" (#4) och "Security policy as code" (#15). Begreppet förekommer endast i temattexten: "This topic concerning policy, compliance and governance as code reappeared multiple times in our conversations. We see a natural evolution in the software development ecosystem of increasing automation: continuous integration with automated testing, continuous delivery, infrastructure as code, and now automated governance." (tr_technology_radar_vol_21_en.pdf, s. 3). Formuleringen om "without manual gatekeeping" finns inte i källan.
- **Förslag:** Citera temat i Vol. 21 korrekt ("Thoughtworks Technology Radar Vol. 21, November 2019, tema om automatiserad styrning") med länk till PDF:en https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2019/11/tr_technology_radar_vol_21_en.pdf, återge dess faktiska innehåll och ta bort den ogiltiga arkivlänken.

### B1-10 Fantomkälla: "Thoughtworks (2024). Architecture as Code: The Next Evolution. Technology Radar"
- **Fil:rad:** docs/05_automation_devops_cicd.md:591 (Sources 9; motsvarar Source [1] i docs/33_references.md:7)
- **Påstående:** "**Thoughtworks (2024).** *Architecture as Code: The Next Evolution.* Technology Radar."
- **Bedömning:** FELCITERAT / EJ VERIFIERBART
- **Allvarlighet:** Hög
- **Evidens:** Texten i Technology Radar Vol. 30 (apr 2024), Vol. 31 (okt 2024) och Vol. 32 (apr 2025) innehåller inte strängen "architecture as code" (pdftotext + grep på de officiella PDF:erna). En webbsökning på den exakta titeln gav inga träffar på thoughtworks.com. Källan åberopas dessutom inte någonstans i kapitel 5:s löptext (inga `Source [1]`-anchors) utan dyker bara upp i källistan.
- **Förslag:** Stryk posten ur kapitel 5:s källista. Eftersom Source [1] återanvänds i sex andra kapitel bör författaren antingen hitta den verkliga publikationen (titel, volym, datum, URL) eller ersätta hänvisningen bokomfattande.

### B1-11 Fantomkälla: Brown (2022) "Documenting Software Architecture with Structurizr" och termen "diagram decay"
- **Fil:rad:** docs/06_structurizr.md:51 och 1273 (jfr docs/33_references.md:54–55)
- **Påstående:** "Brown (2022) describes "diagram decay" as the gradual divergence between architecture diagrams and the systems they represent" samt källan "Brown, S. "Documenting Software Architecture with Structurizr." Structurizr Blog, 2022. https://web.archive.org/web/2024*/https://blog.structurizr.com/diagrams-as-code-automation/ [archived]"
- **Bedömning:** FELCITERAT / EJ VERIFIERBART
- **Allvarlighet:** Hög
- **Evidens:** Värden `blog.structurizr.com` går inte att slå upp (ENOTFOUND) och Wayback Machine har inga ögonblicksbilder av vare sig `blog.structurizr.com/` eller den angivna sökvägen (`archive.org/wayback/available` → tomt för båda) – en blogg som funnits hade arkiverats. Webbsökning på Simon Brown + "diagram decay" ger inga träffar; Browns publicerade material ligger på dev.to/simonbrown, structurizr.com och docs.structurizr.com. Idén (diagram som genereras från en modell blir inte inaktuella) finns däremot t.ex. i Browns dev.to-artiklar om Structurizr DSL.
- **Förslag:** Ta bort attributionen "Brown (2022)" och termen inom citattecken, eller ersätt med en verifierbar källa (t.ex. Browns "Getting started with the Structurizr DSL", https://dev.to/simonbrown/getting-started-with-the-structurizr-dsl-34dh, eller https://docs.structurizr.com/as-code) och formulera om som bokens egen slutsats.

### B1-12 Structurizr Cloud och On-Premises beskrivs som aktuella produkter – cloud service har nått end-of-life och on-prem/CLI/Lite är ersatta
- **Fil:rad:** docs/06_structurizr.md:281–283, 1014, 1025, 1036 (även 287, 440, 472)
- **Påstående:** "1. **Structurizr Cloud** - SaaS offering with hosted workspace 2. **Structurizr On-Premises** - Self-hosted installation 3. **Structurizr Lite** ..."; "**Cost** | ✅ Free (Lite) or subscription"; "Dedicated tools (Lite, Cloud)"; "Structurizr Lite/Cloud"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Hög
- **Evidens:** structurizr/lite-README: "Structurizr Lite will not receive any further updates - please migrate to the new consolidated tooling. See Introducing Structurizr vNext and local" (repot är arkiverat, https://raw.githubusercontent.com/structurizr/lite/main/README.md). Dokumentationen beskriver `local` som "equivalent to the previous Structurizr Lite tooling" (gratis, öppen källkod, https://docs.structurizr.com/local) och `server` som "equivalent to the previous Structurizr on-premises installation" med öppen kärna gratis från källkod men licens för färdigbyggda binärer, £300–£2 400/månad beroende på antal användare (https://docs.structurizr.com/server, https://docs.structurizr.com/server/pricing). Cloud-tjänstens dokumentationssida är tom och structurizr.com har inga signup-/pricing-sidor längre (404); enligt Patreon-inlägget "Cloud service end of life announcement" (1 nov 2025, https://www.patreon.com/posts/142577083, återgivet i sökträff – sidan kunde inte öppnas från sandboxen) upphör cloud service 30 september 2026 med sista nyregistrering 31 december 2025. Kapitlet noterar Lite-EOL men inte att Cloud/On-Premises/CLI också ersatts, vilket gör avsnittet internt inkonsekvent.
- **Förslag:** Skriv om "Workspace Types" till dagens tre lägen: `local` (gratis, personligt), `server` (självhostat; öppen kärna gratis, binärer licensierade) och `export`/`static` (statisk HTML-sajt), med not om att cloud service upphörde 2026-09-30. Uppdatera jämförelsetabellerna (rad 1014, 1025, 1036) och Docker-exemplet (rad 291–293) till `docker run -it --rm -p 8080:8080 -v $(pwd)/workspace:/usr/local/structurizr structurizr/structurizr local` (https://docs.structurizr.com/local/quickstart).

### B1-13 Dynamiska vyer refererar relationer som inte finns i modellen, inklusive en förälder→barn-relation
- **Fil:rad:** docs/06_structurizr.md:197–205 och 695–706
- **Påstående:** "customer -> webApp "Places order"", "orderService -> emailService "SendConfirmation()"" (emailService är en komponent i orderService); i mönster 1: "messageBus -> inventoryService "OrderCreated event"", "notificationService -> user "Send confirmation""
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Språkreferensen: "With a dynamic view, you're showing instances of relationships that are defined in the static model" (https://docs.structurizr.com/dsl/language). I exemplen saknar modellen customer→webApp (bara customer→ecommerce), messageBus→inventoryService (bara motsatt riktning) och notificationService→user. Relationen orderService→emailService är dessutom otillåten i kärnan: "Relationships cannot be added between parents and children." (`Model.java`, https://raw.githubusercontent.com/structurizr/structurizr/main/structurizr-core/src/main/java/com/structurizr/model/Model.java). Exemplen kan därför inte renderas som skrivet.
- **Förslag:** Lägg till motsvarande relationer i den statiska modellen (t.ex. `customer -> webApp "Uses"`, `messageBus -> inventoryService "Delivers events to"`, `notificationService -> user "Sends confirmations to"`) och ersätt orderService→emailService med en relation mellan komponenter (t.ex. `orderController -> emailService`), eller scopa den dynamiska vyn till containern `orderService`.

### B1-14 `!include` med jokertecken stöds inte
- **Fil:rad:** docs/06_structurizr.md:1101
- **Påstående:** "!include views/components/*.dsl"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** "!include <file|directory|url> – file: a single local file ...; directory: a local directory containing one or more DSL files ...; url: a HTTPS URL pointing to a single DSL file" (https://docs.structurizr.com/dsl/includes). Inget jokerteckenstöd dokumenteras.
- **Förslag:** Skriv `!include views/components` (hela katalogen inkluderas i filordning).

### B1-15 Radslutskommentarer efter DSL-satser stöds inte
- **Fil:rad:** docs/06_structurizr.md:1061, 1192, 1198, 1206, 1212
- **Påstående:** "autoLayout lr  # left-to-right", "background #FF6B35  # Brand colour", "routing curved  # or: orthogonal, direct"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Parsern känner bara igen kommentarer som börjar raden: `COMMENT_PATTERN = Pattern.compile("^\\s*?(//|#).*$")` (`StructurizrDslParser.java`, https://raw.githubusercontent.com/structurizr/structurizr/main/structurizr-dsl/src/main/java/com/structurizr/dsl/StructurizrDslParser.java); dokumentationen listar enbart hel-radskommentarer `#`, `//` och `/* */` (https://docs.structurizr.com/dsl/basics). `# left-to-right` tolkas som extra tokens (rankSeparation måste vara ett heltal) och ger parsefel.
- **Förslag:** Flytta kommentarerna till egna rader ovanför satserna.

### B1-16 jq-kvalitetsgrinden pekar på en JSON-sökväg som inte finns i Structurizr-formatet
- **Fil:rad:** docs/06_structurizr.md:420–421 (jfr 424–426)
- **Påstående:** "jq -e 'all(.workspace.model.containers[]?.name; test(...))' "$output_dir/workspace.json""
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Structurizr-JSON har ingen toppnyckel `workspace`; containrar ligger under `.model.softwareSystems[].containers[]` (JSON-exporten `-format json` skriver workspace-objektet direkt, https://docs.structurizr.com/export). Eftersom `[]?` ger en tom ström blir `all(...)` alltid `true`, dvs. grinden passerar oavsett namn.
- **Förslag:** `jq -e '[.model.softwareSystems[]?.containers[]?.name] | all(test("^[A-Z][A-Za-z]+( [A-Z][A-Za-z]+)* API$"))' "$output_dir/<workspace>.json"` – och kontrollera att minst ett element finns (`length > 0`).

### B1-17 Docker-action för PlantUML: `$(pwd)` och glob expanderas inte (ingen shell)
- **Fil:rad:** docs/06_structurizr.md:565–567
- **Påstående:** "uses: docker://plantuml/plantuml:latest with: args: -tpng -o $(pwd)/docs/architecture/views docs/architecture/views/*.puml"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** "GitHub passes the args to the container's ENTRYPOINT when the container starts up" och variabelsubstitution sker bara om "your action runs a command shell ... if your entrypoint attribute is set to "sh -c", args will be run in a command shell" (https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions). `$(pwd)` skickas alltså bokstavligt till PlantUML.
- **Förslag:** Använd en relativ utdatakatalog (`-o docs/architecture/views`, arbetskatalogen är GITHUB_WORKSPACE) eller kör PlantUML i ett `run:`-steg med shell.

### B1-18 GitLab-jobbet anropar `structurizr` som inte finns i PATH i `structurizr/cli`-imagen
- **Fil:rad:** docs/06_structurizr.md:584–598 (även bara `structurizr export` på rad 902 och 1079)
- **Påstående:** "image: structurizr/cli:latest ... script: - structurizr validate -w docs/architecture/workspace.dsl"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Imagens Dockerfile packar upp CLI:n till `/usr/local/structurizr-cli` och sätter `ENTRYPOINT ["/usr/local/structurizr-cli/structurizr.sh"]` utan att lägga något `structurizr`-kommando i PATH (https://raw.githubusercontent.com/structurizr/cli/master/Dockerfile). GitLab Runner kör jobbets script via shell och använder inte imagens entrypoint-argument, så `structurizr validate` ger "command not found".
- **Förslag:** Skriv `/usr/local/structurizr-cli/structurizr.sh validate -w ...` (eller sätt `entrypoint: [""]` och anropa skriptet), och använd `rules:` i stället för det äldre `only: changes:`.

### B1-19 Infracost-installationen flyttar binären från en sökväg där den inte finns
- **Fil:rad:** docs/05_automation_devops_cicd.md:446–447
- **Påstående:** "RUN curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh && mv /root/.local/bin/infracost /usr/local/bin/"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Installationsskriptet skriver "Moving /tmp/infracost-$os-$arch to /usr/local/bin/infracost" och kör `mv "/tmp/infracost-$os-$arch" "/usr/local/bin/infracost"` (rad 77–81 i https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh). `/root/.local/bin/infracost` existerar aldrig, så `mv` misslyckas och Docker-bygget avbryts.
- **Förslag:** Ta bort `&& mv /root/.local/bin/infracost /usr/local/bin/`.

### B1-20 tfsec och Terrascan presenteras som aktuella skanningsverktyg
- **Fil:rad:** docs/05_automation_devops_cicd.md:316, 393
- **Påstående:** "Checkov, tfsec, Terrascan" respektive "Static analysis tools such as tflint, Checkov, or Terrascan"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** tfsec-repots beskrivning är "Tfsec is now part of Trivy" och README: "Going forward we want to encourage the tfsec community to transition over to Trivy ... our engineering attention will be directed at Trivy going forward" (https://raw.githubusercontent.com/aquasecurity/tfsec/master/README.md). Terrascan är arkiverat ("This project is no longer maintained", se B1-06).
- **Förslag:** Ersätt tfsec med Trivy (`trivy config`) och Terrascan med ett underhållet alternativ; behåll Checkov och tflint.

### B1-21 Microsoft Learn-källan "Design multi-stage release pipelines with approvals" finns inte – och den riktiga dokumentationen motsäger påståendet om kodifierade godkännanden
- **Fil:rad:** docs/05_automation_devops_cicd.md:356, 363, 369, 370, 382, 387 (Source [12], docs/33_references.md:18 – utan URL)
- **Påstående:** "Azure DevOps, GitLab, and GitHub environment protections allow these checks and approvals to be codified, ensuring architectural stewards have documented sign-off before production releases ([Source [12]])"
- **Bedömning:** FELCITERAT / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Ingen Microsoft Learn-sida med den titeln hittades; närmaste verkliga titlar är "Pipeline deployment approvals - Azure Pipelines" (https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals), "Tutorial: Create a multistage pipeline with Azure DevOps" (https://learn.microsoft.com/en-us/azure/devops/pipelines/process/create-multistage-pipeline) och Learn-modulen "Create a multistage pipeline by using Azure Pipelines". Approvals-sidan säger uttryckligen: "Approvals and other checks aren't defined in the yaml file. Users modifying the pipeline yaml file can't modify the checks performed before start of a stage. Administrators of resources manage checks using the web interface of Azure Pipelines." Påståendet att godkännandena "kodifieras" stöds alltså inte för Azure DevOps (det går via UI/REST-API, ej pipeline-YAML).
- **Förslag:** Byt Source [12] till den verkliga sidan "Pipeline deployment approvals" med URL, och omformulera rad 363 till att miljöskydd konfigureras som plattformsresurser (UI/API/Terraform-provider) medan pipeline-YAML refererar miljön.

### B1-22 GDPR.eu-källan: ogiltig URL och påhittad titel
- **Fil:rad:** docs/05_automation_devops_cicd.md:589 (Source [27], docs/33_references.md:33)
- **Påstående:** "**GDPR.eu (2024).** *GDPR for Organisations: Practical Guide.* GDPR.eu." med URL https://gdpr.eu/for-organizations/
- **Bedömning:** FEL (URL) / TVEKSAMT (titel)
- **Allvarlighet:** Medel
- **Evidens:** `https://gdpr.eu/for-organizations/` svarar 404. Startsidans navigering innehåller ingen sida med titeln "GDPR for Organisations"; befintliga sidor är t.ex. "Everything you need to know about GDPR compliance" (https://gdpr.eu/compliance/) och "GDPR compliance checklist" (https://gdpr.eu/checklist/). Sajten drivs av Proton AG och anger själv att den "is not an official EU Commission or Government resource".
- **Förslag:** Ersätt med en verklig sida och titel (t.ex. GDPR.eu, "GDPR compliance checklist", https://gdpr.eu/checklist/) eller hellre med primärkällan (EUR-Lex, förordning (EU) 2016/679) och ange att GDPR.eu är en privat resurs.

### B1-23 Fel ISBN för The Site Reliability Workbook
- **Fil:rad:** docs/05_automation_devops_cicd.md:354, 381, 387 (Source [8], docs/33_references.md:14)
- **Påstående:** "*The Site Reliability Workbook: Practical Ways to Implement SRE.* O'Reilly Media, 2018. ISBN: 978-1-4920-2974-8"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Open Library registrerar boken med ISBN 9781492029502 / 1492029505, O'Reilly Media, 2018 (https://openlibrary.org/search.json?title=site+reliability+workbook); sökning på 9781492029748 ger noll träffar. (Kontrollsumman för 978-1-4920-2974-8 är giltig men numret tillhör inte denna bok.)
- **Förslag:** Ändra till ISBN 978-1-4920-2950-2 och ange redaktörerna (Beyer, Murphy, Rensin, Kawahara, Thorne).

### B1-24 Kapiteltitlar stämmer inte med book_index.json/mkdocs/BOOK_REQUIREMENTS
- **Fil:rad:** docs/05_automation_devops_cicd.md:1; docs/06_structurizr.md:1
- **Påstående:** "# Automation, DevOps and CI/CD for Architecture as Code" respektive "# Structurizr: Architecture Modelling as Code"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` (kanonisk källa) anger kapitel 5 som "Automation, DevOps and CI/CD for **Infrastructure** as Code" och kapitel 6 som "Structurizr: Architecture **Modeling** as Code" (amerikansk stavning); `mkdocs.yml` rad 19–20 använder "Infrastructure as Code" respektive "Modelling"; `BOOK_REQUIREMENTS.md` rad 57/412 "Modelling". `docs/33_references.md` kallar kapitel 6 "Structurizr and Diagram Automation" (rad 43, 52, 55, 58, 133, 136, 139, 142).
- **Förslag:** Bestäm en titel per kapitel (rimligen filens rubrik: "…for Architecture as Code" och "…Modelling as Code") och synkronisera book_index.json, mkdocs.yml, BOOK_REQUIREMENTS.md och 33_references.md.

### B1-25 Kapitel 5:s källista speglar inte de källor som faktiskt citeras, och 33_references tillskriver kapitlet källor det inte använder
- **Fil:rad:** docs/05_automation_devops_cicd.md:581–593 (jfr 17, 350–387); docs/33_references.md:8, 161–162
- **Påstående:** Källistan innehåller Source [1] (Thoughtworks 2024) och Source [28] (DORA 2023) men inte Source [8], [9], [12] eller Thoughtworks "Governance as Code"/AWS CDK som citeras inline.
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Inline-citat i kapitlet: `Source [5]` (39), `Source [9]` (350, 356), `Source [8]` (354, 381, 387), `Source [12]` (356, 363, 369, 370, 382, 387), Thoughtworks/AWS CDK (17). Ingen inline-hänvisning till `Source [1]` eller `Source [28]` (DORA nämns bara som "DORA-inspired throughput metrics", rad 385). `docs/33_references.md` rad 161–162 anger att IDC:s "Worldwide DevOps Software Tools Forecast, 2023–2027" refereras i kapitel 5, men ordet "IDC" förekommer inte i kapitlet; Source [2] (rad 8) listar inte kapitel 5 trots citatet på rad 17.
- **Förslag:** Bygg om källistan från de faktiska inline-hänvisningarna (lägg till [8], [9], [12] och en korrekt Thoughtworks Vol. 21-post; ta bort [1] och antingen ta bort [28] eller citera DORA-rapporten explicit där DORA-måtten nämns) och rätta "Referenced in"-listorna i 33_references.md.

### B1-26 `include platform` i en container-vy scopad till `platform` är otillåtet; avsnittet "Filtered Views" visar inte filtrerade vyer
- **Fil:rad:** docs/06_structurizr.md:787–810 (särskilt 795)
- **Påstående:** "### Filtered Views ... container platform "ExternalDependencies" { include platform include ->platform-> ..."
- **Bedömning:** FEL / TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** structurizr-core: "The software system in scope cannot be added to a container view." (`ContainerView.java`, https://raw.githubusercontent.com/structurizr/structurizr/main/structurizr-core/src/main/java/com/structurizr/view/ContainerView.java). Structurizr har en egen konstruktion "filtered view": `filtered <baseKey> <include|exclude> <tags> [key] [description]` (https://docs.structurizr.com/dsl/language, https://docs.structurizr.com/dsl/cookbook/filtered-view/); det kapitlet visar är vanliga vyer med include/exclude-uttryck. Uttrycken `element.tag==…`, `element.type==Person` och `->…->` är i sig korrekta (https://docs.structurizr.com/dsl/expressions).
- **Förslag:** Ta bort `include platform`, döp om avsnittet till "Include/exclude expressions" och visa ett riktigt `filtered`-exempel.

### B1-27 Påståendet att CLI-exporten skriver "deterministic coordinates"
- **Fil:rad:** docs/06_structurizr.md:428–429
- **Påstående:** "Because `structurizr.sh export` writes deterministic coordinates, `git diff` highlights when layout templates change or when an element moves."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Vyer med `autoLayout` får sina koordinater av renderaren vid visning, inte av DSL-parsern/CLI:n; JSON-exporten innehåller bara den layout som redan finns i workspace.json (manuell layout från `local`/`server`). Språkreferensen beskriver manuell layout som knuten till vynycklar och lagrad utanför DSL:n (https://docs.structurizr.com/dsl/language; https://docs.structurizr.com/getting-started/local: "Store the workspace.dsl and workspace.json files in version control").
- **Förslag:** Skriv att `workspace.json` (sparad av `local`) versionshanteras tillsammans med DSL:n, och att `git diff` på den visar layoutförändringar.

### B1-28 "Early 2000s" för CI:s rötter i XP
- **Fil:rad:** docs/05_automation_devops_cicd.md:37
- **Påstående:** "The CI/CD concept has roots in Extreme Programming (XP) and the agile movement of the early 2000s."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Fowler: "Continuous Integration was developed as a practice by Kent Beck as part of Extreme Programming in the 1990s" (https://martinfowler.com/articles/continuousIntegration.html; artikelns första version publicerades 10 september 2000). Agile Manifesto är 2001, så "agile movement of the early 2000s" är i sig rätt men XP-rötterna hör till 1990-talet.
- **Förslag:** "...roots in Extreme Programming (XP) in the late 1990s and the agile movement of the early 2000s".

### B1-29 Jenkins-metriker saknar pluginens standardprefix och `match[]` är inte en pluginfunktion
- **Fil:rad:** docs/05_automation_devops_cicd.md:540–548
- **Påstående:** "metrics_path: /prometheus params: match[]: - 'jenkins_builds_duration_milliseconds_summary{job=~".*"}' ..."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Jenkins Prometheus-pluginen exponerar `/prometheus/` med metrikprefix (namespace) "default" som standard ("Prefix of metric (Default: default)", https://plugins.jenkins.io/prometheus/), dvs. `default_jenkins_builds_duration_milliseconds_summary`. `match[]` är en parameter för Prometheus federation-endpoint, inte för Jenkins-pluginen.
- **Förslag:** Ta bort `params: match[]` och använd prefixade metriknamn (eller nämn att prefixet konfigureras via `PROMETHEUS_NAMESPACE`).

### B1-30 Föråldrade pinnade versioner i kodexempel
- **Fil:rad:** docs/05_automation_devops_cicd.md:191, 203, 263, 442; docs/06_structurizr.md:515, 522, 552, 616
- **Påstående:** "actions/checkout@v4", "actions/upload-artifact@v4", "conftest ... v0.46.0"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Aktuella versioner: actions/checkout 7.0.1 och actions/upload-artifact 7.0.2 (`package.json` på main, https://raw.githubusercontent.com/actions/checkout/main/package.json, https://raw.githubusercontent.com/actions/upload-artifact/main/package.json); conftest senaste tagg v0.71.1 (2026-10-06, Docker Hub). `@v4` fungerar fortfarande men ligger tre major-versioner efter; conftest 0.46.0 finns som release (asset-URL svarar 200).
- **Förslag:** Uppdatera till `@v7` (eller skriv "senaste major") och en aktuell conftest-version, alternativt notera i texten att versioner är exempel.

### B1-31 Structurizr Lite beskrivs som "no server required" men startar en lokal webbserver; "Structurizr Local" är inte produktens namn
- **Fil:rad:** docs/06_structurizr.md:283, 287, 296, 380
- **Påstående:** "**Structurizr Lite** - Local viewer for DSL files (free, no server required)" ... "This launches a local web server" ... "readers should use [Structurizr Local]"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Lite-imagen är en Spring Boot-webbapp (`CMD ["java", ... "-jar", "/usr/local/structurizr-lite.war"]`, `EXPOSE ${PORT}`, https://raw.githubusercontent.com/structurizr/lite/main/Dockerfile) – rad 296 säger också "local web server". Ersättaren heter i dokumentationen kommandot `local` i den konsoliderade `structurizr`-distributionen ("the free and open source local command", https://docs.structurizr.com/local), startat med `docker run ... structurizr/structurizr local` (https://docs.structurizr.com/local/quickstart).
- **Förslag:** Skriv "no account or hosted service required" och referera till "the `local` command (Structurizr vNext)".

### B1-32 Länk till DSL-språkreferensen pekar på ett repo som inte längre innehåller parsern
- **Fil:rad:** docs/06_structurizr.md:371, 1275
- **Påstående:** "[Structurizr DSL Language Reference](https://github.com/structurizr/dsl)"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Parserkällkoden ligger numera i monorepot structurizr/structurizr (`structurizr-dsl/src/main/java/com/structurizr/dsl/StructurizrDslParser.java` svarar 200 där, medan motsvarande sökväg i structurizr/dsl svarar 404), och språkreferensen publiceras på https://docs.structurizr.com/dsl/language.
- **Förslag:** Länka till https://docs.structurizr.com/dsl/language (och ev. https://github.com/structurizr/structurizr).

### B1-33 Årtal för "Software Architecture for Developers" skiljer sig mellan kapitlet och referenslistan
- **Fil:rad:** docs/06_structurizr.md:1274 (jfr docs/33_references.md:57)
- **Påstående:** "Brown, S. "Software Architecture for Developers." Leanpub, 2024."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Leanpub-sidan anger "Last updated on 2022-05-28" (https://leanpub.com/software-architecture-for-developers); 33_references skriver "Leanpub, 2022 (continuously updated)".
- **Förslag:** Använd "Leanpub, 2022 (continuously updated)" i båda.

### B1-34 Återgiven workflow avviker från den fil som påstås levereras i repot; "pinned CLI version" är bara en fri egenskap
- **Fil:rad:** docs/06_structurizr.md:458, 498–528
- **Påstående:** "The repository ships with `.github/workflows/structurizr-diagrams.yml`, which performs the following tasks ..." och "Configuration metadata – Pins a minimum Structurizr CLI version so that exports remain reproducible"
- **Bedömning:** INKONSEKVENT / TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Den verkliga filen har dessutom sökvägen `.github/workflows/structurizr-diagrams.yml`, `workflow_dispatch:`, ett namngivet checkout-steg och `if-no-files-found: warn`. DSL-egenskapen `structurizr.cli.version "2024.03.01"` i `configuration { properties {} }` är syntaktiskt tillåten (https://docs.structurizr.com/dsl/language, "Permitted children: scope, visibility, users, properties") men är en fri nyckel/värde-egenskap utan någon verkställande effekt – och värdet pekar på en version som inte finns (se B1-04).
- **Förslag:** Skriv "the workflow below is an abridged version of ..." och beskriv egenskapen som dokumenterande metadata som skriptet läser, inte som en pinning.

### B1-35 Del B-introduktionen: amerikansk stavning och ofullständig innehållsöversikt
- **Fil:rad:** docs/part_b_platform.md:11, 17 (jfr 13–20)
- **Påstående:** "architecture modeling with tools like Structurizr" / "Architecture modeling and visualisation using Structurizr"; punktlistan nämner inte kapitel 8 (Microservices Architecture as Code) som ingår i Del B enligt book_index.json.
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** CLAUDE.md/STYLE_GUIDE kräver brittisk stavning ("modelling"); `docs/book_index.json` placerar kapitel 8 i part_b.
- **Förslag:** Byt till "modelling" och lägg till en punkt om mikrotjänstarkitektur som kod.

### B1-36 Kapitelreferens "Chapter 15" stämmer inte med book_index-identifieraren 15B
- **Fil:rad:** docs/05_automation_devops_cicd.md:487
- **Påstående:** "see [Chapter 15: Cost Optimisation and Resource Management](15_cost_optimization.md)"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `docs/book_index.json` ger filen identifieraren "15B" (Del D) medan "15A" (Evidence as Code) ligger i Del C; filen själv har ingen nummerrubrik. Övriga korsreferenser i kapitlet (3, 7, 9, 9B, 11, 12, 13, 24, 4) stämmer med indexet.
- **Förslag:** Skriv "Chapter 15B" (eller låt bokens numreringsskript avgöra) konsekvent i hela boken.

## Verifierat korrekt (urval)

- GDPR artikel 25 heter "Data protection by design and by default" och punkt 2 kräver att "by default, only personal data which are necessary for each specific purpose of the processing are processed" – kapitel 5 rad 102/118 återger detta korrekt. https://gdpr-info.eu/art-25-gdpr/
- C4-modellens fyra nivåer (System Context, Container, Component, Code) och att kodnivån är "very much an optional level of detail"; titeln "The C4 model for visualising software architecture" (kapitel 6 rad 29–36, 1272). https://c4model.com/ , https://c4model.com/diagrams/code
- Structurizr skapades av Simon Brown och är referensimplementationen för C4 ("Structurizr was created by the author of the C4 model and remains the reference implementation"). https://structurizr.com/
- Thoughtworks Technology Radar "Diagrams as code": oktober 2020 (Vol. 23), ring Trial, nämner Structurizr DSL, PlantUML och WebSequenceDiagrams (kapitel 6 rad 1277). https://www.thoughtworks.com/radar/techniques/diagrams-as-code
- Structurizr Lite är faktiskt utfasat och ersatt av `local` (kapitel 6 rad 283, 380): repot arkiverat, README "will not receive any further updates"; `local` är "equivalent to the previous Structurizr Lite tooling" och gratis/öppen källkod. https://raw.githubusercontent.com/structurizr/lite/main/README.md , https://docs.structurizr.com/local
- DSL-grundsyntax i kapitlet är korrekt: `workspace [name] [description] { model {} views {} configuration {} }`; `person`/`softwareSystem`/`container <name> [description] [technology] [tags]`/`component`; relationer `-> [description] [technology] [tags]` med `{ tags ... }`; `systemContext/container/component <id> [key] [description]`; `dynamic <*|system|container> [key] [description]`; `autoLayout tb|bt|lr|rl`; `include *`, `exclude "element.tag==…"`, `element.type==Person`; `styles { element <tag> { shape person|cylinder|roundedbox, background, colour, fontSize } relationship <tag> { routing orthogonal|curved|direct, thickness } }`; `themes <url>`; `perspectives { <name> <description> [value] }`; `url <url>`; `group <name> {}`; `!docs <path>`, `!adrs <path>`, `!include <file|directory|url>` på workspace-nivå; `configuration { properties { } }`. https://docs.structurizr.com/dsl/language , https://docs.structurizr.com/dsl/expressions , https://docs.structurizr.com/dsl/includes
- Lite-Docker-kommandot (rad 291–293) stämmer med imagens gränssnitt (port 8080, monteringspunkt `/usr/local/structurizr` – samma som `local` använder). https://docs.structurizr.com/local/quickstart , https://raw.githubusercontent.com/structurizr/lite/main/Dockerfile
- `docker run --rm -v $(pwd):/workspace structurizr/cli validate -w /workspace/...` (rad 620–621) är rätt anropsform eftersom imagens ENTRYPOINT är `structurizr.sh`; flaggorna `-workspace/-w`, `-format/-f`, `-output/-o` och kommandot `validate` finns i den fristående CLI:n. https://raw.githubusercontent.com/structurizr/cli/master/Dockerfile , ExportCommand.java (v2024.03.03)
- `terraform -chdir=<dir> init -backend=false` / `validate` (kapitel 5 rad 230–231) är giltig Terraform-syntax; Terraform 1.6.0-arkivet finns. https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
- conftest v0.46.0 release-asset `conftest_0.46.0_Linux_x86_64.tar.gz` finns (HTTP 200). https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz
- `@asyncapi/cli` finns på npm och `asyncapi validate [SPEC-FILE]` är rätt kommando. https://registry.npmjs.org/@asyncapi%2Fcli , https://www.asyncapi.com/docs/tools/cli/usage
- `pip install checkov` är korrekt (checkov 3.4.0 på PyPI). https://pypi.org/pypi/checkov/json
- The Site Reliability Workbook existerar som angivet (O'Reilly, 2018) – bara ISBN är fel. https://openlibrary.org/search.json?title=site+reliability+workbook
- Kent Beck/XP som ursprung för Continuous Integration (kapitel 5 rad 37, bortsett från årtalet). https://martinfowler.com/articles/continuousIntegration.html
- AWS-regionerna `eu-west-1`, `eu-central-1`, `eu-south-1` (rad 130) är alla EU-regioner (Irland, Frankfurt, Milano) – allmänt känt, ej webbverifierat i denna körning.
- Alla URL:er i kapitel 5:s källista utom gdpr.eu svarar 200 (med redirects): jenkins.io/doc/book/pipeline, docs.github.com/en/actions, learn.microsoft.com what-is-azure-pipelines, docs.gitlab.com/ee/ci/ (→ /ci/), developer.hashicorp.com/terraform/language/tests, developer.hashicorp.com/terraform/intro, kubernetes.io/docs/concepts/, dora.dev/research/2023/dora-report/, commission.europa.eu/law/law-topic/data-protection_en. AWS CDK-länken `cdk/latest/guide/home.html` (rad 17) omdirigeras korrekt till `cdk/v2/guide/home.html`.
- Jenkins Prometheus-pluginens standardendpoint är `/prometheus/` (rad 543 använder `/prometheus`). https://plugins.jenkins.io/prometheus/
- GitHub Actions-uttrycket `if: ${{ always() && hashFiles('build/structurizr/**') != '' }}` och `actions/upload-artifact@v4` (rad 521–522) är giltiga och överensstämmer med repots faktiska workflow.
- Anchors `#05_code_1` och `#05_code_3` i `docs/30_appendix_code_examples.md` (rad 30, 423) och bilderna `diagram_07_chapter5.png`, `diagram_05_gantt_timeline.png`, `diagram_06_structurizr_overview.png` finns; `docs/examples/structurizr/` med DSL, README, manifest och tre ADR-filer finns; skripten `render_structurizr_diagrams.sh`, `update_structurizr_manifest.py`, `check_structurizr_manifest.py` och workflowfilen finns (kapitel 6 rad 450–460, 498, 508–509).
- Korsreferenserna till kapitel 3, 4, 7, 9, 9B, 11, 12, 13 och 24 pekar på rätt filer och rubriker enligt book_index.json.
- FINOS architecture-as-code finns och är ett graduerat FINOS-projekt (men beskrivs fel, se B1-08). https://raw.githubusercontent.com/finos/architecture-as-code/main/README.md

## Ej verifierbart

- **Exakt EOL-datum för Structurizr cloud service (30 september 2026) och sista registreringsdag (31 december 2025):** kommer från sökmotorns utdrag av Patreon-inlägget "Cloud service end of life announcement" (1 nov 2025); själva inlägget svarade 403 från sandboxen och structurizr.com/help/changelog är borttagen (404). Att tjänsten är nedlagd/under avveckling stöds indirekt av att docs.structurizr.com/cloud är tom och att signup/pricing-sidorna är borta.
- **Exakt felbeteende för DSL-felen (B1-01, -02, -03, -13, -14, -15):** structurizr-cli kunde inte laddas ned och köras i sandboxen (nedladdning/exekvering av extern binär nekades), så bedömningen bygger på språkreferensen, kokboken och parser-/kärnkällkoden i stället för på körning. Rekommendation: kör `structurizr.sh validate -w` på varje kodblock i kapitel 6 i repots CI (t.ex. extrahera ```structurizr-block till temporära filer).
- **IDC "Worldwide DevOps Software Tools Forecast, 2023–2027":** en sökning hittade bara IDC:s DevSecOps-prognos 2023–2027 (gii.co.jp id1337804) och DevOps-prognosen 2024–2028 (id1555108), inte exakt den citerade titeln; webbsökbudgeten tog slut innan en andra sökning kunde göras. Rapporten citeras dock inte i kapitel 5 (bara felaktigt i 33_references.md, se B1-25).
- **`https://static.structurizr.com/themes/default/theme.json` (kapitel 6 rad 271):** värden är inte nåbar från sandboxen (502/ENOTFOUND), så URL:ens giltighet kunde inte bekräftas. Syntaxen `themes <url>` är korrekt.
- **Jenkins-pluginens exakta metriknamn (rad 546–548):** endast standardprefixet "default" kunde verifieras; pluginens metriklista kunde inte hämtas.
- **Huruvida `[skip ci]` "may bypass mandatory status checks" (kapitel 6 rad 580):** formuleringen är tveksam (hoppade workflows rapporterar inga checks alls) men kontrollerades inte mot GitHub-dokumentationen.
- **Thoughtworks Vol. 21-länken i 33_references.md (`/about-us/news/2019/technology-radar-edition21`):** omdirigeras till nyhetsindexet; posten ligger utanför granskade filer men påverkar Source [2] som kapitel 5 indirekt bygger på.
