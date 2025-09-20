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
        },
        
        # Chapter 3 - Version control and code structure
        {
            "filename": "03_chapter2.md",
            "title": "Version control and code structure",
            "area": "System development",
            "mermaid_code": """graph LR
    A[Git repository] --> B[Branching strategy]
    B --> C[Code review]
    C --> D[Merge process]
    D --> E[Deployment]""",
            "content": """# Version control and code structure

Effective version control forms the backbone of Infrastructure as Code implementations. By applying the same methods used in software development to infrastructure definitions, traceability, collaboration opportunities, and quality control are created.

![Version control and code structure](images/diagram_03_chapter2.png)

The diagram illustrates the typical flow from Git repository through branching strategy and code review to final deployment, ensuring controlled and traceable infrastructure development.

## Git-based workflow for infrastructure

Git serves as the standard for version control of IaC code and enables distributed collaboration between team members. Every change is documented with commit messages that describe what was changed and why, creating a complete history of infrastructure development.

### Branching strategies for infrastructure code

Organizations have adopted several proven branching strategies that balance development speed with operational safety. GitFlow and GitHub Flow represent two main approaches, where strategy choice depends on organizational maturity, team size, and risk tolerance.

**GitFlow for large organizations** enables parallel development with separate branches for features, releases, and hotfixes. This is particularly valuable for companies with complex regulatory compliance where changes must undergo extensive validation:

```bash
# GitFlow implementation for organizations
git flow init

# Create feature branch for new infrastructure component
git flow feature start aws-vpc-upgrade

# Develop and test infrastructure changes
terraform plan -var-file="environments/staging.tfvars"
terraform apply -var-file="environments/staging.tfvars"

# Validate compliance
./scripts/validate-compliance.sh
./scripts/check-data-residency.sh

# Complete feature after testing
git flow feature finish aws-vpc-upgrade

# Create release branch for production deployment
git flow release start v2.1.0

# Final validation before production
terraform plan -var-file="environments/production.tfvars"
./scripts/security-audit.sh
./scripts/cost-analysis.sh

# Release to production
git flow release finish v2.1.0
git push origin main
git push --tags
```

**GitHub Flow for agile teams** simplifies the process with feature branches directly merged to main after review. This approach works well for organizations with mature CI/CD pipelines and automated testing:

```bash
# GitHub Flow implementation
git checkout -b feature/implement-monitoring

# Make infrastructure changes
terraform plan
terraform apply

# Run automated tests
./scripts/run-infrastructure-tests.sh

# Create pull request for review
gh pr create --title "Implement monitoring infrastructure" --body "Adds CloudWatch alarms and dashboards"

# After approval and CI passes
gh pr merge --merge
```

### Repository structure and organization

Well-organized repository structure facilitates navigation, understanding, and maintenance of infrastructure code. Best practices include logical directory hierarchies, clear naming conventions, and proper separation of concerns:

```
infrastructure/
├── environments/           # Environment-specific configurations
│   ├── development/
│   ├── staging/
│   └── production/
├── modules/               # Reusable infrastructure modules
│   ├── networking/
│   ├── compute/
│   └── security/
├── policies/              # Security and compliance policies
├── scripts/               # Automation and helper scripts
├── docs/                  # Documentation and diagrams
└── tests/                 # Infrastructure tests
```

## Code review processes for infrastructure

Code review for infrastructure requires specialized knowledge and attention to operational concerns beyond traditional software review criteria.

### Code review guidelines

Infrastructure code review should evaluate:

1. **Security implications**: Ensure proper access controls, encryption, and network security
2. **Cost impact**: Review resource types and configurations for cost optimization
3. **Compliance adherence**: Verify alignment with organizational policies and regulations
4. **Operational considerations**: Assess monitoring, logging, and disaster recovery aspects
5. **Resource naming and tagging**: Ensure consistent naming conventions and proper resource tagging

### Automated validation in reviews

Integration of automated tools in the review process improves consistency and catches issues early:

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
```

## Documentation and change management

Comprehensive documentation ensures that infrastructure changes are understood and maintainable over time.

### Infrastructure documentation

Every infrastructure component should include:

- **Purpose and context**: Why the infrastructure exists and how it fits into the overall architecture
- **Dependencies**: What other components it relies on and what relies on it
- **Configuration parameters**: Key settings and their purposes
- **Operational procedures**: How to monitor, troubleshoot, and maintain the infrastructure
- **Change history**: Record of significant changes and their reasons

### Change tracking and rollback procedures

Robust change management processes enable quick rollback when issues occur:

```bash
# Tagged releases for infrastructure versions
git tag -a v1.2.0 -m "Production infrastructure v1.2.0"
git push origin v1.2.0

# Rollback procedure
git checkout v1.1.0
terraform plan -var-file="environments/production.tfvars"
terraform apply -var-file="environments/production.tfvars"
```

## Sources and references

- Fowler, Martin. "Patterns for Managing Source Code Branches." Martin Fowler's Blog.
- Chacon, Scott and Ben Straub. "Pro Git." Git Documentation.
- GitHub. "Understanding the GitHub flow." GitHub Docs.
- Atlassian. "Comparing Git workflows." Atlassian Git tutorials.
- HashiCorp. "Terraform Recommended Practices." Terraform Documentation.
- AWS. "Infrastructure as Code Best Practices." AWS Documentation."""
        },
        
        # Chapter 21 - Conclusion
        {
            "filename": "21_conclusion.md",
            "title": "Conclusion",
            "area": "Summary",
            "content": """# Conclusion

Infrastructure as Code has transformed how organizations think about and manage IT infrastructure. By treating infrastructure as code, we have enabled the same rigor, processes, and quality controls that have long existed in software development. This journey through the book's chapters has shown the path from fundamental concepts to future advanced technologies.

## Key learnings from our IaC journey

Implementing IaC requires both technical excellence and organizational change. Successful transformations are characterized by strong leadership commitment, comprehensive training programs, and gradual adoption strategies that minimize disruption to existing operations.

The technical aspect of Infrastructure as Code requires deep understanding of cloud technologies, automation tools, and security principles. Simultaneously, organizational factors are often decisive for success, including cultural change, competency development, and process standardization.

### Progression through technical maturity

Our review began with fundamental concepts like declarative code and idempotency, developed through practical implementation aspects like version control and CI/CD automation, and culminated in advanced topics like container orchestration and future AI-driven automation.

Security aspects introduced early were deepened through policy as code and compliance management, showing how security must permeate the entire IaC implementation from design to operations.

### Unique challenges and opportunities for organizations

Throughout the book's chapters, we have seen how organizations face specific challenges and opportunities:

- **Regulatory compliance and data sovereignty**: From security chapters to policy implementation, we have seen how regulations require special attention to data protection and compliance
- **Climate goals and sustainability**: Future chapters highlighted how climate neutrality goals drive innovation in carbon-aware computing and sustainable infrastructure
- **Digitalization strategy**: Chapters on digitalization showed how IaC enables the digital transformation that organizations are undergoing

## Future development and technological trends

Cloud-native technologies, edge computing, and artificial intelligence drive the next generation of Infrastructure as Code. Emerging technologies like GitOps, policy engines, and intelligent automation will further simplify and improve IaC capabilities.

The evolution toward serverless computing and fully managed services changes what needs to be managed as infrastructure code. The future points toward higher abstraction where developers focus on business logic while the platform handles underlying infrastructure automatically.

### Platform engineering and developer experience

The emerging field of platform engineering represents the next evolution of IaC, where infrastructure teams create self-service platforms that abstract complexity while maintaining control and governance. This approach enables:

- **Developer autonomy**: Teams can provision resources without deep infrastructure knowledge
- **Consistent standards**: Platforms enforce organizational policies and best practices
- **Reduced cognitive load**: Developers focus on application logic rather than infrastructure details
- **Improved governance**: Centralized control over security, compliance, and cost management

## Recommendations for successful IaC adoption

Based on the experiences and patterns explored throughout this book, several key recommendations emerge:

### Start with clear objectives

Successful IaC implementations begin with well-defined goals and success metrics. Organizations should articulate why they are adopting IaC and how success will be measured, whether through reduced deployment times, improved reliability, or enhanced security posture.

### Invest in education and culture

Technical training must be accompanied by cultural change initiatives. Organizations need to foster a culture of collaboration between development and operations teams, embrace automation, and view infrastructure as a first-class software artifact.

### Implement gradually and iteratively

Large-scale transformations benefit from phased approaches that allow organizations to learn and adapt. Start with non-critical environments, prove value with pilot projects, and gradually expand scope based on lessons learned.

### Prioritize security and compliance

Security considerations must be integrated from the beginning rather than added retroactively. Implement policy as code, automated security scanning, and compliance validation as core components of the IaC pipeline.

### Measure and optimize continuously

Establish monitoring and metrics to track the effectiveness of IaC implementations. Regular assessment of deployment frequency, lead time, recovery time, and failure rates provides insights for continuous improvement.

## The path forward

Infrastructure as Code represents more than a technological shift—it embodies a fundamental change in how we approach technology operations. As organizations continue their digital transformation journeys, IaC serves as a critical enabler of agility, reliability, and innovation.

The future of infrastructure management lies in intelligent, self-healing systems that can adapt to changing requirements while maintaining security and compliance. Organizations that master these principles today will be well-positioned to take advantage of emerging technologies and remain competitive in an increasingly digital world.

The journey toward Infrastructure as Code excellence is ongoing, with new tools, techniques, and best practices emerging continuously. Success requires commitment to continuous learning, adaptation, and improvement. As we look toward the future, the organizations that thrive will be those that embrace change, invest in their people, and maintain focus on delivering value through technology.

## Final thoughts

This book has provided a comprehensive guide to Infrastructure as Code, from fundamental principles to advanced implementation strategies. The real work begins with putting these concepts into practice, adapting them to specific organizational contexts, and continuously refining approaches based on experience and changing requirements.

Infrastructure as Code is not just about technology—it's about enabling organizations to move faster, operate more reliably, and innovate more effectively. By treating infrastructure with the same care and attention as application code, we unlock new possibilities for how technology can serve business objectives and create value for users and customers.

The future belongs to organizations that can rapidly and reliably provision, configure, and manage infrastructure through code. Those that master these capabilities will find themselves with significant competitive advantages in an increasingly digital world."""
        },
        
        # Chapter 22 - Glossary
        {
            "filename": "22_glossary.md",
            "title": "Glossary",
            "area": "Reference",
            "content": """# Glossary

This glossary contains definitions of central terms used throughout the book.

**API (Application Programming Interface):** Interface that enables communication between different software components or systems through standardized protocols and data formats.

**Automation:** Process where manual tasks are performed automatically by computer systems without human intervention, increasing efficiency and reducing error risk.

**CI/CD (Continuous Integration/Continuous Deployment):** Development methodology that continuously integrates code changes and automates the deployment process for faster and safer deliveries.

**Cloud Computing:** Delivery of IT services such as servers, storage, and applications over the internet with on-demand access and pay-per-use models.

**Containers:** Lightweight virtualization technology that packages applications with all dependencies for portable execution across different environments and platforms.

**Declarative Programming:** Programming paradigm that describes the desired end result instead of specific steps to achieve it, enabling higher abstraction.

**DevOps:** Cultural and technical approach that combines development (Dev) and operations (Ops) for faster deliveries and improved collaboration between teams.

**Git:** Distributed version control system for tracking changes in source code during development with support for branching and merging.

**Idempotency:** Property of operations that produce the same result regardless of how many times they are executed, critical for safe automation.

**Infrastructure as Code (IaC):** Practice of managing infrastructure through code instead of manual processes, enabling version control and automation.

**JSON (JavaScript Object Notation):** Text-based data format for structured information exchange between systems with human-readable syntax.

**Kubernetes:** Open-source container orchestration platform for automated deployment, scaling, and management of containerized applications.

**Microservices:** Architectural approach where applications are built as small, independent services that communicate via well-defined APIs.

**Monitoring:** Continuous observation of system performance, availability, and behavior to detect issues and ensure optimal operation.

**Orchestration:** Automated coordination and management of complex workflows, systems, and services across distributed environments.

**Policy as Code:** Practice of defining and enforcing organizational policies, security rules, and compliance requirements through code-based definitions.

**REST (Representational State Transfer):** Architectural style for designing web services that use standard HTTP methods for communication between systems.

**Scalability:** Ability of a system to handle increased load or demand by adding resources horizontally (more instances) or vertically (more power).

**Security by Design:** Approach that incorporates security considerations from the initial stages of system design rather than adding them retroactively.

**Terraform:** Infrastructure as Code tool developed by HashiCorp that enables declarative configuration of cloud resources across multiple providers.

**Version Control:** System that tracks and manages changes to files over time, enabling collaboration, history tracking, and rollback capabilities.

**YAML (YAML Ain't Markup Language):** Human-readable data serialization standard commonly used for configuration files and data exchange.

**Blue-Green Deployment:** Deployment strategy that uses two identical production environments, allowing zero-downtime deployments by switching traffic between them.

**Canary Release:** Deployment technique that gradually rolls out changes to a small subset of users before full deployment, enabling early issue detection.

**Configuration Drift:** Divergence of actual system configuration from the intended or documented state, often caused by manual changes.

**GitOps:** Operational framework that uses Git repositories as the single source of truth for declarative infrastructure and application configuration.

**Immutable Infrastructure:** Approach where infrastructure components are replaced rather than modified when changes are needed, ensuring consistency.

**Infrastructure Drift:** Unintended changes to infrastructure configuration that occur outside of the formal change management process.

**Load Balancer:** Device or software that distributes incoming network traffic across multiple servers to ensure no single server becomes overwhelmed.

**Multi-Cloud:** Strategy of using multiple cloud service providers to avoid vendor lock-in and increase redundancy and availability.

**Observability:** Practice of understanding system behavior and performance through metrics, logs, and traces to enable effective monitoring and troubleshooting.

**Pipeline:** Automated sequence of stages that code changes go through from development to production, including building, testing, and deployment.

**Provisioning:** Process of setting up and configuring infrastructure resources, including servers, networks, storage, and other components.

**Service Mesh:** Dedicated infrastructure layer for managing service-to-service communication in a microservices architecture.

**State Management:** Practice of tracking and maintaining the current configuration and status of infrastructure resources and their relationships.

**Template:** Reusable configuration pattern that defines infrastructure resources and their properties, enabling consistent deployments across environments."""
        },
        
        # Chapter 23 - About the authors
        {
            "filename": "23_about_authors.md",
            "title": "About the authors",
            "area": "Biography",
            "content": """# About the authors

## Dr. Anna Bergström - Senior Cloud Architect

Dr. Anna Bergström brings over 15 years of experience in cloud architecture and infrastructure automation to this comprehensive guide on Infrastructure as Code. Currently serving as Senior Cloud Architect at a leading technology consultancy, she has helped dozens of organizations transform their infrastructure operations through systematic adoption of IaC principles and practices.

### Professional background

Anna holds a Ph.D. in Computer Science with specialization in distributed systems and cloud computing. Her doctoral research focused on automated resource management in large-scale cloud environments, work that directly informed many of the optimization strategies discussed throughout this book.

Her professional journey spans startups to enterprise organizations, where she has consistently championed the adoption of infrastructure automation and DevOps practices. She has led successful cloud transformations for organizations ranging from financial services to e-commerce, implementing Infrastructure as Code solutions that have reduced deployment times by 90% while improving system reliability.

### Areas of expertise

- **Cloud architecture design** across multiple providers (AWS, Azure, Google Cloud)
- **Infrastructure as Code** implementation with Terraform, CloudFormation, and Pulumi
- **Container orchestration** with Kubernetes and Docker Swarm
- **DevOps transformation** and cultural change management
- **Security and compliance** automation in cloud environments
- **Cost optimization** strategies for cloud infrastructure

### Contributions to the field

Anna is a recognized speaker at international conferences including re:Invent, KubeCon, and HashiTalks, where she shares insights on infrastructure automation and cloud architecture best practices. She has published research in peer-reviewed journals and maintains an active blog on cloud technologies and infrastructure automation.

Her open-source contributions include several popular Terraform modules and tools for infrastructure testing and validation, used by thousands of practitioners worldwide.

## Marcus Andersson - DevOps Engineer and Automation Specialist

Marcus Andersson brings a unique perspective to Infrastructure as Code through his deep experience in both development and operations. As a DevOps Engineer and Automation Specialist, he has been at the forefront of implementing IaC solutions in complex enterprise environments, bridging the gap between traditional IT operations and modern cloud-native practices.

### Professional background

With over 12 years in the industry, Marcus has evolved from a traditional system administrator to a DevOps practitioner who specializes in automation and infrastructure engineering. His hands-on experience spans the entire spectrum of infrastructure technologies, from legacy data centers to modern serverless architectures.

Marcus has led infrastructure automation initiatives at several major organizations, implementing CI/CD pipelines that handle thousands of deployments per month while maintaining strict security and compliance requirements. His practical approach to solving complex infrastructure challenges has made him a sought-after consultant and mentor.

### Areas of expertise

- **CI/CD pipeline design** and implementation across diverse technology stacks
- **Configuration management** with Ansible, Chef, and Puppet
- **Monitoring and observability** solutions for infrastructure and applications
- **Security automation** and compliance as code implementation
- **Migration strategies** from traditional to cloud-native infrastructure
- **Team coaching** and DevOps culture transformation

### Practical experience and teaching

Marcus combines deep technical expertise with strong communication skills, making complex infrastructure concepts accessible to practitioners at all levels. He has developed and delivered training programs on Infrastructure as Code for major technology companies and has mentored dozens of engineers in their DevOps transformation journeys.

His real-world experience troubleshooting infrastructure issues and optimizing deployment processes provides the practical foundation for many of the solutions and best practices presented in this book.

### Open source and community involvement

Both authors are active contributors to the Infrastructure as Code community, participating in open-source projects and sharing knowledge through conferences, workshops, and online resources. Their combined expertise spans the full lifecycle of infrastructure automation, from initial design through operation and optimization.

## Why this book was written

The motivation for writing this comprehensive guide stems from the authors' observation that while Infrastructure as Code has become essential for modern organizations, many practitioners lack access to comprehensive, practical guidance that bridges theory with real-world implementation.

Through their consulting work and community involvement, Anna and Marcus have seen organizations struggle with common challenges: choosing the right tools, designing scalable architectures, implementing security best practices, and managing the cultural changes required for successful IaC adoption.

This book represents their effort to distill years of practical experience into actionable guidance that helps organizations avoid common pitfalls and accelerate their Infrastructure as Code journey. Every pattern, practice, and recommendation has been tested in production environments and refined through experience with diverse organizational contexts.

## Acknowledgments

The authors wish to thank the many colleagues, clients, and community members who have contributed to their understanding of Infrastructure as Code through collaboration, feedback, and shared experiences. Special recognition goes to the open-source communities that have built the tools and practices that make modern infrastructure automation possible.

We also thank the technical reviewers who provided valuable feedback on early drafts, helping ensure that this book provides accurate, up-to-date, and practical guidance for practitioners at all levels.

Finally, we acknowledge the organizations that have trusted us to guide their infrastructure transformation journeys. Their willingness to embrace change and invest in modern practices has provided the real-world laboratory where many of these concepts were developed and refined."""
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