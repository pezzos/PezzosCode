# Development Tasks: Commit gated by completed ticket docs

> **LLM-executable tasks**

---

## Overview

**Feature:** Commit gated by completed ticket docs

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

## Task Breakdown

- [ ] **Task 1 - Define mandatory commit-doc checklist (data model)**
  - Identify required sections and evidence fields from protocol/docs.
  - Define normalization for section presence detection.
  - **Acceptance:** Checklist documented and traceable to protocol references.

- [ ] **Task 2 - Implement completeness evaluator (pure logic)**
  - Parse execution docs and evaluate required-section coverage.
  - Return structured missing-field diagnostics.
  - **Acceptance:** Deterministic pass/fail output for complete/incomplete fixtures.

- [ ] **Task 3 - Handle edge cases and fail-closed policy**
  - Handle malformed markdown, duplicate sections, and conflicting states.
  - Prevent false pass when evidence is ambiguous.
  - **Acceptance:** Ambiguous inputs block commit with remediation guidance.

- [ ] **Task 4 - Integrate gate with commit flow**
  - Wire evaluator into final commit gate.
  - Ensure blocking behavior is explicit and logged.
  - **Acceptance:** Commit path denied on incomplete docs and allowed on complete docs.

- [ ] **Task 5 - Docs/log sync**
  - Update process docs if commit-gate semantics change.
  - Record implementation and validation outcomes in `docs/03-logs/*`.
  - **Acceptance:** Documentation and logs match final behavior.

## Allowed Tests (Planner must populate before Tester runs)

- `python3 -m unittest tests.test_pc_feature.TestPcFeature`
- `python3 -m unittest tests.test_docs_logs`

## Related Documents

- Feature Spec: `docs/02-features/18-commit-gated-by-completed-ticket-docs/feature-spec.md`
- Tech Design: `docs/02-features/18-commit-gated-by-completed-ticket-docs/tech-design.md`
- Test Plan: `docs/02-features/18-commit-gated-by-completed-ticket-docs/test-plan.md`
- Planner Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/planner-log.md`
- Plan Reviewer Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/plan-reviewer-log.md`
- Reporter Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/reporter-log.md`
- Validation Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/validation-log.md`

## Change Log

| Date       | Changes       | Author |
| ---------- | ------------- | ------ |
| 2026-02-11 | Initial tasks | Codex  |
