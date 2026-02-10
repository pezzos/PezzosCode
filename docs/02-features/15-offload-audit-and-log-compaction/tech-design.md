# Technical Design: Offload audit + useful log compaction

> **Architecture & implementation approach**

---

## Overview

**Feature:** Offload audit + log compaction

**Status:** Complete

**Last Updated:** 2026-02-10

### Summary

Extend the current offload wrapper workflow with metadata indexing and retention commands, then add skill-driven compaction for high-volume logs with an explicit usefulness contract for continuous workflow improvement.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Persist offload metadata in an append-friendly index format.
- Provide list/get/purge command interfaces with predictable filtering.
- Keep compaction output reproducible, useful, and linked to source sections.
- Ensure compaction does not mutate canonical source logs.
- Require compact artifacts to include source/date/work-item/evidence references.
- Persist compact artifacts in a non-destructive derived location.

## Architecture

### System Context

```text
command -> tools/offload-proxy/pp -> .offload/<id>.txt
                                 -> offload index (metadata)
                                 -> list/get/purge utilities

logs (decision/implementation/validation)
  -> compaction skill
  -> docs/03-logs/compacted/<source>-compact.md (derived summary, no source mutation)
```

### Data Model

Proposed offload index record (jsonl or equivalent line-based format):

- `id`
- `command`
- `work_item_id`
- `agent_name`
- `timestamp`
- `size_bytes`
- `path`

Compaction output contract includes:

- source file path
- source section/date reference
- work item id/reference (if available)
- concise outcome/rationale summary
- evidence references (offload ids and/or `logs/<WI>/<step>.log` paths)
- concise summary text

## Implementation Plan

1. Define index schema and storage location (`.offload/index.*`).
2. Hook index writes into offload path in `tools/offload-proxy/pp` flow.
3. Implement list/get/purge utilities with retention policy options.
4. Define compact artifact location and naming under `docs/03-logs/compacted/`.
5. Create compaction skills for decision/implementation/validation logs.
6. Add validation for index integrity, compaction fidelity, and contract completeness.

## Validation Strategy

- Unit tests for index record creation and schema validation.
- Command tests for list/get/purge behavior and retention handling.
- Golden-style checks confirming compaction keeps critical references.
- Contract checks confirming compact outputs always contain source/date/outcome/evidence fields.

## Documentation Needs

- [x] Process/doc updates
- [x] Implementation log entry
- [x] Validation log entry (if tests executed)
- [ ] API documentation
- [ ] User guide updates

## Related Documents

- Feature Spec: `docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md`
- Dev Tasks: `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- Test Plan: `docs/02-features/15-offload-audit-and-log-compaction/test-plan.md`
- Offload Process Doc: `docs/04-process/output-offload.md`

## Change Log

| Date       | Version | Changes                                                                  | Author       |
| ---------- | ------- | ------------------------------------------------------------------------ | ------------ |
| 2026-02-09 | 0.3     | Reformulated around useful compaction contract + validation-log coverage | Codex        |
| 2026-02-08 | 0.2     | Rebased design to explicit index/retention/compaction flow               | Codex        |
| 2026-02-05 | 0.1     | Initial design                                                           | Primary user |
