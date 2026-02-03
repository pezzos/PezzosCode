---
id: 401
title: "Add or update tests"
prd_ref: "P1 - Update/reapply templates"
status: "To Do"
status_timestamp: ""
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 6
  max_new_modules: 0
---

# Ticket: Add or update tests

## Title

Add or update tests

## Type

- Tech Debt

## Context

- Task: Add regression tests or checks where applicable.
- Acceptance: Tests cover the primary path.
- Estimate: 0.5 day.
- Feature context: Update/reapply templates (CLI-only workflow).
- References: `docs/02-features/03-update-reapply-templates/feature-spec.md`, `docs/02-features/03-update-reapply-templates/tech-design.md`, `docs/02-features/03-update-reapply-templates/test-plan.md`.

## Scope

- **Choose one:** 1 feature folder
- In scope:
  - Tests for the update/reapply workflow primary path.
  - Validation of key gates/outputs.
- Out of scope:
  - UI/TUI tests.
  - Load/perf testing.

## PRD Traceability

- PRD feature/order: P1 - Update/reapply templates
- Link to PRD section: `docs/01-product/prd.md` (Prioritized Feature List)

## Success Criteria

- [ ] Tests cover the primary CLI path.
- [ ] Tests validate expected outputs and exit codes.

## Definition of Done (Ticket-Specific)

- [ ] Test cases align with the feature test plan.
- [ ] Primary path is covered with repeatable tests.
- [ ] Tests run without failures.

## Plan (Draft)

- Approach: Add or extend tests to cover the update/reapply CLI behavior and key gates.
- Files to change: `tests/*` or tooling test fixtures referenced by the workflow.
- Risks/assumptions: Test harness is available and stable.
- Tests to run: `make test`.

## Evidence Hints

- `tests/*` entries covering update/reapply CLI flow.
- Test plan alignment in `docs/02-features/03-update-reapply-templates/test-plan.md`.

## References

- Feature spec: `docs/02-features/03-update-reapply-templates/feature-spec.md` (Acceptance Criteria + Test Scenarios)
- Tech design: `docs/02-features/03-update-reapply-templates/tech-design.md` (CLI Commands)
- Test plan: `docs/02-features/03-update-reapply-templates/test-plan.md` (Test Strategy + Cases)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH):

## Change Budget

- Max files: 6
- Max new modules: 0
- Max lines changed (estimate): 240

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Add or update tests for the CLI workflow.
- Cover primary path and critical gates.
- Add fixtures as needed for repeatable runs.

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
