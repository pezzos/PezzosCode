# Development Tasks: Synthetic feature workflow smoke test

> **LLM-executable tasks**

---

## Overview

**Feature:** Synthetic feature workflow smoke test

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

- [ ] **Task 1 - Define synthetic fixture schema (data model)**
  - Define minimal fake feature inputs and expected stage outcomes.
  - Define invariant checklist and evidence map.
  - **Acceptance:** Fixture schema and expected outputs documented.

- [ ] **Task 2 - Implement invariant evaluator (pure logic)**
  - Build evaluator for route/gate/log/resume invariants.
  - Return deterministic pass/fail payload with failed-stage details.
  - **Acceptance:** Evaluator unit tests pass for baseline and injected failures.

- [ ] **Task 3 - Harden edge-case scenarios**
  - Add scenarios for gate violation and resume recovery route.
  - Ensure stable assertions that avoid brittle implementation coupling.
  - **Acceptance:** Edge-case smoke scenarios provide actionable failures.

- [ ] **Task 4 - Integrate smoke path into workflow**
  - Add command/test entry point for synthetic workflow run.
  - Ensure artifacts are isolated from production feature state.
  - **Acceptance:** Synthetic run executes end-to-end with concise summary output.

- [ ] **Task 5 - Docs/log sync**
  - Document smoke-test run instructions and expected usage cadence.
  - Update decision/implementation/validation logs after rollout.
  - **Acceptance:** Process docs and logs reflect the smoke-test workflow.

## Allowed Tests (Planner must populate before Tester runs)

- `python3 -m unittest tests.test_pc_feature`
- `python3 -m unittest tests.test_orchestrator_workflow_docs`

## Related Documents

- Feature Spec: `docs/02-features/20-synthetic-feature-workflow-smoke-test/feature-spec.md`
- Tech Design: `docs/02-features/20-synthetic-feature-workflow-smoke-test/tech-design.md`
- Test Plan: `docs/02-features/20-synthetic-feature-workflow-smoke-test/test-plan.md`
- Planner Log: `docs/02-features/20-synthetic-feature-workflow-smoke-test/planner-log.md`
- Plan Reviewer Log: `docs/02-features/20-synthetic-feature-workflow-smoke-test/plan-reviewer-log.md`
- Reporter Log: `docs/02-features/20-synthetic-feature-workflow-smoke-test/reporter-log.md`
- Validation Log: `docs/02-features/20-synthetic-feature-workflow-smoke-test/validation-log.md`

## Change Log

| Date       | Changes       | Author |
| ---------- | ------------- | ------ |
| 2026-02-11 | Initial tasks | Codex  |
