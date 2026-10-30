<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del E, kapitel 17–19

## Omfattning

Granskade filer (lästa i sin helhet, rad för rad):

- `docs/part_e_leadership.md` (28 rader)
- `docs/17_organisational_change.md` (105 rader)
- `docs/18_team_structure.md` (279 rader)
- `docs/19_management_as_code.md` (300 rader)

Stödmaterial som lästs för korskontroll: `docs/33_references.md` (hela), `docs/book_index.json`, `mkdocs.yml` (Del E–F), `docs/pandoc.yaml`, `scripts/verify_sources.py` (ISBN-logiken), samtliga 14 Mermaid-källor (`docs/images/*_17*.mmd`, `*_18_*.mmd`, `*_19_*.mmd`) samt ankarna `17_code_1..3` i `docs/30_appendix_code_examples.md`.

Inventering: cirka 60 kontrollerbara påståenden (15 källposter i kapitlens "## Sources", 1 URL, 8 ramverks-/modellbeskrivningar, 10 verktygs-/tjänstpåståenden om GitHub, certifieringar och utbildningsplattformar, 2 YAML-exempel, cirka 20 interna korsreferenser/konsistenspunkter, bildfiler). Av dessa har cirka 35 verifierats mot primärkällor på webben (Open Library, Internet Archive, IT Revolution, dora.dev, docs.github.com, GitHub community/tags, Atlassian, HashiCorp, Puppet/Perforce, CD Foundation, Spotify Engineering, Crisp, Pluralsight, AWS, Microsoft Learn, Wikipedia) och resten lokalt (grep, ISBN-13-kontrollsiffra, YAML-parsning, filexistens). Datum för verifiering: 2026-10-30. Obs: webbsökbudgeten tog slut mot slutet; alla kvarvarande kontroller gjordes med direkta hämtningar av kända URL:er.

Övergripande iakttagelse: kapitlen 17–19 innehåller nästan inga hårda siffror, citat eller namngivna personer i löptexten. Inga av källposterna i "## Sources" citeras inline – de är "dekorativa" referenslistor. Faktaproblemen ligger därför nästan uteslutande i källlistorna, i verktygspåståenden om GitHub och i intern konsistens (rubrikstruktur, index, bibliografi).

## Sammanfattning

Löptexten i kapitel 17–19 är i huvudsak generisk ledarskaps-/organisationsprosa utan kontroversiella fakta; ramverksbeskrivningarna som faktiskt förekommer (Conways lag, DORA-mått, CODEOWNERS/branch protection, YAML-exempel) stämmer eller är bara lätt föråldrade. De allvarligaste problemen är i stället: (1) en McKinsey-källa som inte går att finna och sannolikt är påhittad; (2) "Spotify Engineering Culture" felaktigt daterad till 2023 och tillskriven företaget, när det är Henrik Knibergs videor från 2014; (3) ett upprepat påstående i kapitel 19 att man kan skapa "private Issues" i GitHub för sårbarheter – funktionen finns inte (ärenden följer repots synlighet; GitHubs privata kanal är Security Advisories/Private Vulnerability Reporting); (4) ISBN för *Team Topologies* i bibliografin (978-1-942788-81-4) är ogiltigt – kontrollsiffran stämmer inte, korrekt är 978-1-942788-81-2; (5) ett strukturfel i kapitel 18 där mallen för "Community of Practice" ligger som riktiga rubriker (en extra H1) utanför kodblock, vilket med `top-level-division: chapter` skapar ett spökkapitel "Infrastructure as Code Community of Practice" i PDF/EPUB. Därtill finns flera förlegade eller felaktiga förlags-/titeluppgifter ("Puppet Labs" 2023, "HashiCorp Learn" 2024, Linux Academy som aktuell plattform, Drucker/Harper & Row, OpenGitOps 2024) samt inkonsekvenser mellan kapitel, `book_index.json`, `mkdocs.yml` och `33_references.md`.

## Fynd

### E1-01 Påhittad/ospårbar McKinsey-källa
- **Fil:rad:** docs/17_organisational_change.md:105
- **Påstående:** "**McKinsey & Company (2023).** *Organisational Transformation Best Practices.* McKinsey Digital."
- **Bedömning:** FELCITERAT (fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** Ingen publikation med denna titel finns på mckinsey.com eller i externa index (sökning i två varianter, inkl. domänbegränsad till mckinsey.com). Närmaste verkliga McKinsey-publikationer 2023 är *The State of Organizations 2023* (https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-state-of-organizations-2023), *How to implement transformations for long-term impact* (maj 2023, https://www.mckinsey.com/capabilities/implementation/our-insights/how-to-implement-transformations-for-long-term-impact) och *The science behind successful organizational transformations* (https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/successful-transformations). "McKinsey Digital" är dessutom en affärsenhet, inte ett förlag. Källan citeras aldrig i kapitlets löptext.
- **Förslag:** Ersätt med en verklig, verifierad publikation (t.ex. *The State of Organizations 2023*, McKinsey & Company, april 2023, med URL) eller stryk posten. Om något i löptexten ska stödjas av McKinsey måste det anges inline.

### E1-02 "Spotify Engineering Culture" feldaterad och feltillskriven
- **Fil:rad:** docs/17_organisational_change.md:102
- **Påstående:** "**Spotify Technology (2023).** *Spotify Engineering Culture.* Spotify Technology."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Verket är Henrik Knibergs tvådelade animerade video "Spotify Engineering Culture", del 1 publicerad 27 mars 2014 (Spotify Engineering/Labs-bloggen: https://engineering.atspotify.com/spotify-engineering-culture-part-1/ ; Crisp-bloggen: https://blog.crisp.se/2014/03/27/henrikkniberg/spotify-engineering-culture-part-1), del 2 september 2014. Det finns ingen företagspublikation från "Spotify Technology" 2023 med den titeln. Kapitlet behandlar dessutom inte Spotify-modellen alls, så posten är en föräldralös referens. Notera även att Spotify själva och Kniberg betonat att modellen var en ögonblicksbild, inte ett ramverk.
- **Förslag:** Ändra till "Kniberg, H. & Ivarsson, A. (2012). *Scaling Agile @ Spotify*" och/eller "Kniberg, H. (2014). *Spotify Engineering Culture* (parts 1–2), Spotify Engineering blog" med URL – eller stryk posten eftersom texten inte använder den.

### E1-03 GitHub "private Issue" finns inte som funktion
- **Fil:rad:** docs/19_management_as_code.md:115 (även :122)
- **Påstående:** "The team creates a private Issue (maintaining appropriate confidentiality) that: …" och "Even though the Issue remains private for security reasons, the transparency within the authorised team ensures coordinated response…"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** GitHub Issues har ingen synlighet per ärende; ärenden följer repositoriets synlighet. Funktionen "private/hidden issues" är en återkommande, ej implementerad användarförfrågan: community-diskussion #16385 (11 maj 2022, "Private/Hidden Issues", obesvarad: https://github.com/community/community/discussions/16385), #61373 (juli 2023, där det enda alternativet som anges är ett separat privat repo: https://github.com/orgs/community/discussions/61373) och #169786 (augusti 2025: https://github.com/orgs/community/discussions/169786). GitHubs changelog fram till oktober 2026 innehåller ingen lansering av privata ärenden (däremot "restricted issue creation" juni 2026 och "structured forms for private vulnerability reports" 1 okt 2026: https://github.blog/changelog/2026-10-01-structured-forms-for-private-vulnerability-reports/). GitHubs avsedda privata kanal för exakt detta scenario är Repository Security Advisories med "temporary private fork" och Private Vulnerability Reporting (https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories ; https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository). Exemplet riskerar att få läsare att publicera sårbarhetsdetaljer i ett publikt repo.
- **Förslag:** Skriv om exempel 3: "The team opens a draft repository security advisory (or receives a private vulnerability report) and collaborates in the temporary private fork; alternatively it tracks the work as an Issue in a private repository. Issues inherit repository visibility – GitHub has no per-issue confidentiality." Justera rad 122 i linje med detta.

### E1-04 Ogiltigt ISBN för Team Topologies i bibliografin (länkad från kap. 17 och 18)
- **Fil:rad:** docs/33_references.md:36 (länkas från docs/17_organisational_change.md:103 och docs/18_team_structure.md:276 som "Source [30]")
- **Påstående:** "Skelton, M. & Pais, M. *Team Topologies: Organising Business and Technology Teams for Fast Flow.* IT Revolution Press, 2019. ISBN: 978-1-942788-81-4."
- **Bedömning:** FEL
- **Allvarlighet:** Medel (ISBN-detalj enligt skalan, men numret är ogiltigt, inte bara "fel utgåva")
- **Evidens:** ISBN-13-kontrollsiffran för 978-1-942788-81-? är 2, inte 4 (viktad summa 128 → 10−8 = 2). Open Library: ISBN 9781942788812 = *Team Topologies: Organizing Business and Technology Teams for Fast Flow*, IT Revolution Press, 17 sep 2019 (https://openlibrary.org/isbn/9781942788812.json); 9781942788814 ger inget resultat. Projektets `scripts/verify_sources.py` (rad 222–240) kontrollerar bara att ISBN består av 13 siffror, inte kontrollsiffran – därför har felet passerat.
- **Förslag:** Ändra till "ISBN: 978-1-942788-81-2". Komplettera `verify_sources.py` med kontrollsiffreberäkning för ISBN-10/13.

### E1-05 Spökkapitel: mall för Community of Practice ligger som riktiga rubriker (extra H1)
- **Fil:rad:** docs/18_team_structure.md:201–259
- **Påstående:** "# Infrastructure as Code Community of Practice" följt av "## Purpose", "## Structure", "### Core Team" … "### Metrics and Success Criteria" (ej inom kodblock).
- **Bedömning:** INKONSEKVENT (strukturfel som påverkar den publicerade boken)
- **Allvarlighet:** Medel
- **Evidens:** Rad 199 säger "This template accompanies the knowledge sharing guidance", men mallen är inte inkapslad i ``` ```markdown ``` som de två YAML-mallarna (rad 63–139, 153–189). `docs/pandoc.yaml` har `top-level-division: chapter` (rad 13) och `epub-chapter-level: 1` (rad 133), så H1 på rad 201 blir ett eget kapitel "Infrastructure as Code Community of Practice" i PDF-innehållsförteckningen och en egen EPUB-fil; "## Purpose" etc. blir sektioner på samma nivå som kapitlets riktiga sektioner. På MkDocs-sidan blir det en andra H1. Rubriken säger dessutom "Infrastructure as Code" medan brödtexten (rad 204) säger "Architecture as Code practices" – terminologiskt inkonsekvent med bokens titelkonvention. Inga tester i `tests/` fångar dubbla H1.
- **Förslag:** Lägg mallen i ett ```markdown-kodblock (som YAML-mallarna), eller degradera rubrikerna till fet text/listor. Byt "Infrastructure as Code Community of Practice" till "Architecture as Code Community of Practice". Överväg ett test som förbjuder fler än en H1 per kapitelfil.

### E1-06 Bibliografin påstår att kapitel 17 citerar Gartner- och HashiCorp-undersökningar som inte förekommer i kapitlet
- **Fil:rad:** docs/33_references.md:157–158 och :164–165 (gäller docs/17_organisational_change.md)
- **Påstående:** "**Gartner.** 'Forecast Analysis: Public Cloud Services Worldwide.' … *Referenced in: … [Chapter 17: Organisational Change]*" och "**HashiCorp.** 'State of Cloud Strategy Survey 2024.' … *Referenced in: [Chapter 17: Organisational Change], [Chapter 27: Conclusion]*"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `grep -i 'gartner\|hashicorp' docs/17_organisational_change.md` ger inga träffar i löptext eller källlista. "State of Cloud Strategy" förekommer inte i någon kapitelfil alls (grep över docs/*.md exkl. 33_references.md), och `docs/27_conclusion.md` innehåller inte ordet HashiCorp. Gartner-prognosen används bara i kap. 15 (rad 75, 153) och 25 (rad 297).
- **Förslag:** Ta bort "Chapter 17" (och "Chapter 27") från de två posterna, eller stryk HashiCorp-posten helt om ingen kapiteltext använder den. Kör `python3 scripts/verify_sources.py` efter ändringen.

### E1-07 "Puppet Labs (2023)" – förlagsnamn som upphörde 2016; titel saknas; inkonsekvent mellan kap. 17 och 19
- **Fil:rad:** docs/17_organisational_change.md:100 (jfr docs/19_management_as_code.md:296)
- **Påstående:** "**Puppet Labs (2023).** *State of DevOps Report.* Puppet Labs." resp. "**Puppet (2023).** *State of DevOps Report.* Puppet. Annual industry survey on DevOps practices."
- **Bedömning:** FELCITERAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Puppet Labs bytte namn till Puppet den 7 april 2016 (https://www.sdxcentral.com/articles/news/puppet-adds-coo-shortens-name/2016/04/ ; https://www.hpcwire.com/aiwire/2016/04/07/puppet-pulls-strings-expansion-plans-makeover/) och ingår sedan 2022 i Perforce ("Puppet by Perforce"). 2023-utgåvan heter "2023 State of DevOps Report: Platform Engineering Edition" – Puppets egen sida beskriver den som "The State of Platform Engineering Report is the 2023 edition of Puppet's long-running State of DevOps Report" (https://www.puppet.com/resources/state-of-devops-report ; CD Foundation 20 jan 2023: https://cd.foundation/blog/2023/01/20/state-of-devops-report-2023-results-platform-engineering/). Samma rapport anges med två olika utgivarnamn i kap. 17 och 19. Källan citeras inte i löptexten i något av kapitlen.
- **Förslag:** Enhetlig post i båda kapitlen: "**Puppet by Perforce (2023).** *2023 State of DevOps Report: Platform Engineering Edition.* Puppet. Available at: https://www.puppet.com/resources/state-of-devops-report".

### E1-08 HashiCorp "Infrastructure as Code Maturity Model" på "HashiCorp Learn" (2024) – plattformen nedlagd 2022, dokumentet oidentifierbart
- **Fil:rad:** docs/18_team_structure.md:279
- **Påstående:** "**HashiCorp (2024).** *Infrastructure as Code Maturity Model.* HashiCorp Learn Platform."
- **Bedömning:** FELCITERAT / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** HashiCorp Learn slogs ihop med HashiCorp Developer i oktober 2022 (blogg 5 okt 2022: https://www.hashicorp.com/blog/hashicorp-developer-your-new-experience-for-docs-and-tutorials); learn.hashicorp.com omdirigerar i dag till https://developer.hashicorp.com/tutorials (verifierat med curl). Något dokument med titeln "Infrastructure as Code Maturity Model" finns inte där. Det närmaste verkliga HashiCorp-materialet är (a) Terraform recommended practices med "four stages of operational maturity around provisioning": Manual changes → Semi-automation → Infrastructure as Code → Collaborative Infrastructure as Code (https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices) och (b) ett HashiCorp/Google Cloud-webbinarium "Unlocking Google Cloud at Scale: The Infrastructure as Code Maturity Model with Terraform" (odaterad listning, talare Arslan Saeed och Jake Lundberg; sidan kunde inte hämtas p.g.a. 429/Vercel-kontroll). Kapitlet nämner ingen mognadsmodell i löptexten.
- **Förslag:** Byt till "HashiCorp. *Terraform Recommended Practices* (provisioning maturity model). HashiCorp Developer. https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices" eller stryk posten.

### E1-09 DORA-måtten återges i föråldrad fyrmåttsform med gamla namn
- **Fil:rad:** docs/17_organisational_change.md:86 (även docs/18_team_structure.md:265, docs/18_team_structure.md:15)
- **Påstående:** "DORA metrics (deployment frequency, lead time, change failure rate, and recovery time) provide baseline technical health indicators" resp. "(deployment frequency, change failure rate, mean time to restore)"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** DORA:s nuvarande modell omfattar fem mått för mjukvaruleverans: *change lead time*, *deployment frequency*, *failed deployment recovery time*, *change fail rate* och *deployment rework rate* (https://dora.dev/guides/dora-metrics/). Enligt DORA:s metrikhistorik (https://dora.dev/insights/dora-metrics-history/) lades *availability* till 2018 som operativt mått, döptes om till *reliability* 2021, "mean time to recover (MTTR)"/"time to restore service" döptes om och omdefinierades till *failed deployment recovery time* 2023, och *deployment rework rate* infördes 2024. De fyra ursprungliga måtten (2014) är korrekt återgivna i sak, men presenteras som aktuella.
- **Förslag:** "DORA's software delivery metrics – change lead time, deployment frequency, change fail rate and failed deployment recovery time (formerly 'time to restore service'), extended since 2024 with deployment rework rate, alongside reliability as an operational measure –". Ersätt "mean time to restore" i kap. 18 med "failed deployment recovery time".

### E1-10 Linux Academy angiven som aktuell utbildningsplattform (och A Cloud Guru säljs inte längre)
- **Fil:rad:** docs/18_team_structure.md:55
- **Påstående:** "External platforms (A Cloud Guru, Pluralsight, Linux Academy) provide curated curricula aligned to Architecture as Code tooling"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Linux Academy förvärvades av A Cloud Guru 16 dec 2019 och integrerades (https://trainingindustry.com/press-release/it-and-technical-training/a-cloud-guru-announces-acquisition-of-linux-academy/ ; https://devclass.com/2019/12/17/a-cloud-guru-swallows-linux-academy-as-scotch-io-pours-itself-into-digital-ocean/); A Cloud Guru förvärvades av Pluralsight 2021 och Pluralsight uppger att "A Cloud Guru plans are no longer available for purchase" samt att innehållet flyttats in i Pluralsights bibliotek (https://www.pluralsight.com/cloud-guru, dit acloudguru.com omdirigerar). linuxacademy.com svarar inte längre (502 vid hämtning 2026-10-30). Tre namn i listan är i praktiken en enda leverantör.
- **Förslag:** "External platforms (for example Pluralsight, which absorbed A Cloud Guru and Linux Academy, KodeKloud or vendor academies) …" – eller formulera generiskt utan varumärken.

### E1-11 Del E-introduktionen och navigationen stämmer inte med book_index.json (kapitel 23)
- **Fil:rad:** docs/part_e_leadership.md:19–26 (jfr docs/book_index.json "part_e", mkdocs.yml:39–49)
- **Påstående:** "**What you will learn in this part:** – Organisational change patterns … – Team structure designs … – Cultural practices … – Management as Code principles … – AI agent team models … – Digitalisation strategies …"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` (kanonisk enligt CLAUDE.md) placerar Del E som kapitlen 17, 18, 19, **23** ("The Interplay Between Soft As Code Disciplines"), 20, 21. Introduktionen nämner inte kapitel 23:s tema alls, och `mkdocs.yml` lägger kapitel 23 i Del F (rad 47–49). Kanonisk ordning, webbplatsnavigation och delintroduktion pekar alltså åt tre olika håll.
- **Förslag:** Bestäm var kapitel 23 hör hemma; uppdatera antingen `book_index.json`/`mkdocs.yml` eller lägg till en punkt i introduktionen ("How the 'soft as code' disciplines – policy, governance, documentation and management – interlock") och nämn kapitlet i avslutningsstycket (rad 28).

### E1-12 Kapitel 18:s titel skiljer sig mellan fil, index, navigation och bibliografi
- **Fil:rad:** docs/18_team_structure.md:1 (jfr docs/book_index.json, mkdocs.yml:41, docs/33_references.md:36)
- **Påstående:** "# Team Structure and Competency Development for Architecture as Code"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `book_index.json` och `mkdocs.yml` kallar kapitlet "Team Structure and Competency Development for IaC"; `33_references.md` kallar det "Chapter 18: Team Structure". Bokens titelkonvention är "Architecture as Code", så filens H1 är sannolikt den avsedda.
- **Förslag:** Synkronisera `book_index.json`, `mkdocs.yml` och 33_references.md till H1-lydelsen.

### E1-13 Atlassian-källans titel och publikationstyp är felaktiga
- **Fil:rad:** docs/18_team_structure.md:278
- **Påstående:** "**Atlassian (2024).** *DevOps Team Structure and Best Practices.* Atlassian Documentation."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Låg
- **Evidens:** Den verkliga sidan heter "The Importance of DevOps Team Structure" och är en odaterad artikel i Atlassians DevOps-guider (inte produktdokumentation): https://www.atlassian.com/devops/frameworks/team-structure (HTTP 200). Artikeln bygger uttryckligen på Team Topologies och på Skeltons DevOps-topologier (t.ex. "DevOps as an external party").
- **Förslag:** "Atlassian. *The Importance of DevOps Team Structure.* Atlassian DevOps guides. Available at: https://www.atlassian.com/devops/frameworks/team-structure (accessed 2026-10-30)."

### E1-14 Drucker (1954) anges med förlaget Harper & Row, som bildades först 1962
- **Fil:rad:** docs/19_management_as_code.md:294
- **Påstående:** "**Drucker, P.F. (1954).** *The Practice of Management.* Harper & Row."
- **Bedömning:** FELCITERAT (förlagsdetalj)
- **Allvarlighet:** Låg
- **Evidens:** Originalutgåvan 1954 gavs ut av Harper & Brothers, New York (Internet Archive-post practiceofmanage0000pete, "Harper & Brothers Publishers", 1954: https://archive.org/details/practiceofmanage0000pete ; Open Library-utgåvor 1954 "Harper"/"Harper & Brothers Publishers, New York": https://openlibrary.org/works/OL274337W). Harper & Row uppstod 1962 genom fusionen Harper & Brothers + Row, Peterson & Company (https://en.wikipedia.org/wiki/Harper_%26_Row). Vissa bibliotekskataloger anger felaktigt "Harper & Row" på 1954-poster, vilket förklarar felet. Drucker citeras inte i kapitlets löptext (trots att OKR/MBO-kopplingen hade varit naturlig).
- **Förslag:** "Drucker, P.F. (1954). *The Practice of Management.* New York: Harper & Brothers." Överväg att faktiskt referera Drucker där OKR introduceras (rad 25) – OKR härstammar från Druckers Management by Objectives via Andy Grove (Intel) och John Doerr.

### E1-15 OpenGitOps-principerna daterade 2024; de publicerades som v1.0.0 i oktober 2021
- **Fil:rad:** docs/19_management_as_code.md:295
- **Påstående:** "**GitOps Working Group (2024).** *GitOps Principles.* OpenGitOps. Available at: https://opengitops.dev/"
- **Bedömning:** FELCITERAT (årtal)
- **Allvarlighet:** Låg
- **Evidens:** URL:en svarar 200 och visar principerna v1.0.0 (Declarative; Versioned and Immutable; Pulled Automatically; Continuously Reconciled), "Overseen by the GitOps Working Group" (CNCF TAG App Delivery). Taggen v1.0.0 är daterad 8 okt 2021 (https://github.com/open-gitops/documents/tags); projektets egna BibTeX-mall anger `year = {2021}` (https://github.com/open-gitops/documents/blob/main/README.md). Källan citeras inte i löptexten.
- **Förslag:** "CNCF GitOps Working Group (2021). *GitOps Principles v1.0.0.* OpenGitOps. https://opengitops.dev/ (accessed 2026-10-30)".

### E1-16 Team Topologies: titelstavning ändrad och undertitel inkonsekvent; andra upplagan (2025) finns
- **Fil:rad:** docs/17_organisational_change.md:103; docs/18_team_structure.md:276; docs/33_references.md:36
- **Påstående:** "*Team Topologies: Organising Business and Technology Teams for Fast Flow.*" (kap. 17) resp. "*Team Topologies: Organising Business and Technology Teams.*" (kap. 18)
- **Bedömning:** INKONSEKVENT / FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Originaltiteln är *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (Open Library 9781942788812). Verktitlar är egennamn och bör inte "britticiseras" trots stilguiden; kap. 18 trunkerar dessutom undertiteln och kap. 27 utelämnar den helt. En andra upplaga utkom 23 sep 2025: *Team Topologies, 2nd Edition: Organizing Business and Technology for Fast Flow of Value*, ISBN 9781966280002 (https://itrevolution.com/product/team-topologies/).
- **Förslag:** Använd originalstavningen "Organizing" och samma fullständiga undertitel i alla tre kapitel samt bibliografin; överväg att nämna 2:a upplagan (2025) eller uppdatera referensen.

### E1-17 DORA-rapporten 2023 benämns olika och är inte kopplad till Source [28]
- **Fil:rad:** docs/17_organisational_change.md:101; docs/18_team_structure.md:277 (jfr docs/33_references.md:34)
- **Påstående:** "**Google Cloud (2023).** *DORA State of DevOps Research.* Google Cloud." resp. "**Google Cloud (2023).** *DevOps Research and Assessment (DORA) Reports.* Google Cloud Platform."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Rapportens faktiska titel är *Accelerate State of DevOps Report 2023* (DORA, "a program run by Google Cloud"): https://dora.dev/research/2023/dora-report/ (HTTP 200). Bibliografin har redan en korrekt post som Source [28], men kapitlen länkar inte till den och använder två påhittade titlar. Dessutom har DORA sedan dess publicerat 2024- och 2025-rapporter.
- **Förslag:** I båda kapitlen: "**DORA (2023).** *Accelerate State of DevOps Report 2023.* Google Cloud. [Source [28]](33_references.md#source-28)" – eller uppdatera till den senaste rapporten.

### E1-18 Certifieringsnamnen är inte de officiella
- **Fil:rad:** docs/18_team_structure.md:55
- **Påstående:** "Industry certifications such as AWS Certified DevOps Engineer, Microsoft Azure DevOps Engineer Expert, and HashiCorp Certified Terraform Associate (at time of writing; …)"
- **Bedömning:** TVEKSAMT (namnprecision)
- **Allvarlighet:** Låg
- **Evidens:** Officiella namn: "AWS Certified DevOps Engineer – Professional" (exam DOP-C02; https://aws.amazon.com/certification/certified-devops-engineer-professional/), "Microsoft Certified: DevOps Engineer Expert" (exam AZ-400; https://learn.microsoft.com/en-us/credentials/certifications/devops-engineer/), "HashiCorp Certified: Terraform Associate" – version 004 ersatte 003 den 8 jan 2026 (https://developer.hashicorp.com/certifications/infrastructure-automation ; https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004). Reservationen "at time of writing" finns redan, vilket mildrar problemet.
- **Förslag:** Skriv de officiella namnen: "AWS Certified DevOps Engineer – Professional, Microsoft Certified: DevOps Engineer Expert, and HashiCorp Certified: Terraform Associate".

### E1-19 "## Sources" placerad före "## Summary" i kapitel 19
- **Fil:rad:** docs/19_management_as_code.md:292–300
- **Påstående:** "## Sources … ## Summary"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Kapitel 17 (rad 90/98) och 18 (rad 269/273) och övriga kapitel avslutar med Summary följt av Sources. Kapitel 19 har omvänd ordning.
- **Förslag:** Flytta "## Summary" före "## Sources".

### E1-20 Bibliografins fullständighetspåstående stämmer inte för kapitel 17–19
- **Fil:rad:** docs/33_references.md:178 (gäller källposter i docs/17:100–102,105; docs/18:275,277–279; docs/19:294–296)
- **Påstående:** "All citations in the manuscript are included in this compiled list, ensuring complete transparency and academic rigour throughout the work."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `grep -i 'drucker\|devops handbook\|spotify\|mckinsey\|opengitops\|puppet' docs/33_references.md` ger inga träffar; Atlassians team-structure-sida och HashiCorps "maturity model" saknas också. Nio av femton källposter i kapitel 17–19 finns alltså inte i den "kompletta" listan.
- **Förslag:** Lägg in de (korrigerade) posterna i 33_references.md eller tona ned påståendet.

### E1-21 Trasig intern länk i bibliografin till "Chapter 20" (20_team_structures.md)
- **Fil:rad:** docs/33_references.md:10 (utanför de fyra granskade filerna, men i bibliografin som kap. 17–19 länkar till)
- **Påstående:** "[Chapter 20](20_team_structures.md)"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Filen `docs/20_team_structures.md` finns inte; kapitel 20 är `docs/20_ai_agent_team.md` enligt `book_index.json`. Sannolikt en rest från en äldre kapitelindelning där kapitel 18/20 hette "team structures".
- **Förslag:** Rätta länken (eller ta bort kapitel 20 från Source [4] om det inte citerar protected branches).

### E1-22 "PCI-DSS" – inofficiell stavning, inkonsekvent i manuskriptet
- **Fil:rad:** docs/19_management_as_code.md:102
- **Påstående:** "Security team highlights PCI-DSS requirements"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** PCI Security Standards Council skriver "PCI DSS" (utan bindestreck). Manuskriptet använder "PCI-DSS" 10 gånger och "PCI DSS" 1 gång (grep över docs/*.md).
- **Förslag:** Normalisera till "PCI DSS" i hela manuskriptet (lämpligt att lägga i `tests/test_consistency.py`).

## Verifierat korrekt (urval)

- **Accelerate** – Forsgren, Humble & Kim, *Accelerate: The Science of Lean Software and DevOps: Building and Scaling High Performing Technology Organizations*, IT Revolution Press, 27 mars 2018, ISBN 978-1-942788-33-1 (kontrollsiffra OK; https://openlibrary.org/isbn/9781942788331.json). Posterna i docs/17:104, docs/19:297 och Source [31] stämmer.
- **The DevOps Handbook** (docs/18:275) – Kim, Humble, Debois & Willis, IT Revolution Press, 2016 ("by Gene Kim, Jez Humble, Patrick Debois, and John Willis"; https://openlibrary.org/isbn/9781942788003.json). Korrekt.
- **Team Topologies** – författare, förlag och år (IT Revolution Press, 2019) stämmer; endast ISBN och titelstavning är fel (se E1-04, E1-16). https://openlibrary.org/isbn/9781942788812.json
- **Conways lag** (docs/18:19) – parafrasen "the system design mirrors the communication pathways" stämmer med Conway (1968): "organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations", *Datamation*, april 1968. https://www.melconway.com/Home/Committees_Paper.html
- **CODEOWNERS och protected branches** (docs/19:11, 59) – CODEOWNERS kan mappa kataloger/mönster till användare eller team, filen kan ligga i `.github/`, roten eller `docs/`, och branch protection/rulesets kan kräva "Require review from Code Owners". https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- **GitHub Discussions** för ledningsforum (docs/19:61 ff.) – "Anyone with access to a repository or organization can create and participate in discussions there" (måste aktiveras av administratör). https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions
- **OpenGitOps-URL** (docs/19:295) – https://opengitops.dev/ svarar HTTP 200 och innehåller GitOps-principerna v1.0.0 (endast årtalet är fel, E1-15).
- **DORA-rapporten 2023** finns och Source [28]-URL:en fungerar: https://dora.dev/research/2023/dora-report/ (HTTP 200, titel "Accelerate State of DevOps Report 2023").
- **Puppet 2023 State of DevOps Report** finns (Platform Engineering Edition, jan 2023) – https://www.puppet.com/resources/state-of-devops-report ; endast utgivarnamn/titel är felaktiga (E1-07).
- **De fyra ursprungliga DORA-måtten** (deployment frequency, lead time for changes, MTTR, change fail rate) är korrekt återgivna som 2014-modellen – https://dora.dev/insights/dora-metrics-history/ (men se E1-09 om aktuell modell).
- **YAML-exemplen** i docs/18 (training-program.yaml, team-structure.yaml) parsas felfritt med PyYAML; det är rena datamodeller utan API-beroenden.
- **Interna referenser**: ankarna `#17_code_1`, `#17_code_2`, `#17_code_3` finns i docs/30_appendix_code_examples.md (rad 1862, 1976, 2299) med rätt listnings-namn 17-A/17-B/17-C; "Appendix A" stämmer med book_index.json; länkarna till 16_migration.md, 13_testing_strategies.md och 14_practical_implementation.md i part_e_leadership.md pekar på existerande filer med rätt del (Del D). Alla 14 refererade PNG-filer och deras .mmd-källor finns.
- **Private Vulnerability Reporting / Security Advisories** finns som GitHubs privata kanal för sårbarheter (relevant för rättelsen i E1-03). https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository

## Ej verifierbart

- **HashiCorp/Google Cloud-webbinariet "Unlocking Google Cloud at Scale: The Infrastructure as Code Maturity Model with Terraform"** – sidan https://hashicorp.com/en/events/webinars/unlocking-google-cloud-at-scale-the-infrastructure-as-code-maturity-model-with-te kunde inte läsas (HTTP 429, Vercel Security Checkpoint; alternativ slug gav 404). Titel och talare kommer från sökresultatets sammanfattning; datum och stegindelning är obekräftade. Påverkar inte bedömningen i E1-08 (dokumentet som citeras finns ändå inte på "HashiCorp Learn").
- **Exakt publiceringsdag för Spotify Labs-versionen av "Spotify Engineering Culture" del 1** – Spotify Engineering-bloggen anger 27 mars 2014, Knibergs senare YouTube-beskrivning länkar till en Labs-post daterad 20 sep 2014. Året 2014 är säkert; dagen är sekundär för fyndet E1-02.
- **Huruvida A Cloud Guru som varumärke är formellt "pensionerat"** – Pluralsight skriver "A Cloud Guru is now part of Pluralsight" och att ACG-planer inte längre säljs, men använder fortfarande namnet som etikett på innehåll. E1-10 bygger därför på Linux Academy (klart nedlagt) snarare än på ACG.
- **Perforce pressmeddelande 18 jan 2023** (https://perforce.com/node/1186826) gav 404 vid hämtning; den exakta titeln "2023 State of DevOps Report: Platform Engineering Edition" bekräftas i stället av Puppets egen sida, CD Foundations blogg (20 jan 2023) och PlatformCon-programmet.
- **Webbsökning** var inte tillgänglig under slutfasen (delad sökbudget förbrukad); följande kontrollerades därför enbart med direkta URL-hämtningar och lokala beräkningar: OpenGitOps-datum, Drucker-förlag, GitHub-diskussionerna. Inget av dessa fynd vilar på en enda källa.
