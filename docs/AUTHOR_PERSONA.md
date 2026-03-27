# Author Persona: Gunnar Nordqvist {#author-persona}

## Purpose

This document defines the authorial voice, register, and technical language conventions for all manuscript content in *Architecture as Code*. It is the reference for any contributor, editor, or AI-assisted tooling when generating, reviewing, or revising content on behalf of the author.

---

## Who Is the Author

**Gunnar Nordqvist** is a self-employed certified Chief Architect and IT Architect consultant operating within the Kvadrat network in Sweden. He writes from the perspective of a senior practitioner who has spent decades working at the intersection of enterprise architecture, infrastructure engineering, and organisational transformation.

He is not an academic. He is not a vendor. He is an experienced architect who has lived through the evolution of architecture practice—from heavyweight TOGAF ceremonies and Visio diagrams to codified, automated, continuously validated architecture.

His voice is that of a **trusted colleague explaining hard-won knowledge**, not a textbook author presenting theory.

---

## Voice and Tone

### Primary Register

- **Authoritative but collegial.** The author speaks with confidence, but never condescends. He assumes the reader is technically capable and treats them as a peer.
- **Direct and precise.** Sentences are purposeful. He does not hedge unnecessarily, nor does he use filler phrases such as "it is worth noting that" or "as we have seen".
- **Practitioner-first.** Every concept is grounded in real-world application. Theory is introduced only to provide context for practice.
- **Reflective.** He draws on personal experience and the broader community of practice to illustrate points, using "we" when referring to the architecture profession collectively.

### Tone Modifiers by Context

| Content Type | Tone |
|---|---|
| Conceptual introductions | Measured, explanatory, contextualising |
| Technical instructions | Precise, step-by-step, unambiguous |
| Architectural principles | Declarative, persuasive, evidence-backed |
| Anti-patterns and pitfalls | Frank, cautionary, experience-grounded |
| Future trends | Analytical, considered, appropriately speculative |
| Case studies | Narrative, concrete, outcome-focused |

---

## Technical Register: IT Architecture Vocabulary

The following terms and conventions define the technical language used throughout the book. They represent the working vocabulary of senior IT architects in enterprise and cloud-native contexts.

### Core Discipline Terms

| Preferred Term | Meaning / Usage Notes |
|---|---|
| **Architecture as Code** | The primary discipline. Always capitalised. Never "architecture-as-code" in prose. |
| **Infrastructure as Code (IaC)** | The foundational discipline from which Architecture as Code extends. |
| **Architecture Decision Record (ADR)** | A formal record of a significant architectural decision. Plural: ADRs. |
| **Architecture Decision Log (ADL)** | The collection of ADRs for a system or domain. |
| **architecture runway** | The pre-built extensible code that allows features to be developed more easily. Use lowercase. |
| **enterprise architecture (EA)** | The discipline governing the alignment of technology with business strategy. Lowercase unless part of a title. |
| **solution architecture** | The architectural design of a specific system or product. |
| **domain model** | A representation of business concepts and their relationships within a bounded context. |
| **bounded context** | From Domain-Driven Design; a boundary within which a particular model applies. |
| **capability map** | A structured view of an organisation's business and technical capabilities. |
| **architecture fitness function** | An objective evaluation criterion for an architectural characteristic. |
| **architectural characteristic** | A quality attribute such as scalability, observability, or resilience. |

### Platform and Tooling Terms

| Preferred Term | Usage Notes |
|---|---|
| **Structurizr** | The C4 model tooling platform. Always capitalised. |
| **C4 model** | Simon Brown's hierarchical diagram approach: Context, Container, Component, Code. |
| **Terraform** | HashiCorp's IaC tool. Always capitalised. |
| **Ansible** | Red Hat's configuration management tool. Always capitalised. |
| **Kubernetes** | Container orchestration platform. Always capitalised. K8s is acceptable in technical shorthand. |
| **Helm** | The Kubernetes package manager. Always capitalised. |
| **pipeline** | CI/CD automation chain. Lowercase unless part of a proper name. |
| **GitOps** | The operational model where Git is the single source of truth. CamelCase. |
| **policy as code** | Machine-readable governance rules. Lowercase in prose. |
| **compliance as code** | Automated compliance verification. Lowercase in prose. |
| **diagram as code** | Diagrams defined in a text format. Lowercase in prose. |

### Architecture Patterns and Concepts

| Preferred Term | Usage Notes |
|---|---|
| **microservices** | Plural noun; architectural style. Lowercase. |
| **event-driven architecture (EDA)** | Hyphenate as compound adjective. |
| **service mesh** | Two words, lowercase. |
| **sidecar pattern** | Lowercase. |
| **strangler fig pattern** | Preferred over "strangler pattern". Lowercase. |
| **golden path** | The recommended, well-supported development pathway. Lowercase. |
| **paved road** | Alternative to golden path. Lowercase. |
| **blast radius** | The scope of impact from a failure or change. Lowercase. |
| **drift** | Configuration or architectural drift from the desired state. |
| **desired state** | The declared, intended configuration or architecture. |
| **observed state** | The actual, measured current configuration or architecture. |
| **idempotent** | An operation that produces the same result regardless of how many times it is applied. |
| **immutable infrastructure** | Infrastructure that is replaced rather than modified. |

### Organisational and Process Terms

| Preferred Term | Usage Notes |
|---|---|
| **platform team** | The team responsible for the internal developer platform. |
| **stream-aligned team** | From Team Topologies; a team aligned to a business domain. |
| **enabling team** | From Team Topologies; a team that helps other teams adopt new practices. |
| **complicated subsystem team** | From Team Topologies; a team owning a complex technical domain. |
| **cognitive load** | The mental effort required of a team. Use deliberately. |
| **inner-source** | Open-source practices applied to internal codebases. Hyphenated. |
| **four-eyes principle** | Dual-approval requirement for critical changes. |
| **shift left** | Moving quality or security activities earlier in the lifecycle. |
| **shift right** | Monitoring and testing in production. |
| **runbook** | Documented operational procedures. Lowercase, one word. |
| **playbook** | Strategic or operational guidance document. Lowercase. |

### Security and Governance Terms

| Preferred Term | Usage Notes |
|---|---|
| **zero trust** | Security model; two words, lowercase. |
| **threat model** | A structured analysis of potential threats. |
| **attack surface** | The sum of points where an attacker can attempt entry. |
| **least privilege** | Granting only the minimum required permissions. |
| **secrets management** | The practice of securely handling credentials and keys. |
| **RBAC** | Role-Based Access Control. Always use the acronym after first definition. |
| **ABAC** | Attribute-Based Access Control. |
| **control plane** | The layer that manages and configures the data plane. |
| **data plane** | The layer that carries operational traffic. |

---

## Grammatical Conventions

### Sentence Structure

- Prefer **active voice**. "The pipeline validates the manifest" rather than "The manifest is validated by the pipeline."
- Use **imperative mood** in instructional sections. "Define the desired state in a Terraform module." Not "You should define..."
- Avoid **nominalisation** where a verb is clearer. "The team decided" rather than "A decision was made by the team."
- Use **parallel construction** in lists, headings, and comparative statements.

### Technical References

- On first use in a chapter, write the full term followed by the acronym in parentheses: "Infrastructure as Code (IaC)".
- In subsequent references within the same chapter, the acronym alone is acceptable.
- Code elements, CLI commands, file names, and configuration keys are always rendered in `monospace`.
- Tool names and product names retain their original capitalisation even when embedded in prose.

### Lists and Enumerations

- Use the Oxford (serial) comma in all lists of three or more items.
- Use bullet lists for non-sequential items; numbered lists for sequential steps or ranked items.
- Begin each bullet with a capital letter.
- End bullets consistently: either all with full stops, or none—do not mix.

### Headings

- Use sentence case for all headings: "Architecture decision records in practice", not "Architecture Decision Records In Practice".
- Exception: proper nouns and product names retain their standard capitalisation within headings.

---

## What the Author Does Not Write

To preserve voice consistency, the following stylistic patterns should be avoided:

- **Marketing language**: "powerful", "seamless", "robust solution", "best-in-class"
- **Vague superlatives**: "extremely important", "very significant", "highly complex"
- **Rhetorical questions used as transitions**: "So, what does this mean for architects?"
- **Unnecessary hedging**: "it could be argued that", "some might say"
- **Prescriptive moralising**: "architects must always...", "you should never..."
- **Filler openers**: "In today's fast-paced world...", "As we enter a new era of..."
- **Passive-aggressive qualifiers**: "surprisingly", "obviously", "of course", "clearly"

---

## Pronoun and Reference Conventions

| Context | Convention |
|---|---|
| The reader as individual | "you" (second person, direct address) |
| The profession collectively | "we" (inclusive first person plural) |
| A hypothetical team | "the team" (third person, avoids gender) |
| A hypothetical architect | "the architect" (role, not gendered pronoun) |
| The author's own experience | "I" (first person, used sparingly and purposefully) |

---

## British English Quick Reference

The following spellings are mandatory in all prose. See `docs/STYLE_GUIDE.md` for the complete list.

| American | British (required) |
|---|---|
| organization | organisation |
| optimization | optimisation |
| standardization | standardisation |
| containerization | containerisation |
| modernization | modernisation |
| behavior | behaviour |
| color | colour |
| center | centre |
| program (non-computing) | programme |
| analyze | analyse |
| recognize | recognise |
| utilize | utilise |
| catalog | catalogue |
| dialog | dialogue |

> **Exception:** Spellings inside code blocks, configuration samples, API names, and tool-specific terminology are never altered. Only surrounding prose is updated.

---

## Usage Examples

### Preferred

> "The ADR captures the rationale behind choosing an event-driven architecture over a synchronous request–response model. This decision should be revisited when the team's bounded contexts are better established."

> "Structurizr DSL allows the architecture model to be version controlled alongside the systems it describes. When the codebase changes, the architecture can change with it—and that change is reviewable, auditable, and reversible."

> "Policy as code shifts compliance verification left. Instead of waiting for an audit, the pipeline enforces controls continuously."

### Avoid

> "In today's rapidly evolving technology landscape, organisations face the extremely important challenge of keeping their architecture documentation up to date. This powerful solution enables seamless integration across all your systems."

---

## Related Documents

- `docs/STYLE_GUIDE.md` — Spelling, punctuation, and grammar standards
- `docs/VISUAL_ELEMENTS_GUIDE.md` — Diagram and visual presentation standards
- `docs/29_about_the_author.md` — Biographical information
- `CLAUDE.md` — Project-level instructions for AI-assisted tooling
