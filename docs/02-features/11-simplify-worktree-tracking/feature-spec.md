# Feature Specification: Simplify worktree tracking

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-11`

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Remove `feature-worktrees.json` and standardize on a single worktree per feature.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** reduce bookkeeping and confusion
- **Current pain:** extra tracking file is unnecessary for single worktree

### Why do they need it?

**As a** developer/PO

**I want to** a simpler worktree policy

**So that** cleaner workflow with fewer files

### User Value

- **Value proposition:** cleaner workflow with fewer files
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P0 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Remove references to `feature-worktrees.json`
- **Requirement 2:** Update process docs to single worktree per feature

#### Edge Cases

- **Edge Case 1:** Multiple worktrees exist for a feature
- **Edge Case 2:** Legacy files still present

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Docs and tooling no longer require feature-worktrees.json

## Scope

### In Scope

- Docs/process updates
- Tooling cleanup

### Out of Scope

- Changing worktree naming convention

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Older repos relying on the file

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                               | Risk                                                                                                                                                                                                                                  | Action                                                                                                                                                                                 |
| ---------- | -------- | ------- | -------------- | -------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-11-001 | High     | patcher | patch          | Yes      | Single-worktree invariant is not fail-closed                        | The spec lists the edge case "Multiple worktrees exist for a feature", but acceptance only says to remove `feature-worktrees.json`. Without an enforced stop when candidate worktrees != 1, patch/test can run in the wrong checkout. | Implement deterministic worktree resolution that hard-fails when match count is 0 or >1, with explicit remediation output before any patch/test step proceeds.                         |
| SEC-11-002 | High     | patcher | patch          | Yes      | Path-boundary controls are missing after metadata removal           | Moving from explicit JSON tracking to filesystem discovery introduces path/symlink abuse risk if canonical-path validation is not enforced, allowing operations outside the intended repo/worktree root.                              | Canonicalize with `realpath`, reject symlinks/untrusted paths, and enforce allowed root-prefix checks before any read/write or command execution against a resolved worktree path.     |
| SEC-11-003 | Medium   | patcher | automated-test | Yes      | Legacy `feature-worktrees.json` is an unneutralized trust input     | The edge case "Legacy files still present" is documented, but no required control states runtime must ignore/deprecate the file. Residual code paths could still consume stale or attacker-modified JSON.                             | Remove all runtime reads/writes of `feature-worktrees.json`, add explicit deprecated-file handling (ignore + warning), and fail CI if executable code references the file.             |
| SEC-11-004 | Medium   | patcher | automated-test | Yes      | No negative security regression tests for ambiguous worktree states | Current tasks do not require tests that prove fail-closed behavior for multi-worktree and legacy-file scenarios, so unsafe fallback behavior can regress silently.                                                                    | Add automated negative tests for: multiple matching worktrees, zero matching worktrees, legacy file present, and symlinked candidate path; require non-zero exit and no file mutation. |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                       | Risk                                                                                                                                     | Action                                                                                                                                                                                        |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-11-001 | High     | patcher | patch            | Yes      | Fail-closed worktree selection is not an explicit user acceptance condition | If zero or multiple worktrees match, users can run patch/test in the wrong checkout or face unclear failure behavior.                    | Add explicit acceptance and implementation behavior to hard-fail when match count is 0 or >1, with deterministic remediation text and guaranteed no mutation before resolution.               |
| PROD-11-002 | Medium   | patcher | patch            | Yes      | Legacy `feature-worktrees.json` deprecation UX is undefined                 | Users with existing repos may assume the legacy file is still authoritative, causing workflow confusion and inconsistent outcomes.       | Define and implement consistent deprecated-file handling in docs and CLI output: ignore legacy file, warn clearly, and provide the next action.                                               |
| PROD-11-003 | Medium   | patcher | automated-test   | Yes      | Recovery behavior is not acceptance-tested from the user perspective        | Regressions in ambiguous/missing/symlink/legacy states can silently return, breaking trust and increasing manual recovery effort.        | Add automated negative tests that assert non-zero exit, no file mutation, and actionable remediation messaging for zero/multiple worktrees, symlink path rejection, and legacy file presence. |
| PROD-11-004 | Medium   | patcher | patch            | Yes      | Migration path for existing repositories is under-specified                 | Current users may not know how to move from legacy tracking to the single-worktree model, leading to blocked or inconsistent executions. | Add a migration section to process docs covering detection of extra worktrees, canonical selection/remediation, legacy cleanup expectations, and rerun-safe verification.                     |
| PROD-11-005 | Medium   | human   | human-validation | Yes      | No required human validation of workflow clarity after migration            | Implementation can pass technical checks while still leaving end-user instructions unclear in real legacy scenarios.                     | Require PO/end-user sign-off in human validation using at least one legacy scenario (legacy file present and multiple worktrees) to confirm instructions are understandable and actionable.   |

<!-- review-findings:end -->
