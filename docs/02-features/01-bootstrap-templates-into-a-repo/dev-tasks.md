# Development Tasks: Bootstrap templates into a repo

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Bootstrap templates into a repo

**Status:** Not Started

**Last Updated:** 2026-02-02

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-01-001` Missing repo-boundary and symlink escape controls
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Resolve target/destination with canonical paths, reject any write that escapes repo root after resolution, and block writes through symlinked paths with a fail-closed error.
- [ ] `SEC-01-002` No protected-path policy for overwrite/merge/skip
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement protected path rules: hard-deny `.git/**`, default-skip sensitive patterns, and require explicit opt-in with deterministic confirmation for any protected overwrite.
- [ ] `SEC-01-003` Local-only security requirement is not enforced
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce offline behavior by default (no network subprocesses), require explicit flag for any remote source, and log source provenance in run output.
- [ ] `SEC-01-004` Permission and executable-bit hardening is unspecified
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Normalize file modes on write, allow executable bit only for approved script paths, and strip suid/sgid bits.
- [ ] `SEC-01-005` Security regression coverage is absent in test scenarios
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add negative automated tests for all mandatory controls and make them required in the feature test gate.
- [ ] `PROD-01-001` CLI contract is not explicit enough for users to execute confidently
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define the exact command(s), required/optional flags, exit code behavior, and deterministic summary fields (applied/merged/skipped/conflicts, rerun status, log path).
- [ ] `PROD-01-002` Core promise of safe re-runs is not acceptance-tested
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated tests for first-run and rerun behavior across clean and conflicted repos; assert deterministic no-op/expected changes and user-facing rerun summary output.
- [ ] `PROD-01-003` Conflict handling UX is under-specified for destructive choices
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Specify deterministic prompt copy with safe default, preview impacted files before apply, explicit confirmation for destructive paths, and cancel/retry guidance aligned with SEC-01 protected-path constraints.
- [ ] `PROD-01-004` Recovery contract for failure states is incomplete
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Require fail-closed preflight checks before writes and standardize blocking error messages to include remediation and explicit rerun-safety status.
- [ ] `PROD-01-005` Acceptance quality is weakened by unresolved template and subjective metrics
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Replace placeholders with measurable targets and map each acceptance criterion to concrete automated-test or human-validation evidence.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-01-006` No explicit human validation gate for end-user clarity
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Run human validation on at least: clean repo bootstrap, conflicted repo choice flow, and non-git path failure; require explicit PO sign-off.

<!-- review-backlog:end -->

## Task Breakdown

### CLI Development

- [ ] **TASK-101: Define workflow behavior**
  - Document required steps, gates, and outputs
  - **Acceptance:** Behavior is specified in docs
  - **Estimate:** 0.5 day

- [ ] **TASK-102: Implement or update tooling/scripts**
  - Update scripts or templates to enforce behavior
  - **Acceptance:** Tooling matches specification
  - **Estimate:** 1 day

### Testing

- [ ] **TASK-401: Add or update tests**
  - Add regression tests or checks where applicable
  - **Acceptance:** Tests cover the primary path
  - **Estimate:** 0.5 day

### Documentation

- [ ] **TASK-501: Update docs/logs**
  - Update process docs and logs
  - **Acceptance:** Documentation matches implementation
  - **Estimate:** 0.5 day

## Task Summary

### By Status

- **Not Started:** 4
- **In Progress:** 0
- **Complete:** 0
- **Blocked:** 0

### By Category

- **Setup:** 0 tasks
- **Backend:** 0 tasks
- **Frontend:** 0 tasks
- **Integration:** 0 tasks
- **Testing:** 1 task
- **Documentation:** 1 task
- **Deployment:** 0 tasks

## Blocked Tasks

None.

## Notes for LLM Execution

### Context to Provide

- Feature specification (feature-spec.md)
- Technical design (tech-design.md)
- Current system map (docs/00-context/system-map.md)

### Execution Guidelines

- Complete tasks in dependency order
- Run tests after each task
- Commit after each completed task
- Ask questions if requirements are unclear

## Related Documents

- Feature Spec: feature-spec.md
- Tech Design: tech-design.md
- Test Plan: test-plan.md

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-02 | Initial task breakdown | Developer/PO |
