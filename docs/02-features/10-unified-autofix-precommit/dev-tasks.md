# Development Tasks: Unified autofix for CI + precommit

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Unified autofix for CI + precommit

**Status:** Not Started

**Last Updated:** 2026-02-05

## Tasks

- Task 1: Design unified script interface
- Task 2: Update make + hook wiring
- Task 3: Document precommit behavior

## Execution Log

### WI-20260206-01 - Work item execution

- Date: 2026-02-06
- Scope / tasks covered:
- Planner: Codex
- Patcher:
- Tester:
- Reporter:
- Outcome: needs replan
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes: Awaiting PO Approval

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

1. Preflight: Use Serena to locate and read `docs/04-process/ticket-execution-protocol.md` and confirm HIGH RISK gate wording and required artifacts for WI-20260206-01.
2. Evidence scan: Using `pp`, inspect diffs and WI artifacts to confirm which logs/tests were removed or malformed and capture exact deltas.
3. Align plan: Update the plan to explicitly restore/align protocol, code, tests, and logs; include a step to fix the malformed test pattern and to re-run tests with the correct pattern.
4. Execution (post-approval): Follow Plan → Patch → Test → Report, ensuring required logs are written and `make feature F=<feature-id>` is run.

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

#### Commit

- Commit message:

#### Final Report

-

- No runs yet.

## Related Documents

- Feature Spec: [link to feature-spec.md]
- Tech Design: [link to tech-design.md]
- Test Plan: [link to test-plan.md]
- Planner Log: [link to planner-log.md]
- Reporter Log: [link to reporter-log.md]
- Validation Log: [link to validation-log.md]

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-05 | Initial task breakdown | Primary user |
