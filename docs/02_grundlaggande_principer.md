# Fundamental Principles of Architecture as Code

Architecture as Code builds on fundamental principles as ensures successful implementation of codified system architecture. These principles encompasses the entire system landscape and creates a holistic view for architecture management.

![Fundamental principles diagram](images/diagram_02_kapitel1.png)

Diagram shows the natural flow from declarative code through version control and automation to reproducibility and scalability - the five fundamental pillars within Architecture as Code.

## Declarative architecture definition

The deklarativa approach in Architecture as Code means describing desired system state at all levels - from application components to infrastructure. This differs from imperative programming where each step must be specified explicitly.

Declarative definition enables describing architecture's desired state, that Architecture as Code extends to encompass application architecture, API-contracts and organizational Structures.

## Helhetsperspektiv at kodifiering

Architecture as Code encompasses the entire system ecosystem through a holistic approach. This includes application logic, data flows, security policies, compliance-rules and organizational structures.

A practical Example is how a change in a application's API automatically can propagate through entire architecture - from security configurations to documentation - all that is defined as code.

## immutable architecture patterns

Principen about immutable architecture means the entire system architecture is managed through immutable components. instead to modify existing parts are created new versions as replace old at all levels.

This creates predictability and eliminates architectural drift - where systems gradually diverge from their intended design over time.

## Testbarhet at architecture level

Architecture as Code enables testing of entire system architecture, not only individual components. This includes validation of architecture patterns, compliance with design principles and verification of end-to-end flows.

Arkitekturtester validates design decisions, system complexity and ensures the entire architecture fungerar as avsett.

## Documentation as Code

Documentation as Code (DaC) represents the principle of treat documentation as a integrerad del of codebase snarare än as A separat artefakt. This means to documentation stored together with koden, version-controlled with the same tools and undergoes the same quality assurance processes as applikationskoden.

### Benefits with Documentation as Code

**version control and history**: by lagra documentation in Git or other version control systems organizations get automatic traceability of changes, ability to restore tidigare versions and full historik over documentation's development.

**Collaboration and review**: Pull requests and merge-processes ensures documentation changes are reviewed before being published. This forbättrar quality and minskar risken for felaktig or foråldrad information.

**CI/CD integration**: Automated pipelines can generate, validate and publish documentation automatically when code changes. This eliminates manual steps and ensures dokumentationen alltid is uppdaterad.

### Practical implementation

```yaml
# .github/workflows/docs.yml
name: Documentation Build and Deploy
on:
  push:
    paths: ['docs/**', 'README.md']
  pull_request:
    paths: ['docs/**']

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Generate documentation
        run: |
          npm run docs:build
          npm run docs:lint
          
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/dist
```

Moderna verktyg that GitBook, Gitiles and MkDocs enables automatisk generering of webbdokumentation from Markdown-filer lagrade tosammans with koden.

## Requirements as Code

Requirements as Code (RaC) transformerar traditionell kravspecifikation from textdokument to maskinläsbar code as can exekveras, valideras and automatiseras. This paradigmskifte enables kontinuerlig verification of to systemet uppfyller sina krav through entire utvecklingslivscykeln.

### automation and traceability

**Automatiserad validation**: Krav uttryckta as code can exekveras automatically mot systemet to verifiera compliance. This eliminates manuell testing and ensures konsekvent validation.

**Direkt koppling mellan krav and code**: each systemkomponent can kopplas tobaka to specifika krav, which creates fullständig traceability from affärsbehov to Technical implementation.

**Continuous compliance**: Changes in systemet valideras automatically mot all definierade krav, which forhindrar regression and ensures ongoing compliance.

### practical example with Open Policy Agent (OPA)

```yaml
# requirements/security-requirements.yaml
apiVersion: policy/v1
kind: RequirementSet
metadata:
  name: svenska-sakerhetskrav
  version: "1.2"
spec:
  requirements:
    - id: SEC-001
      type: security
      description: "all S3 buckets must ha kryptering aktiverad"
      priority: critical
      compliance: ["GDPR", "ISO27001"]
      policy: |
        package security.s3_encryption
        
        deny[msg] {
          input.resource_type == "aws_s3_bucket"
          not input.server_side_encryption_configuration
          msg := "S3 bucket must ha server-side encryption"
        }
    
    - id: GDPR-001
      type: compliance  
      description: "Persondata must lagras inom EU/EES"
      priority: critical
      compliance: ["GDPR"]
      policy: |
        package compliance.data_residency
        
        deny[msg] {
          input.resource_type == "aws_rds_instance"
          not contains(input.availability_zone, "eu-")
          msg := "RDS instans must placeras in EU-region"
        }
```

### validation and test-automation

Requirements as Code integreras naturligt with test-automation by krav blir executable specifications:

```python
# test/requirements_validation.py
import yaml
import opa

class RequirementsValidator:
    def __init__(self, requirements_file: str):
        with open(requirements_file, 'r') as f:
            self.requirements = yaml.safe_load(f)
    
    def validate_requirement(self, req_id: str, system_config: dict):
        requirement = self.find_requirement(req_id)
        policy_result = opa.evaluate(
            requirement['policy'], 
            system_config
        )
        return {
            'requirement_id': req_id,
            'status': 'passed' if not policy_result else 'failed',
            'violations': policy_result
        }
    
    def validate_all_requirements(self) -> dict:
        results = []
        for req in self.requirements['spec']['requirements']:
            result = self.validate_requirement(req['id'], self.system_config)
            results.append(result)
        
        return {
            'total_requirements': len(self.requirements['spec']['requirements']),
            'passed': len([r for r in results if r['status'] == 'passed']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'details': results
        }
```

Svenska organisationer drar särskild nytta of Requirements as Code to automatically validate GDPR-compliance, finansiella regleringar and myndighetskrav as konstant must uppfyllas.

Sources:
- Red Hat. "Architecture as Code Principles and Best Practices." Red Hat Developer.
- Martin, R. "Clean Architecture: A Craftsman's Guide to Software Structure." Prentice Hall, 2017.
- ThoughtWorks. "Architecture as Code: The Next Evolution." Technology Radar, 2024.
- GitLab. "Documentation as Code: Best Practices and implementation." GitLab Documentation, 2024.
- Open Policy Agent. "Policy as Code: Expressing Requirements as Code." CNCF OPA Project, 2024.
- Atlassian. "Documentation as Code: Treating Docs as a First-Class Citizen." Atlassian Developer, 2023.
- NIST. "Requirements Engineering for Secure Systems." NIST Special Publication 800-160, 2023.