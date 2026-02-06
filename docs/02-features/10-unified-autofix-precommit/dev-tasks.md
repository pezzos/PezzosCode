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
- Planner:
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

- (list exact commands; do not include `make feature` or `pc-feature`)

#### Files to Change + Change Budget

- Files: tools/pc-autofix, tools/pc-precommit, Makefile, docs/04-process/git-workflow.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/02-features/10-unified-autofix-precommit/dev-tasks.md
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- docs/03-logs/implementation-log.md
- docs/03-logs/validation-log.md
- docs/04-process/git-workflow.md
- docs/02-features/10-unified-autofix-precommit/dev-tasks.md

#### Plan

- (pending)

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

-

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
