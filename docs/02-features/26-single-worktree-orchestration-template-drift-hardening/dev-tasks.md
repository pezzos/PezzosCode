# Development Tasks: Single-worktree orchestration + template-drift hardening

> **LLM-executable tasks**

---

## Overview

Feature: Single-worktree orchestration + template-drift hardening

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

- [ ] **TASK-001: Confirm requirements for `Single-worktree orchestration + template-drift hardening`**
  - Align acceptance criteria with PRD priority `P0` and requirements `FR-014, FR-017, FR-018`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-26-REQ-FR-014: map requirement to implementation**
  - Requirement: Harden template drift detection and scoped autofix recovery.
  - Acceptance evidence: Workflow detects template/living-file drift, attempts deterministic scoped repairs, re-stages only allowed files, and fails with explicit remediation when unresolved.
- [ ] **TASK-26-REQ-FR-017: map requirement to implementation**
  - Requirement: Enforce token budget guardrails with compact summaries.
  - Acceptance evidence: Each role step records concise summaries, offloads overflow output, and reports deterministic remediation when budget guardrails are exceeded.
- [ ] **TASK-26-REQ-FR-018: map requirement to implementation**
  - Requirement: Expand deterministic auto-fix and auto-recovery for common failure classes.
  - Acceptance evidence: Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.

### Implementation

- [ ] **TASK-002: Implement `Single-worktree orchestration + template-drift hardening` capability**
  - Implement PRD outcome: Reliable role collaboration without worktree tracking-file drift.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-014, FR-017, FR-018` plus at least one edge condition.
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
