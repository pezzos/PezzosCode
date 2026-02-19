# Feature Specification: Output offload enforcement

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-04`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Ensure large command outputs are offloaded to disk and referenced by id in prompts.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Noisy outputs stored in .offload/ and referenced by id
- **Current pain:** offload noisy outputs is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** offload noisy outputs

**So that** model context stays focused

### User Value

- **Value proposition:** Noisy outputs stored in .offload/ and referenced by id
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P0 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Wrap noisy commands with tools/offload-proxy/pp
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Noisy outputs stored in .offload/ and referenced by id

- [ ] **Requirement 2:** Store outputs in .offload/ with pointer id
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Output below threshold
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Offload directory missing
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

### Workflow Steps and Gates

The workflow steps make the noisy command handling behavior explicit: the CLI command is evaluated, an approval gate enumerates the required artifacts, and the offload id reference from the noisy output is attached to the next check-in. This creates a clear handoff at each gate so the user always knows which outputs have been offloaded, which approvals are needed, and how to resume the flow.

1. The user triggers the CLI command and the system notes the noisy command handling context before any long-running work starts.
2. An approval gate verifies the command, lists the expected artifacts, and refuses to continue until the noisy output is safely stored.
3. Once the output is offloaded, the offload id reference is logged, surfaced in prompts, and passed to the next gate so downstream steps can look up the exact artifacts they depend on.

#### Error Handling

| Scenario              | User Sees          | System Does   | Recovery Path     |
| --------------------- | ------------------ | ------------- | ----------------- |
| Offload write failure | Error message      | Exit non-zero | Check permissions |
| Pointer id missing    | Fallback to stdout | Continue      | Re-run with pp    |

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

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                           | Risk                                                                                                                                                                                                                                | Action                                                                                                                                                                                         |
| ---------- | -------- | ------- | -------------- | -------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-04-001 | High     | patcher | patch          | Yes      | Fail-open pointer-missing path exposes raw command output       | The feature spec error table states "Pointer id missing -> Fallback to stdout -> Continue". If offload fails, full noisy output can be emitted inline to prompts/logs, which can leak secrets and bypass the offload gate.          | Change pointer-missing handling to fail-closed for offload-eligible commands (non-zero exit), emit only minimal remediation metadata, and require explicit opt-in for any stdout fallback.     |
| SEC-04-002 | High     | patcher | patch          | Yes      | Offload artifacts lack confidentiality controls                 | The docs require writing `.offload/<id>.txt` and `logs/<WI>/<step>.log` but define no file permission, ignore-list, or retention controls. Sensitive command output may be readable by other local users or accidentally committed. | Enforce secure permissions (`0700` dirs, `0600` files), verify `.offload/` and sensitive logs are ignored by git templates, and add deterministic cleanup/retention handling.                  |
| SEC-04-003 | Medium   | patcher | patch          | Yes      | Pointer ID and path safety requirements are missing             | Requirement 2 defines pointer IDs but does not require strict ID validation or canonical path checks. Crafted IDs or symlinked offload directories can cause path traversal or writes outside the intended location.                | Generate IDs internally, validate against a strict allowlist, canonicalize target paths under `.offload`, reject symlinks/non-regular files, and use exclusive file creation.                  |
| SEC-04-004 | Medium   | patcher | automated-test | Yes      | Security regression tests are not required by current task plan | TASK-401 only targets primary-path coverage; it does not require tests for fail-closed behavior, permission enforcement, traversal/symlink rejection, or output-leak prevention.                                                    | Add automated tests for pointer-missing failure mode, missing-offload-dir recovery, path traversal/symlink attempts, and no-large-output-to-stdout guarantees; gate completion on these tests. |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                 | Risk                                                                                                                                                                                                             | Action                                                                                                                                                                                |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-04-001 | High     | patcher | patch            | Yes      | Fail-open pointer handling breaks user trust in offload enforcement   | Current behavior allows pointer-missing cases to continue with stdout fallback, which defeats the feature promise (token efficiency and consistent gated workflow) and can expose noisy/sensitive output inline. | Update spec and implementation to fail-closed by default when pointer generation fails, show concise remediation guidance, and allow stdout fallback only via explicit opt-in.        |
| PROD-04-002 | High     | patcher | patch            | Yes      | No deterministic definition of "noisy output" creates inconsistent UX | Users cannot predict when offload will trigger, so behavior may vary by command/run and reduce confidence in workflow gates.                                                                                     | Define and enforce explicit offload eligibility rules (e.g., size/line thresholds and command classes), document them in feature docs, and surface them in CLI preflight/status text. |
| PROD-04-003 | Medium   | patcher | automated-test   | Yes      | Recovery-path UX is underspecified and may stall users                | On write failure or missing `.offload/`, users may not know exact next steps or whether rerun is safe, increasing retry errors and abandoned runs.                                                               | Standardize blocking error messages to include immediate remediation and rerun-safety status; add tests that assert this copy is emitted for failure scenarios.                       |
| PROD-04-004 | Medium   | patcher | automated-test   | Yes      | Test plan does not guarantee end-user outcomes                        | Primary-path-only coverage can miss regressions where large output leaks inline, pointer IDs are absent, or edge behavior diverges from UX constraints.                                                          | Expand TASK-401 coverage to include pointer-missing failure mode, missing offload directory recovery, below-threshold behavior, and explicit no-large-output-to-stdout assertions.    |
| PROD-04-005 | Medium   | patcher | patch            | Yes      | Acceptance quality is not measurable                                  | Placeholder metrics and generic DoD criteria allow subjective completion without proving reduced workflow errors or token waste.                                                                                 | Replace placeholder success metric with concrete measurable targets and pass/fail thresholds tied to logs and automated checks.                                                       |
| PROD-04-006 | Medium   | human   | human-validation | Yes      | Human usability sign-off is required for pointer-first debugging flow | Even if technically correct, users may find pointer lookup and next-step handoff unclear and bypass the intended workflow.                                                                                       | Run human validation on one happy path and two failure paths to confirm pointer discoverability, clarity of next actions, and acceptable debug speed; record explicit PO sign-off.    |

<!-- review-findings:end -->
