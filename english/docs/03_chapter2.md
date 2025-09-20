# Version control and code structure

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
- AWS. "Infrastructure as Code Best Practices." AWS Documentation.