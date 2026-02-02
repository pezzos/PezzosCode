---
id: 401
title: "Add or update tests"
prd_ref: "01"
status: "To Do"
status_reason: ""
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 10
  max_new_modules: 2
---

# Ticket: Add or update tests

> Simple, consistent ticket format for 1 feature folder or 1 mini change.

## Title

Add or update tests

## Type

- Feature

## Context

- Feature: Bootstrap Templates Into A Repo
- Summary: See feature-spec.md
- Task: Add or update tests
- Acceptance: Tests cover the primary path
- Estimate: 0.5 day
- Derived from dev-tasks.md

## Scope

- **Choose one:** 1 feature folder OR 1 mini change
- In scope: Complete the task as defined in dev-tasks.md
- Out of scope: Unrelated feature work

## PRD Traceability

- PRD feature/order: 01 (P0)
- Link to PRD section: Prioritized Feature List

## Success Criteria

- [ ] Tests cover the primary path
- [ ] Gates and logs updated

## Definition of Done (Ticket-Specific)

- [ ] Tests cover the primary path
- [ ] Relevant tests updated and passing
- [ ] Logs/docs updated if required by this task

## Plan (Draft)

- Add regression tests or checks where applicable

## Evidence Hints

- [Optional] Add 1-2 objective hints that prove completion (file + anchor).

## References

- Feature spec: feature-spec.md (Summary, Feature Requirements)
- Tech design: tech-design.md (Technical Requirements, Architecture)
- Test plan: test-plan.md (Test Strategy, Test Cases)
- Dev tasks: dev-tasks.md (Task Breakdown for TASK-401)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH): N/A

## Change Budget

- Max files: 10
- Max new modules: 2
- Max lines changed (estimate): 500

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Expected changes:
- Add regression tests or checks where applicable
- Key decisions: TBD
- Trade-offs: TBD

## Tests Run

- Command(s): make ci (or agreed test command)
- Result(s): TBD

## Implementer Notes

- Implementation choices: TBD
- Edge cases covered: TBD
- Files changed: TBD

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

- [ ] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)

## Docs Updated

- [ ] Feature docs (feature-spec/tech-design/dev-tasks/test-plan)
- [ ] PRD (if scope/priority changed)
- [ ] Other: TBD

## Report (Final)

- What changed: TBD
- Commands run (use `pp` for noisy output): TBD
- Results: TBD

## Commit

- Message: TBD
