# Add release text to describe what is included in each release

## Summary
Introduce a structured release notes process that documents the features, improvements, and fixes included in every release so users can follow project progress with confidence.

## Background
Releases currently lack consistent narrative summaries, leaving adopters uncertain about the changes they contain. Formalising release notes will improve transparency and set expectations for each iteration.

## Objectives
- Define a repeatable process for drafting and publishing release notes alongside artefacts.
- Capture key highlights, enhancements, and fixes in a user-friendly format.
- Integrate release documentation into the existing release pipeline to avoid manual drift.

## Proposed Approach
1. Review the current release workflow to identify where notes can be generated or injected automatically.
2. Establish a template that outlines sections for features, improvements, fixes, and acknowledgements.
3. Update automation or scripts to compile release content from merged pull requests or curated summaries.
4. Document the workflow so maintainers know how to add context or manual edits when necessary.

## Acceptance Criteria
- A documented release notes template with guidance on how to populate each section.
- Automation or documented steps ensuring release notes are generated and published with each release.
- Historical releases retrofitted with consistent notes, or a clear statement defining the starting point for the new process.
- Confirmation from stakeholders that the release notes provide sufficient clarity on changes.

## Suggested Labels
- `release`
- `documentation`
- `process`

