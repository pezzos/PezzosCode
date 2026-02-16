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

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                           |
| ---------- | -------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| SEC-10-001 | High     | Unvalidated input can trigger data corruption or unsafe behavior.              | Add explicit validation rules, error paths, and anti-bypass tests in feature-spec and dev-tasks. |
| SEC-10-002 | High     | Access controls may be implemented inconsistently or omitted.                  | Specify authN/authZ requirements, denied-path behavior, and least-privilege checks.              |
| SEC-10-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios.        |
| SEC-10-005 | Medium   | Unsafe defaults can bypass intended runtime protections.                       | Capture required config defaults, permission boundaries, and misconfiguration failure behavior.  |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                                  |
| ----------- | -------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| PROD-10-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                                   |
| PROD-10-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Unified autofix for CI + precommit' journey and workflow. |
| PROD-10-004 | Medium   | Execution order and handoff expectations may be unclear for delivery.   | Define end-to-end workflow states, system responses, and handoff boundaries.                            |
| PROD-10-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.            |

<!-- review-findings:end -->
