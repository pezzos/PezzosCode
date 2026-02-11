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

### WI-20260211-02 - Work item execution

- Date: 2026-02-11
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
- Notes: Main head locked: 22b4f76000fb5e584fd9418a512b1720b0127c01

#### Preflight Report

- Work Item: WI-20260211-02
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Deterministic resume-state detection from existing work-item artifacts and role logs', 'Resume policy resolution for modes `auto`, `prompt`, and `fresh`', 'Fail-closed handling for contradictory artifact state with explicit remediation', 'Step routing that skips only safe completed steps while always re-running tests and final CI gate', 'Traceable resume decisions/checkpoints logged in feature/work-item documentation']
- Scope out: ['Multi-feature concurrent resume orchestration', 'Background/daemon-based resume automation', 'Non-CLI surfaces (TUI/API/Web)']
- Non-goals reminder: Do not change the single-feature-worktree operating model, do not add scheduler/daemon behavior, and do not weaken mandatory rerun of tests and final CI on resume.
- Files to change: tools/pc-feature, tests/test_pc_feature.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md, docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
- TDD plan: TC-17-001 resume from completed planner+reviewer continues at patcher, TC-17-002 resume after tester fail routes back to planner, TC-17-003 resume after reporter pass proceeds to final gates, TC-17-101 contradictory step state blocks with remediation, TC-17-102 dirty worktree preserved in auto mode, TC-17-201 missing critical artifacts returns deterministic block/error, TC-17-301 non-resume execution path regression remains unchanged, python -m pytest tests/test_pc_feature.py::TestPcFeature, python3 -m unittest tests.test_docs_logs
- Systematic review:
  - `rg -n "WI-20260211-02|#### Allowed Tests|#### Plan" docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` -> located WI-20260211-02 placeholders requiring planner updates.
  - `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '1,220p'` -> inspected WI-20260211-02 execution block, confirmed placeholder plan and disallowed non-compacted log targets in docs update notes.
  - `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '40,170p'` -> verified Plan Contract v1 content, exact Allowed Tests commands, and ownership handoff note after patch.

#### TDD Plan

- Tests to write first:
  - TC-17-001 resume from completed planner+reviewer continues at patcher
  - TC-17-002 resume after tester fail routes back to planner
  - TC-17-003 resume after reporter pass proceeds to final gates
  - TC-17-101 contradictory step state blocks with remediation
  - TC-17-102 dirty worktree preserved in auto mode
  - TC-17-201 missing critical artifacts returns deterministic block/error
  - TC-17-301 non-resume execution path regression remains unchanged
  - python -m pytest tests/test_pc_feature.py::TestPcFeature
  - python3 -m unittest tests.test_docs_logs

#### Allowed Tests

- `python -m pytest tests/test_pc_feature.py::TestPcFeature`
- `python3 -m unittest tests.test_docs_logs`

#### Files to Change

- Files: tools/pc-feature, tests/test_pc_feature.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md, docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md

#### Docs Updated

- docs/02-features/17-resume-in-progress-tickets/dev-tasks.md: populate WI-20260211-02 preflight, TDD plan, file list, executed command review, and outcome sections
- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md: record implementation/test evidence and offload pointers for traceability
- Non-compacted `docs/03-logs/*` updates are reporter/orchestrator-owned and out of patcher scope for this work item.

#### Plan

Plan Contract v1
Approach:

1. Reproduce and isolate the `tests.test_docs_logs` failure path tied to WI-20260211-02 and identify the exact docs/log contract mismatch causing exit code 1.
   Files to change:

- tests/test_docs_logs.py
- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Fixing assertions too narrowly could hide a real logging contract regression.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Validate at least one passing and one failing docs/log layout fixture for compacted evidence expectations.
- Deterministic seed strategy: Use static file names/content and fixed temporary directory structure.
- Invariant checks: The same docs tree input must always produce the same pass/fail verdict.
- Contract boundary coverage: Verify boundaries between compacted evidence location rules and WI-scoped evidence content checks.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Patch resume-routing/guardrail implementation and/or test expectations so contradictory in-progress artifacts still fail closed while remaining compliant with docs/log validation rules.
   Files to change:

- tools/pc-feature
- tests/test_pc_feature.py
- tests/test_docs_logs.py
  Risks:
- Behavioral guardrail changes could unintentionally alter valid resume flows.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Keep complete, incomplete, contradictory, and non-resume fixtures with at least two fixtures for each critical path.
- Deterministic seed strategy: Use fixed artifacts and stable temp-path construction; no time/random-dependent logic.
- Invariant checks: Identical artifacts plus mode must always yield identical route and block/continue outcomes.
- Contract boundary coverage: Enforce the same consistency gate for inferred and explicit resume modes while preserving docs/log contract compliance.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Re-run all Allowed Tests, record compacted WI evidence with exact commands and outcomes, and keep patcher edits scoped away from non-compacted docs logs.
   Files to change:

- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Incomplete or inaccurate evidence can block reporter/orchestrator handoff.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for evidence update; reference executed fixtures from steps 1-2.
- Deterministic seed strategy: Record exact command lines and deterministic outcomes only.
- Invariant checks: Evidence must match executed commands/results verbatim.
- Contract boundary coverage: Limit patcher evidence updates to compacted WI output only.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator, and patcher will not edit non-compacted `docs/03-logs` files.

Work Item ID: WI-20260211-02

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

- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=1/3).
- Attempt 1: reporter no-op; reason=tester failed.
- Attempt 1: tester=FAIL, reporter=SKIPPED; planner decision=REVISE_PLAN; rationale=One required Allowed Tests command is failing (`python3 -m unittest tests.test_docs_logs`), so the plan must add explicit remediation to restore full green status before review.; patcher feedback pending.

#### Commit

- Commit message:

#### Final Report

-

### WI-20260211-01 - Work item execution

- Date: 2026-02-11
- Scope / tasks covered:
- Planner: Codex
- Plan Reviewer: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: needs replan
- Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`
- Offload ids (if any):
- Docs/logs updated: `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`, `docs/03-logs/compacted/WI-20260211-01-patcher-evidence.md`
- Notes: Main head locked: 889795e5c315dfe4a2b7f612f8b51108475e50e8

#### Preflight Report

- Work Item: WI-20260211-01
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Resume-state detection from existing work-item artifacts', 'Resume policy enforcement for modes: auto, prompt, fresh', 'Deterministic step routing with safe step-skipping', 'Always rerun tests and final CI gate on resumed runs', 'Resume decision/checkpoint logging in feature/work-item logs']
- Scope out: ['Multi-feature concurrent resume orchestration', 'Background/daemon resume automation']
- Non-goals reminder: Do not add new orchestration models, schedulers, or non-CLI surfaces; keep single-feature-worktree policy unchanged.
- Files to change: tools/pc-feature, tests/test_pc_feature.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md
- TDD plan: TC-17-001 resume from planner+reviewer continues at patcher, TC-17-002 resume after tester fail routes back to planner, TC-17-003 resume after reporter pass proceeds to final gates, TC-17-101 contradictory step state blocks with remediation, TC-17-102 dirty worktree preserved in auto mode, TC-17-201 missing critical artifacts deterministically blocks/errors, TC-17-301 non-resume path unchanged regression, python3 -m unittest tests.test_pc_feature.TestPcFeature, python3 -m unittest tests.test_docs_logs
- Systematic review:
  - `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '60,130p'` -> confirmed placeholders and disallowed planned log-file edits before patching.
  - `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '30,95p'` -> verified Plan Contract content, Allowed Tests, and scoped file-edit list after patching.

#### TDD Plan

- Tests to write first:
  - TC-17-001 resume from planner+reviewer continues at patcher
  - TC-17-002 resume after tester fail routes back to planner
  - TC-17-003 resume after reporter pass proceeds to final gates
  - TC-17-101 contradictory step state blocks with remediation
  - TC-17-102 dirty worktree preserved in auto mode
  - TC-17-201 missing critical artifacts deterministically blocks/errors
  - TC-17-301 non-resume path unchanged regression
  - python3 -m unittest tests.test_pc_feature.TestPcFeature
  - python3 -m unittest tests.test_docs_logs

#### Allowed Tests

- `python -m pytest tests/test_pc_feature.py::TestPcFeature`

#### Files to Change

- Files: tools/pc-feature, tests/test_pc_feature.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md

#### Docs Updated

- docs/02-features/17-resume-in-progress-tickets/dev-tasks.md (Preflight, TDD plan, Files to Change, Systematic review)

#### Plan

Plan Contract v1
Approach:

1. Add/adjust tests that fail when tester/reporter artifacts exist but execution-entry completion signals are still pending, while preserving existing resume-routing expectations.
   Files to change:

- tests/test_pc_feature.py
  Risks:
- Tests may accidentally encode file-format specifics too tightly and become brittle to harmless wording changes.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Include fixtures for complete execution entries, pending execution entries with tester/reporter artifacts present, and clean non-resume runs.
- Deterministic seed strategy: Use fixed fixture content and stable temp paths for repeatable outcomes.
- Invariant checks: Assert identical inputs always produce identical block/continue decisions.
- Contract boundary coverage: Validate boundaries between artifact discovery, execution-entry completeness checks, and mode policy handling.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

2. Implement execution-record consistency guardrails in orchestration logic so contradictory resume evidence is blocked with explicit reasons.
   Files to change:

- tools/pc-feature
  Risks:
- Over-strict validation could block legitimate recovery paths if edge cases are missed.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Reuse contradictory/complete fixture corpus from step 1 for implementation validation.
- Deterministic seed strategy: Keep checks purely input-derived with no time/order dependence.
- Invariant checks: Ensure guardrails never allow continuation when required completion signals are absent.
- Contract boundary coverage: Confirm explicit mode selections and inferred resume state both pass through the same consistency gate.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

3. Re-run targeted validation and capture compacted evidence only; hand off role-scoped and non-compacted documentation updates for final reporting pass.
   Files to change:

- docs/03-logs/compacted/
  Risks:
- Incomplete evidence handoff can still delay reporter approval even when code behavior is correct.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for documentation-only evidence step.
- Deterministic seed strategy: N/A for documentation-only evidence step.
- Invariant checks: Evidence must match executed command and resulting guard behavior.
- Contract boundary coverage: Document only this work item’s implemented scope and validation outcome.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator; patcher will not edit non-compacted `docs/03-logs` files. Role-scoped execution-record updates and reporter rerun handoff remain outside patcher file edits in this plan.

Work Item ID: WI-20260211-01

#### Patch

- Updated `tools/pc-feature` resume consistency routing to block contradictory states when tester/reporter role artifacts exist while execution sections remain pending.
- Added focused resume consistency tests in `tests/test_pc_feature.py`.
- Updated WI execution record and compacted evidence for traceability handoff.

#### Test Results

- `tools/offload-proxy/pp python -m pytest tests/test_pc_feature.py::TestPcFeature` -> PASS (`115 passed`, `0 failed`).

#### Reporter Review

- Outcome: FAIL (latest reporter run)
- Handoff: execution sections updated from pending to completed patch/test/review context; rerun reporter for approval.

#### Gates

- make ci:

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes: PASS. `python -m pytest tests/test_pc_feature.py::TestPcFeature` succeeded.

#### Reporter Feedback

- Notes: FAIL on prior run because Patch/Test Results/Reporter Review and run status remained pending despite tester/reporter artifacts. Execution record has been aligned for rerun.

#### Iteration Log

- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=1/3).
- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter failure shows a traceability gap not covered by the prior implementation-focused plan, so execution-record consistency must be enforced before approval.; patcher feedback pending.
- Attempt 2: patcher updated execution-record consistency guardrails + tests; targeted pytest PASS; reporter rerun pending.

#### Commit

- Commit message:

#### Final Report

- Work item patched and validated for the reporter-identified traceability gap; awaiting reporter rerun/approval.

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
