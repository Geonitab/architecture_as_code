# Create workflow to aggregate results of all workflows since the latest build-all run

## Summary
Develop automation that monitors every workflow run following the most recent `build-all` orchestration job, aggregating their outcomes into a concise report that updates continuously until the next orchestration run.

## Background
Multiple specialised workflows execute between orchestrated `build-all` runs, but their results are scattered across separate logs. A consolidated summary will help maintainers gauge overall system health without inspecting each workflow individually.

## Objectives
- Detect when the `build-all` workflow completes and use that event as a baseline for aggregation.
- Collect the status, duration, and key artefacts of every workflow triggered after that point.
- Present the aggregated data in an accessible format, such as a comment, dashboard, or status page.

## Proposed Approach
1. Review existing workflow files to understand naming conventions and available events.
2. Implement a GitHub Actions workflow (or companion script) that watches for `build-all` completions.
3. Use the GitHub API to gather run metadata for subsequent workflows until the next orchestration event.
4. Produce a summary output that highlights successes, failures, and notable artefacts.
5. Store or publish the summary in a location that is easy for maintainers to find, updating it whenever new runs are detected.

## Acceptance Criteria
- Automation in place that triggers on completion of the `build-all` workflow.
- Aggregated reporting that includes run names, conclusions, runtimes, and links to artefacts or logs.
- Documentation describing how the aggregation works and where to view the latest summary.
- Evidence that the process updates automatically as new workflows finish between orchestration runs.

## Suggested Labels
- `ci`
- `automation`
- `reporting`

