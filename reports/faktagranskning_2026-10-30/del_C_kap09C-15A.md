<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del C, kapitel 9C, 10, 11, 12 och 15A

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, endast bedömning – inga filer i repot har ändrats).

## Omfattning

Lästa filer (varje rad, i sin helhet):

- `docs/09c_risk_and_threat_as_code.md` (91 rader)
- `docs/10_policy_and_security.md` (151 rader)
- `docs/11_governance_as_code.md` (213 rader)
- `docs/12_compliance.md` (272 rader)
- `docs/15a_evidence_as_code.md` (227 rader)

Stödfiler som lästs/grep:ats för intern konsistens: `docs/book_index.json`, `docs/33_references.md`, `docs/appendix_d_control_mapping_matrix_template.md`, relevanta avsnitt av `docs/30_appendix_code_examples.md` (10_CODE_1–10_CODE_4), `docs/images/`.

Inventerade påståenden: cirka 150 (källposter, standarder/regelverk, verktygs-API:er och kodblock, produktnamn, korsreferenser, siffror). Cirka 70 av dem har verifierats mot primärkällor via webben (NIST CSRC, OASIS, OPA-dokumentation och release notes, SLSA-specifikationen, Sigstore, HashiCorp, AWS-dokumentation, Thoughtworks Radar-PDF, anchore action.yml per tagg, CISA/NTIA, Microsoft Learn, OWASP). Samtliga URL:er i kapitlen har kontrollerats med curl. Kodblocken (YAML/JSON/jq) har validerats lokalt med PyYAML, `json` och `jq`. Rego-koden kunde inte köras lokalt (nedladdning/körning av OPA-binären nekades av behörighetssystemet); Rego-bedömningarna bygger därför på OPA:s officiella release notes och uppgraderingsguide. Webbsöknings-budgeten tog slut i slutfasen, vilket noteras under "Ej verifierbart".

Siffror/statistik: kapitlen innehåller inga externa statistiska påståenden (procentsatser, bötesbelopp, undersökningsresultat); de siffror som förekommer är interna målvärden (KPI-tabellen i kapitel 11) och exempeldata.

## Sammanfattning

Textinnehållet i de fem kapitlen är i huvudsak begreppsmässigt korrekt och kontrollerat försiktigt formulerat, men källapparaten och kodexemplen håller inte samma nivå. De allvarligaste problemen är: (1) tre Rego-block i kapitel 10 och 11 som inte kompilerar i OPA ≥ 1.0 – ett blandar `import rego.v1` med gammal regelsyntax, ett använder v0-syntax utan kompatibilitetsflagga och testmodulen refererar `governance.storage.deny` utan `data.`-prefix; (2) ett CI-steg i kapitel 11 som skriver `opa eval --format pretty` till fil och sedan läser filen som JSON; (3) källan "Thoughtworks Technology Radar, Governance as Code, Vol. 21, november 2019" – det finns ingen sådan blip; Vol. 21 innehåller "Security policy as code" (Trial), och kapitlet anger dessutom år 2024 medan referenslistan anger 2019; (4) SLSA-provenance-exemplet i 15A kombinerar predicateType "v1.0" (felaktig URI) med v0.2-schemats fält; (5) `anchore/scan-action@v3` ges en `output-file`-indata som inte finns förrän v6; (6) ISO-kontrollen "A.12.6.1" i 15A tillhör ISO 27001:2013 (motsvarar 8.8 i 2022-utgåvan) trots att boken i övrigt använder 2022-strukturen; (7) kapitel 12:s källista består av fyra–fem titlar som inte kunnat återfinnas hos de angivna utgivarna. Därtill finns ett antal föråldrade produkt- och tjänstenamn (Azure Sentinel, AWS Fault Injection Simulator, Open Web Application Security Project, DynamoDB-låsning för Terraform-state, Lambda python3.9) och inkonsekvenser mellan kapitlens kontrollkartläggning (IAM-01 vs SEC-ID-001, artefaktsökvägar) och mellan kapitlens källistor och `docs/33_references.md`.

## Fynd

### C-01 Rego-utdrag med `import rego.v1` använder gammal regelsyntax (kompilerar inte)
- **Fil:rad:** docs/10_policy_and_security.md:48-62 (samma fel i bilagan docs/30_appendix_code_examples.md:3289, 3305, 3366, 3404)
- **Påstående:** "```rego … import rego.v1 … encryption_compliant[resource] { resource := input.resources[_] … }```"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA:s kompatibilitetsdokumentation: "The `rego.v1` import makes OPA apply all restrictions that are enforced by default in OPA v1.0" (https://www.openpolicyagent.org/docs/v0-compatibility). Uppgraderingsguiden: "OPA v1.0 requires the usage of `if` and `contains` keywords when declaring rules" (https://www.openpolicyagent.org/docs/v0-upgrade). Release notes för OPA v1.0.0 (publicerad 20 december 2024): "Using `if` for all rule definitions and `contains` for multi-value rules is now mandatory, not just when using the `rego.v1` import." (https://github.com/open-policy-agent/opa/releases/tag/v1.0.0). En partiell mängdregel skriven som `encryption_compliant[resource] { … }` är därför ett parsefel både med `import rego.v1` (alla OPA-versioner som stöder importen) och i OPA ≥ 1.0 utan import. Dessutom är `validate_encryption(resource)` odefinierad i utdraget och heter `validate_encryption_strength` i bilagan.
- **Förslag:** Skriv `encryption_compliant contains resource if { … }` (och motsvarande `network_security_violations contains violation if`, `data_sovereignty_compliant contains resource if` i bilagan). Ange i brödtexten att exemplen kräver OPA ≥ 0.59 med `import rego.v1` eller OPA ≥ 1.0.

### C-02 Rego-exempel i v0-syntax utan import – fungerar inte i OPA 1.x
- **Fil:rad:** docs/10_policy_and_security.md:101-125
- **Påstående:** "```rego package enterprise.identity.mfa … violation[identity] { identity := input.identities[_] … }```"
- **Bedömning:** FEL / INKONSEKVENT
- **Allvarlighet:** Hög
- **Evidens:** Se C-01 (OPA v1.0.0 release notes). Blocket saknar `import rego.v1`, använder `violation[identity] { … }` och ger "compile error" i OPA ≥ 1.0 om inte `--v0-compatible` används (https://www.openpolicyagent.org/docs/v0-upgrade). Samma kapitel använder `import rego.v1` i blocket ovan, så boken lär ut två inkompatibla stilar utan att förklara skillnaden. Kapitel 11 använder genomgående korrekt v1-syntax (`deny contains msg if`).
- **Förslag:** `import rego.v1` + `violation contains identity if { … }`. Lägg till en mening om att OPA 1.0 (december 2024) gjorde `if`/`contains` obligatoriska.

### C-03 OPA-testmodul refererar en annan package utan `data.`-prefix
- **Fil:rad:** docs/11_governance_as_code.md:144-174
- **Påstående:** "test_denies_missing_encryption if { count(governance.storage.deny) > 0 with input as { … } }"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** I Rego nås regler i andra paket via `data.<package>` eller en explicit `import data.governance.storage`. Inom `package governance.storage_test` är `governance` varken lokal variabel, regel eller import; referensen tolkas som en obunden variabel och `opa test`/`opa check` avbryter med kompileringsfel (unsafe var). Jämför OPA:s testdokumentation som genomgående använder `data.`-prefix eller import (https://www.openpolicyagent.org/docs/policy-testing). Dessutom testar `test_allows_cmk_encryption` en resurs av typen `aws_s3_bucket`, medan regeln SEC-STOR-002 bara träffar typen `aws_s3_bucket_server_side_encryption_configuration` – testet passerar trivialt och verifierar inte CMK-logiken.
- **Förslag:** Lägg till `import data.governance.storage` och skriv `count(storage.deny) > 0 with input as …` (alternativt `data.governance.storage.deny`). Komplettera med ett testfall som använder resurstypen `aws_s3_bucket_server_side_encryption_configuration` med `sse_algorithm: "aws:kms"`.

### C-04 CI-steget skriver `--format pretty` till fil och läser den som JSON
- **Fil:rad:** docs/11_governance_as_code.md:117-138
- **Påstående:** "opa eval --data policies/ --input tfplan.json --format pretty "data.governance[_].deny[msg]" | tee policy-results.json … results = json.load(open("policy-results.json")) … for r in results["result"]"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA CLI-referensen listar `--format` för `opa eval` som `json, values, bindings, pretty, source, raw, discard` och beskriver "--format=json : output raw query results as JSON" (https://www.openpolicyagent.org/docs/cli). `pretty` ger en människoläsbar tabell, så `json.load` kastar `JSONDecodeError`. Vidare: när inga överträdelser finns skriver `opa eval --format json` `{}`, och `results["result"]` ger `KeyError: 'result'` (verifierat lokalt med en simulering av parsern). Pipelinen skulle alltså fallera även i det lyckade fallet.
- **Förslag:** Använd `--format json`, och skriv `for r in results.get("result", [])`. Överväg `opa eval --fail-defined` som enklare felmekanism.

### C-05 Fantomkälla: Thoughtworks Technology Radar "Governance as Code", Vol. 21 (2019) – och årtalskonflikt 2024/2019
- **Fil:rad:** docs/11_governance_as_code.md:213; docs/33_references.md:8 och 150
- **Påstående:** "**Thoughtworks Technology Radar (2024).** *Governance as Code.* Thoughtworks. [Source [2]]" respektive "Thoughtworks Technology Radar. *Governance as Code.* Thoughtworks Technology Radar Vol. 21, November 2019. Available at: https://www.thoughtworks.com/about-us/news/2019/technology-radar-edition21 [blip introduced Vol. 21; archived from techniques listing]"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Vol. 21-PDF:en (https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2019/11/tr_technology_radar_vol_21_en.pdf, hämtad och textgenomsökt) innehåller ingen blip "Governance as Code". Den tekniken som finns är blip 15 "Security policy as code" i ringen TRIAL. Frasen "governance as code" förekommer endast i temat "What's new": "This topic concerning policy, compliance and governance as code reappeared multiple times in our conversations … infrastructure as code, and now automated governance." Blip-sidan https://www.thoughtworks.com/radar/techniques/security-policy-as-code visar Nov 2019 Trial, May 2020 Trial, Oct 2020 Adopt. URL:en https://www.thoughtworks.com/radar/techniques/governance-as-code omdirigeras till den generella teknik-listningen (ingen sådan blip). Den citerade nyhets-URL:en omdirigeras i dag till https://www.thoughtworks.com/about-us/news (generisk sida). Kapitel 11 anger år 2024, referenslistan 2019.
- **Förslag:** Byt källan till "Thoughtworks. *Security policy as code.* Technology Radar Vol. 21 (Trial), november 2019; Vol. 23 (Adopt), oktober 2020. https://www.thoughtworks.com/radar/techniques/security-policy-as-code" och – om temat ska citeras – ange att "policy, compliance and governance as code" nämns som tema i Vol. 21:s inledning. Harmonisera årtalet i kapitel 11 och `33_references.md`.

### C-06 SLSA-provenance-exemplet blandar v1-predicateType (felstavad) med v0.2-schema
- **Fil:rad:** docs/15a_evidence_as_code.md:143-175
- **Påstående:** "\"_type\": \"https://in-toto.io/Statement/v0.1\", \"predicateType\": \"https://slsa.dev/provenance/v1.0\", … \"predicate\": { \"builder\": …, \"buildType\": …, \"invocation\": { \"configSource\": … }, \"buildConfig\": {}, \"metadata\": { \"buildStartedOn\": …, \"completeness\": … } }"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** SLSA Provenance v1 (https://slsa.dev/spec/v1.0/provenance): predicateType är exakt `https://slsa.dev/provenance/v1` (specifikationen anger att strängen alltid ska skrivas utan minor-version); fälten är `buildDefinition { buildType, externalParameters, internalParameters, resolvedDependencies }` och `runDetails { builder { id }, metadata { invocationId, startedOn, finishedOn }, byproducts }`; `invocation`, `configSource`, `buildConfig`, `metadata.buildStartedOn` och `completeness` finns inte i v1 (migreringsnoterna: "buildStartedOn renamed to startedOn", "completeness … now implicit"). Statement-typen för v1 är `https://in-toto.io/Statement/v1`. De fält boken använder tillhör SLSA Provenance v0.2 (predicateType `https://slsa.dev/provenance/v0.2`, Statement `v0.1`; https://slsa.dev/spec/v0.2/provenance). buildType-strängen `…/slsa-github-generator/container@v1` är den som slsa-github-generator använder i v0.2-provenance. Observera även att SLSA-specifikationen i dag är v1.2 (v1.0 markerad "Retired").
- **Förslag:** Antingen sätt `"predicateType": "https://slsa.dev/provenance/v0.2"` och behåll fälten (och beskriv det som v0.2-format, det som slsa-github-generator faktiskt ger), eller skriv om exemplet till v1-schemat med `_type: https://in-toto.io/Statement/v1`, `buildDefinition`/`runDetails`.

### C-07 `anchore/scan-action@v3` har ingen `output-file`-indata (och v3 är föråldrad)
- **Fil:rad:** docs/15a_evidence_as_code.md:96-103 och 131-133
- **Påstående:** "uses: anchore/scan-action@v3 with: sbom: … output-format: json output-file: artefacts/vulnerability-report.json fail-build: true severity-cutoff: critical" samt "The vulnerability report produced by the scan step becomes an evidence artefact in its own right."
- **Bedömning:** FEL / FÖRÅLDRAT
- **Allvarlighet:** Hög
- **Evidens:** `action.yml` på taggen v3 (https://raw.githubusercontent.com/anchore/scan-action/v3/action.yml) definierar indatana `image, path, sbom, fail-build, output-format, severity-cutoff, only-fixed, add-cpes-if-none, by-cve, grype-version, vex` – ingen `output-file`; `output-format` tillåter `json, sarif, table`. v4 och v5 saknar också `output-file`; indatan introduceras först i v6 (https://raw.githubusercontent.com/anchore/scan-action/v6/action.yml). Senaste utgåvan är v7.4.2 (https://github.com/anchore/scan-action/releases). Med `@v3` ignoreras indatan (GitHub Actions varnar "Unexpected input(s)"), filen `artefacts/vulnerability-report.json` skapas aldrig och det "evidensartefakt" texten beskriver existerar inte; rapportsökvägen finns i stället i utdatat `json`.
- **Förslag:** Pinna `anchore/scan-action@v7` (eller minst v6) och behåll `output-file`; alternativt använd `steps.<id>.outputs.json` och kopiera filen till `artefacts/`.

### C-08 ISO 27001-kontroll "A.12.6.1" tillhör 2013-utgåvan
- **Fil:rad:** docs/15a_evidence_as_code.md:118
- **Påstående:** "\"iso_27001\": [\"A.12.6.1\"],"
- **Bedömning:** FÖRÅLDRAT / INKONSEKVENT
- **Allvarlighet:** Hög
- **Evidens:** ISO/IEC 27001:2022 Annex A har 93 kontroller i fyra teman (5 Organisational, 6 People, 7 Physical, 8 Technological); numreringen A.5–A.18 från 2013 används inte längre. 2013-kontrollen A.12.6.1 "Management of technical vulnerabilities" (och A.18.2.3) motsvarar kontroll 8.8 "Management of technical vulnerabilities" i 2022-utgåvan (t.ex. https://www.isms.online/iso-27001/annex-a-2022/8-8-management-of-technical-vulnerabilities-2022/, https://www.upguard.com/compliance/iso-27001/8-8). Boken refererar själv "ISO/IEC 27001:2022" (Source [14]) och använder 2022-teman (A.5/A.8) i kapitel 10 och 12.
- **Förslag:** Ersätt med `"iso_27001": ["A.8.8"]` (ev. även A.5.21 "Managing information security in the ICT supply chain" för SBOM-aspekten).

### C-09 Kapitel 12:s källista: titlar som inte kunnat återfinnas
- **Fil:rad:** docs/12_compliance.md:268-272
- **Påstående:** "1. **IEEE Computer Society.** *Quantum Computing Impact on Infrastructure.* IEEE Quantum Computing Standards. 2. **Green Software Foundation.** *Sustainable Infrastructure Patterns.* Green Software Principles. 3. **NIST.** *Post-Quantum Cryptography Standards.* … 4. **Cloud Native Computing Foundation.** *Future of Cloud Native Infrastructure.* CNCF Research. 5. **Gartner Research (2024).** *Infrastructure and Operations Technology Trends 2024.* Gartner IT Infrastructure Reports."
- **Bedömning:** FELCITERAT / EJ VERIFIERBART
- **Allvarlighet:** Hög
- **Evidens:** (1) Ingen IEEE Computer Society-publikation med titeln "Quantum Computing Impact on Infrastructure" hittades; närmaste träff är arXiv-preprinten "Cybersecurity in the Quantum Era: Assessing the Impact of Quantum Computing on Infrastructure" (Baseri, Chouhan, Ghorbani, 2024, https://arxiv.org/abs/2404.10659), som inte är en IEEE-publikation. (2) Green Software Foundation publicerar "Green Software Patterns" (https://patterns.greensoftware.foundation) och "Principles of Green Software Engineering" – ingen "Sustainable Infrastructure Patterns". (4) CNCF har "CNCF Annual Cloud Native Survey" och "State of Cloud Native Development" (https://www.cncf.io/reports/) – ingen rapport "Future of Cloud Native Infrastructure". (5) Gartners faktiska publikation är pressmeddelandet "Gartner Identifies the Top Trends Impacting Infrastructure and Operations for 2024", 5 december 2023 (https://www.gartner.com/en/newsroom/press-releases/2023-12-5-gartner-identifies-the-top-trends-impacting-infrastructure-and-operations-for-2024). (3) NIST-posten är korrekt i sak men opreciserad: de färdiga standarderna är FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) och FIPS 205 (SLH-DSA), 13 augusti 2024 (https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Ingen av posterna är kopplad till `33_references.md`.
- **Förslag:** Ersätt 1, 2 och 4 med verifierbara källor (t.ex. arXiv 2404.10659 om den avses; GSF "Green Software Patterns"-katalogen; CNCF Annual Survey 2024/2025), ange Gartner-pressmeddelandets korrekta titel och datum, och precisera NIST-posten till FIPS 203/204/205 (2024). Lägg in posterna i den numrerade referenslistan.

### C-10 Felaktigt namn och årtal för STIX/TAXII
- **Fil:rad:** docs/09c_risk_and_threat_as_code.md:89
- **Påstående:** "**OASIS (2022).** *STIX/TAXII Standards: Structured Threat Intelligence Expression and Transport Specifications.* OASIS Open."
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** OASIS tillkännagivande 23 juni 2021 "STIX V2.1 and TAXII V2.1 OASIS Standards are published" (https://www.oasis-open.org/?p=7287): STIX = "Structured Threat Information Expression", TAXII = "Trusted Automated Exchange of Indicator Information"; båda godkändes som OASIS Standards den 10 juni 2021. Specifikationerna: https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html och https://docs.oasis-open.org/cti/taxii/v2.1/os/taxii-v2.1-os.html.
- **Förslag:** "OASIS (2021). *STIX Version 2.1* och *TAXII Version 2.1*, OASIS Standards, 10 juni 2021." Rätta namnet till "Structured Threat Information Expression".

### C-11 Källa "Chaos Engineering for Security" hittas inte; "AWS Fault Injection Simulator" är föråldrat namn
- **Fil:rad:** docs/09c_risk_and_threat_as_code.md:91
- **Påstående:** "**Gremlin & AWS.** *Chaos Engineering for Security.* Gremlin Platform Documentation and AWS Fault Injection Simulator Documentation."
- **Bedömning:** FELCITERAT / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Gremlins sidindex (https://www.gremlin.com/llms.txt) innehåller ingen sida med titeln "Chaos Engineering for Security" (endast t.ex. "Security Overview", "Chaos Engineering for Financial Services"). AWS:s dokumenthistorik: "Name change of AWS FIS – Updated service name to AWS Fault Injection Service – November 15, 2023" (https://docs.aws.amazon.com/fis/latest/userguide/doc-history.html); aktuell dokumentation heter "What is AWS Fault Injection Service?" (https://docs.aws.amazon.com/fis/latest/userguide/what-is.html).
- **Förslag:** Byt till verifierbara källor för avsnittet "security chaos engineering", t.ex. Rinehart, A. & Shortridge, K. *Security Chaos Engineering* (O'Reilly, 2023) och "AWS Fault Injection Service User Guide" (AWS, 2024). Uppdatera tjänstenamnet.

### C-12 Källtiteln "Policy as Code Overview" finns inte hos OPA
- **Fil:rad:** docs/10_policy_and_security.md:149; docs/11_governance_as_code.md:212; docs/33_references.md:16 och 114
- **Påstående:** "**Open Policy Agent (2024).** *Policy as Code Overview.* CNCF OPA Project. [Source [10]]"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** Den angivna URL:en https://www.openpolicyagent.org/docs leder till dokumentationens startsida med titeln "Open Policy Agent (OPA)" och rubrikerna "Writing Policies with Rego", "Install and Run OPA", "Next Steps"; frasen "Policy as Code Overview" förekommer inte på sidan. Dessutom länkar referensposten Source [10] till icke-existerande filer `10_policy_as_code.md` och `32_index.md` (verifierat med `ls`).
- **Förslag:** Citera som "Open Policy Agent. *OPA Documentation* (Introduction / Policy Language). CNCF, åtkomst 2026-10." och rätta länkarna i `33_references.md` till `10_policy_and_security.md` och `32_finos_project_blueprint.md`.

### C-13 HashiCorp-källan har fel titel och olika årtal i kapitel och referenslista
- **Fil:rad:** docs/10_policy_and_security.md:151; docs/33_references.md:26
- **Påstående:** "**HashiCorp (2024).** *Terraform Security Best Practices.* HashiCorp Learning Resources. [Source [20]]" (referenslistan: "HashiCorp Learning Resources, 2023")
- **Bedömning:** FELCITERAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** URL:en https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices har titeln "Learn Terraform recommended practices" och tillhör HCP Terraform-dokumentationen; frasen "Terraform Security Best Practices" förekommer inte på sidan. Kapitlet anger 2024, referensposten 2023. Kapitel 10 citerar inte heller något i texten som bygger på denna sida.
- **Förslag:** "HashiCorp. *Terraform recommended practices.* HCP Terraform documentation." med ett årtal; eller byt till en källa som faktiskt handlar om säkerhet (t.ex. "Sensitive data in state", https://developer.hashicorp.com/terraform/language/state/sensitive-data).

### C-14 SSDF-kartläggningen för SBOM pekar på fel praktiker
- **Fil:rad:** docs/15a_evidence_as_code.md:117
- **Påstående:** "\"nist_ssdf\": [\"PO.1.3\", \"PS.3.1\"],"
- **Bedömning:** FEL (opreciserad kartläggning)
- **Allvarlighet:** Medel
- **Evidens:** NIST SP 800-218 (SSDF v1.1, februari 2022, https://doi.org/10.6028/NIST.SP.800-218), textutdrag från PDF:en: PS.3.1 "Securely archive the necessary files and supporting data (e.g., integrity verification information, provenance data) to be retained for each software release."; PS.3.2 "Collect, safeguard, maintain, and share provenance data for all components of each software release (e.g., in a software bill of materials [SBOM])."; PO.1.3 "Communicate requirements to all third parties who will provide commercial software components to the organization for reuse by the organization's own software." SSDF:s egen mappningstabell kopplar EO 14028 §4e(vii) (SBOM till köpare) enbart till PS.3.2. Den praktik som uttryckligen avser SBOM saknas alltså i bokens lista.
- **Förslag:** `"nist_ssdf": ["PS.3.2"]` (ev. tillsammans med PS.3.1 för arkivering); ta bort PO.1.3 eller motivera den.

### C-15 S3-krypteringspolicyn använder objekt-sökväg där Terraform-JSON har listor; policyn träffar inte
- **Fil:rad:** docs/11_governance_as_code.md:59-86 (jämför testdata 165-168)
- **Påstående:** "rule := resource.values.rule[_] … rule.apply_server_side_encryption_by_default.sse_algorithm == \"AES256\"" och "not resource.values.server_side_encryption_configuration"
- **Bedömning:** TVEKSAMT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** I AWS-providerns schema är `rule` ett block ("Currently, only a single rule is supported") och `apply_server_side_encryption_by_default` ett nästlat block (https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/s3_bucket_server_side_encryption_configuration.html.markdown). Nästlade block i SDKv2-providers serialiseras som JSON-arrayer i `terraform show -json`, vilket kapitlets eget testfall också visar (`"apply_server_side_encryption_by_default": [ { "sse_algorithm": … } ]`, rad 166–168). Policyns `rule.apply_server_side_encryption_by_default.sse_algorithm` (objektåtkomst) blir därför odefinierad och SEC-STOR-002 larmar aldrig. Vidare: giltiga `sse_algorithm`-värden är `AES256`, `aws:kms`, `aws:kms:dsse`; om `kms_master_key_id` saknas vid `aws:kms` används AWS-hanterade nyckeln `aws/s3` – att enbart neka `AES256` upptäcker alltså inte "default AWS key" så som kommentaren hävdar. För `aws_s3_bucket` (provider ≥ 4) är `server_side_encryption_configuration` ett beräknat/avvecklat attribut som i planen kan vara `[]` – en tom lista är inte falsk i Rego, så `not …` slår inte till.
- **Förslag:** `rule.apply_server_side_encryption_by_default[_].sse_algorithm` och neka `sse_algorithm != "aws:kms" or not kms_master_key_id`; kontrollera `count(resource.values.server_side_encryption_configuration) == 0` eller evaluera resursen `aws_s3_bucket_server_side_encryption_configuration` i stället.

### C-16 Rekommenderar DynamoDB-låsning av Terraform-state, som är avvecklad
- **Fil:rad:** docs/11_governance_as_code.md:204
- **Påstående:** "Deliver a Terraform module for Amazon S3 with DynamoDB state locking … asserts S3 encryption and DynamoDB locking via `aws` CLI."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** HashiCorps S3-backend-dokumentation: "DynamoDB-based locking is deprecated and will be removed in a future minor version"; `dynamodb_table` är märkt "(Optional, Deprecated)"; i stället `use_lockfile` – "Whether to use a lockfile for locking the state file. Defaults to `false`." (https://developer.hashicorp.com/terraform/language/backend/s3). S3-nativ låsning infördes i Terraform 1.10 och blev standardrekommendation i 1.11 (sekundärkällor; versionsnumren ej bekräftade i primärdokumentet).
- **Förslag:** Skriv "Amazon S3 with native S3 state locking (`use_lockfile = true`)" och nämn DynamoDB endast som äldre mönster under utfasning; uppdatera acceptanstestet.

### C-17 "Azure Sentinel" heter Microsoft Sentinel
- **Fil:rad:** docs/10_policy_and_security.md:68
- **Påstående:** "Policy evaluation logs stream to SIEM platforms such as Splunk or Azure Sentinel for immutable evidence."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Produkten döptes om till Microsoft Sentinel i samband med Microsoft Ignite i november 2021 (Microsofts namnbytesöversikt och produktdokumentation; t.ex. https://www.schneider.im/microsoft-azure-products-name-changes).
- **Förslag:** "Microsoft Sentinel".

### C-18 "Quantum-safe"-Terraform-exemplet är varken kvantsäkert eller komplett, och PQC-kommentaren är inaktuell
- **Fil:rad:** docs/12_compliance.md:187-252 (särskilt 207, 210-212, 249)
- **Påstående:** "ecdsa_curve = \"P384\"  # P-384 provides 192-bit classical security; migrate to NIST PQC algorithms (ML-KEM, ML-DSA) when available" … "certificate_body = tls_self_signed_cert.quantum_safe.cert_pem" … "Protocol = \"TLS1.3-PQC\""
- **Bedömning:** FÖRÅLDRAT / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** NIST publicerade FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) och FIPS 205 (SLH-DSA) den 13 augusti 2024 (https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) – "when available" är inaktuellt. Resursen `tls_self_signed_cert.quantum_safe` definieras inte i listningen, så `terraform validate` fallerar. Inget i koden är post-kvant: ECDSA P-384 (giltigt värde enligt providern, https://github.com/hashicorp/terraform-provider-tls/blob/main/docs/resources/private_key.md), AES-256 KMS-nyckel och taggar som "TLS1.3-PQC" påverkar inte protokollvalet. Rubriken "Quantum-safe Security Implementation" blir därmed missvisande.
- **Förslag:** Lägg till `resource "tls_self_signed_cert" "quantum_safe"`, byt rubriken till "Crypto-agility baseline (pre-PQC)", uppdatera kommentaren till "NIST PQC standards FIPS 203/204/205 published August 2024; ACM/ALB support for hybrid PQ-TLS is rolling out" och ta bort taggar som ger sken av PQC.

### C-19 Serverless-exemplet använder avvecklad Lambda-runtime och avvecklad konfigurationsnyckel
- **Fil:rad:** docs/12_compliance.md:124-138, 155, 163
- **Påstående:** "runtime: python3.9" … "iamRoleStatements:" … "MODEL_BUCKET: ${self:custom.modelBucket}" … "OPTIMISATION_TABLE: ${self:service}-optimisation-${self:provider.stage}"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** AWS Lambda-runtime-tabellen: Python 3.9 avvecklad 15 december 2025 (block create 29 juli 2027, block update 31 augusti 2027); stödda Python-runtimes är 3.10–3.14 (https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html). Serverless Framework avvecklade `provider.iamRoleStatements` till förmån för `provider.iam.role.statements` (deprecationskod PROVIDER_IAM_SETTINGS, v3; https://www.serverless.com/framework/docs-deprecations). `custom`-sektionen (modelBucket, tensorflowLayer) saknas, och `${self:provider.stage}` förutsätter att `provider.stage` är satt.
- **Förslag:** `runtime: python3.12` (eller 3.13), `provider.iam.role.statements`, lägg till en `custom:`-sektion och använd `${sls:stage}`.

### C-20 Kontrollkartläggning och artefaktsökvägar skiljer sig mellan kapitel 10, 12 och 15A
- **Fil:rad:** docs/12_compliance.md:39; docs/10_policy_and_security.md:118, 121-124; docs/15a_evidence_as_code.md:39-59
- **Påstående:** Kapitel 12: "| SEC-ID-001 | … | `ci/policy-report.json`, `evidence/mfa-snapshot-202501.json` | … | Article 32 | IAM-01 |"; kapitel 10 och 15A: "\"internal\": [\"SEC-ID-001\"]"; 15A skriver artefakterna till `artefacts/policy-report.json` och `artefacts/mfa-snapshot-${SNAPSHOT_DATE}.json`.
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Samma kontroll (SEC-ID-001) får den interna mappningen "IAM-01" i matrisen men "SEC-ID-001" i policyn och i evidensmanifestet; artefaktsökvägarna i matrisen (`ci/…`, `evidence/…`) motsvarar inte vad pipelinen i 15A producerar (`artefacts/…`). Kapitel 12 hänvisar uttryckligen till båda ("the policy module and evidence pipeline each execute once").
- **Förslag:** Välj en intern identifierare (t.ex. "IAM-01" som internt policy-ID och SEC-ID-001 som kontroll-ID, förklarat i texten) och använd samma sökvägar i alla tre kapitel.

### C-21 Ramverksmappningen för MFA-kontrollen är för grov (ISO-teman i stället för kontroller; bara privilegierade konton i NIST)
- **Fil:rad:** docs/10_policy_and_security.md:113-119; docs/12_compliance.md:39; docs/15a_evidence_as_code.md:51
- **Påstående:** "\"iso_27001\": [\"A.5\", \"A.8\"], … \"nist_800_53\": [\"IA-2(1)\", \"AC-2\"]" för "Enforce MFA for all human identities in production"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** I ISO/IEC 27001:2022 är A.5 och A.8 teman (Organisational controls, 37 kontroller; Technological controls, 34 kontroller), inte kontroller; relevanta kontroller är 5.15 Access control, 5.17 Authentication information och 8.5 Secure authentication (som uttryckligen tar upp MFA). I NIST SP 800-53 Rev 5 (OSCAL-katalogen, version 5.2.0) heter IA-2(1) "Multi-factor Authentication to Privileged Accounts" och IA-2(2) "Multi-factor Authentication to Non-privileged Accounts"; en kontroll för "all human identities" behöver båda. SOC 2-mappningen CC6.1/CC6.6 är rimlig (sekundärkällor).
- **Förslag:** `"iso_27001": ["A.5.15", "A.5.17", "A.8.5"]`, `"nist_800_53": ["IA-2(1)", "IA-2(2)", "AC-2"]` i alla tre kapitel samt i matrisen.

### C-22 "Evaluate MFA policy" kör enhetstester, inte en utvärdering – rapporten är inte kontrollevidens
- **Fil:rad:** docs/15a_evidence_as_code.md:38-39 och 67
- **Påstående:** "- name: Evaluate MFA policy  run: opa test policies/identity --format=json > artefacts/policy-report.json" … "The job produces a manifest and two evidence files."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** `opa test` kör policyns egna testfall mot fixturer (flaggan `--format=json` finns: `pretty, json, gobench`, https://www.openpolicyagent.org/docs/cli) och säger ingenting om de faktiska identiteterna i `mfa-snapshot-*.json`. Evidens för kontrollens tillstånd kräver `opa eval -d policies/identity -i artefacts/mfa-snapshot-<YYYYMM>.json 'data.enterprise.identity.mfa.violation' --format json`. Dessutom skapas inte katalogen `artefacts/` innan omdirigeringen (`> artefacts/policy-report.json` fallerar på en ren runner).
- **Förslag:** Lägg till `mkdir -p artefacts`, kör snapshot-steget före policysteget och byt till `opa eval` mot snapshoten; behåll `opa test` som separat kvalitetssteg.

### C-23 Struktur och korsreferenser stämmer inte med `book_index.json`
- **Fil:rad:** docs/12_compliance.md:260-264; docs/15a_evidence_as_code.md:1 och 3; docs/10_policy_and_security.md:99
- **Påstående:** Kapitel 12: "we now shift focus to the practical delivery … Part D examines … [Chapter 13 on Testing Strategies]"; 15A: "# Evidence as Code {#evidence-as-code}" och "![Evidence pipeline …](images/diagram_12_compliance.png)"; kapitel 10: "the **assure once, comply many** mindset introduced in [Governance as Code](11_governance_as_code.md)"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` placerar 15A ("Evidence as Code and Continuous Assurance") sist i Part C, efter kapitel 12 – övergångstexten i kapitel 12 hoppar därmed över 15A. Rubriken i 15A ("Evidence as Code") avviker från indexets titel. 15A återanvänder kapitel 12:s figur 12.1 (`diagram_12_compliance.png`) med en annan alt-text; ingen dedikerad 15A-bild finns i `docs/images/`. Kapitel 10 presenterar principen som "introduced in" kapitel 11, som kommer efter kapitel 10 i läsordningen.
- **Förslag:** Flytta övergångsavsnittet "Moving from Governance to Delivery" till slutet av 15A (eller nämn 15A i kapitel 12), harmonisera 15A:s rubrik med indexet, ge 15A en egen figur eller korrekt figurtext, och skriv "introduced in … (Chapter 11, below)" eller flytta definitionen till kapitel 10.

### C-24 Kapitlens källistor och `33_references.md` stämmer inte överens
- **Fil:rad:** docs/33_references.md:16-17, 20, 26, 178; docs/09c_risk_and_threat_as_code.md:84-91; docs/12_compliance.md:266-272; docs/15a_evidence_as_code.md:221-227
- **Påstående:** Referenslistan: "Source [11] … Referenced in: Chapter 09, Chapter 11, Chapter 12"; "Source [14] … Referenced in: Chapter 12, Chapter 15A"; "Source [20] … Referenced in: Chapter 9, Chapter 9b"; "All citations in the manuscript are included in this compiled list".
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Kapitel 10 citerar Source [11] och [20] men nämns inte under dem; kapitel 11 och 12 citerar inte Source [11]; varken kapitel 12 eller 15A citerar Source [14] (ISO 27001). Ingen av källposterna i kapitel 9C (6 st), kapitel 12 (5 st) eller 15A (5 st) finns i den numrerade listan, i strid med påståendet på rad 178. Source [10] länkar till filer som inte finns (se C-12).
- **Förslag:** Generera "Referenced in"-listorna automatiskt från kapitlens Sources-avsnitt (t.ex. utöka `scripts/verify_sources.py`) och lägg in 9C/12/15A-källorna som numrerade poster.

### C-25 Kapitel 10 beskriver bilagans listningar fel (PSD2, UK, paketnamn)
- **Fil:rad:** docs/10_policy_and_security.md:46, 49, 87 (jämför docs/30_appendix_code_examples.md:3284, 3287, 3526)
- **Påstående:** "contains a full example tailored for EU and UK regulators" … "package eu.enterprise.security" … "import NIST controls, overlay GDPR Article 32, and incorporate PSD2 requirements in one document"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** 10_CODE_1 i bilagan beskrivs som "network segmentation checks inspired by MSB guidance, and GDPR Article 44 data residency controls" (svensk MSB, ingen UK-koppling) och har `package se.enterprise.security`. 10_CODE_2 "merges controls from NIST SP 800-53 with GDPR Article 32 and MSB network segmentation expectations" – PSD2 förekommer inte någonstans i listningen (grep på "psd2" ger inga träffar).
- **Förslag:** Skriv "tailored for EU regulators (Swedish MSB guidance and GDPR)" , använd samma paketnamn i kapitel och bilaga, och ersätt "PSD2 requirements" med "MSB network-segmentation expectations" (eller lägg till PSD2-kontroller i listningen).

### C-26 Produkt- och organisationsnamn: föråldrade eller angliciserade former
- **Fil:rad:** docs/09c_risk_and_threat_as_code.md:53, 87, 88; docs/11_governance_as_code.md:206
- **Påstående:** "the Microsoft Threat Modelling Tool"; "**OWASP.** *OWASP Threat Dragon.* Open Web Application Security Project."; "**Microsoft.** *STRIDE Threat Modelling Methodology.* Microsoft Security Development Lifecycle Documentation."; "link Security Command Centre alerts"
- **Bedömning:** FÖRÅLDRAT / FELCITERAT
- **Allvarlighet:** Låg
- **Evidens:** OWASP:s styrelse beslutade i februari 2023 att ändra namnet till "Open Worldwide Application Security Project" (https://owasp.org/board/meetings/202302.15; https://en.wikipedia.org/wiki/OWASP). Microsofts produkt heter "Microsoft Threat Modeling Tool" och sidan som beskriver STRIDE heter "Threats - Microsoft Threat Modeling Tool" (https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) – det finns ingen publikation med titeln "STRIDE Threat Modelling Methodology". Googles produkt heter "Security Command Center". Egennamn bör inte anpassas till brittisk stavning (jfr `docs/STYLE_GUIDE.md`).
- **Förslag:** "Open Worldwide Application Security Project", "Microsoft Threat Modeling Tool", källtitel "Threats – Microsoft Threat Modeling Tool (STRIDE model)", "Security Command Center".

### C-27 Fyrfasmodellen för säkerhetsautomation presenteras som fakta utan källa
- **Fil:rad:** docs/10_policy_and_security.md:15-22, 34; docs/11_governance_as_code.md:53
- **Påstående:** "Security automation in modern enterprises has matured through four distinct phases. … Phase 1: Manual validation | 2010–2015 … Phase 3: Policy engine integration | 2018–2021 … Phase 4 | 2021–present"; "OPA has become the de facto standard for policy automation"; "Open Policy Agent (OPA) is the most widely adopted engine for policy as code."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Periodiseringen saknar källa och är författarens egen; OPA lanserades 2016 och Gatekeeper 2018–2019, så "2018–2021" är rimligt som adoptionsfas men inte som etablerat faktum. "De facto standard"/"most widely adopted" är marknadspåståenden utan belägg (OPA:s CNCF-graduering 2021 kan användas som indikator).
- **Förslag:** Märk tabellen som "author's synthesis" eller ange källor; mjuka upp till "a widely adopted, CNCF-graduated engine (2021)".

### C-28 Terminologi- och utgåvedetaljer kring standarder
- **Fil:rad:** docs/10_policy_and_security.md:80, 127, 150; docs/33_references.md:17
- **Påstående:** "NIS2 directives"; "SOC 2 Trust Service Criteria"; "**NIST (2020).** *Security and Privacy Controls for Information Systems and Organisations.* NIST Special Publication 800-53, Revision 5, 2020."
- **Bedömning:** FELCITERAT / Låg precision
- **Allvarlighet:** Låg
- **Evidens:** NIS2 är ett enda direktiv (2022/2555). AICPA:s ramverk heter "Trust Services Criteria" (TSP Section 100, 2017 med 2022-reviderade points of focus); bilaga D använder den korrekta formen. NIST:s officiella titel stavas "…Information Systems and Organizations" (https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final; publicerad september 2020, uppdaterad 10 december 2020); NIST gav ut Release 5.2.0 den 27 augusti 2025 – fortfarande Rev 5, men värt att nämna.
- **Förslag:** "the NIS2 Directive"; "Trust Services Criteria"; behåll originaltitelns stavning och lägg till "(Release 5.2.0, 2025)" om boken vill vara aktuell.

### C-29 Mindre precisionsbrister i kapitel 15A
- **Fil:rad:** docs/15a_evidence_as_code.md:71, 115, 141, 226
- **Påstående:** "Supply chain Levels for Software Artefacts (SLSA)"; "datetime.datetime.utcnow().isoformat() + \"Z\""; "Regulatory frameworks such as the US Executive Order on Improving the Nation's Cybersecurity and the EU Cyber Resilience Act increasingly require SBOM disclosure."; källa "NTIA – Minimum Elements for a Software Bill of Materials" (2021)
- **Bedömning:** Låg precision / FÖRÅLDRAT (delvis)
- **Allvarlighet:** Låg
- **Evidens:** Officiellt namn: "Supply-chain Levels for Software Artifacts, or SLSA ('salsa')" (https://slsa.dev/). `datetime.utcnow()` är avvecklad sedan Python 3.12 (bokens låsta version). EO 14028 §4(e)(vii) kräver SBOM till köparen ("providing a purchaser a Software Bill of Materials … directly or by publishing it on a public website"); CRA (förordning (EU) 2024/2847, bilaga I del II punkt 1) kräver att tillverkaren upprättar en SBOM som lämnas till marknadskontrollmyndigheter på motiverad begäran – ingen publik "disclosure"-plikt. CISA publicerade ett utkast "2025 Minimum Elements for a SBOM" för kommentarer 22 augusti–3 oktober 2025 som bygger vidare på NTIA 2021 (https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom).
- **Förslag:** "Supply-chain Levels for Software Artifacts"; `datetime.now(datetime.timezone.utc).isoformat()`; "require manufacturers to produce and, on request or to purchasers, provide SBOMs"; lägg till CISA 2025-utkastet som kompletterande källa.

## Verifierat korrekt (urval)

- OSCAL utvecklas av NIST och stöder XML, JSON och YAML; modellerna är Catalog, Profile (och Mapping) i kontrollagret, Component Definition och SSP i implementationslagret samt Assessment Plan, Assessment Results och POA&M i bedömningslagret – kapitel 10:s tabell (fyra modeller) är korrekt men ofullständig. https://pages.nist.gov/OSCAL/ och https://pages.nist.gov/OSCAL/learn/concepts/layer/
- NIST SP 800-53 Rev 5: publicerad september 2020, uppdaterad 10 december 2020; kontrolltitlar AC-2 "Account Management", IA-2(1) "Multi-factor Authentication to Privileged Accounts", SI-2 "Flaw Remediation" (OSCAL-katalogen, https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json; https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).
- NIST SP 800-30 Rev. 1 "Guide for Conducting Risk Assessments", september 2012, status Final. https://csrc.nist.gov/pubs/sp/800/30/r1/final
- NIST SP 800-218 (SSDF v1.1), februari 2022, DOI-länken fungerar. https://doi.org/10.6028/NIST.SP.800-218
- ISO/IEC 27001:2022 Annex A: 93 kontroller i fyra teman (5 Organisational 37, 6 People 8, 7 Physical 14, 8 Technological 34). https://certpro.com/hub/iso-27001/controls/iso-27001-controls-list/ (sekundärkälla; ISO-texten är betalvara)
- STRIDE beskrivs på Microsoft Learn som Microsofts modell i Threat Modeling Tool (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- Threat Modeling Manifesto finns och listar bl.a. Adam Shostack, Izar Tarandach och Avi Douglen som författare samt de fyra frågorna. https://www.threatmodelingmanifesto.org/
- OWASP Threat Dragon finns (fri, öppen källkod, stöder STRIDE, CIA, LINDDUN). https://owasp.org/www-project-threat-dragon/
- OPA: `opa test` har `--format` med värdena `pretty, json, gobench`; `opa eval` har `--format json|values|bindings|pretty|source|raw|discard`. https://www.openpolicyagent.org/docs/cli
- OPA 1.0 gjorde `if`/`contains` obligatoriska (20 december 2024). https://github.com/open-policy-agent/opa/releases/tag/v1.0.0
- Kapitel 11:s Rego-policyer för kryptering och taggar använder korrekt v1-syntax (`import rego.v1`, `deny contains msg if`, `in`, mängdkomprehension); GitHub Actions-YAML i kapitel 11 och 15A samt serverless-YAML i kapitel 12 är syntaktiskt giltig YAML (PyYAML); SLSA-JSON är giltig JSON; jq-kommandot i 15A kör och ger avsett manifest (testat lokalt).
- Syft genererar CycloneDX- och SPDX-SBOM:er (`-o cyclonedx-json`, `-o spdx-json`) och stöder källan `dir` (katalog på disk). https://github.com/anchore/syft, https://github.com/anchore/syft/wiki/supported-sources
- `anchore/sbom-action@v0` har indatana `image`, `format` (default `spdx-json`), `artifact-name`, `output-file`. https://raw.githubusercontent.com/anchore/sbom-action/main/action.yml
- Cosign KMS-URI för Google Cloud KMS: `gcpkms://projects/$PROJECT/locations/$LOCATION/keyRings/$KEYRING/cryptoKeys/$KEY[/versions/$KEY_VERSION]`; dokumentations-URL:en i 15A svarar 200. https://docs.sigstore.dev/cosign/key_management/overview/, https://docs.sigstore.dev/cosign/signing/overview/
- `tls_private_key`: `algorithm` ∈ {RSA, ECDSA, ED25519}, `ecdsa_curve` ∈ {P224, P256, P384, P521}; P-384 ≈ 192 bitars klassisk säkerhet. https://github.com/hashicorp/terraform-provider-tls/blob/main/docs/resources/private_key.md
- `aws_s3_bucket_server_side_encryption_configuration`: `sse_algorithm` ∈ {AES256, aws:kms, aws:kms:dsse}. https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/s3_bucket_server_side_encryption_configuration.html.markdown
- EO 14028 §4(e)(vii) kräver SBOM till köparen; CRA bilaga I del II punkt 1 kräver maskinläsbar SBOM (minst toppnivåberoenden). https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance ; https://www.springlex.eu/en/packages/cra/cra-regulation/
- NTIA "The Minimum Elements For a Software Bill of Materials (SBOM)" (juli 2021) – länken svarar 200. https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom
- SLSA v1-provenance-schemat och slsa-github-generators buildType `…/container@v1` (v0.2-provenance). https://slsa.dev/spec/v1.0/provenance, https://slsa.dev/spec/v0.2/provenance, https://slsa.dev/blog/2023/02/slsa-github-workflows-container-ga
- STIX 2.1 och TAXII 2.1 godkända som OASIS Standards 10 juni 2021. https://www.oasis-open.org/?p=7287
- NIST PQC: FIPS 203/204/205 publicerade 13 augusti 2024. https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- AWS FIS namnbyte 15 november 2023; Lambda python3.9 avvecklad 15 december 2025. https://docs.aws.amazon.com/fis/latest/userguide/doc-history.html, https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
- Thoughtworks "Security policy as code": Trial (nov 2019, maj 2020), Adopt (okt 2020). https://www.thoughtworks.com/radar/techniques/security-policy-as-code
- GitHub Docs "About protected branches" – URL svarar 200 och titeln stämmer. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Gartner-pressmeddelandet om I&O-trender 2024 finns (5 december 2023) – men med annan titel än i boken (se C-09).
- Kapitel 12:s hänvisningar till kapitel 10, 13 ("Testing Strategies for Infrastructure as Code"), 17 och Part D:s innehåll stämmer med `book_index.json`; 15A:s länk till appendix D och ankaret `#pipeline-example-exporting-mfa-evidence` finns.

## Ej verifierbart

- **SOC 2-kriteriernas exakta lydelse (CC6.1, CC6.6, CC7.1).** AICPA:s TSC-dokument ligger bakom registrering; endast sekundärkällor (Vanta, Secureframe, myctrl.tools) kunde konsulteras. De bekräftar att CC6.1/CC6.6 avser logisk åtkomst respektive hot utanför systemgränsen och CC7.1 sårbarhetsdetektion, vilket gör bokens mappning rimlig.
- **Rego-kompilering i praktiken.** Nedladdning/körning av OPA-binären nekades av behörighetssystemet. Fynden C-01–C-04 bygger på OPA:s officiella release notes, uppgraderingsguide och CLI-referens samt på en lokal simulering av Python-parsern. Rekommendation: kör `opa check --strict` och `opa test` på kodblocken i CI (t.ex. via `tests/test_technical_accuracy.py`).
- **Terraform-JSON:s representation av nästlade block i `planned_values`.** HashiCorps JSON-format-dokumentation säger endast att `values` "depends on the resource type schema"; slutsatsen i C-15 bygger på providerns blockschema och kapitlets eget testdata (arrayer).
- **Exakt Terraform-version för DynamoDB-låsningens avveckling (1.10/1.11).** Primärdokumentet säger bara "deprecated … removed in a future minor version"; versionsnumren kommer från sekundärkällor.
- **`${self:provider.stage}` i Serverless Framework v4 utan definierad `provider.stage`.** Inte verifierat mot v4-dokumentationen (sökbudgeten slut).
- **Om CISA:s "2025 Minimum Elements for a SBOM" har fastställts efter kommentarsperioden (3 oktober 2025).** Sidan som hämtades beskriver fortfarande ett utkast.
- **Årtalet för OPA v1.0.0.** GitHub-sidan visar "20 Dec" utan år; 2024 följer av utgåvekronologin (1.0 följdes av 1.1 i januari 2025) men syns inte i hämtad text.
- **Gremlins dokumentation.** Sidindexet (llms.txt) lästes till 100 000 tecken (758 tecken återstod); ingen sida "Chaos Engineering for Security" hittades, men fullständig uteslutning kan inte garanteras.
- **Thoughtworks "Governance as Code" i senare volymer.** Vol. 21 (PDF) och blip-registret (omdirigering av `/radar/techniques/governance-as-code`) visar att ingen sådan blip finns; samtliga Radar-volymer efter 2019 har inte genomsökts i fulltext.
- **Fyrfasmodellens årtal (C-27)** och påståendena "de facto standard"/"most widely adopted" – saknar källa i manuskriptet och kan inte verifieras som fakta.
