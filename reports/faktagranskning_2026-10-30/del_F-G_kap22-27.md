<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del F och G

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, enbart bedömning – inga filer i repot har ändrats).

## Omfattning

Lästa filer (varje rad, i sin helhet):

- `docs/part_f_practices.md` (29 rader)
- `docs/22_documentation_vs_architecture.md` (268 rader)
- `docs/24_best_practices.md` (232 rader)
- `docs/part_g_future.md` (28 rader)
- `docs/25_future_trends.md` (304 rader)
- `docs/26b_aac_anti_patterns.md` (177 rader)
- `docs/27_conclusion.md` (133 rader)

Stödmaterial som lästs för korsreferenser: `docs/book_index.json`, `docs/33_references.md`, samt grep i övriga kapitel (idempotens, observability, OpenTofu/BUSL, ISO 42010, "Chapter 15", MarketsandMarkets/Gartner/IDC).

Inventerade påståenden: cirka 125 (statistik, citeringar, standarder, regelverk, verktyg/kodblock, historik, korsreferenser). Cirka 75 av dem verifierades mot primärkällor via webb (WebSearch/WebFetch/curl, dvs. officiella scheman, pressmeddelanden, standardkataloger, förlagssidor, API-specifikationer). Kodblock (CALM-JSON, Structurizr DSL, PlantUML, Python/Terraform) kontrollerades mot aktuella scheman och leverantörsdokumentation. Alla fem URL:er i kapitel 22 testades med curl. CALM-schemat verifierades genom en sparse clone av `finos/architecture-as-code` samt de publicerade schemafilerna på calm.finos.org (release/1.0, 1.0-rc1/rc2, 1.1, draft/2025-03, draft/2026-03). Electricity Maps-API:et verifierades via dess publika OpenAPI-specifikation (`https://api.electricitymaps.com/v3/openapi.json`) och `/v3/zones`.

Begränsningar: GitHub-webbgränssnittet och Internet Archive är blockerade från granskningsmiljön (därför kunde Structurizr-bloggens arkiverade kopia inte kontrolleras); Google Books-kvoten var uttömd (ISBN kontrollerades i stället via förlagssidor och ISBN-13-kontrollsiffra); IDC:s rapporter ligger bakom betalvägg.

## Sammanfattning

Textens övergripande teknikbeskrivningar (C4-nivåer, Structurizr DSL, PlantUML, Mermaid, NIST:s PQC-standarder FIPS 203/204/205, Quantum Flagship, EuroQCI, Climate Neutral Data Centre Pact, MarketsandMarkets-prognosen, Terraform-argument) är i huvudsak korrekta. De allvarligaste problemen är i stället (1) att kapitel 22:s CALM-exempel inte följer CALM-schemat (relationstyp som sträng, påhittat fält `parties`, protokoll `PostgreSQL` som inte finns i enumerationen) trots att kapitlet lyfter fram just maskinell validering som CALM:s styrka; (2) ett betydande antal käll-poster i kapitel 24, 25 och 26B som inte går att återfinna hos de angivna utgivarna (CNCF, HashiCorp, FinOps Foundation, OPA, McKinsey Global Institute, "MIT Technology Review/MIT Press", IEEE Computer Society, Green Software Foundation) och som därför måste betraktas som fantomcitat eller påhittade titlar; (3) kodexemplet för koldioxidmedveten schemaläggning i kapitel 25 som mappar AWS-regioner till fel länder (eu-west-1 är Irland, inte Frankrike; eu-south-1 är Milano, inte Spanien) och läser ett fält (`renewablePercentage`) som API-ändpunkten inte returnerar; (4) tre felaktiga ISBN i de verk som kapitel 22 och 27 lutar sig mot (Team Topologies, Software Architecture in Practice, Microservices Patterns – samtliga underkänns av ISBN-13-kontrollsiffran). Därtill finns föråldrade formuleringar (AI-förordningen beskrivs som "emerging proposals", ISO/IEC 42010:2011 i stället för 2022-utgåvan, Gartner-siffran 679 mdr USD, Terraform som "open source") och flera interna inkonsekvenser mellan delintroduktionerna, `book_index.json`, slutsatskapitlets sammanfattning och referenslistan.

## Fynd

### FG-01 CALM-exemplet följer inte CALM-schemat (ogiltig relation och protokoll)
- **Fil:rad:** docs/22_documentation_vs_architecture.md:61-87 (särskilt rad 80-82)
- **Påstående:** `"relationship-type": "connects", "parties": ["payment-service", "payment-db"], "protocol": "PostgreSQL"` (presenterat som "Example CALM definition" och i texten som något som kan "Validated automatically", rad 55)
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** I CALM:s kärnschema (både `https://calm.finos.org/release/1.0/meta/core.json` och aktuellt `draft/2026-03/meta/core.json`, samt klonat repo `finos/architecture-as-code`, commit 2026-10-29) är `relationship-type` ett **objekt** med exakt en av nycklarna `interacts`, `connects`, `deployed-in`, `composed-of`, `options`; `connects` kräver `source` och `destination` (vardera ett `node-interface`-objekt med `node`). Fältet `parties` existerar inte i schemat. `protocol` är en enumeration: `HTTP, HTTPS, FTP, SFTP, JDBC, WebSocket, SocketIO, LDAP, AMQP, TLS, mTLS, TCP` – "PostgreSQL" skulle fallera vid validering. Exemplet saknar också `$schema`-referens. Nod-delen (unique-id, node-type, name, description) är däremot korrekt; `service` och `database` ingår i node-type-enumerationen.
- **Förslag:** Byt relationen till t.ex. `{"unique-id": "payment-service-db-connection", "description": "Payment service connects to database", "relationship-type": {"connects": {"source": {"node": "payment-service"}, "destination": {"node": "payment-db"}}}, "protocol": "JDBC"}` och lägg till `"$schema": "https://calm.finos.org/release/1.0/meta/calm.json"` överst. Kör gärna `calm validate` (FINOS CALM CLI) på exemplet innan tryck.

### FG-02 Fyra källor i kapitel 25 går inte att återfinna (fantomcitat)
- **Fil:rad:** docs/25_future_trends.md:292-294, 299
- **Påstående:** "McKinsey Global Institute. *The Future of Infrastructure.* McKinsey & Company." / "MIT Technology Review. *Quantum Computing and Cryptography.* MIT Press." / "IEEE Computer Society. *Edge Computing and 5G Integration.* IEEE Publications." / "Green Software Foundation. *Carbon-Aware Computing Guidelines.* GSF Documentation."
- **Bedömning:** FELCITERAT (sannolikt fantomkällor)
- **Allvarlighet:** Hög
- **Evidens:** Ingen MGI-rapport med titeln "The Future of Infrastructure" kunde hittas; MGI:s infrastrukturrapporter heter bl.a. "Infrastructure productivity: How to save $1 trillion a year" (2013) och "Bridging global infrastructure gaps" (2016). En rapport med exakt den titeln är AECOM:s (2018) – inte McKinseys. MIT Technology Review ges ut av Technology Review, Inc. (helägt av MIT) – inte av MIT Press (https://en.wikipedia.org/wiki/MIT_Technology_Review; https://news.mit.edu/2005/techreview); ingen publikation "Quantum Computing and Cryptography" kunde identifieras. Ingen IEEE Computer Society-publikation med titeln "Edge Computing and 5G Integration" kunde hittas (sökbudgeten tog slut innan en andra sökning kunde göras – se "Ej verifierbart"). Green Software Foundation publicerar SCI-specifikationen (ISO/IEC 21031:2024), Carbon Aware SDK och "Green Software Patterns" (https://greensoftware.foundation/standards/sci/) – ingen "Carbon-Aware Computing Guidelines". Samtliga fyra poster saknar år och URL, vilket i sig avviker från kapitlets övriga källformat.
- **Förslag:** Stryk posterna eller ersätt med verifierbara verk: t.ex. Green Software Foundation, *Software Carbon Intensity (SCI) Specification*, ISO/IEC 21031:2024, https://sci.greensoftware.foundation/; Green Software Foundation, *Carbon Aware SDK*, https://github.com/Green-Software-Foundation/carbon-aware-sdk; NIST IR 8547 (ipd, nov 2024) för PQC-migrering; ETSI MEC-specifikationer för edge/5G.

### FG-03 Källor i kapitel 24 som inte existerar under angiven titel/utgivare
- **Fil:rad:** docs/24_best_practices.md:227-229
- **Påstående:** "Cloud Native Computing Foundation (2024). *Infrastructure as Code Best Practices.* CNCF." / "HashiCorp (2024). *Terraform Maturity Model.* HashiCorp Documentation." / "FinOps Foundation (2024). *Cloud Financial Management Playbook.* FinOps Foundation."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Ingen CNCF-publikation "Infrastructure as Code Best Practices" kunde hittas (webbsökning gav endast leverantörsbloggar; CNCF:s TAG-whitepapers listar ingen sådan). HashiCorp har ingen sida med titeln "Terraform Maturity Model"; närmast är "Learn Terraform recommended practices" (https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices, ursprungligen 2017/2018) som beskriver "four stages of operational maturity around provisioning", samt HashiCorp Validated Designs "Terraform Operating Guides" (Adopt/Standardize/Scale). FinOps Foundations resurslista (https://www.finops.org/resources/) innehåller ingen "Cloud Financial Management Playbook"; organisationens huvuddokument är "FinOps Framework" och det finns en "US Gov Playbook" (2022). Inga av de tre posterna har URL.
- **Förslag:** Byt till verifierbara källor: HashiCorp, *Terraform recommended practices* (URL ovan) eller *HVD: Terraform Operating Guides*; FinOps Foundation, *FinOps Framework* (https://www.finops.org/framework/); för CNCF, välj ett existerande dokument (t.ex. *CNCF Platforms White Paper*, TAG App Delivery, v1.0 2023) eller stryk.

### FG-04 Fantomkällor i kapitel 26B
- **Fil:rad:** docs/26b_aac_anti_patterns.md:172, 175
- **Påstående:** "FinOps Foundation. *Cloud Cost Management for Sustainable Delivery*. FinOps Foundation, 2024." / "Open Policy Agent Project. *Policy as Code Cookbook*. OPA Community, 2024."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Varken FinOps Foundations resurssida eller webbsökning ger någon publikation "Cloud Cost Management for Sustainable Delivery". OPA-projektet har ingen "Policy as Code Cookbook"; OPA:s dokumentation finns på https://www.openpolicyagent.org/docs och det närmast liknande verket är Jimmy Rays bok *Policy as Code* (O'Reilly, 2024), som inte är ett OPA-projektdokument. Posterna saknar URL.
- **Förslag:** Ersätt med FinOps Foundation, *FinOps Framework* / *State of FinOps 2024* (https://data.finops.org/) och Open Policy Agent, *Documentation* (https://www.openpolicyagent.org/docs) – som redan är bokens Source [10].

### FG-05 Fel mappning AWS-region → land i kodexemplet
- **Fil:rad:** docs/25_future_trends.md:75-80 och 87-92
- **Påstående:** `'eu-west-1': 'FR',       # France` / `'eu-south-1': 'ES',      # Spain` (och `'eu-west-1': {'location': 'Western EU' ...}`), i kod som genererar `provider "aws" { region = "{region}" }`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Enligt AWS:s officiella regionlista (https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html) är `eu-west-1` = Europe (Ireland), `eu-west-3` = Europe (Paris), `eu-south-1` = Europe (Milan, Italien), `eu-south-2` = Europe (Spain). Korrekta är `eu-north-1` = Stockholm (SE) och `eu-central-1` = Frankfurt (DE). Eftersom Terraform-mallen använder region-ID:na som riktiga AWS-regioner blir koldioxiddata för två av fyra regioner hämtade för fel elnät (Frankrikes kärnkraftsdominerade mix i stället för Irlands, Spaniens i stället för Italiens), vilket undergräver exemplets hela syfte. Texten (rad 57) kallar dem "generic EU zone identifiers", men det motsägs av Terraform-utdraget.
- **Förslag:** Använd `'eu-west-1': 'IE'`, `'eu-west-3': 'FR'`, `'eu-south-1': 'IT'`, `'eu-south-2': 'ES'`, `'eu-north-1': 'SE'`, `'eu-central-1': 'DE'` och justera `eu_regions`-tabellen (eller gör exemplet uttryckligen leverantörsneutralt och ta bort AWS-providern).

### FG-06 Electricity Maps-koden läser fält som ändpunkten inte returnerar, använder ogiltig zon och gammal domän
- **Fil:rad:** docs/25_future_trends.md:73, 94, 98, 106-107
- **Påstående:** `self.electricity_maps_api = "https://api.electricitymap.org/v3"` … `zone = zone_mapping.get(region, 'EU')` … `f"{self.electricity_maps_api}/carbon-intensity/latest"` … `'renewable_ratio': data.get('renewablePercentage', 40) / 100`
- **Bedömning:** FEL (tyst fel – koden kör men ger fel resultat)
- **Allvarlighet:** Hög
- **Evidens:** Electricity Maps OpenAPI-specifikation (https://api.electricitymaps.com/v3/openapi.json, "Electricity Maps API" v3.0.0) anger att `GET /carbon-intensity/latest` returnerar fälten `zone, carbonIntensity, datetime, updatedAt, createdAt, emissionFactorType, flowTraced, isEstimated, estimationMethod, temporalGranularity` – **inte** `renewablePercentage`. Det fältet (och `fossilFreePercentage`) returneras av `GET /power-breakdown/latest`. Följden är att `renewable_ratio` alltid blir standardvärdet 0,40 för alla regioner och att viktningen på rad 130-133 i praktiken bara speglar `carbonIntensity`. Zonen `EU` finns inte i `/v3/zones` (351 zoner; `SE`, `FR`, `DE`, `ES`, `IE`, `IT` finns). Specifikationens server-URL är `https://api.electricitymaps.com/v3` (det äldre `api.electricitymap.org` svarar fortfarande men är inte den dokumenterade adressen). Autentiseringsrubriken `auth-token` är korrekt.
- **Förslag:** Hämta `renewablePercentage` från `/power-breakdown/latest` (ett andra anrop) eller ta bort förnybarhetsfaktorn; byt bas-URL till `https://api.electricitymaps.com/v3`; ersätt fallback-zonen `EU` med ett faktiskt zon-ID eller returnera fel.

### FG-07 Tre felaktiga ISBN i de verk som kapitel 22 och 27 lutar sig mot
- **Fil:rad:** docs/27_conclusion.md:129 och 131 (via docs/33_references.md:36 och 38); docs/22_documentation_vs_architecture.md:267 (via docs/33_references.md:126)
- **Påstående:** "Team Topologies … ISBN: 978-1-942788-81-4"; "Software Architecture in Practice (4th ed.) … ISBN: 978-0-13-688580-4"; "Microservices Patterns … ISBN: 978-1-617-29454-1"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Alla tre underkänns av ISBN-13-kontrollsiffran (beräknad kontrollsiffra 2, 1 resp. 9). Korrekta nummer: *Team Topologies* (1:a uppl., IT Revolution 2019) 978-1-942788-81-2 (https://teamtopologies.com/book); *Software Architecture in Practice*, 4th ed. (Addison-Wesley, 3 aug 2021) 978-0-13-688609-9 (https://www.informit.com/store/software-architecture-in-practice-9780136886099); *Microservices Patterns* (Manning, okt 2018) 978-1-617-29454-9 (https://www.manning.com/books/microservices-patterns). Kontrollerat korrekta: *Accelerate* 978-1-942788-33-1 (https://itrevolution.com/product/accelerate/). Observera också att *Team Topologies* kom i 2:a upplaga 23 sep 2025 (ISBN 978-1-966280-00-2).
- **Förslag:** Rätta de tre ISBN i `docs/33_references.md` och överväg att ange 2:a upplagan av *Team Topologies*. Kör `python3 scripts/verify_sources.py` efter rättning.

### FG-08 Gartner-siffran är felattribuerad till "2024 forecast" och numera reviderad
- **Fil:rad:** docs/25_future_trends.md:229 (och källa 15, rad 297)
- **Påstående:** "Gartner's 2024 forecast for public cloud services anticipates worldwide spend of USD 679 billion during 2024"
- **Bedömning:** FELCITERAT / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Siffran 678,8 mdr USD kommer från Gartners pressmeddelande **13 november 2023** (https://www.gartner.com/en/newsroom/press-releases/2023-11-13-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-reach-679-billion-in-20240). Gartners 2024-prognos (20 maj 2024) angav 675,4 mdr USD (https://www.gartner.com/en/newsroom/press-releases/2024-05-20-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-surpass-675-billion-in-2024), och i november 2024 reviderade Gartner 2024-utfallet till 595,7 mdr USD och prognosen för 2025 till 723,4 mdr USD (https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025). Samma formulering finns i docs/15_cost_optimization.md:75.
- **Förslag:** Skriv "Gartner forecast (November 2023) … USD 679 billion in 2024" eller uppdatera till Gartners senaste siffror med datum; samordna med kapitel 15.

### FG-09 ENISA-rapporten är från 2021, inte 2024
- **Fil:rad:** docs/25_future_trends.md:290
- **Påstående:** "ENISA (2024). *Post-Quantum Cryptography: Current State and Quantum Mitigation.*"
- **Bedömning:** FEL (årtal)
- **Allvarlighet:** Medel
- **Evidens:** ENISA:s publikationssida anger titeln "Post-Quantum Cryptography: Current state and quantum mitigation" och publiceringsdatum **3 maj 2021** (https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation).
- **Förslag:** Ändra till "ENISA (2021)" och lägg till URL; överväg att även citera ENISA:s "Post-Quantum Cryptography – Integration study" (2022).

### FG-10 ISO/IEC 42010:2011 är ersatt av ISO/IEC/IEEE 42010:2022
- **Fil:rad:** docs/26b_aac_anti_patterns.md:173
- **Påstående:** "International Organisation for Standardisation. *ISO/IEC 42010:2011 Systems and Software Engineering — Architecture Description*. ISO, 2011."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Standarden är en gemensam ISO/IEC/IEEE-standard; 2011-utgåvan drogs tillbaka och ersattes av ISO/IEC/IEEE 42010:2022 (publicerad november 2022; "This second edition cancels and replaces the first edition (ISO/IEC/IEEE 42010:2011)") – https://www.iso.org/standard/74393.html (iso.org gav 403 från granskningsmiljön; verifierat via SIS- och Standards Council of Canada-kataloger, t.ex. https://www.sis.se/en/produkter/information-technology-office-machines/software-development-and-system-documentation/isoiecieee-420102022). Standarden åberopas dessutom inte någonstans i kapiteltexten.
- **Förslag:** Citera "ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description" eller stryk posten om den inte används.

### FG-11 NCSC-källor med fel titel och/eller årtal
- **Fil:rad:** docs/26b_aac_anti_patterns.md:174; docs/24_best_practices.md:231
- **Påstående:** "National Cyber Security Centre. *Principles for Secure Design*. NCSC, 2023." / "UK National Cyber Security Centre (2023). *Security Principles for Cloud-Hosted Services.* NCSC."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** NCSC:s samling heter "Secure design principles" och publicerades 21 maj 2019 (version 1.0, senast granskad samma datum) – https://www.ncsc.gov.uk/collection/cyber-security-design-principles. Molnvägledningen heter "Cloud security guidance" med sidan "The cloud security principles" (14 principer, version 2.1, granskad 7 juni 2023) – https://www.ncsc.gov.uk/collection/cloud/the-cloud-security-principles.
- **Förslag:** 26B: "NCSC. *Secure design principles* (v1.0). NCSC, 2019." 24: "NCSC. *Cloud security guidance: The cloud security principles* (v2.1). NCSC, 2023." – båda med URL.

### FG-12 Del F-introduktionen räknar in kapitel 23, som enligt index ligger i Del E
- **Fil:rad:** docs/part_f_practices.md:11 och 21
- **Påstående:** "The [soft as code interplay](23_soft_as_code_interplay.md) shows how these seemingly distinct concerns actually reinforce one another." samt punktlistan "How different 'as Code' disciplines create synergies through integration"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` placerar kapitel 23 ("The Interplay Between Soft As Code Disciplines") i `part_e` (Organisation & Leadership); Del F innehåller endast kapitel 22 och 24. Del F-introduktionen presenterar ändå kapitel 23 som en del av "this part" och listar dess innehåll under "What you will learn in this part".
- **Förslag:** Antingen flytta kapitel 23 till Del F i `book_index.json` (och uppdatera kapitel 27:s hänvisning "from Chapter 23") eller skriv om stycket till en bakåthänvisning ("as Chapter 23 in Part E showed …") och ta bort punkten ur lärandelistan.

### FG-13 Del G-introduktionen räknar in kapitel 26A, som enligt index ligger i Del A
- **Fil:rad:** docs/part_g_future.md:11
- **Påstående:** "[Chapter 26A on prerequisites](26a_prerequisites_for_aac.md) describes the cultural, technical, and economic signals …" (presenterat mellan kapitel 25 och 26B som del av Del G)
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` listar 26A under `part_a` (mellan kapitel 1 och 2); Del G består av 25, 26B och 27. Kapitel 26B (rad 5) hänvisar korrekt bakåt ("Before exploring anti-patterns, ensure your organisation has assessed its readiness using the framework in Chapter 26A"), vilket förutsätter att 26A redan lästs.
- **Förslag:** Skriv om stycket som en bakåthänvisning till Del A, eller flytta 26A i index om avsikten är att det ska ligga i Del G.

### FG-14 Slutsatsen hänvisar till "idempotent configuration in chapter 2" – kapitel 2 behandlar inte idempotens
- **Fil:rad:** docs/27_conclusion.md:33-34 (även 110)
- **Påstående:** "from declarative blueprints and idempotent configuration in [chapter 2](02_fundamental_principles.md)" och "The concepts outlined in this book—declarative intent, idempotence, automated testing, and continuous delivery—remain constants"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `grep -i idempoten docs/02_fundamental_principles.md` ger 0 träffar. Ordet förekommer i hela manuskriptet endast i 08_microservices.md (1 gång), 27_conclusion.md (2) och 28_glossary.md (1). Kapitel 2 behandlar däremot "declarative" (7 träffar).
- **Förslag:** Stryk "idempotent configuration" ur hänvisningen till kapitel 2, eller lägg till ett avsnitt om idempotens i kapitel 2 (där det hör hemma som grundprincip) så att slutsatsens sammanfattning stämmer.

### FG-15 AI-förordningen beskrivs som "emerging proposals" trots att den är gällande rätt
- **Fil:rad:** docs/27_conclusion.md:55 (jfr rad 63)
- **Påstående:** "how GDPR, the NIS2 Directive, and emerging AI governance proposals influence design choices"
- **Bedömning:** FÖRÅLDRAT (och internt inkonsekvent med rad 63 "the AI Act's conformity assessment regime")
- **Allvarlighet:** Medel
- **Evidens:** Förordning (EU) 2024/1689 (AI-förordningen) trädde i kraft 1 augusti 2024; förbuden gäller sedan 2 februari 2025, GPAI-reglerna sedan 2 augusti 2025 och förordningen blev i huvudsak tillämplig 2 augusti 2026. Enligt kommissionens sida (https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) antogs "AI Omnibus" 19 nov 2025, nåddes politisk överenskommelse 7 maj 2026 och trädde den i kraft 27 juli 2026 med förlängda tidsfrister för högrisk-AI (bilaga III: 2 december 2027; bilaga I-produkter: 2 augusti 2028).
- **Förslag:** Skriv "the EU AI Act (Regulation (EU) 2024/1689)" och, om tidslinjer nämns, ange de reviderade datumen ovan.

### FG-16 Terraform beskrivs som del av "the open-source ecosystem"
- **Fil:rad:** docs/27_conclusion.md:119
- **Påstående:** "The open-source ecosystem that underpins this discipline—from Terraform and Pulumi to Structurizr and Open Policy Agent—advances because practitioners share …"
- **Bedömning:** FÖRÅLDRAT / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** HashiCorp bytte 10 augusti 2023 licens för Terraform från MPL 2.0 till Business Source License 1.1 (https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license), som inte är en OSI-godkänd open source-licens. Den öppna forken OpenTofu drivs under Linux Foundation (https://opentofu.org/, senaste version 1.13). Manuskriptet nämner varken BUSL eller OpenTofu någonstans (`grep -ri "opentofu\|BUSL" docs/` = 0 träffar). Pulumi (Apache 2.0), OPA (Apache 2.0, CNCF graduated) och Structurizr DSL/CLI (Apache 2.0) är däremot open source.
- **Förslag:** Skriv t.ex. "the open-source and source-available ecosystem … from OpenTofu and Pulumi to Structurizr and Open Policy Agent" eller lägg till en fotnot om Terraforms licensbyte 2023.

### FG-17 Länken till Structurizr DSL-repot är död
- **Fil:rad:** docs/22_documentation_vs_architecture.md:263 (även docs/33_references.md:135)
- **Påstående:** "Structurizr (2024). *Structurizr DSL Language Reference.* … [https://github.com/structurizr/dsl](https://github.com/structurizr/dsl)"
- **Bedömning:** FÖRÅLDRAT (bruten URL)
- **Allvarlighet:** Medel
- **Evidens:** `git ls-remote https://github.com/structurizr/dsl.git` begär autentisering (repot är inte längre publikt tillgängligt), medan `structurizr/java`, `structurizr/structurizr` och `structurizr/cli` svarar utan autentisering. DSL-källkoden ligger numera i modulen `structurizr-dsl` i både `structurizr/java` och det nya samlingsrepot `structurizr/structurizr` (vars README beskriver Structurizr som "a 'models as code' tool designed for the C4 model"). Dokumentationen på https://docs.structurizr.com/dsl länkar till https://github.com/structurizr/structurizr. (Webbläsaråtkomst till github.com var blockerad i granskningsmiljön, så kontrollen gjordes via git.)
- **Förslag:** Byt URL till https://docs.structurizr.com/dsl/language (språkreferensen) och/eller https://github.com/structurizr/structurizr.

### FG-18 Påhittade titlar på EU-källor samt källor utan år/URL
- **Fil:rad:** docs/25_future_trends.md:286, 288 (samt 292-295, 299-304)
- **Påstående:** "European Commission (2024). *EU Quantum Flagship: Bringing Quantum Technologies to Europe.*" / "European Commission (2024). *Post-Quantum Cryptography: Preparing for the Quantum Threat.* EU Cybersecurity Strategy."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Inget EU-dokument med titeln "Bringing Quantum Technologies to Europe" kunde hittas; Flaggskeppets officiella sidor är https://digital-strategy.ec.europa.eu/en/policies/quantum-technologies-flagship och https://qt.eu/. Kommissionens PQC-dokument heter "Commission Recommendation of 11.4.2024 on a Coordinated Implementation Roadmap for the transition to Post-Quantum Cryptography" (C(2024) 2393; https://digital-strategy.ec.europa.eu/en/library/recommendation-coordinated-implementation-roadmap-transition-post-quantum-cryptography), följt av NIS Cooperation Groups "A Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography" (juni 2025). Frasen "preparing for the quantum threat" härrör från 18 medlemsstaters cybersäkerhetsmyndigheters gemensamma uttalande "Securing Tomorrow, Today" (nov 2024) – inte från kommissionen. Källorna 10-13 och 17-22 saknar dessutom helt år och URL.
- **Förslag:** Använd de faktiska titlarna/URL:erna ovan; komplettera alla poster med år och URL i enlighet med STYLE_GUIDE.

### FG-19 Structurizr-bloggposten kan inte verifieras och attribueras felaktigt till kapitel 24
- **Fil:rad:** docs/33_references.md:54-55 (hänvisar till docs/24_best_practices.md); jfr docs/06_structurizr.md:1273
- **Påstående:** "Brown, S. 'Documenting Software Architecture with Structurizr.' Structurizr Blog, 2022. *Referenced in: … Chapter 24: Best Practices*"
- **Bedömning:** EJ VERIFIERBART / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Ingen bloggpost med den titeln kunde hittas; `blog.structurizr.com` svarar inte (HTTP 000/502) och Internet Archive är blockerat från granskningsmiljön. Kapitel 6 anger en arkiv-URL med jokertecken (`web.archive.org/web/2024*/...`) som inte är en giltig direktlänk. Kapitel 24:s källista innehåller inte denna post (och inte heller "Brown, S. C4 Model Overview", som referenslistan också säger refereras i kapitel 24).
- **Förslag:** Ersätt med Simon Browns verifierbara texter, t.ex. "Brown, S. *Diagrams as code 2.0*" (https://dev.to/simonbrown/diagrams-as-code-2-0-2d3o, 2021) eller https://docs.structurizr.com, och rensa "Referenced in"-fälten.

### FG-20 Referenslistan (33_references.md) stämmer inte med kapitlens källistor
- **Fil:rad:** docs/33_references.md:7-8, 10, 16, 20, 51-55, 157-165 i relation till docs/22_…:259-268, docs/24_…:225-232, docs/25_…:281-304, docs/27_…:125-131
- **Påstående:** T.ex. "HashiCorp. *State of Cloud Strategy Survey 2024* … Referenced in: … Chapter 27: Conclusion"; "Gartner … Referenced in: Chapter 15, Chapter 17"; "IDC … Referenced in: Chapter 5, Chapter 21"; Source [14] "Referenced in: Chapter 12, Chapter 15A"; Source [10] rubricerad "Policy as Code Overview" medan kapitel 22 (rad 266) kallar samma källa "Policy as Code: Expressing Requirements as Code"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Kapitel 27 citerar inte HashiCorp-undersökningen alls; kapitel 25 citerar Gartner och IDC men saknas i deras "Referenced in"; kapitel 24 citerar Source [14] men saknas; ingen av kapitel 25:s 22 källor återfinns i referenslistan utom MarketsandMarkets, Gartner och IDC; kapitel 24:s och 26B:s källor saknas helt. Referenslistan innehåller dessutom brutna fillänkar (`26a_future_trends.md`, `20_team_structures.md`, `10_policy_as_code.md`, `32_index.md` – ingen av filerna finns) och påståendet på rad 178 "All citations in the manuscript are included in this compiled list" är därmed inte sant.
- **Förslag:** Generera "Referenced in"-fälten automatiskt från kapitlens källistor, rätta fillänkarna och harmonisera källtitlar (Source [10]).

### FG-21 Figur 24.1 är en platshållare och figurhänvisningen till "seven practice clusters" pekar på fel figur
- **Fil:rad:** docs/24_best_practices.md:7 och 31
- **Påstående:** "*(Note: Figure 24.1, showing an overview of the seven practice clusters, will be inserted in final production.)*" … "Figure 24.2 introduces the seven practice clusters explored throughout this chapter."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Figur 24.2 (rad 11-13) är tankekartan "Code organisation and module design", inte en översikt över sju kluster. Platshållartexten för figur 24.1 får inte följa med till tryck. Bildfilerna `mindmap_22a–22e` och `diagram_22_continuous_improvement.png` finns i `docs/images/`.
- **Förslag:** Skapa översiktsfiguren (eller stryk hänvisningen) och ändra rad 31 till att hänvisa till tabellen/figur 24.1.

### FG-22 "Observability … first introduced in security and resilience chapters" stämmer inte
- **Fil:rad:** docs/27_conclusion.md:43-44
- **Påstående:** "Observability patterns, first introduced in [security and resilience chapters](09_security_fundamentals.md), support data-driven decisions"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Observability behandlas tidigare i kapitel 1 (2 träffar), 5 (7), 7 (3) och 8 (6) innan kapitel 9 (1 träff), enligt grep i kapitelordning.
- **Förslag:** Hänvisa till kapitel 5 (automation/CI/CD) eller 7–8 i stället.

### FG-23 "three primary components" underskattar CALM:s modell
- **Fil:rad:** docs/22_documentation_vs_architecture.md:47-51
- **Påstående:** "It provides a standardised, machine-readable format for defining software architectures through three primary components: Nodes … Relationships … Metadata"
- **Bedömning:** TVEKSAMT (förenkling)
- **Allvarlighet:** Låg
- **Evidens:** Kärnschemats toppnivå har `nodes, relationships, metadata, controls, flows, adrs`; CALM:s referensdokumentation listar kärnbegreppen Nodes, Relationships, Interfaces, Controls, Standards, Flows, Timelines, Decorators, Metadata, Patterns, Widgets (https://calm.finos.org/reference). Controls och flows är centrala för just de "compliance checks" kapitlet lyfter fram.
- **Förslag:** "… built around nodes, relationships, interfaces, controls, flows and metadata" eller "three of its core components".

### FG-24 CALM-källan saknar version; CALM har släppts i version 1.0 och 1.1
- **Fil:rad:** docs/22_documentation_vs_architecture.md:261
- **Påstående:** "FINOS (2024). *CALM: Common Architecture Language Model.* FINOS Architecture as Code Community."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Publicerade scheman finns för `release/1.0`, `release/1.1` samt utkast `draft/2025-03` och `draft/2026-03` (det senare för "CALM 1.3 release" enligt repots README). Projektet är "FINOS incubating" under programmet Architecture as Code, licens Apache-2.0 (https://calm.finos.org/).
- **Förslag:** "FINOS (2025). *CALM – Common Architecture Language Model*, schema release 1.x. FINOS Architecture as Code project. https://calm.finos.org/" och ange vilken schemaversion exemplet följer.

### FG-25 Kapiteltiteln avviker från book_index.json
- **Fil:rad:** docs/24_best_practices.md:1
- **Påstående:** "# Modern Best Practices and Lessons Learned"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `docs/book_index.json` anger titeln "Best Practices and Lessons Learned"; Del F-introduktionen och kapitel 27 använder inte heller "Modern".
- **Förslag:** Harmonisera (ta bort "Modern" eller uppdatera index).

### FG-26 "Chapter 15" saknar bokstavsidentifieraren 15B
- **Fil:rad:** docs/25_future_trends.md:259
- **Påstående:** "Chapter 15 outlines how multi-region design, egress budgeting, and FinOps automation …"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Index-identifieraren för `15_cost_optimization.md` är "15B" (Del D), medan 15A är "Evidence as Code" i Del C. Övriga kapitel (5, 21, 26A) använder dock också "Chapter 15", så felet är systematiskt. Innehållspåståendet stämmer (kapitel 15 rad 65-67 behandlar egress, multi-region och GAIA-X/suveränitet).
- **Förslag:** Besluta en konvention (t.ex. "Chapter 15B") och tillämpa den i hela boken, eller numrera om.

### FG-27 Produktnamn och status för suveräna molnerbjudanden
- **Fil:rad:** docs/25_future_trends.md:261
- **Påstående:** "the EU sovereign offerings of global hyperscalers (AWS European Sovereign Cloud, Azure EU Data Boundary, or Google Cloud Sovereign Controls)"
- **Bedömning:** TVEKSAMT (benämningar) / delvis FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Microsofts erbjudande heter "EU Data Boundary for the Microsoft Cloud" (omfattar Azure, M365, Dynamics 365, Power Platform) och färdigställdes 26 feb 2025 (https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/). Googles erbjudanden heter "Sovereign Controls by Partners" (T-Systems, S3NS) och "Data Boundary". AWS European Sovereign Cloud blev allmänt tillgängligt 14–15 jan 2026 med regionen Brandenburg (`eusc-de-east-1`) (https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe).
- **Förslag:** Använd leverantörernas egna produktnamn och, i en framtidstext, ange att AWS-erbjudandet nu är lanserat.

### FG-28 NIST-listan är korrekt men inte längre komplett
- **Fil:rad:** docs/25_future_trends.md:23-27
- **Påstående:** "NIST has standardised the following post-quantum cryptographic algorithms: ML-KEM (FIPS 203) … ML-DSA (FIPS 204) … SLH-DSA (FIPS 205)"
- **Bedömning:** FÖRÅLDRAT (ofullständigt)
- **Allvarlighet:** Låg
- **Evidens:** De tre standarderna publicerades 13 aug 2024 och rollbeskrivningarna (primär för kryptering, primär för signaturer, backup) stämmer (https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Därefter valde NIST 11 mars 2025 HQC som andra KEM/backup till ML-KEM, med utkast till standard ca 2026 och slutlig standard ca 2027 (https://csrc.nist.gov/News/2025/hqc-announced-as-a-4th-round-selection); FN-DSA (Falcon, planerad FIPS 206) är fortfarande "underway" enligt NIST:s projektsida (uppdaterad 27 okt 2026).
- **Förslag:** Lägg till en mening om HQC (kodbaserad backup-KEM) och FN-DSA för att undvika att listan läses som uttömmande.

### FG-29 IDC-prognosen kunde inte lokaliseras i angiven utgåva
- **Fil:rad:** docs/25_future_trends.md:229, 298
- **Påstående:** "IDC's DevOps Software Tools outlook highlights sustained expansion of automation and platform engineering investment through 2027" / "IDC (2023). *Worldwide DevOps Software Tools Forecast, 2023–2027.*"
- **Bedömning:** EJ VERIFIERBART
- **Allvarlighet:** Låg
- **Evidens:** IDC publicerar serien "Worldwide DevOps Software Tools Forecast" årligen; återförsäljarlistningar visar en DevSecOps-utgåva 2023–2027 (aug 2023) och en DevOps-utgåva 2024–2028 (sep 2024), men ingen listning för exakt "DevOps … 2023–2027" hittades och rapporten ligger bakom betalvägg. Innehållspåståendet (och kapitel 15:s "more than a third of DevOps investment") kan därför inte kontrolleras.
- **Förslag:** Ange IDC-dokumentnummer och datum, eller byt till en öppet tillgänglig källa (t.ex. IDC:s pressmeddelande).

### FG-30 GDS-källans titel finns inte
- **Fil:rad:** docs/26b_aac_anti_patterns.md:177
- **Påstående:** "United Kingdom Government Digital Service. *Service Manual: Technology and Architecture*. GDS, 2024."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Låg
- **Evidens:** GOV.UK Service Manual har avsnittet "Technology" ("Choosing technology, development, integration, hosting, testing, security and maintenance") – inget avsnitt "Technology and Architecture" (https://www.gov.uk/service-manual/technology).
- **Förslag:** "Government Digital Service. *Service Manual – Technology*. GOV.UK. https://www.gov.uk/service-manual/technology".

### FG-31 Richardson och Ford listas som källor utan att åberopas; 1:a upplagan citeras trots 2:a upplagan
- **Fil:rad:** docs/22_documentation_vs_architecture.md:267-268
- **Påstående:** "Richardson, C. (2018). *Microservices Patterns: With Examples in Java.*" / "Ford, N. et al. (2017). *Building Evolutionary Architectures.*"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Kapitlet innehåller inga textcitat till något av verken. *Building Evolutionary Architectures* finns i 2:a upplaga (Ford, Parsons, Kua, Sadalage; O'Reilly, dec 2022; ISBN 978-1-492-09754-9, https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/) med utökat material om fitness functions – det som är relevant för "architectural enforcement". Referenslistans ISBN för 1:a upplagan (978-1-491-98634-9) kunde inte bekräftas hos O'Reilly, vars sidor anger 978-1-491-98636-3 (tryck).
- **Förslag:** Åberopa verken i texten (t.ex. fitness functions i avsnittet om validering) eller stryk dem; uppdatera till 2:a upplagan och kontrollera ISBN.

### FG-32 MarketsandMarkets-prognosen: korrekt siffra men daterad källa
- **Fil:rad:** docs/25_future_trends.md:229, 296
- **Påstående:** "MarketsandMarkets (2023) projects that the Infrastructure as Code market will grow from USD 0.8 billion in 2022 to USD 2.3 billion by 2027—equating to roughly 24 per cent compound annual growth."
- **Bedömning:** FÖRÅLDRAT (siffrorna stämmer)
- **Allvarlighet:** Låg
- **Evidens:** Rapporten (TC 8140) publicerades augusti 2022 och pressmeddelandet med samma siffror (0,8 → 2,3 mdr USD, CAGR 24,0 %) 3 maj 2023 (https://www.marketsandmarkets.com/PressReleases/infrastructure-as-code.asp; https://www.globenewswire.com/news-release/2023/05/03/2660509/0/en/…). Prognoshorisonten 2027 är nu nära och nyare estimat är avsevärt högre.
- **Förslag:** Ange "MarketsandMarkets (2022/2023)" med URL och presentera siffran som historisk prognos.

### FG-33 Dataförvaltningsakten beskrivs som sektorsspecifik
- **Fil:rad:** docs/27_conclusion.md:57-58
- **Påstående:** "sector-specific controls such as DORA for financial services and the European Data Governance Act for cross-border data sharing"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Förordning (EU) 2022/868 (Data Governance Act) är horisontell och reglerar vidareutnyttjande av skyddade offentliga data, dataförmedlingstjänster och dataaltruism – inte sektorsspecifika kontroller för gränsöverskridande datadelning.
- **Förslag:** "… and horizontal frameworks such as the Data Governance Act and the Data Act for data sharing".

### FG-34 CSRD-hänvisningen tar inte hänsyn till Omnibus-ändringarna
- **Fil:rad:** docs/27_conclusion.md:66-68
- **Påstående:** "transparent procurement aligned with the European Green Deal, the Fit for 55 package, and the Corporate Sustainability Reporting Directive"
- **Bedömning:** FÖRÅLDRAT (nyans)
- **Allvarlighet:** Låg
- **Evidens:** "Stop-the-clock"-direktivet (EU) 2025/794 (i kraft 17 apr 2025) sköt upp CSRD-tillämpningen för våg 2 och 3; den provisoriska Omnibus I-överenskommelsen 9 dec 2025 (godkänd av parlamentet 16 dec 2025) begränsar CSRD till företag med >1 000 anställda och >450 MEUR omsättning.
- **Förslag:** Lägg till "as amended by the 2025–2026 Omnibus simplification package" eller formulera neutralt ("EU sustainability-reporting rules").

### FG-35 Climate Neutral Data Centre Pact – formulering och upphovsmän
- **Fil:rad:** docs/25_future_trends.md:51 och 303
- **Påstående:** "the Climate Neutral Data Centre Pact, where leading operators commit to net-zero emissions by 2030" / "Climate Neutral Data Centre Pact. *Self-Regulatory Initiative.* European Data Centre Association."
- **Bedömning:** TVEKSAMT (mindre precision)
- **Allvarlighet:** Låg
- **Evidens:** Pakten (lanserad jan 2021 av CISPE och EUDCA tillsammans med kommissionen) lyder "make data centres climate neutral by 2030", med delmål 2025 (PUE 1,3/1,4; 75 % förnybart/timmatchad fossilfri el) och 2030 (100 %) – https://www.climateneutraldatacentre.net/.
- **Förslag:** Skriv "climate neutral by 2030" och ange "CISPE & EUDCA" som utgivare, med URL.

### FG-36 Terraform-utdraget refererar resurser som inte definieras
- **Fil:rad:** docs/25_future_trends.md:187 och 207
- **Påstående:** `ami           = data.aws_ami.eu_optimised.id` … `autoscaling_group_name = aws_autoscaling_group.carbon_aware.name`
- **Bedömning:** TVEKSAMT (ofullständigt exempel)
- **Allvarlighet:** Låg
- **Evidens:** Varken `data "aws_ami" "eu_optimised"` eller `resource "aws_autoscaling_group" "carbon_aware"` finns i den genererade konfigurationen, så `terraform validate` skulle fallera. Övriga argument är korrekta: `instance_market_options { market_type = "spot" }` (giltiga värden `spot`, `capacity-block`, `interruptible-capacity-reservation`) och `aws_autoscaling_schedule`-argumenten `scheduled_action_name`, `autoscaling_group_name` (obligatoriska), `min_size`, `max_size`, `desired_capacity`, `recurrence` (valfria) enligt AWS-providerns dokumentation (website/docs/r/instance.html.markdown, autoscaling_schedule.html.markdown i hashicorp/terraform-provider-aws).
- **Förslag:** Lägg till de två definitionerna eller markera utdraget som förkortat ("… omitted for brevity").

## Verifierat korrekt (urval)

- C4-modellens fyra nivåer (system context, containers, components, code) och Simon Brown som upphovsman – https://c4model.com/
- Structurizr CLI har kommandona `validate` och `export` (samt push, pull, lock, unlock, merge, inspect, list m.fl.) – https://docs.structurizr.com/cli
- Structurizr DSL: `systemContext <software system identifier> [key] [description] { … }`, `include *`, `autoLayout`, och relationer person → container är tillåtna – https://docs.structurizr.com/dsl/language (DSL-exemplet i kapitel 22 är syntaktiskt korrekt)
- CALM är ett FINOS-projekt (incubating, Apache-2.0) under programmet Architecture as Code; JSON-schemabaserat; relationstyper `interacts`, `connects`, `deployed-in`, `composed-of` – https://calm.finos.org/ och https://calm.finos.org/introduction/what-is-calm
- CALM-nodexemplet (unique-id, node-type `service`/`database`, name, description) uppfyller schemats krav – https://calm.finos.org/release/1.0/meta/core.json
- PlantUML-sekvensdiagrammet i kapitel 22 är giltig syntax; Mermaid är JavaScript-baserat och stöds i GitHub/GitLab – https://mermaid.js.org/, https://plantuml.com/
- URL:erna https://calm.finos.org/, https://c4model.com/, https://mermaid.js.org/, https://plantuml.com/, https://www.openpolicyagent.org/docs svarar HTTP 200
- FIPS 203 (ML-KEM, f.d. CRYSTALS-Kyber), FIPS 204 (ML-DSA, f.d. CRYSTALS-Dilithium), FIPS 205 (SLH-DSA, f.d. SPHINCS+), publicerade 13 aug 2024, med angivna roller – https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- EU Quantum Flagship: lanserat okt 2018, "funded at the 1b € level on a 10-year timescale" – https://qt.eu/about-quantum-flagship/
- EuroQCI: säker kvantkommunikationsinfrastruktur med QKD, alla 27 medlemsstater, mark- och rymdsegment – https://digital-strategy.ec.europa.eu/en/policies/european-quantum-communication-infrastructure-euroqci
- Kommissionens PQC-rekommendation 11 apr 2024 och NIS Cooperation Groups samordnade färdplan (juni 2025; start senast slutet 2026, högriskfall senast 2030) – https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography
- EuroHPC JU: sex värdplatser för kvantdatorer (Tjeckien, Frankrike, Tyskland, Italien, Polen, Spanien) integrerade med befintliga superdatorer – https://eurohpc-ju.europa.eu/one-step-closer-european-quantum-computing-eurohpc-ju-signs-hosting-agreements-six-quantum-computers-2023-06-22_en
- EU Code of Conduct for Energy Efficiency in Data Centres drivs av JRC (sedan 2008) – https://joint-research-centre.ec.europa.eu/scientific-activities-z/energy-efficiency/energy-efficiency-products/code-conduct-ict/european-code-conduct-energy-efficiency-data-centres_en
- MarketsandMarkets: IaC-marknad 0,8 mdr USD (2022) → 2,3 mdr USD (2027), CAGR 24,0 % – https://www.marketsandmarkets.com/PressReleases/infrastructure-as-code.asp
- Gartner 13 nov 2023: 678,8 mdr USD för 2024 (+20,4 %) – TelecomTV:s återgivning av pressmeddelandet, https://www.telecomtv.com/content/digital-platforms-services/gartner-forecasts-worldwide-public-cloud-end-user-spending-to-reach-679-billion-in-2024-48956/
- Thoughtworks Technology Radar Vol 30 publicerades april 2024 (PDF-sökväg 2024/04) och tas fram av Thoughtworks Technology Advisory Board – https://www.thoughtworks.com/en-gb/about-us/events/technology-radar-volume-30-uk
- WEF Global Risks Report 2024 (19:e utgåvan) publicerad 10 jan 2024 – https://www.weforum.org/publications/global-risks-report-2024/
- ISO/IEC 27001:2022 (kapitel 24, Source [14]) – korrekt utgåva
- European Alliance for Industrial Data, Edge and Cloud lanserad 19 juli 2021 – https://digital-strategy.ec.europa.eu/en/policies/cloud-alliance
- Accelerate: Forsgren, Humble & Kim, IT Revolution, 27 mars 2018, ISBN 978-1-942788-33-1 – https://itrevolution.com/product/accelerate/
- Software Architecture in Practice, 4th ed., Addison-Wesley, 3 aug 2021 (årtalet 2021 i kapitel 27 stämmer) – https://www.informit.com/store/software-architecture-in-practice-9780136886099
- Team Topologies, IT Revolution 2019 (årtalet stämmer; ISBN se FG-07) – https://teamtopologies.com/book
- Microservices Patterns, Manning, okt 2018 (årtalet stämmer; ISBN se FG-07) – https://www.manning.com/books/microservices-patterns
- Electricity Maps-API:ets autentiseringsrubrik `auth-token` och zonkoderna SE, FR, DE, ES – https://api.electricitymaps.com/v3/openapi.json, https://api.electricitymaps.com/v3/zones
- Terraform: `instance_market_options.market_type = "spot"` och `aws_autoscaling_schedule`-argumenten (se FG-36) – hashicorp/terraform-provider-aws dokumentation
- HashiCorp BUSL-övergång 10 aug 2023 – https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license
- Alla bildfiler och `docs/examples/structurizr/aac_reference_workspace.dsl` som kapitlen refererar finns i repot

## Ej verifierbart

- **"IEEE Computer Society. *Edge Computing and 5G Integration.*"** (25:294) – webbsökbudgeten för sessionen tog slut innan en riktad sökning kunde göras; inget sådant verk är känt för granskaren och posten saknar år/URL. Behandlas som sannolik fantomkälla (se FG-02) men bör kontrolleras av författaren.
- **IDC "Worldwide DevOps Software Tools Forecast, 2023–2027"** och dess innehållspåstående (25:229, 298) – betalvägg; endast DevSecOps 2023–2027 och DevOps 2024–2028 kunde identifieras via återförsäljare (se FG-29).
- **Brown, S. "Documenting Software Architecture with Structurizr", Structurizr Blog 2022** (33_references:54, hänvisad till kapitel 24) – blog.structurizr.com svarar inte; Internet Archive blockerat i miljön (se FG-19).
- **ISBN 978-1-491-98634-9** för *Building Evolutionary Architectures* (1:a uppl.) – kontrollsiffran är giltig men numret kunde inte bekräftas hos O'Reilly (403 på copyright-sidan); O'Reilly anger 978-1-491-98636-3 för tryckt utgåva (se FG-31).
- **Thoughtworks Radar Vol 30 exakt publiceringsdag** – endast månaden (april 2024) kunde bekräftas; påverkar inte kapitel 26B:s citering.
- **CNCF "Infrastructure as Code Best Practices" (2024)** – inte funnen; kan inte uteslutas att ett internt TAG-dokument avses (se FG-03).
- **Påståenden om AI-Omnibus-datum efter juni 2026** – hämtade från kommissionens webbsida 2026-10-30 och sekundära juridiska källor; bör kontrolleras mot EUT-texten innan de tas in i manuskriptet.

Rekommenderade körningar efter rättning: `python3 scripts/verify_links.py`, `python3 scripts/verify_sources.py`, `python3 -m pytest tests/test_technical_accuracy.py -v`.
