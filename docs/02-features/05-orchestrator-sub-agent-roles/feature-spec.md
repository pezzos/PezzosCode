# Feature Specification: Orchestrator + sub-agent roles

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-05`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Define role responsibilities so parallel sessions stay scoped and coordinated.

Role responsibilities for the orchestrator and sub-agents are detailed below.

The orchestrator sequences the workflow through the Plan, Patch, Test, and Report gates, requiring each gate's artifact to be archived before releasing control to the next role.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Clear role separation and gates
- **Current pain:** define clear agent roles is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** define clear agent roles

**So that** work is parallel but predictable

### User Value

- **Value proposition:** Clear role separation and gates
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P1 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Define orchestrator, implementer, reviewer, tester roles
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Clear role separation and gates
- [ ] **Requirement 2:** Map role outputs to Plan/Patch/Test/Report gates
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

Sub-agent outputs include the implementer patch artifact, the tester pass/fail summary, and the reviewer recommendations, all documented for the orchestrator to verify.
These documented artifacts ensure the orchestrator can confirm readiness before advancing any gate.

Orchestrator Plan gate ensures preflight readiness, documents the patch plan, and hands off the task to the implementer.

#### Edge Cases

- [ ] **Edge Case 1:** Conflicting recommendations between roles
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Role skips a gate
  - **Expected behavior:** Fail safely and allow a clean retry

### User Experience Requirements

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

#### User Flow

```
CLI → Run command → Review output → Confirm next step
```

**Detailed Steps:**

1. User runs the relevant CLI command.
2. System executes the workflow step and logs output.
3. User reviews results and proceeds to the next gate.

#### Error Handling

| Scenario            | User Sees        | System Does | Recovery Path        |
| ------------------- | ---------------- | ----------- | -------------------- |
| Conflicting outputs | Conflict summary | Hold merge  | Orchestrator decides |
| Gate skipped        | Blocked status   | Stop        | Re-run required step |

### Non-Functional Requirements

- **Performance:** CLI commands complete within reasonable local dev time
- **Scalability:** Single-user workflow; no multi-user scaling needed
- **Security:** Local-only operations, no remote data transfer
- **Compatibility:** macOS-first, CLI-only

## Acceptance Criteria

### Definition of Done

- [ ] All core functionality works as specified
- [ ] Edge cases are handled appropriately
- [ ] Error states are user-friendly
- [ ] Documentation is complete
- [ ] Tests are passing
- [ ] Code is reviewed and merged

### Test Scenarios

#### Happy Path

1. **Scenario:** Execute the primary CLI flow
   - **Given:** Repo and dependencies are present
   - **When:** The command is executed
   - **Then:** Output is correct and logs are updated

#### Unhappy Path

1. **Scenario:** Required precondition is missing
   - **Given:** A dependency or approval is missing
   - **When:** The command runs
   - **Then:** Execution stops with a clear error

### Success Metrics

| Metric                | Target   | How Measured                  |
| --------------------- | -------- | ----------------------------- |
| {feature['outcome']}  | Achieved | Logs and user confirmation    |
| Fewer workflow errors | Reduced  | Error summaries               |
| Token waste           | Lower    | Offload ids and prompt review |

## Scope

### In Scope

- Implement the feature as described in the PRD
- Update process docs and templates as needed

### Out of Scope

- UI/TUI interfaces
- Cloud services

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Risk of inconsistent adoption without clear documentation
- Risk of skipping gates under time pressure
