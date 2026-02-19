# Development Tasks: Execute ticket workflow

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Execute ticket workflow

**Status:** Not Started

**Last Updated:** 2026-02-02

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-02-001` HIGH-risk approval gate is not identity-bound
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Require interactive TTY approval with an explicit typed confirmation containing the ticket ID, record approver OS user + timestamp in run metadata, and fail closed in non-interactive contexts. Add tests for missing/invalid approval paths.
- [ ] `SEC-02-002` Offload/log artifacts lack secret redaction controls
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement pre-write redaction for common secret patterns and configured project patterns, suppress raw secret-bearing env output, and add regression tests asserting masking behavior.
- [ ] `SEC-02-003` Dynamic log path inputs are not constrained against traversal
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce strict allowlist regex for IDs/step names, canonicalize and verify resolved paths remain under approved directories, and reject `..`, absolute paths, and separator variants. Add negative-path tests.
- [ ] `SEC-02-004` Workflow execution lacks explicit command allowlisting
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define per-stage command allowlists and argument schemas, execute via structured argv (no shell interpolation), and fail closed on unknown commands. Add tests proving denied commands are blocked.
- [ ] `SEC-02-005` Permissions for local security-relevant artifacts are unspecified
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: No
  - Action: Create artifact directories/files with restrictive permissions (`0700`/`0600`) and add automated checks to enforce expected modes on macOS.
- [ ] `PROD-02-001` Gate behavior is not specified as a deterministic user contract
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define explicit, testable output/state requirements for each gate (Plan, Patch, Test, Report), including required status labels, offload/log pointers, and remediation messaging.
- [ ] `PROD-02-002` Approval UX conflicts with security-required HIGH-risk approval flow
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Reconcile specs to one canonical HIGH-risk approval interaction aligned with SEC-02-001, then update tests and user-facing copy accordingly.
- [ ] `PROD-02-003` Retry/resume acceptance quality is underspecified
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated tests for fail-safe rerun behavior, including state integrity after failed tests and required summary markers (resumed/skipped/repaired/newly executed).
- [ ] `PROD-02-005` Success metrics are not measurable
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: No
  - Action: Replace placeholder metrics with concrete targets and measurement method tied to logs/offload artifacts.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-02-004` No explicit end-user sign-off gate for blocking prompt clarity
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Require PO human validation of blocking UX copy across happy/unhappy paths (HIGH-risk approval, missing preconditions, test failure, retry guidance) before completion.

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
