---
id: 101
title: "Define workflow behavior"
prd_ref: "P1 - Update/reapply templates"
status: "To Do"
status_timestamp: ""
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 4
  max_new_modules: 0
---

# Ticket: Define workflow behavior

## Title

Define workflow behavior

## Type

- Docs

## Context

- Task: Document required steps, gates, and outputs.
- Acceptance: Behavior is specified in docs.
- Estimate: 0.5 day.
- Feature context: Update/reapply templates (CLI-only workflow).
- References: `docs/02-features/03-update-reapply-templates/feature-spec.md`, `docs/02-features/03-update-reapply-templates/tech-design.md`, `docs/02-features/03-update-reapply-templates/test-plan.md`.

## Scope

- **Choose one:** 1 feature folder
- In scope:
  - Define the workflow behavior for template reapply in feature docs.
  - Capture required gates and outputs for the CLI flow.
- Out of scope:
  - Implementing tooling changes.
  - Adding tests.

## PRD Traceability

- PRD feature/order: P1 - Update/reapply templates
- Link to PRD section: `docs/01-product/prd.md` (Prioritized Feature List)

## Success Criteria

- [ ] Required steps, gates, and outputs are documented in feature docs.
- [ ] Behavior matches the feature specification and tech design.

## Definition of Done (Ticket-Specific)

- [ ] Feature docs describe the update/reapply workflow steps and gates.
- [ ] Outputs and error handling expectations are documented.

## Plan (Draft)

- Approach: Update feature docs to describe workflow behavior, gates, and outputs.
- Files to change: `docs/02-features/03-update-reapply-templates/feature-spec.md`, `docs/02-features/03-update-reapply-templates/tech-design.md` (if needed), `docs/02-features/03-update-reapply-templates/dev-tasks.md` (status).
- Risks/assumptions: Assumes CLI-only surface and local-only operations remain unchanged.
- Tests to run: None (docs-only).

## Evidence Hints

- `docs/02-features/03-update-reapply-templates/feature-spec.md` (User Flow, Error Handling)
- `docs/02-features/03-update-reapply-templates/tech-design.md` (CLI Commands section)

## References

- Feature spec: `docs/02-features/03-update-reapply-templates/feature-spec.md` (Summary + Requirements + User Flow)
- Tech design: `docs/02-features/03-update-reapply-templates/tech-design.md` (Architecture + CLI Commands)
- Test plan: `docs/02-features/03-update-reapply-templates/test-plan.md` (Test Strategy + Cases)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH):

## Change Budget

- Max files: 4
- Max new modules: 0
- Max lines changed (estimate): 120

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Document workflow steps for update/reapply templates.
- List gates (approvals/confirmations) and expected outputs.
- Capture error handling expectations for conflicts and partial updates.

## Tests Run

- Command(s):
- Result(s):

## Implementer Notes

- Implementation choices:
- Edge cases covered:
- Files changed:

## Tester Feedback

- Tests executed:
- Failures observed:
- Suggested fixes:

## Reviewer Feedback

- Issues found:
- Suggestions:
- Approval status:

## Iteration Log

- [ ] Implementer updated after tester feedback
- [ ] Implementer updated after reviewer feedback

## Logs Updated

- [ ] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)

## Docs Updated

- [ ] Feature docs (feature-spec/tech-design/dev-tasks/test-plan)
- [ ] PRD (if scope/priority changed)
- [ ] Other: [list]

## Report (Final)

- What changed:
- Commands run (use `pp` for noisy output):
- Results:

## Commit

- Message:
