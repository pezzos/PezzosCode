# Feature Specification: Execute ticket workflow

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-02`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Run the canonical ticket flow with gates, TDD, and logging to keep execution consistent.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** AI can implement approved tasks reliably
- **Current pain:** execute tickets end-to-end is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** execute tickets end-to-end

**So that** I get reliable, logged changes

### User Value

- **Value proposition:** AI can implement approved tasks reliably
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P0 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Enforce Plan → Patch → Test → Report
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** AI can implement approved tasks reliably

- [ ] **Requirement 2:** Require ticket-specific DoD before coding
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** HIGH risk ticket without approval
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Tests fail after patch
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

| Scenario                   | User Sees           | System Does      | Recovery Path       |
| -------------------------- | ------------------- | ---------------- | ------------------- |
| HIGH risk without approval | Blocked with prompt | Stop execution   | Grant approval      |
| Test failure               | Fail with summary   | Stop after tests | Fix code and re-run |

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

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                             | Risk                                                                                                                                                                                        | Action                                                                                                                                                                                                                                         |
| ---------- | -------- | ------- | -------------- | -------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-02-001 | High     | patcher | patch          | Yes      | HIGH-risk approval gate is not identity-bound                     | The UX requires a simple `y/n` approval prompt for HIGH-risk work, but no control ties approval to a human PO identity; an automated actor could self-approve and bypass the intended gate. | Require interactive TTY approval with an explicit typed confirmation containing the ticket ID, record approver OS user + timestamp in run metadata, and fail closed in non-interactive contexts. Add tests for missing/invalid approval paths. |
| SEC-02-002 | High     | patcher | patch          | Yes      | Offload/log artifacts lack secret redaction controls              | Workflow output is written to `.offload/<id>.txt` and `logs/<WI>/<step>.log` with no stated scrubbing, so credentials/tokens printed by tools or tests can be persisted and exposed.        | Implement pre-write redaction for common secret patterns and configured project patterns, suppress raw secret-bearing env output, and add regression tests asserting masking behavior.                                                         |
| SEC-02-003 | High     | patcher | patch          | Yes      | Dynamic log path inputs are not constrained against traversal     | The design uses dynamic path parts like `<WI>` and `<step>` but defines no validation/canonicalization, enabling path traversal or overwrite outside approved logging roots.                | Enforce strict allowlist regex for IDs/step names, canonicalize and verify resolved paths remain under approved directories, and reject `..`, absolute paths, and separator variants. Add negative-path tests.                                 |
| SEC-02-004 | High     | patcher | patch          | Yes      | Workflow execution lacks explicit command allowlisting            | Requirements say to run the relevant CLI/tooling step but do not define allowed commands/args, creating risk of unintended or injected command execution during role handoffs.              | Define per-stage command allowlists and argument schemas, execute via structured argv (no shell interpolation), and fail closed on unknown commands. Add tests proving denied commands are blocked.                                            |
| SEC-02-005 | Medium   | patcher | automated-test | No       | Permissions for local security-relevant artifacts are unspecified | Local-only operation does not prevent data exposure if `.offload`/`logs` files are created with permissive defaults on shared hosts.                                                        | Create artifact directories/files with restrictive permissions (`0700`/`0600`) and add automated checks to enforce expected modes on macOS.                                                                                                    |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                | Risk                                                                                                                                                                                                                                    | Action                                                                                                                                                                            |
| ----------- | -------- | ------- | ---------------- | -------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-02-001 | High     | patcher | patch            | Yes      | Gate behavior is not specified as a deterministic user contract      | Core requirements and tests are too generic ('perform workflow action'), so different implementations can pass while producing inconsistent CLI behavior, reducing user trust and making failures hard to recover.                      | Define explicit, testable output/state requirements for each gate (Plan, Patch, Test, Report), including required status labels, offload/log pointers, and remediation messaging. |
| PROD-02-002 | High     | patcher | patch            | Yes      | Approval UX conflicts with security-required HIGH-risk approval flow | UX constraints require a simple 'y/n' approval prompt while security requires typed ticket confirmation with identity/timestamp (SEC-02-001). This conflict will create rework and unclear user expectations at the most critical gate. | Reconcile specs to one canonical HIGH-risk approval interaction aligned with SEC-02-001, then update tests and user-facing copy accordingly.                                      |
| PROD-02-003 | High     | patcher | automated-test   | Yes      | Retry/resume acceptance quality is underspecified                    | Feature says failures should allow a clean retry, but no automated assertions define what must be preserved, reset, or re-run. Users can face partial-state confusion and inconsistent rerun outcomes.                                  | Add automated tests for fail-safe rerun behavior, including state integrity after failed tests and required summary markers (resumed/skipped/repaired/newly executed).            |
| PROD-02-004 | Medium   | human   | human-validation | Yes      | No explicit end-user sign-off gate for blocking prompt clarity       | Technical implementation may pass while the Developer/PO still finds blocking prompts and recovery instructions ambiguous, leading to workflow stalls or incorrect actions.                                                             | Require PO human validation of blocking UX copy across happy/unhappy paths (HIGH-risk approval, missing preconditions, test failure, retry guidance) before completion.           |
| PROD-02-005 | Medium   | patcher | patch            | No       | Success metrics are not measurable                                   | A placeholder metric remains (`{feature['outcome']}`), so user value cannot be objectively verified and acceptance may become subjective.                                                                                               | Replace placeholder metrics with concrete targets and measurement method tied to logs/offload artifacts.                                                                          |

<!-- review-findings:end -->
