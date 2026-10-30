<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del D (Delivery & Operations)

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, enbart bedömning – inga ändringar i repot).

## Omfattning

Lästa filer (varje rad, i sin helhet):

- `docs/part_d_delivery.md` (28 rader)
- `docs/13_testing_strategies.md` (420 rader)
- `docs/14_practical_implementation.md` (106 rader)
- `docs/15_cost_optimization.md` (155 rader)
- `docs/16_migration.md` (409 rader)

Stödfiler som lästs för korsreferenser: `docs/book_index.json`, `docs/33_references.md`, utdrag ur `docs/30_appendix_code_examples.md`, `docs/appendix_templates_and_tools.md`, `docs/12_compliance.md`, `docs/25_future_trends.md`, `BOOK_REQUIREMENTS.md`.

Inventering: cirka 130 kontrollerbara påståenden (siffror, citat/källor, standarder, verktygs- och CLI-påståenden, kodblock, korsreferenser). Cirka 70 av dem verifierades mot primärkällor på webben (officiell dokumentation, pressmeddelanden, changelogs, paketregister); resten kontrollerades lokalt (figurer, ankare, filer, bokindex). Observera att den delade WebSearch-budgeten tog slut under granskningen; de återstående kontrollerna gjordes därför med direkta hämtningar av leverantörsdokumentation (WebFetch/curl), vilket anges där det påverkar säkerheten i bedömningen.

Notering om valideringsskript: `scripts/verify_links.py` som nämns i `CLAUDE.md` finns inte i repot. `scripts/verify_sources.py` skriver en rapportfil i repot och kördes därför inte (granskningen skulle inte ändra några filer). Rekommenderat efter korrigering: `python3 scripts/verify_sources.py` samt `python3 -m pytest tests/test_technical_accuracy.py -v`.

## Sammanfattning

Den tekniska huvudtexten i Del D är i stora drag korrekt: rabattsatser för AWS Savings Plans/Reserved Instances och Azure-reservationer, Kubernetes PSP/PSA-historiken, Terraform-kommandon och flaggor (`fmt -check`, `validate`, `init -backend=false`, `test`, import-block i 1.5), Vitest- och Checkov-flaggor, GitHub branch protection samt AWS-regionerna stämmer mot primärkällor. De allvarliga problemen ligger i källapparaten och i två kodexempel. Den centrala källan [15] ("Pulumi. *Testing Infrastructure as Code Programs*. Pulumi Blog, 2024") existerar inte med den titeln och det året; kapitel 13 och 14 tillskriver den dessutom påståenden (kontrasten mot Terraform/HCL, `terraform test`) som bara finns i ett Pulumi-inlägg från juni 2026. Kapitel 14 anger en testharness `@pulumi/pulumi/testing` som inte finns i paketet. Kapitel 16:s CloudFormation-exempel beskriver ett importförfarande med ett AWS CLI-kommando som inte existerar (`import-resources-to-stack`) och en mall som bryter mot CloudFormations importregler (saknar `DeletionPolicy`, blandar import med nyskapade resurser). Därutöver är minst tolv källposter i kapitlens "## Sources" leverantörs-/organisationsrapporter vars titlar inte går att återfinna (NIST, CSA, FinOps Foundation, AXELOS, Gartner, Microsoft m.fl.), och flera av dem innehåller bokens eget begrepp "Architecture as Code" i titeln, vilket starkt talar för att de är fabricerade. Marknadssiffrorna (MarketsandMarkets, Gartner) är korrekt återgivna men fel- eller ofullständigt daterade, och Gartner-siffran är överspelad av senare prognoser. Några påståenden är föråldrade per 2026 (Amazon Linux 2, `dynamodb_table`-låsning, Node 20, GCP:s CUD-procent) och Terraform-testbarheten beskrivs som den såg ut före `terraform test` 1.6/1.7.

## Fynd

### D-01 Källa [15] "Testing Infrastructure as Code Programs" (Pulumi Blog, 2024) finns inte – och tillskrivs innehåll från ett inlägg daterat 2026
- **Fil:rad:** docs/13_testing_strategies.md:29, :31, :39, :420; docs/14_practical_implementation.md:58, :106; docs/33_references.md:21
- **Påstående:** "Pulumi's *Testing Infrastructure as Code Programs* guidance (2024, [Source [15]]) emphasises that defining infrastructure through general-purpose languages lets engineers reuse familiar unit-testing frameworks ... The same guidance contrasts Pulumi's approach with declarative tools such as Terraform, highlighting that HCL lacks first-class unit-testing hooks and therefore leans on `terraform plan`, Terratest, `terraform test`, and policy-as-code engines" samt "[Source [15]] sets clear expectations that Infrastructure as Code repositories must treat testing as a first-class pipeline citizen"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Ingen Pulumi-bloggpost med titeln "Testing Infrastructure as Code Programs" kunde återfinnas (sökning på pulumi.com och webben). De två närmaste är (a) "Testing Your Infrastructure as Code with Pulumi", Joe Duffy, 17 april 2019 (https://www.pulumi.com/blog/testing-your-infrastructure-as-code-with-pulumi/) – inlägget är markerat "Some parts of this blog post are out-of-date", nämner inte Terraform, HCL, Terratest eller `terraform test` och använder inte formuleringen "first-class pipeline citizen"; och (b) "How to Test Infrastructure as Code", Alex Leventer, publicerad 30 juni 2026 (https://www.pulumi.com/blog/how-to-test-infrastructure-as-code/) – det är detta inlägg som innehåller kontrasten mot Terraform ("With Terraform, your infrastructure is HCL but your tests must be something else—either Go (Terratest) or a constrained HCL DSL (`terraform test`)") och nämner pytest/Mocha. Pulumis officiella testdokumentation (https://www.pulumi.com/docs/iac/concepts/testing/) nämner inte Terraform alls. Kapitlets beskrivning kan alltså inte stämma för en källa daterad 2024.
- **Förslag:** Byt källa [15] till en verklig och daterbar referens, t.ex. Pulumi, *Testing* (dokumentation, https://www.pulumi.com/docs/iac/concepts/testing/, hämtad 2026-10-30) och, om kontrasten mot Terraform ska behållas, Leventer, A., *How to Test Infrastructure as Code*, Pulumi Blog, 30 juni 2026. Tona ned "sets clear expectations ... first-class pipeline citizen" till en egen slutsats eller stryk attributionen. Uppdatera även raden i `33_references.md` (titel, år, URL, "Referenced in" ska inkludera kapitel 14).

### D-02 Testharnessen `@pulumi/pulumi/testing` existerar inte
- **Fil:rad:** docs/14_practical_implementation.md:38
- **Påstående:** "Teams can exercise architectural guardrails without provisioning resources by using Pulumi's `@pulumi/pulumi/testing` harness to assert resource properties"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Paketet `@pulumi/pulumi` (v3.273.0, kontrollerat via unpkg 2026-10-30) innehåller ingen `testing/`-modul (`https://unpkg.com/@pulumi/pulumi@3.273.0/testing/index.js` ger 404; `package.json` har inget `exports`-fält som exponerar en sådan sökväg). Mock-stödet ligger i `runtime/mocks.js` och används som `pulumi.runtime.setMocks(...)` från `@pulumi/pulumi` (TypeScript/JavaScript), `pulumi.runtime.set_mocks()` (Python) respektive namnrymden `Pulumi.Testing` i .NET – vilket sannolikt är förväxlingskällan (se Pulumis inlägg "How to Test Infrastructure as Code", 2026, som listar dessa API:er).
- **Förslag:** Skriv t.ex. "...by using Pulumi's mocking API (`pulumi.runtime.setMocks` in TypeScript, `pulumi.runtime.set_mocks` in Python, the `Pulumi.Testing` namespace in .NET) to assert resource properties".

### D-03 AWS CLI-kommandot `aws cloudformation import-resources-to-stack` existerar inte, och `create-stack` importerar inte resurser
- **Fil:rad:** docs/16_migration.md:196–200
- **Påstående:** "1. aws cloudformation create-stack --stack-name ${ProjectName}-import --template-body file://legacy-import-template.yaml / 2. aws cloudformation import-resources-to-stack --stack-name ${ProjectName}-import --resources file://import-resources.json"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** AWS CLI v2-referensen för CloudFormation (https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloudformation/index.html, kontrollerad 2026-10-30) innehåller inget kommando `import-resources-to-stack` (det enda import-kommandot är `import-stacks-to-stack-set`). Enligt AWS-dokumentationen "Creating a stack from existing resources" (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-new-stack.html) sker import via `aws cloudformation create-change-set --stack-name ... --change-set-name ... --change-set-type IMPORT --template-body/--template-url ... --resources-to-import file://ResourcesToImport.txt` följt av `aws cloudformation execute-change-set`. Ett `create-stack` med mallen i kapitlet skulle i stället skapa nya resurser (VPC, instans, säkerhetsgrupp, subnät).
- **Förslag:** Ersätt instruktionerna med: (1) `aws cloudformation create-change-set --stack-name <name> --change-set-name import --change-set-type IMPORT --template-body file://legacy-import-template.yaml --resources-to-import file://resources-to-import.json`, (2) `aws cloudformation describe-change-set ...`, (3) `aws cloudformation execute-change-set ...`, (4) `aws cloudformation detect-stack-drift --stack-name <name>`. Visa även formatet för `resources-to-import.json` (`ResourceType`, `LogicalResourceId`, `ResourceIdentifier`).

### D-04 CloudFormation-importmallen bryter mot importreglerna (saknar `DeletionPolicy`, blandar import med nyskapande)
- **Fil:rad:** docs/16_migration.md:90–179
- **Påstående:** Mallen "legacy-import-template.yaml" med `ExistingVPC`, `ExistingInstance`, `ExistingSecurityGroup`, `ExistingSubnet` presenteras som "Template for import of existing resources to CloudFormation management"
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** AWS: "Each resource to import must have a `DeletionPolicy` attribute for the import operation to succeed" och "Import operations don't allow new resource creations, resource deletions, or changes to property configurations" (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources-manually.html). Ingen resurs i mallen har `DeletionPolicy`. Säkerhetsgruppen och subnätet beskrivs som nyskapade stödresurser (de har inga parametrar för befintliga ID:n och nämns inte som importmål), vilket inte är tillåtet i samma importoperation. Dessutom tillåter mallen ingress på port 22 från 10.0.0.0/8 och 80/443 från 0.0.0.0/0 på en resurs som rubriceras som "Imported security group", vilket motsäger kravet att egenskaperna ska matcha den befintliga konfigurationen.
- **Förslag:** Lägg till `DeletionPolicy: Retain` på varje importerad resurs, ta med säkerhetsgrupp och subnät i `resources-to-import.json` (med `GroupId` respektive `SubnetId` som identifierare) eller flytta dem till en separat uppdatering efter importen, och ersätt det hårdkodade AMI-ID:t (se D-11). Kör gärna `aws cloudformation validate-template` och en faktisk IMPORT-changeset mot ett testkonto innan exemplet publiceras.

### D-05 Kapitel 13: tre källor utan verifierbar existens (AWS, NIST, CSA)
- **Fil:rad:** docs/13_testing_strategies.md:416, :418, :419 (samt :414)
- **Påstående:** "**Amazon Web Services (2024).** *Infrastructure Testing Strategy Guide.*"; "**NIST (2024).** *Security Testing for Cloud Infrastructure.* NIST Cybersecurity Framework."; "**Cloud Security Alliance (2024).** *Cloud Security Testing Guidelines.*"
- **Bedömning:** EJ VERIFIERBART (sannolikt fabricerade titlar)
- **Allvarlighet:** Hög
- **Evidens:** Riktade sökningar på exakta titlar gav inga träffar hos NIST (csrc.nist.gov/nist.gov), CSA (cloudsecurityalliance.org) eller AWS. NIST har ingen publikation med titeln "Security Testing for Cloud Infrastructure"; NIST CSF 2.0 (februari 2024) är ett ramverk, inte en testguide. CSA:s publikationer heter bl.a. "Security Guidance for Critical Areas of Focus in Cloud Computing" och "Cloud Controls Matrix". Posterna saknar URL, dokumentnummer och finns inte i `docs/33_references.md`. Även post 1 ("Gruntwork (2024). *Terratest Documentation: Infrastructure Testing for Terraform*") använder en beskrivande text som titel; dokumentationssajten heter bara "Terratest" (https://terratest.gruntwork.io/docs/).
- **Förslag:** Stryk posterna 3, 5 och 6 eller ersätt dem med verifierbara källor, t.ex. AWS Well-Architected Framework (Operational Excellence, "Perform operations as code"), NIST SP 800-53 Rev. 5 (redan källa [11]) och CSA *Cloud Controls Matrix v4* med URL och hämtningsdatum. Rätta post 1 till "Gruntwork. *Terratest* (documentation). https://terratest.gruntwork.io/docs/".

### D-06 Kapitel 15: tre källor med fabricerade titlar (FinOps Foundation, CSA, Microsoft)
- **Fil:rad:** docs/15_cost_optimization.md:149, :151, :155
- **Påstående:** "**FinOps Foundation (2023).** *FinOps Framework and Architecture as Code Best Practices.* The Linux Foundation."; "**Cloud Security Alliance (2023).** *Cloud Cost Optimisation Security Guidelines.* CSA Research."; "**Microsoft (2023).** *Azure Cost Management Architecture as Code Best Practices.* Microsoft Azure Documentation."
- **Bedömning:** EJ VERIFIERBART (sannolikt fabricerade titlar)
- **Allvarlighet:** Hög
- **Evidens:** FinOps Foundations ramverkssida (https://www.finops.org/framework/) listar inga publikationer med "Architecture as Code" i titeln; sökning på den exakta titeln gav inga träffar. Samma gäller CSA-titeln. Microsofts faktiska vägledning heter "Optimize your cloud investment with Cost Management" (https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-best-practices) och nämner inte "Architecture as Code". Att bokens eget nyckelbegrepp förekommer i två leverantörstitlar talar för att titlarna är konstruerade.
- **Förslag:** Ersätt med FinOps Foundation, *FinOps Framework* (https://www.finops.org/framework/, hämtad 2026-10-30), Microsoft Learn, *Optimize your cloud investment with Cost Management* (2025) och stryk CSA-posten eller byt till en verklig CSA-publikation.

### D-07 Kapitel 16: tre källor med fabricerade titlar (Microsoft, Gartner, AXELOS)
- **Fil:rad:** docs/16_migration.md:406, :408, :409
- **Påstående:** "**Microsoft (2023).** *Azure Migration Framework and Architecture as Code Best Practices.*"; "**Gartner (2023).** *Infrastructure Migration Trends in European Markets.* Gartner Research."; "**AXELOS (2023).** *ITIL Foundation: IT Service Management for Cloud Migration.* AXELOS."
- **Bedömning:** EJ VERIFIERBART (sannolikt fabricerade titlar)
- **Allvarlighet:** Hög
- **Evidens:** Riktade sökningar på de exakta titlarna gav inga träffar hos Gartner, AXELOS/PeopleCert eller Microsoft. Microsofts migrationsvägledning heter "Cloud Adoption Framework – Migrate" (https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/); något "Azure Migration Framework" finns inte och sidan nämner inte "Architecture as Code". AXELOS officiella ITIL-publikation är *ITIL Foundation, ITIL 4 Edition* (TSO, 2019, ISBN 978-0-11-331607-6); ingen titel om "Cloud Migration" finns. Ingen av posterna finns i `docs/33_references.md`.
- **Förslag:** Ersätt med verifierbara källor, t.ex. Microsoft Learn, *Cloud Adoption Framework for Azure: Migrate* (2025); AXELOS, *ITIL Foundation, ITIL 4 Edition* (2019) om ITIL alls behövs; stryk Gartner-posten eller ersätt med ett verkligt, citerbart Gartner-dokument med dokument-ID.

### D-08 Gartner-prognosen är feldaterad och överspelad (679 miljarder USD/20,4 %)
- **Fil:rad:** docs/15_cost_optimization.md:75, :153; docs/33_references.md:157
- **Påstående:** "Gartner's *Forecast Analysis: Public Cloud Services Worldwide* (2024) anticipates worldwide public cloud spending reaching USD 679 billion in 2024—a year-on-year increase of 20.4 per cent."
- **Bedömning:** FÖRÅLDRAT / FELCITERAT (år)
- **Allvarlighet:** Medel
- **Evidens:** Siffrorna kommer från Gartners pressmeddelande av den 13 november 2023 ("Worldwide end-user spending on public cloud services is forecast to grow 20.4% to total $678.8 billion in 2024", https://www.gartner.com/en/newsroom/press-releases/11-13-2023-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-reach-679-billion-in-20240) – alltså publicerat 2023, inte 2024. Gartner reviderade sedan: pressmeddelandet 19 november 2024 anger 2024-utfallet till 595,7 miljarder USD (+19,2 %) och 2025 till 723,4 miljarder USD (+21,5 %) (https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025; sekundärt bekräftat via digit.fyi 2024-11-19). För en bok med release 2025.10 och läsare 2026 är 679-siffran inaktuell.
- **Förslag:** Skriv t.ex. "Gartner (November 2024) estimated worldwide public cloud end-user spending at USD 595.7 billion for 2024 and forecast USD 723.4 billion for 2025 (+21.5 per cent)" och datera källan korrekt (Gartner pressmeddelande, 19 november 2024) i både kapitlet och `33_references.md`.

### D-09 Terraforms testbarhet beskrivs som den var före `terraform test` 1.6/1.7
- **Fil:rad:** docs/13_testing_strategies.md:31; docs/14_practical_implementation.md:42
- **Påstående:** "HCL lacks first-class unit-testing hooks and therefore leans on `terraform plan`, Terratest, `terraform test`, and policy-as-code engines to approximate the same assurance. Those options ... routinely execute against rendered plans or ephemeral infrastructure, so feedback loops tend to stretch towards integration-time cadences" och "their testing story often centres on plan evaluation, module contract tests, and policy-as-code gatekeeping rather than true unit-level execution"
- **Bedömning:** TVEKSAMT / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Terraform 1.6 (GA 4 oktober 2023) införde det inbyggda testramverket (`.tftest.hcl`, `run`-block med `command = plan`), och Terraform 1.7 (17 januari 2024) lade till provider-mocking (`mock_provider`, `mock_resource`, `override_*`) så att tester kan köras "without having to create actual infrastructure or requiring credentials" (https://www.hashicorp.com/blog/terraform-1-6-adds-a-test-framework-for-enhanced-code-validation; https://www.hashicorp.com/blog/terraform-1-7-adds-test-mocking-and-config-driven-remove). Att kalla detta "approximate" och "rather than true unit-level execution" är en Pulumi-färgad förenkling som inte längre speglar läget; texten nämner inte mocking alls.
- **Förslag:** Nyansera: "Since Terraform 1.6 (test framework) and 1.7 (provider mocking) HCL modules can be unit-tested without real infrastructure; the remaining difference is expressiveness of HCL assertions versus a general-purpose language and ecosystem maturity." Lägg till källa [26] (HashiCorp, *Write Terraform Tests*) som redan finns i `33_references.md`.

### D-10 Kubecost beskrivs som öppen källkod – det är IBM/Apptios kommersiella produkt; OpenCost är open source-projektet
- **Fil:rad:** docs/15_cost_optimization.md:63, :150
- **Påstående:** "Open source tools like Cloud Custodian and Kubecost can be integrated into Architecture as Code pipelines to automate this analysis and recommend optimal resource placement across regions."
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Kubecost säljs i dag som "IBM Kubecost" via Apptio ("Apptio, an IBM Company") med en gratis Foundations-nivå och betalda Enterprise-nivåer; sidan säger endast att "Kubecost began as an open-source project" (https://www.apptio.com/products/kubecost/). Den öppna komponenten är OpenCost (Apache 2.0), "originally developed and open sourced by Kubecost" (https://github.com/opencost/opencost/blob/develop/README.md), CNCF Incubating sedan 25 oktober 2024 (https://www.cncf.io/projects/opencost/). Cloud Custodian är korrekt beskrivet (open source, CNCF Incubating, https://cloudcustodian.io/). Varken OpenCost eller Cloud Custodian "rekommenderar optimal resursplacering across regions"; de allokerar/rapporterar kostnader respektive upprätthåller policyer.
- **Förslag:** "Open source tools such as Cloud Custodian (policy enforcement) and OpenCost (Kubernetes cost allocation, the CNCF project from which the commercial IBM Kubecost product originates) can be integrated ... to automate cost attribution and reporting". Rätta källpost 3 i enlighet med detta.

### D-11 Exemplet pekar på Amazon Linux 2, som nådde end-of-support 2026-06-30
- **Fil:rad:** docs/16_migration.md:117
- **Påstående:** "ImageId: 'ami-0c94855bb95b03c2e'  # Replace with SSM Parameter Store lookup: {{resolve:ssm:/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2}}"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** "Amazon Linux 2 reached its end of support on 2026-06-30" och AWS rekommenderar migrering till AL2023 (https://aws.amazon.com/amazon-linux-2/faqs/). AWS officiella CloudFormation-mönster för AL2023 använder en parameter av typen `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` med default `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64` (https://docs.aws.amazon.com/linux/al2023/ug/ec2.html).
- **Förslag:** Byt till AL2023-sökvägen och parametertypen ovan. Notera också att i ett importscenario måste `ImageId` matcha den befintliga instansens AMI – kommentaren om "latest AMI" är i sig motsägelsefull för en importmall.

### D-12 `dynamodb_table` för S3-backend-låsning är utfasat sedan Terraform 1.11
- **Fil:rad:** docs/13_testing_strategies.md:87–90
- **Påstående:** "terraform init -backend-config=\"bucket=${TF_BACKEND_BUCKET}\" -backend-config=\"dynamodb_table=${TF_LOCK_TABLE}\" -backend-config=\"kms_key_id=${TF_KMS_KEY}\""
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Terraform 1.10 (november 2024) införde S3-nativ låsning; Terraform 1.11.0 CHANGELOG: "S3 native state locking is now generally available. The `use_lockfile` argument enables users to adopt the S3-native mechanism for state locking. As part of this change, we've deprecated the DynamoDB-related arguments" (https://github.com/hashicorp/terraform/blob/v1.11.0/CHANGELOG.md). Backend-dokumentationen markerar `dynamodb_table` som "(Optional, **Deprecated**)" och säger att "DynamoDB-based locking is deprecated and will be removed in a future minor version" (https://developer.hashicorp.com/terraform/language/backend/s3).
- **Förslag:** Ersätt raden med `-backend-config="use_lockfile=true"` (och behåll `encrypt=true`/`kms_key_id`). Lägg till en fotnot om att DynamoDB-låsning fortfarande fungerar för migrering men är utfasad.

### D-13 Del D-introduktionen räknar in kapitel 15A (Evidence as Code), som i bokindexet tillhör Del C
- **Fil:rad:** docs/part_d_delivery.md:13, :23; docs/book_index.json:35, :44
- **Påstående:** "The dedicated chapter on [Evidence as Code](15a_evidence_as_code.md) shows how to package these artefacts ..." under "What you will learn in this part: ... Evidence automation practices that keep compliance artefacts reusable and trustworthy"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `docs/book_index.json` placerar `15A` ("Evidence as Code and Continuous Assurance") i `part_c` ("Security, Governance & Assurance") och Del D innehåller 13, 14, 15B och 16. Del D-texten presenterar däremot 15A som en del av "this part". Kapitel 15 identifieras i indexet som `15B` men omnämns i hela boken (kap. 5, 21, 25, 26A, bilaga A, `33_references.md`) som "Chapter 15"; identifieraren 15B syns ingenstans i brödtexten.
- **Förslag:** Antingen flytta 15A till Del D i `book_index.json` (om det är avsikten) eller skriv om stycket till en framåt-/bakåtreferens ("The Evidence as Code chapter in Part C ..."). Besluta om kapitlet ska heta 15 eller 15B och gör det konsekvent i index, korsreferenser och referenslista.

### D-14 Kapitel 13:s källa 2 har en titel som varken motsvarar källa [10] eller något OPA-dokument
- **Fil:rad:** docs/13_testing_strategies.md:415; docs/33_references.md:16
- **Påstående:** "**Open Policy Agent (2024).** *Policy Testing Best Practices for Infrastructure as Code.* CNCF OPA Project. [Source [10]]"
- **Bedömning:** FELCITERAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Källa [10] i `33_references.md` lyder "Open Policy Agent. *Policy as Code Overview.* CNCF OPA Project, 2024. https://www.openpolicyagent.org/docs" – en annan titel. OPA:s dokumentationssida om tester heter "Policy Testing" (https://www.openpolicyagent.org/docs/policy-testing, `opa test`, `test_`-regler); inget OPA-dokument heter "Policy Testing Best Practices for Infrastructure as Code".
- **Förslag:** Ändra posten till "Open Policy Agent. *Policy Testing.* OPA Documentation, https://www.openpolicyagent.org/docs/policy-testing (hämtad 2026-10-30)" och lägg till den som egen numrerad källa, eller använd exakt samma titel som källa [10].

### D-15 Kapitel 14: fem odaterade leverantörskällor med titlar som inte kan återfinnas
- **Fil:rad:** docs/14_practical_implementation.md:99–103
- **Påstående:** "**HashiCorp.** *Terraform Architecture as Code Best Practices.* HashiCorp Learn Platform."; "**Amazon Web Services.** *AWS Well-Architected Framework: Infrastructure as Code.*"; "**Google Cloud.** *Infrastructure as Code Design Patterns.* Google Cloud Architecture Centre."; "**Microsoft Azure.** *Azure Resource Manager Best Practices.*"; "**Puppet.** *Infrastructure as Code Implementation Guide.* Puppet Enterprise Documentation."
- **Bedömning:** EJ VERIFIERBART / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** HashiCorp har ingen publikation med bokens begrepp "Architecture as Code" i titeln (deras närmaste är "Terraform recommended practices", https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices, redan källa [20], och "Terraform style guide"). AWS Well-Architected Framework består av sex pelare; något dokument "AWS Well-Architected Framework: Infrastructure as Code" finns inte (IaC behandlas som designprincipen "Perform operations as code"). Google Clouds IaC-vägledning heter "Best practices for general style and structure" under "Infrastructure as code" (https://docs.cloud.google.com/docs/terraform/best-practices-for-terraform); inget dokument heter "Infrastructure as Code Design Patterns". Microsofts sida heter "Best practices for templates - Azure Resource Manager" (https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/best-practices) – den enda posten med en nära motsvarighet. Puppet-titeln kunde inte verifieras (sökbudget slut). Ingen av posterna har år, URL eller finns i `33_references.md`.
- **Förslag:** Ersätt med exakta titlar, år och URL:er (t.ex. HashiCorp *Terraform recommended practices* [källa 20]; AWS *AWS Well-Architected Framework* (2024); Google Cloud *Best practices for general style and structure* (Terraform); Microsoft Learn *Best practices for templates - Azure Resource Manager* (2026)) och stryk Puppet-posten om ingen verklig källa finns.

### D-16 Övriga leverantörskällor i kapitel 15 och 16 med fel eller oklara titlar
- **Fil:rad:** docs/15_cost_optimization.md:148, :150; docs/16_migration.md:405, :407
- **Påstående:** "**Amazon Web Services (2023).** *AWS Cost Optimisation Guide.*"; "**Kubecost (2023).** *Kubernetes Cost Optimisation Guide.*"; "**Amazon Web Services (2023).** *Large-Scale Migration and Modernisation Guide.*"; "**Google Cloud (2023).** *Infrastructure Migration Strategies.* Google Cloud Architecture Centre."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** AWS närmaste dokument är whitepapern "Cost Optimization Pillar - AWS Well-Architected Framework" (publicerad 27 juni 2024, https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html) – inte "AWS Cost Optimisation Guide" (brittisk stavning används inte av AWS). AWS migrationsvägledning heter "Guide for AWS large migrations" (AWS Prescriptive Guidance, https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/introduction.html). Google Clouds serie heter "Migrate to Google Cloud: Get started" m.fl. (https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started); inget dokument heter "Infrastructure Migration Strategies". Kubecost-guiden kunde inte verifieras (Kubecost-domänen omdirigerar numera till apptio.com).
- **Förslag:** Byt till de verkliga titlarna ovan med URL och publiceringsdatum; stryk Kubecost-posten eller ersätt med OpenCost-dokumentationen (https://www.opencost.io/docs/).

### D-17 Besparingsintervallet 20–40 % saknar källa
- **Fil:rad:** docs/15_cost_optimization.md:144
- **Påstående:** "EU organisations that implement these strategies can achieve 20–40% cost reduction in their cloud operations (Figures drawn from practitioner case studies; actual savings vary by workload profile and baseline optimisation maturity.) whilst ensuring regulatory compliance"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Ingen av kapitlets källor stöder siffran; "practitioner case studies" är inte namngivna eller citerbara. Bokens referenslista hänvisar endast till "Nordqvist, G. ... Author's own professional practice. Available on request" (33_references.md:155). Parentesen avslutas dessutom med punkt mitt i en mening.
- **Förslag:** Antingen koppla siffran till en namngiven, publik källa (t.ex. FinOps Foundation *State of FinOps* eller Flexera *State of the Cloud Report* med årtal och vad populationen avser) eller skriv om till "Practitioner reports commonly cite savings in the range of 20–40 per cent; results vary ..." och flytta förbehållet till en fotnot.

### D-18 Referenslistan är ofullständig och inkonsekvent gentemot Del D-kapitlen
- **Fil:rad:** docs/33_references.md:10, :15, :16, :21, :22, :99–100, :157–162, :178; docs/14_practical_implementation.md:58, :104–106; docs/15_cost_optimization.md:77
- **Påstående:** "All citations in the manuscript are included in this compiled list, ensuring complete transparency and academic rigour throughout the work."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** (a) Inga av kapitel 13:s källor 1, 3, 5, 6, kapitel 14:s 1–5, kapitel 15:s 1–4 och 8 eller kapitel 16:s 1–5 återfinns i `33_references.md`. (b) Källa [15] anges "Referenced in: Chapter 13" trots att kapitel 14 citerar den (rad 58, 106); källa [16] anges för kapitel 9/9b men citeras i kapitel 14 rad 58 – och kapitel 14:s egen källista utelämnar [16]. (c) IDC-posten anges "Referenced in: Chapter 5, Chapter 21" men citeras i kapitel 15 rad 77. (d) Posterna för källa [1], [4], [10] länkar till filer som inte finns (`26a_future_trends.md`, `20_team_structures.md`, `10_policy_as_code.md`, `32_index.md`). (e) Gartner- och MarketsandMarkets-posterna saknar URL/dokument-ID.
- **Förslag:** Kör `python3 scripts/audit_references.py` och `python3 scripts/verify_sources.py`, lägg till alla kapitelkällor i referenslistan med URL och hämtningsdatum, rätta "Referenced in"-fälten och de brutna filnamnen, och tona ned meningen om fullständighet tills listan stämmer.

### D-19 CloudFormation drift detection presenteras som importmekanism
- **Fil:rad:** docs/16_migration.md:38
- **Påstående:** "Infrastructure inventory automation through tools such as Terraform import, CloudFormation drift detection and Azure Resource Manager templates enables systematic conversion of existing resources to Architecture as Code management."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Drift detection jämför en befintlig stacks resurser med mallen; den konverterar inte oförvaltade resurser. CloudFormations funktioner för detta är "IaC generator" (skannar och genererar mallar) och "resource import" (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html). För Azure är motsvarigheten "Export template"/`az group export` samt Bicep `import`-stöd, inte ARM-mallar i sig.
- **Förslag:** "...such as Terraform `import` blocks, the CloudFormation IaC generator and resource import, and Azure Resource Manager template export ..."

### D-20 MarketsandMarkets-rapporten är daterad 2022, inte 2023, och titeln är inte rapportens
- **Fil:rad:** docs/15_cost_optimization.md:73, :152; docs/33_references.md:99
- **Påstående:** "MarketsandMarkets (2023) forecasts that the global Infrastructure as Code market will expand from USD 0.8 billion in 2022 to USD 2.3 billion by 2027, representing a compound annual growth rate of about 24 per cent." / "**MarketsandMarkets (2023).** *Infrastructure as Code Market Report.*"
- **Bedömning:** FELCITERAT (datering/titel) – siffrorna är korrekta
- **Allvarlighet:** Låg
- **Evidens:** Pressmeddelandet "Infrastructure as Code Market worth $2.3 billion by 2027" är daterat 12 augusti 2022 och anger exakt "to reach USD 2.3 billion by 2027 from USD 0.8 billion in 2022 ... CAGR of 24.0%" (https://nz.finance.yahoo.com/news/infrastructure-code-market-worth-2-143000264.html; rapporten är kodad TC 8140, augusti 2022, https://www.marketsandmarkets.com/Market-Reports/infrastructure-as-code-market-115458264.html). Rapportens titel är "Infrastructure as Code Market – Global Forecast to 2027". En återpublicering via GlobeNewswire den 3 maj 2023 förklarar sannolikt årtalet 2023.
- **Förslag:** "MarketsandMarkets (2022), *Infrastructure as Code Market – Global Forecast to 2027* (report TC 8140, August 2022)"; ange också att prognosen är fyra år gammal.

### D-21 Google Clouds CUD-rabatt anges till "up to 57%" – aktuell dokumentation säger 55 % (70 % för minnesoptimerade)
- **Fil:rad:** docs/15_cost_optimization.md:128
- **Påstående:** "| Google Cloud | Committed Use Discounts (resource-based and spend-based) | Up to 57% |"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Google: "You get a discount of up to 70% for memory-optimized machine series and a discount of up to 55% for all other machine series" (resursbaserade CUD:er); flexibla (spend-based) CUD:er ger 28 % (1 år) respektive 46 % (3 år) för de flesta maskinserier (https://docs.cloud.google.com/compute/docs/instances/committed-use-discounts-overview; https://docs.cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts, kontrollerade 2026-10-30). Siffran 57 % är Googles äldre marknadsföringsvärde.
- **Förslag:** "Up to 55% (resource-based; up to 70% for memory-optimised series); 28–46% for flexible spend-based CUDs".

### D-22 Pulumi CLI-flaggor: `pulumi stack ls --json` är inte längre dokumenterad; "`pulumi up --policy-pack` in preview mode" är motsägelsefullt
- **Fil:rad:** docs/13_testing_strategies.md:43, :45
- **Påstående:** "`pulumi stack ls --json` to verify workspace metadata" och "`pulumi up --policy-pack policies/` in preview mode"
- **Bedömning:** FÖRÅLDRAT / TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Den aktuella CLI-referensen för `pulumi stack ls` listar `--output string  Output format. Supported values are: default and json` men ingen `--json`/`-j`-flagga (https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_ls/). `--json` lades till i v0.16.6 (2018) och `--output $format` i 3.249.0 (1 juli 2026) enligt Pulumis CHANGELOG; om `--json` kvarstår som dold alias kunde inte fastställas. `pulumi preview` har en egen `--policy-pack`-flagga (https://www.pulumi.com/docs/iac/cli/commands/pulumi_preview/), så "up ... in preview mode" bör vara `pulumi preview --policy-pack policies/`.
- **Förslag:** Skriv `pulumi stack ls --output json` respektive `pulumi preview --policy-pack policies/`.

### D-23 GitHub Actions-exemplet pinnar Node.js 20, som nådde end-of-life 2026-04-30
- **Fil:rad:** docs/13_testing_strategies.md:63–65
- **Påstående:** "- uses: actions/setup-node@v4 / with: node-version: 20"
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Node.js release-schema: v20 "end": "2026-04-30" (https://github.com/nodejs/Release/blob/main/schedule.json); v22 stöds till 2027-04-30. Samma gäller `node: "20.11.1"` i `BOOK_REQUIREMENTS.md` (utanför granskade filer).
- **Förslag:** `node-version: 22` (eller `lts/*`) och uppdatera verktygskedjans pinning.

### D-24 Migrationstestskriptet: hårdkodat 2023-datum, null-hantering och CloudWatch-anrop utan dimensioner
- **Fil:rad:** docs/16_migration.md:227, :234–237, :282–287, :352–362
- **Påstående:** "--query 'Snapshots[?StartTime>=`2023-01-01T00:00:00.000Z`]' > /tmp/recent-snapshots.json" ... "WARNING: Insufficient recent snapshots"; "aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization ... --statistics Average" följt av "jq '.Datapoints | map(.Average) | add / length'"; kommentaren "(The -dry-run flag does not exist in Terraform; use import blocks instead.)"
- **Bedömning:** FÖRÅLDRAT / TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Ett fast datum från 2023 definierar inte "recent" i en bok som läses 2026 (använd `date -u -d '7 days ago'`). `INSTANCE_COUNT` blir `null` om inga reservationer finns (`jq -s 'add'` på tom indata), varpå `[ ... -lt ... ]` ger "integer expression expected". AWS: "Aggregate statistics are available for instances that have detailed monitoring enabled. Instances that use basic monitoring are not included in the aggregates" (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/GetSingleMetricAllDimensions.html) – med basic monitoring blir `Datapoints` tom och `add / length` faller på division med noll. Parentesen om `-dry-run` är ett redaktionellt restmeddelande som inte hör hemma i ett kodexempel; att import-block kom i Terraform 1.5 (12 juni 2023) är däremot korrekt (https://www.hashicorp.com/blog/terraform-1-5-brings-config-driven-import-and-checks).
- **Förslag:** Beräkna datumgränsen dynamiskt, sätt `INSTANCE_COUNT=${INSTANCE_COUNT:-0}` (eller `jq -s 'add // 0'`), lägg till `--dimensions Name=InstanceId,Value=...` eller en kommentar om detailed monitoring, skydda `add / length` mot tom lista och stryk `-dry-run`-kommentaren.

### D-25 Överdrivna verktygspåståenden om kostnadskontroll (Terraform Enterprise, Terraform-providers, CloudWatch)
- **Fil:rad:** docs/15_cost_optimization.md:29, :41, :51
- **Påstående:** "Terraform Enterprise, AWS Cost Management, and Azure Cost Management offer APIs that can be integrated into Architecture as Code workflows for real-time cost control"; "Terraform providers for AWS, Azure, and GCP can automatically implement rightsizing recommendations"; "CloudWatch, Azure Monitor, and Google Cloud Monitoring can be configured as code to track costs at a granular level"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** HCP Terraform/Terraform Enterprise erbjuder "cost estimation" – en uppskattning per körning för AWS, GCP och Azure som visas mellan plan och apply och kan användas i Sentinel-policyer; dokumentationen beskriver inga budgetlarm eller realtidskontroll (https://developer.hashicorp.com/terraform/cloud-docs/cost-estimation). Terraform-providers implementerar inte rightsizing-rekommendationer; det kräver att någon (person eller automation) ändrar konfigurationen utifrån AWS Compute Optimizer/Azure Advisor/GCP Recommender. CloudWatch exponerar endast faktureringsmetriken `EstimatedCharges` (i us-east-1); granulär kostnadsdata kommer från Cost Explorer/CUR, Azure Cost Management respektive Cloud Billing export till BigQuery.
- **Förslag:** Skriv "cost estimation in HCP Terraform/Terraform Enterprise", "rightsizing recommendations from AWS Compute Optimizer, Azure Advisor and GCP Recommender can be turned into reviewed Terraform changes" och "Cost Explorer/CUR, Azure Cost Management and Cloud Billing export (with CloudWatch/Azure Monitor billing alarms)".

### D-26 AWS Config Rules beskrivs som i första hand preventiva
- **Fil:rad:** docs/13_testing_strategies.md:264
- **Påstående:** "Policy-as-code frameworks such as Open Policy Agent (OPA) and AWS Config Rules enable declarative definition of compliance policies that can be enforced automatically during infrastructure deployment. This preventative approach is more effective than reactive compliance monitoring."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** AWS Config utvärderar som standard resurser efter att de skapats/ändrats (detektivt läge, med valfri automatisk remediering); ett proaktivt läge finns men måste aktiveras separat ("Turning on Proactive Evaluation", https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html). Att gruppera AWS Config med OPA som "preventative" utan den nyansen är missvisande.
- **Förslag:** "...OPA (preventive, in the pipeline) and AWS Config Rules (detective by default, with optional proactive evaluation and automated remediation)".

### D-27 Figurhantering: kapitel 13 återanvänder kapitel 12:s diagram med annan bildtext; kapitel 15–16 saknar figurnumrering
- **Fil:rad:** docs/13_testing_strategies.md:280–283; docs/12_compliance.md:27; docs/15_cost_optimization.md:3–9, :23, :47; docs/16_migration.md:3
- **Påstående:** "<!-- Note: This diagram is referenced from Chapter 12 assets --> ![Requirements and testing relation](images/diagram_12_requirements_testing.png) *Figure 13.3: Requirements as Code - Traceability ...*"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Samma PNG används i kapitel 12 rad 27 med bildtexten "Compliance requirements traceability map". HTML-kommentaren är ett redaktionellt restmeddelande som följer med till EPUB/HTML. Kapitel 13 och 14 numrerar figurer ("Figure 13.1", "Figure 14.1 –") medan kapitel 15 och 16 bara har kursiva beskrivningar utan nummer.
- **Förslag:** Ta bort HTML-kommentaren, skapa ett kapitel 13-specifikt diagram eller hänvisa explicit till Figure 12.x, och numrera figurerna i kapitel 15 och 16 (validera med `scripts/validate_figure_captions.py`).

### D-28 "GAIA-X" bör skrivas "Gaia-X"
- **Fil:rad:** docs/15_cost_optimization.md:67 (även docs/25_future_trends.md:257, :291, :301)
- **Påstående:** "Cloud sovereignty frameworks, such as the GAIA-X data space model referenced in Chapter 25"
- **Bedömning:** INKONSEKVENT (mot officiell stavning)
- **Allvarlighet:** Låg
- **Evidens:** Organisationen skriver sig "Gaia-X" ("Gaia-X: A Federated Secure Data Infrastructure", https://gaia-x.eu/). Boken är internt konsekvent (versaler i både kap. 15 och 25) men avviker från källan.
- **Förslag:** Ändra till "Gaia-X" i hela manuskriptet (grep `GAIA-X`).

### D-29 Bilagelänkar i kapitel 15 saknar filnamn (bryter i MkDocs-webbplatsen)
- **Fil:rad:** docs/15_cost_optimization.md:92, :105, :116
- **Påstående:** "see [15_CODE_1: Cost-aware Terraform infrastructure configuration](#15_code_1) in Appendix A"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Ankarna `#15_code_1`–`#15_code_3` finns i `docs/30_appendix_code_examples.md` (rad 2793, 2927, 3035), inte i kapitel 15. Kapitel 14 länkar korrekt med filnamn (`30_appendix_code_examples.md#14_code_1`). I den sammanfogade PDF:en fungerar bara-ankare, men på webbplatsen (aac.geon.se, en sida per kapitel) pekar länken till en icke-existerande rubrik på samma sida.
- **Förslag:** Byt till `30_appendix_code_examples.md#15_code_1` osv.

### D-30 Terratest beskrivs som policyvalidator med IDE-integration
- **Fil:rad:** docs/13_testing_strategies.md:25
- **Påstående:** "Terraform testing tools such as Terratest, terraform-compliance and Checkov enable automated validation of HCL code against predefined policies and codified infrastructure best practices. These tools can integrate into IDEs for real-time feedback"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Terratest är ett Go-bibliotek som provisionerar riktig infrastruktur och verifierar den (https://terratest.gruntwork.io/docs/); det validerar inte HCL mot policyer och har ingen IDE-integration. Checkov (VS Code-tillägg) och terraform-compliance (BDD mot plan-JSON) passar beskrivningen bättre. terraform-compliance underhålls aktivt (1.16.0 publicerad 2026-10-22 på PyPI).
- **Förslag:** Dela upp: "Checkov and terraform-compliance validate HCL/plan output against policies (Checkov also in the IDE); Terratest exercises deployed infrastructure from Go tests."

## Verifierat korrekt (urval)

- AWS Compute Savings Plans "up to 66%", EC2 Instance Savings Plans "up to 72%", 1- eller 3-årsterm, flexibilitet över instansfamilj/storlek/AZ/region/OS/tenancy samt Fargate/Lambda – https://aws.amazon.com/savingsplans/compute-pricing/
- AWS Reserved Instances: Standard "up to 72%", Convertible "up to 66%"; AWS egna genomsnitt 40 %/60 % (1/3 år, Standard) gör bokens "30–60%" rimligt som "typical" – https://aws.amazon.com/ec2/pricing/reserved-instances/
- Azure Reservations "up to 72%" (1- eller 3-årsterm) – https://azure.microsoft.com/en-us/pricing/reservations/ och https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-best-practices
- PodSecurityPolicy "deprecated in Kubernetes v1.21, and removed from Kubernetes in v1.25"; Pod Security Admission med lägena enforce/audit/warn, stabil sedan v1.25 – https://kubernetes.io/docs/concepts/security/pod-security-policy/ och https://kubernetes.io/docs/concepts/security/pod-security-admission/
- Terraform 1.5 (12 juni 2023) införde `import`-block ("Import is now a plannable operation"), ingen `-dry-run`-flagga finns – https://www.hashicorp.com/blog/terraform-1-5-brings-config-driven-import-and-checks
- `terraform test` GA i Terraform 1.6 (4 oktober 2023), `.tftest.hcl` – https://www.hashicorp.com/blog/terraform-1-6-adds-a-test-framework-for-enhanced-code-validation
- `terraform init -backend=false`, `terraform fmt -check`, `terraform validate`, `terraform show -json` – https://developer.hashicorp.com/terraform/cli/commands/init
- `checkov -d, --directory` – https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html
- Vitest: `vitest run`, `vitest watch` (alias `vitest dev`), `--coverage`, `--ui`, `--changed [since]` – https://vitest.dev/guide/cli.html
- `pulumi login --cloud-url`, `pulumi preview --policy-pack`, `pulumi up --policy-pack`, `-s/--stack` – https://www.pulumi.com/docs/iac/cli/commands/pulumi_login/, .../pulumi_preview/, .../pulumi_up/
- Pulumi-testnivåer unit/property/integration och användning av värdspråkets testramverk (Mocha, pytest, go test) – https://www.pulumi.com/docs/iac/concepts/testing/
- GitHub branch protection omfattar "Require status checks before merging", "Require pull request reviews before merging" och "Require signed commits" – https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches (källa [4])
- URL:erna för källorna [4], [9], [10], [13], [16] (omdirigerar till /language/manage-sensitive-data) och [26] svarar 200 (curl 2026-10-30)
- AWS-regioner eu-west-1 (Ireland), eu-central-1 (Frankfurt), eu-south-1 (Milan), eu-west-3 (Paris) – https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html
- CloudFormation: AWS::EC2::VPC, ::Instance, ::SecurityGroup, ::Subnet är importerbara resurstyper – https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-supported-resources.html
- JMESPath-strängjämförelse (`StartTime>=\`2023-...\``) fungerar i AWS CLI eftersom jmespath.py tillåter strängar i `_is_comparable` – https://github.com/jmespath/jmespath.py/blob/develop/jmespath/visitor.py
- MarketsandMarkets-siffrorna (0,8 → 2,3 miljarder USD 2022–2027, CAGR 24,0 %) – https://nz.finance.yahoo.com/news/infrastructure-code-market-worth-2-143000264.html (pressmeddelande 12 augusti 2022)
- Gartners siffror 678,8 miljarder USD och 20,4 % för 2024 återges korrekt från pressmeddelandet 13 november 2023 (se dock D-08 om datering och revidering)
- FinOps Framework-faserna Inform, Optimize, Operate; FinOps Foundation är "a Series of LF Projects, LLC" (Linux Foundation) – https://www.finops.org/framework/
- Cloud Custodian är open source och CNCF Incubating – https://cloudcustodian.io/; OpenCost är CNCF Incubating sedan 2024-10-25 – https://www.cncf.io/projects/opencost/
- Amazon Linux 2 end of support 2026-06-30 och AL2023 SSM-parametersökvägar – https://aws.amazon.com/amazon-linux-2/faqs/, https://docs.aws.amazon.com/linux/al2023/ug/ec2.html
- Node.js 20 EOL 2026-04-30 – https://github.com/nodejs/Release/blob/main/schedule.json
- Alla figurfiler som refereras i de fem filerna finns i `docs/images/`; alla Appendix A-ankare (Listing 13-A–13-L, 14_code_1–3, 15_code_1–3) och länkade kapitelfiler (05, 09, 11, 13, 15a, 17, 18, appendix_templates_and_tools) finns; Appendix D innehåller "Migration Assessment Automation" som kapitel 16 hänvisar till; kapitel 25 nämner GAIA-X som kapitel 15 hänvisar till.
- Chaos Monkey beskrivs av Netflix som "responsible for randomly terminating instances in production" – https://netflix.github.io/chaosmonkey/ (bokens "terminating running services" är en acceptabel förenkling).

## Ej verifierbart

- **IDC, *Worldwide DevOps Software Tools Forecast, 2023–2027*** (docs/15_cost_optimization.md:77, :154) och påståendet att "platform engineering, automation, and configuration management account for more than a third of DevOps investment through 2027". Rapporten är betalvara; sökningar hittade IDC:s *Worldwide DevSecOps Software Tools Forecast, 2023–2027* (augusti 2023) och *Worldwide DevOps Software Tools Forecast, 2024–2028*, men inte 2023–2027-utgåvan av DevOps-rapporten eller någon publik siffra om "more than a third". Rekommendation: ange IDC-dokumentnummer (#US...) och sidhänvisning, eller stryk siffran.
- **Puppet, *Infrastructure as Code Implementation Guide*** (docs/14_practical_implementation.md:103) och **Kubecost, *Kubernetes Cost Optimisation Guide*** (docs/15_cost_optimization.md:150): kunde inte sökas efter att WebSearch-budgeten tagit slut; Kubecost-domänen omdirigerar till apptio.com. Behandlas som oklara i D-15/D-16.
- **Anekdoterna** "European government agencies have successfully implemented standardised Architecture as Code templates" (docs/16_migration.md:40) och "European telecommunications companies have successfully transitioned ..." (docs/16_migration.md:50) saknar källa och kan inte kontrolleras; föreslå konkreta, citerbara fall eller omformulering till "some ...".
- **Chaos-/testpyramid-attributioner**: filerna nämner varken Mike Cohn, Martin Fowler/strangler fig, Gartners 5 R eller AWS 7 R, så inga sådana påståenden fanns att verifiera (kapitel 16:s strategitabell använder egna etiketter "Lift-and-shift / Re-architecting / Lift-and-improve / Application retirement" utan attribution, vilket inte är fel men avviker från branschens rehost/replatform/refactor/retire-terminologi).
- Huruvida `pulumi stack ls --json` fortfarande fungerar som dold alias till `--output json` (D-22) kunde inte avgöras från CLI-dokumentationen; källkodsfilen kunde inte hämtas från GitHub-sökvägarna som provades.
- AXELOS nuvarande organisationsstatus (PeopleCert) kunde inte bekräftas från axelos.com (sidan är JavaScript-renderad); påverkar inte bedömningen i D-07, som gäller den obefintliga titeln.
