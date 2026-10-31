<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Kapitel 7, 8, 9 och 9B

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, delmängd B2). Endast bedömning – inga filer i repot har ändrats.

## Omfattning

Lästa filer (varje rad, i sin helhet):

- `docs/07_containerisation.md` (311 rader)
- `docs/08_microservices.md` (218 rader)
- `docs/part_c_security.md` (24 rader)
- `docs/09_security_fundamentals.md` (295 rader)
- `docs/09b_security_patterns.md` (647 rader)

Stödfiler: `docs/book_index.json`, `docs/33_references.md` (Source [1]–[32]), samt grep i övriga kapitel för terminologi och korsreferenser (`docs/01_introduction.md`, `docs/10_policy_and_security.md`, `docs/11_governance_as_code.md`, `docs/15a_evidence_as_code.md`, `docs/images/`).

Inventering: cirka 140 kontrollerbara påståenden (statistik, citat/attribueringar, standarder/regelverk, verktyg/syntax i kodblock, historik, korsreferenser, källförteckningar). Cirka 90 av dessa kontrollerades mot primärkällor via webben (cirka 60 webbanrop: HashiCorp-, AWS-, Google-, Microsoft-, Kubernetes-, Linkerd-, Istio-, OPA-, Gatekeeper-, Thoughtworks-, CNCF/SlashData-, EDPB-, EBA-, CSA-, CIS-, ENISA-, FIRST- och NIST-sidor; tre CNCF/SlashData-PDF:er laddades ned och textextraherades lokalt). Resterande kontrollerades mot lokala filer. Webbsökbudgeten tog slut i slutskedet, vilket påverkade två sekundära kontroller (se "Ej verifierbart").

De fem filerna innehåller inga externa URL:er i löptexten (endast interna ankare till `33_references.md` samt exempeladresser i kod). Samtliga URL:er i de åberopade posterna Source [2], [5], [6], [7], [9], [10], [13], [16]–[20] i `33_references.md` kontrollerades med `curl` (statuskod + slutlig adress) och lästes.

## Sammanfattning

Kapitel 7 och 8 är tekniskt i stort sett sunda (Kubernetes-, Argo CD-, Helm-, Compose- och GKE-exemplen är giltiga), men kapitel 7:s inledande statistik från CNCF:s "State of Cloud Native Development 2024" (67 %/58 %/52 %) kan inte återfinnas i någon utgåva av rapportserien, och serien mäter utvecklare – inte organisationer; den senaste utgåvan ger 46 % (mikrotjänster) och 27 % (händelsedriven arkitektur). Kapitel 8:s centrala styrningskälla "Thoughtworks Technology Radar – Governance as Code" (Vol. 21, 2019) existerar inte som radar-blip; det som fanns i Vol. 21 är "Security policy as code". Kapitel 9 och 9B lider av allvarliga källproblem: GDPR betecknas som "Directive (EU) 2016/679", HashiCorp-källan "Terraform Security Best Practices" är i verkligheten sidan "Learn Terraform recommended practices" (en arbetsflödesguide utan det innehåll som tillskrivs den), Google- och HashiCorp-sidorna tillskrivs rekommendationer de inte innehåller, och minst två källor (ENISA "Cloud Security Guidelines for EU Organisations", OWASP "Application Security Architecture Guide") verkar inte existera. Flera standarder citeras med fel årtal (EDPB 2019/2020, EBA 2019, CSA v4.0 2017, CIS v8 2021) och NIST CSF beskrivs med fem funktioner trots att CSF 2.0 (feb 2024) har sex. Två kodexempel i 9B är trasiga: CloudTrail-selektorn använder den ogiltiga typen `AWS::KMS::Key` och Rego-regeln `encryption_enabled { ... }` kompilerar inte under `import rego.v1`. Dessutom innehåller kapitel 9 och 9B hårda radbrytningar mitt i ord (61 respektive 35 förekomster) som renderas som delade ord i den färdiga boken. Terraform-stateavsnittet (dubblerat i 9 och 9B) är delvis föråldrat: DynamoDB-låsning är deprecierad till förmån för S3-native låsning (`use_lockfile`), och "Terraform Cloud" heter HCP Terraform sedan april 2024.

## Fynd
### B2-01 CNCF-statistiken (67 %/58 %/52 %) kan inte återfinnas och beskriver fel population
- **Fil:rad:** docs/07_containerisation.md:9 (även :45, :90; docs/08_microservices.md:88; docs/01_introduction.md:17 upprepar "two thirds")
- **Påstående:** "The Cloud Native Computing Foundation's *State of Cloud Native Development 2024* report ... confirms that distributed architectures are now the norm: 67% of surveyed organisations run microservices in production and 58% operate event-driven workloads alongside them. The same research notes that 52% are investing in internal developer platforms"
- **Bedömning:** FEL / EJ VERIFIERBART
- **Allvarlighet:** Hög
- **Evidens:** Rapportserien heter "State of Cloud Native Development Qx YYYY" och produceras av SlashData för CNCF (CNCF:s rapportlista: https://www.cncf.io/lf-report-type/survey listar utgåvorna Q1 2025 (25 apr 2025), Q3 2025 (11 nov 2025), Q1 2026 (24 mar 2026) och Japan 2026; ingen utgåva med titeln "... 2024" finns listad). Q3 2025-rapporten (https://www.cncf.io/wp-content/uploads/2025/11/cncf_report_stateofcloud_111025a.pdf, textextraherad) anger: "46% are operating microservices" och "microservices ... adopted by 46% of backend developers", "event-driven architecture (27%)", samt "IDP usage has risen from 23% in Q3 2024 to 27% in Q3 2025". Populationen är utvecklare/backend-utvecklare, inte "surveyed organisations". Orden "governance", "audit trail" och "repeatability" förekommer inte i Q3 2025-rapporten, så påståendena på rad 9 ("the report identifies as critical"), rad 45 (policy-as-code-stöd) och rad 90 ("governance gaps observed in the CNCF research") samt kap. 8 rad 88 ("coupling signals") har inget stöd i källan. CNCF Annual Survey 2023 (https://www.cncf.io/reports/cncf-annual-survey-2023/) anger "66% of potential/actual consumers were using Kubernetes in production" – sannolikt ursprunget till "two thirds", men det gäller Kubernetes, inte mikrotjänster. Source [7] i `33_references.md` saknar URL.
- **Förslag:** Byt ut siffrorna mot verifierbara uppgifter med exakt utgåva, t.ex. "SlashData/CNCF, *State of Cloud Native Development Q3 2025*: 46 % av backend-utvecklarna använder mikrotjänster, 27 % händelsedriven arkitektur; andelen som använder interna utvecklarplattformar steg från 23 % (Q3 2024) till 27 % (Q3 2025)". Stryk formuleringarna om att rapporten identifierar styrning/revisionsspår som kritiska. Uppdatera Source [7] med korrekt titel, utgivare (SlashData för CNCF) och URL, och rätta `docs/01_introduction.md:17`.

### B2-02 "Thoughtworks Technology Radar – Governance as Code" (Vol. 21, 2019) är inte en radar-blip
- **Fil:rad:** docs/08_microservices.md:84 (även :217; docs/33_references.md:8 Source [2])
- **Påstående:** "Thoughtworks' Governance as Code guidance stresses that automating these controls is the sustainable path to consistent service quality across federated teams ([Thoughtworks Technology Radar – "Governance as Code"](33_references.md#source-2))" och i källförteckningen "**Thoughtworks Technology Radar (2024).** *Governance as Code.*"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** https://www.thoughtworks.com/radar/techniques/governance-as-code finns inte (omdirigeras till den generiska listan /radar/techniques). Blipen som faktiskt fanns i Vol. 21 är "Security policy as code" (https://www.thoughtworks.com/radar/techniques/security-policy-as-code: Trial nov 2019, Trial maj 2020, Adopt okt 2020). Webbsökning efter en Thoughtworks-blip "Governance as Code" gav inga träffar. Source [2]:s URL https://www.thoughtworks.com/about-us/news/2019/technology-radar-edition21 omdirigeras till den generiska nyhetssidan https://www.thoughtworks.com/about-us/news (länken är i praktiken bruten). Kapitel 8 anger dessutom årtalet 2024 medan Source [2] anger november 2019.
- **Förslag:** Ersätt med den faktiska blipen ("Security policy as code", Technology Radar Vol. 21, nov 2019 – Adopt Vol. 23, okt 2020, med radar-URL:en ovan) och omformulera texten så att den speglar vad blipen säger (policyer som kod: versionshantering, automatiserad validering, utrullning och övervakning; OPA och Istio nämns). Rätta årtalet i rad 217 och Source [2].

### B2-03 "HashiCorp – Terraform Security Best Practices (2023)" är i själva verket en arbetsflödesguide utan det tillskrivna innehållet
- **Fil:rad:** docs/09_security_fundamentals.md:209 (även :284; docs/09b_security_patterns.md:65, :636; docs/33_references.md:26 Source [20])
- **Påstående:** "**HashiCorp – “Terraform Security Best Practices” (2023) [Source [20]]:** details the policy guardrails, key management requirements, and secret-handling approaches HashiCorp recommends for enterprise Terraform programmes."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Source [20] pekar på https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices. Sidans H1 är "Learn Terraform recommended practices"; den beskriver en mognadsresa i tre delar (manuella ändringar → semi-automation → IaC → kollaborativ IaC) för team som inför HCP Terraform. Sidan innehåller ingen vägledning om nyckelhantering, kryptering eller hantering av hemligheter, och det finns ingen HashiCorp-publikation med titeln "Terraform Security Best Practices" från 2023 under "HashiCorp Learning Resources".
- **Förslag:** Stryk posten eller ersätt den med faktiska HashiCorp-källor för respektive påstående: "Manage sensitive data in your configuration" (https://developer.hashicorp.com/terraform/language/manage-sensitive-data) för hemligheter/state-kryptering, "Backend Type: s3" för backend-inställningar och HCP Terraform-dokumentationen "Policy enforcement" (https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement) för policyvakter. Ta bort formuleringen "key management requirements".

### B2-04 CloudTrail-exemplet använder en ogiltig datahändelsetyp (`AWS::KMS::Key`)
- **Fil:rad:** docs/09b_security_patterns.md:240-243 (kodblock, `aws_cloudtrail.security_audit`)
- **Påstående:** `data_resource { type = "AWS::KMS::Key" values = [aws_kms_key.org_key.arn] }` inuti ett `event_selector`-block
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** AWS CloudTrail API, DataResource: "You can specify the following *basic* event selector resource types: AWS::DynamoDB::Table, AWS::Lambda::Function, AWS::S3::Object. Additional resource types are available through *advanced* event selectors" (https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_DataResource.html). Terraform-providern (`aws_cloudtrail`, `event_selector.data_resource.type`): "You can specify only the following value: "AWS::S3::Object", "AWS::Lambda::Function" and "AWS::DynamoDB::Table"" (https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudtrail). KMS-anrop (Encrypt/Decrypt/GenerateDataKey) loggas som management events och täcks redan av `include_management_events = true`. `terraform apply` skulle misslyckas.
- **Förslag:** Ta bort `AWS::KMS::Key`-blocket (KMS-händelser fångas av management-loggningen) eller, om finkornig filtrering behövs, ersätt `event_selector` med `advanced_event_selector` (som inte kan kombineras med `event_selector`). Se även B2-25 om rekursiv loggning av loggbucketen.

### B2-05 Rego-exemplet kompilerar inte under `import rego.v1`
- **Fil:rad:** docs/09b_security_patterns.md:295-306
- **Påstående:** `import rego.v1` följt av `encryption_enabled {\n    input.resource.encryption.enabled == true\n}`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA:s uppgraderingsguide: "OPA v1.0 requires the usage of `if` and `contains` keywords when declaring rules"; exemplet `p { true }` listas som kompileringsfel i v1.0 medan `p if { true }` är giltigt (https://www.openpolicyagent.org/docs/v0-upgrade). `import rego.v1` aktiverar samma krav i OPA 0.59+ (Regal-regeln use-rego-v1, https://docs.styra.com/regal/rules/imports/use-rego-v1). Regeln `personal_data_encryption_required if {...}` på rad 298 använder korrekt `if`, så filen är internt inkonsekvent. Dessutom blandas två olika indatamodeller: `input.resource_type`/`input.attributes.tags` (rad 299–300) kontra `input.resource.encryption.enabled` (rad 305).
- **Förslag:** Skriv `encryption_enabled if {` och harmonisera indatamodellen (t.ex. `input.attributes.encryption.enabled` eller `input.resource.tags`). Kör `opa check --v1-compatible policies/` i CI så att exemplen i boken valideras.

### B2-06 GDPR betecknas som ett direktiv
- **Fil:rad:** docs/09_security_fundamentals.md:276 (även docs/09b_security_patterns.md:628)
- **Påstående:** "**Official Journal of the European Union.** *Directive (EU) 2016/679: General Data Protection Regulation.*"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** GDPR är en förordning: "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016" (EUR-Lex, https://eur-lex.europa.eu/eli/reg/2016/679/oj). Direktivet som GDPR ersatte var dataskyddsdirektivet 95/46/EG. Rättsaktstypen är central: en förordning är direkt tillämplig i medlemsstaterna, ett direktiv måste införlivas.
- **Förslag:** "European Parliament and Council (2016). *Regulation (EU) 2016/679 (General Data Protection Regulation).* Official Journal of the European Union, L 119, 4 May 2016."

### B2-07 `kubectl apply --server-side --dry-run=client` är en ogiltig flaggkombination
- **Fil:rad:** docs/07_containerisation.md:45
- **Påstående:** "tools such as `kubectl apply --server-side --dry-run=client`, `kubeval`, and `kubeconform` verify that every API field matches the targeted Kubernetes version"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** kubectl:s källkod (`pkg/cmd/apply/apply.go`, `ApplyOptions.Validate()`): `if o.DryRunStrategy == cmdutil.DryRunClient && o.ServerSideApply { return fmt.Errorf("--dry-run=client doesn't work with --server-side (did you mean --dry-run=server instead?)") }` (https://raw.githubusercontent.com/kubernetes/kubectl/master/pkg/cmd/apply/apply.go). Kommandot avbryts alltså med fel. Dessutom validerar en klientsidig dry-run inte mot "the targeted Kubernetes version" – det gör en serversidig dry-run mot det anslutna klustret, eller kubeconform med schema för angiven version.
- **Förslag:** Skriv `kubectl apply --server-side --dry-run=server -f manifests/` (kräver klusteråtkomst) och förtydliga att `kubeconform -kubernetes-version 1.31.0` är verktyget som validerar offline mot en vald version. Se B2-26 om `kubeval`.

### B2-08 NIST Cybersecurity Framework beskrivs med fem funktioner – CSF 2.0 har sex
- **Fil:rad:** docs/09_security_fundamentals.md:258 (även :266 och docs/09b_security_patterns.md:618 som anger "Cybersecurity Framework Version 1.1" (2018) som källa)
- **Påstående:** "The NIST Cybersecurity Framework offers a practical approach built around the functions Identify, Protect, Detect, Respond, and Recover."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Hög
- **Evidens:** NIST publicerade CSF 2.0 den 26 februari 2024 (NIST CSWP 29, https://doi.org/10.6028/NIST.CSWP.29; https://www.nist.gov/cyberframework). CSF 2.0 lade till funktionen Govern och har sex funktioner: Govern, Identify, Protect, Detect, Respond, Recover. Version 1.1 (april 2018) är ersatt. För en bok om styrning som kod är just Govern-funktionen den mest relevanta nyheten.
- **Förslag:** "The NIST Cybersecurity Framework 2.0 (February 2024) is built around six functions—Govern, Identify, Protect, Detect, Respond, and Recover—where the new Govern function maps directly onto governance-as-code concerns." Uppdatera källposten till "NIST (2024). *The NIST Cybersecurity Framework (CSF) 2.0.* NIST CSWP 29."

### B2-09 "ENISA (2023). Cloud Security Guidelines for EU Organisations" kan inte återfinnas
- **Fil:rad:** docs/09_security_fundamentals.md:270 (även docs/09b_security_patterns.md:622)
- **Påstående:** "**ENISA (2023).** *Cloud Security Guidelines for EU Organisations.* European Union Agency for Cybersecurity."
- **Bedömning:** EJ VERIFIERBART (sannolikt fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** Webbsökning på den exakta titeln gav inga träffar. ENISA:s faktiska molnpublikationer har andra titlar och årtal: "Cloud Security Guide for SMEs" (2015), "Security Framework for Governmental Clouds" (2015), "Good Practice Guide for securely deploying Governmental Clouds" (2013), "Cloud Security for Healthcare Services" (2021), samt EUCS-utkastet (certifieringsschema). Ingen ENISA-publikation från 2023 med denna titel kunde identifieras (https://www.enisa.europa.eu/publications).
- **Förslag:** Stryk posten eller ersätt med en verifierad ENISA-publikation med korrekt titel, år och URL. Eftersom posten inte refereras i löptexten kan den utgå utan följdändringar.

### B2-10 "OWASP (2023). Application Security Architecture Guide" existerar inte
- **Fil:rad:** docs/09_security_fundamentals.md:277 (även docs/09b_security_patterns.md:629)
- **Påstående:** "**OWASP (2023).** *Application Security Architecture Guide.* Open Web Application Security Project."
- **Bedömning:** EJ VERIFIERBART (sannolikt fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** Ingen OWASP-publikation med den titeln kunde hittas (owasp.org, wiki.owasp.org, webbsökning). Närmaste verkliga OWASP-dokument är Application Security Verification Standard (ASVS) 4.0.3 (okt 2021; ASVS 5.0 maj 2025), OWASP Developer Guide, OWASP Cheat Sheet Series och det äldre CISO AppSec Guide v2.
- **Förslag:** Ersätt med "OWASP Foundation (2025). *Application Security Verification Standard 5.0.*" (https://owasp.org/www-project-application-security-verification-standard/) eller stryk posten (den citeras inte i löptexten).

### B2-11 "HashiCorp – Securing Terraform State" (Source [16]) har annan titel och innehåller inte det som tillskrivs den
- **Fil:rad:** docs/09_security_fundamentals.md:205-207 (även :283; docs/09b_security_patterns.md:61-63, :635; docs/33_references.md:22)
- **Påstående:** "**HashiCorp – “Securing Terraform State” (2024) [Source [16]]:** instructs teams to store state in remote backends, enable state locking, and avoid local copies to eliminate workstation exposure and race conditions during deployment." samt "HashiCorp's definitive recommendations for safeguarding Terraform state"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Source [16]:s URL (/terraform/language/state/sensitive-data) omdirigeras till https://developer.hashicorp.com/terraform/language/manage-sensitive-data med H1 "Manage sensitive data in your configuration". Sidan behandlar känsliga värden i konfiguration och state, säger att state kan lagras i fjärrbackend och krypteras i vila ("The S3 backend ... can encrypt state at rest if you enable the `encrypt` option"; "HCP Terraform automatically encrypts state at rest"), men nämner varken state-låsning eller "race conditions". Det finns ingen HashiCorp-sida med titeln "Securing Terraform State".
- **Förslag:** Cita sidan med dess faktiska titel och begränsa det tillskrivna innehållet till fjärrlagring och kryptering i vila. Hänvisa till "State locking" (https://developer.hashicorp.com/terraform/language/state/locking) och "Remote state" (https://developer.hashicorp.com/terraform/language/state/remote) för låsning och fjärrbackends. Uppdatera URL:en i Source [16].

### B2-12 S3-backend: DynamoDB-låsning är deprecierad och "versioning" är ingen backend-inställning
- **Fil:rad:** docs/09_security_fundamentals.md:208 (även :213; docs/09b_security_patterns.md:64, :69)
- **Påstående:** "documents the `dynamodb_table`, `encrypt`, and `kms_key_id` settings that enforce DynamoDB-backed locking, server-side encryption, and versioning for Amazon S3 state backends"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Backend-dokumentationen (https://developer.hashicorp.com/terraform/language/backend/s3): "State locking is an opt-in feature of the S3 backend"; `use_lockfile` – "Whether to use a lockfile for locking the state file. Defaults to `false`"; "**DynamoDB-based locking is deprecated** and will be removed in a future minor version"; `dynamodb_table` – "(Optional, **Deprecated**)". S3-native låsning infördes experimentellt i Terraform 1.10 (nov 2024) och blev standardvägen i 1.11 (feb 2025). Versionshantering är ingen backend-inställning: "It is highly recommended that you enable Bucket Versioning on the S3 bucket" (en rekommendation för bucketen). Kapitel 13, 21 och appendix A använder också `dynamodb_table`.
- **Förslag:** "documents the `use_lockfile` (S3-native locking, Terraform ≥ 1.10; `dynamodb_table` is deprecated), `encrypt` and `kms_key_id` settings, and recommends enabling S3 Bucket Versioning on the state bucket". Byt "AWS S3 with DynamoDB locking" (rad 213, 9B rad 69) till "S3 with native lockfile locking".

### B2-13 Google Cloud-sidan rekommenderar inte kundhanterade krypteringsnycklar
- **Fil:rad:** docs/09_security_fundamentals.md:211 (även :213; docs/09b_security_patterns.md:67, :69)
- **Påstående:** "**Google Cloud – “Store Terraform state in Cloud Storage” (2024) [Source [19]]:** recommends uniform bucket-level access, object versioning, and customer-managed encryption keys to govern Terraform state"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Sidan (https://cloud.google.com/docs/terraform/resource-management/store-state, nu "Store Terraform state in a Cloud Storage bucket") visar en bucket med `uniform_bucket_level_access = true`, `versioning { enabled = true }` och `public_access_prevention = "enforced"`, men nämner varken kryptering, CMEK/Cloud KMS eller state-låsning. Påståendet om CMEK saknar stöd i den angivna källan (CMEK är i sig en rimlig rekommendation men måste då källbeläggas med Cloud Storage-dokumentationen för CMEK).
- **Förslag:** Begränsa referatet till det sidan faktiskt visar (enhetlig åtkomst på bucketnivå, objektversionering, blockerad publik åtkomst) och källbelägg CMEK separat (https://cloud.google.com/storage/docs/encryption/customer-managed-keys).

### B2-14 EDPB "upprätthåller" inte GDPR – det gör de nationella tillsynsmyndigheterna
- **Fil:rad:** docs/09_security_fundamentals.md:49
- **Påstående:** "GDPR enforced by the European Data Protection Board (EDPB)"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** EDPB:s egen beskrivning: "The data protection authorities are responsible for enforcing data protection law at a national level"; EDPB "ensures that the General Data Protection Regulation and the Law Enforcement Directive are applied consistently" och "takes binding decisions on cross-border cases on which no consensus is reached" (https://www.edpb.europa.eu/about-edpb/who-we-are/european-data-protection-board_en). Rättslig grund: GDPR art. 51–59 (tillsynsmyndigheter) och art. 68–70 (EDPB:s uppgifter).
- **Förslag:** "GDPR, enforced by national supervisory authorities (such as IMY in Sweden) and coordinated by the European Data Protection Board (EDPB) through the consistency mechanism".

### B2-15 "Audit logging aligned with GDPR Article 30" – artikel 30 gäller register över behandling
- **Fil:rad:** docs/09b_security_patterns.md:224
- **Påstående:** "# Comprehensive audit logging aligned with GDPR Article 30"
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** GDPR artikel 30 har rubriken "Records of processing activities" och ålägger den personuppgiftsansvarige att föra ett register över behandlingsverksamheter (https://gdpr-info.eu/art-30-gdpr/). Det är en dokumentationsskyldighet, inte ett krav på teknisk revisionsloggning. Tekniska loggningskrav härleds snarare ur artikel 32 (säkerhet i behandlingen) och artikel 5(2) (ansvarsskyldighet).
- **Förslag:** "# Audit logging supporting GDPR Article 32 (security of processing) and Article 5(2) accountability".

### B2-16 Gatekeeper-exemplet: fel objekttyp i kommentaren, fel beskrivning i texten och icke-standardiserad mall utan definition
- **Fil:rad:** docs/07_containerisation.md:47-62
- **Påstående:** "a minimal OPA Gatekeeper constraint that prohibits containers running as root" (rad 47), "# OPA Gatekeeper ConstraintTemplate — block privileged containers" (rad 50), `kind: K8sBlockPrivilegedContainers` med `allowPrivileged: false` (rad 52, 61)
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** YAML:en är en Constraint (`apiVersion: constraints.gatekeeper.sh/v1beta1`), inte en ConstraintTemplate (`templates.gatekeeper.sh/v1`). Löptexten säger "running as root" men policyn gäller privilegierade containrar – två olika kontroller (Gatekeeper-biblioteket har separata mallar: `K8sPSPPrivilegedContainer` respektive `K8sPSPAllowedUsers`). Bibliotekets mall för privilegierade containrar har kinden `K8sPSPPrivilegedContainer` och parametern `exemptImages`, inte `allowPrivileged` (https://open-policy-agent.github.io/gatekeeper-library/website/validation/privileged-containers/). Den egna kinden `K8sBlockPrivilegedContainers` fungerar bara om motsvarande ConstraintTemplate finns, vilken inte visas.
- **Förslag:** Använd bibliotekets mall: `kind: K8sPSPPrivilegedContainer` med `parameters: { exemptImages: [] }`, ändra kommentaren till "Constraint" och löptexten till "prohibits privileged containers" (eller byt till `K8sPSPAllowedUsers` med `runAsUser: { rule: MustRunAsNonRoot }` om root-förbud avses). Nämn att ConstraintTemplate måste installeras först.

### B2-17 AWS App Mesh har upphört
- **Fil:rad:** docs/08_microservices.md:102
- **Påstående:** "Istio, Linkerd, or AWS App Mesh policies can be generated from declarative manifests"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** AWS: "On September 30, 2026, AWS will discontinue support for AWS App Mesh. After September 30, 2026, you will no longer be able to access the AWS App Mesh console or AWS App Mesh resources"; nya kunder kunde inte onboardas efter 24 september 2024 (https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html). Per granskningsdatum (2026-10-30) är tjänsten nedlagd; AWS rekommenderar Amazon ECS Service Connect / VPC Lattice.
- **Förslag:** Byt till "Istio, Linkerd, or Cilium Service Mesh" (eller Amazon VPC Lattice för AWS-estat) och ta bort App Mesh.

### B2-18 "Azure Security Benchmark v3.0 (2023)" – omdöpt till Microsoft cloud security benchmark 2022
- **Fil:rad:** docs/09_security_fundamentals.md:282 (även docs/09b_security_patterns.md:634)
- **Påstående:** "**Microsoft (2023).** *Azure Security Benchmark v3.0.* Microsoft Security Documentation."
- **Bedömning:** FÖRÅLDRAT / FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Microsoft Learn: "Microsoft cloud security benchmark is the successor of Azure Security Benchmark (ASB), which was rebranded in October 2022" (https://learn.microsoft.com/en-us/security/benchmark/azure/overview). ASB v3 publicerades 2021; 2023 var namnet redan MCSB v1.
- **Förslag:** "Microsoft (2024). *Microsoft cloud security benchmark (MCSB) v1.* Microsoft Learn." med URL ovan.

### B2-19 CSA Security Guidance v4.0 är från 2017, inte 2023
- **Fil:rad:** docs/09_security_fundamentals.md:278 (även docs/09b_security_patterns.md:630)
- **Påstående:** "**Cloud Security Alliance (2023).** *Security Guidance v4.0.* Cloud Security Alliance."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** CSA släppte "Security Guidance for Critical Areas of Focus in Cloud Computing v4.0" den 26 juli 2017 (https://cloudsecurityalliance.org/press-releases/2017/07/26/security-guidance-v4; "Released: 07/26/2017"). Version 5 släpptes 15 juli 2024 (https://cloudsecurityalliance.org/artifacts/security-guidance-v5).
- **Förslag:** "Cloud Security Alliance (2024). *Security Guidance for Critical Areas of Focus in Cloud Computing v5.*" (eller v4.0 med årtalet 2017).

### B2-20 EDPB:s riktlinjer om inbyggt dataskydd antogs 2020 (v2.0), inte 2023
- **Fil:rad:** docs/09_security_fundamentals.md:272 (även docs/09b_security_patterns.md:624)
- **Påstående:** "**EDPB (2023).** *Guidelines on Data Protection by Design and by Default.* European Data Protection Board."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Det korrekta dokumentet är "Guidelines 4/2019 on Article 25 Data Protection by Design and by Default", version 1.0 nov 2019 (samråd), version 2.0 antagen 20 oktober 2020 (https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en). Ingen 2023-utgåva finns.
- **Förslag:** "EDPB (2020). *Guidelines 4/2019 on Article 25 Data Protection by Design and by Default, Version 2.0.* European Data Protection Board, 20 October 2020."

### B2-21 EBA:s riktlinjer om IKT- och säkerhetsrisk är från 2019, inte 2023
- **Fil:rad:** docs/09_security_fundamentals.md:275 (även docs/09b_security_patterns.md:627)
- **Påstående:** "**EBA (2023).** *Guidelines on ICT and Security Risk Management.* European Banking Authority."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** EBA/GL/2019/04 "Guidelines on ICT and security risk management", slutrapport 28 november 2019, tillämpliga från 30 juni 2020 (https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/internal-governance/guidelines-ict-and-security-risk-management). Ändrade genom EBA/GL/2025/02 (11 feb 2025) för att smalna av tillämpningsområdet när DORA började tillämpas.
- **Förslag:** "EBA (2019). *Guidelines on ICT and security risk management (EBA/GL/2019/04).* European Banking Authority (amended by EBA/GL/2025/02)."

### B2-22 "ENISA (2023). NIS2 Directive Implementation Guidance" – ENISA:s vägledning publicerades i juni 2025
- **Fil:rad:** docs/09_security_fundamentals.md:273 (även docs/09b_security_patterns.md:625)
- **Påstående:** "**ENISA (2023).** *NIS2 Directive Implementation Guidance.* European Union Agency for Cybersecurity."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** ENISA:s dokument heter "NIS2 Technical Implementation Guidance" (version 1.0, juni 2025), publicerat 26 juni 2025 (https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance); utkast på samråd nov 2024. Ingen ENISA-vägledning med detta namn fanns 2023.
- **Förslag:** "ENISA (2025). *NIS2 Technical Implementation Guidance, v1.0.* European Union Agency for Cybersecurity, June 2025."

### B2-23 "CMMI for security ... aligned with ENISA guidelines" saknar stöd
- **Fil:rad:** docs/09_security_fundamentals.md:256
- **Påstående:** "The Capability Maturity Model Integration (CMMI) for security supplies a five-level ladder from initial reactive practices to optimised proactive operations. European organisations can benchmark against industry peers by conducting regular CMMI assessments aligned with ENISA guidelines."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Det finns ingen modell som heter "CMMI for security". ISACA/CMMI Institute erbjuder "CMMI Cybermaturity Platform" (lanserad 2018; https://www.isaca.org/enterprise/cmmi-cybermaturity-platform), som är ett riskbaserat självskattningsverktyg kopplat till NIST CSF, COBIT och ISO. Ingen koppling mellan CMMI-bedömningar och "ENISA guidelines" kunde hittas; ENISA:s mognadsramverk (National Capabilities Assessment Framework, EU cyber crisis management maturity) riktar sig till medlemsstater, inte företag.
- **Förslag:** "Maturity models such as ISACA's CMMI Cybermaturity Platform or the NIST CSF 2.0 tiers provide a graded ladder..." och stryk hänvisningen till ENISA, eller källbelägg den.

### B2-24 `conftest test deployment/policies` använder conftest fel
- **Fil:rad:** docs/08_microservices.md:70-72
- **Påstående:** `- name: Enforce policy guardrails` / `run: |` / `conftest test deployment/policies`
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** `conftest test <files>` tar de konfigurationsfiler som ska testas som argument och letar policyer i `./policy` om inte `--policy/-p` anges: "Policies by default should be placed in a directory called `policy`, but this can be overridden with the `--policy` flag" (https://www.conftest.dev/). Kommandot i boken skulle försöka tolka Rego-filerna i `deployment/policies` som indata och utvärdera dem mot en obefintlig `policy/`-katalog.
- **Förslag:** `conftest test --policy deployment/policies deployment/helm/values.yaml deployment/terraform/tfplan.json` (plan-filen konverterad med `terraform show -json tfplan > tfplan.json`).

### B2-25 CloudTrail loggar datahändelser för sin egen loggbucket (rekursiv loggning)
- **Fil:rad:** docs/09b_security_patterns.md:229, 235-238
- **Påstående:** `s3_bucket_name = aws_s3_bucket.audit_logs[0].bucket` i kombination med `data_resource { type = "AWS::S3::Object" values = ["${aws_s3_bucket.audit_logs[0].arn}/*"] }`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** AWS: varje leverans av loggfiler är ett `PutObject`-anrop som i sig blir en datahändelse som levereras till samma bucket, "generating another event" – rekursiv loggning; AWS införde inställningen `RecursiveLogging` (standard på) just för detta (https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-trail-recursive-logging.html). Mönstret ger onödig volym och kostnad i ett exempel som presenteras som bästa praxis.
- **Förslag:** Logga S3-datahändelser för applikationsbucketar (inte loggbucketen) eller sätt `--no-recursive-logging`/`recursive_logging = false` när providern stöder det; lägg till en kommentar om rekursionsrisken.

### B2-26 `kubeval` är inte längre underhållet
- **Fil:rad:** docs/07_containerisation.md:45
- **Påstående:** "`kubeval`, and `kubeconform` verify that every API field matches the targeted Kubernetes version"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** kubeval:s README: "NOTE: This project is no longer maintained, a good replacement is kubeconform" (https://github.com/instrumenta/kubeval; arkiverat 2023).
- **Förslag:** Nämn endast `kubeconform` (och `kubectl --dry-run=server`), eventuellt med not om att kubeval är avvecklat.

### B2-27 CIS Controls v8 daterat 2023 och organisationsnamnet felstavat
- **Fil:rad:** docs/09_security_fundamentals.md:279 (även docs/09b_security_patterns.md:631)
- **Påstående:** "**CIS (2023).** *CIS Controls v8: Critical Security Controls for Effective Cyber Defence.* Centre for Internet Security."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** CIS Controls v8 publicerades i maj 2021; v8.1 (med en ny Governance-funktion i linje med NIST CSF 2.0) publicerades 24–25 juni 2024 (https://www.cisecurity.org/insights/white-papers/cis-critical-security-controls-v8-1). Organisationen heter "Center for Internet Security" (egennamn; ska inte anglifieras till "Centre").
- **Förslag:** "Center for Internet Security (2024). *CIS Critical Security Controls v8.1.*"

### B2-28 Hårda radbrytningar mitt i ord i kapitel 9 och 9B
- **Fil:rad:** docs/09_security_fundamentals.md:5-8, 40-43, 45-47, 51-53, 59-62 m.fl. (61 förekomster); docs/09b_security_patterns.md:11-19, 23-29, 33-35, 41-47, 51-55, 590-593, 607-614 (35 förekomster)
- **Påstående:** T.ex. rad 40–41: "...traditional defensive pract" / "ices. As organisations adopt..." (radslut mitt i ordet; ingen avstavning)
- **Bedömning:** FEL (formatering)
- **Allvarlighet:** Medel
- **Evidens:** `od -c` visar byte `\n` mitt i ordet ("c o n t e m p o r \n i c e s"); raderna är hårt brutna vid 128 tecken. Markdown/Pandoc renderar en radbrytning i ett stycke som blanksteg, så den färdiga texten får "pract ices", "complian ce", "sl owing", "incid ent" osv. i PDF, EPUB och på webbplatsen. (Träffarna i kap. 7 och 8 vid samma kontroll är enbart YAML-blockgränser och inte fel.)
- **Förslag:** Sammanfoga styckena till en rad per stycke (t.ex. `awk`/`pandoc --wrap=none`) och lägg till en test i `tests/test_clarity.py` som fångar rader som slutar mitt i ett ord följt av rad som börjar med gemen.

### B2-29 "Containers share network namespaces" – gäller bara inom en Pod
- **Fil:rad:** docs/09_security_fundamentals.md:239-240
- **Påstående:** "Containers share network namespaces and often communicate directly, bypassing traditional controls."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Kubernetes: "Every container in a Pod shares the network namespace, including the IP address and network ports" medan "Containers in different Pods have distinct IP addresses" (https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking). Containrar i olika poddar har egna nätverksnamnrymder; det är podd-till-podd-trafiken i ett platt klusternät som motiverar NetworkPolicy/CNI-kontroller.
- **Förslag:** "Containers within a pod share a network namespace, and pods communicate directly over a flat cluster network that bypasses traditional perimeter controls; CNI plug-ins and NetworkPolicy objects restore segmentation."

### B2-30 ECSO- och SANS-källorna kan inte återfinnas
- **Fil:rad:** docs/09_security_fundamentals.md:292-293 (även docs/09b_security_patterns.md:644-645)
- **Påstående:** "**European Cyber Security Organisation (2023).** *European Cybersecurity Survey 2023.* ECSO." och "**SANS Institute (2023).** *Security Architecture Design Principles.* SANS Institute."
- **Bedömning:** EJ VERIFIERBART
- **Allvarlighet:** Medel
- **Evidens:** Webbsökning hittar ingen ECSO-publikation "European Cybersecurity Survey 2023" (ECSO publicerar CISO-enkäter – 2021 och en årlig enkät med Bitdefender – samt marknadsrapporter, https://ecs-org.eu) och ingen SANS-publikation med titeln "Security Architecture Design Principles" (sans.org). Ingen av posterna refereras i löptexten.
- **Förslag:** Stryk posterna eller ersätt med verifierbara dokument med URL (t.ex. ECSO:s faktiska CISO-rapport eller NIST SP 800-160 Vol. 1 Rev. 1 för designprinciper).

### B2-31 Chapter 7 Source 3 har annan titel än den länkade Source [5]
- **Fil:rad:** docs/07_containerisation.md:307
- **Påstående:** "**HashiCorp (2024).** *Introduction to Infrastructure as Code with Terraform.* HashiCorp Developer Documentation. [Source [5]]"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Source [5] i `33_references.md` är "What is Terraform" (https://developer.hashicorp.com/terraform/intro, verifierad 200). HashiCorp-handledningen heter "What is Infrastructure as Code with Terraform?" (https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code). Ingen av dem heter "Introduction to Infrastructure as Code with Terraform".
- **Förslag:** Använd den faktiska titeln för den sida som avses och se till att den matchar posten i `33_references.md`.

### B2-32 "Terraform Cloud" heter HCP Terraform
- **Fil:rad:** docs/09_security_fundamentals.md:215, 225; docs/09b_security_patterns.md:71, 73
- **Påstående:** "audit trails from Terraform Cloud", "Terraform Cloud run tasks", "Terraform Cloud audit trails"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** "Effective April 22, 2024, Terraform Cloud is now HCP Terraform" (https://developer.hashicorp.com/terraform/cloud-docs). Source [20]:s URL-sökväg innehåller fortfarande "cloud-docs", vilket är korrekt tekniskt, men produktnamnet i löptext bör vara HCP Terraform.
- **Förslag:** Ersätt "Terraform Cloud" med "HCP Terraform (formerly Terraform Cloud)" vid första förekomsten, därefter "HCP Terraform".

### B2-33 Istio VirtualService använder `v1alpha3`
- **Fil:rad:** docs/08_microservices.md:108
- **Påstående:** `apiVersion: networking.istio.io/v1alpha3`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Istio 1.22 (maj 2024) befordrade VirtualService m.fl. till `networking.istio.io/v1` ("Introducing Istio v1 APIs", https://istio.io/latest/blog/2024/v1-apis/); referensdokumentationen använder `v1`. `v1alpha3` accepteras fortfarande men är inte längre rekommenderat. Fälten i exemplet (`route`, `weight`, `retries.attempts`, `perTryTimeout`) är korrekta.
- **Förslag:** `apiVersion: networking.istio.io/v1`.

### B2-34 "Federation APIs" (KubeFed) är avvecklat; Cluster API är ett projekt, inte en specifikation
- **Fil:rad:** docs/07_containerisation.md:41
- **Påstående:** "Federation APIs and the Cluster API specification capture cluster lifecycle operations in code"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** KubeFed (kubernetes-sigs/kubefed) arkiverades 25 april 2023 (https://github.com/kubernetes-retired/kubefed). Cluster API är ett Kubernetes SIG-projekt med CRD:er och controllers (https://cluster-api.sigs.k8s.io/), inte en "specifikation".
- **Förslag:** "Multi-cluster tooling such as Cluster API (cluster lifecycle), Karmada or Open Cluster Management captures cluster operations in code" och stryk "Federation APIs".

### B2-35 `node_count` tillsammans med `autoscaling` i GKE-nodpoolen
- **Fil:rad:** docs/07_containerisation.md:269, 281-284
- **Påstående:** `node_count = 3` kombinerat med `autoscaling { min_node_count = 1 max_node_count = 10 }`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Provider-dokumentationen för `google_container_node_pool`: `node_count` "should not be used alongside `autoscaling`" (https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_node_pool). Kombinationen ger plan-drift när autoskalaren ändrar antalet noder.
- **Förslag:** Byt `node_count = 3` mot `initial_node_count = 3` med `lifecycle { ignore_changes = [initial_node_count] }`, eller ta bort `node_count`.

### B2-36 `data.aws_region.current.name` är deprecierat
- **Fil:rad:** docs/09b_security_patterns.md:139, 151, 168
- **Påstående:** `"logs.${data.aws_region.current.name}.amazonaws.com"` m.fl.
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** AWS-providern (v6): `name` – "(Optional, **Deprecated**) Full name of the region to select. Use `region` instead." (https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region). Övriga argument i modulen (`customer_master_key_spec`, `enable_key_rotation`, `deletion_window_in_days`, `enable_log_file_validation`, `is_organization_trail`) är giltiga.
- **Förslag:** `data.aws_region.current.region`.

### B2-37 CVSS-poäng över 7,0 klassas som "CRITICAL"
- **Fil:rad:** docs/09b_security_patterns.md:472-476
- **Påstående:** `ThreatSeverity.CRITICAL if risk["cvss_score"] > 7.0 else ThreatSeverity.HIGH`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** CVSS v3.1, Qualitative Severity Rating Scale: High 7.0–8.9, Critical 9.0–10.0 (https://www.first.org/cvss/v3.1/specification-document, tabell 14). Koden avviker från den etablerade skalan (och klassar 7,0 exakt som HIGH men 7,1 som CRITICAL).
- **Förslag:** `CRITICAL if cvss >= 9.0 else HIGH if cvss >= 7.0 else MEDIUM ...`.

### B2-38 Föråldrade organisations-/publikationsuppgifter i källförteckningen (ISC2, NIST PQC, CERT-EU)
- **Fil:rad:** docs/09_security_fundamentals.md:268, 291, 295 (även docs/09b_security_patterns.md:620, 643, 647)
- **Påstående:** "**NIST (2023).** *Post-Quantum Cryptography Standardisation.*"; "**CERT-EU (2023).** *Cybersecurity Threat Landscape Report 2023.*"; "**(ISC)² (2023).** *Cybersecurity Workforce Study.*"
- **Bedömning:** FÖRÅLDRAT / FELCITERAT
- **Allvarlighet:** Låg
- **Evidens:** NIST:s PQC-standarder FIPS 203/204/205 blev slutgiltiga 13 augusti 2024 (https://csrc.nist.gov/projects/post-quantum-cryptography); 2023 fanns endast utkast. CERT-EU:s rapport heter "Threat Landscape Report 2023: Year Review" (v1.1, februari 2024, https://www.cert.europa.eu/publications/threat-intelligence/tlr2023/pdf) – utan "Cybersecurity" i titeln och publicerad 2024. (ISC)² bytte namn till ISC2 den 17 augusti 2023 (https://www.isc2.org/Insights/2023/08/cybersecurity-is-evolving-so-are-we); studien heter "ISC2 Cybersecurity Workforce Study".
- **Förslag:** "NIST (2024). *FIPS 203, 204 and 205: Post-Quantum Cryptography Standards.*"; "CERT-EU (2024). *Threat Landscape Report 2023: Year Review.*"; "ISC2 (2023). *ISC2 Cybersecurity Workforce Study.*"

### B2-39 Övriga vaga/ospårbara källposter i kapitel 7 och 9
- **Fil:rad:** docs/07_containerisation.md:306, 310, 311; docs/09_security_fundamentals.md:281, 288 (även docs/09b_security_patterns.md:633, 640)
- **Påstående:** "**Docker Inc.** *Docker Architecture as Code best practices.*"; "**Helm Community.** *Chart Development Guide.*"; "**Istio Project.** *Service Mesh Architecture.*"; "**Amazon Web Services (2023).** *AWS Security Best Practices.*"; "**Open Policy Agent (2023).** *OPA Policy Authoring Guide.* Cloud Native Computing Foundation."
- **Bedömning:** EJ VERIFIERBART
- **Allvarlighet:** Låg
- **Evidens:** Docker har ingen dokumentationssida om "Architecture as Code"; Helm-dokumentationen heter "Chart Template Guide"/"Chart Development Tips and Tricks"/"Chart Best Practices"; Istios sida heter "Architecture" (https://istio.io/latest/docs/ops/deployment/architecture/); AWS whitepaper "AWS Security Best Practices" (2016) är arkiverat till förmån för Well-Architected Security Pillar; OPA-dokumentationen har ingen "Policy Authoring Guide" (det finns Styra Academys kurs "OPA Policy Authoring" och OPA:s "Policy Language"-sida). Posterna saknar URL och år eller har fel utgivare.
- **Förslag:** Ge varje post exakt titel, år och URL (t.ex. "Docker Inc. *Building best practices.* https://docs.docker.com/build/building/best-practices/"; "Helm. *Chart Template Guide.* https://helm.sh/docs/chart_template_guide/"; "AWS. *Security Pillar – AWS Well-Architected Framework.*"; "OPA. *Policy Language.* https://www.openpolicyagent.org/docs/policy-language") eller stryk dem.

### B2-40 Delens titel stämmer inte med `book_index.json`; övergångstexten utelämnar kapitel i Del C
- **Fil:rad:** docs/part_c_security.md:2-5; docs/07_containerisation.md:297, 301 (även docs/01_introduction.md:71)
- **Påstående:** "# Part C: Security and Governance" / "\part{Security and Governance}" / "## Transition to Security and Governance"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `docs/book_index.json` (kanonisk källa) anger Del C:s titel som "Security, Governance & Assurance" och innehåller kapitel 9, 9B, 9C, 10, 11, 12 och 15A. Kapitel 7:s övergångstext nämner 9, 9B, 10, 11 och 12 men inte 9C ("Risk as Code and Threat Handling as Code") eller 15A ("Evidence as Code and Continuous Assurance"). CLAUDE.md beskriver dessutom Del C som kapitel 9–12.
- **Förslag:** Harmonisera titeln med `book_index.json` i `part_c_security.md`, kapitel 1 och kapitel 7, och komplettera övergångstexten med 9C och 15A.

### B2-41 Identiska källförteckningar i kapitel 9 och 9B; de flesta poster citeras aldrig; samma bild används i båda kapitlen
- **Fil:rad:** docs/09_security_fundamentals.md:264-295 och docs/09b_security_patterns.md:616-647; docs/09b_security_patterns.md:3
- **Påstående:** 30 identiska poster i båda kapitlen; `![Security as code workflow](images/diagram_11_chapter9.png)` i både kapitel 9 (rad 3) och 9B (rad 3)
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** `diff` av raderna 266–295 och 618–647 ger ingen skillnad. Poster som DORA, EBA, COBIT, MITRE ATT&CK, CSA, CIS, (ISC)² och NIST PQC nämns inte i någon av löptexterna. Kapitel 9B är enda kapitel utöver 9 som använder `diagram_11_chapter9.png`.
- **Förslag:** Behåll endast de källor som faktiskt refereras i respektive kapitel och ge 9B en egen diagramfil (`diagram_12_chapter9b.png`).

### B2-42 "Swedish" kontra "European" inramning i 9B
- **Fil:rad:** docs/09b_security_patterns.md:119, 315
- **Påstående:** "# Automated rotation in line with Swedish security expectations"; `"""Advanced threat detection for Swedish organisations"""`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Kapitlets rubriker och övriga kommentarer talar genomgående om "European organisations"/"European environments" (rad 57, 79, 89, 331, 359). Rester från en tidigare svenskinriktad version.
- **Förslag:** Ersätt "Swedish" med "European" (eller "EU") på båda ställena.

### B2-43 AsyncAPI-exemplet: JSON i ett `yaml`-block, äldre specversion och tveksam `publish`-semantik
- **Fil:rad:** docs/08_microservices.md:147-173
- **Påstående:** "```yaml" följt av JSON med `"asyncapi": "2.6.0"` och `"publish": { "message": ... }` beskrivet som "a saga choreography step captured as an AsyncAPI event schema"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** AsyncAPI 3.0.0 släpptes i december 2023 (https://www.asyncapi.com/blog/release-notes-3.0.0) och ersatte `publish`/`subscribe` med `send`/`receive` just för att 2.x-semantiken var förvirrande: i 2.x betyder `publish` att *applikationen tar emot* meddelanden som andra publicerar på kanalen. För en händelse som ordertjänsten själv skickar ut var 2.x-konventionen `subscribe`. Kodblocket är dessutom JSON men märkt `yaml` (giltigt eftersom JSON är en delmängd av YAML, men syntaxmarkeringen blir fel).
- **Förslag:** Uppgradera till `"asyncapi": "3.0.0"` med `operations: { sendOrderPaymentRequested: { action: send, channel: ... } }`, eller märk blocket ```json och förklara 2.x-semantiken.

### B2-44 NIS2 beskrivs som krav för "critical infrastructure"
- **Fil:rad:** docs/09_security_fundamentals.md:49
- **Påstående:** "NIS2 Directive requirements for critical infrastructure"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** NIS2 (direktiv (EU) 2022/2555) gäller "essential and important entities" i 18 sektorer enligt bilaga I och II (storleksbaserat urval); begreppet "kritiska entiteter" hör till CER-direktivet (EU) 2022/2557, och entiteter som pekas ut enligt CER blir automatiskt väsentliga entiteter enligt NIS2 (https://eur-lex.europa.eu/eli/dir/2022/2555/oj).
- **Förslag:** "NIS2 Directive requirements for essential and important entities".

### B2-45 Artikel 25 tillskrivs krav som hör till artikel 5
- **Fil:rad:** docs/09_security_fundamentals.md:200-201
- **Påstående:** "Privacy by design requirements from GDPR Article 25 demand data minimisation, purpose limitation, and automated deletion when retention periods expire."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Artikel 25(1) kräver tekniska och organisatoriska åtgärder "designed to implement data-protection principles, such as data minimisation"; ändamålsbegränsning och lagringsminimering är principer i artikel 5(1)(b) och (e). Artikel 25 nämner inte "automated deletion" – det är en möjlig implementering av lagringsminimering (https://gdpr-info.eu/art-25-gdpr/).
- **Förslag:** "Article 25 requires controllers to build in measures that implement the Article 5 principles—data minimisation, purpose limitation and storage limitation—for example through automated deletion when retention periods expire."

### B2-46 "container leases" i Azure Storage – det är blob-lån
- **Fil:rad:** docs/09_security_fundamentals.md:213 (jfr :210 "blob leases")
- **Påstående:** "Azure Storage with container leases"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** azurerm-backend låser state-bloben: "Azure Storage blobs are automatically locked before any operation that writes state" (https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage). Rad 210 och 9B rad 66 säger korrekt "blob leases".
- **Förslag:** "Azure Storage with blob leases".

### B2-47 Microsoft Learn-sidan "kräver" inte Entra ID/SAS
- **Fil:rad:** docs/09_security_fundamentals.md:210 (även docs/09b_security_patterns.md:66)
- **Påstående:** "requires Azure Storage accounts with encryption at rest, Microsoft Entra ID or SAS-based access control, and blob leases"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Sidan använder en lagringskontonyckel (`ARM_ACCESS_KEY`) i exemplet och säger endast: "In a production deployment, evaluate the available authentication options supported by the azurerm backend and use the most secure option" (https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage). Kryptering i vila och automatisk blob-låsning beskrivs korrekt.
- **Förslag:** "describes encryption at rest and automatic blob locking, and recommends evaluating the azurerm backend's authentication options (Microsoft Entra ID, managed identity, SAS) instead of account keys for production".

### B2-48 Flyway/Liquibase-migreringar är versionerade, inte idempotenta
- **Fil:rad:** docs/08_microservices.md:207
- **Påstående:** "Tools such as Flyway and Liquibase apply versioned, idempotent migration scripts from a controlled directory"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Flyways versionerade migreringar körs exakt en gång och spåras i `flyway_schema_history`; endast "repeatable migrations" (R__) återkörs vid checksum-ändring (https://documentation.red-gate.com/flyway/flyway-concepts/migrations). Liquibase spårar changesets i `DATABASECHANGELOG` på samma sätt. Idempotens är inte en egenskap hos skripten utan hos verktygets körningsmodell.
- **Förslag:** "apply versioned migration scripts exactly once per environment, tracked in a schema history table".

### B2-49 AWS CDK-källan (Source [9]) tillskrivs ett innehåll den inte uttrycker
- **Fil:rad:** docs/07_containerisation.md:86 (även :96)
- **Påstående:** "The AWS Cloud Development Kit guidance documents the same pattern for infrastructure as code pipelines: manifests and infrastructure definitions must pass unit tests, integration tests, and policy checks before promotion, with results stored in version control to support ongoing maintenance ([Source [9]])"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Source [9] är hela CDK Developer Guide (https://docs.aws.amazon.com/cdk/v2/guide/home.html, verifierad 200). Guidens CDK Pipelines-kapitel beskriver stegvisa stadier, tester och manuella godkännanden, men inte att "manifests" (Kubernetes) måste passera policykontroller eller att resultat lagras i versionskontroll.
- **Förslag:** Peka på det specifika avsnittet ("Continuous integration and delivery (CI/CD) using CDK Pipelines", https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html) och tona ned formuleringen till det guiden faktiskt säger.

### B2-50 Brutna relativa länkar i Source [10] som kapitel 8 åberopar
- **Fil:rad:** docs/33_references.md:16 (Source [10], citerad i docs/08_microservices.md:84, 216)
- **Påstående:** "[Chapter 10](10_policy_as_code.md)" och "[Chapter 32](32_index.md)"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Filerna `docs/10_policy_as_code.md` och `docs/32_index.md` finns inte (kanoniska filer är `10_policy_and_security.md` och `32_finos_project_blueprint.md` enligt `book_index.json`).
- **Förslag:** Rätta länkarna i Source [10]; kör `python3 scripts/verify_links.py`.

### B2-51 DORA tillskrivs Europeiska kommissionen
- **Fil:rad:** docs/09_security_fundamentals.md:274 (även docs/09b_security_patterns.md:626)
- **Påstående:** "**European Commission (2022).** *Regulation (EU) 2022/2554 on Digital Operational Resilience (DORA).* Official Journal of the European Union."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Låg
- **Evidens:** DORA antogs av Europaparlamentet och rådet den 14 december 2022 (EUT L 333, 27.12.2022; https://eur-lex.europa.eu/eli/reg/2022/2554/oj). Kommissionen föreslår men är inte utfärdare. DORA nämns inte i kapitlets löptext.
- **Förslag:** "European Parliament and Council (2022). *Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA).*"

## Verifierat korrekt (urval)

- S3-backendens `encrypt` ("Enable server side encryption of the state and lock files") och `kms_key_id` (KMS-nyckelns ARN för kryptering av state- och låsfiler) beskrivs korrekt – https://developer.hashicorp.com/terraform/language/backend/s3
- Azure Storage som Terraform-backend: automatisk blob-låsning före skrivning och kryptering i vila – https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage
- Google Cloud-sidans faktiska rekommendationer (uniform bucket-level access, objektversionering, blockerad publik åtkomst) – https://cloud.google.com/docs/terraform/resource-management/store-state
- HashiCorp-sidan bakom Source [16] rekommenderar fjärrlagring och kryptering i vila av state ("The S3 backend ... can encrypt state at rest if you enable the `encrypt` option"; HCP Terraform krypterar alltid state i vila) – https://developer.hashicorp.com/terraform/language/manage-sensitive-data
- CNCF Cloud Native Definition finns på den angivna adressen (v1.1, godkänd av TOC/GB 2024-02-26) – https://github.com/cncf/toc/blob/main/DEFINITION.md (Source [6])
- Source [5], [9], [10], [13], [17], [18], [19], [20] svarar HTTP 200 (Source [16] 301 → ny adress; Source [2] 301 → generisk nyhetssida, se B2-02)
- Thoughtworks-blipen "Security policy as code": Trial nov 2019 (Vol. 21), Trial maj 2020, Adopt okt 2020 – https://www.thoughtworks.com/radar/techniques/security-policy-as-code
- Istio: VirtualService-fälten `route[].destination.host/subset`, `weight`, `retries.attempts`, `perTryTimeout` är giltiga; API:erna befordrades till v1 i Istio 1.22 – https://istio.io/latest/blog/2024/v1-apis/
- Linkerd: annotationen `linkerd.io/inject: enabled` på namnrymd eller arbetslast aktiverar proxyinjektion med mTLS – https://linkerd.io/2-edge/features/proxy-injection/
- Gatekeeper: Constraint-objekt använder `constraints.gatekeeper.sh/v1beta1`; bibliotekets mall för privilegierade containrar är `K8sPSPPrivilegedContainer` – https://open-policy-agent.github.io/gatekeeper-library/website/validation/privileged-containers/
- `aws_kms_key`: `customer_master_key_spec` (standard `SYMMETRIC_DEFAULT`), `key_usage = "ENCRYPT_DECRYPT"`, `enable_key_rotation`, `deletion_window_in_days` är giltiga argument utan deprecieringsnoter – https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key
- `google_container_node_pool`/`google_container_cluster`-argumenten i kapitel 7 (`release_channel`, `workload_identity_config.workload_pool`, `addons_config`, `management.auto_repair/auto_upgrade`, `autoscaling.min/max_node_count`) är giltiga – https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_node_pool
- Argo CD `Application` med `syncPolicy.automated.prune/selfHeal` och Kubernetes `apps/v1 Deployment`/`v1 Service`-manifesten i kapitel 7 är syntaktiskt korrekta (kontrollerade mot API-referensen; inga deprecierade fält)
- GDPR artikel 33: anmälan till tillsynsmyndighet "without undue delay and, where feasible, not later than 72 hours" (kapitel 9B rad 420) – https://gdpr-info.eu/art-33-gdpr/
- Kubernetes: "Every container in a Pod shares the network namespace, including the IP address and network ports" – https://kubernetes.io/docs/concepts/workloads/pods/
- SOC 2 CC6 = Logical and Physical Access Controls; NIST SP 800-53 IA-2(1) = Multi-factor Authentication to Privileged Accounts (kapitel 9 rad 159) – https://www.tarleton.edu/security-controls-catalog/identification-and-authentication-ia/ia-21-identification-and-authentication-organizational-users-multifactor-authentication-to-privileged-accounts/
- NIST SP 800-53 Rev. 5 (september 2020) och ISO/IEC 27001:2022 (oktober 2022) citeras med rätt år; EDPB Guidelines 4/2019 och EBA/GL/2019/04 existerar (men med fel årtal i boken, se B2-20/B2-21)
- ENISA Threat Landscape 2023 (okt 2023) och CERT-EU Threat Landscape Report 2023 existerar – https://www.enisa.europa.eu/publications/enisa-threat-landscape-2023; https://www.cert.europa.eu/publications/threat-intelligence/tlr2023/pdf
- NIST CSF 1.1 publicerades i april 2018 (bokens årtal för 1.1 är korrekt, men versionen är ersatt – se B2-08)
- CNCF Annual Survey 2023: "66% of potential/actual consumers were using Kubernetes in production" – https://www.cncf.io/reports/cncf-annual-survey-2023/ (relevant som trolig källa till "two thirds" i kapitel 1)
- AWS App Mesh: nedläggningsdatum 30 september 2026 bekräftat av AWS – https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html

## Ej verifierbart

- **Siffrorna 67 %/58 %/52 % (B2-01):** Kunde inte återfinnas i Q1 2025- eller Q3 2025-utgåvan (båda textextraherade) eller på CNCF:s rapportsidor. Utgåvorna före 2025 (Q1 2020–Q3 2023) finns inte längre i CNCF:s rapportlista och kunde inte hämtas innan webbsökbudgeten tog slut; det kan inte helt uteslutas att en äldre utgåva innehåller liknande siffror för en specifik delpopulation, men formuleringen "surveyed organisations" är under alla omständigheter fel population för denna rapportserie.
- **Thoughtworks "Governance as Code" utanför Radar:** Det kan finnas Thoughtworks-artiklar om styrning som kod i Insights-serien; granskningen visar endast att det inte finns någon radar-blip med det namnet och att Source [2]:s URL är bruten.
- **ENISA "Cloud Security Guidelines for EU Organisations" (2023), OWASP "Application Security Architecture Guide" (2023), ECSO "European Cybersecurity Survey 2023", SANS "Security Architecture Design Principles" (2023):** Inga träffar vid sökning på exakta titlar (ENISA-, OWASP-, ECSO- och SANS-webbplatser samt allmän webbsökning). Bedömda som sannolika fantomkällor; författaren bör antingen ange URL eller stryka dem.
- **Chapter 7 Sources 2, 6 och 7 (Docker, Helm, Istio) samt chapter 9 Sources 16 och 23 (AWS, OPA):** Titlarna matchar ingen känd publikation och saknar URL/år; kan inte verifieras i nuvarande form.
- **Source [7] i `33_references.md`:** Saknar URL; den exakta utgåva författaren avser kan inte fastställas.
- **Påståendet att SlashData-rapporten "identifies [repeatability and audit trail] as critical" (kapitel 7 rad 9) och "highlights how sprawling integration surfaces create maintainability pressure" (kapitel 8 rad 88):** Inte återfunnet i de två tillgängliga utgåvorna; äldre utgåvor ej kontrollerade (se ovan).
- **Kommandot `helmfile apply --environment=...` och `redocly lint` (kapitel 8 rad 64, 77):** Flaggorna är kända och använda i dokumentationen men hann inte verifieras mot primärkällorna innan sökbudgeten var slut; inga indikationer på fel.
