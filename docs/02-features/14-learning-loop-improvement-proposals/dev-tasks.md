# Development Tasks: Learning loop improvement proposals

> **LLM-executable tasks**

---

## Overview

**Feature:** Learning loop improvement proposals

**Status:** Not Started

**Last Updated:** 2026-02-08

## Task Breakdown

- [ ] **Task 1 - Define proposal trigger contract**
  - Identify exact fail/stall points in `tools/pc-feature` where proposal generation should run.
  - Define required metadata fields and fallback behavior when metadata is missing.
  - Output: documented trigger matrix.

- [ ] **Task 2 - Implement proposal writer**
  - Add deterministic markdown writer/update helper for `docs/possible-improvements.md`.
  - Ensure new entries follow the existing entry template exactly.
  - Output: reliable proposal append/update behavior.

- [ ] **Task 3 - Implement dedup and status defaults**
  - Normalize failure signatures to prevent duplicate entries.
  - Default status to `Proposed` and prevent automatic `Approved`/patch execution.
  - Output: deduped proposals with human-gated lifecycle.

- [ ] **Task 4 - Add tests and docs/log sync**
  - Add/refresh tests for fail/stall proposal generation, dedup, and success-path no-op.
  - Update process docs and `docs/03-logs` entries with implementation/validation evidence.
  - Output: tested behavior with traceable logs.

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
- Notes: Main head locked: e62ec2a98e85280dcd2ee0d89bfb4a22c31b68e9

#### Preflight Report

- Work Item: WI-20260209-01
- PRD ref: docs/01-product/prd.md#FR-011
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Fail/stall detection for work item runs with WI/agent/step/failure summary context', 'Proposal generation into docs/possible-improvements.md using existing template fields', 'Human-gated status defaults (Proposed only)', 'Signature-based deduplication/skip or merge with rationale', 'Process/feature doc wording alignment for post-run proposals']
- Scope out: ['Automatic patch application', 'Remote ticketing integrations', 'Proposal sources outside workflow runs']
- Non-goals reminder: No auto-apply of fixes; no external integrations; only workflow run outcomes (fail/stall) generate proposals.
- Files to change: tools/pc-feature, docs/possible-improvements.md, tests/test_learning_loop_proposals.py, docs/04-process/dev-workflow.md, docs/04-process/human-orchestration-workflow.md, docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md, docs/02-features/14-learning-loop-improvement-proposals/tech-design.md, docs/02-features/14-learning-loop-improvement-proposals/test-plan.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md
- TDD plan: tests/test_learning_loop_proposals.py::test_proposal_created_on_fail, tests/test_learning_loop_proposals.py::test_dedup_skips_duplicate, tests/test_learning_loop_proposals.py::test_no_proposal_on_success
- Systematic review:

#### TDD Plan

- Tests to write first:
  - tests/test_learning_loop_proposals.py::test_proposal_created_on_fail
  - tests/test_learning_loop_proposals.py::test_dedup_skips_duplicate
  - tests/test_learning_loop_proposals.py::test_no_proposal_on_success

#### Allowed Tests

- `pytest tests/test_pc_feature.py`
- `pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py`

#### Files to Change

- Files: tools/pc-feature, docs/possible-improvements.md, tests/test_learning_loop_proposals.py, docs/04-process/dev-workflow.md, docs/04-process/human-orchestration-workflow.md, docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md, docs/02-features/14-learning-loop-improvement-proposals/tech-design.md, docs/02-features/14-learning-loop-improvement-proposals/test-plan.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md

#### Docs Updated

- docs/04-process/dev-workflow.md
- docs/04-process/human-orchestration-workflow.md
- docs/possible-improvements.md
- docs/03-logs/implementation-log.md
- docs/03-logs/validation-log.md
- docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md
- docs/02-features/14-learning-loop-improvement-proposals/tech-design.md
- docs/02-features/14-learning-loop-improvement-proposals/test-plan.md

#### Plan

Plan Contract v1
Approach:

1. Add post-run proposal generation for fail/stall outcomes by wiring a hook that builds a proposal from outcome payloads and invokes the proposal updater.
   Files to change:

- lib/pc_runner.py
  Risks:
- Hook may run in unintended contexts and create duplicate proposals if outcome filtering is wrong.
- Missing or partial outcome fields could cause malformed proposal entries.

2. Fix proposal merge to aggregate distinct agent names per signature while preserving `Proposed` status and existing fields.
   Files to change:

- lib/pc_runner.py
  Risks:
- Agent aggregation could over-merge if signatures are too broad.
- Backward compatibility with existing proposal entries could be broken.

3. Extend tests to cover new hook invocation, multi-agent aggregation for same signature, and no-op on success.
   Files to change:

- tests/test_pc_feature.py
  Risks:
- Tests may not cover missing-context boundaries introduced by hook integration.

Tests (anti-hardcode coverage required):

- Fixture coverage: At least 2 fixtures per critical path (fail/stall with full context; fail/stall with missing context) plus success-path fixture; ensure dedup path has at least 2 variants.
- Deterministic seed strategy: Use fixed seed for any randomized normalization or ID generation in tests (e.g., `random.seed(0)` or deterministic time/ID stubs).
- Invariant checks: Verify status remains `Proposed`, no proposals on success, and dedup never creates duplicate entries for same signature while aggregating agents.
- Contract boundary coverage: Validate inputs from post-run outcome payloads into the proposal writer (missing fields, multiple agents) and ensure writer outputs valid template fields.
- Allowed test commands:
  - `pytest tests/test_pc_feature.py`

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

- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=1/3).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_attempt=1/3).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=3/12, planner_revision=3/12, execution_attempt=1/3).
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=4/12, planner_revision=4/12, execution_attempt=1/3).
- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter found missing integration hook and incorrect multi-agent merge behavior, so implementation steps and tests must be updated.; patcher feedback pending.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=5/12, planner_revision=5/12, execution_attempt=2/3).
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=6/12, planner_revision=6/12, execution_attempt=2/3).
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=7/12, planner_revision=7/12, execution_attempt=2/3).

#### Commit

- Commit message:

#### Final Report

-

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md`
- Tech Design: `docs/02-features/14-learning-loop-improvement-proposals/tech-design.md`
- Test Plan: `docs/02-features/14-learning-loop-improvement-proposals/test-plan.md`
- Planner Log: `docs/02-features/14-learning-loop-improvement-proposals/planner-log.md`
- Reporter Log: `docs/02-features/14-learning-loop-improvement-proposals/reporter-log.md`
- Validation Log: `docs/02-features/14-learning-loop-improvement-proposals/validation-log.md`

## Change Log

| Date       | Changes                                                                  | Author       |
| ---------- | ------------------------------------------------------------------------ | ------------ |
| 2026-02-09 | Aligned workflow baseline to remove change-budget fields/section wording | Codex        |
| 2026-02-08 | Rebased tasks to explicit fail/stall learning loop                       | Codex        |
| 2026-02-05 | Initial task breakdown                                                   | Primary user |
