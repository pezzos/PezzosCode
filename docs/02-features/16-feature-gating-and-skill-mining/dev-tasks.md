# Development Tasks: Feature gating + skill mining

> **LLM-executable tasks**

---

## Overview

**Feature:** Feature gating + skill mining

**Status:** Not Started

**Last Updated:** 2026-02-08

## Task Breakdown

- [ ] **Task 1 - Implement feature status parser**
  - Parse ordered feature folders and each `dev-tasks.md` `Status` value.
  - Handle malformed/missing status values with explicit fallback warnings.
  - Output: deterministic status map for gating checks.

- [ ] **Task 2 - Add precommit soft warning**
  - In `tools/pc-precommit`, warn when editing feature `N` while earlier features are not `Done`.
  - Ensure warning is advisory only and does not block commit.
  - Output: actionable sequencing warning with remediation hints.

- [ ] **Task 3 - Implement skill-mining proposal generator**
  - Detect repeated prompt/workflow patterns using bounded thresholds.
  - Emit candidate skill proposals with evidence references.
  - Output: reviewable skill proposals (no auto-install).

- [ ] **Task 4 - Add tests and docs/log sync**
  - Add tests for status parsing, warning behavior, and mining thresholds.
  - Update process docs and `docs/03-logs` entries with implementation/validation evidence.
  - Output: validated behavior and traceable documentation.

## Execution Log

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/16-feature-gating-and-skill-mining/feature-spec.md`
- Tech Design: `docs/02-features/16-feature-gating-and-skill-mining/tech-design.md`
- Test Plan: `docs/02-features/16-feature-gating-and-skill-mining/test-plan.md`
- Planner Log: `docs/02-features/16-feature-gating-and-skill-mining/planner-log.md`
- Reporter Log: `docs/02-features/16-feature-gating-and-skill-mining/reporter-log.md`
- Validation Log: `docs/02-features/16-feature-gating-and-skill-mining/validation-log.md`

## Change Log

| Date       | Changes                                                                  | Author       |
| ---------- | ------------------------------------------------------------------------ | ------------ |
| 2026-02-09 | Aligned workflow baseline to remove change-budget fields/section wording | Codex        |
| 2026-02-08 | Rebased tasks to sequencing warning + skill mining flow                  | Codex        |
| 2026-02-05 | Initial task breakdown                                                   | Primary user |
