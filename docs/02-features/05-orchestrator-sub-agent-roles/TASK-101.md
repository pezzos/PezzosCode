---
id: 101
title: "Define workflow behavior"
prd_ref: "P1 - Orchestrator + sub-agent roles"
status: "To Do"
status_timestamp: ""
complexity: "simple"
approval: ""
change_budget:
  max_files: 4
  max_new_modules: 0
---

<!-- allowed status: To Do | Ongoing | Done | Fail | Awaiting PO Approval -->
<!-- allowed complexity: simple | complex -->
<!-- set approval to "granted" to resume HIGH risk tickets -->

# Ticket: Define workflow behavior

## Title

Define workflow behavior

## Type

- Docs

## Context

- Task: Document required steps, gates, and outputs.
- Acceptance: Behavior is specified in docs.
- Estimate: 0.5 day.
- Feature context: Orchestrator + sub-agent roles (process feature, CLI-only workflow).
- References: `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md`, `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md`, `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md`.

## Scope

- **Choose one:** 1 feature folder
- In scope:
  - Define required workflow steps for orchestrator and sub-agent roles.
  - Document gates and outputs for each role in the flow.
- Out of scope:
  - Implementing tooling changes.
  - Adding or updating tests.

## PRD Traceability

- PRD feature/order: P1 - Orchestrator + sub-agent roles (Process Features)
- Link to PRD section: `docs/01-product/prd.md` (Process Features)

## Success Criteria

- [ ] Required steps, gates, and outputs are documented in feature docs.
- [ ] Behavior aligns with orchestrator/sub-agent role requirements.

## Definition of Done (Ticket-Specific)

- [ ] Feature docs describe orchestrator and sub-agent role responsibilities.
- [ ] Required gates and outputs are documented for each role.

## Plan (Draft)

- Approach: Update feature docs to specify role workflow, gates, and outputs.
- Files to change: `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md`, `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md`, `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md` (if needed), `docs/02-features/05-orchestrator-sub-agent-roles/dev-tasks.md` (status).
- Risks/assumptions: Assumes CLI-only workflow and current role separation model remains unchanged.
- Tests to run: None (docs-only).

## Evidence Hints

- `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md` (Workflow Steps, Role Responsibilities)
- `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md` (Role Flow, Gates)

## References

- Feature spec: `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md` (Summary + Requirements)
- Tech design: `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md` (Architecture + Constraints)
- Test plan: `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md` (Test Strategy + Cases)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH):

## Change Budget

- Max files: 4
- Max new modules: 0
- Max lines changed (estimate): 180

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Document orchestrator vs sub-agent responsibilities.
- Capture gates for handoffs and approvals.
- Record expected outputs per role.

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
