# Feature Specification: Update/reapply templates

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-03`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-16

### Summary

Reapply updated templates to an existing repo with deterministic overwrite in `--reapply` mode while preserving protected paths.

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

- [ ] **Requirement 1:** Detect existing files and preserve protected paths
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Existing repos stay in sync

- [ ] **Requirement 2:** `--reapply` overwrites syncable files without interactive prompts
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Local changes diverge from template
  - **Expected behavior:** Default mode remains conservative; `--reapply` force-overwrites syncable files and reports the action

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

| Scenario                 | User Sees                | System Does                       | Recovery Path      |
| ------------------------ | ------------------------ | --------------------------------- | ------------------ |
| Reapply overwrite action | Clear overwrite summary  | Overwrite syncable files in-place | Re-run if needed   |
| Partial update           | Summary of applied files | Safe re-run                       | Re-run after fixes |

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

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                                 | Risk                                                                                                                                                                                                                                | Action                                                                                                                                                                                     |
| ---------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEC-03-001 | High     | patcher | patch            | Yes      | Reapply write path is not constrained to repo root                    | The spec requires deterministic overwrite in `--reapply` mode but does not require canonical path checks. A crafted path (`../`) or symlinked target could cause writes outside the repository and overwrite arbitrary local files. | In patching, resolve each target with canonical path checks, reject path traversal, and fail closed on symlinked targets (or enforce a strict symlink policy) before any write.            |
| SEC-03-002 | High     | patcher | patch            | Yes      | Protected-path policy is underspecified for non-interactive overwrite | Requirement 1 says to preserve protected paths, but no concrete protected-path rules are defined while Requirement 2 enables promptless overwrite. Sensitive files can be overwritten if not explicitly guarded.                    | Implement an explicit protected-path policy (denylist/allowlist with precedence) and enforce it before overwrite decisions; include deterministic skip reporting for every protected file. |
| SEC-03-003 | Medium   | patcher | patch            | Yes      | Partial failure safety lacks atomic reapply controls                  | Edge Case 2 requires safe retry, but no atomic write/checkpoint mechanism is defined. Interrupted reapply can leave mixed template states that execute inconsistent or unsafe scripts.                                              | Use temp-file writes plus atomic rename, record resumable state, and ensure retries are idempotent and fail closed when state is inconsistent.                                             |
| SEC-03-004 | High     | patcher | automated-test   | Yes      | Security guardrail tests are missing from task plan                   | `TASK-401` only requires primary-path coverage; there are no required tests for traversal, symlink abuse, protected-path enforcement, or partial-failure recovery under `--reapply`.                                                | Add automated tests that must pass for: path traversal rejection, symlink boundary enforcement, protected-path non-overwrite, and safe retry after forced interruption.                    |
| SEC-03-005 | Low      | human   | human-validation | No       | Repo-specific secret path review is not explicitly required           | Default protected paths may miss repository-specific credential files, causing accidental overwrite in local environments.                                                                                                          | During human validation, review and approve the protected-path inventory for this repo and log the decision in `docs/03-logs`.                                                             |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                               | Risk                                                                                                                                                                                                                   | Action                                                                                                                                                                                      |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-03-001 | High     | patcher | patch            | Yes      | Reapply mode contract is ambiguous for end users    | The spec does not clearly define the exact CLI contract for default mode vs `--reapply` (what is overwritten, what is always skipped, and expected exit outcomes), creating a high risk of unintended destructive use. | Define and document deterministic mode semantics with concrete CLI examples: default conservative behavior, `--reapply` overwrite scope, protected-path precedence, and exit code meanings. |
| PROD-03-002 | High     | patcher | automated-test   | Yes      | User-visible acceptance quality is not testable yet | Current test scope is primary-path only; it does not prove user-facing guarantees for overwrite summaries, rerun safety, and deterministic outcomes, so regressions can ship unnoticed.                                | Expand automated tests to assert before/after file states, per-file applied/skipped reporting, idempotent reruns, and alignment with required security guardrail scenarios in `SEC-03-004`. |
| PROD-03-003 | Medium   | patcher | patch            | Yes      | Partial-failure recovery UX is underspecified       | Users are told retry is safe, but required failure output is not explicit; without clear remediation and rerun guidance, recovery becomes manual and error-prone.                                                      | Require deterministic failure output that includes: what was applied, what was skipped, why execution stopped, exact safe rerun command, and whether cleanup is required.                   |
| PROD-03-004 | Medium   | patcher | patch            | Yes      | Workflow gate behavior conflicts are unresolved     | The UX blueprint references review/conflict gates while `--reapply` is non-interactive; without explicit per-mode gate behavior, implementation will drift and confuse users.                                          | Specify gate behavior by mode: interactive/default path vs non-interactive `--reapply`, with mandatory conflict/overwrite summaries in output when prompts are suppressed.                  |
| PROD-03-005 | Low      | human   | human-validation | No       | Repo-specific protected-path sign-off is missing    | Even with defaults, repository-specific critical files may be missed, leaving residual overwrite risk in local environments.                                                                                           | PO/end-user must review and approve the protected-path inventory and exceptions, then record the decision in `docs/03-logs` before final sign-off.                                          |

<!-- review-findings:end -->
