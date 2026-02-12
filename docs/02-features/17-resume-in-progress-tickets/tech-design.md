# Technical Design: Resume in-progress tickets

> **Architecture & implementation approach**

---

## Overview

**Feature:** Resume in-progress tickets

**Status:** Completed

**Last Updated:** 2026-02-12

### Summary

Implement deterministic resume orchestration in `tools/pc-feature` so interrupted work items can continue from safe checkpoints.
The design uses artifact-state inspection, explicit resume policy modes, and fail-closed guards when state is inconsistent.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

## Technical Requirements

### From Feature Spec

- Auto-detect resumable state from existing work-item artifacts.
- Enforce `auto`/`prompt`/`fresh` behavior without ambiguity.
- Preserve WIP state unless explicit fresh reset is requested.
- Always re-run tests and final CI gate on resume.

### Technical Constraints

- Keep single-feature-worktree policy unchanged.
- Do not introduce background execution or schedulers.
- Keep logs deterministic and tail-friendly.

## Architecture

### System Context

- Entry point: `tools/pc-feature`
- Inputs: feature id, current worktree state, existing role logs/execution artifacts
- Outputs: resumed execution route, resume notes in logs, updated execution state

### Component Design

- Resume State Collector
  - Scans execution artifacts and role logs.
  - Produces normalized resume snapshot.
- Resume Policy Resolver
  - Applies mode-specific rules (`auto`, `prompt`, `fresh`).
  - Validates whether resume can proceed safely.
- Resume Router
  - Chooses next step in control flow based on completed/failed steps.
  - Enforces "tests and CI always rerun".
- Resume Logger
  - Writes explicit resume decisions and checkpoint notes.

### Data Model

- `resume_mode`: enum (`auto`, `prompt`, `fresh`)
- `resume_snapshot`: completed steps, pending steps, dirty-path summary, work-item id
- `resume_decision`: proceed/block/recreate and rationale

## Integration Points

- `docs/02-features/<feature>/dev-tasks.md` execution log state
- role logs (`planner-log.md`, `plan-reviewer-log.md`, `validation-log.md`, `reporter-log.md`)
- `logs/<WI>/<step>.log` structured outputs

## Implementation Approach

### Phase 1: Artifact and state detection

- Add deterministic parsing for existing work-item artifacts.
- Normalize dirty-state and completed-step signals.

### Phase 2: Policy enforcement and routing

- Apply resume policy rules.
- Route execution to correct restart point.

### Phase 3: Logging and validation hardening

- Emit explicit resume notes in logs.
- Add/extend tests for policy behavior and failure modes.

## Technical Decisions

### Decision 1: Repair pending planner-owned sections before fail-closed blocking

- Reason: stale pending placeholders can contradict valid role artifacts and cause avoidable resume failures.
- Outcome: attempt deterministic startup repair of pending execution sections from role artifacts, then fail closed if contradictions remain.

### Decision 2: Always rerun tests and final CI after resume

- Reason: prior pass results may be stale after resumed patches.
- Outcome: keep final quality gates trustworthy.

## Error Handling

- Missing required artifacts: continue as fresh start only when safe, else block.
- Conflicting completion markers: block and log remediation details.
- Dirty state with disallowed mode: prompt/block per policy.

## Testing Strategy

### Unit Tests

- Resume snapshot parsing from representative artifact sets.
- Policy resolver behavior by mode.

### Integration Tests

- End-to-end resume from planner/tester/reporter checkpoints.
- Dirty-worktree handling under `auto` vs `fresh`.

### E2E Tests

- Simulated interrupted work item resumed to completion with valid gates.

## Documentation Needs

- Update protocol/docs references if resume behavior semantics change.
- Record implementation and validation outcomes in `docs/03-logs/*`.

## Related Documents

- Feature Spec: `docs/02-features/17-resume-in-progress-tickets/feature-spec.md`
- Dev Tasks: `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`
- Test Plan: `docs/02-features/17-resume-in-progress-tickets/test-plan.md`

## Change Log

| Date       | Version | Changes        | Author |
| ---------- | ------- | -------------- | ------ |
| 2026-02-11 | 0.1     | Initial design | Codex  |
