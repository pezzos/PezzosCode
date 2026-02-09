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

### WI-20260209-01 - Work item execution

- Date: 2026-02-09
- Scope / tasks covered:
- Planner: Codex
- Plan Reviewer: Codex
- Patcher:
- Tester:
- Reporter:
- Outcome: needs replan
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes: Main head locked: 76446b1a7824683141ea6bd986cddfa46091228f

#### Preflight Report

- Work Item: WI-20260209-01
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Incremental feature generation from PRD priority list', 'Add-only behavior for missing feature folders', 'Skip features with Status: Done in dev-tasks.md', 'Update-in-place for existing non-done features (missing sections only)', 'Action summary with created/updated/skipped + reasons']
- Scope out: ['Rewriting completed feature folders', 'Automatic reindex/rename of existing feature folders', 'Generating non-PRD features']
- Non-goals reminder: Do not delete or overwrite existing feature folders; do not regenerate features marked Status: Done; do not reindex/rename existing folders automatically.
- Files to change: (none)
- Change budget: max_files=6, max_new_modules=1
- TDD plan: python -m unittest discover -s tests -p "test\_\*.py"
- Systematic review:

#### TDD Plan

- Tests to write first:
  - python -m unittest discover -s tests -p "test\_\*.py"

#### Allowed Tests

- `python -m unittest discover -s tests -p 'test_*.py'`

#### Files to Change + Change Budget

- Files: (none)
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- (none)

#### Plan

Plan Contract v1
Approach:

1. Inspect current `prd-to-features` implementation and tests to locate generation flow, status parsing, and summary reporting gaps; align behavior to incremental contract.
   Files to change:

- scripts or modules implementing `prd-to-features` (exact path TBD after inspection)
- tests covering feature generation (exact path TBD after inspection)
- feature docs as needed for spec alignment (excluding role-scoped logs)
  Risks:
- Incorrect status parsing could reprocess done features.
- Update-in-place logic could accidentally overwrite completed sections.
  Tests (anti-hardcode coverage required):
- Fixture coverage: At least 2 fixtures per critical path (missing folder, existing done, existing non-done with missing sections, malformed/missing Status).
- Deterministic seed strategy: Fixed seed for any randomized ordering or fixture generation; avoid nondeterministic filesystem iteration by sorting.
- Invariant checks: Assert no deletes, no duplicates, idempotent rerun produces no changes.
- Contract boundary coverage: Validate behavior when `dev-tasks.md` missing or Status line malformed; validate slug/title drift handling.
- Allowed test commands:
  - python -m unittest discover -s tests -p "test\_\*.py"

Work Item ID: WI-20260209-01

#### Patch

- (pending)

#### Test Results

- (pending)

#### Reporter Review

- (pending)

#### Gates

- make ci: PASS

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

- Attempt 1: allowed-tests validation failed; routed back to planner. Issues: no allowed tests listed.
- Attempt 1: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 1: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 1: reporter no-op; reason=blocked by invalid allowed tests.
- Attempt 2: allowed-tests validation failed; routed back to planner. Issues: no allowed tests listed.
- Attempt 2: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 2: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 2: reporter no-op; reason=blocked by invalid allowed tests.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=3/3).
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_attempt=3/3).
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (reviewer_block=3/12, planner_revision=3/12, execution_attempt=3/3).

#### Commit

- Commit message:

#### Final Report

-

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
