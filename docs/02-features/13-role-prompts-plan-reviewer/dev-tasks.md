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
- Notes: Main head locked: e37428dd1b91b6ebb45d07c0538c91adac7d325f

#### Preflight Report

- Work Item: WI-20260209-01
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: Prompt contracts and prompt-file parity; Plan Reviewer gate wording/guardrails; Process-doc alignment for role prompts; Tests covering prompt loading and gate flow.
- Scope out: Reordering workflow gates; New agent roles beyond current Planner/Plan Reviewer/Patcher/Tester/Reporter model; UI or API surfaces.
- Non-goals reminder: Do not add new roles or change workflow order; no UI/API work.
- Files to change: tools/pc-feature, tests/test_pc_feature.py, prompts/, tools/templates/prompts/, docs/04-process/ticket-execution-protocol.md, docs/03-logs/implementation-log.md
- Change budget: max_files=6, max_new_modules=1
- TDD plan: prompt loading succeeds for base + task variants, missing prompt file fails with actionable error, plan-reviewer approve path, plan-reviewer block/retry path, plan-reviewer policy conflict path
- Systematic review:

#### TDD Plan

- Tests to write first:
  - prompt loading succeeds for base + task variants
  - missing prompt file fails with actionable error
  - plan-reviewer approve path
  - plan-reviewer block/retry path
  - plan-reviewer policy conflict path

#### Allowed Tests

- `python -m unittest discover -s tests -p 'test_*.py'`
- `pytest tests/test_pc_feature.py`

#### Files to Change + Change Budget

- Files: tools/pc-feature, tests/test_pc_feature.py, prompts/, tools/templates/prompts/, docs/04-process/ticket-execution-protocol.md, docs/03-logs/implementation-log.md
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- docs/04-process/ticket-execution-protocol.md
- docs/04-process/dev-workflow.md
- docs/04-process/human-orchestration-workflow.md
- docs/03-logs/implementation-log.md
- docs/03-logs/validation-log.md

#### Plan

Plan Contract v1
Approach:

1. Audit prompt inventory and template parity, then map required prompt paths used by runtime loader to existing files.
   Files to change:

- `prompts/`
- `tools/templates/prompts/`
  Risks:
- Missing prompt variants could break runtime prompt loading.
- Prompt/template drift can reintroduce inconsistent role behavior.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Create at least 2 fixtures per critical path (prompt-load success, missing prompt fail, reviewer approve, reviewer block/retry, reviewer conflict) with distinct prompt sets.
- Deterministic seed strategy: Use fixed seed(s) for any randomized fixture inputs or ordering to keep test outputs stable.
- Invariant checks: Assert prompt path resolution invariant (root + template parity) and invariant error messaging for missing prompts.
- Contract boundary coverage: Validate file-based prompt loading boundaries and explicit remediation text for missing task-specific prompts.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

2. Align prompt contracts and loader logic with current workflow, ensuring file-based loading and explicit failure guidance.
   Files to change:

- `tools/pc-feature/`
- `prompts/`
- `tools/templates/prompts/`
  Risks:
- Over-tightening reviewer wording could deadlock high-risk flows.
- Loader changes could break existing task-specific prompt selection.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Two fixtures for each prompt-loading path (base role and task-specific variant).
- Deterministic seed strategy: Fixed seeds for any generated prompt IDs or ordering.
- Invariant checks: Assert loader always uses `load_prompt_template()`/fallback, never embedded prompt bodies.
- Contract boundary coverage: Ensure missing prompt file throws actionable, user-facing remediation.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

3. Add/refresh plan-reviewer gate tests for approve, block/retry, and conflict paths.
   Files to change:

- `tests/test_pc_feature.py`
  Risks:
- Tests could encode outdated gate policy and force incorrect behavior.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Two fixtures per gate outcome with different risk states.
- Deterministic seed strategy: Fixed seeds for gate decision inputs.
- Invariant checks: Assert gate outcome matches risk policy inputs and allowed-tests constraints.
- Contract boundary coverage: Verify explicit failure guidance and next-step instructions on conflict.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

4. Sync process docs with prompt/gate semantics and finalize.
   Files to change:

- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
  Risks:
- Process docs could diverge from live behavior, causing execution drift.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A (docs change).
- Deterministic seed strategy: N/A.
- Invariant checks: Ensure docs reference canonical prompt paths and reviewer gate semantics.
- Contract boundary coverage: Ensure docs specify missing-prompt remediation and allowed-tests behavior.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

Work Item ID: WI-20260209-01

#### Patch

- (pending)

#### Test Results

- (pending)

#### Reporter Review

- (pending)

#### Gates

- make ci:

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
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=2/3).

#### Commit

- Commit message:

#### Final Report

-

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
