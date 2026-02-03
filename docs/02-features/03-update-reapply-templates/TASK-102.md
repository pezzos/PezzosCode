---
id: 102
title: "Implement or update tooling/scripts"
prd_ref: "P1 - Update/reapply templates"
status: "Done"
status_timestamp: "2026-02-03T14:17:36Z"
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 6
  max_new_modules: 1
---

# Ticket: Implement or update tooling/scripts

## Title

Implement or update tooling/scripts

## Type

- Feature

## Context

- Task: Update scripts or templates to enforce behavior.
- Acceptance: Tooling matches specification.
- Estimate: 1 day.
- Feature context: Update/reapply templates (CLI-only workflow).
- References: `docs/02-features/03-update-reapply-templates/feature-spec.md`, `docs/02-features/03-update-reapply-templates/tech-design.md`, `docs/02-features/03-update-reapply-templates/test-plan.md`.

## Scope

- **Choose one:** 1 feature folder
- In scope:
  - Implement or update CLI tooling to reapply templates safely.
  - Enforce overwrite/merge/skip behavior as specified.
- Out of scope:
  - New UI/TUI surfaces.
  - Cloud services or remote data transfer.

## PRD Traceability

- PRD feature/order: P1 - Update/reapply templates
- Link to PRD section: `docs/01-product/prd.md` (Prioritized Feature List)

## Success Criteria

- [ ] Tooling enforces the documented reapply workflow.
- [ ] Overwrite/merge/skip behavior matches the feature spec.

## Definition of Done (Ticket-Specific)

- [x] CLI tooling updates are implemented per spec.
- [x] Edge case handling for conflicts/partial updates is in place.
- [x] Documentation or logs updated if required by the workflow.

## Plan (Draft)

- Approach: Update the relevant CLI scripts to detect existing files and apply merge/skip/overwrite rules; align outputs and exit codes with the spec.
- Files to change: likely `tools/*` scripts and any templates referenced by update/reapply behavior.
- Risks/assumptions: Assumes macOS/local CLI execution; avoid destructive overwrites.
- Tests to run: `make test` (or targeted tests added in TASK-401).

## Evidence Hints

- `tools/*` script changes implementing overwrite/merge/skip gates.
- `docs/02-features/03-update-reapply-templates/tech-design.md` updates if architecture notes change.

## References

- Feature spec: `docs/02-features/03-update-reapply-templates/feature-spec.md` (Summary + Requirements + Edge Cases)
- Tech design: `docs/02-features/03-update-reapply-templates/tech-design.md` (Architecture + CLI Commands)
- Test plan: `docs/02-features/03-update-reapply-templates/test-plan.md` (Test Strategy + Cases)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH):

## Change Budget

- Max files: 6
- Max new modules: 1
- Max lines changed (estimate): 300

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Update scripts/templates that govern reapply behavior.
- Ensure overwrite/merge/skip options are enforced.
- Keep outputs and exit codes consistent with CLI expectations.

## Tests Run

- Command(s):
  - `make test`
  - `make ci`
- Result(s):
  - make test: PASS
  - make ci: PASS

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

- [x] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)

## Docs Updated

- [ ] Feature docs (feature-spec/tech-design/dev-tasks/test-plan)
- [ ] PRD (if scope/priority changed)
- [ ] Other: [list]

## Report (Final)

- What changed: docs/03-logs/tickets/03-102--implement-or-update-tooling-scripts.md
- Commands run (use `pp` for noisy output): `make test`, `make ci`
- Results: make test PASS; make ci PASS

## Commit

- Message:
