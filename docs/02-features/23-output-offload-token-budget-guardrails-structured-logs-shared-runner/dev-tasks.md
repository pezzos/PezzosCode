# Development Tasks: Output offload + token budget guardrails + structured logs + shared runner

> **LLM-executable tasks**

---

## Overview

Feature: Output offload + token budget guardrails + structured logs + shared runner

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

- [ ] **TASK-001: Confirm requirements for `Output offload + token budget guardrails + structured logs + shared runner`**
  - Align acceptance criteria with PRD priority `P0` and requirements `FR-017, FR-004, FR-006`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-23-REQ-FR-017: map requirement to implementation**
  - Requirement: Enforce token budget guardrails with compact summaries.
  - Acceptance evidence: Each role step records concise summaries, offloads overflow output, and reports deterministic remediation when budget guardrails are exceeded.
- [ ] **TASK-23-REQ-FR-004: map requirement to implementation**
  - Requirement: Offload noisy command output.
  - Acceptance evidence: Noisy outputs are stored in `.offload/`, referenced by id, and retrievable through deterministic index metadata.
- [ ] **TASK-23-REQ-FR-006: map requirement to implementation**
  - Requirement: Write structured, tail-friendly logs for CI/tests/precommit/feature runs.
  - Acceptance evidence: Logs are written to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix and timestamps.

### Implementation

- [ ] **TASK-002: Implement `Output offload + token budget guardrails + structured logs + shared runner` capability**
  - Implement PRD outcome: Noisy output stays token-efficient and every step is traceable.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-017, FR-004, FR-006` plus at least one edge condition.
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
