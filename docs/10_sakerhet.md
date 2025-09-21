# Säkerhet i Infrastructure as Code

Säkerhet som kod (Security as Code) integrerar säkerhetspraktiker direkt i Infrastructure as Code-definitioner och automatiserar säkerhetskontroller genom hela utvecklingslivscykeln. Detta kapitel utforskar hur säkerhet kan kodifieras och automatiseras för robust cybersäkerhet.

![Säkerhet i Infrastructure as Code](images/diagram_10_sakerhet.png)

*Security as Code integrerar säkerhetspolicies, access controls och threat detection i infrastructure definitions för proaktiv och automatiserad säkerhetshantering.*

## Grundprinciper för Security as Code

Security as Code bygger på shift-left security principles där säkerhetskontroller implementeras tidigt i utvecklingsprocessen genom kodifierade policyer, automatiserad scanning och continuous security monitoring.

Säkerhet integreras som en naturlig del av Infrastructure as Code snarare än som efterhandskontroller, vilket möjliggör proaktiv riskhantering och compliance automation.

## Infrastructure security policies

Säkerhetspolicyer kodifieras genom policy-as-code verktyg som Open Policy Agent (OPA), AWS Config Rules och Azure Policy för automatisk enforcement av säkerhetsstandarder.

```rego
# OPA Rego policy för Kubernetes säkerhet
package kubernetes.security

# Deny containers running as root
deny[msg] {
    input.kind == "Pod"
    input.spec.containers[_].securityContext.runAsUser == 0
    msg := "Container must not run as root user"
}

# Require security context
deny[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.securityContext
    msg := "Container must define securityContext"
}

# Require resource limits
deny[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.resources.limits
    msg := "Container must define resource limits"
}

# Prohibit privileged containers
deny[msg] {
    input.kind == "Pod"
    input.spec.containers[_].securityContext.privileged == true
    msg := "Privileged containers are prohibited"
}
```

## Identity and Access Management (IAM) som kod

IAM-konfigurationer definieras genom Infrastructure as Code för konsistent access control, role-based permissions och least-privilege principles across olika miljöer och resurser.

```yaml
# AWS IAM policy som Terraform
resource "aws_iam_role" "application_role" {
  name = "application-${var.environment}-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

resource "aws_iam_policy" "application_policy" {
  name        = "application-${var.environment}-policy"
  description = "IAM policy for application access"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = [
          aws_kms_key.application_key.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "application_attachment" {
  role       = aws_iam_role.application_role.name
  policy_arn = aws_iam_policy.application_policy.arn
}
```

## Network security som kod

Network security policies, firewalls, VPNs och micro-segmentation definieras genom Infrastructure as Code för konsistent nätverkssäkerhet och traffic control.

```hcl
# Network Security Groups som Terraform
resource "aws_security_group" "web_tier" {
  name_prefix = "web-tier-${var.environment}"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "web-tier-${var.environment}"
    Environment = var.environment
    Tier        = "web"
  }
}

resource "aws_security_group" "app_tier" {
  name_prefix = "app-tier-${var.environment}"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "Application port"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web_tier.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "app-tier-${var.environment}"
    Environment = var.environment
    Tier        = "application"
  }
}
```

## Secrets management som kod

Secrets management integreras med Infrastructure as Code genom encrypted storage, rotation policies och access controls för känslig information som passwords, API keys och certificates.

```yaml
# Kubernetes Secrets management
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-west-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: prod/database
      property: username
  - secretKey: password
    remoteRef:
      key: prod/database
      property: password
```

## Compliance automation

Compliance frameworks som GDPR, ISO 27001 och SOC 2 implementeras genom automatiserade kontroller och audit trails definierade som Infrastructure as Code.

## Security scanning och vulnerability management

Automated security scanning integreras i CI/CD pipelines för Infrastructure as Code med verktyg som Checkov, Trivy och Snyk för continuous vulnerability assessment.

```yaml
# Security scanning pipeline
name: Security Scan
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Checkov
      uses: bridgecrewio/checkov-action@master
      with:
        directory: infrastructure/
        framework: terraform
        output_format: cli,sarif
        output_file_path: reports/checkov.sarif
        
    - name: Run Trivy
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: config
        scan-ref: infrastructure/
        format: sarif
        output: trivy-results.sarif
        
    - name: Upload results to GitHub Security
      uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: reports/
```

## Incident response automation

Security incident response automation kodifieras genom runbooks, automated remediation och escalation procedures för snabb response på security threats.

## Sammanfattning

Säkerhet i Infrastructure as Code möjliggör proaktiv, automatiserad och konsistent säkerhetshantering. Genom att kodifiera säkerhetspolicyer och kontroller uppnås robust cybersäkerhet och compliance automation.

Källor:
- NIST Cybersecurity Framework. National Institute of Standards and Technology, 2024.
- OWASP. "Infrastructure as Code Security Best Practices." OWASP, 2024.
- CIS Controls. Center for Internet Security, 2024.
- AWS Security Best Practices. Amazon Web Services, 2024.