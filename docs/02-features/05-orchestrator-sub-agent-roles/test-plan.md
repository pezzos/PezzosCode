# Test Plan: Orchestrator + sub-agent roles

> **Validation strategy**
>
> Comprehensive testing approach to ensure feature quality, reliability, and correctness.

---

## Overview

**Feature:** Orchestrator + sub-agent roles

**Status:** Draft

**Last Updated:** 2026-02-02

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

### Test Objectives

- Verify functional requirements are met
- Ensure edge cases are handled safely
- Confirm output and logs are correct

### Test Scope

**In Scope:**

- CLI behavior for this feature
- Docs/log updates

**Out of Scope:**

- UI/TUI behaviors
- Cloud services

## Test Strategy

### Test Levels

#### Unit Tests

- **Purpose:** Validate helper functions and small logic
- **Coverage Target:** Focused on changed modules
- **Tools:** pytest/unittest (project standard)
- **Responsibility:** Developers

#### Integration Tests

- **Purpose:** Validate CLI workflow boundaries
- **Coverage Target:** Command-level behavior
- **Tools:** shell scripts or python tests
- **Responsibility:** Developers

#### CLI Tests

- **Purpose:** Validate command behavior, exit codes, and output
- **Coverage Target:** All commands and flags touched
- **Tools:** Shell scripts, snapshot testing
- **Responsibility:** Developers

## Test Cases

### Functional Tests

- **TC-F001:** Primary CLI flow succeeds
- **TC-F002:** Output/logs are created with expected content
- **TC-F003:** Gates enforce required approvals/DoD

### Edge Cases

- **TC-E001:** Missing dependency or precondition
- **TC-E002:** Conflict or existing state handled safely

### Anti-Hardcode Checks (if applicable)

- Multiple fixtures for key behaviors
- Seeded randomness where used
- Invariants verified instead of fixed outputs

### Workflow & Role Gate Tests

- **TC-WF001:** Orchestrator Plan gate enforcement
  - Verify the orchestrator command produces the documented workflow steps, records the Plan/Patch/Test/Report gate states, and emits the expected handoff artifact (e.g., a manifest or worklog update) before releasing control to a sub-agent.
- **TC-WF002:** Sub-agent input gate validation
  - Run the sub-agent command without the orchestrator artifact/gate record and verify it fails fast with a clear error referencing the missing gate, then rerun with the artifact present to ensure the gate is marked satisfied and execution continues.
- **TC-WF003:** Role output traceability
  - Confirm each role writes its expected outputs (summary, gate log, or artifact) to the docs/logs targets defined in the feature spec so auditors can trace the workflow from Plan through Report.
- TC-WF004: Gate artifact audit ensures the orchestrator inspects each sub-agent artifact before approving the next gate.

## Exit Criteria

- All tests pass
- Manual spot-check completed
- Logs updated
