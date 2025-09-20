import os

def generate_iac_book_content_english():
    """
    Generates all markdown files for the English book 'Architecture as Code'
    Translation of the Swedish original with English terminology and examples
    """
    
    # Define directories
    output_dir = "english/docs"
    images_dir = os.path.join(output_dir, "images")
    
    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Book structure with all 23 files (English version)
    book_structure = [
        {
            "filename": "01_introduction.md",
            "title": "Introduction to Architecture as Code",
            "area": "Fundamental concepts",
            "mermaid_code": """graph LR
    A[Traditional infrastructure] --> B[Manual processes]
    C[Infrastructure as Code] --> D[Automated processes] 
    E[Code-based architecture] --> F[Scalable infrastructure]""",
            "content": """# Introduction to Architecture as Code

Infrastructure as Code (IaC) represents a fundamental shift in how we manage and develop IT infrastructure. By treating infrastructure as code, the same methodologies used in software development can be applied to infrastructure management. For organizations, this transformation brings not only technical benefits but also the ability to meet increasingly stringent compliance requirements and optimize costs in a competitive market.

![Introduction to Architecture as Code](images/diagram_01_introduction.png)

The diagram illustrates the transition from traditional manual processes to code-based automated solutions that enable scalable infrastructure. This progression from manual processes through Infrastructure as Code to fully automated and scalable infrastructure forms the foundation for modern digital transformation.

## Background and motivation

Infrastructure as Code emerged as a response to the challenges organizations faced with manual infrastructure management. Traditional methods involved high risk of human error, limited reproducibility, and difficulties handling complex environments at scale.

By codifying infrastructure definitions, organizations can achieve the same benefits that software development offers: version control, automated testing, continuous integration and deployment. This results in increased reliability, faster deliveries, and better traceability of changes.

### Challenges with traditional infrastructure management

Organizations have long struggled with the inherent problems of manual infrastructure administration. These challenges become particularly evident in an era where digital transformation drives increased demands for agility, security, and cost efficiency.

**Manual error sources and inconsistency** pose the greatest risks in traditional infrastructure management. Every manual configuration change introduces potential errors that can lead to system outages, security vulnerabilities, or performance issues. Financial institutions, for example, have reported that over 60% of critical incidents can be traced back to manual configuration errors.

**Scalability limitations** quickly become apparent when organizations grow or need to handle multiple environments. What works for a handful of servers becomes unsustainable when managing hundreds or thousands of resources across multiple data centers or cloud regions. E-commerce companies have been pioneers in addressing these challenges through early IaC implementations.

**Compliance and auditability** present growing challenges for organizations that must meet GDPR, financial regulations, and other compliance requirements. Traditional systems make it difficult to track what changes were made, when they were made, and by whom, complicating audit processes and risk management.

**Cost control and optimization** become problematic when infrastructure resources are provisioned manually without systematic monitoring or automated cost management. Without Infrastructure as Code, organizations lack tools to automatically optimize resource utilization based on actual usage.

### Drivers for IaC adoption

Organizations drive IaC adoption through several specific factors that reflect both local conditions and global trends:

**Regulatory requirements and compliance** have become increasingly stringent, particularly in financial services, healthcare, and public sector. GDPR implementation in 2018 accelerated the need for systematic infrastructure management that can demonstrate compliance through code and automation.

**IT operations talent shortage** forces organizations to automate routine tasks to free qualified personnel for more strategic work. System administrators and infrastructure engineers are among the most sought-after and hard-to-recruit roles in the market.

**Cloud adoption and hybrid cloud strategies** require new approaches to infrastructure management that can handle the complexity of multi-cloud and hybrid deployments. Cloud providers and their regional services drive this development.

**Digital innovation and time-to-market pressure** from both startups and established companies digitalizing their business models. Companies like Spotify, Uber, and Airbnb have demonstrated how IaC enables rapid scaling and innovation.

## Definition and scope

Infrastructure as Code is defined as the practice of managing and provisioning infrastructure through machine-readable code rather than manual processes or interactive configuration tools. This approach encompasses everything from servers and networks to databases and security policies.

IaC enables declarative description of desired infrastructure state, where tools automatically ensure that actual infrastructure matches the defined specification. This creates predictability and consistency across different environments and development stages.

### Fundamental principles for Infrastructure as Code

Infrastructure as Code builds on several fundamental principles that distinguish it from traditional approaches:

**Declarative over Imperative**: IaC focuses on describing *what* the infrastructure should contain rather than *how* it should be created. This enables the same code to be applied repeatedly to ensure consistent state, regardless of previous state.

**Version Control Everything**: All infrastructure definitions are stored in version control systems, enabling the same practices as software development: branching, merging, code review, and rollback capabilities.

**Immutable Infrastructure**: Instead of modifying existing infrastructure, IaC promotes creating new infrastructure instances and replacing old ones. This eliminates configuration drift and ensures consistency.

**Self-Service and Automation**: Teams can provision and manage their own infrastructure through code, reducing dependencies on operations teams and accelerating delivery cycles.

## Benefits and value proposition

Infrastructure as Code delivers measurable benefits across multiple dimensions of organizational performance:

### Technical benefits

**Reduced manual errors**: Automation eliminates human mistakes that commonly occur in manual configuration processes. Studies show up to 90% reduction in configuration-related incidents after IaC implementation.

**Faster deployment cycles**: Automated provisioning reduces infrastructure deployment time from weeks to minutes, enabling faster time-to-market for applications and services.

**Environment consistency**: Identical infrastructure can be created across development, testing, and production environments, eliminating "works on my machine" issues.

**Improved disaster recovery**: Infrastructure can be recreated quickly and consistently in case of failures, reducing recovery time objectives (RTO) and recovery point objectives (RPO).

### Business benefits

**Cost optimization**: Automated resource management enables dynamic scaling and resource optimization, typically reducing infrastructure costs by 20-40%.

**Increased agility**: Development teams can rapidly provision environments and experiment with new architectures without operational bottlenecks.

**Better compliance**: Automated compliance checks and audit trails provide continuous compliance monitoring and simplified regulatory reporting.

**Enhanced security**: Security policies can be embedded in code and consistently applied across all environments, reducing security vulnerabilities.

## Implementation approaches

Organizations can adopt Infrastructure as Code through various approaches depending on their current state, requirements, and constraints:

### Greenfield implementation

New projects and applications can be built with IaC from the beginning, providing the cleanest implementation path. This approach allows:

- Clean architecture design without legacy constraints
- Modern tooling and best practices from start
- Team training and skill development
- Proof of concept for broader organizational adoption

### Brownfield migration

Existing infrastructure can be gradually migrated to IaC through systematic approaches:

**Assessment and inventory**: Document existing infrastructure and identify migration priorities based on business value and technical complexity.

**Pilot projects**: Start with non-critical environments or specific application stacks to build experience and demonstrate value.

**Incremental migration**: Gradually move infrastructure components to code-based management while maintaining operational stability.

**Parallel operation**: Run traditional and IaC approaches in parallel during transition periods to minimize risk.

### Hybrid approaches

Many organizations adopt hybrid strategies that combine traditional and IaC approaches:

- Critical production systems remain manually managed during initial phases
- New development uses IaC exclusively
- Non-critical environments serve as testing grounds
- Gradual expansion based on success metrics

## Sources and references

- HashiCorp. "Infrastructure as Code in a Private or Public Cloud." HashiCorp Learn Documentation.
- Puppet. "2021 State of DevOps Report." Puppet Labs Annual Survey.
- AWS. "Infrastructure as Code Best Practices." Amazon Web Services Documentation.
- Microsoft. "Azure Resource Manager Templates." Microsoft Azure Documentation.
- Google Cloud. "Deployment Manager Fundamentals." Google Cloud Documentation.
- Terraform. "Terraform Best Practices Guide." HashiCorp Official Documentation.
- Ansible. "Ansible for Infrastructure as Code." Red Hat Documentation.
- Chef. "Infrastructure Automation Cookbook." Chef Software Documentation.
- Gartner. "Market Guide for Cloud Infrastructure as Code Tools." Gartner Research.
- Forrester. "The Forrester Wave: Infrastructure as Code Platforms." Forrester Research."""
        },
        
        # Chapter 2 - Basic principles
        {
            "filename": "02_chapter1.md",
            "title": "Basic principles for Infrastructure as Code",
            "area": "System development",
            "mermaid_code": """graph LR
    A[Code] --> B[Version Control]
    B --> C[Automated Testing]
    C --> D[Deployment]
    D --> E[Infrastructure]""",
            "content": """# Basic principles for Infrastructure as Code

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
RUN addgroup -g 1001 -S nginx && \\
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx

# Set timezone
RUN apk add --no-cache tzdata && \\
    cp /usr/share/zoneinfo/UTC /etc/localtime && \\
    echo "UTC" > /etc/timezone

EXPOSE 80
USER nginx

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
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
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation."""
        }
    ]
    
    # Create all markdown files
    markdown_files = []
    mermaid_files = []
    
    for item_data in book_structure:
        filename = item_data["filename"]
        content = item_data["content"]
        mermaid_code = item_data.get("mermaid_code")
        
        print(f"Creating {filename}...")
        
        # Handle Mermaid diagrams if they exist
        if mermaid_code:
            image_name_base = f"diagram_{filename.split('.')[0]}"
            mermaid_file = os.path.join(images_dir, f"{image_name_base}.mmd")
            
            with open(mermaid_file, "w", encoding="utf-8") as f:
                f.write(mermaid_code.strip())
            
            mermaid_files.append(mermaid_file)
            print(f"Mermaid diagram saved to {mermaid_file}")
        
        # Create markdown file
        markdown_path = os.path.join(output_dir, filename)
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        markdown_files.append(markdown_path)
        print(f"Chapter saved to {markdown_path}")
    
    print(f"\nBook generation completed!")
    print(f"Created {len(markdown_files)} markdown files")
    print(f"Created {len(mermaid_files)} Mermaid diagrams")
    print(f"\nFiles created in: {output_dir}")

if __name__ == "__main__":
    generate_iac_book_content_english()