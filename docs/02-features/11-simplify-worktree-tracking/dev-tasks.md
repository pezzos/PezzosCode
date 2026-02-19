# Development Tasks: Simplify worktree tracking

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Simplify worktree tracking

Status: Done

**Last Updated:** 2026-02-05

## Tasks

- Task 1: Remove file references
- Task 2: Update docs/templates

## Execution Log

- No runs yet.

## Related Documents

- Feature Spec: [link to feature-spec.md]
- Tech Design: [link to tech-design.md]
- Test Plan: [link to test-plan.md]
- Planner Log: [link to planner-log.md]
- Reporter Log: [link to reporter-log.md]
- Validation Log: [link to validation-log.md]

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-05 | Initial task breakdown | Primary user |

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-11-001` Single-worktree invariant is not fail-closed
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement deterministic worktree resolution that hard-fails when match count is 0 or >1, with explicit remediation output before any patch/test step proceeds.
- [ ] `SEC-11-002` Path-boundary controls are missing after metadata removal
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Canonicalize with `realpath`, reject symlinks/untrusted paths, and enforce allowed root-prefix checks before any read/write or command execution against a resolved worktree path.
- [ ] `SEC-11-003` Legacy `feature-worktrees.json` is an unneutralized trust input
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Remove all runtime reads/writes of `feature-worktrees.json`, add explicit deprecated-file handling (ignore + warning), and fail CI if executable code references the file.
- [ ] `SEC-11-004` No negative security regression tests for ambiguous worktree states
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated negative tests for: multiple matching worktrees, zero matching worktrees, legacy file present, and symlinked candidate path; require non-zero exit and no file mutation.
- [ ] `PROD-11-001` Fail-closed worktree selection is not an explicit user acceptance condition
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Add explicit acceptance and implementation behavior to hard-fail when match count is 0 or >1, with deterministic remediation text and guaranteed no mutation before resolution.
- [ ] `PROD-11-002` Legacy `feature-worktrees.json` deprecation UX is undefined
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Define and implement consistent deprecated-file handling in docs and CLI output: ignore legacy file, warn clearly, and provide the next action.
- [ ] `PROD-11-003` Recovery behavior is not acceptance-tested from the user perspective
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add automated negative tests that assert non-zero exit, no file mutation, and actionable remediation messaging for zero/multiple worktrees, symlink path rejection, and legacy file presence.
- [ ] `PROD-11-004` Migration path for existing repositories is under-specified
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Add a migration section to process docs covering detection of extra worktrees, canonical selection/remediation, legacy cleanup expectations, and rerun-safe verification.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-11-005` No required human validation of workflow clarity after migration
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Require PO/end-user sign-off in human validation using at least one legacy scenario (legacy file present and multiple worktrees) to confirm instructions are understandable and actionable.

<!-- review-backlog:end -->
