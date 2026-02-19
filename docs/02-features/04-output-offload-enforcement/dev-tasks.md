# Development Tasks: Output offload enforcement

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Output offload enforcement

Status: Done

**Last Updated:** 2026-02-03

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-04-001` Fail-open pointer-missing path exposes raw command output
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Change pointer-missing handling to fail-closed for offload-eligible commands (non-zero exit), emit only minimal remediation metadata, and require explicit opt-in for any stdout fallback.
- [ ] `SEC-04-002` Offload artifacts lack confidentiality controls
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce secure permissions (`0700` dirs, `0600` files), verify `.offload/` and sensitive logs are ignored by git templates, and add deterministic cleanup/retention handling.
- [ ] `SEC-04-003` Pointer ID and path safety requirements are missing
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Generate IDs internally, validate against a strict allowlist, canonicalize target paths under `.offload`, reject symlinks/non-regular files, and use exclusive file creation.
- [ ] `SEC-04-004` Security regression tests are not required by current task plan
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated tests for pointer-missing failure mode, missing-offload-dir recovery, path traversal/symlink attempts, and no-large-output-to-stdout guarantees; gate completion on these tests.
- [ ] `PROD-04-001` Fail-open pointer handling breaks user trust in offload enforcement
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Update spec and implementation to fail-closed by default when pointer generation fails, show concise remediation guidance, and allow stdout fallback only via explicit opt-in.
- [ ] `PROD-04-002` No deterministic definition of "noisy output" creates inconsistent UX
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define and enforce explicit offload eligibility rules (e.g., size/line thresholds and command classes), document them in feature docs, and surface them in CLI preflight/status text.
- [ ] `PROD-04-003` Recovery-path UX is underspecified and may stall users
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Standardize blocking error messages to include immediate remediation and rerun-safety status; add tests that assert this copy is emitted for failure scenarios.
- [ ] `PROD-04-004` Test plan does not guarantee end-user outcomes
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Expand TASK-401 coverage to include pointer-missing failure mode, missing offload directory recovery, below-threshold behavior, and explicit no-large-output-to-stdout assertions.
- [ ] `PROD-04-005` Acceptance quality is not measurable
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Replace placeholder success metric with concrete measurable targets and pass/fail thresholds tied to logs and automated checks.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-04-006` Human usability sign-off is required for pointer-first debugging flow
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Run human validation on one happy path and two failure paths to confirm pointer discoverability, clarity of next actions, and acceptable debug speed; record explicit PO sign-off.

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

- **Not Started:** 3
- **In Progress:** 1
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
