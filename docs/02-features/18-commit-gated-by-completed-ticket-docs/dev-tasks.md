# Development Tasks: Commit gated by completed ticket docs

> **LLM-executable tasks**

---

## Overview

**Feature:** Commit gated by completed ticket docs

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

### WI-20260212-01 - Work item execution

- Date: 2026-02-12
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
- Notes: Main head locked: 739817736d198be9d4605ba1b248f141dd2af200

#### Preflight Report

- Work Item: WI-20260212-01
- PRD ref: docs/01-product/prd.md (Feature F-18)
- Risk level: LOW
- Triggers: (none)
- Scope in: Commit precheck for execution-doc completeness at commit gate; deterministic missing-section diagnostics; logging of gate pass/fail decisions.
- Scope out: No new git workflow beyond existing tools/pc-commit contract; no auto-authoring of narrative tester/reporter evidence; no remote/git host integration changes.
- Non-goals reminder: Do not change commit message style policy or workflow model; do not fabricate human-authored report/test evidence.
- Files to change: tools/pc-feature, tools/pc-commit, docs/04-process/ticket-execution-protocol.md, tests/test_pc_feature.py
- TDD plan: TC-18-001: Missing `Tests Run` blocks commit with remediation., TC-18-002: Missing final report fields block commit with remediation., TC-18-003: Complete docs allow commit flow to continue., TC-18-101: Duplicate section headings are interpreted deterministically., TC-18-102: Empty section body is treated as missing evidence., TC-18-201: Malformed markdown fails closed with path+section guidance., TC-18-301: Existing successful final-gate flow remains unchanged., python3 -m unittest tests.test_pc_feature.TestPcFeature, python3 -m unittest tests.test_docs_logs
- Systematic review:

#### TDD Plan

- Tests to write first:
  - TC-18-001: Missing `Tests Run` blocks commit with remediation.
  - TC-18-002: Missing final report fields block commit with remediation.
  - TC-18-003: Complete docs allow commit flow to continue.
  - TC-18-101: Duplicate section headings are interpreted deterministically.
  - TC-18-102: Empty section body is treated as missing evidence.
  - TC-18-201: Malformed markdown fails closed with path+section guidance.
  - TC-18-301: Existing successful final-gate flow remains unchanged.
  - python3 -m unittest tests.test_pc_feature.TestPcFeature
  - python3 -m unittest tests.test_docs_logs

#### Allowed Tests

- `pytest tests/test_pc_feature.py::TestPcFeature`
- `python -m unittest tests.test_pc_feature.TestPcFeature`

#### Files to Change

- Files: tools/pc-feature, tools/pc-commit, docs/04-process/ticket-execution-protocol.md, tests/test_pc_feature.py

#### Docs Updated

- docs/04-process/ticket-execution-protocol.md (if semantics change)
- docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md execution log fields for WI-20260212-01
- Non-compacted `docs/03-logs/*` updates are reporter/orchestrator-owned and out of planner/patcher scope for this work item.

#### Plan

Updated `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md` with:

- `#### Allowed Tests` populated with exact commands.
- `#### Plan` replaced with the requested **Plan Contract v1** structure.
- Explicit anti-hardcode coverage in every approach step:
  - fixture coverage (`>=2` fixtures per critical path),
  - deterministic seed strategy,
  - invariant checks,
  - contract boundary coverage.
- Explicit handoff note that non-compacted `docs/03-logs/*` is reporter/orchestrator-owned and patcher will not edit those files.
- Removed non-compacted `docs/03-logs/*` from planned patcher file-edit lists.

File changed:

- `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`

Systematic review (commands executed and results):

1. `search_for_pattern` for `#### Plan` placeholder
   Result: located pending plan section.
2. `search_for_pattern` for `#### Allowed Tests` / `## Allowed Tests`
   Result: identified where to populate exact allowed test commands.
3. `apply_patch` (first pass)
   Result: inserted WI block content, allowed tests, and full Plan Contract v1 section.
4. `git diff -- .../dev-tasks.md`
   Result: detected forbidden non-compacted `docs/03-logs/*` in planned file-edit fields.
5. `apply_patch` (second pass)
   Result: removed forbidden planned file-edit references and added explicit ownership handoff text.
6. `git diff -- .../dev-tasks.md | sed -n '1,220p'`
   Result: verified final content and constraints compliance.
7. `git add ... && git commit -m "docs(F-18): add planner contract for WI-20260212-01"`
   Result: failed due sandbox permission on git worktree lock creation:
   `Unable to create .../.git/worktrees/.../index.lock: Operation not permitted`

Commit status:

- Commit was attempted once at the end, but could not be completed due filesystem permission restrictions on the parent git worktree metadata.

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

- Attempt 1: allowed-tests validation failed; routed back to planner (tester_retry=1/3). Issues: missing targets: tests.test_pc_feature.TestPcFeature.
- Attempt 1: plan-reviewer no-op; reason=blocked by invalid allowed tests.
- Attempt 1: patcher no-op; reason=blocked by invalid allowed tests.
- Attempt 1: reporter no-op; reason=blocked by invalid allowed tests.

#### Commit

- Commit message:

#### Final Report

-

- No runs yet.

## Task Breakdown

- [ ] **Task 1 - Define mandatory commit-doc checklist (data model)**
  - Identify required sections and evidence fields from protocol/docs.
  - Define normalization for section presence detection.
  - **Acceptance:** Checklist documented and traceable to protocol references.

- [ ] **Task 2 - Implement completeness evaluator (pure logic)**
  - Parse execution docs and evaluate required-section coverage.
  - Return structured missing-field diagnostics.
  - **Acceptance:** Deterministic pass/fail output for complete/incomplete fixtures.

- [ ] **Task 3 - Handle edge cases and fail-closed policy**
  - Handle malformed markdown, duplicate sections, and conflicting states.
  - Prevent false pass when evidence is ambiguous.
  - **Acceptance:** Ambiguous inputs block commit with remediation guidance.

- [ ] **Task 4 - Integrate gate with commit flow**
  - Wire evaluator into final commit gate.
  - Ensure blocking behavior is explicit and logged.
  - **Acceptance:** Commit path denied on incomplete docs and allowed on complete docs.

- [ ] **Task 5 - Docs/log sync**
  - Update process docs if commit-gate semantics change.
  - Record implementation and validation outcomes in `docs/03-logs/*`.
  - **Acceptance:** Documentation and logs match final behavior.

## Allowed Tests (Planner must populate before Tester runs)

- `python3 -m unittest tests.test_pc_feature.TestPcFeature`
- `python3 -m unittest tests.test_docs_logs`

## Related Documents

- Feature Spec: `docs/02-features/18-commit-gated-by-completed-ticket-docs/feature-spec.md`
- Tech Design: `docs/02-features/18-commit-gated-by-completed-ticket-docs/tech-design.md`
- Test Plan: `docs/02-features/18-commit-gated-by-completed-ticket-docs/test-plan.md`
- Planner Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/planner-log.md`
- Plan Reviewer Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/plan-reviewer-log.md`
- Reporter Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/reporter-log.md`
- Validation Log: `docs/02-features/18-commit-gated-by-completed-ticket-docs/validation-log.md`

## Change Log

| Date       | Changes       | Author |
| ---------- | ------------- | ------ |
| 2026-02-11 | Initial tasks | Codex  |
