# Basic principles for Infrastructure as Code

Infrastructure as Code fundamentally transforms how we approach infrastructure management by applying software development principles to infrastructure provisioning and management. This chapter explores the core principles that make IaC effective and sustainable at enterprise scale.

![Basic principles for Infrastructure as Code](images/diagram_02_chapter1.png)

The diagram shows the fundamental flow from code through version control, automated testing, and deployment to infrastructure. This pipeline ensures that infrastructure changes follow the same rigor as application code changes.

## Declarative configuration

Declarative configuration represents one of the most important paradigm shifts in Infrastructure as Code. Instead of specifying step-by-step instructions for how to create infrastructure, declarative approaches describe the desired end state.

### Benefits of declarative approaches

**Idempotency**: Declarative configurations can be applied multiple times with the same result. Running the same configuration twice will not create duplicate resources or cause errors.

**State management**: Tools automatically determine what changes are needed to reach the desired state from the current state, handling complex dependency relationships.

**Self-healing**: Infrastructure can automatically correct drift from the desired state when monitoring and reconciliation loops are implemented.

### Implementation patterns

**Resource definitions**: Infrastructure components are defined as resources with properties rather than procedures.

```hcl
# Declarative Terraform configuration
resource "aws_instance" "web_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}
```

**Dependency management**: Tools automatically resolve dependencies between resources and create them in the correct order.

**State tracking**: Current infrastructure state is tracked and compared against desired state to determine necessary changes.

## Immutable infrastructure

Immutable infrastructure treats infrastructure components as immutable artifacts that are replaced rather than modified when changes are needed.

### Core concepts

**Replace, don't modify**: Instead of updating existing servers or components, create new ones with the desired configuration and decommission the old ones.

**Artifact-based deployment**: Infrastructure components are built as versioned artifacts (AMIs, container images, etc.) that can be deployed consistently.

**Stateless design**: Applications and services are designed to be stateless, with persistent data stored in external systems.

### Implementation patterns

**Golden images**: Create standardized machine images with all necessary software pre-installed and configured.

```dockerfile
# Immutable container image
FROM node:18-alpine

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
COPY public/ ./public/

# Build application
RUN npm run build

# Production stage - immutable runtime environment
FROM nginx:alpine
LABEL maintainer="ops@example.com"
LABEL version="${BUILD_VERSION}"
LABEL environment="production"

# Copy built application
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Security hardening
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx

# Set timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

EXPOSE 80
USER nginx

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

**Blue-green deployments**: Maintain two identical production environments and switch traffic between them for zero-downtime deployments.

**Canary releases**: Deploy new versions to a subset of infrastructure and gradually increase traffic based on success metrics.

## Security by design

Security must be integrated into Infrastructure as Code from the beginning rather than added as an afterthought.

### Security automation patterns

**Policy as Code**: Security policies are defined in code and automatically enforced across all infrastructure.

```yaml
# Open Policy Agent (OPA) security policy
package aws.security

deny[msg] {
    input.resource_type == "aws_s3_bucket"
    not input.encrypted
    msg := "S3 buckets must be encrypted"
}

deny[msg] {
    input.resource_type == "aws_security_group"
    input.ingress[_].cidr_blocks[_] == "0.0.0.0/0"
    msg := "Security groups must not allow unrestricted access"
}
```

**Automated security scanning**: Integration of security scanning tools into CI/CD pipelines to detect vulnerabilities and misconfigurations.

```yaml
# GitHub Actions security workflow
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Checkov
      uses: bridgecrewio/checkov-action@master
      with:
        directory: terraform/
        
    - name: Run tfsec
      uses: aquasecurity/tfsec-action@v1.0.0
      with:
        working_directory: terraform/
        
    - name: Run Terrascan
      run: |
        docker run --rm -v $(pwd):/src tenable/terrascan scan -i terraform -d /src
```

**Least Privilege by Default**: Implement minimal necessary permissions through Infrastructure as Code:

```hcl
# IAM roles with least privilege
resource "aws_iam_role" "app_role" {
  name = "app-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:RequestedRegion": ["us-west-2", "us-east-1"]
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "app_policy" {
  name = "app-execution-policy"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::app-bucket/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:*:*:secret:app/*"
      }
    ]
  })
}
```

## Testability and quality assurance

Infrastructure code must be thoroughly tested to ensure reliability and prevent production issues.

### Comprehensive testing strategy

**Unit tests**: Test individual infrastructure components in isolation.

**Integration tests**: Verify that multiple infrastructure components work together correctly.

**End-to-end tests**: Validate complete application functionality on provisioned infrastructure.

```go
// Terratest integration tests
package test

import (
    "testing"
    "time"
    
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/stretchr/testify/assert"
)

func TestInfrastructureIntegration(t *testing.T) {
    t.Parallel()
    
    // AWS region for testing
    awsRegion := "us-west-2"
    
    // Terraform options
    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../terraform/environments/integration",
        Vars: map[string]interface{}{
            "environment": "integration-test",
            "region":      awsRegion,
        },
    })
    
    // Clean up resources after test
    defer terraform.Destroy(t, terraformOptions)
    
    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)
    
    // Get outputs
    instanceId := terraform.Output(t, terraformOptions, "instance_id")
    publicIp := terraform.Output(t, terraformOptions, "public_ip")
    
    // Verify instance is running
    aws.GetInstancesByTag(t, awsRegion, "Environment", "integration-test")
    
    // Verify web service is accessible
    maxRetries := 30
    timeBetweenRetries := 5 * time.Second
    
    url := fmt.Sprintf("http://%s", publicIp)
    expectedStatus := 200
    
    http_helper.HttpGetWithRetry(
        t,
        url,
        nil,
        expectedStatus,
        "Service should be accessible",
        maxRetries,
        timeBetweenRetries,
    )
}
```

### Quality gates and validation

**Static analysis**: Analyze infrastructure code for potential issues without execution.

**Policy validation**: Ensure infrastructure configurations comply with organizational policies.

**Cost estimation**: Validate that infrastructure changes fall within budget constraints.

**Security scanning**: Automatically detect security vulnerabilities and misconfigurations.

## Version control integration

All infrastructure code must be stored in version control systems with proper branching strategies and code review processes.

### Git workflows for infrastructure

**Feature branches**: Develop infrastructure changes in isolated branches before merging.

**Pull request reviews**: Require code review and approval before infrastructure changes are deployed.

**Automated validation**: Run tests and validation checks on every pull request.

```yaml
# GitHub workflow for infrastructure validation
name: Infrastructure Validation
on:
  pull_request:
    paths:
      - 'terraform/**'
      - 'ansible/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
          
      - name: Terraform init
        run: terraform init -backend=false
        
      - name: Terraform validate
        run: terraform validate
        
      - name: Security scan
        uses: aquasecurity/tfsec-pr-commenter-action@v1.2.0
        with:
          github_token: ${{ github.token }}
          
      - name: Cost estimation
        uses: infracost/infracost-gh-action@v0.16
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
          
      - name: Plan for affected environments
        run: |
          for env in development staging production; do
            terraform plan -var-file="environments/${env}.tfvars" -out="${env}.tfplan"
          done
```

## Sources and references

- Fowler, Martin. "Infrastructure as Code." Martin Fowler's Blog.
- Kim, Gene, Jez Humble, Patrick Debois, and John Willis. "The DevOps Handbook."
- Morris, Kief. "Infrastructure as Code: Managing Servers in the Cloud."
- Terraform. "Terraform Best Practices." HashiCorp Documentation.
- AWS. "Infrastructure as Code Best Practices." AWS Documentation.
- Google Cloud. "Best Practices for Infrastructure as Code." Google Cloud Documentation.
- Microsoft. "Azure Resource Manager Best Practices." Microsoft Documentation.
- Cloud Native Computing Foundation. "Cloud Native Security Principles."
- Open Policy Agent. "Policy as Code Best Practices." OPA Documentation.
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation.