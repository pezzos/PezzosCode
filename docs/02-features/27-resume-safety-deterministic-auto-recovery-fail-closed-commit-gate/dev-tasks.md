# Development Tasks: Resume safety + deterministic auto-recovery + fail-closed commit gate

> **LLM-executable tasks**

---

## Overview

Feature: Resume safety + deterministic auto-recovery + fail-closed commit gate

Priority: P0

Status: Not Started

Last Updated: 2026-02-20

Product Surfaces: CLI

## Ownership and Traceability

Source of truth: `dev-tasks.md` (tasks + execution log)

Roles (record names or agent ids):

- Orchestrator: Unassigned
- Planner: Unassigned
- Patcher: Unassigned
- Tester: Unassigned
- Reporter: Unassigned
- Product Owner: Unassigned

## Execution Log

Record each execution round here. Link any related logs in `docs/03-logs/`.

- No runs yet.

When execution starts, add a new work-item entry using
`docs/02-features/feature-template/dev-tasks.md` format.

## Task Breakdown

### Discovery and Spec Sync

- [ ] **TASK-001: Confirm requirements for `Resume safety + deterministic auto-recovery + fail-closed commit gate`**
  - Align acceptance criteria with PRD priority `P0` and requirements `FR-018, FR-011, FR-012`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-27-REQ-FR-018: map requirement to implementation**
  - Requirement: Expand deterministic auto-fix and auto-recovery for common failure classes.
  - Acceptance evidence: Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.
- [ ] **TASK-27-REQ-FR-011: map requirement to implementation**
  - Requirement: Post-run improvement proposals with human gate.
  - Acceptance evidence: Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.
- [ ] **TASK-27-REQ-FR-012: map requirement to implementation**
  - Requirement: Resume in-progress work items deterministically.
  - Acceptance evidence: Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

### Implementation

- [ ] **TASK-002: Implement `Resume safety + deterministic auto-recovery + fail-closed commit gate` capability**
  - Implement PRD outcome: Interrupted runs resume safely; common deterministic failures self-heal safely.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-018, FR-011, FR-012` plus at least one edge condition.
  - **Acceptance:** Tests guard against regressions.

### Validation and Reporting

- [ ] **TASK-004: Validate and capture evidence**
  - Run allowed tests and record results.
  - Capture offload ids for noisy command output.
  - **Acceptance:** Validation evidence is complete and reproducible.

- [ ] **TASK-005: Finalize docs and logs**
  - Update feature docs and required `docs/03-logs/` entries.
  - Summarize tradeoffs and follow-ups in Final Report.
  - **Acceptance:** Plan -> Patch -> Test -> Report is fully documented.
