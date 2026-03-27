# Issue: Strengthen Architecture as Code Foundations with Current Industry Sources

## Problem Statement

The foundations chapters (1–4) introduce Architecture as Code principles and version control practices but could be strengthened by more explicitly citing the current ThoughtWorks Technology Radar positioning and the GitHub branch protection documentation. Several code examples reference Terraform and CDK without linking to the canonical provider documentation.

## Relevant Manuscript Sections

- Chapter 1: Introduction to Architecture as Code (`01_introduction.md`)
- Chapter 2: Fundamental Principles of Architecture as Code (`02_fundamental_principles.md`)
- Chapter 3: Version Control and Code Structure (`03_version_control.md`)
- Chapter 4: Architecture Decision Records (`04_adr.md`)
- Chapter 5: Automation, DevOps and CI/CD (`05_automation_devops_cicd.md`)
- Chapter 7: Containerisation and Orchestration as Code (`07_containerisation.md`)

## Source IDs

The following curated sources from the catalogue support this issue:

- [1] ThoughtWorks. "Architecture as Code: The Next Evolution." Technology Radar, 2024.
- [3] Atlassian. "Git Workflows for Architecture as Code." Atlassian Git Documentation, 2024.
- [4] GitHub Docs. "About protected branches." GitHub Documentation, 2024.
- [5] HashiCorp. "Introduction to Infrastructure as Code with Terraform." HashiCorp Developer Documentation, 2024.
- [6] Cloud Native Computing Foundation. "Cloud Native Definition." CNCF GitHub, 2024.
- [9] AWS. "AWS Cloud Development Kit (CDK) Developer Guide." Amazon Web Services, 2024.

## Acceptance Criteria

- [ ] Chapter 1 cites Source [1] when introducing the Architecture as Code concept
- [ ] Chapter 3 references Source [3] and Source [4] in the version control patterns section
- [ ] Chapter 5 links to Source [5] and Source [9] when discussing Terraform and CDK tooling
- [ ] Chapter 7 references Source [6] in the cloud native definition context
- [ ] All new citations follow the `Author. "Title." Publication, Year.` format

## Recommended Labels

`documentation`, `req`, `content-quality`
