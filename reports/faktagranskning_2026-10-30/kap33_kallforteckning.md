<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Kapitel 33 Källförteckning

Granskad fil: `docs/33_references.md` (178 rader). Granskningsdatum: 2026-10-30. Enbart bedömning – inga filer i repot har ändrats.

## Omfattning

- **74 poster granskade:** 32 numrerade källor (rad 7–38), 37 poster i "Academic and Industry Publications" (rad 42–151) och 5 poster i "Industry Research and Reports" (rad 155–168). Av dessa är 8 korshänvisningar ("See numbered index") till numrerade källor, dvs. 66 unika verk.
- **Metoder:**
  - Existens och bibliografiska uppgifter: Open Library (`openlibrary.org/isbn/<isbn>.json`), Crossref (`api.crossref.org`), förlagssidor (O'Reilly, Manning, Pearson/Addison-Wesley, Springer/Kluwer), NIST CSRC, IEEE Standards, OMG:s dokumentarkiv, Thoughtworks Radar-blippsidor, CNCF:s rapportlistor, Pulumi/HashiCorp/Microsoft Learn/GitHub/Red Hat-dokumentation, dev.to/simonbrown, Wayback Machine availability-API (endast existenskontroll av ögonblicksbilder).
  - ISBN: kontrollsiffra beräknad programmatiskt (ISBN-13 mod 10) **och** uppslag av vad varje ISBN faktiskt pekar på. Observera: endast 4 av 8 ISBN klarar kontrollsiffran (uppgiften antog att alla 8 gjorde det).
  - URL:er: `curl -sSL` med statuskod, slutlig URL efter omdirigering och sidans `<title>`; GitHub-repon via raw.githubusercontent.com och WebFetch (api.github.com var blockerat i sessionen).
  - "Referenced in": `grep` på `#source-n`-ankare och på författare/titel i samtliga `docs/*.md`; kapitelrubriker jämförda med `docs/book_index.json`; existens av länkade filer kontrollerad.
  - Kapitlens "## Sources"-avsnitt extraherade (36 kapitel) och jämförda mot kapitel 33 för luckanalys.
- **Begränsningar:** iso.org och gartner.com blockerar automatiserad hämtning (Cloudflare 403) – ISO 27001:2022:s titel anges från standardens kända beteckning; Gartner- och IDC-rapporter ligger bakom betalvägg; Thoughtworks Radar Vol. 21-PDF:en svarade 503. Websökbudgeten tog slut mot slutet, så tre poster (GitLab "Single Source of Truth", GitHub "Collaborative Software Development", Kvadrat "Technology Consulting Excellence") bygger på en sökomgång plus direkta hämtningar.

## Sammanfattning

Källförteckningen har allvarliga trovärdighetsproblem. Nio poster bedöms som fiktiva eller felaktiga på ett sätt som riskerar bokens akademiska trovärdighet: Thoughtworks Technology Radar har aldrig publicerat någon blipp "Architecture as Code: The Next Evolution" eller "Governance as Code" (Vol. 21:s blipp heter "Security policy as code"), Red Hat har ingen publikation "Architecture as Code Principles and Best Practices" (och URL:en ger 404), GitLab-, GitHub- och Structurizr-blogg-posterna kunde inte återfinnas någonstans, NIST SP 800-160 heter inte "Requirements Engineering for Secure Systems", och ISBN:et för *Clean Architecture* pekar på *Effective Java* (3:e uppl., Bloch). Sex av åtta ISBN är felaktiga: fyra klarar inte ens kontrollsiffran (Team Topologies, Software Architecture in Practice, Chung et al., Microservices Patterns) och två är giltiga men oregistrerade nummer (Site Reliability Workbook, Building Evolutionary Architectures). Flera webbkällor har påhittade titlar på verkliga sidor (Atlassian, HashiCorp ×2, Pulumi, Microsoft Learn, GDPR.eu) och fyra URL:er är döda eller omdirigerar till irrelevanta sidor (Red Hat, GDPR.eu, Kvadrat-profil, Thoughtworks nyhetssida; github.com/structurizr/dsl finns inte längre). "Referenced in"-listorna stämmer dåligt med den faktiska citeringen: 12 källor saknar kapitel som citerar dem, 8 anger kapitel som inte citerar dem, fyra länkade kapitelfiler finns inte och minst nio kapitelrubriker avviker från `book_index.json`. Påståendet på rad 178 att "All citations in the manuscript are included in this compiled list" är felaktigt – cirka 114 källposter i kapitlens egna Sources-avsnitt saknas i kapitel 33. Det som är korrekt är i huvudsak de officiella dokumentationslänkarna (HashiCorp, Kubernetes, AWS CDK, GitHub, GitLab, Jenkins, Azure Pipelines, DORA, OPA, Write the Docs, CNCF-definitionen, FINOS/CALM, Structurizr Lite, Mermaid, PlantUML, c4model, adr.github.io), NIST SP 800-53 Rev. 5, OMG MDA 2001, Nygard 2011, Selic 2003, Schmidt 2006 och *Accelerate* (det enda helt korrekta ISBN:et).

## Tabell över alla poster

| Post | Bedömning | Kommentar |
|---|---|---|
| [1] Thoughtworks. *Architecture as Code: The Next Evolution.* Technology Radar, 2024 (rad 7) | FIKTIV? | Ingen sådan blipp finns på Radarn (blipp-URL omdirigerar till kvadrantindex; ingen sökträff). Enda Thoughtworks-källan med namnet är podcasten "Architecture as code" (feb 2025). Länk till 26a_future_trends.md trasig. Citeras även i kap. 29 (saknas i listan). Se R-01. |
| [2] Thoughtworks Technology Radar. *Governance as Code.* Vol. 21, Nov 2019 (rad 8) | FIKTIV? / FÖRÅLDRAD URL | Ingen blipp "Governance as code" existerar (URL /radar/techniques/governance-as-code omdirigerar till kvadrantindex). Vol. 21-blippen heter "Security policy as code" (Trial nov 2019, Trial maj 2020, Adopt okt 2020). Angiven URL omdirigerar till generisk nyhetssida. Kap. 03/08/11/26a daterar källan 2024, kap. 33 2019. Kap. 23 citerar den inte. Se R-02. |
| [3] Atlassian. *Git Workflows for Architecture as Code* (rad 9) | FELCITERAT | Sidan heter "Comparing Workflows" (Atlassian Git Tutorial) och nämner inte Architecture as Code. URL OK (200). Se R-17. |
| [4] GitHub Docs. *About protected branches* (rad 10) | OK (länkfel) | Titel/URL korrekt (200). Länk "Chapter 20" → 20_team_structures.md finns inte (kap. 20 = 20_ai_agent_team.md, citerar via URL). "Chapter 14/23"-titlar avviker från book_index. |
| [5] HashiCorp. *What is Terraform* (rad 11) | OK | Titel/URL korrekt. Kap. 07 citerar samma källa under titeln "Introduction to Infrastructure as Code with Terraform" (inkonsekvent). |
| [6] CNCF. *Cloud Native Definition.* CNCF GitHub (rad 12) | OK | DEFINITION.md finns (v1.1, godkänd av TOC 2024-02-26). Kap. 08 citerar den inte (falsk "Referenced in"). |
| [7] CNCF. *State of Cloud Native Development 2024* (rad 13) | TVEKSAMT | Rapportserien är SlashData:s (för CNCF). CNCF:s rapportlistor visar utgåvor Q1 2025, nov 2025 (Q3 2025), Q1 2026 – ingen 2024-utgåva kunde verifieras. CNCF:s egen 2024-rapport heter "Cloud Native 2024: Approaching a Decade of Code, Cloud, and Change". Länk 26a_future_trends.md trasig. Se R-21. |
| [8] Beyer et al. *The Site Reliability Workbook.* O'Reilly 2018, ISBN 978-1-4920-2974-8 (rad 14) | FEL (ISBN) | ISBN klarar kontrollsiffran men finns inte registrerat (Open Library 404, inga handelsträffar). Korrekt tryckt ISBN: 978-1-492-02950-2. Redaktörer: Beyer, Murphy, Rensin, Kawahara, Thorne. Se R-10. |
| [9] AWS. *AWS CDK Developer Guide* (rad 15) | OK | URL 200, "What is the AWS CDK? – AWS CDK v2". |
| [10] OPA. *Policy as Code Overview.* CNCF OPA Project (rad 16) | OK (titel parafras, länkfel) | URL 200 (sidtitel "Open Policy Agent (OPA)"). Länkar 10_policy_as_code.md och 32_index.md finns inte. Kap. 30 citerar källan men saknas. Kapitlen citerar källan under tre olika titlar (kap. 02/22: "Policy as Code: Expressing Requirements as Code"; kap. 13: "Policy Testing Best Practices for Infrastructure as Code"). |
| [11] NIST SP 800-53 Rev. 5, 2020 (rad 17) | OK (ref-lista fel) | Titel korrekt (originalstavning "Organizations"), sept 2020 (uppd. dec 2020). Kap. 11 och 12 citerar inte källan; kap. 09b och 10 gör det men saknas. |
| [12] Microsoft Learn. *Design multi-stage release pipelines with approvals* (rad 18) | TVEKSAMT | Ingen Learn-sida med denna titel. Närmaste: "Pipeline deployment approvals", "Understand release gates, checks, and approvals", "Tutorial: Create a multistage pipeline with Azure DevOps". Ingen URL angiven; citeras 6 ggr i kap. 05. Se R-18. |
| [13] Kubernetes. *Kubernetes Documentation: Concepts* (rad 19) | OK | URL 200. Kap. 30 citerar men saknas i listan. |
| [14] ISO/IEC 27001:2022 *Information Security Management* (rad 20) | OK (titel förkortad, ref-lista fel) | Standarden finns (3:e uppl., okt 2022); fullständig titel "Information security, cybersecurity and privacy protection — Information security management systems — Requirements" (iso.org ej hämtbar: Cloudflare 403). Kap. 12 och 15a citerar inte källan; kap. 09, 09b, 24 gör det men saknas. |
| [15] Pulumi. *Testing Infrastructure as Code Programs.* Pulumi Blog, 2024 (rad 21) | FELCITERAT | Inget blogginlägg med den titeln. Närmaste: Duffy, J. "Testing Your Infrastructure as Code with Pulumi", Pulumi Blog, 17 apr 2019 (markerat inaktuellt) och dokumentationen "Testing Pulumi programs". Kap. 14 citerar men saknas. Se R-19. |
| [16] HashiCorp. *Securing Terraform State* (rad 22) | TVEKSAMT / FÖRÅLDRAD URL | Sidan hette "Sensitive Data in State"; URL omdirigerar nu till "Manage sensitive data in your configuration" (…/language/manage-sensitive-data). Titeln är påhittad. Kap. 04 och 14 citerar men saknas. |
| [17] HashiCorp. *Backend Type: s3* (rad 23) | OK | URL 200, titel exakt. |
| [18] Microsoft Learn. *Store Terraform state in Azure Storage* (rad 24) | OK | Sidan finns (learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage); URL saknas i posten. |
| [19] Google Cloud. *Store Terraform state in Cloud Storage* (rad 25) | OK | 200; sidan heter nu "Store Terraform state in a Cloud Storage bucket" (omdirigeras till docs.cloud.google.com). |
| [20] HashiCorp. *Terraform Security Best Practices.* 2023 (rad 26) | FELCITERAT | URL 200 men sidan heter "Learn Terraform recommended practices" (HCP Terraform-dokumentation) – inte en säkerhetsguide. Kap. 10 citerar men saknas. Se R-20. |
| [21] Write the Docs. *Docs as Code* (rad 27) | OK | 200, "Docs as code — Write the Docs". |
| [22] Jenkins. *Pipeline Overview* (rad 28) | OK | 200, sidan "Pipeline" i Jenkins User Handbook. |
| [23] GitHub. *Understanding GitHub Actions* (rad 29) | OK (Låg) | URL går till Actions-landningssidan; sidan "Understanding GitHub Actions" ligger på /en/actions/get-started/understand-github-actions. |
| [24] Microsoft. *What is Azure Pipelines?* (rad 30) | OK | 200, titel exakt. |
| [25] GitLab. *Get started with GitLab CI/CD* (rad 31) | OK | 200 (omdirigeras till docs.gitlab.com/ci/), titel exakt. |
| [26] HashiCorp. *Write Terraform Tests* (rad 32) | OK (Låg) | URL går till referenssidan "Tests – Configuration Language"; handledningen "Write Terraform Tests" ligger på /terraform/tutorials/configuration-language/test. |
| [27] GDPR.eu. *GDPR for Organisations: Practical Guide* (rad 33) | FÖRÅLDRAD URL / TVEKSAMT | URL ger 404 och har ingen Wayback-ögonblicksbild (har sannolikt aldrig funnits). Titeln finns inte på gdpr.eu. Se R-22. |
| [28] DORA. *Accelerate State of DevOps Report 2023* (rad 34) | OK | 200, "DORA \| Accelerate State of DevOps Report 2023". |
| [29] Red Hat. *Architecture as Code Principles and Best Practices.* Red Hat Developer, 2023 (rad 35) | FIKTIV? / FÖRÅLDRAD URL | Ingen Red Hat-publikation med denna titel. URL ger 404; sidan "What is Infrastructure as Code (IaC)?" finns på /en/topics/automation/what-is-infrastructure-as-code-iac och handlar om IaC, inte AaC. Se R-03. |
| [30] Skelton & Pais. *Team Topologies.* IT Revolution 2019, ISBN 978-1-942788-81-4 (rad 36) | FEL (ISBN) | ISBN klarar inte kontrollsiffran (summa 132). Korrekt: 978-1-942788-81-2 (paperback, 17 sep 2019). Originaltitel stavas "Organizing". Se R-11. |
| [31] Forsgren, Humble & Kim. *Accelerate.* IT Revolution 2018, ISBN 978-1-942788-33-1 (rad 37) | OK | Open Library: Accelerate, IT Revolution Press, 27 mar 2018 – enda helt korrekta ISBN:et. |
| [32] Bass, Clements & Kazman. *Software Architecture in Practice* 4 uppl., Addison-Wesley 2021, ISBN 978-0-13-688580-4 (rad 38) | FEL (ISBN) | ISBN klarar inte kontrollsiffran (summa 113). Korrekt tryckt ISBN: 978-0-13-688609-9 (Addison-Wesley Professional, 2021). Se R-12. |
| AaC Open Source Project. *Architecture-as-Code Repository.* github.com/finos/architecture-as-code (rad 42) | OK | Repot finns (FINOS Graduated; CALM-specifikation och verktyg). "Chapter 6"-titel avviker från book_index. |
| Architecture Decision Records Community. *ADR Guidelines and Templates.* adr.github.io (rad 45) | OK (Låg) | 200, sidtitel "Architectural Decision Records (ADRs)"; posttitel är parafras. |
| Write the Docs (rad 48) | OK | Korshänvisning till [21]. |
| Brown, S. *C4 Model Overview.* c4model.com (rad 51) | OK (ref-lista fel) | 200. Kap. 24 citerar inte c4model; kap. 22 gör det men saknas. Sidans titel: "The C4 model for visualising software architecture". |
| Brown, S. *Documenting Software Architecture with Structurizr.* Structurizr Blog, 2022 (rad 54) | FIKTIV? | blog.structurizr.com svarar inte (DNS) och URL:en som kap. 06 anger har ingen Wayback-ögonblicksbild; inget inlägg med titeln på dev.to/simonbrown (närmast: "Diagrams as code 2.0", 13 maj 2021). Kap. 24 citerar den inte. Se R-07. |
| Brown, S. *Software Architecture for Developers.* Leanpub, 2022 (rad 57) | OK (Låg) | Leanpub-sidan finns (200). Kap. 06 anger 2024, kap. 33 2022 – inkonsekvent. Verket är två volymer. |
| Chung, Nixon, Yu & Mylopoulos. *Non-Functional Requirements in Software Engineering.* Springer 2000, ISBN 978-0-7923-8666-6 (rad 60) | FEL (ISBN) | ISBN klarar inte kontrollsiffran (summa 139). Korrekt: 978-0-7923-8666-7 (inbunden, Kluwer Academic Publishers, Boston, 2000; nu Springer US, DOI 10.1007/978-1-4615-5269-7). Se R-13. |
| CNCF. *State of Cloud Native Development 2024* (rad 63) | TVEKSAMT | Korshänvisning till [7]; samma problem. |
| FINOS. *CALM: Common Architecture Language Model.* calm.finos.org (rad 66) | OK | 200, "Common Architecture Language Model \| Architecture as Code". Kap. 32 citerar men saknas i listan. |
| Ford, Parsons & Kua. *Building Evolutionary Architectures.* O'Reilly 2017, ISBN 978-1-491-98634-9 (rad 69) | FEL (ISBN) | ISBN klarar kontrollsiffran men är oregistrerat (Open Library 404, inga handelsträffar). Korrekt: 978-1-491-98636-3 (1 uppl., O'Reilly, sep/okt 2017). Se R-14. |
| Forsberg & Mooz. *The Relationship of System Engineering to the Project Cycle.* Engineering Management Journal, 1991 (rad 72) | FEL (venue/år) | 1991-versionen publicerades i Proc. 1st Annual NCOSE Symposium (INCOSE Int. Symposium 1(1):57–65, okt 1991, DOI 10.1002/j.2334-5837.1991.tb01484.x). EMJ-versionen är 1992, 4(3):36–43, med titeln "…Systems Engineering…" (DOI 10.1080/10429247.1992.11414684). Se R-15. |
| GitLab. *Documentation as Code: Best Practices and Implementation.* GitLab Documentation, 2024 (rad 75) | FIKTIV? | Ingen GitLab-sida med denna titel kunde hittas (GitLab:s egna dokumentationsriktlinjer heter "Documentation" / "GitLab documentation guidelines"). Ingen URL. Se R-04. |
| GitLab. *Building a Single Source of Truth with APIs and CLI.* GitLab Topics, 2024 (rad 78) | FIKTIV? | Ingen träff någonstans; citeras dessutom inte i något kapitel (kap. 02 och 11 saknar posten). Se R-05. |
| GitHub Docs. *About protected branches* (rad 81) | OK | Korshänvisning till [4]. |
| GitHub Open Source Community. *Collaborative Software Development.* Platform Documentation, 2024 (rad 84) | FIKTIV? | Ingen sådan publikation; "GitHub Open Source Community" är inte en utgivare. Se R-06. |
| IEEE. *IEEE Standard for Software Verification and Validation.* IEEE Std 1012-2016, 2017 (rad 87) | FEL (titel) | IEEE 1012-2016 heter "IEEE Standard for System, Software, and Hardware Verification and Validation" (godkänd 2016-05-15, publicerad 2017-09-29; ersatt av IEEE 1012-2024). Angiven titel är 1998/2004-utgåvans. Se R-16. |
| HashiCorp. *Policy as Code Overview.* …/cloud-docs/policy-enforcement (rad 90) | OK (Låg) | 200, sidtitel "Policy enforcement overview". Kap. 20 citerar men saknas i listan. |
| Kvadrat AB. *Gunnar Nordqvist – Chief Architect Profile* (rad 93) | FÖRÅLDRAD URL | URL ger 404 (Wayback har ögonblicksbild 2026-01-19 med status 200, dvs. sidan har funnits). Se R-23. |
| Kvadrat AB. *Technology Consulting Excellence.* Company Profile, 2024 (rad 96) | TVEKSAMT | kvadrat.se svarar 200 men heter "Sveriges vassaste konsulter \| Kvadrat"; "Technology Consulting Excellence" är en påhittad titel på en startsida. Se R-24. |
| MarketsandMarkets. *Infrastructure as Code Market Report.* 2023 (rad 99) | TVEKSAMT (år) | Rapporten finns: "Infrastructure as Code (IaC) Market … Global Forecast to 2027", rapportkod TC 8140, aug 2022; pressmeddelande 3 maj 2023. Se R-25. |
| Martin, R.C. *Clean Architecture.* Prentice Hall 2017, ISBN 978-0-13-468599-1 (rad 102) | FEL (ISBN → annat verk) | ISBN 9780134685991 = *Effective Java*, 3:e uppl., Joshua Bloch (Addison-Wesley, dec 2017). Korrekt: 978-0-13-449416-6. Kap. 01/02 anger trunkerad titel. Se R-09. |
| Mermaid. *Mermaid: Diagramming and Charting Tool* (rad 105) | OK | 200, "Mermaid \| Diagramming and charting tool". |
| NIST. *Requirements Engineering for Secure Systems.* NIST SP 800-160, 2023 (rad 108) | FEL (titel/år) | SP 800-160 Vol. 1 Rev. 1 = "Engineering Trustworthy Secure Systems" (nov 2022); Vol. 2 Rev. 1 = "Developing Cyber-Resilient Systems: A Systems Security Engineering Approach" (dec 2021). Ingen volym heter som angivet; ingen 2023-utgåva. Se R-08. |
| Nygard, M. *Documenting Architecture Decisions.* 2011 (rad 111) | OK (Låg) | Bekräftat: Michael Nygard, 15 nov 2011, cognitect.com/blog/2011/11/15/documenting-architecture-decisions. URL saknas i posten. |
| Open Policy Agent (rad 114) | OK | Korshänvisning till [10]. |
| OMG. *Model Driven Architecture (MDA).* OMG White Paper, 2001 (rad 117) | OK (Låg) | OMG-dokument ormsc/2001-07-01 "Model Driven Architecture (MDA)" finns i OMG:s arkiv (omg.org/cgi-bin/doc?ormsc/2001-07-01); red. J. Miller & J. Mukerji, 9 juli 2001. Lägg till dokumentnummer. |
| PlantUML (rad 120) | OK | 200. |
| Red Hat (rad 123) | FIKTIV? | Korshänvisning till [29]; samma problem. |
| Richardson, C. *Microservices Patterns: With Examples in Java.* Manning 2018, ISBN 978-1-617-29454-1 (rad 126) | FEL (ISBN) | ISBN klarar inte kontrollsiffran (summa 102). Korrekt: 978-1-61729-454-9 (Manning, nov 2018). Se R-13. |
| Schmidt, D.C. *Model-Driven Engineering.* IEEE Computer, 2006 (rad 129) | OK (Låg) | Crossref: "Guest Editor's Introduction: Model-Driven Engineering", Computer 39(2):25–31, feb 2006, DOI 10.1109/MC.2006.58. Lägg till vol/nr/sidor. |
| Selic, B. *The Pragmatics of Model-Driven Development.* IEEE Software, 2003 (rad 132) | OK (ref-lista fel) | Crossref: IEEE Software 20(5):19–25, sep/okt 2003, DOI 10.1109/MS.2003.1231146. Citeras endast i kap. 02 – inte i kap. 06 eller 23. |
| Structurizr. *Structurizr DSL Language Reference.* github.com/structurizr/dsl (rad 135) | FÖRÅLDRAD URL | Repot github.com/structurizr/dsl finns inte längre (404). Koden flyttades till structurizr/java (arkiverat 2026-03-28) och vidare till github.com/structurizr/structurizr; språkreferensen ligger på docs.structurizr.com/dsl. Kap. 30 citerar men saknas i listan. Se R-26. |
| Structurizr. *Structurizr Lite.* docs.structurizr.com/lite (rad 138) | OK | 200. |
| Thoughtworks Technology Radar. *Diagrams as Code* (rad 141) | OK (Låg) | Blippen finns: "Diagrams as code", Techniques, Trial, Vol. 23 (okt 2020) – enda förekomst. Datum saknas i posten. |
| Thoughtworks. *Architecture as Code: The Next Evolution* (rad 144) | FIKTIV? | Korshänvisning till [1]. |
| Thoughtworks. *Architecture Decision Records.* Technology Radar, 2023 (rad 147) | FEL (titel/år) | Blippen heter "Lightweight Architecture Decision Records": Trial nov 2016 (Vol. 15) och mar 2017, Adopt nov 2017 och maj 2018 (Vol. 18); inte på Radarn 2023. Se R-27. |
| Thoughtworks Technology Radar. *Governance as Code* (rad 150) | FIKTIV? | Korshänvisning till [2]. |
| Nordqvist, G. *Architecture as Code: practitioner experience … 2019–2024* (rad 155) | TVEKSAMT | Inte en publikation ("Author's own professional practice … available on request"). Hör inte hemma i en källförteckning. Se R-28. |
| Gartner. *Forecast Analysis: Public Cloud Services Worldwide.* 2024 (rad 157) | TVEKSAMT | Gartner publicerar serien, men 2024-dokumentet som pressmeddelandet 20 maj 2024 citerar heter "Forecast: Public Cloud Services, Worldwide, 2022-2028, 1Q24 Update" (betalvägg). Kap. 17 citerar inte källan; kap. 25 gör det men saknas. Se R-29. |
| IDC. *Worldwide DevOps Software Tools Forecast, 2023–2027.* 2023 (rad 161) | TVEKSAMT | IDC-serien finns (DevSecOps 2023–2027 och DevOps 2024–2028 bekräftade via återförsäljarlistor), men just DevOps-utgåvan 2023–2027 kunde inte lokaliseras; inget dokumentnummer. Kap. 05 och 21 citerar inte källan; kap. 15 och 25 gör det men saknas. Se R-29. |
| HashiCorp. *State of Cloud Strategy Survey 2024* (rad 164) | OK (ref-lista fel) | Finns: HashiCorp 2024 State of Cloud Strategy Survey (Forrester Consulting, 27 jun 2024, hashicorp.com/state-of-the-cloud). Varken kap. 17 eller 27 citerar den. Se R-30. |
| Microsoft Learn. *Store Terraform state in Azure Storage* (rad 167) | OK | Korshänvisning till [18]. Kapitelrubrik "Chapter 9b: Security Patterns and Implementation" avviker från rad 22–26 ("Advanced …") och book_index. |

## Fynd

### R-01 Fiktiv Thoughtworks-källa "Architecture as Code: The Next Evolution"
- **Fil:rad:** docs/33_references.md:7 (även rad 144–145)
- **Post:** "Thoughtworks. *Architecture as Code: The Next Evolution.* Technology Radar, 2024."
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv
- **Allvarlighet:** Hög
- **Evidens:** Thoughtworks Technology Radar har ingen blipp med detta eller liknande namn; https://www.thoughtworks.com/radar/techniques/architecture-as-code omdirigerar till kvadrantindexet https://www.thoughtworks.com/radar/techniques (kontrollerat 2026-10-30). Sökning på thoughtworks.com ger endast Technology Podcast-avsnittet "Architecture as code" (Prem Chandrasekaran med Neal Ford och Mark Richards, 19 feb 2025, https://www.thoughtworks.com/en-us/insights/podcasts/technology-podcasts/architecture-as-code). Källan är bokens mest citerade (kap. 01, 02, 04, 05, 26a, 29, 32).
- **Förslag:** Ta bort posten, eller ersätt med den verkliga källan om det är podcasten som avses: "Thoughtworks Technology Podcast. *Architecture as code.* Thoughtworks, 19 februari 2025. https://www.thoughtworks.com/insights/podcasts/technology-podcasts/architecture-as-code". Uppdatera "Referenced in" (lägg till kap. 29; rätta 26A-länken).

### R-02 Fiktiv Radar-blipp "Governance as Code" (Vol. 21) och död URL
- **Fil:rad:** docs/33_references.md:8 (även rad 150–151)
- **Post:** "Thoughtworks Technology Radar. *Governance as Code.* Vol. 21, November 2019. Available at: …/about-us/news/2019/technology-radar-edition21"
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv; FÖRÅLDRAT (URL); INKONSEKVENT (år)
- **Allvarlighet:** Hög
- **Evidens:** https://www.thoughtworks.com/radar/techniques/governance-as-code omdirigerar till kvadrantindexet – blippen finns inte. Vol. 21 (nov 2019) innehåller i stället "Security policy as code" (Techniques, Trial), som enligt blippsidan https://www.thoughtworks.com/radar/techniques/security-policy-as-code publicerades 20 nov 2019 (Trial), maj 2020 (Trial) och okt 2020 (Adopt). Vol. 21:s temaöversikt talar om "policy, compliance and governance as code" som ett återkommande tema (citat ur PDF via sökträff; PDF:en svarade 503 vid direkt hämtning). Angiven URL svarar 200 men omdirigerar till https://www.thoughtworks.com/about-us/news (generisk nyhetssida utan koppling). Kapitlen 03, 08, 11 och 26a daterar källan "(2024)" medan kap. 33 anger 2019.
- **Förslag:** Ersätt med: "Thoughtworks Technology Radar. *Security policy as code.* Techniques, Trial, Vol. 21, November 2019 (Adopt, Vol. 23, Oktober 2020). https://www.thoughtworks.com/radar/techniques/security-policy-as-code". Ändra årtalen i kap. 03/08/11/26a, ta bort kap. 23 från "Referenced in" och rätta 26A-länken.

### R-03 Fiktiv Red Hat-titel, URL ger 404 och handlar om IaC
- **Fil:rad:** docs/33_references.md:35 (även rad 123–124)
- **Post:** "Red Hat. *Architecture as Code Principles and Best Practices.* Red Hat Developer, 2023. …/topics/devops/what-is-infrastructure-as-code"
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv; FÖRÅLDRAT (URL)
- **Allvarlighet:** Hög
- **Evidens:** Ingen Red Hat-publikation med titeln hittas (Red Hat Developer, redhat.com/topics, cloud.redhat.com/experts). Angiven URL ger HTTP 404 ("404 - Red Hat"). Den sida som sannolikt avsågs finns på https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac med titeln "What is Infrastructure as Code (IaC)?" (200) och behandlar IaC, inte Architecture as Code. Kap. 01 och 02 bygger på källan.
- **Förslag:** "Red Hat. *What is Infrastructure as Code (IaC)?* Red Hat Topics. https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac" – och se över de påståenden i kap. 01–02 som tillskrivs Red Hat om AaC-principer.

### R-04 Fiktiv GitLab-publikation "Documentation as Code: Best Practices and Implementation"
- **Fil:rad:** docs/33_references.md:75
- **Post:** "GitLab. *Documentation as Code: Best Practices and Implementation.* GitLab Documentation, 2024."
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv
- **Allvarlighet:** Hög
- **Evidens:** Ingen sida med titeln på docs.gitlab.com eller about.gitlab.com (sökt: exakt titel, "docs as code" GitLab). GitLab:s faktiska dokumentation om ämnet är "GitLab documentation guidelines" (https://docs.gitlab.com/development/documentation/), som beskriver dokumentationen som "single source of truth" och docs-as-code-arbetsflödet. Posten har ingen URL.
- **Förslag:** Ersätt med "GitLab. *Documentation guidelines.* GitLab Docs. https://docs.gitlab.com/development/documentation/" eller stryk och låt Write the Docs [21] bära påståendet.

### R-05 Fiktiv GitLab-publikation "Building a Single Source of Truth with APIs and CLI" – citeras inte ens
- **Fil:rad:** docs/33_references.md:78–79
- **Post:** "GitLab. *Building a Single Source of Truth with APIs and CLI.* GitLab Topics, 2024. Referenced in: Chapter 2, Chapter 11"
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv; FELCITERAT (Referenced in)
- **Allvarlighet:** Hög
- **Evidens:** Inga träffar på titeln någonstans (GitLab Topics, docs, blogg). `grep -ril "Single Source of Truth with APIs" docs/` ger noll träffar utanför kap. 33 – varken kap. 02 eller kap. 11 citerar posten.
- **Förslag:** Stryk posten.

### R-06 Fiktiv källa "GitHub Open Source Community. Collaborative Software Development"
- **Fil:rad:** docs/33_references.md:84–85
- **Post:** "GitHub Open Source Community. *Collaborative Software Development.* Platform Documentation, 2024."
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv
- **Allvarlighet:** Hög
- **Evidens:** "GitHub Open Source Community" är ingen utgivare, "Platform Documentation" ingen publikation, och GitHub Docs har ingen sida med titeln (sökt exakt fras). Citeras bara i kap. 29 (Om författaren).
- **Förslag:** Stryk, eller ersätt med en verklig sida, t.ex. "GitHub Docs. *Collaborating with pull requests.* https://docs.github.com/en/pull-requests/collaborating-with-pull-requests".

### R-07 Oåterfinnbar bloggpost "Documenting Software Architecture with Structurizr" (Structurizr Blog, 2022)
- **Fil:rad:** docs/33_references.md:54–55
- **Post:** "Brown, S. *Documenting Software Architecture with Structurizr.* Structurizr Blog, 2022. Referenced in: Chapter 6, Chapter 24"
- **Bedömning:** EJ VERIFIERBART – sannolikt fiktiv; FELCITERAT (Referenced in)
- **Allvarlighet:** Hög
- **Evidens:** Värden blog.structurizr.com svarar inte alls (curl 000, ingen DNS-upplösning); URL:en som kap. 06 anger (blog.structurizr.com/diagrams-as-code-automation/) har ingen ögonblicksbild i Wayback Machine (availability-API: "no snapshot"). Simon Browns bloggflöde https://dev.to/simonbrown innehåller inget inlägg med titeln; närmast är "Diagrams as code 2.0" (13 maj 2021), "Diagrams as code" (28 okt 2020) och "A minimal approach to software architecture documentation" (16 jul 2020). Kap. 24 citerar inte posten.
- **Förslag:** Ersätt med "Brown, S. *Diagrams as code 2.0.* dev.to, 13 maj 2021. https://dev.to/simonbrown/diagrams-as-code-2-0-…" (verifiera slug) eller med Structurizr-dokumentationen https://docs.structurizr.com/; ta bort kap. 24 ur "Referenced in".

### R-08 Fel titel och år för NIST SP 800-160
- **Fil:rad:** docs/33_references.md:108–109
- **Post:** "NIST. *Requirements Engineering for Secure Systems.* NIST Special Publication 800-160, 2023."
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** NIST CSRC: SP 800-160 Vol. 1 Rev. 1 "Engineering Trustworthy Secure Systems", Ross, Winstead, McEvilley, november 2022 (https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final); SP 800-160 Vol. 2 Rev. 1 "Developing Cyber-Resilient Systems: A Systems Security Engineering Approach", december 2021 (https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final). Ingen volym heter "Requirements Engineering for Secure Systems" och ingen utgåva är från 2023. Samma felaktiga titel står i kap. 02:s Sources.
- **Förslag:** "Ross, R., Winstead, M. & McEvilley, M. *Engineering Trustworthy Secure Systems.* NIST Special Publication 800-160, Vol. 1, Rev. 1. NIST, november 2022. https://doi.org/10.6028/NIST.SP.800-160v1r1" – och rätta kap. 02.

### R-09 ISBN för *Clean Architecture* pekar på *Effective Java*
- **Fil:rad:** docs/33_references.md:102 (även kap. 01 rad 95–96)
- **Post:** "Martin, R.C. *Clean Architecture…* Prentice Hall, 2017. ISBN: 978-0-13-468599-1"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Open Library https://openlibrary.org/isbn/9780134685991.json → "Effective Java", 3rd Edition, Addison-Wesley Professional, 27 dec 2017 (Joshua Bloch). Korrekt ISBN https://openlibrary.org/isbn/9780134494166.json → "Clean Architecture: A Craftsman's Guide to Software Structure and Design", Pearson (Prentice Hall-imprint), 10 sep 2017.
- **Förslag:** "Martin, R.C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design.* Prentice Hall (Pearson), 2017. ISBN 978-0-13-449416-6" – samt fullständig titel i kap. 01/02 (där står "…Software Structure." utan "and Design").

### R-10 Fel ISBN för *The Site Reliability Workbook*
- **Fil:rad:** docs/33_references.md:14
- **Post:** "Beyer, B. et al. (Google LLC). *The Site Reliability Workbook…* O'Reilly Media, 2018. ISBN: 978-1-4920-2974-8"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** 9781492029748 klarar kontrollsiffran men är inte registrerat (Open Library 404; inga förlags- eller handelsträffar). Tryckt utgåva: Open Library https://openlibrary.org/isbn/9781492029502.json → "The Site Reliability Workbook: Practical Ways to Implement SRE", O'Reilly Media, aug 2018. Redaktörer: Beyer, Murphy, Rensin, Kawahara & Thorne.
- **Förslag:** "Beyer, B., Murphy, N.R., Rensin, D.K., Kawahara, K. & Thorne, S. (red.). *The Site Reliability Workbook: Practical Ways to Implement SRE.* O'Reilly Media, 2018. ISBN 978-1-492-02950-2".

### R-11 Fel ISBN (ogiltig kontrollsiffra) för *Team Topologies*
- **Fil:rad:** docs/33_references.md:36
- **Post:** "Skelton, M. & Pais, M. *Team Topologies: Organising…* IT Revolution Press, 2019. ISBN: 978-1-942788-81-4"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** 9781942788814 klarar inte ISBN-13-kontrollen (viktad summa 132). Open Library https://openlibrary.org/isbn/9781942788812.json → "Team Topologies: Organizing Business and Technology Teams for Fast Flow", IT Revolution Press, paperback, 17 sep 2019.
- **Förslag:** "Skelton, M. & Pais, M. *Team Topologies: Organizing Business and Technology Teams for Fast Flow.* IT Revolution Press, 2019. ISBN 978-1-942788-81-2" (behåll originalets amerikanska stavning i titeln).

### R-12 Fel ISBN (ogiltig kontrollsiffra) för *Software Architecture in Practice*, 4 uppl.
- **Fil:rad:** docs/33_references.md:38
- **Post:** "Bass, L., Clements, P. & Kazman, R. *Software Architecture in Practice* (4th ed.). Addison-Wesley, 2021. ISBN: 978-0-13-688580-4"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** 9780136885804 klarar inte kontrollsiffran (summa 113) och finns inte i någon katalog. Open Library https://openlibrary.org/isbn/9780136886099.json → "Software Architecture in Practice", Pearson Education, 2021; återförsäljare bekräftar 4:e upplagan, Addison-Wesley Professional (ISBN-10 0136886094).
- **Förslag:** "… (4th ed.). Addison-Wesley Professional, 2021. ISBN 978-0-13-688609-9".

### R-13 Fel ISBN för Chung et al. och Richardson (ogiltiga kontrollsiffror)
- **Fil:rad:** docs/33_references.md:60 och 126
- **Post:** "Chung … Springer, 2000. ISBN: 978-0-7923-8666-6" och "Richardson, C. *Microservices Patterns…* Manning, 2018. ISBN: 978-1-617-29454-1"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** 9780792386666 (summa 139) och 9781617294541 (summa 102) klarar inte ISBN-13-kontrollen. Open Library https://openlibrary.org/isbn/9780792386667.json → "Non-Functional Requirements in Software Engineering" (Kluwer International Series in Software Engineering vol. 5), inbunden; Crossref DOI 10.1007/978-1-4615-5269-7 (Springer US, 2000; e-bok 978-1-4615-5269-7). Open Library https://openlibrary.org/isbn/9781617294549.json → "Microservices Patterns: With examples in Java", Manning Publications, 19 nov 2018.
- **Förslag:** "Chung, L., Nixon, B.A., Yu, E. & Mylopoulos, J. *Non-Functional Requirements in Software Engineering.* Kluwer Academic Publishers (Springer), 2000. ISBN 978-0-7923-8666-7" och "Richardson, C. *Microservices Patterns: With Examples in Java.* Manning Publications, 2018. ISBN 978-1-61729-454-9".

### R-14 Fel ISBN för *Building Evolutionary Architectures*
- **Fil:rad:** docs/33_references.md:69
- **Post:** "Ford, N., Parsons, R. & Kua, P. *Building Evolutionary Architectures: Support Constant Change.* 1st ed. O'Reilly Media, 2017. ISBN: 978-1-491-98634-9"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** 9781491986349 klarar kontrollsiffran men är oregistrerat (Open Library 404; inga träffar). Open Library https://openlibrary.org/isbn/9781491986363.json → "Building Evolutionary Architectures: Support Constant Change", O'Reilly Media, 8 okt 2017 (O'Reilly-katalogen: sep 2017).
- **Förslag:** "… O'Reilly Media, 2017. ISBN 978-1-491-98636-3".

### R-15 Forsberg & Mooz: fel tidskrift/år-kombination
- **Fil:rad:** docs/33_references.md:72 (även kap. 02 Sources)
- **Post:** "Forsberg, K., Mooz, H. *The Relationship of System Engineering to the Project Cycle.* Engineering Management Journal, 1991."
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Crossref: (a) "The Relationship of System Engineering to the Project Cycle", INCOSE International Symposium (Proc. 1st Annual NCOSE Symposium, Chattanooga) 1(1):57–65, oktober 1991, DOI 10.1002/j.2334-5837.1991.tb01484.x; (b) "The Relationship of Systems Engineering to the Project Cycle", Engineering Management Journal 4(3):36–43, september 1992, DOI 10.1080/10429247.1992.11414684. Posten blandar titel/år från (a) med venue från (b).
- **Förslag:** "Forsberg, K. & Mooz, H. (1991). *The Relationship of System Engineering to the Project Cycle.* Proceedings of the First Annual Symposium of the National Council on Systems Engineering (NCOSE), Chattanooga, TN, oktober 1991, s. 57–65. https://doi.org/10.1002/j.2334-5837.1991.tb01484.x".

### R-16 Fel titel på IEEE Std 1012-2016
- **Fil:rad:** docs/33_references.md:87 (även kap. 02 Sources)
- **Post:** "IEEE. *IEEE Standard for Software Verification and Validation.* IEEE Std 1012-2016, 2017."
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** IEEE Standards Association https://standards.ieee.org/ieee/1012/5609/: "IEEE 1012-2016 – IEEE Standard for System, Software, and Hardware Verification and Validation", godkänd 2016-05-15, publicerad 2017-09-29, status "Superseded" (ersatt av IEEE 1012-2024). Den angivna titeln tillhör 1998/2004-utgåvorna.
- **Förslag:** "IEEE. *IEEE Standard for System, Software, and Hardware Verification and Validation.* IEEE Std 1012-2016. IEEE, 2017 (ersatt av IEEE Std 1012-2024)."

### R-17 Påhittad titel för Atlassian-sidan
- **Fil:rad:** docs/33_references.md:9
- **Post:** "Atlassian. *Git Workflows for Architecture as Code.* Atlassian Git Documentation, 2024."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** https://www.atlassian.com/git/tutorials/comparing-workflows (200) har sidtiteln "Git Workflow | Atlassian Git Tutorial" och rubriken "Comparing Workflows"; sidan nämner inte Architecture as Code.
- **Förslag:** "Atlassian. *Comparing Git workflows.* Atlassian Git Tutorial. https://www.atlassian.com/git/tutorials/comparing-workflows".

### R-18 Microsoft Learn-titel som inte finns (citeras 6 gånger i kap. 05)
- **Fil:rad:** docs/33_references.md:18
- **Post:** "Microsoft Learn. *Design multi-stage release pipelines with approvals.* Microsoft Learn Documentation, 2024."
- **Bedömning:** EJ VERIFIERBART / FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Ingen Learn-sida med titeln. Verkliga sidor: "Pipeline deployment approvals" (https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals, 200), "Understand release gates, checks, and approvals" (https://learn.microsoft.com/en-us/azure/devops/pipelines/release/approvals/, 200), "Tutorial: Create a multistage pipeline with Azure DevOps" (https://learn.microsoft.com/en-us/azure/devops/pipelines/process/create-multistage-pipeline, 200). Posten saknar URL.
- **Förslag:** "Microsoft Learn. *Pipeline deployment approvals.* Azure Pipelines documentation. https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals" (eller tutorialen om flerstegspipelines, beroende på vad kap. 05 stödjer sig på).

### R-19 Pulumi-bloggpost med påhittad titel och fel år
- **Fil:rad:** docs/33_references.md:21
- **Post:** "Pulumi. *Testing Infrastructure as Code Programs.* Pulumi Blog, 2024."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Inget inlägg med titeln på pulumi.com/blog. Närmaste: Duffy, J. "Testing Your Infrastructure as Code with Pulumi", Pulumi Blog, 17 apr 2019 (https://www.pulumi.com/blog/testing-your-infrastructure-as-code-with-pulumi/, 200) – sidan bär noten "Some parts of this blog post are out-of-date. Please refer to our Testing Guide". Aktuell dokumentation: "Testing Pulumi programs" (https://www.pulumi.com/docs/iac/guides/testing/, 200). Kap. 14 citerar källan men saknas i "Referenced in".
- **Förslag:** "Pulumi. *Testing Pulumi programs.* Pulumi Documentation. https://www.pulumi.com/docs/iac/guides/testing/" och lägg till kap. 14.

### R-20 HashiCorp-titlar som inte motsvarar sidorna ([16], [20])
- **Fil:rad:** docs/33_references.md:22 och 26
- **Post:** "[16] HashiCorp. *Securing Terraform State.* …/language/state/sensitive-data" och "[20] HashiCorp. *Terraform Security Best Practices.* HashiCorp Learning Resources, 2023. …/cloud-docs/recommended-practices"
- **Bedömning:** FELCITERAT / FÖRÅLDRAT (URL [16])
- **Allvarlighet:** Medel
- **Evidens:** [16]: URL:en omdirigerar (200) till https://developer.hashicorp.com/terraform/language/manage-sensitive-data med titeln "Manage sensitive data in your configuration"; den gamla sidan hette "Sensitive Data in State" (Wayback-ögonblicksbild 2025-08-15). [20]: sidan heter "Learn Terraform recommended practices" (HCP Terraform-dokumentation, allmänna rekommendationer – inte en säkerhetsguide). Kap. 04/14 ([16]) och kap. 10 ([20]) citerar men saknas i listorna.
- **Förslag:** "[16] HashiCorp. *Manage sensitive data in your configuration.* Terraform Documentation. https://developer.hashicorp.com/terraform/language/manage-sensitive-data" och "[20] HashiCorp. *Terraform recommended practices.* HCP Terraform Documentation. https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices".

### R-21 CNCF "State of Cloud Native Development 2024" – fel utgivare, utgåva ej verifierad
- **Fil:rad:** docs/33_references.md:13 (även rad 63–64)
- **Post:** "Cloud Native Computing Foundation. *State of Cloud Native Development 2024.* CNCF, 2024."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Serien produceras av SlashData i samarbete med CNCF ("CNCF + SlashData State of Cloud Native Development Report", https://www.cncf.io/reports/state-of-cloud-native-development/). CNCF:s rapportlista (https://www.cncf.io/lf-report-type/survey/, sid 1–2) visar utgåvorna Q1 2025 (25 apr 2025), Q3 2025 (11 nov 2025), Q1 2026 (24 mar 2026) och Japan 2026 – ingen 2024-utgåva. CNCF:s egen 2024-undersökning heter "Cloud Native 2024: Approaching a Decade of Code, Cloud, and Change" (https://www.cncf.io/reports/cncf-annual-survey-2024/). Kap. 01, 07, 08 och 26a bygger på posten.
- **Förslag:** Ange vilken rapport som faktiskt använts, t.ex. "SlashData & CNCF. *State of Cloud Native Development Q1 2025.* CNCF, april 2025. https://www.cncf.io/reports/state-of-cloud-native-development-q1-2025/" eller "CNCF. *Cloud Native 2024: Approaching a Decade of Code, Cloud, and Change* (CNCF Annual Survey 2024). https://www.cncf.io/reports/cncf-annual-survey-2024/". Rätta 26A-länken.

### R-22 GDPR.eu-länk död och titel påhittad
- **Fil:rad:** docs/33_references.md:33
- **Post:** "GDPR.eu. *GDPR for Organisations: Practical Guide.* GDPR.eu, 2024. https://gdpr.eu/for-organizations/"
- **Bedömning:** FÖRÅLDRAT / FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** URL:en ger HTTP 404 ("Page not found - GDPR.eu") och Wayback Machine har ingen ögonblicksbild av den – sidan har sannolikt aldrig funnits. gdpr.eu har bl.a. "Everything you need to know about GDPR compliance" (https://gdpr.eu/compliance/, 200) och "GDPR compliance checklist" (https://gdpr.eu/checklist/, 200).
- **Förslag:** "GDPR.eu. *Everything you need to know about GDPR compliance.* Proton AG. https://gdpr.eu/compliance/" (eller EU-kommissionens officiella sida, som kap. 05 redan citerar).

### R-23 Kvadrat-konsultprofil: URL ger 404
- **Fil:rad:** docs/33_references.md:93 (även kap. 29 Sources)
- **Post:** "Kvadrat AB. *Gunnar Nordqvist – Chief Architect Profile.* … https://www.kvadrat.se/anlita-kvadrat/hitta-konsult/gunnar-nordqvist/"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** HTTP 404 ("404 | Kvadrat") 2026-10-30; Wayback-availability visar en ögonblicksbild 2026-01-19 med status 200, dvs. sidan har funnits men är borttagen/flyttad. Rolltiteln "Chief Architect" kunde inte verifieras.
- **Förslag:** Uppdatera till aktuell profil-URL (eller LinkedIn) eller ange "arkiverad: web.archive.org/web/20260119231653/…".

### R-24 "Technology Consulting Excellence" är ingen publikation
- **Fil:rad:** docs/33_references.md:96
- **Post:** "Kvadrat AB. *Technology Consulting Excellence.* Company Profile, 2024. https://www.kvadrat.se/"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** kvadrat.se (200) har titeln "Sveriges vassaste konsulter | Kvadrat"; frasen "Technology Consulting Excellence" förekommer inte. Posten är en påhittad titel på en startsida.
- **Förslag:** "Kvadrat AB. *Kvadrat – Sveriges vassaste konsulter* [företagswebbplats]. https://www.kvadrat.se/" eller stryk posten (en företagsstartsida hör knappast hemma i en källförteckning).

### R-25 MarketsandMarkets-rapport: fel år, ofullständig titel
- **Fil:rad:** docs/33_references.md:99 (även kap. 15 och 25 Sources)
- **Post:** "MarketsandMarkets. *Infrastructure as Code Market Report.* MarketsandMarkets, 2023."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Rapporten heter "Infrastructure as Code (IaC) Market by Tool, Service, Type, Infrastructure Type, Deployment Mode, Vertical and Region – Global Forecast to 2027", rapportkod TC 8140, augusti 2022 (USD 0,8 mdr 2022 → 2,3 mdr 2027, CAGR 24,0 %); pressmeddelandet via GlobeNewswire är daterat 3 maj 2023.
- **Förslag:** "MarketsandMarkets. *Infrastructure as Code (IaC) Market – Global Forecast to 2027* (rapportkod TC 8140). MarketsandMarkets, augusti 2022. https://www.marketsandmarkets.com/Market-Reports/infrastructure-as-code-market-115458264.html".

### R-26 github.com/structurizr/dsl finns inte längre
- **Fil:rad:** docs/33_references.md:135 (även kap. 06, 22, 30 Sources)
- **Post:** "Structurizr. *Structurizr DSL Language Reference.* https://github.com/structurizr/dsl"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** github.com/structurizr/dsl svarar 404 (WebFetch; raw.githubusercontent 404 för både main/master). Koden flyttades till github.com/structurizr/java (arkiverat 2026-03-28, README: "The code in this repo has been moved to https://github.com/structurizr/structurizr") och språkreferensen ligger på https://docs.structurizr.com/dsl ("DSL | Structurizr", 200). Kap. 30 citerar posten men saknas i "Referenced in".
- **Förslag:** "Structurizr. *Structurizr DSL – language reference.* Structurizr Documentation. https://docs.structurizr.com/dsl (källkod: https://github.com/structurizr/structurizr)". Lägg till kap. 30.

### R-27 Thoughtworks ADR-blipp: fel namn och år
- **Fil:rad:** docs/33_references.md:147 (även kap. 04 Sources)
- **Post:** "Thoughtworks. *Architecture Decision Records.* Technology Radar, 2023."
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Blippen heter "Lightweight Architecture Decision Records" (https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records): Trial nov 2016 (Vol. 15, publicerad 7 nov 2016), Trial mar 2017, Adopt nov 2017, Adopt maj 2018 (Vol. 18) – därefter inte på Radarn. Ingen 2023-förekomst.
- **Förslag:** "Thoughtworks Technology Radar. *Lightweight Architecture Decision Records.* Techniques, Adopt, Vol. 17, November 2017 (först Trial, Vol. 15, November 2016). https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records".

### R-28 Författarens egen praktik listad som källa
- **Fil:rad:** docs/33_references.md:155
- **Post:** "Nordqvist, G. *Architecture as Code: practitioner experience … 2019–2024.* Author's own professional practice. Available on request via the book repository."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Inte en publikation och inte verifierbar; saknar "Referenced in". En källförteckning bör bara innehålla kontrollerbara verk.
- **Förslag:** Stryk posten och förklara i stället i förordet/kap. 29 att erfarenhetsbaserade påståenden bygger på författarens uppdrag.

### R-29 Gartner- och IDC-rapporter: oprecisa titlar och felaktiga "Referenced in"
- **Fil:rad:** docs/33_references.md:157–158 och 161–162
- **Post:** "Gartner. *Forecast Analysis: Public Cloud Services Worldwide.* 2024" / "IDC. *Worldwide DevOps Software Tools Forecast, 2023–2027.* 2023"
- **Bedömning:** TVEKSAMT; FELCITERAT (Referenced in)
- **Allvarlighet:** Medel
- **Evidens:** Gartners pressmeddelande 20 maj 2024 ("Gartner Forecasts Worldwide Public Cloud End-User Spending to Surpass $675 Billion in 2024") hänvisar till dokumentet "Forecast: Public Cloud Services, Worldwide, 2022-2028, 1Q24 Update"; en 2024-rapport med exakt titeln "Forecast Analysis: Public Cloud Services, Worldwide" kunde inte verifieras (betalvägg, gartner.com blockerar hämtning). IDC:s serie finns (bekräftat: "Worldwide DevSecOps Software Tools Forecast, 2023–2027" och "Worldwide DevOps Software Tools Forecast, 2024–2028" via GII-listor) men just DevOps-utgåvan 2023–2027 lokaliserades inte och saknar dokumentnummer. "Referenced in": Gartner citeras i kap. 15 och 25 (inte 17); IDC citeras i kap. 15 och 25 (inte 05 eller 21).
- **Förslag:** Gartner: "Gartner. *Gartner Forecasts Worldwide Public Cloud End-User Spending to Surpass $675 Billion in 2024* [pressmeddelande]. 20 maj 2024. https://www.gartner.com/en/newsroom/press-releases/2024-05-20-…" (eller exakt dokumenttitel + ID). IDC: lägg till IDC-dokumentnummer och publiceringsmånad, eller använd 2024–2028-utgåvan. Rätta "Referenced in" till kap. 15 och 25 för båda.

### R-30 "Referenced in"-listor som inte stämmer med den faktiska citeringen
- **Fil:rad:** docs/33_references.md:7, 8, 12, 13, 16, 17, 19, 20, 21, 22, 26, 52, 55, 64, 67, 79, 91, 133, 136, 158, 162, 165
- **Post:** "Referenced in:"-listor för källorna [1], [2], [6], [7], [10], [11], [13], [14], [15], [16], [20], Brown C4, Brown Structurizr-blogg, CALM, GitLab SSOT, HashiCorp policy, Selic, Structurizr DSL, Gartner, IDC, HashiCorp-survey
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens (grep på `#source-n` och författare/titel i docs/*.md):**
  - *Listade men citerar inte (falska):* [2] kap. 23; [6] kap. 08; [11] kap. 11 och 12; [14] kap. 12 och 15a; Brown C4 kap. 24; Brown Structurizr-blogg kap. 24; GitLab SSOT kap. 02 och 11; Selic kap. 06 och 23; Gartner kap. 17; IDC kap. 05 och 21; HashiCorp State of Cloud Strategy Survey kap. 17 och 27 (frasen förekommer inte i något kapitel).
  - *Citerar men saknas (falska negativa):* [1] kap. 29; [10] kap. 30; [11] kap. 09b och 10; [13] kap. 30; [14] kap. 09, 09b och 24; [15] kap. 14; [16] kap. 04 och 14; [20] kap. 10; Brown C4 kap. 22; CALM kap. 32; HashiCorp policy enforcement kap. 20; Structurizr DSL kap. 30; Gartner kap. 25; IDC kap. 15 och 25.
- **Förslag:** Generera "Referenced in" automatiskt från `#source-n`-ankare och kapitlens Sources-avsnitt (t.ex. i `scripts/verify_sources.py`) i stället för att underhålla listorna manuellt.

### R-31 Trasiga interna länkar och kapitelrubriker som avviker från book_index.json
- **Fil:rad:** docs/33_references.md:7, 8, 10, 13, 16 (trasiga filer); 8, 10, 15, 16, 36, 37, 43, 52, 55, 58, 82, 91, 100, 115, 133, 136, 139, 142, 158, 162, 165, 168 (rubriker)
- **Post:** Länkar till 26a_future_trends.md (×3), 20_team_structures.md, 10_policy_as_code.md, 32_index.md; rubriker som "Chapter 23: Software as Code Interplay", "Chapter 6: Structurizr and Diagram Automation", "Chapter 25: Future Trends Development", "Chapter 15: Cost Optimisation", "Chapter 14: Practical Implementation", "Chapter 21: Digitalisation", "Chapter 18: Team Structure", "Chapter 17: Organisational Change", "Chapter 9b: Security Patterns and Implementation"
- **Bedömning:** FEL (länkar) / INKONSEKVENT (rubriker)
- **Allvarlighet:** Medel
- **Evidens:** Filkontroll: 26a_future_trends.md, 20_team_structures.md, 10_policy_as_code.md och 32_index.md finns inte i docs/. `docs/book_index.json`: 26A = 26a_prerequisites_for_aac.md "Prerequisites for Architecture as Code Adoption"; 20 = 20_ai_agent_team.md "AI Agent Team for Architecture as Code Initiatives"; 10 = 10_policy_and_security.md "Policy and Security as Code in Detail"; 32 = 32_finos_project_blueprint.md "Appendix C: FINOS Project Blueprint"; 23 = "The Interplay Between Soft As Code Disciplines"; 6 = "Structurizr: Architecture Modeling as Code"; 25 = "Future Trends in Architecture as Code"; 15B = "Cost Optimisation and Resource Management"; 14 = "Architecture as Code in Practice"; 21 = "Digitalisation through Code-based Infrastructure"; 18 = "Team Structure and Competency Development for IaC"; 17 = "Organisational Change and Team Structures"; 9B = "Advanced Security Patterns and Implementation" (rad 168 säger "Security Patterns and Implementation", rad 22–26 "Advanced …"). Rad 13 skriver "Chapter 7" medan övriga rader skriver "Chapter 07".
- **Förslag:** Byt filnamn till de kanoniska och hämta rubriker från `book_index.json` (via `scripts/navigation.py`) vid generering.

### R-32 Påståenden i inledning/avslutning stämmer inte
- **Fil:rad:** docs/33_references.md:3 och 178
- **Post:** "compiled in alphabetical order" (rad 3); "All citations in the manuscript are included in this compiled list" (rad 178)
- **Bedömning:** FEL
- **Allvarlighet:** Låg
- **Evidens:** Det numrerade indexet är inte alfabetiskt och den alfabetiska listan har felsorteringar (Write the Docs mellan "Architecture Decision Records Community" och "Brown"; IEEE före HashiCorp; "Thoughtworks Technology Radar. Diagrams…" före "Thoughtworks. Architecture…"). Luckanalysen nedan visar ca 114 kapitelkällor som saknas i kapitel 33.
- **Förslag:** Skriv om rad 3 ("a numbered index followed by an alphabetical list") och rad 178, eller komplettera listan.

### R-33 Inkonsekventa titlar/år mellan kapitel och kapitel 33 för samma källa
- **Fil:rad:** docs/33_references.md:11, 16, 20, 57, 102 (jämfört med kapitlens Sources)
- **Post:** [5], [10], [14], Brown SA4D, Martin
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** [5] citeras i kap. 07 som "Introduction to Infrastructure as Code with Terraform"; [10] citeras i kap. 02/22 som "Policy as Code: Expressing Requirements as Code" och i kap. 13 som "Policy Testing Best Practices for Infrastructure as Code"; [14] har tre titelvarianter (kap. 33, 09, 24); Brown SA4D: Leanpub 2022 (kap. 33) vs 2024 (kap. 06); Martin: trunkerad titel i kap. 01/02.
- **Förslag:** En kanonisk titel per källa, speglad i kapitlens Sources.

### R-34 Smärre bibliografiska brister i korrekta poster
- **Fil:rad:** docs/33_references.md:16, 17, 29, 32, 36, 45, 111, 117, 129, 132, 141
- **Post:** [10] (titel parafras), [11] ("Organisations" i stället för originalets "Organizations"), [23] (URL till landningssidan, sidan ligger på /en/actions/get-started/understand-github-actions), [26] (URL till referenssidan "Tests"; handledningen "Write Terraform Tests" ligger på /terraform/tutorials/configuration-language/test), [30] (titelstavning "Organising"), adr.github.io (sidan heter "Architectural Decision Records (ADRs)"), Nygard (URL saknas), OMG (dokumentnr ormsc/2001-07-01 och red. Miller & Mukerji saknas), Schmidt (vol. 39 nr 2 s. 25–31, DOI 10.1109/MC.2006.58 saknas; egentlig titel "Guest Editor's Introduction: Model-Driven Engineering"), Selic (vol. 20 nr 5 s. 19–25, DOI 10.1109/MS.2003.1231146 saknas), Diagrams as code (Vol. 23, okt 2020, Trial saknas)
- **Bedömning:** FÖRÅLDRAT / INKONSEKVENT (formalia)
- **Allvarlighet:** Låg
- **Evidens:** Se tabellen ovan; samtliga sidor/poster kontrollerade 2026-10-30.
- **Förslag:** Komplettera enligt ovan; behåll originalstavning i titlar (STYLE_GUIDE:s brittiska stavning gäller löptext, inte citerade titlar).

## Kapitelkällor som saknas i kapitel 33

Kapitlens "## Sources"-avsnitt innehåller följande poster som inte finns i `docs/33_references.md` (existensen hos dessa poster har inte kontrollerats – endast utelämnandet rapporteras). Totalt ca 114 unika poster.

- **05_automation_devops_cicd.md:** European Commission (2024). *Data Protection in the EU.* https://commission.europa.eu/law/law-topic/data-protection_en
- **07_containerisation.md:** Docker Inc. *Docker Architecture as Code best practices*; Helm Community. *Chart Development Guide*; Istio Project. *Service Mesh Architecture*
- **09_security_fundamentals.md** och **09b_security_patterns.md** (identiska listor, 24 poster): NIST (2018) *Cybersecurity Framework Version 1.1*; NIST (2020) *SP 800-207: Zero Trust Architecture*; NIST (2023) *Post-Quantum Cryptography Standardisation*; ENISA (2023) *Cloud Security Guidelines for EU Organisations*; EDPB (2023) *Guidelines on Data Protection by Design and by Default*; ENISA (2023) *NIS2 Directive Implementation Guidance*; European Commission (2022) *Regulation (EU) 2022/2554 (DORA)*; EBA (2023) *Guidelines on ICT and Security Risk Management*; Official Journal of the EU *"Directive" (EU) 2016/679 GDPR* (obs: GDPR är en förordning, inte ett direktiv); OWASP (2023) *Application Security Architecture Guide*; Cloud Security Alliance (2023) *Security Guidance v4.0*; CIS (2023) *CIS Controls v8*; MITRE (2023) *ATT&CK Enterprise Matrix*; AWS (2023) *AWS Security Best Practices*; Microsoft (2023) *Azure Security Benchmark v3.0*; OPA (2023) *OPA Policy Authoring Guide*; Kubernetes (2023) *Pod Security Standards*; ENISA (2023) *Threat Landscape Report 2023*; CERT-EU (2023) *Cybersecurity Threat Landscape Report 2023*; ECSO (2023) *European Cybersecurity Survey 2023*; SANS Institute (2023) *Security Architecture Design Principles*; ISACA (2019) *COBIT 2019*; (ISC)² (2023) *Cybersecurity Workforce Study*
- **09c_risk_and_threat_as_code.md:** Threat Modeling Manifesto Community *Threat Modeling Manifesto*; OWASP *OWASP Threat Dragon*; Microsoft *STRIDE Threat Modelling Methodology*; OASIS (2022) *STIX/TAXII Standards*; NIST *SP 800-30: Guide for Conducting Risk Assessments*; Gremlin & AWS *Chaos Engineering for Security*
- **12_compliance.md:** IEEE Computer Society *Quantum Computing Impact on Infrastructure*; Green Software Foundation *Sustainable Infrastructure Patterns*; NIST *Post-Quantum Cryptography Standards*; CNCF *Future of Cloud Native Infrastructure*; Gartner Research (2024) *Infrastructure and Operations Technology Trends 2024*
- **13_testing_strategies.md:** Gruntwork (2024) *Terratest Documentation*; AWS (2024) *Infrastructure Testing Strategy Guide*; NIST (2024) *Security Testing for Cloud Infrastructure*; Cloud Security Alliance (2024) *Cloud Security Testing Guidelines*
- **14_practical_implementation.md:** HashiCorp *Terraform Architecture as Code Best Practices*; AWS *AWS Well-Architected Framework: Infrastructure as Code*; Google Cloud *Infrastructure as Code Design Patterns*; Microsoft Azure *Azure Resource Manager Best Practices*; Puppet *Infrastructure as Code Implementation Guide*
- **15_cost_optimization.md:** AWS (2023) *AWS Cost Optimisation Guide*; FinOps Foundation (2023) *FinOps Framework and Architecture as Code Best Practices*; Kubecost (2023) *Kubernetes Cost Optimisation Guide*; Cloud Security Alliance (2023) *Cloud Cost Optimisation Security Guidelines*; Microsoft (2023) *Azure Cost Management Architecture as Code Best Practices*
- **15a_evidence_as_code.md:** NIST SP 800-218 *Secure Software Development Framework (SSDF)*; SLSA Framework; Sigstore *Cosign documentation*; NTIA *Minimum Elements for a Software Bill of Materials*
- **16_migration.md:** AWS (2023) *Large-Scale Migration and Modernisation Guide*; Microsoft (2023) *Azure Migration Framework and Architecture as Code Best Practices*; Google Cloud (2023) *Infrastructure Migration Strategies*; Gartner (2023) *Infrastructure Migration Trends in European Markets*; AXELOS (2023) *ITIL Foundation*; European Commission (2023) *Digital Transformation Guidelines for Public Sector*
- **17_organisational_change.md:** Puppet Labs (2023) *State of DevOps Report*; Google Cloud (2023) *DORA State of DevOps Research*; Spotify Technology (2023) *Spotify Engineering Culture*; McKinsey & Company (2023) *Organisational Transformation Best Practices*
- **18_team_structure.md:** Kim, Humble, Debois & Willis (2016) *The DevOps Handbook*; Google Cloud (2023) *DORA Reports*; Atlassian (2024) *DevOps Team Structure and Best Practices*; HashiCorp (2024) *Infrastructure as Code Maturity Model*
- **19_management_as_code.md:** Drucker (1954) *The Practice of Management*; GitOps Working Group (2024) *GitOps Principles* (https://opengitops.dev/); Puppet (2023) *State of DevOps Report*
- **20_ai_agent_team.md:** Edmondson (2012) *Teaming* (Jossey-Bass); Anthropic *Claude Agent SDK Documentation*
- **21_digitalisation.md:** Gartner (2023) *Cloud Adoption Strategies for Enterprises*; McKinsey (2023) *Digital Transformation: A Global Perspective*; AWS (2023) *Cloud Adoption Framework for Enterprises*; Microsoft (2023) *Azure for Enterprise Digital Transformation*; HashiCorp (2023) *Infrastructure as Code Best Practices*; SANS Institute (2023) *Cloud Security for Enterprise Organisations*
- **24_best_practices.md:** CNCF (2024) *Infrastructure as Code Best Practices*; HashiCorp (2024) *Terraform Maturity Model*; FinOps Foundation (2024) *Cloud Financial Management Playbook*; UK NCSC (2023) *Security Principles for Cloud-Hosted Services*; World Economic Forum (2024) *Global Risks Report*
- **25_future_trends.md** (19 poster): European Commission (2024) *The EU Artificial Intelligence Act*; *Horizon Europe*; *Digital Europe Programme*; *EU Quantum Flagship*; *European Quantum Communication Infrastructure (EuroQCI)*; *Post-Quantum Cryptography: Preparing for the Quantum Threat*; EuroHPC JU (2024); ENISA (2024) *Post-Quantum Cryptography: Current State and Quantum Mitigation*; GAIA-X (2024) *A Federated Secure Data Infrastructure for Europe*; McKinsey Global Institute *The Future of Infrastructure*; MIT Technology Review *Quantum Computing and Cryptography*; IEEE Computer Society *Edge Computing and 5G Integration*; FinOps Foundation *State of FinOps*; Green Software Foundation *Carbon-Aware Computing Guidelines*; CNCF *Platforms for Cloud Native Applications* (whitepaper); GAIA-X *GAIA-X Framework*; European Commission *European Green Deal*; Climate Neutral Data Centre Pact *Self-Regulatory Initiative*; European Commission/JRC *EU Code of Conduct for Energy Efficiency in Data Centres*
- **26b_aac_anti_patterns.md:** FinOps Foundation (2024) *Cloud Cost Management for Sustainable Delivery*; ISO/IEC 42010:2011 *Systems and Software Engineering — Architecture Description*; NCSC (2023) *Principles for Secure Design*; OPA Project (2024) *Policy as Code Cookbook*; Thoughtworks Technology Advisory Board (2024) *Technology Radar — Volume 30*; UK GDS (2024) *Service Manual: Technology and Architecture*
- **30_appendix_code_examples.md:** HashiCorp (2024) *Terraform Language Documentation* (https://developer.hashicorp.com/terraform/language)
- **architecture_as_code_maturity_model.md:** dwmkerr/architecture-as-code (GitHub-repo); övriga referenser är självreferenser till bokens egna kapitel via raw.githubusercontent.com

Kapitel utan luckor: 01, 02, 03, 04, 06, 08, 10, 11, 22, 23, 26a, 27, 29, 31, 32.

## Verifierat korrekt

- [4] GitHub Docs. *About protected branches* – https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches (200, titel exakt)
- [5] HashiCorp. *What is Terraform* – https://developer.hashicorp.com/terraform/intro (200, titel exakt)
- [6] CNCF. *Cloud Native Definition* – https://raw.githubusercontent.com/cncf/toc/main/DEFINITION.md (v1.1, godkänd av TOC/GB 2024-02-26)
- [9] AWS. *AWS CDK Developer Guide* – https://docs.aws.amazon.com/cdk/v2/guide/home.html (200)
- [11] NIST SP 800-53 Rev. 5 *Security and Privacy Controls for Information Systems and Organizations*, september 2020 (uppd. 10 dec 2020) – https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- [13] Kubernetes. *Concepts* – https://kubernetes.io/docs/concepts/ (200)
- [17] HashiCorp. *Backend Type: s3* – https://developer.hashicorp.com/terraform/language/backend/s3 (200, titel exakt)
- [18] Microsoft Learn. *Store Terraform state in Azure Storage* – https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage (200, titel exakt)
- [19] Google Cloud. *Store Terraform state in a Cloud Storage bucket* – https://cloud.google.com/docs/terraform/resource-management/store-state (200)
- [21] Write the Docs. *Docs as code* – https://www.writethedocs.org/guide/docs-as-code/ (200)
- [22] Jenkins. *Pipeline* – https://www.jenkins.io/doc/book/pipeline/ (200)
- [24] Microsoft. *What is Azure Pipelines?* – https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines (200, titel exakt)
- [25] GitLab. *Get started with GitLab CI/CD* – https://docs.gitlab.com/ee/ci/ → https://docs.gitlab.com/ci/ (200, titel exakt)
- [28] DORA. *Accelerate State of DevOps Report 2023* – https://dora.dev/research/2023/dora-report/ (200, titel exakt)
- [31] Forsgren, Humble & Kim. *Accelerate*, IT Revolution Press, 2018, ISBN 978-1-942788-33-1 – https://openlibrary.org/isbn/9781942788331.json
- AaC Open Source Project / FINOS. *architecture-as-code* – https://github.com/finos/architecture-as-code (FINOS Graduated; CALM)
- Architecture Decision Records. adr.github.io – https://adr.github.io (200)
- Brown, S. C4 model – https://c4model.com/ (200)
- Brown, S. *Software Architecture for Developers* – https://leanpub.com/software-architecture-for-developers (200)
- FINOS. *CALM* – https://calm.finos.org/ (200)
- HashiCorp. *Policy enforcement overview* – https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement (200)
- HashiCorp. *2024 State of Cloud Strategy Survey* (Forrester Consulting, 27 juni 2024) – https://www.hashicorp.com/blog/hashicorp-state-of-cloud-strategy-survey-2024-forrester-s-key-recommendations, https://www.hashicorp.com/state-of-the-cloud
- Mermaid – https://mermaid.js.org/ (200); PlantUML – https://plantuml.com/ (200)
- Nygard, M. *Documenting Architecture Decisions*, 15 november 2011 – https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- OMG. *Model Driven Architecture (MDA)*, ormsc/2001-07-01, juli 2001 – https://www.omg.org/cgi-bin/doc?ormsc/2001-07-01
- Schmidt, D.C. "Guest Editor's Introduction: Model-Driven Engineering", *Computer* 39(2):25–31, 2006 – https://doi.org/10.1109/MC.2006.58 (Crossref)
- Selic, B. "The pragmatics of model-driven development", *IEEE Software* 20(5):19–25, 2003 – https://doi.org/10.1109/MS.2003.1231146 (Crossref)
- Structurizr. *Structurizr Lite* – https://docs.structurizr.com/lite (200)
- Thoughtworks Technology Radar. *Diagrams as code* (Trial, Vol. 23, okt 2020) – https://www.thoughtworks.com/radar/techniques/diagrams-as-code
- Chung et al., Ford et al., Richardson, Skelton & Pais, Bass et al., Beyer et al., Martin: verk, författare, förlag och år stämmer – endast ISBN-numren är fel (se R-09 till R-14).
