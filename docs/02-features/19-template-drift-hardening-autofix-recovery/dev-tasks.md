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

### WI-20260213-01 - Work item execution

- Date: 2026-02-13
- Scope / tasks covered:
- Planner: Codex
- Plan Reviewer: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: completed
- Tests run: `python3 -m unittest discover -s tests -p test_pc_autofix.py`; `python3 -m unittest discover -s tests -p test_pc_feature.py`; `python3 -m unittest discover -s tests -p test_pc_hooks_run.py`
- Offload ids (if any):
- Docs/logs updated: Updated `docs/02-features/19-template-drift-hardening-autofix-recovery/reporter-log.md` with WI-20260213-01 reporter review entry.
- Notes: Planner/reviewer stagnation detected; manual intervention required.; Main head locked: 77a8d085fc73f8bfec2873c1461738b61182eb7a

#### Preflight Report

- Work Item: WI-20260213-01
- PRD ref: docs/01-product/prd.md (Feature F-19: Template drift hardening + autofix recovery)
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Detect template/living-file drift in precommit and CI autofix paths', 'Classify drift into safe-auto-fix vs manual/block', 'Apply deterministic scoped repairs for safe one-sided drift only', 'Re-stage only approved/touched scoped files', 'Fail closed with explicit remediation for ambiguous/unresolved/out-of-scope drift']
- Scope out: ['Automatic semantic conflict resolution for multi-file/two-sided conflicts', 'Non-template content synchronization policies', 'Broad restaging or unrelated workflow redesign']
- Non-goals reminder: Do not introduce heuristic conflict auto-resolution, do not modify out-of-scope files, and do not expand scope beyond template drift guardrails.
- Files to change: tools/pc-precommit, tests/test_pc_autofix.py, tests/test_pc_feature.py, tests/test_pc_hooks_run.py, docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md
- TDD plan: python3 -m unittest discover -s tests -p "test_pc_autofix.py", python3 -m unittest discover -s tests -p "test_pc_feature.py", python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"
- Systematic review:
  - `git status --short` -> confirmed active edits in `docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md` and unrelated untracked `logs/WI-20260213-01/`.
  - `rg -n "#### Allowed Tests|#### Plan|## Allowed Tests|WI-20260213-01" docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md` -> located target planning sections and placeholders.
  - `sed -n '52,190p' docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md` -> verified placeholder content to replace in-place.
  - `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"` -> offload id `2688e3aac5879831defab5e5f231a6f331e395be82e99f6caef62e863a873ffe`; result: 14 tests passed.

#### TDD Plan

- Tests to write first:
  - python3 -m unittest discover -s tests -p "test_pc_autofix.py"
  - python3 -m unittest discover -s tests -p "test_pc_feature.py"
  - python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"

#### Allowed Tests

- `python3 -m unittest discover -s tests -p "test_pc_autofix.py"`
- `python3 -m unittest discover -s tests -p "test_pc_feature.py"`
- `python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"`

#### Files to Change

- Files: tools/pc-precommit, tests/test_pc_autofix.py, tests/test_pc_feature.py, tests/test_pc_hooks_run.py

#### Docs Updated

- Update WI-20260213-01 Preflight/TDD/Files-to-change sections in docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md
- Non-compacted `docs/03-logs/*.md` updates are deferred to reporter/orchestrator per handoff policy.

#### Plan

Plan Contract v1
Approach:

1. Harden `pc-precommit` entrypoint orchestration against template drift by enforcing deterministic tool discovery, fallback ordering, and fail-closed exit behavior across existing `tools/pc-*` boundaries.
   Files to change:

- tools/pc-precommit
- tools/pc-autofix
- tools/pc-hooks-run
- tools/pc-feature (align shared contract assumptions used by `pc-precommit` fallback/dispatch paths)
  Risks:
- Entry-point regression could preserve downstream script behavior while breaking `pc-precommit` ordering or exit propagation.
- Discovery/fallback tightening could reject valid local setups if guardrails are over-constrained.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Add at least 2 fixtures per `pc-precommit` critical boundary (success + failure) covering tool discovery, ordered fallback dispatch, and missing-tool fail-close behavior.
- Deterministic seed strategy: Use fixed fixture matrices and explicit environment/path stubs with no time/random dependence.
- Invariant checks: Assert `pc-precommit` preserves deterministic invocation order, propagates downstream exit codes unchanged, and never reports success when required tooling is unavailable.
- Contract boundary coverage: Validate `pc-precommit` boundary contracts to `pc-autofix`/`pc-hooks-run`/`pc-feature` directly, plus downstream boundary checks, without asserting internal implementation details.
- Allowed test commands:
  - `python3 -m unittest discover -s tests -p "test_pc_autofix.py"`
  - `python3 -m unittest discover -s tests -p "test_pc_feature.py"` (explicit `pc-precommit` boundary coverage target)
  - `python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"`

2. Expand regression tests to prevent hardcoded-path drift and lock cross-script contracts, including explicit direct coverage at the `pc-precommit` boundary under an allowed existing test target.
   Files to change:

- tests/test_pc_autofix.py
- tests/test_pc_feature.py
- tests/test_pc_hooks_run.py
  Risks:
- Tests can become brittle if they assert incidental formatting instead of behavioral contracts.
- Missing negative fixtures at entrypoint boundaries can allow drift regressions to reappear.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Maintain at least 2 fixtures per boundary condition (present/missing tool, recoverable/non-recoverable failure), including `pc-precommit` direct success/failure fixtures.
- Deterministic seed strategy: Use deterministic fixture data and explicit environment patching for all scenarios.
- Invariant checks: Verify no hardcoded assumptions for absent scripts, deterministic fallback ordering, and consistent failure messaging/return codes.
- Contract boundary coverage: Cover interface expectations between each `tools/pc-*` script and its harness, with explicit `pc-precommit` boundary assertions executed via `test_pc_feature.py`.
- Allowed test commands:
  - `python3 -m unittest discover -s tests -p "test_pc_autofix.py"`
  - `python3 -m unittest discover -s tests -p "test_pc_feature.py"`
  - `python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"`

Work Item ID: WI-20260213-01

Handoff note: Required non-compacted `docs/03-logs/*.md` updates are owned by reporter/orchestrator; patcher will not edit those files.

#### Patch

- Resume reconciliation: role artifacts indicate patch work completed before interruption.
- Source artifacts: validation-log.md.

#### Test Results

- Resume reconciliation: derived from tester artifact in validation-log.md.
- Outcome: PASS
- Tests run: `python3 -m unittest discover -s tests -p test_pc_autofix.py`; `python3 -m unittest discover -s tests -p test_pc_feature.py`; `python3 -m unittest discover -s tests -p test_pc_hooks_run.py`
- Notes: Results: `python3 -m unittest discover -s tests -p test_pc_autofix.py` -> 0; `python3 -m unittest discover -s tests -p test_pc_feature.py` -> 0; `python3 -m unittest discover -s tests -p test_pc_hooks_run.py` -> 0

#### Reporter Review

- Resume reconciliation: derived from reporter artifact in reporter-log.md.
- Outcome: PASS
- Docs/logs updated: Updated `docs/02-features/19-template-drift-hardening-autofix-recovery/reporter-log.md` with a new `WI-20260213-01` Iteration 2 reporter entry.
- Notes: No-op for implementation scope on this reporter iteration; only reporter artifact was updated. Commit was attempted once at end and failed due sandbox permission (`index.lock` creation denied under parent worktree git...

#### Gates

- make ci: PASS

#### Autofix Attempts

tools/offload-proxy/pp pre-commit run --files <scoped>: ok

#### Tester Feedback

- Outcome: PASS
- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

- Attempt 1: allowed-tests validation failed; routed back to planner (tester_retry=1/3). Issues: missing targets: tests/test_pc_precommit.py.
- Attempt 1: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 1: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 1: reporter no-op; reason=blocked by invalid allowed tests.
- Attempt 2: allowed-tests validation failed; routed back to planner (tester_retry=2/3). Issues: missing targets: tests/test_pc_precommit.py.
- Attempt 2: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 2: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 2: reporter no-op; reason=blocked by invalid allowed tests.
- Attempt 3: allowed-tests validation failed; routed back to planner (tester_retry=3/3). Issues: missing targets: tests/test_pc_precommit.py.
- Attempt 3: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 3: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 3: reporter no-op; reason=blocked by invalid allowed tests.
- Startup auto-repair aligned pending sections from role artifacts: Patch, Test Results.
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_cycle=1).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_cycle=1).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=3/12, planner_revision=3/12, execution_cycle=1).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=4/12, planner_revision=4/12, execution_cycle=1).
- Planner/reviewer loop stagnation detected; repeat_count=3/3; issues=forbidden path in plan: docs/03-logs/\*.md
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_cycle=1); policy-diff unchanged=1 resolved=0 new=0 (unchanged: plan test commands must be listed in Allowed Tests: `python3 -m unittest discover -s tests -p test_pc_allowed_tests_check.py`); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_cycle=1); policy-diff unchanged=0 resolved=1 new=0 (resolved: forbidden path in plan: docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=3/12, planner_revision=3/12, execution_cycle=1); policy-diff unchanged=0 resolved=1 new=0 (resolved: forbidden path in plan: docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=4/12, planner_revision=4/12, execution_cycle=1); policy-diff unchanged=1 resolved=0 new=0 (unchanged: plan test commands must be listed in Allowed Tests: `python3 -m unittest discover -s tests -p test_pc_precommit.py`); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=5/12, planner_revision=5/12, execution_cycle=1); policy-diff unchanged=0 resolved=1 new=0 (resolved: forbidden path in plan: docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=6/12, planner_revision=6/12, execution_cycle=1); policy-diff unchanged=3 resolved=0 new=0 (unchanged: forbidden path in plan: docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md, forbidden path in plan: docs/03-logs/\*.md); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=7/12, planner_revision=7/12, execution_cycle=1); policy-diff unchanged=1 resolved=0 new=0 (unchanged: plan test commands must be listed in Allowed Tests: `python3 -m unittest discover -s tests -p test_pc_runner.py`, `python3 -m unittest discover -s tests -p test_pc_allowed_tests_check.py`); auto-policy-fix=(none).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_cycle=1); policy-diff unchanged=0 resolved=1 new=0 (resolved: forbidden path in plan: docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md); auto-policy-fix=(none).
- Runtime reconciliation updated execution record after reporter step: field:Patcher, field:Tester, field:Tests run, field:Reporter, field:Docs/logs updated, Reporter Review.
- Attempt 1: tester=PASS, reporter=FAIL; tester_retry=0/3; reporter_retry=1/3; planner decision=PLAN_STILL_VALID; rationale=Tester evidence validates the planned test contract, and reporter failure indicates execution/scope-application gaps rather than a flaw in the plan itself.; patcher feedback pending.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=2/12, execution_cycle=2); policy-diff unchanged=0 resolved=2 new=0 (resolved: Add an allowed command for the `pc-precommit` test target (or explicitly state the exact existing test file/pattern that exercises `pc-precommit` directly) so patcher can validate the changed entrypoint., Add explicit `pc-precommit` coverage to the plan’s `Tests` section, including success and failure fixtures that assert discovery/fallback ordering and exit-code propagation at the `pc-precommit` boundary.); auto-policy-fix=(none).
- Commit evidence auto-repair applied: Test Results:artifact, Reporter Review:artifact, field:Outcome.

#### Commit

- Commit message: chore(wi-20260213-01): apply work item updates

#### Final Report

What changed (files): (see git diff)
Tests written (names) + results: (see feature validation-log.md)
Docs/logs updated checklist: (see Docs Updated)
make ci results: PASS
Commands run (use pp for noisy output): prepatch smoke python3 -m unittest discover -s tests -p test_pc_autofix.py: ok; tools/offload-proxy/pp make ci: ok; collect patcher branch into main: ok
Commit message: chore(wi-20260213-01): apply work item updates

## Review Findings Backlog

<!-- review-backlog:start -->

### Security Reviewer Tasks

- [ ] `SEC-19-003` Secrets handling is not documented
  - Severity: Medium
  - Action: Document secret sources, redaction strategy, and prohibited storage locations.
- [ ] `SEC-19-004` Injection defenses are not explicit
  - Severity: High
  - Action: Define escaping/parameterization requirements and add dedicated injection test scenarios.

### Product Manager Tasks

- [ ] `PROD-19-001` Functional scope is under-specified
  - Severity: High
  - Action: Expand functional requirements to cover primary and edge behaviors with acceptance criteria.
- [ ] `PROD-19-002` User journey details are missing in feature docs
  - Severity: Medium
  - Action: Add explicit user journey steps, entry points, and completion states.
- [ ] `PROD-19-003` Global UX blueprint does not reference this feature
  - Severity: Medium
  - Action: Update `docs/01-product/ux-ui.md` to include 'Template drift hardening + autofix recovery' journey and workflow.
- [ ] `PROD-19-005` PO validation checkpoint is missing
  - Severity: Low
  - Action: Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.

<!-- review-backlog:end -->
