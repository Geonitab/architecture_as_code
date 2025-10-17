# Issue 14: Shift Passive Voice to Active Construction

## Relevant Documentation Sections
Architecture as Code manuscript, ADR workflow explanations, and tooling guidance sections.

## Problem Statement
Extensive passive voice (for example, "Versioning is managed through the Git history") hides the responsible actor and adds unnecessary words. Passive constructions can be harder to parse and dilute the authoritative tone required for prescriptive technical guidance.

## Impact
- Readers expend more effort to understand who performs critical actions.
- Sentences lengthen, reducing pace and engagement.
- Passive voice undermines clear ownership in governance and process descriptions.

## Recommended Remediation
- Identify passive constructions across documentation and rewrite them in active voice with explicit subjects (for example, "Git history manages versioning").
- Prioritise sections discussing ADR lifecycle, governance checkpoints, and version control responsibilities.
- Ensure edits maintain technical accuracy while improving readability.

## Acceptance Criteria
- Passive constructions are replaced by active voice statements except where passive voice is necessary (for instance, when the actor is unknown).
- Updated passages clearly state the responsible actor for key activities.
- Editorial review verifies improved clarity in the cited examples and representative sections.

## Recommended Labels
`documentation`
