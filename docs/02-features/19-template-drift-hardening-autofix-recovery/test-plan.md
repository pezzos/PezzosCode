# Test Plan: Template drift hardening + autofix recovery

> **Validation strategy**

---

## Overview

**Feature:** Template drift hardening + autofix recovery

**Status:** Draft

**Last Updated:** 2026-02-11

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Test Objectives

- Verify drift detection catches template/living divergence reliably.
- Verify safe drift is auto-fixed with scoped restaging only.
- Verify ambiguous/out-of-scope drift fails closed with clear remediation.

### Test Scope

**In Scope:**

- Drift detector and classifier
- Scoped repair and restaging guardrails
- Precommit and CI path consistency

**Out of Scope:**

- Full semantic merge conflict resolution
- Non-template synchronization workflows

## Test Strategy

### Unit Tests

- Drift classifier by fixture category and direction.
- Touched-path allowlist enforcement.
- `pc-hooks-run` concise-failure summary/offload behavior (`tests/test_pc_hooks_run.py`).

### Integration Tests

- Precommit one-sided drift auto-fix flow.
- CI drift recheck behavior after autofix pass.

### E2E Tests

- End-to-end run starting from a drifted repo and ending with deterministic pass or fail-close.

## Test Cases

### Functional Tests

- `TC-19-001`: One-sided drift auto-fixes and re-stages allowed files.
- `TC-19-002`: Equivalent drift case yields same decision in precommit and CI.
- `TC-19-003`: Repaired repo passes subsequent targeted checks.

### Edge Cases

- `TC-19-101`: Conflicting two-sided drift blocks with remediation.
- `TC-19-102`: Drift touching disallowed path fails and reports file.

### Error Handling

- `TC-19-201`: Missing template mapping fails with actionable message.

### Regression

- `TC-19-301`: Existing non-drift precommit path remains unchanged.

## Test Execution

### Environment

- Local macOS CLI with fixture repos reflecting template/living drift scenarios.

### Entry Criteria

- Drift detection and scoped autofix implementation complete.
- Fixture matrix available for all critical paths.

### Exit Criteria

- All drift tests pass.
- No regressions in baseline precommit/CI behavior.

## Sign-off

**Approved By:** Developer/PO

**Date:** 2026-02-11

## Related Documents

- Feature Spec: `docs/02-features/19-template-drift-hardening-autofix-recovery/feature-spec.md`
- Tech Design: `docs/02-features/19-template-drift-hardening-autofix-recovery/tech-design.md`
- Dev Tasks: `docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md`

## Change Log

| Date       | Changes           | Author |
| ---------- | ----------------- | ------ |
| 2026-02-11 | Initial test plan | Codex  |
