# Development Tasks: Bootstrap + safe template reapply

> **LLM-executable tasks**

---

## Overview

Feature: Bootstrap + safe template reapply

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

- [ ] **TASK-001: Confirm requirements for `Bootstrap + safe template reapply`**
  - Align acceptance criteria with PRD priority `P0` and requirements `FR-101, FR-003, FR-012`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-22-REQ-FR-101: map requirement to implementation**
  - Requirement: Reapply templates to existing repos safely.
  - Acceptance evidence: Conflicts handled by overwrite/merge/skip; idempotent reruns.
- [ ] **TASK-22-REQ-FR-003: map requirement to implementation**
  - Requirement: Require ticket-specific Definition of Done before coding.
  - Acceptance evidence: Ticket template includes explicit work-item DoD; execution blocks patching until DoD, tests, and report sections are defined.
- [ ] **TASK-22-REQ-FR-012: map requirement to implementation**
  - Requirement: Resume in-progress work items deterministically.
  - Acceptance evidence: Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

### Implementation

- [ ] **TASK-002: Implement `Bootstrap + safe template reapply` capability**
  - Implement PRD outcome: New/existing repos become execution-ready with idempotent reruns.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-101, FR-003, FR-012` plus at least one edge condition.
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
