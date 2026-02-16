# Feature Specification: Runner library + structured logs

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-09`

**Status:** Draft

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

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                          |
| ---------- | -------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| SEC-09-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios.       |
| SEC-09-005 | Medium   | Unsafe defaults can bypass intended runtime protections.                       | Capture required config defaults, permission boundaries, and misconfiguration failure behavior. |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                                |
| ----------- | -------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| PROD-09-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                                 |
| PROD-09-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Runner library + structured logs' journey and workflow. |
| PROD-09-004 | Medium   | Execution order and handoff expectations may be unclear for delivery.   | Define end-to-end workflow states, system responses, and handoff boundaries.                          |
| PROD-09-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.          |

<!-- review-findings:end -->
