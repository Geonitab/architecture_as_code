# Issue: Align Security, Governance and Compliance Chapters with Authoritative Standards

## Problem Statement

The security and governance chapters reference policy-as-code and compliance frameworks in narrative form but could be more precisely anchored to the authoritative sources, particularly NIST SP 800-53, ISO/IEC 27001, and the OPA documentation. The SRE workbook and Kubernetes documentation are referenced implicitly but not cited consistently in the sources sections.

## Relevant Manuscript Sections

- Chapter 8: Microservices Architecture as Code (`08_microservices.md`)
- Chapter 9: Security Fundamentals (`09_security_fundamentals.md`)
- Chapter 9b: Advanced Security Patterns (`09b_security_patterns.md`)
- Chapter 11: Governance as Code (`11_governance_as_code.md`)
- Chapter 12: Compliance and Regulatory Adherence (`12_compliance.md`)
- Chapter 13: Testing Strategies (`13_testing_strategies.md`)
- Chapter 14: Practical Implementation (`14_practical_implementation.md`)
- Chapter 15A: Evidence as Code (`15a_evidence_as_code.md`)

## Source IDs

The following curated sources from the catalogue support this issue:

- [2] Thoughtworks Technology Radar. "Governance as Code." Thoughtworks, 2024.
- [7] Cloud Native Computing Foundation. "State of Cloud Native Development 2024." CNCF, 2024.
- [8] Google Cloud. "The Site Reliability Workbook." O'Reilly Media, 2018.
- [10] Open Policy Agent. "Policy as Code Overview." CNCF OPA Project, 2024.
- [11] NIST. "Security and Privacy Controls for Information Systems and Organisations." NIST SP 800-53, 2024.
- [12] Microsoft Learn. "Design multi-stage release pipelines with approvals." Microsoft Learn, 2024.
- [13] Kubernetes. "Kubernetes Documentation: Concepts." Kubernetes Project, 2024.
- [14] ISO/IEC. "ISO/IEC 27001:2022 Information Security Management." ISO, 2022.
- [15] Pulumi. "Testing Infrastructure as Code Programs." Pulumi Blog, 2024.
- [16] HashiCorp. "Securing Terraform State." HashiCorp Developer Documentation, 2024.

## Acceptance Criteria

- [ ] Chapter 11 cites Source [2] when describing governance-as-code adoption trends
- [ ] Chapter 8 and 9 reference Source [7] for cloud native development statistics
- [ ] Chapter 13 cites Source [8] for SRE reliability testing practices
- [ ] Chapters 10–11 reference Source [10] for OPA/Rego policy pattern examples
- [ ] Chapter 11 and 12 cite Source [11] when mapping controls to NIST 800-53
- [ ] Chapter 5 and 14 reference Source [12] for multi-stage pipeline configuration
- [ ] Chapter 7 cites Source [13] for Kubernetes configuration patterns
- [ ] Chapter 12 and 15A cite Source [14] for ISO 27001 control mapping examples
- [ ] Chapter 13 and 14 cite Source [15] for infrastructure testing patterns
- [ ] Chapter 9 cites Source [16] for Terraform state encryption guidance

## Recommended Labels

`documentation`, `req`, `content-quality`, `architecture`
