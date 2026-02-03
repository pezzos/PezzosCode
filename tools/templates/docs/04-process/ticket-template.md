---
id: 101
title: "<short>"
prd_ref: "<FR-XXX or feature id>"
status: "To Do"
status_timestamp: ""
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 10
  max_new_modules: 2
---

<!-- allowed status: To Do | Ongoing | Done | Fail | Awaiting PO Approval -->
<!-- allowed complexity: simple | complex -->

# Ticket Template

> Simple, consistent ticket format for 1 feature folder or 1 mini change.

## Title

## Type

- Feature / Bug / Refactor / Docs / Tech Debt

## Context

- What problem are we solving?
- Why now?

## Scope

- **Choose one:** 1 feature folder OR 1 mini change
- In scope:
- Out of scope:

## PRD Traceability

- PRD feature/order:
- Link to PRD section:

## Success Criteria

- [ ]
- [ ]

## Plan (Draft)

- Approach:
- Files to change:
- Risks/assumptions:
- Tests to run:

## Evidence Hints

- [Optional] Add 1-2 objective hints that prove completion (file + anchor).

## References

- Feature spec: docs/02-features/<feature>/feature-spec.md (see Summary + Requirements)
- Tech design: docs/02-features/<feature>/tech-design.md (see Architecture + Constraints)
- Test plan: docs/02-features/<feature>/test-plan.md (see Test Strategy + Cases)

## Risk Classification

- Risk level: [LOW|HIGH]
- Triggers (if HIGH):

## Change Budget

- Max files:
- Max new modules:
- Max lines changed (estimate):

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Key decisions:
- Trade-offs:

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

## Commit

- Message:
