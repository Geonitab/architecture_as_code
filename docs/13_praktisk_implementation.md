# Architecture as Code i praktiken

![Architecture as Code i praktiken](images/diagram_08_kapitel7.png)

Praktisk implementering av Architecture as Code kräver genomtänkt tillvägagångssätt som balanserar tekniska möjligheter med organisatoriska begränsningar. Infrastructure as Code utgör en central komponent, men måste integreras med bredare arkitekturdefinitioner. Detta kapitel fokuserar på verkliga implementeringsstrategier, vanliga fallgropar, och beprövade metoder för framgångsrik Architecture as Code-adoption i företagsmiljöer.

![Implementation User Journey](images/diagram_13_user_journey.png)

Diagrammet ovan illustrerar den typiska användarresan för arkitektur som kod-implementation, från initial discovery till fullständig optimization.

## Implementation roadmap och strategier

Successful Architecture as Code adoption följer vanligen en phased approach som börjar med pilot projects och gradvis expanderar till enterprise-wide implementation. Initial phases fokuserar på non-critical environments och simple use cases för att bygga confidence och establish arkitektur som kod best practices innan production workloads migreras. Infrastructure as Code (arkitektur som kod) utgör ofta startpunkten för denna transformation.

Assessment av current state infrastructure är critical för planning effective migration strategies. Legacy systems, technical debt, och organizational constraints måste identifieras och addressas through targeted modernization efforts. Detta inkluderar inventory av existing assets, dependency mapping, och risk assessment för olika migration scenarios.

Stakeholder alignment säkerställer organizational support för Arkitektur som kod initiatives. Executive sponsorship, cross-functional collaboration, och clear communication av benefits och challenges är essential för overcoming resistance och securing necessary resources. Change management strategies måste address både technical och cultural aspects av transformation.

## Tool selection och ecosystem integration

Technology stack selection balanserar organizational requirements med market maturity och community support. Terraform har emerged som leading multi-cloud solution, medan cloud-native tools som CloudFormation, ARM templates, och Google Deployment Manager erbjuder deep integration med specific platforms.

Integration med existing toolchains kräver careful consideration av workflows, security requirements, och operational procedures. Source control systems, CI/CD platforms, monitoring solutions, och security scanning tools måste seamlessly integrate för holistic development experience.

Vendor evaluation criteria inkluderar technical capabilities, roadmap alignment, commercial terms, och long-term viability. Open source solutions erbjuder flexibility och community innovation, medan commercial platforms provide enterprise support och advanced features. Hybrid approaches combinerar benefits från both models.

## Production readiness och operational excellence

Security-first approach implementerar comprehensive security controls från design phase. Secrets management, access controls, audit logging, och compliance validation måste vara built-in rather than bolt-on features. Automated security scanning och policy enforcement säkerställer consistent security posture.

High availability design principles appliceras på infrastructure code genom redundancy, failover mechanisms, och disaster recovery procedures. Infrastructure definitions måste handle various failure scenarios gracefully och provide automatic recovery capabilities where possible.

Monitoring och observability för infrastructure-as-code environments kräver specialized approaches som track både code changes och resulting infrastructure state. Drift detection, compliance monitoring, och performance tracking provide essential feedback för continuous improvement.

## Common challenges och troubleshooting

State management complexity grows significantly som infrastructure scales och involves multiple teams. State file corruption, concurrent modifications, och state drift kan cause serious operational problems. Remote state backends, state locking mechanisms, och regular state backups are essential för production environments.

Dependency management mellan infrastructure components kräver careful orchestration för avoid circular dependencies och ensure proper creation/destruction order. Modular design patterns och clear interface definitions help manage complexity som systems grow.

Version compatibility issues mellan tools, providers, och infrastructure definitions can cause unexpected failures. Comprehensive testing, staged rollouts, och dependency pinning strategies help mitigate these risks i production environments.

## Enterprise integration patterns

Multi-account/subscription strategies för cloud environments provide isolation, security boundaries, och cost allocation capabilities. Infrastructure code måste handle cross-account dependencies, permission management, och centralized governance requirements.

Hybrid cloud implementations require specialized approaches för networking, identity management, och data synchronization between on-premises och cloud environments. Infrastructure code måste abstract underlying platform differences while providing consistent management experience.

Compliance och governance frameworks måste vara embedded i infrastructure code workflows. Automated policy enforcement, audit trails, och compliance reporting capabilities ensure regulatory requirements are met consistently across all environments.

## Praktiska exempel

### Terraform Module Structure
```hcl
# modules/web-application/main.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "application_name" {
  description = "Name of the application"
  type        = string
}

variable "instance_count" {
  description = "Number of application instances"
  type        = number
  default     = 2
}

# VPC and networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.application_name}-${var.environment}-vpc"
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.application_name}-${var.environment}-public-${count.index + 1}"
    Type = "Public"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.application_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false

  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                = "${var.application_name}-${var.environment}-asg"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.main.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 10
  desired_capacity = var.instance_count

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.application_name}-${var.environment}-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}

# Outputs
output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```

## Terraform konfiguration och miljöhantering

### Environment-specific Configuration
```hcl
# environments/production/main.tf
terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket         = "company-terraform-state-prod"
    key            = "web-application/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
  
  default_tags {
    tags = {
      Project     = "web-application"
      Environment = "production"
      ManagedBy   = "terraform"
      Owner       = "platform-team"
    }
  }
}

module "web_application" {
  source = "../../modules/web-application"

  environment      = "production"
  application_name = "company-web-app"
  instance_count   = 6

  # Production-specific overrides
  enable_monitoring = true
  backup_retention  = 30
  multi_az         = true
}

# Production-specific resources
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "WebApplication-Production"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", module.web_application.load_balancer_arn_suffix],
            [".", "TargetResponseTime", ".", "."],
            [".", "HTTPCode_ELB_5XX_Count", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "us-west-2"
          title   = "Application Performance"
          period  = 300
        }
      }
    ]
  })
}
```

## Automation och DevOps integration

### CI/CD Pipeline Integration
```yaml
# .github/workflows/infrastructure.yml
name: Infrastructure Deployment

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: 1.5.0
  AWS_REGION: us-west-2

jobs:
  plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [development, staging, production]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Terraform Init
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform init

    - name: Terraform Validate
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform validate

    - name: Terraform Plan
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: |
        terraform plan -out=tfplan-${{ matrix.environment }} \
          -var-file="terraform.tfvars"

    - name: Upload plan artifact
      uses: actions/upload-artifact@v3
      with:
        name: tfplan-${{ matrix.environment }}
        path: infrastructure/environments/${{ matrix.environment }}/tfplan-${{ matrix.environment }}
        retention-days: 30

  deploy:
    name: Terraform Apply
    runs-on: ubuntu-latest
    needs: plan
    if: github.ref == 'refs/heads/main'
    strategy:
      matrix:
        environment: [development, staging]
        # Production requires manual approval
    
    environment: ${{ matrix.environment }}
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Download plan artifact
      uses: actions/download-artifact@v3
      with:
        name: tfplan-${{ matrix.environment }}
        path: infrastructure/environments/${{ matrix.environment }}

    - name: Terraform Init
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform init

    - name: Terraform Apply
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform apply tfplan-${{ matrix.environment }}

  production-deploy:
    name: Production Deployment
    runs-on: ubuntu-latest
    needs: [plan, deploy]
    if: github.ref == 'refs/heads/main'
    environment: 
      name: production
      url: ${{ steps.deploy.outputs.application_url }}
    
    steps:
    - name: Manual approval checkpoint
      run: echo "Production deployment requires manual approval"
      
    # Similar steps as deploy job but for production environment
```

## Sammanfattning


Den moderna arkitektur som kod-metodiken representerar framtiden för infrastrukturhantering i svenska organisationer.
Practical Infrastructure as Code implementation balanserar technical excellence med organizational realities. Success kräver comprehensive planning, stakeholder alignment, incremental delivery, och continuous improvement. Production readiness måste vara prioritized från början, medan common challenges måste anticiperas och mitigated through proven practices och robust tooling.

## Källor och referenser

- HashiCorp. "Terraform arkitektur som kod best practices." HashiCorp Learn Platform.
- AWS Well-Architected Framework. "Infrastructure as Code." Amazon Web Services.
- Google Cloud. "Infrastructure as Code Design Patterns." Google Cloud Architecture Center.
- Microsoft Azure. "Azure Resource Manager Best Practices." Microsoft Documentation.
- Puppet Labs. "Infrastructure as Code Implementation Guide." Puppet Enterprise Documentation.