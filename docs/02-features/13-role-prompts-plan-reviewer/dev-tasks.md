# Development Tasks: Role prompts + Plan Reviewer

> **LLM-executable tasks**

---

## Overview

**Feature:** Role prompts + Plan Reviewer

**Status:** Not Started

**Last Updated:** 2026-02-08

## Task Breakdown

- [ ] **Task 1 - Prompt inventory audit**
  - Confirm every prompt path consumed by `tools/pc-feature` exists in `prompts/`.
  - Confirm matching template prompt files exist in `tools/templates/prompts/`.
  - Output: checked prompt matrix added to planner log or execution entry.

- [ ] **Task 2 - Prompt contract alignment**
  - Update outdated prompt wording for planner, plan-reviewer, tester, and reporter roles.
  - Ensure task-specific prompts (`*-create`, `*-update-from-feedback`, `plan-reviewer-gate`) remain consistent with protocol constraints.
  - Output: prompt wording aligned with current gate/Allowed Tests policy.

- [ ] **Task 3 - Workflow gate verification**
  - Add/update tests in `tests/test_pc_feature.py` for plan-reviewer approval, block-loop, and policy-conflict handling.
  - Ensure missing prompt files fail fast with actionable errors.
  - Output: passing tests that enforce prompt-loading and reviewer-gate behavior.

- [ ] **Task 4 - Process + log sync**
  - Update process docs if prompt/gate wording changed.
  - Update `docs/03-logs/implementation-log.md` and `docs/03-logs/validation-log.md` with concise evidence.
  - Output: docs/logs reflect the final behavior.

## Execution Log

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/13-role-prompts-plan-reviewer/feature-spec.md`
- Tech Design: `docs/02-features/13-role-prompts-plan-reviewer/tech-design.md`
- Test Plan: `docs/02-features/13-role-prompts-plan-reviewer/test-plan.md`
- Planner Log: `docs/02-features/13-role-prompts-plan-reviewer/planner-log.md`
- Reporter Log: `docs/02-features/13-role-prompts-plan-reviewer/reporter-log.md`
- Validation Log: `docs/02-features/13-role-prompts-plan-reviewer/validation-log.md`

## Change Log

| Date       | Changes                                           | Author       |
| ---------- | ------------------------------------------------- | ------------ |
| 2026-02-08 | Rebased tasks to current prompt/gate architecture | Codex        |
| 2026-02-05 | Initial task breakdown                            | Primary user |
