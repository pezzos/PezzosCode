# Test Plan: Synthetic feature workflow smoke test

> **Validation strategy**

---

## Overview

**Feature:** Synthetic feature workflow smoke test

**Status:** Draft

**Last Updated:** 2026-02-13

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Test Objectives

- Verify synthetic fixture can exercise full workflow deterministically with fixed scenario-id/seed mapping.
- Verify critical paths include at least 2 fixtures per path (baseline pass path and gate/resume failure path) with distinct evidence pointers.
- Verify invariant checks detect role-routing, Allowed Tests whitelist, resume-stage, and structured-log regressions.
- Verify smoke output points to actionable evidence.

### Test Scope

**In Scope:**

- Fixture setup and teardown
- End-to-end role loop execution
- Invariant evaluator and report generation

**Out of Scope:**

- Performance benchmarking under large workloads
- Product-specific business feature validation

## Test Strategy

### Unit Tests

- Invariant evaluator pass/fail behavior.
- Synthetic fixture parser/loader validation.

### Integration Tests

- Baseline synthetic workflow run passes.
- Injected gate violation fails at expected stage.
- Allowed Tests whitelist mismatch is rejected with deterministic policy feedback.

### E2E Tests

- Full synthetic run including resume-path scenario.
- Resume-path failure scenario reports required structured log artifact pointers.

## Test Cases

### Functional Tests

- `TC-20-001`: Baseline synthetic run completes all stages.
- `TC-20-002`: Stage routing matches expected control-flow contract.
- `TC-20-003`: Summary includes failed stage and log pointers.

### Edge Cases

- `TC-20-101`: Resume scenario after synthetic interruption routes correctly.
- `TC-20-102`: Missing synthetic artifact fails with clear remediation.

### Error Handling

- `TC-20-201`: Unexpected gate outcome returns deterministic failure report.

### Regression

- `TC-20-301`: Standard non-synthetic runs remain unchanged.

## Test Execution

### Environment

- Local macOS CLI with synthetic fixture artifacts and standard tooling.

### Entry Criteria

- Synthetic fixture + evaluator implementation complete.
- Required logs and assertion helpers available.
- Allowed Tests section contains only scoped unittest/pytest commands.

### Exit Criteria

- All synthetic smoke tests pass.
- Failure diagnostics are clear and reproducible.
- Pass/fail summaries include explicit evidence pointers for each fixture.

### Allowed Test Commands

- `python3 -m unittest tests.test_pc_feature`
- `python3 -m unittest tests.test_orchestrator_workflow_docs`

## Sign-off

**Approved By:** Developer/PO

**Date:** 2026-02-11

## Related Documents

- Feature Spec: `docs/02-features/20-synthetic-feature-workflow-smoke-test/feature-spec.md`
- Tech Design: `docs/02-features/20-synthetic-feature-workflow-smoke-test/tech-design.md`
- Dev Tasks: `docs/02-features/20-synthetic-feature-workflow-smoke-test/dev-tasks.md`

## Change Log

| Date       | Changes                                                         | Author |
| ---------- | --------------------------------------------------------------- | ------ |
| 2026-02-11 | Initial test plan                                               | Codex  |
| 2026-02-13 | Added deterministic fixture/invariant and Allowed Tests details | Codex  |
