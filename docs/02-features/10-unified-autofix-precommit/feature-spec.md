# Feature Specification: Unified autofix for CI + precommit

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-10`

**Status:** Done

**Owner:** Developer/PO

**Last Updated:** 2026-02-07

### Summary

Use a single autofix script for CI and precommit, re-stage fixes, and run Codex in vanilla config for staged-only fixes.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** consistent autofix behavior across CI and hooks
- **Current pain:** autofix logic diverges and staged fixes are not re-applied

### Why do they need it?

**As a** developer/PO

**I want to** one script used by both CI and precommit

**So that** fewer regressions and predictable fixes

### User Value

- **Value proposition:** fewer regressions and predictable fixes
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P0 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Create a unified autofix script used by `make ci` and precommit
- **Requirement 2:** Run `git add -u` after autofix and print modified files
- **Requirement 3:** Ensure precommit uses vanilla Codex config (no Serena MCP)

#### Edge Cases

- **Edge Case 1:** No staged files to fix
- **Edge Case 2:** Autofix fails and must surface clear error

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- CI and precommit both invoke the same script
- Modified files are re-staged and listed

## Scope

### In Scope

- Autofix script
- Precommit behavior
- Docs/process updates

### Out of Scope

- Changing lint/format rules

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Unexpected staging of unrelated files

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                     | Risk                                                                                                                                                                                            | Action                                                                                                                                                                                                                          |
| ---------- | -------- | ------- | -------------- | -------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-10-001 | High     | patcher | patch          | Yes      | Unscoped `git add -u` can stage unrelated tracked changes | The feature spec already flags "Unexpected staging of unrelated files"; using `git add -u` after autofix can silently include unrelated edits in the commit.                                    | In the unified autofix script, snapshot the pre-hook staged path set (`git diff --cached --name-only -z`), restage only that set (or its autofix-touched subset), and hard-fail if autofix changed tracked files outside scope. |
| SEC-10-002 | High     | patcher | patch          | Yes      | Vanilla Codex mode is required but not fail-closed        | Requirement 3 mandates vanilla config (no Serena MCP), but acceptance criteria do not enforce a guard; hook execution could fall back to user/global config and enable external MCP connectors. | Hard-pin vanilla config/env in `tools/pc-precommit` and fail immediately if vanilla mode cannot be applied; add a regression check that rejects Serena-enabled execution.                                                       |
| SEC-10-003 | High     | patcher | automated-test | Yes      | Autofix failure path is not explicitly commit-blocking    | Edge case only requires a clear error message; without explicit non-zero propagation, precommit/CI can fail open and allow partially fixed or unchecked code.                                   | Propagate non-zero exit codes from unified autofix through precommit and CI, and add a negative-path automated test that injects autofix failure and asserts commit/CI is blocked.                                              |
| SEC-10-004 | Medium   | patcher | patch          | No       | Filename/path parsing safety is unspecified               | If staged-file handling is whitespace/shell-split based, crafted filenames (spaces/newlines/globs) can be misparsed, causing unintended file processing or staging.                             | Use NUL-delimited git output (`-z`) and strict quoted/array-safe shell handling, plus a regression test with problematic filenames.                                                                                             |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                 | Risk                                                                                                                                       | Action                                                                                                                                                                        |
| ----------- | -------- | ------- | ---------------- | -------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-10-001 | High     | patcher | patch            | Yes      | Restaging scope can include unrelated user work       | Using broad restage behavior after autofix can silently add unrelated tracked edits, breaking user trust and making commits unpredictable. | Snapshot the pre-hook staged set (`git diff --cached --name-only -z`), restage only that set (or its autofix-touched subset), and fail if out-of-scope tracked files changed. |
| PROD-10-002 | High     | patcher | patch            | Yes      | Vanilla precommit mode is not fail-closed             | If precommit can fall back to non-vanilla config, behavior diverges from spec and can enable unintended MCP integrations.                  | Hard-pin vanilla Codex config/env in precommit and exit non-zero if vanilla mode cannot be enforced; add a regression check that rejects Serena-enabled execution.            |
| PROD-10-003 | High     | patcher | automated-test   | Yes      | Autofix failure path may fail open                    | If unified autofix errors do not reliably propagate, commits/CI can proceed with partially fixed or unchecked code.                        | Propagate non-zero exit codes end-to-end and add negative-path automated tests that inject autofix failure and assert commit/CI is blocked.                                   |
| PROD-10-004 | Medium   | patcher | automated-test   | Yes      | No-staged-files behavior is under-specified for users | Without explicit no-op behavior and messaging, users cannot tell whether nothing needed fixing or the hook skipped work incorrectly.       | Define and test a deterministic no-staged-files outcome (clear message, no staging changes, correct exit code).                                                               |
| PROD-10-005 | Medium   | patcher | patch            | No       | Filename parsing robustness is not guaranteed         | Whitespace/newline/special-character paths can be misparsed, causing wrong files to be processed or staged.                                | Use NUL-delimited git output and array-safe shell handling; add regression tests with problematic filenames.                                                                  |
| PROD-10-006 | Low      | human   | human-validation | No       | Human validation of CLI workflow clarity is missing   | Even with technical correctness, unclear hook output can cause incorrect user decisions during commit flow.                                | Run PO validation on success/failure/no-op scenarios and record explicit sign-off for message clarity and remediation guidance.                                               |

<!-- review-findings:end -->
