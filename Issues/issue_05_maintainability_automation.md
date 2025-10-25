# Address Maintainability Weaknesses in Chapter 05: Automation, DevOps, and CI/CD

## Source IDs
- [8]
- [9]
- [12]

## Relevant Manuscript Sections
- Chapter 05 – Automation, DevOps and CI/CD for Architecture as Code
- Chapter 13 – Testing Strategies for Infrastructure as Code

## Problem Statement
The automation chapter acknowledges regulatory pressure and complex dependency graphs, yet the remediation guidance remains largely conceptual. Readers are left without concrete steps for implementing regression tests, resilience checks, or reporting loops across environments. That omission risks leaving IaC pipelines brittle and labour-intensive to maintain.

## Acceptance Criteria
- [ ] Document explicit automated test categories (unit, integration, compliance) and how they are wired into CI/CD workflows.
- [ ] Provide examples of environment promotion policies that ensure architectural parity across regions.
- [ ] Highlight metrics and dashboards that surface maintainability signals such as flaky deployments or policy breaches.
- [ ] Link the added material to the cited sources for traceability.

## Recommended Labels
- maintainability
- chapter-05
- automation
