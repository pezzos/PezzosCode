# Feature Specification: Update/reapply templates

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-03`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Reapply updated templates to an existing repo without clobbering local changes.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Existing repos stay in sync
- **Current pain:** reapply template updates safely is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** reapply template updates safely

**So that** repos stay current without losing local edits

### User Value

- **Value proposition:** Existing repos stay in sync
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P1 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Detect existing files and avoid destructive overwrites
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Existing repos stay in sync

- [ ] **Requirement 2:** Provide overwrite/merge/skip options
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Local changes diverge from template
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Partial reapply after failure
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

#### Workflow behavior steps, gates, and outputs

The documented workflow behavior steps, gates, and outputs ensure every CLI run surfaces the checks, confirmations, and results that keep template reapplications safe, walking through the preflight validation gate, template diff review gate, and conflict summary output whenever a decision or remediation point is needed.

#### Error Handling

| Scenario             | User Sees                | System Does | Recovery Path      |
| -------------------- | ------------------------ | ----------- | ------------------ |
| Unmergeable conflict | Clear conflict report    | Skip file   | Resolve manually   |
| Partial update       | Summary of applied files | Safe re-run | Re-run after fixes |

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
