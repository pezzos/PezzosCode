# Feature Specification: Resume in-progress tickets

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-17`

**Status:** Completed

**Owner:** Developer/PO

**Last Updated:** 2026-02-12

### Summary

Allow `make feature` runs to resume safely from existing execution artifacts instead of restarting from scratch.
Resume behavior must be deterministic, preserve in-progress work by default, and keep final gates trustworthy.

## User Intent

### Who is this for?

- Primary: Developer/PO running ticket execution repeatedly on the same feature.

### Why do they need it?

- Interrupted runs should not force manual reconstruction of context, plans, or role outputs.
- Safe resume reduces rework, token waste, and accidental loss of worktree state.

### User Value

- Faster recovery after failures/interruption.
- Predictable continuation from the correct workflow step.
- Fewer manual "cleanup before rerun" interventions.

## Feature Requirements

### Functional Requirements

- [ ] Detect existing work-item artifacts and determine resumable state automatically.
- [ ] Support resume policy modes (`auto`, `prompt`, `fresh`) with deterministic behavior.
- [ ] Preserve dirty active feature-worktree changes in `auto`/`prompt`; reset only in explicit `fresh` mode.
- [ ] Skip already-completed steps where safe, while always re-running tests and final CI gate.
- [ ] Record resume decisions and checkpoints in role/workflow logs.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Resume detection must be idempotent across repeated invocations.
- Resume logic must fail closed when artifact state is contradictory.
- Resume decisions must be traceable in logs for debugging.

## Acceptance Criteria

### Definition of Done

- A stopped run can be resumed without losing valid prior outputs.
- Resume policy behavior matches selected mode.
- Tests/CI are always re-executed on resumed runs.
- Documentation and logs reflect resume-state decisions.

### Test Scenarios

- Resume from a run stopped after planner step; skip planner init and continue at next gate.
- Resume from a run with dirty patcher worktree in `auto`; checkpoint state and continue safely.
- Attempt resume with incompatible artifact state; run blocks with explicit remediation.

### Success Metrics

- Reduced rate of full-run restarts after interruptions.
- Reduced manual cleanup steps before re-running `make feature`.

## Scope

### In Scope

- Resume-state detection and policy selection.
- Artifact-aware step skipping rules.
- Logging of resume decisions and recovery actions.

### Out of Scope

- Multi-feature concurrent resume orchestration.
- Background/daemon resume automation.

## Dependencies

### Requires

- `tools/pc-feature`
- `docs/04-process/ticket-execution-protocol.md`
- Work-item artifacts under `docs/02-features/<feature>/` and `logs/<WI>/`

### Blocks

- Commit-gating and smoke-test features that depend on reliable reruns.

## Risks & Considerations

- Incorrect skip logic could hide required validation.
- Aggressive reset behavior could discard user WIP.

## Open Questions

- Should `prompt` mode be interactive-only or support non-interactive default policy override?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Process Protocol: `docs/04-process/ticket-execution-protocol.md`
- Workflow: `docs/04-process/dev-workflow.md`

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                | Risk                                                                                                                                                                                                                | Action                                                                                                                                                                                                                         |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEC-17-001 | High     | patcher | automated-test | Yes      | Required resume safety tests are not consistently enforced           | Work-item history shows repeated `tests.test_docs_logs` failures/skips and `needs replan` outcomes while resume work continued, so fail-closed resume/traceability controls can be bypassed in practice.            | Make both Allowed Tests mandatory for resumed and non-resumed paths; hard-fail execution when either test is missing or non-zero, and add a regression asserting resume cannot advance after docs-log contract failure.        |
| SEC-17-002 | High     | patcher | patch          | Yes      | `prompt` mode is security-ambiguous in non-interactive runs          | The feature spec leaves an open question for `prompt` behavior; in CI/non-TTY contexts this can silently choose resume/fresh behavior, causing unintended reset of WIP or unsafe continuation.                      | Define and implement deterministic non-interactive behavior now (recommended: `prompt` fails closed unless explicit override flag is provided) and cover TTY/non-TTY cases in tests.                                           |
| SEC-17-003 | High     | patcher | automated-test | Yes      | Contradictory artifact handling lacks completed proof of enforcement | Feature requirements demand fail-closed blocking on contradictory artifacts, but multiple execution blocks remain pending/needs-replan, so there is no reliable evidence the contradiction gate cannot be bypassed. | Centralize resume-state validation before any role routing; reject contradictory/malformed/missing-critical artifact combinations with explicit remediation and add deterministic negative tests for each contradiction class. |
| SEC-17-004 | Medium   | patcher | automated-test | Yes      | Resume audit trail completeness is not guaranteed                    | Reporter failures explicitly cite missing Patch/Test/Reporter execution fields; incomplete logs weaken forensic traceability and commit-gate integrity for resumed runs.                                            | Enforce required resume checkpoint/evidence fields in writer logic and docs-log tests, and block completion when any required field is missing.                                                                                |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                     | Risk                                                                                                                                                     | Action                                                                                                                                                                                                    |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-17-001 | High     | patcher | automated-test   | Yes      | Resume path can pass with incomplete quality gates        | Run history shows resumed flow continued while `tests.test_docs_logs` failed or was skipped, so users can get unsafe continuation with false confidence. | Require both Allowed Tests on every resumed and non-resumed run; hard-stop progression when either test is missing or non-zero; add regression proving resume cannot advance after docs-log test failure. |
| PROD-17-002 | High     | patcher | patch            | Yes      | Non-interactive `prompt` behavior is ambiguous            | In non-TTY/CI contexts, undefined `prompt` handling can silently continue stale state or reset active WIP, causing user data/workflow loss.              | Implement deterministic non-interactive policy (fail closed unless explicit override), with TTY/non-TTY tests and explicit CLI messaging.                                                                 |
| PROD-17-003 | High     | patcher | automated-test   | Yes      | Contradictory artifact handling is not proven fail-closed | Users may be routed to the wrong step and skip required validation gates if contradictory/malformed artifact combinations are not centrally blocked.     | Centralize resume-state validation before routing; reject contradictory/malformed/missing-critical artifacts with clear remediation; add deterministic negative tests per contradiction class.            |
| PROD-17-004 | Medium   | patcher | automated-test   | Yes      | Resume audit trail completeness is inconsistent           | Missing Patch/Test/Reporter checkpoints reduce user ability to understand what resumed, what reran, and why completion is blocked.                       | Enforce required resume checkpoint fields in writer logic and docs-log tests, and block completion when required evidence is missing.                                                                     |
| PROD-17-005 | Medium   | human   | human-validation | Yes      | Risky resume-choice UX needs human sign-off               | Even with technical fixes, unclear `auto`/`prompt`/`fresh` wording can lead users to destructive choices and perceived workflow unreliability.           | Run PO/end-user validation of resume prompts and summaries on interrupted-run scenarios; approve wording/defaults before release.                                                                         |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
