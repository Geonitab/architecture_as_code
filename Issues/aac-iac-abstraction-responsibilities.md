# Issue: Clarify AaC versus IaC Abstraction Responsibilities

**Priority:** Medium  
**Suggested Labels:** documentation, architecture  
**Linked Finding:** #4 – Abstraction and Opinionation

## Summary
Strengthen the automation chapter with an explicit comparison between AaC and IaC abstraction layers, using visuals or call-out boxes to prevent reader confusion.

## Background
Readers must grasp that AaC specifies architectural intent and guardrails, while IaC implements the concrete infrastructure. Without a clear delineation, automation discussions risk conflating responsibilities. Introducing a visual diagram or structured explainer in `docs/05_automation_devops_cicd.md` will sharpen understanding and underline governance themes.

## Acceptance Criteria
- [ ] Review the current narrative in `docs/05_automation_devops_cicd.md` and identify where clarification is most impactful.
- [ ] Add a diagram (Mermaid or similar) or a visually distinct text box contrasting AaC and IaC roles.
- [ ] Emphasise how AaC embeds governance and standardisation, with IaC executing the specifics.
- [ ] Cite the relevant findings and sources so readers can trace the factual basis for the distinction.

## Additional Notes
Coordinate with existing diagrams to maintain stylistic consistency (fonts, colours, British English spellings).
