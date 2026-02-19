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

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                            | Risk                                                                                                                                                                                                                                                                  | Action                                                                                                                                                                                     |
| ---------- | -------- | ------- | -------------- | -------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEC-05-001 | High     | patcher | patch          | Yes      | Gate artifacts are not integrity-protected                       | The spec requires Plan/Patch/Test/Report artifacts to be archived before gate transitions, but it does not require checksums/signatures. A compromised or buggy sub-agent could alter evidence after generation and the orchestrator could advance on forged results. | Add a per-run artifact manifest (run_id, role, timestamp, SHA-256 for each artifact) and verify it at every gate transition; fail closed on any mismatch.                                  |
| SEC-05-002 | High     | patcher | patch          | Yes      | Role boundaries are defined but not enforceably sandboxed        | Docs describe role separation and role-scoped outputs, but no technical control is specified to prevent cross-role file writes (for example, patcher modifying reviewer/tester artifacts). This enables privilege escalation inside the workflow.                     | Enforce role-based path allowlists/denylists in the orchestrator runner and reject out-of-scope writes with explicit errors.                                                               |
| SEC-05-003 | High     | patcher | patch          | Yes      | HIGH-risk approval gate can be bypassed in non-interactive flows | The UX requires an explicit `y/n` approval and `Awaiting PO Approval`, but no control is defined to ensure approval is interactive and tied to the current run. Piped input or automation could unintentionally approve blocked work.                                 | Require interactive TTY for HIGH-risk approval, bind approval to current run_id, and persist an approval audit record before unblocking.                                                   |
| SEC-05-004 | High     | patcher | automated-test | Yes      | Offload/log pipeline lacks secret redaction requirements         | Journey C mandates offloading noisy command output to `.offload/<id>.txt` and structured logs, but no masking policy is defined. Tokens, credentials, or private env values may be persisted in plaintext artifacts.                                                  | Implement output scrubbing before write (credential/token patterns and configured secret keys), and add regression tests that fail when known secret fixtures appear in offload/log files. |
| SEC-05-005 | Medium   | patcher | patch          | Yes      | Artifact file permissions are unspecified                        | The feature is local-only, but no requirement sets restrictive permissions for `.offload` and `logs/` artifacts. On shared machines, other local users could read sensitive workflow data.                                                                            | Create artifact directories/files with least-privilege permissions (`0700` dirs, `0600` files) and add automated checks for permission mode on creation.                                   |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                   | Risk                                                                                                                                                                                            | Action                                                                                                                                                                                                     |
| ----------- | -------- | ------- | ---------------- | -------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-05-001 | High     | patcher | patch            | Yes      | Gate UX contract is underspecified for end users                        | The feature does not define deterministic CLI outputs per gate/role, so users may not know current stage, required artifact, or exact next action, increasing skipped-gate and recovery errors. | Define and implement a strict CLI message contract for each Plan/Patch/Test/Report transition and failure state, including role, stage, artifact pointer, and explicit remediation; add output assertions. |
| PROD-05-002 | High     | patcher | automated-test   | Yes      | Acceptance tests do not cover critical workflow failure loops           | Current scenarios miss conflict resolution, gate-skip prevention, reviewer/tester failure loopbacks, and resume behavior, so regressions can ship while the workflow appears nominal.           | Add automated tests for conflicting-role outputs, skipped-gate fail-safe behavior, loopback-to-planner routing, and interrupted-run resume semantics with pass/fail expectations.                          |
| PROD-05-003 | High     | human   | human-validation | Yes      | Human decision points are not explicitly captured as sign-off artifacts | Conflict adjudication and HIGH-risk approvals can be treated as implicit decisions, weakening PO control and creating user-trust and accountability gaps.                                       | Require human validation artifacts for PO decisions (run_id, decision, rationale, timestamp) and make completion contingent on that record.                                                                |
| PROD-05-004 | Medium   | patcher | patch            | Yes      | Blocked-state recovery guidance is too vague                            | Messages like 're-run required step' without prerequisite identifiers or next eligible action create repeated failed attempts and avoidable user friction.                                      | Update blocked/error UX to include missing prerequisite slugs, next valid command/action, and rerun-safety guidance; verify in tests.                                                                      |
| PROD-05-005 | Medium   | patcher | patch            | No       | Success metrics are not measurable                                      | A placeholder metric and non-quantified targets prevent objective validation that user pain (workflow failures/confusion) was reduced.                                                          | Replace placeholder metrics with measurable thresholds and evidence sources in feature docs and validation logs.                                                                                           |

<!-- review-findings:end -->
