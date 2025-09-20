# Versionhantering och kodstruktur

Effektiv versionhantering utgör ryggraden i Infrastructure as Code-implementationer. Genom att tillämpa samma metoder som mjukvaruutveckling på infrastrukturdefinitioner skapas spårbarhet, samarbetsmöjligheter och kvalitetskontroll. Som vi diskuterade i [kapitel 2 om grundläggande principer](02_kapitel1.md), är systematisk hantering av infrastrukturkod en förutsättning för skalbar och tillförlitlig automatisering.

![Versionhantering och kodstruktur](images/diagram_03_kapitel2.png)

Diagrammet illustrerar det typiska flödet från Git repository genom branching strategy och code review till slutlig deployment, vilket säkerställer kontrollerad och spårbar infrastrukturutveckling. Detta flöde ligger till grund för den automatisering som vi kommer att fördjupa oss i [kapitel 4 om CI/CD-pipelines](04_kapitel3.md).

## Git-baserad arbetsflöde för infrastruktur

Git utgör standarden för versionhantering av IaC-kod och möjliggör distribuerat samarbete mellan team-medlemmar. Varje förändring dokumenteras med commit-meddelanden som beskriver vad som ändrats och varför, vilket skapar en komplett historik över infrastrukturutvecklingen.

### Branching-strategier för infrastruktukod

Svenska organisationer har adopterat flera beprövade branching-strategier som balanserar utvecklingshastighet med operational säkerhet. GitFlow och GitHub Flow representerar två huvudsakliga approaches, där val av strategi beror på organisationens mognad, team-storlek och risk-tolerans.

**GitFlow för stora organisationer** möjliggör parallell utveckling med separata branches för features, releases och hotfixes. Detta är särskilt värdefullt för svenska företag med komplex regulatory compliance där changes måste genomgå omfattande validering:

```bash
# GitFlow implementation för svenska organisationer
git flow init

# Skapa feature branch för ny infrastruktur-komponent
git flow feature start aws-vpc-upgrade

# Utveckla och testa infrastruktur-ändringar
terraform plan -var-file="environments/staging.tfvars"
terraform apply -var-file="environments/staging.tfvars"

# Validera svensk compliance
./scripts/validate-gdpr-compliance.sh
./scripts/check-data-residency.sh

# Slutför feature efter testing
git flow feature finish aws-vpc-upgrade

# Skapa release branch för production deployment
git flow release start v2.1.0

# Slutlig validering innan production
terraform plan -var-file="environments/production.tfvars"
./scripts/security-audit.sh
./scripts/cost-analysis.sh

# Release till production
git flow release finish v2.1.0
git push origin main
git push --tags
```

**GitHub Flow för agila team** erbjuder förenklad workflow med feature branches som mergas direkt till main efter code review. Detta passar mindre svenska team som prioriterar snabb iteration över formell process:

```bash
# GitHub Flow för svenska startup
git checkout main
git pull origin main

# Skapa feature branch
git checkout -b feature/kubernetes-monitoring

# Implementera infrastruktur-förändringar
cat > monitoring-stack.tf << EOF
# Prometheus och Grafana för svenska Kubernetes-miljö
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "monitoring"
  
  values = [
    file("${path.module}/monitoring-values.yaml")
  ]
  
  set {
    name  = "grafana.ingress.hosts[0]"
    value = "monitoring.svenska-startup.se"
  }
  
  set {
    name  = "grafana.adminPassword"
    value = var.grafana_admin_password
  }
}
EOF

# Commit och push
git add .
git commit -m "feat: lägg till Prometheus monitoring för K8s"
git push origin feature/kubernetes-monitoring

# Skapa pull request för code review
gh pr create --title "Prometheus monitoring setup" \
             --body "Implementerar comprehensive monitoring för Kubernetes-miljö"
```

### Commit-meddelanden och dokumentation

Strukturerade commit-meddelanden följer Conventional Commits-standarden anpassad för Infrastructure as Code context. Detta möjliggör automated changelog generation och semantic versioning av infrastructure components:

```bash
# Exempel på Infrastructure as Code commit-meddelanden

# Feature additions
git commit -m "feat(vpc): lägg till multi-AZ setup för Stockholm region

- Implementerar redundant VPC-konfiguration över 3 availability zones
- Lägger till NAT gateways för each AZ för improved availability  
- Konfigurerar route tables för optimal traffic routing
- Uppfyller svenska resilience-krav för kritisk infrastruktur

Breaking: Kräver migration av befintliga subnets"

# Bug fixes
git commit -m "fix(security-groups): stäng otillåten SSH-access från internet

- Tar bort 0.0.0.0/0 från SSH security group rules
- Begränsar SSH-access till VPN och bastion host ranges
- Uppfyller MSB säkerhetskrav för kritisk infrastruktur

Closes: SEC-2024-001"

# Configuration changes
git commit -m "config(rds): uppdatera backup retention för GDPR compliance

- Ökar RDS backup retention till 35 dagar
- Implementerar cross-region backup replication
- Aktiverar point-in-time recovery för production databaser
- Säkerställer data recovery capabilities enligt svenska regelverk"

# Documentation updates
git commit -m "docs(terraform): dokumentera svenska compliance-modules

- Lägger till usage examples för GDPR-compliance module
- Dokumenterar cost optimization för svenska marknaden
- Uppdaterar README med svenska security requirements"
```

### Tagging och versioning strategies

Infrastructure versioning följer semantic versioning (SemVer) principles anpassade för infrastructure context. Major versions indikerar breaking changes som kräver manual intervention, minor versions tillför ny functionality, och patch versions innehåller bugfixes och security updates:

```bash
# Semantic versioning för infrastructure components
git tag -a v1.0.0 -m "Initial production release av svenska VPC-module

Major components:
- Multi-AZ VPC setup för Stockholm region
- Security groups följer MSB säkerhetskrav  
- NAT gateways och internet gateway konfiguration
- Compliance med svenska data residency requirements"

git tag -a v1.1.0 -m "Lägg till monitoring och logging capabilities

New features:
- CloudWatch log aggregation för VPC Flow Logs
- SNS notifications för security group changes
- CloudTrail integration för audit logging
- Automated cost reporting för svenska kostnadsrapporter"

git tag -a v1.1.1 -m "Säkerhetsuppdatering för security groups

Fixes:
- Tar bort default outbound rules för database security groups
- Implementerar least privilege principle för application access
- Uppdaterar SSH access patterns för bastion hosts"
```

## Kodorganisation och modulstruktur

Välorganiserad kodstruktur är avgörande för maintainability och collaboration i större IaC-projekt. Modulär design möjliggör återanvändning av infrastrukturkomponenter across olika projekt och miljöer.

### Repository-struktur för svenska organisationer

Svenska företag har utvecklat beprövade patterns för Infrastructure as Code repository organization som balanserar team autonomy med operational governance:

```
svenska-infrastruktur-monorepo/
├── environments/                    # Environment-specific configurations
│   ├── development/
│   │   ├── terraform.tfvars        # Dev environment variables
│   │   ├── main.tf                 # Dev-specific resource definitions
│   │   └── outputs.tf              # Development output values
│   ├── staging/
│   │   ├── terraform.tfvars        # Staging environment variables
│   │   ├── main.tf                 # Staging-specific configuration
│   │   └── outputs.tf              # Staging output values
│   └── production/
│       ├── terraform.tfvars        # Production environment variables
│       ├── main.tf                 # Production infrastructure
│       └── outputs.tf              # Production output values
├── modules/                         # Reusable infrastructure modules
│   ├── svenska-vpc/                 # VPC module för svenska organisationer
│   │   ├── main.tf                 # VPC resource definitions
│   │   ├── variables.tf            # Input variables
│   │   ├── outputs.tf              # Output values
│   │   ├── versions.tf             # Provider version constraints
│   │   └── README.md               # Module documentation
│   ├── svenska-security-groups/    # Security groups med svenska compliance
│   │   ├── main.tf                 # Security group definitions
│   │   ├── gdpr-compliance.tf      # GDPR-specific rules
│   │   ├── msb-security.tf         # MSB säkerhetskrav implementation
│   │   └── variables.tf            # Configurable parameters
│   └── svenska-monitoring/         # Monitoring stack för svenska krav
│       ├── cloudwatch.tf          # CloudWatch konfiguration
│       ├── alerting.tf             # Alert rules för svenska arbetstider
│       └── dashboards.tf           # Grafana dashboards på svenska
├── shared/                          # Shared configuration och utilities
│   ├── providers.tf                # Common provider configurations
│   ├── data-sources.tf             # Shared data sources
│   └── locals.tf                   # Common local values
├── scripts/                         # Automation och validation scripts
│   ├── validate-compliance.sh      # GDPR och MSB compliance validation
│   ├── cost-analysis.py           # Cost optimization för svenska marknaden
│   ├── security-audit.sh          # Security assessment automation
│   └── backup-validation.py       # Backup verification för data protection
├── policies/                        # Policy as Code definitions
│   ├── opa/                        # Open Policy Agent policies
│   │   ├── gdpr-compliance.rego    # GDPR validation rules
│   │   ├── cost-control.rego       # Cost control policies
│   │   └── security-baseline.rego  # Security baseline enforcement
│   └── sentinel/                   # HashiCorp Sentinel policies
│       ├── mandatory-tags.sentinel # Obligatoriska tags för svenska org
│       └── region-restrictions.sentinel # Data residency enforcement
├── docs/                           # Documentation och runbooks
│   ├── svenska-compliance-guide.md # Compliance guide för svenska regler
│   ├── deployment-runbook.md       # Deployment procedures
│   ├── disaster-recovery.md        # Disaster recovery procedures
│   └── cost-optimization.md        # Cost optimization strategies
├── .github/                        # GitHub-specific configuration
│   ├── workflows/                  # CI/CD pipeline definitions
│   │   ├── terraform-plan.yml      # Terraform planning workflow
│   │   ├── terraform-apply.yml     # Terraform deployment workflow
│   │   ├── compliance-check.yml    # Automated compliance validation
│   │   └── cost-monitoring.yml     # Cost tracking och alerting
│   └── CODEOWNERS                  # Code ownership definitions
├── .gitignore                      # Git ignore patterns
├── README.md                       # Repository documentation
└── terraform.tf                    # Root Terraform configuration
```

### Module design principles för svenska miljöer

Svenska Infrastructure as Code modules följer etablerade design principles som säkerställer reusability, maintainability och compliance med lokala krav:

**Single Responsibility Principle** innebär att varje module har ett specifikt, väldefinierat ansvar. En VPC module hanterar endast network infrastructure, medan en security module fokuserar exclusively på säkerhetskonfiguration:

```hcl
# modules/svenska-vpc/main.tf
# VPC module med fokus på svenska compliance krav

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Huvudsaklig VPC resource
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(var.common_tags, {
    Name                  = "${var.environment}-svenska-vpc"
    DataResidency        = "Sweden"
    ComplianceFramework  = "GDPR,MSB"
    Environment          = var.environment
    CostCenter           = var.cost_center
  })
}

# Availability Zones för Stockholm region
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "region-name"
    values = ["eu-north-1"]  # Stockholm region
  }
}

# Public subnets för internet-facing resources
resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-public-subnet-${count.index + 1}"
    Type = "public"
    Tier = "dmz"
  })
}

# Private subnets för internal applications
resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-private-subnet-${count.index + 1}"
    Type = "private"
    Tier = "application"
  })
}

# Database subnets för sensitive data
resource "aws_subnet" "database" {
  count = length(var.database_subnet_cidrs)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.database_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-database-subnet-${count.index + 1}"
    Type = "database"
    Tier = "data"
    DataClassification = "sensitive"
  })
}

# Internet Gateway för public access
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-svenska-igw"
  })
}

# NAT Gateways för private subnet internet access
resource "aws_eip" "nat" {
  count = length(aws_subnet.public)
  
  domain = "vpc"
  depends_on = [aws_internet_gateway.main]
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-nat-eip-${count.index + 1}"
  })
}

resource "aws_nat_gateway" "main" {
  count = length(aws_subnet.public)
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-nat-gateway-${count.index + 1}"
  })
  
  depends_on = [aws_internet_gateway.main]
}

# Route tables för network traffic steering
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-public-rt"
    Type = "public"
  })
}

resource "aws_route_table" "private" {
  count = length(aws_nat_gateway.main)
  
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = merge(var.common_tags, {
    Name = "${var.environment}-private-rt-${count.index + 1}"
    Type = "private"
  })
}

# Route table associations
resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = length(aws_subnet.private)
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
```

### Configuration management patterns

Svenska organisationer använder flera patterns för configuration management som säkerställer consistency across environments samtidigt som flexibility bibehålls för environment-specific requirements:

**Environment-specific variable files** möjliggör samma infrastructure code att deployeras med olika configurations för development, staging och production:

```hcl
# environments/development/terraform.tfvars
# Development environment configuration för svenska organisation

# Basic environment settings
environment = "development"
project_name = "svenska-fintech-app"
cost_center = "innovation-lab"
owner_team = "platform-engineering"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]
private_subnet_cidrs = [
  "10.0.10.0/24",
  "10.0.11.0/24"
]
database_subnet_cidrs = [
  "10.0.20.0/24",
  "10.0.21.0/24"
]

# Instance configurations för development
instance_types = {
  web_servers = "t3.micro"
  app_servers = "t3.small"
  database = "db.t3.micro"
}

# Auto-scaling settings för development
auto_scaling = {
  min_size = 1
  max_size = 3
  desired_capacity = 1
}

# Monitoring och logging för development
monitoring = {
  detailed_monitoring = false
  log_retention_days = 7
  enable_xray = false
}

# Development-specific security settings
security = {
  enable_ssh_from_internet = true  # Only för development!
  enable_rdp_access = false
  require_mfa = false
}

# Data retention för development
data_retention = {
  database_backup_retention = 1  # days
  log_retention = 7  # days
  snapshot_retention = 3  # days
}

# Svenska compliance settings för development
compliance = {
  enable_gdpr_mode = true
  data_classification = "internal"
  require_encryption = true
  audit_logging = "basic"
}
```

```hcl
# environments/production/terraform.tfvars
# Production environment configuration för svenska organisation

# Basic environment settings
environment = "production"
project_name = "svenska-fintech-app"
cost_center = "core-platform"
owner_team = "platform-engineering"

# VPC Configuration för production scale
vpc_cidr = "10.100.0.0/16"
public_subnet_cidrs = [
  "10.100.1.0/24",
  "10.100.2.0/24",
  "10.100.3.0/24"
]
private_subnet_cidrs = [
  "10.100.10.0/24",
  "10.100.11.0/24",
  "10.100.12.0/24"
]
database_subnet_cidrs = [
  "10.100.20.0/24",
  "10.100.21.0/24",
  "10.100.22.0/24"
]

# Production instance configurations
instance_types = {
  web_servers = "c5.large"
  app_servers = "m5.xlarge"
  database = "db.r5.2xlarge"
}

# Production auto-scaling
auto_scaling = {
  min_size = 3
  max_size = 20
  desired_capacity = 6
}

# Production monitoring och logging
monitoring = {
  detailed_monitoring = true
  log_retention_days = 365
  enable_xray = true
  enable_enhanced_monitoring = true
}

# Production security settings
security = {
  enable_ssh_from_internet = false  # Säkert för production
  enable_rdp_access = false
  require_mfa = true
  enable_waf = true
  enable_shield_advanced = true
}

# Production data retention
data_retention = {
  database_backup_retention = 35  # days för GDPR compliance
  log_retention = 365  # days för audit trails
  snapshot_retention = 30  # days
}

# Fullständig svenska compliance för production
compliance = {
  enable_gdpr_mode = true
  data_classification = "restricted"
  require_encryption = true
  audit_logging = "comprehensive"
  enable_data_residency_enforcement = true
  require_approval_workflows = true
}
```

## Code review-processer för infrastruktur

Infrastructure code review kräver specialiserade approaches som adresserar säkerhet, cost implications, och operational impact beyond traditional software code review. Svenska organisationer har utvecklat comprehensive review processes som balanserar utvecklingshastighet med risk management.

### Pull request workflows för IaC

Strukturerade pull request workflows säkerställer att infrastructure changes genomgår appropriate validation before deployment:

```yaml
# .github/pull_request_template.md
## Infrastructure Change Request

### Beskrivning av förändringar
<!-- Beskriv vad som ändras och varför -->

### Miljöer som påverkas
- [ ] Development
- [ ] Staging  
- [ ] Production

### Typ av förändring
- [ ] Ny infrastruktur-komponent
- [ ] Konfigurationsändring
- [ ] Säkerhetsuppdatering
- [ ] Kostnadsoptimering
- [ ] Bug fix
- [ ] Breaking change

### Svenska compliance validering
- [ ] GDPR-påverkan utvärderad
- [ ] MSB säkerhetskrav validerade
- [ ] Data residency requirements uppfyllda
- [ ] Cost impact analyserad (SEK)

### Säkerhetskontroller
- [ ] Security groups granskade
- [ ] IAM permissions validerade
- [ ] Encryption aktiverad för sensitive data
- [ ] Network segmentation kontrollerad
- [ ] Audit logging konfigurerat

### Testing utfört
- [ ] Terraform plan granskat
- [ ] Security scan genomförd (checkov/tfsec)
- [ ] Cost estimation completed
- [ ] Manual testing i development environment
- [ ] Integration tests körda

### Deployment plan
- [ ] Deployment window identifierat
- [ ] Rollback plan dokumenterat
- [ ] Monitoring och alerting uppdaterat
- [ ] Documentation uppdaterad

### Reviewer checklist
- [ ] Code följer svenska naming conventions
- [ ] Resource tagging complete och korrekt
- [ ] Variable naming och documentation appropriate
- [ ] Module dependencies reasonable
- [ ] Output values well-defined

### Risk assessment
**Risk Level:** [ ] Low [ ] Medium [ ] High [ ] Critical

**Potential Impact:**
<!-- Beskriv potential impact på systems, users, costs -->

**Mitigation Strategies:**
<!-- Beskriv hur risks mitigeras -->
```

### Code review guidelines för svenska team

Svenska Infrastructure as Code teams följer etablerade guidelines som säkerställer consistency, quality och compliance:

```markdown
# Code Review Guidelines för Svenska IaC Teams

## Allmänna principer

### 1. Svenska språk conventions
- Kommentarer och documentation på svenska
- Resource names på engelska (för tool compatibility)
- Variable descriptions på svenska
- Commit messages på svenska

### 2. Resource naming standards
```hcl
# Korrekt resource naming för svenska organisationer
resource "aws_instance" "web_server" {
  # NOT: resource "aws_instance" "webbserver" (Swedish in resource name)
  
  tags = {
    Name = "svenska-org-web-server-prod"  # Svenskt prefix OK i tags
    Environment = "production"
    Project = "customer-portal"
    Owner = "platform-team"
    CostCenter = "infrastructure"
    DataClassification = "internal"
  }
}
```

### 3. Säkerhetskontroller som MÅSTE reviewas
- Inga hardcoded credentials eller API keys
- Security groups följer least privilege principle
- Database passwords stored i AWS Secrets Manager
- S3 buckets har appropriate access controls
- IAM roles följer principle of least privilege
- All data in transit och at rest encrypted

### 4. Cost optimization checkpoints
- Instance types appropriate för workload
- Auto-scaling configuration reasonable
- Storage classes optimized för usage patterns  
- Reserved instances considered för predictable workloads
- Spot instances used för fault-tolerant workloads

### 5. Svenska compliance specifics
- Personal data handling follows GDPR requirements
- Data residency enforced för svenska data
- Audit logging enabled för compliance reporting
- Backup retention follows svenska regulations
- Incident response procedures documented
```

### Automated validation i PR workflows

Automated tools integreras i pull request workflows för att catch common issues innan manual review:

```yaml
# .github/workflows/terraform-pr-validation.yml
name: Terraform PR Validation

on:
  pull_request:
    paths: ['**/*.tf', '**/*.tfvars']

jobs:
  validation:
    name: Terraform Validation
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
          
      - name: Terraform fmt check
        run: terraform fmt -check -recursive
        
      - name: Terraform init
        run: terraform init -backend=false
        
      - name: Terraform validate
        run: terraform validate
        
      - name: Security scan med tfsec
        uses: aquasecurity/tfsec-pr-commenter-action@v1.2.0
        with:
          github_token: ${{ github.token }}
          
      - name: Cost estimation
        uses: infracost/infracost-gh-action@v0.16
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
          
      - name: Compliance check för svenska regler
        run: |
          # Custom compliance validation script
          ./scripts/validate-swedish-compliance.sh
          
      - name: Plan för affected environments
        run: |
          for env in development staging production; do
            if terraform plan -var-file="environments/${env}/terraform.tfvars" -out="${env}.tfplan"; then
              echo "✅ Plan successful för ${env}"
              terraform show -json "${env}.tfplan" > "${env}-plan.json"
            else
              echo "❌ Plan failed för ${env}"
              exit 1
            fi
          done
          
      - name: Upload plans som artifacts
        uses: actions/upload-artifact@v3
        with:
          name: terraform-plans
          path: "*-plan.json"
```

## State management och collaboration

Terraform state management utgör en kritisk komponent för team collaboration och infrastructure consistency. Svenska organisationer kräver robust state management strategies som säkerställer säkerhet, backup capabilities och team access control.

### Remote state backends för svenska miljöer

S3-based remote state backends med DynamoDB locking provides robust foundation för team collaboration med svenska compliance considerations:

```hcl
# backend-config/production.tf
# Remote state configuration för svenska production environment

terraform {
  backend "s3" {
    bucket         = "svenska-org-terraform-state-prod"
    key            = "infrastructure/production/terraform.tfstate"
    region         = "eu-north-1"  # Stockholm region för data residency
    encrypt        = true
    kms_key_id     = "arn:aws:kms:eu-north-1:123456789012:key/12345678-1234-1234-1234-123456789012"
    dynamodb_table = "svenska-org-terraform-locks"
    
    # Access logging för audit compliance
    logging = {
      target_bucket = "svenska-org-audit-logs"
      target_prefix = "terraform-state-access/"
    }
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# State bucket med comprehensive security
resource "aws_s3_bucket" "terraform_state" {
  bucket = "svenska-org-terraform-state-prod"
  
  tags = {
    Purpose = "terraform-remote-state"
    Environment = "production"
    DataClassification = "internal"
    Backup = "critical"
  }
}

# Versioning för state recovery
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Encryption för data protection
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.terraform_state.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# KMS key för state encryption
resource "aws_kms_key" "terraform_state" {
  description             = "KMS key för Terraform state encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  
  tags = {
    Purpose = "terraform-state-encryption"
    Environment = "production"
  }
}

# DynamoDB table för state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "svenska-org-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  tags = {
    Purpose = "terraform-state-locking"
    Environment = "production"
  }
}
```

### Team access patterns och säkerhet

Infrastructure teams kräver structured access patterns som balanserar collaboration needs med security requirements:

```hcl
# iam-roles/terraform-team-access.tf
# IAM roles för svenska Terraform teams

# Platform Engineering team - full infrastructure access
resource "aws_iam_role" "platform_engineering" {
  name = "TerraformPlatformEngineering"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = [
            for user in var.platform_engineering_users :
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${user}"
          ]
        }
        Condition = {
          StringEquals = {
            "aws:RequestedRegion" = ["eu-north-1", "eu-west-1"]  # Begränsad till EU
          }
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"  # Kräver MFA
          }
        }
      }
    ]
  })
}

# Application teams - begränsad access till sina resources
resource "aws_iam_role" "application_team" {
  count = length(var.application_teams)
  name  = "TerraformTeam${var.application_teams[count.index].name}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = [
            for user in var.application_teams[count.index].members :
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${user}"
          ]
        }
        Condition = {
          StringEquals = {
            "aws:RequestedRegion" = ["eu-north-1"]  # Endast Stockholm för teams
          }
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"
          }
        }
      }
    ]
  })
}

# Read-only access för audit och monitoring
resource "aws_iam_role" "terraform_auditor" {
  name = "TerraformAuditor"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/AuditRole"
        }
      }
    ]
  })
}
```

## Praktiska exempel

### Komplett Git workflow implementation

Ett verkligt exempel på hur svenska organisationer implementerar end-to-end Git workflows för Infrastructure as Code, med omfattande automation och compliance validation.

Detta exempel visar en fullständig implementation av svenska compliance-krav integrerat i Git workflows för Infrastructure as Code development.

## Sammanfattning

Versionhantering och kodstruktur för Infrastructure as Code kräver samma rigor och systematik som modern mjukvaruutveckling, men med ytterligare hänsyn till svenska compliance-krav, cost implications och operational impact. Genom att implementera robusta Git workflows, modulär kodorganisation och comprehensive code review processes kan svenska organisationer uppnå både utvecklingshastighet och operational säkerhet.

Framgångsrik IaC versionhantering bygger på etablerade principer: tydlig branching strategy, automatiserad validation, comprehensive documentation och team collaboration practices. Som vi kommer att se i [nästa kapitel om CI/CD-pipelines](04_kapitel3.md), utgör dessa foundations grunden för automatiserad deployment och continuous delivery av infrastruktur.

Investering i proper versionhantering och kodstruktur ger compounding benefits över tid genom improved maintainability, reduced errors och faster delivery cycles. Svenska organisationer som implementerar dessa practices positionerar sig för sustainable infrastructure growth och effective team scaling.

## Källor och referenser

- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation.
- HashiCorp. "Terraform State Management Best Practices." Terraform Documentation, 2024.
- GitHub. "Infrastructure as Code Repository Patterns." GitHub Enterprise Documentation, 2024.
- AWS. "Multi-Account Strategy för Infrastructure as Code." AWS Well-Architected Framework, 2024.
- Microsoft. "Git Branching Strategies för Enterprise." Azure DevOps Documentation, 2024.
- NIST. "Configuration Management för Cybersecurity Framework." NIST Special Publication 800-53, 2024.