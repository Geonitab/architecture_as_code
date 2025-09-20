# Versionhantering och kodstruktur

Effektiv versionhantering utgör ryggraden i Infrastructure as Code-implementationer. Genom att tillämpa samma metoder som mjukvaruutveckling på infrastrukturdefinitioner skapas spårbarhet, samarbetsmöjligheter och kvalitetskontroll. Som vi såg i [kapitel 2 om grundläggande principer](02_kapitel1.md), är reproducerbarhet och konsistens avgörande för framgångsrik IaC-implementation.

![Versionhantering och kodstruktur](images/diagram_03_kapitel2.png)

Diagrammet illustrerar det typiska flödet från Git repository genom branching strategy och code review till slutlig deployment, vilket säkerställer kontrollerad och spårbar infrastrukturutveckling. Detta flöde ligger till grund för den automatisering som vi kommer att fördjupa oss i [kapitel 4 om CI/CD-pipelines](04_kapitel3.md).

## Git-baserad arbetsflöde för infrastruktur

Git utgör standarden för versionhantering av IaC-kod och möjliggör distribuerat samarbete mellan team-medlemmar. Varje förändring dokumenteras med commit-meddelanden som beskriver vad som ändrats och varför, vilket skapar en komplett historik över infrastrukturutvecklingen.

### Branching-strategier för infrastrukturkod

Effektiva branching-strategier balanserar utvecklarhastighet med stabilitet och säkerhet. GitFlow-modellen anpassad för infrastrukturkod använder separata branches för olika environment och säkerställer att endast testade förändringar når produktionsmiljöer.

**Feature branches** möjliggör isolerad utveckling av nya infrastrukturkomponenter utan att påverka huvudkodbasen. Varje feature branch bör omfatta en logisk uppsättning relaterade infrastrukturändringar som kan testats och verifieras oberoende.

**Environment-specific branches** (development, staging, production) säkerställer att infrastrukturändringar deployas i rätt ordning och genomgår lämpliga valideringsprocesser. Pull requests mellan dessa branches utgör quality gates där code reviews och automated testing verifierar att förändringar uppfyller säkerhets- och kvalitetsstandarder.

### Commit-meddelanden och dokumentation

Strukturerade commit-meddelanden följer konventionella format som möjliggör automatisk changelog-generering och impact-analys. Commit-meddelanden för infrastrukturkod bör inkludera:

- **Type**: feat (ny feature), fix (bugfix), refactor (kodförbättring), docs (dokumentation)
- **Scope**: vilken del av infrastrukturen som påverkas (networking, security, storage)
- **Description**: kortfattad beskrivning av förändringen
- **Impact**: potentiell påverkan på befintliga system och användare

```
feat(networking): add VPC peering for cross-region connectivity

- Implemented VPC peering between Stockholm and Frankfurt regions
- Added route tables for secure inter-region communication  
- Updated security groups to allow necessary traffic flows
- Enables disaster recovery capabilities for production workloads

Impacts: Requires approval for cross-region data transfer costs
Breaking: None
```

## Kodorganisation och modulstruktur

Välorganiserad kodstruktur är avgörande för maintainability och collaboration i större IaC-projekt. Modulär design möjliggör återanvändning av infrastrukturkomponenter across olika projekt och miljöer.

### Hierarkisk katalogstruktur

En standardiserad katalogstruktur underlättar navigation och förståelse av infrastrukturkodbasen. Följande struktur har bevisat sig effektiv för svenska organisationer:

```
infrastructure/
├── environments/
│   ├── development/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── networking/
│   │   ├── vpc/
│   │   ├── subnets/
│   │   └── security-groups/
│   ├── compute/
│   │   ├── ec2/
│   │   ├── autoscaling/
│   │   └── load-balancers/
│   ├── data/
│   │   ├── rds/
│   │   ├── s3/
│   │   └── dynamodb/
│   └── security/
│       ├── iam/
│       ├── kms/
│       └── secrets-manager/
├── shared/
│   ├── locals.tf
│   ├── data-sources.tf
│   └── providers.tf
├── policies/
│   ├── security-policies/
│   ├── backup-policies/
│   └── compliance-policies/
└── documentation/
    ├── runbooks/
    ├── architecture-diagrams/
    └── troubleshooting-guides/
```

### Moduldesign och återanvändning

Terraform-moduler utgör byggstenar för infrastrukturkomponenter som kan återanvändas across olika projekt och miljöer. Väldesignade moduler följer single responsibility principle och exponerar konfigurerbara interfaces genom variables.

**Input variables** definierar konfigurationsmöjligheter för modulen och bör inkludera comprehensive validation rules och descriptive documentation. Standard svenska organisationsvariabler inkluderar:

```hcl
# modules/networking/vpc/variables.tf
variable "environment" {
  description = "Miljönamn (development, staging, production)"
  type        = string
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment måste vara development, staging eller production."
  }
}

variable "cost_center" {
  description = "Kostnadscenter för fakturering och rapportering"
  type        = string
  validation {
    condition     = can(regex("^CC-[0-9]{4}$", var.cost_center))
    error_message = "Cost center måste följa format CC-XXXX."
  }
}

variable "data_classification" {
  description = "Dataklassificering enligt svenska säkerhetskrav"
  type        = string
  default     = "internal"
  validation {
    condition = contains([
      "public", "internal", "confidential", "restricted", "personal"
    ], var.data_classification)
    error_message = "Data classification måste vara giltig klassificeringsnivå."
  }
}

variable "compliance_requirements" {
  description = "Lista över compliance-krav som måste uppfyllas"
  type        = list(string)
  default     = ["gdpr"]
  validation {
    condition = alltrue([
      for req in var.compliance_requirements : 
      contains(["gdpr", "iso27001", "soc2", "pci-dss", "msb"], req)
    ])
    error_message = "Compliance requirements måste vara giltiga standarder."
  }
}
```

**Output values** exponerar viktiga resurser och information som andra moduler eller root configurations kan använda. Outputs bör vara comprehensive och inkludera både resource identifiers och metadata:

```hcl
# modules/networking/vpc/outputs.tf
output "vpc_id" {
  description = "ID för det skapade VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR-block för VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "Lista över public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Lista över private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "security_group_defaults" {
  description = "Default security groups skapade för VPC"
  value = {
    web_sg_id = aws_security_group.web.id
    app_sg_id = aws_security_group.app.id
    db_sg_id  = aws_security_group.database.id
  }
}

output "compliance_metadata" {
  description = "Compliance-relaterade metadata för auditing"
  value = {
    gdpr_compliant     = var.data_classification != "public"
    encryption_enabled = true
    audit_logging      = aws_cloudtrail.vpc_audit.arn
    msb_compliant      = local.msb_security_enabled
  }
}
```

### Environment-specifik konfiguration

Separation av environment-specifik konfiguration från modullogik möjliggör samma infrastrukturkod att användas across development, staging och production environments med olika parametrar och skalning.

**Development environment** optimeras för kostnad och utvecklarhastighet:

```hcl
# environments/development/terraform.tfvars
environment = "development"
region      = "eu-north-1"

# Mindre instanser för kostnadseffektivitet
instance_types = {
  web = "t3.micro"
  app = "t3.small"
  db  = "db.t3.micro"
}

# Simplified networking för development
availability_zones = ["eu-north-1a"]
enable_nat_gateway = false
enable_vpn_gateway = false

# Development-specific features
enable_debug_logging    = true
enable_ssh_access      = true
backup_retention_days  = 7

# Kostnadskontroller
enable_spot_instances = true
auto_shutdown_schedule = "0 18 * * MON-FRI"  # Stäng av 18:00 vardagar
```

**Production environment** prioriterar prestanda, säkerhet och tillgänglighet:

```hcl
# environments/production/terraform.tfvars
environment = "production"
region      = "eu-north-1"

# Production-grade instances
instance_types = {
  web = "c5.large"
  app = "m5.xlarge"
  db  = "db.r5.2xlarge"
}

# Multi-AZ för high availability
availability_zones = ["eu-north-1a", "eu-north-1b", "eu-north-1c"]
enable_nat_gateway = true
enable_vpn_gateway = true

# Production security requirements
enable_debug_logging = false
enable_ssh_access   = false
backup_retention_days = 90

# Compliance och säkerhet
enable_encryption_at_rest = true
enable_encryption_in_transit = true
enable_access_logging = true
enable_compliance_monitoring = true

# Disaster recovery
enable_cross_region_backups = true
rto_requirement_hours = 4
rpo_requirement_hours = 1
```

## Code review-processer för infrastruktur

Code reviews för infrastrukturkod kräver specialized approaches som fokuserar på säkerhets-, prestanda- och kostnadsimplikationer utöver traditional code quality aspects.

### Review checklist för IaC

Strukturerade checklists säkerställer att alla viktiga aspekter granskas systematiskt:

**Säkerhetsaspekter:**
- [ ] Finns inga hardkodade credentials eller secrets i koden
- [ ] Säkerhetsgrupper följer least privilege principle
- [ ] Kryptering är aktiverad för all känslig data
- [ ] IAM-roller och policies följer minimal behörighetsprincip
- [ ] Nätverkssegmentering implementerar defense-in-depth

**Compliance och governance:**
- [ ] Resurstagging följer organisationsstandarder
- [ ] GDPR-krav uppfylls för persondata-hantering
- [ ] MSB säkerhetskrav implementeras för kritiska system
- [ ] Audit logging är konfigurerat för alla relevanta åtgärder
- [ ] Backup och disaster recovery policies följs

**Prestanda och kostnad:**
- [ ] Rätt instance-storlekar valda baserat på workload-krav
- [ ] Auto-scaling konfigurerat för optimal resursanvändning
- [ ] Reserved instances används där lämpligt för kostnadsoptimering
- [ ] Monitoring och alerting konfigurerat för prestanda-metrics

**Operationella aspekter:**
- [ ] Dokumentation uppdaterad för nya komponenter
- [ ] Runbooks finns för troubleshooting och maintenance
- [ ] Deployment-process är automated och reproducerbar
- [ ] Rollback-procedurer dokumenterade och testade

### Automated code analysis

Automatiserade verktyg kompletterar manuella code reviews genom att identifiera vanliga problem och säkerhetshot:

```yaml
# .github/workflows/infrastructure-review.yml
name: Infrastructure Code Review

on:
  pull_request:
    paths: ['infrastructure/**']

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Terraform Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: 'infrastructure/'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  cost-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Terraform Cost Estimation
        uses: infracost/infracost-gh-action@master
        with:
          path: infrastructure/
        env:
          INFRACOST_API_KEY: ${{ secrets.INFRACOST_API_KEY }}
      
      - name: Comment Cost Estimate
        uses: infracost/infracost-gh-action@master
        with:
          behavior: update
          path: infrastructure/

  compliance-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: GDPR Compliance Check
        run: |
          # Custom script för GDPR compliance validation
          python scripts/gdpr-compliance-check.py infrastructure/
      
      - name: Swedish Security Requirements
        run: |
          # Validera MSB säkerhetskrav
          python scripts/msb-security-validation.py infrastructure/
```

## State management och collaboration

Terraform state management utgör en kritisk komponent för team collaboration och måste hanteras med särskild omsorg för säkerhet och consistency.

### Remote state backends

Remote state storage säkerställer att team-medlemmar arbetar mot samma infrastructure state och möjliggör safe concurrent operations genom state locking:

```hcl
# shared/backend.tf
terraform {
  backend "s3" {
    bucket         = "svenska-org-terraform-state"
    key            = "environments/${var.environment}/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
    
    # Aktivera versioning för state recovery
    versioning = true
    
    # Säkerhetskonfiguration
    server_side_encryption_configuration {
      rule {
        apply_server_side_encryption_by_default {
          kms_master_key_id = "arn:aws:kms:eu-north-1:123456789012:key/svenska-terraform-key"
          sse_algorithm     = "aws:kms"
        }
      }
    }
  }
}

# State locking med DynamoDB
resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-state-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Locks"
    Environment = "shared"
    Purpose     = "infrastructure-state-management"
  }
}
```

### State security och backup

State files innehåller känslig information och måste skyddas mot unauthorized access och data loss:

**Encryption och access control:**
- State files krypteras både at rest och in transit
- IAM policies begränsar access till endast authorized team members
- MFA krävs för åtkomst till production state
- Audit logging spårar alla state-modifikationer

**Backup och disaster recovery:**
- Automatiska backups av state files med point-in-time recovery
- Cross-region replication för disaster recovery scenarios
- Automated testing av backup restoration procedures
- Documentation av recovery procedures och contact information

## Praktiska exempel

### Komplett Git workflow implementation

```bash
#!/bin/bash
# scripts/infrastructure-workflow.sh
# Standardiserat workflow för infrastruktur-förändringar

set -e

ENVIRONMENT=${1:-development}
FEATURE_NAME=${2:-"feature-$(date +%Y%m%d-%H%M)"}

echo "🏗️ Startar Infrastructure Workflow"
echo "Environment: $ENVIRONMENT"
echo "Feature: $FEATURE_NAME"

# 1. Skapa feature branch
git checkout main
git pull origin main
git checkout -b "infra/$FEATURE_NAME"

echo "✅ Feature branch skapad: infra/$FEATURE_NAME"

# 2. Planera förändringar
cd "environments/$ENVIRONMENT"

echo "📋 Kör Terraform plan..."
terraform init
terraform plan -out="$FEATURE_NAME.tfplan"

# 3. Validera säkerhet och compliance
echo "🔒 Kör säkerhetsscan..."
trivy config --format json --output security-report.json .

echo "💰 Beräknar kostnadspåverkan..."
infracost breakdown --path . --format json --out-file cost-estimate.json

# 4. Generera PR-beskrivning
echo "📝 Genererar PR-beskrivning..."
cat > pr-description.md << EOF
## Infrastructure Changes for $ENVIRONMENT

### 🎯 Purpose
Automated infrastructure changes for feature: $FEATURE_NAME

### 📊 Impact Analysis
- **Environment**: $ENVIRONMENT
- **Terraform Plan**: Attached as \`$FEATURE_NAME.tfplan\`
- **Security Report**: See \`security-report.json\`
- **Cost Estimate**: See \`cost-estimate.json\`

### ✅ Pre-deployment Checklist
- [ ] Security scan passed
- [ ] Cost impact reviewed and approved
- [ ] Compliance requirements validated
- [ ] Documentation updated
- [ ] Rollback plan documented

### 🚀 Deployment Instructions
1. Review and approve this PR
2. Merge to trigger automated deployment
3. Monitor deployment through CloudWatch dashboard
4. Verify functionality through health checks

EOF

echo "🎉 Workflow komplett!"
echo "Nästa steg:"
echo "1. Granska terraform plan: terraform show $FEATURE_NAME.tfplan"
echo "2. Kontrollera säkerhetsrapporten: cat security-report.json"
echo "3. Granska kostnadspåverkan: cat cost-estimate.json"
echo "4. Commita dina ändringar: git add . && git commit -m 'feat($ENVIRONMENT): $FEATURE_NAME'"
echo "5. Pusha och skapa PR: git push origin infra/$FEATURE_NAME"
```

## Sammanfattning

Effektiv versionhantering och kodstruktur bildar grunden för all framgångsrik Infrastructure as Code-implementation. Genom att använda Git-baserade workflows, modulär kodorganisation och automated review-processer kan svenska organisationer uppnå samma kvalitet och collaboration benefits för infrastrukturkod som för applikationskod.

Strukturerade approaches för branching, code review och state management säkerställer att infrastrukturändringar är spårbara, säkra och reproducerbara. Detta skapar förutsättningar för de avancerade automatiseringsprocesser som vi kommer att utforska i nästa kapitel om [CI/CD-pipelines](04_kapitel3.md).

Investment i proper versionhantering och kodstruktur från början av IaC-journey betalar sig genom reduced operational overhead, improved team collaboration och enhanced system reliability over time.

Källor:
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation.
- HashiCorp. "Terraform Team Collaboration." HashiCorp Learn Platform.
- AWS. "Infrastructure as Code Best Practices." Amazon Web Services Documentation.
- Google Cloud. "Terraform State Management." Google Cloud Architecture Center.
- Microsoft Azure. "Infrastructure as Code with Azure DevOps." Microsoft Documentation.