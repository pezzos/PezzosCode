# Development Tasks: Workflow complexity reduction + skill inventory pruning

> **LLM-executable tasks**

---

## Overview

Feature: Workflow complexity reduction + skill inventory pruning

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

- [ ] **TASK-001: Confirm requirements for `Workflow complexity reduction + skill inventory pruning`**
  - Align acceptance criteria with PRD priority `P1` and requirements `FR-104, FR-105, FR-005`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Requirement Mapping

- [ ] **TASK-31-REQ-FR-104: map requirement to implementation**
  - Requirement: Prune low-value skill inventory regularly.
  - Acceptance evidence: Workflow includes periodic review to remove/archive unused or redundant skills while preserving required execution capabilities.
- [ ] **TASK-31-REQ-FR-105: map requirement to implementation**
  - Requirement: Reduce redundant execution paths and configuration complexity.
  - Acceptance evidence: Equivalent behavior is maintained while consolidating redundant paths; removed paths are documented with rollback notes.
- [ ] **TASK-31-REQ-FR-005: map requirement to implementation**
  - Requirement: Provide a shared runner library for tool/script execution.
  - Acceptance evidence: Tools can call a shared runner that injects `work_item_id`, `agent_name`, `run_id` and logging helpers.

### Implementation

- [ ] **TASK-002: Implement `Workflow complexity reduction + skill inventory pruning` capability**
  - Implement PRD outcome: Lower maintenance overhead with fewer fragile execution paths.
  - Target product surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end with documented constraints.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover requirement refs `FR-104, FR-105, FR-005` plus at least one edge condition.
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
