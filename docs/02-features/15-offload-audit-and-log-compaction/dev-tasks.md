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
