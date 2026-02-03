---
id: 102
title: "Implement or update tooling/scripts"
prd_ref: "P1 - Orchestrator + sub-agent roles"
status: "To Do"
status_timestamp: ""
complexity: "simple"
approval: ""
change_budget:
  max_files: 6
  max_new_modules: 1
---

<!-- allowed status: To Do | Ongoing | Done | Fail | Awaiting PO Approval -->
<!-- allowed complexity: simple | complex -->
<!-- set approval to "granted" to resume HIGH risk tickets -->

# Ticket: Implement or update tooling/scripts

## Title

Implement or update tooling/scripts

## Type

- Feature

## Context

- Task: Update scripts or templates to enforce behavior.
- Acceptance: Tooling matches specification.
- Estimate: 1 day.
- Feature context: Orchestrator + sub-agent roles (process feature, CLI-only workflow).
- References: `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md`, `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md`, `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md`.

## Scope

- **Choose one:** 1 mini change
- In scope:
  - Update tooling/templates to enforce orchestrator and sub-agent role flows.
  - Ensure role handoffs and gates are enforced per spec.
- Out of scope:
  - Expanding beyond the orchestrator/sub-agent workflow.
  - Building new tooling beyond what the feature requires.

## PRD Traceability

- PRD feature/order: P1 - Orchestrator + sub-agent roles (Process Features)
- Link to PRD section: `docs/01-product/prd.md` (Process Features)

## Success Criteria

- [ ] Tooling enforces the orchestrator/sub-agent workflow as documented.
- [ ] Role handoffs and gates are executed as required by the feature spec.

## Definition of Done (Ticket-Specific)

- [ ] Scripts/templates enforce required role steps and approvals.
- [ ] Outputs reference the correct role transitions and artifacts.

## Plan (Draft)

- Approach: Implement enforcement points described in the feature spec/tech design.
- Files to change: `tools/` scripts and templates referenced by the feature docs, `docs/02-features/05-orchestrator-sub-agent-roles/dev-tasks.md` (status).
- Risks/assumptions: Assumes existing tooling already supports role separation patterns.
- Tests to run: Targeted regression tests from the feature test plan.

## Evidence Hints

- `tools/` scripts enforcing role workflow gates.
- `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md` (updated test cases, if needed)

## References

- Feature spec: `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md` (Summary + Requirements)
- Tech design: `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md` (Architecture + Constraints)
- Test plan: `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md` (Test Strategy + Cases)

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

- Enforce orchestrator/sub-agent role steps in scripts.
- Ensure handoff gates and approvals are recorded.
- Keep changes minimal and aligned with documented workflow.

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
