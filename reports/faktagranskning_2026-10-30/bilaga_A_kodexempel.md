<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Bilaga A (kodexempel, kapitel 30)

Granskad fil: `docs/30_appendix_code_examples.md` (4 267 rader, ca 12 500 ord). Granskningsdatum: 2026-10-30. Alla radnummer nedan avser denna fil om inget annat anges.

## Omfattning

**Kodblock: 33 totalt** (fördelning per språkmarkering i filen):

| Språk (fence) | Antal | Validering med verktyg | Validering genom läsning |
|---|---|---|---|
| yaml | 12 | 11 parsade med PyYAML (CloudFormation-taggar via egen loader); Kubernetes-fält, GitHub Actions-nycklar och action-versioner kontrollerade mot officiell dokumentation/README | 1 (block 02 är Groovy/Jenkinsfile felmärkt som `yaml`, parsar inte som YAML) |
| python | 5 | 5 kompilerade med `py_compile`; 4 exekverade/stubbade för att bevisa körfel (13_CODE_H, 15_CODE_3, 24_CODE_1, 17_CODE_2) | – |
| typescript | 5 | 5 typkontrollerade med `tsc 6.0.2 --strict` (endast miljöfel för saknade `vitest`/`node`-typer) | – |
| hcl (Terraform) | 4 | – (nedladdning av terraform-binär nekades av behörighetssystemet) | 4, kontrollerade mot HashiCorp-dokumentation och rå providerdokumentation (`terraform-provider-aws`, `terraform-provider-azurerm`) |
| go | 2 | 2 syntaxkontrollerade med `gofmt -e` och typkontrollerade med `go vet`/`go test -c` mot terratest v0.48.2, aws-sdk-go v1.55.7, testify v1.10.0 | – |
| rego | 2 | builtins kontrollerade mot OPA:s `builtin_metadata.json` | 2, syntax kontrollerad mot OPA v1-dokumentation (opa-binär kunde inte laddas ned) |
| json (OSCAL) | 2 | 2 parsade och schemavaliderade mot NIST:s officiella OSCAL 1.1.2 JSON-scheman (jsonschema 4.26) | – |
| structurizr | 1 | – | 1, kontrollerad mot docs.structurizr.com/dsl/language och /dsl/expressions |

Summering: 25 av 33 block har validerats med verktyg (parser/kompilator/schema), 8 enbart genom läsning mot primärkällor.

**Prosa- och faktapåståenden kontrollerade (urval, ca 25):** GDPR art. 32 och 44–49; FIPS 140-2/140-3-status (NIST CMVP); DORA-nivåer (DORA-rapporten 2024, PDF); Pod Security Admission (etikett på namespace); PodSecurityPolicy borttagen i 1.25; Bitnami-bildernas flytt till `bitnamilegacy`; EOL-datum för Kubernetes 1.29 och Node 20; aws-sdk-go v1 end-of-support; deprecation av artefakt-actions v3; Checkov-, Infracost- och Conftest-flaggor; OPA 1.0-syntaxkrav; Terraform `timeadd`-format och S3-backendens `dynamodb_table`; azurerm-providerns argument; AWS Cost Explorer `GroupBy`-gräns och `CurrentInstance`-fält; OSCAL-krav på UUID och glob-mönster; Vitest-trösklar; RDS PostgreSQL-versioner; aktuella versioner av Terraform (1.17.1), AWS-provider (6.71), azurerm (5.12), actions/checkout (v7), setup-node (v7), upload-artifact (v7), setup-terraform (v4), configure-aws-credentials (v6), dorny/test-reporter (v3).

**URL:er i filen (8):** 6 svarar 200 (developer.hashicorp.com/terraform/language, NIST-katalogen på raw.githubusercontent.com, conftest v0.46.0-releasen, infracost install.sh, ietf.org/rfc/rfc4122 → rfc-editor.org, docs.structurizr.com/dsl/language). `https://github.com/structurizr/dsl` ger 404 (repot finns inte längre). `https://static.structurizr.com/themes/default/theme.json` kunde inte nås från sessionen (värden ej tillåten i nätverkspolicyn) – ej verifierbar.

**Korsreferenser:** alla `[nn]_CODE_x`-ankare i filen jämförda med `grep` över `docs/*.md`, kapiteltitlar jämförda med `docs/book_index.json`, källförteckningen jämförd med `docs/33_references.md`. `docs/examples/structurizr/` (referensworkspace + 3 ADR:er) nämns inte alls i bilagan och är fristående från 06_CODE_5.

## Sammanfattning

Bilagan presenteras som ett "praktiskt referensbibliotek" med "complete, working code samples" (part_h_appendices.md), men en stor andel av listningarna går inte att köra i den form de står. Båda Go-listningarna kompilerar inte (oanvända importer, fel fältnamn `Filters`, icke-existerande terratest-funktion, omkastade argument). Båda Rego-listningarna misslyckas under OPA 1.x: 10_CODE_1 blandar `import rego.v1` med v0-regelhuvuden och anropar den obefintliga builtin-funktionen `math.max`; 13_CODE_J använder v0-syntax och testar en mängd med `results[0]`, vilket aldrig blir sant. Tre av fyra Terraform-listningar refererar till odeklarerade resurser, variabler eller modulargument, och 21_CODE_1 sätter ett `location`-argument som azurerm-providern inte har; 15_CODE_1 använder ett ogiltigt `timeadd`-format och det borttagna `cost_filters`. CloudFormation-mallen använder `!Contains` i `Conditions`, vilket bara är tillåtet i `Rules`. Två Python-listningar kraschar bevisat på sin egen indata (13_CODE_H mot 13_CODE_G; `generate_terraform_cost_optimizations` i 15_CODE_3), och tre listningar anropar metoder som inte finns. Structurizr-workspacet laddas inte (fyra relationer i den dynamiska vyn saknas i modellen; `thickness` är inte en elementstil). OSCAL-komponentdefinitionen ger 25 schemafel mot NIST:s officiella schema och SSP-generatorn producerar en struktur som inte är OSCAL-giltig. Säkerhetsmässigt allvarligast är att flera "compliance-grindar" tyst inte kontrollerar något: Jenkins-pipelinens Conftest-steg kör `verify` i stället för `test` och utvärderar aldrig paketet `a.tagging`; Kubernetes-testsviten letar PSA-etiketter på poddar i stället för namespaces och använder en påhittad PV-annotation; `kubectl get resourcequota -A ||` kan aldrig falera. Därtill är många versioner föråldrade (artefakt-actions v3 slutade fungera 2025-01-30; aws-sdk-go v1 end-of-support 2025-07-31; FIPS 140-2 på Historical List sedan 2026-09-21; Node 20 och Kubernetes 1.29 EOL). Korsreferenserna är ofullständiga: fem listningar refereras inte från de kapitel de hävdar, två navigationslänkar pekar på sektioner som inte finns och källans Structurizr-URL är död.

## Fynd

### K-01 10_CODE_1 blandar `import rego.v1` med Rego v0-syntax – modulen parsar inte
- **Fil:rad:** docs/30_appendix_code_examples.md:3289, 3305, 3313, 3322, 3327, 3365, 3404, 3465 (m.fl.)
- **Påstående/kod:** `import rego.v1` följt av `encryption_compliant[resource] {`, `get_encryption_status(resource) := result {`, `network_security_violations[violation] {`, `compliance_assessment := result {`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA:s uppgraderingsguide: "OPA v1.0 requires the usage of `if` and `contains` keywords when declaring rules"; `rego.v1`-importen aktiverar samma krav i äldre versioner. Regler med kropp utan `if` och partiella mängdregler utan `contains` listas som kompileringsfel (https://www.openpolicyagent.org/docs/v0-upgrade). Kapitel 10:s eget utdrag (docs/10_policy_and_security.md:52–62) har samma fel.
- **Förslag:** `encryption_compliant contains resource if { ... }`, `get_encryption_status(resource) := result if { ... }`, `network_security_violations contains violation if { ... }`, `compliance_assessment := result if { ... }`, `data_sovereignty_compliant contains resource if { ... }`, `calculate_score(violations) := score if { ... }`. Kör `opa check --strict` på listningen före tryck.

### K-02 10_CODE_1 anropar obefintlig builtin `math.max`
- **Fil:rad:** docs/30_appendix_code_examples.md:3509
- **Påstående/kod:** `score := math.max(0, 100 - sum(penalties))`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA:s builtin-register (`builtin_metadata.json`, main) innehåller `max`, `min`, `sum`, `count`, `array.concat`, `substring`, `sprintf`, `contains`, `lower` – men inget `math.max` (`jq 'has("math.max")'` → `false`). `max` tar en kollektion: "Returns the maximum value in a collection." Kompilering ger "undefined function math.max".
- **Förslag:** `score := max([0, 100 - sum(penalties)])`

### K-03 10_CODE_1 har catch-all-funktioner som ger konfliktfel vid körning
- **Fil:rad:** docs/30_appendix_code_examples.md:3357, 3432, 3440–3448, 3454
- **Påstående/kod:** `validate_key_management(_) := {"approved": false, ...}` jämte `validate_key_management("customer_managed") := {...}`; `determine_classification(_) := "internal"` jämte tre specifika definitioner; `validate_region(resource, _) := {"compliant": true, ...}` jämte `validate_region(resource, "personal")`; `get_resource_region(_) := "unknown"` jämte definitioner som returnerar regionen
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OPA Policy Language: "If a call matches multiple functions, they must produce the same output, or else a conflict error will occur." För en resurs med `tags.DataClassification = "personal"` matchar både den specifika definitionen ("personal") och catch-all ("internal") → `eval_conflict_error: functions must not produce multiple outputs for same inputs`. Samma sak för varje resurs med `kms_key_type = "customer_managed"` och för varje `validate_region(resource, "personal")`. Standardvärden för funktioner uttrycks med `default` ("the `default` keyword can be applied to functions as well"). (https://www.openpolicyagent.org/docs/policy-language)
- **Förslag:** `default determine_classification(_) := "internal"`, `default get_resource_region(_) := "unknown"`, `default validate_key_management(_) := {"approved": false, "strength": "low", "recommendations": [...]}`, och skriv `validate_region` som en funktion med `if classification == "personal"` respektive `default`.

### K-04 13_CODE_J: v0-syntax som avvisas av OPA 1.x och tester som aldrig kan passera
- **Fil:rad:** docs/30_appendix_code_examples.md:1628–1691 (särskilt 1630, 1636, 1644, 1663, 1677, 1690)
- **Påstående/kod:** `deny[msg] {`, `test_enforces_bucket_encryption {`, `results[0] == "Bucket audit-logs must enable server-side encryption"`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** (1) 13_CODE_L kör `opa test policies/infrastructure -v` (rad 1794) – i OPA ≥ 1.0 är Rego v1 standard och v0-syntax ger kompileringsfel om inte `--v0-compatible` anges (`opa test --v0-compatible`: "Opt-in to OPA features and behaviors prior to the OPA v1.0 release", https://www.openpolicyagent.org/docs/cli). (2) `deny` är en mängd (set). `results[0]` på en mängd är ett medlemskapstest för värdet `0`, inte indexering; uttrycket blir odefinierat och alla tre tester misslyckas även under OPA v0. Mängder indexeras inte positionellt i Rego.
- **Förslag:** Policyn: `package infrastructure.security` + `import rego.v1`, `deny contains msg if { ... }`. Testerna: `test_enforces_bucket_encryption if { results := data.infrastructure.security.deny with input as {...}; "Bucket audit-logs must enable server-side encryption" in results }`. Lägg även testfilen i paketet `infrastructure.security_test`.

### K-05 05_CODE_3 (Terratest) kompilerar inte
- **Fil:rad:** docs/30_appendix_code_examples.md:433, 444, 546
- **Påstående/kod:** `"encoding/json"` och `"github.com/gruntwork-io/terratest/modules/test-structure"` importeras men används inte; `&ec2.DescribeFlowLogsInput{ Filters: []*ec2.Filter{ ... } }`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** `go test -c` mot terratest v0.48.2/aws-sdk-go v1.55.7: `./a_vpc_test.go:7:5: "encoding/json" imported and not used`, `:18:5: ".../modules/test-structure" imported as test_structure and not used`, `:120:9: unknown field Filters in struct literal of type ec2.DescribeFlowLogsInput`. I aws-sdk-go v1 (`service/ec2/api.go`) heter fältet `Filter []*Filter` (EC2-API-parametern `Filter.N`). `DescribeTagsInput` (rad 650) har däremot korrekt `Filters`.
- **Förslag:** Ta bort de två oanvända importerna och ändra rad 546 till `Filter: []*ec2.Filter{`.

### K-06 13_CODE_I använder en funktion som inte finns i Terratest och kastar om argument
- **Fil:rad:** docs/30_appendix_code_examples.md:1609, 1612
- **Påstående/kod:** `encryption := aws.GetS3BucketEncryption(t, "eu-west-1", bucketID)`; `tags := aws.GetTagsForVpc(t, "eu-west-1", vpcID)`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** `go test -c`: `undefined: aws.GetS3BucketEncryption`. Terratest `modules/aws/s3.go` (v0.48.2) exporterar `GetS3BucketVersioning`, `GetS3BucketPolicy`, `GetS3BucketLoggingTarget`, `GetS3BucketTags`, `GetS3BucketOwnershipControls` m.fl. men ingen krypteringsfunktion. `modules/aws/vpc.go:212`: `func GetTagsForVpc(t testing.TestingT, vpcID string, region string)` – bokens anrop skickar regionen som VPC-id och VPC-id som region; det kompilerar (båda är strängar) men misslyckas vid körning.
- **Förslag:** `tags := aws.GetTagsForVpc(t, vpcID, "eu-west-1")`. För kryptering: skapa klient med `aws.NewS3Client(t, "eu-west-1")` och anropa `GetBucketEncryption` direkt, eller verifiera via Terraform-output (`logging_bucket_sse_algorithm`).

### K-07 07_CODE_1 använder `!Contains` i `Conditions` – ogiltigt i CloudFormation
- **Fil:rad:** docs/30_appendix_code_examples.md:782–783
- **Påstående/kod:** `RequiresGDPR: !Contains [!Ref ComplianceRequirements, gdpr]`, `RequiresISO27001: !Contains [!Ref ComplianceRequirements, iso27001]`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** AWS-dokumentationen för villkorsfunktioner listar endast `Fn::And`, `Fn::Equals`, `Fn::If`, `Fn::Not`, `Fn::Or` (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html). `Fn::Contains` är en "rule-specific function" – "functions that can only be used in the `Rules` section of a template" (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/rules-section-structure.html). Mallen avvisas vid `validate-template`.
- **Förslag:** Ersätt listparametern med två `String`-parametrar (`RequireGDPR`/`RequireISO27001`, `AllowedValues: [true, false]`) och `!Equals [!Ref RequireGDPR, "true"]`, eller flytta kontrollen till en `Rules`-sektion med `Fn::Contains`.

### K-08 21_CODE_1 sätter `location` på azurerm-providern – argumentet finns inte
- **Fil:rad:** docs/30_appendix_code_examples.md:715–718
- **Påstående/kod:** `provider "azurerm" { features {} location = var.azure_eu_region }`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Providerns argumentreferens (`terraform-provider-azurerm/website/docs/index.html.markdown`, main) listar `features`, `subscription_id`, `client_id`, `tenant_id`, `environment`, `use_oidc`, `use_msi`, `use_cli`, `storage_use_azuread`, `resource_provider_registrations` m.fl. – inget `location`. `terraform init/validate` ger "Unsupported argument". Region anges per resurs (`location = ...` på t.ex. `azurerm_resource_group`).
- **Förslag:** Ta bort raden och skicka `var.azure_eu_region` till modulen `./modules/azure` som variabel.

### K-09 15_CODE_3: tre `GroupBy`-dimensioner mot Cost Explorer – max två tillåts
- **Fil:rad:** docs/30_appendix_code_examples.md:3085–3089
- **Påstående/kod:** `GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}, {'Type': 'TAG', 'Key': 'Project'}, {'Type': 'DIMENSION', 'Key': 'REGION'}]`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** API-referensen för `GetCostAndUsage`: "You can group AWS costs using up to two different groups, either dimensions, tag keys, cost categories, product attributes, or any two group by types." (https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html). Anropet ger `ValidationException`.
- **Förslag:** Behåll två grupperingar (t.ex. `SERVICE` + `TAG Project`) och filtrera på region via `Filter` (som redan görs), eller gör två anrop.

### K-10 15_CODE_3: `generate_terraform_cost_optimizations` kraschar på sin egen formatsträng
- **Fil:rad:** docs/30_appendix_code_examples.md:3250–3275 (särskilt 3255)
- **Påstående/kod:** `"""...resource "aws_launch_template" "spot_optimized" {{ ... instance_market_options { market_type = "spot" spot_options {{ ...""".format(...)`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Raden `instance_market_options {` har en oescapad `{` i en `str.format`-mall. Körning med ett minimalt `cost_plan` där `spot_instances` är satt: `ValueError: unexpected '{' in field name` (reproducerat lokalt). Funktionen kan alltså aldrig generera spot-konfigurationen den beskriver.
- **Förslag:** Skriv `instance_market_options {{` (och kontrollera alla klammerpar), eller använd en template-motor (Jinja2) i stället för `str.format` för HCL.

### K-11 13_CODE_H kraschar på katalogen i 13_CODE_G
- **Fil:rad:** docs/30_appendix_code_examples.md:1522–1528, 1539 (och 1470, 1481, 1494)
- **Påstående/kod:** `class Requirement: id, title, classification, priority, tests` … `requirements = [Requirement(**item) for item in data['requirements']]`; katalogen innehåller nyckeln `rationale`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Körning av `load_validator('catalogue.yaml')` med bokens katalog: `TypeError: Requirement.__init__() got an unexpected keyword argument 'rationale'` (reproducerat lokalt). Kapitel 13 (rad 301–311) hänvisar till paret som ett komplett ramverk.
- **Förslag:** Lägg till `rationale: str = ""` i dataklassen, eller filtrera: `Requirement(**{k: v for k, v in item.items() if k in Requirement.__dataclass_fields__})`.

### K-12 14_CODE_1 refererar till resurser som inte deklareras i modulen
- **Fil:rad:** docs/30_appendix_code_examples.md:2514, 2529, 2544, 2553
- **Påstående/kod:** `data.aws_availability_zones.available.names`, `aws_security_group.alb.id`, `aws_lb_target_group.main.arn`, `aws_launch_template.main.id`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Ingen av dessa fyra (datakälla, säkerhetsgrupp, target group, launch template) definieras i listningen, som enligt prosan (rad 2468, 2478 och docs/14_practical_implementation.md:87) är den "complete infrastructure example". `terraform validate` ger "Reference to undeclared resource" för varje referens. (Terraform-binären kunde inte laddas ned i sessionen; bedömningen bygger på Terraforms deklarationsregler, inte på körning.)
- **Förslag:** Lägg till `data "aws_availability_zones" "available" { state = "available" }`, `resource "aws_security_group" "alb"`, `resource "aws_lb_target_group" "main"` och `resource "aws_launch_template" "main"`, eller markera listningen uttryckligen som ett utdrag.

### K-13 14_CODE_2 skickar odeklarerade modulargument och läser en output som inte finns
- **Fil:rad:** docs/30_appendix_code_examples.md:2629–2631, 2649
- **Påstående/kod:** `enable_monitoring = true`, `backup_retention = 30`, `multi_az = true`; `module.web_application.load_balancer_arn_suffix`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Modulen i 14_CODE_1 deklarerar endast `environment`, `application_name`, `instance_count` och outputs `load_balancer_dns`, `vpc_id`. Terraform avbryter med "Unsupported argument" respektive "Unsupported attribute". Listningen beskrivs som att den "layers production-specific settings on top of the shared module".
- **Förslag:** Deklarera variablerna i modulen (eller ta bort dem) och lägg till `output "load_balancer_arn_suffix" { value = aws_lb.main.arn_suffix }`.

### K-14 15_CODE_1: ogiltigt `timeadd`-format, borttaget `cost_filters` och odeklarerade variabler
- **Fil:rad:** docs/30_appendix_code_examples.md:2817, 2830–2835, 2857 samt 2812–2816, 2823, 2862, 2900–2904
- **Påstående/kod:** `formatdate("YYYY-MM-DD", timeadd(timestamp(), "30*24h"))`; `cost_filters = { Tag = { Project = [var.project_name] } Region = [var.aws_region] }`; `data.aws_ami.amazon_linux.id`; `var.cost_centre`, `var.monthly_budget_limit_usd` m.fl.
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** `timeadd` tar "sequences of number and unit pairs, such as "1.5h" or "1h30m"" med enheterna ns/us/ms/s/m/h – ingen aritmetik, inget `d` (https://developer.hashicorp.com/terraform/language/functions/timeadd); `"30*24h"` ger fel vid plan. `aws_budgets_budget` dokumenterar i dag endast `cost_filter`-block och `filter_expression` (`website/docs/r/budgets_budget.html.markdown`, main); det tidigare `cost_filters` var deprecated och typat som `map(string)`, så nästlade mappar/listor är typfel även i v5. Datakällan `aws_ami.amazon_linux` och 13 `var.*` saknar deklaration. `timestamp()` i taggar ger dessutom en ny plan-diff vid varje körning.
- **Förslag:** `timeadd(timestamp(), "720h")` (eller sätt datumet i en variabel); `cost_filter { name = "TagKeyValue" values = ["user:Project$${var.project_name}"] }` och `cost_filter { name = "Region" values = [var.aws_region] }`; deklarera datakällan och variablerna.

### K-15 14_CODE_3 använder artefakt-actions v3 som slutade fungera 2025-01-30
- **Fil:rad:** docs/30_appendix_code_examples.md:2725, 2760
- **Påstående/kod:** `uses: actions/upload-artifact@v3`, `uses: actions/download-artifact@v3`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Hög
- **Evidens:** GitHub Changelog 2024-04-16: "Starting January 30th, 2025, GitHub Actions customers will no longer be able to use v3 of actions/upload-artifact or actions/download-artifact … attempting to use a version of the actions after the deprecation date will result in a workflow failure." (https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/). Aktuell major är v7 (README, main).
- **Förslag:** `actions/upload-artifact@v4` / `actions/download-artifact@v4` (eller aktuell v7) och notera att artefaktnamn i v4 måste vara unika per jobb.

### K-16 13_CODE_K testar inte det som påstås (PSA på poddar, påhittad PV-annotation, kvotkontroll som aldrig faller)
- **Fil:rad:** docs/30_appendix_code_examples.md:1712–1714, 1717–1718, 1723–1724 (och prosan 1698)
- **Påstående/kod:** `kubectl get resourcequota -A || { ... exit 1; }`; `kubectl get pods -A -o json | jq '.items[].metadata.labels["pod-security.kubernetes.io/enforce"]'`; `jq '.items[].metadata.annotations["encryption.alpha.kubernetes.io/encrypted"]'`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** (1) `kubectl get resourcequota -A` returnerar exit 0 även när inga kvoter finns ("No resources found"), så `||`-grenen körs aldrig. (2) PSA-etiketterna sätts på namespace-objekt: "you can configure namespaces to define the admission control mode" och referensen anger `pod-security.kubernetes.io/enforce` – "Used on: Namespace" (https://kubernetes.io/docs/concepts/security/pod-security-admission/, https://kubernetes.io/docs/reference/labels-annotations-taints/). Poddar bär inte etiketten, så `grep -q baseline` misslyckas alltid. (3) `encryption.alpha.kubernetes.io/encrypted` finns inte i Kubernetes officiella förteckning över kända etiketter/annotationer; kryptering styrs av CSI-driverns StorageClass-parametrar (t.ex. EBS `encrypted: "true"`). Prosan talar dessutom om "pod security policies", trots att kapitel 13 själv (rad 344) påpekar att PSP togs bort i 1.25.
- **Förslag:** `test "$(kubectl get resourcequota -A --no-headers 2>/dev/null | wc -l)" -gt 0`; `kubectl get ns -o json | jq -e '[.items[] | select(.metadata.labels["pod-security.kubernetes.io/enforce"] == null)] | length == 0'`; kontrollera kryptering via `kubectl get sc -o json | jq '.items[].parameters.encrypted'` eller via leverantörens API. Byt "pod security policies" till "Pod Security Admission levels".

### K-17 10_CODE_3 är inte en giltig OSCAL-komponentdefinition (25 schemafel)
- **Fil:rad:** docs/30_appendix_code_examples.md:3620–3731 (bl.a. 3622, 3632, 3637–3650, 3647)
- **Påstående/kod:** `"uuid": "11223344-5566-7788-99aa-bbccddeeff00"`, `"uuid": "comp-aws-rds-mysql"`, `control-implementations` utan `uuid`/`description`, `implemented-requirements` och `statements` utan `uuid`, `"implementation-status"` i `statements`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Validering mot NIST:s `oscal_component_schema.json` v1.1.2 (release-artefakt) ger 25 fel: `'uuid' is a required property` för alla `control-implementations`, `implemented-requirements` och `statements`; `'description' is a required property` för `control-implementations`; `Additional properties are not allowed ('implementation-status' was unexpected)` på `statements`; UUID-mönstret `^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$` uppfylls inte av `11223344-5566-7788-…` (tredje gruppen börjar på 7) eller av `comp-aws-*`. Schemats `required`: control-implementation `['uuid','source','description','implemented-requirements']`, implemented-requirement `['uuid','control-id','description']`, statement `['statement-id','uuid','description']`.
- **Förslag:** Ge varje objekt ett RFC 4122 v4-UUID, lägg till `description` på `control-implementations`, flytta `implementation-status` till `implemented-requirements`-nivån (där det är tillåtet) och validera med `oscal-cli validate` före tryck.

### K-18 10_CODE_4 producerar inte en "OSCAL-compliant" SSP
- **Fil:rad:** docs/30_appendix_code_examples.md:3773–3806, 3836–3848 (särskilt 3777, 3788–3796, 3801, 3847)
- **Påstående/kod:** `"uuid": self._uuid()` → `"ssp-%Y%m%d%H%M%S"`; `"identifier-type": "https://ietf.org/rfc/rfc4122", "id": self._account_id()`; `"control-implementation": {"implemented-requirements": implementations}` där `implementations` är komponentdefinitionens `control-implementations`-objekt
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OSCAL SSP-schemat 1.1.2 kräver på toppnivå `['uuid','metadata','import-profile','system-characteristics','system-implementation','control-implementation']` (saknar `system-implementation`), i `system-characteristics` `['system-ids','system-name','description','system-information','status','authorization-boundary']` (tre saknas), i `control-implementation` `['description','implemented-requirements']` (saknar `description`) och per `implemented-requirement` `['uuid','control-id']` – men listan fylls med objekt av typen `{"source": ..., "implemented-requirements": [...]}` från komponentdefinitionen, dvs. fel modellnivå. `ssp-20260101…` är inget UUID, och ett 12-siffrigt AWS-konto-id är inte ett RFC 4122-id. Prosan (rad 3736) hävdar att skriptet "produces a machine-readable OSCAL SSP" som uppdaterar "compliance evidence".
- **Förslag:** Använd `uuid.uuid4()`, bygg `implemented-requirements` genom att platta ut komponenternas `implemented-requirements` (med `uuid`, `control-id`, `by-components`), lägg till obligatoriska `system-implementation`, `system-information`, `status`, `authorization-boundary` och `control-implementation.description`, och validera resultatet i CI.

### K-19 06_CODE_5 (Structurizr) laddas inte: relationer saknas i modellen och `thickness` är ingen elementstil
- **Fil:rad:** docs/30_appendix_code_examples.md:4157, 4158, 4161, 4162, 4241
- **Påstående/kod:** Dynamisk vy: `messageBus -> paymentService "8. OrderCreated event"`, `paymentService -> paymentProvider "9. Charge customer"`, `notificationService -> emailService "12. Send confirmation"`, `emailService -> customer "13. Confirmation email"`; stil: `element "Critical Path" { border solid thickness 4 }`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Modellen (rad 4042–4071) definierar inga av dessa fyra relationer (endast `paymentService -> messageBus`, `ecommercePlatform -> paymentProvider`, `ecommercePlatform -> emailService`); dynamiska vyer visar "instances of relationships that are defined in the static model" och DSL-tolken avbryter med "A relationship between … does not exist in model". Elementstilens tillåtna egenskaper är `shape, icon, width, height, background, color/colour, stroke, strokeWidth, fontSize, border, opacity, metadata, description` – `thickness` finns endast för `relationship` (https://docs.structurizr.com/dsl/language). Workspacet kan därför inte parsas med structurizr-cli.
- **Förslag:** Lägg till `messageBus -> paymentService "OrderCreated event" "AMQP"`, `paymentService -> paymentProvider "Charges cards" "HTTPS/REST"`, `notificationService -> emailService "Sends emails" "HTTPS/REST"`, `emailService -> customer "Delivers email"` i modellen; byt `thickness 4` mot `strokeWidth 4`.

### K-20 05_CODE_2: Conftest-steget utvärderar aldrig policyn (fel underkommando, fel namespace, v0-syntax)
- **Fil:rad:** docs/30_appendix_code_examples.md:305–333 (särskilt 306, 312, 319, 331)
- **Påstående/kod:** `package a.tagging` … `deny[msg] {` … `find infrastructure/ -name "*.tf" -exec conftest verify --policy policies/ {} \;`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** conftest.dev: `conftest test` "evaluates policies against input files", medan `conftest verify` "runs Rego unit tests (`*_test.rego`)" – kommandot testar alltså aldrig .tf-filerna. Standardnamespace är `main` (`--namespace` default `["main"]`, `internal/commands/test.go`), så regler i `a.tagging` ignoreras utan `--namespace a.tagging`/`--all-namespaces`. Aktuell Conftest har `--rego-version` med default `v1` ("Which version of Rego syntax to use. Options: v0, v1"), så `deny[msg] {` avvisas (fungerar med den fastnålade v0.46.0, men läsaren får ingen varning). Steget loggar ändå "# Pass: Policy validation completed" – en säkerhetsgrind som tyst släpper igenom allt.
- **Förslag:** `conftest test --policy policies/ --namespace a.tagging --parser hcl2 infrastructure/` med regler skrivna som `deny contains msg if { ... }` (`import rego.v1`), och låt kommandots exit-kod styra stegets resultat.

### K-21 05_CODE_2: Checkov-flaggan `--output-file` finns inte
- **Fil:rad:** docs/30_appendix_code_examples.md:268–274
- **Påstående/kod:** `checkov -d infrastructure/ --framework terraform --output json --output-file checkov-results.json --soft-fail`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Checkovs CLI-referens har `-o/--output` ("Report output format") och `--output-file-path OUTPUT_FILE_PATH` ("Name of the output folder to save the chosen output formats") – ingen `--output-file` (https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html). Kommandot avbryts med argumentfel innan `readJSON` körs.
- **Förslag:** `checkov -d infrastructure/ --framework terraform -o json --output-file-path results/ --soft-fail` och läs `results/results_json.json`.

### K-22 05_CODE_2: Groovy-sträng med enkla citattecken interpoleras inte
- **Fil:rad:** docs/30_appendix_code_examples.md:250
- **Påstående/kod:** `dir('infrastructure/environments/${params.ENVIRONMENT}') {`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** I Groovy interpoleras `${...}` endast i dubbelciterade/GString-strängar; enkla citattecken ger den bokstavliga katalogen `infrastructure/environments/${params.ENVIRONMENT}` och `terraform init` misslyckas.
- **Förslag:** `dir("infrastructure/environments/${params.ENVIRONMENT}") {`

### K-23 05_CODE_2: `infracost breakdown --currency EUR` – flaggan finns inte på `breakdown`
- **Fil:rad:** docs/30_appendix_code_examples.md:353–357
- **Påstående/kod:** `infracost breakdown --path . --currency EUR --format json --out-file ../../../cost-estimate.json`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** I Infracost v0.10.x (`cmd/infracost/run.go` + `breakdown.go`, tag v0.10.41) definieras flaggorna `path, format, out-file, fields, show-skipped, usage-file, terraform-var(-file), compare-to, …` – ingen `currency`; valutan styrs av konfigurationen/`INFRACOST_CURRENCY` (`internal/config/config.go`: `Currency string envconfig:"CURRENCY"`). I Infracost 2.x har `breakdown` ersatts av `scan`/`price`, där `--currency` finns ("Override the display currency (ISO 4217 code)", https://www.infracost.io/docs/features/cli_commands/); miljövariabeln heter numera `INFRACOST_CLI_CURRENCY`. Kommandot som står i boken avbryts med "unknown flag".
- **Förslag:** `infracost configure set currency EUR` (eller `export INFRACOST_CURRENCY=EUR`) följt av `infracost breakdown --path . --format json --out-file …`; alternativt uppdatera till 2.x-syntaxen `infracost scan --path . --currency EUR --format json`.

### K-24 `aws_rds_instance` är inte en Terraform-resurstyp – policyerna matchar aldrig riktiga planer
- **Fil:rad:** docs/30_appendix_code_examples.md:1376, 1645, 1684, 3293, 3323, 3407, 3426
- **Påstående/kod:** `type: 'aws_rds_instance'` (13_CODE_E), `input.resource.type == "aws_rds_instance"` (13_CODE_J), `"aws_rds_instance"` i `encryption_required_services` och `determine_classification` (10_CODE_1)
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** AWS-providern har `aws_db_instance` (`website/docs/r/db_instance.html.markdown` → HTTP 200) och `aws_rds_cluster`; `r/rds_instance.html.markdown` finns inte (HTTP 404). 13_CODE_B använder korrekt `aws_db_instance`. En policy som letar efter `aws_rds_instance` ger falsk trygghet mot verkliga planer.
- **Förslag:** Byt till `aws_db_instance` (och komplettera med `aws_rds_cluster`/`aws_rds_cluster_instance`) på samtliga sju ställen.

### K-25 13_CODE_F: `setup-node` med `cache: 'pnpm'` innan pnpm finns
- **Fil:rad:** docs/30_appendix_code_examples.md:1425–1435
- **Påstående/kod:** `uses: actions/setup-node@v4 with: node-version: 20, cache: 'pnpm'` följt av `run: corepack enable && pnpm install --frozen-lockfile`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** setup-node:s cache-steg kör `pnpm store path` under själva setup-steget; pnpm aktiveras först i nästa steg. Den dokumenterade ordningen är `pnpm/action-setup` → `actions/setup-node` med `cache: 'pnpm'` → `pnpm install` (https://github.com/actions/setup-node/blob/main/docs/advanced-usage.md, avsnittet "Caching pnpm (v6.10+) dependencies").
- **Förslag:** Lägg in `- uses: pnpm/action-setup@v4 with: version: 9` före `setup-node`, och ta bort `corepack enable`.

### K-26 13_CODE_F: `dorny/test-reporter` har ingen `vitest`-reporter och matas med en coverage-fil
- **Fil:rad:** docs/30_appendix_code_examples.md:1448–1452
- **Påstående/kod:** `uses: dorny/test-reporter@v1 with: name: Vitest, path: coverage/coverage-final.json, reporter: vitest`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** README listar reporters `dart-json, dotnet-nunit, dotnet-trx, flutter-json, golang-json, java-junit, jest-junit, mocha-json, phpunit-junit, python-xunit, rspec-json, swift-xunit, unreal-json` – inget `vitest`; `path` ska peka på testresultat ("Comma-separated list of paths to test results"), inte Istanbul-coverage. Aktuell major är v3 (https://github.com/dorny/test-reporter). Kapitel 13 (rad 163) lovar också "PR comments", vilket workflowen inte gör.
- **Förslag:** `pnpm vitest run --coverage --reporter=default --reporter=junit --outputFile=reports/junit.xml` och `dorny/test-reporter@v3 with: path: reports/junit.xml, reporter: java-junit`.

### K-27 15_CODE_3 läser fältet `UtilizationMetrics` som inte finns i Cost Explorer-svaret
- **Fil:rad:** docs/30_appendix_code_examples.md:3126
- **Påstående/kod:** `'utilisation': recommendation['CurrentInstance']['UtilizationMetrics']`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Datatypen `CurrentInstance` har fälten `CurrencyCode, InstanceName, MonthlyCost, OnDemandHoursInLookbackPeriod, ReservationCoveredHoursInLookbackPeriod, ResourceDetails, ResourceId, ResourceUtilization, SavingsPlansCoveredHoursInLookbackPeriod, Tags, TotalRunningHoursInLookbackPeriod` (https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CurrentInstance.html). Första "Modify"-rekommendationen ger `KeyError`.
- **Förslag:** `recommendation['CurrentInstance'].get('ResourceUtilization', {})` och regionen från `ResourceDetails.EC2ResourceDetails.Region`.

### K-28 Tre listningar anropar metoder som aldrig definieras
- **Fil:rad:** docs/30_appendix_code_examples.md:3098, 3140–3143, 3159–3160 (15_CODE_3); 860–865 (24_CODE_1); 2149, 2174–2175, 2184–2185 (17_CODE_2)
- **Påstående/kod:** `self._process_cost_data(...)`, `_find_unused_elastic_ips`, `_find_idle_load_balancers`, `_find_stopped_instances`, `_get_current_monthly_cost`, `_analyze_reserved_instance_opportunities`, `_analyze_spot_instance_opportunities`; `_test_encryption_in_transit`, `_test_vpc_flow_logs`, `_test_security_groups`, `_test_iam_policies`, `_test_s3_bucket_policies`, `_test_rds_security`; `_recommend_next_module`, `_calculate_competency_score`, `_identify_development_needs`, `_identify_team_skill_gaps`, `_recommend_team_training`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** Reflektion över de importerade klasserna: 7 + 6 + 5 anropade metoder saknas (`hasattr` → False). `test_infrastructure_security()`, `analyze_cost_trends()`, `generate_cost_optimization_plan()`, `track_progress()` och `generate_team_competency_matrix()` kastar `AttributeError`. Prosan kallar listningarna "Comprehensive test framework" respektive "complete Python implementation" (docs/15_cost_optimization.md:116).
- **Förslag:** Implementera metoderna eller markera dem tydligt som stubbar (`raise NotImplementedError`) och skriv i prosan att listningarna är skelett.

### K-29 10_CODE_2: glob-mönstret `ac-.*` väljer inga kontroller
- **Fil:rad:** docs/30_appendix_code_examples.md:3545–3549
- **Påstående/kod:** `"include-controls": [ { "matching": [ { "pattern": "ac-.*" }, { "pattern": "au-.*" }, { "pattern": "sc-.*" } ] } ]`
- **Bedömning:** FEL
- **Allvarlighet:** Hög
- **Evidens:** OSCAL-profilschemat 1.1.2 beskriver `matching.pattern` som "A glob expression matching the IDs of one or more controls to be selected." I glob-syntax är `.` ett bokstavligt tecken, så `ac-.*` kräver `ac-.` som prefix och matchar varken `ac-1` eller `ac-2.1`; profilen importerar därmed noll NIST-kontroller. (Regex-liknande mönster är ett vanligt missförstånd.)
- **Förslag:** `"pattern": "ac-*"`, `"au-*"`, `"sc-*"`.

### K-30 10_CODE_2: profilens UUID är inte ett giltigt OSCAL-UUID
- **Fil:rad:** docs/30_appendix_code_examples.md:3531
- **Påstående/kod:** `"uuid": "87654321-4321-8765-4321-876543218765"`
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** Schemavalidering mot `oscal_profile_schema.json` 1.1.2 ger exakt ett fel: värdet matchar inte `^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$` (tredje gruppen måste börja på 4 eller 5, fjärde på 8/9/A/B). Resten av profilstrukturen (`imports`, `merge.combine.method: merge`, `modify.set-parameters`, `alters/adds position after by-id`) är schemagiltig.
- **Förslag:** Generera ett v4-UUID, t.ex. `"uuid": "3f2d7c2e-5a1b-4c8e-9f0a-1b2c3d4e5f60"`.

### K-31 10_CODE_2 hänvisar till "FIPS 140-2 validated encryption modules"
- **Fil:rad:** docs/30_appendix_code_examples.md:3587
- **Påstående/kod:** `"prose": "Payment service providers must use FIPS 140-2 validated encryption modules and review key material every 90 days."`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** NIST CMVP: FIPS 140-2-inlämningar accepteras inte sedan 2022-04-01, "FIPS 140-3 validations are currently being accepted", och "After this date [September 21, 2026], FIPS 140-2 validation certificates will be moved to the Historical List" (https://csrc.nist.gov/projects/cryptographic-module-validation-program). Vid granskningsdatumet är alla 140-2-certifikat historiska.
- **Förslag:** "FIPS 140-3 validated cryptographic modules".

### K-32 14_CODE_2 använder DynamoDB-låsning som är deprecated i S3-backenden
- **Fil:rad:** docs/30_appendix_code_examples.md:2592–2598
- **Påstående/kod:** `backend "s3" { … encrypt = true dynamodb_table = "terraform-state-lock" }`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** "DynamoDB-based locking is deprecated and will be removed in a future minor version"; `dynamodb_table` är markerat "(Optional, Deprecated)"; S3-nativ låsning aktiveras med `use_lockfile` (https://developer.hashicorp.com/terraform/language/backend/s3). Boken citerar själv denna sida som Source [17] i docs/33_references.md.
- **Förslag:** Ersätt `dynamodb_table = …` med `use_lockfile = true` (Terraform ≥ 1.10).

### K-33 14_CODE_3: föråldrade action-versioner och Terraform-pin
- **Fil:rad:** docs/30_appendix_code_examples.md:2683, 2696, 2699, 2704, 2745, 2748, 2753
- **Påstående/kod:** `TF_VERSION: 1.5.0`, `actions/checkout@v3`, `hashicorp/setup-terraform@v2`, `aws-actions/configure-aws-credentials@v2`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Aktuella majorversioner enligt respektive README (main): `actions/checkout@v7`, `hashicorp/setup-terraform@v4`, `aws-actions/configure-aws-credentials@v6`. v3/v2-versionerna är Node 16-actions som GitHub sedan 2024-06-03 tvingar att köra på Node 20 (https://github.blog/changelog/2024-03-07-github-actions-all-actions-will-run-on-node20-instead-of-node16-by-default/). Senaste Terraform är 1.17.1 (releases.hashicorp.com); 05_CODE_1/05_CODE_2 pinnar 1.6.0 – inkonsekvent inom bilagan.
- **Förslag:** `actions/checkout@v4` (eller nyare), `hashicorp/setup-terraform@v3`+, `aws-actions/configure-aws-credentials@v4`+ och en gemensam `TF_VERSION` (t.ex. `1.9.x` eller senare) i hela bilagan.

### K-34 14_CODE_3 autentiserar mot AWS med långlivade nycklar i stället för OIDC
- **Fil:rad:** docs/30_appendix_code_examples.md:2703–2708, 2752–2757
- **Påstående/kod:** `aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}`, `aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Actionens README inleder med "Quick Start (OIDC, recommended)" och beskriver IAM Identity Provider för GitHub OIDC (https://github.com/aws-actions/configure-aws-credentials). Boken argumenterar i kapitel 9/9B för kortlivade identiteter; exemplet motsäger det utan kommentar.
- **Förslag:** `permissions: id-token: write, contents: read` och `with: role-to-assume: arn:aws:iam::<account>:role/github-deploy, aws-region: ${{ env.AWS_REGION }}`.

### K-35 05_CODE_3 bygger på AWS SDK for Go v1, som nått end-of-support
- **Fil:rad:** docs/30_appendix_code_examples.md:436–439
- **Påstående/kod:** `"github.com/aws/aws-sdk-go/aws"`, `".../aws/session"`, `".../service/ec2"`, `".../service/cloudtrail"`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** AWS: SDK:n "will enter maintenance mode on July 31, 2024 and reach end-of-support on July 31, 2025 … We recommend that you migrate to AWS SDK for Go v2" (https://aws.amazon.com/blogs/developer/announcing-end-of-support-for-aws-sdk-for-go-v1-on-july-31-2025/). Terratest ≥ 0.47 använder SDK v2 (`modules/aws` importerar `aws-sdk-go-v2`), så exemplet blandar två SDK-generationer.
- **Förslag:** Använd `terratest/modules/aws` (`aws.NewEc2Client`, `aws.GetVpcById`) eller SDK v2 (`ec2.NewFromConfig`).

### K-36 05_CODE_3: regionkontrollen är tautologisk och "encryption at rest" kontrolleras inte
- **Fil:rad:** docs/30_appendix_code_examples.md:569–578, 594–606
- **Påstående/kod:** `region := *suite.AWSSession.Config.Region … assert.True(t, regionAllowed, "VPC must be in EU region …")`; `assert.Contains(t, kmsKeyArn, "eu-west-1", …)` under rubriken "validates that all storage is encrypted"
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Testet jämför sessionens egen hårdkodade region (`eu-west-1`, rad 517) med en vitlista – det kan inte misslyckas och säger ingenting om var VPC:n ligger. Krypteringstestet verifierar bara att en ARN innehåller en regionsträng, inte att något är krypterat. Som GDPR-exempel ger det falsk trygghet.
- **Förslag:** Läs regionen ur VPC-ARN/`DescribeVpcs`-svaret eller ur Terraform-output, och verifiera kryptering via `DescribeVolumes`/`GetBucketEncryption`/`DescribeDBInstances(StorageEncrypted)`.

### K-37 13_CODE_K: `bitnami/kubectl:1.29` – EOL-version och borttagna Bitnami-taggar
- **Fil:rad:** docs/30_appendix_code_examples.md:1741
- **Påstående/kod:** `image: bitnami/kubectl:1.29`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Kubernetes 1.29 nådde EOL 2025-02-28 (endoflife.date/kubernetes). Bitnami flyttade "All existing container images, including older or versioned tags" till `bitnamilegacy` (2025-08-28/2025-09-29), ett arkiv som "will receive no further updates or support", och behåller endast `latest`-taggar fritt (https://github.com/bitnami/containers/issues/83267).
- **Förslag:** Använd en version inom support, t.ex. `registry.k8s.io/kubectl:v1.33.x` eller `alpine/k8s`, och pinna med digest.

### K-38 15_CODE_2 kombinerar VPA (Auto) och HPA på samma CPU/minnes-mått
- **Fil:rad:** docs/30_appendix_code_examples.md:2971–3010
- **Påstående/kod:** `kind: VerticalPodAutoscaler … updateMode: "Auto"` och `kind: HorizontalPodAutoscaler … metrics: cpu/memory Utilization` för samma `Deployment web-application`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** VPA:s kända begränsningar: "Vertical Pod Autoscaler should not be used with the Horizontal Pod Autoscaler (HPA) on the same resource metric (CPU or memory) at this moment" (https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/known-limitations.md). Exemplet presenteras som kostnadsoptimering men skapar motverkande skalning.
- **Förslag:** Låt VPA köra i `updateMode: "Off"` (rekommendationer) eller låt HPA skala på anpassade mått (t.ex. RPS) när VPA styr CPU/minne.

### K-39 13_CODE_L: steg som inte kan köras på en ren runner
- **Fil:rad:** docs/30_appendix_code_examples.md:1778–1783, 1792–1795, 1843–1845
- **Påstående/kod:** `run: terraform fmt -check -recursive` / `run: terraform validate` utan `terraform init`; `run: opa test policies/infrastructure -v` utan OPA installerad; `run: k6 run tests/performance/k6-load-test.js` utan k6
- **Bedömning:** FEL
- **Allvarlighet:** Medel
- **Evidens:** `terraform validate` kräver initierade providers/moduler ("Missing required provider … run terraform init"); OPA och k6 ingår inte i `ubuntu-latest`-bilden (Terraform gör det). Policysteget skulle dessutom falla på v0-syntaxen i 13_CODE_J (se K-04). Workflowen är uttryckligen en skiss (placeholder-skript), därför Medel.
- **Förslag:** Lägg till `hashicorp/setup-terraform@v3` + `terraform init -backend=false` i `static-analysis`, `open-policy-agent/setup-opa@v2` i `policy` och `grafana/setup-k6-action@v1` i `performance`.

### K-40 13_CODE_A: coverage-trösklar på fel nivå (Vitest < 1.0)
- **Fil:rad:** docs/30_appendix_code_examples.md:1040–1043
- **Påstående/kod:** `coverage: { … lines: 80, functions: 80, branches: 80, statements: 80 }`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Vitest 1.0-migreringsguiden ("Migrating from Vitest 0.34.6", avsnittet "Changes to Coverage"): "Coverage thresholds API's shape was changed, and it now supports specifying thresholds for specific files using glob patterns" – `lines/functions/branches/statements` flyttades in under `thresholds` (https://v1.vitest.dev/guide/migration.html). Aktuell konfigurationsreferens dokumenterar endast `coverage.thresholds.*` (https://vitest.dev/config/coverage). I Vitest ≥ 1 ignoreras bokens nycklar tyst och ingen tröskel upprätthålls.
- **Förslag:** `coverage: { provider: 'v8', reporter: [...], thresholds: { lines: 80, functions: 80, branches: 80, statements: 80 } }`.

### K-41 05_CODE_2: Checkov-filtret på `severity == 'CRITICAL'` är sannolikt tomt
- **Fil:rad:** docs/30_appendix_code_examples.md:277–281
- **Påstående/kod:** `def criticalIssues = results.results.failed_checks.findAll { it.severity == 'CRITICAL' }`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Severity-metadata hämtas från Prisma Cloud/Bridgecrew-plattformen; CLI-referensen för `--skip-download` anger att nedladdningen kan hoppas över, vilket "will omit … severities" (https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html). Utan plattformsdata är `severity` `null` i JSON-utdata och grinden "Critical security issues must be resolved" slår aldrig till. Dokumentationen säger inte explicit att API-nyckel krävs för severities – därför TVEKSAMT.
- **Förslag:** Filtrera på check-id:n (t.ex. en lista över kritiska `CKV_AWS_*`) eller använd `--hard-fail-on CRITICAL` med plattformsnyckel och låt Checkovs exit-kod avgöra.

### K-42 05_CODE_1: jobbvillkoret bygger på `head_commit`, som saknas vid `pull_request`
- **Fil:rad:** docs/30_appendix_code_examples.md:45–49, 64
- **Påstående/kod:** `on: push … pull_request …`; `if: contains(github.event.head_commit.message, 'personal-data') || contains(github.event.head_commit.message, 'gdpr')`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** `head_commit` ingår endast i `push`-händelsens payload (GitHub webhook events: `push`), inte i `pull_request`; uttrycket blir `contains(null, …)` → false, så "GDPR Compliance Validation" körs aldrig på PR:er trots att workflowen triggas av dem. Kommentaren (rad 65–69) varnar för nyckelordsstyrning men inte för detta.
- **Förslag:** Ta bort `if:` och kör skanningen alltid (så som kommentaren själv rekommenderar), eller använd `github.event.pull_request.title` vid PR.

### K-43 13_CODE_B: RDS PostgreSQL 14.7 kan inte längre skapas
- **Fil:rad:** docs/30_appendix_code_examples.md:1143
- **Påstående/kod:** `engine_version: '14.7'`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** RDS release-kalendern listar för major 14 endast minorversionerna 14.18–14.24 som stödda (14.21 i `NO_CREATE`); major 14 lämnar standardsupport 2027-02-28 (https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html). En generator som hårdkodar 14.7 producerar oanvändbar konfiguration.
- **Förslag:** Parametrisera (`engineVersion = '16'`, låt RDS välja minor) och nämn att versionen bör följa supportkalendern.

### K-44 13_CODE_F: Node 20 har nått end-of-life
- **Fil:rad:** docs/30_appendix_code_examples.md:1426–1428
- **Påstående/kod:** `name: Use Node.js 20 … node-version: 20`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** Node.js 20 EOL 2026-04-30 (endoflife.date/nodejs); setup-node:s README använder Node 24 i exemplen. (Bokens egen toolchain pinnar Node 20.11.1 i BOOK_REQUIREMENTS.md – samma problem gäller där.)
- **Förslag:** `node-version: 22` (LTS) eller `node-version-file: .nvmrc`.

### K-45 21_CODE_1 pinnar azurerm `~> 3.0`
- **Fil:rad:** docs/30_appendix_code_examples.md:702–705
- **Påstående/kod:** `azurerm = { source = "hashicorp/azurerm" version = "~> 3.0" }`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** azurerm CHANGELOG (main): aktuell version 5.12.0 (2026-10-29), 5.0.0 släpptes 2026-07-27 och 4.x i augusti 2024. 3.x får inga uppdateringar. AWS-providern pinnas däremot `~> 5.0` medan aktuell är 6.71 (acceptabelt men gammalt).
- **Förslag:** `version = "~> 5.0"` för azurerm (och `~> 6.0` för aws), eller en kommentar om att versioner ska uppdateras.

### K-46 Källa 3: död URL till Structurizr DSL-repot
- **Fil:rad:** docs/30_appendix_code_examples.md:4266 (och docs/33_references.md:135)
- **Påstående/kod:** `**Structurizr (2024).** *Structurizr DSL Language Reference.* … Available at: [https://github.com/structurizr/dsl](https://github.com/structurizr/dsl)`
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Medel
- **Evidens:** `https://github.com/structurizr/dsl` svarar 404 (WebFetch) / 403 (curl). DSL-koden flyttades till modulen `structurizr-dsl` i `structurizr/java`, som i sin tur arkiverades 2026-03-28 med texten "The code in this repo has been moved to https://github.com/structurizr/structurizr". Den kanoniska språkreferensen är https://docs.structurizr.com/dsl/language (svarar 200).
- **Förslag:** `Structurizr (2026). Structurizr DSL language reference. https://docs.structurizr.com/dsl/language` – uppdatera även docs/33_references.md:135.

### K-47 Navigationslistan länkar till sektioner som inte finns
- **Fil:rad:** docs/30_appendix_code_examples.md:19, 21 (jfr 12–22)
- **Påstående/kod:** `6. **[Testing and validation](#testing-validation)**`, `8. **[Shell scripts and utilities](#shell-scripts)**`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Filen definierar ankarna `#cicd-pipelines, #terraform-iac, #cloudformation-architecture-as-code, #automation-scripts, #configuration, #chapter-13-testing, #organisational-change, #security-compliance, #structurizr-workspaces` – inget `#testing-validation` eller `#shell-scripts` (det finns inga shell-skript i bilagan). Sektionerna "Chapter 13: Testing Strategies Reference Implementations", "Organisational Change and Team Structures", "Chapter 14 Reference Implementations" och "Chapter 15 Reference Implementations" saknas i listan.
- **Förslag:** Byt punkt 6 till `[Testing strategies (Chapter 13)](#chapter-13-testing)`, ta bort punkt 8 och lägg till poster för kapitel 14, 15 och 17.

### K-48 Fem listningar refereras inte från de kapitel de hävdar
- **Fil:rad:** docs/30_appendix_code_examples.md:116 (05_CODE_2), 755 (07_CODE_1), 818 (24_CODE_1), 914–915 (22_CODE_2), 3877 (06_CODE_5)
- **Påstående/kod:** `*Referenced from chapter 5 …*`, `*Referenced from Chapter 7: Containerisation and Orchestration as Code*`, `*Referenced from chapter 24 …*`, `### 22_CODE_2 … *Referenced from chapter 24*`, `*Referenced from chapter 6: Structurizr*`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** `grep` över docs/*.md: kapitel 5 refererar 05_CODE_1 och 05_CODE_3 men inte Jenkins-listningen; kapitel 7 innehåller varken "CloudFormation", "appendix" eller "07_code"; kapitel 22 och 24 nämner inte 22_CODE_2/24_CODE_1; kapitel 6 refererar inte 06_CODE_5. 22_CODE_2 har kapitel-22-id men anges som refererad från kapitel 24, vilket bryter mot bilagans egen konvention (rad 24). Kapitel 15 länkar med `(#15_code_1)` i stället för `30_appendix_code_examples.md#15_code_1` (docs/15_cost_optimization.md:92, 105, 116), vilket inte fungerar i flerfilsbyggen.
- **Förslag:** Lägg in korsreferenser i kapitel 5, 6, 22/24 (eller ta bort listningarna), flytta 07_CODE_1 till ett passande kapitel (t.ex. kapitel 9 eller 12) eller byt id, och rätta länkarna i kapitel 15.

### K-49 Kapitel 10 och 10_CODE_1/10_CODE_2 beskriver olika innehåll
- **Fil:rad:** docs/30_appendix_code_examples.md:3284–3287, 3384, 3400, 3526, 3586–3587 (jfr docs/10_policy_and_security.md:46, 52, 87)
- **Påstående/kod:** `package se.enterprise.security`, `"reference": "MSB 3.2.1 Network Segmentation"`, `"title": "Finansinspektionen Supplement"`; prosan "network segmentation checks inspired by MSB guidance"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Kapitel 10 säger att 10_CODE_1 är "tailored for EU and UK regulators" och visar `package eu.enterprise.security`; bilagan har `se.`-paket och svenska myndigheter (MSB, Finansinspektionen; 22_CODE_2 nämner IMY). Kapitel 10 (rad 87) lovar att 10_CODE_2 "incorporate[s] PSD2 requirements" – profilen innehåller ingen PSD2-kontroll. Begreppet MSB förklaras inte för en internationell läsekrets.
- **Förslag:** Harmonisera paketnamn och regulatorer mellan kapitel och bilaga (t.ex. ENISA/NIS2 som EU-neutral referens) och lägg till en PSD2-kontroll i profilen eller stryk löftet i kapitel 10.

### K-50 17_CODE_3: "DORA-liknande" nivåer stämmer inte med DORA
- **Fil:rad:** docs/30_appendix_code_examples.md:2309–2347 (särskilt 2313–2316, 2323–2326, 2333–2336, 2343–2346)
- **Påstående/kod:** lead time `elite: "< 1 hour", high: "1 day - 1 week", medium: "1 week - 1 month", low: "> 1 month"`; MTTR `medium: "1 day - 1 week", low: "> 1 week"`; change failure rate `elite: "0-15%", high: "16-30%", medium: "31-45%", low: "> 45%"`; deployment frequency `low: "< 1 per month"`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** DORA 2024 (Accelerate State of DevOps Report, s. "Four distinct clusters"): Elite – lead time "Less than one day", deployment "On demand", CFR 5 %, recovery "Less than one hour"; High – "Between one day and one week", "Between once per day and once per week", 20 %, "Less than one day"; Medium – "Between one week and one month", "Between once per week and once per month", 10 %, "Less than one day"; Low – "Between one month and six months", "Between once per month and once every six months", 40 %, "Between one week and one month". Bokens CFR-band (16–30 %, 31–45 %) och MTTR-band motsvarar ingen DORA-årgång; "< 1 hour" för lead time är 2021-rapportens värde. Avsnittet nämner "DevOps industry standards" (rad 2425) utan källa.
- **Förslag:** Ange DORA 2024 som källa och använd dess nivåer, eller skriv uttryckligen att värdena är organisationens egna mål.

### K-51 06_CODE_5: wildcard i taggexpression saknar stöd i DSL-dokumentationen
- **Fil:rad:** docs/30_appendix_code_examples.md:4177–4178
- **Påstående/kod:** `include element.tag==External*`, `include ->element.tag==External*->`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** Uttrycksreferensen specificerar `element.tag==<tag>[,tag]` ("all elements that have all of the specified tags", kommaseparerad lista) och dokumenterar inga wildcards (https://docs.structurizr.com/dsl/expressions). Taggen i modellen heter exakt `External System`, så `External*` matchar sannolikt ingenting.
- **Förslag:** `include "element.tag==External System"` och `include "->element.tag==External System->"`.

### K-52 "Conventions"-avsnittet beskriver markeringar som inte används
- **Fil:rad:** docs/30_appendix_code_examples.md:2451–2456
- **Påstående/kod:** "Security aspects are marked with 🔒", "GDPR-related configurations are marked with 🇪🇺", "Local customisations are marked with 🇸🇪"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Varje symbol förekommer exakt en gång i filen – på konventionsraden själv. 🇸🇪 "Local customisations" är en kvarleva från den svenska utgåvan.
- **Förslag:** Stryk avsnittet eller inför markeringarna konsekvent.

### K-53 Påståendet att bilagan samlar "every code example" i boken
- **Fil:rad:** docs/30_appendix_code_examples.md:5 (jfr docs/part_h_appendices.md:13)
- **Påstående/kod:** "Appendix A collects every code example, configuration file, and technical implementation referenced throughout the book."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Kapitlen innehåller mängder av inline-kod som inte finns i bilagan (t.ex. Prometheus-konfiguration i docs/05_automation_devops_cicd.md:539–548, DSL-exempel i docs/06_structurizr.md:83–125, Rego-utdraget i docs/10_policy_and_security.md:48–62).
- **Förslag:** "Appendix A collects the extended code listings that the chapters refer to by identifier."

### K-54 Kapiteltitlar i backlinks avviker från book_index.json
- **Fil:rad:** docs/30_appendix_code_examples.md:31, 116, 424, 692, 818
- **Påstående/kod:** "chapter 5: Automation, DevOps and CI/CD for Architecture as Code"; "Chapter 21: Digital Transformation in Enterprises"; "chapter 24: Architecture as Code Best Practices and Lessons Learned"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** docs/book_index.json: kapitel 5 = "Automation, DevOps and CI/CD for Infrastructure as Code", kapitel 21 = "Digitalisation through Code-based Infrastructure", kapitel 24 = "Best Practices and Lessons Learned" (rad 915 använder den korrekta titeln). Kapitel 15 heter "15B" i indexet men "Chapter 15" i bilagan (rad 2789–2794).
- **Förslag:** Generera backlink-titlarna från book_index.json i byggskriptet.

### K-55 Källa 1 saknas i den numrerade bibliografin
- **Fil:rad:** docs/30_appendix_code_examples.md:4264
- **Påstående/kod:** `1. **HashiCorp (2024).** *Terraform Language Documentation.* … https://developer.hashicorp.com/terraform/language`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** docs/33_references.md har HashiCorp-poster [5] "What is Terraform", [16] "Securing Terraform State", [17] "Backend Type: s3", [26] "Write Terraform Tests" – men ingen "Terraform Language Documentation"; källorna 2 och 4 länkar korrekt till [13] respektive [10]. (Sidonotering: Source [10] i 33_references.md pekar på filerna `10_policy_as_code.md` och `32_index.md`, som inte finns.)
- **Förslag:** Lägg till posten i 33_references.md med ett nummer och länka `[Source [n]]`, eller hänvisa till Source [5].

### K-56 05_CODE_2: felaktig språkmarkering, odefinierad variabel och ospecificerat "lagkrav"
- **Fil:rad:** docs/30_appendix_code_examples.md:118–119, 150, 392
- **Påstående/kod:** fence ```` ```yaml ```` runt en Jenkinsfile; `AUDIT_RETENTION_YEARS = '7'  // Legal requirement for audit retention`; `# Cost Report - ${env.ORGANIZATION_NAME}`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Blocket är Groovy (PyYAML: "mapping values are not allowed here"); miljövariabeln deklareras som `ORGANISATION_NAME` (rad 143) så rapporten skriver `null`; "legal requirement" anges utan lag (7 år motsvarar t.ex. svenska bokföringslagen, inte GDPR). Conftest pinnas till v0.46.0 (rad 328) från 2023.
- **Förslag:** ```` ```groovy ````, `${env.ORGANISATION_NAME}`, och "e.g. 7 years under national accounting legislation".

### K-57 13_CODE_G: testbeskrivning nämner Locust men verktyget är k6
- **Fil:rad:** docs/30_appendix_code_examples.md:1488–1490
- **Påstående/kod:** `description: Execute Locust load test to validate latency thresholds.` / `tooling: k6`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Två olika lasttestverktyg i samma testpost; 13_CODE_L kör k6.
- **Förslag:** "Execute k6 load test …".

### K-58 10_CODE_4 använder `datetime.utcnow()`
- **Fil:rad:** docs/30_appendix_code_examples.md:3773, 3847
- **Påstående/kod:** `now = datetime.utcnow().isoformat() + "Z"`; `datetime.utcnow().strftime("ssp-%Y%m%d%H%M%S")`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Python-dokumentationen: "Deprecated since version 3.12: Use datetime.now() with UTC instead." (https://docs.python.org/3/library/datetime.html). Bokens toolchain är Python 3.12.3.
- **Förslag:** `datetime.now(timezone.utc).isoformat()`.

### K-59 24_CODE_1: dataklassen `TestCase` kolliderar med pytest-insamling; oanvända importer
- **Fil:rad:** docs/30_appendix_code_examples.md:822–827, 830–839
- **Påstående/kod:** `import pytest … import json import yaml … from datetime import datetime, timedelta`; `@dataclass class TestCase:`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** pytest samlar klasser med prefixet `Test`; en klass med `__init__` ger `PytestCollectionWarning: cannot collect test class 'TestCase' because it has a __init__ constructor`. `pytest`, `json`, `yaml` och `timedelta` används inte. Även 15_CODE_3 (`import pandas as pd`, rad 3046) och 17_CODE_2 (`timedelta`, `Optional`, `json`) har oanvända importer.
- **Förslag:** Döp om till `CheckResult` och ta bort oanvända importer.

### K-60 14_CODE_2/14_CODE_3: `us-west-2` i en bilaga som annars betonar EU-residens
- **Fil:rad:** docs/30_appendix_code_examples.md:2592, 2608, 2655, 2684
- **Påstående/kod:** `region = "us-west-2"`, `AWS_REGION: us-west-2`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** Övriga listningar (05, 07, 10, 13, 15, 21) hårdkodar eller kräver EU-regioner och motiverar det med GDPR; kapitel 14-listningarna bryter mönstret utan kommentar.
- **Förslag:** `eu-west-1`/`eu-north-1`, eller en not om att regionen är ett exempel.

### K-61 14_CODE_3: `environment.url` refererar till ett steg-id som inte finns
- **Fil:rad:** docs/30_appendix_code_examples.md:2778–2786
- **Påstående/kod:** `environment: name: production url: ${{ steps.deploy.outputs.application_url }}` följt av enbart `run: echo "Production deployment requires manual approval"`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Inget steg har `id: deploy`; uttrycket evalueras till tom sträng. Dessutom är `-var-file="terraform.tfvars"` (rad 2719) redundant eftersom `terraform.tfvars` laddas automatiskt.
- **Förslag:** Ge apply-steget `id: deploy` och sätt `echo "application_url=…" >> "$GITHUB_OUTPUT"`, eller stryk `url`.

### K-62 06_CODE_5: manuell numrering i dynamisk vy; tom deployment node
- **Fil:rad:** docs/30_appendix_code_examples.md:4150–4162, 4113–4115
- **Påstående/kod:** `customer -> webApp "1. Submits order"` … `"13. Confirmation email"`; `deploymentNode "Read Replicas" { instances 2 }`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Structurizr numrerar stegen i dynamiska vyer automatiskt, så etiketterna renderas "1. 1. Submits order". En deployment node utan container-/infrastrukturinstans visas tom i deployment-vyn.
- **Förslag:** Ta bort siffrorna; lägg `containerInstance orderDb` (eller `infrastructureNode`) i "Read Replicas".

### K-63 `actions/checkout@v4` och `hashicorp/setup-terraform@v3` är inte längre aktuella major
- **Fil:rad:** docs/30_appendix_code_examples.md:72, 1423, 1776, 1791, 1801, 1813, 1803, 1815
- **Påstående/kod:** `uses: actions/checkout@v4`, `uses: hashicorp/setup-terraform@v3`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** README (main): `actions/checkout@v7`, `hashicorp/setup-terraform@v4`. v4/v3 fungerar fortfarande.
- **Förslag:** Behåll men lägg till en not om att major-versioner ska uppdateras, eller använd aktuella.

### K-64 13_CODE_J: `default allow = true` utan funktion och v0-tilldelning
- **Fil:rad:** docs/30_appendix_code_examples.md:1628
- **Påstående/kod:** `default allow = true`
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** `allow` används varken av Conftest (som läser `deny/warn/violation`) eller av testerna; i Rego v1 skrivs defaults `default allow := true` ("the rule syntax is restricted to: default <name> := <term>").
- **Förslag:** Stryk raden.

### K-65 10_CODE_1 använder legacytypen `aws_elasticsearch_domain`
- **Fil:rad:** docs/30_appendix_code_examples.md:3296, 3408
- **Påstående/kod:** `"aws_elasticsearch_domain"`
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Resursen finns kvar i AWS-providern men Amazon OpenSearch Service hanteras med `aws_opensearch_domain`; en modern policy bör omfatta båda.
- **Förslag:** Lägg till `"aws_opensearch_domain"` i mängden.

## Verifierat korrekt (urval)

- **Alla fem Python-block kompilerar** (`python3 -m py_compile`), alla elva riktiga YAML-block parsar, båda JSON-blocken parsar; alla fem TypeScript-block (13_CODE_A–E) typkontrollerar med `tsc --strict` (endast miljöfel för saknade `vitest`/`@types/node`). 13_CODE_C och 13_CODE_E är logiskt konsistenta med sina implementationer.
- **15_CODE_2 Kubernetes-manifest:** `ResourceQuota` med `count/pods`, `count/services`, `persistentvolumeclaims`, `requests.cpu`, `limits.memory` (https://kubernetes.io/docs/concepts/policy/resource-quotas/ – "count/<resource> for resources from the core API group"); `LimitRange` typ `Container`; `autoscaling.k8s.io/v1 VerticalPodAutoscaler` med `updatePolicy`/`resourcePolicy`; `autoscaling/v2 HorizontalPodAutoscaler` med `metrics` och `behavior` – korrekta API-versioner och fält.
- **13_CODE_K:** `batch/v1 Job`, `restartPolicy: Never`, ConfigMap-volym med `defaultMode: 0555` och etikettnamnet `pod-security.kubernetes.io/enforce` är korrekta (felet är objektet, se K-16).
- **15_CODE_1:** `aws_launch_template.instance_requirements` (med `memory_mib`, `vcpu_count`, `instance_generations`) är ett giltigt toppnivåblock ("If present then `instance_type` cannot be present"), liksom `instance_market_options.spot_options.max_price` och `tag_specifications` (`website/docs/r/launch_template.html.markdown`); `mixed_instances_policy.instances_distribution` och `dynamic "tag"` i `aws_autoscaling_group` är korrekta.
- **14_CODE_1/14_CODE_2:** `aws_lb`, `aws_autoscaling_group.launch_template { version = "$Latest" }`, `default_tags`, `jsonencode`-dashboard och `required_version`/`required_providers` är syntaktiskt korrekta.
- **05_CODE_1:** `env`-uttrycket `${{ github.ref_name == 'main' && 'production' || github.ref_name }}`, `paths`-filter och `fetch-depth: 0` är giltig GitHub Actions-syntax.
- **13_CODE_L:** `bridgecrewio/checkov-action@v12` finns och tar `directory:` (README, master); `hashicorp/setup-terraform@v3` är giltig; `terraform workspace new … || terraform workspace select …` är korrekt idiom.
- **05_CODE_3/13_CODE_I:** `terraform.Options`-fälten `TerraformDir`, `Vars`, `BackendConfig`, `RetryableTerraformErrors`, `MaxRetries`, `TimeBetweenRetries`, samt `terraform.InitAndApply/Output/Destroy` och `aws.GetTagsForVpc` finns i terratest v0.48.2 (typkontrollerat); `ec2.DescribeVpcs`, `ec2.DescribeTags`, `cloudtrail.DescribeTrails` är korrekta SDK v1-anrop.
- **10_CODE_1/10_CODE_2:** GDPR-referenserna är korrekta: art. 32 "Security of processing"; art. 44–49 utgör kapitel V om överföringar till tredjeland (https://gdpr-info.eu/chapter-5/). `oscal-version: 1.1.2` är en publicerad OSCAL-version; profilens `imports.href` till `NIST_SP-800-53_rev5_catalog.json` svarar HTTP 200; `merge.combine.method: "merge"` och `alters.adds.position: "after"` + `by-id` är schemagiltiga (endast UUID-felet rapporterades).
- **10_CODE_4:** `import hcl2` är korrekt modulnamn för paketet `python-hcl2`, och `hcl2.load()` returnerar `resource` som en lista av objekt så `data.get("resource", [])` fungerar.
- **15_CODE_3:** `boto3.client('ce')`, `get_cost_and_usage(TimePeriod, Granularity='DAILY', Metrics=['BlendedCost'], Filter={'Dimensions': {'Key': 'REGION', 'Values': [...]}})` och `get_rightsizing_recommendation(Service='AmazonEC2', Configuration={'BenefitsConsidered': True, 'RecommendationTarget': 'SAME_INSTANCE_FAMILY'})` är korrekta anrop; `describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])` är korrekt.
- **07_CODE_1:** `!If`, `!Equals`, `!Sub '${AWS::StackName}-vpc'`, `CommaDelimitedList`-parametern och `AWS::EC2::VPC`-egenskaperna är korrekta (felet är `!Contains`, K-07).
- **06_CODE_5:** `!docs`/`!adrs` på workspace-nivå, `person`, `softwareSystem`, `container`, `component`, `group`, `tags` med flera argument, `perspectives`, `deploymentEnvironment`/`deploymentNode`/`containerInstance`/`instances`, `systemContext`/`container`/`component`/`dynamic`/`deployment`-vyer, `include *`, `autoLayout lr|tb`, `description` i vyer, `colour` som synonym till `color`, `routing orthogonal`, `themes <url>` och `configuration { scope softwaresystem }` är dokumenterade DSL-konstruktioner (https://docs.structurizr.com/dsl/language).
- **05_CODE_2:** Conftest v0.46.0-nedladdningen (`conftest_0.46.0_Linux_x86_64.tar.gz`) och Infracost-installationsskriptet svarar HTTP 200; `readJSON`/`writeFile`/`archiveArtifacts` är korrekta Jenkins-steg (Pipeline Utility Steps).
- **Källor 2 och 4** länkar till befintliga ankare `#source-13` (Kubernetes Documentation: Concepts) och `#source-10` (OPA, Policy as Code Overview) i docs/33_references.md med matchande titlar och årtal.

## Ej verifierbart

- **"MSB 3.2.1 Network Segmentation", "MSB 3.2.2 Minimal Exposure" och kontroll-id:n `msb-3.2.1`, `msb-3.2.1.1`, `msb-3.2.1.2`** (rad 3384, 3400, 3556, 3600, 3660, 3684, 3715): ingen numrerad MSB-vägledning med denna struktur kunde identifieras; MSBFS 2020:7 är indelad i kapitel/paragrafer, inte i "3.2.1 Network Segmentation". Webbsökning var inte tillgänglig i sessionen (sökbudget förbrukad) och msb.se kontrollerades inte. Bör bekräftas av IT-arkitekturexperten/författaren eller ersättas av en verifierbar källa (t.ex. NIST SP 800-53 SC-7, ISO/IEC 27001:2022 A.8.22). Samma gäller "Finansinspektionen Supplement" och de påhittade parameter-id:na `gdpr-art32-1_prm1` m.fl. (de förutsätter en `regional-catalog.json` som inte visas).
- **`themes https://static.structurizr.com/themes/default/theme.json`** (rad 4252): värden `static.structurizr.com` kunde inte nås från sessionen (DNS blockerad av nätverkspolicyn; curl 000). DSL-syntaxen `theme <name|url|file>` är korrekt; huruvida exakt denna URL finns är obekräftat.
- **Om `bitnami/kubectl` innehåller `jq`** (13_CODE_K använder `jq` i containern, rad 1717–1723): bildens innehåll kunde inte inspekteras (ingen registry-åtkomst). Rekommendation: använd en bild som garanterat har både `kubectl` och `jq`, eller `kubectl … -o jsonpath=`.
- **Checkov-`severity` i OSS-JSON utan plattformsnyckel** (K-41): dokumentationen antyder att severities kommer från plattformsdata men säger inte uttryckligen att API-nyckel krävs; kunde inte köras lokalt (checkov ej installerat, pip-installation ej gjord i repot).
- **Terraform-validering av HCL-blocken** (K-08, K-12–K-14) och **OPA-parsning av Rego-blocken** (K-01–K-04): bedömningarna bygger på officiell dokumentation, providerkällkod och OPA:s builtin-register, inte på körning, eftersom nedladdning av `terraform`/`opa`/`conftest` nekades av sessionens behörighetsklassificerare. Rekommenderad verifiering i repot: `terraform init -backend=false && terraform validate` per listning samt `opa check --strict` / `opa test` på Rego-blocken, gärna som ett nytt test i `tests/test_technical_accuracy.py`.
- **Kostnadsuppgifter i 15_CODE_3** (EBS-priser per GB/månad, rad 3200–3220): markerade som "representative values" i koden; inte kontrollerade mot aktuell prislista.
