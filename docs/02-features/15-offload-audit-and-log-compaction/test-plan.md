# Test Plan: Offload audit + useful log compaction

> **Validation strategy**

---

## Overview

**Feature:** Offload audit + log compaction

**Status:** Draft

**Last Updated:** 2026-02-09

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Test Strategy

- Validate offload index creation and schema integrity.
- Validate list/get/purge behavior under retention scenarios.
- Validate compaction output fidelity against source decision/implementation/validation logs.
- Validate compact-output contract fields and derived-output location invariants.

## Planned Test Commands

- `python -m unittest discover -s tests -p "test_*.py"`
- `tools/offload-proxy/pp rg -n "offload|index|purge|retention" tools tests docs/04-process/output-offload.md`
- `tools/offload-proxy/pp rg -n "decision-log|implementation-log|validation-log|compact|compacted" .codex/skills docs/03-logs docs/02-features/15-offload-audit-and-log-compaction`

## Acceptance Tests

- Offload index record is created for an offloaded command and includes required fields.
- List/get utilities can retrieve the artifact by id and metadata filters.
- Purge obeys retention rules and reports removed/kept entries.
- Compaction output preserves source references and does not alter canonical logs.
- Compaction generates useful compact artifacts for decision/implementation/validation logs under `docs/03-logs/compacted/`.
- Each compact artifact includes required fields: source path, source section/date, work item reference (if available), concise outcome/rationale, and evidence reference(s).

## Approval

**Approved By:** TBD

**Date:** TBD

## Related Documents

- Feature Spec: `docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md`
- Tech Design: `docs/02-features/15-offload-audit-and-log-compaction/tech-design.md`
- Dev Tasks: `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- Offload Process Doc: `docs/04-process/output-offload.md`
- Bug Log: `docs/03-logs/bug-log.md`

## Change Log

| Date       | Changes                                                                                | Author       |
| ---------- | -------------------------------------------------------------------------------------- | ------------ |
| 2026-02-09 | Reformulated validation scope for useful compaction contract + validation-log coverage | Codex        |
| 2026-02-08 | Rebased tests for index/list/get/purge + compaction                                    | Codex        |
| 2026-02-05 | Initial test plan                                                                      | Primary user |
