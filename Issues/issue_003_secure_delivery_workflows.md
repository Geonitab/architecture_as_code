# Improve Secure Delivery Workflows Across Multi-Cloud Tooling

## Source IDs
- [9] Google Cloud. "Store Terraform state in Cloud Storage." Google Cloud Documentation, 2024. https://cloud.google.com/docs/terraform/resource-management/store-terraform-state.
- [10] Microsoft Learn. "Store Terraform state in Azure Storage." Microsoft Learn Documentation, 2024. https://learn.microsoft.com/en-gb/azure/developer/terraform/store-state-in-azure-storage.
- [11] Pulumi. "Testing Infrastructure as Code Programs." Pulumi Blog, 2024.
- [12] AWS. "AWS Cloud Development Kit (CDK) Developer Guide." https://docs.aws.amazon.com/cdk/latest/guide/home.html.

## Relevant Manuscript Sections
- `13_testing_strategies.md` – clarify how Pulumi's testing approach generalises to the book's framework.
- `14_practical_implementation.md` – show how CDK and testing practices reinforce delivery assurance.
- `05_automation_devops_cicd.md` – ensure AWS CDK content is grounded in the authoritative guide.
- `09b_security_patterns.md` – reference the multi-cloud state storage guidance when comparing Terraform patterns.

## Problem Statement
Infrastructure delivery chapters mention cross-cloud tooling but do not connect storage and testing practices coherently. Reviewers flagged that Terraform state security patterns and CDK automation should be juxtaposed to highlight vendor-neutral principles. The lack of explicit cross-referencing leaves gaps when teams adopt Architecture as Code across providers.

## Acceptance Criteria
- Chapter 13 references the Pulumi article when describing automated tests for Infrastructure as Code.
- Chapter 14 links CDK workflow guidance to Pulumi testing recommendations to demonstrate end-to-end assurance.
- Terraform security discussions reference both Google Cloud and Microsoft state-storage guides when outlining multi-cloud posture.
- Updates clarify the shared control objectives using British English terminology.

## Recommended Labels
- dev
- security
- qa
