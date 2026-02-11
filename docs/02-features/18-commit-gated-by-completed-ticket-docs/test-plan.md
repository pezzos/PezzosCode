# Test Plan: Commit gated by completed ticket docs

> **Validation strategy**

---

## Overview

**Feature:** Commit gated by completed ticket docs

**Status:** Draft

**Last Updated:** 2026-02-11

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Test Objectives

- Verify commit is blocked when required ticket docs are incomplete.
- Verify commit proceeds when required fields are complete.
- Verify diagnostics are precise and actionable.

### Test Scope

**In Scope:**

- Required-section parser
- Completeness evaluator
- Final commit gate integration
- Logging of gate outcomes

**Out of Scope:**

- Changes to commit message style policy
- Remote/git host integrations

## Test Strategy

### Unit Tests

- Required-section extraction from canonical and malformed markdown.
- Missing-field detection and stable error messages.

### Integration Tests

- Commit gate fail path with incomplete `dev-tasks`/role logs.
- Commit gate pass path with complete docs.

### E2E Tests

- Full work-item simulation validating gate behavior before commit.

## Test Cases

### Functional Tests

- `TC-18-001`: Missing `Tests Run` blocks commit.
- `TC-18-002`: Missing final report blocks commit.
- `TC-18-003`: Complete docs allow commit flow.

### Edge Cases

- `TC-18-101`: Duplicate section headings use deterministic interpretation.
- `TC-18-102`: Empty section body counts as missing evidence.

### Error Handling

- `TC-18-201`: Malformed markdown returns remediation guidance.

### Regression

- `TC-18-301`: Existing successful final-gate flows remain unchanged.

## Test Execution

### Environment

- Local macOS CLI with representative feature docs and role logs.

### Entry Criteria

- Commit-gate implementation present.
- Test fixtures include complete and incomplete documentation samples.

### Exit Criteria

- All commit-gate tests pass.
- No regressions in existing gate behavior.

## Sign-off

**Approved By:** Developer/PO

**Date:** 2026-02-11

## Related Documents

- Feature Spec: `docs/02-features/18-commit-gated-by-completed-ticket-docs/feature-spec.md`
- Tech Design: `docs/02-features/18-commit-gated-by-completed-ticket-docs/tech-design.md`
- Dev Tasks: `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`

## Change Log

| Date       | Changes           | Author |
| ---------- | ----------------- | ------ |
| 2026-02-11 | Initial test plan | Codex  |
