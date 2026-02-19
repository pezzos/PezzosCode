# Development Tasks: Orchestrator + sub-agent roles

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Orchestrator + sub-agent roles

Status: In Progress

**Last Updated:** 2026-02-03

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-05-001` Gate artifacts are not integrity-protected
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Add a per-run artifact manifest (run_id, role, timestamp, SHA-256 for each artifact) and verify it at every gate transition; fail closed on any mismatch.
- [ ] `SEC-05-002` Role boundaries are defined but not enforceably sandboxed
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce role-based path allowlists/denylists in the orchestrator runner and reject out-of-scope writes with explicit errors.
- [ ] `SEC-05-003` HIGH-risk approval gate can be bypassed in non-interactive flows
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Require interactive TTY for HIGH-risk approval, bind approval to current run_id, and persist an approval audit record before unblocking.
- [ ] `SEC-05-004` Offload/log pipeline lacks secret redaction requirements
  - Reviewer: Security Expert
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Implement output scrubbing before write (credential/token patterns and configured secret keys), and add regression tests that fail when known secret fixtures appear in offload/log files.
- [ ] `SEC-05-005` Artifact file permissions are unspecified
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Create artifact directories/files with least-privilege permissions (`0700` dirs, `0600` files) and add automated checks for permission mode on creation.
- [ ] `PROD-05-001` Gate UX contract is underspecified for end users
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define and implement a strict CLI message contract for each Plan/Patch/Test/Report transition and failure state, including role, stage, artifact pointer, and explicit remediation; add output assertions.
- [ ] `PROD-05-002` Acceptance tests do not cover critical workflow failure loops
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated tests for conflicting-role outputs, skipped-gate fail-safe behavior, loopback-to-planner routing, and interrupted-run resume semantics with pass/fail expectations.
- [ ] `PROD-05-004` Blocked-state recovery guidance is too vague
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Update blocked/error UX to include missing prerequisite slugs, next valid command/action, and rerun-safety guidance; verify in tests.
- [ ] `PROD-05-005` Success metrics are not measurable
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: No
  - Action: Replace placeholder metrics with measurable thresholds and evidence sources in feature docs and validation logs.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-05-003` Human decision points are not explicitly captured as sign-off artifacts
  - Reviewer: Product Manager
  - Severity: High
  - Phase: human-validation
  - Action: Require human validation artifacts for PO decisions (run_id, decision, rationale, timestamp) and make completion contingent on that record.

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

| Date       | Changes                                          | Author       |
| ---------- | ------------------------------------------------ | ------------ |
| 2026-02-02 | Initial task breakdown                           | Developer/PO |
| 2026-02-03 | Document workflow gating details and update logs | Developer/PO |
