# Technical Design: Incremental prd-to-features

> **Architecture & implementation approach**

---

## Overview

**Feature:** Incremental prd-to-features

**Status:** Done

**Last Updated:** 2026-02-09

### Summary

Implement deterministic update-in-place generation for feature docs, driven by PRD priority list and existing feature folder state.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Parse PRD feature list and map it to indexed folder names.
- Discover existing feature folders and current `Status` from `dev-tasks.md`.
- Enforce additive-only behavior (no deletion) and `Status: Done` skip.
- Produce a clear action summary (`created`, `updated`, `skipped`).

## Architecture

### System Context

```text
docs/00-context + docs/01-product/prd.md
                    |
                    v
          prd-to-features workflow
                    |
      docs/02-features/<index>-<slug>/
```

### Data Model

Input records:

- PRD feature entry (priority/order/title/outcome)
- existing feature folder map (index/slug/path)
- dev-task status (`Status: ...`)

Output actions:

- `create_missing`
- `update_in_place`
- `skip_done`
- `skip_existing`

## Implementation Plan

1. Parse PRD prioritized feature list into ordered feature records.
2. Build existing feature map from `docs/02-features/` (excluding template folder).
3. For each PRD feature:
   - if folder missing: create from template
   - if folder exists and done: skip
   - if folder exists and not done: update missing sections only
4. Emit deterministic action summary with reasons.
5. Validate that no delete operations are performed.

## Validation Strategy

- Fixture tests for create/update/skip cases.
- Regression test ensuring done features are not regenerated.
- Regression test ensuring existing folders are never deleted.
- Diff-based validation that reruns are idempotent.

## Documentation Needs

- [x] Process/doc updates
- [x] Implementation log entry
- [x] Validation log entry (if checks run)
- [ ] API documentation
- [ ] User guide updates

## Related Documents

- Feature Spec: `docs/02-features/12-incremental-prd-to-features/feature-spec.md`
- Dev Tasks: `docs/02-features/12-incremental-prd-to-features/dev-tasks.md`
- Test Plan: `docs/02-features/12-incremental-prd-to-features/test-plan.md`
- PO Loop Policy: `docs/04-process/human-orchestration-workflow.md`

## Change Log

| Date       | Version | Changes                                     | Author       |
| ---------- | ------- | ------------------------------------------- | ------------ |
| 2026-02-08 | 0.2     | Rebased design to current incremental rules | Codex        |
| 2026-02-05 | 0.1     | Initial design                              | Primary user |
