# Architecture as Code — Agent Team

This directory contains the specialised agent definitions for the
*Architecture as Code* book project. Each agent is a Claude Code sub-agent
with a focused role and domain expertise.

---

## The Team

| Agent File | Role | Primary Responsibility |
|---|---|---|
| [`editor.md`](editor.md) | Lead Editor | Language, style, British English, voice consistency |
| [`writer.md`](writer.md) | Lead Writer | Drafting prose in the author's voice and persona |
| [`graphic-designer.md`](graphic-designer.md) | Lead Graphic Designer | Mermaid diagrams, visual assets, `.mmd` sources |
| [`researcher.md`](researcher.md) | Lead Researcher | Fact-checking, source verification, URL and ISBN validation |
| [`critic.md`](critic.md) | Critical Reviewer | Structural critique, argument quality, reader experience |
| [`it-architect.md`](it-architect.md) | Senior IT Architecture Expert | Technical accuracy, architectural patterns, diagram fidelity |

---

## How to Invoke an Agent

In Claude Code, use the `@` mention syntax:

```
@editor Review chapter 05 for British English compliance.
@writer Draft an introduction for the section on GitOps reconciliation loops.
@graphic-designer Create a C4 container diagram for the CI/CD platform.
@researcher Verify the Structurizr DSL syntax examples in chapter 07.
@critic Critique the argument structure in chapter 12 on policy as code.
@it-architect Validate the Kubernetes operator pattern described in chapter 15.
```

---

## Typical Workflows

### New Chapter Draft
1. `@researcher` — gather sources and verify technical claims
2. `@writer` — draft the chapter content
3. `@graphic-designer` — create supporting diagrams
4. `@it-architect` — validate technical accuracy
5. `@critic` — critique structure and pedagogical value
6. `@editor` — final language and style review

### Diagram Update
1. `@graphic-designer` — update `.mmd` source
2. `@it-architect` — validate the architecture depicted
3. `@editor` — check label text for British English

### Technical Fact-Check
1. `@researcher` — locate primary sources
2. `@it-architect` — interpret and validate technical findings
3. `@editor` — update prose to reflect corrections

---

## Project Context

- **Author:** Gunnar Nordqvist, certified Chief Architect (Kvadrat, Sweden)
- **Language:** Oxford-standard British English throughout
- **Book title:** *Architecture as Code* (always this capitalisation)
- **Style reference:** `docs/STYLE_GUIDE.md`
- **Author persona:** `docs/AUTHOR_PERSONA.md`
- **Chapter index:** `docs/book_index.json`
