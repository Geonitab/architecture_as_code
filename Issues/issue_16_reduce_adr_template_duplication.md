# Issue 16: Reduce ADR Template Duplication

## Priority
Medium

## Type
Example duplication

## Component
ADR chapter

## Problem Statement
Chapter 4 repeats the four-part ADR structure (Status, Context, Decision, Consequences) in the introductory explanation, the standard template, and two full examples. The repetition focuses on formatting rather than demonstrating diverse decision outcomes, making the chapter feel formulaic.

## Evidence of Repetition
- “What Are Architecture Decision Records?” section: table presenting Status, Context, Decision, Consequences.
- “Standardised ADR Template” section: Markdown template repeating the same headings.
- Example 1 (Terraform selection) and Example 2 (PostgreSQL selection): both restate the identical structure before delivering content.

## Impact
- Consumes space that could showcase varied ADR scenarios (rejected, superseded, escalated decisions).
- Reduces reader engagement by reiterating structure instead of insight.
- Suggests limited creativity in applying ADRs beyond the standard format.

## Recommended Actions
1. Present the ADR structure once with detailed guidance on populating each section.
2. Replace duplicate structural descriptions in examples with brief reminders or annotations focusing on content quality.
3. Introduce varied ADR states (for example, superseded, rejected) to demonstrate lifecycle management.

## Acceptance Criteria
- [ ] Chapter 4 contains a single authoritative description of the ADR template.
- [ ] Examples focus on decision rationale and outcomes without reprinting the full template each time.
- [ ] At least one example showcases a non-“Accepted” ADR status to illustrate lifecycle variety.

## Recommended Labels
`documentation`, `editor`
