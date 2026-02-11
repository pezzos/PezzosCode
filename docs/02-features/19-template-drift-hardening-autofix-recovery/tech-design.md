# Technical Design: Template drift hardening + autofix recovery

> **Architecture & implementation approach**

---

## Overview

**Feature:** Template drift hardening + autofix recovery

**Status:** Draft

**Last Updated:** 2026-02-11

### Summary

Introduce deterministic drift detection and scoped autofix controls in precommit/CI flows.
The system classifies drift, applies safe repairs, enforces scoped restaging, and blocks on unresolved ambiguity.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

## Technical Requirements

### From Feature Spec

- Detect and classify template/living-file drift.
- Auto-repair only deterministic one-sided drift.
- Enforce strict scoped restaging.
- Fail closed for unresolved or unsafe drift.

### Technical Constraints

- No broad/staged-all restaging in autofix path.
- Preserve existing CI two-attempt model.
- Keep precommit-only autofix from modifying global logs/execution logs.

## Architecture

### System Context

- Precommit path: detects drift before commit completes.
- CI autofix path: retries once after deterministic fixers.
- Shared drift classifier provides consistent decisioning.

### Component Design

- Drift Detector
  - Compares template source paths and live repo targets.
  - Produces structured drift report.
- Drift Classifier
  - Labels drift as safe-auto-fix, unsafe, or unknown.
- Scoped Repair Engine
  - Applies deterministic file-level sync operations.
  - Tracks touched files for enforcement.
- Scope Guard
  - Validates re-staged paths are within allowed scope.

### Data Model

- `drift_item`: template path, target path, drift direction, hash metadata
- `drift_decision`: auto-fix/manual/block
- `touched_paths`: autofix-modified file list for scope enforcement

## Integration Points

- Precommit script(s)
- CI autofix script path
- `tools/templates/` source-of-truth files
- Logging/output offload for diagnostics

## Implementation Approach

### Phase 1: Drift detection primitives

- Build drift report generator.
- Add deterministic classification rules.

### Phase 2: Scoped autofix + restage guardrails

- Implement safe repair operations.
- Enforce touched-path allowlist and fail out-of-scope touches.

### Phase 3: CI/precommit integration + regression tests

- Wire detector/classifier into both flows.
- Add tests for one-sided/ambiguous/out-of-scope scenarios.

## Technical Decisions

### Decision 1: Shared drift classifier for precommit and CI

- Reason: avoid divergent behavior across gates.
- Outcome: single decision model for consistency.

### Decision 2: Fail closed on ambiguous drift

- Reason: safety is higher priority than speculative autofix.
- Outcome: explicit remediation instead of risky edits.

## Error Handling

- Missing template path mapping: block with mapping remediation.
- Repair modifies out-of-scope file: rollback scoped action and fail.
- Drift report parse failure: block and require manual check.

## Testing Strategy

### Unit Tests

- Drift detection/classification with fixture matrix.
- Scoped-path enforcement logic.

### Integration Tests

- Precommit one-sided drift auto-fix path.
- CI ambiguous drift fail-closed path.

### E2E Tests

- Simulated repo drift through full precommit + CI cycle.

## Documentation Needs

- Update process docs for drift classification and remediation flow.
- Add implementation/validation log entries after rollout.

## Related Documents

- Feature Spec: `docs/02-features/19-template-drift-hardening-autofix-recovery/feature-spec.md`
- Dev Tasks: `docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md`
- Test Plan: `docs/02-features/19-template-drift-hardening-autofix-recovery/test-plan.md`

## Change Log

| Date       | Version | Changes        | Author |
| ---------- | ------- | -------------- | ------ |
| 2026-02-11 | 0.1     | Initial design | Codex  |
