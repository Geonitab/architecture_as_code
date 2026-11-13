# Fact-check log: unit uE

Files: docs/architecture_as_code_maturity_model.md; docs/maturity_model_radar.html (prose and chapter references only; JS/CSS mechanics skipped). Date: 2026-11-13.
Round 2: 4 rows changed (SERIES 0, OWN 0, CORRECTED 0, REVIEW 0, VERIFIED-with-new-evidence 4: rows 3, 9, 10 re-fetched from https://docs.structurizr.com/ because the quoted sentences are on the home page, not the DSL language page; row 11 split, 11a now VERIFIED). All other VERIFIED rows re-checked against cache files by exact phrase; Terratest quote re-fetched from https://terratest.gruntwork.io/.
Counts: 15 claims, 10 VERIFIED, 2 CORRECTED, 3 REVIEW, 0 SERIES, 0 OWN.
The file's own "Sources" list ([1] external; [2]-[11] internal chapter links) is local numbering, not the bibliography numbering. Local [1] = bibliography Source [38].

| # | Location | Claim in brief | Source ID | URL actually read | Verdict | Evidence note |
|---|----------|----------------|-----------|-------------------|---------|---------------|
| 1 | Aspects table, IaC | Terraform uses declarative templates | Source [5] | developer.hashicorp.com/terraform/intro (cache) | VERIFIED | "Terraform configuration files are declarative, meaning that they describe the end state of your infrastructure." |
| 2 | Aspects table, IaC | Pulumi and AWS CDK are programmatic frameworks | Sources [15], [9] | pulumi.com/docs/iac/concepts/testing/unit/ (cache); docs.aws.amazon.com/cdk/v2/guide/home.html | VERIFIED | Pulumi: "authored in a general-purpose language like TypeScript, Python, Go"; CDK: "expressive power of a programming language". |
| 3 | Aspects table, AaC | C4 model and Structurizr DSL encode architecture; Structurizr DSL reference | Sources [37], [38] | c4model.com (cache); docs.structurizr.com/dsl/language (cache); docs.structurizr.com | VERIFIED | Re-fetched https://docs.structurizr.com/ : "Structurizr is a “models as code” tool designed for the C4 model - you write Structurizr DSL to create multiple software architecture diagrams from a single model." Also cache source-37: C4 "hierarchical abstractions" |
| 4 | Aspects table, containers | Container images, Kubernetes manifests, Compose files, Helm charts | none in bibliography for Helm/Compose | helm.sh/docs/; docs.docker.com/compose/ | REVIEW | Helm "is the package manager for Kubernetes"; Compose "a tool for defining and running multi-container applications". Consistent, but no bibliography entry covers Helm or Compose; candidates: https://helm.sh/docs/ and https://docs.docker.com/compose/. |
| 5 | Aspects table, PaC | Open Policy Agent translates policy into executable rules | Source [10] | openpolicyagent.org/docs/ (cache) | VERIFIED | "OPA generates policy decisions by evaluating the query input against policies and data." |
| 6 | Level 2 | Rego is a policy language | Source [10] | openpolicyagent.org/docs/ (cache) | VERIFIED | "OPA policies are expressed in a high-level declarative language called Rego." |
| 7 | Level 2 | Terratest enforces compliance | Source [90] | terratest.gruntwork.io/docs/ (cache); terratest.gruntwork.io | CORRECTED | Source re-read at https://terratest.gruntwork.io/ : "Terratest is a Go library that provides patterns and helper functions for testing infrastructure". Old: "Tools such as Terratest and Checkov enforce compliance." New: "Tools such as Terratest (automated tests for infrastructure code) and Checkov (static scanning for misconfigurations) check compliance." |
| 8 | Level 2 | Checkov checks compliance (scans for misconfigurations) | none in bibliography | checkov.io | REVIEW | Page: "Checkov scans cloud infrastructure configurations to find misconfigurations before they're deployed." Supports the new wording; no bibliography entry for Checkov. Candidate: https://www.checkov.io/. |
| 9 | Level 2 | Structurizr models systems and generates diagrams | Source [38] | docs.structurizr.com (cache and live) | VERIFIED | Re-fetched https://docs.structurizr.com/ : "you write Structurizr DSL to create multiple software architecture diagrams from a single model." |
| 10 | Aspects table, Documentation as code | Markdown or AsciiDoc documentation with version control | Source [38] | docs.structurizr.com/dsl/language (cache) | VERIFIED | Re-fetched https://docs.structurizr.com/language page navigation: "Markdown/Asciidoc documentation"; home page: "The as code approach is version control friendly, supporting traditional Git collaboration workflows." |
| 11a | Aspects table, Governance | Branch protection rules exist as a codifiable GitHub feature | none cited here | not retrieved | VERIFIED (branch protection rules) | Cache source-4 (GitHub Docs, About protected branches, retrieved this session): "You can protect important branches by setting branch protection rules". |
| 11b | Aspects table, Management | GitHub issues and pull-request workflows used to encode leadership practices (templates, bots) | none in bibliography | not retrieved | REVIEW | Source [4] covers branch protection (and pull-request requirements) but not issue templates or bots as a management-encoding practice; no bibliography entry covers GitHub issues. Candidate: https://docs.github.com/en/issues. Wording unchanged. |
| 12 | Local source [1] | Structurizr DSL language reference URL and title | Source [38] | docs.structurizr.com/dsl/language | VERIFIED | Page titled "Language reference | Structurizr"; link resolves. |
| 13 | Local sources [2]-[11] | Chapter titles of internal links | n/a (internal) | repository headings | CORRECTED | Local [10] said "...CI/CD for Infrastructure as Code"; the chapter heading is "Automation, DevOps and CI/CD for Architecture as Code". Changed in the Sources list. Other nine titles match their chapter H1s. |
| 14 | Radar HTML | Intro prose and 19 chapter anchor links | n/a | docs/*.md | VERIFIED | No external factual claims in HTML prose; every `url: "NN_x/#anchor"` target file and heading anchor exists. |

Not claims (author's framework): maturity Levels 0-5 definitions, checklist questions, "Using the maturity model" steps, level descriptions of AI, quantum-safe, zero-trust and carbon-aware practices.

## Bibliography metadata issues
- Source [38]: none found (title, publisher and URL match; resolves).
- Source [37], [10], [5], [15], [9], [90]: titles/URLs match retrieved pages; no issues.

## Claims resting only on cross-reference to another volume
None.
