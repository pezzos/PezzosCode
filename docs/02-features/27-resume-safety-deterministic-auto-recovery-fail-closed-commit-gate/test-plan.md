# Test Plan: Resume safety + deterministic auto-recovery + fail-closed commit gate

> **Validation strategy**

---

## Overview

**Feature:** Resume safety + deterministic auto-recovery + fail-closed commit gate

**Status:** Draft

**Last Updated:** 2026-02-19

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

### Test Objectives

- Validate `Resume safety + deterministic auto-recovery + fail-closed commit gate` acceptance criteria.
- Prove deterministic behavior across reruns.
- Cover edge conditions and failure handling.

### Test Scope

**In Scope:**

- Core behavior for `Resume safety + deterministic auto-recovery + fail-closed commit gate`
- Integration points touched by the implementation
- Regression checks for existing behavior

**Out of Scope:**

- Unrelated roadmap features
- Infrastructure changes outside this feature boundary

## Test Strategy

### Unit Tests

- Validate core logic and helper behavior.
- Include both expected path and boundary conditions.

### Integration Tests

- Validate interactions between changed modules.
- Confirm artifacts/log updates are deterministic when applicable.

### Manual Verification

- Verify developer workflow remains stable after changes.
- Confirm generated docs/artifacts are feature-specific.

## Test Cases

### Functional Tests

- **TC-F001:** Generate or update feature artifacts and verify content is hydrated.
- **TC-F002:** Re-run workflow and confirm idempotent behavior.
- **TC-F003:** Verify skip behavior for done/deferred/rejected items.

### Edge Cases

- Missing status lines in existing `dev-tasks.md`.
- Existing folder index/slug drift.
- Missing template files in partially-created folders.

## Exit Criteria

- `Interrupted runs resume safely; common deterministic failures self-heal safely.`
- Targeted automated tests pass.
- Validation evidence is recorded in `docs/03-logs/validation-log.md`.
