# Development Tasks: Incremental prd-to-features

> **LLM-executable tasks**

---

## Overview

**Feature:** Incremental prd-to-features

**Status:** Not Started

**Last Updated:** 2026-02-08

## Task Breakdown

- [ ] **Task 1 - Implement deterministic feature discovery**
  - Parse PRD feature list and existing feature folders with stable index mapping.
  - Handle slug/title drift without destructive actions.
  - Output: ordered action plan for each PRD feature.

- [ ] **Task 2 - Enforce additive-only generation**
  - Create missing feature folders from template.
  - Prevent duplicate folder creation and any deletion path.
  - Output: missing features created, existing features preserved.

- [ ] **Task 3 - Implement done-status skip + in-place updates**
  - Parse `Status:` from existing `dev-tasks.md`.
  - Skip `Status: Done` folders; update only missing sections for non-done folders.
  - Output: done features untouched; active features safely refreshed.

- [ ] **Task 4 - Add reporting, tests, and doc/log sync**
  - Add summary output with explicit `created/updated/skipped` reasons.
  - Add/update tests for done-skip, duplicate prevention, idempotent rerun, and no-delete guarantees.
  - Update relevant process docs and `docs/03-logs` with implementation/validation evidence.
  - Output: reproducible incremental workflow with traceability.

## Execution Log

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/12-incremental-prd-to-features/feature-spec.md`
- Tech Design: `docs/02-features/12-incremental-prd-to-features/tech-design.md`
- Test Plan: `docs/02-features/12-incremental-prd-to-features/test-plan.md`
- Planner Log: `docs/02-features/12-incremental-prd-to-features/planner-log.md`
- Reporter Log: `docs/02-features/12-incremental-prd-to-features/reporter-log.md`
- Validation Log: `docs/02-features/12-incremental-prd-to-features/validation-log.md`

## Change Log

| Date       | Changes                                       | Author       |
| ---------- | --------------------------------------------- | ------------ |
| 2026-02-08 | Rebased tasks to current incremental contract | Codex        |
| 2026-02-05 | Initial task breakdown                        | Primary user |
