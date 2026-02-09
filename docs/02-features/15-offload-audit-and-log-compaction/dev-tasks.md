# Development Tasks: Offload audit + log compaction

> **LLM-executable tasks**

---

## Overview

**Feature:** Offload audit + log compaction

**Status:** Not Started

**Last Updated:** 2026-02-08

## Task Breakdown

- [ ] **Task 1 - Define and persist offload index schema**
  - Choose index format and location under `.offload/`.
  - Capture metadata fields: id, command, WI, agent, timestamp, size, path.
  - Output: deterministic index entries for every offloaded artifact.

- [ ] **Task 2 - Implement offload lifecycle commands**
  - Add list/get/purge utilities for indexed artifacts.
  - Include retention policy options (for example by age/count).
  - Output: predictable artifact retrieval and cleanup workflow.

- [ ] **Task 3 - Implement log compaction skills**
  - Add skills for compacting decision and implementation logs.
  - Preserve source references and chronology in compact outputs.
  - Output: reusable compaction workflows with no source-log deletion.

- [ ] **Task 4 - Add tests and docs/log sync**
  - Add tests for index integrity, list/get/purge behavior, and compaction fidelity.
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

| Date       | Changes                                                                  | Author       |
| ---------- | ------------------------------------------------------------------------ | ------------ |
| 2026-02-09 | Aligned workflow baseline to remove change-budget fields/section wording | Codex        |
| 2026-02-08 | Rebased tasks to explicit offload index lifecycle                        | Codex        |
| 2026-02-05 | Initial task breakdown                                                   | Primary user |
