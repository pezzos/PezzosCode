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

### WI-20260212-03 - Work item execution

- Date: 2026-02-12
- Scope / tasks covered:
- Planner: Codex
- Plan Reviewer: Codex
- Patcher:
- Tester:
- Reporter:
- Outcome:
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes: Main head locked: 68e8d4a402c2b8fa117e6d5b5a03366298d6d683

#### Preflight Report

- Work Item: WI-20260212-03
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Deterministic resume-state detection from existing work-item artifacts and role logs', 'Resume policy enforcement for `auto`, `prompt`, and `fresh`', 'Fail-closed blocking on contradictory artifact state with explicit remediation', 'Artifact-aware step routing that skips only safe completed steps', 'Mandatory re-run of tests and final CI gate on resumed runs', 'Traceable resume/checkpoint decisions in workflow logs']
- Scope out: ['Multi-feature concurrent resume orchestration', 'Background/daemon resume automation', 'Non-CLI surfaces (TUI/API/Web)']
- Non-goals reminder: Do not change the single-feature-worktree operating model, do not add schedulers/daemons, and do not weaken mandatory test + final CI reruns on resume.
- Files to change: tools/pc-feature, tests/test_pc_feature.py, tests/test_docs_logs.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md, docs/03-logs/compacted/WI-20260212-03-patcher-evidence.md
- TDD plan: TC-17-001 resume from completed planner+reviewer continues at patcher, TC-17-002 resume after tester fail routes back to planner, TC-17-003 resume after reporter pass proceeds to final gates, TC-17-101 contradictory step state blocks with remediation, TC-17-102 dirty worktree preserved in auto mode, TC-17-201 missing critical artifacts deterministically blocks/errors, TC-17-301 non-resume execution path unchanged (regression), python -m pytest tests/test_pc_feature.py::TestPcFeature, python3 -m unittest tests.test_docs_logs
- Systematic review:
  - `tools/offload-proxy/pp rg -n "WI-20260212-03|#### Allowed Tests|#### Plan" docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` -> confirmed WI-20260212-03 planner placeholders and captured offload id `d5903b56ab2c0981e9afba33bcafd4a85313711ee05d29d54a11acb944ab8311`.
  - `mcp__serena__search_for_pattern` on `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` with pattern `### WI-20260212-03 - Work item execution[\\s\\S]*?### WI-20260211-02 - Work item execution` -> extracted only the target WI block for focused planner-only edits.

#### TDD Plan

- Tests to write first:
  - TC-17-001 resume from completed planner+reviewer continues at patcher
  - TC-17-002 resume after tester fail routes back to planner
  - TC-17-003 resume after reporter pass proceeds to final gates
  - TC-17-101 contradictory step state blocks with remediation
  - TC-17-102 dirty worktree preserved in auto mode
  - TC-17-201 missing critical artifacts deterministically blocks/errors
  - TC-17-301 non-resume execution path unchanged (regression)
  - python -m pytest tests/test_pc_feature.py::TestPcFeature
  - python3 -m unittest tests.test_docs_logs

#### Allowed Tests

- `python -m pytest tests/test_pc_feature.py::TestPcFeature`
- `python3 -m unittest tests.test_docs_logs`

#### Files to Change

- Files: tools/pc-feature, tests/test_pc_feature.py, tests/test_docs_logs.py, docs/02-features/17-resume-in-progress-tickets/dev-tasks.md, docs/03-logs/compacted/WI-20260212-03-patcher-evidence.md

#### Docs Updated

- docs/02-features/17-resume-in-progress-tickets/dev-tasks.md (WI-20260212-03 preflight, TDD plan, files, systematic review, outcomes)
- docs/03-logs/compacted/WI-20260212-03-patcher-evidence.md (implementation and validation evidence)
- Non-compacted `docs/03-logs/*` updates are reporter/orchestrator-owned and out of patcher scope for this work item.

#### Plan

Plan Contract v1
Approach:

1. Implement deterministic resume-state detection and safe step routing for single-feature execution, including fail-closed handling for contradictory artifact state and explicit remediation messaging.
   Files to change:

- `tools/pc-feature`
  Risks:
- Misclassifying partially complete runs could skip required work or re-run wrong roles.
- Contradictory artifacts may be silently tolerated unless fail-closed checks are enforced first.
  Tests (anti-hardcode coverage required):
- Fixture coverage: add scenarios for completed planner+reviewer, failed tester, completed reporter, contradictory role artifacts, and missing critical artifacts.
- Deterministic seed strategy: use fixed fixture directory structures and fixed identifiers/timestamps in test artifacts so resume classification is stable across runs.
- Invariant checks: enforce that `auto`, `prompt`, and `fresh` preserve policy guarantees, never bypass required gates, and never advance on contradictory state.
- Contract boundary coverage: validate resume decision boundaries at role transitions and error boundaries between recoverable and blocking states.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Add and update automated tests that lock behavior for resume policies, artifact-aware routing, fail-closed contradictions, regression on non-resume flows, and mandatory gate re-runs.
   Files to change:

- `tests/test_pc_feature.py`
- `tests/test_docs_logs.py`
  Risks:
- Tests may overfit current output text instead of behavior contracts.
- Missing edge fixtures can leave contradictory-state or missing-artifact branches unverified.
  Tests (anti-hardcode coverage required):
- Fixture coverage: include explicit artifacts for each role state and mixed/invalid combinations.
- Deterministic seed strategy: use stable fixture names and controlled environment inputs to avoid flaky ordering.
- Invariant checks: assert blocked-on-contradiction, no unsafe skip, and required final gates remain mandatory on resumed runs.
- Contract boundary coverage: assert CLI-visible outcomes at policy boundaries (`auto` vs `prompt` vs `fresh`) and artifact-presence boundaries.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Record compacted implementation/validation evidence for this work item and keep non-compacted project logs out of patcher scope.
   Files to change:

- `docs/03-logs/compacted/WI-20260212-03-patcher-evidence.md`
  Risks:
- Evidence can drift from implemented behavior if test outcomes and decisions are not summarized precisely.
  Tests (anti-hardcode coverage required):
- Fixture coverage: document which resume fixtures and contradiction fixtures were executed.
- Deterministic seed strategy: document fixed fixture/seeding choices used to keep outcomes reproducible.
- Invariant checks: document verified invariants (fail-closed contradiction, mandatory gate rerun, no unsafe step skip).
- Contract boundary coverage: document validated transition boundaries and blocking boundaries.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required note: non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator; patcher will not edit those files.

Work Item ID: WI-20260212-03

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

#### Commit

- Commit message:

#### Final Report

-

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

1. Reproduce and isolate the `tests.test_docs_logs` failure by running only the Allowed Test command, then identify the exact failing assertion and the contract rule it enforces.
   Files to change:

- `tests/test_docs_logs.py`
- `tools/pc-feature`
  Risks:
- Fixing only the symptom could leave the docs/log contract inconsistent with resume guardrails.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Add/verify at least one passing and one failing fixture for compacted WI evidence contract checks.
- Deterministic seed strategy: Use fixed fixture names/content and stable temp paths only; no clock/random input.
- Invariant checks: The same fixture inputs must always produce identical pass/fail outcomes.
- Contract boundary coverage: Validate path-placement rules independently from content-schema rules.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Patch contract enforcement so invalid or contradictory artifacts fail closed while valid compacted WI evidence passes, without regressing resume-routing behavior.
   Files to change:

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `tests/test_docs_logs.py`
  Risks:
- Guardrail changes may accidentally alter explicit vs inferred resume decisions.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Keep complete, incomplete, contradictory, and non-resume branches covered with at least two fixtures for each critical branch.
- Deterministic seed strategy: Keep all artifact inputs static and ordering deterministic.
- Invariant checks: Identical artifacts and mode must always yield the same route/block decision.
- Contract boundary coverage: Enforce parity between inferred and explicit resume consistency checks while preserving docs/log validation constraints.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Run all Allowed Tests until both exit 0, then update compacted WI evidence with exact executed commands and final results.
   Files to change:

- `docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md`
  Risks:
- Evidence can drift from actual execution if not updated from final command outputs only.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for evidence update; reference fixture coverage completed in steps 1-2.
- Deterministic seed strategy: Record exact command strings and deterministic exit codes only.
- Invariant checks: Evidence entries must exactly match executed commands/results.
- Contract boundary coverage: Limit patcher docs edits to compacted outputs only.
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
- Attempt 2: reporter no-op; reason=tester failed.
- Attempt 2: tester=FAIL, reporter=SKIPPED; planner decision=REVISE_PLAN; rationale=One allowed test command still exits non-zero, so the plan must tighten failure isolation and acceptance criteria to guarantee both allowed tests pass before handoff.; patcher feedback pending.
- Attempt 3: reporter no-op; reason=tester failed.
- Attempt 3: tester=FAIL, reporter=SKIPPED; planner decision=REVISE_PLAN; rationale=One required Allowed Test command (`python3 -m unittest tests.test_docs_logs`) still exits 1, so the current plan is not sufficient to reach a passing gate.; patcher feedback pending.

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
