# Feature Specification: Bootstrap templates into a repo

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-01`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Copy the PezzosCode docs/tools/templates into a target repo in one command with safe re-runs.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Project is ready for AI workflow
- **Current pain:** bootstrap a repo in one command is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** bootstrap a repo in one command

**So that** I can start the AI workflow immediately

### User Value

- **Value proposition:** Project is ready for AI workflow
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P0 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Copy docs/templates/tools into the target repo
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Project is ready for AI workflow

- [ ] **Requirement 2:** Handle existing files via overwrite/merge/skip
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Target repo already has conflicting files
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Target path is not a git repo
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

| Scenario             | User Sees           | System Does        | Recovery Path               |
| -------------------- | ------------------- | ------------------ | --------------------------- |
| Missing dependencies | Clear error         | Abort bootstrap    | Install required tools      |
| Conflicting files    | Prompt with options | Pause for decision | Choose overwrite/merge/skip |

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

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                    | Risk                                                                                                                                                                                                      | Action                                                                                                                                                                         |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEC-01-001 | High     | patcher | patch          | Yes      | Missing repo-boundary and symlink escape controls        | The feature requires copying into a target repo, but the spec does not define canonical path or symlink checks. A crafted path/symlink can cause writes outside the repo root.                            | Resolve target/destination with canonical paths, reject any write that escapes repo root after resolution, and block writes through symlinked paths with a fail-closed error.  |
| SEC-01-002 | High     | patcher | patch          | Yes      | No protected-path policy for overwrite/merge/skip        | Conflict handling is defined as overwrite/merge/skip, but no restricted path set is defined. Security-critical files (e.g., `.git/**`, secret env files, hooks, CI security config) could be overwritten. | Implement protected path rules: hard-deny `.git/**`, default-skip sensitive patterns, and require explicit opt-in with deterministic confirmation for any protected overwrite. |
| SEC-01-003 | Medium   | patcher | patch          | Yes      | Local-only security requirement is not enforced          | The spec states local-only/no remote transfer, but no technical control is defined to prevent network egress during bootstrap.                                                                            | Enforce offline behavior by default (no network subprocesses), require explicit flag for any remote source, and log source provenance in run output.                           |
| SEC-01-004 | Medium   | patcher | patch          | Yes      | Permission and executable-bit hardening is unspecified   | Copy/merge behavior does not define safe permission handling; unsafe executable bits or special mode bits could be propagated into the target repo.                                                       | Normalize file modes on write, allow executable bit only for approved script paths, and strip suid/sgid bits.                                                                  |
| SEC-01-005 | Medium   | patcher | automated-test | Yes      | Security regression coverage is absent in test scenarios | Current tests are generic and do not validate traversal/symlink escapes, protected-path overwrite blocking, offline enforcement, or permission hardening, leaving controls vulnerable to regression.      | Add negative automated tests for all mandatory controls and make them required in the feature test gate.                                                                       |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                        | Risk                                                                                                                                                                 | Action                                                                                                                                                                                                           |
| ----------- | -------- | ------- | ---------------- | -------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-01-001 | High     | patcher | patch            | Yes      | CLI contract is not explicit enough for users to execute confidently         | The spec uses placeholders like "relevant CLI command/step," so users cannot reliably know what to run, what output means success, or what constitutes a safe rerun. | Define the exact command(s), required/optional flags, exit code behavior, and deterministic summary fields (applied/merged/skipped/conflicts, rerun status, log path).                                           |
| PROD-01-002 | High     | patcher | automated-test   | Yes      | Core promise of safe re-runs is not acceptance-tested                        | Without explicit automated idempotency checks, users can see inconsistent outcomes on second run and lose trust in bootstrap safety.                                 | Add automated tests for first-run and rerun behavior across clean and conflicted repos; assert deterministic no-op/expected changes and user-facing rerun summary output.                                        |
| PROD-01-003 | High     | patcher | patch            | Yes      | Conflict handling UX is under-specified for destructive choices              | Overwrite/merge/skip is named but decision safety is unclear, increasing accidental destructive outcomes under time pressure.                                        | Specify deterministic prompt copy with safe default, preview impacted files before apply, explicit confirmation for destructive paths, and cancel/retry guidance aligned with SEC-01 protected-path constraints. |
| PROD-01-004 | Medium   | patcher | patch            | Yes      | Recovery contract for failure states is incomplete                           | For missing dependencies or non-git targets, users may not know if partial state exists or whether rerun is safe, causing workflow stalls.                           | Require fail-closed preflight checks before writes and standardize blocking error messages to include remediation and explicit rerun-safety status.                                                              |
| PROD-01-005 | Medium   | patcher | patch            | Yes      | Acceptance quality is weakened by unresolved template and subjective metrics | The `{feature['outcome']}` placeholder and "user confirmation" measurement make completion criteria ambiguous and prone to premature sign-off.                       | Replace placeholders with measurable targets and map each acceptance criterion to concrete automated-test or human-validation evidence.                                                                          |
| PROD-01-006 | Medium   | human   | human-validation | Yes      | No explicit human validation gate for end-user clarity                       | Automated checks alone will not confirm that a Developer/PO can interpret prompts and next steps correctly in realistic repos.                                       | Run human validation on at least: clean repo bootstrap, conflicted repo choice flow, and non-git path failure; require explicit PO sign-off.                                                                     |

<!-- review-findings:end -->
