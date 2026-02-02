---
id: 102
title: "Implement or update tooling/scripts"
prd_ref: "01"
status: "Done"
status_reason: "Tooling updated; tests and gates passing."
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 10
  max_new_modules: 2
---

# Ticket: Implement or update tooling/scripts

> Simple, consistent ticket format for 1 feature folder or 1 mini change.

## Title

Implement or update tooling/scripts

## Type

- Feature

## Context

- Feature: Bootstrap Templates Into A Repo
- Summary: See feature-spec.md
- Task: Implement or update tooling/scripts
- Acceptance: Tooling matches specification
- Estimate: 1 day
- Derived from dev-tasks.md

## Scope

- **Choose one:** 1 feature folder OR 1 mini change
- In scope: Complete the task as defined in dev-tasks.md
- Out of scope: Unrelated feature work

## PRD Traceability

- PRD feature/order: 01 (P0)
- Link to PRD section: Prioritized Feature List

## Success Criteria

- [x] Tooling matches specification
- [x] Gates and logs updated

## Definition of Done (Ticket-Specific)

- [x] Tooling matches specification
- [x] Relevant tests updated and passing
- [x] Logs/docs updated if required by this task

## Plan (Draft)

- Update scripts or templates to enforce behavior

## Evidence Hints

- tools/bootstrap-into: git repo guard + conflict prompt handling
- tools/pc-ticket: ticket id normalization with T-/TASK- prefixes

## References

- Feature spec: feature-spec.md (Summary, Feature Requirements)
- Tech design: tech-design.md (Technical Requirements, Architecture)
- Test plan: test-plan.md (Test Strategy, Test Cases)
- Dev tasks: dev-tasks.md (Task Breakdown for TASK-102)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH): N/A

## Change Budget

- Max files: 10
- Max new modules: 2
- Max lines changed (estimate): 500

## Human Gates

- [x] Plan validated
- [x] Diff validated
- [x] Tests validated

## Implementation Notes

- Expected changes:
- Update scripts or templates to enforce behavior
- Key decisions: Preserve original stdin for prompts to avoid process-substitution conflicts; normalize ticket IDs for display while keeping numeric IDs for bootstrap/worklog lookup.
- Trade-offs: Merge action remains unsupported and logs a skip warning instead of attempting an automated merge.

## Tests Run

- Command(s): python -m unittest discover -s tests; make ci
- Result(s): pass

## Implementer Notes

- Implementation choices: Added git repo guard and prompt-driven overwrite/skip path for syncable files; ensured prompt reads from preserved stdin.
- Edge cases covered: Non-git target repo fails fast; existing syncable files can be skipped via prompt.
- Files changed: tools/bootstrap-into, tools/pc-ticket

## Tester Feedback

- Tests executed: TBD
- Failures observed: TBD
- Suggested fixes: TBD

## Reviewer Feedback

- Issues found: TBD
- Suggestions: TBD
- Approval status: TBD

## Iteration Log

- [ ] Implementer updated after tester feedback
- [ ] Implementer updated after reviewer feedback

## Logs Updated

- [x] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)

## Docs Updated

- [ ] Feature docs (feature-spec/tech-design/dev-tasks/test-plan)
- [ ] PRD (if scope/priority changed)
- [x] Other: docs/03-logs/tickets/102--implement-or-update-tooling-scripts.md

## Report (Final)

- What changed: Updated bootstrap tooling to enforce git repo requirement and prompt for existing syncable files; improved ticket id normalization while keeping numeric lookup.
- Commands run (use `pp` for noisy output): python -m unittest discover -s tests; make ci
- Results: tests and CI pass

## Commit

- Message: TBD
