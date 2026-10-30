<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del E, kapitel 23, 20 och 21

Granskningsdatum: 2026-10-30. Repo-HEAD: df6bd77 (2026-03-29). Granskare: Lead Researcher-agenten.

## Omfattning

Lästa filer (varje rad, med radnummer):

- `docs/23_soft_as_code_interplay.md` (262 rader)
- `docs/20_ai_agent_team.md` (188 rader)
- `docs/21_digitalisation.md` (393 rader)

Stödmaterial som lästs för korsreferenser: `docs/book_index.json`, `docs/33_references.md`, `docs/part_e_leadership.md`, `docs/part_f_practices.md`, `docs/book_structure.md`, `.github/workflows/*` (samtliga 14 filer listade, 5 lästa i sin helhet), `.claude/agents/*.md` (7 filer), `docs/images/diagram_28_agent_team.mmd`, `diagram_21_*.mmd`, `mindmap_21*.mmd`, `diagram_23_soft_as_code.mmd`, `mindmap_23a/b.mmd`, `tests/test_chapter23_assets.py`, `docs/STYLE_GUIDE.md` (citeringsregler), samt grep i kapitel 11, 15B, 25, 26A, 27, 30.

Påståendeinventering: cirka 95 verifierbara påståenden (statistik, företagshistorik, standarder/regelverk, verktygs-API:er, URL:er, källposter, korsreferenser). Cirka 60 av dessa kontrollerades mot primärkällor på webben (45 WebSearch-anrop, 12 WebFetch/curl mot primärdokument, nedladdning och textextraktion av Thoughtworks Technology Radar Vol. 21-PDF:en, PyPI-JSON, GitHub-taggar via `git ls-remote`). Resten kontrollerades lokalt i repot. Sökbudgeten tog slut efter 45 sökningar; de två påståenden som därför inte kunde slutverifieras listas under "Ej verifierbart".

Alla tre URL:er i kapitlens källistor svarar HTTP 200, men två av dem landar på andra sidor än den beskrivna (se E2-14 och E2-16).

## Sammanfattning

Kapitel 23 är i huvudsak konceptuellt och innehåller få kontrollerbara faktapåståenden; dess problem är framför allt källposterna (felaktiga titlar på OPA- och HashiCorp-dokumenten, en källa som inte används i texten) och ett par tekniska oprecisioner i det illustrativa Terraform-exemplet. Kapitel 20 beskriver repots egna bot-arbetsflöden på ett sätt som inte stämmer med vad som faktiskt finns i `.github/workflows/` och `.claude/agents/`, och dess GitHub Actions-exempel använder GitHub-API:et fel (saknar obligatoriskt `commit_id` och skrivrättigheter) samt saknar den stavningskontrollsmotor som pyspelling kräver. Kapitel 21 har de allvarligaste bristerna: en siffra om digitaliseringsinvesteringar ("över 500 miljarder pund på fem år") som är fel med mer än en tiopotens mot IDC:s egna data, påståenden om att Spotify, Netflix och Capital One byggdes "cloud-native från start" (alla tre migrerade från egna datacenter), Capital One-siffror (99,99 %, 40 %, 70 %) som inte går att hitta i någon primärkälla, en falsk orsakskedja mellan Backstage och Spotifys användartillväxt, en Terraform-mall som inte kan initieras (variabler i backend-blocket och ett argument som inte existerar), sex källposter utan URL vars titlar inte motsvarar några kända publikationer, samt flera föråldrade beskrivningar av de europeiska suveränitetsmolnen (AWS European Sovereign Cloud är GA sedan januari 2026; Google är inte längre "carbon neutral"). Därtill finns en strukturell inkonsekvens: kapitel 21 (och `part_f_practices.md`) placerar kapitel 23 i Del F, medan `book_index.json` lägger det i Del E före kapitel 20.

Antal fynd: 8 Hög, 12 Medel, 15 Låg.

## Fynd

### E2-01 Investeringssiffran för digital transformation är fel med mer än en tiopotens
- **Fil:rad:** docs/21_digitalisation.md:38
- **Påstående:** "According to recent industry reports, organisations globally have invested over £500 billion in digital transformation initiatives in the past five years, yet many projects fail due to inadequate infrastructure governance and accumulating technical debt."
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** IDC Worldwide Digital Transformation Spending Guide (pressmeddelande 2024-05-30): "Worldwide spending on Digital Transformation (DX) is forecast to reach almost $4 trillion in 2027", CAGR 16,2 % för 2022–2027, vilket ger ca 1,9 biljoner USD redan 2022 och en femårssumma 2022–2026 på väl över 10 biljoner USD. Enbart tillverkningsindustrin spenderade "almost half a trillion dollars in 2024". https://www.idc.com/resource-center/press-releases/worldwide-spending-on-digital-transformation-is-forecast-to-reach-almost-4-trillion-by-2027-according-to-new-idc-spending-guide/ ; även IDC 2023-11-01 (3,9 biljoner USD 2027). "Recent industry reports" preciseras inte, och ingen av kapitlets källor (E2-06) stöder siffran. Orsaksförklaringen ("fail due to inadequate infrastructure governance and accumulating technical debt") har inget stöd i någon citerad källa.
- **Förslag:** Ersätt med en sourcad siffra, t.ex. "IDC forecasts worldwide digital-transformation spending of almost USD 4 trillion in 2027 (CAGR 16.2 % 2022–2027)" med IDC-länk, och stryk eller beläggs orsaksmeningen (t.ex. med McKinseys 2022-undersökning om att företag realiserar under en tredjedel av förväntade intäktslyft).

### E2-02 Spotify, Netflix och Capital One var inte "cloud-native/cloud-based from inception"
- **Fil:rad:** docs/21_digitalisation.md:70 och :196
- **Påstående:** "Spotify: Revolutionised the music industry through cloud-native architecture from inception" och "Global enterprises such as Spotify, Netflix, and Capital One have demonstrated leadership by building their technical platforms on cloud-based infrastructure from inception."
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Spotify drev egna/leasade datacenter till dess att flytten till Google Cloud Platform annonserades 2016-02-23 (InfoQ: https://www.infoq.com/news/2016/02/Spotify-Google-Cloud/ ; Data Center Knowledge: https://datacenterknowledge.com/cloud/spotify-ditches-own-data-centers-in-favor-of-google-cloud ); 100 % av trafiken låg på GCP i december 2017 och datacenterstängningarna fortsatte därefter. Netflix (grundat 1997) avslutade sin sjuåriga AWS-migrering i januari 2016: "in early January, 2016, after seven years of diligent effort, we have finally completed our cloud migration" (https://about.netflix.com/news/completing-the-netflix-cloud-migration). Capital One (grundat 1994) lämnade åtta egna datacenter under en åttaårig resa och stängde det sista 2020 (https://siliconangle.com/2020/12/01/capital-one-closes-all-data-centers-to-rely-on-aws-on-demand-infrastructure-reinvent/ ; https://www.datacenterknowledge.com/cloud/capital-one-shut-down-its-last-three-data-centers-next-year).
- **Förslag:** Skriv om till migreringsberättelser: "Spotify migrated from its own data centres to Google Cloud between 2016 and 2018; Netflix completed a seven-year migration to AWS in January 2016; Capital One closed its last data centre in 2020 after an eight-year programme." Stryk "from inception" på båda ställena.

### E2-03 Capital One-siffrorna (99,99 %, 40 %, 70 %) saknar källa och motsägs av primärkällor
- **Fil:rad:** docs/21_digitalisation.md:76
- **Påstående:** "achieving 99.99% uptime for critical banking systems whilst reducing infrastructure costs by 40% and accelerating feature deployment by 70%."
- **Bedömning:** EJ VERIFIERBART (sannolikt fabricerat)
- **Allvarlighet:** Hög
- **Evidens:** Inga av siffrorna återfinns i AWS:s eller Capital Ones egna material. AWS-fallstudien nämner "70% faster disaster recovery time" (inte featureutrullning) (https://aws.amazon.com/solutions/case-studies/capital-one-all-in-on-aws/ via https://cloudzero.com/blog/capital-one-aws). CNCF-fallstudien anger "time to market from 1 quarter to 1 day" och att AWS-kostnaden utan Kubernetes hade varit 4x (https://www.cncf.io/case-study/capitalone/). Kombinationen "99.99% uptime" + "45% lower costs" tillhör en annan kunds fallstudie (Version 1, amerikansk bolåneservicer). Capital Ones VP of Cloud Evolution uppgav 2025 att kostnaderna i stället steg efter datacenterstängningen tills FinOps infördes (https://biztechmagazine.com/article/2025/08/how-capital-one-controls-cloud-costs). Chefsstrateg George Brady: besparingar "hasn't been the main reason" (Data Center Knowledge, ovan).
- **Förslag:** Ersätt med belagda utfall (t.ex. "time to market reduced from a quarter to a day per CNCF's case study; 70 % faster disaster-recovery tests per AWS") eller stryk siffrorna helt.

### E2-04 Backstage tillskrivs Spotifys tillväxt från 1 till 500 miljoner användare
- **Fil:rad:** docs/21_digitalisation.md:198–199
- **Påstående:** "Spotify developed an internal developer portal called Backstage, which they open-sourced in 2020 under CNCF governance. ... This developer portal approach enabled scaling from 1 million to over 500 million users without linear increases in infrastructure complexity."
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Spotify passerade 1 miljon användare 2009 och 1 miljon betalande i mars 2011 (https://thenextweb.com/news/spotify-reaches-1-million-paid-subscribers ; https://www.forrester.com/blogs/11-03-08-just_how_big_a_deal_is_spotifys_1_million_subscribers_milestone). Backstage skapades internt först omkring 2016 och öppnades som öppen källkod i mars 2020 (https://backstage.io/blog/2022/03/16/backstage-turns-two); CNCF Sandbox 2020-09-23 (https://backstage.io/blog/2020/09/23/backstage-cncf-sandbox), Incubating 2022-03-15 (https://cncf.io/blog/2022/03/15/backstage-project-joins-the-cncf-incubator). Orsakskedjan är alltså kronologiskt omöjlig; dessutom är "open-sourced in 2020 under CNCF governance" oprecist (öppen källkod i mars, CNCF-donation i september). Stycket är också internt motsägelsefullt: rubriken "Spotify's Infrastructure as Code Architecture" följs av "Backstage ... not an Infrastructure as Code platform per se".
- **Förslag:** "Spotify open-sourced its internal developer portal Backstage in March 2020 and donated it to the CNCF in September 2020 (incubating since March 2022). Backstage addresses developer experience and service cataloguing rather than infrastructure provisioning." Stryk tillväxtpåståendet eller koppla det till Spotifys faktiska GCP-migrering.

### E2-05 Terraform-mallen kan inte initieras: variabler i backend-blocket och ett obefintligt argument
- **Fil:rad:** docs/21_digitalisation.md:109–119 (hela blocket 96–191)
- **Påstående:** `backend "s3" { ... region = var.eu_region  # Parameterized EU region selection ... kms_key_id = var.kms_key_id ... dynamodb_table = "terraform-locks" ... versioning = true }`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** HashiCorp: "A backend block cannot refer to named values (like input variables, locals, or data source attributes)." (https://developer.hashicorp.com/terraform/language/backend). `terraform init` avbryts därför. Argumentet `versioning` finns inte i S3-backendens argumentlista; dokumentationen säger i stället "It is highly recommended that you enable Bucket Versioning" på själva bucketen (https://developer.hashicorp.com/terraform/language/backend/s3) → "Unsupported argument". `dynamodb_table` är markerat "(Optional, Deprecated)": "DynamoDB-based locking is deprecated and will be removed in a future minor version"; S3-nativ låsning (`use_lockfile = true`) blev experimentell i Terraform 1.10 och GA i 1.11 ("As part of this change, we've deprecated the DynamoDB-related arguments") (https://developer.hashicorp.com/terraform/language/v1.11.x/upgrade-guides). Kommentaren "Audit logging for compliance" vid `versioning` är dessutom missvisande – bucketversionering är inte revisionsloggning (det är CloudTrail/S3 access logging).
- **Förslag:** Flytta region/KMS-nyckel till partiell backend-konfiguration (`terraform init -backend-config="region=eu-central-1" -backend-config="kms_key_id=..."` eller en `backend.hcl`), ta bort `versioning = true` och sätt versionering på bucket-resursen, ersätt `dynamodb_table` med `use_lockfile = true` (kräv `required_version = ">= 1.11"`). Samma mönster bör kontrolleras i appendix-listning 21_CODE_1.

### E2-06 Sex källposter i kapitel 21 är overifierbara eller har fel titel, saknar URL och finns inte i referenslistan
- **Fil:rad:** docs/21_digitalisation.md:388–393
- **Påstående:** "Gartner (2023). Cloud Adoption Strategies for Enterprises."; "McKinsey & Company (2023). Digital Transformation: A Global Perspective."; "Amazon Web Services (2023). Cloud Adoption Framework for Enterprises."; "Microsoft (2023). Azure for Enterprise Digital Transformation."; "HashiCorp (2023). Infrastructure as Code Best Practices. HashiCorp Learn."; "SANS Institute (2023). Cloud Security for Enterprise Organisations."
- **Bedömning:** FELCITERAT / EJ VERIFIERBART (fantomkällor)
- **Allvarlighet:** Hög
- **Evidens:** Riktade sökningar hittar ingen Gartner-, McKinsey-, Microsoft- eller SANS-publikation med dessa titlar (närmast: Gartner "Accept and Address the Financial Impact of Cloud Adoption", 2023-06-02; McKinseys 2023-utgivning är boken *Rewired*, Wiley; Everest Group "Microsoft Azure Services State of the Market 2023"; SANS "Cloud Security Exchange 2023"). AWS-ramverkets verkliga titel är "An Overview of the AWS Cloud Adoption Framework" (AWS CAF 3.0, november 2021, uppdaterad 2025): https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/welcome.html . "HashiCorp Learn" finns inte längre som plattform – learn.hashicorp.com omdirigerar till https://developer.hashicorp.com/terraform/tutorials (kontrollerat 2026-10-30), och inget dokument heter "Infrastructure as Code Best Practices" (närmast "Terraform recommended practices"). Ingen av posterna finns i `docs/33_references.md`, trots att den filen hävdar att "All citations in the manuscript are included in this compiled list". `docs/STYLE_GUIDE.md:117` förbjuder uttryckligen kategoribeskrivningar som citat.
- **Förslag:** Byt ut mot verifierbara primärkällor med URL (IDC DX Spending Guide; AWS "An Overview of the AWS Cloud Adoption Framework"; Microsoft "Cloud Adoption Framework for Azure"; HashiCorp "Terraform recommended practices"; EDPB/EUR-Lex för GDPR/NIS2) och lägg in dem i `33_references.md`.

### E2-07 GitHub Actions-exemplet anropar `pulls.createReviewComment` utan obligatoriskt `commit_id` och utan skrivrättigheter
- **Fil:rad:** docs/20_ai_agent_team.md:113–128 (jobbdefinitionen 83–86)
- **Påstående:** `await github.rest.pulls.createReviewComment({ owner, repo, pull_number: context.issue.number, body: ..., path: finding.file, line: finding.line });`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** GitHub REST-dokumentationen för "Create a review comment for a pull request" anger `body`, `commit_id` ("The SHA of the commit needing a comment") och `path` som **Required** (https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#create-a-review-comment-for-a-pull-request). Anropet ger därför HTTP 422. Jobbet deklarerar ingen `permissions:`-block; för repon skapade efter februari 2023 är GITHUB_TOKEN som standard läsbehörigt, så även ett korrekt anrop nekas (403). Jämför repots egna `mermaid-designer-bot.yml` som sätter `pull-requests: write`.
- **Förslag:** Lägg till `commit_id: context.payload.pull_request.head.sha` och `side: 'RIGHT'`, samt `permissions: { contents: read, pull-requests: write }` på jobbet. Alternativt samla fynden i ett `pulls.createReview`-anrop med `comments: [...]` och `event: 'COMMENT'`.

### E2-08 Beskrivningen av repots bot-arbetsflöden stämmer inte med repot
- **Fil:rad:** docs/20_ai_agent_team.md:133–141 (och indirekt 151–153)
- **Påstående:** "The repository's bot workflows demonstrate a practical pattern ... When a contributor applies the `architecture` label to an issue, the Architect Bot workflow triggers ..." följt av tabellen `architecture`/Architect Bot, `documentation`/Editor Bot, `qa`/QA Bot, `dev`/Developer Bot, `design`/Designer Bot.
- **Bedömning:** FEL / INKONSEKVENT
- **Allvarlighet:** Hög
- **Evidens:** `.github/workflows/` innehåller (HEAD df6bd77) inga filer `architect-bot.yml`, `editor-bot.yml`, `qa-bot.yml`, `developer-bot.yml`, `designer-bot.yml` eller `requirements-bot.yml`. Det enda etikettstyrda bot-flödet är `mermaid-designer-bot.yml`, som triggas av etiketterna `mermaid`/`diagram` (inte `design`) och skapar en PR med ett .mmd-diagram via `anthropics/claude-code-action@v1`. Övriga automationer: `claude.yml` (@claude-omnämnanden), `claude-code-review.yml` (PR-granskning), `assign-codex2.yml` och `issue-create-draft-pr.yml` (skapar utkast-PR vid öppnat ärende, OpenAI Codex). `.claude/agents/` definierar rollerna editor, writer, graphic-designer, researcher, critic och it-architect – inte kapitlets Project Manager, Requirements Analyst, Designer, Developer och Quality Control. (Samma felaktiga lista finns i `CLAUDE.md`, avsnittet "Bot Workflows".) Diagrammet `diagram_28_agent_team.mmd` visar dessutom bara sex roller och saknar Requirements Analyst och Graphic Designer som texten beskriver.
- **Förslag:** Antingen beskriv de faktiska flödena (Mermaid Designer Bot med etiketterna `mermaid`/`diagram`; @claude-driven granskning; Codex-utkast-PR) eller markera tabellen som ett förslag ("a pattern the repository could adopt"). Uppdatera `CLAUDE.md` i samma veva.

### E2-09 Suveränitetsmolnen beskrivs i ett föråldrat läge (AWS "roadmap"/"upcoming", Azure/Google utan 2025–2026-utvecklingen)
- **Fil:rad:** docs/21_digitalisation.md:220, 223, 228, 231, 239
- **Påstående:** "When AWS is approved through the European Sovereign Cloud roadmap or EU regional deployments ..."; "Dedicated support with European expertise, GDPR compliance guidance, and the upcoming sovereign controls programme"; "Azure's EU Data Boundary commitments ..."; "Google Cloud's sovereign controls, implemented with partners such as T-Systems and Thales ..."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** AWS European Sovereign Cloud blev allmänt tillgängligt 14–15 januari 2026 med första regionen i Brandenburg (`eusc-de-east-1`), drivet uteslutande av EU-bosatt personal via ett nytt europeiskt moderbolag med tre tyska dotterbolag; sovereign Local Zones planeras i Belgien, Nederländerna och Portugal (https://press.aboutamazon.com/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe). Microsoft slutförde EU Data Boundary 2025-02-26 (https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/) och lanserade 2025-06-16 "Microsoft Sovereign Cloud" (Sovereign Public Cloud, Sovereign Private Cloud, National Partner Clouds, Data Guardian) (https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/). Googles erbjudande heter "Sovereign Controls by Partners" (T-Systems: GA; S3NS/Thales i Frankrike; SecNumCloud-mål) (https://www.datacenterdynamics.com/en/news/google-reaffirms-sovereign-cloud-solutions-for-eu/).
- **Förslag:** Uppdatera avsnittet till status per 2026: AWS ESC är i drift (regionkod, driftmodell), Azure: EU Data Boundary slutförd + Microsoft Sovereign Cloud, Google: Sovereign Controls by Partners (T-Systems, S3NS). Ta bort "roadmap" och "upcoming".

### E2-10 Google Cloud är inte längre "carbon-neutral"
- **Fil:rad:** docs/21_digitalisation.md:242
- **Påstående:** "Carbon-neutral operations aligned with EU sustainability goals"
- **Bedömning:** FEL / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Googles Environmental Report 2024 (juli 2024): "Starting in 2023, we're no longer maintaining operational carbon neutrality"; bolaget slutade köpa billiga kompensationskrediter och siktar på nettonoll 2030, samtidigt som utsläppen ökat ca 48 % sedan 2019 (https://www.bloomberg.com/news/articles/2024-07-08/google-is-no-longer-claiming-to-be-carbon-neutral ; https://www.fortune.com/2024/07/10/ai-has-destroyed-googles-promise-of-carbon-neutrality-with-emissions-rising-50-over-the-last-five-years).
- **Förslag:** Ersätt med "Net-zero 2030 target and published carbon-free-energy metrics per region" eller stryk punkten; den har heller ingen koppling till suveränitet.

### E2-11 "IaC minskar manuellt arbete med upp till 70 %" saknar studie
- **Fil:rad:** docs/21_digitalisation.md:44
- **Påstående:** "Studies demonstrate that Infrastructure as Code reduces manual effort by up to 70%"
- **Bedömning:** TVEKSAMT / EJ VERIFIERBART
- **Allvarlighet:** Medel
- **Evidens:** Siffran förekommer bara i leverantörsmarknadsföring utan angiven studie (t.ex. SmartDev-glossar "70–80 % reduction in provisioning time"; Hypersense "70 % fewer configuration-related failures", "industry research" utan namn). Den enda akademiska träffen (IRJET 2020) rapporterar 90 % för ett enskilt projekt. Ingen peer-reviewed eller DORA-källa stöder "upp till 70 % manuellt arbete".
- **Förslag:** Stryk "Studies demonstrate" eller ersätt med en specifik, citerad källa (t.ex. DORA Accelerate State of DevOps, som redan är Source [28]) och formulera måttet exakt.

### E2-12 Kapitel 21 placerar kapitel 23 i Del F och tillskriver det innehåll det inte har
- **Fil:rad:** docs/21_digitalisation.md:380–384
- **Påstående:** "The organisational transformation explored in this part—from changing team structures to Management as Code and digitalisation ... Part F explores the interplay between different 'as Code' practices ... Chapter 23 on the Interplay Between Soft 'as Code' Disciplines reveals how Documentation as Code, Requirements as Code, Policy as Code, and other practices create synergies"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` placerar kapitel 23 i Del E i ordningen 17, 18, 19, 23, 20, 21; Del F består enbart av kapitel 22 och 24. Övergångstexten hoppar alltså över två kapitel i den egna delen (23 och 20) och pekar på fel del. `docs/part_f_practices.md:11` upprepar samma felplacering. Kapitel 23 nämner inte "Requirements as Code" en enda gång (grep ger noll träffar); dess discipliner är Compliance, Architecture, Documentation, Knowledge och Culture as Code.
- **Förslag:** Skriv om övergången: "Part E has moved from team structures (Ch. 17–18) via Management as Code (Ch. 19), the interplay of soft 'as code' disciplines (Ch. 23) and AI agent teams (Ch. 20) to digitalisation. Part F contrasts Documentation as Code with Architecture as Code (Ch. 22) and distils best practices (Ch. 24)." Rätta även `part_f_practices.md` eller flytta kapitel 23 i indexet – men gör det konsekvent.

### E2-13 Källtitlarna "Policy as Code Overview" motsvarar inte dokumenten (OPA och HashiCorp)
- **Fil:rad:** docs/23_soft_as_code_interplay.md:260–261; docs/20_ai_agent_team.md:186 (samt 33_references Source [10])
- **Påstående:** "Open Policy Agent (2024). *Policy as Code Overview.* CNCF OPA Project." och "HashiCorp. *Policy as Code Overview.* HashiCorp Developer Documentation. https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** https://www.openpolicyagent.org/docs har titeln "Open Policy Agent (OPA)"; frasen "Policy as Code Overview" förekommer inte på sidan (den säger "lets you specify policy as code" och "graduated Cloud Native Computing Foundation (CNCF) project", graduation 2021-02-04, https://www.cncf.io/announcements/2021/02/04/cloud-native-computing-foundation-announces-open-policy-agent-graduation/). HashiCorp-sidan heter "Policy enforcement overview", gäller "HCP Terraform" (Terraform Cloud döptes om 2024-04-22, https://developer.hashicorp.com/terraform/docs/cloud) och beskriver Sentinel, OPA och det nya HCL-baserade policyramverket; frasen "Policy as Code Overview" förekommer inte. Dessutom används ingen av de tre källorna i kapitel 23:s löptext (skyddade grenar nämns inte alls; OPA nämns en gång utan hänvisning).
- **Förslag:** "Open Policy Agent. *Open Policy Agent (OPA) documentation.* CNCF graduated project, https://www.openpolicyagent.org/docs (besökt 2026-10-30)" och "HashiCorp. *Policy enforcement overview (HCP Terraform).* https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement". Ta bort GitHub-källan ur kapitel 23 eller lägg in en hänvisning i texten.

### E2-14 "Governance as Code" finns inte som blip i Technology Radar Vol. 21 (Source [2], påstås refererad i kapitel 23)
- **Fil:rad:** docs/33_references.md Source [2] (hävdar "Referenced in ... Chapter 23: Software as Code Interplay"); docs/23_soft_as_code_interplay.md:258–262 saknar hänvisningen
- **Påstående:** "Thoughtworks Technology Radar. *Governance as Code.* Thoughtworks Technology Radar Vol. 21, November 2019. Available at: https://www.thoughtworks.com/about-us/news/2019/technology-radar-edition21 [blip introduced Vol. 21; archived from techniques listing]"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Vol. 21-PDF:en (https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2019/11/tr_technology_radar_vol_21_en.pdf, nedladdad och textextraherad 2026-10-30) innehåller ingen blip med namnet "Governance as code". Techniques-kvadranten har "4. Pipelines for infrastructure as code" och "15. Security policy as code" (ring TRIAL; nämner Open Policy Agent och Istio). Uttrycket förekommer bara i ett temastycke: "This topic concerning policy, compliance and governance as code reappeared multiple times in our conversations ... infrastructure as code, and now automated governance." Blip-sidan https://www.thoughtworks.com/radar/techniques/security-policy-as-code bekräftar "Nov 2019 Trial". URL:en i Source [2] omdirigerar till den generiska nyhetsindexsidan https://www.thoughtworks.com/about-us/news, och https://www.thoughtworks.com/radar/techniques/governance-as-code omdirigerar till kvadrantindexet (blipen existerar inte).
- **Förslag:** Skriv om Source [2] till "Thoughtworks. *Technology Radar Vol. 21*, November 2019, theme 'Protecting the software supply chain / automated governance' and technique 'Security policy as code' (Trial)" med PDF-länken, och ta bort "Chapter 23" från dess referenslista (kapitel 23 citerar den inte).

### E2-15 Referenslistan och kapitlens källavsnitt stämmer inte överens
- **Fil:rad:** docs/33_references.md Source [2], [4], [10], Selic-posten, IDC-posten; docs/20_ai_agent_team.md:183–188; docs/21_digitalisation.md:386–393
- **Påstående:** Source [4] "... [Chapter 20](20_team_structures.md), [Chapter 23: Software as Code Interplay]"; Selic (2003) "Referenced in ... Chapter 23"; IDC "Worldwide DevOps Software Tools Forecast, 2023–2027 ... Referenced in ... Chapter 21"; "All citations in the manuscript are included in this compiled list".
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Filen `docs/20_team_structures.md` finns inte (kapitel 20 är `20_ai_agent_team.md`); kapitel 23 heter "The Interplay Between Soft As Code Disciplines", inte "Software as Code Interplay"; kapitel 23 citerar varken Selic (2003) eller Source [2]; kapitel 21 citerar inte IDC alls, och ingen IDC-rapport med exakt titeln "Worldwide DevOps Software Tools Forecast, 2023–2027" kunde hittas (IDC publicerade "Worldwide DevSecOps Software Tools Forecast, 2023–2027" i augusti 2023 och "Worldwide DevOps Software Tools Forecast, 2024–2028", https://www.gii.co.jp/report/id1337804-worldwide-devsecops-software-tools-forecast.html ; https://www.gii.co.jp/report/id1555108-worldwide-devops-software-tools-forecast.html). Kapitel 20:s källor Edmondson (2012) och Anthropic saknas helt i referenslistan, liksom alla sex källor i kapitel 21.
- **Förslag:** Kör `python3 scripts/verify_sources.py` och synkronisera: rätta filnamn och kapiteltitel, ta bort ogrundade "Referenced in"-angivelser, lägg till kapitel 20/21-källorna (efter att de rättats enligt E2-06, E2-16, E2-32).

### E2-16 Anthropic-källan pekar på fel sida och är föråldrad
- **Fil:rad:** docs/20_ai_agent_team.md:188
- **Påstående:** "[Anthropic – Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/)"
- **Bedömning:** FÖRÅLDRAT / FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** URL:en omdirigerar (kontrollerat 2026-10-30) till https://platform.claude.com/docs/en/intro – den generiska introduktionen till utvecklarplattformen, inte Agent SDK-dokumentationen. Claude Agent SDK (omdöpt från Claude Code SDK i slutet av september 2025; paket `@anthropic-ai/claude-agent-sdk` och `claude-agent-sdk`) dokumenteras på https://code.claude.com/docs/en/agent-sdk/overview (https://docs.claude.com/en/api/agent-sdk/overview omdirigerar dit; migrationsguide: https://code.claude.com/docs/en/agent-sdk/migration-guide). Kapitlets löptext hänvisar heller inte till SDK:n. Posten saknas i `33_references.md`.
- **Förslag:** "Anthropic. *Claude Agent SDK – Overview.* https://code.claude.com/docs/en/agent-sdk/overview (accessed 2026-10-30)" och lägg till en mening i texten om vad SDK:n används till, eller stryk källan.

### E2-17 Editor-arbetsflödet saknar stavningsmotor och använder ett verktyg det aldrig kör
- **Fil:rad:** docs/20_ai_agent_team.md:94–98 (och 109–111)
- **Påstående:** `run: pip install vale pyspelling` följt av `run: pyspelling --config .pyspelling.yml`
- **Bedömning:** FEL (körbarhet)
- **Allvarlighet:** Medel
- **Evidens:** PySpellings dokumentation: "If you do not have a working Aspell or Hunspell on your system, PySpelling will not work" (https://facelessuser.github.io/pyspelling/). Arbetsflödet installerar varken `aspell`/`hunspell` (t.ex. `sudo apt-get install -y aspell aspell-en`) eller ordlistor. `.pyspelling.yml` finns inte i repot. PyPI-paketet `vale` (3.25.1.0) finns och installerar Vale-binären, men Vale körs aldrig i flödet. Kommentaren på raderna 109–111 erkänner att skripten är illustrativa, men nämner inte dessa två brister; `scripts/validate_heading_capitalization.py` finns faktiskt i repot medan `scripts/check_terminology.py` saknas.
- **Förslag:** Lägg till ett steg `sudo apt-get update && sudo apt-get install -y aspell aspell-en` före pyspelling, lägg till ett `vale docs/`-steg eller ta bort `vale`, och utvidga den illustrativa anmärkningen till `.pyspelling.yml`.

### E2-18 `timestamp()` i resurs-taggar ger diff vid varje körning
- **Fil:rad:** docs/21_digitalisation.md:131
- **Påstående:** `CreatedDate = formatdate("YYYY-MM-DD", timestamp())` inuti `locals.enterprise_tags` som appliceras på alla resurser
- **Bedömning:** TVEKSAMT (dokumenterat antimönster i en mall som presenteras som best practice)
- **Allvarlighet:** Medel
- **Evidens:** HashiCorp: "The result of this function will change every second ... using this function directly with resource attributes will cause a diff to be detected on every Terraform run. We do not recommend using this function in resource attributes, but in rare cases it can be used in conjunction with the ignore_changes lifecycle meta-argument" (https://developer.hashicorp.com/terraform/language/functions/timestamp). Eftersom taggen ingår i `merge()` på VPC och nio subnät kommer varje `plan` att föreslå uppdateringar.
- **Förslag:** Ta bort `CreatedDate` eller använd `time_static`-resursen från Time-providern / `lifecycle { ignore_changes = [tags["CreatedDate"]] }`.

### E2-19 General Electric som exempel på lyckad digital omställning
- **Fil:rad:** docs/21_digitalisation.md:259
- **Påstående:** "Traditional industrial companies such as General Electric, Siemens, and ABB have redefined their business models through digital initiatives built on modern cloud infrastructure. Architecture as Code has enabled these companies to develop IoT platforms, AI services, and data analytics solutions that create new revenue streams."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** GE Digital/Predix betraktas allmänt som ett misslyckande: över 4 miljarder USD investerade, nedskrivningar och avyttringsförsök (ServiceMax, Meridium, Predix) (https://en.wikipedia.org/wiki/Predix_(software) ; https://www.intelligentautomation.network/resiliency/articles/lessons-learned-from-ges-digital-transformation-failure). GE delades upp (annonserat november 2021, slutfört april 2024) och GE Digital uppgick i GE Vernova. Att "Architecture as Code" skulle ha möjliggjort dessa bolags IoT-plattformar saknar källa.
- **Förslag:** Ta bort GE eller använd det som lärdom (kultur/organisation före plattform); belägg Siemens (MindSphere → Insights Hub) och ABB (ABB Ability) med källor och tona ned "Architecture as Code has enabled".

### E2-20 Rekommenderade IaC-skanners är delvis i förvaltningsläge; `terraform plan` körs utan `init`
- **Fil:rad:** docs/21_digitalisation.md:283–291
- **Påstående:** "For real compliance gates, use dedicated policy tools such as checkov, tfsec, or terrascan." samt steget `terraform plan | grep -E "(encrypt|encryption)" || exit 1` direkt efter `actions/checkout@v4`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** tfsec: "tfsec is joining the Trivy family ... our engineering attention will be directed at Trivy going forward"; migrationsguide `tfsec <dir>` → `trivy config <dir>` (https://github.com/aquasecurity/tfsec/blob/master/tfsec-to-trivy-migration-guide.md); senaste tagg v1.28.14 (enbart beroendeuppdateringar). Terrascan (Tenable): senaste tagg v1.19.9, inga nya regler på länge (taggar kontrollerade via `git ls-remote` 2026-10-30). Steget saknar `hashicorp/setup-terraform` och `terraform init`, så `terraform plan` misslyckas; utan `set -o pipefail` maskeras felet dessutom av `grep`. Kapitlet markerar visserligen exemplet som illustrativt.
- **Förslag:** Byt rekommendationen till "Trivy (`trivy config`), Checkov eller OPA/Conftest", lägg till `hashicorp/setup-terraform@v3` + `terraform init -backend=false` och `set -euo pipefail` i exemplet.

### E2-21 Versionerna på GitHub Actions ligger flera major-versioner efter
- **Fil:rad:** docs/20_ai_agent_team.md:87, 90, 114; docs/21_digitalisation.md:283
- **Påstående:** `actions/checkout@v4`, `actions/setup-python@v5`, `actions/github-script@v7`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Taggar per 2026-10-30 (`git ls-remote --tags`): actions/checkout v7.0.1, actions/setup-python v7.1.0, actions/github-script v9.0.0. De äldre taggarna fungerar fortfarande men utgår från Node 20-runtime som GitHub fasar ut.
- **Förslag:** Uppdatera till `@v7`, `@v7` respektive `@v9` före publicering, eller skriv pinning-anvisning i texten.

### E2-22 Kodkommentaren om `terraform_runner` är inte längre korrekt
- **Fil:rad:** docs/21_digitalisation.md:315–318, 351–355
- **Påstående:** "# Note: 'terraform_runner' is not a published PyPI package." och `from terraform_runner import TerraformRunner ... tf_runner.apply_configuration(template=..., variables=...)`
- **Bedömning:** FEL (sedan april 2025)
- **Allvarlighet:** Låg
- **Evidens:** PyPI har paketet `terraform-runner` (import `terraform_runner`) i versionerna 1.0.0–1.0.2, publicerade 2025-04-28 av "ctogaigenticai" ("A Python package to automate Terraform deployment workflows for agents and cloud services", https://pypi.org/project/terraform-runner/). Det är ett orelaterat tredjepartspaket och exponerar inte kapitlets `TerraformRunner().apply_configuration()`-API, så exemplet förblir fiktivt. `python-terraform` (0.10.1) finns som wrapper.
- **Förslag:** Skriv om kommentaren: "The TerraformRunner interface is illustrative; there is no official HashiCorp Python SDK – use subprocess, python-terraform or the Terraform CLI/HCP Terraform API."

### E2-23 Spotifys användarsiffra är inaktuell
- **Fil:rad:** docs/21_digitalisation.md:70 (och :199)
- **Påstående:** "a global platform serving over 500 million users"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Spotify rapporterade 788 miljoner månatliga aktiva användare och 306 miljoner prenumeranter för Q3 2026 (6-K, 2026-10-22, https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm); 713 miljoner ett år tidigare.
- **Förslag:** "nearly 800 million monthly active users (Q3 2026)" med datumangivelse, eller skriv tidlöst ("hundreds of millions").

### E2-24 EDPB "enforces" inte GDPR
- **Fil:rad:** docs/21_digitalisation.md:48
- **Påstående:** "guided by the EDPB's enforcement of GDPR"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** EDPB:s uppgift är att säkerställa en enhetlig tillämpning av GDPR genom riktlinjer, yttranden (art. 64) och bindande beslut i tvister mellan tillsynsmyndigheter (art. 65); tillsyn och sanktioner utövas av de nationella dataskyddsmyndigheterna (https://www.edpb.europa.eu/our-work-tools/consistency-findings/binding-decisions_nb ; https://www.edpb.europa.eu/consistency-findings_en).
- **Förslag:** "guided by EDPB guidelines and enforced by national supervisory authorities".

### E2-25 NIS2 beskrivs som ett "critical infrastructure"-direktiv
- **Fil:rad:** docs/21_digitalisation.md:42, 48 (jämför korrekt terminologi på rad 296)
- **Påstående:** "the NIS2 Directive for critical infrastructure cybersecurity"
- **Bedömning:** TVEKSAMT (förenkling)
- **Allvarlighet:** Låg
- **Evidens:** Direktiv (EU) 2022/2555 omfattar "essential and important entities" i 18 sektorer, inklusive digitala tjänster och offentlig förvaltning; fysisk resiliens för "critical entities" regleras i CER-direktivet 2022/2557. Införlivandefrist 2024-10-17, tillämpning från 2024-10-18 (https://ccb.belgium.be/de/node/434 ; https://www.mayerbrown.com/de/insights/publications/2024/08/new-eu-cyber-rules-implementation-of-nis2-in-the-eu-member-states).
- **Förslag:** "the NIS2 Directive (EU) 2022/2555 for essential and important entities".

### E2-26 Skrivsättet "PCI-DSS" och "certifications ... SOC 2"
- **Fil:rad:** docs/21_digitalisation.md:210, 227, 299, 302
- **Påstående:** "PCI-DSS"; "Comprehensive compliance certifications including ISO 27001, SOC 2, and PCI-DSS"
- **Bedömning:** TVEKSAMT (terminologi)
- **Allvarlighet:** Låg
- **Evidens:** PCI Security Standards Council skriver "PCI DSS" utan bindestreck; gällande version är v4.0.1 (v4.0 pensionerad 2024-12-31) (https://commerce.uwo.ca/documentation/PCI-DSS-v4-0-to-v4-0-1-Summary-of-Changes-r1-1.pdf). SOC 2 är en attestationsrapport (AICPA), inte en certifiering.
- **Förslag:** "PCI DSS v4.0.1" genomgående; "certifications and attestations (ISO/IEC 27001, SOC 2 reports, PCI DSS)".

### E2-27 "GAIA-X" bör skrivas "Gaia-X"
- **Fil:rad:** docs/21_digitalisation.md:218, 249
- **Påstående:** "the GAIA-X or EU Cloud Code of Conduct commitments"; "GAIA-X aligned services"
- **Bedömning:** TVEKSAMT (stavning)
- **Allvarlighet:** Låg
- **Evidens:** Organisationen skriver sig "Gaia-X" (sidtitel på https://gaia-x.eu/: "Gaia-X: A Federated Secure Data Infrastructure"). EU Cloud Code of Conduct är korrekt (godkänd under GDPR art. 40 av belgiska dataskyddsmyndigheten 2021-05-20 efter EDPB-yttrande, https://dataprotectionauthority.be/publications/decision-n05-2021-of-20-may-2021.pdf). Kapitel 15B och 25 använder också "GAIA-X", så rättningen bör göras bokövergripande.
- **Förslag:** "Gaia-X" överallt.

### E2-28 Open Telekom Cloud sammanblandas med "Sovereign Controls by T-Systems"
- **Fil:rad:** docs/21_digitalisation.md:251
- **Påstående:** "Open Telekom Cloud combines Deutsche Telekom operations with T-Systems sovereign controls"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Open Telekom Cloud drivs av T-Systems på OpenStack-teknik levererad av Huawei, med tvillingdatacenter i Biere/Magdeburg och en region i Amsterdam (https://www.prnewswire.co.uk/news-releases/deutsche-telekom-and-huawei-launch-new-open-telekom-cloud-572080601.html ; https://www.telecompaper.com/news/t-systems-zet-2e-open-telekom-cloud-datacenter-in-amsterdam--1324096). "Sovereign Controls by T-Systems" är ett separat erbjudande byggt på Google Cloud (E2-09). Huawei-beroendet är dessutom en känd suveränitetsinvändning som kapitlet inte nämner.
- **Förslag:** "Open Telekom Cloud, operated by T-Systems on OpenStack with data centres in Germany and the Netherlands" – och nämn den separata Google-baserade T-Systems Sovereign Cloud där relevant.

### E2-29 "Chapter 15" är tvetydigt i indexet
- **Fil:rad:** docs/21_digitalisation.md:218
- **Påstående:** "Sovereignty guardrails described in Chapter 15 and the Future Trends chapter"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `book_index.json` har 15A (Evidence as Code, i Del C – noll träffar på "sovereign") och 15B (Cost Optimisation – två omnämnanden, rad 65 och 67). Kapitel 25 ("Cloud and Digital Sovereignty in Europe", rad 255) är korrekt. Övriga kapitel (26A) hänvisar också till "Chapter 15" utan bokstav.
- **Förslag:** "Chapter 15B (Cost Optimisation) and Chapter 25 (Future Trends)" med Markdown-länkar.

### E2-30 Redaktionella arbetsanteckningar kvar i manuskriptet; diagrammet matchar inte rollerna
- **Fil:rad:** docs/20_ai_agent_team.md:13, 17–19, 21, 41
- **Påstående:** "This chapter reframes the agent ecosystem in British English, translating previous checklists into narrative guidance ..."; `<!-- Note: This file uses a diagram_28_ prefix; rename to diagram_20_agent_team.png ... -->`; bilden `images/diagram_28_agent_team.png`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Meningen på rad 13 är en meta-kommentar om redigeringshistorik, inte läsartext. HTML-kommentaren beskriver ett ogjort arbete; filen heter fortfarande `diagram_28_agent_team.mmd/.png`. Diagrammet innehåller Project Owner, Project Manager, Architect, Designer, Developer, Quality Control och Editor men saknar Requirements Analyst och Graphic Designer som texten (rad 21, 31, 41) beskriver. `docs/book_structure.md:140` och `diagram_21_chapter20.mmd` (Lovable-mockups) visar att kapitel 20 tidigare hade annat innehåll, vilket förklarar restposterna.
- **Förslag:** Stryk meningen på rad 13 och HTML-kommentaren; döp om diagrammet till `diagram_20_agent_team` (uppdatera .mmd och PNG) och lägg till de två saknade rollerna.

### E2-31 Prompten hänvisar till en fil som inte finns
- **Fil:rad:** docs/20_ai_agent_team.md:153
- **Påstående:** "Ensure all diagrams follow the Kvadrat theme defined in docs/VISUAL_ELEMENTS_GUIDE.md"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `docs/VISUAL_ELEMENTS_GUIDE.md` finns inte i repot; Kvadrat-temat definieras i `docs/mermaid-kvadrat-theme.json` (och klasserna `kv-*` beskrivs i `.github/workflows/README_MERMAID_BOT.md`). Samma döda hänvisning finns i `docs/STYLE_GUIDE.md` och `docs/AUTHOR_PERSONA.md`. Övriga sökvägar i prompten (`docs/examples/structurizr/adrs/`, `book_index.json`) finns.
- **Förslag:** Ersätt med `docs/mermaid-kvadrat-theme.json` eller skapa guiden.

### E2-32 Edmondson-titeln är ändrad och saknar ISBN
- **Fil:rad:** docs/20_ai_agent_team.md:187
- **Påstående:** "Edmondson, A. C. "Teaming: How Organisations Learn, Innovate, and Compete in the Knowledge Economy." Jossey-Bass, 2012."
- **Bedömning:** FELCITERAT (titel)
- **Allvarlighet:** Låg
- **Evidens:** Originaltiteln är *Teaming: How Organizations Learn, Innovate, and Compete in the Knowledge Economy* (amerikansk stavning i titeln), Jossey-Bass, 2012-04-03, ISBN 978-0-7879-7093-2 (https://bookpal.com/teaming-9780787970932/ ; https://psnet.ahrq.gov/issue/teaming-how-organizations-learn-innovate-and-compete-knowledge-economy). Boken nämns inte i kapitlets löptext och saknas i `33_references.md`.
- **Förslag:** Återställ originalstavningen i titeln (titlar citeras ordagrant), lägg till ISBN, och knyt boken till texten (t.ex. avsnittet om psykologisk trygghet/"Teaming") eller stryk.

### E2-33 Terraform-låsningsexemplet använder ett påhittat felmeddelande och en avvecklad mekanism
- **Fil:rad:** docs/23_soft_as_code_interplay.md:174–189
- **Påstående:** "DynamoDB lock contention caused random failures with LockTimeoutError"; "The DynamoDB lock table was provisioned with default read/write capacity units insufficient for more than two simultaneous lock requests"; "Enable DynamoDB auto-scaling on the lock table, set a minimum of 5 read/write capacity units"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Terraform rapporterar "Error acquiring the state lock" med `ConditionalCheckFailedException` från DynamoDB; "LockTimeoutError" är inte ett Terraform-/AWS-felmeddelande (sökning gav noll träffar; https://oneuptime.com/blog/post/2026-02-23-how-to-fix-terraform-state-lock-stuck-conditionalcheckfailedexception/markdown). Låset tas med ett enda villkorat `PutItem`; 5 WCU (Terraforms dokumenterade standard) klarar långt fler än två samtidiga försök, så orsaksförklaringen är tekniskt osannolik. DynamoDB-låsning är dessutom avvecklad (deprecated) sedan Terraform 1.11 till förmån för S3-nativ låsning `use_lockfile` (se E2-05).
- **Förslag:** Byt till ett realistiskt scenario (t.ex. "Error acquiring the state lock" på grund av föräldralösa lås efter avbrutna pipelines; åtgärd `terraform force-unlock` + övergång till `use_lockfile = true`), eller markera exemplet tydligare som fiktivt.

### E2-34 Stilregel och titelvarianter för kapitel 23
- **Fil:rad:** docs/23_soft_as_code_interplay.md:1, 5, 254; docs/book_index.json:55; docs/book_structure.md:101
- **Påstående:** "compliance as code, architecture as code, documentation as code" (rad 5); "architecture as code serves as the hub" (rad 254); kapitelrubrik 'Soft "as code"' mot indexets "Soft As Code" och bokstrukturens "Soft 'as Code'"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `docs/STYLE_GUIDE.md:36`: "Always refer to the discipline and book title as **Architecture as Code** ... Avoid variations such as 'Architecture As Code' or 'architecture as code' unless quoting another source." Indexets "Soft As Code" bryter samma regel i omvänd riktning.
- **Förslag:** Skriv "Architecture as Code" på rad 5 och 254; välj en titelform ("The Interplay Between Soft 'as Code' Disciplines") i `book_index.json`, `book_structure.md` och kapitelrubriken.

### E2-35 "C4 models generated from Markdown" är oprecist
- **Fil:rad:** docs/23_soft_as_code_interplay.md:81
- **Påstående:** "This might take the form of models in DSLs such as Structurizr, C4 models generated from Markdown, or Terraform/CloudFormation modules representing architectural patterns."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** C4-modeller uttrycks i Structurizr DSL/JSON, C4-PlantUML, Mermaid-C4-syntax eller LikeC4; Markdown används i Structurizr för kompletterande dokumentation och ADR:er, inte för att generera modellen (https://docs.structurizr.com/dsl ; https://c4model.com/). Kapitel 22 i boken gör just den distinktionen mellan modelleringsverktyg och diagramverktyg.
- **Förslag:** "C4 models expressed in Structurizr DSL or C4-PlantUML, with Markdown used for the accompanying documentation".

## Verifierat korrekt (urval)

- Thoughtworks Technology Radar Vol. 21 publicerades november 2019 och innehåller tekniken "Security policy as code" i ring Trial (blip 15), med OPA och Istio som exempel – https://www.thoughtworks.com/radar/techniques/security-policy-as-code och Vol. 21-PDF:en.
- Open Policy Agent är ett CNCF graduated-projekt (4 februari 2021) – https://www.cncf.io/announcements/2021/02/04/cloud-native-computing-foundation-announces-open-policy-agent-graduation/
- HashiCorp Sentinel finns som policy-as-code-ramverk vid sidan av OPA i HCP Terraform – https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement
- GitHub Docs "About protected branches" (Source [4]) svarar 200 på angiven URL och beskriver skyddade grenar/obligatoriska granskare – https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Korsreferenserna `11_governance_as_code.md#governance-and-security-controls-as-code-backlog` (rubrik på rad 197) och `30_appendix_code_examples.md#21_code_1` (rad 691) finns; `docs/examples/structurizr/adrs/` innehåller tre ADR:er; filerna `03_version_control.md` och `14_practical_implementation.md` som knowledge-registry-exemplet refererar finns.
- GitHub Actions-sökvägsfiltret `docs/**.md` är giltigt: "`**`: Matches zero or more of any character" och exemplet `'**.js'` "Matches all .js files in the repository" – https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions
- `pyspelling --config` är en giltig flagga (`-c`/`--config`) och PyPI-paketen `pyspelling` (2.13) och `vale` (3.25.1.0) finns – https://facelessuser.github.io/pyspelling/ ; https://pypi.org/pypi/vale/json
- Netflix slutförde sin molnmigrering i januari 2016 efter sju år; sista rapporterade prenumerantsiffra 301,6 miljoner (Q4 2024), rapportering upphörde 2025 – https://about.netflix.com/news/completing-the-netflix-cloud-migration ; https://www.axios.com/2024/04/18/netflix-subscribers-count-stop-quarterly
- Stripe är tillgängligt för företag i 46 länder enligt Stripes egen sida (kapitel 21 rad 72) – https://stripe.com/en-gb-de/use-cases/global-businesses (via sökresultat)
- Backstage: öppen källkod mars 2020, CNCF Sandbox 2020-09-23, Incubating 2022-03-15 – https://backstage.io/blog/2020/09/23/backstage-cncf-sandbox ; https://cncf.io/blog/2022/03/15/backstage-project-joins-the-cncf-incubator
- "Spotify Model" bygger på Kniberg & Ivarssons whitepaper "Scaling Agile @ Spotify" (oktober 2012) – https://holub.com/goodies/SpotifyScaling.pdf
- Google Clouds suveränitetspartners är T-Systems (Tyskland) och Thales via S3NS (Frankrike) – https://www.datacenterdynamics.com/en/news/google-reaffirms-sovereign-cloud-solutions-for-eu/
- OVHcloud har SecNumCloud 3.2-kvalificering (Hosted Private Cloud; Bare Metal Pod mars 2025) – https://corporate.ovhcloud.com/en/newsroom/news/secnumcloud-strategy-acceleration/
- Microsofts EU Data Boundary slutfördes 2025-02-26 – https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/
- EU Cloud Code of Conduct godkändes under GDPR art. 40 i maj 2021 – https://dataprotectionauthority.be/publications/decision-n05-2021-of-20-may-2021.pdf
- Edmondson, *Teaming* (Jossey-Bass, 2012) existerar – ISBN 978-0-7879-7093-2.
- Terraform-backend-restriktionen, S3-backendens argumentlista och 1.10/1.11-ändringarna – https://developer.hashicorp.com/terraform/language/backend ; https://developer.hashicorp.com/terraform/language/backend/s3 ; https://developer.hashicorp.com/terraform/language/v1.11.x/upgrade-guides
- Kapitel 23:s påståenden om det egna innehållet (fem adoptionssteg, två scenarier, `team-norms.yaml`) stämmer med texten; `tests/test_chapter23_assets.py` verifierar att alla sex mindmaps och diagrammet finns (bekräftat i `docs/images/`).

## Ej verifierbart

- **docs/21_digitalisation.md:76 – Capital One 99,99 % / 40 % / 70 %.** Sökt i AWS- och CNCF-fallstudier, Data Center Knowledge, SiliconANGLE, BizTech 2025, CloudZero. Inget stöd hittat; se E2-03. Författaren bör ange källa eller stryka.
- **docs/21_digitalisation.md:44 – "up to 70 %" för IaC.** Ingen primärstudie hittad; se E2-11.
- **docs/21_digitalisation.md:72 – Stripe "built on Infrastructure as Code" och Netflix/Spotify-plattformarna "based on Infrastructure as Code".** Allmänt rimligt men inget företagsspecifikt belägg sökt fram; formuleringarna är marknadsmässiga snarare än faktapåståenden.
- **docs/21_digitalisation.md:202–204 – Spotifys "Automated compliance checking for GDPR and intellectual property rights", "time-to-market from weeks to hours".** Inga källor funna; Backstage-bloggar talar om onboarding-tid, inte GDPR-kontroller.
- **docs/21_digitalisation.md:250 – Scaleway "operated entirely within the EU with transparent supply-chain disclosure".** Scaleways dokumentationssida svarade 403 vid hämtning och sökbudgeten var slut. Regionerna Paris, Amsterdam och Warszawa ligger i EU enligt allmän kännedom, men "transparent supply-chain disclosure" kunde inte verifieras.
- **docs/33_references.md – IDC "Worldwide DevOps Software Tools Forecast, 2023–2027".** Endast DevSecOps-varianten (2023–2027) och DevOps-varianten för 2024–2028 hittades; exakt titel kunde inte bekräftas (se E2-15).
- **docs/26a_prerequisites_for_aac.md:39, 43 (utanför granskningsfilerna men pekar på kapitel 21):** hänvisar till "the burnout scenario warned about in Chapter 21" och "surprise budget cuts that destabilised earlier digital initiatives in Chapter 21" – kapitel 21 innehåller varken något utbrändhetsscenario eller någon diskussion om budgetnedskärningar. Bör följas upp av den som granskar kapitel 26A.
