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

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                    |
| ---------- | -------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| SEC-17-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios. |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                          |
| ----------- | -------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| PROD-17-001 | High     | Key product capabilities may be missed during implementation.           | Expand functional requirements to cover primary and edge behaviors with acceptance criteria.    |
| PROD-17-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                           |
| PROD-17-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Resume in-progress tickets' journey and workflow. |
| PROD-17-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.    |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
