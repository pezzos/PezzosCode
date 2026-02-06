# Development Tasks: Runner library + structured logs

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Runner library + structured logs

**Status:** In Progress

**Last Updated:** 2026-02-05

## Tasks

- Task 1: Define runner API and metadata contract
- Task 2: Implement logging helper and log path conventions
- Task 3: Update docs and templates to require runner usage

## Execution Log

### WI-20260205-01 - Work item execution

- Date: 2026-02-05
- Scope / tasks covered: Runner library + structured logs (runner API + metadata, log helper, tool entrypoints).
- Planner: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: pass
- Tests run: python -m unittest discover -s tests -p "test\_\*.py"
- Offload ids (if any): (none)
- Docs/logs updated: docs/02-features/09-runner-structured-logs/dev-tasks.md, docs/02-features/09-runner-structured-logs/validation-log.md, docs/02-features/09-runner-structured-logs/reporter-log.md, docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/03-logs/validation-log.md
- Notes: Execution log added to record WI; validation log invalidated due to tests outside Allowed Tests. Re-ran Allowed Tests after patch (61 tests passed).

#### Preflight Report

- Work Item: WI-20260205-01
- PRD ref: F-09 Runner library + structured logs
- Risk level: LOW (no triggers)
- Triggers: (none)
- Scope in: runner library, structured logs, tool entrypoints
- Scope out: cloud logging, daemonized logging
- Non-goals reminder: no new execution surfaces beyond `make feature`
- Files to change: lib/pc_runner.py, tools/pc-feature, tools/pc-precommit, tools/pc-autofix, tests/test_pc_runner.py
- Change budget: max_files=6, max_new_modules=1
- TDD plan: tests for log prefix + path creation
- Systematic review: pending (log reconciliation)

#### TDD Plan

- Tests to write first: tests/test_pc_runner.py::test_log_prefix_formatting, tests/test_pc_runner.py::test_log_path_creation

#### Allowed Tests

- python -m unittest discover -s tests -p "test\_\*.py"
- make test
- make ci

#### Files to Change + Change Budget

- Files: lib/pc_runner.py, tools/pc-feature, tools/pc-precommit, tools/pc-autofix, tests/test_pc_runner.py
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- [x] Implementation log
- [x] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)
- [x] Feature docs
- [ ] PRD (if needed)

#### Plan

- Define runner API + metadata contract.
- Implement structured log helper and log path conventions.
- Update tool entrypoints to use runner and pass metadata.
- Add tests for log prefix + path creation.
- Update docs and logs per protocol.

#### Patch

- (pending)

#### Test Results

- Outcome: PASS
- Tests run: python -m unittest discover -s tests -p "test\_\*.py"
- Notes: 61 tests passed.

#### Reporter Review

- Outcome: PASS
- Docs/logs updated: dev-tasks.md, validation-log.md, reporter-log.md, implementation-log.md, decision-log.md, validation-log.md (global)
- Notes: Log hygiene fixed; per-feature WI sequencing implemented; tests rerun per Allowed Tests.

#### Gates

- make ci: (not run)

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes: Allowed Tests ran; 61 tests passed.

#### Reporter Feedback

- Notes: (pending)

#### Iteration Log

-

#### Commit

- Commit message:

#### Final Report

- (pending)

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
