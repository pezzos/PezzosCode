# Feature Specification: Anti-cheat testing strategy

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-08`

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Require tests that prevent hardcoded responses and validate behavior.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Tests validate behavior through fixtures/invariants/contracts
- **Current pain:** apply anti-cheat test rules is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** apply anti-cheat test rules

**So that** behavior is real and not hardcoded

### User Value

- **Value proposition:** Tests validate behavior through fixtures/invariants/contracts
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P1 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [x] **Requirement 1:** Multiple fixtures per critical path
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Tests validate behavior through fixtures/invariants/contracts

- [x] **Requirement 2:** Seeded randomness and invariants
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [x] **Edge Case 1:** Single fixture passes a hardcoded implementation
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [x] **Edge Case 2:** Unseeded randomness causes flaky tests
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

| Scenario          | User Sees      | System Does   | Recovery Path      |
| ----------------- | -------------- | ------------- | ------------------ |
| Flaky tests       | Fail with seed | Stop test run | Re-run with seed   |
| Hardcoded outputs | Test failure   | Stop pipeline | Fix implementation |

### Non-Functional Requirements

- **Performance:** CLI commands complete within reasonable local dev time
- **Scalability:** Single-user workflow; no multi-user scaling needed
- **Security:** Local-only operations, no remote data transfer
- **Compatibility:** macOS-first, CLI-only

## Acceptance Criteria

### Definition of Done

- [x] All core functionality works as specified
- [x] Edge cases are handled appropriately
- [x] Error states are user-friendly
- [x] Documentation is complete
- [x] Tests are passing
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

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                               | Risk                                                                                                                                                                                            | Action                                                                                                                                  |
| ---------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-08-001 | High     | patcher | automated-test   | Yes      | Final fail-closed CI gate was skipped                               | In WI-20260205-02, `make ci` is explicitly marked as not run while outcome is pass/complete. This leaves anti-cheat controls and integration checks unverified and allows fail-open completion. | Require `make ci` evidence before feature completion and fail closed when the command is missing or failing.                            |
| SEC-08-002 | High     | patcher | patch            | Yes      | Restored `pc-ticket` stub creates potential gate-bypass path        | Patch notes state `pc-ticket` was restored as a stub; if this path does not strictly delegate to hardened anti-cheat checks, users can bypass enforcement in `pc-feature`/allowed-tests flow.   | Make `pc-ticket` either hard-fail with migration guidance or delegate to the exact same validated gate path with explicit proof output. |
| SEC-08-003 | Medium   | patcher | automated-test   | Yes      | Current anti-cheat spec can still be beaten by fixture memorization | The feature requires multiple fixtures, but provided docs do not require fixture mutation/generation. A hardcoded implementation can still pass by memorizing known fixture sets.               | Add invariant/metamorphic or generated-fixture tests for each critical path and require at least one non-static fixture source in CI.   |
| SEC-08-004 | Medium   | patcher | automated-test   | Yes      | Local-only security claim is not enforced by tests                  | Spec says local-only with no remote transfer, but test evidence shown does not include a network-egress denial check. Outbound calls could leak data or fetch answers.                          | Add automated tests that block/monitor outbound network access during anti-cheat workflows and fail on any egress.                      |
| SEC-08-005 | Low      | human   | human-validation | Yes      | Human security review gate is incomplete                            | DoD shows `Code is reviewed and merged` unchecked while feature status is Complete, creating a security sign-off gap for gate logic changes.                                                    | Require explicit human security/PO validation of anti-cheat gate behavior before marking feature complete.                              |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                  | Risk                                                                                                                                                             | Action                                                                                                                                            |
| ----------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-08-001 | High     | patcher | automated-test   | Yes      | Completion can be marked without final CI proof        | WI-20260205-02 shows outcome pass/complete while `make ci` was not run, so users can receive a 'done' signal without full anti-cheat and integration validation. | Enforce a fail-closed completion gate: require recorded `make ci` pass evidence before status can be set to Complete.                             |
| PROD-08-002 | High     | patcher | patch            | Yes      | `pc-ticket` restoration creates user path ambiguity    | Restoring `pc-ticket` as a stub can let users follow a weaker or unclear execution path, reducing confidence that anti-cheat gates were actually applied.        | Either hard-fail `pc-ticket` with migration guidance or force strict delegation to the exact validated gate path with equivalent evidence output. |
| PROD-08-003 | Medium   | patcher | automated-test   | Yes      | Current anti-cheat acceptance can still be gamed       | Multiple static fixtures and invariants alone may still allow memorized/hardcoded behavior to pass, weakening user trust in test quality.                        | Add generated or mutated fixture coverage plus metamorphic/invariant checks per critical path and require them in CI.                             |
| PROD-08-004 | Medium   | patcher | automated-test   | Yes      | Local-only promise is not enforced in automated checks | Without outbound network denial/monitoring tests, workflows may accidentally call remote services, violating local-only expectations and reproducibility.        | Add automated anti-egress checks for anti-cheat workflows and fail tests on any outbound network attempt.                                         |
| PROD-08-005 | Low      | human   | human-validation | Yes      | Human sign-off gate is incomplete                      | Feature is marked Complete while DoD item 'Code is reviewed and merged' remains unchecked, leaving product acceptance accountability unresolved.                 | Route final PO/security review through human validation and require explicit sign-off before completion status is retained.                       |
| PROD-08-006 | Low      | patcher | patch            | No       | Success metrics are partially non-actionable           | The metric table still contains a placeholder (`{feature['outcome']}`), so users cannot verify outcome quality consistently across runs.                         | Replace placeholders with explicit measurable outcomes and map each to a concrete validation artifact.                                            |

<!-- review-findings:end -->
