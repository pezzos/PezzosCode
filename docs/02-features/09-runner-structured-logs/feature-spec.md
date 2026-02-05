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
