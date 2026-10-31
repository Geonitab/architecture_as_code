<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del A (Foundations)

## Omfattning

**Granskade filer (lästa i sin helhet, rad för rad):**

- `docs/part_a_foundations.md` (21 rader)
- `docs/01_introduction.md` (98 rader)
- `docs/26a_prerequisites_for_aac.md` (136 rader)
- `docs/02_fundamental_principles.md` (604 rader)
- `docs/03_version_control.md` (97 rader)
- `docs/04_adr.md` (295 rader)

Som referensmaterial lästes dessutom `docs/33_references.md` (hela) och `docs/book_index.json` (hela), och övriga kapitel genomsöktes med grep för att kontrollera korsreferenser ("Chapter 14 warns …" osv.).

**Inventering:** cirka 110 påståenden inventerades (statistik, citat/attributioner, standarder och regelverk, verktyg/kommandon/kodexempel, historik och personer, interna korsreferenser, URL:er). Cirka 70 av dem kontrollerades mot primärkällor på webben (WebFetch/curl mot officiell dokumentation, standardiseringsorgan, förlag, GitHub, CNCF, Thoughtworks). 19 URL:er statuskontrollerades med curl. Fem Thoughtworks Technology Radar-PDF:er (vol. 21, 28, 29, 30, 31) och två CNCF-rapporter (Annual Survey 2024; State of Cloud Native Development Q3 2025) laddades ned och genomsöktes i fulltext. Webbsökbudgeten för sessionen tog slut mot slutet av arbetet; de sista kontrollerna gjordes därför uteslutande mot direkta primärkällor (URL:er) och inte via sökmotor.

**Kontrolldatum:** 2026-10-30.

## Sammanfattning

Del A:s faktagrund är svag på källsidan. De fyra källor som bär upp kapitel 1 och 2 argumentativt – Thoughtworks "Architecture as Code: The Next Evolution" (2024), Red Hat "Architecture as Code Principles and Best Practices" (2023), Thoughtworks Radar-blippen "Governance as Code" och CNCF:s "State of Cloud Native Development 2024" med uppgiften att "two thirds of modern organisations already run microservices" – kan inte återfinnas i någon primärkälla; Red Hat-URL:en ger 404 och pekar dessutom på en IaC-artikel, Radar-URL:erna omdirigeras till indexsidan, 2024-upplagan av CNCF-rapporten finns inte på CNCF:s egen webbplats, och den senaste upplagan (Q3 2025) anger 46 % av backend-utvecklarna, inte två tredjedelar av organisationerna. Flera citat i kapitlens källförteckningar har uppfunna eller felaktiga titlar (NIST SP 800-160, IEEE 1012-2016, Atlassian, GitLab, OPA, HashiCorp), ett ISBN pekar på en helt annan bok (Effective Java i stället för Clean Architecture) och Thoughtworks ADR-blipp dateras till 2023 trots att den fanns 2016–2018. På teknisk sida är de viktigaste problemen att Rego-exemplen använder syntax som OPA 1.0 (december 2024) inte längre accepterar, att Python-validatorn inte kan köras som skriven, att CODEOWNERS-exemplet använder ogiltig team-syntax, att ett AWS CLI-kommando saknar obligatorisk parameter, och att GitHub Actions-exemplet bygger på Node 18 (EOL april 2025). Kapitel 26A innehåller ett tiotal hänvisningar till andra kapitel ("Chapter 14 … automation without alignment amplifies chaos", "Chapter 15 … expensive hobby", flera hänvisningar till kapitel 20) som inte har stöd i de kapitlen; de verkar härröra från en tidigare kapitelnumrering. Historiska uppgifter (Nygard 2011, OMG/MDA 2001, Schmidt 2006, Selic 2003 som publikationer, Forsberg & Mooz) är i huvudsak korrekta, med undantag för årtal/forum för Forsberg & Mooz och en övertolkning av Selic 2003.

## Fynd

### A-01 Fantomkälla: Thoughtworks (2024) "Architecture as Code: The Next Evolution"
- **Fil:rad:** docs/01_introduction.md:23, docs/01_introduction.md:29, docs/01_introduction.md:95; docs/02_fundamental_principles.md:596; docs/04_adr.md:214, docs/04_adr.md:232, docs/04_adr.md:293; docs/26a_prerequisites_for_aac.md:134 (samt docs/33_references.md:7 och :144)
- **Påstående:** "Thoughtworks (2024) characterises this discipline as producing *live, executable specifications* that stay synchronised with the running estate rather than lingering as aspirational design artefacts." / "Thoughtworks (2024) warns that this entropy erodes trust, leaving teams to improvise workarounds that bypass architectural guardrails altogether." / "**Thoughtworks (2024).** *Architecture as Code: The Next Evolution.* Technology Radar."
- **Bedömning:** FELCITERAT (fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** Ingen publikation med denna titel kan återfinnas. Thoughtworks Radar har ingen blipp "architecture as code": https://www.thoughtworks.com/radar/techniques/architecture-as-code omdirigeras (HTTP 200 efter redirect) till indexsidan https://www.thoughtworks.com/radar/techniques, medan befintliga blippar (t.ex. .../security-policy-as-code, .../lightweight-architecture-decision-records) svarar på sin egen URL. Fulltextsökning i de två Radar-utgåvorna från 2024 (vol. 30, april 2024: https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2024/04/tr_technology_radar_vol_30_en.pdf; vol. 31, oktober 2024: https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2024/10/tr_technology_radar_vol_31_en.pdf) ger noll träffar på "architecture as code", "executable specification", "slideware" och "architectural entropy". Webbsökning på den exakta titeln ger inga träffar. Källan är dessutom bokens mest använda (Source [1]; åberopas i sju kapitel).
- **Förslag:** Ta bort attributionerna till Thoughtworks eller skriv om till författarens egna påståenden. Om en Thoughtworks-källa önskas, använd verkliga blippar med korrekt volym/datum, t.ex. "Diagrams as code" (Radar vol. 23, oktober 2020, https://www.thoughtworks.com/radar/techniques/diagrams-as-code) eller "Infrastructure as code"; för "executable architecture" kan FINOS CALM/Architecture as Code-projektet (https://calm.finos.org/) eller Structurizr-dokumentationen användas. Uppdatera Source [1] i 33_references.md i alla sju kapitel.

### A-02 Fantomkälla: Red Hat (2023) "Architecture as Code Principles and Best Practices" (adoptability/extensibility/productivity)
- **Fil:rad:** docs/01_introduction.md:35, docs/01_introduction.md:39, docs/01_introduction.md:43, docs/01_introduction.md:98; docs/02_fundamental_principles.md:23, docs/02_fundamental_principles.md:27, docs/02_fundamental_principles.md:31, docs/02_fundamental_principles.md:594 (samt docs/33_references.md:35 och :123)
- **Påstående:** "Red Hat (2023) [Source [29]](33_references.md#source-29) stresses that Architecture as Code succeeds only when teams can adopt it without wholesale tooling upheaval." / "Red Hat recommends treating architecture models as modular building blocks" / "Red Hat notes that this automation-first mindset removes approval bottlenecks"
- **Bedömning:** FELCITERAT (fantomkälla) + FÖRÅLDRAT (bruten URL)
- **Allvarlighet:** Hög
- **Evidens:** Source [29] i 33_references.md pekar på https://www.redhat.com/en/topics/devops/what-is-infrastructure-as-code som ger HTTP 404. Sidan har flyttat till https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac med titeln "What is Infrastructure as Code (IaC)?" – en allmän IaC-förklaring (Ansible-fokus) som inte nämner "Architecture as Code" och inte formulerar några principer om adoptability, extensibility eller productivity. Sidan ligger på redhat.com/topics, inte på Red Hat Developer. Webbsökning efter en Red Hat Developer-artikel om "Architecture as Code" med dessa tre principer ger inga träffar. De tre "Red Hat-principerna" verkar vara författarens egna.
- **Förslag:** Ta bort Red Hat-attributionen i båda kapitlen och presentera adoptability/extensibility/productivity som bokens egna designkriterier. Om Red Hat ska citeras för IaC-grunder: ange korrekt titel "What is Infrastructure as Code (IaC)?", korrekt URL (ovan) och att den handlar om IaC, inte AaC. Rätta Source [29].

### A-03 Fantomblipp: Thoughtworks Technology Radar "Governance as Code" (Source [2])
- **Fil:rad:** docs/03_version_control.md:26, docs/03_version_control.md:33, docs/03_version_control.md:96; docs/26a_prerequisites_for_aac.md:136 (samt docs/33_references.md:8 och :150)
- **Påstående:** "Thoughtworks highlights how Governance as Code requires opinionated policy checks and review automation at the architecture layer … ([Thoughtworks Technology Radar – Governance as Code](https://web.archive.org/web/2024*/https://www.thoughtworks.com/radar/techniques/governance-as-code) [archived])." Source [2]: "Thoughtworks Technology Radar Vol. 21, November 2019 … [blip introduced Vol. 21; archived from techniques listing]"
- **Bedömning:** FELCITERAT (fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** https://www.thoughtworks.com/radar/techniques/governance-as-code omdirigeras till den generella indexsidan https://www.thoughtworks.com/radar/techniques (ingen blipp finns). Radar vol. 21 (november 2019, https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2019/11/tr_technology_radar_vol_21_en.pdf) innehåller i fulltext ingen "Governance as code"; den blipp som finns är "Security policy as code" (Trial, nr 15). Radar vol. 28–31 (2023–2024) innehåller inte heller "governance as code". Nyhetslänken i Source [2] (https://www.thoughtworks.com/about-us/news/2019/technology-radar-edition21) omdirigeras till den generella nyhetssidan. Wayback-URL:en med jokertecken ("/web/2024*/") är en sökvy, inte en arkiverad sida, och är inte en giltig referens. Att hänvisa till Vol. 21/2019 i 33_references men "(2024)" i kapitlens källförteckningar är dessutom inkonsekvent.
- **Förslag:** Ersätt med den verkliga blippen "Security policy as code" (Radar vol. 21, nov 2019, https://www.thoughtworks.com/radar/techniques/security-policy-as-code) om Thoughtworks ska citeras, och anpassa påståendet till vad den säger (policy under versionskontroll, automatisk validering). Ta bort Wayback-jokerlänken. Harmonisera år i 03:96 och 26A:136 med 33_references.

### A-04 Statistiken "two thirds … run microservices" och källan "State of Cloud Native Development 2024"
- **Fil:rad:** docs/01_introduction.md:17, docs/01_introduction.md:96; docs/26a_prerequisites_for_aac.md:135 (samt docs/33_references.md:13)
- **Påstående:** "The Cloud Native Computing Foundation's *State of Cloud Native Development 2024* report notes that two thirds of modern organisations already run microservices in production while simultaneously coordinating event-driven workloads."
- **Bedömning:** FEL (siffra, population och upplaga) / delvis EJ VERIFIERBART (upplagan finns inte)
- **Allvarlighet:** Hög
- **Evidens:** CNCF:s egen webbplats listar upplagorna av SlashData-rapporten "State of Cloud Native Development": Q1 2025 (publ. 25 april 2025, https://www.cncf.io/reports/state-of-cloud-native-development-q1-2025/), Q3 2025 (publ. 11 november 2025, https://www.cncf.io/reports/state-of-cloud-native-development/) och Q1 2026, plus regionala rapporter och äldre 2020–2022-upplagor; ingen upplaga benämnd 2024 finns (kontroll via https://www.cncf.io/lf-report-type/survey/ och CNCF:s sök-API). Rapporten produceras av SlashData för CNCF, inte av CNCF själv. Den senaste upplagan (Q3 2025, PDF https://www.cncf.io/wp-content/uploads/2025/11/cncf_report_stateofcloud_111025a.pdf) anger: "API gateways are the most popular technology, used by 50% of backend developers, with microservices being the leading approach, adopted by 46% of backend developers" och "event-driven architecture (27%)". Populationen är backend-utvecklare, inte organisationer; siffran är 46 %, inte två tredjedelar. CNCF Annual Survey 2024 (publ. 1 april 2025, PDF https://www.cncf.io/wp-content/uploads/2025/04/cncf_annual_survey24_031225a.pdf) innehåller ingen mikrotjänst-procentsats alls. Source [7] saknar URL.
- **Förslag:** Skriv om till t.ex.: "The CNCF/SlashData *State of Cloud Native Development Q3 2025* report finds that 46 % of backend developers work with microservices and 27 % with event-driven architecture" med URL, eller stryk siffran. Rätta Source [7] (titel, upplaga, utgivare SlashData/CNCF, URL) i 33_references.md och i kapitel 1, 7, 8 och 26A. Notera att 26A inte alls refererar till rapporten i löptexten (se A-36).

### A-05 Uppfunnen NIST-titel: "Requirements Engineering for Secure Systems", SP 800-160 (2023)
- **Fil:rad:** docs/02_fundamental_principles.md:601 (samt docs/33_references.md:108)
- **Påstående:** "**NIST (2023).** *Requirements Engineering for Secure Systems.* NIST Special Publication 800-160."
- **Bedömning:** FELCITERAT (fantomtitel, fel år)
- **Allvarlighet:** Hög
- **Evidens:** NIST SP 800-160 Vol. 1 Rev. 1 heter "Engineering Trustworthy Secure Systems" och publicerades november 2022 (https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final). Vol. 2 Rev. 1 heter "Developing Cyber-Resilient Systems: A Systems Security Engineering Approach" (december 2021). Ingen NIST-publikation bär titeln "Requirements Engineering for Secure Systems". Källan åberopas inte heller någonstans i kapitlets löptext.
- **Förslag:** Byt till "NIST (2022). *Engineering Trustworthy Secure Systems.* NIST SP 800-160 Vol. 1 Rev. 1. https://doi.org/10.6028/NIST.SP.800-160v1r1" – eller stryk posten eftersom den inte används i texten. Rätta även 33_references.md.

### A-06 GitLab-källor som inte kan återfinnas (SSOT via CLI/API; "Documentation as Code: Best Practices and Implementation")
- **Fil:rad:** docs/02_fundamental_principles.md:47, docs/02_fundamental_principles.md:597 (samt docs/33_references.md:75 och :78)
- **Påstående:** "GitLab (2024) documents how platform teams expose a hardened command-line interface for everyday contributors, coupling familiar Git flows with guardrail scripts that validate models before merge. The same SSOT repository publishes an API that downstream systems use to synchronise diagrams, catalogues, and service metadata" / "**GitLab (2024).** *Documentation as Code: Best Practices and Implementation.* GitLab Documentation."
- **Bedömning:** FELCITERAT / EJ VERIFIERBART (sannolikt fantomkällor)
- **Allvarlighet:** Hög
- **Evidens:** Varken "Documentation as Code: Best Practices and Implementation" eller "Building a Single Source of Truth with APIs and CLI" (33_references.md:78, "GitLab Topics, 2024") kan återfinnas via webbsökning eller på about.gitlab.com/docs.gitlab.com; båda posterna saknar URL. https://about.gitlab.com/topics/single-source-of-truth/ ger 404. Det som finns är GitLabs blogginlägg "Five fast facts about docs as code at GitLab" (https://about.gitlab.com/blog/five-fast-facts-about-docs-as-code-at-gitlab/, 2022) och "Contribute to the GitLab documentation" (https://docs.gitlab.com/development/documentation/) – ingen av dem beskriver det specifika CLI/API-SSOT-mönstret som attribueras GitLab på rad 47.
- **Förslag:** Skriv om rad 47 utan GitLab-attribution (mönstret är rimligt men är författarens). Ersätt källposten med en verklig, t.ex. GitLab (2022) "Five fast facts about docs as code at GitLab" med URL, eller stryk. Rätta 33_references.md:75 och :78.

### A-07 Rego-exemplen använder syntax som OPA 1.0 inte accepterar
- **Fil:rad:** docs/02_fundamental_principles.md:352–357 och docs/02_fundamental_principles.md:366–371
- **Påstående:** 
  ```
  deny[msg] {
    input.resource_type == "aws_s3_bucket"
    not input.server_side_encryption_configuration
    msg := "S3 bucket must have server-side encryption"
  }
  ```
- **Bedömning:** FÖRÅLDRAT (koden parsar inte i aktuell OPA)
- **Allvarlighet:** Hög
- **Evidens:** OPA 1.0 (GitHub-release v1.0.0 daterad 20 december; releasen är från 2024) gör nyckelorden `if` och `contains` obligatoriska: "OPA v1.0 requires the usage of `if` and `contains` keywords when declaring rules" (https://www.openpolicyagent.org/docs/v0-upgrade); release notes: "using `if` for all rule definitions and `contains` for multi-value rules is now mandatory, not just when using the `rego.v1` import" (https://github.com/open-policy-agent/opa/releases/tag/v1.0.0). Formen `deny[msg] { … }` ger parsefel i OPA ≥ 1.0 om inte `--v0-compatible` används. Kapitel 2 presenterar koden som aktuell utan reservation.
- **Förslag:** Skriv om till v1-syntax: `deny contains msg if { … }` i båda policyerna (och kontrollera samma mönster i kapitel 10, 11, 13 och 23). Lägg gärna till en mening om att OPA 1.0 (dec 2024) ändrade syntaxen.

### A-08 Fel ISBN och trunkerad titel för Clean Architecture
- **Fil:rad:** docs/01_introduction.md:97; docs/02_fundamental_principles.md:595 (samt docs/33_references.md:102)
- **Påstående:** "**Martin, R. (2017).** *Clean Architecture: A Craftsman's Guide to Software Structure.* Prentice Hall. ISBN: 978-0-13-468599-1"
- **Bedömning:** FEL (ISBN tillhör en annan bok)
- **Allvarlighet:** Medel
- **Evidens:** Open Library: ISBN 9780134685991 = *Effective Java* (3:e uppl.), Joshua Bloch, Addison-Wesley Professional, 27 december 2017 (https://openlibrary.org/api/books?bibkeys=ISBN:9780134685991&format=json&jscmd=data). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Robert C. Martin, Pearson/Prentice Hall, 10 september 2017, har ISBN 978-0-13-449416-6 (https://openlibrary.org/api/books?bibkeys=ISBN:9780134494166&format=json&jscmd=data). Titeln saknar "and Design" i kapitel 1 och 2 (fullständig i 33_references). Boken citeras dessutom inte någonstans i löptexten i kapitel 1 eller 2.
- **Förslag:** Ändra till "Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design.* Prentice Hall. ISBN 978-0-13-449416-6" på alla tre ställen – eller stryk posten där den inte används.

### A-09 Thoughtworks ADR-blipp daterad 2023 med fel namn
- **Fil:rad:** docs/04_adr.md:295 (samt docs/33_references.md:147)
- **Påstående:** "**Thoughtworks (2023).** *Architecture Decision Records.* Technology Radar."
- **Bedömning:** FEL (år och titel)
- **Allvarlighet:** Medel
- **Evidens:** Blippen heter "Lightweight Architecture Decision Records" och förekom nov 2016 (Trial), mar 2017 (Trial), nov 2017 (Adopt) och maj 2018 (Adopt); ingen förekomst 2023 (https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records). Fulltextsökning i Radar vol. 28 (april 2023) och vol. 29 (september 2023) ger ingen ADR-blipp; vol. 29 har endast "Design system decision records", som nämner ADR i förbifarten.
- **Förslag:** "Thoughtworks (2017). *Lightweight Architecture Decision Records.* Technology Radar vol. 17 (Adopt), november 2017. https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records". Rätta 33_references.md:147.

### A-10 Atlassian-källan har uppfunnen titel ("Git Workflows for Architecture as Code")
- **Fil:rad:** docs/03_version_control.md:95; docs/02_fundamental_principles.md:84 (samt docs/33_references.md:9)
- **Påstående:** "**Atlassian.** *Git Workflows for Architecture as Code.* Atlassian Git Documentation. [Source [3]]"
- **Bedömning:** FELCITERAT (titel)
- **Allvarlighet:** Medel
- **Evidens:** URL:en https://www.atlassian.com/git/tutorials/comparing-workflows (HTTP 200) är Atlassians handledning "Comparing Workflows" (sidtitel "Git Workflow | Atlassian Git Tutorial"), som jämför Centralized, Feature branch, Gitflow och Forking workflow. Sidan nämner inte Architecture as Code.
- **Förslag:** "Atlassian. *Comparing Workflows* (Git Tutorials). https://www.atlassian.com/git/tutorials/comparing-workflows". Rätta Source [3] i 33_references.md.

### A-11 Fel titel på IEEE 1012-2016; standarden är dessutom ersatt
- **Fil:rad:** docs/02_fundamental_principles.md:603 (samt docs/33_references.md:87)
- **Påstående:** "**IEEE (2017).** *IEEE Standard for Software Verification and Validation.* IEEE Std 1012-2016."
- **Bedömning:** FEL (titel) + FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** IEEE Std 1012-2016 heter "IEEE Standard for System, Software, and Hardware Verification and Validation" (godkänd 2016-05-15, publicerad 2017-09-29) och är ersatt av IEEE 1012-2024 (https://standards.ieee.org/ieee/1012/5609/). Titeln "IEEE Standard for Software Verification and Validation" tillhör de äldre utgåvorna 1012-2004/1012-2012. Standarden åberopas inte i löptexten.
- **Förslag:** "IEEE (2017). *IEEE Standard for System, Software, and Hardware Verification and Validation.* IEEE Std 1012-2016 (superseded by IEEE Std 1012-2024)." Överväg att citera 1012-2024 direkt.

### A-12 Forsberg & Mooz: fel år/forum
- **Fil:rad:** docs/02_fundamental_principles.md:602 (samt docs/33_references.md:72)
- **Påstående:** "**Forsberg, K. & Mooz, H. (1991).** *The Relationship of System Engineering to the Project Cycle.* Engineering Management Journal."
- **Bedömning:** FEL (bibliografiska detaljer)
- **Allvarlighet:** Medel
- **Evidens:** 1991-versionen presenterades vid NCOSE:s första årliga symposium (Chattanooga, 21–23 oktober 1991, Proceedings s. 57–65); tidskriftsversionen publicerades i *Engineering Management Journal* vol. 4, nr 3, september 1992, s. 36–43 (SEBoK: https://sebokwiki.org/wiki/Vee_(V)_Model_(glossary); Wikipedia "Harold Mooz"). Kombinationen "1991" + "Engineering Management Journal" är alltså fel.
- **Förslag:** Antingen "Forsberg, K. & Mooz, H. (1991). The Relationship of System Engineering to the Project Cycle. *Proceedings of the First Annual Symposium of the National Council on Systems Engineering (NCOSE)*, Chattanooga, TN, pp. 57–65" eller "(1992) … *Engineering Management Journal*, 4(3), 36–43".

### A-13 Selic (2003) tillskrivs slutsatser artikeln inte drar
- **Fil:rad:** docs/02_fundamental_principles.md:37, docs/02_fundamental_principles.md:39
- **Påstående:** "Selic (2003) documents how brittle round-trip engineering, tool lock-in, and ambiguous semantics caused MDD artefacts to fall out of sync as soon as teams customised generated code or adopted new frameworks."
- **Bedömning:** FELCITERAT (övertolkning)
- **Allvarlighet:** Medel
- **Evidens:** Selic, B. "The Pragmatics of Model-Driven Development", *IEEE Software* 20(5), sept/okt 2003, s. 19–25, DOI 10.1109/MS.2003.1231146. Abstraktet: "The potential benefits of using models are significantly greater in software than in other engineering disciplines… Unfortunately, models have rarely produced anticipated benefits. The key lies in resolving pragmatic issues related to the artifacts and culture of the previous generation of software technologies." (https://api.openalex.org/works/doi:10.1109/MS.2003.1231146). Artikeln är ett framåtblickande förespråkande av MDD från 2003, inte en dokumentation av hur senare "wider industry adoption" misslyckades; den nämner inte round-trip engineering eller ramverksbyten som orsaker.
- **Förslag:** Skriv om till "Selic (2003) already warned that models 'have rarely produced anticipated benefits' and that success depends on resolving pragmatic tooling and cultural issues", och stöd påståendena om round-trip engineering och tool lock-in med en annan källa (t.ex. France & Rumpe 2007, "Model-driven Development of Complex Software: A Research Roadmap", ICSE FOSE) eller presentera dem som författarens erfarenhet.

### A-14 V-modellen: "NFR → testing, FR → validation" är en icke-standardiserad och missvisande indelning
- **Fil:rad:** docs/02_fundamental_principles.md:461–472, docs/02_fundamental_principles.md:566–574, docs/02_fundamental_principles.md:580–588
- **Påstående:** "**Non-Functional Requirements → Testing**: NFRs are inherently testable through automated metrics and measurements." / "**Functional Requirements → Validation**: … validating that the system solves the correct business problem requires human judgment" / "**Unit Testing** verifies low-level NFRs (code quality, performance of individual components)"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** I IEEE 1012 och SEBoK definieras verifiering ("solved the problem right") och validering ("working the right problem") oberoende av kravtyp; båda tillämpas på funktionella och icke-funktionella krav (https://sebokwiki.org/wiki/System_Verification). I V-modellen enligt Forsberg & Mooz matchar varje dekompositionsnivå sin integrations-/verifieringsnivå (enhetstest mot moduldesign, systemtest mot systemkrav) – inte NFR mot FR. Funktionella krav är dessutom de som oftast automatiseras (enhets-, integrations-, BDD-/acceptanstester), medan många NFR (underhållbarhet, användbarhet, säkerhetskultur) kräver bedömning. Påståendet att enhetstester "verifies low-level NFRs" avviker från gängse definition.
- **Förslag:** Behåll distinktionen "automatiserbar mätning vs. intressentbedömning" men koppla den inte till FR/NFR som kategorier. Formulera t.ex.: "Quantitative requirements (many NFRs, but also precise functional rules) can be verified automatically; requirements that express business intent need stakeholder validation." Justera figur 2.2 och tabellen på rad 566–574 i enlighet med detta.

### A-15 "Personal data must be stored within the EU/EEA" presenteras som GDPR-krav
- **Fil:rad:** docs/02_fundamental_principles.md:359–371
- **Påstående:** "- id: GDPR-001 … description: \"Personal data must be stored within the EU/EEA\" … compliance: [\"GDPR\"]" samt Rego-regeln "RDS instance must be located in an EU region"
- **Bedömning:** TVEKSAMT (juridiskt felaktig förenkling)
- **Allvarlighet:** Medel
- **Evidens:** GDPR innehåller inget krav på datalokalisering. Kapitel V (art. 44–49) reglerar överföringar till tredjeland och tillåter dem vid beslut om adekvat skyddsnivå (art. 45) eller lämpliga skyddsåtgärder (art. 46, t.ex. standardavtalsklausuler); art. 44: överföring får ske "only if … the conditions laid down in this Chapter are complied with" (https://gdpr-info.eu/art-44-gdpr/). Dessutom bygger regeln på `availability_zone` som börjar med "eu-", vilket också matchar t.ex. "eu-west-2" (London, Storbritannien) – ett tredjeland med adekvansbeslut, men inte EU/EES.
- **Förslag:** Märk kravet som organisationens egen policy ("ORG-RES-001: data residency policy – store personal data in EU/EEA regions") med `compliance: ["GDPR Chapter V (transfer restrictions)", "internal data residency policy"]`, och använd en explicit lista över tillåtna regioner i stället för prefixet "eu-".

### A-16 Felaktiga/obefintliga referenser i koden: EDPB Guidelines 07/2020 och "ENISA Information Security Baseline, 2024"
- **Fil:rad:** docs/02_fundamental_principles.md:331–332, docs/02_fundamental_principles.md:385–394, docs/02_fundamental_principles.md:442–445
- **Påstående:** "individual controls reference guidance from the European Data Protection Board (EDPB) alongside ENISA security baselines" / `"reference": "EDPB Guidelines 07/2020"` / `"reference": "ENISA Information Security Baseline, 2024"`
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** EDPB Guidelines 07/2020 heter "Guidelines 07/2020 on the concepts of controller and processor in the GDPR" (version 2.1 antagen 7 juli 2021, https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en) och handlar om rollfördelning, inte om datalokalisering eller kryptering. Ingen ENISA-publikation med titeln "Information Security Baseline" (2024) kan återfinnas i ENISA:s publikationsindex (https://www.enisa.europa.eu/publications); ENISA:s närmaste 2024-material är det tekniska genomförandestödet för NIS2-säkerhetsåtgärder.
- **Förslag:** För dataöverföring: hänvisa till EDPB "Recommendations 01/2020 on measures that supplement transfer tools" eller GDPR art. 44–46. För ISO 27001-kontroller: hänvisa till ISO/IEC 27001:2022 Annex A / ISO/IEC 27002:2022, eller ENISA:s "Technical implementation guidance on cybersecurity risk management measures (NIS2)" (2025) med korrekt titel. Alternativt gör referenserna uttryckligen fiktiva ("example-reference").

### A-17 Python-validatorn kan inte köras och validerar fel sak
- **Fil:rad:** docs/02_fundamental_principles.md:377–403 (särskilt 392–399)
- **Påstående:** 
  ```
  def validate_requirement(self, req_id: str, system_config: dict):
      requirement = self.find_requirement(req_id)
      # Derive OPA data path from the policy package name
      policy_path = req_id.lower().replace("-", "_")
      violation = self._evaluate_policy(policy_path, system_config)
  ```
- **Bedömning:** FEL (kod som inte fungerar)
- **Allvarlighet:** Medel
- **Evidens:** (1) `find_requirement` definieras aldrig i klassen – anropet ger `AttributeError`. (2) Kommentaren säger att sökvägen härleds "from the policy package name", men den härleds från `req_id` ("sec_001"), medan paketen heter `security.s3_encryption` respektive `compliance.data_residency`; OPA:s Data API kräver `POST /v1/data/security/s3_encryption/deny`. (3) För en obefintlig sökväg svarar OPA `200 {}` utan nyckeln `result`, varpå `result.get("result", False)` blir `False` och varje krav rapporteras som "passed" – en tyst falsk-positiv. (4) Parametern `system_config` i `validate_requirement` används men `validate_all_requirements` skickar alltid `self.system_config`; redundans som döljer bugg (2).
- **Förslag:** Lägg till `find_requirement`, härled sökvägen från `package`-raden i policyn (t.ex. regex `^package\s+(\S+)` → ersätt "." med "/" och lägg till "/deny"), och behandla svar utan `result`-nyckel som fel ("policy not loaded") i stället för "passed".

### A-18 CODEOWNERS-exemplet använder ogiltig team-syntax
- **Fil:rad:** docs/02_fundamental_principles.md:61–67 (även docs/02_fundamental_principles.md:112)
- **Påstående:** "/docs/architecture/**          @architecture-team @platform-team"
- **Bedömning:** FEL (syntax)
- **Allvarlighet:** Medel
- **Evidens:** GitHub Docs: "Teams should be identified in the format @org/team-name" och "using the standard `@username` or `@org/team-name` format"; "If you specify a user or team that doesn't exist or has insufficient access, a code owner will not be assigned" (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners). `@architecture-team` tolkas som ett användarnamn; granskningskravet blir aldrig aktivt.
- **Förslag:** Skriv `@acme/architecture-team @acme/platform-team` (eller motsvarande organisationsnamn) och nämn att teamet måste ha skrivrättighet i repot.

### A-19 AWS CLI-kommando saknar obligatorisk parameter; "drift-detection" är inget kommando
- **Fil:rad:** docs/02_fundamental_principles.md:236; docs/02_fundamental_principles.md:78
- **Påstående:** "aws cloudformation describe-stack-drift-detection-status" / "CloudFormation `drift-detection`"
- **Bedömning:** FEL (kommando)
- **Allvarlighet:** Medel
- **Evidens:** `describe-stack-drift-detection-status` har en obligatorisk parameter `--stack-drift-detection-id <value>` (id:t returneras av `detect-stack-drift`); kommandot kan inte köras utan den (https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stack-drift-detection-status.html). AWS CLI-underkommandot heter `detect-stack-drift`, inte `drift-detection`.
- **Förslag:** 
  ```
  DRIFT_ID=$(aws cloudformation detect-stack-drift --stack-name production-stack --query StackDriftDetectionId --output text)
  aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id "$DRIFT_ID"
  ```
  Byt "CloudFormation `drift-detection`" på rad 78 till "CloudFormation `detect-stack-drift`".

### A-20 GitHub Actions-exemplet bygger på Node 18 (EOL) och gamla action-versioner
- **Fil:rad:** docs/02_fundamental_principles.md:283–301
- **Påstående:** "uses: actions/checkout@v4" / "uses: actions/setup-node@v4 … node-version: '18'" / "uses: peaceiris/actions-gh-pages@v3"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Node.js 18 nådde end-of-life 2025-04-30 (https://raw.githubusercontent.com/nodejs/Release/main/schedule.json; aktuella LTS: 20 t.o.m. 2026-04-30, 22 t.o.m. 2027-04-30, 24 t.o.m. 2028-04-30). actions/setup-node har v5.0.0 (4 sept 2025) och senaste v7.1.0; actions/checkout har senaste v7.0.1 (https://github.com/actions/setup-node/releases, https://github.com/actions/checkout/releases). peaceiris/actions-gh-pages v4.0.0 släpptes 8 april 2024 (https://github.com/peaceiris/actions-gh-pages/releases). Boken daterar sig till 2025.10 (BOOK_REQUIREMENTS.md) och kapitlet presenterar exemplet som aktuellt.
- **Förslag:** `node-version: '22'` (eller `'lts/*'`), `actions/checkout@v5`, `actions/setup-node@v5`, `peaceiris/actions-gh-pages@v4` – eller GitHubs egna `actions/upload-pages-artifact` + `actions/deploy-pages`. Överväg en fotnot om att action-versioner bör pinnas till commit-SHA.

### A-21 Structurizr CLI-exemplet: verktyget är arkiverat och flaggsyntaxen avviker från dokumentationen
- **Fil:rad:** docs/02_fundamental_principles.md:129
- **Påstående:** "structurizr-cli export --workspace structurizr/workspace.dsl --format plantuml"
- **Bedömning:** FÖRÅLDRAT (+ Låg: syntax)
- **Allvarlighet:** Medel
- **Evidens:** GitHub-repot structurizr/cli arkiverades 2026-02-04 med meddelandet "The Structurizr CLI will not receive any further updates - please migrate to the new consolidated tooling" (https://github.com/structurizr/cli). Homebrew-formeln `structurizr-cli` (som ger körbara filen `structurizr-cli`) är markerad deprecated med avstängningsdatum 2027-02-17 (https://formulae.brew.sh/formula/structurizr-cli). Den aktuella dokumentationen beskriver det konsoliderade verktyget (binaries v2026.09.19) som körs via `docker run … structurizr/structurizr export …` eller `java -jar structurizr.war export …`, med ensamt bindestreck: `export -workspace workspace.json -format plantuml -output diagrams` (https://docs.structurizr.com/export, https://docs.structurizr.com/binaries). Dubbla bindestreck (`--workspace`) förekommer inte i någon officiell dokumentation.
- **Förslag:** Byt exemplet till det konsoliderade verktyget: `docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr export -workspace structurizr/workspace.dsl -format plantuml -output diagrams`, och lägg till en not om att Structurizr CLI arkiverades i februari 2026. Samordna med kapitel 6.

### A-22 HashiCorp-källan: bruten ankarlänk, uppfunnen titel och påstående som sidan inte stöder
- **Fil:rad:** docs/04_adr.md:224, docs/04_adr.md:242, docs/04_adr.md:294 (samt docs/33_references.md:22)
- **Påstående:** "HashiCorp's guidance on protecting Terraform state demonstrates how surfacing operational controls in dashboards prevents regressions … ([HashiCorp, 2024](33_references.md#hashicorp-securing-terraform-state))" / "**HashiCorp (2024).** *Securing Terraform State.* HashiCorp Developer Documentation. [Source [16]]"
- **Bedömning:** FELCITERAT + bruten länk
- **Allvarlighet:** Medel
- **Evidens:** Ankaret `#hashicorp-securing-terraform-state` finns inte i 33_references.md (ankarna är `#source-1` … `#source-32`); länken är bruten i båda förekomsterna. Source [16]:s URL https://developer.hashicorp.com/terraform/language/state/sensitive-data omdirigeras till https://developer.hashicorp.com/terraform/language/manage-sensitive-data med titeln "Manage sensitive data in your configuration"; sidan handlar om `sensitive`/ephemeral-värden och rekommenderar fjärrlagring, kryptering, åtkomstkontroll och auditloggar. Den nämner inte dashboards, "surfacing operational controls", rotationsscheman eller någon mekanism som "prevents regressions". Titeln "Securing Terraform State" finns inte. 33_references.md:22 anger dessutom att Source [16] bara refereras i kapitel 9 och 9B.
- **Förslag:** Ändra länkarna till `33_references.md#source-16`, rätta titeln till "Manage sensitive data in your configuration" (ny URL), skriv om påståendet till vad sidan faktiskt säger (auditloggar och åtkomstkontroll för state), och lägg till kapitel 4 i "Referenced in".

### A-23 "`adr log`" är inget adr-tools-kommando
- **Fil:rad:** docs/04_adr.md:228 (jfr docs/04_adr.md:171–172)
- **Påstående:** "a chronological view generated via `adr log` that shows proposals, acceptances, and supersessions"
- **Bedömning:** FEL (kommando)
- **Allvarlighet:** Medel
- **Evidens:** adr-tools (npryce) har underkommandona `adr init`, `adr new`, `adr link`, `adr list`, `adr generate` (toc/graph), `adr config`, `adr upgrade-repository`, `adr help` – inget `adr log` (källkatalogen https://github.com/npryce/adr-tools/tree/master/src). Verktyget `adr-log` (npm, adr-organisationen) är ett separat program som genererar ett beslutsregister (TOC), och det är detta rad 172 beskriver.
- **Förslag:** Skriv "generated with `adr-log` (or `adr generate toc`)" och beskriv adr-log som "generates an architecture decision log (index)" snarare än "timeline".

### A-24 Kapitel 26A tillskriver andra kapitel varningar/argument som inte finns där
- **Fil:rad:** docs/26a_prerequisites_for_aac.md:11, docs/26a_prerequisites_for_aac.md:17, docs/26a_prerequisites_for_aac.md:39, docs/26a_prerequisites_for_aac.md:43
- **Påstående:** "The caution covered later in this book in Chapter 14 still stands: automation without alignment amplifies chaos." / "As Chapter 19 argues, narratives anchor change." / "Chapter 15 warns that automation without cost transparency becomes an expensive hobby." / "the surprise budget cuts that destabilised earlier digital initiatives in Chapter 21" / "the burnout scenario warned about in [Chapter 21]"
- **Bedömning:** INKONSEKVENT (interna felattributioner)
- **Allvarlighet:** Medel
- **Evidens:** grep i respektive kapitel: docs/14_practical_implementation.md innehåller varken "amplif", "chaos" eller någon sådan varning; docs/15_cost_optimization.md innehåller inte "hobby" eller "cost transparency" (endast "transparent cost distribution", rad 33); docs/19_management_as_code.md innehåller inte "anchor" och använder "narrative" bara i kontrasten "declarative specifications over narrative documents" (rad 30); docs/21_digitalisation.md innehåller inte "budget", "burnout" eller "heroic". Formuleringarna "Product-centric budgeting from Chapter 19" (rad 39) har visst stöd ("Budgeting as Code") men inte ordalydelsen.
- **Förslag:** Antingen stryk "Chapter N warns/argues"-formuleringarna och skriv påståendena som bokens egna, eller lägg in motsvarande resonemang i kapitel 14, 15, 19 och 21 så att hänvisningarna blir sanna. Kör sedan en konsekvenskontroll av alla "Chapter N …"-hänvisningar i 26A.

### A-25 Inaktuella hänvisningar till "Chapter 20" i kapitel 26A (kapitel 20 är nu "AI Agent Team")
- **Fil:rad:** docs/26a_prerequisites_for_aac.md:5, docs/26a_prerequisites_for_aac.md:19, docs/26a_prerequisites_for_aac.md:32, docs/26a_prerequisites_for_aac.md:35
- **Påstående:** "the organisational narratives in Chapters 17 to 20" / "aligning reward systems and career frameworks with the collaborative ethos described in Chapter 20" / "telemetry, cost analytics, and resilience signals inform architectural decisions in the spirit of Chapter 20" / "Telemetry and feedback channels—highlighted in Chapters 20 and 24"
- **Bedömning:** INKONSEKVENT (stale efter omnumrering)
- **Allvarlighet:** Medel
- **Evidens:** Enligt docs/book_index.json är kapitel 20 "AI Agent Team for Architecture as Code Initiatives" (docs/20_ai_agent_team.md). Kapitlet innehåller inget om belöningssystem, karriärramverk eller feedbackkanaler i organisationen (grep: "reward"/"career" 0 träffar; "telemetry" 1 träff, om testtäckning). docs/33_references.md:10 länkar fortfarande "[Chapter 20](20_team_structures.md)" – en fil som inte finns – vilket visar att kapitel 20 tidigare var ett teamstruktur-kapitel (nu kapitel 18). Hänvisningarna i 26A pekar därmed på fel kapitel.
- **Förslag:** Byt "Chapter 20" till kapitel 18 (teamstruktur/karriär) respektive kapitel 17/19 där det passar, och "Chapters 17 to 20" till "Chapters 17 to 19". Rätta länken i 33_references.md:10.

### A-26 Bokstrukturbeskrivningen i kapitel 1 och kapitelrubriker stämmer inte med book_index.json
- **Fil:rad:** docs/01_introduction.md:71, docs/01_introduction.md:77; docs/02_fundamental_principles.md:43; docs/26a_prerequisites_for_aac.md:5, :11, :39, :104, :112, :124
- **Påstående:** "**Part F: Experience and Best Practices** synthesises lessons learned from real-world implementations, exploring how different \"as Code\" disciplines work together" / "**Part C: Security and Governance**" / "[Chapter 14: Practical Implementation](14_practical_implementation.md)" / "the financial guardrails covered in Chapter 15"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** docs/book_index.json (kanonisk) placerar kapitel 23 "The Interplay Between Soft As Code Disciplines" i Part E, inte Part F (Part F = kap. 22 och 24) – medan kapitel 1 och docs/part_f_practices.md beskriver det som Part F-innehåll (CLAUDE.md säger också 22–24). Part C heter i book_index "Security, Governance & Assurance" (inkl. 15A), i kapitel 1 och part_c_security.md "Security and Governance". Kapitel 14 heter "Architecture as Code in Practice" (book_index, BOOK_REQUIREMENTS.md och filens H1), inte "Practical Implementation". Kostnadskapitlet har identifieraren "15B" i book_index men kallas genomgående "Chapter 15" i 26A (och i kap. 5, 21, 25, 30), medan "15A" (Evidence as Code) ligger i Part C – "Chapter 15" är därmed tvetydigt.
- **Förslag:** Avgör var kapitel 23 ska ligga och synka book_index.json, part_e/part_f-introduktionerna och kapitel 1. Skriv "Chapter 14: Architecture as Code in Practice" och "Chapter 15B" (eller döp om identifieraren till 15). Harmonisera Part C-namnet.

### A-27 Brutna "Referenced in"-länkar i bibliografin för källor som används i Del A
- **Fil:rad:** docs/33_references.md:7, :8, :13 ("[Chapter 26A](26a_future_trends.md)"); :10 ("[Chapter 20](20_team_structures.md)"); :16 ("[Chapter 32](32_index.md)")
- **Påstående:** "Referenced in: … [Chapter 26A](26a_future_trends.md)"
- **Bedömning:** INKONSEKVENT (brutna interna länkar; utanför de granskade filerna men direkt kopplade till deras källförteckningar)
- **Allvarlighet:** Medel
- **Evidens:** Filerna `docs/26a_future_trends.md`, `docs/20_team_structures.md` och `docs/32_index.md` finns inte (ls docs/). Kapitel 26A är "Prerequisites for Architecture as Code Adoption" (`26a_prerequisites_for_aac.md`), kapitel 32 är `32_finos_project_blueprint.md`.
- **Förslag:** Rätta länkmålen; låt `scripts/verify_links.py` köras i CI mot 33_references.md.

### A-28 "Drift scenarios documented earlier in this chapter" – tabellen kommer senare
- **Fil:rad:** docs/02_fundamental_principles.md:55, docs/02_fundamental_principles.md:80, docs/02_fundamental_principles.md:86 (tabellen finns på rad 190–196)
- **Påstående:** "The drift scenarios documented earlier in this chapter—manual configuration changes, emergency patches bypassing governance, knowledge loss through turnover, and fragmented tooling—" / "countering the validation gap identified in the drift causes table"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Avsnittet "Understanding architectural drift" med tabellen "Causes of architectural drift" börjar först på rad 182/190, dvs. efter de tre hänvisningarna.
- **Förslag:** Flytta avsnittet om drift före "Architecture as a single source of truth", eller ändra till "documented later in this chapter (see *Causes of architectural drift*)".

### A-29 OPA-källans titel är uppfunnen och stämmer inte med bibliografin
- **Fil:rad:** docs/02_fundamental_principles.md:599 (jfr docs/33_references.md:16)
- **Påstående:** "**Open Policy Agent (2024).** *Policy as Code: Expressing Requirements as Code.* CNCF OPA Project. [Source [10]]"
- **Bedömning:** INKONSEKVENT / FELCITERAT (titel)
- **Allvarlighet:** Låg
- **Evidens:** Source [10] i 33_references.md heter "Policy as Code Overview" med URL https://www.openpolicyagent.org/docs (HTTP 200). Ingen av titlarna är en faktisk OPA-sida; dokumentationens startsida heter "Introduction"/"OPA Documentation".
- **Förslag:** "Open Policy Agent. *OPA Documentation – Introduction.* https://www.openpolicyagent.org/docs/" i båda filerna.

### A-30 "Terraform Cloud" heter HCP Terraform; ADR-exemplet blandar AaC och IaC
- **Fil:rad:** docs/04_adr.md:137 (jfr docs/04_adr.md:123–127)
- **Påstående:** "Cost for Terraform Cloud or Enterprise features" / "#### ADR-0003: Selection of Terraform for Architecture as Code … Terraform becomes the primary Infrastructure as Code tool"
- **Bedömning:** FÖRÅLDRAT (+ Låg terminologi)
- **Allvarlighet:** Låg
- **Evidens:** HashiCorp: "effective April 22, 2024, Terraform Cloud is now HCP Terraform" (https://developer.hashicorp.com/terraform/enterprise/v202409-1 m.fl.). Rubriken säger "for Architecture as Code" medan beslutet gäller ett IaC-verktyg; kapitel 3 betonar själv att AaC ligger "one abstraction layer above Infrastructure as Code".
- **Förslag:** "Cost for HCP Terraform (formerly Terraform Cloud) or Terraform Enterprise features". Döp om ADR-0003 till "Selection of Terraform as the Infrastructure as Code tool". Överväg att nämna BSL-licensbytet (augusti 2023) och OpenTofu som övervägt alternativ, eftersom det är ett typiskt ADR-övervägande idag.

### A-31 Structurizr beskrivs som "MBSE-aligned tooling"
- **Fil:rad:** docs/02_fundamental_principles.md:39
- **Påstående:** "Modern MBSE-aligned tooling such as Structurizr focuses on keeping a single authoritative architecture model close to the codebase"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Structurizr är verktyg för C4-modellen (mjukvaruarkitekturdiagram ur en modell); MBSE avser systemteknik-modellering (SysML, Cameo, Capella). Structurizrs dokumentation positionerar sig inte som MBSE.
- **Förslag:** "Modern model-based architecture tooling such as Structurizr (C4 model) …".

### A-32 "Commit sign-off" förväxlas med kryptografisk signering
- **Fil:rad:** docs/02_fundamental_principles.md:155
- **Påstående:** "**Automated commit sign-off** via GPG signatures or commit verification, ensuring non-repudiation"
- **Bedömning:** TVEKSAMT (begreppsförväxling)
- **Allvarlighet:** Låg
- **Evidens:** "Sign-off" (`git commit -s`, Developer Certificate of Origin, raden "Signed-off-by:") är en textrad utan kryptografisk betydelse; icke-förnekbarhet kräver signering (`git commit -S`, GPG/SSH/S/MIME) som GitHub sedan markerar "Verified" (GitHub Docs, "About commit signature verification").
- **Förslag:** "**Signed commits** (GPG/SSH signatures with verification), ensuring non-repudiation".

### A-33 k6-tröskeln gäller en taggad delmetrik som ingen request matchar
- **Fil:rad:** docs/02_fundamental_principles.md:507–509 och 513
- **Påstående:** "'http_req_duration{type:api}': ['p(95)<200']," medan anropet är "http.get('https://api.example.com/health')" utan taggar
- **Bedömning:** FEL (exemplet gör inte det som påstås)
- **Allvarlighet:** Låg
- **Evidens:** k6-dokumentationen: "tagged requests create sub-metrics that you can use in thresholds", med exemplet att requests sätter `tags: { type: 'API' }` för att tröskeln `http_req_duration{type:API}` ska gälla dem (https://grafana.com/docs/k6/latest/using-k6/thresholds/). Utan taggen samlar delmetriken inga värden och tröskeln styr inte testets utfall.
- **Förslag:** `http.get('https://api.example.com/health', { tags: { type: 'api' } })` eller använd `'http_req_duration': ['p(95)<200']`.

### A-34 "Including administrators" gäller bara om bypass-skyddet är aktiverat
- **Fil:rad:** docs/02_fundamental_principles.md:69
- **Påstående:** "Protected branch rules enforce these review gates at the Git level, preventing any contributor—including administrators—from bypassing the governance workflow."
- **Bedömning:** TVEKSAMT (överdrift)
- **Allvarlighet:** Låg
- **Evidens:** GitHub Docs: "By default, admins and users with the 'bypass branch protections' permission are exempt" – administratörer omfattas bara om "Do not allow bypassing the above settings" är påslaget (https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
- **Förslag:** "…preventing any contributor from bypassing the workflow, provided the rule's *Do not allow bypassing the above settings* option is enabled so that administrators are included."

### A-35 adr.github.io beskrivs som "official"
- **Fil:rad:** docs/04_adr.md:30
- **Påstående:** "Official guidelines and templates are available at [https://adr.github.io](https://adr.github.io), which serves as the primary resource for ADR methodology."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Webbplatsen beskriver sig som "Homepage of the ADR GitHub organization" (community-drivet; repo adr/adr.github.io) och gör inget anspråk på officiell status; ADR har inget standardiseringsorgan (https://adr.github.io/, HTTP 200).
- **Förslag:** "Community-maintained guidelines and templates (including MADR) are available at https://adr.github.io, the homepage of the ADR GitHub organisation."

### A-36 Källförteckningen i kapitel 26A används inte i texten och har årtalsfel
- **Fil:rad:** docs/26a_prerequisites_for_aac.md:132–136; jfr docs/03_version_control.md:96
- **Påstående:** "1. **Thoughtworks (2024).** *Architecture as Code: The Next Evolution.* … 2. **Cloud Native Computing Foundation (2024).** *State of Cloud Native Development 2024.* … 3. **Thoughtworks Technology Radar (2024).** *Governance as Code.*"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Ingen av de tre källorna åberopas i kapitlets löptext (kapitlet refererar enbart till andra kapitel). Post 3 anger 2024 medan Source [2] i 33_references.md anger "Vol. 21, November 2019" (samma avvikelse i 03:96). Dessutom gäller A-01, A-03 och A-04 för posternas existens.
- **Förslag:** Ta bort källförteckningen i 26A eller ersätt med källor som faktiskt stöder kapitlets påståenden (t.ex. Forsgren/Humble/Kim *Accelerate* för DORA-mått, Skelton & Pais *Team Topologies* för teamstrukturer, Westrum för kultur).

### A-37 AWS CDK-länken använder föråldrad "latest"-sökväg
- **Fil:rad:** docs/03_version_control.md:26
- **Påstående:** "https://docs.aws.amazon.com/cdk/latest/guide/home.html"
- **Bedömning:** FÖRÅLDRAT (fungerar via redirect)
- **Allvarlighet:** Låg
- **Evidens:** URL:en omdirigeras till https://docs.aws.amazon.com/cdk/v2/guide/home.html (HTTP 200), som också är den URL Source [9] i 33_references.md använder.
- **Förslag:** Använd v2-URL:en direkt och hänvisa till Source [9] i stället för en inline-länk.

### A-38 Chung et al.: ISBN med fel kontrollsiffra (i bibliografin)
- **Fil:rad:** docs/33_references.md:60 (kapitelposten docs/02_fundamental_principles.md:604 saknar ISBN)
- **Påstående:** "Chung, L., Nixon, B.A., Yu, E. & Mylopoulos, J. … Springer, 2000. ISBN: 978-0-7923-8666-6"
- **Bedömning:** FEL (ISBN)
- **Allvarlighet:** Låg
- **Evidens:** Open Library: *Non-functional requirements in software engineering*, Chung/Nixon/Yu/Mylopoulos, Kluwer Academic (nu Springer), 1999/2000, ISBN-10 0-7923-8666-3, ISBN-13 978-0-7923-8666-7 (https://openlibrary.org/search.json?title=Non-Functional+Requirements+in+Software+Engineering&author=Chung). Kontrollsiffran för 978079238666x är 7, inte 6.
- **Förslag:** "ISBN 978-0-7923-8666-7 (Kluwer Academic Publishers, 1999; Springer reprint)".

### A-39 Oklar anekdot presenterad som faktum
- **Fil:rad:** docs/04_adr.md:242
- **Påstående:** "This workflow prevented significant disruption during a recent platform rotation: when the outgoing lead departed, the incoming engineer replayed the ADR change log to rebuild the rationale for Terraform state hardening…"
- **Bedömning:** EJ VERIFIERBART
- **Allvarlighet:** Låg
- **Evidens:** Ingen organisation, tidpunkt eller källa anges; HashiCorp-länken i samma mening (se A-22) handlar inte om detta.
- **Förslag:** Markera som författarens erfarenhet ("In one engagement the author observed …") i linje med posten "Nordqvist, G. … Author's own professional practice" i 33_references.md, eller stryk.

## Verifierat korrekt (urval)

- **Nygard introducerade ADR** (docs/04_adr.md:9, :292): blogginlägget "Documenting Architecture Decisions" publicerades 15 november 2011 av Michael Nygard; mallens sektioner Title/Context/Decision/Status/Consequences och statusarna proposed/accepted/deprecated/superseded stämmer med bokens tabell (docs/04_adr.md:25). https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- **GitHub protected branches** (docs/02_fundamental_principles.md:51; docs/03_version_control.md:46): alternativen "Require pull request reviews", "Require status checks", "Require signed commits" och "Require linear history" finns som beskrivet. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- **CDK assertions utvärderar syntetiserade mallar utan att skapa resurser** (docs/03_version_control.md:50): modulen `aws-cdk-lib/assertions` (`Template.fromStack`) testar den genererade CloudFormation-mallen. https://docs.aws.amazon.com/cdk/v2/guide/testing.html
- **`az deployment group what-if --resource-group … --template-file infrastructure.bicep`** (docs/02_fundamental_principles.md:239–241) är korrekt syntax; what-if jämför mallen med nuvarande resurstillstånd utan att göra ändringar. https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if
- **`aws cloudformation detect-stack-drift --stack-name …`** (docs/02_fundamental_principles.md:235) är korrekt. https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stack-drift-detection-status.html (hänvisar till detect-stack-drift)
- **Azure Bicep är ett deklarativt språk för Azure-resurser; Pulumi stöder flera molnleverantörer med allmänna programspråk** (docs/03_version_control.md:26) – stämmer med leverantörsdokumentationen.
- **Kapitel 19 behandlar GitHub Issues och Discussions** (docs/03_version_control.md:80): docs/19_management_as_code.md rad 13 och avsnittet "Achieving Transparency Through Issues and Discussions" (rad 72 ff.).
- **Kapitel 5 använder DORA-mått och citerar DORA 2023** (docs/26a_prerequisites_for_aac.md:124): docs/05_automation_devops_cicd.md:385 och :593.
- **Schmidt (2006)** är en verklig publikation: D. C. Schmidt, "Guest Editor's Introduction: Model-Driven Engineering", *IEEE Computer* 39(2), februari 2006, s. 25–31. https://api.openalex.org/works/doi:10.1109/MC.2006.58
- **Selic (2003)** är en verklig publikation: *IEEE Software* 20(5), sept/okt 2003, s. 19–25 (innehållet övertolkas dock, se A-13). https://api.openalex.org/works/doi:10.1109/MS.2003.1231146
- **OMG, 2001** (docs/02_fundamental_principles.md:35): OMG:s Architecture Board-dokument ormsc/01-07-01 "Model Driven Architecture (MDA)" (juli 2001) finns på OMG:s dokumentserver, https://www.omg.org/cgi-bin/doc?ormsc/2001-07-01. Nyans: initiativet lanserades redan november 2000 (Soleys white paper; OMG-tidslinje https://www.omg.org/sda/Richard-Soley-17-05-03.pdf), MDA Guide 1.0.1 kom 2003.
- **Chung et al. (2000), Springer/Kluwer** (docs/02_fundamental_principles.md:604) finns som angivet (ISBN-kontrollsiffran i bibliografin är dock fel, se A-38).
- **IEEE 1012-2016 publicerades 2017** (årtalet "IEEE (2017)" stämmer; titeln gör det inte, se A-11). https://standards.ieee.org/ieee/1012/5609/
- **Write the Docs, "Docs as Code"** (docs/02_fundamental_principles.md:600; Source [21]) finns på angiven URL. https://www.writethedocs.org/guide/docs-as-code/
- **Lightweight ADR-blippen** finns (som faktum; bokens datering är fel, se A-09). https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- **HCP Terraform-namnbytet** gäller från 22 april 2024 (grund för A-30). https://developer.hashicorp.com/terraform/enterprise/v202409-1
- **OPA 1.0 kräver `if`/`contains`** (grund för A-07). https://www.openpolicyagent.org/docs/v0-upgrade
- **Node.js-releaseplanen** (grund för A-20): Node 18 EOL 2025-04-30. https://raw.githubusercontent.com/nodejs/Release/main/schedule.json
- **Homebrew-formeln `structurizr-cli` ger ett körbart program med det namnet** (dvs. kommandonamnet i docs/02_fundamental_principles.md:129 var legitimt när det skrevs), men formeln är nu deprecated. https://formulae.brew.sh/formula/structurizr-cli
- **GDPR art. 44** reglerar överföringar, inte lagringsplats (grund för A-15). https://gdpr-info.eu/art-44-gdpr/
- **EDPB Guidelines 07/2020 finns** (men handlar om controller/processor, se A-16). https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en
- **Alla bildfiler som refereras i de sex kapitlen finns** som både `.mmd` och `.png` i docs/images/ (diagram_01_introduction, diagram_01_aac_flow, diagram_17_transformation_journey, diagram_02_chapter1, diagram_02_v_model, diagram_03_chapter2, diagram_04_adr_process, diagram_04_adr_structure, diagram_04_adr_lifecycle).
- **`course/`-katalogen finns** med curriculum, exercises, materials och templates (docs/01_introduction.md:85).
- **Readiness-scorecardens poängskala** (docs/26a_prerequisites_for_aac.md:72–98) är internt konsekvent: 15 kriterier × max 5 = 75.
- **URL-status (HTTP 200):** https://adr.github.io, https://docs.aws.amazon.com/cdk/v2/guide/home.html, https://www.atlassian.com/git/tutorials/comparing-workflows, GitHub Docs protected branches, https://www.openpolicyagent.org/docs, https://www.writethedocs.org/guide/docs-as-code/, https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions, CNCF-rapportsidorna. **HTTP 404:** Source [29] (Red Hat). **Omdirigerade till annan sida:** Thoughtworks governance-as-code, Thoughtworks edition21-nyheten, HashiCorp sensitive-data (ny URL), AWS CDK "latest".

## Ej verifierbart

- **Existensen av en "State of Cloud Native Development 2024"-upplaga** (docs/01_introduction.md:17): CNCF:s egen webbplats och sök-API listar inga 2024-upplagor (endast 2020–2022, Q1 2025, Q3 2025, Q1 2026 och regionala rapporter), men en negativ sökning bevisar inte frånvaro i t.ex. SlashDatas eget arkiv. Oavsett detta stämmer inte siffran "two thirds" med någon tillgänglig upplaga (se A-04).
- **Schmidt (2006) om "telecoms, aerospace, and defence programmes"** (docs/02_fundamental_principles.md:35): endast abstraktet kunde läsas (MDE som svar på tredje generationens språks begränsningar); huruvida artikeln lyfter fram just dessa domäners vinster kunde inte kontrolleras i fulltext. Bör kontrolleras av författaren mot artikeln (IEEE Xplore, DOI 10.1109/MC.2006.58).
- **GitLab-källorna** (A-06) och **"ENISA Information Security Baseline, 2024"** (A-16): kunde inte återfinnas via webbsökning eller på utgivarnas webbplatser; webbsökbudgeten tog slut innan ytterligare varianter kunde prövas.
- **Exakt releaseår för OPA v1.0.0 och GitHub Actions-versionerna** (A-07, A-20): GitHubs releasesidor visade dag/månad ("20 Dec", "04 Sep", "08 Apr") men inte år i det hämtade innehållet; åren 2024/2025/2024 följer av releasehistoriken (OPA 1.0 kräver Go 1.22; setup-node v5 följer efter v4 från 2023; peaceiris v4 efter v3) men bör bekräftas om de ska skrivas ut i boken.
- **Thoughtworks Radar vol. 22–27 och ≤20** söktes inte i fulltext efter "governance as code" (endast vol. 21 och 28–31); blipp-URL:ens omdirigering till indexsidan är dock stark evidens för att ingen sådan blipp existerar i Radars arkiv.
- **Wayback-länken** i docs/03_version_control.md:26: web.archive.org återställde anslutningen (connection reset) vid två försök; länken är dessutom en jokersökning och inte en arkiverad sida.
- **Anekdoten om "a recent platform rotation"** (docs/04_adr.md:242), se A-39.
