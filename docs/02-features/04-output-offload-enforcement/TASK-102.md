---
id: 102
title: "Implement or update tooling/scripts"
prd_ref: "P0 - Output offload enforcement"
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
- Feature context: Output offload enforcement (process feature, CLI-only workflow).
- References: `docs/02-features/04-output-offload-enforcement/feature-spec.md`, `docs/02-features/04-output-offload-enforcement/tech-design.md`, `docs/02-features/04-output-offload-enforcement/test-plan.md`.

## Scope

- **Choose one:** 1 mini change
- In scope:
  - Update tooling/templates to enforce offload behavior for noisy commands.
  - Ensure offload ids are recorded in outputs per spec.
- Out of scope:
  - Expanding beyond the output-offload workflow.
  - Building new tooling beyond what the feature requires.

## PRD Traceability

- PRD feature/order: P0 - Output offload enforcement (Process Features)
- Link to PRD section: `docs/01-product/prd.md` (Process Features)

## Success Criteria

- [ ] Tooling enforces the output offload workflow as documented.
- [ ] Offload ids are captured and referenced as required by the feature spec.

## Definition of Done (Ticket-Specific)

- [ ] Scripts/templates enforce the required offload steps and gates.
- [ ] Outputs reference offload ids instead of inline noisy output.

## Plan (Draft)

- Approach: Implement the enforcement points described in the feature spec/tech design.
- Files to change: `tools/` scripts and templates referenced by the feature docs, `docs/02-features/04-output-offload-enforcement/dev-tasks.md` (status).
- Risks/assumptions: Assumes current tooling already uses `tools/offload-proxy/pp` for large outputs.
- Tests to run: Targeted regression tests from the feature test plan.

## Evidence Hints

- `tools/` scripts enforcing offload behavior (updated calls to `tools/offload-proxy/pp`)
- `docs/02-features/04-output-offload-enforcement/test-plan.md` (updated test cases, if needed)

## References

- Feature spec: `docs/02-features/04-output-offload-enforcement/feature-spec.md` (Summary + Requirements)
- Tech design: `docs/02-features/04-output-offload-enforcement/tech-design.md` (Architecture + Constraints)
- Test plan: `docs/02-features/04-output-offload-enforcement/test-plan.md` (Test Strategy + Cases)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH):

## Change Budget

- Max files: 6
- Max new modules: 1
- Max lines changed (estimate): 260

## Human Gates

- [ ] Plan validated
- [ ] Diff validated
- [ ] Tests validated

## Implementation Notes

- Enforce offload usage in scripts that produce noisy output.
- Ensure offload id references are emitted where required.
- Keep changes minimal and aligned with the documented workflow.

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
