# Development Tasks: Resume in-progress tickets

> **LLM-executable tasks**

---

## Overview

**Feature:** Resume in-progress tickets

**Status:** Not Started

**Last Updated:** 2026-02-11

## Ownership and Traceability

**Source of truth:** `dev-tasks.md` (tasks + execution log)

**Role ownership:**

- Planner writes: this file (`dev-tasks.md`)
- Plan Reviewer writes: `plan-reviewer-log.md`
- Tester writes: `validation-log.md`
- Reporter writes: `reporter-log.md`
- Patcher edits implementation/docs except role-owned log files

## Execution Log

- No runs yet.

## Task Breakdown

- [ ] **Task 1 - Define resume state model (data model)**
  - Define normalized resume snapshot schema (completed steps, pending steps, dirty-state summary).
  - Define mode semantics for `auto`, `prompt`, `fresh`.
  - **Acceptance:** Snapshot and mode schema documented and test fixtures identified.

- [ ] **Task 2 - Implement resume routing logic (pure logic)**
  - Add deterministic routing from resume snapshot to next workflow step.
  - Enforce "tests and CI rerun" regardless of skipped steps.
  - **Acceptance:** Routing behavior matches protocol rules for planner/reviewer/tester/reporter restarts.

- [ ] **Task 3 - Harden resume edge cases**
  - Block contradictory artifact states with clear remediation.
  - Handle dirty worktree state per mode without unintended resets.
  - **Acceptance:** Fail-closed behavior validated by targeted tests.

- [ ] **Task 4 - Integrate with logs and user-facing workflow**
  - Emit structured resume decision entries in work-item logs.
  - Ensure resumed runs preserve traceability in `dev-tasks.md` and `logs/<WI>/`.
  - **Acceptance:** Resume decisions are visible and auditable.

- [ ] **Task 5 - Docs/log sync**
  - Update process docs if behavior changed.
  - Add implementation + validation entries in `docs/03-logs/*`.
  - **Acceptance:** Documentation reflects final resume semantics.

## Allowed Tests (Planner must populate before Tester runs)

- `python3 -m unittest tests.test_pc_feature.TestPcFeature`
- `python3 -m unittest tests.test_docs_logs`

## Related Documents

- Feature Spec: `docs/02-features/17-resume-in-progress-tickets/feature-spec.md`
- Tech Design: `docs/02-features/17-resume-in-progress-tickets/tech-design.md`
- Test Plan: `docs/02-features/17-resume-in-progress-tickets/test-plan.md`
- Planner Log: `docs/02-features/17-resume-in-progress-tickets/planner-log.md`
- Plan Reviewer Log: `docs/02-features/17-resume-in-progress-tickets/plan-reviewer-log.md`
- Reporter Log: `docs/02-features/17-resume-in-progress-tickets/reporter-log.md`
- Validation Log: `docs/02-features/17-resume-in-progress-tickets/validation-log.md`

## Change Log

| Date       | Changes       | Author |
| ---------- | ------------- | ------ |
| 2026-02-11 | Initial tasks | Codex  |
