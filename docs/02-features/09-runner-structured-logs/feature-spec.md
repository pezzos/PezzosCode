# Feature Specification: Runner library + structured logs

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-09`

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Standardize tool execution with a shared runner and provide structured, tail-friendly logs for CI/tests/precommit/feature runs.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** consistent, low-token execution with traceable logs
- **Current pain:** inconsistent command invocation and hard-to-debug failures

### Why do they need it?

**As a** developer/PO

**I want to** a shared runner with standard metadata and logging helpers

**So that** deterministic execution and faster debugging

### User Value

- **Value proposition:** deterministic execution and faster debugging
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P0 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Provide a shared runner (`lib/pc_runner.*`) for Codex/Serena execution
- **Requirement 2:** Inject `work_item_id`, `agent_name`, and `run_id` into runs
- **Requirement 3:** Write structured logs to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix and timestamps

#### Edge Cases

- **Edge Case 1:** Logs directory missing or not writable
- **Edge Case 2:** Runner invoked without required metadata

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Runner invoked by tools/scripts without duplicated setup
- Logs exist for CI/tests/precommit/feature runs with required prefix

## Scope

### In Scope

- Runner library
- Structured log helpers
- Docs/process updates

### Out of Scope

- Cloud logging
- Daemonized logging

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Inconsistent adoption without updates to tools
- Log verbosity creep

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                           | Risk                                                                                                                                                                                                                       | Action                                                                                                                                                                                                               |
| ---------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-09-001 | High     | patcher | patch            | Yes      | Path traversal risk in `logs/<WI>/<step>.log` construction      | The feature requires metadata-driven log paths (`logs/<WI>/<step>.log`) but the provided docs do not define path sanitization. Malformed `work_item_id` or `step` values can escape `logs/` and overwrite arbitrary files. | In the runner/log helper, validate `work_item_id`, `agent_name`, `step`, and `run_id` against a strict allowlist (e.g., `[A-Za-z0-9._-]+`), resolve canonical paths, and hard-fail if the target is outside `logs/`. |
| SEC-09-002 | High     | patcher | patch            | Yes      | Log forging/injection via unescaped metadata fields             | Required prefix format (`[WI-...][agent][step]`) is vulnerable if metadata contains newlines/control characters; attackers can spoof entries, break parsers, or hide actions in tail/debug workflows.                      | Escape or reject control characters in all metadata fields and enforce one-event-per-line output (prefer JSONL with encoded fields). Add tests that inject newline/tab/ANSI characters and verify safe output.       |
| SEC-09-003 | Medium   | patcher | patch            | Yes      | Sensitive data exposure in structured command logs              | Feature scope logs CI/tests/precommit output, which often contains secrets or tokens. No redaction control is specified in feature docs, creating credential leakage risk in local/CI artifacts.                           | Implement output redaction before write (token/header/password patterns), add regression tests with synthetic secrets, and document a denylist/allowlist policy for logged fields.                                   |
| SEC-09-004 | Medium   | patcher | automated-test   | Yes      | Fail-open behavior for unwritable log directory is not enforced | Edge case `logs directory missing or not writable` is listed, but docs do not require fail-closed behavior. Execution may continue without audit logs, defeating traceability controls.                                    | Require non-zero exit when required step logs cannot be created/appended, and add automated tests for missing/unwritable `logs/<WI>` paths.                                                                          |
| SEC-09-005 | Medium   | human   | human-validation | Yes      | Security gate evidence incomplete before feature completion     | Execution log records `make ci` failure (permission error) while feature is marked Done. This leaves security-relevant checks unproven in the full gate path.                                                              | Resolve the permission issue and rerun full `make ci`; do not finalize feature status until the gate passes with evidence recorded in validation logs.                                                               |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                              | Risk                                                                                                                                                       | Action                                                                                                                                    |
| ----------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-09-001 | High     | human   | human-validation | Yes      | Feature marked Done without full gate evidence                     | make ci is recorded as failed while the feature is marked complete, so users cannot trust deterministic gate outcomes or final quality status.             | Resolve the permission blocker, rerun full make ci, and record passing evidence in validation logs before keeping status Done.            |
| PROD-09-002 | High     | patcher | patch            | Yes      | Traceability can fail open when logs are unavailable               | If required logs cannot be created/appended, execution may proceed without audit trails, breaking the core user promise of debuggable, deterministic runs. | Enforce fail-closed behavior for missing/unwritable log paths and emit clear remediation plus rerun-safety messaging.                     |
| PROD-09-003 | High     | patcher | patch            | Yes      | Structured log trust can be broken by unsafe metadata handling     | Unsanitized metadata can cause path traversal or forged log lines, making user-facing logs unreliable for debugging and review.                            | Validate metadata with a strict allowlist, enforce canonical paths under logs/, reject/escape control characters, and add negative tests. |
| PROD-09-004 | Medium   | patcher | patch            | Yes      | Sensitive output redaction is not guaranteed                       | CI/tests/precommit logs can capture secrets, creating end-user security and cleanup risk in local and CI artifacts.                                        | Implement redaction for sensitive patterns, add regression tests with synthetic secrets, and document the redaction policy/limits.        |
| PROD-09-005 | Medium   | patcher | automated-test   | Yes      | Acceptance evidence is incomplete across all required run surfaces | User expectations require logs for CI, tests, precommit, and feature runs; current validation evidence does not clearly prove all surfaces end-to-end.     | Add automated validation covering all required run types and record concrete log-path/prefix evidence in feature validation logs.         |

<!-- review-findings:end -->
