# Development Tasks: Update/reapply templates

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Update/reapply templates

**Status:** Not Started

**Last Updated:** 2026-02-02

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-03-001` Reapply write path is not constrained to repo root
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: In patching, resolve each target with canonical path checks, reject path traversal, and fail closed on symlinked targets (or enforce a strict symlink policy) before any write.
- [ ] `SEC-03-002` Protected-path policy is underspecified for non-interactive overwrite
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement an explicit protected-path policy (denylist/allowlist with precedence) and enforce it before overwrite decisions; include deterministic skip reporting for every protected file.
- [ ] `SEC-03-003` Partial failure safety lacks atomic reapply controls
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Use temp-file writes plus atomic rename, record resumable state, and ensure retries are idempotent and fail closed when state is inconsistent.
- [ ] `SEC-03-004` Security guardrail tests are missing from task plan
  - Reviewer: Security Expert
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated tests that must pass for: path traversal rejection, symlink boundary enforcement, protected-path non-overwrite, and safe retry after forced interruption.
- [ ] `PROD-03-001` Reapply mode contract is ambiguous for end users
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define and document deterministic mode semantics with concrete CLI examples: default conservative behavior, `--reapply` overwrite scope, protected-path precedence, and exit code meanings.
- [ ] `PROD-03-002` User-visible acceptance quality is not testable yet
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Expand automated tests to assert before/after file states, per-file applied/skipped reporting, idempotent reruns, and alignment with required security guardrail scenarios in `SEC-03-004`.
- [ ] `PROD-03-003` Partial-failure recovery UX is underspecified
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Require deterministic failure output that includes: what was applied, what was skipped, why execution stopped, exact safe rerun command, and whether cleanup is required.
- [ ] `PROD-03-004` Workflow gate behavior conflicts are unresolved
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Specify gate behavior by mode: interactive/default path vs non-interactive `--reapply`, with mandatory conflict/overwrite summaries in output when prompts are suppressed.

### Human Validation Requests (Product Owner / end-user)

- [ ] `SEC-03-005` Repo-specific secret path review is not explicitly required
  - Reviewer: Security Expert
  - Severity: Low
  - Phase: human-validation
  - Action: During human validation, review and approve the protected-path inventory for this repo and log the decision in `docs/03-logs`.
- [ ] `PROD-03-005` Repo-specific protected-path sign-off is missing
  - Reviewer: Product Manager
  - Severity: Low
  - Phase: human-validation
  - Action: PO/end-user must review and approve the protected-path inventory and exceptions, then record the decision in `docs/03-logs` before final sign-off.

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
