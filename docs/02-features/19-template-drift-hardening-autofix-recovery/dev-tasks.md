# Development Tasks: Template drift hardening + autofix recovery

> **LLM-executable tasks**

---

## Overview

**Feature:** Template drift hardening + autofix recovery

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

- [ ] **Task 1 - Define drift model and fixture matrix (data model)**
  - Define drift categories: one-sided, conflicting, out-of-scope.
  - Build fixture matrix covering critical paths.
  - **Acceptance:** Drift model and fixtures documented with explicit invariants.

- [ ] **Task 2 - Implement deterministic drift classification (pure logic)**
  - Implement classifier producing `auto-fix`, `manual`, or `block`.
  - Ensure deterministic outputs for identical inputs.
  - **Acceptance:** Classifier passes unit tests for all categories.

- [ ] **Task 3 - Harden edge cases and safety guards**
  - Enforce scoped restaging only for allowed touched paths.
  - Block ambiguous drift and out-of-scope modifications.
  - **Acceptance:** Safety guard tests pass; fail-close behavior is explicit.

- [ ] **Task 4 - Integrate precommit + CI autofix paths**
  - Wire shared drift logic into precommit and CI flow.
  - Preserve existing CI attempt limits and hook semantics.
  - **Acceptance:** Both gates behave consistently for equivalent drift cases.

- [ ] **Task 5 - Docs/log sync**
  - Update process docs for drift workflow changes.
  - Record decision/implementation/validation entries in `docs/03-logs/*`.
  - **Acceptance:** Final behavior documented with evidence.

## Allowed Tests (Planner must populate before Tester runs)

- `python3 -m unittest discover -s tests -p "test_pc_autofix.py"`
- `python3 -m unittest discover -s tests -p "test_pc_feature.py"`
- `python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"`

## Related Documents

- Feature Spec: `docs/02-features/19-template-drift-hardening-autofix-recovery/feature-spec.md`
- Tech Design: `docs/02-features/19-template-drift-hardening-autofix-recovery/tech-design.md`
- Test Plan: `docs/02-features/19-template-drift-hardening-autofix-recovery/test-plan.md`
- Planner Log: `docs/02-features/19-template-drift-hardening-autofix-recovery/planner-log.md`
- Plan Reviewer Log: `docs/02-features/19-template-drift-hardening-autofix-recovery/plan-reviewer-log.md`
- Reporter Log: `docs/02-features/19-template-drift-hardening-autofix-recovery/reporter-log.md`
- Validation Log: `docs/02-features/19-template-drift-hardening-autofix-recovery/validation-log.md`

## Change Log

| Date       | Changes       | Author |
| ---------- | ------------- | ------ |
| 2026-02-11 | Initial tasks | Codex  |
