# Development Tasks: Synthetic feature workflow smoke test

> **LLM-executable tasks**

---

## Overview

**Feature:** Synthetic feature workflow smoke test

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
- Tests run: `python3 -m unittest tests.test_pc_feature`; `python3 -m unittest tests.test_orchestrator_workflow_docs`
- Offload ids (if any):
- Docs/logs updated: `docs/02-features/20-synthetic-feature-workflow-smoke-test/reporter-log.md` (entry added for `WI-20260213-01`)
- Notes: Main head locked: 6bf1645f7c730b6ea2784fe27437df017270fa73

#### Preflight Report

- Work Item: WI-20260213-01
- PRD ref: docs/01-product/prd.md (Feature F-20: Synthetic feature workflow smoke test)
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Define deterministic synthetic fixture and scenario metadata for workflow smoke path.', 'Implement invariant evaluator for role routing, Allowed Tests enforcement, resume behavior, and structured log presence.', 'Integrate smoke-run entry path into existing workflow engine without external dependencies.', 'Add deterministic pass/fail summary with evidence pointers.', 'Add/extend tests for baseline pass, injected gate failure, and resume-path behavior.', 'Update feature/process logs for traceability.']
- Scope out: ['Product/business feature behavior validation beyond workflow mechanics.', 'Load/performance benchmarking or long-running stress scenarios.', 'Changes to real feature execution semantics unrelated to smoke assertions.', 'Any invocation of make feature/pc-feature by Codex without explicit PO approval.']
- Non-goals reminder: Keep fixture lightweight, isolated, deterministic, and idempotent; avoid broad refactors or production-state coupling.
- Files to change: docs/02-features/20-synthetic-feature-workflow-smoke-test/test-plan.md, docs/04-process/ticket-execution-protocol.md, tests/test_orchestrator_workflow_docs.py, tests/test_pc_feature.py, tools/pc-feature
- TDD plan: python3 -m unittest tests.test_pc_feature, python3 -m unittest tests.test_orchestrator_workflow_docs
- Systematic review:

#### TDD Plan

- Tests to write first:
  - python3 -m unittest tests.test_pc_feature
  - python3 -m unittest tests.test_orchestrator_workflow_docs

#### Allowed Tests

- `python3 -m unittest tests.test_pc_feature`
- `python3 -m unittest tests.test_orchestrator_workflow_docs`

#### Files to Change

- Files: docs/02-features/20-synthetic-feature-workflow-smoke-test/test-plan.md, docs/04-process/ticket-execution-protocol.md, tests/test_orchestrator_workflow_docs.py, tests/test_pc_feature.py, tools/pc-feature

#### Docs Updated

- docs/02-features/20-synthetic-feature-workflow-smoke-test/dev-tasks.md (Preflight, TDD Plan, Files to Change, Test Results, Final Report)
- docs/03-logs/implementation-log.md (implementation decisions and changes)
- docs/03-logs/validation-log.md (executed tests and outcomes)
- docs/03-logs/decision-log.md (only if new architectural/process decision is made)
- docs/03-logs/bug-log.md (only if defects are discovered during execution)
- Handoff-only docs/log updates (reporter/orchestrator-owned; patcher will not edit these files): docs/02-features/20-synthetic-feature-workflow-smoke-test/dev-tasks.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md

#### Plan

- Plan Contract v1
- Approach:
  1. Implement deterministic synthetic smoke-path fixture handling, invariant evaluation (role routing, Allowed Tests policy, resume behavior, structured log presence), and concise pass/fail evidence reporting aligned to workflow protocol constraints.
     Files to change:
  - `tools/pc-feature`
  - `tests/test_pc_feature.py`
  - `tests/test_orchestrator_workflow_docs.py`
  - `docs/04-process/ticket-execution-protocol.md`
  - `docs/02-features/20-synthetic-feature-workflow-smoke-test/test-plan.md`
    Risks:
  - Invariant assertions may overfit transient log formatting and create false failures.
  - Resume-path checks may become flaky if fixture state isolation is incomplete.
  - Allowed Tests enforcement may drift if parser/normalization logic is inconsistent between docs and runner checks.
    Tests (anti-hardcode coverage required):
  - Fixture coverage: Add and validate at least 2 fixtures per critical path (baseline pass path and gate/resume failure path) with distinct evidence pointers.
  - Deterministic seed strategy: Use a fixed scenario-id/seed mapping for fixture generation and expected outputs so repeated runs are byte-stable.
  - Invariant checks: Assert role routing sequence, Allowed Tests command whitelist matching, resume-stage routing, and required structured log artifact presence.
  - Contract boundary coverage: Validate accepted/rejected command boundaries and missing/invalid artifact boundaries at evaluator inputs and workflow adapter outputs.
  - Allowed test commands:
    - `python3 -m unittest tests.test_pc_feature`
    - `python3 -m unittest tests.test_orchestrator_workflow_docs`
  - Handoff note: Any required non-compacted `docs/03-logs/*.md` updates are reporter/orchestrator-owned; patcher will not edit those files.

#### Patch

- Runtime reconciliation: patch step completed in this execution loop.
- Source artifacts: patcher role commit and scoped diff.

#### Test Results

- Runtime reconciliation: derived from tester feedback in this execution loop.
- Outcome: PASS
- Tests run: `python3 -m unittest tests.test_pc_feature`; `python3 -m unittest tests.test_orchestrator_workflow_docs`
- Notes: Results: `python3 -m unittest tests.test_pc_feature` -> 0; `python3 -m unittest tests.test_orchestrator_workflow_docs` -> 0

#### Reporter Review

- Runtime reconciliation: derived from reporter feedback in this execution loop.
- Outcome: PASS
- Docs/logs updated: `docs/02-features/20-synthetic-feature-workflow-smoke-test/reporter-log.md` (entry added for `WI-20260213-01`)
- Notes: Systematic review commands executed: `git status --short`, `git diff --stat refs/heads/main..HEAD`, `git diff --stat HEAD~1..HEAD`, per-file `git diff` on all changed files, and artifact checks via `find`/`sed` under...

#### Gates

- make ci: PASS

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

- Runtime reconciliation updated execution record after reporter step: Patch, field:Patcher, Test Results, field:Tester, field:Tests run, field:Reporter, field:Docs/logs updated, Reporter Review.
- Commit evidence auto-repair applied: field:Outcome.

#### Commit

- Commit message: chore(wi-20260213-01): complete work item updates

#### Final Report

What changed (files): (see git diff)
Tests written (names) + results: (see feature validation-log.md)
Docs/logs updated checklist: (see Docs Updated)
make ci results: PASS
Commands run (use pp for noisy output): prepatch smoke python3 -m unittest tests.test_pc_feature: ok; tools/offload-proxy/pp make ci: ok; collect patcher branch into main: ok
Commit message: chore(wi-20260213-01): complete work item updates
