# Appendix: Infrastructure as Code Tooling

Architecture as Code teams frequently evaluate the same set of infrastructure platforms. Rather than repeating feature lists in every chapter, this appendix summarises the distinct strengths of leading tools and links to the chapters where their capabilities are explored in more depth. Use it as the single reference point when choosing or cross-referencing tooling options.

## Comparative overview

| Tool | Primary Strengths | Ideal Scenarios | Integration Notes |
|------|-------------------|-----------------|-------------------|
| **Terraform** | Broad multi-cloud provider ecosystem, mature module registry, state back-end flexibility | Organisations orchestrating resources across several cloud providers or SaaS platforms | Chapters [2](02_fundamental_principles.md) and [5](05_automation_devops_cicd.md) describe how Terraform underpins automated enforcement and policy validation. |
| **Pulumi** | General-purpose languages (TypeScript, Python, Go, .NET) for infrastructure definitions, strong testing story | Teams with existing software engineering skills who want to reuse language ecosystems and testing frameworks | See [Chapter 13](13_testing_strategies.md) for approaches to unit testing infrastructure code using mainstream languages. |
| **AWS CloudFormation** | Deep integration with AWS services, managed drift detection, StackSets for multi-account governance | Enterprises heavily invested in AWS that require first-party support and compliance alignment | Refer to [Chapter 11](11_governance_as_code.md) for examples of federated governance using AWS-native services. |
| **Azure Bicep** | Concise syntax over Azure Resource Manager templates, strong tooling in Visual Studio Code, native type safety | Azure-focused environments that value consistent authoring experience and incremental deployments | Chapters [5](05_automation_devops_cicd.md) and [31](31_technical_architecture.md) provide patterns for combining Bicep with policy automation. |
| **Ansible** | Agentless configuration management, procedural orchestration for hybrid estates, rich module ecosystem | Hybrid or on-premise estates where configuration management and orchestration need to operate without cloud dependency | Use alongside declarative definitions described in [Chapter 7](07_containerization.md) and [Chapter 14](14_practical_implementation.md) to manage operating system baselines. |
| **Chef Habitat** | Application lifecycle automation, package-based deployment model, compliance scanning | Teams standardising application packaging whilst maintaining strict compliance controls | Connects with the compliance automation practices in [Chapter 12](12_compliance.md). |
| **Crossplane** | Kubernetes-native control plane for composing cloud services, GitOps alignment | Organisations adopting Kubernetes as the universal abstraction for multi-cloud infrastructure | Linked with the platform engineering discussion in [Chapter 20](20_ai_agent_team.md) where control planes need policy-aware automation. |

## Selection guidance

1. **Start with the dominant platform** in your estate and evaluate the native option (CloudFormation, Bicep) alongside a cross-cloud alternative (Terraform, Pulumi).
2. **Layer specialised tooling**—such as Ansible for configuration drift or Chef Habitat for application packaging—only when a measurable gap exists.
3. **Document the rationale** in an ADR rather than repeating comparative arguments elsewhere; the ADR guidance in [Chapter 4](04_adr.md) includes prompts for evaluating tooling trade-offs.
4. **Establish shared validation libraries** so that policy-as-code checks can be reused irrespective of the provisioning tool.

## Keeping the appendix current

This appendix deliberately separates vendor feature updates from the main chapters. When a new tool is introduced or existing capabilities change, update the relevant row here and reference the change from the chapters that rely on it. Doing so keeps the book concise and avoids proliferating near-identical tool descriptions.
