# Development Tasks: Unified autofix for CI + precommit

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Unified autofix for CI + precommit

Status: Done

**Last Updated:** 2026-02-07

## Tasks

- [x] Task 1: Design unified script interface
- [x] Task 2: Update make + hook wiring
- [x] Task 3: Document precommit behavior

## Execution Log

### WI-20260206-01 - Work item execution

- Date: 2026-02-06
- Scope / tasks covered:
- Planner: Codex
- Patcher:
- Tester:
- Reporter:
- Outcome: pass
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes: High-risk gate approved interactively.

#### Preflight Report

- Work Item: WI-20260206-01
- PRD ref: docs/01-product/prd.md
- Risk level: HIGH
- Triggers: change budget exceeded (file count), cross-cutting refactor impacting 3+ modules
- Scope in: Autofix script; precommit behavior; docs/process updates.
- Scope out: Changing lint/format rules.
- Non-goals reminder: No scope creep; local CLI only; stop at MVP and avoid unrelated refactors or background automation.
- Files to change: tools/pc-autofix, tools/pc-precommit, Makefile, docs/04-process/git-workflow.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/02-features/10-unified-autofix-precommit/dev-tasks.md
- Change budget: max_files=6, max_new_modules=1
- TDD plan: Hook integration test (pre-commit invokes unified script), Autofix script dry-run test
- Systematic review:

#### TDD Plan

- Tests to write first:
  - Hook integration test (pre-commit invokes unified script)
  - Autofix script dry-run test

#### Allowed Tests

- `python -m unittest discover -s tests -p "test_*.py"`

#### Files to Change + Change Budget

- Files: tools/pc-autofix, tools/pc-precommit, Makefile, docs/04-process/git-workflow.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/02-features/10-unified-autofix-precommit/dev-tasks.md
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- docs/03-logs/implementation-log.md
- docs/03-logs/validation-log.md
- docs/04-process/git-workflow.md
- docs/02-features/10-unified-autofix-precommit/dev-tasks.md

#### Plan

1. Preflight: Read `docs/README.md`, `docs/04-process/ticket-execution-protocol.md`, `docs/00-context/context-boundaries-operating-model.md`, and `docs/04-process/definition-of-done.md` to confirm scope, stop conditions, HIGH RISK criteria, and required execution order.
2. Preflight: Read `docs/02-features/10-unified-autofix-precommit/AGENTS.md` (if present) and any setup instructions to confirm prerequisites and feature-specific constraints.
3. Preflight: Locate the WI-20260206-01 spec using `rg "WI-20260206-01" docs/` via `pp`; if multiple matches, open each candidate and choose the one under `docs/02-features/10-unified-autofix-precommit/` or ask the user to disambiguate; if none, request the exact document and pause.
4. Preflight: Using `pp`, extract all anti-hardcode requirements (fixture coverage >=2 per critical path, deterministic seed strategy, invariant checks, contract boundary coverage) and translate them into concrete patch tasks.
5. Preflight: Determine HIGH RISK status per `docs/00-context/context-boundaries-operating-model.md`. If HIGH RISK and no approval, stop here and set status to “Awaiting PO Approval”.
6. Report (Planner): Summarize required patch tasks and constraints for handoff; explicitly note that `docs/03-logs/*.md` must be updated by the Patcher (Planner role scope does not permit editing those logs), or state why no log entry is needed.

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

- Plan Reviewer BLOCK; planner updated plan (block count: 1).
- Execution attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows regressions (removed WI tracking, deleted log entries, behavior change without tests, malformed validation log), so the plan must explicitly add remediation and validation steps.; patcher feedback task executed.
- Execution attempt 2: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter failure adds concrete regressions and missing artifacts that require explicit restore steps beyond the current plan wording.; patcher feedback task executed.
- Plan Reviewer BLOCK; planner updated plan (block count: 2).
- Plan Reviewer BLOCK; planner updated plan (block count: 3).
- Plan Reviewer BLOCK; planner updated plan (block count: 4).
- Execution attempt 3: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter found protocol/code/tests/logs misalignment and missing WI evidence, so the plan must include remediation steps beyond Preflight.; patcher feedback task executed.
- [2026-02-06T13:34:16Z] attempt=01 step=plan-reviewer status=APPROVE
- [2026-02-06T13:34:16Z] attempt=01 step=execution status=START | attempt_base=b043f849a140ee15e03a1c0abcb6435bddba0200
- [2026-02-06T13:35:52Z] attempt=01 step=prepatch-smoke status=PASS | python -m unittest discover -s tests -p 'test\_\*.py'
- [2026-02-06T13:37:48Z] attempt=01 step=patcher status=NOOP | changed=0 paths: (no-op)
- [2026-02-06T16:07:47Z] attempt=01 step=plan-reviewer status=CONFLICT | blocked on stop-after-preflight policy despite approved high-risk gate
- [2026-02-06T17:24:44Z] attempt=01 step=plan-reviewer status=APPROVE
- [2026-02-06T17:24:44Z] attempt=01 step=execution status=START | attempt_base=1e18a7141f74b226b1bc49f8254a6ddd3dc55069
- [2026-02-06T17:26:21Z] attempt=01 step=prepatch-smoke status=PASS | python -m unittest discover -s tests -p 'test\_\*.py'
- [2026-02-06T17:38:32Z] attempt=01 step=patcher status=NOOP | changed=0 paths: (no-op)
- [2026-02-06T17:40:10Z] attempt=01 step=tests status=PASS | python -m unittest discover -s tests -p 'test\_\*.py'
- [2026-02-06T17:41:13Z] attempt=01 step=reporter status=PASS
- [2026-02-06T17:41:16Z] attempt=01 step=ci status=FAIL-1
- Attempt 1: Plan Reviewer BLOCK; planner updated plan.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan.
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (block count: 1).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (block count: 2).
- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback identifies regressions and missing scope evidence that the current plan doesn’t explicitly remediate or validate.; patcher feedback task executed.
- Attempt 2: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows scope-impacting deletions and missing WI scope, plus tests discovered zero tests due to malformed pattern, so the current plan is insufficient.; patcher feedback task executed.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (block count: 3).
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (block count: 4).
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (block count: 5).
- Attempt 3: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows scope ambiguity plus regressions and log deletions that the current plan does not explicitly gate on restoring before proceeding.; patcher feedback task executed.
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (block count: 3).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (block count: 4).
- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows WI requirements and reviewer blockers were not addressed and test evidence is insufficient, so the plan must include re-preflight, fixing blockers, and valid test proof.; patcher feedback task executed.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (block count: 5).
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (block count: 6).
- Attempt 2: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback indicates no implementation progress and unresolved BLOCK, so the plan must explicitly address missing scope work and test discovery gap.; patcher feedback task executed.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (block count: 7).
- Attempt 1: planner no-op; reason=plan already present.
- Attempt 1: Plan Reviewer APPROVE; proceeding to patch.

#### Step Trace

- (pending)
- [2026-02-06T17:41:16Z] attempt=01 flow: plan-reviewer(APPROVE) -> execution(START) -> prepatch-smoke(PASS) -> patcher(NOOP) -> tests(PASS) -> reporter(PASS) -> ci(FAIL-1)

#### Commit

- Commit message: logs: record WI-20260206-01 execution and validation

#### Final Report

What changed (files): (see git diff)
Tests written (names) + results: (see feature validation-log.md)
Docs/logs updated checklist: (see Docs Updated)
make ci results: PASS
Commands run (use pp for noisy output): prepatch smoke python -m unittest discover -s tests -p 'test\_\*.py': ok; tools/offload-proxy/pp make ci: ok
Commit message: logs: record WI-20260206-01 execution and validation

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-10-001` Unscoped `git add -u` can stage unrelated tracked changes
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: In the unified autofix script, snapshot the pre-hook staged path set (`git diff --cached --name-only -z`), restage only that set (or its autofix-touched subset), and hard-fail if autofix changed tracked files outside scope.
- [ ] `SEC-10-002` Vanilla Codex mode is required but not fail-closed
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Hard-pin vanilla config/env in `tools/pc-precommit` and fail immediately if vanilla mode cannot be applied; add a regression check that rejects Serena-enabled execution.
- [ ] `SEC-10-003` Autofix failure path is not explicitly commit-blocking
  - Reviewer: Security Expert
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Propagate non-zero exit codes from unified autofix through precommit and CI, and add a negative-path automated test that injects autofix failure and asserts commit/CI is blocked.
- [ ] `SEC-10-004` Filename/path parsing safety is unspecified
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: No
  - Action: Use NUL-delimited git output (`-z`) and strict quoted/array-safe shell handling, plus a regression test with problematic filenames.
- [ ] `PROD-10-001` Restaging scope can include unrelated user work
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Snapshot the pre-hook staged set (`git diff --cached --name-only -z`), restage only that set (or its autofix-touched subset), and fail if out-of-scope tracked files changed.
- [ ] `PROD-10-002` Vanilla precommit mode is not fail-closed
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Hard-pin vanilla Codex config/env in precommit and exit non-zero if vanilla mode cannot be enforced; add a regression check that rejects Serena-enabled execution.
- [ ] `PROD-10-003` Autofix failure path may fail open
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Propagate non-zero exit codes end-to-end and add negative-path automated tests that inject autofix failure and assert commit/CI is blocked.
- [ ] `PROD-10-004` No-staged-files behavior is under-specified for users
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Define and test a deterministic no-staged-files outcome (clear message, no staging changes, correct exit code).
- [ ] `PROD-10-005` Filename parsing robustness is not guaranteed
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: No
  - Action: Use NUL-delimited git output and array-safe shell handling; add regression tests with problematic filenames.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-10-006` Human validation of CLI workflow clarity is missing
  - Reviewer: Product Manager
  - Severity: Low
  - Phase: human-validation
  - Action: Run PO validation on success/failure/no-op scenarios and record explicit sign-off for message clarity and remediation guidance.

<!-- review-backlog:end -->
