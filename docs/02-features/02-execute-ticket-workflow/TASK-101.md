---
id: 101
title: "Define workflow behavior"
prd_ref: "02"
status: "Done"
status_timestamp: "2026-02-03T08:29:00Z"
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 10
  max_new_modules: 2
---

# Ticket: Define workflow behavior

> Simple, consistent ticket format for 1 feature folder or 1 mini change.

## Title

Define workflow behavior

## Type

- Docs

## Context

- Feature: Execute ticket workflow
- Summary: See feature-spec.md
- Task: Define workflow behavior
- Acceptance: Behavior is specified in docs
- Estimate: 0.5 day
- Derived from dev-tasks.md

## Scope

- **Choose one:** 1 feature folder OR 1 mini change
- In scope: Document required steps, gates, and outputs for the ticket workflow
- Out of scope: Unrelated feature work or implementation changes

## PRD Traceability

- PRD feature/order: 02 (P0)
- Link to PRD section: Prioritized Feature List

## Success Criteria

- [ ] Behavior is specified in docs
- [ ] Gates and logs updated

## Definition of Done (Ticket-Specific)

- [x] Behavior is specified in docs
- [x] Relevant docs/logs updated

## Plan (Draft)

- Document required steps, gates, and outputs
- Update process docs to match the defined workflow

## Evidence Hints

- File: docs/04-process/dev-workflow.md contains: "Plan → Patch → Test → Report"
- File: docs/04-process/ticket-execution-protocol.md contains: "Plan → Patch → Test → Report"

## References

- Feature spec: feature-spec.md (Summary, Feature Requirements)
- Tech design: tech-design.md (Technical Requirements, Architecture)
- Test plan: test-plan.md (Test Strategy, Test Cases)
- Dev tasks: dev-tasks.md (Task Breakdown for TASK-101)

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

- Expected changes: Document required steps, gates, and outputs
- Key decisions: TBD
- Trade-offs: TBD

## Tests Run

- Command(s): TBD
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
- [ ] Other: docs/04-process/ticket-execution-protocol.md
- [ ] Other: docs/04-process/dev-workflow.md

## Report (Final)

- What changed:
- Commands run (use `pp` for noisy output):
- Results:

## Commit

- Message:
