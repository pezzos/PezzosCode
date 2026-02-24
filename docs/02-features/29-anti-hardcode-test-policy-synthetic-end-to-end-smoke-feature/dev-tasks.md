# Development Tasks: Anti-hardcode test policy + synthetic end-to-end smoke feature

> **LLM-executable tasks**

---

## Overview

Feature: Anti-hardcode test policy + synthetic end-to-end smoke feature

Priority: P1

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

- [ ] **TASK-001: Confirm requirements for `Anti-hardcode test policy + synthetic end-to-end smoke feature`**
  - Align acceptance criteria with PRD priority `P1` and requirements `FR-102, FR-103, FR-002`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-29-REQ-FR-102: map requirement to implementation**
  - Requirement: Provide a synthetic feature for end-to-end workflow smoke testing.
  - Acceptance evidence: A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.
- [ ] **TASK-29-REQ-FR-103: map requirement to implementation**
  - Requirement: Enforce anti-hardcode testing coverage.
  - Acceptance evidence: Plan/TDD states fixture count (>=2 critical-path fixtures), deterministic seed strategy, invariant assertions, and boundary contract tests.
- [ ] **TASK-29-REQ-FR-002: map requirement to implementation**
  - Requirement: Execute a ticket end-to-end with AI and minimal manual work.
  - Acceptance evidence: Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.

### Implementation

- [ ] **TASK-002: Implement `Anti-hardcode test policy + synthetic end-to-end smoke feature` capability**
  - Implement PRD outcome: Better regression resistance and early workflow break detection.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-102, FR-103, FR-002` plus at least one edge condition.
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
