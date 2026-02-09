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
- Outcome:
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes: Main head locked: eabec517e15ba4a8b23eaf74f43bdbe19cc6d829

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

1. Inspect existing offload wrapper and config, then define/implement the index schema and lifecycle commands (list/get/purge) with retention options.
   Files to change:

- `tools/offload-proxy/pp`
- `pp.yml`
- `.offload/index.jsonl` (if committed as a schema/sample)
- `tools/offload-proxy/` (supporting scripts/modules as needed)
  Risks:
- Retention logic could remove artifacts still referenced by active work items.
- Index format changes could break existing consumers.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Use at least 2 fixtures each for index entries and retention scenarios (e.g., “missing file”, “active WI reference”).
- Deterministic seed strategy: Use a fixed seed for any randomized ordering/filtering in tests.
- Invariant checks: Validate required fields and stable ordering for list/get/purge outputs.
- Contract boundary coverage: Ensure list/get/purge handle missing backing files and unknown ids.

2. Implement compaction skills and compact-output contract enforcement for decision/implementation/validation logs, writing derived outputs to the compacted location.
   Files to change:

- `.codex/skills/` (new/updated compaction skills)
- `docs/04-process/output-offload.md` (if process guidance needs alignment)
  Risks:
- Compaction could drop critical rationale or evidence references.
  Tests (anti-hardcode coverage required):
- Fixture coverage: At least 2 fixtures per log type (decision/implementation/validation).
- Deterministic seed strategy: Fixed seed for any ordering or sampling in compaction.
- Invariant checks: Compact output always includes source path, date/section, WI ref (if available), outcome/rationale, evidence refs.
- Contract boundary coverage: Handle stale/missing source sections gracefully with explicit markers.

3. Add tests for index integrity, retention behavior, and compaction contract completeness.
   Files to change:

- `tests/test_offload_index.py`
- `tests/test_offload_retention.py`
- `tests/test_log_compaction.py`
  Risks:
- Overly brittle fixtures may cause false negatives.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Minimum 2 fixtures per critical path (index, retention, compaction).
- Deterministic seed strategy: Fixed seed applied in test setup.
- Invariant checks: Schema validation, ordering, and contract completeness.
- Contract boundary coverage: Missing artifacts, stale references, and empty log sections.

Handoff note: Any required updates to `docs/03-logs/*` (including compacted outputs) are owned by reporter/orchestrator; patcher will not edit those files.

- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

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

-

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
