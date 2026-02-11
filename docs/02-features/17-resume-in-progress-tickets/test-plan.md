# Test Plan: Resume in-progress tickets

> **Validation strategy**

---

## Overview

**Feature:** Resume in-progress tickets

**Status:** Draft

**Last Updated:** 2026-02-11

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Test Objectives

- Verify resume mode behavior is deterministic.
- Verify resume routing never skips mandatory validation gates.
- Verify inconsistent state is blocked with explicit diagnostics.

### Test Scope

**In Scope:**

- Resume snapshot parsing
- Mode policy (`auto`/`prompt`/`fresh`)
- Step routing and rerun requirements
- Resume logging

**Out of Scope:**

- Multi-user workflows
- Non-CLI surfaces

## Test Strategy

### Unit Tests

- Resume snapshot parser handles complete, partial, and inconsistent artifacts.
- Policy resolver applies each mode correctly.

### Integration Tests

- Resume from planner/tester/reporter checkpoints.
- Dirty-worktree handling in `auto` and `fresh` modes.

### E2E Tests

- Simulated interrupted run resumes and completes final `make ci` gate.

## Test Cases

### Functional Tests

- `TC-17-001`: Resume from completed planner+reviewer and continue at patcher.
- `TC-17-002`: Resume after tester fail routes back to planner.
- `TC-17-003`: Resume after reporter pass proceeds to final gates.

### Edge Cases

- `TC-17-101`: Contradictory step state blocks with remediation.
- `TC-17-102`: Dirty worktree preserved in `auto` mode.

### Error Handling

- `TC-17-201`: Missing critical artifacts returns deterministic block/error.

### Regression

- `TC-17-301`: Existing non-resume execution path remains unchanged.

## Test Execution

### Environment

- Local macOS CLI environment with representative feature worktree artifacts.

### Entry Criteria

- Resume implementation merged in working tree.
- Test fixtures for interrupted runs prepared.

### Exit Criteria

- All resume tests pass.
- No regressions in baseline workflow tests.

## Sign-off

**Approved By:** Developer/PO

**Date:** 2026-02-11

## Related Documents

- Feature Spec: `docs/02-features/17-resume-in-progress-tickets/feature-spec.md`
- Tech Design: `docs/02-features/17-resume-in-progress-tickets/tech-design.md`
- Dev Tasks: `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`

## Change Log

| Date       | Changes           | Author |
| ---------- | ----------------- | ------ |
| 2026-02-11 | Initial test plan | Codex  |
