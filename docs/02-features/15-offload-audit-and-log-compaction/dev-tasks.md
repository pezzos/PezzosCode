# Development Tasks: Offload audit + useful log compaction

> **LLM-executable tasks**

---

## Overview

**Feature:** Offload audit + log compaction

**Status:** Not Started

**Last Updated:** 2026-02-09

## Task Breakdown

- [ ] **Task 1 - Define and persist offload index schema**
  - Choose index format and location under `.offload/`.
  - Capture metadata fields: id, command, WI, agent, timestamp, size, path.
  - Output: deterministic index entries for every offloaded artifact.

- [ ] **Task 2 - Implement offload lifecycle commands**
  - Add list/get/purge utilities for indexed artifacts.
  - Include retention policy options (for example by age/count).
  - Output: predictable artifact retrieval and cleanup workflow.

- [ ] **Task 3 - Implement useful log compaction skills**
  - Add skills for compacting decision, implementation, and validation logs.
  - Enforce compact-output contract fields: source path, section/date reference, work item reference (if available), concise outcome/rationale, evidence reference(s).
  - Write derived compact artifacts to `docs/03-logs/compacted/` without modifying canonical logs.
  - Output: reusable compaction workflows with no source-log deletion and high learning value.

- [ ] **Task 4 - Add tests and docs/log sync**
  - Add tests for index integrity, list/get/purge behavior, compaction fidelity, and contract completeness.
  - Update process docs and `docs/03-logs` entries with implementation/validation evidence.
  - Output: verified behavior and traceable documentation updates.

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
- Notes: Loop exhausted; review Iteration Log for actionable remediation.; Main head locked: eabec517e15ba4a8b23eaf74f43bdbe19cc6d829

#### Preflight Report

- Work Item: WI-20260209-01
- PRD ref: docs/01-product/prd.md
- Risk level: LOW
- Triggers: (none)
- Scope in: ['Offload metadata index under .offload with required fields', 'List/get/purge lifecycle utilities with retention options', 'Compaction skills for decision/implementation/validation logs', 'Compact-output usefulness contract fields', 'Derived compact outputs in docs/03-logs/compacted/', 'Traceability updates in docs/03-logs and process docs', 'Tests for index/retention/compaction invariants']
- Scope out: ['Remote artifact storage', 'Destructive rewriting of canonical docs/03-logs/*.md', 'New UI for offload browsing']
- Non-goals reminder: Do not mutate or delete canonical logs; no remote storage or new UI.
- Files to change: tools/offload-proxy/pp, pp.yml, .offload/index.jsonl, tools/offload-proxy/_, docs/04-process/output-offload.md, docs/03-logs/decision-log.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/03-logs/compacted/decision-log-compact.md, docs/03-logs/compacted/implementation-log-compact.md, docs/03-logs/compacted/validation-log-compact.md, .codex/skills/_, tests/test_offload_index.py, tests/test_offload_retention.py, tests/test_log_compaction.py, docs/02-features/15-offload-audit-and-log-compaction/\*, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md
- TDD plan: python -m unittest discover -s tests -p "test\_\*.py"
- Systematic review:

#### TDD Plan

- Tests to write first:
  - python -m unittest discover -s tests -p "test\_\*.py"

#### Allowed Tests

- `python -m unittest discover -s tests -p 'test_*.py'`

#### Files to Change

- Files: tools/offload-proxy/pp, pp.yml, .offload/index.jsonl, tools/offload-proxy/_, docs/04-process/output-offload.md, docs/03-logs/decision-log.md, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/03-logs/compacted/decision-log-compact.md, docs/03-logs/compacted/implementation-log-compact.md, docs/03-logs/compacted/validation-log-compact.md, .codex/skills/_, tests/test_offload_index.py, tests/test_offload_retention.py, tests/test_log_compaction.py, docs/02-features/15-offload-audit-and-log-compaction/\*, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md

#### Docs Updated

- docs/04-process/output-offload.md
- docs/03-logs/implementation-log.md
- docs/03-logs/validation-log.md
- docs/03-logs/decision-log.md (if needed)
- docs/03-logs/bug-log.md (if needed)
- docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md
- docs/02-features/15-offload-audit-and-log-compaction/tech-design.md
- docs/02-features/15-offload-audit-and-log-compaction/test-plan.md

#### Plan

Plan Contract v1
Approach:

1. Update compaction path resolution and workflow so the compacted output directory is derived from configuration (defaulting to the required compacted outputs location) and ensure metadata requirements are enforced in generated artifacts.
   Files to change:

- `tools/log-compaction`
- `lib/log_compaction.py`
- Compaction workflow script/config that resolves compacted output path
  Risks:
- Incorrect path derivation could misroute artifacts or overwrite unrelated outputs.
  Tests (anti-hardcode coverage required):
- Fixture coverage: At least 2 fixtures per log type (decision/implementation/validation).
- Deterministic seed strategy: Fixed seed if ordering is applied.
- Invariant checks: Output includes source path, date/section, WI ref (if available), outcome/rationale, evidence refs.
- Contract boundary coverage: Missing/stale sections are marked explicitly.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

2. Run the compaction workflow to generate compacted outputs at the derived location and verify the expected decision/implementation/validation artifacts are created.
   Files to change:

- None (command execution only)
  Risks:
- Validation may miss edge cases if fixture coverage is insufficient.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A (workflow run).
- Deterministic seed strategy: N/A.
- Invariant checks: Derived location contains expected compacted outputs after run.
- Contract boundary coverage: N/A.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

3. Run the allowed tests to confirm behavior remains correct after path changes.
   Files to change:

- None (test execution only)
  Risks:
- Tests may still discover zero cases; verify expectations align with current test suite.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A.
- Deterministic seed strategy: N/A.
- Invariant checks: N/A.
- Contract boundary coverage: N/A.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

Note: Required updates to `docs/03-logs/*` are owned by reporter/orchestrator; patcher will not edit those files.

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

- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter failure shows missing compacted outputs and traceability log updates, so the plan must add explicit steps to generate compacted logs and ensure traceability updates.; patcher feedback pending.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=2/3).
- Attempt 2: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows outputs were written to the wrong location, so the plan must be updated to target the required derived path.; patcher feedback pending.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_attempt=3/3).
- Attempt 3: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows compacted outputs are written to the wrong location, so the plan must be updated to correct the output path and cleanup/migration behavior.; patcher feedback pending.
- Loop exhausted at MAX*LOOPS; last failure context: tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python -m unittest discover -s tests -p 'test*\_.py'`Notes: Results:`python -m unittest discover -s tests -p 'test\_\_.py'`-> 0 Discovery: no explicit discovery summary found in command output. Work Item ID: WI-20260209-01; reporter_feedback=Outcome: FAIL Docs/logs updated:`docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`File/Path:`docs/03-logs/compacted/`Check: Compacted outputs must be written to the derived location defined in the feature spec and dev tasks. Evidence:`docs/03-logs/compacted/`is missing; compacted outputs are present under`docs/02-features/WI-20260209-01/compacted`. Feature spec and dev tasks require `doc...
- Attempt 1: Plan Reviewer BLOCK; planner updated plan (reviewer_block=1/12, planner_revision=1/12, execution_attempt=1/3).
- Attempt 1: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows required compacted outputs are missing under `docs/03-logs/compacted/`, so the plan must explicitly ensure compaction writes there and re-run compaction.; patcher feedback pending.
- Attempt 2: Plan Reviewer BLOCK; planner updated plan (reviewer_block=2/12, planner_revision=2/12, execution_attempt=2/3).
- Attempt 2: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter failure indicates outputs are not generated in `docs/03-logs/compacted/`, so plan must explicitly fix path resolution and generate artifacts there.; patcher feedback pending.
- Attempt 3: Plan Reviewer BLOCK; planner updated plan (reviewer_block=3/12, planner_revision=3/12, execution_attempt=3/3).
- Attempt 3: tester=PASS, reporter=FAIL; planner decision=REVISE_PLAN; rationale=Reporter feedback shows compacted outputs are not being generated under the required location, so the plan must add explicit generation and verification of those artifacts.; patcher feedback pending.

#### Commit

- Commit message:

#### Final Report

-

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md`
- Tech Design: `docs/02-features/15-offload-audit-and-log-compaction/tech-design.md`
- Test Plan: `docs/02-features/15-offload-audit-and-log-compaction/test-plan.md`
- Planner Log: `docs/02-features/15-offload-audit-and-log-compaction/planner-log.md`
- Reporter Log: `docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`
- Validation Log: `docs/02-features/15-offload-audit-and-log-compaction/validation-log.md`

## Change Log

| Date       | Changes                                                                                                    | Author       |
| ---------- | ---------------------------------------------------------------------------------------------------------- | ------------ |
| 2026-02-09 | Reformulated compaction scope for decision/implementation/validation + usefulness contract/output location | Codex        |
| 2026-02-09 | Aligned workflow baseline to remove change-budget fields/section wording                                   | Codex        |
| 2026-02-08 | Rebased tasks to explicit offload index lifecycle                                                          | Codex        |
| 2026-02-05 | Initial task breakdown                                                                                     | Primary user |
