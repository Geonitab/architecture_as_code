# Samtliga fynd – översiktstabell

Sorterad efter allvarlighet och därefter per delrapport. Fullständig beskrivning, evidens och förslag finns i respektive delrapport (länk i sista kolumnen).

| ID | Allvarlighet | Fil:rad | Rubrik | Bedömning | Delrapport |
|---|---|---|---|---|---|
| A-01 | Hög | `docs/01_introduction.md:23, docs/01_introduction.md:29, docs/01_int…` | Fantomkälla: Thoughtworks (2024) "Architecture as Code: The Next Evolution" | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-02 | Hög | `docs/01_introduction.md:35, docs/01_introduction.md:39, docs/01_int…` | Fantomkälla: Red Hat (2023) "Architecture as Code Principles and Best Practices" (adoptability/extensibility/productivity) | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-03 | Hög | `docs/03_version_control.md:26, docs/03_version_control.md:33, docs/…` | Fantomblipp: Thoughtworks Technology Radar "Governance as Code" (Source [2]) | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-04 | Hög | `docs/01_introduction.md:17, docs/01_introduction.md:96` | Statistiken "two thirds … run microservices" och källan "State of Cloud Native Development 2024" | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-05 | Hög | `docs/02_fundamental_principles.md:601` | Uppfunnen NIST-titel: "Requirements Engineering for Secure Systems", SP 800-160 (2023) | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-06 | Hög | `docs/02_fundamental_principles.md:47, docs/02_fundamental_principle…` | GitLab-källor som inte kan återfinnas (SSOT via CLI/API; "Documentation as Code: Best Practices and Implementation") | FELCITERAT / EJ VERIFIERBART | [del_A_foundations.md](del_A_foundations.md) |
| A-07 | Hög | `docs/02_fundamental_principles.md:352–357 och docs/02_fundamental_p…` | Rego-exemplen använder syntax som OPA 1.0 inte accepterar | FÖRÅLDRAT | [del_A_foundations.md](del_A_foundations.md) |
| B1-01 | Hög | `docs/06_structurizr.md:208–224` | Deployment-vy definierad med modellsyntax (deploymentNode/containerInstance inuti views) | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-02 | Hög | `docs/06_structurizr.md:393–397` | Ogiltig autoLayout-syntax och icke-existerande `paperSize`-nyckelord | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-03 | Hög | `docs/06_structurizr.md:1066–1075` | Manuella koordinater via `element <id> x y` finns inte i DSL:n | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-04 | Hög | `docs/06_structurizr.md:418, 466, 471, 631–633` | structurizr-cli anropas med exportformat som inte finns (`png`, `structurizr`) och med en obefintlig version (2024.03.01) | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-05 | Hög | `docs/05_automation_devops_cicd.md:198, 213` | npm-paketet `@swagger-api/swagger-validator` existerar inte | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-06 | Hög | `docs/05_automation_devops_cicd.md:434–439` | `pip3 install terrascan` installerar ett övergivet Python-verktyg från 2020 – och Terrascan är arkiverat | FEL / FÖRÅLDRAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-07 | Hög | `docs/05_automation_devops_cicd.md:217, 225, 239, 251` | `conftest verify` används för att validera konfigurationsfiler – kommandot kör Rego-enhetstester | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-08 | Hög | `docs/06_structurizr.md:19 och 1278` | AaC-projektets beskrivning (YAML + plugin-arkitektur) tillskrivs FINOS architecture-as-code | FELCITERAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-09 | Hög | `docs/05_automation_devops_cicd.md:17` | Thoughtworks "Governance as Code" finns inte som Radar-teknik; arkivlänken är ogiltig | FELCITERAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-10 | Hög | `docs/05_automation_devops_cicd.md:591` | Fantomkälla: "Thoughtworks (2024). Architecture as Code: The Next Evolution. Technology Radar" | FELCITERAT / EJ VERIFIERBART | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-11 | Hög | `docs/06_structurizr.md:51 och 1273` | Fantomkälla: Brown (2022) "Documenting Software Architecture with Structurizr" och termen "diagram decay" | FELCITERAT / EJ VERIFIERBART | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-12 | Hög | `docs/06_structurizr.md:281–283, 1014, 1025, 1036` | Structurizr Cloud och On-Premises beskrivs som aktuella produkter – cloud service har nått end-of-life och on-prem/CLI/Lite är ersatta | FÖRÅLDRAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B2-01 | Hög | `docs/07_containerisation.md:9` | CNCF-statistiken (67 %/58 %/52 %) kan inte återfinnas och beskriver fel population | FEL / EJ VERIFIERBART | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-02 | Hög | `docs/08_microservices.md:84` | "Thoughtworks Technology Radar – Governance as Code" (Vol. 21, 2019) är inte en radar-blip | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-03 | Hög | `docs/09_security_fundamentals.md:209` | "HashiCorp – Terraform Security Best Practices (2023)" är i själva verket en arbetsflödesguide utan det tillskrivna innehållet | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-04 | Hög | `docs/09b_security_patterns.md:240-243` | CloudTrail-exemplet använder en ogiltig datahändelsetyp (`AWS::KMS::Key`) | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-05 | Hög | `docs/09b_security_patterns.md:295-306` | Rego-exemplet kompilerar inte under `import rego.v1` | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-06 | Hög | `docs/09_security_fundamentals.md:276` | GDPR betecknas som ett direktiv | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-07 | Hög | `docs/07_containerisation.md:45` | `kubectl apply --server-side --dry-run=client` är en ogiltig flaggkombination | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-08 | Hög | `docs/09_security_fundamentals.md:258` | NIST Cybersecurity Framework beskrivs med fem funktioner – CSF 2.0 har sex | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-09 | Hög | `docs/09_security_fundamentals.md:270` | "ENISA (2023). Cloud Security Guidelines for EU Organisations" kan inte återfinnas | EJ VERIFIERBART | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-10 | Hög | `docs/09_security_fundamentals.md:277` | "OWASP (2023). Application Security Architecture Guide" existerar inte | EJ VERIFIERBART | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| C-01 | Hög | `docs/10_policy_and_security.md:48-62` | Rego-utdrag med `import rego.v1` använder gammal regelsyntax (kompilerar inte) | FEL | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-02 | Hög | `docs/10_policy_and_security.md:101-125` | Rego-exempel i v0-syntax utan import – fungerar inte i OPA 1.x | FEL / INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-03 | Hög | `docs/11_governance_as_code.md:144-174` | OPA-testmodul refererar en annan package utan `data.`-prefix | FEL | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-04 | Hög | `docs/11_governance_as_code.md:117-138` | CI-steget skriver `--format pretty` till fil och läser den som JSON | FEL | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-05 | Hög | `docs/11_governance_as_code.md:213` | Fantomkälla: Thoughtworks Technology Radar "Governance as Code", Vol. 21 (2019) – och årtalskonflikt 2024/2019 | FELCITERAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-06 | Hög | `docs/15a_evidence_as_code.md:143-175` | SLSA-provenance-exemplet blandar v1-predicateType (felstavad) med v0.2-schema | FEL | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-07 | Hög | `docs/15a_evidence_as_code.md:96-103 och 131-133` | `anchore/scan-action@v3` har ingen `output-file`-indata (och v3 är föråldrad) | FEL / FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-08 | Hög | `docs/15a_evidence_as_code.md:118` | ISO 27001-kontroll "A.12.6.1" tillhör 2013-utgåvan | FÖRÅLDRAT / INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-09 | Hög | `docs/12_compliance.md:268-272` | Kapitel 12:s källista: titlar som inte kunnat återfinnas | FELCITERAT / EJ VERIFIERBART | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| K-01 | Hög | `docs/30_appendix_code_examples.md:3289, 3305, 3313, 3322, 3327, 336…` | 10_CODE_1 blandar `import rego.v1` med Rego v0-syntax – modulen parsar inte | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-02 | Hög | `docs/30_appendix_code_examples.md:3509` | 10_CODE_1 anropar obefintlig builtin `math.max` | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-03 | Hög | `docs/30_appendix_code_examples.md:3357, 3432, 3440–3448, 3454` | 10_CODE_1 har catch-all-funktioner som ger konfliktfel vid körning | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-04 | Hög | `docs/30_appendix_code_examples.md:1628–1691` | 13_CODE_J: v0-syntax som avvisas av OPA 1.x och tester som aldrig kan passera | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-05 | Hög | `docs/30_appendix_code_examples.md:433, 444, 546` | 05_CODE_3 (Terratest) kompilerar inte | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-06 | Hög | `docs/30_appendix_code_examples.md:1609, 1612` | 13_CODE_I använder en funktion som inte finns i Terratest och kastar om argument | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-07 | Hög | `docs/30_appendix_code_examples.md:782–783` | 07_CODE_1 använder `!Contains` i `Conditions` – ogiltigt i CloudFormation | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-08 | Hög | `docs/30_appendix_code_examples.md:715–718` | 21_CODE_1 sätter `location` på azurerm-providern – argumentet finns inte | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-09 | Hög | `docs/30_appendix_code_examples.md:3085–3089` | 15_CODE_3: tre `GroupBy`-dimensioner mot Cost Explorer – max två tillåts | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-10 | Hög | `docs/30_appendix_code_examples.md:3250–3275` | 15_CODE_3: `generate_terraform_cost_optimizations` kraschar på sin egen formatsträng | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-11 | Hög | `docs/30_appendix_code_examples.md:1522–1528, 1539` | 13_CODE_H kraschar på katalogen i 13_CODE_G | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-12 | Hög | `docs/30_appendix_code_examples.md:2514, 2529, 2544, 2553` | 14_CODE_1 refererar till resurser som inte deklareras i modulen | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-13 | Hög | `docs/30_appendix_code_examples.md:2629–2631, 2649` | 14_CODE_2 skickar odeklarerade modulargument och läser en output som inte finns | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-14 | Hög | `docs/30_appendix_code_examples.md:2817, 2830–2835, 2857 samt 2812–2…` | 15_CODE_1: ogiltigt `timeadd`-format, borttaget `cost_filters` och odeklarerade variabler | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-15 | Hög | `docs/30_appendix_code_examples.md:2725, 2760` | 14_CODE_3 använder artefakt-actions v3 som slutade fungera 2025-01-30 | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-16 | Hög | `docs/30_appendix_code_examples.md:1712–1714, 1717–1718, 1723–1724` | 13_CODE_K testar inte det som påstås (PSA på poddar, påhittad PV-annotation, kvotkontroll som aldrig faller) | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-17 | Hög | `docs/30_appendix_code_examples.md:3620–3731` | 10_CODE_3 är inte en giltig OSCAL-komponentdefinition (25 schemafel) | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-18 | Hög | `docs/30_appendix_code_examples.md:3773–3806, 3836–3848` | 10_CODE_4 producerar inte en "OSCAL-compliant" SSP | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-19 | Hög | `docs/30_appendix_code_examples.md:4157, 4158, 4161, 4162, 4241` | 06_CODE_5 (Structurizr) laddas inte: relationer saknas i modellen och `thickness` är ingen elementstil | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-20 | Hög | `docs/30_appendix_code_examples.md:305–333` | 05_CODE_2: Conftest-steget utvärderar aldrig policyn (fel underkommando, fel namespace, v0-syntax) | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-21 | Hög | `docs/30_appendix_code_examples.md:268–274` | 05_CODE_2: Checkov-flaggan `--output-file` finns inte | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-22 | Hög | `docs/30_appendix_code_examples.md:250` | 05_CODE_2: Groovy-sträng med enkla citattecken interpoleras inte | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-23 | Hög | `docs/30_appendix_code_examples.md:353–357` | 05_CODE_2: `infracost breakdown --currency EUR` – flaggan finns inte på `breakdown` | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-24 | Hög | `docs/30_appendix_code_examples.md:1376, 1645, 1684, 3293, 3323, 340…` | `aws_rds_instance` är inte en Terraform-resurstyp – policyerna matchar aldrig riktiga planer | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-25 | Hög | `docs/30_appendix_code_examples.md:1425–1435` | 13_CODE_F: `setup-node` med `cache: 'pnpm'` innan pnpm finns | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-26 | Hög | `docs/30_appendix_code_examples.md:1448–1452` | 13_CODE_F: `dorny/test-reporter` har ingen `vitest`-reporter och matas med en coverage-fil | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-27 | Hög | `docs/30_appendix_code_examples.md:3126` | 15_CODE_3 läser fältet `UtilizationMetrics` som inte finns i Cost Explorer-svaret | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-28 | Hög | `docs/30_appendix_code_examples.md:3098, 3140–3143, 3159–3160` | Tre listningar anropar metoder som aldrig definieras | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-29 | Hög | `docs/30_appendix_code_examples.md:3545–3549` | 10_CODE_2: glob-mönstret `ac-.*` väljer inga kontroller | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| D-01 | Hög | `docs/13_testing_strategies.md:29, :31, :39, :420` | Källa [15] "Testing Infrastructure as Code Programs" (Pulumi Blog, 2024) finns inte – och tillskrivs innehåll från ett inlägg daterat 2026 | FELCITERAT | [del_D_delivery.md](del_D_delivery.md) |
| D-02 | Hög | `docs/14_practical_implementation.md:38` | Testharnessen `@pulumi/pulumi/testing` existerar inte | FEL | [del_D_delivery.md](del_D_delivery.md) |
| D-03 | Hög | `docs/16_migration.md:196–200` | AWS CLI-kommandot `aws cloudformation import-resources-to-stack` existerar inte, och `create-stack` importerar inte resurser | FEL | [del_D_delivery.md](del_D_delivery.md) |
| D-04 | Hög | `docs/16_migration.md:90–179` | CloudFormation-importmallen bryter mot importreglerna (saknar `DeletionPolicy`, blandar import med nyskapande) | FEL | [del_D_delivery.md](del_D_delivery.md) |
| D-05 | Hög | `docs/13_testing_strategies.md:416, :418, :419` | Kapitel 13: tre källor utan verifierbar existens (AWS, NIST, CSA) | EJ VERIFIERBART | [del_D_delivery.md](del_D_delivery.md) |
| D-06 | Hög | `docs/15_cost_optimization.md:149, :151, :155` | Kapitel 15: tre källor med fabricerade titlar (FinOps Foundation, CSA, Microsoft) | EJ VERIFIERBART | [del_D_delivery.md](del_D_delivery.md) |
| D-07 | Hög | `docs/16_migration.md:406, :408, :409` | Kapitel 16: tre källor med fabricerade titlar (Microsoft, Gartner, AXELOS) | EJ VERIFIERBART | [del_D_delivery.md](del_D_delivery.md) |
| E1-01 | Hög | `docs/17_organisational_change.md:105` | Påhittad/ospårbar McKinsey-källa | FELCITERAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-02 | Hög | `docs/17_organisational_change.md:102` | "Spotify Engineering Culture" feldaterad och feltillskriven | FELCITERAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-03 | Hög | `docs/19_management_as_code.md:115` | GitHub "private Issue" finns inte som funktion | FEL | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E2-01 | Hög | `docs/21_digitalisation.md:38` | Investeringssiffran för digital transformation är fel med mer än en tiopotens | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-02 | Hög | `docs/21_digitalisation.md:70 och :196` | Spotify, Netflix och Capital One var inte "cloud-native/cloud-based from inception" | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-03 | Hög | `docs/21_digitalisation.md:76` | Capital One-siffrorna (99,99 %, 40 %, 70 %) saknar källa och motsägs av primärkällor | EJ VERIFIERBART | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-04 | Hög | `docs/21_digitalisation.md:198–199` | Backstage tillskrivs Spotifys tillväxt från 1 till 500 miljoner användare | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-05 | Hög | `docs/21_digitalisation.md:109–119` | Terraform-mallen kan inte initieras: variabler i backend-blocket och ett obefintligt argument | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-06 | Hög | `docs/21_digitalisation.md:388–393` | Sex källposter i kapitel 21 är overifierbara eller har fel titel, saknar URL och finns inte i referenslistan | FELCITERAT / EJ VERIFIERBART | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-07 | Hög | `docs/20_ai_agent_team.md:113–128` | GitHub Actions-exemplet anropar `pulls.createReviewComment` utan obligatoriskt `commit_id` och utan skrivrättigheter | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-08 | Hög | `docs/20_ai_agent_team.md:133–141` | Beskrivningen av repots bot-arbetsflöden stämmer inte med repot | FEL / INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| FG-01 | Hög | `docs/22_documentation_vs_architecture.md:61-87` | CALM-exemplet följer inte CALM-schemat (ogiltig relation och protokoll) | FEL | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-02 | Hög | `docs/25_future_trends.md:292-294, 299` | Fyra källor i kapitel 25 går inte att återfinna (fantomcitat) | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-03 | Hög | `docs/24_best_practices.md:227-229` | Källor i kapitel 24 som inte existerar under angiven titel/utgivare | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-04 | Hög | `docs/26b_aac_anti_patterns.md:172, 175` | Fantomkällor i kapitel 26B | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-05 | Hög | `docs/25_future_trends.md:75-80 och 87-92` | Fel mappning AWS-region → land i kodexemplet | FEL | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-06 | Hög | `docs/25_future_trends.md:73, 94, 98, 106-107` | Electricity Maps-koden läser fält som ändpunkten inte returnerar, använder ogiltig zon och gammal domän | FEL | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| H-01 | Hög | `docs/32_finos_project_blueprint.md:1-3, 9, 25, 29-37, 41-47, 69-74` | "FINOS Project Blueprint" beskrivs som ett arkitekturinitiativ som inte finns | FEL / FELCITERAT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-02 | Hög | `docs/31_appendix_b_technical_architecture.md:69, 71, 75, 323` | AaC-beskrivningen i Appendix B tillskrivs fel projekt; `aacplatform/aac` finns inte | FELCITERAT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-03 | Hög | `docs/29_about_the_author.md:142` | Source [1] "Thoughtworks (2024). Architecture as Code: The Next Evolution" går inte att belägga | FELCITERAT / EJ VERIFIERBART | [del_H_bilagor.md](del_H_bilagor.md) |
| H-04 | Hög | `docs/29_about_the_author.md:119-128` | Licensuppgiften CC BY 4.0 motsägs av repot | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-05 | Hög | `docs/31_appendix_b_technical_architecture.md:147-165, 192-194` | Beskrivna GitHub Actions-arbetsflöden finns inte längre | FÖRÅLDRAT / FEL | [del_H_bilagor.md](del_H_bilagor.md) |
| H-06 | Hög | `docs/29_about_the_author.md:140-143` | Källorna till författarbiografin är döda eller oidentifierbara | FELCITERAT | [del_H_bilagor.md](del_H_bilagor.md) |
| R-01 | Hög | `docs/33_references.md:7` | Fiktiv Thoughtworks-källa "Architecture as Code: The Next Evolution" | EJ VERIFIERBART – sannolikt fiktiv | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-02 | Hög | `docs/33_references.md:8` | Fiktiv Radar-blipp "Governance as Code" (Vol. 21) och död URL | EJ VERIFIERBART – sannolikt fiktiv; FÖRÅLDRAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-03 | Hög | `docs/33_references.md:35` | Fiktiv Red Hat-titel, URL ger 404 och handlar om IaC | EJ VERIFIERBART – sannolikt fiktiv; FÖRÅLDRAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-04 | Hög | `docs/33_references.md:75` | Fiktiv GitLab-publikation "Documentation as Code: Best Practices and Implementation" | EJ VERIFIERBART – sannolikt fiktiv | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-05 | Hög | `docs/33_references.md:78–79` | Fiktiv GitLab-publikation "Building a Single Source of Truth with APIs and CLI" – citeras inte ens | EJ VERIFIERBART – sannolikt fiktiv; FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-06 | Hög | `docs/33_references.md:84–85` | Fiktiv källa "GitHub Open Source Community. Collaborative Software Development" | EJ VERIFIERBART – sannolikt fiktiv | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-07 | Hög | `docs/33_references.md:54–55` | Oåterfinnbar bloggpost "Documenting Software Architecture with Structurizr" (Structurizr Blog, 2022) | EJ VERIFIERBART – sannolikt fiktiv; FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-08 | Hög | `docs/33_references.md:108–109` | Fel titel och år för NIST SP 800-160 | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-09 | Hög | `docs/33_references.md:102` | ISBN för *Clean Architecture* pekar på *Effective Java* | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| A-08 | Medel | `docs/01_introduction.md:97` | Fel ISBN och trunkerad titel för Clean Architecture | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-09 | Medel | `docs/04_adr.md:295` | Thoughtworks ADR-blipp daterad 2023 med fel namn | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-10 | Medel | `docs/03_version_control.md:95` | Atlassian-källan har uppfunnen titel ("Git Workflows for Architecture as Code") | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-11 | Medel | `docs/02_fundamental_principles.md:603` | Fel titel på IEEE 1012-2016; standarden är dessutom ersatt | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-12 | Medel | `docs/02_fundamental_principles.md:602` | Forsberg & Mooz: fel år/forum | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-13 | Medel | `docs/02_fundamental_principles.md:37, docs/02_fundamental_principle…` | Selic (2003) tillskrivs slutsatser artikeln inte drar | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-14 | Medel | `docs/02_fundamental_principles.md:461–472, docs/02_fundamental_prin…` | V-modellen: "NFR → testing, FR → validation" är en icke-standardiserad och missvisande indelning | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-15 | Medel | `docs/02_fundamental_principles.md:359–371` | "Personal data must be stored within the EU/EEA" presenteras som GDPR-krav | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-16 | Medel | `docs/02_fundamental_principles.md:331–332, docs/02_fundamental_prin…` | Felaktiga/obefintliga referenser i koden: EDPB Guidelines 07/2020 och "ENISA Information Security Baseline, 2024" | FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-17 | Medel | `docs/02_fundamental_principles.md:377–403` | Python-validatorn kan inte köras och validerar fel sak | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-18 | Medel | `docs/02_fundamental_principles.md:61–67` | CODEOWNERS-exemplet använder ogiltig team-syntax | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-19 | Medel | `docs/02_fundamental_principles.md:236` | AWS CLI-kommando saknar obligatorisk parameter; "drift-detection" är inget kommando | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-20 | Medel | `docs/02_fundamental_principles.md:283–301` | GitHub Actions-exemplet bygger på Node 18 (EOL) och gamla action-versioner | FÖRÅLDRAT | [del_A_foundations.md](del_A_foundations.md) |
| A-21 | Medel | `docs/02_fundamental_principles.md:129` | Structurizr CLI-exemplet: verktyget är arkiverat och flaggsyntaxen avviker från dokumentationen | FÖRÅLDRAT | [del_A_foundations.md](del_A_foundations.md) |
| A-22 | Medel | `docs/04_adr.md:224, docs/04_adr.md:242, docs/04_adr.md:294` | HashiCorp-källan: bruten ankarlänk, uppfunnen titel och påstående som sidan inte stöder | FELCITERAT + bruten länk | [del_A_foundations.md](del_A_foundations.md) |
| A-23 | Medel | `docs/04_adr.md:228` | "`adr log`" är inget adr-tools-kommando | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-24 | Medel | `docs/26a_prerequisites_for_aac.md:11, docs/26a_prerequisites_for_aa…` | Kapitel 26A tillskriver andra kapitel varningar/argument som inte finns där | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| A-25 | Medel | `docs/26a_prerequisites_for_aac.md:5, docs/26a_prerequisites_for_aac…` | Inaktuella hänvisningar till "Chapter 20" i kapitel 26A (kapitel 20 är nu "AI Agent Team") | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| A-26 | Medel | `docs/01_introduction.md:71, docs/01_introduction.md:77` | Bokstrukturbeskrivningen i kapitel 1 och kapitelrubriker stämmer inte med book_index.json | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| A-27 | Medel | `docs/33_references.md:7, :8, :13` | Brutna "Referenced in"-länkar i bibliografin för källor som används i Del A | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| B1-13 | Medel | `docs/06_structurizr.md:197–205 och 695–706` | Dynamiska vyer refererar relationer som inte finns i modellen, inklusive en förälder→barn-relation | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-14 | Medel | `docs/06_structurizr.md:1101` | `!include` med jokertecken stöds inte | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-15 | Medel | `docs/06_structurizr.md:1061, 1192, 1198, 1206, 1212` | Radslutskommentarer efter DSL-satser stöds inte | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-16 | Medel | `docs/06_structurizr.md:420–421` | jq-kvalitetsgrinden pekar på en JSON-sökväg som inte finns i Structurizr-formatet | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-17 | Medel | `docs/06_structurizr.md:565–567` | Docker-action för PlantUML: `$(pwd)` och glob expanderas inte (ingen shell) | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-18 | Medel | `docs/06_structurizr.md:584–598` | GitLab-jobbet anropar `structurizr` som inte finns i PATH i `structurizr/cli`-imagen | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-19 | Medel | `docs/05_automation_devops_cicd.md:446–447` | Infracost-installationen flyttar binären från en sökväg där den inte finns | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-20 | Medel | `docs/05_automation_devops_cicd.md:316, 393` | tfsec och Terrascan presenteras som aktuella skanningsverktyg | FÖRÅLDRAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-21 | Medel | `docs/05_automation_devops_cicd.md:356, 363, 369, 370, 382, 387` | Microsoft Learn-källan "Design multi-stage release pipelines with approvals" finns inte – och den riktiga dokumentationen motsäger påståendet om kodifierade godkännanden | FELCITERAT / TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-22 | Medel | `docs/05_automation_devops_cicd.md:589` | GDPR.eu-källan: ogiltig URL och påhittad titel | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-23 | Medel | `docs/05_automation_devops_cicd.md:354, 381, 387` | Fel ISBN för The Site Reliability Workbook | FEL | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-24 | Medel | `docs/05_automation_devops_cicd.md:1` | Kapiteltitlar stämmer inte med book_index.json/mkdocs/BOOK_REQUIREMENTS | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-25 | Medel | `docs/05_automation_devops_cicd.md:581–593` | Kapitel 5:s källista speglar inte de källor som faktiskt citeras, och 33_references tillskriver kapitlet källor det inte använder | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B2-11 | Medel | `docs/09_security_fundamentals.md:205-207` | "HashiCorp – Securing Terraform State" (Source [16]) har annan titel och innehåller inte det som tillskrivs den | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-12 | Medel | `docs/09_security_fundamentals.md:208` | S3-backend: DynamoDB-låsning är deprecierad och "versioning" är ingen backend-inställning | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-13 | Medel | `docs/09_security_fundamentals.md:211` | Google Cloud-sidan rekommenderar inte kundhanterade krypteringsnycklar | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-14 | Medel | `docs/09_security_fundamentals.md:49` | EDPB "upprätthåller" inte GDPR – det gör de nationella tillsynsmyndigheterna | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-15 | Medel | `docs/09b_security_patterns.md:224` | "Audit logging aligned with GDPR Article 30" – artikel 30 gäller register över behandling | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-16 | Medel | `docs/07_containerisation.md:47-62` | Gatekeeper-exemplet: fel objekttyp i kommentaren, fel beskrivning i texten och icke-standardiserad mall utan definition | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-17 | Medel | `docs/08_microservices.md:102` | AWS App Mesh har upphört | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-18 | Medel | `docs/09_security_fundamentals.md:282` | "Azure Security Benchmark v3.0 (2023)" – omdöpt till Microsoft cloud security benchmark 2022 | FÖRÅLDRAT / FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-19 | Medel | `docs/09_security_fundamentals.md:278` | CSA Security Guidance v4.0 är från 2017, inte 2023 | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-20 | Medel | `docs/09_security_fundamentals.md:272` | EDPB:s riktlinjer om inbyggt dataskydd antogs 2020 (v2.0), inte 2023 | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-21 | Medel | `docs/09_security_fundamentals.md:275` | EBA:s riktlinjer om IKT- och säkerhetsrisk är från 2019, inte 2023 | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-22 | Medel | `docs/09_security_fundamentals.md:273` | "ENISA (2023). NIS2 Directive Implementation Guidance" – ENISA:s vägledning publicerades i juni 2025 | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-23 | Medel | `docs/09_security_fundamentals.md:256` | "CMMI for security ... aligned with ENISA guidelines" saknar stöd | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-24 | Medel | `docs/08_microservices.md:70-72` | `conftest test deployment/policies` använder conftest fel | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-25 | Medel | `docs/09b_security_patterns.md:229, 235-238` | CloudTrail loggar datahändelser för sin egen loggbucket (rekursiv loggning) | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-26 | Medel | `docs/07_containerisation.md:45` | `kubeval` är inte längre underhållet | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-27 | Medel | `docs/09_security_fundamentals.md:279` | CIS Controls v8 daterat 2023 och organisationsnamnet felstavat | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-28 | Medel | `docs/09_security_fundamentals.md:5-8, 40-43, 45-47, 51-53, 59-62 m.fl.` | Hårda radbrytningar mitt i ord i kapitel 9 och 9B | FEL | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-29 | Medel | `docs/09_security_fundamentals.md:239-240` | "Containers share network namespaces" – gäller bara inom en Pod | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-30 | Medel | `docs/09_security_fundamentals.md:292-293` | ECSO- och SANS-källorna kan inte återfinnas | EJ VERIFIERBART | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| C-10 | Medel | `docs/09c_risk_and_threat_as_code.md:89` | Felaktigt namn och årtal för STIX/TAXII | FELCITERAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-11 | Medel | `docs/09c_risk_and_threat_as_code.md:91` | Källa "Chaos Engineering for Security" hittas inte; "AWS Fault Injection Simulator" är föråldrat namn | FELCITERAT / FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-12 | Medel | `docs/10_policy_and_security.md:149` | Källtiteln "Policy as Code Overview" finns inte hos OPA | FELCITERAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-13 | Medel | `docs/10_policy_and_security.md:151` | HashiCorp-källan har fel titel och olika årtal i kapitel och referenslista | FELCITERAT / INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-14 | Medel | `docs/15a_evidence_as_code.md:117` | SSDF-kartläggningen för SBOM pekar på fel praktiker | FEL | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-15 | Medel | `docs/11_governance_as_code.md:59-86` | S3-krypteringspolicyn använder objekt-sökväg där Terraform-JSON har listor; policyn träffar inte | TVEKSAMT / INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-16 | Medel | `docs/11_governance_as_code.md:204` | Rekommenderar DynamoDB-låsning av Terraform-state, som är avvecklad | FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-17 | Medel | `docs/10_policy_and_security.md:68` | "Azure Sentinel" heter Microsoft Sentinel | FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-18 | Medel | `docs/12_compliance.md:187-252` | "Quantum-safe"-Terraform-exemplet är varken kvantsäkert eller komplett, och PQC-kommentaren är inaktuell | FÖRÅLDRAT / TVEKSAMT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-19 | Medel | `docs/12_compliance.md:124-138, 155, 163` | Serverless-exemplet använder avvecklad Lambda-runtime och avvecklad konfigurationsnyckel | FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-20 | Medel | `docs/12_compliance.md:39` | Kontrollkartläggning och artefaktsökvägar skiljer sig mellan kapitel 10, 12 och 15A | INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-21 | Medel | `docs/10_policy_and_security.md:113-119` | Ramverksmappningen för MFA-kontrollen är för grov (ISO-teman i stället för kontroller; bara privilegierade konton i NIST) | TVEKSAMT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-22 | Medel | `docs/15a_evidence_as_code.md:38-39 och 67` | "Evaluate MFA policy" kör enhetstester, inte en utvärdering – rapporten är inte kontrollevidens | TVEKSAMT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-23 | Medel | `docs/12_compliance.md:260-264` | Struktur och korsreferenser stämmer inte med `book_index.json` | INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-24 | Medel | `docs/33_references.md:16-17, 20, 26, 178` | Kapitlens källistor och `33_references.md` stämmer inte överens | INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-25 | Medel | `docs/10_policy_and_security.md:46, 49, 87` | Kapitel 10 beskriver bilagans listningar fel (PSD2, UK, paketnamn) | INKONSEKVENT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| K-30 | Medel | `docs/30_appendix_code_examples.md:3531` | 10_CODE_2: profilens UUID är inte ett giltigt OSCAL-UUID | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-31 | Medel | `docs/30_appendix_code_examples.md:3587` | 10_CODE_2 hänvisar till "FIPS 140-2 validated encryption modules" | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-32 | Medel | `docs/30_appendix_code_examples.md:2592–2598` | 14_CODE_2 använder DynamoDB-låsning som är deprecated i S3-backenden | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-33 | Medel | `docs/30_appendix_code_examples.md:2683, 2696, 2699, 2704, 2745, 274…` | 14_CODE_3: föråldrade action-versioner och Terraform-pin | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-34 | Medel | `docs/30_appendix_code_examples.md:2703–2708, 2752–2757` | 14_CODE_3 autentiserar mot AWS med långlivade nycklar i stället för OIDC | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-35 | Medel | `docs/30_appendix_code_examples.md:436–439` | 05_CODE_3 bygger på AWS SDK for Go v1, som nått end-of-support | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-36 | Medel | `docs/30_appendix_code_examples.md:569–578, 594–606` | 05_CODE_3: regionkontrollen är tautologisk och "encryption at rest" kontrolleras inte | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-37 | Medel | `docs/30_appendix_code_examples.md:1741` | 13_CODE_K: `bitnami/kubectl:1.29` – EOL-version och borttagna Bitnami-taggar | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-38 | Medel | `docs/30_appendix_code_examples.md:2971–3010` | 15_CODE_2 kombinerar VPA (Auto) och HPA på samma CPU/minnes-mått | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-39 | Medel | `docs/30_appendix_code_examples.md:1778–1783, 1792–1795, 1843–1845` | 13_CODE_L: steg som inte kan köras på en ren runner | FEL | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-40 | Medel | `docs/30_appendix_code_examples.md:1040–1043` | 13_CODE_A: coverage-trösklar på fel nivå (Vitest < 1.0) | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-41 | Medel | `docs/30_appendix_code_examples.md:277–281` | 05_CODE_2: Checkov-filtret på `severity == 'CRITICAL'` är sannolikt tomt | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-42 | Medel | `docs/30_appendix_code_examples.md:45–49, 64` | 05_CODE_1: jobbvillkoret bygger på `head_commit`, som saknas vid `pull_request` | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-43 | Medel | `docs/30_appendix_code_examples.md:1143` | 13_CODE_B: RDS PostgreSQL 14.7 kan inte längre skapas | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-44 | Medel | `docs/30_appendix_code_examples.md:1426–1428` | 13_CODE_F: Node 20 har nått end-of-life | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-45 | Medel | `docs/30_appendix_code_examples.md:702–705` | 21_CODE_1 pinnar azurerm `~> 3.0` | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-46 | Medel | `docs/30_appendix_code_examples.md:4266` | Källa 3: död URL till Structurizr DSL-repot | FELCITERAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-47 | Medel | `docs/30_appendix_code_examples.md:19, 21` | Navigationslistan länkar till sektioner som inte finns | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-48 | Medel | `docs/30_appendix_code_examples.md:116` | Fem listningar refereras inte från de kapitel de hävdar | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-49 | Medel | `docs/30_appendix_code_examples.md:3284–3287, 3384, 3400, 3526, 3586…` | Kapitel 10 och 10_CODE_1/10_CODE_2 beskriver olika innehåll | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-50 | Medel | `docs/30_appendix_code_examples.md:2309–2347` | 17_CODE_3: "DORA-liknande" nivåer stämmer inte med DORA | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-51 | Medel | `docs/30_appendix_code_examples.md:4177–4178` | 06_CODE_5: wildcard i taggexpression saknar stöd i DSL-dokumentationen | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| D-08 | Medel | `docs/15_cost_optimization.md:75, :153` | Gartner-prognosen är feldaterad och överspelad (679 miljarder USD/20,4 %) | FÖRÅLDRAT / FELCITERAT | [del_D_delivery.md](del_D_delivery.md) |
| D-09 | Medel | `docs/13_testing_strategies.md:31` | Terraforms testbarhet beskrivs som den var före `terraform test` 1.6/1.7 | TVEKSAMT / FÖRÅLDRAT | [del_D_delivery.md](del_D_delivery.md) |
| D-10 | Medel | `docs/15_cost_optimization.md:63, :150` | Kubecost beskrivs som öppen källkod – det är IBM/Apptios kommersiella produkt; OpenCost är open source-projektet | FEL | [del_D_delivery.md](del_D_delivery.md) |
| D-11 | Medel | `docs/16_migration.md:117` | Exemplet pekar på Amazon Linux 2, som nådde end-of-support 2026-06-30 | FÖRÅLDRAT | [del_D_delivery.md](del_D_delivery.md) |
| D-12 | Medel | `docs/13_testing_strategies.md:87–90` | `dynamodb_table` för S3-backend-låsning är utfasat sedan Terraform 1.11 | FÖRÅLDRAT | [del_D_delivery.md](del_D_delivery.md) |
| D-13 | Medel | `docs/part_d_delivery.md:13, :23` | Del D-introduktionen räknar in kapitel 15A (Evidence as Code), som i bokindexet tillhör Del C | INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-14 | Medel | `docs/13_testing_strategies.md:415` | Kapitel 13:s källa 2 har en titel som varken motsvarar källa [10] eller något OPA-dokument | FELCITERAT / INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-15 | Medel | `docs/14_practical_implementation.md:99–103` | Kapitel 14: fem odaterade leverantörskällor med titlar som inte kan återfinnas | EJ VERIFIERBART / TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-16 | Medel | `docs/15_cost_optimization.md:148, :150` | Övriga leverantörskällor i kapitel 15 och 16 med fel eller oklara titlar | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-17 | Medel | `docs/15_cost_optimization.md:144` | Besparingsintervallet 20–40 % saknar källa | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-18 | Medel | `docs/33_references.md:10, :15, :16, :21, :22, :99–100, :157–162, :178` | Referenslistan är ofullständig och inkonsekvent gentemot Del D-kapitlen | INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-19 | Medel | `docs/16_migration.md:38` | CloudFormation drift detection presenteras som importmekanism | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| E1-04 | Medel | `docs/33_references.md:36` | Ogiltigt ISBN för Team Topologies i bibliografin (länkad från kap. 17 och 18) | FEL | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-05 | Medel | `docs/18_team_structure.md:201–259` | Spökkapitel: mall för Community of Practice ligger som riktiga rubriker (extra H1) | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-06 | Medel | `docs/33_references.md:157–158 och :164–165` | Bibliografin påstår att kapitel 17 citerar Gartner- och HashiCorp-undersökningar som inte förekommer i kapitlet | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-07 | Medel | `docs/17_organisational_change.md:100` | "Puppet Labs (2023)" – förlagsnamn som upphörde 2016; titel saknas; inkonsekvent mellan kap. 17 och 19 | FELCITERAT / INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-08 | Medel | `docs/18_team_structure.md:279` | HashiCorp "Infrastructure as Code Maturity Model" på "HashiCorp Learn" (2024) – plattformen nedlagd 2022, dokumentet oidentifierbart | FELCITERAT / FÖRÅLDRAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-09 | Medel | `docs/17_organisational_change.md:86` | DORA-måtten återges i föråldrad fyrmåttsform med gamla namn | FÖRÅLDRAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-10 | Medel | `docs/18_team_structure.md:55` | Linux Academy angiven som aktuell utbildningsplattform (och A Cloud Guru säljs inte längre) | FÖRÅLDRAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-11 | Medel | `docs/part_e_leadership.md:19–26` | Del E-introduktionen och navigationen stämmer inte med book_index.json (kapitel 23) | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E2-09 | Medel | `docs/21_digitalisation.md:220, 223, 228, 231, 239` | Suveränitetsmolnen beskrivs i ett föråldrat läge (AWS "roadmap"/"upcoming", Azure/Google utan 2025–2026-utvecklingen) | FÖRÅLDRAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-10 | Medel | `docs/21_digitalisation.md:242` | Google Cloud är inte längre "carbon-neutral" | FEL / FÖRÅLDRAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-11 | Medel | `docs/21_digitalisation.md:44` | "IaC minskar manuellt arbete med upp till 70 %" saknar studie | TVEKSAMT / EJ VERIFIERBART | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-12 | Medel | `docs/21_digitalisation.md:380–384` | Kapitel 21 placerar kapitel 23 i Del F och tillskriver det innehåll det inte har | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-13 | Medel | `docs/23_soft_as_code_interplay.md:260–261` | Källtitlarna "Policy as Code Overview" motsvarar inte dokumenten (OPA och HashiCorp) | FELCITERAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-14 | Medel | `docs/33_references.md Source [2]` | "Governance as Code" finns inte som blip i Technology Radar Vol. 21 (Source [2], påstås refererad i kapitel 23) | FELCITERAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-15 | Medel | `docs/33_references.md Source [2], [4], [10], Selic-posten, IDC-posten` | Referenslistan och kapitlens källavsnitt stämmer inte överens | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-16 | Medel | `docs/20_ai_agent_team.md:188` | Anthropic-källan pekar på fel sida och är föråldrad | FÖRÅLDRAT / FELCITERAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-17 | Medel | `docs/20_ai_agent_team.md:94–98` | Editor-arbetsflödet saknar stavningsmotor och använder ett verktyg det aldrig kör | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-18 | Medel | `docs/21_digitalisation.md:131` | `timestamp()` i resurs-taggar ger diff vid varje körning | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-19 | Medel | `docs/21_digitalisation.md:259` | General Electric som exempel på lyckad digital omställning | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-20 | Medel | `docs/21_digitalisation.md:283–291` | Rekommenderade IaC-skanners är delvis i förvaltningsläge; `terraform plan` körs utan `init` | FÖRÅLDRAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| FG-07 | Medel | `docs/27_conclusion.md:129 och 131` | Tre felaktiga ISBN i de verk som kapitel 22 och 27 lutar sig mot | FEL | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-08 | Medel | `docs/25_future_trends.md:229` | Gartner-siffran är felattribuerad till "2024 forecast" och numera reviderad | FELCITERAT / FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-09 | Medel | `docs/25_future_trends.md:290` | ENISA-rapporten är från 2021, inte 2024 | FEL | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-10 | Medel | `docs/26b_aac_anti_patterns.md:173` | ISO/IEC 42010:2011 är ersatt av ISO/IEC/IEEE 42010:2022 | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-11 | Medel | `docs/26b_aac_anti_patterns.md:174` | NCSC-källor med fel titel och/eller årtal | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-12 | Medel | `docs/part_f_practices.md:11 och 21` | Del F-introduktionen räknar in kapitel 23, som enligt index ligger i Del E | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-13 | Medel | `docs/part_g_future.md:11` | Del G-introduktionen räknar in kapitel 26A, som enligt index ligger i Del A | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-14 | Medel | `docs/27_conclusion.md:33-34` | Slutsatsen hänvisar till "idempotent configuration in chapter 2" – kapitel 2 behandlar inte idempotens | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-15 | Medel | `docs/27_conclusion.md:55` | AI-förordningen beskrivs som "emerging proposals" trots att den är gällande rätt | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-16 | Medel | `docs/27_conclusion.md:119` | Terraform beskrivs som del av "the open-source ecosystem" | FÖRÅLDRAT / TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-17 | Medel | `docs/22_documentation_vs_architecture.md:263` | Länken till Structurizr DSL-repot är död | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-18 | Medel | `docs/25_future_trends.md:286, 288` | Påhittade titlar på EU-källor samt källor utan år/URL | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-19 | Medel | `docs/33_references.md:54-55` | Structurizr-bloggposten kan inte verifieras och attribueras felaktigt till kapitel 24 | EJ VERIFIERBART / INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-20 | Medel | `docs/33_references.md:7-8, 10, 16, 20, 51-55, 157-165 i relation ti…` | Referenslistan (33_references.md) stämmer inte med kapitlens källistor | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-21 | Medel | `docs/24_best_practices.md:7 och 31` | Figur 24.1 är en platshållare och figurhänvisningen till "seven practice clusters" pekar på fel figur | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| H-07 | Medel | `docs/appendix_templates_and_tools.md:23-213` | Kodexemplet i Appendix D anropar åtta metoder som inte finns | FEL | [del_H_bilagor.md](del_H_bilagor.md) |
| H-08 | Medel | `docs/31_appendix_b_technical_architecture.md:15-32` | Felaktigt antal manuskriptfiler och föråldrat filträd | FEL / FÖRÅLDRAT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-09 | Medel | `docs/31_appendix_b_technical_architecture.md:83-100, 111-122` | Kodutdrag för pandoc.yaml och mmdc stämmer inte med repot | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-10 | Medel | `docs/31_appendix_b_technical_architecture.md:169-179` | Beskrivningen av arbetsflödets steg och cachning motsvarar inte den faktiska pipelinen | FÖRÅLDRAT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-11 | Medel | `docs/31_appendix_b_technical_architecture.md:244-281` | `exports/book-cover/`-trädet finns inte; CSS-utdraget kommer från presentationsmallen | FÖRÅLDRAT / INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-12 | Medel | `docs/31_appendix_b_technical_architecture.md:285-291` | Antal whitepapers och påstådda funktioner stämmer inte | FÖRÅLDRAT / TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-13 | Medel | `docs/31_appendix_b_technical_architecture.md:60-65, 200-218` | generate_book.py och generate_presentation.py beskrivs/citeras felaktigt | FÖRÅLDRAT / INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-14 | Medel | `docs/architecture_as_code_maturity_model.md:30-31, 214-222` | Mognadsmodellens källor: odefinierad [13] och felattribuerad [1] | FELCITERAT / INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-15 | Medel | `docs/appendix_templates_and_tools.md:7, 11` | Appendix D överdriver mognadsmodellens och radarverktygets funktioner | TVEKSAMT / INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-16 | Medel | `docs/maturity_model_radar.html` | Sju referenslänkar i radarverktyget pekar på ankare som inte finns | FEL | [del_H_bilagor.md](del_H_bilagor.md) |
| H-17 | Medel | `docs/28_glossary.md:107` | Ordlistans "relationsdatabas" är ur synk och används inte av några pipelines | TVEKSAMT / INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-18 | Medel | `docs/32_finos_project_blueprint.md:5` | Bildtexten "Blueprint governance spine" visar mognadstrappan | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-19 | Medel | `docs/29_about_the_author.md:11, 31` | Motstridiga uppgifter om författarens relation till Kvadrat och om Kvadrat | INKONSEKVENT / TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-20 | Medel | `docs/29_about_the_author.md:35-40` | "Swedish Terminology Reference" förklarar institutioner som aldrig nämns | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-21 | Medel | `docs/part_h_appendices.md:9-21, 25-30` | Del H-introduktionen utelämnar Appendix C och Referenser; bilagebokstäver skiljer sig i repot | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| R-10 | Medel | `docs/33_references.md:14` | Fel ISBN för *The Site Reliability Workbook* | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-11 | Medel | `docs/33_references.md:36` | Fel ISBN (ogiltig kontrollsiffra) för *Team Topologies* | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-12 | Medel | `docs/33_references.md:38` | Fel ISBN (ogiltig kontrollsiffra) för *Software Architecture in Practice*, 4 uppl. | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-13 | Medel | `docs/33_references.md:60 och 126` | Fel ISBN för Chung et al. och Richardson (ogiltiga kontrollsiffror) | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-14 | Medel | `docs/33_references.md:69` | Fel ISBN för *Building Evolutionary Architectures* | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-15 | Medel | `docs/33_references.md:72` | Forsberg & Mooz: fel tidskrift/år-kombination | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-16 | Medel | `docs/33_references.md:87` | Fel titel på IEEE Std 1012-2016 | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-17 | Medel | `docs/33_references.md:9` | Påhittad titel för Atlassian-sidan | FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-18 | Medel | `docs/33_references.md:18` | Microsoft Learn-titel som inte finns (citeras 6 gånger i kap. 05) | EJ VERIFIERBART / FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-19 | Medel | `docs/33_references.md:21` | Pulumi-bloggpost med påhittad titel och fel år | FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-20 | Medel | `docs/33_references.md:22 och 26` | HashiCorp-titlar som inte motsvarar sidorna ([16], [20]) | FELCITERAT / FÖRÅLDRAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-21 | Medel | `docs/33_references.md:13` | CNCF "State of Cloud Native Development 2024" – fel utgivare, utgåva ej verifierad | TVEKSAMT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-22 | Medel | `docs/33_references.md:33` | GDPR.eu-länk död och titel påhittad | FÖRÅLDRAT / FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-23 | Medel | `docs/33_references.md:93` | Kvadrat-konsultprofil: URL ger 404 | FÖRÅLDRAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-24 | Medel | `docs/33_references.md:96` | "Technology Consulting Excellence" är ingen publikation | FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-25 | Medel | `docs/33_references.md:99` | MarketsandMarkets-rapport: fel år, ofullständig titel | TVEKSAMT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-26 | Medel | `docs/33_references.md:135` | github.com/structurizr/dsl finns inte längre | FÖRÅLDRAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-27 | Medel | `docs/33_references.md:147` | Thoughtworks ADR-blipp: fel namn och år | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-28 | Medel | `docs/33_references.md:155` | Författarens egen praktik listad som källa | TVEKSAMT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-29 | Medel | `docs/33_references.md:157–158 och 161–162` | Gartner- och IDC-rapporter: oprecisa titlar och felaktiga "Referenced in" | TVEKSAMT; FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-30 | Medel | `docs/33_references.md:7, 8, 12, 13, 16, 17, 19, 20, 21, 22, 26, 52,…` | "Referenced in"-listor som inte stämmer med den faktiska citeringen | FELCITERAT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-31 | Medel | `docs/33_references.md:7, 8, 10, 13, 16` | Trasiga interna länkar och kapitelrubriker som avviker från book_index.json | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| A-28 | Låg | `docs/02_fundamental_principles.md:55, docs/02_fundamental_principle…` | "Drift scenarios documented earlier in this chapter" – tabellen kommer senare | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| A-29 | Låg | `docs/02_fundamental_principles.md:599` | OPA-källans titel är uppfunnen och stämmer inte med bibliografin | INKONSEKVENT / FELCITERAT | [del_A_foundations.md](del_A_foundations.md) |
| A-30 | Låg | `docs/04_adr.md:137` | "Terraform Cloud" heter HCP Terraform; ADR-exemplet blandar AaC och IaC | FÖRÅLDRAT | [del_A_foundations.md](del_A_foundations.md) |
| A-31 | Låg | `docs/02_fundamental_principles.md:39` | Structurizr beskrivs som "MBSE-aligned tooling" | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-32 | Låg | `docs/02_fundamental_principles.md:155` | "Commit sign-off" förväxlas med kryptografisk signering | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-33 | Låg | `docs/02_fundamental_principles.md:507–509 och 513` | k6-tröskeln gäller en taggad delmetrik som ingen request matchar | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-34 | Låg | `docs/02_fundamental_principles.md:69` | "Including administrators" gäller bara om bypass-skyddet är aktiverat | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-35 | Låg | `docs/04_adr.md:30` | adr.github.io beskrivs som "official" | TVEKSAMT | [del_A_foundations.md](del_A_foundations.md) |
| A-36 | Låg | `docs/26a_prerequisites_for_aac.md:132–136` | Källförteckningen i kapitel 26A används inte i texten och har årtalsfel | INKONSEKVENT | [del_A_foundations.md](del_A_foundations.md) |
| A-37 | Låg | `docs/03_version_control.md:26` | AWS CDK-länken använder föråldrad "latest"-sökväg | FÖRÅLDRAT | [del_A_foundations.md](del_A_foundations.md) |
| A-38 | Låg | `docs/33_references.md:60` | Chung et al.: ISBN med fel kontrollsiffra (i bibliografin) | FEL | [del_A_foundations.md](del_A_foundations.md) |
| A-39 | Låg | `docs/04_adr.md:242` | Oklar anekdot presenterad som faktum | EJ VERIFIERBART | [del_A_foundations.md](del_A_foundations.md) |
| B1-26 | Låg | `docs/06_structurizr.md:787–810` | `include platform` i en container-vy scopad till `platform` är otillåtet; avsnittet "Filtered Views" visar inte filtrerade vyer | FEL / TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-27 | Låg | `docs/06_structurizr.md:428–429` | Påståendet att CLI-exporten skriver "deterministic coordinates" | TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-28 | Låg | `docs/05_automation_devops_cicd.md:37` | "Early 2000s" för CI:s rötter i XP | TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-29 | Låg | `docs/05_automation_devops_cicd.md:540–548` | Jenkins-metriker saknar pluginens standardprefix och `match[]` är inte en pluginfunktion | TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-30 | Låg | `docs/05_automation_devops_cicd.md:191, 203, 263, 442` | Föråldrade pinnade versioner i kodexempel | FÖRÅLDRAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-31 | Låg | `docs/06_structurizr.md:283, 287, 296, 380` | Structurizr Lite beskrivs som "no server required" men startar en lokal webbserver; "Structurizr Local" är inte produktens namn | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-32 | Låg | `docs/06_structurizr.md:371, 1275` | Länk till DSL-språkreferensen pekar på ett repo som inte längre innehåller parsern | FÖRÅLDRAT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-33 | Låg | `docs/06_structurizr.md:1274` | Årtal för "Software Architecture for Developers" skiljer sig mellan kapitlet och referenslistan | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-34 | Låg | `docs/06_structurizr.md:458, 498–528` | Återgiven workflow avviker från den fil som påstås levereras i repot; "pinned CLI version" är bara en fri egenskap | INKONSEKVENT / TVEKSAMT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-35 | Låg | `docs/part_b_platform.md:11, 17` | Del B-introduktionen: amerikansk stavning och ofullständig innehållsöversikt | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B1-36 | Låg | `docs/05_automation_devops_cicd.md:487` | Kapitelreferens "Chapter 15" stämmer inte med book_index-identifieraren 15B | INKONSEKVENT | [del_B_kap05-06.md](del_B_kap05-06.md) |
| B2-31 | Låg | `docs/07_containerisation.md:307` | Chapter 7 Source 3 har annan titel än den länkade Source [5] | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-32 | Låg | `docs/09_security_fundamentals.md:215, 225` | "Terraform Cloud" heter HCP Terraform | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-33 | Låg | `docs/08_microservices.md:108` | Istio VirtualService använder `v1alpha3` | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-34 | Låg | `docs/07_containerisation.md:41` | "Federation APIs" (KubeFed) är avvecklat; Cluster API är ett projekt, inte en specifikation | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-35 | Låg | `docs/07_containerisation.md:269, 281-284` | `node_count` tillsammans med `autoscaling` i GKE-nodpoolen | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-36 | Låg | `docs/09b_security_patterns.md:139, 151, 168` | `data.aws_region.current.name` är deprecierat | FÖRÅLDRAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-37 | Låg | `docs/09b_security_patterns.md:472-476` | CVSS-poäng över 7,0 klassas som "CRITICAL" | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-38 | Låg | `docs/09_security_fundamentals.md:268, 291, 295` | Föråldrade organisations-/publikationsuppgifter i källförteckningen (ISC2, NIST PQC, CERT-EU) | FÖRÅLDRAT / FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-39 | Låg | `docs/07_containerisation.md:306, 310, 311` | Övriga vaga/ospårbara källposter i kapitel 7 och 9 | EJ VERIFIERBART | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-40 | Låg | `docs/part_c_security.md:2-5` | Delens titel stämmer inte med `book_index.json`; övergångstexten utelämnar kapitel i Del C | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-41 | Låg | `docs/09_security_fundamentals.md:264-295 och docs/09b_security_patt…` | Identiska källförteckningar i kapitel 9 och 9B; de flesta poster citeras aldrig; samma bild används i båda kapitlen | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-42 | Låg | `docs/09b_security_patterns.md:119, 315` | "Swedish" kontra "European" inramning i 9B | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-43 | Låg | `docs/08_microservices.md:147-173` | AsyncAPI-exemplet: JSON i ett `yaml`-block, äldre specversion och tveksam `publish`-semantik | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-44 | Låg | `docs/09_security_fundamentals.md:49` | NIS2 beskrivs som krav för "critical infrastructure" | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-45 | Låg | `docs/09_security_fundamentals.md:200-201` | Artikel 25 tillskrivs krav som hör till artikel 5 | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-46 | Låg | `docs/09_security_fundamentals.md:213` | "container leases" i Azure Storage – det är blob-lån | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-47 | Låg | `docs/09_security_fundamentals.md:210` | Microsoft Learn-sidan "kräver" inte Entra ID/SAS | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-48 | Låg | `docs/08_microservices.md:207` | Flyway/Liquibase-migreringar är versionerade, inte idempotenta | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-49 | Låg | `docs/07_containerisation.md:86` | AWS CDK-källan (Source [9]) tillskrivs ett innehåll den inte uttrycker | TVEKSAMT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-50 | Låg | `docs/33_references.md:16` | Brutna relativa länkar i Source [10] som kapitel 8 åberopar | INKONSEKVENT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| B2-51 | Låg | `docs/09_security_fundamentals.md:274` | DORA tillskrivs Europeiska kommissionen | FELCITERAT | [del_B-C_kap07-09B.md](del_B-C_kap07-09B.md) |
| C-26 | Låg | `docs/09c_risk_and_threat_as_code.md:53, 87, 88` | Produkt- och organisationsnamn: föråldrade eller angliciserade former | FÖRÅLDRAT / FELCITERAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-27 | Låg | `docs/10_policy_and_security.md:15-22, 34` | Fyrfasmodellen för säkerhetsautomation presenteras som fakta utan källa | TVEKSAMT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-28 | Låg | `docs/10_policy_and_security.md:80, 127, 150` | Terminologi- och utgåvedetaljer kring standarder | FELCITERAT / Låg precision | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| C-29 | Låg | `docs/15a_evidence_as_code.md:71, 115, 141, 226` | Mindre precisionsbrister i kapitel 15A | Låg precision / FÖRÅLDRAT | [del_C_kap09C-15A.md](del_C_kap09C-15A.md) |
| K-52 | Låg | `docs/30_appendix_code_examples.md:2451–2456` | "Conventions"-avsnittet beskriver markeringar som inte används | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-53 | Låg | `docs/30_appendix_code_examples.md:5` | Påståendet att bilagan samlar "every code example" i boken | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-54 | Låg | `docs/30_appendix_code_examples.md:31, 116, 424, 692, 818` | Kapiteltitlar i backlinks avviker från book_index.json | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-55 | Låg | `docs/30_appendix_code_examples.md:4264` | Källa 1 saknas i den numrerade bibliografin | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-56 | Låg | `docs/30_appendix_code_examples.md:118–119, 150, 392` | 05_CODE_2: felaktig språkmarkering, odefinierad variabel och ospecificerat "lagkrav" | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-57 | Låg | `docs/30_appendix_code_examples.md:1488–1490` | 13_CODE_G: testbeskrivning nämner Locust men verktyget är k6 | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-58 | Låg | `docs/30_appendix_code_examples.md:3773, 3847` | 10_CODE_4 använder `datetime.utcnow()` | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-59 | Låg | `docs/30_appendix_code_examples.md:822–827, 830–839` | 24_CODE_1: dataklassen `TestCase` kolliderar med pytest-insamling; oanvända importer | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-60 | Låg | `docs/30_appendix_code_examples.md:2592, 2608, 2655, 2684` | 14_CODE_2/14_CODE_3: `us-west-2` i en bilaga som annars betonar EU-residens | INKONSEKVENT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-61 | Låg | `docs/30_appendix_code_examples.md:2778–2786` | 14_CODE_3: `environment.url` refererar till ett steg-id som inte finns | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-62 | Låg | `docs/30_appendix_code_examples.md:4150–4162, 4113–4115` | 06_CODE_5: manuell numrering i dynamisk vy; tom deployment node | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-63 | Låg | `docs/30_appendix_code_examples.md:72, 1423, 1776, 1791, 1801, 1813,…` | `actions/checkout@v4` och `hashicorp/setup-terraform@v3` är inte längre aktuella major | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-64 | Låg | `docs/30_appendix_code_examples.md:1628` | 13_CODE_J: `default allow = true` utan funktion och v0-tilldelning | TVEKSAMT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| K-65 | Låg | `docs/30_appendix_code_examples.md:3296, 3408` | 10_CODE_1 använder legacytypen `aws_elasticsearch_domain` | FÖRÅLDRAT | [bilaga_A_kodexempel.md](bilaga_A_kodexempel.md) |
| D-20 | Låg | `docs/15_cost_optimization.md:73, :152` | MarketsandMarkets-rapporten är daterad 2022, inte 2023, och titeln är inte rapportens | FELCITERAT | [del_D_delivery.md](del_D_delivery.md) |
| D-21 | Låg | `docs/15_cost_optimization.md:128` | Google Clouds CUD-rabatt anges till "up to 57%" – aktuell dokumentation säger 55 % (70 % för minnesoptimerade) | FÖRÅLDRAT | [del_D_delivery.md](del_D_delivery.md) |
| D-22 | Låg | `docs/13_testing_strategies.md:43, :45` | Pulumi CLI-flaggor: `pulumi stack ls --json` är inte längre dokumenterad; "`pulumi up --policy-pack` in preview mode" är motsägelsefullt | FÖRÅLDRAT / TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-23 | Låg | `docs/13_testing_strategies.md:63–65` | GitHub Actions-exemplet pinnar Node.js 20, som nådde end-of-life 2026-04-30 | FÖRÅLDRAT | [del_D_delivery.md](del_D_delivery.md) |
| D-24 | Låg | `docs/16_migration.md:227, :234–237, :282–287, :352–362` | Migrationstestskriptet: hårdkodat 2023-datum, null-hantering och CloudWatch-anrop utan dimensioner | FÖRÅLDRAT / TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-25 | Låg | `docs/15_cost_optimization.md:29, :41, :51` | Överdrivna verktygspåståenden om kostnadskontroll (Terraform Enterprise, Terraform-providers, CloudWatch) | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-26 | Låg | `docs/13_testing_strategies.md:264` | AWS Config Rules beskrivs som i första hand preventiva | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| D-27 | Låg | `docs/13_testing_strategies.md:280–283` | Figurhantering: kapitel 13 återanvänder kapitel 12:s diagram med annan bildtext; kapitel 15–16 saknar figurnumrering | INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-28 | Låg | `docs/15_cost_optimization.md:67` | "GAIA-X" bör skrivas "Gaia-X" | INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-29 | Låg | `docs/15_cost_optimization.md:92, :105, :116` | Bilagelänkar i kapitel 15 saknar filnamn (bryter i MkDocs-webbplatsen) | INKONSEKVENT | [del_D_delivery.md](del_D_delivery.md) |
| D-30 | Låg | `docs/13_testing_strategies.md:25` | Terratest beskrivs som policyvalidator med IDE-integration | TVEKSAMT | [del_D_delivery.md](del_D_delivery.md) |
| E1-12 | Låg | `docs/18_team_structure.md:1` | Kapitel 18:s titel skiljer sig mellan fil, index, navigation och bibliografi | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-13 | Låg | `docs/18_team_structure.md:278` | Atlassian-källans titel och publikationstyp är felaktiga | FELCITERAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-14 | Låg | `docs/19_management_as_code.md:294` | Drucker (1954) anges med förlaget Harper & Row, som bildades först 1962 | FELCITERAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-15 | Låg | `docs/19_management_as_code.md:295` | OpenGitOps-principerna daterade 2024; de publicerades som v1.0.0 i oktober 2021 | FELCITERAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-16 | Låg | `docs/17_organisational_change.md:103` | Team Topologies: titelstavning ändrad och undertitel inkonsekvent; andra upplagan (2025) finns | INKONSEKVENT / FÖRÅLDRAT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-17 | Låg | `docs/17_organisational_change.md:101` | DORA-rapporten 2023 benämns olika och är inte kopplad till Source [28] | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-18 | Låg | `docs/18_team_structure.md:55` | Certifieringsnamnen är inte de officiella | TVEKSAMT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-19 | Låg | `docs/19_management_as_code.md:292–300` | "## Sources" placerad före "## Summary" i kapitel 19 | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-20 | Låg | `docs/33_references.md:178` | Bibliografins fullständighetspåstående stämmer inte för kapitel 17–19 | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-21 | Låg | `docs/33_references.md:10` | Trasig intern länk i bibliografin till "Chapter 20" (20_team_structures.md) | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E1-22 | Låg | `docs/19_management_as_code.md:102` | "PCI-DSS" – inofficiell stavning, inkonsekvent i manuskriptet | INKONSEKVENT | [del_E_kap17-19.md](del_E_kap17-19.md) |
| E2-21 | Låg | `docs/20_ai_agent_team.md:87, 90, 114` | Versionerna på GitHub Actions ligger flera major-versioner efter | FÖRÅLDRAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-22 | Låg | `docs/21_digitalisation.md:315–318, 351–355` | Kodkommentaren om `terraform_runner` är inte längre korrekt | FEL | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-23 | Låg | `docs/21_digitalisation.md:70` | Spotifys användarsiffra är inaktuell | FÖRÅLDRAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-24 | Låg | `docs/21_digitalisation.md:48` | EDPB "enforces" inte GDPR | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-25 | Låg | `docs/21_digitalisation.md:42, 48` | NIS2 beskrivs som ett "critical infrastructure"-direktiv | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-26 | Låg | `docs/21_digitalisation.md:210, 227, 299, 302` | Skrivsättet "PCI-DSS" och "certifications ... SOC 2" | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-27 | Låg | `docs/21_digitalisation.md:218, 249` | "GAIA-X" bör skrivas "Gaia-X" | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-28 | Låg | `docs/21_digitalisation.md:251` | Open Telekom Cloud sammanblandas med "Sovereign Controls by T-Systems" | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-29 | Låg | `docs/21_digitalisation.md:218` | "Chapter 15" är tvetydigt i indexet | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-30 | Låg | `docs/20_ai_agent_team.md:13, 17–19, 21, 41` | Redaktionella arbetsanteckningar kvar i manuskriptet; diagrammet matchar inte rollerna | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-31 | Låg | `docs/20_ai_agent_team.md:153` | Prompten hänvisar till en fil som inte finns | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-32 | Låg | `docs/20_ai_agent_team.md:187` | Edmondson-titeln är ändrad och saknar ISBN | FELCITERAT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-33 | Låg | `docs/23_soft_as_code_interplay.md:174–189` | Terraform-låsningsexemplet använder ett påhittat felmeddelande och en avvecklad mekanism | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-34 | Låg | `docs/23_soft_as_code_interplay.md:1, 5, 254` | Stilregel och titelvarianter för kapitel 23 | INKONSEKVENT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| E2-35 | Låg | `docs/23_soft_as_code_interplay.md:81` | "C4 models generated from Markdown" är oprecist | TVEKSAMT | [del_E_kap23-20-21.md](del_E_kap23-20-21.md) |
| FG-22 | Låg | `docs/27_conclusion.md:43-44` | "Observability … first introduced in security and resilience chapters" stämmer inte | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-23 | Låg | `docs/22_documentation_vs_architecture.md:47-51` | "three primary components" underskattar CALM:s modell | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-24 | Låg | `docs/22_documentation_vs_architecture.md:261` | CALM-källan saknar version; CALM har släppts i version 1.0 och 1.1 | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-25 | Låg | `docs/24_best_practices.md:1` | Kapiteltiteln avviker från book_index.json | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-26 | Låg | `docs/25_future_trends.md:259` | "Chapter 15" saknar bokstavsidentifieraren 15B | INKONSEKVENT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-27 | Låg | `docs/25_future_trends.md:261` | Produktnamn och status för suveräna molnerbjudanden | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-28 | Låg | `docs/25_future_trends.md:23-27` | NIST-listan är korrekt men inte längre komplett | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-29 | Låg | `docs/25_future_trends.md:229, 298` | IDC-prognosen kunde inte lokaliseras i angiven utgåva | EJ VERIFIERBART | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-30 | Låg | `docs/26b_aac_anti_patterns.md:177` | GDS-källans titel finns inte | FELCITERAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-31 | Låg | `docs/22_documentation_vs_architecture.md:267-268` | Richardson och Ford listas som källor utan att åberopas; 1:a upplagan citeras trots 2:a upplagan | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-32 | Låg | `docs/25_future_trends.md:229, 296` | MarketsandMarkets-prognosen: korrekt siffra men daterad källa | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-33 | Låg | `docs/27_conclusion.md:57-58` | Dataförvaltningsakten beskrivs som sektorsspecifik | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-34 | Låg | `docs/27_conclusion.md:66-68` | CSRD-hänvisningen tar inte hänsyn till Omnibus-ändringarna | FÖRÅLDRAT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-35 | Låg | `docs/25_future_trends.md:51 och 303` | Climate Neutral Data Centre Pact – formulering och upphovsmän | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| FG-36 | Låg | `docs/25_future_trends.md:187 och 207` | Terraform-utdraget refererar resurser som inte definieras | TVEKSAMT | [del_F-G_kap22-27.md](del_F-G_kap22-27.md) |
| H-22 | Låg | `docs/31_appendix_b_technical_architecture.md:135` | "structurizr.sh validate … on every pull request" stämmer inte med CI | TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-23 | Låg | `docs/28_glossary.md:104` | Ordlistans CALM-post: fel kapitelhänvisning och oprecis karakterisering | INKONSEKVENT / TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-24 | Låg | `docs/28_glossary.md:63` | Chaos Monkey definieras som ett experiment i stället för Netflix verktyg | TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-25 | Låg | `docs/28_glossary.md:10, 39, 51, 52, 66, 75, 100, 101` | Flera ordlistetermer används inte i boken trots löftet om spegling | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-26 | Låg | `docs/28_glossary.md:32` | GitOps-definitionen antyder push-modell | TVEKSAMT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-27 | Låg | `docs/29_about_the_author.md:50-53` | Verktygskedjans versioner presenteras som aktuella men är tre år gamla / end-of-life | FÖRÅLDRAT | [del_H_bilagor.md](del_H_bilagor.md) |
| H-28 | Låg | `docs/31_appendix_b_technical_architecture.md:323` | Små källinkonsekvenser mellan bilagornas Sources och 33_references.md | INKONSEKVENT | [del_H_bilagor.md](del_H_bilagor.md) |
| R-32 | Låg | `docs/33_references.md:3 och 178` | Påståenden i inledning/avslutning stämmer inte | FEL | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-33 | Låg | `docs/33_references.md:11, 16, 20, 57, 102` | Inkonsekventa titlar/år mellan kapitel och kapitel 33 för samma källa | INKONSEKVENT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
| R-34 | Låg | `docs/33_references.md:16, 17, 29, 32, 36, 45, 111, 117, 129, 132, 141` | Smärre bibliografiska brister i korrekta poster | FÖRÅLDRAT / INKONSEKVENT | [kap33_kallforteckning.md](kap33_kallforteckning.md) |
